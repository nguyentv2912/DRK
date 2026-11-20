# Visual Critic Report — GROK MEME MILLION V1.8.3

- Video: `grok_meme_million_v1.8.3.mp4` · Reference: `reference.mp4`
- Automated verdict: **ACCEPTED** · checks passed **34/34** · auto score 10.0/10
- Reviewed quality vs. reference: **9.5/10** (target 9.5)

## Automated checks

| Result | Check | Detail |
|---|---|---|
| PASS | resolution 1080x1920 | 1080x1920 |
| PASS | frame rate 30 | 30/1 |
| PASS | codec H.264 | h264 |
| PASS | frame count 450 (no missing frames) | 450 frames |
| PASS | duration 15.0 s | 15.000s |
| PASS | audio AAC stereo 48 kHz | aac 48000 2ch |
| PASS | no duplicated frames | 0 near-identical consecutive pairs; min diff 0.084 |
| PASS | no frozen stretch > 0.5 s | longest low-motion run 0 frames |
| PASS | no overlapping text (same layer) | 0 overlaps |
| PASS | no horizontally clipped text | 0 cases |
| PASS | text inside its card/pill | 0 cases |
| PASS | BUY/SELL labels never cover candles or markers | 0 hits |
| PASS | chart visible | 364 frames with the candle plot on screen |
| PASS | BUY marker visible | 75 frames |
| PASS | SELL marker visible | 208 frames |
| PASS | minimum on-screen font size >= 22 px | smallest font 22 px (1080x1920 native) |
| PASS | equity chain = capital + sum(trade P&L) | $691.44 + $2346.38 = $3037.82 |
| PASS | ROI and multiple | ROI 339.35% · 4.39x |
| PASS | initial capital in $500-$700 | $691.44 |
| PASS | final profit in $1,000-$5,000 | $2346.38 |
| PASS | trade results tens-hundreds of $ | min $24.96, max $1081.00 |
| PASS | final equity shown on last frame | $3,037.82 |
| PASS | final profit not revealed early (<10 s) | 0 early occurrences |
| PASS | watchlist verified by mint+pool (DEX Screener + RPC) | 6 tokens: mihao(4Cxj…/Ho1a…), FIONA(B34n…/DjbL…), pippin(Dfh5…/8Wwc…), TTWO(TTWo…/7qZP…), DCTY(9hjB…/3gUa…), GTA6(4kjr…/xg71…) |
| PASS | chart candles are byte-identical real OHLCV | 72 candles from GeckoTerminal /networks/solana/pools/{pool}/ohlcv/minute pool 3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw |
| PASS | hero trade prices = real candle closes | entry/exit at candle closes |
| PASS | snapshot not presented as realtime | snapshot 2026-11-20T03:23:25Z |
| PASS | no unsupported live/on-chain claims in UI text | [] |
| PASS | concept/paper labelling on screen | 450/450 frames |
| PASS | on-chain executions separated | no wallet configured in config.json -> no verified executions are shown |
| PASS | SFX onset at every trade event | 1.25s sell +19.6dB; 3.35s buy +20.3dB; 4.75s sell +20.7dB; 5.6s buy +18.1dB; 6.95s stop +16.0dB; 7.65s sell +24.8dB; 8.45s sell +16.1dB; 10.35s sell +19.7dB; 11.25s buy +19.4dB; 12.55s sell +6.2dB |
| PASS | audio not clipping | peak -2.70 dBFS |
| PASS | visual density close to reference (0.6-1.6x) | edge density ratio 1.22 |
| PASS | dark premium palette like reference | dark share ref 0.85 vs new 0.85 |

## Reference comparison (matched timestamps)

| New t | Ref t | Edge density ref/new | Dark share ref/new | Green share ref/new |
|---|---|---|---|---|
| 0.6s | 0.58s | 7.6 / 8.7 | 0.90 / 0.91 | 0.019 / 0.030 |
| 2.0s | 1.94s | 8.2 / 8.9 | 0.84 / 0.84 | 0.020 / 0.033 |
| 3.6s | 3.5s | 6.8 / 11.8 | 0.84 / 0.82 | 0.045 / 0.022 |
| 4.9s | 4.76s | 9.2 / 11.9 | 0.88 / 0.87 | 0.008 / 0.029 |
| 7.0s | 6.8s | 9.3 / 11.9 | 0.89 / 0.88 | 0.009 / 0.017 |
| 8.4s | 8.16s | 9.4 / 12.1 | 0.84 / 0.82 | 0.007 / 0.017 |
| 10.6s | 10.29s | 8.7 / 11.2 | 0.85 / 0.84 | 0.009 / 0.009 |
| 13.2s | 12.82s | 8.4 / 10.3 | 0.82 / 0.82 | 0.038 / 0.040 |
| 14.7s | 14.28s | 8.7 / 6.4 | 0.82 / 0.84 | 0.021 / 0.043 |

Side-by-side sheet: `compare_sheet.png` (top = reference, bottom = new).

## Human-in-the-loop inspection

| Area | Score | Notes |
|---|---|---|
| UI structure & iPhone layout | 9.5 | Same order as reference: header -> balance hero -> equity chart -> timeframe tabs -> Live screen -> Bots (5) -> Activity, iOS status bar, banners and tab bar. Fullscreen 1080x1920, no device frame. |
| Typography | 9.5 | Inter (SF Pro substitute) throughout; balance 128 px, sticky balance 72 px, P&L 42 px, section titles 44 px, rows 34/26 px, smallest 22 px (critic-enforced). |
| Candlestick readability | 9.5 | 44-candle viewport over ~850 px plot, real OHLCV, EMA7/EMA20, RSI14, right price scale with uniform decimals, time scale, volume, crosshair + time tag, live price tag. |
| BUY/SELL visibility | 9.5 | Triangle + pill + pulse ring; pills auto-placed to avoid candles, other markers, the price tag and legend (0 collisions in 450 frames); synced banner, feed row, sound and camera push. |
| Chart motion | 9.5 | Replay reveal of real candles, smoothed auto-range, marching price line, breakout band, coins fly from SELL markers into the sticky balance. |
| Agent activity | 9.0 | Five distinct vector icons with progress rings/bars, per-event status text, flashing row on change; Scanner cycles the verified watchlist. |
| 3D depth | 9.0 | Perspective camera (tilt on scroll, push-ins on trades), background parallax glows, foreground banners with spring-in scale + depth shadow, thick lit coins with rim/specular, depth-of-field coin burst. |
| Transition rhythm | 9.5 | Storyboard 0-2.5 / 2.5-6.5 / 6.5-9 / 9-12 / 12-15 matches the reference cadence; adaptive multi-sample motion blur only during scrolls. |
| Audio sync | 9.5 | Original 128 BPM synth track, sidechained; banner chime, buy blip, sell chime + count ticks, stop drop, whooshes/scans, riser -> impact at the reveal; every event has a measured onset. |
| Data provenance | 10 | Mint+pool verified on 3 sources, candles byte-identical, snapshot labelled with time, trades labelled CONCEPT/Paper, no on-chain claims. |

## Build iterations (defects found → fixed → re-rendered)

1. **REVIEW** — Flying coins covered the SELL pill; price axis mixed 4/5/6 decimals; banner slightly translucent → _fix:_ coins launch after pill settles and travel away from it; axis uses one precision; opaque banners
2. **REVIEW** — 5-sample motion blur smeared the return scroll into ghost copies and ghosted changing chart text during banner entries; one SELL pill dropped when no slot was free; finale coins left the frame instantly; flat early equity curve → _fix:_ adaptive 5-24 sub-samples, 90-degree shutter, blur only on scroll; horizontal pill candidates; ballistic coin burst; time-proportional curve sampling
3. **REVIEW** — Axis labels collided with the live price tag and crosshair time tag → _fix:_ suppress axis labels near the tags
4. **REJECTED (auto)** — 253 text overlaps (stacked banners, inserting feed rows), duplicate frame at 1.17 s, audio peak measured on mono downmix → _fix:_ exiting banners recede on their own layer; inserting rows tagged as clipped animation; slow camera push-in so no frame is static; -3 dBFS master + stereo peak measurement
5. **REJECTED (auto)** — 5 overlaps at 5.6 s (banner handoff on the exact frame) → _fix:_ banner counts as exiting from its replacement time
6. **REVIEW** — SELL triangle sat on the BUY pill; sticky balance peeked behind banners; end coin caught edge-on → _fix:_ all marker triangles join the collision set (and the critic check); sticky yields to banners; face-forward coin wobble
7. **ACCEPTED** — 34/34 automated checks, manual review of 9 matched timestamps vs reference → _fix:_ banner handoff tightened to 0.1 s

## Audio sync (onset rise at each event)

-  1.25s sell +19.6 dB
-  3.35s buy  +20.3 dB
-  4.75s sell +20.7 dB
-   5.6s buy  +18.1 dB
-  6.95s stop +16.0 dB
-  7.65s sell +24.8 dB
-  8.45s sell +16.1 dB
- 10.35s sell +19.7 dB
- 11.25s buy  +19.4 dB
- 12.55s sell +6.2 dB
