"""The demo catalogue, in one place: what it holds and what each item looks like.

Both the seeding script and the image generator read this, so a product can never end up
with another product's picture.
"""

CATEGORIES = {
    "general": "11111111-1111-4111-8111-111111111111",
    "herramientas": "22222222-2222-4222-8222-222222222222",
    "electricidad": "33333333-3333-4333-8333-333333333333",
    "fontaneria": "44444444-4444-4444-8444-444444444444",
    "pinturas": "55555555-5555-4555-8555-555555555555",
}

# Tint, ink. The tint is the tile background, the ink is the line art on top of it.
PALETTE = {
    "herramientas": ("#FEF6E7", "#B45309"),
    "electricidad": ("#EAF1FE", "#1D4ED8"),
    "fontaneria": ("#E6F7F4", "#0F766E"),
    "pinturas": ("#F0EBFE", "#6D28D9"),
    "general": ("#EDF1F6", "#334155"),
}

# name, price (COP), stock, category, icon
PRODUCTS = [
    ("Martillo de carpintero 16 oz",          38900,  24, "herramientas", "hammer"),
    ("Juego de destornilladores 6 piezas",    52500,  18, "herramientas", "screwdriver"),
    ("Llave inglesa ajustable 10\"",          41200,  15, "herramientas", "wrench"),
    ("Taladro percutor 650 W",               289900,   7, "herramientas", "drill"),
    ("Flexómetro 5 m",                        18500,  40, "herramientas", "tape"),
    ("Alicate universal 8\"",                 32400,  22, "herramientas", "pliers"),

    ("Bombilla LED 9 W luz cálida",            9800, 120, "electricidad", "bulb"),
    ("Cable encauchetado 3x14, por metro",     6400, 300, "electricidad", "cable"),
    ("Interruptor doble para empotrar",       14700,  45, "electricidad", "switch"),
    ("Extensión múltiple 6 tomas",            46900,  12, "electricidad", "powerstrip"),
    ("Multímetro digital",                    78500,   6, "electricidad", "multimeter"),

    ("Tubo PVC presión 1/2\" x 6 m",          23600,  35, "fontaneria",   "pipe"),
    ("Llave de paso en bronce 1/2\"",         27900,  20, "fontaneria",   "valve"),
    ("Cinta de teflón 12 m",                   2900, 150, "fontaneria",   "teflon"),
    ("Grifo para lavamanos cromado",          89500,   9, "fontaneria",   "faucet"),

    ("Vinilo tipo 1 blanco, galón",           74900,  16, "pinturas",     "paintcan"),
    ("Rodillo de felpa 9\" con mango",        21300,  28, "pinturas",     "roller"),
    ("Brocha 3\" de cerda natural",           12800,  35, "pinturas",     "brush"),
    ("Esmalte sintético negro 1/4",           34600,  14, "pinturas",     "paintbucket"),

    ("Guantes de carnaza talla M",            15900,  50, "general",      "glove"),
    ("Escalera tijera 5 pasos en aluminio",  219000,   4, "general",      "ladder"),
    ("Candado de seguridad 50 mm",            28700,  26, "general",      "padlock"),
]

# Line art on a 100x100 canvas. Stroke and joins come from the wrapper, so each icon is
# only its own geometry.
ICONS = {
    "hammer": """
      <path d="M26 26 h30 v18 h-30 z"/>
      <path d="M26 26 l-11 5 l7 4 l-7 4 l11 5"/>
      <path d="M52 44 l12 32 a5.5 5.5 0 0 1 -10 4 l-11 -31"/>
    """,
    "screwdriver": """
      <path d="M22 78 l10 -4 l30 -30 l-6 -6 l-30 30 z"/>
      <path d="M62 44 l14 -14 a8 8 0 0 0 -12 -12 l-14 14"/>
      <path d="M58 26 l16 16"/>
    """,
    "wrench": """
      <path d="M70 22 a18 18 0 1 0 8 26 l-8 -8 l-10 -10 z"/>
      <path d="M62 46 l-34 34 a8 8 0 0 0 11 11 l34 -34"/>
    """,
    "drill": """
      <rect x="20" y="34" width="38" height="24" rx="6"/>
      <path d="M58 40 h14 v12 h-14"/>
      <path d="M72 46 h14"/>
      <path d="M30 58 l-4 24 h16 l2 -24"/>
    """,
    "tape": """
      <circle cx="48" cy="50" r="26"/>
      <circle cx="48" cy="50" r="9"/>
      <path d="M70 62 l14 8 v12 h-16 v-8"/>
    """,
    "pliers": """
      <circle cx="50" cy="48" r="4"/>
      <path d="M50 48 l-9 -22 a5 5 0 0 1 9 -3 l4 11"/>
      <path d="M50 48 l9 -22 a5 5 0 0 0 -9 -3"/>
      <path d="M50 48 l-13 34"/>
      <path d="M50 48 l13 34"/>
    """,
    "bulb": """
      <path d="M50 18 a22 22 0 0 1 14 39 v7 h-28 v-7 a22 22 0 0 1 14 -39 z"/>
      <path d="M40 72 h20"/>
      <path d="M43 80 h14"/>
    """,
    "cable": """
      <path d="M24 58 c10 -22 22 20 32 -2 c10 -20 18 16 24 -4"/>
      <rect x="12" y="50" width="12" height="16" rx="4"/>
      <rect x="76" y="40" width="12" height="16" rx="4"/>
    """,
    "switch": """
      <rect x="28" y="18" width="44" height="64" rx="8"/>
      <rect x="38" y="30" width="24" height="18" rx="3"/>
      <rect x="38" y="54" width="24" height="18" rx="3"/>
    """,
    "powerstrip": """
      <rect x="14" y="38" width="64" height="26" rx="6"/>
      <rect x="24" y="46" width="10" height="10" rx="2"/>
      <rect x="40" y="46" width="10" height="10" rx="2"/>
      <rect x="56" y="46" width="10" height="10" rx="2"/>
      <path d="M78 51 h10"/>
    """,
    "multimeter": """
      <rect x="24" y="18" width="52" height="64" rx="8"/>
      <rect x="34" y="28" width="32" height="16" rx="3"/>
      <circle cx="50" cy="62" r="11"/>
      <path d="M50 62 l6 -7"/>
    """,
    "pipe": """
      <path d="M18 38 h44 v24 h-44 z"/>
      <ellipse cx="18" cy="50" rx="6" ry="12"/>
      <path d="M62 32 h14 v36 h-14"/>
      <ellipse cx="76" cy="50" rx="6" ry="18"/>
    """,
    "valve": """
      <path d="M32 42 h36 v18 h-36 z"/>
      <path d="M14 46 h18 v10 h-18 z"/>
      <path d="M68 46 h18 v10 h-18 z"/>
      <path d="M50 42 v-10"/>
      <path d="M32 26 h36 a3 3 0 0 1 0 7 h-36 a3 3 0 0 1 0 -7 z"/>
    """,
    "teflon": """
      <circle cx="50" cy="50" r="30"/>
      <circle cx="50" cy="50" r="12"/>
      <path d="M50 20 a30 30 0 0 1 26 15"/>
    """,
    "faucet": """
      <path d="M26 82 h34"/>
      <path d="M36 82 v-12 h14 v12"/>
      <path d="M43 70 v-22"/>
      <path d="M43 48 a15 15 0 0 1 15 -15 a15 15 0 0 1 15 15 v9"/>
      <path d="M30 48 h26"/>
    """,
    "paintcan": """
      <path d="M28 40 h44 v40 a4 4 0 0 1 -4 4 h-36 a4 4 0 0 1 -4 -4 z"/>
      <ellipse cx="50" cy="40" rx="22" ry="8"/>
      <path d="M32 34 a22 20 0 0 1 36 0"/>
      <path d="M28 60 h44"/>
    """,
    "roller": """
      <rect x="16" y="22" width="48" height="18" rx="9"/>
      <path d="M64 31 h8 a4 4 0 0 1 4 4 v10 a4 4 0 0 1 -4 4 h-28 v18"/>
      <rect x="38" y="66" width="12" height="20" rx="6"/>
    """,
    "brush": """
      <path d="M36 74 h28 l4 -26 h-36 z"/>
      <rect x="38" y="36" width="24" height="12"/>
      <path d="M46 36 v-20 a4 4 0 0 1 8 0 v20"/>
    """,
    "paintbucket": """
      <path d="M26 30 h48 l-6 50 h-36 z"/>
      <path d="M26 44 h48"/>
      <path d="M74 44 l12 6 v14"/>
      <circle cx="86" cy="68" r="5"/>
    """,
    "glove": """
      <path d="M36 84 v-32 a10 10 0 0 1 10 -10 h14 a10 10 0 0 1 10 10 v32 z"/>
      <path d="M36 58 h-6 a7 7 0 0 0 0 14 h6"/>
      <path d="M47 42 v14"/>
      <path d="M56 42 v14"/>
      <path d="M65 45 v11"/>
      <path d="M36 76 h34"/>
    """,
    "ladder": """
      <path d="M32 84 l8 -68"/>
      <path d="M68 84 l-8 -68"/>
      <path d="M37 32 h26"/>
      <path d="M35 48 h30"/>
      <path d="M33 64 h34"/>
    """,
    "padlock": """
      <rect x="26" y="44" width="48" height="38" rx="7"/>
      <path d="M36 44 v-12 a14 14 0 0 1 28 0 v12"/>
      <circle cx="50" cy="60" r="5"/>
      <path d="M50 65 v8"/>
    """,
}
