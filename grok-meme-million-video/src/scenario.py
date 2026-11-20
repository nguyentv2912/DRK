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

# Fixed event slots (seconds) derived from the 15 s storyboard.
T_HIST_BANNER = 1.25   # portfolio: SELL banner (token A)
T_HERO_BUY = 3.35      # live: BUY hero (chart marker)
T_HERO_TP = 4.75       # live: SELL 50% hero (chart marker)
T_B_BUY = 5.6          # live: BUY token B (feed)
T_B_STOP = 6.95        # execution: STOP token B (negative, red banner)
T_HERO_EXIT = 7.65     # execution: SELL rest hero (chart marker)
T_C_SELL = 8.45        # execution: SELL token C (banner)
T_D_SELL = 10.35       # agents/activity: SELL token D (feed row)
T_E_BUY = 11.25        # agents/activity: BUY token E (feed row)
T_E_SELL = 12.55       # finale: SELL token E -> final equity reveal
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
                        if not (0.10 <= g1 <= 3.0 and g2 >= 0.04):
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
    for attempt in range(20000):
        cap = cents(rng.uniform(*sc["initial_capital_range"]))
        target = cents(rng.uniform(*sc["final_profit_range"]))
        n_hist = rng.randint(3, 5)
        trades = []  # closed results in chronological order
        eq = cap

        def add(tok, size_c, pct, kind, label, when, agent="Executor", t_video=None, extra=None):
            nonlocal eq
            pnl = int(round(size_c * pct))
            r = {"symbol": tok["symbol"] if tok else hero_sym, "mint": tok["mint"] if tok else None,
                 "size_c": size_c, "pnl_c": pnl, "pct": pnl / size_c, "kind": kind, "label": label,
                 "agent": agent, "time": when, "t_video": t_video, "equity_before_c": eq}
            if extra:
                r.update(extra)
            eq += pnl
            r["equity_after_c"] = eq
            trades.append(r)
            return r

        # history (before the video starts) - modest, mixed results
        hist_budget = target * rng.uniform(0.10, 0.22)
        ok = True
        for k in range(n_hist):
            tok = others[k % len(others)]
            size = cents(eq / 100 * rng.uniform(*sc["trade_size_frac_range"]) / 1) // 1
            if rng.random() < sc["loss_probability"]:
                pct = rng.uniform(*sc["loss_pct_range"]); kind = "stop"; lab = f"-{abs(round(pct*100))}% stop"
            else:
                pct = min(rng.uniform(*sc["win_pct_range"]), hist_budget / max(size, 1) / max(1, n_hist - k) * 1.6)
                pct = max(pct, 0.08); kind = "tp"; lab = rng.choice(["take profit 50%", "trail 40%"])
            add(tok, size, pct, kind, lab, t0 - 300 * (n_hist - k) * 6 - 600)
        # A: sell during portfolio
        sA = cents(eq / 100 * rng.uniform(0.15, 0.3))
        add(tokA, sA, rng.uniform(0.35, 1.2), "tp", "trail 40%", t0 + 300 * 4, t_video=T_HIST_BANNER)
        # hero BUY -> TP 50% -> exit rest (REAL prices)
        hs = cents(eq / 100 * sc["hero_trade_size_frac"])
        half = hs // 2
        hero_buy = {"symbol": hero_sym, "size_c": hs, "price": pb, "time": win[ib]["t"], "t_video": T_HERO_BUY,
                    "idx": ib, "mc": mc_at(pb)}
        add(hero_tok, half, p1 / pb - 1, "tp", "take profit 50%", win[i1]["t"], t_video=T_HERO_TP,
            extra={"idx": i1, "price": p1, "mc": mc_at(p1), "hero": True, "partial": "50%"})
        bB = {"tok": tokB, "size_c": cents(eq / 100 * rng.uniform(0.15, 0.25)), "time": win[min(i1 + 3, WINDOW - 1)]["t"], "t_video": T_B_BUY}
        add(tokB, bB["size_c"], rng.uniform(-0.38, -0.18), "stop", "-25% stop", win[min(i1 + 8, WINDOW - 1)]["t"],
            agent="Risk", t_video=T_B_STOP)
        add(hero_tok, hs - half, p2 / pb - 1, "trail", "trail 40%", win[i2]["t"], t_video=T_HERO_EXIT,
            extra={"idx": i2, "price": p2, "mc": mc_at(p2), "hero": True, "partial": ""})
        add(tokC, cents(eq / 100 * rng.uniform(0.18, 0.32)), rng.uniform(0.4, 1.6), "tp", "take profit 50%",
            win[min(i2 + 2, WINDOW - 1)]["t"] + 600, t_video=T_C_SELL)
        add(tokD, cents(eq / 100 * rng.uniform(0.2, 0.34)), rng.uniform(0.5, 1.8), "trail", "trail 40%",
            win[-1]["t"] + 1500, t_video=T_D_SELL)
        # E: final trade absorbs the residual so total profit == target exactly
        resid = target - (eq - cap)
        sE = cents(eq / 100 * rng.uniform(0.28, 0.45))
        if not (15000 <= resid <= 0.5 * target and sE > 0 and 0.4 <= resid / sE <= 3.5):
            continue
        eE = {"tok": tokE, "size_c": sE, "time": win[-1]["t"] + 2400, "t_video": T_E_BUY}
        add(tokE, sE, resid / sE, "tp", "take profit 100%", win[-1]["t"] + 3900, t_video=T_E_SELL)
        trades[-1]["pnl_c"] = resid  # exact (pct recomputed below)
        trades[-1]["equity_after_c"] = trades[-1]["equity_before_c"] + resid
        eq = trades[-1]["equity_after_c"]
        # sanity: all non-final trade results "tens to hundreds"
        if any(abs(t["pnl_c"]) < 800 or abs(t["pnl_c"]) > 150000 for t in trades):
            continue
        if eq - cap != target:
            continue
        break
    else:
        sys.exit("scenario: could not satisfy constraints")
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
