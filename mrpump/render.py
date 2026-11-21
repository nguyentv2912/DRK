"""MR PUMP Terminal — vẽ video từ data/<date>/night.json (PIL -> ffmpeg).

  python3 render.py [--date D] still 1 9 18 27     # xem trước vài khung
  python3 render.py [--date D] video [--jobs 4]    # output/mrpump_<date>_silent.mp4
"""
import json, math, os, subprocess, sys, datetime as dt
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fetch import ddir, default_date, ICT

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, TH, OY = 1080, 1920, 1440, 240          # khung 9:16, terminal 3:4 đặt ở y=240
FPS, T0, T1, TEND = 30, 3.6, 26.0, 28.0      # 0,3–3,4 s quét trending, 3,6–26 s là đêm 23:00→07:00
SCAN0, SCAN_END = 0.3, 3.4

BG, PANEL, LINE, DIM, TXT = (8, 22, 16), (11, 29, 21), (34, 66, 50), (112, 140, 124), (222, 236, 228)
GREEN, PINK, ORANGE, PURPLE, BLUE, YELLOW, GREY = (61, 220, 132), (255, 77, 122), (255, 159, 67), (167, 139, 250), (79, 163, 255), (245, 197, 66), (150, 160, 155)

JB = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-{}.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
_fc = {}


def F(kind, size):
    k = (kind, size)
    if k not in _fc:
        path = JB.format(kind) if kind in ("Regular", "Medium", "Bold", "ExtraBold", "SemiBold") else INTER.format(kind[1:])
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]


def money(v, sign=False):
    s = f"${abs(v):,.2f}"
    return (("+" if v >= 0 else "-") + s) if sign else ("-" + s if v < 0 else s)


def short(v):
    return f"${v/1e6:.1f}M" if v >= 1e6 else f"${v/1e3:.0f}k"


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def alpha(c, a):
    return tuple(int(BG[i] + (c[i] - BG[i]) * a) for i in range(3))


def rr(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def dashed_rr(d, box, r, color, width=2, dash=9, gap=6):
    x0, y0, x1, y1 = box
    for (ax, ay, bx, by) in ((x0 + r, y0, x1 - r, y0), (x0 + r, y1, x1 - r, y1), (x0, y0 + r, x0, y1 - r), (x1, y0 + r, x1, y1 - r)):
        L = max(abs(bx - ax), abs(by - ay))
        s = 0
        while s < L:
            e = min(L, s + dash)
            if ax == bx:
                d.line((ax, ay + s, ax, ay + e), fill=color, width=width)
            else:
                d.line((ax + s, ay, ax + e, ay), fill=color, width=width)
            s += dash + gap
    for cx, cy, a0 in ((x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90)):
        d.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 90, fill=color, width=width)


def glow_sprite(size, color, radius=18, r=16, strength=1.0):
    w, h = size
    pad = radius * 2
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad, pad + w, pad + h), r, outline=color + (int(255 * strength),), width=6)
    return im.filter(ImageFilter.GaussianBlur(radius)), pad


def circle_glow(rad, color, blur=22):
    pad = blur * 2
    s = 2 * (rad + pad)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((pad, pad, s - pad, s - pad), outline=color + (255,), width=10)
    return im.filter(ImageFilter.GaussianBlur(blur)), rad + pad


# ---------------------------------------------------------------- mascot Mr Pump (vẽ bằng code)
def mascot(size):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(60):                      # đầu tròn xanh có gradient
        t = i / 59
        c = (int(40 + 60 * t), int(170 + 70 * t), int(100 + 50 * t), 255)
        m = int(S * 0.08 + t * S * 0.06)
        d.ellipse((m, m + int(S * 0.04), S - m, S - m + int(S * 0.02)), fill=c)
    # mũi tên "pump" trên đỉnh
    d.polygon([(S * .5, S * .02), (S * .62, S * .16), (S * .54, S * .16), (S * .54, S * .24), (S * .46, S * .24), (S * .46, S * .16), (S * .38, S * .16)], fill=(245, 197, 66, 255))
    # kính râm
    d.rounded_rectangle((S * .2, S * .38, S * .47, S * .55), int(S * .06), fill=(10, 14, 12, 255))
    d.rounded_rectangle((S * .53, S * .38, S * .8, S * .55), int(S * .06), fill=(10, 14, 12, 255))
    d.rectangle((S * .45, S * .42, S * .55, S * .46), fill=(10, 14, 12, 255))
    d.line((S * .26, S * .42, S * .33, S * .42), fill=(120, 255, 190, 255), width=int(S * .02))
    d.line((S * .59, S * .42, S * .66, S * .42), fill=(120, 255, 190, 255), width=int(S * .02))
    # cười nhếch
    d.arc((S * .33, S * .5, S * .72, S * .78), 15, 160, fill=(10, 30, 20, 255), width=int(S * .035))
    return im.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- dữ liệu -> trạng thái theo thời gian
class Story:
    def __init__(self, night):
        self.n = night
        self.s0 = dt.datetime.fromisoformat(night["window"][0]).timestamp()
        self.s1 = dt.datetime.fromisoformat(night["window"][1]).timestamp()
        self.items = []                                   # (vt, kind, payload)
        checks = night["checks"]
        for i, c in enumerate(checks):
            self.items.append((SCAN0 + (SCAN_END - SCAN0) * (i + 0.5) / len(checks), "check", c))
        for e in night["events"]:
            self.items.append((self.vt(e["t"]), e["kind"], e))
        self.items.sort(key=lambda x: x[0])
        # dòng log (bảng LOG) và tail -f
        self.rows, self.tail = [], []
        t0 = dt.datetime.fromtimestamp(self.s0, ICT)
        self.rows.append((0.0, "23:00", "SCAN", None, f"{night['scanned']} trending pools", "GeckoTerminal · Solana", "", DIM))
        self.rows.append((SCAN_END, "23:00", "CHECK", None, f"{night['passed']} pass · {night['filtered']} filtered", "mint/freeze · top10 · liq · vol", "", DIM))
        line = 2
        for vt, k, p in self.items:
            if k == "check":
                if p["ok"]:
                    self.tail.append((vt, f"PASS  ${p['symbol']}", f"liq {short(p['liq'])} · top10 {p['top10']:.0f}%", GREEN))
                else:
                    self.tail.append((vt, f"BLOCK ${p['symbol']}", p["reason"], PINK))
            elif k in ("enter", "exit"):
                hh = dt.datetime.fromtimestamp(p["t"], ICT).strftime("%H:%M")
                line += 1
                if k == "enter":
                    self.rows.append((vt, hh, "ENTER", p["sym"], p["sym"], p["why"], f"size {p['size']*100:.0f}%", TXT))
                    self.tail.append((vt, f"{hh} ENTER ${p['sym']} size {p['size']*100:.0f}%", p["why"].replace(" over 30m high", ""), ORANGE))
                else:
                    self.rows.append((vt, hh, "EXIT", p["sym"], p["sym"], p["why"], money(p["pnl"], True), GREEN if p["pnl"] > 0 else PINK))
                    self.tail.append((vt, f"{hh} EXIT  ${p['sym']} {money(p['pnl'], True)}", p["why"], GREEN if p["pnl"] > 0 else PINK))
        self.sym_color = {}
        pal = [ORANGE, BLUE, GREEN, PINK, PURPLE, YELLOW, (90, 220, 230)]
        for i, c in enumerate(checks):
            self.sym_color.setdefault(c["symbol"], pal[len(self.sym_color) % len(pal)])

    def vt(self, ts):
        return T0 + (T1 - T0) * (ts - self.s0) / (self.s1 - self.s0)

    def clock(self, t):
        x = min(1.0, max(0.0, (t - T0) / (T1 - T0)))
        return dt.datetime.fromtimestamp(self.s0 + x * (self.s1 - self.s0), ICT)

    def state(self, t):
        n = self.n
        st = dict(bal=n["start"], prev_bal=n["start"], bal_t=-9, trades=0, wins=0, losses=0, checked=0, filtered=0,
                  passed=0, line=2, last=None, last_t=-9, chips=[], sizer=None, equity=None, open={}, trade=None,
                  lastk=None)
        for vt, k, p in self.items:
            if vt > t:
                break
            st["last"], st["last_t"], st["lastk"] = p, vt, k
            if k == "check":
                st["checked"] += 1
                st["passed" if p["ok"] else "filtered"] += 1
                st["chips"].append((vt, p["symbol"], p["ok"], p["reason"] or f"liq {short(p['liq'])} · top10 {p['top10']:.0f}%", p))
            elif k == "skip" and p["why"].startswith("busy"):
                st["chips"].append((vt, p["sym"], None, p["why"], p))
            elif k == "enter":
                st["line"] += 1
                st["open"][p["sym"]] = p
                st["sizer"] = p
                st["trade"] = ("enter", p, vt)
                st["chips"].append((vt, p["sym"], True, p["why"].split(" · ")[1], p))
            elif k == "exit":
                st["line"] += 1
                st["open"].pop(p["sym"], None)
                st["trades"] += 1
                st["wins" if p["pnl"] > 0 else "losses"] += 1
                st["prev_bal"], st["bal"], st["bal_t"] = st["bal"], p["bal"], vt
                st["equity"] = p
                st["trade"] = ("exit", p, vt)
        return st


# ---------------------------------------------------------------- khung tĩnh
class Painter:
    AG = [("SCANNER", ORANGE, "trending pools · real", "flags only, never trades", "SCAN"),
          ("RUG CHECK", PINK, "filters suspicious tokens", "nothing executes before a pass", "PASS"),
          ("SIZER", PURPLE, "sizes from account equity", "never trades a fixed ticket", "SIZE"),
          ("EXECUTOR", GREEN, "opens + closes, tracks slip", "slippage + fee 1.5%", "LIVE"),
          ("LOGGER", ORANGE, "writes every decision", "no trade without a reason", "WRITE"),
          ("EQUITY", BLUE, "balance + curve", "updates on every close", "UPDATE"),
          ("YOU", TXT, "read the log at 7am", "stopped asking, started reading", "ASLEEP")]
    AX0, AX1, AY0, AH, AGAP = 26, 314, 278, 150, 13

    def __init__(self, story):
        self.s = story
        n = story.n
        self.mascot = mascot(112)
        self.mascot_s = mascot(96)
        self.base = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(self.base)
        # dải trên + dưới (9:16)
        d.text((W // 2, 92), "MR PUMP", font=F("iExtraBold", 74), fill=YELLOW, anchor="mm")
        date_s = dt.datetime.fromisoformat(n["window"][0]).strftime("%d %b %Y")
        d.text((W // 2, 160), f"1 night · {n['scanned']} trending tokens · real 5m prices", font=F("iSemiBold", 30), fill=TXT, anchor="mm")
        d.text((W // 2, 202), f"Solana · {date_s} · 23:00 → 07:00 (UTC+7)", font=F("Medium", 22), fill=DIM, anchor="mm")
        d.text((W // 2, OY + TH + 70), "Paper trades simulated on real on-chain prices", font=F("iSemiBold", 28), fill=TXT, anchor="mm")
        d.text((W // 2, OY + TH + 112), "Not financial advice · data: GeckoTerminal", font=F("Medium", 22), fill=DIM, anchor="mm")
        # lưới chấm
        for y in range(OY + 20, OY + TH - 10, 24):
            for x in range(20, W - 10, 24):
                d.point((x, y), fill=(18, 40, 30))
        o = OY
        rr(d, (10, o + 10, W - 10, o + TH - 10), 22, fill=None, outline=LINE, width=2)
        for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
            d.ellipse((34 + i * 22, o + 30, 46 + i * 22, o + 42), fill=c)
        d.text((W // 2 - 40, o + 36), "MR PUMP Terminal — overnight · six agents · log first", font=F("Regular", 15), fill=DIM, anchor="mm")
        dashed_rr(d, (858, o + 22, 1050, o + 50), 8, GREEN, 2, 6, 4)
        d.text((954, o + 36), "paper · real prices", font=F("Medium", 15), fill=GREEN, anchor="mm")
        d.line((12, o + 62, W - 12, o + 62), fill=LINE, width=1)
        # header
        d.ellipse((30, o + 78, 146, o + 194), fill=(14, 36, 26), outline=LINE, width=2)
        self.base.paste(self.mascot, (32, o + 80), self.mascot)
        d.text((168, o + 80), "MR PUMP", font=F("ExtraBold", 32), fill=YELLOW)
        w = F("ExtraBold", 32).getlength("MR PUMP ")
        d.text((168 + w, o + 80), "Terminal", font=F("ExtraBold", 32), fill=TXT)
        w2 = F("ExtraBold", 32).getlength("MR PUMP Terminal ")
        dashed_rr(d, (168 + w2, o + 86, 168 + w2 + 104, o + 112), 6, YELLOW, 2, 5, 3)
        d.text((168 + w2 + 52, o + 99), "v1.0-night", font=F("Medium", 14), fill=YELLOW, anchor="mm")
        d.text((170, o + 206), "every trade gets a reason", font=F("Regular", 16), fill=DIM)
        for x, y, lab in ((640, 128, "balance"), (930, 128, "trades"), (640, 204, "wins"), (930, 204, "losses")):
            d.text((x, o + y), lab, font=F("Regular", 15), fill=DIM)
        d.line((12, o + 234, W - 12, o + 234), fill=LINE, width=1)
        # agents
        d.text((self.AX0 + 4, o + 250), "AGENTS", font=F("Medium", 15), fill=DIM)
        d.text((self.AX1, o + 250), "6 online", font=F("Regular", 15), fill=DIM, anchor="ra")
        for i, (name, col, desc, rule, badge) in enumerate(self.AG):
            y = o + self.AY0 + i * (self.AH + self.AGAP)
            ix, iy = self.AX0 + 10, y + 14
            rr(d, (ix, iy, ix + 44, iy + 44), 12, fill=alpha(col, .9) if name != "YOU" else (235, 240, 236))
            self.icon(d, name, ix + 22, iy + 22)
            d.text((ix + 58, y + 10), name, font=F("Bold", 21), fill=col)
            d.text((ix + 58, y + 40), desc, font=F("iRegular", 14), fill=DIM)
            d.text((ix, y + 78), rule, font=F("iSemiBold", 15), fill=col if name != "YOU" else TXT)
        # panel phải
        self.RX0, self.RX1 = 334, 1048
        for (y0, y1) in ((250, 642), (874, 998), (1010, 1418)):
            rr(d, (self.RX0, o + y0, self.RX1, o + y1), 16, outline=LINE, width=2)
        rr(d, (self.RX0, o + 654, 684, o + 862), 16, outline=LINE, width=2)
        rr(d, (694, o + 654, self.RX1, o + 862), 16, outline=LINE, width=2)
        d.text((self.RX0 + 14, o + 262), "LIVE FLOW · SCAN → CHECK → SIZE → EXEC → LOG", font=F("Medium", 15), fill=DIM)
        d.text((self.RX0 + 14, o + 666), "TRADE · ENTRY vs EXIT", font=F("Medium", 15), fill=DIM)
        d.text((708, o + 666), "$ tail -f night.log", font=F("Medium", 16), fill=TXT)
        d.text((self.RX0 + 14, o + 886), "RESULT · start vs now", font=F("Medium", 15), fill=DIM)
        d.text((self.RX1 - 14, o + 886), "one night · 23:00 → 07:00", font=F("Regular", 15), fill=DIM, anchor="ra")
        d.text((self.RX0 + 14, o + 916), "START", font=F("Medium", 15), fill=DIM)
        d.text((self.RX0 + 14, o + 948), "NOW", font=F("Medium", 15), fill=DIM)
        d.text((self.RX1 - 14, o + 912), money(n["start"]), font=F("Bold", 22), fill=TXT, anchor="ra")
        d.text((self.RX1 - 14, o + 976), "paper trades · real 5m candles", font=F("Regular", 14), fill=DIM, anchor="ra")
        d.line((self.RX0 + 90, o + 926, 900, o + 926), fill=LINE, width=6)
        d.ellipse((self.RX0 + 84, o + 920, self.RX0 + 96, o + 932), fill=GREY)
        d.text((self.RX0 + 14, o + 1022), "LOG", font=F("Medium", 15), fill=DIM)
        tx = self.RX1 - 14 - F("Regular", 15).getlength(" → reading the log")
        d.text((tx, o + 1022), " → reading the log", font=F("Regular", 15), fill=DIM)
        q = "would you long this?"
        qw = F("Regular", 15).getlength(q)
        d.text((tx - qw, o + 1022), q, font=F("Regular", 15), fill=DIM)
        d.line((tx - qw, o + 1031, tx, o + 1031), fill=DIM, width=1)
        # các nút luồng + nét chấm
        self.nodes = [(470, o + 452, 44, PINK, "RUG CHECK"), (690, o + 452, 58, GREEN, "MR PUMP"), (900, o + 452, 44, GREEN, "EXECUTOR")]
        for (ax, ay, ar, _, _), (bx, by, br, _, _) in zip(self.nodes, self.nodes[1:]):
            for x in range(ax + ar + 8, bx - br - 6, 12):
                d.ellipse((x - 2, ay - 2, x + 2, ay + 2), fill=LINE)
        for x, y, r, col, lab in self.nodes:
            d.ellipse((x - r, y - r, x + r, y + r), fill=(12, 26, 20), outline=col, width=4)
        self.icon(d, "RUG CHECK", 470, o + 452, big=True)
        self.icon(d, "EXECUTOR", 900, o + 452, big=True)
        self.base.paste(self.mascot_s, (690 - 48, o + 452 - 50), self.mascot_s)
        # 4 thẻ
        self.cards = [(PINK, "FILTERED"), (PURPLE, "SIZER"), (ORANGE, "LOGGER"), (BLUE, "EQUITY")]
        for i, (col, lab) in enumerate(self.cards):
            x0 = self.RX0 + 12 + i * 175
            dashed_rr(d, (x0, o + 548, x0 + 165, o + 630), 10, alpha(col, .7), 2, 6, 4)
            d.text((x0 + 12, o + 556), "• " + lab, font=F("Medium", 14), fill=col)
        # sprite phát sáng
        self.g_agent = {}
        for name, col, *_ in self.AG:
            self.g_agent[name] = glow_sprite((self.AX1 - self.AX0, self.AH), col, 14, 16, 0.9)
        self.g_node = {lab: circle_glow(r + 6, col) for x, y, r, col, lab in self.nodes}
        self.g_gold = circle_glow(70, YELLOW, 26)

    def icon(self, d, name, cx, cy, big=False):
        k = 1.5 if big else 1.0
        c = (20, 20, 20) if not big else None
        if name == "SCANNER":
            for r in (14, 9, 4):
                d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=3)
        elif name == "RUG CHECK":
            col = c or PINK
            s = 12 * k
            d.polygon([(cx, cy - s - 2), (cx + s, cy - s * .6), (cx + s * .85, cy + s * .4), (cx, cy + s + 2), (cx - s * .85, cy + s * .4), (cx - s, cy - s * .6)], outline=col, width=3)
            d.line([(cx - s * .4, cy), (cx - s * .05, cy + s * .35), (cx + s * .5, cy - s * .35)], fill=col, width=3)
        elif name == "SIZER":
            d.line((cx, cy - 13, cx, cy + 12), fill=c, width=3)
            d.line((cx - 13, cy - 7, cx + 13, cy - 7), fill=c, width=3)
            d.arc((cx - 17, cy - 9, cx - 5, cy + 5), 0, 180, fill=c, width=3)
            d.arc((cx + 5, cy - 9, cx + 17, cy + 5), 0, 180, fill=c, width=3)
            d.line((cx - 8, cy + 13, cx + 8, cy + 13), fill=c, width=3)
        elif name == "EXECUTOR":
            col = c or GREEN
            s = 1.5 * k
            pts = [(2, -12), (-7, 2), (0, 2), (-3, 13), (8, -3), (1, -3), (4, -12)]
            d.polygon([(cx + x * s / 1.5 * (1.4 if big else 1), cy + y * s / 1.5 * (1.4 if big else 1)) for x, y in pts], fill=col)
        elif name == "LOGGER":
            d.rounded_rectangle((cx - 10, cy - 13, cx + 10, cy + 13), 3, outline=c, width=3)
            for yy in (-5, 1, 7):
                d.line((cx - 5, cy + yy, cx + 5, cy + yy), fill=c, width=2)
        elif name == "EQUITY":
            d.line([(cx - 13, cy + 8), (cx - 5, cy), (cx + 1, cy + 5), (cx + 12, cy - 8)], fill=(255, 255, 255), width=3)
            d.polygon([(cx + 13, cy - 11), (cx + 13, cy - 3), (cx + 6, cy - 9)], fill=(255, 255, 255))
        elif name == "YOU":
            d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=(30, 40, 34))
            d.ellipse((cx - 6, cy - 16, cx + 16, cy + 6), fill=(235, 240, 236))

    # ------------------------------------------------------------ khung động
    def frame(self, t):
        s = self.s
        st = s.state(t)
        im = self.base.copy()
        d = ImageDraw.Draw(im)
        o = OY
        n = s.n
        end = t >= T1
        clk = s.clock(t)
        since = t - st["last_t"]

        # header
        blink = (int(t * 2) % 2 == 0) or end
        d.ellipse((172, o + 140, 184, o + 152), fill=ORANGE if blink else alpha(ORANGE, .4))
        d.text((196, o + 132), f"{'done' if end else ('running' if t >= T0 else 'scanning')} · {clk:%H:%M:%S}", font=F("Medium", 22), fill=TXT)
        status = self.status(st, end)
        w = F("Medium", 15).getlength(status) + 24
        rr(d, (168, o + 168, 168 + w, o + 194), 5, outline=GREEN, width=2)
        d.text((180, o + 181), status, font=F("Medium", 15), fill=GREEN, anchor="lm")
        k = ease((t - st["bal_t"]) / 0.35)
        bal = st["prev_bal"] + (st["bal"] - st["prev_bal"]) * k
        jit = 0 if k >= 1 else int(4 * (1 - k))
        bcol = TXT if k >= 1 else (GREEN if st["bal"] >= st["prev_bal"] else PINK)
        d.text((636, o + 76 - jit), money(bal), font=F("ExtraBold", 42), fill=bcol)
        d.text((928, o + 76), str(st["trades"]), font=F("ExtraBold", 40), fill=TXT)
        d.text((636, o + 150), str(st["wins"]), font=F("ExtraBold", 40), fill=GREEN)
        d.text((928, o + 150), str(st["losses"]), font=F("ExtraBold", 40), fill=PINK)

        # agents: viền sáng cho agent đang làm
        act = self.active(st, t, end)
        for i, (name, col, desc, rule, badge) in enumerate(self.AG):
            y = o + self.AY0 + i * (self.AH + self.AGAP)
            box = (self.AX0, y, self.AX1, y + self.AH)
            if name in act:
                g, pad = self.g_agent[name]
                im.paste(g, (box[0] - pad, box[1] - pad), g)
                d = ImageDraw.Draw(im)
                rr(d, box, 16, fill=alpha(col, .10))
                dashed_rr(d, box, 16, col, 2)
                d.text((self.AX0 + 10, y + 78), rule, font=F("iSemiBold", 15), fill=col if name != "YOU" else TXT)
                ix, iy = self.AX0 + 10, y + 14
                rr(d, (ix, iy, ix + 44, iy + 44), 12, fill=col if name != "YOU" else (235, 240, 236))
                self.icon(d, name, ix + 22, iy + 22)
                d.text((ix + 58, y + 10), name, font=F("Bold", 21), fill=col)
                d.text((ix + 58, y + 40), desc, font=F("iRegular", 14), fill=DIM)
            b = self.badge(name, st, end)
            bw = F("Medium", 13).getlength(b) + 14
            rr(d, (self.AX1 - 10 - bw, y + 12, self.AX1 - 10, y + 34), 5, outline=col, width=2)
            d.text((self.AX1 - 10 - bw / 2, y + 23), b, font=F("Medium", 13), fill=col, anchor="mm")
            d.text((self.AX0 + 10, y + 108), self.agent_line(name, st, end)[:34], font=F("Regular", 15), fill=TXT)

        # chip token
        chips = st["chips"][-4:]
        for j, (vt, sym, ok, why, p) in enumerate(chips[::-1]):
            age = t - vt
            x0 = self.RX1 - 14 - (j + 1) * 172 + 4
            col = GREEN if ok else (PINK if ok is False else GREY)
            dy = int(22 * (1 - ease(age / 0.22))) if j == 0 else 0
            box = (x0, o + 290 + dy, x0 + 162, o + 352 + dy)
            rr(d, box, 10, fill=(13, 31, 23))
            dashed_rr(d, box, 10, alpha(ORANGE if ok is not False else PINK, .85), 2, 6, 4)
            cc = s.sym_color.get(sym, ORANGE)
            d.ellipse((x0 + 10, o + 300 + dy, x0 + 30, o + 320 + dy), fill=cc)
            d.text((x0 + 20, o + 310 + dy), sym[:1].upper(), font=F("Bold", 13), fill=BG, anchor="mm")
            d.text((x0 + 38, o + 299 + dy), "$" + sym[:9], font=F("Bold", 18), fill=TXT)
            d.text((x0 + 12, o + 330 + dy), why[:20], font=F("Regular", 12), fill=DIM)
            if ok is False and age < 0.45:
                a = min(1, age / 0.08)
                stamp = Image.new("RGBA", (130, 34), (0, 0, 0, 0))
                sd = ImageDraw.Draw(stamp)
                sd.rounded_rectangle((2, 2, 128, 32), 6, outline=PINK + (int(255 * a),), width=3, fill=(60, 10, 25, int(200 * a)))
                sd.text((65, 17), "FILTERED", font=F("ExtraBold", 18), fill=PINK + (int(255 * a),), anchor="mm")
                stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
                im.paste(stamp, (x0 + 30, o + 318 + dy), stamp)
                d = ImageDraw.Draw(im)
            elif ok and age < 0.8 and st["lastk"] == "check":
                d.text((x0 + 150, o + 310), "PASS", font=F("ExtraBold", 14), fill=GREEN, anchor="rm")
        d.text((self.RX1 - 14, o + 262), f"checked {st['checked']}", font=F("Regular", 15), fill=DIM, anchor="ra")

        # nút luồng phát sáng + hạt
        hot = self.hot_nodes(st, since, end)
        for x, y, r, col, lab in self.nodes:
            if lab in hot:
                g, pad = self.g_node[lab]
                im.paste(g, (x - pad, y - pad), g)
        if end:
            g, pad = self.g_gold
            im.paste(g, (690 - pad, o + 452 - pad), g)
        d = ImageDraw.Draw(im)
        for x, y, r, col, lab in self.nodes:
            ring = col if lab != "MR PUMP" or not end else YELLOW
            d.ellipse((x - r, y - r, x + r, y + r), outline=ring, width=4)
        for k2 in range(3):
            ph = (t * 1.6 + k2 / 3) % 1
            for (ax, ay, ar, _, _), (bx, by, br, _, _) in zip(self.nodes, self.nodes[1:]):
                xx = ax + ar + (bx - br - ax - ar) * ph
                d.ellipse((xx - 4, ay - 4, xx + 4, ay + 4), fill=GREEN if not end else YELLOW)
        last_sym = st["last"]["symbol"] if st["lastk"] == "check" else (st["last"] or {}).get("sym", "")
        d.text((470, o + 512), "RUG CHECK", font=F("Medium", 14), fill=PINK, anchor="mm")
        d.text((470, o + 530), ("PASS $" if st["lastk"] != "check" or st["last"]["ok"] else "BLOCK $") + str(last_sym)[:8], font=F("Regular", 13), fill=PINK, anchor="mm")
        d.text((690, o + 530), "MR PUMP · " + ("done" if end else f"{(st['checked'] * 7 + int(t * 13)) % 90 + 20} msg/s"), font=F("Medium", 14), fill=YELLOW, anchor="mm")
        ex = "FLAT" if not st["open"] else "LIVE $" + list(st["open"])[-1][:7]
        d.text((900, o + 512), "EXECUTOR", font=F("Medium", 14), fill=GREEN, anchor="mm")
        d.text((900, o + 530), ex, font=F("Regular", 13), fill=GREEN, anchor="mm")

        # 4 thẻ
        sz = st["sizer"]
        eqp = st["equity"]
        vals = [(str(st["filtered"]), f"+ {st['passed']} passed"),
                ((f"{sz['size']*100:.0f}% eq" if sz else "--"), (money(sz["size"] * self.eq_at(st)) if sz else "waiting")),
                (f"line #{st['line']}", "each with a reason"),
                ((money(eqp["pnl"], True) if eqp else "+$0.00"), "last close")]
        for i, (v, sub) in enumerate(vals):
            x0 = self.RX0 + 12 + i * 175
            col = self.cards[i][0]
            if i == 3 and eqp:
                col = GREEN if eqp["pnl"] > 0 else PINK
            d.text((x0 + 12, o + 576), v, font=F("Bold", 24), fill=TXT if i < 3 else col)
            d.text((x0 + 12, o + 608), sub[:20], font=F("Regular", 13), fill=DIM)

        # TRADE
        tr = st["trade"]
        if tr:
            kind, p, vt = tr
            sym = p["sym"]
            cc = s.sym_color.get(sym, ORANGE)
            d.ellipse((350, o + 700, 378, o + 728), fill=cc)
            d.text((364, o + 714), sym[:1].upper(), font=F("Bold", 15), fill=BG, anchor="mm")
            d.text((388, o + 698), "$" + sym[:9], font=F("ExtraBold", 26), fill=TXT)
            lw = F("ExtraBold", 26).getlength("$" + sym[:9])
            rr(d, (396 + lw, o + 704, 448 + lw, o + 726), 5, outline=GREEN, width=2)
            d.text((422 + lw, o + 715), "LONG", font=F("Medium", 12), fill=GREEN, anchor="mm")
            ent = p if kind == "enter" else self.find_entry(p)
            if kind == "enter":
                d.text((672, o + 702), "live", font=F("Bold", 20), fill=GREEN, anchor="ra")
            else:
                d.text((672, o + 702), f"{p['pct']*100:+.1f}%", font=F("Bold", 20), fill=GREEN if p["pnl"] > 0 else PINK, anchor="ra")
            rows = [("entry", f"{ent['price']:.8g}" if ent else "--", GREEN),
                    ("exit", "open" if kind == "enter" else "closed", GREEN if kind == "enter" or p["pnl"] > 0 else PINK),
                    ("slip", "1.5% + fee", TXT), ("size", f"{(ent or p).get('size', 0)*100:.0f}% of equity", TXT)]
            for j, (a, b, c) in enumerate(rows):
                d.text((350, o + 740 + j * 26), a, font=F("Regular", 16), fill=DIM)
                d.text((420, o + 740 + j * 26), b, font=F("Medium", 16), fill=c)
            d.text((350, o + 842), "reason:", font=F("Regular", 13), fill=ORANGE)
            d.text((412, o + 842), (p["why"] if kind == "exit" else p["why"])[:34], font=F("Regular", 13), fill=TXT)
        else:
            d.text((350, o + 720), "waiting for a signal…", font=F("Regular", 16), fill=DIM)

        # tail -f
        tl = [x for x in s.tail if x[0] <= t][-4:]
        d.text((self.RX1 - 14, o + 668), f"{len([x for x in s.tail if x[0] <= t]) + 2} lines", font=F("Regular", 13), fill=DIM, anchor="ra")
        for j, (vt, a, b, c) in enumerate(tl):
            yy = o + 694 + j * 40
            d.text((708, yy), a[:34], font=F("Regular", 14), fill=c)
            d.text((722, yy + 18), b[:33], font=F("Regular", 12), fill=DIM)
        if int(t * 3) % 2 == 0:
            d.rectangle((708, o + 694 + len(tl) * 40, 716, o + 710 + len(tl) * 40), fill=GREEN)

        # RESULT
        frac = (bal - n["start"]) / max(1e-9, n["end"] - n["start"]) if n["end"] != n["start"] else 1
        frac = max(0.02, min(1.0, frac)) if n["end"] >= n["start"] else 0.5
        x1 = self.RX0 + 90 + int((900 - self.RX0 - 90) * frac)
        d.line((self.RX0 + 90, o + 958, 900, o + 958), fill=LINE, width=8)
        d.line((self.RX0 + 90, o + 958, x1, o + 958), fill=GREEN if bal >= n["start"] else PINK, width=8)
        d.text((self.RX1 - 14, o + 944), money(bal), font=F("Bold", 24 if not end else 26), fill=GREEN if bal >= n["start"] else PINK, anchor="ra")
        d.text((self.RX0 + 90, o + 974), f"{st['wins']} W / ", font=F("Bold", 17), fill=GREEN)
        d.text((self.RX0 + 90 + F("Bold", 17).getlength(f"{st['wins']} W / "), o + 974), f"{st['losses']} L", font=F("Bold", 17), fill=PINK)
        if end:
            pct = (n["end"] / n["start"] - 1) * 100
            d.text((self.RX0 + 205, o + 974), f"{pct:+.1f}% in one night", font=F("ExtraBold", 17), fill=GREEN if pct >= 0 else PINK)

        # LOG
        rows = [r for r in s.rows if r[0] <= t][-6:]
        for j, (vt, hh, kind, sym, title, why, right, rc) in enumerate(rows):
            yy = o + 1052 + j * 60
            new = (j == len(rows) - 1) and (t - vt) < 1.5
            if new:
                d.rectangle((self.RX0 + 4, yy - 6, self.RX1 - 4, yy + 48), fill=(18, 40, 30))
                d.rectangle((self.RX0 + 4, yy - 6, self.RX0 + 8, yy + 48), fill=ORANGE)
            d.text((self.RX0 + 20, yy + 6), hh, font=F("Medium", 18), fill=DIM)
            bc = {"ENTER": ORANGE, "EXIT": GREEN, "SCAN": BLUE, "CHECK": PINK}[kind]
            rr(d, (self.RX0 + 88, yy + 4, self.RX0 + 178, yy + 30), 4, outline=bc, width=2, fill=alpha(bc, .12))
            d.text((self.RX0 + 133, yy + 17), kind, font=F("Medium", 13), fill=bc, anchor="mm")
            if sym:
                d.ellipse((self.RX0 + 196, yy + 2, self.RX0 + 216, yy + 22), fill=s.sym_color.get(sym, ORANGE))
                d.text((self.RX0 + 206, yy + 12), sym[:1].upper(), font=F("Bold", 11), fill=BG, anchor="mm")
                d.text((self.RX0 + 224, yy), "$" + title[:10], font=F("Bold", 18), fill=TXT)
            else:
                d.text((self.RX0 + 196, yy), title, font=F("Bold", 18), fill=TXT)
            d.text((self.RX0 + 196, yy + 26), "reason: " + why[:44], font=F("Regular", 13), fill=alpha(ORANGE, .85))
            d.text((self.RX1 - 18, yy + 4), right, font=F("Bold", 18), fill=rc if kind == "EXIT" else ORANGE, anchor="ra")
        return im

    def find_entry(self, p):
        best = None
        for e in self.s.n["events"]:
            if e["kind"] == "enter" and e["sym"] == p["sym"] and e["t"] <= p["t"]:
                best = e
        return best

    def eq_at(self, st):
        return st["bal"]

    def status(self, st, end):
        if end:
            return f"NIGHT CLOSED · {st['trades']} TRADES LOGGED"
        k, p = st["lastk"], st["last"]
        if k == "check":
            return f"SCANNER · {'PASSED' if p['ok'] else 'BLOCKED'} ${p['symbol'][:10]}"
        if k == "enter":
            return f"EXECUTOR · ENTERED ${p['sym'][:10]}"
        if k == "exit":
            return f"TRADE CLOSED · LOGGED ${p['sym'][:10]}"
        if k == "skip":
            return f"SIZER · SKIPPED ${p['sym'][:10]}"
        return "BOOTING · LOADING TRENDING"

    def active(self, st, t, end):
        if end:
            return {"YOU"}
        k, since = st["lastk"], t - st["last_t"]
        if k == "check":
            return {"SCANNER"} if st["last"]["stage"] == "SCANNER" else {"RUG CHECK"}
        if since > 0.9:
            return set()
        if k == "enter":
            return {"SIZER"} if since < 0.3 else {"EXECUTOR"}
        if k == "exit":
            return {"EXECUTOR"} if since < 0.2 else ({"LOGGER"} if since < 0.5 else {"EQUITY"})
        if k == "skip":
            return {"SIZER"}
        return set()

    def hot_nodes(self, st, since, end):
        if end:
            return {"MR PUMP"}
        k = st["lastk"]
        if since > 0.6:
            return set()
        return {"check": {"RUG CHECK"}, "enter": {"MR PUMP", "EXECUTOR"}, "exit": {"EXECUTOR"}, "skip": {"MR PUMP"}}.get(k, set())

    def badge(self, name, st, end):
        if name == "YOU":
            return "READING" if end else "ASLEEP"
        if name == "EXECUTOR":
            return "LIVE" if st["open"] else "FLAT"
        return dict(SCANNER="SCAN", **{"RUG CHECK": "PASS"}, SIZER="SIZE", LOGGER="WRITE", EQUITY="UPDATE")[name]

    def agent_line(self, name, st, end):
        n = self.s.n
        lc = [c for c in st["chips"] if c[2] is not None]
        if name == "SCANNER":
            if lc:
                p = lc[-1][4]
                if "liq" in p:
                    return f"${p['symbol'][:8]} · liq {short(p['liq'])}"
                return f"signal ${lc[-1][1][:8]}"
            return "loading trending…"
        if name == "RUG CHECK":
            return f"{st['passed']} passed · {st['filtered']} blocked"
        if name == "SIZER":
            sz = st["sizer"]
            return f"{sz['size']*100:.0f}% of {money(st['bal'])}" if sz else "idle"
        if name == "EXECUTOR":
            return ("LONG $" + list(st["open"])[-1][:8] + " · slip 1.5%") if st["open"] else "flat · waiting"
        if name == "LOGGER":
            return f"line #{st['line']}"
        if name == "EQUITY":
            return f"{money(st['bal'])} · {st['trades']} closes"
        if name == "YOU":
            return f"{st['line']} lines to read"


def load(date):
    return json.load(open(os.path.join(ddir(date), "night.json")))


_P = None


def _init(date):
    global _P
    _P = Painter(Story(load(date)))


def _seg(args):
    date, f0, f1, path = args
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", path],
                         stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(_P.frame(f / FPS).tobytes())
    p.stdin.close()
    p.wait()
    return path


def video(date, jobs=4):
    out = os.path.join(HERE, "output")
    os.makedirs(out, exist_ok=True)
    N = int(TEND * FPS)
    cuts = [N * i // jobs for i in range(jobs + 1)]
    segs = [(date, cuts[i], cuts[i + 1], f"{out}/_seg{i}.mp4") for i in range(jobs)]
    with Pool(jobs, initializer=_init, initargs=(date,)) as pool:
        paths = pool.map(_seg, segs)
    lst = f"{out}/_segs.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in paths))
    dst = f"{out}/mrpump_{date}_silent.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", dst], check=True)
    for p_ in paths + [lst]:
        os.remove(p_)
    print(dst)
    return dst


if __name__ == "__main__":
    a = sys.argv[1:]
    date = dt.date.fromisoformat(a[a.index("--date") + 1]) if "--date" in a else default_date()
    if "still" in a:
        P = Painter(Story(load(date)))
        ts = [float(x) for x in a[a.index("still") + 1:] if x.replace(".", "").isdigit()]
        out = os.path.join(HERE, "output")
        os.makedirs(out, exist_ok=True)
        for t in ts:
            P.frame(t).save(f"{out}/still_{t:05.1f}.png")
        print("ok", ts)
    elif "video" in a:
        video(date, int(a[a.index("--jobs") + 1]) if "--jobs" in a else 4)
