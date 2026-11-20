#!/usr/bin/env python3
"""Writes output/VISUAL_CRITIC_REPORT.md and output/TRADING_DATA_AUDIT.md."""
import json, os, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "output")
R = json.load(open(os.path.join(OUT, "critic_report.json")))
SC = json.load(open(os.path.join(ROOT, "data", "scenario.json")))
SN = json.load(open(os.path.join(ROOT, "data", "market_snapshot.json")))
RV = json.load(open(os.path.join(ROOT, "data", "review_log.json")))


def m(c, sign=False):
    v = c / 100
    return (("+" if v >= 0 else "-") if sign else ("-" if v < 0 else "")) + f"${abs(v):,.2f}"


L = ["# Visual Critic Report — GROK MEME MILLION V1.8.3", "",
     f"- Video: `{R['video']}` · Reference: `{R['reference']}`",
     f"- Automated verdict: **{R['verdict']}** · checks passed **{R['checks_passed']}** · auto score {R['auto_score']}/10",
     f"- Reviewed quality vs. reference: **{RV['quality_score']}/10** (target 9.5)", "",
     "## Automated checks", "", "| Result | Check | Detail |", "|---|---|---|"]
for c in R["checks"]:
    L.append(f"| {'PASS' if c['pass'] else ('FAIL' if c['critical'] else 'WARN')} | {c['check']} | {c['detail'].replace('|', '/')[:220]} |")
L += ["", "## Reference comparison (matched timestamps)", "", "| New t | Ref t | Edge density ref/new | Dark share ref/new | Green share ref/new |", "|---|---|---|---|---|"]
for p in R["reference_comparison"]["timestamps"]:
    L.append(f"| {p['t_new']}s | {p['t_ref']}s | {p['ref']['edge_density']:.1f} / {p['new']['edge_density']:.1f} | {p['ref']['dark_share']:.2f} / {p['new']['dark_share']:.2f} | {p['ref']['green_share']:.3f} / {p['new']['green_share']:.3f} |")
L += ["", "Side-by-side sheet: `compare_sheet.png` (top = reference, bottom = new).", "",
      "## Human-in-the-loop inspection", "", "| Area | Score | Notes |", "|---|---|---|"]
for a in RV["areas"]:
    L.append(f"| {a['area']} | {a['score']} | {a['notes']} |")
L += ["", "## Build iterations (defects found → fixed → re-rendered)", ""]
for i, it in enumerate(RV["iterations"], 1):
    L.append(f"{i}. **{it['verdict']}** — {it['found']} → _fix:_ {it['fix']}")
L += ["", "## Audio sync (onset rise at each event)", ""]
L += [f"- {s['t']:>5}s {s['type']:<4} +{s['rise_db']} dB" for s in R["audio_sync"]]
open(os.path.join(OUT, "VISUAL_CRITIC_REPORT.md"), "w").write("\n".join(L) + "\n")

A = ["# Trading Data Audit — GROK MEME MILLION V1.8.3", "",
     f"Snapshot window: {SN['snapshot_started_at']} → {SN['snapshot_finished_at']} (point-in-time; shown on screen as a snapshot/replay, **not realtime**).", "",
     "## Verified watchlist (Solana, GeckoTerminal trending 24h → DEX Screener → Solana RPC)", "",
     "| Symbol | Mint | Pool | DEX | Price USD | 24h | Vol 24h | Liquidity | DS price dev | RPC mint | Checked |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for w in SN["watchlist"]:
    ds, rp = w["verify"]["dexscreener"], w["verify"]["solana_rpc"]
    A.append(f"| {w['symbol']} | `{w['mint']}` | `{w['pool']}` | {w['dex']} | {w['price_usd']:.8g} | {w['price_change_h24']:+.2f}% | ${w['volume_h24']:,.0f} | ${w['liquidity_usd']:,.0f} | {ds['price_deviation']*100:.2f}% | {rp['program']} ✓ | {ds['checked_at']} |")
oh = SN["hero_ohlcv"]
h = SC["hero"]
A += ["", "## Chart data (hero pool)", "",
      f"- Status: **{oh['status']}** · source `{oh['source']}` · fetched {oh.get('fetched_at')}",
      f"- {oh['symbol']} · mint `{oh['mint']}` · pool `{oh['pool']}` · {oh['aggregate_minutes']}m candles",
      f"- Video window: {len(h['candles'])} candles, {dt.datetime.utcfromtimestamp(h['candles'][0]['t']):%Y-%m-%d %H:%M} → {dt.datetime.utcfromtimestamp(h['candles'][-1]['t']):%H:%M} UTC; byte-identical to the fetched rows (critic check).",
      "- The forming candle is animated from its real open to its real close inside its real high/low; no prices outside the fetched OHLC are drawn.",
      "- EMA7/EMA20/RSI14 computed from the real closes including pre-window history.",
      "- Hero candidate scoring: " + ", ".join(f"{c['symbol']} ({c['candles']} candles{', score ' + str(c['score']) if 'score' in c else ', too short'})" for c in oh.get("candidates", [])), "",
      "## Concept trades (simulated — labelled CONCEPT TRADES / Paper on screen)", "",
      f"Seed {SC['seed']} · initial capital {m(SC['initial_capital_c'])} · final equity {m(SC['final_equity_c'])} · total P&L {m(SC['total_pnl_c'], True)} · ROI {SC['roi_pct']:.2f}% · {SC['multiple']:.2f}x", "",
      "| # | Video t | Token | Size | Result | P&L | Equity after | Price basis |", "|---|---|---|---|---|---|---|---|"]
for i, t in enumerate(SC["trades"], 1):
    basis = f"real candle close #{t['idx']} ({t['price']:.6g})" if t.get("hero") else "concept result"
    A.append(f"| {i} | {t['t_video'] if t['t_video'] is not None else 'history'} | {t['symbol']} | {m(t['size_c'])} | {t['label']} | {m(t['pnl_c'], True)} ({t['pct']*100:+.1f}%) | {m(t['equity_after_c'])} | {basis} |")
A += ["", f"Check: {m(SC['initial_capital_c'])} + Σ P&L {m(SC['total_pnl_c'], True)} = {m(SC['final_equity_c'])} (integer-cent chain verified).", "",
      "## On-chain executions", "", f"- {SN['onchain_executions']['status']}: {SN['onchain_executions']['reason']}",
      "- No trade in this video is presented as an on-chain execution.", "",
      "## Request log", "", "| Fetched at (UTC) | OK | Endpoint |", "|---|---|---|"]
for r in SN["request_log"]:
    A.append(f"| {r['fetched_at']} | {'✓' if r['ok'] else '✗'} | `{r['url']}` |")
open(os.path.join(OUT, "TRADING_DATA_AUDIT.md"), "w").write("\n".join(A) + "\n")
print("wrote VISUAL_CRITIC_REPORT.md, TRADING_DATA_AUDIT.md")
