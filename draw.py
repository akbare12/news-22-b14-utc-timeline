#!/usr/bin/env python3
"""news-22 b14 utc-timeline: draw the 1024x1024 front page (PIL only)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 239, 219)
INK = (25, 25, 25)
RED = (169, 30, 34)
RED_DK = (140, 20, 25)
CREAM2 = (238, 229, 203)
LINE = (120, 110, 85)
OCEAN = (207, 224, 234)
LAND = (227, 213, 168)
LAND_LN = (138, 122, 82)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _cache:
        path = SERIF_B if (serif and bold) else SERIF if serif else SANS_B if bold else SANS
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(text, f):
    return f.getlength(text)


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if f.getlength(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, f, maxw, fill=INK, lh=None, max_lines=None):
    lines = wrap(text, f, maxw)
    if max_lines:
        lines = lines[:max_lines]
    if lh is None:
        lh = int(f.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


CHIP_COLORS = {
    "CONFIRMED": (46, 125, 79),
    "REPORTED": (46, 90, 136),
    "CLAIM": (176, 122, 30),
    "OFFICIAL": (70, 70, 70),
    "FORECAST": (106, 76, 147),
    "ONGOING": (198, 90, 30),
    "PENDING": (120, 110, 85),
}


def chip(d, x, y, label, h=13):
    f = font(8, bold=True)
    w = int(f.getlength(label)) + 10
    col = CHIP_COLORS.get(label, (90, 90, 90))
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=col)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- scenes
def scene_drones(d, x0, y0, w, h):
    """Night sky over Kyiv: explosions, drone trails, skyline, collapsed block."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 24, 48))
    for sx, sy, r in [(30, 14, 1), (90, 8, 1), (150, 18, 2), (210, 10, 1), (60, 26, 1),
                      (180, 30, 1), (120, 6, 1), (235, 24, 1)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r], fill=(220, 220, 200))
    # explosion blooms
    for cx, cy, r, col in [(70, 30, 14, (255, 140, 40)), (170, 22, 11, (255, 170, 60)),
                           (215, 42, 9, (255, 120, 30))]:
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r], fill=col)
        d.ellipse([x0 + cx - r // 2, y0 + cy - r // 2, x0 + cx + r // 2, y0 + cy + r // 2],
                  fill=(255, 220, 120))
    # drone dots with trails
    for dx, dy in [(40, 18), (110, 12), (150, 34), (200, 14), (90, 40)]:
        d.line([x0 + dx - 14, y0 + dy + 6, x0 + dx, y0 + dy], fill=(200, 200, 200), width=1)
        d.ellipse([x0 + dx - 2, y0 + dy - 2, x0 + dx + 2, y0 + dy + 2], fill=(230, 230, 230))
    # skyline
    base = y0 + h
    for bx, bw, bh in [(0, 34, 26), (36, 26, 34), (64, 30, 22), (96, 24, 30), (122, 30, 20),
                       (154, 28, 32), (184, 30, 24), (216, 34, 28)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(8, 12, 26))
        for wx in range(bx + 5, bx + bw - 3, 8):
            for wy in range(base - bh + 5, base - 4, 8):
                if (wx + wy) % 16 == 0:
                    d.rectangle([x0 + wx, wy, x0 + wx + 3, wy + 3], fill=(255, 190, 90))
    # collapsed block: tilted slab + rubble, under the big bloom
    d.polygon([(x0 + 96, base - 2), (x0 + 128, base - 2), (x0 + 122, base - 16),
               (x0 + 102, base - 12)], fill=(60, 55, 50))
    d.polygon([(x0 + 100, base - 12), (x0 + 118, base - 18), (x0 + 124, base - 10)],
              fill=(90, 80, 70))
    d.ellipse([x0 + 104, base - 20, x0 + 118, base - 8], fill=(255, 150, 50))


def scene_cop31(d, x0, y0, w, h):
    """Sunset over Antalya: cracked globe, conference hall silhouettes."""
    # sunset gradient bands
    bands = [(255, 170, 60), (245, 130, 50), (220, 90, 45), (180, 60, 55)]
    bh = h // 4 + 1
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * bh, x0 + w, y0 + min(h, (i + 1) * bh)], fill=col)
    # sun
    d.ellipse([x0 + w - 52, y0 + 8, x0 + w - 22, y0 + 38], fill=(255, 230, 150))
    # cracked globe, left
    cx, cy, r = x0 + 62, y0 + h // 2 - 4, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 120, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 60, 45), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(30, 60, 45), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(30, 60, 45), width=2)
    d.line([cx - 6, cy - r + 4, cx + 4, cy - 6, cx - 2, cy + 8, cx + 8, cy + r - 6],
           fill=(255, 240, 200), width=3)
    d.ellipse([cx - 16, cy - 12, cx - 2, cy + 2], fill=(40, 90, 60))
    d.ellipse([cx + 6, cy + 8, cx + 20, cy + 20], fill=(40, 90, 60))
    # conference hall: table + flags + seated silhouettes
    base = y0 + h
    d.rectangle([x0 + 108, base - 26, x0 + w - 8, base - 18], fill=(60, 40, 30))
    for fx in range(116, x0 + w - 16, 22):
        d.line([fx, base - 44, fx, base - 26], fill=(40, 30, 20), width=2)
        d.polygon([(fx, base - 44), (fx + 12, base - 40), (fx, base - 36)], fill=RED)
    for hx in range(120, x0 + w - 20, 26):
        d.ellipse([hx, base - 34, hx + 10, base - 26], fill=(25, 20, 18))
        d.rectangle([hx - 1, base - 26, hx + 11, base - 18], fill=(25, 20, 18))


def scene_bahrain(d, x0, y0, w, h):
    """Radar base at night: dish, fire glow at a civilian site, smoke."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(14, 20, 38))
    for sx, sy, r in [(20, 10, 1), (70, 6, 1), (130, 12, 2), (200, 8, 1), (160, 20, 1),
                      (100, 16, 1)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r], fill=(210, 210, 190))
    # radar mast: lattice triangle + rotating bar antenna + small dish
    mx, my = x0 + 58, y0 + 18
    d.line([mx - 14, y0 + h - 6, mx, my + 8], fill=(150, 150, 150), width=2)
    d.line([mx + 14, y0 + h - 6, mx, my + 8], fill=(150, 150, 150), width=2)
    d.line([mx - 8, y0 + h - 24, mx + 8, y0 + h - 24], fill=(150, 150, 150), width=1)
    d.line([mx - 5, y0 + h - 40, mx + 5, y0 + h - 40], fill=(150, 150, 150), width=1)
    d.line([mx - 20, my + 4, mx + 20, my + 4], fill=(200, 200, 200), width=4)
    d.ellipse([mx - 3, my + 1, mx + 3, my + 7], fill=(220, 220, 220))
    d.line([mx, my + 8, mx + 12, my - 6], fill=(180, 180, 180), width=2)
    d.ellipse([mx + 8, my - 10, mx + 16, my - 2], fill=(180, 180, 180))
    # fire glow at civilian site, right
    fx, fy = x0 + w - 55, y0 + h - 30
    d.ellipse([fx - 26, fy - 22, fx + 26, fy + 18], fill=(255, 140, 40))
    d.ellipse([fx - 16, fy - 14, fx + 16, fy + 12], fill=(255, 200, 80))
    d.ellipse([fx - 8, fy - 8, fx + 8, fy + 8], fill=(255, 240, 160))
    # smoke wisps
    for sx, sy, r in [(fx - 8, fy - 30, 7), (fx + 4, fy - 42, 9), (fx - 2, fy - 54, 6)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r], fill=(90, 90, 100))
    # low buildings + fence
    base = y0 + h
    for bx, bw, bh in [(120, 26, 14), (150, 20, 18), (178, 24, 12)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(10, 14, 26))
    d.line([x0, base - 4, x0 + w, base - 4], fill=(70, 70, 80), width=1)


# ------------------------------------------------------------ small icons
def icon(d, x0, y0, s, kind):
    bg = {"ballot": (46, 90, 136), "f1": (25, 25, 25), "fire": (169, 30, 34),
          "ship": (46, 90, 136), "cricket": (46, 125, 79), "basket": (198, 90, 30),
          "tennis": (106, 140, 40), "dome": (46, 90, 136), "virus": (169, 30, 34),
          "coin": (176, 122, 30)}[kind]
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=bg)
    c = s // 2
    if kind == "ballot":
        d.rectangle([x0 + 12, y0 + 20, x0 + s - 12, y0 + s - 10], fill=(255, 255, 255))
        d.rectangle([x0 + 18, y0 + 14, x0 + s - 18, y0 + 20], fill=(230, 230, 230))
        d.line([x0 + 18, y0 + 34, x0 + 24, y0 + 40, x0 + 36, y0 + 26], fill=RED, width=3)
    elif kind == "f1":
        for r in range(3):
            for col in range(4):
                if (r + col) % 2 == 0:
                    d.rectangle([x0 + 8 + col * 9, y0 + 10 + r * 9,
                                 x0 + 17 + col * 9, y0 + 19 + r * 9], fill=(255, 255, 255))
        d.line([x0 + 8, y0 + 42, x0 + s - 8, y0 + 42], fill=(255, 200, 60), width=3)
        d.line([x0 + 8, y0 + 47, x0 + s - 14, y0 + 47], fill=(255, 255, 255), width=2)
    elif kind == "fire":
        d.polygon([(x0 + c, y0 + 8), (x0 + c + 12, y0 + 26), (x0 + c + 6, y0 + 26),
                   (x0 + c + 10, y0 + 38), (x0 + c - 10, y0 + 38), (x0 + c - 6, y0 + 26),
                   (x0 + c - 12, y0 + 26)], fill=(255, 170, 40))
        d.polygon([(x0 + c, y0 + 24), (x0 + c + 6, y0 + 34), (x0 + c - 6, y0 + 34)],
                  fill=(255, 230, 120))
        d.rectangle([x0 + 8, y0 + s - 12, x0 + s - 8, y0 + s - 6], fill=(60, 60, 60))
    elif kind == "ship":
        d.polygon([(x0 + 8, y0 + 30), (x0 + s - 8, y0 + 30), (x0 + s - 16, y0 + 42),
                   (x0 + 16, y0 + 42)], fill=(230, 230, 230))
        d.rectangle([x0 + c - 2, y0 + 14, x0 + c + 2, y0 + 30], fill=(230, 230, 230))
        d.polygon([(x0 + c + 2, y0 + 14), (x0 + c + 14, y0 + 26), (x0 + c + 2, y0 + 26)],
                  fill=(255, 200, 60))
        d.ellipse([x0 + s - 20, y0 + 8, x0 + s - 8, y0 + 20], fill=(120, 120, 120))
        d.line([x0 + 6, y0 + 46, x0 + s - 6, y0 + 46], fill=(180, 220, 240), width=2)
    elif kind == "cricket":
        d.rectangle([x0 + c - 3, y0 + 10, x0 + c + 5, y0 + 34], fill=(220, 180, 120))
        d.ellipse([x0 + c + 8, y0 + 34, x0 + c + 18, y0 + 44], fill=(200, 40, 40))
        d.line([x0 + 8, y0 + 46, x0 + s - 8, y0 + 46], fill=(255, 255, 255), width=2)
    elif kind == "basket":
        d.ellipse([x0 + 10, y0 + 10, x0 + s - 10, y0 + s - 10], fill=(255, 140, 40))
        d.ellipse([x0 + 10, y0 + 10, x0 + s - 10, y0 + s - 10], outline=(120, 60, 10), width=2)
        d.line([x0 + 10, y0 + c, x0 + s - 10, y0 + c], fill=(120, 60, 10), width=2)
        d.line([x0 + c, y0 + 10, x0 + c, y0 + s - 10], fill=(120, 60, 10), width=2)
        d.arc([x0 + 4, y0 + 4, x0 + s - 4, y0 + s - 4], 300, 60, fill=(120, 60, 10), width=2)
    elif kind == "tennis":
        d.ellipse([x0 + 10, y0 + 10, x0 + s - 10, y0 + s - 10], fill=(190, 220, 60))
        d.arc([x0 + 10, y0 + 10, x0 + s - 10, y0 + s - 10], 250, 110, fill=(255, 255, 255), width=3)
        d.arc([x0 + 10, y0 + 10, x0 + s - 10, y0 + s - 10], 70, 290, fill=(255, 255, 255), width=3)
    elif kind == "dome":
        d.pieslice([x0 + 12, y0 + 8, x0 + s - 12, y0 + 34], 180, 360, fill=(255, 255, 255))
        d.rectangle([x0 + 10, y0 + 30, x0 + s - 10, y0 + 38], fill=(255, 255, 255))
        d.rectangle([x0 + 8, y0 + 38, x0 + s - 8, y0 + 44], fill=(230, 230, 230))
        for px in range(14, s - 12, 8):
            d.rectangle([x0 + px, y0 + 32, x0 + px + 3, y0 + 37], fill=bg)
    elif kind == "virus":
        d.ellipse([x0 + 14, y0 + 14, x0 + s - 14, y0 + s - 14], fill=(220, 60, 60))
        for ang in range(0, 360, 45):
            import math
            a = math.radians(ang)
            x1 = x0 + c + int(17 * math.cos(a))
            y1 = y0 + c + int(17 * math.sin(a))
            x2 = x0 + c + int(24 * math.cos(a))
            y2 = y0 + c + int(24 * math.sin(a))
            d.line([x1, y1, x2, y2], fill=(220, 60, 60), width=3)
            d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=(220, 60, 60))
        d.ellipse([x0 + c - 4, y0 + c - 4, x0 + c + 4, y0 + c + 4], fill=(255, 255, 255))
    elif kind == "coin":
        d.ellipse([x0 + 10, y0 + 10, x0 + s - 10, y0 + s - 10], fill=(255, 200, 60))
        d.ellipse([x0 + 10, y0 + 10, x0 + s - 10, y0 + s - 10], outline=(140, 100, 20), width=2)
        d.text((x0 + c - 7, y0 + c - 11), "$", font=font(20, bold=True), fill=(140, 100, 20))


# ------------------------------------------------------------------ data
NUMBERS = [
    ("186", "DRONES FIRED"), ("161", "SHOT DOWN"), ("720/9", "INDIA DECLARE"),
    ("98.79%", "HK TURNOUT"), ("$120bn", "ADAPTATION AXED"), ("35%", "CLEAN POWER 2035"),
    ("44h", "OVERTIME"), ("50", "WEMBANYAMA PTS"), ("258", "DEMS SEATS"),
]

REGIONS = [
    ("EUROPE 8", (46, 90, 136)), ("MIDDLE EAST 7", (176, 122, 30)),
    ("ASIA-PACIFIC 7", (46, 125, 79)), ("AMERICAS 5", (14, 124, 123)),
    ("AFRICA 3", (198, 90, 30)), ("OCEANIA 3", (106, 76, 147)),
    ("WORLD 3", (85, 85, 85)),
]
REGION_COUNTS = [8, 7, 7, 5, 3, 3, 3]

HEROES = [
    dict(n=1, hour="OVERNIGHT", kicker="KYIV · WAR · OVERNIGHT", chip="REPORTED",
         scene="drones",
         title="186 drones rain on Ukraine overnight",
         body=("Russia fires 186 drones; 161 are shot down or jammed. A five-storey "
               "block in Dymer collapses \u2014 1 dead, 14 unaccounted for. "
               "Strikes hit 18 locations."),
         src="Ukrainian Air Force \u00b7 Reuters"),
    dict(n=9, hour="~16:00", kicker="ANTALYA · CLIMATE · ~16:00", chip="CONFIRMED",
         scene="cop31",
         title="COP31 collapses: NO DEAL",
         body=("Antalya talks end with no agreement after 44 hours overtime \u2014 the first "
               "climate-summit failure since 2009. Final text had no fossil-fuel language; "
               "$120bn adaptation target axed."),
         src="AP \u00b7 Reuters"),
    dict(n=10, hour="~20:00", kicker="BAHRAIN · GULF · FIRST REPORTED SUNDAY", chip="CLAIM",
         scene="bahrain",
         title="Iran claims 2 US Patriot radars hit in Bahrain",
         body=("Tehran says its missiles struck radars at al-Riffa and Awali; Bahrain denies "
               "a military attack. A civilian site in Sitra burns, 2 hurt, no one killed."),
         src="IRGC vs Bahrain MoI \u00b7 Al Jazeera"),
]

SMALL = [
    # row 2 (01:00)
    dict(n=2, kicker="HONG KONG \u00b7 ELECTION", chip="CONFIRMED", icon="ballot",
         title="Hong Kong votes, 98.79% turnout",
         body="856 candidates for 723 seats; 5,640 of 5,709 electors vote.", src="Reuters"),
    dict(n=3, kicker="LAS VEGAS \u00b7 F1", chip="CONFIRMED", icon="f1",
         title="Verstappen wins by 0.639s",
         body="Beats Norris in Las Vegas; Piastri third; 75th win.", src="AP"),
    # row 3 (06:00)
    dict(n=16, kicker="CIKANDE \u00b7 DISASTER", chip="REPORTED", icon="fire",
         title="Candy-factory fire: 3 dead, 36 missing",
         body="Blaze began Saturday night; 15 rescued, search goes on.", src="Detiknews"),
    dict(n=8, kicker="BALTIC \u00b7 SHIPPING", chip="REPORTED", icon="ship",
         title="Sparta II still burning, towed home",
         body="Hit by drone Saturday; 16 crew safe; Finland blames Kyiv.", src="Reuters"),
    # row 4 (12:00)
    dict(n=17, kicker="CHRISTCHURCH \u00b7 CRICKET", chip="CONFIRMED", icon="cricket",
         title="India declare 720/9, record in NZ",
         body="Rahul 136, Pant 128; highest Test total in New Zealand.", src="BBC"),
    dict(n=25, kicker="SAN ANTONIO \u00b7 NBA", chip="CONFIRMED", icon="basket",
         title="Wembanyama drops 50 points",
         body="19 rebounds, 5 blocks; Spurs beat Pelicans 114\u201391.", src="AP"),
    # row 6 (17:00)
    dict(n=4, kicker="TURIN \u00b7 TENNIS", chip="CONFIRMED", icon="tennis",
         title="Alcaraz beats Zverev for ATP title",
         body="6\u20132, 7\u20136(7); first ATP Finals crown.", src="ATP"),
    dict(n=23, kicker="WASHINGTON \u00b7 POLITICS", chip="CONFIRMED", icon="dome",
         title="Democrats take House, 258 seats",
         body="Hubbard beats Foxx by 330 in NC recount; 4 races uncalled.", src="AP"),
    # row 8 (23:00)
    dict(n=30, kicker="DR CONGO \u00b7 HEALTH", chip="OFFICIAL", icon="virus",
         title="Ebola cases reach 11,613",
         body="WHO count climbs as fighting traps health workers.", src="WHO"),
    dict(n=34, kicker="MARKETS \u00b7 CRYPTO", chip="REPORTED", icon="coin",
         title="Bitcoin back above $60,000",
         body="Trades $60,020, up 1.85% on the day.", src="Reuters"),
]

ALSO = [
    (5, "Estonia closes 5 Russia crossings from 1 Dec"),
    (6, "Denmark expels Russian attach\u00e9 over plot"),
    (7, "Belgian air-traffic staff join Monday strike"),
    (11, "Merkury corvette hit by sea drone off Benghazi [CLAIM]"),
    (12, "Tehran starts power rationing, ~2h cuts a day"),
    (13, "Gaza: 4 killed by Israeli fire; aid-van strike"),
    (14, "Eisenkot invites Likud to coalition talks"),
    (15, "Settlers burn 12 cars in West Bank; attack homes"),
    (18, "Seoul minister quits over AI exam-cheat scandal"),
    (19, "Nepal PM Shah lands in Delhi, first trip abroad"),
    (20, "Manipur liquor toll rises; ~600 treated"),
    (21, "EU\u2013Indonesia trade deal signed (date disputed)"),
    (22, "Australia rejects US report on AUKUS subs"),
    (24, "Bolsonaro in intensive care, Bras\u00edlia"),
    (26, "Falcon 9 launches NROL-136 spy satellite"),
    (27, "FBI probes NCIC crime-database hack"),
    (28, "Drones kill 4 near Khartoum; UN site hit"),
    (29, "Nigeria boat capsizes; 24 mourners drown"),
    (31, "Melbourne marks 70 yrs since 1956 Olympics"),
    (32, "Fred Nile dies, 92 (died 21 Nov, announced 22)"),
    (33, "Cummins stays Australia Test captain"),
    (35, "Nvidia faces SEC accounting probe"),
    (36, "Liverpool rout Man Utd 4\u20130"),
]

# (lon, lat) pins for all 36 stories
PINS = {
    1: (30.5, 50.5), 2: (114.2, 22.3), 3: (-115.1, 36.2), 4: (7.7, 45.1),
    5: (25.0, 58.5), 6: (10.0, 56.0), 7: (4.5, 50.5), 8: (21.0, 59.5),
    9: (30.7, 36.9), 10: (50.6, 26.2), 11: (20.1, 32.1), 12: (51.4, 35.7),
    13: (34.5, 31.5), 14: (35.0, 31.8), 15: (35.2, 31.9), 16: (106.2, -6.1),
    17: (172.6, -43.5), 18: (127.0, 37.5), 19: (77.2, 28.6), 20: (93.9, 24.8),
    21: (106.8, -6.2), 22: (149.1, -35.3), 23: (-77.0, 38.9), 24: (-47.9, -15.8),
    25: (-98.5, 29.4), 26: (-80.6, 28.4), 27: (-77.5, 39.3), 28: (32.5, 15.6),
    29: (6.3, 4.9), 30: (23.0, -2.5), 31: (145.0, -37.8), 32: (151.2, -33.9),
    33: (151.8, -34.3), 34: (-74.0, 40.7), 35: (-122.0, 37.4), 36: (-2.97, 53.4),
}
# manual nudges (px) for dense clusters
NUDGE = {13: (-5, 4), 14: (5, -4), 15: (6, 5), 10: (4, -3), 12: (5, 2),
         23: (-4, -3), 27: (5, 4), 32: (-4, 3), 33: (5, -3), 16: (-4, 3),
         21: (4, -3)}

NA = [(-168, 65), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-100, 73),
      (-90, 74), (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-65, 44),
      (-70, 42), (-76, 35), (-81, 26), (-84, 30), (-90, 21), (-94, 17),
      (-97, 16), (-104, 23), (-110, 24), (-117, 33), (-124, 40), (-124, 48),
      (-132, 58), (-150, 59), (-162, 58)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 65), (-32, 68), (-25, 70),
             (-20, 74), (-30, 76), (-45, 78), (-58, 76), (-60, 70)]
SA = [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
      (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -50),
      (-73, -40), (-80, -30), (-80, -18), (-81, -6)]
AFRICA = [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (32, 31), (35, 28),
          (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (32, -29), (20, -35),
          (15, -27), (12, -18), (9, 4), (-8, 5)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
          (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (25, 71),
          (18, 69), (12, 65), (5, 60), (5, 58), (0, 54), (-5, 50)]
ASIA = [(30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 74), (130, 72),
        (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
        (142, 50), (140, 40), (135, 35), (127, 35), (122, 30), (120, 22),
        (110, 20), (105, 10), (100, 8), (97, 16), (92, 21), (88, 22), (80, 15),
        (77, 8), (72, 20), (66, 25), (60, 25), (57, 27), (52, 28), (48, 30),
        (43, 36), (36, 36), (30, 36), (30, 42), (35, 45), (40, 50), (45, 55),
        (50, 60), (55, 65), (50, 68)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
             (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
             (137, -12), (132, -11), (126, -14), (122, -17)]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=OCEAN)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=LINE, width=1)
    # graticule
    for gx in range(1, 6):
        gx0 = x0 + w * gx // 6
        d.line([gx0, y0, gx0, y0 + h], fill=(190, 208, 220), width=1)
    for gy in range(1, 3):
        gy0 = y0 + h * gy // 3
        d.line([x0, gy0, x0 + w, gy0], fill=(190, 208, 220), width=1)

    def proj(lon, lat):
        px = x0 + (lon + 180.0) / 360.0 * w
        py = y0 + (75.0 - lat) / 130.0 * h
        return (px, py)

    for poly in (NA, GREENLAND, SA, AFRICA, EUROPE, ASIA, AUSTRALIA):
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LN)
    for lab, (lon, lat) in [("NORTH AMERICA", (-100, 48)), ("SOUTH AMERICA", (-60, -15)),
                            ("AFRICA", (18, 2)), ("EUROPE", (15, 54)),
                            ("ASIA", (95, 55)), ("AUSTRALIA", (134, -25))]:
        px, py = proj(lon, lat)
        f = font(7, bold=True)
        d.text((px - f.getlength(lab) / 2, py - 4), lab, font=f, fill=(120, 108, 72))
    # pins
    for n in range(1, 37):
        lon, lat = PINS[n]
        px, py = proj(lon, lat)
        dx, dy = NUDGE.get(n, (0, 0))
        px, py = px + dx, py + dy
        col = RED if n in (1, 9, 10) else (176, 122, 30) if n in (10, 11) else INK
        r = 5
        d.ellipse([px - r, py - r, px + r, py + r], fill=col, outline=(255, 255, 255), width=1)
        f = font(6, bold=True)
        t = str(n)
        d.text((px - f.getlength(t) / 2, py - 3.5), t, font=f, fill=(255, 255, 255))


def hero_row(d, y, hgt, hero):
    x0, x1 = 72, 1008
    # scene
    sw = 250
    if hero["scene"] == "drones":
        scene_drones(d, x0, y, sw, hgt)
    elif hero["scene"] == "cop31":
        scene_cop31(d, x0, y, sw, hgt)
    else:
        scene_bahrain(d, x0, y, sw, hgt)
    d.rectangle([x0, y, x0 + sw, y + hgt], outline=INK, width=1)
    tx = x0 + sw + 12
    twd = x1 - tx
    # number badge
    fnum = font(20, bold=True, serif=True)
    d.text((tx, y + 2), str(hero["n"]), font=fnum, fill=RED)
    nw = fnum.getlength(str(hero["n"])) + 8
    d.text((tx + nw, y + 4), hero["kicker"], font=font(9, bold=True), fill=RED)
    chip(d, x1 - 78, y + 4, hero["chip"])
    ty = y + 24
    ty = draw_wrapped(d, tx, ty, hero["title"], font(16, bold=True, serif=True),
                      twd, lh=19, max_lines=2)
    ty += 2
    ty = draw_wrapped(d, tx, ty, hero["body"], font(10.5), twd, lh=13, max_lines=2)
    d.text((tx, y + hgt - 14), "Source: " + hero["src"], font=font(8.5), fill=(90, 80, 60))


def small_card(d, x0, y, w, hgt, card):
    d.rectangle([x0, y, x0 + w, y + hgt], fill=(255, 252, 244), outline=LINE, width=1)
    icon(d, x0 + 1, y + 1, hgt - 2, card["icon"])
    tx = x0 + hgt + 6
    twd = x0 + w - tx - 6
    # kicker + chip on one line
    f_k = font(8, bold=True)
    d.text((tx, y + 3), str(card["n"]) + " \u00b7 " + card["kicker"], font=f_k, fill=RED)
    chip(d, x0 + w - 66, y + 3, card["chip"])
    ty = y + 15
    ty = draw_wrapped(d, tx, ty, card["title"], font(11, bold=True), twd, lh=13, max_lines=2)
    ty = draw_wrapped(d, tx, ty, card["body"], font(9.5), twd, lh=11, max_lines=1)
    d.text((tx, y + hgt - 11), card["src"], font=font(8), fill=(120, 110, 85))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top red bar
    d.rectangle([0, 0, W, 6], fill=RED)
    # masthead
    d.text((16, 10), "THE WORLD TODAY", font=font(40, bold=True, serif=True), fill=INK)
    d.text((1008 - font(19, bold=True, serif=True).getlength("SUNDAY 22 NOVEMBER 2026"), 12),
           "SUNDAY 22 NOVEMBER 2026", font=font(19, bold=True, serif=True), fill=RED)
    d.text((1008 - font(11).getlength("THE WORLD IN ONE DAY"), 38),
           "THE WORLD IN ONE DAY", font=font(11), fill=(90, 80, 60))
    d.line([16, 56, 1008, 56], fill=INK, width=2)
    # kicker
    d.text((16, 60), "ONE DAY \u00b7 36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ITEM HAPPENED OR "
                     "WAS FIRST REPORTED 22 NOV 2026",
           font=font(11, bold=True), fill=INK)
    d.text((1008 - font(11, bold=True).getlength("ALL TIMES UTC"), 60),
           "ALL TIMES UTC", font=font(11, bold=True), fill=RED)
    # number strip
    y0, y1 = 78, 108
    d.rectangle([16, y0, 1008, y1], fill=CREAM2, outline=LINE, width=1)
    cw = (1008 - 16) / len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 16 + cw * i + cw / 2
        fn = font(19, bold=True, serif=True)
        d.text((cx - fn.getlength(num) / 2, y0 + 2), num, font=fn, fill=RED)
        fl = font(7.5, bold=True)
        d.text((cx - fl.getlength(lab) / 2, y0 + 22), lab, font=fl, fill=INK)
        if i:
            d.line([16 + cw * i, y0 + 3, 16 + cw * i, y1 - 3], fill=LINE, width=1)
    # region bar
    y0, y1 = 112, 130
    x = 16
    total = sum(REGION_COUNTS)
    for (lab, col), cnt in zip(REGIONS, REGION_COUNTS):
        wseg = (1008 - 16) * cnt / total
        d.rectangle([x, y0, x + wseg, y1], fill=col)
        f = font(10, bold=True)
        d.text((x + wseg / 2 - f.getlength(lab) / 2, y0 + 3), lab, font=f, fill=(255, 255, 255))
        x += wseg
    # timeline header
    d.text((16, 134), "THE DAY IN UTC", font=font(12, bold=True), fill=INK)
    d.text((1008 - font(10, bold=True).getlength("WIRES READ TO 23:00 UTC"), 136),
           "WIRES READ TO 23:00 UTC", font=font(10, bold=True), fill=RED)
    ms = ("01:00 HK polls open \u00b7 03:00 COP31 objections close \u00b7 06:00 COP31 session "
          "\u00b7 ~16:00 COP31 collapses \u00b7 17:00 Alcaraz wins \u00b7 18:13 Dems reach 258 "
          "\u00b7 23:00 wires read")
    d.text((16, 149), ms, font=font(9.5), fill=(70, 62, 45))

    # ---- timeline spine + rows
    SPINE_X = 66
    d.line([SPINE_X, 162, SPINE_X, 723], fill=(90, 80, 60), width=2)
    rows = [
        ("hero", 162, 86, HEROES[0]),
        ("small", 252, 55, (SMALL[0], SMALL[1])),
        ("small", 311, 55, (SMALL[2], SMALL[3])),
        ("small", 370, 55, (SMALL[4], SMALL[5])),
        ("hero", 429, 86, HEROES[1]),
        ("small", 519, 55, (SMALL[6], SMALL[7])),
        ("hero", 578, 86, HEROES[2]),
        ("small", 668, 55, (SMALL[8], SMALL[9])),
    ]
    hour_labels = ["OVERNIGHT", "01:00", "06:00", "12:00", "~16:00", "17:00", "~20:00", "23:00"]
    for (kind, y, hgt, payload), hl in zip(rows, hour_labels):
        cy = y + hgt // 2
        d.ellipse([SPINE_X - 5, cy - 5, SPINE_X + 5, cy + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(8, bold=True)
        d.text((SPINE_X - 9 - f.getlength(hl), cy - 5), hl, font=f, fill=INK)
        if kind == "hero":
            hero_row(d, y, hgt, payload)
        else:
            c1, c2 = payload
            small_card(d, 72, y, 462, hgt, c1)
            small_card(d, 546, y, 462, hgt, c2)

    # ---- map + ALSO list
    d.text((16, 729), "THE WORLD \u2014 WHERE IT HAPPENED", font=font(11, bold=True), fill=INK)
    d.text((440, 729), "ALSO ON SUNDAY 22 NOVEMBER \u2014 23 MORE STORIES",
           font=font(11, bold=True), fill=INK)
    draw_map(d, 16, 747, 414, 135)
    cols = [ALSO[:12], ALSO[12:]]
    for ci, col in enumerate(cols):
        cx = 440 + ci * 292
        yy = 749
        for n, txt in col:
            f = font(9)
            d.text((cx, yy), str(n), font=font(9, bold=True), fill=RED)
            d.text((cx + 18, yy), txt, font=f, fill=INK)
            yy += 11.5
    d.text((16, 886 - 0), "", font=font(9))

    # ---- DATE CHECK
    d.rectangle([16, 888, 1008, 970], fill=(255, 244, 240), outline=RED, width=2)
    d.text((26, 892), "DATE CHECK", font=font(11, bold=True), fill=RED)
    yy = 908
    yy = draw_wrapped(d, 26, yy,
                      "EVERY STORY HAPPENED OR WAS FIRST REPORTED SUNDAY 22 NOV 2026 \u00b7 "
                      "WIRES READ TO 23:00 UTC",
                      font(9.5, bold=True), 972, lh=12, max_lines=1)
    yy = draw_wrapped(d, 26, yy,
                      "LEFT OUT \u2014 NOT 22 NOV: 400-drone barrage 19\u201320 Nov \u00b7 El Chapo "
                      "Isidro captured 20 Nov \u00b7 BepiColombo Mercury orbit 21 Nov (burn 18:24 GMT) "
                      "\u00b7 Kryvyi Rih 20 Nov \u00b7 Peru quake 20 Nov \u00b7 Hormuz tankers hit Sat "
                      "21 Nov 05:00 GMT (reported Sun 17:13 UTC) \u00b7 Nigeria boat Fri 20 Nov "
                      "\u00b7 FBI NCIC hack 20/21 Nov",
                      font(9.5), 972, lh=12, max_lines=2)
    draw_wrapped(d, 26, yy,
                 "NOT YET: COP32 venue \u00b7 Dymer final toll \u00b7 4 House races uncalled",
                 font(9.5), 972, lh=12, max_lines=1)

    # ---- footer
    d.text((16, 976), "SOURCES: AP \u00b7 Reuters \u00b7 BBC \u00b7 CNN \u00b7 Guardian \u00b7 France 24 \u00b7 "
                     "Al Jazeera \u00b7 Yonhap \u00b7 Anadolu \u00b7 Detiknews \u00b7 Basarnas \u00b7 "
                     "WHO \u00b7 Ukrainian Air Force",
           font=font(8.5), fill=(70, 62, 45))
    d.text((16, 989), "CONFIRMED 2+ outlets \u00b7 REPORTED carried by wires that day \u00b7 CLAIM one "
                     "side, not yet verified \u00b7 OFFICIAL recorded result \u00b7 FORECAST not yet "
                     "decided when drawn",
           font=font(8.5), fill=(70, 62, 45))
    d.text((16, 1002), "Scenes are drawn illustrations, not photographs. \u00b7 THE WORLD TODAY, "
                      "Sunday 22 November 2026",
           font=font(8.5), fill=(90, 80, 60))

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
