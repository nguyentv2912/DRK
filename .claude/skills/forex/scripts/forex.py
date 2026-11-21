#!/usr/bin/env python3
"""forex.py — dựng video dọc 9:16 kiểu "quay tay màn hình app giao dịch forex".

Phong cách (phân tích từ video mẫu TikTok ~24s):
  điện thoại cầm tay trong phòng tối, đèn bokeh vàng phía trên, màn hình trắng sáng
  app kiểu terminal di động: tab Trade (Balance/Equity/Margin + Positions + Orders),
  chạm liên tục để đóng lệnh (vòng chạm màu, ô đỏ Close, thanh cam "Close #... with profit"),
  xen 2 lần biểu đồ M1 (ô SELL/BUY đỏ), kết thúc ở History > Deals cuộn danh sách.
  Cắt cảnh nhanh (jump cut 1–3s), rung tay, nhạc nhẹ ~92 BPM.

Lệnh:
  python3 -I forex.py sim  --seed 7 --out data.json [--n 10] [--start 100000]
  python3 -I forex.py check data.json
  python3 -I forex.py render data.json out.mp4 [--keys 2 8 15 22 --keydir dir] [--no-audio] [--lang vi|en]

Nhãn bắt buộc: mode "sim" luôn có nhãn MÔ PHỎNG; mode "demo" có nhãn DEMO ACCOUNT;
mode "real" có chú thích nhỏ "không phải lời khuyên đầu tư". Không thể tắt.
"""
import argparse, json, math, os, random, subprocess, sys, wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SW, SH = 800, 1733          # màn hình điện thoại (px nội bộ)
BEZ = 20                    # viền máy
FONT_DIR = "/usr/share/fonts/opentype/inter"

BLUE = (30, 80, 220)
RED = (205, 30, 40)
GRAY = (130, 130, 138)
DARK = (25, 25, 30)
SEC_BG = (236, 236, 240)
ORANGE = (243, 166, 18)
TAP_COLORS = [(255, 120, 200), (120, 220, 120), (255, 200, 60), (160, 140, 255), (255, 130, 60), (90, 200, 255)]

# kích thước hợp đồng mặc định (broker có thể khác -> check chỉ cảnh báo)
CONTRACT = {"XAU": 100, "XAG": 5000, "US30": 1, "NAS100": 1, "US500": 1, "UKOIL": 100, "USOIL": 100,
            "BTC": 1, "ETH": 1}

_fc = {}


def F(size, w="Regular", disp=False):
    k = (size, w, disp)
    if k not in _fc:
        name = ("InterDisplay-" if disp and size >= 40 else "Inter-") + w + ".otf"
        _fc[k] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _fc[k]


def fmt(v, d=2, sign=False):
    s = f"{abs(v):,.{d}f}".replace(",", " ")
    if sign:
        return ("+" if v >= 0 else "−") + s
    return ("−" if v < 0 else "") + s


def digits(sym, price):
    if "JPY" in sym:
        return 3
    if price > 500:
        return 2
    if price > 20:
        return 2
    return 5


# ---------------------------------------------------------------- dữ liệu
def contract_size(sym):
    s = sym.upper().replace(".U", "").replace(".", "")
    for k, v in CONTRACT.items():
        if s.startswith(k):
            return v
    return 100000


def calc_profit(p):
    """Lãi xấp xỉ theo USD (tài khoản USD). Dùng cho mô phỏng và cảnh báo khi check."""
    s = p["symbol"].upper().replace(".U", "")
    d = 1 if p["side"] == "buy" else -1
    diff = (p["close"] - p["open"]) * d
    cs = contract_size(s)
    v = diff * p["lots"] * cs
    if cs == 100000 and not s.endswith("USD"):
        # quote không phải USD: đổi bằng giá đóng (USDJPY, USDCAD...) hoặc ước lượng cho chéo
        if s.startswith("USD"):
            v /= p["close"]
        elif "JPY" in s:
            v /= 155.0
        elif s.endswith("GBP"):
            v *= 1.27
        elif s.endswith("CHF"):
            v /= 0.88
        elif s.endswith("CAD"):
            v /= 1.37
        elif s.endswith("AUD"):
            v *= 0.65
    return round(v, 2)


SIM_SYMS = [("XAUUSD", 3900, 6.0, (0.2, 1.6)), ("GBPJPY", 212.7, 0.25, (0.3, 2.5)), ("EURUSD", 1.0850, 0.0020, (0.5, 3)),
            ("USDJPY", 158.6, 0.25, (0.5, 2)), ("US30", 51540, 60, (0.3, 1.5)), ("UKOIL", 95.8, 0.6, (0.2, 1)),
            ("GBPUSD", 1.2710, 0.0020, (0.5, 3)), ("BTCUSD", 98000, 400, (0.05, 0.6)), ("AUDUSD", 0.6540, 0.0016, (0.5, 3))]


def make_sim(seed, n, start):
    rnd = random.Random(seed)
    pos = []
    for i in range(n):
        sym, px, vol, (l0, l1) = rnd.choice(SIM_SYMS)
        side = rnd.choice(["buy", "sell"])
        lots = round(rnd.uniform(l0, l1), 2)
        o = px * (1 + rnd.uniform(-0.004, 0.004))
        dd = digits(sym, o)
        move = vol * rnd.uniform(0.2, 1.4) * (1 if rnd.random() < 0.8 else -0.4)
        c = o + move if side == "buy" else o - move
        p = {"id": rnd.randint(2_080_000_000, 2_089_999_999), "symbol": sym, "side": side, "lots": lots,
             "open": round(o, dd), "close": round(c, dd)}
        p["profit"] = calc_profit(p)
        pos.append(p)
    deals = []
    for i in range(24):
        sym, px, vol, (l0, l1) = rnd.choice(SIM_SYMS)
        deals.append({"symbol": sym, "side": rnd.choice(["buy", "sell"]), "lots": round(rnd.uniform(l0, l1), 2),
                      "time": f"2026.11.{rnd.randint(10,20):02d} {rnd.randint(1,23):02d}:{rnd.randint(0,59):02d}",
                      "profit": round(rnd.uniform(-120, 520), 2)})
    for p in pos:
        deals.insert(0, {"symbol": p["symbol"], "side": "buy" if p["side"] == "sell" else "sell", "lots": p["lots"],
                         "time": "2026.11.21 19:1%d" % rnd.randint(0, 9), "profit": p["profit"]})
    hp = round(sum(d["profit"] for d in deals), 2)
    gold = [p for p in pos if p["symbol"].startswith("XAU")]
    last = gold[0]["close"] if gold else 3906.10
    data = {
        "mode": "sim", "currency": "USD", "seed": seed,
        "account": {"balance_start": None, "leverage": 500},
        "positions": pos,
        "pending": [{"symbol": "XAUUSD", "type": "buy stop", "lots": 1.5, "price": round(last + 7, 2)}],
        "chart": {"symbol": "XAUUSD", "tf": "M1", "last": last},
        "history": {"deposit": start, "swap": round(-rnd.uniform(50, 300), 2), "commission": 0.0, "deals": deals},
    }
    h = data["history"]
    # số dư cuối ở tab Trade == Balance ở History (nhất quán)
    data["account"]["balance_start"] = round(start + hp + h["swap"] + h["commission"] - sum(p["profit"] for p in pos), 2)
    return data


def derive(d):
    """Tính các số phụ thuộc — mọi con số hiển thị đều đi qua đây."""
    acc = d["account"]
    pos = d["positions"]
    total_float = sum(p["profit"] for p in pos)
    bal0 = acc["balance_start"]
    h = d.get("history", {})
    deals = h.get("deals", [])
    hp = round(sum(x["profit"] for x in deals), 2)
    out = {"float0": total_float, "bal0": bal0, "bal_end": round(bal0 + total_float, 2),
           "hist_profit": hp,
           "hist_balance": round(h.get("deposit", 0) + hp + h.get("swap", 0) + h.get("commission", 0), 2)}
    return out


def check(d, strict=False):
    msgs = []
    assert d.get("mode") in ("sim", "demo", "real"), "mode phải là sim | demo | real"
    for p in d["positions"]:
        est = calc_profit(p)
        if abs(est - p["profit"]) > max(5, 0.15 * abs(p["profit"])):
            msgs.append(f"cảnh báo: #{p.get('id')} {p['symbol']} profit {p['profit']} lệch ước tính {est} "
                        "(contract size broker có thể khác — đối chiếu ảnh gốc)")
    dv = derive(d)
    msgs.append(f"balance {fmt(dv['bal0'])} → {fmt(dv['bal_end'])}  (đóng {len(d['positions'])} lệnh, "
                f"tổng {fmt(dv['float0'], sign=True)})")
    msgs.append(f"history: profit {fmt(dv['hist_profit'])}, balance {fmt(dv['hist_balance'])}")
    hb = d.get("history", {}).get("balance")
    if abs(dv["bal_end"] - dv["hist_balance"]) > 0.01:
        msgs.append(f"cảnh báo: số dư cuối tab Trade {fmt(dv['bal_end'])} ≠ Balance tab History {fmt(dv['hist_balance'])}")
    if hb is not None and abs(hb - dv["hist_balance"]) > 0.01:
        msgs.append(f"LỖI: history.balance {hb} ≠ deposit+profit+swap+commission {dv['hist_balance']}")
    return msgs


# ---------------------------------------------------------------- timeline
def build_timeline(d, dur):
    n = len(d["positions"])
    g = [max(1, round(n * 0.45)), max(1, round(n * 0.35))]
    g.append(max(0, n - g[0] - g[1]))
    if sum(g) > n:
        g[1] = n - g[0]; g[2] = 0
    # cảnh: (start, end, screen)
    k = dur / 24.0
    scenes = [(0, 6.6 * k, "trade"), (6.6 * k, 9.4 * k, "chart"), (9.4 * k, 15.8 * k, "trade"),
              (15.8 * k, 18.0 * k, "chart"), (18.0 * k, 20.4 * k, "trade"), (20.4 * k, dur, "history")]
    trade_scenes = [s for s in scenes if s[2] == "trade"]
    closes = []  # (t_tap, idx)
    taps = []    # (t, kind, arg, x, y) toạ độ trên màn hình
    rnd0 = random.Random(d.get("seed", 1) * 7 + 3)
    open_list = list(range(n))
    for (a, b, _), cnt in zip(trade_scenes, g):
        if cnt == 0:
            continue
        step = (b - a - 0.8) / cnt
        for j in range(cnt):
            tt = a + 0.5 + j * step + rnd0.uniform(-0.12, 0.12)
            rank = rnd0.randrange(min(3, len(open_list)))   # không phải lúc nào cũng dòng đầu
            idx = open_list.pop(rank)
            closes.append((tt, idx))
            taps.append((tt, "close", idx, SW - 170 + rnd0.uniform(-30, 30), ROW0 + rank * ROWH + 32))
    for a, b, sc in scenes[1:]:
        i = {"chart": 1, "trade": 2, "history": 3}.get(sc, 2)
        taps.append((a - 0.12, "tab", sc, SW * (i + 0.5) / 5, SH - 105))
    hs = scenes[-1][0]
    for tf in (hs + 0.9, hs + 2.3):          # vuốt cuộn danh sách deal
        if tf < dur - 0.5:
            taps.append((tf, "flick", None, SW * 0.55, SH * 0.72))
    # jump cut camera shots ~1.3–2.6s
    rnd = random.Random(d.get("seed", 1))
    shots, t = [], 0.0
    while t < dur:
        ln = rnd.uniform(1.3, 2.6)
        shots.append((t, dict(scale=rnd.uniform(0.64, 0.74), dx=rnd.uniform(-40, 40), dy=rnd.uniform(10, 60),
                              ang=rnd.uniform(-4, 4), ph=rnd.uniform(0, 100))))
        t += ln
    # cắt cảnh bắt buộc trùng chỗ đổi màn hình
    for a, _, _ in scenes[1:]:
        shots.append((a, dict(scale=rnd.uniform(0.64, 0.74), dx=rnd.uniform(-40, 40), dy=rnd.uniform(10, 60),
                              ang=rnd.uniform(-4, 4), ph=rnd.uniform(0, 100))))
    shots.sort(key=lambda s: s[0])
    return {"scenes": scenes, "closes": closes, "taps": sorted(taps, key=lambda x: x[0]), "shots": shots, "dur": dur}


ROW0, ROWH = 442, 82   # y dòng lệnh đầu tiên và khoảng cách dòng trong tab Trade


def thumb_state(t, taps):
    """Vị trí đầu ngón cái (toạ độ màn hình) và độ nhấc (0 = đang chạm, 1 = lơ lửng)."""
    REST = (SW + 140, SH + 260)
    kf = [(-1.0, REST[0], REST[1], 1.0)]
    prev_end = -1.0
    for tt, kind, arg, x, y in taps:
        hx, hy = x + 26, y + 46
        if tt - prev_end > 1.6:
            kf.append((prev_end + 0.5, *REST, 1.0))
            kf.append((tt - 0.5, *REST, 1.0))
        kf.append((tt - 0.16, hx, hy, 1.0))
        kf.append((tt, x, y, 0.0))
        if kind == "flick":
            kf.append((tt + 0.22, x, y - 520, 0.0))
            kf.append((tt + 0.42, x + 30, y - 470, 1.0))
            prev_end = tt + 0.42
        else:
            kf.append((tt + 0.1, x, y, 0.0))
            kf.append((tt + 0.3, hx, hy, 1.0))
            prev_end = tt + 0.3
    kf.append((prev_end + 0.5, *REST, 1.0))
    kf.append((1e9, *REST, 1.0))
    kf.sort(key=lambda k: k[0])
    for a, b in zip(kf, kf[1:]):
        if a[0] <= t < b[0]:
            u = (t - a[0]) / max(1e-6, b[0] - a[0])
            u = u * u * (3 - 2 * u)
            return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
    return (*REST, 1.0)


# ---------------------------------------------------------------- vẽ màn hình
def status_bar(dr, clock):
    dr.text((70, 30), clock, font=F(30, "SemiBold"), fill=DARK)
    dr.rounded_rectangle((SW // 2 - 120, 18, SW // 2 + 120, 82), 32, fill=(0, 0, 0))  # dynamic island
    dr.text((SW - 200, 32), "5G", font=F(26, "SemiBold"), fill=DARK)
    for i in range(4):
        dr.rectangle((SW - 240 + i * 9, 54 - i * 6, SW - 234 + i * 9, 58), fill=DARK)
    dr.rounded_rectangle((SW - 150, 36, SW - 90, 60), 7, outline=DARK, width=2)
    dr.rectangle((SW - 146, 40, SW - 104, 56), fill=DARK)


TABS = [("Quotes", "q"), ("Chart", "c"), ("Trade", "t"), ("History", "h"), ("Settings", "s")]


def tab_bar(dr, active):
    y = SH - 150
    dr.line((0, y, SW, y), fill=(225, 225, 230), width=2)
    for i, (name, _) in enumerate(TABS):
        cx = int(SW * (i + 0.5) / 5)
        on = name.lower() == active
        col = (60, 90, 200) if on else (120, 120, 128)
        if on:
            dr.ellipse((cx - 38, y + 18, cx + 38, y + 74), fill=(225, 230, 248))
        # icon tối giản
        if i == 0:
            dr.line((cx - 12, y + 34, cx - 12, y + 58), fill=col, width=3); dr.line((cx + 8, y + 34, cx + 8, y + 58), fill=col, width=3)
        elif i == 1:
            for k, hh in enumerate((18, 26, 14)):
                x = cx - 12 + k * 12; dr.line((x, y + 46 - hh // 2, x, y + 46 + hh // 2), fill=col, width=4)
        elif i == 2:
            dr.rounded_rectangle((cx - 15, y + 32, cx + 15, y + 60), 5, outline=col, width=3)
            dr.line((cx - 8, y + 50, cx - 2, y + 44), fill=col, width=3); dr.line((cx - 2, y + 44, cx + 8, y + 52), fill=col, width=3)
        elif i == 3:
            dr.ellipse((cx - 15, y + 31, cx + 15, y + 61), outline=col, width=3); dr.line((cx, y + 46, cx, y + 37), fill=col, width=3)
            dr.line((cx, y + 46, cx + 8, y + 50), fill=col, width=3)
        else:
            dr.ellipse((cx - 14, y + 32, cx + 14, y + 60), outline=col, width=3); dr.ellipse((cx - 5, y + 41, cx + 5, y + 51), fill=col)
        tw = dr.textlength(name, font=F(20))
        dr.text((cx - tw / 2, y + 82), name, font=F(20, "Medium"), fill=col)
    dr.rounded_rectangle((SW // 2 - 110, SH - 22, SW // 2 + 110, SH - 14), 4, fill=(20, 20, 20))


def toast(dr, text1, text2, alpha_y):
    y0 = SH - 150 - 96 + alpha_y
    dr.rectangle((0, y0, SW, y0 + 96), fill=ORANGE)
    for k, t in enumerate((text1, text2)):
        tw = dr.textlength(t, font=F(22, "Medium"))
        dr.text(((SW - tw) / 2, y0 + 16 + k * 32), t, font=F(22, "Medium"), fill=(60, 40, 5))


def right(dr, x, y, s, font, fill):
    dr.text((x - dr.textlength(s, font=font), y), s, font=font, fill=fill)


def live_profit(p, t, idx):
    """Lãi trôi nổi nhấp nháy quanh giá trị cuối (giống tick thật), hội tụ đúng số khi đóng."""
    a = 0.012 * abs(p["profit"]) + 2
    j = math.sin(t * 7.3 + idx * 1.7) * 0.6 + math.sin(t * 13.1 + idx * 0.9) * 0.4
    return p["profit"] + a * j


def draw_trade(t, d, st, dv, lang):
    img = Image.new("RGB", (SW, SH), (252, 252, 253))
    dr = ImageDraw.Draw(img)
    status_bar(dr, st["clock"])
    pos = d["positions"]
    closed_at = {i: tt for tt, i in st["tl"]["closes"]}
    open_idx = [i for i in range(len(pos)) if closed_at.get(i, 1e9) + 0.35 > t]
    closed_idx = [i for i in range(len(pos)) if closed_at.get(i, 1e9) + 0.35 <= t]
    flo = sum(live_profit(pos[i], t, i) for i in open_idx)
    bal = dv["bal0"] + sum(pos[i]["profit"] for i in closed_idx)
    eq = bal + flo
    margin = sum(pos[i]["lots"] for i in open_idx) * 520.0
    # header
    dr.rounded_rectangle((50, 118, 86, 146), 5, outline=(90, 90, 100), width=3)
    dr.text((SW - 82, 104), "+", font=F(52, "Light"), fill=(60, 60, 70))
    hdr = f"{fmt(flo)} {d.get('currency','USD')}"
    tw = dr.textlength(hdr, font=F(42, "SemiBold", True))
    dr.text(((SW - tw) / 2, 106), hdr, font=F(42, "SemiBold", True), fill=BLUE if flo >= 0 else RED)
    rows = [("Balance:", fmt(bal)), ("Equity:", fmt(eq)), ("Margin:", fmt(margin)),
            ("Free Margin:", fmt(eq - margin)), ("Margin Level (%):", fmt(eq / margin * 100 if margin else 0))]
    y = 182
    for a, b in rows:
        dr.text((40, y), a, font=F(25), fill=(70, 70, 78))
        right(dr, SW - 40, y, b, F(25), (40, 40, 48))
        y += 38
    y += 14
    dr.rectangle((0, y, SW, y + 46), fill=SEC_BG); dr.text((40, y + 9), "Positions", font=F(24, "SemiBold"), fill=(70, 70, 78))
    y += 56
    rowy = {}
    for i in open_idx:
        p = pos[i]
        ct = closed_at.get(i, 1e9)
        slide = 0
        if ct - 0.25 <= t:              # vuốt trái lộ ô đỏ Close
            slide = min(1.0, (t - (ct - 0.25)) / 0.25) * 150
        lp = live_profit(p, t, i) if t < ct else p["profit"]
        x0 = 40 - slide
        sideword = f"{p['side']} {p['lots']:.2f}"
        dr.text((x0, y), p["symbol"] + ", ", font=F(27, "SemiBold"), fill=DARK)
        dr.text((x0 + dr.textlength(p["symbol"] + ", ", font=F(27, "SemiBold")), y), sideword, font=F(27, "SemiBold"),
                fill=BLUE if p["side"] == "buy" else RED)
        dd = digits(p["symbol"], p["open"])
        dr.text((x0, y + 36), f"{p['open']:.{dd}f} → {p['close']:.{dd}f}", font=F(21), fill=GRAY)
        rowy[i] = y
        big = (i == open_idx[0]) or abs(p["profit"]) > 300
        right(dr, SW - 40 - slide, y + (4 if big else 10), fmt(lp, sign=big) if big else fmt(lp),
              F(34 if big else 27, "SemiBold" if big else "Regular"), BLUE if lp >= 0 else RED)
        if slide > 0:
            dr.rectangle((SW - slide, y - 8, SW, y + 70), fill=(225, 20, 30))
            right(dr, SW - 20, y + 20, "Close", F(24, "SemiBold"), (255, 255, 255))
        y += 82
        if y > SH - 420:
            break
    y += 6
    dr.rectangle((0, y, SW, y + 46), fill=SEC_BG); dr.text((40, y + 9), "Orders", font=F(24, "SemiBold"), fill=(70, 70, 78))
    y += 58
    for o in d.get("pending", [])[:2]:
        dr.text((40, y), f"{o['symbol']}, {o['type']}", font=F(27, "SemiBold"), fill=BLUE if "buy" in o["type"] else RED)
        dr.text((40, y + 36), f"{o['lots']:.2f} / 0 at {fmt(o['price'])}", font=F(21), fill=GRAY)
        right(dr, SW - 40, y + 14, "placed", F(26), GRAY)
        y += 82
    # toast của lệnh vừa đóng
    last = [(tt, i) for tt, i in st["tl"]["closes"] if tt <= t < tt + 1.9]
    if last:
        tt, i = last[-1]
        p = pos[i]
        cs = "buy" if p["side"] == "sell" else "sell"
        k = min(1.0, (t - tt) / 0.12)
        toast(dr, f"Close #{p.get('id', 2084713400 + i)} {cs} {p['lots']:.2f} {p['symbol']} at "
                  f"{p['close']:.{digits(p['symbol'], p['close'])}f}", f"with profit {fmt(p['profit'])}", int((1 - k) * 96))
    tab_bar(dr, "trade")
    return img, rowy


def candle_series(d):
    rnd = np.random.default_rng(d.get("seed", 3))
    last = d["chart"]["last"]
    n = 120
    t = np.linspace(0, 1, n)
    base = np.sin(t * math.pi * 2.6 + 0.6) * 0.55 + np.sin(t * 9) * 0.08
    noise = np.cumsum(rnd.normal(0, 0.035, n))
    path = base + noise - (base + noise)[-1]
    span = last * 0.0035
    closes = last + path * span
    o = np.roll(closes, 1); o[0] = closes[0]
    hi = np.maximum(o, closes) + np.abs(rnd.normal(0, span * 0.05, n))
    lo = np.minimum(o, closes) - np.abs(rnd.normal(0, span * 0.05, n))
    return o, hi, lo, closes


def draw_chart(t, d, st, dv, lang):
    img = Image.new("RGB", (SW, SH), (252, 252, 253))
    dr = ImageDraw.Draw(img)
    status_bar(dr, st["clock"])
    sym = d["chart"]["symbol"]; last = d["chart"]["last"]
    o, hi, lo, c = st["candles"]
    # tick sống: nến cuối nhấp nháy
    c = c.copy(); c[-1] = last + math.sin(t * 9) * last * 0.00012
    dr.text((40, 104), d["chart"].get("tf", "M1"), font=F(26, "SemiBold"), fill=DARK)
    dr.text((SW // 2 - 50, 104), "+  f  ⋮", font=F(26), fill=(80, 80, 90))
    sp = last * 0.00013
    dr.rectangle((40, 150, 330, 214), fill=(220, 30, 30))
    dr.text((56, 156), "SELL", font=F(18, "SemiBold"), fill=(255, 220, 220))
    dr.text((56, 176), fmt(c[-1] - sp), font=F(30, "Bold"), fill=(255, 255, 255))
    dr.rectangle((SW - 330, 150, SW - 40, 214), fill=(220, 30, 30))
    dr.text((SW - 316, 156), "BUY", font=F(18, "SemiBold"), fill=(255, 220, 220))
    dr.text((SW - 316, 176), fmt(c[-1] + sp), font=F(30, "Bold"), fill=(255, 255, 255))
    right(dr, SW // 2 + 34, 166, "0.50", F(26), DARK)
    dr.text((40, 232), f"{sym} • {d['chart'].get('tf','M1')}", font=F(22, "SemiBold"), fill=DARK)
    dr.text((40, 260), "Gold Spot / U.S. Dollar", font=F(19), fill=GRAY)
    top, bot, left, rgt = 320, SH - 300, 30, SW - 130
    pmin, pmax = lo.min(), hi.max()
    pad = (pmax - pmin) * 0.08
    pmin -= pad; pmax += pad
    Y = lambda p: bot - (p - pmin) / (pmax - pmin) * (bot - top)
    n = len(c)
    cw = (rgt - left) / n
    for k in range(6):
        pv = pmin + (pmax - pmin) * k / 5
        dr.text((rgt + 12, Y(pv) - 12), f"{pv:.2f}", font=F(19), fill=GRAY)
    for i in range(n):
        x = left + i * cw + cw / 2
        col = (40, 70, 200) if c[i] >= o[i] else (30, 30, 40)
        dr.line((x, Y(hi[i]), x, Y(lo[i])), fill=col, width=2)
        dr.line((x - cw * 0.35, Y(o[i]), x, Y(o[i])), fill=col, width=2)
        dr.line((x, Y(c[i]), x + cw * 0.35, Y(c[i])), fill=col, width=2)
    # đường lệnh đang mở trên symbol này (từ dữ liệu)
    lines = [p for p in d["positions"] if p["symbol"].upper().startswith(sym.upper()[:6])][:2]
    for p in lines:
        if pmin < p["open"] < pmax:
            yy = Y(p["open"])
            for x in range(int(left), int(rgt), 14):
                dr.line((x, yy, x + 7, yy), fill=(120, 130, 160), width=2)
            dr.text((left + 6, yy - 26), f"{p['side'].upper()} {p['lots']:.2f}, {fmt(p['profit'], sign=True)} USD",
                    font=F(18), fill=(90, 100, 140))
    yl = Y(c[-1])
    dr.rectangle((rgt + 4, yl - 16, SW - 10, yl + 16), fill=(40, 100, 230))
    dr.text((rgt + 10, yl - 12), f"{c[-1]:.2f}", font=F(19, "SemiBold"), fill=(255, 255, 255))
    pos = d["positions"]
    recent = [(tt, i) for tt, i in st["tl"]["closes"] if tt <= t]
    if recent:
        tt, i = recent[-1]
        p = pos[i]; cs = "buy" if p["side"] == "sell" else "sell"
        toast(dr, f"Close #{p.get('id', 2084713400 + i)} {cs} {p['lots']:.2f} {p['symbol']} at "
                  f"{p['close']:.{digits(p['symbol'], p['close'])}f}", f"with profit {fmt(p['profit'])}", 0)
    tab_bar(dr, "chart")
    return img, {}


def draw_history(t, d, st, dv, lang, t0):
    img = Image.new("RGB", (SW, SH), (252, 252, 253))
    dr = ImageDraw.Draw(img)
    h = d.get("history", {})
    deals = h.get("deals", [])
    scroll = 0.0
    for tt, kind, *_ in st["tl"]["taps"]:
        if kind == "flick" and tt <= t:
            scroll += 2600 * 0.32 * (1 - math.exp(-(t - tt) / 0.32))
    scroll = min(scroll, max(0, len(deals) * 74 - (SH - 160 - 560) + 40))
    # danh sách (vẽ trước, header che lên)
    y = 560 - scroll
    for x in deals:
        if y > SH - 160:
            break
        if y > 470:
            dr.text((40, y), f"{x['symbol']}, ", font=F(25, "SemiBold"), fill=DARK)
            w1 = dr.textlength(f"{x['symbol']}, ", font=F(25, "SemiBold"))
            dr.text((40 + w1, y), f"{x['side']} {x['lots']:.2f} out", font=F(25, "SemiBold"),
                    fill=BLUE if x["side"] == "buy" else RED)
            dr.text((40, y + 32), x.get("time", ""), font=F(19), fill=GRAY)
            right(dr, SW - 40, y + 10, fmt(x["profit"]), F(26), BLUE if x["profit"] >= 0 else RED)
        y += 74
    dr.rectangle((0, 0, SW, 470), fill=(252, 252, 253))
    status_bar(dr, st["clock"])
    seg = ["Positions", "Orders", "Deals"]
    dr.rounded_rectangle((150, 104, SW - 150, 152), 24, fill=(238, 238, 242))
    sw = (SW - 300) / 3
    dr.rounded_rectangle((150 + 2 * sw + 4, 108, SW - 154, 148), 20, fill=(255, 255, 255))
    for k, s in enumerate(seg):
        tw = dr.textlength(s, font=F(22, "Medium"))
        dr.text((150 + k * sw + (sw - tw) / 2, 116), s, font=F(22, "Medium"), fill=DARK)
    rows = [("Profit:", fmt(dv["hist_profit"])), ("Deposit:", fmt(h.get("deposit", 0))), ("Swap:", fmt(h.get("swap", 0))),
            ("Commission:", fmt(h.get("commission", 0))), ("Balance:", fmt(dv["hist_balance"]))]
    y = 190
    for a, b in rows:
        dr.text((40, y), a, font=F(25), fill=(70, 70, 78))
        right(dr, SW - 40, y, b, F(25), (40, 40, 48))
        y += 40
    dr.rectangle((0, y + 8, SW, y + 50), fill=SEC_BG)
    win = sum(1 for x in deals if x["profit"] > 0)
    dr.text((40, y + 16), f"{len(deals)} deals · {win}/{len(deals)} in profit", font=F(20), fill=GRAY)
    tab_bar(dr, "history")
    return img, {}


# ---------------------------------------------------------------- ống kính / cảnh
def make_background(seed):
    rnd = random.Random(seed)
    bg = Image.new("RGB", (W, H), (12, 13, 18))
    px = np.zeros((H, W, 3), np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    g = np.exp(-(((xx - W * 0.5) / (W * 0.9)) ** 2 + ((yy - H * 0.55) / (H * 0.6)) ** 2))
    px[..., 0] = 14 + 22 * g; px[..., 1] = 15 + 22 * g; px[..., 2] = 22 + 30 * g
    bg = Image.fromarray(px.clip(0, 255).astype(np.uint8))
    bok = Image.new("RGB", (W, H), (0, 0, 0))
    bd = ImageDraw.Draw(bok)
    for _ in range(26):  # đèn bokeh trần nhà
        x = rnd.uniform(0, W); y = rnd.uniform(0, H * 0.16); r = rnd.uniform(5, 14)
        c = (255, rnd.randint(200, 235), rnd.randint(120, 170))
        bd.ellipse((x - r, y - r, x + r, y + r), fill=c)
    bok = bok.filter(ImageFilter.GaussianBlur(6))
    bg = Image.fromarray(np.clip(np.asarray(bg, np.int16) + np.asarray(bok, np.int16), 0, 255).astype(np.uint8))
    return bg


def make_phone_mask():
    pw, ph = SW + 2 * BEZ, SH + 2 * BEZ
    m = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pw - 1, ph - 1), 110, fill=255)
    sm = Image.new("L", (SW, SH), 0)
    ImageDraw.Draw(sm).rounded_rectangle((0, 0, SW - 1, SH - 1), 92, fill=255)
    return m, sm


def _skin(mask, lx, ly, base=(150, 104, 84), seed=0):
    """Tô da theo mask: sáng dần về phía màn hình (lx, ly), có kết cấu nhẹ."""
    m = np.asarray(mask, np.float32) / 255
    # khối tròn: giữa ngón sáng, mép tối (dùng mask làm mờ như bản đồ độ cao)
    hb = np.asarray(mask.filter(ImageFilter.GaussianBlur(24)), np.float32) / 255
    vol = 0.30 + 0.70 * np.clip(hb * 1.6, 0, 1) ** 0.9
    hh, ww = m.shape
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    dist = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2)
    light = (0.22 + 0.78 * np.exp(-dist / 300.0)) * vol
    tex = np.random.default_rng(seed).normal(1, 0.035, (hh // 4 + 1, ww // 4 + 1)).astype(np.float32)
    tex = np.repeat(np.repeat(tex, 4, 0), 4, 1)[:hh, :ww]
    rgb = np.stack([base[0] * light * tex, base[1] * light * tex, (base[2] * light + 14 * light) * tex], 2)
    a = (m * 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb.clip(0, 255).astype(np.uint8), a]), "RGBA")


def hand_layer(pw, ph):
    """Tay trái cầm máy: lòng bàn tay phía sau, 4 ngón ôm mép phải (đè lên viền máy)."""
    size = (pw + 400, ph + 400)
    ox, oy = 200, 200
    mb = Image.new("L", size, 0)
    d = ImageDraw.Draw(mb)
    d.ellipse((ox - 260, oy + ph * 0.58, ox + pw * 0.75, oy + ph + 380), fill=255)      # lòng bàn tay
    d.rounded_rectangle((ox - 120, oy + ph * 0.50, ox + 40, oy + ph * 0.80), 70, fill=255)  # gốc ngón cái tay trái
    mb = mb.filter(ImageFilter.GaussianBlur(5))
    back = _skin(mb, ox + pw * 0.3, oy + ph * 0.7, (96, 68, 56), 1)
    mf = Image.new("L", size, 0)
    d = ImageDraw.Draw(mf)
    FING = [(0.44, 0.070, 150), (0.525, 0.074, 175), (0.615, 0.071, 160), (0.70, 0.060, 120)]
    for fy, fh, fl in FING:                  # 4 ngón ôm mép phải, chồng lên viền máy ~22px
        y = oy + ph * fy
        d.rounded_rectangle((ox + pw - 22, y, ox + pw + fl + 60, y + ph * fh), 50, fill=255)
    d.rounded_rectangle((ox - 30, oy + ph * 0.62, ox + 26, oy + ph * 0.76), 28, fill=255)  # đầu ngón cái trái ở mép trái
    mf = mf.filter(ImageFilter.GaussianBlur(2.5))
    front = _skin(mf, ox + pw - 20, oy + ph * 0.6, (150, 104, 86), 2)
    ov = Image.new("RGBA", size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(ov)
    for fy, fh, fl in FING:                  # đầu ngón bắt sáng màn hình
        y = oy + ph * fy
        fd.rounded_rectangle((ox + pw - 18, y + 16, ox + pw + 4, y + ph * fh - 16), 10, fill=(225, 195, 185, 80))
    ov = ov.filter(ImageFilter.GaussianBlur(3))
    ov.putalpha(Image.fromarray(np.minimum(np.asarray(ov)[..., 3], np.asarray(front)[..., 3])))
    front.alpha_composite(ov)
    front = front.filter(ImageFilter.GaussianBlur(1.2))
    return back, front, ox, oy


def thumb_sprite():
    """Ngón cái tay phải đi từ góc dưới phải; đầu ngón nằm đúng tâm sprite. Trả về (sprite, tâm), bản nhấc, bóng."""
    S = 1100
    c = S // 2
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((c - 62, c - 20, c + 62, c + 190), fill=255)          # đầu ngón (tâm chạm ở trên)
    d.rounded_rectangle((c - 74, c + 80, c + 74, S + 80), 72, fill=255)   # thân ngón
    m = m.filter(ImageFilter.GaussianBlur(2))
    spr = _skin(m, c, c, (205, 150, 126), 3)
    ov = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    dd.ellipse((c - 40, c - 6, c + 40, c + 110), fill=(240, 212, 205, 175))      # móng
    dd.arc((c - 40, c - 6, c + 40, c + 110), 200, 340, fill=(255, 240, 235, 160), width=4)
    dd.line((c - 50, c + 260, c + 46, c + 272), fill=(120, 80, 66, 120), width=3)  # nếp khớp
    spr.alpha_composite(ov.filter(ImageFilter.GaussianBlur(1.5)))
    spr = spr.resize((int(S * 0.82), int(S * 0.82)), Image.BICUBIC)
    S = spr.width; c = S // 2
    spr = spr.rotate(38, resample=Image.BICUBIC)
    lift = spr.resize((int(S * 1.06), int(S * 1.06)), Image.BILINEAR).crop((int(S * 0.03), int(S * 0.03), int(S * 0.03) + S, int(S * 0.03) + S))
    a = np.asarray(spr)[..., 3]
    shadow = Image.fromarray(np.dstack([np.zeros_like(a)] * 3 + [(a * 0.35).astype(np.uint8)]), "RGBA")
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    return (spr, (c, c)), lift, shadow


def glass_overlay(seed):
    """Phản chiếu kính chéo + vết vân tay mờ trên màn hình."""
    rnd = np.random.default_rng(seed + 11)
    yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
    band = np.exp(-(((xx * 0.55 + yy * 0.45) - SW * 0.9) / 160.0) ** 2) * 16
    smudge = np.zeros((SH // 8, SW // 8), np.float32)
    for _ in range(5):
        cx, cy = rnd.uniform(0, SW // 8), rnd.uniform(SH // 16, SH // 8)
        r = rnd.uniform(5, 11)
        y2, x2 = np.mgrid[0:SH // 8, 0:SW // 8]
        smudge += np.exp(-((x2 - cx) ** 2 + (y2 - cy) ** 2) / (2 * r * r)) * rnd.uniform(4, 9)
    smudge = np.asarray(Image.fromarray(smudge).resize((SW, SH), Image.BILINEAR)) * rnd.normal(1, 0.5, (SH, SW))
    a = np.clip(band + smudge, 0, 40).astype(np.uint8)
    return Image.fromarray(np.dstack([np.full((SH, SW), 255, np.uint8)] * 3 + [a]), "RGBA")


def cam_at(t, shots):
    cur = shots[0]
    for s in shots:
        if s[0] <= t:
            cur = s
    p = cur[1]
    ph = p["ph"]
    # rung tay: tổng sin chậm + run nhẹ
    jx = 9 * math.sin(t * 2.1 + ph) + 4 * math.sin(t * 5.3 + ph * 2) + 1.5 * math.sin(t * 17 + ph)
    jy = 11 * math.sin(t * 1.7 + ph * 1.3) + 4 * math.sin(t * 4.7 + ph) + 1.5 * math.sin(t * 19 + ph)
    ja = 0.8 * math.sin(t * 1.3 + ph) + 0.25 * math.sin(t * 6.1 + ph)
    # zoom chậm trong mỗi shot (cảm giác đưa máy lại gần)
    z = 1 + 0.03 * min(1.0, (t - cur[0]) / 2.0)
    return p["scale"] * z, p["dx"] + jx, p["dy"] + jy, p["ang"] + ja


LABELS = {
    "sim": {"vi": "MÔ PHỎNG · KHÔNG PHẢI KẾT QUẢ THẬT", "en": "SIMULATED · NOT REAL RESULTS"},
    "demo": {"vi": "TÀI KHOẢN DEMO", "en": "DEMO ACCOUNT"},
    "real": {"vi": "Không phải lời khuyên đầu tư", "en": "Not financial advice"},
}


def footer(dr, txt):
    f2 = F(24, "Medium")
    tw2 = dr.textlength(txt, font=f2)
    dr.rounded_rectangle(((W - tw2) / 2 - 16, H - 58, (W + tw2) / 2 + 16, H - 20), 12, fill=(0, 0, 0))
    dr.text(((W - tw2) / 2, H - 53), txt, font=f2, fill=(210, 210, 215))


def overlay_label(img, mode, lang):
    dr = ImageDraw.Draw(img)
    txt = LABELS[mode][lang]
    if mode in ("sim", "demo"):          # nhãn nhỏ gọn nhưng luôn đọc được; real: không phủ chữ
        f = F(24, "Bold")
        tw = dr.textlength(txt, font=f)
        x = (W - tw) / 2
        dr.rounded_rectangle((x - 16, 40, x + tw + 16, 80), 10, fill=(0, 0, 0))
        dr.text((x, 47), txt, font=f, fill=(255, 210, 60))


# ---------------------------------------------------------------- render
G = {}


def iphone_rim(size, ox, oy, pw, ph):
    """Khung titan quanh máy + nút bên hông + bóng đổ (thay cho bàn tay)."""
    rim = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(rim)
    for k, col in enumerate([(70, 72, 78), (150, 152, 158), (105, 107, 113)]):
        e = 7 - k * 2
        d.rounded_rectangle((ox - e, oy - e, ox + pw + e, oy + ph + e), 116 + e, fill=col + (255,))
    for y0, y1 in ((0.17, 0.21), (0.25, 0.32), (0.34, 0.41)):       # action, volume +/-
        d.rounded_rectangle((ox - 13, oy + ph * y0, ox - 4, oy + ph * y1), 4, fill=(120, 122, 128, 255))
    d.rounded_rectangle((ox + pw + 4, oy + ph * 0.27, ox + pw + 13, oy + ph * 0.38), 4, fill=(120, 122, 128, 255))
    sh = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((ox + 30, oy + 50, ox + pw + 40, oy + ph + 60), 120, fill=(0, 0, 0, 150))
    return rim, sh.filter(ImageFilter.GaussianBlur(30))


def init_worker(data, tl, lang, use_hand=False):
    G["d"] = data; G["tl"] = tl; G["lang"] = lang; G["use_hand"] = use_hand
    G["dv"] = derive(data)
    G["bg"] = make_background(data.get("seed", 1))
    G["pmask"], G["smask"] = make_phone_mask()
    G["hand"] = hand_layer(SW + 2 * BEZ, SH + 2 * BEZ)
    G["candles"] = candle_series(data)
    rnd = np.random.default_rng(5)
    G["grain"] = [np.concatenate([rnd.normal(0, 6, (H // 2, W // 2, 1)), rnd.normal(0, 2.5, (H // 2, W // 2, 3))], 2)
                  .astype(np.float32) for _ in range(6)]
    G["thumb"], G["thumb_lift"], G["thumb_shadow"] = thumb_sprite()
    _b, _f, _ox, _oy = G["hand"]
    G["rim"], G["pshadow"] = iphone_rim(_b.size, _ox, _oy, SW + 2 * BEZ, SH + 2 * BEZ)
    G["glass"] = glass_overlay(data.get("seed", 1))
    sp = np.full((SH, SW, 3), 0.94, np.float32)
    for c in range(3):
        sp[:, c::3, c] = 1.0
    sp[1::4, :, :] *= 0.985
    G["subpix"] = sp


def scene_at(t, tl):
    for a, b, s in tl["scenes"]:
        if a <= t < b:
            return a, s
    return tl["scenes"][-1][0], tl["scenes"][-1][2]


def draw_thumb(canvas_l, t, tl, ox, oy):
    tx, ty, lift = thumb_state(t, tl["taps"])
    spr, (kx, ky) = G["thumb"]
    sh = G["thumb_shadow"]
    lx, ly = int(ox + BEZ + tx), int(oy + BEZ + ty)
    so = int(8 + 22 * lift)
    tmp = Image.new("RGBA", canvas_l.size, (0, 0, 0, 0))
    tmp.paste(sh, (lx - kx + so, ly - ky + so))
    canvas_l.alpha_composite(tmp)
    tmp = Image.new("RGBA", canvas_l.size, (0, 0, 0, 0))
    tsp = spr if lift < 0.5 else G["thumb_lift"]
    tmp.paste(tsp, (lx - kx, ly - ky))
    canvas_l.alpha_composite(tmp)


def render_frame(fi):
    d, tl, lang, dv = G["d"], G["tl"], G["lang"], G["dv"]
    t = fi / FPS
    st = {"tl": tl, "candles": G["candles"], "clock": d.get("clock", "19:%02d" % (8 + int(t // 8)))}
    t0, sc = scene_at(t, tl)
    if sc == "trade":
        scr, _ = draw_trade(t, d, st, dv, lang)
    elif sc == "chart":
        scr, _ = draw_chart(t, d, st, dv, lang)
    else:
        scr, _ = draw_history(t, d, st, dv, lang, t0)
    # vòng chạm màu (touch indicator)
    sd = ImageDraw.Draw(scr, "RGBA")
    for k, (tt, kind, arg, x, y) in enumerate(tl["taps"]):
        if kind != "flick" and tt <= t < tt + 0.45:
            a = (t - tt) / 0.45
            r = 14 + 26 * a
            col = TAP_COLORS[k % len(TAP_COLORS)]
            sd.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(170 * (1 - a)),))
            sd.ellipse((x - 14, y - 14, x + 14, y + 14), fill=col + (int(230 * (1 - a)),))
    for tt, kind, arg, x, y in tl["taps"]:
        if kind == "close" and tt + 0.1 <= t < tt + 1.1 and sc == "trade":
            u = (t - tt - 0.1) / 1.0
            pr = d["positions"][arg]["profit"]
            txt = ("+$" if pr >= 0 else "−$") + fmt(abs(pr))
            al = int(255 * min(1, 4 * (1 - u)))
            fnt = F(40, "Bold", True)
            sd.text((SW - 60 - sd.textlength(txt, font=fnt), y - 40 - 90 * u), txt, font=fnt,
                    fill=(BLUE if pr >= 0 else RED) + (al,))
    a_scr = np.asarray(scr, np.float32) * G["subpix"]
    scr = Image.fromarray(a_scr.clip(0, 255).astype(np.uint8)).convert("RGBA")
    scr.alpha_composite(G["glass"])
    # điện thoại
    pw, ph = SW + 2 * BEZ, SH + 2 * BEZ
    phone = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    body = Image.new("RGBA", (pw, ph), (18, 18, 22, 255))
    phone.paste(body, (0, 0), G["pmask"])
    phone.paste(scr, (BEZ, BEZ), G["smask"])
    back, front, ox, oy = G["hand"]
    canvas_l = Image.new("RGBA", back.size, (0, 0, 0, 0))
    if G["use_hand"]:
        canvas_l.alpha_composite(back)
    else:
        canvas_l.alpha_composite(G["pshadow"])
    canvas_l.alpha_composite(G["rim"])
    canvas_l.alpha_composite(phone, (ox, oy))
    if G["use_hand"]:
        canvas_l.alpha_composite(front)
        draw_thumb(canvas_l, t, tl, ox, oy)
    scale, dx, dy, ang = cam_at(t, tl["shots"])
    s = scale * W / pw
    lay = canvas_l.resize((int(canvas_l.width * s), int(canvas_l.height * s)), Image.BILINEAR)
    lay = lay.rotate(ang, resample=Image.BILINEAR, expand=True)
    frame = G["bg"].copy().convert("RGBA")
    # quầng sáng màn hình
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx, cy = W / 2 + dx, H / 2 + dy
    gd = ImageDraw.Draw(glow)
    gw, gh = pw * s * 0.65, ph * s * 0.6
    gd.ellipse((cx - gw, cy - gh, cx + gw, cy + gh), fill=(200, 205, 230, 40))
    glow = glow.resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
    frame.alpha_composite(glow)
    frame.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))
    img = frame.convert("RGB")
    # bloom nhẹ (màn hình hơi cháy sáng như quay bằng máy thứ hai)
    small = img.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)
    a = np.asarray(img, np.int16)
    b = np.asarray(small, np.int16)
    out = a + (b * 0.22).astype(np.int16)
    # nhiễu cảm biến: mạnh ở vùng tối, có nhiễu màu
    lum = out.mean(axis=2, keepdims=True)
    gr = np.repeat(np.repeat(G["grain"][fi % 6], 2, 0), 2, 1)
    out = out + gr[..., :1] * (1.5 - np.clip(lum, 0, 255) / 200.0) + gr[..., 1:]
    # quang sai màu nhẹ
    out[..., 0] = np.roll(out[..., 0], 1, axis=1)
    out[..., 2] = np.roll(out[..., 2], -1, axis=1)
    img = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    # lấy nét lại sau mỗi lần cắt cảnh + độ mềm của việc quay màn hình
    ts = max(s0 for s0, _ in tl["shots"] if s0 <= t)
    blur = 0.7 + (2.0 * math.exp(-(t - ts) / 0.13) if ts > 0 else 0)
    img = img.filter(ImageFilter.GaussianBlur(blur))
    overlay_label(img, d["mode"], lang)
    return img.tobytes()


# ---------------------------------------------------------------- âm thanh
def synth_audio(tl, path, bpm=92.0, sr=44100):
    dur = tl["dur"]
    n = int(dur * sr)
    t = np.arange(n) / sr
    out = np.zeros(n)
    beat = 60 / bpm
    def env(L, a=0.005, r=0.3):
        x = np.arange(L) / sr
        return np.minimum(1, x / a) * np.exp(-x / r)
    # hợp âm lo-fi (Fmaj7 - Em7 - Dm7 - Cmaj7)
    chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
    bar = beat * 4
    for bi in range(int(dur / bar) + 1):
        ch = chords[bi % 4]
        s = int(bi * bar * sr); L = min(int(bar * sr), n - s)
        if L <= 0:
            break
        x = np.arange(L) / sr
        e = np.minimum(1, x / 0.08) * np.exp(-x / 2.2)
        for m in ch:
            f = 440 * 2 ** ((m - 69) / 12)
            out[s:s + L] += 0.05 * e * (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(4 * np.pi * f * x) * np.exp(-x / 0.4))
        fb = 440 * 2 ** ((ch[0] - 12 - 69) / 12)
        out[s:s + L] += 0.10 * np.exp(-x / 1.2) * np.sin(2 * np.pi * fb * x)
    rnd = np.random.default_rng(1)
    for k in range(int(dur / beat) + 1):
        s = int(k * beat * sr)
        if s >= n:
            break
        if k % 2 == 0:  # kick mềm
            L = min(int(0.35 * sr), n - s); x = np.arange(L) / sr
            out[s:s + L] += 0.35 * np.exp(-x / 0.12) * np.sin(2 * np.pi * (50 + 60 * np.exp(-x / 0.03)) * x)
        else:           # snap
            L = min(int(0.15 * sr), n - s)
            out[s:s + L] += 0.10 * env(L, 0.001, 0.04) * rnd.normal(0, 1, L)
        for hh in (0, 0.5):  # hi-hat
            s2 = int((k + hh) * beat * sr); L = min(int(0.05 * sr), n - s2)
            if L > 0:
                out[s2:s2 + L] += 0.03 * env(L, 0.0005, 0.012) * rnd.normal(0, 1, L)
    # tiếng chạm + "ting" khi đóng lệnh có lãi
    room = np.convolve(rnd.normal(0, 1, n), np.ones(40) / 40, "same")
    out += 0.012 * room / (np.abs(room).max() + 1e-9) * 3
    for tt, kind, *_ in tl["taps"]:
        s = int(tt * sr)
        if s >= n:
            continue
        L = min(int(0.04 * sr), n - s)
        out[s:s + L] += 0.25 * env(L, 0.0003, 0.006) * rnd.normal(0, 1, L)
        if kind == "close":
            s2 = int((tt + 0.35) * sr); L = min(int(0.6 * sr), n - s2)
            if L > 0:
                x = np.arange(L) / sr
                out[s2:s2 + L] += 0.12 * np.exp(-x / 0.18) * (np.sin(2 * np.pi * 1568 * x) + 0.6 * np.sin(2 * np.pi * 2093 * x))
    # fade
    f = int(0.6 * sr); out[-f:] *= np.linspace(1, 0, f)
    out = out / (np.abs(out).max() + 1e-9) * 0.89  # ~ -1 dBFS
    st = np.stack([out, out], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def render(data, out, dur, keys=None, keydir=None, audio=True, lang="en", workers=None, hand=False):
    tl = build_timeline(data, dur)
    if keys:
        init_worker(data, tl, lang, hand)
        os.makedirs(keydir, exist_ok=True)
        for k in keys:
            b = render_frame(int(k * FPS))
            p = os.path.join(keydir, f"key_{k:05.2f}.png")
            Image.frombytes("RGB", (W, H), b).save(p)
            print(p)
        return
    nf = int(dur * FPS)
    silent = out + ".silent.part.mp4"
    ff = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                           "-crf", "19", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    with Pool(workers or os.cpu_count(), initializer=init_worker, initargs=(data, tl, lang, hand)) as pool:
        for i, b in enumerate(pool.imap(render_frame, range(nf), chunksize=4)):
            ff.stdin.write(b)
            if i % 90 == 0:
                print(f"frame {i}/{nf}", flush=True)
    ff.stdin.close(); ff.wait()
    if audio:
        wav = out + ".music.wav"
        synth_audio(tl, wav)
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v",
                        "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".part.mp4"],
                       check=True)
        os.remove(silent); os.remove(wav)
        os.replace(out + ".part.mp4", out)
    else:
        os.replace(silent, out)
    print("done", out)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("sim"); a.add_argument("--seed", type=int, default=7); a.add_argument("--n", type=int, default=10)
    a.add_argument("--start", type=float, default=100000); a.add_argument("--out", required=True)
    c = sub.add_parser("check"); c.add_argument("data")
    r = sub.add_parser("render"); r.add_argument("data"); r.add_argument("out")
    r.add_argument("--dur", type=float, default=24.0); r.add_argument("--keys", type=float, nargs="*")
    r.add_argument("--keydir", default="keys"); r.add_argument("--no-audio", action="store_true")
    r.add_argument("--lang", default="en", choices=["vi", "en"]); r.add_argument("--workers", type=int)
    r.add_argument("--hand", action="store_true", help="vẽ tay cầm máy + ngón cái (mặc định tắt)")
    ar = ap.parse_args()
    if ar.cmd == "sim":
        d = make_sim(ar.seed, ar.n, ar.start)
        json.dump(d, open(ar.out, "w"), indent=1, ensure_ascii=False)
        print("\n".join(check(d)))
    elif ar.cmd == "check":
        d = json.load(open(ar.data))
        print("\n".join(check(d)))
    else:
        d = json.load(open(ar.data))
        for m in check(d):
            print(m)
        render(d, ar.out, ar.dur, ar.keys, ar.keydir, not ar.no_audio, ar.lang, ar.workers, ar.hand)


if __name__ == "__main__":
    main()
