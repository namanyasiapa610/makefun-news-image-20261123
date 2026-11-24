#!/usr/bin/env python3
"""THE DAY AT A GLANCE — NI23 G4 entry composer for akun14.

Front page of Monday 23 November 2026, drawn with PIL at 1024x1024.
Newspaper: THE DAY AT A GLANCE (pale sepia, midnight-blue ink, silver).
Lead story: gold slides to $3,538 an ounce (pool #34).
Fleet-style source: grid / NUMS / TL / BRIEFS / dc data blocks below.
Usage: python3 compose.py A|B -> /tmp/ni23g4-akun14-<variant>.png
"""
import sys
import math
from PIL import Image, ImageDraw, ImageFont

FDIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024

PAPER = (238, 229, 208)
PANEL = (247, 242, 229)
PANEL2 = (232, 222, 196)
INK = (18, 32, 54)
INK2 = (52, 68, 92)
SILVER = (133, 143, 160)
SILVER_L = (198, 204, 214)
RED = (168, 38, 32)
WHITE = (252, 250, 244)

REG = {
    "EUROPE": (42, 84, 140),
    "SOUTH ASIA": (28, 118, 88),
    "NORTH AMERICA": (150, 44, 60),
    "MIDDLE EAST": (178, 84, 40),
    "GLOBAL": (96, 96, 96),
    "SE ASIA": (118, 88, 158),
    "AFRICA": (186, 138, 28),
    "ASIA-PACIFIC": (28, 128, 148),
}

def F(name, size):
    return ImageFont.truetype(FDIR + name, size)

def fb(n):   # bold headline font
    return F("Archivo-Bold.ttf", n)

def fr(n):   # regular deck font
    return F("Archivo.ttf", n)

def fsr(n):  # brief font
    return F("Archivo.ttf", n)

PF_BLACK = "PlayfairDisplay-Black.ttf"
PF_BOLD = "PlayfairDisplay-Bold.ttf"
AR_B = "Archivo-Bold.ttf"
AR = "Archivo.ttf"

def tw(d, s, font):
    return d.textlength(s, font=font)

def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def text_block(d, x, y, s, font, fill, maxw, lh, max_lines=None):
    lines = wrap(d, s, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

# ---------------------------------------------------------------- data
# grid tuples: (num, region, topic, src, head, deck, kind)
grid = [
    (1, "GLOBAL", "GLB · MARKETS", "ObserverVoice, 23 Nov",
     "Gold Slides to $3,538 an Ounce",
     "Down more than $2,000 from the 2026 record high of $5,595 an ounce, after a 2.41% Friday fall.",
     "gold"),
    (2, "MIDDLE EAST", "ME · WAR", "AP / AFP wires, 23 Nov",
     "IRGC Claims Patriot Radars Hit",
     "Tehran says two US radars were destroyed in Bahrain.",
     "radar"),
    (3, "EUROPE", "EU · CLIMATE", "BBC / AP, 23 Nov",
     "COP31 Ends With No Deal",
     "COP31 ends in Antalya; draft omits fossil fuels.",
     "climate"),
    (4, "EUROPE", "EU · WAR", "BBC, 23 Nov",
     "Boy Pulled From Rubble",
     "Boy of 7 freed after hours; 6 killed.",
     "rubble"),
    (5, "EUROPE", "EU · WAR", "JagranJosh, 23 Nov",
     "Kyiv Strike: 14 Missing",
     "Drone hit a Kyiv block, Zelenskiy said.",
     "building"),
    (6, "MIDDLE EAST", "ME · WAR", "AP live, 23 Nov",
     "Hormuz Tankers Burn",
     "Iran–US war widens into the Gulf.",
     "tanker"),
    (7, "EUROPE", "EU · SEA", "BBC / JagranJosh, 23 Nov",
     "Russian Ship Burns",
     "Still ablaze in the Gulf of Finland.",
     "ship"),
    (8, "NORTH AMERICA", "NA · POLITICS", "BBC, 23 Nov",
     "Democrats Win House",
     "258–173, confirmed 23 Nov; biggest since 1992.",
     "capitol"),
    (9, "SE ASIA", "SEA · LAW", "Guardian / NYT, 23 Nov",
     "ICJ Finds Genocide",
     "ICJ: Myanmar guilty; Rohingya fled.",
     "scales"),
    (10, "SOUTH ASIA", "SA · CRICKET", "ObserverVoice, 23 Nov",
     "India Post 720/9",
     "A record — declared at Wellington, NZ.",
     "cricket"),
    (11, "NORTH AMERICA", "NA · SAFETY", "BBC, 23 Nov",
     "Army Plans Iowa Blast",
     "US Army explosives in Iowa defy a court order.",
     "bomb"),
    (12, "NORTH AMERICA", "NA · CRIME", "AP wire, 23 Nov",
     "FBI Probes Hack",
     "Suspected hack of FBI database in Washington.",
     "database"),
    (13, "EUROPE", "EU · TENNIS", "BBC, 23 Nov",
     "Alcaraz Tops Zverev",
     "First ATP Finals title, won in Turin.",
     "tennis"),
]

LOC = {1: "WORLD · MARKETS", 2: "BAHRAIN", 3: "ANTALYA, TÜRKIYE", 4: "KYIV, UKRAINE",
       5: "KYIV REGION", 6: "STRAIT OF HORMUZ", 7: "GULF OF FINLAND", 8: "WASHINGTON, US",
       9: "THE HAGUE · MYANMAR", 10: "WELLINGTON, NZ", 11: "IOWA, US",
       12: "WASHINGTON, US", 13: "TURIN, ITALY"}
CHIP = {1: "REPORTED", 2: "CLAIM", 3: "OFFICIAL", 4: "REPORTED", 5: "ONGOING",
        6: "REPORTED", 7: "ONGOING", 8: "CONFIRMED", 9: "OFFICIAL", 10: "REPORTED",
        11: "REPORTED", 12: "REPORTED", 13: "REPORTED"}

CARDS = [dict(n=t[0], region=t[1], cat=t[2], src=t[3], title=t[4], fact=t[5],
              scene=t[6], loc=LOC[t[0]], chip=CHIP[t[0]]) for t in grid]

NUMS = [
    ("$3,538", "GOLD · CARD 1"),
    ("258–173", "US HOUSE · CARD 8"),
    ("720/9", "INDIA · CARD 10"),
    ("14", "KYIV · CARD 5"),
    ("65.9%", "INDIGO · STORY 38"),
    ("₹28,000", "TATA · STORY 37"),
]

dc = ("Xi–Trump–Putin summit — 19 Nov 2026 · Missiles & drones fall in Poland — 20 Nov · "
      "Paolo Bulgari death — reported 22 Nov · 24 civilians killed, South Sudan — 22 Nov · "
      "Kerch Bridge strike — reported 22 Nov · S. Korea minister quit — reported 22 Nov · "
      "Indonesia factory fire itself — 22 Nov")
DATECHECK = dc.split(" · ")

TL = [
    ("00:02 UTC", "UN keeps AI talks going"),
    ("02:00 UTC", "Albanese on COP31"),
    ("MORNING", "Gold prints $3,538"),
    ("MIDDAY", "ICJ rules on Myanmar"),
    ("EVENING", "House confirmed 258–173"),
    ("NIGHT", "Alcaraz wins ATP title"),
]

BRIEFS = [
    "Houthi missile intercepted", "Swimmer crosses Hormuz",
    "Talks on killer AI at the UN", "US frees more UFO footage",
    "Albanese: COP31 a hard era", "Ship bound for Russia towed",
    "Drone suspected in Benghazi", "UK–EU reset 'landmark'",
    "Marches in Lisbon on costs", "Myanmar junta slams ASEAN",
    "Rebels trapped in Cameroon", "Lion loose in Türkiye",
    "Nepal's Shah meets Modi", "India–Bulgaria IMEC talks",
    "Guru Nanak Jayanti marked", "UP drill in 75 districts",
    "7 found, 50 lost in Indonesia", "Famous win chased by India",
    "India take ODI series 3–2", "Snooker: Anupama retains",
    "World Chess draws fans", "MP Wadkute dies in Delhi",
    "Kota bus tragedy: 9 dead", "Tata Steel sells pipe unit",
    "SpiceJet audit; IndiGo 65.9%", "IFFI hosts BRICS table",
    "Trump criticises Schumer",
]
BRIEFS_B = ["Alcaraz beats Zverev in Turin"] + BRIEFS

REGSTRIP = [("EUROPE", 10), ("SOUTH ASIA", 12), ("NORTH AMERICA", 5), ("MIDDLE EAST", 4),
            ("GLOBAL", 3), ("SE ASIA", 3), ("AFRICA", 2), ("ASIA-PACIFIC", 1)]

MAP = [
    "                                                              ",
    "        ####   ###                                            ",
    "     ######## ######        ##  #########  ##                 ",
    "    ##########  ###        #####################  ####        ",
    "     ########            #############################        ",
    "      ######              ###  ##################  ##         ",
    "       ####   ##           ##   ################              ",
    "       ###   ####               ##############      ###       ",
    "        ##    #####              ##########        #####      ",
    "             ######               ########          ###       ",
    "              #####                ######                     ",
    "              ####                  ####        ##            ",
    "              ###                   ##         ####           ",
    "              ##                                ##            ",
    "              #                                               ",
    "                                                              ",
    "                                          ##                  ",
    "                                         ####                 ",
    "                                                              ",
]
PINS = {1: (30, 5), 2: (36, 8), 3: (33, 6), 4: (34, 5), 5: (34, 6), 6: (37, 9),
        7: (33, 3), 8: (11, 6), 9: (44, 10), 10: (56, 17), 11: (9, 6), 12: (11, 7), 13: (31, 6)}

# ---------------------------------------------------------------- scenes
def scene(d, box, key, tint):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=tint)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if key == "gold":
        for dx, dy in [(-38, 6), (0, 6), (38, 6), (-19, -8), (19, -8)]:
            d.polygon([(cx + dx - 15, cy + dy + 8), (cx + dx + 15, cy + dy + 8),
                       (cx + dx + 10, cy + dy - 4), (cx + dx - 10, cy + dy - 4)], fill=(212, 164, 32))
        d.ellipse([cx + 52, cy - 16, cx + 76, cy + 8], fill=(226, 186, 60), outline=(150, 110, 10), width=2)
        d.text((cx + 59, cy - 13), "$", font=fb(15), fill=(90, 64, 4))
    elif key == "radar":
        d.line([x0 + 14, y1 - 4, cx, cy - 6], fill=INK, width=3)
        d.arc([cx - 6, cy - 26, cx + 34, cy + 14], 200, 320, fill=INK, width=3)
        for r in (10, 18, 26):
            d.arc([cx + 20 - r, cy - 4 - r, cx + 20 + r, cy - 4 + r], 180, 300, fill=RED, width=2)
        d.ellipse([cx + 16, cy - 8, cx + 24, cy], fill=RED)
    elif key == "climate":
        d.ellipse([cx - 28, y0 + 2, cx + 28, y1 - 2], outline=(28, 118, 88), width=3)
        d.arc([cx - 28, y0 + 2, cx + 28, y1 - 2], 20, 200, fill=(28, 118, 88), width=3)
        d.polygon([(cx + 20, cy - 6), (cx + 32, cy - 12), (cx + 30, cy + 2)], fill=(90, 160, 60))
    elif key == "rubble":
        d.polygon([(x0 + 8, y1 - 4), (cx - 6, cy - 10), (cx + 16, y1 - 4)], fill=(120, 104, 84))
        d.polygon([(cx + 2, y1 - 4), (cx + 30, cy - 16), (x1 - 8, y1 - 4)], fill=(96, 82, 64))
        d.ellipse([cx - 4, cy - 2, cx + 8, cy + 10], fill=(226, 178, 128))
        d.line([cx + 2, cy + 10, cx + 2, y1 - 6], fill=INK, width=3)
    elif key == "building":
        d.rectangle([cx - 26, cy - 16, cx + 26, cy + 12], fill=(104, 112, 124))
        for r in range(2):
            for c in range(4):
                d.rectangle([cx - 20 + c * 12, cy - 11 + r * 11, cx - 13 + c * 12, cy - 4 + r * 11], fill=(250, 220, 130))
        d.polygon([(cx + 10, cy - 16), (cx + 34, cy - 4), (cx + 10, cy - 2)], fill=(70, 76, 88))
    elif key == "tanker":
        hb = y1 - 3
        d.polygon([(x0 + 10, hb), (x1 - 16, hb), (x1 - 28, hb - 9), (x0 + 20, hb - 9)], fill=(60, 60, 66))
        d.rectangle([cx - 30, hb - 20, cx + 34, hb - 9], fill=(140, 60, 40))
        fh = min(16, (hb - 20) - y0)
        d.polygon([(cx - 2, hb - 20), (cx + 6, hb - 20 - fh), (cx + 12, hb - 20)], fill=(232, 120, 30))
        d.polygon([(cx + 12, hb - 20), (cx + 18, hb - 20 - fh + 4), (cx + 23, hb - 20)], fill=(240, 170, 40))
    elif key == "ship":
        hb = y1 - 3
        d.polygon([(x0 + 12, hb), (x1 - 12, hb), (x1 - 24, hb - 9), (x0 + 22, hb - 9)], fill=(52, 64, 84))
        d.rectangle([cx - 6, hb - 19, cx + 20, hb - 9], fill=(110, 118, 130))
        fh = min(14, (hb - 9) - y0)
        d.polygon([(cx - 22, hb - 9), (cx - 15, hb - 9 - fh), (cx - 8, hb - 9)], fill=(238, 130, 34))
        d.polygon([(cx - 32, hb - 9), (cx - 27, hb - 9 - fh + 3), (cx - 21, hb - 9)], fill=(246, 182, 52))
    elif key == "capitol":
        d.polygon([(cx - 34, cy + 2), (cx + 34, cy + 2), (cx, cy - 20)], fill=(240, 236, 224))
        d.rectangle([cx - 38, cy + 4, cx + 38, cy + 10], fill=(240, 236, 224))
        for i in range(5):
            d.rectangle([cx - 32 + i * 15, cy + 10, cx - 27 + i * 15, cy + 18], fill=(240, 236, 224))
    elif key == "scales":
        d.line([cx, cy - 16, cx, cy + 14], fill=INK, width=3)
        d.line([cx - 26, cy - 10, cx + 26, cy - 10], fill=INK, width=3)
        for sgn in (-1, 1):
            d.polygon([(cx + sgn * 26, cy - 10), (cx + sgn * 16, cy + 6), (cx + sgn * 36, cy + 6)], outline=INK, width=2)
        d.rectangle([cx - 12, cy + 14, cx + 12, cy + 18], fill=INK)
    elif key == "cricket":
        d.polygon([(cx - 22, cy + 14), (cx - 12, cy - 16), (cx - 2, cy - 13), (cx - 10, cy + 16)], fill=(196, 150, 84))
        d.ellipse([cx + 12, cy - 2, cx + 30, cy + 16], fill=(178, 34, 44))
        d.arc([cx + 14, cy, cx + 28, cy + 14], 90, 270, fill=WHITE, width=1)
    elif key == "bomb":
        d.ellipse([cx - 18, cy - 8, cx + 18, cy + 16], fill=(52, 54, 60))
        d.line([cx + 8, cy - 8, cx + 22, cy - 20], fill=INK, width=3)
        for a in range(0, 360, 45):
            ex = cx + 26 + int(9 * math.cos(math.radians(a)))
            ey = cy - 24 + int(9 * math.sin(math.radians(a)))
            d.line([cx + 26, cy - 24, ex, ey], fill=(232, 130, 30), width=2)
    elif key == "database":
        d.rectangle([cx - 24, cy - 14, cx + 24, cy + 14], outline=INK, width=3)
        d.line([cx - 24, cy, cx + 24, cy], fill=INK, width=2)
        d.line([cx - 24, cy - 7, cx + 24, cy - 7], fill=SILVER, width=2)
        d.line([cx - 24, cy + 7, cx + 24, cy + 7], fill=SILVER, width=2)
        d.polygon([(cx + 14, cy - 20), (cx + 22, cy - 8), (cx + 14, cy - 10)], fill=RED)
    elif key == "tennis":
        d.ellipse([cx - 14, cy - 12, cx + 16, cy + 18], outline=INK, width=3)
        d.line([cx + 10, cy + 12, cx + 26, cy + 24], fill=INK, width=4)
        d.ellipse([cx - 34, cy + 2, cx - 18, cy + 18], fill=(168, 204, 60))
    else:
        d.ellipse([cx - 16, cy - 12, cx + 16, cy + 12], outline=INK, width=3)

# ---------------------------------------------------------------- layout
def dotted_map(d, x, y, w_, h_, pinset):
    cols, rows = 62, 19
    sx, sy = w_ / cols, h_ / rows
    for r, row in enumerate(MAP):
        for c, ch in enumerate(row):
            if ch == "#":
                px, py = x + c * sx, y + r * sy
                d.ellipse([px, py, px + 2.6, py + 2.6], fill=(150, 138, 108))
    for n, (c, r) in PINS.items():
        if n not in pinset:
            continue
        px, py = x + c * sx, y + r * sy
        d.ellipse([px - 5, py - 5, px + 6, py + 6], fill=RED)
        s = str(n)
        fnt = fb(8)
        d.text((px - tw(d, s, fnt) / 2, py - 4), s, font=fnt, fill=WHITE)

def header(d):
    d.rectangle([0, 0, W, 20], fill=INK)
    f1 = fb(12)
    d.text((14, 4), "THE DAY AT A GLANCE", font=f1, fill=SILVER_L)
    kick = "40 STORIES · 8 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    d.text((W - 14 - tw(d, kick, f1), 4), kick, font=f1, fill=SILVER_L)
    y = 24
    name = "THE DAY AT A GLANCE"
    fn = F(PF_BOLD, 20)
    d.text(((W - tw(d, name, fn)) / 2, y), name, font=fn, fill=INK2)
    y += 24
    date = "Monday 23 November 2026"
    fd = F(PF_BLACK, 74)
    d.text(((W - tw(d, date, fd)) / 2, y), date, font=fd, fill=INK)
    y += 82
    sub = "Gold slides to $3,538 an ounce  ·  IRGC claims Patriot radars hit in Bahrain  ·  COP31 ends without a deal"
    fs = fb(14)
    d.text(((W - tw(d, sub, fs)) / 2, y), sub, font=fs, fill=RED)
    y += 19
    d.line([14, y, W - 14, y], fill=INK, width=2)
    return y + 4

def region_strip(d, y):
    x = 14
    fnt = fb(12)
    for name, cnt in REGSTRIP:
        label = "%s %d" % (name, cnt)
        wch = tw(d, label, fnt) + 14
        d.rectangle([x, y, x + wch, y + 18], fill=REG[name])
        d.text((x + 7, y + 3), label, font=fnt, fill=WHITE)
        x += wch + 6
    return y + 22

def timeline(d, y):
    f1, f2 = fb(12), fr(12)
    x = 14
    seg = (W - 28) / len(TL)
    for t, ev in TL:
        d.text((x, y), t, font=f1, fill=INK)
        d.text((x, y + 13), ev, font=f2, fill=INK2)
        x += seg
    d.line([14, y + 28, W - 14, y + 28], fill=SILVER, width=1)
    return y + 31

CHIPCOL = {"REPORTED": (42, 84, 140), "CLAIM": (178, 60, 40), "DENIAL": (150, 44, 60),
           "ONGOING": (196, 120, 20), "OFFICIAL": (28, 118, 88), "CONFIRMED": (28, 118, 88),
           "ON RECORD": (96, 96, 96)}

def _card(d, box, c, kind, ft, ff, title_lh):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PANEL, outline=SILVER, width=1)
    d.rectangle([x0, y0, x0 + 5, y1], fill=REG[c["region"]])
    ix = x0 + 12
    iw = x1 - ix - 8
    fh = fb(13)
    num = "%d" % c["n"]
    d.ellipse([ix, y0 + 5, ix + 16, y0 + 21], fill=INK)
    d.text((ix + (16 - tw(d, num, fb(11))) / 2, y0 + 7), num, font=fb(11), fill=WHITE)
    d.text((ix + 21, y0 + 6), c["loc"], font=fh, fill=INK2)
    iy = y0 + 24
    ih = 30 if kind != "grid" else 20
    scene(d, (ix, iy, x1 - 8, iy + ih), c["scene"], PANEL2)
    y = iy + ih + 4
    fc = fb(11)
    fcat = fb(10)
    chip = c["chip"]
    cw_ = tw(d, chip, fc) + 10
    d.rectangle([ix, y, ix + cw_, y + 14], fill=CHIPCOL[chip])
    d.text((ix + 5, y + 2), chip, font=fc, fill=WHITE)
    d.text((ix + cw_ + 7, y + 2), c["cat"], font=fcat, fill=INK2)
    y += 17
    y = text_block(d, ix, y, c["title"], ft, INK, iw, title_lh, max_lines=2)
    y = text_block(d, ix, y + 1, c["fact"], ff, INK2, iw, 16, max_lines=2)
    d.text((ix, y1 - 14), "Source: " + c["src"], font=fr(11), fill=INK2)

def lead(d, box, c, big=False):
    ft = fb(32) if big else fb(28)
    ff = fr(15)
    _card(d, box, c, "big" if big else "lead", ft, ff, 35 if big else 30)

def mini(d, box, c):
    ft = fb(28)
    ff = fr(15)
    _card(d, box, c, "grid", ft, ff, 30)

def numbers_box(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=INK)
    d.text((x0 + 10, y0 + 5), "THE DAY IN NUMBERS", font=fb(13), fill=SILVER_L)
    fn, fl = F(PF_BOLD, 26), fb(10)
    colw = (x1 - x0 - 20) // 3
    for i, (num, lab) in enumerate(NUMS):
        cx = x0 + 10 + (i % 3) * colw
        cy = y0 + 22 + (i // 3) * 46
        d.text((cx, cy), num, font=fn, fill=(240, 226, 180))
        ly = cy + 28
        for ln in wrap(d, lab, fl, colw - 4)[:1]:
            d.text((cx, ly), ln, font=fl, fill=SILVER_L)
            ly += 11

def numbers_rail(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=INK)
    d.text((x0 + 10, y0 + 6), "THE DAY IN NUMBERS", font=fb(13), fill=SILVER_L)
    fn, fl = F(PF_BOLD, 26), fb(10)
    y = y0 + 26
    for num, lab in NUMS:
        d.text((x0 + 10, y), num, font=fn, fill=(240, 226, 180))
        d.text((x0 + 14 + tw(d, num, fn) + 8, y + 13), lab, font=fl, fill=SILVER_L)
        y += 25

def datecheck_box(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(250, 240, 232), outline=RED, width=2)
    d.text((x0 + 9, y0 + 5), "DATE CHECK — NOT TODAY'S NEWS", font=fb(12), fill=RED)
    fnt = fr(11)
    y = y0 + 21
    for item in DATECHECK:
        d.text((x0 + 9, y), "✕ " + item, font=fnt, fill=INK)
        y += 11
    d.text((x0 + 9, y + 2), "→ only its 23 Nov update is news (story 30).", font=fr(10), fill=RED)

def map_box(d, box, pinset):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PANEL, outline=SILVER, width=1)
    d.text((x0 + 9, y0 + 5), "WHERE IT HAPPENED — pins = card numbers", font=fb(12), fill=INK)
    d.text((x0 + 9, y0 + 19), "Land in dots · pins mark card numbers", font=fr(10), fill=INK2)
    dotted_map(d, x0 + 12, y0 + 32, x1 - x0 - 24, y1 - y0 - 36, pinset)

def also_band(d, y, items, start):
    d.rectangle([14, y, W - 14, y + 92], fill=PANEL2)
    d.text((24, y + 4), "ALSO ON MONDAY — STORIES %d–%d" % (start, start + len(items) - 1), font=fb(13), fill=INK)
    fnt = fsr(13)
    cols = 5
    colw = (W - 48) / cols
    rows = (len(items) + cols - 1) // cols
    for i, it in enumerate(items):
        cx = 24 + (i // rows) * colw
        cy = y + 23 + (i % rows) * 12
        d.text((cx, cy), "%d" % (start + i), font=fb(12), fill=RED)
        d.text((cx + 20, cy), it, font=fnt, fill=INK)
    return y + 100

def footer(d, y):
    f1 = fr(11)
    l1 = "HOW SURE: REPORTED = reported by named outlets · CLAIM = one side's account, labelled as such · ONGOING = still developing · OFFICIAL = on the record from an authority."
    l2 = "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. · Original drawings."
    d.text(((W - tw(d, l1, f1)) / 2, y), l1, font=f1, fill=INK2)
    d.text(((W - tw(d, l2, f1)) / 2, y + 12), l2, font=f1, fill=INK2)

def build(variant):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = header(d)
    y = region_strip(d, y)
    y = timeline(d, y)
    top = y + 2
    if variant == "A":
        lh_ = 186
        lead(d, (14, top, 444, top + lh_), CARDS[0], big=True)
        lead(d, (452, top, 719, top + lh_), CARDS[1])
        lead(d, (727, top, 1010, top + lh_), CARDS[2])
        gy = top + lh_ + 8
        gw, gh, gap = 192, 170, 8
        for i, c in enumerate(CARDS[3:]):
            cx = 14 + (i % 5) * (gw + gap)
            cy = gy + (i // 5) * (gh + gap)
            mini(d, (cx, cy, cx + gw, cy + gh), c)
        by = gy + 2 * gh + gap + 8
        numbers_box(d, (14, by, 330, by + 112))
        map_box(d, (338, by, 660, by + 112), set(range(1, 14)))
        datecheck_box(d, (668, by, 1010, by + 112))
        ay = by + 118
        fy = also_band(d, ay, BRIEFS, 14)
        footer(d, fy + 2)
    else:
        lh_ = 186
        lead(d, (14, top, 444, top + lh_), CARDS[0], big=True)
        lead(d, (452, top, 719, top + lh_), CARDS[1])
        numbers_rail(d, (727, top, 1010, top + lh_))
        gy = top + lh_ + 8
        gw, gh, gap = 192, 170, 8
        for i, c in enumerate(CARDS[2:12]):
            cx = 14 + (i % 5) * (gw + gap)
            cy = gy + (i // 5) * (gh + gap)
            mini(d, (cx, cy, cx + gw, cy + gh), c)
        by = gy + 2 * gh + gap + 8
        map_box(d, (14, by, 500, by + 112), set(range(1, 13)))
        datecheck_box(d, (508, by, 1010, by + 112))
        ay = by + 118
        fy = also_band(d, ay, BRIEFS_B, 13)
        footer(d, fy + 2)
    return img

if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = "/tmp/ni23g4-akun14-%s.png" % v.lower()
    build(v).save(out, optimize=True)
    print(out)
