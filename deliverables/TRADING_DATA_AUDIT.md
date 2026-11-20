# Trading Data Audit — GROK MEME MILLION V1.8.3

Snapshot window: 2026-11-20T03:23:03Z → 2026-11-20T03:23:25Z (point-in-time; shown on screen as a snapshot/replay, **not realtime**).

## Verified watchlist (Solana, GeckoTerminal trending 24h → DEX Screener → Solana RPC)

| Symbol | Mint | Pool | DEX | Price USD | 24h | Vol 24h | Liquidity | DS price dev | RPC mint | Checked |
|---|---|---|---|---|---|---|---|---|---|---|
| mihao | `4CxjZyMNoF1p6eXHXHv1TWpS2X47CuUmLwtGe18spump` | `Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz` | pumpswap | 0.0076085268 | +5.00% | $8,825,638 | $328,129 | 0.18% | token-2022 ✓ | 2026-11-20T03:23:04Z |
| FIONA | `B34nXKzCgsJb9ChLuSHPRpXLE3WFSWyeT8Cqkzzmpump` | `DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` | pumpswap | 0.0015548768 | +4890.88% | $7,751,422 | $110,131 | 2.77% | token-2022 ✓ | 2026-11-20T03:23:06Z |
| pippin | `Dfh5DzRgSvvCFDoYc2ciTkMrbDfRKybA4SoFbPmApump` | `8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt` | raydium | 0.018998523 | +7.54% | $4,003,111 | $3,455,053 | 0.41% | spl-token ✓ | 2026-11-20T03:23:07Z |
| TTWO | `TTWofwAge91oFhZs7kpQdyrVRkmevgM88xijGvQFbKo` | `7qZPiJ2Lvwh9DV9gUBH2EwConBE3RUrAvGRjpN8vTjtT` | meteora | 208.78782 | -6.38% | $58,348,406 | $637,674 | 0.66% | token-2022 ✓ | 2026-11-20T03:23:09Z |
| DCTY | `9hjBLBrc7WZW2H8UQvBAvG5WiTZotXUv2Bdcn4f4pump` | `3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw` | meteora | 0.004572483 | -70.83% | $25,431,561 | $156,332 | 0.56% | token-2022 ✓ | 2026-11-20T03:23:11Z |
| GTA6 | `4kjruqGHDsSqkMdFfCjV7Vb62HPFhtXyWc2t6JpQzDnz` | `xg71xrhn7MEj5akrZGteuYeiTLbBzyNCpBn69bRYd5a` | meteora | 0.0016182455 | -83.26% | $1,343,408 | $55,003 | 2.43% | spl-token ✓ | 2026-11-20T03:23:12Z |

## Chart data (hero pool)

- Status: **verified** · source `GeckoTerminal /networks/solana/pools/{pool}/ohlcv/minute` · fetched 2026-11-20T03:23:24Z
- DCTY · mint `9hjBLBrc7WZW2H8UQvBAvG5WiTZotXUv2Bdcn4f4pump` · pool `3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw` · 5m candles
- Video window: 72 candles, 2026-11-19 15:40 → 21:35 UTC; byte-identical to the fetched rows (critic check).
- The forming candle is animated from its real open to its real close inside its real high/low; no prices outside the fetched OHLC are drawn.
- EMA7/EMA20/RSI14 computed from the real closes including pre-window history.
- Hero candidate scoring: mihao (160 candles, score 0.243), FIONA (79 candles, too short), pippin (160 candles, score 0.142), TTWO (160 candles, score -1.0), DCTY (160 candles, score 0.3)

## Concept trades (simulated — labelled CONCEPT TRADES / Paper on screen)

Seed 42 · initial capital $691.44 · final equity $3,037.82 · total P&L +$2,346.38 · ROI 339.35% · 4.39x

| # | Video t | Token | Size | Result | P&L | Equity after | Price basis |
|---|---|---|---|---|---|---|---|
| 1 | history | TTWO | $147.51 | take profit 50% | +$101.26 (+68.6%) | $792.70 | concept result |
| 2 | history | FIONA | $245.52 | trail 40% | +$273.29 (+111.3%) | $1,065.99 | concept result |
| 3 | history | pippin | $149.76 | trail 40% | +$192.78 (+128.7%) | $1,258.77 | concept result |
| 4 | 1.25 | TTWO | $297.83 | trail 40% | +$282.61 (+94.9%) | $1,541.38 | concept result |
| 5 | 4.75 | DCTY | $231.20 | take profit 50% | +$54.28 (+23.5%) | $1,595.66 | real candle close #42 (0.0117114) |
| 6 | 6.95 | FIONA | $246.66 | -25% stop | -$82.49 (-33.4%) | $1,513.17 | concept result |
| 7 | 7.65 | DCTY | $231.21 | trail 40% | +$24.96 (+10.8%) | $1,538.13 | real candle close #63 (0.0105088) |
| 8 | 8.45 | pippin | $339.18 | take profit 50% | +$168.15 (+49.6%) | $1,706.28 | concept result |
| 9 | 10.35 | GTA6 | $396.86 | trail 40% | +$250.54 (+63.1%) | $1,956.82 | concept result |
| 10 | 12.55 | mihao | $640.38 | take profit 100% | +$1,081.00 (+168.8%) | $3,037.82 | concept result |

Check: $691.44 + Σ P&L +$2,346.38 = $3,037.82 (integer-cent chain verified).

## On-chain executions

- none: no wallet configured in config.json -> no verified executions are shown
- No trade in this video is presented as an on-chain execution.

## Request log

| Fetched at (UTC) | OK | Endpoint |
|---|---|---|
| 2026-11-20T03:23:04Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/trending_pools` |
| 2026-11-20T03:23:04Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz` |
| 2026-11-20T03:23:05Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T03:23:06Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` |
| 2026-11-20T03:23:06Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T03:23:07Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt` |
| 2026-11-20T03:23:08Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T03:23:09Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/7qZPiJ2Lvwh9DV9gUBH2EwConBE3RUrAvGRjpN8vTjtT` |
| 2026-11-20T03:23:10Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T03:23:11Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw` |
| 2026-11-20T03:23:11Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T03:23:12Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/xg71xrhn7MEj5akrZGteuYeiTLbBzyNCpBn69bRYd5a` |
| 2026-11-20T03:23:12Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T03:23:13Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz/ohlcv/minute` |
| 2026-11-20T03:23:14Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB/ohlcv/minute` |
| 2026-11-20T03:23:15Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt/ohlcv/minute` |
| 2026-11-20T03:23:23Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/7qZPiJ2Lvwh9DV9gUBH2EwConBE3RUrAvGRjpN8vTjtT/ohlcv/minute` |
| 2026-11-20T03:23:24Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw/ohlcv/minute` |
