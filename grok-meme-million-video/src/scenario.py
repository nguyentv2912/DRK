#!/usr/bin/env python3
"""GROK MEME MILLION V1.8.3 - concept trade scenario + video timeline.

All money is integer cents so equity, P&L, ROI and multiples are exact sums.
Hero-token trades are priced from REAL candles of the hero pool (entry/exit =
candle close). Other trades are CONCEPT results (seeded random) on real,
verified watchlist tokens. Everything is labelled CONCEPT TRADES on screen.
"""
import json, os, random, sys, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Event slots (seconds) from the 15 s storyboard, QUANTIZED to the 1/8-note
# grid of the 128 BPM soundtrack so every trade lands on a beat (V1.8.4).
BPM = 128
EIGHTH = 60 / BPM / 2


def q(t):
    return round(round(t / EIGHTH) * EIGHTH, 6)


T_HIST_BANNER = q(1.25)   # portfolio: SELL banner (token A)
T_HERO_BUY = q(3.35)      # live: BUY hero (chart marker)
T_HERO_TP = q(4.75)       # live: SELL 50% hero (chart marker)
T_B_BUY = q(5.6)          # live: BUY token B (feed)
T_B_STOP = q(6.95)        # execution: STOP token B (negative, red banner)
T_HERO_EXIT = q(7.65)     # execution: SELL rest hero (chart marker)
T_C_SELL = q(8.45)        # execution: SELL token C (banner)
T_D_SELL = q(10.35)       # agents/activity: SELL token D (feed row)
T_E_BUY = q(11.25)        # agents/activity: BUY token E (feed row)
T_E_SELL = q(12.6)        # finale: SELL token E -> final equity reveal (drop)
REVEAL_START, REVEAL_END = 2.5, 9.0
WINDOW = 72            # candles visible in the terminal
PRE_REVEALED = 30      # candles already drawn when the live screen opens


def cents(x):
    return int(round(x * 100))


def pick_hero_trades(candles, rng=None, return_score=False):
    """Find a window + BUY/TP/EXIT candle indices on REAL candles.
    Entry/exit prices are the real candle closes; nothing is invented.
    Returns (window_start, pre_revealed, buy_idx, tp_idx, exit_idx)."""
    n = len(candles)
    best = None
    for s in range(0, max(1, n - WINDOW + 1)):
        cl = [c["c"] for c in candles[s:s + WINDOW]]
        for pre in range(18, 37, 2):
            for ib in range(pre + 2, pre + 10):
                for i1 in range(ib + 5, ib + 15):
                    for i2 in range(i1 + 6, min(WINDOW - 4, i1 + 24)):
                        g1, g2 = cl[i1] / cl[ib] - 1, cl[i2] / cl[ib] - 1
                        if not (0.10 <= g1 <= 3.0 and g2 >= 0.08):
                            continue
                        sc = min(g1, 1.2) + 0.6 * min(g2, 1.5) - 0.02 * abs(pre - 28)
                        if best is None or sc > best[0]:
                            best = (sc, s, pre, ib, i1, i2)
    if best is None:  # no rally in the data: still real prices, result may be a loss
        s = max(0, n - WINDOW); pre = 28; ib = pre + 4
        best = (-1.0, s, pre, ib, ib + 10, ib + 25)
    return best if return_score else best[1:]


def hm(ts):
    d = dt.datetime.fromtimestamp(ts, dt.timezone.utc)
    return d.strftime("%-I:%M %p")


def build(seed=None):
    cfg = json.load(open(os.path.join(ROOT, "config.json")))
    snap = json.load(open(os.path.join(ROOT, "data", "market_snapshot.json")))
    sc = cfg["scenario"]
    if seed is None:
        seed = cfg.get("seed")
    if seed is None:
        seed = random.SystemRandom().randrange(1, 10**6)
    rng = random.Random(seed)
    watch = snap["watchlist"]
    ohlcv = snap["hero_ohlcv"]
    real_chart = ohlcv.get("status") == "verified"
    hero_sym = ohlcv["symbol"] if real_chart else "CONCEPT"
    others = [w for w in watch if w["mint"] != ohlcv.get("mint")]
    rng.shuffle(others)
    tokA, tokB, tokC, tokD, tokE = (others * 3)[:5]
    hero_tok = next((w for w in watch if w["mint"] == ohlcv.get("mint")), None)

    if real_chart:
        candles = ohlcv["candles"]
    else:  # concept chart: clearly labelled, deterministic random walk
        p, candles = 1.0, []
        for i in range(WINDOW + 10):
            o = p; p *= 1 + rng.gauss(0.004, 0.03)
            candles.append({"t": 1_700_000_000 + 300 * i, "o": o, "h": max(o, p) * (1 + abs(rng.gauss(0, .01))),
                            "l": min(o, p) * (1 - abs(rng.gauss(0, .01))), "c": p, "v": rng.uniform(1e3, 5e4)})
    ws, pre, ib, i1, i2 = pick_hero_trades(candles, rng)
    win = candles[ws:ws + WINDOW]
    pb, p1, p2 = win[ib]["c"], win[i1]["c"], win[i2]["c"]
    now_price = candles[-1]["c"]
    fdv = (hero_tok or {}).get("fdv_usd") or 0

    def mc_at(price):
        return fdv * price / now_price if fdv and real_chart else None

    t0 = win[0]["t"]
    L = cfg["trade_limits"]
    WMIN, WMAX = cents(L["win_usd"][0]), cents(L["win_usd"][1])
    LMIN, LMAX = cents(L["loss_usd"][0]), cents(L["loss_usd"][1])
    g1, g2 = p1 / pb - 1, p2 / pb - 1

    def size_range(pnl, eq):
        """Sizes for which pct = pnl/size is allowed and size <= max frac of equity."""
        lo_f, hi_f = 0.08 * eq, L["max_size_frac_of_equity"] * eq
        if pnl >= 0:
            lo, hi = pnl / L["win_pct"][1], pnl / L["win_pct"][0]
        else:
            lo, hi = -pnl / -L["loss_pct"][0], -pnl / -L["loss_pct"][1]
        return max(lo, lo_f), min(hi, hi_f)

    def water_fill(total, weights, lo, hi):
        """Split `total` cents by weights, clipped to [lo, hi] per slot (iterative)."""
        n = len(weights)
        if total < n * lo or total > n * hi:
            return None
        out = [None] * n
        free = list(range(n))
        rem = total
        for _ in range(30):
            ws_ = sum(weights[i] for i in free)
            changed = False
            for i in list(free):
                v = rem * weights[i] / ws_
                if v > hi or v < lo:
                    out[i] = hi if v > hi else lo
                    free.remove(i); rem -= out[i]; changed = True
            if not changed:
                break
        ws_ = sum(weights[i] for i in free) or 1
        for i in free:
            out[i] = rem * weights[i] / ws_
        out = [int(round(v)) for v in out]
        diff = total - sum(out)
        order = sorted(range(n), key=lambda i: -out[i])
        for i in order:  # put rounding cents where they fit
            if diff == 0:
                break
            room = (hi - out[i]) if diff > 0 else (out[i] - lo)
            d = max(-room, min(room, diff))
            out[i] += d; diff -= d
        return out if diff == 0 else None

    for attempt in range(50000):
        cap = cents(rng.uniform(*sc["initial_capital_range"]))
        target = cents(rng.uniform(*sc["final_profit_range"]))
        share_cap = int(L["max_share_of_total"] * target)
        hi_w = min(WMAX, share_cap)
        n_hist = rng.randint(3, 8)
        # slot plan in chronological order: hist..., A, H1, B(loss), H2, C, D, E
        hist_loss = rng.randrange(n_hist) if rng.random() < 0.35 else -1
        plan = [("hist", k == hist_loss) for k in range(n_hist)] + [("A", False), ("H1", None), ("B", True), ("H2", None), ("C", False), ("D", False), ("E", False)]
        losses = {i: rng.randint(LMIN, min(LMAX, int(target * .08))) for i, (_, lo_) in enumerate(plan) if lo_}
        # hero size: target a mid-size position, capped so each half stays within limits
        eq_est = cap + target * (n_hist + 1) / (n_hist + 7)
        hs = cents(eq_est / 100 * rng.uniform(0.22, 0.40))
        half_max = min(hi_w / g1 if g1 > 0 else 1e12, hi_w / g2 if g2 > 0 else 1e12)
        half = int(min(hs / 2, half_max))
        hp1, hp2 = int(round(half * g1)), int(round(half * g2))
        if not all(WMIN <= v <= hi_w for v in (hp1, hp2)):
            continue
        win_slots = [i for i, (_, lo_) in enumerate(plan) if lo_ is False]
        need = target + sum(losses.values()) - hp1 - hp2
        wts = [rng.gammavariate(2.0, 1.0) for _ in win_slots]
        wts[-1] *= 2.2  # finale (E) is the biggest win
        alloc = water_fill(need, wts, WMIN, hi_w)
        if alloc is None:
            continue
        # make sure E is the largest win
        iE = len(alloc) - 1
        j = max(range(len(alloc)), key=lambda i: alloc[i])
        alloc[iE], alloc[j] = alloc[j], alloc[iE]
        pnl_plan = {}
        for i, v in zip(win_slots, alloc):
            pnl_plan[i] = v
        for i, v in losses.items():
            pnl_plan[i] = -v
        # simulate sequentially: choose sizes inside the allowed ranges
        trades, eq, ok = [], cap, True
        hero_buy = None
        times = {"A": (t0 + 300 * 4, T_HIST_BANNER), "C": (win[min(i2 + 2, WINDOW - 1)]["t"] + 600, T_C_SELL),
                 "D": (win[-1]["t"] + 1500, T_D_SELL), "E": (win[-1]["t"] + 3900, T_E_SELL)}
        toks = {"A": tokA, "B": tokB, "C": tokC, "D": tokD, "E": tokE}
        bB = eE = None
        hk = 0
        for i, (slot, _) in enumerate(plan):
            if slot in ("H1", "H2"):
                if slot == "H1":
                    if half * 2 > L["max_size_frac_of_equity"] * eq or half * 2 < 0.08 * eq:
                        ok = False; break
                    hero_buy = {"symbol": hero_sym, "mint": ohlcv.get("mint"), "size_c": half * 2, "price": pb, "time": win[ib]["t"],
                                "t_video": T_HERO_BUY, "idx": ib, "mc": mc_at(pb)}
                    pnl, idx, pr, lab, kind, part, tv = hp1, i1, p1, "take profit 50%", "tp", "50%", T_HERO_TP
                else:
                    pnl, idx, pr, lab, kind, part, tv = hp2, i2, p2, "trail 40%", "trail", "", T_HERO_EXIT
                r = {"symbol": hero_sym, "mint": ohlcv.get("mint"), "size_c": half, "pnl_c": pnl, "kind": kind, "label": lab,
                     "agent": "Executor", "time": win[idx]["t"], "t_video": tv, "equity_before_c": eq,
                     "idx": idx, "price": pr, "mc": mc_at(pr), "hero": True, "partial": part}
            else:
                pnl = pnl_plan[i]
                lo, hi = size_range(pnl, eq)
                if lo > hi:
                    ok = False; break
                size = int(rng.uniform(lo, hi))
                size = max(int(lo) + 1, min(int(hi), size))
                if slot == "hist":
                    tok = others[hk % len(others)]; hk += 1
                    when, tv = t0 - 300 * (n_hist - i) * 6 - 600, None
                else:
                    tok = toks[slot]; when, tv = times[slot] if slot != "B" else (win[min(i1 + 8, WINDOW - 1)]["t"], T_B_STOP)
                if pnl < 0:
                    kind, lab = "stop", f"-{round(-pnl / size * 100)}% stop"
                else:
                    kind = "tp"
                    lab = "take profit 100%" if slot == "E" else rng.choice(["take profit 50%", "trail 40%"])
                r = {"symbol": tok["symbol"], "mint": tok["mint"], "size_c": size, "pnl_c": pnl, "kind": kind, "label": lab,
                     "agent": "Risk" if pnl < 0 else "Executor", "time": when, "t_video": tv, "equity_before_c": eq}
                if slot == "B":
                    bB = {"tok": tok, "size_c": size, "time": win[min(i1 + 3, WINDOW - 1)]["t"], "t_video": T_B_BUY}
                if slot == "E":
                    eE = {"tok": tok, "size_c": size, "time": win[-1]["t"] + 2400, "t_video": T_E_BUY}
            eq += r["pnl_c"]
            r["equity_after_c"] = eq
            trades.append(r)
        if not ok or eq - cap != target:
            continue
        hs = half * 2
        break
    else:
        sys.exit("scenario: could not satisfy trade limits")
    for t in trades:
        t["pct"] = t["pnl_c"] / t["size_c"]
    buys = [dict(hero_buy, kind="buy"),
            {"symbol": bB["tok"]["symbol"], "mint": bB["tok"]["mint"], "size_c": bB["size_c"], "time": bB["time"], "t_video": T_B_BUY, "kind": "buy"},
            {"symbol": eE["tok"]["symbol"], "mint": eE["tok"]["mint"], "size_c": eE["size_c"], "time": eE["time"], "t_video": T_E_BUY, "kind": "buy"}]
    final_c = eq
    out = {
        "seed": seed, "label": sc["label"], "real_chart": real_chart,
        "initial_capital_c": cap, "final_equity_c": final_c, "total_pnl_c": final_c - cap,
        "roi_pct": (final_c - cap) / cap * 100, "multiple": final_c / cap,
        "hero": {"symbol": hero_sym, "mint": ohlcv.get("mint"), "pool": ohlcv.get("pool"),
                 "dex": (hero_tok or {}).get("dex"), "pair": (hero_tok or {}).get("pair"),
                 "window_start": ws, "candles": win, "buy_idx": ib, "tp_idx": i1, "exit_idx": i2,
                 "buy_size_c": hs, "fdv_usd": fdv, "now_price": now_price,
                 "h24": (hero_tok or {}).get("price_change_h24"), "vol24": (hero_tok or {}).get("volume_h24"),
                 "liq": (hero_tok or {}).get("liquidity_usd")},
        "trades": trades, "buys": buys,
        "reveal": {"start": REVEAL_START, "end": REVEAL_END, "pre": pre,
                   "anchors": [[REVEAL_START, pre - 1], [T_HERO_BUY, ib], [T_HERO_TP, i1], [T_HERO_EXIT, i2], [REVEAL_END, WINDOW - 1]]},
        "snapshot_at": snap["snapshot_finished_at"],
    }
    # math audit (re-derived independently)
    s = cap
    for t in trades:
        assert t["equity_before_c"] == s, "equity chain broken"
        s += t["pnl_c"]
        assert t["equity_after_c"] == s
    assert s == final_c and final_c - cap == out["total_pnl_c"]
    return out


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    sc = build(seed)
    p = os.path.join(ROOT, "data", "scenario.json")
    json.dump(sc, open(p, "w"), indent=1)
    print("seed", sc["seed"], "capital $%.2f" % (sc["initial_capital_c"] / 100), "final $%.2f" % (sc["final_equity_c"] / 100),
          "pnl $%.2f" % (sc["total_pnl_c"] / 100), "roi %.1f%%" % sc["roi_pct"], "x%.2f" % sc["multiple"])
    for t in sc["trades"]:
        print(f"  {t['t_video']!s:>5} {t['symbol']:<8} size ${t['size_c']/100:8.2f} pnl ${t['pnl_c']/100:8.2f} {t['pct']*100:7.1f}% eq ${t['equity_after_c']/100:.2f}")
