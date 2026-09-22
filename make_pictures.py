"""Draws one picture per catalogue item.

Chrome renders every tile in a single grid so there is one browser launch instead of
twenty-two, and Pillow then cuts the grid into files. The tiles are laid out with no gap
and a fixed size, which is what makes the cut arithmetic exact rather than approximate.
"""

import pathlib
import subprocess
import sys
import unicodedata

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from catalogue import ICONS, PALETTE, PRODUCTS  # noqa: E402

HERE = pathlib.Path(__file__).parent
OUT = HERE / "img"
TILE = 360
COLS = 4
ROWS = (len(PRODUCTS) + COLS - 1) // COLS
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def slug(name):
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    keep = [c.lower() if c.isalnum() else "-" for c in plain]
    return "-".join(filter(None, "".join(keep).split("-")))[:48]


def tile_html(name, category, icon):
    tint, ink = PALETTE[category]
    return f"""
    <div class="tile" style="background:{tint}">
      <svg viewBox="0 0 100 100" width="200" height="200" fill="none"
           stroke="{ink}" stroke-width="4.5"
           stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg>
    </div>"""


def build_html():
    tiles = "".join(tile_html(n, c, i) for n, _, _, c, i in PRODUCTS)
    blanks = '<div class="tile" style="background:#fff"></div>' * (ROWS * COLS - len(PRODUCTS))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
      *{{margin:0;padding:0;box-sizing:border-box}}
      body{{width:{COLS * TILE}px}}
      .grid{{display:grid;grid-template-columns:repeat({COLS},{TILE}px);
             grid-auto-rows:{TILE}px}}
      .tile{{display:flex;align-items:center;justify-content:center}}
    </style></head><body><div class="grid">{tiles}{blanks}</div></body></html>"""


def main():
    OUT.mkdir(exist_ok=True)
    page = HERE / "grid.html"
    grid = HERE / "grid.png"
    page.write_text(build_html(), encoding="utf-8")

    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--screenshot={grid}",
         f"--window-size={COLS * TILE},{ROWS * TILE}", page.as_uri()],
        check=True, capture_output=True, timeout=180,
    )

    sheet = Image.open(grid).convert("RGB")
    if sheet.size != (COLS * TILE, ROWS * TILE):
        raise SystemExit(f"Chrome returned {sheet.size}, not {(COLS * TILE, ROWS * TILE)}")

    for index, (name, _, _, _, _) in enumerate(PRODUCTS):
        left, top = (index % COLS) * TILE, (index // COLS) * TILE
        sheet.crop((left, top, left + TILE, top + TILE)).save(OUT / f"{slug(name)}.png")

    print(f"{len(PRODUCTS)} pictures in {OUT}")


if __name__ == "__main__":
    main()
