"""MR PUMP Terminal v2 — vẽ video từ data/<date>/{night.json, candles.json} (PIL -> ffmpeg).

  python3 render.py [--date D] still 0.5 2 9 18 27     # xem trước vài khung
  python3 render.py [--date D] video [--jobs 4]        # output/mrpump_<date>_silent.mp4

Dòng thời gian (29 s):
  0–0,95  hook: thẻ kết quả thật của đêm (flash-forward) rồi tua ngược
  0,95–2,4 quét token trending (PASS / FILTERED)
  2,6–26  đêm 23:00 → 07:00 theo giờ thật của từng nến/lệnh
  26–29   thẻ NIGHT REPORT
"""
import json, math, os, subprocess, sys, datetime as dt
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fetch import ddir, default_date, ICT

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, TH, OY = 1080, 1920, 1440, 240
FPS, T0, T1, TEND = 30, 2.6, 26.0, 29.0
HOOK, SCAN0, SCAN_END = 0.95, 1.0, 2.4

BG, PANEL, LINE, DIM, TXT = (8, 22, 16), (11, 29, 21), (34, 66, 50), (120, 148, 132), (226, 238, 230)
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


def back(x):                                   # nảy quá rồi về
    x = max(0.0, min(1.0, x))
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


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


def glow_sprite(size, color, radius=18, r=16, strength=1.0, width=6):
    w, h = size
    pad = radius * 2
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad, pad + w, pad + h), r, outline=color + (int(255 * strength),), width=width)
    return im.filter(ImageFilter.GaussianBlur(radius)), pad


def circle_glow(rad, color, blur=22):
    pad = blur * 2
    s = 2 * (rad + pad)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((pad, pad, s - pad, s - pad), outline=color + (255,), width=10)
    return im.filter(ImageFilter.GaussianBlur(blur)), rad + pad


def paste_a(im, sprite, xy, a):
    if a <= 0:
        return
    if a < 1:
        sprite = sprite.copy()
        sprite.putalpha(sprite.getchannel("A").point(lambda v: int(v * a)))
    im.paste(sprite, (int(xy[0]), int(xy[1])), sprite)


def text_sprite(text, font, color, stroke=0, sc=(0, 0, 0)):
    b = font.getbbox(text, stroke_width=stroke)
    im = Image.new("RGBA", (b[2] - b[0] + 8, b[3] - b[1] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - b[0], 4 - b[1]), text, font=font, fill=color, stroke_width=stroke, stroke_fill=sc)
    return im


def odometer(im, xr, y, old, new, k, font, color):
    """Số lăn kiểu đồng hồ cơ, căn phải tại xr. k: 0→1."""
    n = max(len(old), len(new))
    old, new = old.rjust(n), new.rjust(n)
    cw = font.getlength("0")
    asc, desc = font.getmetrics()
    lh = asc + desc
    x = xr - cw * n
    d = ImageDraw.Draw(im)
    for i, (a, b) in enumerate(zip(old, new)):
        cx = x + i * cw
        if a == b or k >= 1:
            if b != " ":
                d.text((cx, y), b, font=font, fill=color)
            continue
        kk = ease(min(1, k * (1.0 + 0.12 * (n - i))))          # chữ số bên phải lăn nhanh hơn
        tile = Image.new("RGBA", (int(cw) + 2, lh), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        off = int(kk * lh)
        td.text((0, -off), a, font=font, fill=color + (int(255 * (1 - kk * 0.7)),))
        td.text((0, lh - off), b, font=font, fill=color)
        im.paste(tile, (int(cx), int(y)), tile)


# ---------------------------------------------------------------- mascot Mr Pump (vẽ bằng code)
def mascot(size, mood="ok"):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(60):
        t = i / 59
        c = (int(40 + 60 * t), int(170 + 70 * t), int(100 + 50 * t), 255)
        m = int(S * 0.08 + t * S * 0.06)
        d.ellipse((m, m + int(S * 0.04), S - m, S - m + int(S * 0.02)), fill=c)
    d.polygon([(S * .5, S * .02), (S * .62, S * .16), (S * .54, S * .16), (S * .54, S * .24), (S * .46, S * .24), (S * .46, S * .16), (S * .38, S * .16)], fill=(245, 197, 66, 255))
    d.rounded_rectangle((S * .2, S * .38, S * .47, S * .55), int(S * .06), fill=(10, 14, 12, 255))
    d.rounded_rectangle((S * .53, S * .38, S * .8, S * .55), int(S * .06), fill=(10, 14, 12, 255))
    d.rectangle((S * .45, S * .42, S * .55, S * .46), fill=(10, 14, 12, 255))
    d.line((S * .26, S * .42, S * .33, S * .42), fill=(120, 255, 190, 255), width=int(S * .02))
    d.line((S * .59, S * .42, S * .66, S * .42), fill=(120, 255, 190, 255), width=int(S * .02))
    if mood == "win":                                       # cười toác
        d.chord((S * .32, S * .52, S * .72, S * .8), 0, 180, fill=(10, 30, 20, 255))
        d.chord((S * .4, S * .66, S * .64, S * .8), 0, 180, fill=(255, 110, 130, 255))
    elif mood == "loss":                                    # mếu + giọt mồ hôi
        d.arc((S * .36, S * .64, S * .68, S * .86), 200, 340, fill=(10, 30, 20, 255), width=int(S * .035))
        d.ellipse((S * .78, S * .3, S * .9, S * .46), fill=(120, 200, 255, 255))
        d.polygon([(S * .84, S * .2), (S * .79, S * .35), (S * .89, S * .35)], fill=(120, 200, 255, 255))
    else:
        d.arc((S * .33, S * .5, S * .72, S * .78), 15, 160, fill=(10, 30, 20, 255), width=int(S * .035))
    return im.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- dữ liệu -> trạng thái
class Story:
    def __init__(self, night, candles=None):
        self.n = night
        self.s0 = dt.datetime.fromisoformat(night["window"][0]).timestamp()
        self.s1 = dt.datetime.fromisoformat(night["window"][1]).timestamp()
        self.pool_of = {c["symbol"]: c["pool"] for c in night["checks"] if c["ok"]}
        self.rows_of = {}
        if candles:
            for sym, pool in self.pool_of.items():
                if pool in candles["pools"]:
                    self.rows_of[sym] = candles["pools"][pool]
        self.items = []
        checks = night["checks"]
        for i, c in enumerate(checks):
            self.items.append((SCAN0 + (SCAN_END - SCAN0) * (i + 0.5) / len(checks), "check", c))
        for e in night["events"]:
            if e["kind"] == "skip" and not e["why"].startswith("busy"):
                continue
            self.items.append((self.vt(e["t"]), e["kind"], e))
        # nhịp thị trường thật: mỗi nến 5 phút, token qua lọc biến động mạnh nhất
        self.pulses = []
        if self.rows_of:
            ts = int(self.s0)
            while ts < self.s1:
                best = None
                for sym, rows in self.rows_of.items():
                    for i, r in enumerate(rows):
                        if r[0] == ts and i >= 12 and r[1] > 0:
                            av = sum(x[5] for x in rows[i - 12:i]) / 12 or 1e-9
                            pct = r[4] / r[1] - 1
                            if best is None or abs(pct) > abs(best["pct"]):
                                best = dict(sym=sym, pct=pct, volx=r[5] / av, t=ts)
                            break
                if best:
                    self.items.append((self.vt(ts + 300), "pulse", best))
                    self.pulses.append(best)
                ts += 300
        self.items.sort(key=lambda x: x[0])
        # LOG + tail
        self.rows, self.tail = [], []
        self.rows.append((SCAN0, "23:00", "SCAN", None, f"{night['scanned']} trending pools", "GeckoTerminal · Solana", "", DIM))
        self.rows.append((SCAN_END, "23:00", "CHECK", None, f"{night['passed']} pass · {night['filtered']} blocked", "mint/freeze · top10 · liq · vol", "", DIM))
        self.curve = [(T0, night["start"])]
        for vt, k, p in self.items:
            if k == "check":
                if p["ok"]:
                    self.tail.append((vt, f"PASS  ${p['symbol']}", f"liq {short(p['liq'])} · top10 {p['top10']:.0f}%", GREEN))
                else:
                    self.tail.append((vt, f"BLOCK ${p['symbol']}", p["reason"], PINK))
            elif k in ("enter", "exit"):
                hh = dt.datetime.fromtimestamp(p["t"], ICT).strftime("%H:%M")
                if k == "enter":
                    self.rows.append((vt, hh, "ENTER", p["sym"], p["sym"], p["why"], f"size {p['size']*100:.0f}%", TXT))
                    self.tail.append((vt, f"{hh} ENTER ${p['sym']} {p['size']*100:.0f}%", p["why"].replace(" over 30m high", ""), ORANGE))
                else:
                    self.rows.append((vt, hh, "EXIT", p["sym"], p["sym"], p["why"], money(p["pnl"], True), GREEN if p["pnl"] > 0 else PINK))
                    self.tail.append((vt, f"{hh} EXIT  ${p['sym']} {money(p['pnl'], True)}", p["why"], GREEN if p["pnl"] > 0 else PINK))
                    self.curve.append((vt, p["bal"]))
        self.sym_color = {}
        pal = [ORANGE, BLUE, GREEN, PINK, PURPLE, YELLOW, (90, 220, 230)]
        for c in checks:
            self.sym_color.setdefault(c["symbol"], pal[len(self.sym_color) % len(pal)])
        self.entries = {}
        for e in night["events"]:
            if e["kind"] == "enter":
                self.entries.setdefault(e["sym"], []).append(e)

    def vt(self, ts):
        return T0 + (T1 - T0) * (ts - self.s0) / (self.s1 - self.s0)

    def ts_at(self, t):
        x = min(1.0, max(0.0, (t - T0) / (T1 - T0)))
        return self.s0 + x * (self.s1 - self.s0)

    def clock(self, t):
        return dt.datetime.fromtimestamp(self.ts_at(t), ICT)

    def entry_for(self, p):
        best = None
        for e in self.entries.get(p["sym"], []):
            if e["t"] <= p["t"]:
                best = e
        return best

    def state(self, t):
        n = self.n
        st = dict(bal=n["start"], prev_bal=n["start"], bal_t=-9, trades=0, wins=0, losses=0, cnt_t=-9, prev=(0, 0, 0),
                  checked=0, filtered=0, passed=0, line=2, last=None, last_t=-9, lastk=None, chips=[], sizer=None,
                  equity=None, open={}, trade=None, pulse_t=-9, last_exit=None, last_enter=None)
        for vt, k, p in self.items:
            if vt > t:
                break
            if k == "pulse":
                st["pulse_t"] = vt
                st["chips"].append((vt, p["sym"], "pulse", f"{p['pct']*100:+.1f}% 5m · {p['volx']:.1f}×", p))
                continue
            st["last"], st["last_t"], st["lastk"] = p, vt, k
            if k == "check":
                st["checked"] += 1
                st["passed" if p["ok"] else "filtered"] += 1
                st["chips"].append((vt, p["symbol"], p["ok"], p["reason"] or f"liq {short(p['liq'])} · top10 {p['top10']:.0f}%", p))
            elif k == "skip":
                st["chips"].append((vt, p["sym"], None, p["why"], p))
            elif k == "enter":
                st["line"] += 1
                st["open"][p["sym"]] = p
                st["sizer"] = p
                st["trade"] = ("enter", p, vt)
                st["last_enter"] = (vt, p)
                st["chips"].append((vt, p["sym"], True, "ENTER · " + p["why"].split(" · ")[1], p))
            elif k == "exit":
                st["line"] += 1
                st["open"].pop(p["sym"], None)
                st["prev"] = (st["trades"], st["wins"], st["losses"])
                st["trades"] += 1
                st["wins" if p["pnl"] > 0 else "losses"] += 1
                st["cnt_t"] = vt
                st["prev_bal"], st["bal"], st["bal_t"] = st["bal"], p["bal"], vt
                st["equity"] = p
                st["trade"] = ("exit", p, vt)
                st["last_exit"] = (vt, p)
        return st


# ---------------------------------------------------------------- hoạ sĩ
class Painter:
    AG = [("SCANNER", ORANGE, "trending pools · real", "flags only, never trades"),
          ("RUG CHECK", PINK, "filters suspicious tokens", "nothing executes before a pass"),
          ("SIZER", PURPLE, "sizes from account equity", "never trades a fixed ticket"),
          ("EXECUTOR", GREEN, "opens + closes, tracks slip", "slippage + fee 1.5%"),
          ("LOGGER", ORANGE, "writes every decision", "no trade without a reason"),
          ("EQUITY", BLUE, "balance + curve", "updates on every close"),
          ("YOU", TXT, "read the log at 7am", "stopped asking, started reading")]
    AX0, AX1, AY0, AH, AGAP = 26, 314, 278, 150, 13
    RX0, RX1 = 334, 1048

    def __init__(self, story):
        self.s = story
        n = story.n
        self.m = {k: mascot(112, k) for k in ("ok", "win", "loss")}
        self.ms = {k: mascot(96, k) for k in ("ok", "win", "loss")}
        self.base = self.build_base()
        self.g_agent = {name: glow_sprite((self.AX1 - self.AX0, self.AH), col, 14, 16, 0.9) for name, col, *_ in self.AG}
        self.g_node = {lab: circle_glow(r + 6, col) for x, y, r, col, lab in self.nodes}
        self.g_gold = circle_glow(70, YELLOW, 26)
        self.g_loss = glow_sprite((W - 20, TH - 20), PINK, 26, 22, 1.0, 14)
        self.pct = (n["end"] / n["start"] - 1) * 100
        self.captions = [(0.0, "ONE NIGHT. REAL CHARTS.", YELLOW),
                         (HOOK, f"{n['scanned']} trending tokens → {n['filtered']} rejected", TXT),
                         (T0, f"{n['passed']} passed the rug check", GREEN),
                         (8.5, "the bot trades till 7am", TXT),
                         (14.5, "every trade gets a reason", TXT),
                         (20.0, f"{n['trades']} trades · {n['wins']} W / {n['losses']} L", TXT),
                         (T1, f"{self.pct:+.1f}% in one night · paper", GREEN if self.pct >= 0 else PINK)]
        self.cap_sprites = [(t0, text_sprite(txt, F("iExtraBold", 40), c)) for t0, txt, c in self.captions]
        self._end_core = None

    # ------------------------------------------------------------ nền tĩnh
    def build_base(self):
        n = self.s.n
        base = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(base)
        d.text((W // 2, 84), "MR PUMP", font=F("iExtraBold", 72), fill=YELLOW, anchor="mm")
        date_s = dt.datetime.fromisoformat(n["window"][0]).strftime("%d %b %Y")
        d.text((W // 2, 210), f"Solana · {date_s} · 23:00 → 07:00 (UTC+7)", font=F("Medium", 22), fill=DIM, anchor="mm")
        d.text((W // 2, OY + TH + 70), "Paper trades simulated on real on-chain prices", font=F("iSemiBold", 28), fill=TXT, anchor="mm")
        d.text((W // 2, OY + TH + 112), "Not financial advice · data: GeckoTerminal", font=F("Medium", 22), fill=DIM, anchor="mm")
        for y in range(OY + 20, OY + TH - 10, 24):
            for x in range(20, W - 10, 24):
                d.point((x, y), fill=(18, 40, 30))
        o = OY
        rr(d, (10, o + 10, W - 10, o + TH - 10), 22, outline=LINE, width=2)
        for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
            d.ellipse((34 + i * 22, o + 30, 46 + i * 22, o + 42), fill=c)
        d.text((W // 2 - 40, o + 36), "MR PUMP Terminal — overnight · six agents · log first", font=F("Regular", 16), fill=DIM, anchor="mm")
        dashed_rr(d, (858, o + 22, 1050, o + 50), 8, GREEN, 2, 6, 4)
        d.text((954, o + 36), "paper · real prices", font=F("Medium", 15), fill=GREEN, anchor="mm")
        d.line((12, o + 62, W - 12, o + 62), fill=LINE, width=1)
        d.ellipse((30, o + 78, 146, o + 194), fill=(14, 36, 26), outline=LINE, width=2)
        d.text((168, o + 80), "MR PUMP", font=F("ExtraBold", 32), fill=YELLOW)
        w = F("ExtraBold", 32).getlength("MR PUMP ")
        d.text((168 + w, o + 80), "Terminal", font=F("ExtraBold", 32), fill=TXT)
        w2 = F("ExtraBold", 32).getlength("MR PUMP Terminal ")
        dashed_rr(d, (168 + w2, o + 86, 168 + w2 + 104, o + 112), 6, YELLOW, 2, 5, 3)
        d.text((168 + w2 + 52, o + 99), "v2.0-night", font=F("Medium", 14), fill=YELLOW, anchor="mm")
        d.text((170, o + 206), "every trade gets a reason", font=F("Regular", 17), fill=DIM)
        for x, y, lab in ((640, 128, "balance"), (930, 128, "trades"), (640, 204, "wins"), (930, 204, "losses")):
            d.text((x, o + y), lab, font=F("Regular", 16), fill=DIM)
        d.line((12, o + 234, W - 12, o + 234), fill=LINE, width=1)
        d.text((self.AX0 + 4, o + 250), "AGENTS", font=F("Medium", 16), fill=DIM)
        d.text((self.AX1, o + 250), "6 online", font=F("Regular", 16), fill=DIM, anchor="ra")
        for i, (name, col, desc, rule) in enumerate(self.AG):
            self.agent_box(d, i, False)
        for (y0, y1) in ((250, 642), (874, 998), (1010, 1418)):
            rr(d, (self.RX0, o + y0, self.RX1, o + y1), 16, outline=LINE, width=2)
        rr(d, (self.RX0, o + 654, 684, o + 862), 16, outline=LINE, width=2)
        rr(d, (694, o + 654, self.RX1, o + 862), 16, outline=LINE, width=2)
        d.text((self.RX0 + 14, o + 262), "LIVE FLOW · SCAN → CHECK → SIZE → EXEC → LOG", font=F("Medium", 15), fill=DIM)
        d.text((self.RX0 + 14, o + 666), "TRADE · 5m CANDLES", font=F("Medium", 15), fill=DIM)
        d.text((708, o + 666), "$ tail -f night.log", font=F("Medium", 16), fill=TXT)
        d.text((self.RX0 + 14, o + 886), "RESULT · equity curve", font=F("Medium", 15), fill=DIM)
        d.text((self.RX1 - 14, o + 886), "23:00 → 07:00", font=F("Regular", 15), fill=DIM, anchor="ra")
        d.text((self.RX0 + 14, o + 1022), "LOG", font=F("Medium", 15), fill=DIM)
        tx = self.RX1 - 14 - F("Regular", 15).getlength(" → reading the log")
        d.text((tx, o + 1022), " → reading the log", font=F("Regular", 15), fill=DIM)
        q = "would you long this?"
        qw = F("Regular", 15).getlength(q)
        d.text((tx - qw, o + 1022), q, font=F("Regular", 15), fill=DIM)
        d.line((tx - qw, o + 1031, tx, o + 1031), fill=DIM, width=1)
        self.nodes = [(470, o + 452, 44, PINK, "RUG CHECK"), (690, o + 452, 58, GREEN, "MR PUMP"), (900, o + 452, 44, GREEN, "EXECUTOR")]
        for (ax, ay, ar, _, _), (bx, by, br, _, _) in zip(self.nodes, self.nodes[1:]):
            for x in range(ax + ar + 8, bx - br - 6, 12):
                d.ellipse((x - 2, ay - 2, x + 2, ay + 2), fill=LINE)
        for x, y, r, col, lab in self.nodes:
            d.ellipse((x - r, y - r, x + r, y + r), fill=(12, 26, 20), outline=col, width=4)
        self.icon(d, "RUG CHECK", 470, o + 452, big=True)
        self.icon(d, "EXECUTOR", 900, o + 452, big=True)
        self.cards = [(PINK, "FILTERED"), (PURPLE, "SIZER"), (ORANGE, "LOGGER"), (BLUE, "EQUITY")]
        for i, (col, lab) in enumerate(self.cards):
            x0 = self.RX0 + 12 + i * 175
            dashed_rr(d, (x0, o + 548, x0 + 165, o + 630), 10, alpha(col, .7), 2, 6, 4)
            d.text((x0 + 12, o + 555), "• " + lab, font=F("Medium", 15), fill=col)
        return base

    def agent_box(self, d, i, on):
        name, col, desc, rule = self.AG[i]
        o = OY
        y = o + self.AY0 + i * (self.AH + self.AGAP)
        ix, iy = self.AX0 + 10, y + 14
        if on:
            rr(d, (self.AX0, y, self.AX1, y + self.AH), 16, fill=alpha(col, .12))
            dashed_rr(d, (self.AX0, y, self.AX1, y + self.AH), 16, col, 2)
        rr(d, (ix, iy, ix + 44, iy + 44), 12, fill=(alpha(col, 1 if on else .85) if name != "YOU" else (235, 240, 236)))
        self.icon(d, name, ix + 22, iy + 22)
        d.text((ix + 58, y + 10), name, font=F("Bold", 21), fill=col)
        d.text((ix + 58, y + 40), desc, font=F("iRegular", 15), fill=DIM)
        d.text((ix, y + 78), rule, font=F("iSemiBold", 16), fill=col if name != "YOU" else TXT)

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
            s = 1.4 if big else 1.0
            pts = [(2, -12), (-7, 2), (0, 2), (-3, 13), (8, -3), (1, -3), (4, -12)]
            d.polygon([(cx + x * s, cy + y * s) for x, y in pts], fill=col)
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

    # ------------------------------------------------------------ khung
    def frame(self, t):
        if t < HOOK:
            return self.hook(t)
        im = self.core(t)
        if t >= T1 + 0.12:
            im = self.report(im, t)
        self.caption(im, t)
        return im

    def caption(self, im, t):
        cur = None
        for t0, sp in self.cap_sprites:
            if t >= t0:
                cur = (t0, sp)
        t0, sp = cur
        k = back((t - t0) / 0.22)
        a = min(1, (t - t0) / 0.1)
        w, h = sp.size
        s = 0.8 + 0.2 * k
        spr = sp.resize((max(1, int(w * s)), max(1, int(h * s))), Image.BICUBIC)
        paste_a(im, spr, (W / 2 - spr.size[0] / 2, 158 - spr.size[1] / 2), a)

    def hook(self, t):
        if self._end_core is None:
            self._end_core = self.core(T1 + 0.5, quiet=True)
        im = self._end_core.copy()
        dim = Image.new("RGB", (W, H), (4, 10, 7))
        im = Image.blend(im, dim, 0.72)
        n = self.s.n
        d = ImageDraw.Draw(im)
        k = back(t / 0.3)
        cy = OY + 560
        card = Image.new("RGBA", (900, 640), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, 899, 639), 36, fill=(10, 30, 21, 240), outline=YELLOW + (255,), width=4)
        cd.text((450, 70), "ONE NIGHT · REAL CHARTS", font=F("ExtraBold", 34), fill=YELLOW, anchor="mm")
        cd.text((450, 190), f"{money(n['start'])} → {money(n['end'])}", font=F("ExtraBold", 66), fill=TXT, anchor="mm")
        col = GREEN if self.pct >= 0 else PINK
        cd.text((450, 340), f"{self.pct:+.1f}%", font=F("iBlack", 170), fill=col, anchor="mm")
        cd.text((450, 480), f"{n['trades']} trades · {n['scanned']} trending tokens", font=F("iSemiBold", 34), fill=TXT, anchor="mm")
        cd.text((450, 540), "paper trades on real 5m prices", font=F("Medium", 26), fill=DIM, anchor="mm")
        s = 0.6 + 0.4 * k
        c2 = card.resize((int(900 * s), int(640 * s)), Image.BICUBIC)
        im.paste(c2, (int(W / 2 - c2.size[0] / 2), int(cy - c2.size[1] / 2)), c2)
        mm = self.m["win" if self.pct >= 0 else "loss"]
        im.paste(mm, (W // 2 - 56, int(cy - 320 * s - 70)), mm)
        if t > 0.72:                                   # tua ngược: glitch ngang + "REWIND"
            g = (t - 0.72) / (HOOK - 0.72)
            import random
            rnd = random.Random(int(t * 1000))
            src = im.copy()
            for _ in range(14):
                y = rnd.randrange(OY, OY + TH - 40)
                h = rnd.randrange(8, 40)
                dx = int(rnd.uniform(-60, 60) * g)
                im.paste(src.crop((0, y, W, y + h)), (dx, y))
            d = ImageDraw.Draw(im)
            d.text((W // 2, OY + 1060), "◀◀  REWIND TO 23:00", font=F("ExtraBold", 40), fill=TXT, anchor="mm")
        self.caption(im, t)
        return im

    def report(self, im, t):
        n = self.s.n
        k = ease((t - T1 - 0.12) / 0.35)
        im = Image.blend(im, Image.new("RGB", (W, H), (4, 10, 7)), 0.7 * k)
        card = Image.new("RGBA", (940, 1060), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        col = GREEN if self.pct >= 0 else PINK
        cd.rounded_rectangle((0, 0, 939, 1059), 36, fill=(10, 30, 21, 248), outline=col + (255,), width=4)
        date_s = dt.datetime.fromisoformat(n["window"][0]).strftime("%d %b %Y")
        cd.text((470, 150), f"NIGHT REPORT · {date_s}", font=F("ExtraBold", 30), fill=DIM, anchor="mm")
        cd.text((470, 245), money(n["end"]), font=F("iBlack", 120), fill=col, anchor="mm")
        cd.text((470, 345), f"{self.pct:+.1f}% from {money(n['start'])} in one night", font=F("iSemiBold", 34), fill=TXT, anchor="mm")
        wr = n["wins"] / max(1, n["trades"]) * 100
        stats = [(str(n["trades"]), "trades"), (f"{wr:.0f}%", "win rate"), (f"{n['filtered']}/{n['scanned']}", "filtered")]
        for i, (v, lab) in enumerate(stats):
            x = 160 + i * 310
            cd.text((x, 430), v, font=F("ExtraBold", 50), fill=TXT, anchor="mm")
            cd.text((x, 478), lab, font=F("Medium", 22), fill=DIM, anchor="mm")
        cd.line((60, 520, 880, 520), fill=LINE + (255,), width=2)
        ex = sorted([e for e in n["events"] if e["kind"] == "exit"], key=lambda e: -e["pnl"])
        cd.text((60, 548), "BEST TRADES", font=F("Bold", 24), fill=GREEN)
        for i, e in enumerate(ex[:3]):
            y = 600 + i * 70
            hh = dt.datetime.fromtimestamp(e["t"], ICT).strftime("%H:%M")
            cd.text((60, y), f"{hh}  ${e['sym']}", font=F("Bold", 30), fill=TXT)
            cd.text((60, y + 36), e["why"], font=F("Regular", 18), fill=DIM)
            cd.text((880, y + 4), money(e["pnl"], True), font=F("ExtraBold", 32), fill=GREEN if e["pnl"] > 0 else PINK, anchor="ra")
        w = ex[-1]
        cd.text((60, 828), "WORST", font=F("Bold", 24), fill=PINK)
        hh = dt.datetime.fromtimestamp(w["t"], ICT).strftime("%H:%M")
        cd.text((60, 868), f"{hh}  ${w['sym']}", font=F("Bold", 30), fill=TXT)
        cd.text((60, 904), w["why"], font=F("Regular", 18), fill=DIM)
        cd.text((880, 872), money(w["pnl"], True), font=F("ExtraBold", 32), fill=PINK, anchor="ra")
        cd.text((470, 1000), "paper trades on real 5m candles · not financial advice", font=F("Medium", 20), fill=DIM, anchor="mm")
        y = OY + 200 + int(90 * (1 - k))
        paste_a(im, card, (W / 2 - 470, y), k)
        mm = self.m["win" if self.pct >= 0 else "loss"]
        b = 1 + 0.08 * math.sin((t - T1) * 9) * max(0, 1 - (t - T1) / 2)
        m2 = mm.resize((int(112 * b), int(112 * b)), Image.LANCZOS)
        if k > 0.3:
            g, pad = self.g_gold
            paste_a(im, g, (W / 2 - pad, y + 70 - pad), k)
            im.paste(m2, (int(W / 2 - m2.size[0] / 2), int(y + 70 - m2.size[1] / 2)), m2)
        return im

    def core(self, t, quiet=False):
        s = self.s
        st = s.state(t)
        im = self.base.copy()
        d = ImageDraw.Draw(im)
        o = OY
        n = s.n
        end = t >= T1
        clk = s.clock(t)
        since = t - st["last_t"]
        lx = st["last_exit"]
        win_pop = lx and lx[1]["pnl"] > 0 and t - lx[0] < 0.9 and not quiet
        loss_hit = lx and lx[1]["pnl"] <= 0 and t - lx[0] < 0.5 and not quiet
        mood = "win" if (win_pop or end) and self.pct >= 0 else ("loss" if loss_hit else "ok")

        # header
        hm = self.m[mood]
        im.paste(hm, (32, o + 80), hm)
        blink = (int(t * 2) % 2 == 0) or end
        d.ellipse((172, o + 140, 184, o + 152), fill=ORANGE if blink else alpha(ORANGE, .4))
        d.text((196, o + 132), f"{'done' if end else ('running' if t >= T0 else 'scanning')} · {clk:%H:%M:%S}", font=F("Medium", 22), fill=TXT)
        status = self.status(st, end)
        w = F("Medium", 16).getlength(status) + 24
        rr(d, (168, o + 168, 168 + w, o + 196), 5, outline=GREEN, width=2)
        d.text((180, o + 182), status, font=F("Medium", 16), fill=GREEN, anchor="lm")
        kb = (t - st["bal_t"]) / 0.45
        bcol = TXT if kb >= 1.3 else (GREEN if st["bal"] >= st["prev_bal"] else PINK)
        odometer(im, 636 + F("ExtraBold", 42).getlength("$000.00"), o + 76, money(st["prev_bal"]), money(st["bal"]), kb, F("ExtraBold", 42), bcol)
        kc = (t - st["cnt_t"]) / 0.35
        pt, pw, pl = st["prev"]
        odometer(im, 1010, o + 76, str(pt), str(st["trades"]), kc, F("ExtraBold", 40), TXT)
        odometer(im, 700, o + 150, str(pw), str(st["wins"]), kc, F("ExtraBold", 40), GREEN)
        odometer(im, 1010, o + 150, str(pl), str(st["losses"]), kc, F("ExtraBold", 40), PINK)
        d = ImageDraw.Draw(im)

        # agents
        act = self.active(st, t, end)
        for i, (name, col, desc, rule) in enumerate(self.AG):
            y = o + self.AY0 + i * (self.AH + self.AGAP)
            if name in act:
                g, pad = self.g_agent[name]
                im.paste(g, (self.AX0 - pad, y - pad), g)
                d = ImageDraw.Draw(im)
                self.agent_box(d, i, True)
            b = self.badge(name, st, end)
            bw = F("Medium", 14).getlength(b) + 14
            rr(d, (self.AX1 - 10 - bw, y + 12, self.AX1 - 10, y + 36), 5, outline=col, width=2)
            d.text((self.AX1 - 10 - bw / 2, y + 24), b, font=F("Medium", 14), fill=col, anchor="mm")
            d.text((self.AX0 + 10, y + 110), self.agent_line(name, st, end)[:30], font=F("Regular", 17), fill=TXT)

        # chip token
        chips = st["chips"][-4:]
        for j, (vt, sym, ok, why, p) in enumerate(chips[::-1]):
            age = t - vt
            x0 = self.RX1 - 14 - (j + 1) * 172 + 4
            dy = int(22 * (1 - ease(age / 0.22))) if j == 0 else 0
            if ok == "pulse":
                bcol = GREEN if p["pct"] >= 0 else PINK
            else:
                bcol = ORANGE if ok is not False else PINK
            box = (x0, o + 290 + dy, x0 + 162, o + 352 + dy)
            rr(d, box, 10, fill=(13, 31, 23))
            dashed_rr(d, box, 10, alpha(bcol, .85), 2, 6, 4)
            cc = s.sym_color.get(sym, ORANGE)
            d.ellipse((x0 + 10, o + 300 + dy, x0 + 30, o + 320 + dy), fill=cc)
            d.text((x0 + 20, o + 310 + dy), sym[:1].upper(), font=F("Bold", 13), fill=BG, anchor="mm")
            d.text((x0 + 38, o + 298 + dy), "$" + sym[:8], font=F("Bold", 18), fill=TXT)
            d.text((x0 + 10, o + 328 + dy), why[:17], font=F("Regular", 14), fill=bcol if ok == "pulse" else DIM)
            if ok is False and age < 0.45:
                a = min(1, age / 0.08)
                stamp = Image.new("RGBA", (130, 34), (0, 0, 0, 0))
                sd = ImageDraw.Draw(stamp)
                sd.rounded_rectangle((2, 2, 128, 32), 6, outline=PINK + (int(255 * a),), width=3, fill=(60, 10, 25, int(200 * a)))
                sd.text((65, 17), "FILTERED", font=F("ExtraBold", 18), fill=PINK + (int(255 * a),), anchor="mm")
                stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
                im.paste(stamp, (x0 + 30, o + 318 + dy), stamp)
                d = ImageDraw.Draw(im)
        d.text((self.RX1 - 14, o + 262), f"checked {st['checked']}", font=F("Regular", 15), fill=DIM, anchor="ra")

        # nút + hạt
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
        bump = 1.0
        if win_pop:
            bump = 1 + 0.14 * math.sin(min(1, (t - lx[0]) / 0.5) * math.pi)
        ms = self.ms[mood]
        if bump != 1.0:
            ms = ms.resize((int(96 * bump), int(96 * bump)), Image.LANCZOS)
        im.paste(ms, (int(690 - ms.size[0] / 2), int(o + 452 - ms.size[1] / 2 - 2)), ms)
        d = ImageDraw.Draw(im)
        for k2 in range(3):
            ph = (t * 1.6 + k2 / 3) % 1
            for (ax, ay, ar, _, _), (bx, by, br, _, _) in zip(self.nodes, self.nodes[1:]):
                xx = ax + ar + (bx - br - ax - ar) * ph
                d.ellipse((xx - 4, ay - 4, xx + 4, ay + 4), fill=GREEN if not end else YELLOW)
        if win_pop:                                   # tia lấp lánh quanh mascot
            a = 1 - (t - lx[0]) / 0.9
            for i in range(8):
                ang = i * math.pi / 4 + t * 2
                r1, r2 = 70 + 30 * (1 - a), 86 + 40 * (1 - a)
                d.line((690 + r1 * math.cos(ang), o + 452 + r1 * math.sin(ang), 690 + r2 * math.cos(ang), o + 452 + r2 * math.sin(ang)), fill=alpha(YELLOW, a), width=4)
        last_sym = st["last"]["symbol"] if st["lastk"] == "check" else (st["last"] or {}).get("sym", "")
        d.text((470, o + 512), "RUG CHECK", font=F("Medium", 15), fill=PINK, anchor="mm")
        ok_last = st["lastk"] != "check" or st["last"]["ok"]
        d.text((470, o + 531), ("PASS $" if ok_last else "BLOCK $") + str(last_sym)[:8], font=F("Regular", 15), fill=PINK, anchor="mm")
        d.text((690, o + 531), "MR PUMP · " + ("done" if end else f"{(st['checked'] * 7 + int(t * 13)) % 90 + 20} msg/s"), font=F("Medium", 15), fill=YELLOW, anchor="mm")
        ex = "FLAT" if not st["open"] else "LIVE $" + list(st["open"])[-1][:7]
        d.text((900, o + 512), "EXECUTOR", font=F("Medium", 15), fill=GREEN, anchor="mm")
        d.text((900, o + 531), ex, font=F("Regular", 15), fill=GREEN, anchor="mm")

        # 4 thẻ
        sz, eqp = st["sizer"], st["equity"]
        vals = [(str(st["filtered"]), f"{st['passed']} passed"),
                ((f"{sz['size']*100:.0f}% eq" if sz else "--"), (money(sz["size"] * st["bal"]) if sz else "waiting")),
                (f"line #{st['line']}", "with a reason"),
                ((money(eqp["pnl"], True) if eqp else "+$0.00"), "last close")]
        for i, (v, sub) in enumerate(vals):
            x0 = self.RX0 + 12 + i * 175
            col = self.cards[i][0]
            if i == 3 and eqp:
                col = GREEN if eqp["pnl"] > 0 else PINK
            d.text((x0 + 12, o + 576), v, font=F("Bold", 24), fill=TXT if i < 3 else col)
            d.text((x0 + 12, o + 607), sub[:17], font=F("Regular", 15), fill=DIM)

        self.trade_card(im, st, t)
        d = ImageDraw.Draw(im)

        # tail -f (3 dòng, chữ to)
        alltail = [x for x in s.tail if x[0] <= t]
        d.text((self.RX1 - 14, o + 668), f"{len(alltail) + 2} lines", font=F("Regular", 14), fill=DIM, anchor="ra")
        tl = alltail[-3:]
        for j, (vt, a_, b_, c) in enumerate(tl):
            yy = o + 698 + j * 50
            d.text((708, yy), a_[:30], font=F("Medium", 16), fill=c)
            d.text((720, yy + 22), b_[:31], font=F("Regular", 14), fill=DIM)
        if int(t * 3) % 2 == 0:
            d.rectangle((708, o + 698 + len(tl) * 50, 717, o + 716 + len(tl) * 50), fill=GREEN)

        # RESULT: đường số dư
        bal = st["prev_bal"] + (st["bal"] - st["prev_bal"]) * ease(kb)
        self.equity_curve(d, t, bal, end)

        # LOG
        rows = [r for r in s.rows if r[0] <= t][-6:]
        for j, (vt, hh, kind, sym, title, why, right, rc) in enumerate(rows):
            yy = o + 1050 + j * 60
            age = t - vt
            new = (j == len(rows) - 1) and age < 1.5
            if new:
                fl = 1 - min(1, age / 0.4)
                d.rectangle((self.RX0 + 4, yy - 6, self.RX1 - 4, yy + 50), fill=tuple(int(18 + 30 * fl * (c / 255)) for c in (ORANGE if kind == "ENTER" else rc)))
                d.rectangle((self.RX0 + 4, yy - 6, self.RX0 + 8, yy + 50), fill=ORANGE)
            d.text((self.RX0 + 18, yy + 6), hh, font=F("Medium", 18), fill=DIM)
            bc = {"ENTER": ORANGE, "EXIT": GREEN if rc != PINK else PINK, "SCAN": BLUE, "CHECK": PINK}[kind]
            rr(d, (self.RX0 + 86, yy + 4, self.RX0 + 176, yy + 30), 4, outline=bc, width=2, fill=alpha(bc, .12))
            d.text((self.RX0 + 131, yy + 17), kind, font=F("Medium", 14), fill=bc, anchor="mm")
            if sym:
                d.ellipse((self.RX0 + 192, yy + 2, self.RX0 + 212, yy + 22), fill=s.sym_color.get(sym, ORANGE))
                d.text((self.RX0 + 202, yy + 12), sym[:1].upper(), font=F("Bold", 11), fill=BG, anchor="mm")
                d.text((self.RX0 + 220, yy), "$" + title[:10], font=F("Bold", 19), fill=TXT)
            else:
                d.text((self.RX0 + 192, yy), title, font=F("Bold", 19), fill=TXT)
            d.text((self.RX0 + 192, yy + 26), why[:50], font=F("Regular", 16), fill=alpha(ORANGE, .9))
            d.text((self.RX1 - 18, yy + 2), right, font=F("Bold", 20), fill=rc if kind == "EXIT" else ORANGE, anchor="ra")

        # chip bay + pop lãi/lỗ
        if not quiet:
            self.fliers(im, st, t)
        if loss_hit:
            a = 1 - (t - lx[0]) / 0.5
            g, pad = self.g_loss
            paste_a(im, g, (10 - pad, o + 10 - pad), a * 0.8)
            amp = int(6 * a)
            if amp:
                sh = int(amp * math.sin((t - lx[0]) * 90))
                term = im.crop((0, OY, W, OY + TH))
                im.paste(BG, (0, OY, W, OY + TH))
                im.paste(term, (sh, OY))
        return im

    def fliers(self, im, st, t):
        o = OY
        d = ImageDraw.Draw(im)
        le = st["last_enter"]
        if le and 0 <= t - le[0] < 0.6:                 # chip bay: hàng chip -> mascot -> executor
            k = (t - le[0]) / 0.6
            p0, p1, p2 = (self.RX1 - 14 - 172 + 85, o + 321), (690, o + 452), (900, o + 452)
            for gk in (0.0, 0.06, 0.12):
                kk = max(0, k - gk)
                if kk < 0.55:
                    u = ease(kk / 0.55)
                    c = (p0[0] * (1 - u) ** 2 + 2 * (1 - u) * u * 760 + u * u * p1[0], p0[1] * (1 - u) ** 2 + 2 * (1 - u) * u * (o + 250) + u * u * p1[1])
                else:
                    u = ease((kk - 0.55) / 0.45)
                    c = (p1[0] + (p2[0] - p1[0]) * u, p1[1])
                a = 1 if gk == 0 else 0.35
                r = 16 if gk == 0 else 11
                col = self.s.sym_color.get(le[1]["sym"], ORANGE)
                d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=alpha(col, a), outline=alpha(TXT, a), width=2)
                if gk == 0:
                    d.text((c[0] + 22, c[1] - 14), "$" + le[1]["sym"][:8], font=F("Bold", 20), fill=TXT)
        lx = st["last_exit"]
        if lx and 0 <= t - lx[0] < 1.0:                 # số lãi/lỗ bay lên từ thẻ EQUITY
            k = (t - lx[0]) / 1.0
            p = lx[1]
            col = GREEN if p["pnl"] > 0 else PINK
            big = p["pnl"] > 10
            sp = text_sprite(money(p["pnl"], True), F("ExtraBold", 48 if big else 36), col, 4, (4, 12, 8))
            s = back(min(1, k / 0.25))
            sp2 = sp.resize((max(1, int(sp.size[0] * s)), max(1, int(sp.size[1] * s))), Image.BICUBIC)
            x = self.RX0 + 12 + 3 * 175 + 82 - sp2.size[0] / 2
            x = min(x, W - 24 - sp2.size[0])
            y = o + 560 - 90 * ease(k) - sp2.size[1] / 2
            paste_a(im, sp2, (x, y), 1 if k < 0.7 else (1 - k) / 0.3)

    def trade_card(self, im, st, t):
        d = ImageDraw.Draw(im)
        o = OY
        tr = st["trade"]
        if not tr:
            d.text((350, o + 740), "waiting for a signal…", font=F("Regular", 18), fill=DIM)
            return
        kind, p, vt = tr
        sym = p["sym"]
        ent = p if kind == "enter" else self.s.entry_for(p)
        cc = self.s.sym_color.get(sym, ORANGE)
        d.ellipse((350, o + 696, 376, o + 722), fill=cc)
        d.text((363, o + 709), sym[:1].upper(), font=F("Bold", 15), fill=BG, anchor="mm")
        d.text((386, o + 692), "$" + sym[:9], font=F("ExtraBold", 26), fill=TXT)
        rows = self.s.rows_of.get(sym)
        now_ts = self.s.ts_at(t)
        pct = None
        if rows and ent:
            e_ts = ent["t"]
            x_ts = p["t"] if kind == "exit" else None
            vis = [r for r in rows if e_ts - 8 * 300 <= r[0] < (x_ts if x_ts else now_ts) and r[0] <= now_ts][-22:]
            if vis:
                last_c = vis[-1][4]
                pct = (p["pct"] if kind == "exit" else last_c * (1 - 0.015) / ent["price"] - 1)
                X0, X1, Y0, Y1 = 350, 670, o + 736, o + 806
                lo = min(min(r[3] for r in vis), ent["price"])
                hi = max(max(r[2] for r in vis), ent["price"])
                rng_ = (hi - lo) or hi * 0.01
                Y = lambda v: Y1 - (v - lo) / rng_ * (Y1 - Y0)
                cw = (X1 - X0) / 22
                for i, r in enumerate(vis):
                    cx = X0 + cw * (i + 0.5)
                    col = GREEN if r[4] >= r[1] else PINK
                    d.line((cx, Y(r[2]), cx, Y(r[3])), fill=col, width=2)
                    y_a, y_b = sorted((Y(r[1]), Y(r[4])))
                    d.rectangle((cx - cw * 0.32, y_a, cx + cw * 0.32, max(y_b, y_a + 2)), fill=col)
                ye = Y(ent["price"])
                for x in range(X0, X1, 10):
                    d.line((x, ye, x + 5, ye), fill=ORANGE, width=2)
                d.text((X1, ye - 18), "entry", font=F("Medium", 13), fill=ORANGE, anchor="ra")
                if kind == "exit":
                    d.ellipse((X0 + cw * (len(vis) - 0.5) - 6, Y(ent["price"] * (1 + p["pct"])) - 6, X0 + cw * (len(vis) - 0.5) + 6, Y(ent["price"] * (1 + p["pct"])) + 6), outline=TXT, width=3)
        if pct is None and kind == "exit":
            pct = p["pct"]
        if pct is not None:
            col = GREEN if pct >= 0 else PINK
            lab = f"{pct*100:+.1f}%" + (" live" if kind == "enter" else "")
            d.text((672, o + 694), lab, font=F("Bold", 22), fill=col, anchor="ra")
        size = (ent or p).get("size", 0) * 100
        d.text((350, o + 814), f"size {size:.0f}% · slip 1.5% · {'open' if kind == 'enter' else 'closed'}", font=F("Medium", 15), fill=TXT)
        why = p["why"].replace(" over 30m high", "")
        d.text((350, o + 836), why[:34], font=F("Regular", 14), fill=ORANGE)

    def equity_curve(self, d, t, bal, end):
        o = OY
        n = self.s.n
        pts = [(vt, b) for vt, b in self.s.curve if vt <= t]
        allb = [b for _, b in self.s.curve]
        lo, hi = min(allb), max(allb)
        rng_ = (hi - lo) or 1
        X0, X1, Y0, Y1 = self.RX0 + 18, 860, o + 912, o + 966
        X = lambda v: X0 + (min(v, T1) - T0) / (T1 - T0) * (X1 - X0)
        Y = lambda b: Y1 - (b - lo) / rng_ * (Y1 - Y0)
        ys = Y(n["start"])
        for x in range(X0, X1, 12):
            d.line((x, ys, x + 6, ys), fill=LINE, width=1)
        if t >= T0:
            line = []
            prev = pts[0][1]
            for vt, b in pts:
                line += [(X(vt), Y(prev)), (X(vt), Y(b))]
                prev = b
            line.append((X(max(T0, t)), Y(prev)))
            col = GREEN if bal >= n["start"] else PINK
            poly = line + [(line[-1][0], Y1), (line[0][0], Y1)]
            d.polygon(poly, fill=alpha(col, .18))
            d.line(line, fill=col, width=3)
            d.ellipse((line[-1][0] - 5, line[-1][1] - 5, line[-1][0] + 5, line[-1][1] + 5), fill=col)
        d.text((self.RX1 - 14, o + 908), "start " + money(n["start"]), font=F("Medium", 15), fill=DIM, anchor="ra")
        d.text((self.RX1 - 14, o + 930), money(bal), font=F("Bold", 26), fill=GREEN if bal >= n["start"] else PINK, anchor="ra")
        st_w, st_l = self._wl(t)
        d.text((self.RX0 + 18, o + 972), f"{st_w} W / ", font=F("Bold", 17), fill=GREEN)
        d.text((self.RX0 + 18 + F("Bold", 17).getlength(f"{st_w} W / "), o + 972), f"{st_l} L", font=F("Bold", 17), fill=PINK)
        d.text((self.RX1 - 14, o + 974), "paper · real 5m candles", font=F("Regular", 14), fill=DIM, anchor="ra")

    def _wl(self, t):
        w = l = 0
        for vt, k, p in self.s.items:
            if vt > t:
                break
            if k == "exit":
                if p["pnl"] > 0:
                    w += 1
                else:
                    l += 1
        return w, l

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
        if since < 0.9:
            if k == "enter":
                return {"SIZER"} if since < 0.3 else {"EXECUTOR"}
            if k == "exit":
                return {"EXECUTOR"} if since < 0.2 else ({"LOGGER"} if since < 0.5 else {"EQUITY"})
            if k == "skip":
                return {"SIZER"}
        if t - st["pulse_t"] < 0.18:
            return {"SCANNER"}
        return set()

    def hot_nodes(self, st, since, end):
        if end:
            return {"MR PUMP"}
        if since > 0.6:
            return set()
        return {"check": {"RUG CHECK"}, "enter": {"MR PUMP", "EXECUTOR"}, "exit": {"EXECUTOR"}, "skip": {"MR PUMP"}}.get(st["lastk"], set())

    def badge(self, name, st, end):
        if name == "YOU":
            return "READING" if end else "ASLEEP"
        if name == "EXECUTOR":
            return "LIVE" if st["open"] else "FLAT"
        return {"SCANNER": "SCAN", "RUG CHECK": "PASS", "SIZER": "SIZE", "LOGGER": "WRITE", "EQUITY": "UPDATE"}[name]

    def agent_line(self, name, st, end):
        chips = st["chips"]
        if name == "SCANNER":
            if chips:
                vt, sym, ok, why, p = chips[-1]
                if ok == "pulse":
                    return f"${sym[:8]} {p['pct']*100:+.1f}% 5m"
                if "liq" in p:
                    return f"${sym[:8]} · liq {short(p['liq'])}"
                return f"signal ${sym[:8]}"
            return "loading trending…"
        if name == "RUG CHECK":
            return f"{st['passed']} passed · {st['filtered']} blocked"
        if name == "SIZER":
            sz = st["sizer"]
            return f"{sz['size']*100:.0f}% of {money(st['bal'])}" if sz else "idle"
        if name == "EXECUTOR":
            return ("LONG $" + list(st["open"])[-1][:8]) if st["open"] else "flat · waiting"
        if name == "LOGGER":
            return f"line #{st['line']}"
        if name == "EQUITY":
            return f"{money(st['bal'])} · {st['trades']} closes"
        if name == "YOU":
            return f"{st['line']} lines to read"


def load(date):
    return json.load(open(os.path.join(ddir(date), "night.json")))


def load_candles(date):
    p = os.path.join(ddir(date), "candles.json")
    return json.load(open(p)) if os.path.exists(p) else None


def make_story(date):
    return Story(load(date), load_candles(date))


_P = None


def _init(date):
    global _P
    _P = Painter(make_story(date))


def _seg(args):
    date, f0, f1, path = args
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", path],
                         stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(_P.frame(f / FPS).convert("RGB").tobytes())
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
        P = Painter(make_story(date))
        ts = [float(x) for x in a[a.index("still") + 1:] if x.replace(".", "").isdigit()]
        out = os.path.join(HERE, "output")
        os.makedirs(out, exist_ok=True)
        for t in ts:
            P.frame(t).convert("RGB").save(f"{out}/still_{t:05.2f}.png")
        print("ok", ts)
    elif "video" in a:
        video(date, int(a[a.index("--jobs") + 1]) if "--jobs" in a else 4)
