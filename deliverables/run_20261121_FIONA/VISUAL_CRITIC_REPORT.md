# Visual Critic Report — GROK MEME MILLION V1.8.4

- Video: `grok_meme_million_v1.8.4.mp4` · Reference: `reference/ (bundled stills)`
- Automated verdict: **ACCEPTED** · checks passed **50/50** · auto score 10.0/10
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
| PASS | no duplicated frames | 0 near-identical consecutive pairs; min diff 0.126 |
| PASS | no frozen stretch > 0.5 s | longest low-motion run 0 frames |
| PASS | readable (sharp) frames >= 97% | 440/450 sharp; soft frames [363, 364, 365, 366, 367, 368, 369, 370, 409, 410] |
| PASS | no ghost flashes in the banner zone (< 3 frames) | 0 flashes |
| PASS | no overlapping text (same layer) | 0 overlaps |
| PASS | no horizontally clipped text | 0 cases |
| PASS | text inside its card/pill | 0 cases |
| PASS | every visible BUY/SELL marker has its label | 0 frames with a marker but no label |
| PASS | BUY/SELL labels never cover candles or markers | 0 hits |
| PASS | chart visible | 363 frames with the candle plot on screen |
| PASS | BUY marker visible | 264 frames |
| PASS | SELL marker visible | 222 frames |
| PASS | no ghost text (two legible overlapping banner/header texts) | 0 frames |
| PASS | every banner fully visible >= 16 frames | 10 banners, min 17 frames |
| PASS | page text scale under 3D camera >= 0.92 | min 0.925 (fly-out 11.8-12.64 s and end card exempt) |
| PASS | camera rotation within +/-6 deg | max 5.00 deg |
| PASS | parallax depth: >= 3 layers move differently (2.5-3.15 s) | camera-induced layer shifts {'L0': 38.7, 'L1': 1.6, 'L2': 6.2, 'L4': 10.9} |
| PASS | 3D coin = Blender PBR render | coin mode ['blender'] |
| PASS | minimum on-screen font size >= 22 px | smallest font 22 px (1080x1920 native) |
| PASS | equity chain = capital + sum(trade P&L) | $666.36 + $3598.36 = $4264.72 |
| PASS | ROI and multiple | ROI 540.00% · 6.40x |
| PASS | initial capital in $500-$700 | $666.36 |
| PASS | final profit in $1,000-$5,000 | $3598.36 |
| PASS | every win $12-$999.99, every loss $10-$300 | wins $127.45-$602.63; losses $129.15-$129.15 |
| PASS | no single trade > 30% of total profit | largest = 16.7% of total |
| PASS | position size <= 45% of equity | all trades |
| PASS | trade % within allowed ranges | wins [0.15, 2.5], losses [-0.45, -0.1] (hero % = real move) |
| PASS | final equity shown on last frame | $4,264.72 |
| PASS | final profit not revealed early (<10 s) | 0 early occurrences |
| PASS | watchlist verified by mint+pool (DEX Screener + RPC) | 6 tokens: FIONA(B34n…/DjbL…), GATO(Hspr…/5E3d…), CYBERLEEK(ApZu…/G8kg…), pippin(Dfh5…/8Wwc…), mihao(4Cxj…/Ho1a…), CLAUDIA(2j5S…/Fe7b…) |
| PASS | chart candles are byte-identical real OHLCV | 72 candles from GeckoTerminal /networks/solana/pools/{pool}/ohlcv/minute pool DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB |
| PASS | hero trade prices = real candle closes | entry/exit at candle closes |
| PASS | snapshot not presented as realtime | snapshot 2026-11-21T02:22:19Z |
| PASS | no unsupported live/on-chain claims in UI text | [] |
| PASS | concept/paper labelling on screen | 450/450 frames |
| PASS | on-chain executions separated | no wallet configured in config.json -> no verified executions are shown |
| PASS | SFX onset at every trade event | 1.171875s sell +4.7dB; 3.28125s buy +15.4dB; 4.6875s sell +14.8dB; 5.625s buy +14.3dB; 7.03125s stop +17.8dB; 7.734375s sell +7.8dB; 8.4375s sell +11.8dB; 10.3125s sell +10.7dB; 11.25s buy +7.4dB; 12.65625s sell +4.0dB |
| PASS | audio not clipping | peak -1.64 dBFS |
| PASS | loudness -14 LUFS +/-1 (TikTok) | -14.25 LUFS integrated (decoded AAC) |
| PASS | true peak <= -1.0 dBTP | -1.57 dBTP (4x oversampled, decoded AAC) |
| PASS | every trade event on the beat grid (+/-1 frame) | max offset 0.0 ms from the 1/8-note grid |
| PASS | no silent gap > 150 ms | longest quiet run 0 ms |
| PASS | visual density close to reference (0.6-1.6x) | edge density ratio 1.25 |
| PASS | dark premium palette like reference | dark share ref 0.84 vs new 0.84 |

## Reference comparison (matched timestamps)

| New t | Ref t | Edge density ref/new | Dark share ref/new | Green share ref/new |
|---|---|---|---|---|
| 0.6s | 0.6s | 7.7 / 8.9 | 0.89 / 0.90 | 0.020 / 0.034 |
| 2.0s | 2.0s | 8.2 / 9.4 | 0.83 / 0.83 | 0.022 / 0.039 |
| 3.6s | 3.6s | 6.8 / 11.9 | 0.82 / 0.82 | 0.048 / 0.020 |
| 4.9s | 4.9s | 9.2 / 12.3 | 0.87 / 0.82 | 0.009 / 0.017 |
| 7.0s | 7.0s | 9.3 / 12.4 | 0.88 / 0.82 | 0.010 / 0.018 |
| 8.4s | 8.4s | 9.3 / 12.4 | 0.83 / 0.82 | 0.008 / 0.020 |
| 10.6s | 10.6s | 8.7 / 11.7 | 0.83 / 0.83 | 0.010 / 0.010 |
| 13.2s | 13.2s | 8.4 / 10.7 | 0.80 / 0.81 | 0.041 / 0.046 |
| 14.7s | 14.7s | 8.6 / 5.5 | 0.81 / 0.87 | 0.023 / 0.036 |

Side-by-side sheet: `compare_sheet.png` (top = reference, bottom = new).

## Human-in-the-loop inspection

| Area | Score | Notes |
|---|---|---|
| UI structure & iPhone layout | 9.5 | Same order as reference: header -> balance hero -> equity chart -> timeframe tabs -> Live screen -> Bots (5) -> Activity, iOS status bar, banners and tab bar. Fullscreen 1080x1920, no device frame. |
| Typography | 9.5 | Inter (SF Pro substitute) throughout; balance 128 px, sticky balance 72 px, P&L 42 px, section titles 44 px, rows 34/26 px, smallest 22 px (critic-enforced). |
| Candlestick readability | 9.5 | 44-candle viewport over ~850 px plot, real OHLCV, EMA7/EMA20, RSI14, right price scale with uniform decimals, time scale, volume, crosshair + time tag, live price tag. |
| BUY/SELL visibility | 9.6 | Triangle + pill + pulse ring; pills auto-placed to avoid candles, other markers, the price tag and legend (0 collisions in 450 frames); synced banner, feed row, sound and camera push. |
| Chart motion | 9.5 | Replay reveal of real candles, smoothed auto-range, marching price line, breakout band, coins fly from SELL markers into the sticky balance. |
| Agent activity | 9.0 | Five distinct vector icons with progress rings/bars, per-event status text, flashing row on change; Scanner cycles the verified watchlist. |
| 3D depth | 9.5 | 5-layer scene graph with one perspective camera (dolly/crane/yaw/pitch, push-ins on trades, orbit at the finale), DOF background + dust, Blender PBR coin sprites with cast shadows, 3D page fly-out at 11.8-12.64 s; text scale >= 0.92 enforced. |
| Transition rhythm | 9.5 | Events quantized to the 1/8-note grid; screen-recording-crisp scrolls (no blur except the far-shot fly-out); end card readable from its 3rd frame. |
| Audio sync | 9.3 | New engine: intro/build/drop/breakdown/riser/drop B arrangement, hook, layered drums, reverb, sidechain; -14.2 LUFS, -1.6 dBTP, stereo correlation 0.77, all events on beat. Score is estimated from measurements (spectrogram, section levels) - not from listening. |
| Data provenance | 10 | Mint+pool verified on 3 sources, candles byte-identical, snapshot labelled with time, trades labelled CONCEPT/Paper, no on-chain claims. |

## Build iterations (defects found → fixed → re-rendered)

1. **REVIEW** — Flying coins covered the SELL pill; price axis mixed 4/5/6 decimals; banner slightly translucent → _fix:_ coins launch after pill settles and travel away from it; axis uses one precision; opaque banners
2. **REVIEW** — 5-sample motion blur smeared the return scroll into ghost copies and ghosted changing chart text during banner entries; one SELL pill dropped when no slot was free; finale coins left the frame instantly; flat early equity curve → _fix:_ adaptive 5-24 sub-samples, 90-degree shutter, blur only on scroll; horizontal pill candidates; ballistic coin burst; time-proportional curve sampling
3. **REVIEW** — Axis labels collided with the live price tag and crosshair time tag → _fix:_ suppress axis labels near the tags
4. **REJECTED (auto)** — 253 text overlaps (stacked banners, inserting feed rows), duplicate frame at 1.17 s, audio peak measured on mono downmix → _fix:_ exiting banners recede on their own layer; inserting rows tagged as clipped animation; slow camera push-in so no frame is static; -3 dBFS master + stereo peak measurement
5. **REJECTED (auto)** — 5 overlaps at 5.6 s (banner handoff on the exact frame) → _fix:_ banner counts as exiting from its replacement time
6. **REVIEW** — SELL triangle sat on the BUY pill; sticky balance peeked behind banners; end coin caught edge-on → _fix:_ all marker triangles join the collision set (and the critic check); sticky yields to banners; face-forward coin wobble
7. **ACCEPTED** — 34/34 automated checks, manual review of 9 matched timestamps vs reference → _fix:_ banner handoff tightened to 0.1 s
8. **REVIEW (run 2, fresh data)** — FIONA rally filled the space around the SELL 50% marker so its label was skipped at 4.75-5.2 s; page text and a faded sticky balance showed behind incoming banners → _fix:_ pill search extended to 44 vertical steps; new critic check 'every visible marker has its label'; sticky mask stays opaque, only its text yields, faster
9. **REVIEW (run 2)** — Banner handoff at 6.95 s cross-faded two banners for 2 frames; page text faintly visible under the sticky mask → _fix:_ old banner leaves in 0.06 s before the new one appears; sticky mask fully opaque to 72%
10. **ACCEPTED (run 2)** — 35/35 automated checks + manual review of 4.85/4.9/6.95-7.05/7.7/10.6/13.3/14.7 s → _fix:_ -
11. **REJECTED (auto, V1.8.4)** — 72 soft frames, 6 banner-zone flashes, finale SELL chime masked by the riser → _fix:_ continuous blur; follow-up banners stack instead of exiting; 1/16 drop gap before the finale
12. **REJECTED (auto, V1.8.4)** — 3-sample blur doubled text on scrolls; odometer left a digit half-rolled on a static balance; sticky popped for 3 frames before a banner → _fix:_ no blur on normal scrolls (like the screen-recorded reference), dense blur only in the fly-out; odometer snaps when static; banner owns the slot 0.6 s ahead
13. **ACCEPTED (V1.8.4)** — 50/50 automated checks + manual review of 12 stills (0.8-14.5 s) → _fix:_ -

## Audio sync (onset rise at each event)

- 1.171875s sell +4.7 dB
- 3.28125s buy  +15.4 dB
- 4.6875s sell +14.8 dB
- 5.625s buy  +14.3 dB
- 7.03125s stop +17.8 dB
- 7.734375s sell +7.8 dB
- 8.4375s sell +11.8 dB
- 10.3125s sell +10.7 dB
- 11.25s buy  +7.4 dB
- 12.65625s sell +4.0 dB
