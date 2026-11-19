#!/usr/bin/env python3
"""Paint the front page of Thursday 19 November 2026.

One 1024x1024 newspaper front page, drawn from scratch with Pillow:
a masthead naming the day, one big lead story (the first Trump-Xi-Putin
trilateral in Shenzhen), four second-tier stories with small flat
illustrations, a two-column "Around the world" list of 30 more stories
grouped by region, and a "Day in numbers" strip. 35 stories in all.

Everything is fixed: no network, no clock, no randomness except a
fixed-seed speckle for lit windows, so re-running this script writes
byte-identical output.
"""

import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (245, 240, 230)
INK = (26, 26, 26)
RED = (163, 22, 33)
MUTED = (110, 104, 92)
RULE = (26, 26, 26)
NAVY = (28, 43, 74)
SKY_TOP = (58, 44, 96)
SKY_MID = (176, 92, 66)
SKY_LOW = (232, 148, 72)
GOLD = (217, 164, 65)
PANEL = (233, 226, 210)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines, return the y just below the last one."""
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def lit_windows(draw, rng, x0, y0, x1, y1, cols, rows):
    """A grid of small windows, some lit gold, some dark."""
    if cols <= 0 or rows <= 0:
        return
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    for r in range(rows):
        for c in range(cols):
            wx = x0 + c * cw + cw * 0.22
            wy = y0 + r * ch + ch * 0.22
            ww = cw * 0.56
            wh = ch * 0.56
            col = GOLD if rng.random() < 0.55 else (52, 58, 84)
            draw.rectangle([wx, wy, wx + ww, wy + wh], fill=col)


def flag_us(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        col = (178, 34, 52) if i % 2 == 0 else (244, 244, 244)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=col)
    draw.rectangle([x, y, x + w * 0.4, y + stripe * 7], fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            cx = x + 6 + c * (w * 0.4 - 10) / 5.0
            cy = y + 5 + r * (stripe * 7 - 8) / 4.0
            draw.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    def star(cx, cy, r):
        pts = []
        import math
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.42
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=(255, 222, 0))
    star(x + w * 0.18, y + h * 0.28, 7)
    star(x + w * 0.38, y + h * 0.16, 3)
    star(x + w * 0.44, y + h * 0.30, 3)
    star(x + w * 0.40, y + h * 0.46, 3)
    star(x + w * 0.28, y + h * 0.52, 3)


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def hero(draw, x, y, w, h):
    """Shenzhen at dusk: gradient sky, skyline, moon, three flags."""
    rng = random.Random(19)
    for i in range(h):
        t = i / max(1, h - 1)
        if t < 0.55:
            a, b = SKY_TOP, SKY_MID
            u = t / 0.55
        else:
            a, b = SKY_MID, SKY_LOW
            u = (t - 0.55) / 0.45
        col = tuple(int(a[k] + (b[k] - a[k]) * u) for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=col)
    # full moon
    mx, my, mr = x + w - 78, y + 42, 24
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(245, 236, 200))
    # far skyline
    base = y + h - 74
    bx = x
    while bx < x + w:
        bw = rng.randint(34, 66)
        bh = rng.randint(52, 128)
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(44, 40, 74))
        lit_windows(draw, rng, bx + 3, base - bh + 6, bx + bw - 3, base - 6, 3, max(2, bh // 22))
        bx += bw + 4
    # near tower
    tx = x + w * 0.60
    draw.rectangle([tx, y + 34, tx + 44, base], fill=(24, 22, 48))
    for i in range(9):
        wy = y + 44 + i * 15
        draw.rectangle([tx + 7, wy, tx + 37, wy + 7], fill=GOLD)
    # water
    draw.rectangle([x, base, x + w, y + h - 26], fill=(22, 32, 66))
    for i in range(4):
        wy = base + 8 + i * 9
        draw.line([(x + 14, wy), (x + w - 14, wy)], fill=(84, 106, 150), width=2)
    # ground strip with three flags
    gy = y + h - 26
    draw.rectangle([x, gy, x + w, y + h], fill=(30, 26, 40))
    fw, fh = 52, 32
    fx = x + 26
    for fn in (flag_us, flag_cn, flag_ru):
        draw.rectangle([fx + fw / 2 - 1, gy - 26, fx + fw / 2 + 1, gy], fill=(220, 220, 220))
        fn(draw, fx, gy - 26 - fh + 8, fw, fh)
        fx += fw + 34
    draw.text((x + 210, gy + 3), "SHENZHEN · APEC SUMMIT", font=font(SANS_B, 14), fill=(200, 196, 180))


def mini_chart(draw, x, y, w, h):
    """Rising bars for the IPO story."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 38, 66))
    bars = [0.30, 0.45, 0.42, 0.62, 0.58, 0.85, 1.0]
    bw = w / len(bars)
    for i, v in enumerate(bars):
        bh = v * (h - 26)
        col = GOLD if i == len(bars) - 1 else (86, 140, 190)
        draw.rectangle([x + i * bw + 5, y + h - 12 - bh, x + (i + 1) * bw - 5, y + h - 12], fill=col)
    draw.text((x + 8, y + 6), "$81.3bn", font=font(SANS_B, 20), fill=(255, 255, 255))


def mini_tank(draw, x, y, w, h):
    """Tank silhouette on dunes for the Gaza story."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 186, 138))
    draw.ellipse([x + w - 52, y + 10, x + w - 14, y + 48], fill=(240, 214, 160))
    draw.polygon([(x, y + h), (x + w * 0.45, y + h * 0.55), (x + w, y + h * 0.72),
                  (x + w, y + h), ], fill=(186, 150, 96))
    draw.rectangle([x + w * 0.16, y + h - 42, x + w * 0.62, y + h - 26], fill=(74, 72, 66))
    draw.rectangle([x + w * 0.30, y + h - 58, x + w * 0.52, y + h - 40], fill=(74, 72, 66))
    draw.rectangle([x + w * 0.50, y + h - 52, x + w * 0.88, y + h - 48], fill=(74, 72, 66))
    for cx in (x + w * 0.24, x + w * 0.38, x + w * 0.52):
        draw.ellipse([cx - 7, y + h - 24, cx + 7, y + h - 10], fill=(52, 50, 46))


def mini_bridge(draw, x, y, w, h):
    """Bridge span with smoke for the Crimea story."""
    draw.rectangle([x, y, x + w, y + h], fill=(30, 52, 88))
    for sx, sy, sr in ((x + w * 0.30, y + 16, 10), (x + w * 0.38, y + 8, 13), (x + w * 0.47, y + 18, 9)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 152, 160))
    draw.rectangle([x, y + h * 0.62, x + w, y + h * 0.68], fill=(16, 20, 34))
    for px in (x + w * 0.22, x + w * 0.52, x + w * 0.80):
        draw.rectangle([px - 3, y + h * 0.30, px + 3, y + h * 0.66], fill=(16, 20, 34))
    draw.line([(x + 8, y + h * 0.30), (x + w * 0.22, y + h * 0.62)], fill=(120, 124, 140), width=2)
    draw.line([(x + w * 0.22, y + h * 0.30), (x + w * 0.52, y + h * 0.62)], fill=(120, 124, 140), width=2)
    draw.line([(x + w * 0.52, y + h * 0.30), (x + w * 0.80, y + h * 0.62)], fill=(120, 124, 140), width=2)
    draw.line([(x + w * 0.80, y + h * 0.30), (x + w - 8, y + h * 0.62)], fill=(120, 124, 140), width=2)
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(14, 26, 52))
    for i in range(5):
        wx = x + 10 + i * 16
        draw.line([(wx, y + h - 8), (wx + 26, y + h - 8)], fill=(70, 96, 140), width=2)


def mini_capitol(draw, x, y, w, h):
    """Capitol dome for the Speaker story."""
    draw.rectangle([x, y, x + w, y + h], fill=(206, 220, 232))
    draw.ellipse([x + w - 46, y + 8, x + w - 10, y + 44], fill=(244, 226, 160))
    cx = x + w / 2
    draw.rectangle([cx - 52, y + h - 26, cx + 52, y + h - 12], fill=(120, 118, 112))
    draw.rectangle([cx - 40, y + h - 44, cx + 40, y + h - 26], fill=(140, 138, 130))
    draw.rectangle([cx - 26, y + h - 62, cx + 26, y + h - 44], fill=(150, 148, 140))
    draw.pieslice([cx - 24, y + h - 92, cx + 24, y + h - 44], 180, 360, fill=(150, 148, 140))
    draw.rectangle([cx - 2, y + h - 108, cx + 2, y + h - 90], fill=(120, 118, 112))
    for dx in (-46, -28, -10, 8, 26, 44):
        draw.rectangle([cx + dx - 5, y + h - 26, cx + dx + 5, y + h - 12], fill=(96, 94, 88))


LEAD = {
    "kicker": "ASIA · APEC",
    "headline": "Trump, Xi and Putin sit down in Shenzhen",
    "deck": "First-ever three-way summit opens at APEC — Xi hugs Trump on the tarmac as leaders gather.",
}

SECOND = [
    {
        "kicker": "BUSINESS",
        "headline": "Anthropic raises $81.3bn in biggest IPO ever",
        "deck": "Claude-maker prices shares at $83; debut tops a $1.4tn value.",
        "art": mini_chart,
    },
    {
        "kicker": "MIDDLE EAST",
        "headline": "Israeli tanks cross ceasefire line in Gaza",
        "deck": "Rare ground push into central Gaza as floods deepen the crisis.",
        "art": mini_tank,
    },
    {
        "kicker": "EUROPE",
        "headline": "Crimean Bridge hit again",
        "deck": "Traffic halted after a new attack on the Russia–Crimea link.",
        "art": mini_bridge,
    },
    {
        "kicker": "AMERICA",
        "headline": "Jeffries in line to be first Black Speaker",
        "deck": "Democrats nominate Hakeem Jeffries for the gavel.",
        "art": mini_capitol,
    },
]

# Around the world: (region, headline) — 30 items, 15 per column.
AROUND = [
    ("ASIA", "India, Japan hold 2+2 defence talks in Tokyo"),
    ("ASIA", "Cyclone Akvan bears down on India's east coast"),
    ("ASIA", "Indonesia raises rates as rupiah hits record low"),
    ("ASIA", "Seoul backs possible Trump–Kim talks at APEC"),
    ("ASIA", "Bangladesh's Rooppur plant starts trial power"),
    ("ASIA", "India wins record ninth U-19 Asia Cup"),
    ("EUROPE", "EU proposes €45bn loan for Ukraine"),
    ("EUROPE", "France enters fourth weekend of cost protests"),
    ("EUROPE", "Mélenchon could win French presidency: minister"),
    ("EUROPE", "Europe stocks hit two-week low; UK −1.3%"),
    ("EUROPE", "Climber survives 100-metre fall in Alps"),
    ("MIDDLE EAST", "US and Iran trade fire again in the Gulf"),
    ("MIDDLE EAST", "Australia sanctions Israeli settlers"),
    ("MIDDLE EAST", "Tanker sunk off Bulgaria 'hit by projectiles'"),
    ("MIDDLE EAST", "Iraq jails six French citizens over IS ties"),
    ("AMERICAS", "Peltola wins Alaska; Senate now 56–44"),
    ("AMERICAS", "US proposes tougher green-card rules"),
    ("AMERICAS", "Fed minutes point to further rate hikes"),
    ("AMERICAS", "Wall Street mixed; Dow −1.1%, Nasdaq +0.4%"),
    ("AMERICAS", "Oil falls; gold hits 14-month low"),
    ("AMERICAS", "US loses measles-free status after 26 years"),
    ("AMERICAS", "MLB salary-cap standoff; lockout looms"),
    ("AMERICAS", "Hegseth vows deeper US–Venezuela ties"),
    ("TECH & SCIENCE", "Voyager 1 reaches one light-day from Earth"),
    ("TECH & SCIENCE", "Nvidia halts H-series chip shipments to China"),
    ("TECH & SCIENCE", "Wellington IT breach hits 40 Irish credit unions"),
    ("CULTURE & SPORT", "Van Gogh sells for record $190.4m"),
    ("CULTURE & SPORT", "GTA VI begins global rollout"),
    ("CULTURE & SPORT", "Haaland fires Norway to Nations League quarters"),
    ("CULTURE & SPORT", "Duckett's 133 puts England on top in ODI"),
]

NUMBERS = [
    ("35", "STORIES"),
    ("7", "REGIONS"),
    ("$81.3bn", "BIGGEST IPO EVER"),
    ("1", "LIGHT-DAY: VOYAGER 1"),
    ("3", "LEADERS, ONE TABLE"),
]


def paint():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    rx = W - mx

    # ---- Masthead -------------------------------------------------
    d.text((mx, 22), "THE WORLD", font=font(SERIF, 62), fill=INK)
    d.text((rx, 30), "THURSDAY, 19 NOVEMBER 2026",
           font=font(SANS_B, 25), fill=INK, anchor="ra")
    d.text((rx, 62), "35 STORIES  ·  7 REGIONS  ·  ONE DAY",
           font=font(SANS_B, 15), fill=MUTED, anchor="ra")
    d.rectangle([mx, 98, rx, 102], fill=RED)

    # ---- Lead -----------------------------------------------------
    ly = 114
    hero_w, hero_h = 556, 262
    hero(d, mx, ly, hero_w, hero_h)
    tx = mx + hero_w + 24
    tw = rx - tx
    y = ly + 2
    d.text((tx, y), LEAD["kicker"], font=font(SANS_B, 17), fill=RED)
    y += 26
    y = text_block(d, tx, y, wrap(d, LEAD["headline"], font(SERIF, 41), tw),
                   font(SERIF, 41), leading=47)
    y += 8
    text_block(d, tx, y, wrap(d, LEAD["deck"], font(SANS, 18), tw),
               font(SANS, 18), leading=23)
    d.rectangle([mx, 384, rx, 388], fill=RULE)

    # ---- Second tier: four across ---------------------------------
    sy = 398
    col_w = (rx - mx - 3 * 14) // 4
    for i, s in enumerate(SECOND):
        x = mx + i * (col_w + 14)
        s["art"](d, x, sy, col_w, 88)
        y = sy + 94
        d.text((x, y), s["kicker"], font=font(SANS_B, 14), fill=RED)
        y += 18
        y = text_block(d, x, y, wrap(d, s["headline"], font(SERIF, 19), col_w),
                       font(SERIF, 19), leading=21)
        y += 4
        text_block(d, x, y, wrap(d, s["deck"], font(SANS, 13), col_w),
                   font(SANS, 13), leading=15)
    d.rectangle([mx, 618, rx, 622], fill=RULE)

    # ---- Around the world -----------------------------------------
    y = 630
    d.text((mx, y), "AROUND THE WORLD", font=font(SANS_B, 18), fill=INK)
    d.text((rx, y), "30 MORE STORIES", font=font(SANS_B, 15), fill=MUTED, anchor="ra")
    y += 26
    col_w2 = (rx - mx - 24) // 2
    half = len(AROUND) // 2
    for ci in range(2):
        cx = mx + ci * (col_w2 + 24)
        cy = y
        last_region = None
        for region, head in AROUND[ci * half:(ci + 1) * half]:
            if region != last_region:
                if last_region is not None:
                    cy += 3
                d.text((cx, cy), region, font=font(SANS_B, 13), fill=RED)
                cy += 17
                last_region = region
            d.text((cx, cy), "▪ ", font=font(SANS_B, 13), fill=RED)
            d.text((cx + 14, cy), head, font=font(SANS_B, 13), fill=INK)
            cy += 14
    d.rectangle([mx, 932, rx, 936], fill=RULE)

    # ---- Day in numbers -------------------------------------------
    ny = 946
    n_w = (rx - mx - 4 * 10) // 5
    for i, (num, lab) in enumerate(NUMBERS):
        x = mx + i * (n_w + 10)
        d.rectangle([x, ny, x + n_w, ny + 40], fill=PANEL)
        d.text((x + n_w / 2, ny + 2), num, font=font(SERIF, 19),
               fill=INK, anchor="ma")
        d.text((x + n_w / 2, ny + 23), lab, font=font(SANS_B, 10),
               fill=MUTED, anchor="ma")

    # ---- Footer ---------------------------------------------------
    d.text((mx, 996), "All events reported Thursday 19 November 2026  ·  Sources: Reuters, AP, AFP, BBC, Al Jazeera",
           font=font(SANS, 12), fill=MUTED)
    d.text((rx, 996), "THE WORLD IN ONE DAY", font=font(SANS_B, 12),
           fill=MUTED, anchor="ra")
    return img


def main():
    img = paint()
    img.save(OUT, optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
