#!/usr/bin/env python3
"""Render the Round 5 front page for news-image-20261121.

A one-day newspaper: "Saturday 21 November 2026" — 35 dated stories across
7 regions, every one numbered, dated and sourced. Same kind of paper as the
Top 1 entry (samatch-we), but cleaner: bigger numerals in the facts strip,
uniform card geometry, a more accurate world map, crisper illustrations,
no cramped or clipped text.

Deterministic: no randomness, no timestamps, no network. Running this file
twice must produce byte-identical entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (169, 22, 22)
RED_DARK = (140, 18, 18)
GRAY = (90, 86, 78)
LINE = (180, 172, 152)
CARD_BG = (255, 255, 255)
NAVY = (30, 58, 95)

F = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


SERIF = "LiberationSerif-Regular.ttf"
SERIF_B = "LiberationSerif-Bold.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w; returns list of lines (never empty)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def draw_wrapped(draw, x, y, text, fnt, max_w, max_lines, fill, leading=None):
    """Draw wrapped text, at most max_lines; truncate the last line with
    an ellipsis if it still overflows. Returns the y just below the text."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " …", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " …"
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


# ---------------------------------------------------------------- stories
# (number, region, banner, location line, headline, body, source, lon, lat)
BIG = [
    (1, "ME", "COP31: OVERTIME", "1  ANTALYA, TÜRKIYE · CLIMATE",
     "Climate summit runs into Saturday with no deal",
     "COP31 missed its Friday close. A draft with no mention of fossil "
     "fuels split nearly 200 countries; a third text is promised.",
     "(AFP, Al Jazeera)", 30.7, 36.9),
    (2, "ME", "SAUDI: MISSILES", "2  RIYADH · JIZAN · WAR",
     "Five Houthi missiles shot down over Saudi Arabia",
     "The Saudi-led coalition said three were destroyed over Riyadh "
     "before dawn and two over Jizan, a day after it bombed Hodeidah port.",
     "(AFP, Dawn)", 46.7, 24.6),
    (3, "Americas", "PERU: QUAKE 6.7", "3  JUNÍN, PERU · EARTHQUAKE",
     "Magnitude 6.7 earthquake shakes central Peru",
     "The quake in Junín was felt in Lima and along the coast. Residents "
     "rushed into the streets; no casualties or major damage were reported.",
     "(USGS, IGP)", -75.2, -11.2),
]

SMALL = [
    (4, "Europe", "KYIV: WARNING", "4  KYIV · WAR",
     "Zelensky: Crimea bridge “will not stay”",
     "Russia has hit Ukraine’s bridges 109 times; Friday’s Kyiv barrage "
     "killed seven.",
     "(NBC)", 30.5, 50.5),
    (5, "ME", "HORMUZ: DRONE", "5  STRAIT OF HORMUZ · WAR",
     "Iran says it shot down a US drone",
     "IRGC claims its 58th MQ-9 kill over the Strait of Hormuz. No "
     "confirmation from Washington.",
     "(Press TV, ANI)", 56.5, 27.0),
    (6, "ME", "IRAN: URANIUM", "6  TEHRAN · DIPLOMACY",
     "Iran: uranium stock stays in the country",
     "Minister still sees “a fair solution” as talks continue.",
     "(Reuters, Tasnim)", 51.4, 35.7),
    (7, "Americas", "TRUMP: AI TAX", "7  WASHINGTON · TECHNOLOGY",
     "Trump vows tax on data centres abroad",
     "“Tremendous tax” penalty; no details yet.",
     "(Reuters)", -77.0, 38.9),
    (8, "Asia", "CHINA–JAPAN", "8  BEIJING · DIPLOMACY",
     "China tells Japan to “correct” Taiwan words",
     "Tokyo says its stance is unchanged.",
     "(Reuters)", 116.4, 39.9),
    (9, "Asia", "DAVAO: 146 SAFE", "9  DAVAO · AVIATION",
     "Jet lands safely after engine fire alert",
     "Air Niugini 767 diverts after midnight. All 146 aboard safe.",
     "(AP)", 125.6, 7.1),
    (10, "Oceania", "CANBERRA: AI", "10  CANBERRA · DIPLOMACY",
     "Australia and China agree to AI talks",
     "Albanese and Li Qiang agree a formal dialogue on AI in Beijing.",
     "(pm.gov.au)", 149.1, -35.3),
    (11, "Global", "BITCOIN: $58,174", "11  WORLD · MARKETS",
     "Bitcoin slides below $59,000 on Saturday",
     "Down 6.1% in a day to about $58,174 — its weakest since "
     "September 2024.",
     "(CoinMarketCap)", -30.0, 15.0),
    (12, "Americas", "RUSSELL: P1", "12  LAS VEGAS · FORMULA ONE",
     "Russell fastest in final Las Vegas practice",
     "1:34.041 in a damp, messy session. Verstappen sent to stewards "
     "after contact.",
     "(Formula 1)", -115.1, 36.2),
    (13, "Oceania", "RAHUL: 124*", "13  WELLINGTON · CRICKET",
     "Rahul hits a century against New Zealand",
     "124 not out at tea as India reach 344 for 2, replying to 368.",
     "(AFP)", 174.8, -41.3),
]

# Also-list: (number, place, text, source)
ALSO = [
    (14, "KRYVYI RIH", "Double strike kills 2, injures 42.", "Kyiv Independent"),
    (15, "COPENHAGEN", "Denmark expels Russian attaché over “plot”.", "Al Jazeera"),
    (16, "ANTALYA", "EU warns COP31 risks a “fossil summit”.", "AFP"),
    (17, "NATO", "Alliance condemns Poland airspace incursion.", "Vertical Bangladesh"),
    (18, "BASRA", "Fire at Hartha power plant kills 4, injures 30.", "Reuters"),
    (19, "YEMEN", "Houthis threaten Jeddah and Saudi Red Sea ports.", "Al Jazeera"),
    (20, "WASHINGTON", "Vance: Iran strikes were “the president’s call”.", "Reuters"),
    (21, "WASHINGTON", "Lawmaker threatens SpaceX’s funding.", "CNN"),
    (22, "MISSOURI", "Judge approves $7.25bn Roundup settlement.", "Reuters"),
    (23, "LOS ANGELES", "Jury convicts man of starting Palisades fire.", "Reuters"),
    (24, "VANCOUVER", "Canada rests defence in youth climate trial.", "AFP"),
    (25, "PYONGYANG", "Kim tours factories after no Trump meeting.", "AFP"),
    (26, "TAIPEI", "Budget and a cash payout are passed.", "Taipei Times"),
    (27, "BANGKOK", "Six-point plan on arsenic in two rivers.", "The Nation"),
    (28, "SEOUL", "Lee: speed is vital in the AI race.", "Reuters"),
    (29, "VIETNAM", "Parliament speeds land seizures.", "Reuters"),
    (30, "NEW DELHI", "Protests at Meta’s India offices.", "Reuters"),
    (31, "IPOH", "Malaysia beat South Korea 3–0 in hockey.", "RTM World"),
    (32, "SINGAPORE", "Singapore, China open free-trade upgrade talks.", "RTM World"),
    (33, "UNITED NATIONS", "States agree talks to curb “killer robots”.", "Reuters"),
    (34, "PORT LOUIS", "African rating agency talks to 15 states.", "Al Jazeera"),
    (35, "MELBOURNE", "Cummins keeps Australian captaincy.", "ABC"),
]

FACTS = [
    ("Day 13", "of a COP31 summit planned to close on day 12"),
    ("5", "missiles shot down over Riyadh and Jizan"),
    ("6.7", "magnitude of the quake in Junín, Peru"),
    ("146", "people safe after a jet’s emergency landing"),
    ("$58,174", "bitcoin early Saturday, down 6.1% in a day"),
    ("124*", "K L Rahul’s score at tea in Wellington"),
]

REGIONS = [
    ("EUROPE 5", (29, 78, 216)),
    ("ASIA 10", (185, 28, 28)),
    ("MIDDLE EAST 6", (180, 83, 9)),
    ("AFRICA 1", (109, 40, 217)),
    ("AMERICAS 8", (15, 118, 110)),
    ("OCEANIA 3", (21, 128, 61)),
    ("GLOBAL 2", (51, 65, 85)),
]


# ------------------------------------------------------------- illustrations
def illo_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 214))
    d.ellipse([x + 8, y + 6, x + 52, y + h - 6], fill=(59, 130, 200))
    d.ellipse([x + 18, y + 12, x + 30, y + 22], fill=(86, 160, 90))
    d.ellipse([x + 32, y + 26, x + 46, y + 38], fill=(86, 160, 90))
    d.ellipse([x + 20, y + 34, x + 28, y + 44], fill=(86, 160, 90))
    # thermometer
    d.rectangle([x + w - 26, y + 8, x + w - 18, y + h - 14], fill=(255, 255, 255),
                outline=RED, width=2)
    d.rectangle([x + w - 24, y + h - 22, x + w - 20, y + h - 16], fill=RED)
    d.ellipse([x + w - 30, y + h - 16, x + w - 14, y + h - 2], fill=RED)
    # clock
    d.ellipse([x + w - 58, y + 8, x + w - 34, y + 32], fill=(255, 255, 255),
              outline=INK, width=2)
    d.line([x + w - 46, y + 20, x + w - 46, y + 12], fill=INK, width=2)
    d.line([x + w - 46, y + 20, x + w - 40, y + 22], fill=INK, width=2)


def illo_saudi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for bx, bw, bh in [(6, 26, 22), (36, 18, 34), (58, 24, 18), (86, 20, 30),
                       (110, 26, 24), (140, 18, 36), (162, 24, 20)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(8, 12, 26))
        for wy in range(y + h - bh + 5, y + h - 4, 8):
            d.rectangle([x + bx + 4, wy, x + bx + 8, wy + 3], fill=(255, 214, 90))
    # missile arcs with starbursts
    for ax, ay in [(30, 16), (90, 8), (150, 18)]:
        for i in range(6):
            px = x + ax + i * 5
            py = y + ay + int(0.35 * i * i) - 6
            d.ellipse([px, py, px + 2, py + 2], fill=(255, 255, 255))
        d.ellipse([x + ax + 26, y + ay + 2, x + ax + 36, y + ay + 12],
                  fill=(255, 190, 60))
        d.line([x + ax + 31, y + ay - 2, x + ax + 31, y + ay + 16],
               fill=(255, 190, 60), width=2)
        d.line([x + ax + 27, y + ay + 7, x + ax + 35, y + ay + 7],
               fill=(255, 190, 60), width=2)


def illo_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    d.polygon([(x, y + h), (x + 40, y + 14), (x + 80, y + h)], fill=(150, 110, 70))
    d.polygon([(x + 60, y + h), (x + 110, y + 8), (x + 160, y + h)],
              fill=(120, 88, 54))
    # seismograph zigzag
    pts = []
    for i in range(21):
        px = x + 6 + i * (w - 12) / 20
        py = y + h - 26 + (10 if i % 2 else -10)
        pts.append((px, py))
    d.line(pts, fill=RED, width=3)
    d.rectangle([x + w - 40, y + h - 22, x + w - 12, y + h - 6],
                fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(x + w - 42, y + h - 22), (x + w - 26, y + h - 32),
               (x + w - 10, y + h - 22)], fill=RED_DARK)


def illo_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 2], fill=(59, 130, 200))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(255, 209, 60))
    d.rectangle([x + 6, y + h - 18, x + w - 6, y + h - 12], fill=(40, 40, 40))
    d.arc([x + 20, y + 6, x + w - 20, y + h - 6], 180, 360, fill=(40, 40, 40),
          width=3)
    for bx in (10, 46, 82, 118, 154):
        d.rectangle([x + bx, y + h - 34, x + bx + 22, y + h - 18],
                    fill=(30, 30, 30))


def illo_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 220))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 90, 140))
    d.polygon([(x + 30, y + h - 22), (x + 150, y + h - 22),
               (x + 140, y + h - 8), (x + 40, y + h - 8)], fill=(30, 30, 30))
    d.rectangle([x + 50, y + h - 34, x + 70, y + h - 22], fill=(200, 60, 40))
    d.rectangle([x + 76, y + h - 34, x + 96, y + h - 22], fill=(40, 120, 80))
    d.rectangle([x + 102, y + h - 34, x + 122, y + h - 22], fill=(230, 180, 40))
    # drone with dashed path
    for i in range(8):
        px = x + 130 + i * 6
        py = y + 10 + i * 2
        d.ellipse([px, py, px + 2, py + 2], fill=(255, 255, 255))
    d.ellipse([x + 168, y + 22, x + 182, y + 32], fill=(20, 20, 20))
    d.line([x + 166, y + 27, x + 184, y + 27], fill=(20, 20, 20), width=2)


def illo_iran(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 30, cy - 11, cx + 30, cy + 11], outline=(40, 80, 140),
              width=2)
    d.ellipse([cx - 11, cy - 26, cx + 11, cy + 26], outline=(40, 80, 140),
              width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    d.rectangle([x, y, x + w, y + 6], fill=(40, 140, 80))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=RED)


def illo_trump(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 48))
    for rx in (8, 40, 72):
        d.rectangle([x + rx, y + 8, x + rx + 26, y + h - 8], fill=(60, 70, 90),
                    outline=(120, 130, 150), width=1)
        for ry in range(y + 12, y + h - 10, 8):
            d.rectangle([x + rx + 4, ry, x + rx + 10, ry + 3], fill=(90, 200, 120))
            d.rectangle([x + rx + 14, ry, x + rx + 22, ry + 3], fill=(255, 190, 60))
    d.ellipse([x + w - 52, y + 6, x + w - 6, y + h - 6], fill=(255, 200, 40))
    d.text((x + w - 40, y + 8), "$", font=font(SANS_B, 26), fill=(24, 32, 48))


def illo_chinajapan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(185, 28, 28))
    d.ellipse([x + w // 2 - 16, y + 6, x + w // 2 + 16, y + 38],
              fill=(255, 255, 255))
    # torii gate
    d.rectangle([x + 30, y + h - 34, x + w - 30, y + h - 28], fill=(20, 20, 20))
    d.rectangle([x + 44, y + h - 28, x + 50, y + h - 6], fill=(20, 20, 20))
    d.rectangle([x + w - 50, y + h - 28, x + w - 44, y + h - 6], fill=(20, 20, 20))
    d.rectangle([x + 38, y + h - 16, x + w - 38, y + h - 12], fill=(20, 20, 20))


def illo_davao(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 235))
    d.ellipse([x + 10, y + 8, x + 46, y + 22], fill=(255, 255, 255))
    d.ellipse([x + 130, y + 4, x + 168, y + 18], fill=(255, 255, 255))
    # plane, nose down toward runway
    d.polygon([(x + 40, y + 22), (x + 150, y + 44), (x + 146, y + 50),
               (x + 44, y + 30)], fill=(255, 255, 255))
    d.polygon([(x + 96, y + 32), (x + 120, y + 18), (x + 126, y + 24),
               (x + 104, y + 38)], fill=(230, 230, 230))
    d.polygon([(x + 44, y + 24), (x + 60, y + 12), (x + 66, y + 18),
               (x + 52, y + 28)], fill=(230, 230, 230))
    d.rectangle([x, y + h - 10, x + w, y + h - 6], fill=(60, 60, 60))
    for dx in range(0, w, 24):
        d.rectangle([x + dx + 4, y + h - 9, x + dx + 14, y + h - 7],
                    fill=(255, 255, 255))


def illo_canberra(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 225, 190))
    d.polygon([(x + 20, y + h - 12), (x + w // 2, y + 10), (x + w - 20, y + h - 12)],
              fill=(90, 110, 90))
    d.line([x + w // 2, y + 10, x + w // 2, y + 2], fill=INK, width=2)
    d.rectangle([x + w // 2 + 2, y + 2, x + w // 2 + 14, y + 8], fill=RED)
    # chip
    d.rectangle([x + w - 52, y + h - 34, x + w - 16, y + h - 6],
                fill=(30, 30, 30))
    d.rectangle([x + w - 44, y + h - 26, x + w - 24, y + h - 14],
                fill=(90, 200, 120))


def illo_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 150, 30))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(255, 255, 255))
    d.text((cx - 8, cy - 16), "B", font=font(SANS_B, 28), fill=(245, 150, 30))
    d.line([cx - 4, cy - 20, cx - 4, cy + 20], fill=(245, 150, 30), width=2)
    d.line([cx + 4, cy - 20, cx + 4, cy + 20], fill=(245, 150, 30), width=2)


def illo_russell(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 36))
    # chequered flag
    for r in range(4):
        for c in range(6):
            col = (255, 255, 255) if (r + c) % 2 == 0 else (10, 10, 10)
            d.rectangle([x + 8 + c * 7, y + 6 + r * 7, x + 14 + c * 7, y + 12 + r * 7],
                        fill=col)
    d.line([x + 50, y + 6, x + 50, y + h - 8], fill=(200, 200, 200), width=2)
    # track curve + car
    d.arc([x + 60, y + 14, x + w + 30, y + h + 20], 200, 330, fill=(255, 200, 40),
          width=4)
    d.rectangle([x + w - 52, y + h - 26, x + w - 14, y + h - 16], fill=(220, 40, 40))
    d.ellipse([x + w - 46, y + h - 16, x + w - 38, y + h - 8], fill=(10, 10, 10))
    d.ellipse([x + w - 24, y + h - 16, x + w - 16, y + h - 8], fill=(10, 10, 10))


def illo_rahul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
    # stumps
    for sx in (24, 32, 40):
        d.line([x + sx, y + h - 30, x + sx, y + h - 10], fill=(255, 220, 120),
               width=3)
    # bat
    d.polygon([(x + 90, y + 8), (x + 104, y + 8), (x + 112, y + h - 14),
               (x + 96, y + h - 14)], fill=(222, 184, 135))
    d.rectangle([x + 94, y + 2, x + 102, y + 10], fill=(120, 80, 40))
    # ball
    d.ellipse([x + w - 34, y + 10, x + w - 18, y + 26], fill=(200, 40, 40))

ILLOS = {1: illo_cop31, 2: illo_saudi, 3: illo_peru, 4: illo_kyiv,
         5: illo_hormuz, 6: illo_iran, 7: illo_trump, 8: illo_chinajapan,
         9: illo_davao, 10: illo_canberra, 11: illo_bitcoin, 12: illo_russell,
         13: illo_rahul}

# Map display positions for the crowded Europe / Middle East dots: a few
# degrees of nudge so the numbers stay legible (true places stay in SOURCES.md).
MAP_NUDGE = {1: (30.7, 35.0), 2: (46.7, 22.0), 4: (30.5, 52.0),
             5: (58.0, 24.0), 6: (51.4, 38.0)}

# Simplified world continents as (lon, lat) polygons.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-110, 23), (-115, 30), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-65, 76), (-60, 70)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-62, -41), (-68, -52),
     (-70, -55), (-73, -45), (-73, -30), (-70, -18), (-77, -12), (-80, -5),
     (-81, 0)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -28),
     (26, -34), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4),
     (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (40, 68),
     (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 60),
     (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (110, 20), (108, 12), (105, 9), (103, 1),
     (100, 6), (98, 10), (95, 16), (92, 21), (89, 22), (86, 20), (80, 13),
     (77, 8), (75, 12), (72, 20), (66, 25), (60, 25), (57, 26), (52, 26),
     (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36), (26, 38),
     (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (0, 40),
     (-2, 37), (-6, 36), (-9, 37)],
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -39),
     (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    [(95, 5), (98, 3), (100, 0), (104, -3), (106, -6), (110, -7), (114, -8),
     (118, -9), (120, -10), (119, -5), (115, -3), (110, -1), (105, 2),
     (100, 5)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9),
     (142, -8), (138, -8), (134, -4), (131, -2)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (142, 44), (140, 42), (138, 38), (136, 36), (133, 34)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 57), (0, 53), (1, 51)],
    [(167, -45), (170, -42), (173, -41), (175, -38), (177, -38), (174, -41),
     (171, -43), (168, -46)],
]


def draw_card(d, x, y, w, h, story, big):
    num, _reg, banner, loc, headline, body, source, _lon, _lat = story
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=(200, 192, 172),
                width=1)
    bh = 24 if big else 21
    d.rectangle([x, y, x + w, y + bh], fill=RED)
    bf = font(SANS_B, 16 if big else 13)
    d.text((x + 8, y + 4 if big else y + 3), banner, font=bf, fill=(255, 255, 255))
    iy = y + bh + 1
    ih = 48 if big else 30
    ILLOS[num](d, x + 1, iy, w - 2, ih)
    ty = iy + ih + 5
    lf = font(SANS_B, 11 if big else 9)
    d.text((x + 8, ty), loc, font=lf, fill=RED_DARK)
    ty += 15 if big else 13
    hf = font(SERIF_B, 19 if big else 15)
    ty = draw_wrapped(d, x + 8, ty, headline, hf, w - 16, 2, INK,
                      leading=21 if big else 16)
    ty += 2
    bodyf = font(SANS, 12 if big else 10)
    ty = draw_wrapped(d, x + 8, ty, body, bodyf, w - 16, 3, (40, 38, 34),
                      leading=12 if big else 11)
    sf = font(SANS, 10 if big else 9)
    d.text((x + 8, y + h - 14), source, font=sf, fill=GRAY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 14  # side margin

    # ---- header band
    d.text((mx, 8), "THE WORLD IN ONE DAY", font=font(SANS_B, 15), fill=RED)
    right = "35 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - mx - d.textlength(right, font=font(SANS_B, 11)), 10), right,
           font=font(SANS_B, 11), fill=INK)
    d.line([mx, 30, W - mx, 30], fill=INK, width=2)

    # ---- masthead + deck
    title = "Saturday 21 November 2026"
    tf = font(SERIF_B, 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 36), title, font=tf, fill=INK)
    deck = ("Climate summit runs past its deadline · Five missiles shot down "
            "over Saudi Arabia · Strong quake shakes Peru")
    df = font(SERIF_I, 16)
    d.text(((W - d.textlength(deck, font=df)) / 2, 100), deck, font=df, fill=INK)
    d.line([mx, 122, W - mx, 122], fill=INK, width=1)
    d.line([mx, 125, W - mx, 125], fill=INK, width=1)

    # ---- top facts strip: 6 numbered facts
    col_w = (W - 2 * mx) // 6
    for i, (num, cap) in enumerate(FACTS):
        cx = mx + i * col_w
        if i:
            d.line([cx - 5, 130, cx - 5, 168], fill=LINE, width=1)
        nf = font(SERIF_B, 22)
        d.text((cx, 126), num, font=nf, fill=INK)
        draw_wrapped(d, cx, 152, cap, font(SANS, 10), col_w - 12, 2, GRAY,
                     leading=11)

    # ---- region bars
    rx = mx
    bw = (W - 2 * mx) // 7
    for name, color in REGIONS:
        d.rectangle([rx, 176, rx + bw - 3, 190], fill=color)
        rf = font(SANS_B, 10)
        tw = d.textlength(name, font=rf)
        d.text((rx + (bw - 3 - tw) / 2, 179), name, font=rf, fill=(255, 255, 255))
        rx += bw

    # ---- big cards row
    bw3 = 324
    for i, story in enumerate(BIG):
        draw_card(d, mx + i * (bw3 + 12), 196, bw3, 190, story, big=True)

    # ---- small card rows
    bw5 = 196
    for i, story in enumerate(SMALL[:5]):
        draw_card(d, mx + i * (bw5 + 7), 392, bw5, 152, story, big=False)
    for i, story in enumerate(SMALL[5:]):
        draw_card(d, mx + i * (bw5 + 7), 550, bw5, 152, story, big=False)

    # ---- map band + date check
    map_x, map_y, map_w, map_h = mx, 708, 630, 112
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=NAVY)
    d.text((map_x + 8, map_y + 4), "WHERE IT HAPPENED",
           font=font(SANS_B, 11), fill=(255, 255, 255))
    lon0, lon1, lat0, lat1 = -170.0, 190.0, 78.0, -58.0
    ax, ay = map_x + 4, map_y + 20
    aw, ah = map_w - 8, map_h - 24

    def proj(lon, lat):
        px = ax + (lon - lon0) / (lon1 - lon0) * aw
        py = ay + (lat0 - lat) / (lat0 - lat1) * ah
        return px, py

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(232, 220, 192))
    for story in BIG + SMALL:
        num, _r, _b, _l, _h, _bd, _s, lon, lat = story
        # Nudge the crowded Europe / Middle East dots a few degrees apart so
        # their numbers stay legible; all other dots sit at their true place.
        lon, lat = MAP_NUDGE.get(num, (lon, lat))
        px, py = proj(lon, lat)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        nf = font(SANS_B, 8)
        label = str(num)
        d.text((px - d.textlength(label, font=nf) / 2, py - 5), label,
               font=nf, fill=(255, 255, 255))
    d.text((map_x + 8, map_y + map_h - 2),
           "Each number is the story with that number on this page.",
           font=font(SANS, 8), fill=(255, 255, 255))

    # ---- date check box
    dc_x, dc_y, dc_w, dc_h = 656, 708, 354, 112
    d.rectangle([dc_x, dc_y, dc_x + dc_w, dc_y + dc_h], fill=CARD_BG,
                outline=RED, width=2)
    d.text((dc_x + 8, dc_y + 5), "DATE CHECK",
           font=font(SANS_B, 12), fill=RED)
    dc_text = ("Left out as Friday 20 November’s news: Wall Street’s fall into "
               "correction; the Russian barrage that hit Kyiv’s bridges; the "
               "missile that landed in Poland; the UK–EU deal; Cyclone "
               "Akvan’s landfall. Older still: the Texas execution (19 Nov); "
               "Voyager 1’s light-day (18 Nov). Not confirmed when drawn: "
               "BepiColombo’s Mercury flyby; the final COP31 text.")
    draw_wrapped(d, dc_x + 8, dc_y + 22, dc_text, font(SANS, 10), dc_w - 16, 7,
                 INK, leading=12)

    # ---- also list
    ay = 826
    d.text((mx, ay), "ALSO ON SATURDAY 21 NOVEMBER 2026 · 22 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    d.line([mx, ay + 17, W - mx, ay + 17], fill=INK, width=1)
    ly = ay + 24
    col2_x = mx + 498
    af = font(SANS, 11)
    for j, (num, place, text, src) in enumerate(ALSO):
        col = 0 if j < 11 else 1
        row = j if j < 11 else j - 11
        lx = mx if col == 0 else col2_x
        line = f"{num} {place} — {text} ({src})"
        d.text((lx, ly + row * 12.5), line, font=af, fill=INK)

    # ---- footer
    fy = 992
    d.line([mx, fy, W - mx, fy], fill=LINE, width=1)
    foot = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026. Officials’ counts and claims are attributed.")
    ff = font(SERIF_I, 11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy + 8), foot, font=ff,
           fill=INK)
    foot2 = "Sources named beside each story · original drawings"
    d.text((W - mx - d.textlength(foot2, font=font(SANS, 9)), fy + 22), foot2,
           font=font(SANS, 9), fill=GRAY)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
