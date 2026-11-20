---
description: Build a new GROK × MEME COIN — ROAD TO $1M video (skill grok-meme-million-video) from fresh verified Solana trending data
argument-hint: "[seed] [offline] [ref=<path to reference.mp4>]"
---

Run the **grok-meme-million-video** skill (folder `grok-meme-million-video/`, read its `SKILL.md` first and follow it exactly).

Arguments: `$ARGUMENTS`
- a number → use it as the scenario seed (same numbers again); none → random seed
- `offline` → reuse `data/market_snapshot.json` instead of scanning fresh data
- `ref=<path>` → reference video for the Visual Critic; if absent, use the reference video from earlier in the conversation or ask the user for it

Steps:
1. Unless `offline`: run `python3 src/fetch_data.py` to scan the latest Solana meme-token trending data (GeckoTerminal → DEX Screener → Solana RPC, verified by mint + pool) and the hero pool's real OHLCV.
2. Run `./build.sh <ref> [seed] --offline` from `grok-meme-million-video/` (data already fetched in step 1).
3. If the critic rejects, fix the defects and re-render until it is ACCEPTED.
4. Inspect stills by eye at ≥ 7 timestamps against the reference; fix anything the critic missed, re-render, and log it in `data/review_log.json`.
5. Copy the deliverables into `deliverables/run_<date>_<HERO>/` (MP4, previews, contact sheet, compare sheet, VISUAL_CRITIC_REPORT.md, TRADING_DATA_AUDIT.md) and refresh the skill ZIP.
6. Reply in Vietnamese with: the scanned token table, capital → final equity / P&L / ROI, critic result, defects fixed, and send the MP4 + compare sheet with SendUserFile.
