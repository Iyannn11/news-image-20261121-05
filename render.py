"""
News 21 R6 — "THE WORLD IN ONE DAY" for Saturday 21 November 2026.
Fresh broadsheet: 35 stories, 7 regions, all facts from SOURCES.md.
Cream paper, navy header, serif masthead, 6-fact strip, UTC timeline,
region bar, 3 hero cards, 10 small cards, real world map, list 14-35,
DATE CHECK naming stories left out as other days' news.
Deterministic render (same sha256 every run).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 238, 220)
INK = (26, 26, 26)
RED = (185, 28, 28)
NAVY = (31, 58, 95)
GREY = (96, 96, 96)
DARK = (15, 15, 30)
TAN = (176, 148, 94)
BORDER = (190, 180, 165)
SEA = (205, 225, 238)

FDIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FDIR}/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = f"{FDIR}/liberation/LiberationSerif-Italic.ttf"
SANS = f"{FDIR}/dejavu/DejaVuSans.ttf"
SANS_B = f"{FDIR}/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- facts
FACTS = [
    ("6.7", "Peru quake magnitude"),
    ("5", "Houthi missiles downed"),
    ("109", "Russian bridge attacks"),
    ("$58,174", "Bitcoin, down 6.1% in 24h"),
    ("1:34.041", "Fastest in Las Vegas FP3"),
    ("124*", "Rahul not out at tea"),
]

UTC_ITEMS = [
    ("00:09", "Peru quake strikes"),
    ("00:18", "Riyadh intercepts"),
    ("01:56", "COP31 deadlocked"),
    ("03:08", "Bitcoin $58,174"),
    ("06:33", "Araqchi: uranium stays"),
    ("06:41", "Iran drone claim"),
]

REGIONS = [
    ("EUROPE", 5, (185, 28, 28)),
    ("ASIA", 10, (120, 60, 140)),
    ("MIDDLE EAST", 6, (150, 95, 40)),
    ("AFRICA", 1, (210, 120, 30)),
    ("AMERICAS", 8, (20, 120, 120)),
    ("OCEANIA", 3, (40, 130, 60)),
    ("GLOBAL", 2, (31, 58, 95)),
]

# ---------------------------------------------------------------- heroes
HEROES = [
    dict(n=1, loc="ANTALYA, TURKEY · CLIMATE", chip="COP31: OVERTIME",
         caption="Summit president", ill="cop31",
         headline="COP31 STALLS INTO DAY TWO OF OVERTIME",
         body=("Talks missed their Friday deadline and the draft drops "
               "all mention of fossil fuels. A third draft is due Saturday."),
         source="(AP / Reuters)"),
    dict(n=2, loc="RIYADH, SAUDI ARABIA · WAR", chip="MISSILES DOWN",
         caption="Coalition intercepts", ill="missiles",
         headline="HOUTHI MISSILES DOWNED OVER RIYADH",
         body=("Coalition intercepts three ballistic missiles fired "
               "towards Riyadh early on Saturday and two over Jizan. "
               "Strikes hit Hodeidah port."),
         source="(Reuters / AFP)"),
    dict(n=3, loc="JUNIN, PERU · EARTHQUAKE", chip="QUAKE 6.7",
         caption="USGS final", ill="quake",
         headline="6.7 QUAKE SHAKES CENTRAL PERU",
         body=("Felt in Lima and along the coast; residents rush into "
               "the streets. No casualties or major damage reported."),
         source="(USGS / Reuters)"),
]

# ---------------------------------------------------------------- smalls
SMALLS = [
    dict(n=4, loc="KYIV · UKRAINE", chip="BRIDGE VOW", flag="UA",
         caption="NBC interview", ill="kyiv",
         headline="ZELENSKY: CRIMEAN BRIDGE 'WILL NOT STAY'",
         body=("Russia hit bridges 109 times; Nov 20 barrage killed 7. "
               "(NBC)")),
    dict(n=5, loc="STRAIT OF HORMUZ · DRONE", chip="DRONE DOWN", flag="IR",
         caption="IRGC claims", ill="drone",
         headline="IRAN SAYS IT SHOT DOWN A US DRONE",
         body=("IRGC claims 58th MQ-9 downed over Strait. (Press TV)")),
    dict(n=6, loc="TEHRAN · NUCLEAR", chip="RED LINES", flag="IR",
         caption="Araqchi", ill="uranium",
         headline="IRAN: URANIUM STOCK STAYS IN THE COUNTRY",
         body=("Araqchi sets red lines; 'a fair solution' is possible. "
               "(Reuters)")),
    dict(n=7, loc="WASHINGTON · TAX", chip="TAX THREAT", flag="US",
         caption="White House", ill="trump",
         headline="TRUMP VOWS TAX ON DATA CENTRES ABROAD",
         body=("'Tremendous tax' on data centres abroad, said Friday. "
               "(Reuters)")),
    dict(n=8, loc="BEIJING · TAIWAN", chip="TAIWAN ROW", flag="CN",
         caption="Beijing", ill="china",
         headline="CHINA WARNS JAPAN ON TAIWAN WORDS",
         body=("Beijing: Japan must 'correct' Taiwan words. (Reuters)")),
    dict(n=9, loc="DAVAO · AVIATION", chip="SAFE LANDING", flag="PG",
         caption="PX19 diverted", ill="flight",
         headline="JET LANDS SAFELY AFTER ENGINE FIRE",
         body=("Air Niugini 767 diverts to Davao; all 146 safe via "
               "slides. (AP)")),
    dict(n=10, loc="CANBERRA · AI", chip="AI TALKS", flag="AU",
         caption="Joint statement", ill="ai",
         headline="AUSTRALIA AND CHINA AGREE TO AI TALKS",
         body=("Albanese and Li Qiang agree a formal AI dialogue. "
               "(pm.gov.au)")),
    dict(n=11, loc="WORLD · MARKETS", chip="BITCOIN SLIDES", flag="GL",
         caption="CoinMarketCap", ill="bitcoin",
         headline="BITCOIN SLIDES BELOW $59,000",
         body=("$58,174 at 03:08 UTC, down 6.1% in 24h. "
               "(CoinMarketCap)")),
    dict(n=12, loc="LAS VEGAS · F1", chip="FP3 FASTEST", flag="GB",
         caption="Formula 1", ill="f1",
         headline="RUSSELL FASTEST IN LAS VEGAS FP3",
         body=("Russell 1:34.041; Antonelli +0.911; Norris 3rd. (F1)")),
    dict(n=13, loc="WELLINGTON · CRICKET", chip="CENTURY", flag="IN",
         caption="Basin Reserve", ill="cricket",
         headline="RAHUL HITS A CENTURY AGAINST NEW ZEALAND",
         body=("Rahul 124* at tea, India 344-2 on day 3 of the 1st Test. "
               "(AFP)")),
]

# ---------------------------------------------------------------- list 14-35
# (number, prefix, rest, source) — rendered as "N PREFIX: rest (source)"
LIST_ITEMS = [
    (14, "Ukraine", "Kryvyi Rih strike kills 2, injures 42",
     "Kyiv Ind."),
    (15, "Denmark", "Expels attaché over rapper plot", "Al Jazeera"),
    (16, "Antalya", "EU warns COP31 risks a 'fossil summit'", "AFP"),
    (17, "Poland", "NATO condemns airspace breach", "Vertical"),
    (18, "Iraq", "Hartha power plant fire kills 4, injures 30", "Reuters"),
    (19, "Yemen", "Houthis threaten Jeddah, Red Sea ports", "AJ"),
    (20, "US", "Vance — Iran strikes were 'president's call'",
     "Reuters"),
    (21, "US", "Lawmaker threatens SpaceX's funding", "CNN"),
    (22, "Missouri", "Judge approves $7.25bn Roundup deal", "Reuters"),
    (23, "LA", "Jury convicts man of starting Palisades fire", "Reuters"),
    (24, "Canada", "Rests defence in youth climate trial", "AFP"),
    (25, "Pyongyang", "Kim tours factories, no Trump meeting", "AFP"),
    (26, "Taipei", "Budget and cash payout are passed", "Taipei Times"),
    (27, "Bangkok", "Six-point plan on arsenic in rivers", "The Nation"),
    (28, "Seoul", "Lee — speed is vital in the AI race", "Reuters"),
    (29, "Vietnam", "Parliament speeds land seizures", "Reuters"),
    (30, "New Delhi", "Protests at Meta's India offices", "Reuters"),
    (31, "Ipoh", "Malaysia beat S Korea 3–0 in hockey", "RTM World"),
    (32, "Singapore", "FTA upgrade talks open with China", "RTM"),
    (33, "UN", "States agree talks to curb 'killer robots'", "Reuters"),
    (34, "Port Louis", "Rating agency talks to 15 states", "Al Jazeera"),
    (35, "Melbourne", "Cummins keeps Australia captaincy", "Reuters"),
]

DATE_CHECK = (
    "Every story above happened on Saturday 21 November 2026. Left out as "
    "other days' news: the Wall Street correction (20 Nov), Texas execution "
    "(19 Nov), Kyiv bridge barrage (20 Nov), Poland missile (20 Nov), "
    "Voyager 1's light-day (18 Nov)."
)

FOOTER = ("Sources: Reuters · AP · AFP · USGS · NBC · CNN · Formula 1 · "
          "CoinMarketCap · Al Jazeera · Taipei Times · The Nation · "
          "RTM World · pm.gov.au · Kyiv Independent · Press TV · "
          "Tasnim · IGP · CAAP")

# ---------------------------------------------------------------- map data
# PINS: story number -> (x, y) in the map panel; crowded Europe / Middle
# East cluster nudged a few px apart so the numbered circles stay legible.
PINS = {
    1: (175, 845), 2: (181, 859), 3: (95, 877), 4: (170, 832),
    5: (199, 857), 6: (197, 843), 7: (94, 844), 8: (240, 843),
    9: (247, 865), 10: (265, 894), 11: (129, 843), 12: (65, 846),
    13: (284, 897),
}
# City labels: (text, x, y) — every label sits at least 8px inside the
# panel border (panel spans x 12-300, y 806-934).
CITY_LABELS = [
    ("LAS VEGAS", 20, 862),
    ("WASHINGTON", 60, 824),
    ("KYIV", 186, 820),
    ("ANTALYA", 140, 816),
    ("RIYADH", 204, 874),
    ("WELLINGTON", 232, 906),
]
# Rough simplified continent outlines in (lon, lat), drawn tan on the
# pale-blue sea panel.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
     (-85, 70), (-75, 62), (-65, 60), (-55, 52), (-60, 46), (-70, 42),
     (-75, 35), (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 22),
     (-110, 25), (-115, 30), (-120, 34), (-125, 40), (-125, 48),
     (-135, 58), (-150, 60), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-70, 0), (-75, -5), (-80, -10), (-75, -15),
     (-70, -20), (-70, -30), (-70, -40), (-70, -52), (-65, -55),
     (-60, -45), (-55, -35), (-50, -30), (-40, -25), (-35, -15),
     (-35, -5), (-45, 0), (-55, 5), (-60, 8), (-70, 10)],
    # Europe
    [(-10, 36), (-5, 38), (0, 39), (5, 40), (10, 38), (15, 40),
     (20, 40), (25, 36), (30, 36), (35, 36), (30, 40), (25, 45),
     (20, 45), (15, 45), (10, 45), (5, 48), (0, 48), (-5, 48),
     (-10, 45), (-15, 42), (-20, 40)],
    # Africa
    [(-10, 35), (-5, 35), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 20), (45, 12), (50, 10), (45, 0), (40, -10),
     (35, -20), (30, -30), (20, -35), (15, -30), (12, -20), (10, -10),
     (8, 0), (0, 5), (-8, 5), (-15, 10), (-17, 15), (-15, 20),
     (-12, 25), (-10, 30)],
    # Asia
    [(35, 36), (40, 38), (45, 40), (50, 38), (55, 40), (60, 42),
     (65, 45), (70, 45), (75, 50), (80, 55), (90, 60), (100, 65),
     (110, 70), (120, 72), (130, 70), (140, 72), (150, 70), (160, 65),
     (170, 66), (178, 65), (170, 60), (160, 55), (150, 50), (140, 45),
     (135, 40), (130, 35), (125, 30), (120, 25), (115, 20), (110, 15),
     (105, 10), (100, 8), (95, 10), (90, 15), (85, 20), (80, 15),
     (75, 10), (70, 8), (65, 10), (60, 15), (55, 20), (50, 25),
     (45, 30), (40, 32), (35, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (150, -25), (146, -20), (142, -15), (140, -12),
     (135, -12), (130, -13), (125, -15), (120, -18), (115, -20)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-8, 58), (-10, 55), (-8, 52),
     (-6, 50)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 40),
     (143, 42), (145, 44), (142, 44), (140, 40), (138, 37), (135, 35),
     (132, 33)],
]


# ---------------------------------------------------------------- drawing helpers
class ScaleDraw:
    """Draws on a 2x temp image so illustrations downscale smoothly."""

    def __init__(self, d, s):
        self._d = d
        self._s = s

    def _pts(self, box):
        return [c * self._s for c in box]

    def _kw(self, kw):
        out = dict(kw)
        if "width" in out:
            out["width"] = out["width"] * self._s
        return out

    def rectangle(self, box, **kw):
        self._d.rectangle(self._pts(box), **self._kw(kw))

    def rounded_rectangle(self, box, **kw):
        self._d.rounded_rectangle(self._pts(box), **self._kw(kw))

    def ellipse(self, box, **kw):
        self._d.ellipse(self._pts(box), **self._kw(kw))

    def polygon(self, pts, **kw):
        self._d.polygon([(x * self._s, y * self._s) for x, y in pts],
                        **self._kw(kw))

    def line(self, pts, **kw):
        # accept both PIL flat lists [x1, y1, x2, y2] and point lists
        if pts and isinstance(pts[0], (int, float)):
            pts = [(pts[i], pts[i + 1]) for i in range(0, len(pts), 2)]
        self._d.line([(x * self._s, y * self._s) for x, y in pts],
                     **self._kw(kw))

    def arc(self, box, a0, a1, **kw):
        self._d.arc(self._pts(box), a0, a1, **self._kw(kw))


def draw_ill(im, ill_name, x, y, w, h):
    fn = ILLUSTRATIONS[ill_name]
    tmp = Image.new("RGB", (w * 2, h * 2))
    td = ImageDraw.Draw(tmp)
    fn(ScaleDraw(td, 2), 0, 0, w, h)
    tmp = tmp.resize((w, h), Image.LANCZOS)
    im.paste(tmp, (x, y))


def chip(d, x, y, text, size=9):
    f = font(SANS_B, size)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 10, y + size + 7], radius=3,
                        fill=RED)
    d.text((x + 5, y + 3), text, font=f, fill="white")


def number_badge(d, cx, cy, n, r=9):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="white",
              outline=RED, width=2)
    f = font(SANS_B, 11)
    t = str(n)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 6), t, font=f, fill=RED)


def caption_bar(d, x, y, w, text, size=8):
    d.rectangle([x, y, x + w, y + 13], fill=(25, 25, 35))
    d.text((x + 4, y + 2), text, font=font(SANS, size), fill=(245, 245, 235))


def draw_flag(d, code, x, y):
    """Tiny 20x13 flag, drawn from scratch per country code."""
    if code == "UA":  # Ukraine: blue over yellow
        d.rectangle([x, y, x + 20, y + 6], fill=(0, 90, 170))
        d.rectangle([x, y + 7, x + 20, y + 13], fill=(255, 210, 0))
    elif code == "IR":  # Iran: green / white / red
        d.rectangle([x, y, x + 20, y + 4], fill=(0, 130, 60))
        d.rectangle([x, y + 5, x + 20, y + 8], fill="white")
        d.rectangle([x, y + 9, x + 20, y + 13], fill=(200, 30, 30))
    elif code == "US":  # USA: stripes + blue canton
        for i in range(7):
            d.rectangle([x, y + i * 2, x + 20, y + i * 2 + 1],
                        fill=(180, 30, 40) if i % 2 == 0 else "white")
        d.rectangle([x, y, x + 9, y + 6], fill=(30, 50, 110))
    elif code == "CN":  # China: red + yellow star
        d.rectangle([x, y, x + 20, y + 13], fill=(200, 25, 25))
        d.ellipse([x + 3, y + 2, x + 9, y + 8], fill=(255, 220, 0))
    elif code == "PG":  # Papua New Guinea: diagonal red / black + stars
        d.polygon([(x, y), (x + 20, y), (x, y + 13)], fill=(200, 30, 30))
        d.polygon([(x + 20, y), (x + 20, y + 13), (x, y + 13)],
                  fill=(15, 15, 15))
        for sx, sy in [(14, 4), (16, 8), (12, 10), (17, 11)]:
            d.ellipse([x + sx, y + sy, x + sx + 1, y + sy + 1],
                      fill="white")
    elif code == "AU":  # Australia: blue + southern cross stars
        d.rectangle([x, y, x + 20, y + 13], fill=(25, 60, 140))
        for sx, sy in [(13, 3), (16, 6), (12, 8), (17, 10), (14, 11)]:
            d.ellipse([x + sx, y + sy, x + sx + 1, y + sy + 1],
                      fill="white")
    elif code == "GB":  # Britain: blue + white/red cross
        d.rectangle([x, y, x + 20, y + 13], fill=(25, 60, 140))
        d.line([x, y, x + 20, y + 13], fill="white", width=2)
        d.line([x + 20, y, x, y + 13], fill="white", width=2)
        d.line([x + 10, y, x + 10, y + 13], fill=(200, 25, 25), width=3)
        d.line([x, y + 6, x + 20, y + 6], fill=(200, 25, 25), width=3)
    elif code == "IN":  # India: saffron / white / green + wheel
        d.rectangle([x, y, x + 20, y + 4], fill=(255, 150, 40))
        d.rectangle([x, y + 5, x + 20, y + 8], fill="white")
        d.rectangle([x, y + 9, x + 20, y + 13], fill=(20, 130, 60))
        d.ellipse([x + 8, y + 5, x + 11, y + 8], outline=(20, 60, 140))
    else:  # GL: globe for a world story
        d.ellipse([x + 2, y, x + 18, y + 13], fill=(60, 130, 200),
                  outline=(20, 60, 140))
        d.ellipse([x + 5, y + 3, x + 10, y + 7], fill=(60, 160, 80))
        d.ellipse([x + 11, y + 8, x + 15, y + 11], fill=(60, 160, 80))


# ---------------------------------------------------------------- illustrations
def ill_cop31(d, x, y, w, h):
    # Conference hall: dusk sky, globe, flags, delegates at a long table.
    d.rectangle([x, y, x + w, y + h], fill=(70, 110, 160))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 80, 50))
    d.ellipse([x + 24, y + 8, x + 64, y + 48], fill=(90, 180, 110))
    d.ellipse([x + 30, y + 14, x + 42, y + 26], fill=(120, 200, 140))
    d.ellipse([x + 44, y + 28, x + 58, y + 42], fill=(120, 200, 140))
    for i, c in enumerate([(200, 40, 40), (240, 200, 40), (40, 120, 200),
                           (40, 170, 80), (180, 80, 160)]):
        fx = x + 90 + i * 44
        d.line([fx, y + 10, fx, y + 46], fill=(230, 230, 220), width=2)
        d.polygon([(fx, y + 10), (fx + 18, y + 16), (fx, y + 22)],
                  fill=c)
    d.rectangle([x + 10, y + h - 52, x + w - 10, y + h - 26],
                fill=(150, 105, 60))
    for i in range(7):
        px = x + 22 + i * 44
        d.ellipse([px, y + h - 74, px + 18, y + h - 56],
                  fill=(200, 180, 150))
        d.rectangle([px + 2, y + h - 56, px + 16, y + h - 52],
                    fill=[(180, 60, 60), (60, 120, 200), (220, 180, 60),
                          (90, 170, 90), (170, 90, 170), (230, 130, 50),
                          (80, 160, 200)][i])
    d.ellipse([x + w - 58, y + 6, x + w - 18, y + 46], fill=(235, 220, 160))


def ill_missiles(d, x, y, w, h):
    # Night sky over Riyadh: missile trails, interception bursts, skyline.
    d.rectangle([x, y, x + w, y + h], fill=(18, 18, 45))
    for sx, sy in [(30, 14), (90, 8), (150, 18), (210, 10), (260, 16),
                   (60, 30), (180, 28), (300, 26)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                  fill=(240, 240, 220))
    for tx, ty in [(70, 40), (170, 26), (250, 46)]:
        d.line([x + tx, y + ty + 40, x + tx + 26, y + ty],
               fill=(255, 180, 60), width=3)
        d.ellipse([x + tx + 18, y + ty - 8, x + tx + 34, y + ty + 8],
                  fill=(255, 220, 120), outline=(255, 140, 40), width=2)
    for bx in [10, 60, 120, 180, 240, 290]:
        bh = 26 + (bx % 3) * 12
        d.rectangle([x + bx, y + h - bh, x + bx + 34, y + h],
                    fill=(30, 30, 60))
        for wy in range(y + h - bh + 5, y + h - 4, 9):
            d.rectangle([x + bx + 5, wy, x + bx + 10, wy + 4],
                        fill=(255, 210, 90))
    d.polygon([(x + 130, y + h - 60), (x + 150, y + h - 100),
               (x + 170, y + h - 60)], fill=(40, 40, 80))
    d.ellipse([x + 146, y + h - 104, x + 154, y + h - 96],
              fill=(255, 220, 120))


def ill_quake(d, x, y, w, h):
    # Andes mountains, cracked ground, shaking town, seismograph line.
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
    d.polygon([(x, y + h), (x + 70, y + 20), (x + 140, y + h)],
              fill=(120, 110, 100))
    d.polygon([(x + 60, y + h), (x + 150, y + 8), (x + 240, y + h)],
              fill=(100, 95, 88))
    d.polygon([(x + 130, y + 8), (x + 150, y + 8), (x + 160, y + 24),
               (x + 140, y + 24)], fill=(250, 250, 245))
    d.polygon([(x + 200, y + h), (x + 270, y + 30), (x + w, y + h)],
              fill=(130, 120, 108))
    for bx in [20, 70, 120, 200, 260]:
        bh = 22 + (bx % 4) * 6
        d.rectangle([x + bx, y + h - 30 - bh, x + bx + 32, y + h - 30],
                    fill=(190, 160, 120))
        for wy in range(y + h - 30 - bh + 5, y + h - 34, 8):
            d.rectangle([x + bx + 4, wy, x + bx + 9, wy + 4],
                        fill=(60, 50, 40))
    d.line([x, y + h - 30, x + 90, y + h - 22, x + 150, y + h - 34,
            x + 210, y + h - 20, x + w, y + h - 28],
           fill=(60, 45, 35), width=3)
    d.line([x + 10, y + 16, x + 40, y + 16, x + 52, y + 6, x + 64, y + 26,
            x + 76, y + 10, x + 110, y + 10, x + 122, y + 20, x + 150,
            y + 12], fill=(200, 30, 30), width=2)
    d.ellipse([x + w - 40, y + 8, x + w - 12, y + 36], fill=(250, 220, 90))


def ill_kyiv(d, x, y, w, h):
    # River bridge at dusk, Kyiv skyline with domes.
    d.rectangle([x, y, x + w, y + h], fill=(90, 120, 170))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(60, 110, 160))
    for bx in [8, 50, 95, 150, 210, 260]:
        bh = 24 + (bx % 3) * 10
        d.rectangle([x + bx, y + h - 22 - bh, x + bx + 36, y + h - 22],
                    fill=(70, 70, 90))
        for wy in range(y + h - 22 - bh + 5, y + h - 26, 8):
            d.rectangle([x + bx + 5, wy, x + bx + 10, wy + 4],
                        fill=(255, 210, 100))
    d.ellipse([x + 170, y + 6, x + 186, y + 22], fill=(230, 200, 90),
              outline=(180, 150, 60))
    d.rectangle([x + 176, y + 22, x + 180, y + 34], fill=(180, 150, 60))
    d.line([x, y + h - 26, x + w, y + h - 26], fill=(220, 220, 210),
           width=4)
    for px in [40, 110, 180, 250, 300]:
        d.line([x + px, y + h - 26, x + px, y + h - 48],
               fill=(220, 220, 210), width=3)
    d.arc([x + 20, y + h - 50, x + 90, y + h - 10], 180, 360,
          fill=(230, 230, 220), width=3)
    d.arc([x + 230, y + h - 50, x + 300, y + h - 10], 180, 360,
          fill=(230, 230, 220), width=3)


def ill_drone(d, x, y, w, h):
    # Strait of Hormuz: grey sea, tanker, drone silhouette in a pale sky.
    d.rectangle([x, y, x + w, y + h], fill=(190, 210, 225))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 110, 140))
    d.ellipse([x + w - 56, y + 6, x + w - 16, y + 46], fill=(250, 230, 160))
    d.rectangle([x + 30, y + h - 40, x + 150, y + h - 26],
                fill=(140, 50, 40))
    d.rectangle([x + 120, y + h - 56, x + 150, y + h - 40],
                fill=(200, 200, 190))
    d.line([x + 135, y + h - 70, x + 135, y + h - 56], fill=(60, 60, 60),
           width=3)
    for wx in range(10, w - 10, 34):
        d.line([x + wx, y + h - 16, x + wx + 18, y + h - 16],
               fill=(220, 235, 245), width=2)
    d.polygon([(x + 210, y + 18), (x + 262, y + 18), (x + 236, y + 30)],
              fill=(50, 50, 60))
    d.line([x + 236, y + 30, x + 236, y + 44], fill=(50, 50, 60),
           width=3)
    d.ellipse([x + 228, y + 44, x + 244, y + 52], fill=(50, 50, 60))
    d.line([x + 210, y + 18, x + 196, y + 26], fill=(50, 50, 60),
           width=2)
    d.line([x + 262, y + 18, x + 276, y + 26], fill=(50, 50, 60),
           width=2)


def ill_uranium(d, x, y, w, h):
    # Nuclear site: domes, cooling towers, fence, desert ground.
    d.rectangle([x, y, x + w, y + h], fill=(200, 180, 140))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(170, 140, 95))
    d.ellipse([x + 20, y + h - 62, x + 90, y + h - 20],
              fill=(220, 220, 210), outline=(150, 150, 140), width=2)
    d.rectangle([x + 20, y + h - 34, x + 90, y + h - 20],
                fill=(220, 220, 210))
    d.polygon([(x + 120, y + h - 20), (x + 130, y + h - 66),
               (x + 160, y + h - 66), (x + 170, y + h - 20)],
              fill=(190, 190, 180))
    d.polygon([(x + 190, y + h - 20), (x + 200, y + h - 66),
               (x + 230, y + h - 66), (x + 240, y + h - 20)],
              fill=(200, 200, 190))
    d.rectangle([x + 255, y + h - 46, x + 300, y + h - 20],
                fill=(150, 160, 170))
    d.rectangle([x + 262, y + h - 40, x + 272, y + h - 32],
                fill=(255, 220, 90))
    d.rectangle([x + 278, y + h - 40, x + 288, y + h - 32],
                fill=(255, 220, 90))
    for fx in range(0, w, 26):
        d.line([x + fx, y + h - 18, x + fx, y + h - 6],
               fill=(90, 80, 60), width=2)
    d.ellipse([x + w - 44, y + 8, x + w - 14, y + 38],
              fill=(250, 225, 120))


def ill_trump(d, x, y, w, h):
    # White House portico beside a row of server racks.
    d.rectangle([x, y, x + w, y + h], fill=(140, 170, 200))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(90, 140, 80))
    d.rectangle([x + 12, y + 22, x + 130, y + h - 24],
                fill=(235, 232, 220))
    d.polygon([(x + 8, y + 22), (x + 71, y + 4), (x + 134, y + 22)],
              fill=(210, 205, 190))
    for cx in [28, 52, 76, 100]:
        d.rectangle([x + cx, y + 30, x + cx + 8, y + h - 24],
                    fill=(200, 195, 180))
    d.rectangle([x + 58, y + h - 40, x + 84, y + h - 24],
                fill=(90, 70, 50))
    for rx in [150, 205, 260]:
        d.rectangle([x + rx, y + 14, x + rx + 44, y + h - 24],
                    fill=(40, 45, 60))
        for ry in range(y + 20, y + h - 28, 12):
            d.rectangle([x + rx + 5, ry, x + rx + 39, ry + 7],
                        fill=(70, 200, 120) if (ry // 12) % 2 else
                        (60, 140, 220))
    d.ellipse([x + w - 34, y + 6, x + w - 10, y + 30],
              fill=(250, 225, 120))


def ill_china(d, x, y, w, h):
    # Beijing skyline with a red flag and the Great Wall ridge.
    d.rectangle([x, y, x + w, y + h], fill=(180, 200, 220))
    d.polygon([(x, y + h), (x + 80, y + h - 40), (x + 160, y + h),
               (x + 240, y + h - 34), (x + w, y + h)],
              fill=(110, 140, 90))
    for bx in [10, 55, 105, 165, 225, 275]:
        bh = 26 + (bx % 3) * 9
        d.rectangle([x + bx, y + h - 30 - bh, x + bx + 34, y + h - 30],
                    fill=(150, 60, 50))
        for wy in range(y + h - 30 - bh + 5, y + h - 34, 8):
            d.rectangle([x + bx + 5, wy, x + bx + 10, wy + 4],
                        fill=(255, 220, 120))
    d.line([x + 150, y + 8, x + 150, y + 44], fill=(230, 230, 220),
           width=2)
    d.polygon([(x + 150, y + 8), (x + 176, y + 14), (x + 150, y + 20)],
              fill=(200, 25, 25))
    d.ellipse([x + 155, y + 11, x + 161, y + 17], fill=(255, 220, 0))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(90, 110, 70))
    d.ellipse([x + w - 46, y + 6, x + w - 16, y + 36],
              fill=(250, 225, 120))


def ill_flight(d, x, y, w, h):
    # Airliner on final approach over Davao bay, mountains behind.
    d.rectangle([x, y, x + w, y + h], fill=(130, 180, 220))
    d.polygon([(x, y + h), (x + 60, y + 34), (x + 130, y + h)],
              fill=(110, 130, 100))
    d.polygon([(x + 100, y + h), (x + 180, y + 26), (x + 260, y + h)],
              fill=(95, 115, 90))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(60, 110, 150))
    d.ellipse([x + 60, y + 14, x + 250, y + 44], fill=(240, 240, 235))
    d.polygon([(x + 250, y + 22), (x + 296, y + 30), (x + 250, y + 38)],
              fill=(240, 240, 235))
    d.polygon([(x + 90, y + 44), (x + 130, y + 62), (x + 130, y + 44)],
              fill=(210, 210, 205))
    for wx in range(80, 240, 18):
        d.rectangle([x + wx, y + 24, x + wx + 8, y + 30],
                    fill=(40, 90, 160))
    d.rectangle([x, y + h - 10, x + w, y + h - 6], fill=(70, 70, 70))
    d.ellipse([x + w - 40, y + 8, x + w - 14, y + 34],
              fill=(250, 225, 120))


def ill_ai(d, x, y, w, h):
    # Two flags shaking hands over a glowing AI chip.
    d.rectangle([x, y, x + w, y + h], fill=(60, 80, 130))
    d.rectangle([x + 30, y + h - 46, x + 150, y + h - 46],
                fill=(220, 220, 210))
    d.rectangle([x + 150, y + h - 46, x + 270, y + h - 46],
                fill=(220, 220, 210))
    d.rectangle([x + 130, y + 12, x + 190, y + 42], fill=(30, 35, 55),
                outline=(80, 200, 140), width=2)
    d.rectangle([x + 142, y + 18, x + 178, y + 36], fill=(20, 25, 45))
    for cx in [150, 162, 174]:
        d.rectangle([x + cx, y + 22, x + cx + 4, y + 32],
                    fill=(80, 200, 140))
    d.line([x + 60, y + 16, x + 60, y + 52], fill=(230, 230, 220),
           width=2)
    d.polygon([(x + 60, y + 16), (x + 96, y + 22), (x + 60, y + 28)],
              fill=(25, 60, 140))
    d.ellipse([x + 66, y + 19, x + 70, y + 23], fill="white")
    d.ellipse([x + 74, y + 23, x + 78, y + 27], fill="white")
    d.line([x + 250, y + 16, x + 250, y + 52], fill=(230, 230, 220),
           width=2)
    d.polygon([(x + 250, y + 16), (x + 286, y + 22), (x + 250, y + 28)],
              fill=(200, 25, 25))
    d.ellipse([x + 256, y + 19, x + 262, y + 25], fill=(255, 220, 0))
    for i in range(5):
        d.ellipse([x + 20 + i * 56, y + h - 12, x + 32 + i * 56,
                   y + h - 2], fill=(255, 220, 90))


def ill_bitcoin(d, x, y, w, h):
    # Big falling coin and a red down-trend chart.
    d.rectangle([x, y, x + w, y + h], fill=(25, 30, 45))
    d.ellipse([x + 24, y + 6, x + 84, y + 66], fill=(240, 170, 40),
              outline=(180, 120, 20), width=3)
    d.ellipse([x + 38, y + 20, x + 70, y + 52], fill=(240, 170, 40))
    d.line([x + 54, y + 14, x + 54, y + 58], fill=(160, 100, 10),
           width=4)
    d.line([x + 44, y + 22, x + 64, y + 22], fill=(160, 100, 10),
           width=3)
    d.line([x + 44, y + 44, x + 64, y + 44], fill=(160, 100, 10),
           width=3)
    for i, (cx, cy, ch) in enumerate([(120, 30, 14), (150, 36, 10),
                                      (180, 26, 18), (210, 38, 8),
                                      (240, 30, 14), (270, 34, 10)]):
        d.rectangle([x + cx, y + cy, x + cx + 16, y + cy + ch],
                    fill=(60, 200, 110))
    d.line([x + 110, y + 14, x + 160, y + 30, x + 210, y + 22,
            x + 260, y + 44, x + 300, y + 40],
           fill=(230, 60, 60), width=3)
    d.polygon([(x + 292, y + 34), (x + 306, y + 40), (x + 292, y + 48)],
              fill=(230, 60, 60))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(40, 45, 65))


def ill_f1(d, x, y, w, h):
    # Red race car on the Strip at dusk, checkered flag, skyline.
    d.rectangle([x, y, x + w, y + h], fill=(50, 40, 70))
    for bx in [0, 45, 95, 150, 205, 260]:
        bh = 24 + (bx % 3) * 10
        d.rectangle([x + bx, y + 6, x + bx + 36, y + 6 + bh],
                    fill=(25, 25, 45))
        for wy in range(y + 10, y + 6 + bh - 4, 8):
            d.rectangle([x + bx + 5, wy, x + bx + 10, wy + 4],
                        fill=(255, 210, 90))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(35, 35, 40))
    d.line([x, y + h - 14, x + w, y + h - 14], fill=(250, 250, 240),
           width=2)
    d.line([x, y + h - 6, x + w, y + h - 6], fill=(250, 250, 240),
           width=2)
    d.rounded_rectangle([x + 40, y + h - 44, x + 220, y + h - 22],
                        radius=8, fill=(215, 30, 35))
    d.polygon([(x + 90, y + h - 58), (x + 120, y + h - 58),
               (x + 130, y + h - 44), (x + 80, y + h - 44)],
              fill=(215, 30, 35))
    d.polygon([(x + 130, y + h - 58), (x + 165, y + h - 58),
               (x + 175, y + h - 44), (x + 130, y + h - 44)],
              fill=(200, 200, 210))
    d.ellipse([x + 62, y + h - 24, x + 88, y + h - 2], fill=(20, 20, 25),
              outline=(200, 200, 200), width=2)
    d.ellipse([x + 168, y + h - 24, x + 194, y + h - 2], fill=(20, 20, 25),
              outline=(200, 200, 200), width=2)
    d.rectangle([x + 44, y + h - 38, x + 216, y + h - 34],
                fill=(250, 250, 245))
    d.line([x + 260, y + 8, x + 260, y + 40], fill=(230, 230, 220),
           width=2)
    for r in range(3):
        for c in range(4):
            d.rectangle([x + 260 + c * 8, y + 8 + r * 8,
                         x + 268 + c * 8, y + 16 + r * 8],
                        fill="white" if (r + c) % 2 == 0 else (20, 20, 20))
    d.ellipse([x + 20, y + 8, x + 48, y + 36], fill=(250, 225, 120))


def ill_cricket(d, x, y, w, h):
    # Batsman at the crease, stumps, green outfield, packed stand.
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 90))
    d.rectangle([x, y, x + w, y + 16], fill=(90, 110, 160))
    for sx in range(0, w, 22):
        d.ellipse([x + sx + 4, y + 3, x + sx + 14, y + 13],
                  fill=(200, 180, 150))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(210, 190, 140))
    d.rectangle([x + 60, y + h - 26, x + 240, y + h - 12],
                fill=(220, 200, 150))
    d.ellipse([x + 130, y + 16, x + 150, y + 32], fill=(200, 170, 130))
    d.rectangle([x + 132, y + 32, x + 150, y + h - 14],
                fill=(30, 90, 160))
    d.line([x + 148, y + 34, x + 170, y + h - 14], fill=(190, 150, 90),
           width=5)
    d.ellipse([x + 168, y + h - 20, x + 176, y + h - 12],
              fill=(200, 40, 40))
    for sx in [250, 262, 274]:
        d.line([x + sx, y + h - 28, x + sx, y + h - 12],
               fill=(240, 220, 120), width=3)
    d.rectangle([x + 248, y + h - 30, x + 278, y + h - 28],
                fill=(240, 220, 120))
    d.ellipse([x + 20, y + 18, x + 42, y + 40], fill=(250, 225, 120))


ILLUSTRATIONS = {
    "cop31": ill_cop31, "missiles": ill_missiles, "quake": ill_quake,
    "kyiv": ill_kyiv, "drone": ill_drone, "uranium": ill_uranium,
    "trump": ill_trump, "china": ill_china, "flight": ill_flight,
    "ai": ill_ai, "bitcoin": ill_bitcoin, "f1": ill_f1,
    "cricket": ill_cricket,
}


# ---------------------------------------------------------------- cards
def draw_hero(im, d, s, x, y, w):
    ill_h = 136
    draw_ill(im, s["ill"], x, y, w, ill_h)
    chip(d, x + 6, y + 6, s["chip"], size=9)
    caption_bar(d, x, y + ill_h - 15, w, s["caption"], size=8)
    ly = y + ill_h + 6
    d.text((x + 6, ly), f"{s['n']} {s['loc']}", font=font(SANS_B, 12),
           fill=RED)
    # green REPORTED pill, kept 5px inside the card's right border
    tag, tcol = "REPORTED", (30, 130, 60)
    tf = font(SANS_B, 9)
    tw = d.textlength(tag, font=tf) + 10
    d.rounded_rectangle([x + w - tw - 5, ly - 1, x + w - 5, ly + 12],
                        radius=6, fill=tcol)
    d.text((x + w - tw, ly + 1), tag, font=tf, fill="white")
    hy = ly + 14
    lines = wrap(d, s["headline"], font(SERIF_B, 20), w - 12)
    assert len(lines) <= 2, f"hero {s['n']} headline overflow: {lines}"
    for i, ln in enumerate(lines):
        d.text((x + 6, hy + i * 23), ln, font=font(SERIF_B, 20), fill=INK)
    by = hy + len(lines) * 23 + 2
    blines = wrap(d, s["body"], font(SANS, 12), w - 12)
    assert len(blines) <= 3, f"hero {s['n']} body overflow: {blines}"
    for i, ln in enumerate(blines):
        d.text((x + 6, by + i * 15), ln, font=font(SANS, 12),
               fill=(50, 50, 50))
    sy = by + len(blines) * 15 + 1
    d.text((x + 6, sy), s["source"], font=font(SANS, 11), fill=GREY)


def draw_small(im, d, s, x, y, w, h):
    ill_h = 56
    draw_ill(im, s["ill"], x, y, w, ill_h)
    chip(d, x + 4, y + 4, s["chip"], size=8)
    number_badge(d, x + w - 13, y + 12, s["n"], r=9)
    draw_flag(d, s["flag"], x + w - 24, y + 24)
    caption_bar(d, x, y + ill_h - 13, w, s["caption"], size=8)
    ly = y + ill_h + 5
    d.text((x + 6, ly), s["loc"], font=font(SANS_B, 10), fill=RED)
    hy = ly + 14
    lines = wrap(d, s["headline"], font(SANS_B, 13), w - 12)
    assert len(lines) <= 2, f"small {s['n']} headline overflow: {lines}"
    for i, ln in enumerate(lines):
        d.text((x + 6, hy + i * 16), ln, font=font(SANS_B, 13), fill=INK)
    by = hy + len(lines) * 16 + 1
    blines = wrap(d, s["body"], font(SANS, 11), w - 12)
    assert len(blines) <= 2, f"small {s['n']} body overflow: {blines}"
    for i, ln in enumerate(blines):
        d.text((x + 6, by + i * 14), ln, font=font(SANS, 11),
               fill=(50, 50, 50))


def draw_map(d, x0, y0):
    d.text((x0, y0), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
    d.text((x0, y0 + 15), "pins match story numbers",
           font=font(SANS, 10), fill=GREY)
    # pale-blue sea panel (real map, equirectangular lon/lat)
    d.rectangle([x0 + 4, y0 + 32, x0 + 292, y0 + 160], fill=SEA,
                outline=BORDER, width=1)

    def P(lon, lat):
        return (x0 + 16 + ((lon + 180) / 360.0) * 272,
                y0 + 36 + ((90 - lat) / 180.0) * 120)

    for poly in CONTINENTS:
        d.polygon([P(lon, lat) for lon, lat in poly], fill=TAN)
    lf = font(SANS_B, 8)
    for text, ax, ay in CITY_LABELS:
        d.text((ax, ay), text, font=lf, fill=(70, 70, 70))
    for n, (px, py) in PINS.items():
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline="white", width=1)
        fnt = font(SANS_B, 8)
        t = str(n)
        d.text((px - d.textlength(t, font=fnt) / 2, py - 4.5), t,
               font=fnt, fill="white")


def draw_list(d, x0, y0):
    d.text((x0, y0), "ALSO ON SATURDAY", font=font(SANS_B, 13), fill=INK)
    d.line([x0, y0 + 18, x0 + 708, y0 + 18], fill=RED, width=2)
    # thin vertical divider between the two columns
    d.line([x0 + 352, y0 + 22, x0 + 352, y0 + 160], fill=BORDER, width=1)
    for i, (n, prefix, rest, src) in enumerate(LIST_ITEMS):
        col = i // 11
        row = i % 11
        lx = x0 + col * 356
        ly = y0 + 24 + row * 13
        num = f"{n} "
        nf = font(SANS_B, 11)
        pf = font(SANS_B, 11)
        rf = font(SANS, 11)
        nw = d.textlength(num, font=nf)
        pw = d.textlength(prefix + ": ", font=pf)
        rw = d.textlength(rest + " ", font=rf)
        sw = d.textlength(f"({src})", font=rf)
        assert nw + pw + rw + sw <= 348, (
            f"list {n} too wide: {nw + pw + rw + sw}")
        d.text((lx, ly), num, font=nf, fill=RED)
        d.text((lx + nw, ly), prefix + ": ", font=pf, fill=INK)
        d.text((lx + nw + pw, ly), rest + " ", font=rf, fill=INK)
        d.text((lx + nw + pw + rw, ly), f"({src})", font=rf, fill=GREY)


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # Header bar
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((16, 5), "THE WORLD IN ONE DAY", font=font(SANS_B, 15),
           fill="white")
    rt = "35 STORIES · 7 REGIONS"
    d.text((W - 16 - d.textlength(rt, font=font(SANS_B, 15)), 5), rt,
           font=font(SANS_B, 15), fill="white")

    # Masthead + subtitle
    title = "Saturday 21 November 2026"
    tf = font(SERIF_B, 58)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf,
           fill=INK)
    sub = ("COP31 stalls into overtime · 6.7 quake shakes Peru · "
           "Five missiles downed over Riyadh")
    sf = font(SERIF_I, 17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 98), sub, font=sf,
           fill=RED)

    # Fact strip
    fy0, fy1 = 118, 162
    cellw = (W - 16) / 6
    for i, (num, cap) in enumerate(FACTS):
        cx = 8 + i * cellw
        nf = font(SANS_B, 28)
        d.text((cx + (cellw - d.textlength(num, font=nf)) / 2, fy0 + 2),
               num, font=nf, fill=RED)
        clines = wrap(d, cap, font(SANS, 10.5), cellw - 10)
        for j, ln in enumerate(clines[:1]):
            cf = font(SANS, 10.5)
            d.text((cx + (cellw - d.textlength(ln, font=cf)) / 2,
                    fy0 + 35 + j * 13), ln, font=cf, fill=(50, 50, 50))
        if i < 5:
            d.line([cx + cellw, fy0 + 4, cx + cellw, fy1 - 4],
                   fill=BORDER, width=1)

    # THE DAY IN UTC strip
    uy0, uy1 = 166, 182
    d.rectangle([8, uy0, W - 8, uy1], fill=NAVY)
    utc = "  ·  ".join(f"{t} {label}" for t, label in UTC_ITEMS)
    uf = font(SANS_B, 10)
    lw = d.textlength("THE DAY IN UTC  ", font=uf)
    d.text((16, uy0 + 3), "THE DAY IN UTC", font=uf, fill=(255, 220, 90))
    d.text((16 + lw, uy0 + 3), utc, font=font(SANS, 10), fill="white")

    # Region bar
    ry0, ry1 = 186, 202
    segw = (W - 16) / 7
    for i, (name, count, col) in enumerate(REGIONS):
        sx = 8 + i * segw
        d.rectangle([sx, ry0, sx + segw - 2, ry1], fill=col)
        label = f"{name} · {count}"
        lf = font(SANS_B, 11)
        d.text((sx + (segw - 2 - d.textlength(label, font=lf)) / 2,
                ry0 + 2), label, font=lf, fill="white")

    # Hero cards (thin 1px borders, 8px gaps between rows)
    hy = 206
    for i, s in enumerate(HEROES):
        hx = 8 + i * 340
        draw_hero(im, d, s, hx, hy, 328)
        d.rectangle([hx, hy, hx + 328, hy + 270], outline=BORDER, width=1)

    # Small cards, two rows of five
    for row in range(2):
        for col in range(5):
            s = SMALLS[row * 5 + col]
            sx = 8 + col * 204
            sy = 484 + row * 144
            draw_small(im, d, s, sx, sy, 196, 138)
            d.rectangle([sx, sy, sx + 196, sy + 138], outline=BORDER,
                        width=1)

    # Map + list
    draw_map(d, 8, 774)
    draw_list(d, 308, 774)

    # DATE CHECK
    dy0, dy1 = 938, 1002
    d.rectangle([8, dy0, W - 8, dy1], outline=RED, width=2)
    d.text((16, dy0 + 5), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    dc = wrap(d, DATE_CHECK, font(SANS, 12), W - 80)
    assert len(dc) <= 2, f"DATE CHECK overflow ({len(dc)} lines): {dc}"
    for i, ln in enumerate(dc):
        d.text((16, dy0 + 22 + i * 14), ln, font=font(SANS, 12), fill=INK)

    # Footer
    ff = font(SANS, 9)
    d.text(((W - d.textlength(FOOTER, font=ff)) / 2, 1008), FOOTER,
           font=ff, fill=GREY)

    im.save("entry.png", optimize=True)
    print("saved entry.png (1024, 1024)")


if __name__ == "__main__":
    main()
