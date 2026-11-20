---
name: grok-meme-million-video
description: Build the "GROK × MEME COIN — ROAD TO $1M" 15-second 9:16 trading-app video (V1.8.4). Reproduces the reference iPhone "Grok Bot" app (balance, equity chart, Live screen terminal with real Solana OHLCV candles, BUY/SELL markers, 5 AI agents, activity feed, iOS banners), adds 3D camera/coins, an original EDM soundtrack, and gates delivery with an automated Visual Critic. Use when asked to make, update or re-render the Grok meme-coin million video.
---

# GROK MEME MILLION — V1.8.4

Skill name is fixed: **grok-meme-million-video** (do not rename; the project command `/grok`
in `.claude/commands/grok.md` runs it). V1.8.4 upgrades V1.8.3 (itself built on
V1.8.2 "Clear Trading") while keeping the same concept, branding, scenes and data
architecture. Everything on screen is English.

## One command

```bash
./build.sh /path/to/reference.mp4 [seed] [--offline]
```

Pipeline (each step is also runnable alone):

| Step | File | Output |
|---|---|---|
| 1. Market data | `src/fetch_data.py` | `data/market_snapshot.json`, `assets/logos/*.png` |
| 2. Scenario | `src/scenario.py [seed]` | `data/scenario.json` |
| 3. Frames | `src/render.py` (`--still T …` for previews) | `output/*_silent.mp4`, `output/layout_registry.json`, `output/timeline.json` |
| 3b. 3D coin | `blender -b -P src/blender_coin.py -- assets/coins 72 512 64` (once, cached) | `assets/coins/coin_00..71.png` |
| 4. Audio | `src/audio.py` + `src/sound/` | `output/soundtrack.wav` (−14 LUFS, ≤ −1 dBTP), `output/stems/*.wav` |
| 5. Mux | ffmpeg in `build.sh` | `output/grok_meme_million_v1.8.3.mp4` |
| 6. Visual Critic | `src/critic.py --ref ref.mp4` | `critic_report.json`, `compare_sheet.png`, `contact_sheet.png`, previews; exit 1 = rejected |
| 7. Reports | `src/report.py` | `VISUAL_CRITIC_REPORT.md`, `TRADING_DATA_AUDIT.md` |

Requirements: Python 3.11+, `skia-python` (needs `libegl1 libgl1`), numpy, scipy, Pillow, pyloudnorm,
Blender 4.x (optional: coin sprites; vector fallback otherwise),
ffmpeg, Inter fonts at `/usr/share/fonts/opentype/inter/`. Network: `api.geckoterminal.com`,
`api.dexscreener.com`, `api.mainnet-beta.solana.com`, logo CDNs (`assets.geckoterminal.com`,
`coin-images.coingecko.com`, `dd.dexscreener.com`). `--offline` reuses the last snapshot
(it is still labelled with its original timestamp).

## Storyboard (15.0 s, 30 fps, 450 frames)

| Time | Scene | What happens |
|---|---|---|
| 0.0–2.5 | Portfolio | App opens on Portfolio Balance, Total P&L + multiple pill, equity chart, slow push-in; SELL banner at 1.25 s with count-up |
| 2.5–6.5 | Live screen | Scroll to terminal; real candles replay; BUY at 3.35 s, SELL 50 % at 4.75 s with camera push, pulse, coins → sticky balance |
| 6.5–9.0 | Execution | STOP (red) banner, final hero SELL, another win; cumulative P&L counts in the sticky header |
| 9.0–12.0 | Agents + Activity | Scroll to Bots ×5 and the Activity feed; rows insert live; agent statuses/progress change |
| 12.0–15.0 | Finale | Scroll home, last SELL, odometer reveal of final equity + sheen + 3D coin burst, end card "GROK × MEME COIN / ROAD TO $1M" with final numbers |

## Design rules (from the reference)

- Fullscreen iOS app, background `#06090A`, positive `#20D58B`, negative `#FF5D72`,
  text `#F5F7F9` / `#A0ADB7`. Inter as SF Pro substitute.
- Sizes at 1080×1920: balance 128 px, sticky balance 72 px, P&L 42 px, section titles 44 px,
  row titles 34 px, sublines 26 px, **nothing under 22 px** (critic-enforced).
- Live terminal: token logo + `SYMBOL / SOL` + DEX + pool, price + replay change, status strip,
  44-candle plot, EMA7 (gold) / EMA20 (purple) / RSI14 legend, right price scale (uniform
  decimals), time scale, volume bars, dashed current-price line + tag, crosshair + time tag,
  breakout band, 6-tile verified watchlist, provenance footer.
- BUY = green ▲ under the candle + pill `BUY $size`; SELL = red ▼ over the candle + pill
  `SELL [50%] ±$P&L` (P&L green/red). Pills are placed by collision search against candles,
  every marker triangle, the price tag and the legend; if no slot exists the pill is skipped
  rather than covering data.
- 3D: perspective camera (tilt on scroll velocity, push-ins on trades, finale breathe),
  parallax background glows (0.3×), foreground banners (spring scale + depth shadow), thick lit
  coins (rim extrusion, radial lighting, moving specular), depth-of-field coin burst,
  adaptive 5–24-sample motion blur during scrolls only.

## Data provenance (non-negotiable)

- Watchlist = GeckoTerminal Solana trending pools (24 h), quote SOL, liquidity ≥ $50k,
  volume ≥ $300k. Each pool is cross-checked on DEX Screener (same pool → same base **mint**,
  price within 8 %) and each mint is checked on Solana RPC to be an SPL/Token-2022 mint.
  Tokens are never matched by ticker alone; data from different pools is never mixed.
- Chart = real 5 m OHLCV of one verified pool (the one whose real candles contain the
  clearest tradable structure). The critic asserts the drawn candles are byte-identical to
  the fetched rows. If OHLCV is unavailable the chart is titled `CONCEPT / SOL` instead.
- The snapshot time is printed on screen; nothing says "realtime". Header chip says
  **Paper**, the tab says **REPLAY**, balance carries **CONCEPT TRADES**, Activity carries
  **CONCEPT**, chart footer says **Markers = concept trades**.
- Verified on-chain executions are shown only if `config.wallet.address` is set and the
  executions are verified; otherwise none are shown and the audit says so.

## Concept trade maths

- Integer cents. Capital random in `$500–700`; target profit random in `$1,000–5,000`;
  3–5 history trades + 7 in-video results; the last trade absorbs the residual so
  `capital + Σ P&L = final equity` exactly; every result stays in the tens–hundreds range.
- Hero-token trades use real candle closes for entry/exit (their % is the real move).
- Balance on screen = realized equity + hero position marked to the replay price, so the
  value moves progressively and never shows the final number before 12.6 s.

## Visual Critic (auto-reject on any critical)

Tech (1080×1920, 30/1, H.264, 450 frames, 15.000 s, AAC 48 kHz stereo) · no duplicate or
frozen frames · no same-layer text overlap · no clipped text · text inside its card/pill ·
BUY/SELL pills never cover candles/markers · chart and both marker types visible · min font
22 px · equity chain / ROI / multiple / ranges · final equity on last frame and not before
10 s · mint+pool verification · byte-identical candles · no realtime/on-chain claims ·
concept labelling on ≥95 % of frames · SFX onset at every event · no clipping · visual
density and palette vs. reference at 9 matched timestamps. Then inspect
`compare_sheet.png` by eye, log defects in `data/review_log.json`, fix, re-render.

## V1.8.4 systems

- **3D scene graph** (`render.py`, section *camera*): layers L0 background (z −600, DOF blur, dust),
  L1 page (z 0), L2 floating chart labels (z +60), L3 chrome (status/tab bar/sticky, only follows the
  camera in fly-out/end), L4 foreground banners + coins (z +120). One perspective camera
  (D = 1800) does dolly/truck/crane/yaw/pitch; at rest every layer is pixel-exact. Choreography:
  portfolio dolly-in, crane on scrolls, push-in on every BUY/SELL, half-bar truck in execution,
  **3D page fly-out** 11.8–12.64 s instead of a smeared scroll, orbit around the final balance,
  pull-back behind the end card. Guards: |yaw|,|pitch| ≤ 6°, page text scale ≥ 0.92 (critic).
- **Coins**: Blender Cycles PBR gold coin (reeded rim, bevel, embossed original Grok Bot mark),
  72-frame turntable sprites with page shadows along the scene light.
- **Banner Manager**: IDLE → ENTERING → SHOWN → STACKING | EXITING → GONE. A replaced banner
  dims and recedes behind the new one (iOS stack) before the new text appears; the sticky balance
  text is hidden for the whole time the slot is occupied. Critic: no ghost text, ≥ 16 fully
  visible frames per banner, no < 3-frame flashes in the banner zone.
- **Sound engine** (`src/sound/`): PolyBLEP oscillators, 7-voice supersaw, resonant envelope
  filters, 3-layer kick, snare/clap, swung hats, ride, sub + reese bass, pad, pluck, lead hook
  (A4 C5 E5 D5 | C5 A4 G4 A4), convolution reverb, ping-pong delay, chorus, saturation,
  sidechain, SFX ducking, bus compression, BS.1770 mastering to −14 LUFS / ≤ −1 dBTP.
  Arrangement: intro → build → drop A → breakdown → riser → drop B on the finale SELL → end chord.
  All trade events are quantized to the 1/8-note grid (128 BPM) in `scenario.py`.
- **Trade limits** (`config.trade_limits`): wins $12–$999.99, losses $10–$300, no trade > 30 % of
  total profit, size ≤ 45 % of equity, win % 15–250 %, loss % −10…−45 %. Allocation by
  Dirichlet water-filling; the finale trade is the largest win; hero trades keep real % moves.

## Changelog

- **1.8.4** — 3D scene graph + camera, Blender coin, 3D fly-out transition, Banner Manager
  (no ghosting), new sound engine with beat-locked events and LUFS/TP mastering + stems,
  trade limits with water-fill allocation, ~13 new critic checks, `/grok` command.
- **1.8.3** — Skia renderer rebuilt to match the reference app; detailed real-OHLCV terminal
  with EMA/RSI/volume/crosshair/price tag; collision-safe BUY/SELL pills; sticky balance;
  odometer digits; 3D camera + coins; original synced soundtrack; 3-source data
  verification; automated Visual Critic with reference comparison; data audit report.
- 1.8.2 — Clear Trading (previous release).
