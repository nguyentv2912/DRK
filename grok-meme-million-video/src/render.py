#!/usr/bin/env python3
"""GROK MEME MILLION V1.8.3 - frame renderer (Skia, 1080x1920, 30 fps).

Reproduces the reference iPhone trading-app structure (balance hero ->
equity chart -> Live screen terminal -> Bots x5 -> Activity, iOS banners,
bottom tab bar) with a detailed candlestick terminal fed by REAL OHLCV.

Usage: python3 render.py [--frames a:b] [--still T ...] [--out video.mp4]
"""
import json, math, os, sys, subprocess, argparse, functools
import datetime as dt
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(ROOT, "config.json")))
SC = json.load(open(os.path.join(ROOT, "data", "scenario.json")))
SNAP = json.load(open(os.path.join(ROOT, "data", "market_snapshot.json")))
W, H = CFG["video"]["width"], CFG["video"]["height"]
FPS, DUR = CFG["video"]["fps"], CFG["video"]["duration"]
NFR = int(round(FPS * DUR))
COL = CFG["colors"]
MX = 44  # page side margin

# ----------------------------------------------------------------- utilities

def hexc(h, a=1.0):
    h = h.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(max(0, min(1, a)) * 255))


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease(x):  # easeInOutCubic
    x = clamp(x)
    return 4 * x * x * x if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def eout(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def spring(x):  # overshoot settle
    x = clamp(x)
    return 1 - math.exp(-6 * x) * math.cos(9 * x) if x < 1 else 1.0


def lerp(a, b, k):
    return a + (b - a) * k


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


FONT_FILES = {
    ("text", 400): "Inter-Regular.otf", ("text", 500): "Inter-Medium.otf", ("text", 600): "Inter-SemiBold.otf",
    ("text", 700): "Inter-Bold.otf", ("text", 800): "Inter-ExtraBold.otf", ("text", 900): "Inter-Black.otf", ("disp", 600): "InterDisplay-SemiBold.otf", ("disp", 700): "InterDisplay-Bold.otf",
    ("disp", 800): "InterDisplay-ExtraBold.otf", ("disp", 900): "InterDisplay-Black.otf"}


@functools.lru_cache(None)
def typeface(kind, wt):
    return skia.Typeface.MakeFromFile("/usr/share/fonts/opentype/inter/" + FONT_FILES[(kind, wt)])


@functools.lru_cache(None)
def font(size, wt=500, disp=False):
    f = skia.Font(typeface("disp" if disp else "text", wt), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kSubpixelAntiAlias)
    return f


def P(color, stroke=0, shader=None, blur=0, cap=None):
    p = skia.Paint(AntiAlias=True, Color=color)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(cap or skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if shader is not None:
        p.setShader(shader)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


REG = []      # text/label layout registry for the visual critic (pre-camera screen coords)
CTX = {"layer": "page"}


def reg(kind, text, rect, container=None, size=None):
    REG.append({"layer": CTX["layer"], "kind": kind, "text": text, "size": size,
                "rect": [round(v, 1) for v in rect], "container": [round(v, 1) for v in container] if container else None})


def text(c, s, x, y, size, wt=500, color=None, align="l", disp=False, container=None, kind="text", alpha=1.0):
    """y = top of capitals. Returns advance width."""
    f = font(size, wt, disp)
    w = f.measureText(s)
    if align == "r":
        x -= w
    elif align == "c":
        x -= w / 2
    cap = f.getMetrics().fCapHeight
    col = color if color is not None else hexc(COL["text"])
    if alpha < 1:
        col = skia.ColorSetA(col, int(skia.ColorGetA(col) * alpha))
    c.drawString(s, x, y + cap, f, P(col))
    if alpha > 0.5:
        reg(kind, s, (x, y - size * .08, x + w, y + cap + size * .24), container, size)
    return w


def tw(s, size, wt=500, disp=False):
    return font(size, wt, disp).measureText(s)


def money(cents, sign=False, dec=2):
    v = cents / 100
    s = f"{abs(v):,.{dec}f}"
    if sign:
        return ("+$" if v >= 0 else "-$") + s
    return ("-$" if v < 0 else "$") + s


def pct(x, d=1):
    return ("+" if x >= 0 else "") + f"{x*100:.{d}f}%"


def compact(v):
    for k, s in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(v) >= k:
            return f"${v/k:.2f}{s}" if abs(v) / k < 10 else f"${v/k:.1f}{s}"
    return f"${v:.0f}"


def fprice(p):
    if p >= 100:
        return f"{p:,.2f}"
    if p >= 1:
        return f"{p:.3f}"
    d = max(4, -int(math.floor(math.log10(p))) + 3)
    return f"{p:.{d}f}"


def hm(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%-I:%M %p")


# ------------------------------------------------------------------- assets
LOGOS = {}
for w_ in SNAP["watchlist"]:
    if w_.get("logo"):
        try:
            LOGOS[w_["mint"]] = skia.Image.open(os.path.join(ROOT, w_["logo"]["file"]))
        except Exception:
            pass
SYM2MINT = {w_["symbol"]: w_["mint"] for w_ in SNAP["watchlist"]}
TOKCOL = [COL["pos"], COL["gold"], COL["purple"], COL["blue"], COL["orange"], COL["neg"]]


def logo(c, mint, cx, cy, r, ring=None):
    img = LOGOS.get(mint)
    c.save()
    c.clipRRect(skia.RRect.MakeOval(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r)), doAntiAlias=True)
    if img is not None:
        c.drawImageRect(img, skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    else:
        c.drawCircle(cx, cy, r, P(hexc(COL["card2"])))
        sym = next((k for k, v in SYM2MINT.items() if v == mint), "?")
        text(c, sym[:1].upper(), cx, cy - r * .36, r * .95, 700, align="c", kind="icon")
    c.restore()
    if ring:
        c.drawCircle(cx, cy, r, P(ring, 2.5))


def app_mark(c, cx, cy, r, bg=True):
    """Original Grok Bot mark: white disc with an orbit slash (not a third-party logo)."""
    if bg:
        c.drawCircle(cx, cy, r, P(hexc("#FFFFFF")))
    c.drawCircle(cx, cy, r * .46, P(hexc("#06090A"), r * .17))
    pth = skia.Path(); pth.moveTo(cx - r * .62, cy + r * .62); pth.lineTo(cx + r * .62, cy - r * .62)
    c.drawPath(pth, P(hexc("#06090A"), r * .15))


# ---------------------------------------------------------------- timeline
TR = SC["trades"]
HERO = SC["hero"]
VID_TR = [t for t in TR if t["t_video"] is not None]
HIST_TR = [t for t in TR if t["t_video"] is None]
BUYS = SC["buys"]
CAP = SC["initial_capital_c"]
HC = HERO["candles"]
NC = len(HC)
# full real series for EMA warm-up
FULL = SNAP["hero_ohlcv"]["candles"] if SC["real_chart"] else HC
WS = HERO["window_start"] if SC["real_chart"] else 0


def ema(vals, n):
    k, out, e = 2 / (n + 1), [], None
    for v in vals:
        e = v if e is None else v * k + e * (1 - k)
        out.append(e)
    return out


_fc = [c["c"] for c in FULL]
EMA7 = ema(_fc, 7)[WS:WS + NC]
EMA20 = ema(_fc, 20)[WS:WS + NC]


def rsi(closes, n=14):
    g = l = 0.0
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        g = (g * (n - 1) + max(d, 0)) / n
        l = (l * (n - 1) + max(-d, 0)) / n
    return 100 - 100 / (1 + g / l) if l > 0 else 100.0


ANCH = SC["reveal"]["anchors"]


def reveal(t):
    """Number of completed candles (float). Anchors = (time, idx) -> idx+1 complete."""
    pts = [(a[0], a[1] + 1) for a in ANCH]
    if t <= pts[0][0]:
        return float(pts[0][1])
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return float(pts[-1][1])


def candle_state(i, f):
    """Candle i as drawn at reveal f (forming candle grows within its REAL OHLC)."""
    c = HC[i]
    if i < math.floor(f) or i >= NC:
        return c
    k = f - math.floor(f)
    if k <= 0:
        return None
    cl = c["o"] + (c["c"] - c["o"]) * ease(k)
    return {"t": c["t"], "o": c["o"], "c": cl, "h": max(c["o"], cl) + (c["h"] - max(c["o"], c["c"])) * k,
            "l": min(c["o"], cl) - (min(c["o"], c["c"]) - c["l"]) * k, "v": c["v"] * k}


def cur_price(t):
    f = reveal(t)
    i = int(math.floor(f))
    if i >= NC:
        return HC[-1]["c"]
    st = candle_state(i, f)
    return st["c"] if st else HC[max(0, i - 1)]["c"]


HB = next(b for b in BUYS if b["t_video"] == SC["reveal"]["anchors"][1][0])
HERO_PARTS = [t for t in VID_TR if t.get("hero")]


def unrealized(t):
    """Hero open position marked to the REAL replay price."""
    if t < HB["t_video"]:
        return 0
    pb, p = HB["price"], cur_price(t)
    u = 0
    for part in HERO_PARTS:
        if t < part["t_video"]:
            u += part["size_c"] * (p / pb - 1)
    return u


COUNT = 0.65  # seconds for non-hero realized count-ups


def realized(t):
    r = CAP + sum(x["pnl_c"] for x in HIST_TR)
    for x in VID_TR:
        if x.get("hero"):
            if t >= x["t_video"]:
                r += x["pnl_c"]
        else:
            r += x["pnl_c"] * eout(seg(t, x["t_video"] + .12, x["t_video"] + .12 + COUNT))
    return r


def equity(t):
    return realized(t) + unrealized(t)


EQ0 = CAP + sum(x["pnl_c"] for x in HIST_TR)
FINAL = SC["final_equity_c"]

# scroll ----------------------------------------------------------------
HEADER_Y = 150
BAL_LABEL_Y = 268
BAL_Y = 318
PNL_Y = 466
PNL_SUB_Y = 528
EQ_TOP, EQ_BOT = 600, 880
TABS_Y = 906
LIVE_TITLE_Y = 1012
CARD_Y = 1078
CARD_X, CARD_W = 24, W - 48
CH_HEAD, CH_STRIP = 124, 56
CH_TOP = CH_HEAD + CH_STRIP          # chart top inside card
CH_H = 590
CH_AX = 46
WL_TOP = CH_TOP + CH_H + CH_AX + 18
TILE_H, TILE_G = 104, 12
CARD_H = WL_TOP + 50 + 2 * TILE_H + TILE_G + 74
BOTS_Y = CARD_Y + CARD_H + 64
BOT_H, BOT_G = 126, 14
ACT_Y = BOTS_Y + 70 + 5 * (BOT_H + BOT_G) + 46
ACT_H = 132
NAV_Y = 1738
S_LIVE = CARD_Y - 300
S_BOTS = BOTS_Y - 300
KEYS = [(0, 0), (2.5, 26), (3.15, S_LIVE), (9.0, S_LIVE), (9.65, S_BOTS), (11.8, S_BOTS + 300), (12.58, 0), (15, 0)]


def scroll(t):
    for (t0, s0), (t1, s1) in zip(KEYS, KEYS[1:]):
        if t <= t1:
            k = (t - t0) / (t1 - t0)
            if abs(s1 - s0) > 200:
                k = ease(k)
            return s0 + (s1 - s0) * k
    return KEYS[-1][1]


def scroll_vel(t):
    return (scroll(t + 1 / 120) - scroll(t - 1 / 120)) * 60


# ------------------------------------------------------------- events/feed
EVENTS = []  # banners / feed rows / audio
for b in BUYS:
    EVENTS.append({"t": b["t_video"], "type": "buy", "sym": b["symbol"], "mint": b.get("mint") or HERO["mint"],
                   "size_c": b["size_c"], "time": b["time"], "mc": b.get("mc"), "hero": b["symbol"] == HERO["symbol"]})
for x in VID_TR:
    EVENTS.append({"t": x["t_video"], "type": "stop" if x["kind"] == "stop" else "sell", "sym": x["symbol"], "mint": x["mint"],
                   "pnl_c": x["pnl_c"], "pct": x["pct"], "size_c": x["size_c"], "time": x["time"], "label": x["label"],
                   "agent": x["agent"], "mc": x.get("mc"), "partial": x.get("partial", ""), "hero": bool(x.get("hero"))})
EVENTS.sort(key=lambda e: e["t"])

FEED0 = []
for x in HIST_TR:
    FEED0.append({"t": -1, "type": "stop" if x["kind"] == "stop" else "sell", "sym": x["symbol"], "mint": x["mint"],
                  "pnl_c": x["pnl_c"], "pct": x["pct"], "size_c": x["size_c"], "time": x["time"], "label": x["label"],
                  "agent": "Risk" if x["kind"] == "stop" else "Executor", "partial": "50%" if "50" in x["label"] else ""})
    FEED0.append({"t": -1, "type": "buy", "sym": x["symbol"], "mint": x["mint"], "size_c": x["size_c"], "time": x["time"] - 1500})
FEED0.sort(key=lambda e: e["time"])


def feed(t):
    rows = FEED0 + [e for e in EVENTS if e["t"] <= t]
    return sorted(rows, key=lambda e: (e["t"], e["time"]), reverse=True)


def mc_txt(mc):
    return f"at {compact(mc)} MC" if mc else ""


def ev_title(e):
    sym = e["sym"]
    if e["type"] == "buy":
        return f"Bought {money(e['size_c'])} {sym}"
    if e["type"] == "stop":
        return f"Stopped {money(e['size_c'] + e['pnl_c'])} {sym}"
    return f"Sold {money(e['size_c'] + e['pnl_c'])} {sym}" + (f" {e['partial']}" if e.get("partial") else "")


# --------------------------------------------------------------- 3D coins

def draw_coin(c, cx, cy, r, ang, mint=None, alpha=1.0, blur=0.0, shadow=True):
    """Coin with real thickness: rim extrusion + lit face + moving specular."""
    ca = math.cos(ang)
    sx = max(0.06, abs(ca))
    th = r * 0.20 * math.sin(ang)  # rim thickness offset (horizontal)
    a = alpha
    if blur > 0.3:
        c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.Blur(blur, blur)))
    if shadow:
        c.drawOval(skia.Rect.MakeXYWH(cx - r * .9, cy + r * 1.05, r * 1.8, r * .34), P(hexc("#000000", .45 * a), blur=r * .18))
    # rim (back face + side)
    n = 10
    for i in range(n, 0, -1):
        off = th * i / n
        k = 0.55 + 0.25 * (i / n)
        c.drawOval(skia.Rect.MakeXYWH(cx + off - r * sx, cy - r, 2 * r * sx, 2 * r),
                   P(skia.Color(int(150 * k + 40), int(110 * k + 20), int(25 * k), int(255 * a))))
    # face
    face = skia.Rect.MakeXYWH(cx - r * sx, cy - r, 2 * r * sx, 2 * r)
    sh = skia.GradientShader.MakeRadial(skia.Point(cx - r * .35 * sx, cy - r * .45), r * 1.5,
                                        [hexc("#FFF2B0", a), hexc("#F4C34D", a), hexc("#B07A12", a)], [0, .45, 1])
    c.drawOval(face, P(hexc("#F4C34D", a), shader=sh))
    c.drawOval(skia.Rect.MakeXYWH(cx - r * .82 * sx, cy - r * .82, 2 * r * .82 * sx, 2 * r * .82), P(hexc("#8A5A0A", .55 * a), r * .06))
    if ca > 0.25:
        c.save(); c.translate(cx, cy); c.scale(sx, 1)
        if mint and mint in LOGOS:
            c.saveLayerAlpha(None, int(255 * a * clamp((ca - .25) * 3)))
            logo(c, mint, 0, 0, r * .62)
            c.restore()
        else:
            app_mark(c, 0, 0, r * .62, bg=False)
        c.restore()
    # specular sweep
    sp = (math.sin(ang * 2) + 1) / 2
    spec = skia.GradientShader.MakeLinear([skia.Point(cx - r, cy - r), skia.Point(cx + r, cy + r)],
                                          [hexc("#FFFFFF", 0), hexc("#FFFFFF", .55 * a), hexc("#FFFFFF", 0)],
                                          [max(0, sp - .15), sp, min(1, sp + .15)])
    c.drawOval(face, P(hexc("#FFFFFF"), shader=spec))
    if blur > 0.3:
        c.restore()


# ------------------------------------------------------------ status/nav

def clock_ts(t):
    a = HC[SC["reveal"]["pre"]]["t"]
    b = BUYS[-1]["time"] + 1500
    return a + (b - a) * clamp(t / 12.55) - 900 * (1 - clamp(t / 2.5))


def status_bar(c, t):
    CTX["layer"] = "chrome"
    g = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 128)], [hexc(COL["bg"], 1), hexc(COL["bg"], .96)])
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 124), P(hexc(COL["bg"]), shader=g))
    tm = dt.datetime.fromtimestamp(clock_ts(t), dt.timezone.utc).strftime("%-I:%M")
    text(c, tm, 150, 52, 40, 600, align="c")
    x0, y0 = 836, 54
    for i in range(4):
        hh = 12 + i * 7
        c.drawRoundRect(skia.Rect.MakeXYWH(x0 + i * 13, y0 + 30 - hh, 9, hh), 2.5, 2.5, P(hexc(COL["text"])))
    wx, wy = 925, 86
    for i, rr in enumerate((30, 20, 10)):
        if i < 2:
            c.drawArc(skia.Rect.MakeXYWH(wx - rr, wy - rr, 2 * rr, 2 * rr), 225, 90, False, P(hexc(COL["text"]), 6, cap=skia.Paint.kRound_Cap))
    c.drawCircle(wx, wy - 3, 5, P(hexc(COL["text"])))
    c.drawRoundRect(skia.Rect.MakeXYWH(968, 54, 62, 30), 9, 9, P(hexc(COL["text"], .45), 2.5))
    c.drawRoundRect(skia.Rect.MakeXYWH(972, 58, 44, 22), 5, 5, P(hexc(COL["text"])))
    c.drawRoundRect(skia.Rect.MakeXYWH(1032, 63, 5, 12), 2, 2, P(hexc(COL["text"], .45)))
    CTX["layer"] = "page"


def nav_bar(c, t):
    CTX["layer"] = "chrome"
    g = skia.GradientShader.MakeLinear([skia.Point(0, NAV_Y - 40), skia.Point(0, NAV_Y + 10)], [hexc(COL["bg"], 0), hexc("#0A0E10", .98)])
    c.drawRect(skia.Rect.MakeXYWH(0, NAV_Y - 40, W, H - NAV_Y + 40), P(hexc("#0A0E10"), shader=g))
    c.drawRect(skia.Rect.MakeXYWH(0, NAV_Y + 10, W, 1.5), P(hexc(COL["line"])))
    labels = ["Home", "Bots", "Activity", "Account"]
    for i, lab in enumerate(labels):
        cx = 135 + i * 270
        col = hexc(COL["text"]) if i == 0 else hexc(COL["text3"])
        cy = NAV_Y + 62
        if i == 0:
            pth = skia.Path(); pth.moveTo(cx - 22, cy - 2); pth.lineTo(cx, cy - 22); pth.lineTo(cx + 22, cy - 2)
            pth.lineTo(cx + 22, cy + 22); pth.lineTo(cx - 22, cy + 22); pth.close()
            c.drawPath(pth, P(col))
            c.drawRoundRect(skia.Rect.MakeXYWH(cx - 6, cy + 6, 12, 16), 3, 3, P(hexc("#0A0E10")))
        elif i == 1:
            for dx in (-11, 11):
                c.drawCircle(cx + dx, cy - 10, 8, P(col, 3.5))
                c.drawArc(skia.Rect.MakeXYWH(cx + dx - 14, cy + 2, 28, 28), 180, 180, False, P(col, 3.5))
        elif i == 2:
            pth = skia.Path(); pth.moveTo(cx - 26, cy + 4); pth.lineTo(cx - 12, cy + 4); pth.lineTo(cx - 4, cy - 16)
            pth.lineTo(cx + 6, cy + 20); pth.lineTo(cx + 13, cy + 4); pth.lineTo(cx + 26, cy + 4)
            c.drawPath(pth, P(col, 3.5))
        else:
            c.drawCircle(cx, cy - 10, 10, P(col, 3.5))
            c.drawArc(skia.Rect.MakeXYWH(cx - 19, cy + 4, 38, 34), 180, 180, False, P(col, 3.5))
        text(c, lab, cx, NAV_Y + 104, 25, 600 if i == 0 else 500, col, align="c")
    c.drawRoundRect(skia.Rect.MakeXYWH(W / 2 - 140, H - 26, 280, 10), 5, 5, P(hexc(COL["text"], .9)))
    CTX["layer"] = "page"


# ------------------------------------------------------------- odometer

def odometer(c, value_c, x, y, size, wt, color, disp=True, align="l", prefix="$", glow=0.0, layer_kind="value"):
    """Rolling digits (tabular cells). value_c: float cents."""
    v = max(0.0, value_c) / 100.0
    whole = f"{int(v):,}"
    s = prefix + whole + "." + f"{int(round((v - int(v)) * 100)) % 100:02d}"
    f = font(size, wt, disp)
    dw = max(f.measureText(d) for d in "0123456789")
    widths = [dw if ch.isdigit() else f.measureText(ch) for ch in s]
    total = sum(widths)
    if align == "r":
        x -= total
    elif align == "c":
        x -= total / 2
    cap = f.getMetrics().fCapHeight
    # digit place values for odometer roll
    digits = [i for i, ch in enumerate(s) if ch.isdigit()]
    nd = len(digits)
    scaled = v * 100
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(x - 10, y - size * .2, total + 20, cap + size * .42))
    if glow > 0:
        c.save()
        for ch, xx in zip(s, np.cumsum([0] + widths[:-1])):
            pass
        c.restore()
    xx = x
    di = 0
    for ch, wch in zip(s, widths):
        if ch.isdigit():
            place = nd - 1 - di  # 0 = cents units
            q = scaled / (10 ** place)
            d = int(q) % 10
            lower = (scaled % (10 ** place)) / (10 ** place) if place > 0 else q - int(q)
            roll = clamp((lower - 0.9) * 10) if place > 0 else 0
            roll = ease(roll)
            off = roll * (cap + size * .3)
            ox = xx + (dw - f.measureText(str(d))) / 2
            c.drawString(str(d), ox, y + cap - off, f, P(color))
            if roll > 0:
                d2 = (d + 1) % 10
                c.drawString(str(d2), xx + (dw - f.measureText(str(d2))) / 2, y + cap - off + cap + size * .3, f, P(color))
            di += 1
        else:
            c.drawString(ch, xx, y + cap, f, P(color))
        xx += wch
    c.restore()
    reg(layer_kind, s, (x, y - size * .08, x + total, y + cap + size * .24), None, size)
    return total, s


def sheen(c, rect, k):
    """Light reflection sweeping across a value."""
    if k <= 0 or k >= 1:
        return
    x = rect.left() + (rect.width() + 300) * k - 150
    sh = skia.GradientShader.MakeLinear([skia.Point(x - 120, rect.top()), skia.Point(x + 120, rect.bottom())],
                                        [hexc("#FFFFFF", 0), hexc("#FFFFFF", .32), hexc("#FFFFFF", 0)])
    p = P(hexc("#FFFFFF"), shader=sh)
    p.setBlendMode(skia.BlendMode.kSrcATop)
    c.drawRect(rect, p)


# ------------------------------------------------------------- portfolio

def eq_series(t):
    """Equity curve: history points then video timeline sampled; right end = now."""
    pts = [CAP]
    e = CAP
    for x in HIST_TR:
        e0 = e
        e += x["pnl_c"]
        pts += [e0 + x["pnl_c"] * k for k in (.15, .55, .9, 1.0)] + [e - abs(x["pnl_c"]) * .06, e]
    hist_n = len(pts)
    tt = np.linspace(0, max(t, 0.01), max(3, int(6 + t * 7)))
    vid = [equity(s) for s in tt]
    return pts, vid, hist_n


def portfolio(c, oy, t):
    CTX["layer"] = "page"
    y = HEADER_Y - oy
    # header
    app_mark(c, MX + 36, y + 36, 36)
    text(c, CFG["app_name"], MX + 92, y + 22, 40, 700)
    cx = MX + 92 + tw(CFG["app_name"], 40, 700) + 16
    pth = skia.Path(); pth.moveTo(cx, y + 26); pth.lineTo(cx + 9, y + 36); pth.lineTo(cx, y + 46)
    c.drawPath(pth, P(hexc(COL["text3"]), 3.5))
    # search, bell, paper chip
    c.drawCircle(700, y + 33, 15, P(hexc(COL["text"]), 4)); c.drawLine(711, y + 44, 722, y + 55, P(hexc(COL["text"]), 4.5))
    bx = 782
    pth = skia.Path(); pth.moveTo(bx - 17, y + 50); pth.lineTo(bx - 13, y + 44); pth.lineTo(bx - 13, y + 30)
    pth.cubicTo(bx - 13, y + 12, bx + 13, y + 12, bx + 13, y + 30); pth.lineTo(bx + 13, y + 44); pth.lineTo(bx + 17, y + 50); pth.close()
    c.drawPath(pth, P(hexc(COL["text"]), 3.5)); c.drawCircle(bx, y + 56, 4, P(hexc(COL["text"])))
    c.drawCircle(bx + 12, y + 18, 7, P(hexc(COL["neg"])))
    chip = skia.Rect.MakeXYWH(836, y + 10, 200, 52)
    c.drawRoundRect(chip, 26, 26, P(hexc(COL["pos"], .14)))
    pulse = .55 + .45 * math.sin(t * 6)
    c.drawCircle(864, y + 36, 7, P(hexc(COL["pos"], pulse)))
    text(c, "Paper", 882, y + 25, 30, 600, hexc(COL["pos"]), container=(chip.left(), chip.top(), chip.right(), chip.bottom()))
    # wallet row
    n_open = 1 if HB["t_video"] <= t < HERO_PARTS[-1]["t_video"] else 0
    n_open += 1 if any(b["t_video"] <= t < tr for b, tr in ((BUYS[1], VID_TR[2]["t_video"]), (BUYS[2], VID_TR[-1]["t_video"]))) else 0
    text(c, f"Concept wallet · {n_open} open", MX, y + 96, 28, 500, hexc(COL["text2"]))
    text(c, hm(clock_ts(t)) + " UTC", W - MX, y + 96, 28, 500, hexc(COL["text2"]), align="r")
    # balance
    yb = BAL_LABEL_Y + 0 - oy + 44
    text(c, "Portfolio Balance", MX, yb, 30, 500, hexc(COL["text2"]))
    badge = "CONCEPT TRADES"
    bw = tw(badge, 22, 700) + 28
    r = skia.Rect.MakeXYWH(W - MX - bw, yb - 8, bw, 40)
    c.drawRoundRect(r, 10, 10, P(hexc(COL["card2"])))
    c.drawRoundRect(r, 10, 10, P(hexc(COL["line"]), 2))
    text(c, badge, r.left() + 14, yb + 2, 22, 700, hexc(COL["text2"]), container=(r.left(), r.top(), r.right(), r.bottom()))
    e = equity(t)
    by = BAL_Y - oy + 44
    # finale reflection / glow
    fin = seg(t, 12.6, 13.4)
    glow_k = seg(t, 12.6, 12.9) * (1 - seg(t, 14.5, 15))
    if glow_k > 0:
        c.drawRoundRect(skia.Rect.MakeXYWH(MX - 10, by - 16, 760, 130), 40, 40, P(hexc(COL["pos"], .16 * glow_k), blur=40))
    wbal, sbal = odometer(c, e, MX, by, 128, 700, hexc(COL["text"]), disp=True)
    if t > 12.9:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(MX, by - 10, wbal, 120))
        sheen(c, skia.Rect.MakeXYWH(MX, by - 10, wbal, 120), seg(t, 13.25, 13.95))
        c.restore()
    pnl = e - CAP
    roi = pnl / CAP
    py = PNL_Y - oy + 44
    col = hexc(COL["pos"] if pnl >= 0 else COL["neg"])
    tri = skia.Path(); tri.moveTo(MX, py + 30); tri.lineTo(MX + 13, py + 8); tri.lineTo(MX + 26, py + 30); tri.close()
    c.drawPath(tri, P(col))
    s1 = f"{money(int(round(pnl)), True)} ({pct(roi, 2)})"
    w1 = text(c, s1, MX + 40, py, 42, 700, col, kind="value")
    mult = f"{e / CAP:.2f}x"
    pr = skia.Rect.MakeXYWH(MX + 40 + w1 + 22, py - 12, tw(mult, 38, 800, True) + 34, 62)
    c.drawRoundRect(pr, 31, 31, P(hexc(COL["pos"])))
    text(c, mult, pr.centerX(), py, 38, 800, hexc("#04140C"), align="c", disp=True, container=(pr.left(), pr.top(), pr.right(), pr.bottom()), kind="value")
    text(c, f"Total P&L · ROI vs {money(CAP)} start", MX, PNL_SUB_Y - oy + 44, 28, 500, hexc(COL["text2"]))
    # equity chart
    top, bot = EQ_TOP - oy + 44, EQ_BOT - oy + 30
    hist, vid, hn = eq_series(t)
    allv = hist + vid
    lo, hi = min(allv), max(allv)
    hi = max(hi, lo + 1)
    n = len(allv)
    xs = [i / (n - 1) * (W - 70) for i in range(n)]
    ys = [bot - (v - lo) / (hi - lo) * (bot - top - 70) for v in allv]
    path = skia.Path(); path.moveTo(xs[0], ys[0])
    for i in range(1, n):
        mx_ = (xs[i - 1] + xs[i]) / 2
        path.cubicTo(mx_, ys[i - 1], mx_, ys[i], xs[i], ys[i])
    fill = skia.Path(path); fill.lineTo(xs[-1], bot + 10); fill.lineTo(0, bot + 10); fill.close()
    c.drawPath(fill, P(hexc(COL["pos"]), shader=skia.GradientShader.MakeLinear(
        [skia.Point(0, top), skia.Point(0, bot)], [hexc(COL["pos"], .30), hexc(COL["pos"], 0)])))
    c.drawPath(path, P(hexc(COL["pos"], .45), 12, blur=10))
    c.drawPath(path, P(hexc(COL["pos"]), 5))
    ex, ey = xs[-1], ys[-1]
    pr_ = (t * 1.6) % 1
    c.drawCircle(ex, ey, 10 + 26 * pr_, P(hexc(COL["pos"], .5 * (1 - pr_))))
    c.drawCircle(ex, ey, 11, P(hexc(COL["pos"])))
    c.drawCircle(ex, ey, 5, P(hexc("#FFFFFF")))
    # P&L pills for the latest wins (above the point where the sale landed)
    wins = [x for x in VID_TR if x["t_video"] <= t and x["pnl_c"] > 0][-2:]
    placed = []
    for x in wins:
        k = clamp((x["t_video"] + .3) / max(t, .01))
        idx = hn + int(k * (len(vid) - 1))
        idx = min(idx, n - 1)
        px, py_ = xs[idx], ys[idx]
        lab = money(x["pnl_c"], True)
        pw = tw(lab, 28, 700) + 70
        rx = clamp(px - pw / 2, 12, W - 12 - pw)
        ry = max(top - 6, py_ - 92)
        if any(abs(ry - q[1]) < 60 and abs(rx - q[0]) < pw for q in placed):
            ry -= 66
        placed.append((rx, ry))
        a = eout(seg(t, x["t_video"] + .1, x["t_video"] + .45))
        c.saveLayerAlpha(None, int(255 * a))
        rr = skia.Rect.MakeXYWH(rx, ry, pw, 54)
        c.drawRoundRect(rr, 27, 27, P(hexc("#0E1A14")))
        c.drawRoundRect(rr, 27, 27, P(hexc(COL["pos"], .7), 2.5))
        logo(c, x["mint"], rx + 28, ry + 27, 17)
        text(c, lab, rx + 52, ry + 15, 28, 700, hexc(COL["pos"]), container=(rr.left(), rr.top(), rr.right(), rr.bottom()), kind="value")
        c.drawLine(px, ry + 54, px, py_ - 12, P(hexc(COL["pos"], .5), 2))
        c.restore()
    # timeframe tabs
    ty = TABS_Y - oy + 30
    tabs = ["Replay", "1H", "4H", "1D", "1W", "ALL"]
    for i, tb in enumerate(tabs):
        cx = MX + 80 + i * 186 if i else MX + 80
        if i == 0:
            rr = skia.Rect.MakeXYWH(MX, ty, 172, 60)
            c.drawRoundRect(rr, 30, 30, P(hexc(COL["pos"])))
            c.drawCircle(MX + 28, ty + 30, 6, P(hexc("#04140C")))
            text(c, "REPLAY", MX + 44, ty + 19, 26, 800, hexc("#04140C"), container=(rr.left(), rr.top(), rr.right(), rr.bottom()))
        else:
            text(c, tb, MX + 172 + (i - .5) * ((W - 2 * MX - 172) / 5), ty + 18, 30, 600, hexc(COL["text2"]), align="c")
    # live screen title
    ly = LIVE_TITLE_Y - oy + 6
    text(c, "Live screen", MX, ly, 44, 700)
    text(c, "Bot's computer", W - MX, ly + 8, 32, 500, hexc(COL["pos"]), align="r")


# ------------------------------------------------------------- terminal

def chart_status(t):
    st = [(0, "Executor · watching", COL["text2"]), (2.9, "Analyst · scoring", COL["gold"]),
          (HB["t_video"] - .15, "Executor · buying", COL["pos"]), (HB["t_video"] + .7, "Risk · trailing", COL["text2"])]
    for x in HERO_PARTS:
        st += [(x["t_video"] - .2, "Executor · selling", COL["neg"]), (x["t_video"] + .8, "Risk · trailing", COL["text2"])]
    st += [(HERO_PARTS[-1]["t_video"] + .8, "Scanner · next setup", COL["text2"])]
    cur = st[0]
    for s in st:
        if t >= s[0]:
            cur = s
    return cur


def terminal(c, oy, t, cam):
    CTX["layer"] = "page"
    x0, y0 = CARD_X, CARD_Y - oy
    card = skia.Rect.MakeXYWH(x0, y0, CARD_W, CARD_H)
    if y0 > H or y0 + CARD_H < 0:
        return
    c.drawRoundRect(card.makeOffset(0, 18), 34, 34, P(hexc("#000000", .55), blur=28))
    c.drawRoundRect(card, 34, 34, P(hexc("#0B1012")))
    c.drawRoundRect(card, 34, 34, P(hexc(COL["line"]), 2))
    cont = (card.left(), card.top(), card.right(), card.bottom())
    # header: logo, ticker, pair, dex, price
    hx, hy = x0 + 28, y0 + 26
    logo(c, HERO["mint"], hx + 36, hy + 36, 36, ring=hexc(COL["line"]))
    sym = HERO["symbol"].upper() if SC["real_chart"] else "CONCEPT"
    text(c, f"{sym} / SOL", hx + 90, hy + 4, 38, 700, container=cont)
    dex = {"pumpswap": "PumpSwap", "raydium": "Raydium", "meteora": "Meteora", "orca": "Orca"}.get(HERO.get("dex") or "", (HERO.get("dex") or "DEX").title())
    pool = HERO.get("pool") or ""
    text(c, f"{dex} · Pool {pool[:4]}…{pool[-4:]}", hx + 90, hy + 52, 25, 500, hexc(COL["text2"]), container=cont)
    p = cur_price(t)
    f = reveal(t)
    p0 = HC[max(0, SC["reveal"]["pre"] - 1)]["c"]
    ch = p / p0 - 1
    colp = hexc(COL["pos"] if ch >= 0 else COL["neg"])
    text(c, "$" + fprice(p), x0 + CARD_W - 28, hy + 2, 44, 700, colp, align="r", disp=True, container=cont, kind="value")
    text(c, f"{pct(ch, 2)} replay · 5m", x0 + CARD_W - 28, hy + 56, 25, 600, colp, align="r", container=cont)
    # strip
    sy = y0 + CH_HEAD
    c.drawRect(skia.Rect.MakeXYWH(x0, sy, CARD_W, 1.5), P(hexc(COL["line"])))
    c.drawRect(skia.Rect.MakeXYWH(x0, sy + CH_STRIP, CARD_W, 1.5), P(hexc(COL["line"])))
    c.drawCircle(x0 + 34, sy + 28, 7, P(hexc(COL["neg"], .6 + .4 * math.sin(t * 7))))
    text(c, "Replay · Bot's computer", x0 + 50, sy + 18, 26, 600, container=cont)
    sname, scol = chart_status(t)[1:]
    text(c, sname, x0 + CARD_W - 28, sy + 18, 26, 600, hexc(scol), align="r", container=cont)
    # chart geometry
    PL, PR = x0 + 16, x0 + CARD_W - 138
    PT, PB = y0 + CH_TOP + 52, y0 + CH_TOP + CH_H - 120
    VT, VB = PB + 14, y0 + CH_TOP + CH_H - 8
    NV = 44
    spacing = (PR - PL - 40) / NV
    first = clamp(f - (NV - 6), 0, NC)
    xof = lambda i: PL + 20 + (i - first + .5) * spacing
    lo_i, hi_i = max(0, int(first) - 1), min(NC, int(math.ceil(f)) + 1)
    # smoothed y-range (deterministic average over the last 0.5 s)
    los, his = [], []
    for k in range(6):
        fk = reveal(max(0, t - k * .1))
        a_, b_ = max(0, int(clamp(fk - (NV - 6), 0, NC))), min(NC, int(math.ceil(fk)))
        sl = [candle_state(i, fk) for i in range(a_, b_)]
        sl = [s for s in sl if s]
        los.append(min(s["l"] for s in sl)); his.append(max(s["h"] for s in sl))
    lo, hi = sum(los) / len(los), sum(his) / len(his)
    pad = (hi - lo) * .10
    lo, hi = lo - pad, hi + pad
    yof = lambda v: PB - (v - lo) / (hi - lo) * (PB - PT)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(PL, y0 + CH_TOP + 2, x0 + CARD_W - 2, VB + CH_AX))
    # grid + price axis (one decimal precision for the whole axis)
    axd = max(2, -int(math.floor(math.log10(hi))) + 3) if hi < 1 else 3
    p_y = yof(cur_price(t))
    for k in range(6):
        v = lo + (hi - lo) * (k + .5) / 6
        yy = yof(v)
        c.drawLine(PL, yy, PR, yy, P(hexc(COL["line"], .8), 1.2))
        if abs(yy - p_y) < 44:
            continue
        text(c, f"{v:.{axd}f}", x0 + CARD_W - 18, yy - 9, 23, 500, hexc(COL["text2"]), align="r", container=cont, kind="axis")
    c.drawLine(PR, PT - 40, PR, VB, P(hexc(COL["line"]), 1.5))
    # time axis labels
    for i in range(lo_i, hi_i):
        if (HC[i]["t"] // 300) % 12 == 0:
            xx = xof(i)
            if PL + 30 < xx < PR - 40 and abs(xx - xof(min(NC - 1, int(math.floor(f))))) > 110:
                c.drawLine(xx, PT - 30, xx, VB, P(hexc(COL["line"], .5), 1))
                text(c, dt.datetime.fromtimestamp(HC[i]["t"], dt.timezone.utc).strftime("%H:%M"), xx, VB + 14, 23, 500,
                     hexc(COL["text2"]), align="c", container=cont, kind="axis")
    # breakout band
    bo = None
    for i in range(22, int(math.ceil(f))):
        if i < NC and HC[i]["c"] > max(cc["h"] for cc in HC[i - 20:i]):
            bo = i
    if bo is not None:
        tb = SC["reveal"]["start"]
        # time candle bo completed
        lvl = max(cc["h"] for cc in HC[bo - 20:bo])
        age = f - (bo + 1)
        if 0 <= age < 9:
            a = (1 - age / 9)
            c.drawRect(skia.Rect.MakeLTRB(PL, yof(lvl) - 3, PR, yof(lvl) + 3), P(hexc(COL["gold"], .55 * a)))
            c.drawRect(skia.Rect.MakeLTRB(PL, yof(lvl) - 26, PR, yof(lvl)), P(hexc(COL["gold"], .10 * a)))
    # volume
    vis = [candle_state(i, f) for i in range(lo_i, hi_i)]
    vmax = max((s["v"] for s in vis if s), default=1) or 1
    rects = []
    for i in range(lo_i, hi_i):
        s = candle_state(i, f)
        if not s:
            continue
        xx = xof(i)
        up = s["c"] >= s["o"]
        cc = hexc(COL["pos"] if up else COL["neg"])
        vh = (VB - VT) * s["v"] / vmax
        c.drawRect(skia.Rect.MakeLTRB(xx - spacing * .34, VB - vh, xx + spacing * .34, VB), P(skia.ColorSetA(cc, 110)))
        yh, yl, yo, yc = yof(s["h"]), yof(s["l"]), yof(s["o"]), yof(s["c"])
        c.drawLine(xx, yh, xx, yl, P(cc, 2.4, cap=skia.Paint.kButt_Cap))
        body = skia.Rect.MakeLTRB(xx - spacing * .36, min(yo, yc), xx + spacing * .36, max(max(yo, yc), min(yo, yc) + 2.5))
        c.drawRect(body, P(cc))
        rects.append((xx - spacing * .5, yh - 4, xx + spacing * .5, yl + 4))
    # EMAs
    for arr, colr, nn in ((EMA7, COL["gold"], 7), (EMA20, COL["purple"], 20)):
        pth = skia.Path(); started = False
        last = min(NC - 1, int(math.floor(f)) - 1)
        for i in range(lo_i, last + 1):
            if WS + i < nn - 1 and SC["real_chart"]:
                continue
            xx, yy = xof(i), yof(arr[i])
            if not started:
                pth.moveTo(xx, yy); started = True
            else:
                pth.lineTo(xx, yy)
        c.drawPath(pth, P(hexc(colr, .95), 3.2))
    c.restore()
    # legend
    last = max(0, min(NC - 1, int(math.floor(f)) - 1))
    lx = PL + 8
    ly = y0 + CH_TOP + 14
    lw = text(c, f"EMA7 {fprice(EMA7[last])}", lx, ly, 23, 600, hexc(COL["gold"]), container=cont)
    lw2 = text(c, f"EMA20 {fprice(EMA20[last])}", lx + lw + 24, ly, 23, 600, hexc(COL["purple"]), container=cont)
    closes = [cc["c"] for cc in FULL[:WS + last + 1]]
    rs = rsi(closes[-60:])
    text(c, f"RSI14 {rs:.1f}", lx + lw + lw2 + 48, ly, 23, 600, hexc(COL["text2"]), container=cont)
    legend_rect = (lx - 4, ly - 6, lx + lw + lw2 + 48 + tw(f"RSI14 {rs:.1f}", 23, 600) + 4, ly + 30)
    # current price line + crosshair
    cy_ = yof(p)
    lastc = candle_state(min(NC - 1, int(math.floor(f))), f) or HC[last]
    cc = hexc(COL["pos"] if lastc["c"] >= lastc["o"] else COL["neg"])
    dash = P(cc, 2)
    dash.setPathEffect(skia.DashPathEffect.Make([10, 8], (t * 40) % 18))
    c.drawLine(PL, cy_, PR, cy_, dash)
    cxh = xof(min(NC - 1, int(math.floor(f))))
    ch_p = P(hexc(COL["text2"], .6), 1.5)
    ch_p.setPathEffect(skia.DashPathEffect.Make([6, 7], 0))
    c.drawLine(cxh, PT - 30, cxh, VB, ch_p)
    c.drawCircle(cxh, cy_, 9, P(hexc(COL["text"], .25)))
    c.drawCircle(cxh, cy_, 5, P(hexc(COL["text"])))
    lab = f"{p:.{axd}f}"
    pr_r = skia.Rect.MakeXYWH(PR + 2, cy_ - 20, x0 + CARD_W - PR - 10, 40)
    c.drawRoundRect(pr_r, 8, 8, P(cc))
    text(c, lab, pr_r.centerX(), cy_ - 9, 23, 700, hexc("#04140C" if lastc["c"] >= lastc["o"] else "#FFFFFF"), align="c",
         container=(pr_r.left() - 2, pr_r.top(), pr_r.right() + 2, pr_r.bottom()), kind="axis")
    tl = dt.datetime.fromtimestamp(HC[min(NC - 1, int(math.floor(f)))]["t"], dt.timezone.utc).strftime("%H:%M")
    tr = skia.Rect.MakeXYWH(cxh - 46, VB + 8, 92, 36)
    c.drawRoundRect(tr, 8, 8, P(hexc("#2A333A")))
    text(c, tl, cxh, VB + 15, 23, 700, align="c", container=(tr.left(), tr.top(), tr.right(), tr.bottom()), kind="axis")
    # BUY / SELL markers (concept trades at REAL candle closes)
    marks = [("BUY", HERO["buy_idx"], HB["t_video"], HB["size_c"], None)]
    for x in HERO_PARTS:
        marks.append(("SELL", x["idx"], x["t_video"], x["size_c"], x))
    placed = [legend_rect, (pr_r.left(), pr_r.top(), pr_r.right(), pr_r.bottom())]
    tris = []
    for kind, idx, tv, size, x in marks:
        if t >= tv and idx >= first - .5 and xof(idx) <= PR - 4:
            xx_ = xof(idx)
            if kind == "BUY":
                ty0 = yof(HC[idx]["l"]) + 16; tris.append((xx_ - 15, ty0 - 2, xx_ + 15, ty0 + 22))
            else:
                ty0 = yof(HC[idx]["h"]) - 16; tris.append((xx_ - 15, ty0 - 22, xx_ + 15, ty0 + 2))
    placed += tris
    REG.append({"layer": "page", "kind": "triangles", "text": "", "rect": None, "container": None, "tris": [[round(v, 1) for v in r] for r in tris]})
    events = []
    for kind, idx, tv, size, x in marks:
        if t < tv or idx < first - .5:
            continue
        s = HC[idx]
        xx = xof(idx)
        if xx > PR - 4:
            continue
        a = eout(seg(t, tv, tv + .25))
        isbuy = kind == "BUY"
        mc = hexc(COL["pos"] if isbuy else COL["neg"])
        if isbuy:
            ty_ = yof(s["l"]) + 16
            tri = skia.Path(); tri.moveTo(xx, ty_); tri.lineTo(xx - 13, ty_ + 20); tri.lineTo(xx + 13, ty_ + 20); tri.close()
            anchor_y = ty_ + 10
            lab1, lab2 = "BUY", money(size)
        else:
            ty_ = yof(s["h"]) - 16
            tri = skia.Path(); tri.moveTo(xx, ty_); tri.lineTo(xx - 13, ty_ - 20); tri.lineTo(xx + 13, ty_ - 20); tri.close()
            anchor_y = ty_ - 10
            lab1 = "SELL" + (" 50%" if x.get("partial") else "")
            lab2 = money(x["pnl_c"], True)
        # pulse
        pk = seg(t, tv, tv + .8)
        if 0 < pk < 1:
            c.drawCircle(xx, anchor_y, 14 + 70 * eout(pk), P(skia.ColorSetA(mc, int(200 * (1 - pk))), 4))
            c.drawCircle(xx, anchor_y, 30, P(skia.ColorSetA(mc, int(120 * (1 - pk))), blur=18))
        c.drawPath(tri, P(skia.ColorSetA(mc, int(255 * a))))
        # pill placement avoiding candles / price label / legend
        f1, f2 = font(25, 800), font(25, 700)
        pw = f1.measureText(lab1) + f2.measureText(lab2) + 46
        ph = 46
        px_ = clamp(xx - pw / 2, PL + 4, PR - pw - 4)
        cand = []
        for dyk in range(0, 44):
            if isbuy:
                cand += [anchor_y + 22 + dyk * 12, anchor_y - 60 - ph - dyk * 12]
            else:
                cand += [anchor_y - 22 - ph - dyk * 12, anchor_y + 60 + dyk * 12]
        chosen = None
        xs_c = [px_] + [clamp(xx + d, PL + 4, PR - pw - 4) for d in (24, -pw - 24, 60, -pw - 60)]
        for py_, pxx in [(a_, b_) for b_ in xs_c for a_ in cand]:
            rr = (pxx, py_, pxx + pw, py_ + ph)
            if rr[1] < PT - 36 or rr[3] > PB + 8:
                continue
            if any(not (rr[2] < q[0] or rr[0] > q[2] or rr[3] < q[1] or rr[1] > q[3]) for q in rects + placed):
                continue
            if rr[1] - 4 < cy_ < rr[3] + 4:
                continue
            chosen = rr
            break
        if chosen is None:
            REG.append({"layer": "page", "kind": "pill_missing", "text": lab1, "rect": None, "container": None})
            continue
        placed.append(chosen)
        rr = skia.Rect.MakeLTRB(*chosen)
        c.saveLayerAlpha(None, int(255 * a))
        ly_ = rr.top() if rr.top() > anchor_y else rr.bottom()
        c.drawLine(xx, anchor_y, clamp(xx, rr.left() + 12, rr.right() - 12), ly_, P(skia.ColorSetA(mc, 160), 2))
        c.drawRoundRect(rr.makeOffset(0, 6), 12, 12, P(hexc("#000000", .5), blur=8))
        c.drawRoundRect(rr, 12, 12, P(hexc("#0E1316")))
        c.drawRoundRect(rr, 12, 12, P(mc, 3))
        w1 = text(c, lab1, rr.left() + 16, rr.top() + 12, 25, 800, mc, container=chosen, kind="chart_label")
        vcol = hexc(COL["pos"] if isbuy or x["pnl_c"] >= 0 else COL["neg"])
        text(c, lab2, rr.left() + 30 + w1, rr.top() + 12, 25, 700, vcol if not isbuy else hexc(COL["text"]), container=chosen, kind="chart_label")
        c.restore()
        events.append((kind, xx, anchor_y, tv, x))
    REG.append({"layer": "page", "kind": "candles", "text": "", "rect": None, "container": None,
                "candles": [[round(v, 1) for v in r] for r in rects], "plot": [PL, PT, PR, PB],
                "markers_visible": [e[0] for e in events]})
    # watchlist
    wy = y0 + WL_TOP
    text(c, "Trending · Solana · 24h", x0 + 28, wy, 30, 700, container=cont)
    text(c, "verified mint + pool", x0 + CARD_W - 28, wy + 4, 24, 600, hexc(COL["pos"]), align="r", container=cont)
    tiles = SNAP["watchlist"][:6]
    tw_ = (CARD_W - 56 - 2 * 14) / 3
    for k, tk in enumerate(tiles):
        tx = x0 + 28 + (k % 3) * (tw_ + 14)
        ty = wy + 50 + (k // 3) * (TILE_H + TILE_G)
        r = skia.Rect.MakeXYWH(tx, ty, tw_, TILE_H)
        hl = tk["mint"] == HERO["mint"]
        c.drawRoundRect(r, 18, 18, P(hexc("#141B1E" if not hl else "#12221B")))
        c.drawRoundRect(r, 18, 18, P(hexc(COL["pos"] if hl else COL["line"], .9 if hl else 1), 2))
        tc = (r.left(), r.top(), r.right(), r.bottom())
        logo(c, tk["mint"], tx + 34, ty + 34, 22)
        symb = tk["symbol"][:7]
        text(c, symb, tx + 66, ty + 18, 27, 700, container=tc)
        chg = tk["price_change_h24"] / 100
        text(c, pct(chg, 1 if abs(chg) < 10 else 0), r.right() - 14, ty + 20, 23, 700, hexc(COL["pos"] if chg >= 0 else COL["neg"]), align="r", container=tc)
        text(c, "$" + fprice(tk["price_usd"]), tx + 16, ty + 64, 23, 600, hexc(COL["text"]), container=tc)
        text(c, "V " + compact(tk["volume_h24"]).lstrip("$"), r.right() - 14, ty + 64, 22, 500, hexc(COL["text2"]), align="r", container=tc)
    snap_t = dt.datetime.strptime(SNAP["snapshot_finished_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d %H:%M UTC")
    fy = wy + 50 + 2 * TILE_H + TILE_G + 22
    text(c, f"Real OHLCV · GeckoTerminal · snapshot {snap_t}", x0 + 28, fy, 23, 500, hexc(COL["text2"]), container=cont)
    text(c, "Markers = concept trades", x0 + CARD_W - 28, fy, 23, 600, hexc(COL["gold"]), align="r", container=cont)
    return events


# ---------------------------------------------------------------- agents
AG_COL = ["#22D3EE", "#FF5D72", "#A78BFA", "#20D58B", "#FB923C"]
AG_NAMES = ["Scanner", "Analyst", "Brain", "Executor", "Risk Engine"]


def agent_frames(t):
    syms = [w_["symbol"] for w_ in SNAP["watchlist"]]
    mints = [w_["mint"] for w_ in SNAP["watchlist"]]
    out = []
    # Scanner: cycles through verified trending pools
    k = int(t / 0.9) % len(syms)
    pools = 1580 + int(t * 31)
    out.append((f"{syms[k]} → Analyst · trending 24h", f"{pools:,} pools", COL["text"], mints[k], (t / 0.9) % 1))
    # timeline-driven agents
    buys = sorted(BUYS, key=lambda b: b["t_video"])
    an = None
    for b in buys:
        st = b["t_video"] - 0.8
        if t >= st:
            an = b
    if an is None:
        an = buys[0]; prog = 0.05
    else:
        prog = clamp((t - (an["t_video"] - 0.8)) / 0.8)
    checks = 1 + int(prog * 7.99)
    score = 80 + (int(an["size_c"]) % 15)
    out.append((f"{an['symbol']} {checks}/8 · {'passed' if checks == 8 else 'checking'}", f"score {score}",
                COL["pos"] if checks == 8 else COL["gold"], an.get("mint") or HERO["mint"], prog))
    br = None
    for b in buys:
        if t >= b["t_video"] - 0.35:
            br = b
    if br:
        out.append((f"Sizing {br['symbol']} · {round(br['size_c'] / 100 / (equity(br['t_video']) / 100) * 100)}% of cash",
                    money(br["size_c"]), COL["text"], br.get("mint") or HERO["mint"], clamp((t - br["t_video"] + .35) / 1.2)))
    else:
        out.append(("size by score · cap 4% of MC", money(int(equity(t) * .3)) + " free", COL["text"], None, (t / 2) % 1))
    evs = [e for e in EVENTS if e["t"] <= t]
    ntr = 18 + len(evs)
    if evs:
        e = evs[-1]
        verb = {"buy": "Bought", "sell": "Sold", "stop": "Stopped"}[e["type"]]
        out.append((f"{verb} {e['sym']} · filled (paper)", f"{ntr} trades", COL["text"], e["mint"], clamp((t - e["t"]) / 1.0)))
    else:
        out.append(("waiting for signal", f"{ntr} trades", COL["text"], None, (t / 1.5) % 1))
    sells = [e for e in evs if e["type"] != "buy"]
    if sells:
        e = sells[-1]
        txt = (f"stop hit {e['sym']} · -25%" if e["type"] == "stop" else f"trail 40% · {e['sym']}")
        out.append((txt, money(e["pnl_c"], True), COL["pos"] if e["pnl_c"] >= 0 else COL["neg"], e["mint"], clamp((t - e["t"]) / 1.0)))
    else:
        out.append(("trail 40% · stop -25%", "armed", COL["text2"], None, (t / 2) % 1))
    return out


def agent_icon(c, i, cx, cy, r, t, prog):
    col = hexc(AG_COL[i])
    c.drawCircle(cx, cy, r, P(hexc("#0B1012")))
    c.drawCircle(cx, cy, r, P(skia.ColorSetA(col, 60), 6))
    c.drawArc(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), -90 + (t * 140 if i == 0 else 0), 360 * clamp(prog) if i else 110, False, P(col, 6))
    k = r * .5
    if i == 0:  # radar
        c.drawCircle(cx, cy, k, P(col, 3.5)); c.drawCircle(cx, cy, k * .45, P(col))
        a = t * 4
        c.drawLine(cx, cy, cx + math.cos(a) * k, cy + math.sin(a) * k, P(col, 3.5))
    elif i == 1:  # analyst: bars
        for j, hh in enumerate((.5, .9, .7)):
            c.drawRoundRect(skia.Rect.MakeXYWH(cx - k + j * k * .72, cy + k * .6 - k * 1.3 * hh, k * .5, k * 1.3 * hh), 3, 3, P(col))
    elif i == 2:  # brain: node graph
        pts = [(-.6, -.3), (.6, -.4), (0, .55), (0, -.05)]
        for a_ in pts[:3]:
            c.drawLine(cx + pts[3][0] * k, cy + pts[3][1] * k, cx + a_[0] * k, cy + a_[1] * k, P(col, 3))
        for a_ in pts:
            c.drawCircle(cx + a_[0] * k, cy + a_[1] * k, k * .22, P(col))
    elif i == 3:  # executor: bolt
        pth = skia.Path(); pth.moveTo(cx + k * .15, cy - k); pth.lineTo(cx - k * .55, cy + k * .1); pth.lineTo(cx - k * .02, cy + k * .1)
        pth.lineTo(cx - k * .2, cy + k); pth.lineTo(cx + k * .6, cy - k * .15); pth.lineTo(cx + k * .05, cy - k * .15); pth.close()
        c.drawPath(pth, P(col))
    else:  # risk: shield
        pth = skia.Path(); pth.moveTo(cx, cy - k); pth.lineTo(cx + k * .8, cy - k * .6); pth.lineTo(cx + k * .7, cy + k * .3)
        pth.quadTo(cx + k * .4, cy + k * .85, cx, cy + k); pth.quadTo(cx - k * .4, cy + k * .85, cx - k * .7, cy + k * .3)
        pth.lineTo(cx - k * .8, cy - k * .6); pth.close()
        c.drawPath(pth, P(col, 3.5))
        c.drawLine(cx - k * .3, cy, cx - k * .05, cy + k * .3, P(col, 3.5)); c.drawLine(cx - k * .05, cy + k * .3, cx + k * .35, cy - k * .25, P(col, 3.5))


def bots(c, oy, t):
    CTX["layer"] = "page"
    y = BOTS_Y - oy
    if y > H or y + 760 < 0:
        return
    text(c, "Bots", MX, y, 44, 700)
    text(c, "5 running", W - MX, y + 8, 32, 500, hexc(COL["pos"]), align="r")
    fr = agent_frames(t)
    for i, (sub, right, rcol, mint, prog) in enumerate(fr):
        ry = y + 70 + i * (BOT_H + BOT_G)
        if ry > H or ry + BOT_H < 0:
            continue
        r = skia.Rect.MakeXYWH(MX - 14, ry, W - 2 * MX + 28, BOT_H)
        c.drawRoundRect(r.makeOffset(0, 8), 26, 26, P(hexc("#000000", .5), blur=12))
        c.drawRoundRect(r, 26, 26, P(hexc(COL["card"])))
        flash = 1 - clamp(prog * 3) if i > 0 else 0
        if flash > 0:
            c.drawRoundRect(r, 26, 26, P(hexc(AG_COL[i], .10 * flash)))
            c.drawRoundRect(r, 26, 26, P(hexc(AG_COL[i], .55 * flash), 2.5))
        cont = (r.left(), r.top(), r.right(), r.bottom())
        agent_icon(c, i, MX + 36, ry + BOT_H / 2, 40, t, prog)
        c.drawCircle(MX + 100, ry + 37, 6, P(hexc(AG_COL[i], .6 + .4 * math.sin(t * 5 + i))))
        text(c, AG_NAMES[i], MX + 116, ry + 24, 34, 600, container=cont)
        sx = MX + 100
        if mint:
            logo(c, mint, sx + 15, ry + 87, 15)
            sx += 40
        rw = tw(right, 30, 600)
        maxw = r.right() - 30 - rw - 24 - sx
        s = sub
        while tw(s, 26, 500) > maxw and len(s) > 4:
            s = s[:-2].rstrip() + "…" if not s.endswith("…") else s[:-2] + "…"
        text(c, s, sx, ry + 76, 26, 500, hexc(COL["text2"]), container=cont)
        text(c, right, r.right() - 26, ry + 50, 30, 600, hexc(rcol), align="r", container=cont, kind="value")
        # progress bar
        c.drawRoundRect(skia.Rect.MakeXYWH(r.left() + 116, r.bottom() - 10, r.width() - 150, 4), 2, 2, P(hexc(COL["line"])))
        c.drawRoundRect(skia.Rect.MakeXYWH(r.left() + 116, r.bottom() - 10, (r.width() - 150) * clamp(prog), 4), 2, 2, P(hexc(AG_COL[i])))


# -------------------------------------------------------------- activity

def activity(c, oy, t):
    CTX["layer"] = "page"
    y = ACT_Y - oy
    if y > H:
        return
    text(c, "Activity", MX, y, 44, 700)
    bx = MX + tw("Activity", 44, 700) + 20
    r = skia.Rect.MakeXYWH(bx, y - 2, tw("CONCEPT", 22, 700) + 26, 40)
    c.drawRoundRect(r, 10, 10, P(hexc(COL["card2"])))
    text(c, "CONCEPT", bx + 13, y + 7, 22, 700, hexc(COL["text2"]), container=(r.left(), r.top(), r.right(), r.bottom()))
    text(c, "See all", W - MX, y + 8, 32, 500, hexc(COL["pos"]), align="r")
    rows = feed(t)[:9]
    yy = y + 66
    for e in rows:
        k = eout(seg(t, e["t"], e["t"] + .45)) if e["t"] >= 0 else 1
        hgt = ACT_H * k
        if yy > H or yy + hgt < 0:
            yy += hgt
            continue
        c.save()
        CTX["layer"] = "page" if k >= .98 else "page_anim"
        c.clipRect(skia.Rect.MakeXYWH(0, yy, W, hgt))
        hl = 1 - seg(t, e["t"] + .45, e["t"] + 1.6) if e["t"] >= 0 else 0
        if hl > 0:
            col = COL["pos"] if e["type"] != "stop" else COL["neg"]
            c.drawRoundRect(skia.Rect.MakeXYWH(MX - 18, yy + 6, W - 2 * MX + 36, ACT_H - 12), 22, 22, P(hexc(col, .12 * hl)))
        ry = yy + (ACT_H - 120) / 2 - (1 - k) * 40
        cont = (MX - 18, yy, W - MX + 18, yy + ACT_H)
        logo(c, e["mint"], MX + 40, ry + 60, 40)
        bcol = {"buy": COL["blue"], "sell": COL["pos"], "stop": COL["neg"]}[e["type"]]
        c.drawCircle(MX + 70, ry + 90, 15, P(hexc(COL["bg"])))
        c.drawCircle(MX + 70, ry + 90, 12, P(hexc(bcol)))
        if e["type"] == "sell":
            pth = skia.Path(); pth.moveTo(MX + 64, ry + 90); pth.lineTo(MX + 69, ry + 95); pth.lineTo(MX + 77, ry + 85)
            c.drawPath(pth, P(hexc("#FFFFFF"), 3))
        elif e["type"] == "stop":
            c.drawLine(MX + 65, ry + 85, MX + 75, ry + 95, P(hexc("#FFFFFF"), 3)); c.drawLine(MX + 75, ry + 85, MX + 65, ry + 95, P(hexc("#FFFFFF"), 3))
        else:
            c.drawLine(MX + 66, ry + 94, MX + 75, ry + 85, P(hexc("#FFFFFF"), 3)); c.drawLine(MX + 69, ry + 85, MX + 75, ry + 85, P(hexc("#FFFFFF"), 3))
            c.drawLine(MX + 75, ry + 85, MX + 75, ry + 91, P(hexc("#FFFFFF"), 3))
        if e["type"] == "buy":
            title = f"Bought {e['sym']}"
            sub = f"Executor · {hm(e['time'])}"
            v1, c1 = money(e["size_c"]), COL["text"]
            v2 = (compact(e["mc"]) + " MC") if e.get("mc") else "paper fill"
        else:
            title = ("Stopped " if e["type"] == "stop" else "Sold ") + e["sym"] + (f" {e['partial']}" if e.get("partial") else "")
            sub = f"{e.get('agent', 'Executor')} · {e['label']} · {hm(e['time'])}"
            v1, c1 = money(e["pnl_c"], True), COL["pos"] if e["pnl_c"] >= 0 else COL["neg"]
            v2 = pct(e["pct"])
        text(c, title, MX + 104, ry + 26, 34, 600, container=cont)
        text(c, sub, MX + 104, ry + 76, 26, 500, hexc(COL["text2"]), container=cont)
        text(c, v1, W - MX, ry + 26, 34, 700, hexc(c1), align="r", container=cont, kind="value")
        text(c, v2, W - MX, ry + 76, 26, 500, hexc(COL["text2"]), align="r", container=cont)
        c.drawRect(skia.Rect.MakeXYWH(MX + 104, yy + ACT_H - 1.5, W - 2 * MX - 104, 1.5), P(hexc(COL["line"], .7)))
        c.restore()
        CTX["layer"] = "page"
        yy += hgt


# ---------------------------------------------------------- foreground

def sticky(c, t, s):
    cover = max([seg(t, e["t"] - .06, e["t"] + .06) * (1 - seg(t, e["t"] + BAN_DUR, e["t"] + BAN_DUR + .3)) for e in EVENTS] + [0])
    a0 = clamp((s - 300) / 220)
    a = a0 * (1 - .92 * cover)
    if a0 <= 0:
        return
    CTX["layer"] = "sticky"
    g = skia.GradientShader.MakeLinear([skia.Point(0, 110), skia.Point(0, 300)], [hexc(COL["bg"], a0), hexc(COL["bg"], a0), hexc(COL["bg"], 0)], [0, .72, 1])
    c.drawRect(skia.Rect.MakeXYWH(0, 110, W, 190), P(hexc(COL["bg"]), shader=g))
    if a <= 0.02:
        CTX["layer"] = "page"
        return
    c.saveLayerAlpha(None, int(255 * a))
    e = equity(t)
    pulse = max([1 - seg(t, x["t_video"] + .55, x["t_video"] + 1.1) for x in VID_TR if t >= x["t_video"] + .55] + [0])
    if pulse > 0:
        c.drawRoundRect(skia.Rect.MakeXYWH(W / 2 - 230, 128, 460, 96), 48, 48, P(hexc(COL["pos"], .22 * pulse), blur=30))
    odometer(c, e, W / 2, 136, 72, 700, hexc(COL["text"]), align="c")
    pnl = e - CAP
    s2 = f"{'▲' if pnl >= 0 else '▼'} {money(int(round(pnl)), True)} ({pct(pnl / CAP, 1)}) · {e / CAP:.2f}x"
    text(c, s2, W / 2, 230, 30, 600, hexc(COL["pos"] if pnl >= 0 else COL["neg"]), align="c", kind="value")
    c.restore()
    CTX["layer"] = "page"


BAN_DUR = 1.5


def banners(c, t, depth_dx):
    CTX["layer"] = "banner"
    evs = [e for e in EVENTS if e["t"] <= t < e["t"] + BAN_DUR + .4]
    shown = [e for e in EVENTS if e["t"] <= t]
    for e in evs:
        later = [x for x in shown if x["t"] > e["t"]]
        t_out = min([x["t"] for x in later] + [e["t"] + BAN_DUR])
        kin = spring(seg(t, e["t"], e["t"] + .55))
        replaced = t_out < e["t"] + BAN_DUR
        kout = ease(seg(t, t_out, t_out + (.06 if replaced else .35)))
        if kout >= 1:
            continue
        CTX["layer"] = "banner_out" if t >= t_out else "banner"
        y = lerp(-40, 132, kin) - (40 if replaced else 210) * kout
        sc = lerp(1.18, 1.0, eout(seg(t, e["t"], e["t"] + .45))) * (1 - (.08 if replaced else 0) * kout)
        alpha = clamp(seg(t, e["t"] + .067, e["t"] + .16)) * (1 - kout)
        c.save()
        c.translate(W / 2 + depth_dx, y + 80)
        c.scale(sc, sc)
        c.translate(-W / 2, -80)
        r = skia.Rect.MakeXYWH(24, 0, W - 48, 160)
        c.drawRoundRect(r.makeOffset(0, 26), 44, 44, P(hexc("#000000", .65 * alpha), blur=34 * sc))
        c.drawRoundRect(r, 44, 44, P(hexc("#2B3135", alpha)))
        c.drawRoundRect(r, 44, 44, P(hexc("#FFFFFF", .08 * alpha), 2))
        c.saveLayerAlpha(None, int(255 * alpha))
        ic = skia.Rect.MakeXYWH(52, 34, 92, 92)
        c.drawRoundRect(ic, 22, 22, P(hexc("#0B0F11")))
        app_mark(c, ic.centerX(), ic.centerY(), 30)
        cont = (r.left(), r.top(), r.right(), r.bottom())
        text(c, ev_title(e), 168, 38, 36, 700, container=cont)
        if e["type"] == "buy":
            parts = [(mc_txt(e.get("mc")) or "paper fill", COL["text"]), (" · Executor", COL["text"])]
        else:
            parts = []
            if e.get("mc"):
                parts.append((mc_txt(e["mc"]) + " · ", COL["text"]))
            else:
                parts.append((e["label"] + " · ", COL["text"]))
            parts.append((f"{money(e['pnl_c'], True)} ({pct(e['pct'])})", COL["pos"] if e["pnl_c"] >= 0 else COL["neg"]))
        xx = 168
        for s_, cc in parts:
            xx += text(c, s_, xx, 92, 31, 500 if cc == COL["text"] else 700, hexc(cc, .9 if cc == COL["text"] else 1), container=cont)
        text(c, "now", W - 150, 40, 26, 500, hexc(COL["text2"]), align="r", container=cont)
        logo(c, e["mint"], W - 92, 80, 34)
        c.restore()
        c.restore()
    CTX["layer"] = "page"


def coin_flights(c, t, chart_events):
    """Coins fly from SELL markers into the sticky balance (foreground depth)."""
    for kind, mx, my, tv, x in chart_events:
        if kind != "SELL" or not x or x["pnl_c"] <= 0:
            continue
        for j in range(4):
            k = seg(t, tv + .55 + j * .08, tv + 1.35 + j * .08)
            if k <= 0 or k >= 1:
                continue
            kk = ease(k)
            sx, sy = mx, my
            ex, ey = W / 2 + (j - 1.5) * 40, 180
            ctrlx = sx + (330 if sx < W / 2 else -330) - 60 * j
            cx = (1 - kk) ** 2 * sx + 2 * (1 - kk) * kk * ctrlx + kk ** 2 * ex
            cy = (1 - kk) ** 2 * sy + 2 * (1 - kk) * kk * (sy + 120) + kk ** 2 * ey
            r = 26 + 34 * math.sin(math.pi * kk)  # comes toward camera mid-flight
            draw_coin(c, cx, cy, r, t * 7 + j, x["mint"], alpha=1 - seg(k, .85, 1), blur=1.6 * math.sin(math.pi * kk) * (j % 2))


def _burst(t, oy):
    rng = np.random.RandomState(SC["seed"] % 100000)
    out = []
    for j in range(16):
        vx = rng.uniform(-620, 620); vy = rng.uniform(-1500, -900); z = rng.uniform(.55, 1.7)
        t0 = 12.62 + rng.uniform(0, .25); spin = rng.uniform(4, 9)
        k = t - t0
        if k <= 0 or k > 1.9:
            continue
        x = 400 + vx * k
        y = 400 - oy + vy * k + .5 * 1700 * k * k
        a = 1 - seg(k, 1.4, 1.9)
        out.append((z, x, y, 26 * z, t * spin + j, a))
    return out


def finale_coins_back(c, t, oy):
    for z, x, y, r, ang, a in _burst(t, oy):
        if z <= 1.2:
            draw_coin(c, x, y, r, ang, None, alpha=a * .9, blur=(1.2 - z) * 5, shadow=False)


def finale_coins(c, t, oy):
    for z, x, y, r, ang, a in _burst(t, oy):
        if z > 1.2:
            draw_coin(c, x, y, r, ang, None, alpha=a, blur=(z - 1.15) * 10, shadow=False)


def end_card(c, t):
    k = seg(t, 13.75, 14.2)
    if k <= 0:
        return
    CTX["layer"] = "endcard"
    c.drawRect(skia.Rect.MakeWH(W, H), P(hexc(COL["bg"], .80 * k)))
    g = skia.GradientShader.MakeRadial(skia.Point(W / 2, 760), 760, [hexc(COL["pos"], .20 * k), hexc(COL["pos"], 0)])
    c.drawRect(skia.Rect.MakeWH(W, H), P(hexc("#000000"), shader=g))
    a = k
    yk = (1 - eout(k)) * 60
    draw_coin(c, W / 2, 560 + yk + 10 * math.sin(t * 3), 165, .55 * math.sin((t - 13.75) * 2.2) + .25 * (1 - k), None, alpha=a)
    c.saveLayerAlpha(None, int(255 * a))
    text(c, CFG["title_lines"][0], W / 2, 860 + yk, 84, 900, align="c", disp=True, kind="title")
    t2 = CFG["title_lines"][1]
    w2 = tw(t2, 124, 900, True)
    f = font(124, 900, True)
    sh = skia.GradientShader.MakeLinear([skia.Point(W / 2 - w2 / 2, 0), skia.Point(W / 2 + w2 / 2, 0)], [hexc("#7CFFC4"), hexc(COL["pos"]), hexc("#0FB872")])
    c.drawString(t2, W / 2 - w2 / 2, 990 + yk + f.getMetrics().fCapHeight, f, P(hexc(COL["pos"]), shader=sh))
    reg("title", t2, (W / 2 - w2 / 2, 990 + yk, W / 2 + w2 / 2, 990 + yk + 120))
    cap_r = skia.Rect.MakeXYWH(W / 2 - w2 / 2, 980 + yk, w2, 130)
    c.save(); c.clipRect(cap_r); sheen(c, cap_r, seg(t, 14.2, 14.9)); c.restore()
    # final numbers
    py = 1200 + yk
    box = skia.Rect.MakeXYWH(90, py, W - 180, 290)
    c.drawRoundRect(box, 36, 36, P(hexc(COL["card"], .92)))
    c.drawRoundRect(box, 36, 36, P(hexc(COL["pos"], .45), 2))
    cont = (box.left(), box.top(), box.right(), box.bottom())
    text(c, "Final equity", W / 2, py + 34, 30, 500, hexc(COL["text2"]), align="c", container=cont)
    text(c, money(FINAL), W / 2, py + 82, 80, 800, align="c", disp=True, container=cont, kind="value")
    text(c, f"P&L {money(SC['total_pnl_c'], True)} · ROI {pct(SC['roi_pct'] / 100, 1)}", W / 2, py + 196, 36, 700, hexc(COL["pos"]), align="c", container=cont, kind="value")
    text(c, f"Start {money(CAP)} · {len(TR)} concept trades", W / 2, py + 246, 26, 500, hexc(COL["text2"]), align="c", container=cont)
    snap_t = dt.datetime.strptime(SNAP["snapshot_finished_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M UTC")
    text(c, "CONCEPT TRADES · simulated results, not financial advice", W / 2, 1560, 24, 600, hexc(COL["text2"]), align="c")
    text(c, f"Market data: GeckoTerminal + DEX Screener snapshot {snap_t}", W / 2, 1600, 23, 500, hexc(COL["text3"]), align="c")
    c.restore()
    CTX["layer"] = "page"


# ----------------------------------------------------------------- camera

CAM_EVENTS = [(HB["t_video"], "BUY")] + [(x["t_video"], "SELL") for x in HERO_PARTS]


def camera(t, s_vel, marker_pts):
    """Returns (zoom, pivot, tilt_deg)."""
    z = 1.0
    piv = (W / 2, 900)
    for tv, _ in CAM_EVENTS:
        k = seg(t, tv - .25, tv + .15) * (1 - seg(t, tv + .75, tv + 1.25))
        if k > 0:
            z = max(z, 1 + .045 * ease(k))
            mp = marker_pts.get(round(tv, 3))
            if mp:
                piv = (clamp(mp[0], 300, W - 300), clamp(mp[1], 500, 1300))
    z *= 1 + .022 * ease(seg(t, 0, 2.5)) * (1 - ease(seg(t, 2.5, 3.0)))
    piv = (piv[0] + 6 * math.sin(t * 1.3), piv[1] + 8 * math.cos(t * 1.1))
    # breathing push-in during finale
    z *= 1 + .02 * ease(seg(t, 12.55, 13.6)) * (1 - seg(t, 13.75, 14.2))
    tilt = clamp(s_vel / 9000, -1, 1) * 5.0
    pull = 1 - .025 * min(1, abs(s_vel) / 6000)
    return z * pull, piv, tilt


def persp_matrix(zoom, piv, tilt_deg):
    """Screen quad -> rotated-about-X, perspective-projected quad (true 3D camera)."""
    th = math.radians(tilt_deg)
    d = 2400.0
    src = [skia.Point(0, 0), skia.Point(W, 0), skia.Point(W, H), skia.Point(0, H)]
    dst = []
    for p in src:
        x, y = (p.x() - piv[0]) * zoom, (p.y() - piv[1]) * zoom
        yr, zr = y * math.cos(th), y * math.sin(th)
        s = d / (d + zr)
        dst.append(skia.Point(piv[0] + x * s, piv[1] + yr * s))
    m = skia.Matrix()
    m.setPolyToPoly(src, dst)
    return m


# ------------------------------------------------------------------ frame
_last_marks = {}


def draw_frame(c, t):
    REG.clear()
    s = scroll(t)
    sv = scroll_vel(t)
    c.clear(hexc(COL["bg"]))
    # background parallax layer (slow)
    for gx, gy, gr, gc, ga in ((160, 380, 520, COL["pos"], .10), (980, 1500, 620, "#3B82F6", .07), (540, 2900, 700, COL["pos"], .07)):
        y = gy - s * .3
        sh = skia.GradientShader.MakeRadial(skia.Point(gx, y), gr, [hexc(gc, ga), hexc(gc, 0)])
        c.drawCircle(gx, y, gr, P(hexc(gc), shader=sh))
    marker_pts = {}
    # scene layer with 3D camera
    zoom, piv, tilt = camera(t, sv, _last_marks)
    c.save()
    c.concat(persp_matrix(zoom, piv, tilt))
    finale_coins_back(c, t, s)
    portfolio(c, s, t)
    evs = terminal(c, s, t, None) or []
    for kind, mx, my, tv, x in evs:
        marker_pts[round(tv, 3)] = (mx, my)
    bots(c, s, t)
    activity(c, s, t)
    finale_coins(c, t, s)
    c.restore()
    _last_marks.clear(); _last_marks.update(marker_pts)
    # chrome + foreground (faster parallax)
    depth_dx = -sv * .004
    sticky(c, t, s)
    status_bar(c, t)
    nav_bar(c, t)
    CTX["layer"] = "fx"
    coin_flights(c, t, [(k, *persp_matrix(zoom, piv, tilt).mapXY(mx, my), tv, x) for k, mx, my, tv, x in evs])
    banners(c, t, depth_dx)
    end_card(c, t)
    # vignette
    vg = skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), 1250, [hexc("#000000", 0), hexc("#000000", 0), hexc("#000000", .35)], [0, .7, 1])
    c.drawRect(skia.Rect.MakeWH(W, H), P(hexc("#000000"), shader=vg))


def blur_samples(t):
    v = abs(scroll_vel(t))
    if v < 700:
        return 1
    return int(clamp(v / FPS / 4 / 5, 5, 24))  # ~6 px per sub-sample over a 180 deg shutter


def render_t(t, blur=True):
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    n = blur_samples(t) if blur else 1
    if n > 1:
        acc = None
        for k in range(n):
            o = (k / (n - 1) - .5) / FPS / 4
            draw_frame(c, clamp(t + o, 0, DUR - 1e-3))
            a = surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType).astype(np.float32)
            acc = a if acc is None else acc + a
        draw_frame(c, t)  # registry for the centre time
        return (acc / n).round().astype(np.uint8)
    draw_frame(c, t)
    return surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


def worker(i):
    t = i / FPS
    arr = render_t(t)
    return i, arr[:, :, :3].tobytes(), list(REG)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "output", "grok_meme_million_v1.8.3_silent.mp4"))
    ap.add_argument("--still", nargs="*", type=float)
    ap.add_argument("--stills-dir", default=os.path.join(ROOT, "output", "stills"))
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    if a.still:
        os.makedirs(a.stills_dir, exist_ok=True)
        from PIL import Image
        for t in a.still:
            arr = render_t(t)
            p = os.path.join(a.stills_dir, f"still_{t:05.2f}.png")
            Image.fromarray(arr[:, :, :3]).save(p)
            print(p)
        return
    from multiprocessing import Pool
    cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", str(CFG["video"]["crf"]), "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-movflags", "+faststart", a.out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    layout = {}
    with Pool(a.jobs) as pool:
        for i, buf, rg in pool.imap(worker, range(NFR), chunksize=2):
            ff.stdin.write(buf)
            layout[i] = rg
            if i % 30 == 0:
                print(f"frame {i}/{NFR}", flush=True)
    ff.stdin.close(); ff.wait()
    json.dump(layout, open(os.path.join(ROOT, "output", "layout_registry.json"), "w"))
    json.dump({"events": [{k: v for k, v in e.items() if k in ("t", "type", "sym", "pnl_c", "hero")} for e in EVENTS],
               "scroll_keys": KEYS, "cam_events": CAM_EVENTS}, open(os.path.join(ROOT, "output", "timeline.json"), "w"), indent=1)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
