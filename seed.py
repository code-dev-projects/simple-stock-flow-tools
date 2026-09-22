"""Fills an empty system with a catalogue worth looking at.

Everything goes in through the HTTP API, never through SQL, so the seed data obeys the same
rules as anything a person types: a price that breaks an invariant fails here exactly as it
would fail on screen. The one exception is the instant of each sale, which the domain stamps
with the current time -- see `spread_sales_over_time`.

Reads the administrator's credentials from the infrastructure .env and never prints them.
That .env and the compose files live in a separate repository, so their location is a
command-line argument whose default is resolved against this file instead of the working
directory: the script then runs from anywhere as long as both checkouts sit side by side.
"""

import argparse
import datetime as dt
import pathlib
import subprocess
import sys
import unicodedata

import requests

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from catalogue import CATEGORIES, PRODUCTS  # noqa: E402

HERE = pathlib.Path(__file__).parent
IMG = HERE / "img"
DEFAULT_INFRA = HERE.parent / "simple-stock-flow-infra"
API = "http://localhost:5000"
SELLER = "vendedor.demo"

# Who sells what, and how much. Kept here rather than generated so the report always tells the
# same story: a couple of clear best-sellers and a long tail.
SALES = [
    (0,  "admin",  [("Martillo de carpintero 16 oz", 2), ("Flexómetro 5 m", 1)]),
    (1,  "seller", [("Bombilla LED 9 W luz cálida", 12)]),
    (2,  "seller", [("Cable encauchetado 3x14, por metro", 25), ("Interruptor doble para empotrar", 3)]),
    (4,  "admin",  [("Taladro percutor 650 W", 1)]),
    (5,  "seller", [("Vinilo tipo 1 blanco, galón", 2), ("Rodillo de felpa 9\" con mango", 1),
                    ("Brocha 3\" de cerda natural", 2)]),
    (7,  "seller", [("Cinta de teflón 12 m", 6), ("Tubo PVC presión 1/2\" x 6 m", 2)]),
    (8,  "admin",  [("Guantes de carnaza talla M", 4)]),
    (10, "seller", [("Bombilla LED 9 W luz cálida", 20)]),
    (11, "seller", [("Llave inglesa ajustable 10\"", 1), ("Alicate universal 8\"", 1)]),
    (13, "admin",  [("Escalera tijera 5 pasos en aluminio", 1)]),
    (14, "seller", [("Cable encauchetado 3x14, por metro", 40)]),
    (16, "seller", [("Grifo para lavamanos cromado", 1), ("Llave de paso en bronce 1/2\"", 2)]),
    (17, "admin",  [("Juego de destornilladores 6 piezas", 2)]),
    (19, "seller", [("Bombilla LED 9 W luz cálida", 8), ("Extensión múltiple 6 tomas", 1)]),
    (20, "seller", [("Esmalte sintético negro 1/4", 3), ("Brocha 3\" de cerda natural", 1)]),
    (21, "admin",  [("Candado de seguridad 50 mm", 2), ("Multímetro digital", 1)]),
    (23, "seller", [("Flexómetro 5 m", 3)]),
    (24, "seller", [("Martillo de carpintero 16 oz", 1), ("Guantes de carnaza talla M", 2)]),
]


def slug(name):
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    keep = [c.lower() if c.isalnum() else "-" for c in plain]
    return "-".join(filter(None, "".join(keep).split("-")))[:48]


def env(infra):
    settings = infra / ".env"
    if not settings.is_file():
        raise SystemExit(
            f"No .env under {infra}\n"
            "Point at the infrastructure checkout with --infra <path>")
    values = {}
    for line in settings.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
    return values


def login(username, password):
    answer = requests.post(f"{API}/api/auth/login",
                           json={"username": username, "password": password}, timeout=30)
    answer.raise_for_status()
    return answer.json()["accessToken"]


def compose_command(infra):
    """Absolute -f paths rather than a working directory, so that the command this script runs
    and the one `refuse_if_occupied` prints are the same string and cannot drift apart."""
    return ["docker", "compose",
            "-f", str(infra / "docker-compose.yml"),
            "-f", str(infra / "docker-compose.dev.yml")]


def psql(sql, infra):
    return subprocess.run(
        compose_command(infra) + [
            "exec", "-T", "db", "psql", "-U", "simple_stock_flow", "-d", "simple_stock_flow",
            "-v", "ON_ERROR_STOP=1", "-c", sql],
        check=True, capture_output=True, text=True).stdout


def create_products(token):
    head = {"Authorization": f"Bearer {token}"}
    ids = {}

    for name, price, stock, category, _ in PRODUCTS:
        created = requests.post(f"{API}/api/products", headers=head, timeout=30, json={
            "name": name, "price": price, "stock": stock,
            "categoryId": CATEGORIES[category],
        })
        created.raise_for_status()
        ids[name] = created.json()["id"]

        picture = IMG / f"{slug(name)}.png"
        with picture.open("rb") as handle:
            uploaded = requests.post(
                f"{API}/api/products/{ids[name]}/image", headers=head, timeout=60,
                files={"file": (picture.name, handle, "image/png")})
        uploaded.raise_for_status()

    return ids


def create_seller(token, password):
    answer = requests.post(f"{API}/api/auth/register", timeout=30,
                           headers={"Authorization": f"Bearer {token}"},
                           json={"username": SELLER, "password": password, "role": "seller"})
    if answer.status_code not in (200, 201):
        raise SystemExit(f"register -> {answer.status_code} {answer.text[:200]}")


def place_sales(tokens, ids):
    placed = []
    for day, who, lines in SALES:
        answer = requests.post(f"{API}/api/sales", timeout=30,
                               headers={"Authorization": f"Bearer {tokens[who]}"},
                               json={"lines": [{"productId": ids[n], "quantity": q}
                                               for n, q in lines]})
        if answer.status_code not in (200, 201):
            raise SystemExit(f"sale day {day} -> {answer.status_code} {answer.text[:300]}")
        placed.append((answer.json()["id"], day))
    return placed


def spread_sales_over_time(placed, today, infra):
    """The only thing SQL touches, and only because it cannot be done any other way.

    A sale is stamped with the instant it is registered, which is correct and is exactly what
    a person would want -- but it means a freshly seeded system has every sale inside the same
    minute, and the report by date range has nothing to show. Each sale is moved back to its
    own day, at a plausible hour of the working day.
    """
    cases = []
    for index, (sale_id, day) in enumerate(placed):
        when = today - dt.timedelta(days=day)
        hour, minute = 9 + (index * 3) % 9, (index * 17) % 60
        stamp = when.replace(hour=hour, minute=minute, second=0, microsecond=0)
        cases.append(f"when '{sale_id}' then timestamptz '{stamp.isoformat()}'")

    psql("update sales.sale set sold_at = case id::text " + " ".join(cases) + " end;", infra)


def refuse_if_occupied(token, infra):
    """Running twice would duplicate every product and leave the report double-counting.

    Names are not unique in the catalogue, so nothing downstream would complain: the mess
    would only show up on screen, which is the one place nobody looks first.
    """
    answer = requests.get(f"{API}/api/products", timeout=30,
                          headers={"Authorization": f"Bearer {token}"})
    answer.raise_for_status()
    total = answer.json()["total"]
    if total:
        # One line, and the SQL quotes the role with PostgreSQL dollar quoting instead of the
        # single quotes it used before. Doubled single quotes inside a single-quoted shell
        # argument close the quote and reopen it, so the printed command could not be pasted
        # anywhere. The backslash continuations are gone for the same reason: this message
        # also prints on a Windows console, where they are not a continuation at all.
        reset = " ".join(compose_command(infra)) + (
            " exec -T db psql -U simple_stock_flow -d simple_stock_flow -c "
            "'delete from sales.sale_item; delete from sales.sale; delete from sales.product; "
            "delete from sales.\"user\" where role <> $$admin$$;'")
        raise SystemExit(
            f"The catalogue already holds {total} products and this seeder only fills an "
            "empty one.\n"
            "To start over, empty the tables and keep the categories and the administrator:\n"
            f"  {reset}")


def main():
    parser = argparse.ArgumentParser(description="Seeds the demonstration catalogue.")
    parser.add_argument(
        "--infra", type=pathlib.Path, default=DEFAULT_INFRA,
        help="checkout of simple-stock-flow-infra, which holds .env and the compose files "
             f"(default: {DEFAULT_INFRA})")
    infra = parser.parse_args().infra.resolve()

    settings = env(infra)
    admin_token = login(settings["ADMIN_USERNAME"], settings["ADMIN_PASSWORD"])
    refuse_if_occupied(admin_token, infra)

    seller_password = settings.get("DEMO_SELLER_PASSWORD")
    if not seller_password:
        raise SystemExit(f"DEMO_SELLER_PASSWORD is missing from {infra / '.env'}")

    print(f"creating {len(PRODUCTS)} products with their pictures…")
    ids = create_products(admin_token)

    print(f"creating the demonstration seller {SELLER}…")
    create_seller(admin_token, seller_password)

    tokens = {"admin": admin_token, "seller": login(SELLER, seller_password)}

    print(f"placing {len(SALES)} sales…")
    placed = place_sales(tokens, ids)

    today = dt.datetime.now(dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=-5)))
    spread_sales_over_time(placed, today, infra)

    print(f"done: {len(ids)} products, {len(placed)} sales over the last "
          f"{max(d for _, d in placed)} days")


if __name__ == "__main__":
    main()
