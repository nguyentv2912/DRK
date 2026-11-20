# Trading Data Audit — GROK MEME MILLION V1.8.4

Snapshot window: 2026-11-20T04:54:02Z → 2026-11-20T04:54:15Z (point-in-time; shown on screen as a snapshot/replay, **not realtime**).

## Verified watchlist (Solana, GeckoTerminal trending 24h → DEX Screener → Solana RPC)

| Symbol | Mint | Pool | DEX | Price USD | 24h | Vol 24h | Liquidity | DS price dev | RPC mint | Checked |
|---|---|---|---|---|---|---|---|---|---|---|
| mihao | `4CxjZyMNoF1p6eXHXHv1TWpS2X47CuUmLwtGe18spump` | `Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz` | pumpswap | 0.0075695933 | -2.40% | $8,852,158 | $325,612 | 0.05% | token-2022 ✓ | 2026-11-20T04:54:02Z |
| FIONA | `B34nXKzCgsJb9ChLuSHPRpXLE3WFSWyeT8Cqkzzmpump` | `DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` | pumpswap | 0.0016464422 | +5121.58% | $8,188,862 | $113,285 | 2.71% | token-2022 ✓ | 2026-11-20T04:54:04Z |
| TTWO | `TTWofwAge91oFhZs7kpQdyrVRkmevgM88xijGvQFbKo` | `7qZPiJ2Lvwh9DV9gUBH2EwConBE3RUrAvGRjpN8vTjtT` | meteora | 208.80054 | -6.41% | $57,421,922 | $664,904 | 0.31% | token-2022 ✓ | 2026-11-20T04:54:05Z |
| pippin | `Dfh5DzRgSvvCFDoYc2ciTkMrbDfRKybA4SoFbPmApump` | `8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt` | raydium | 0.018862849 | +8.75% | $4,201,802 | $3,426,669 | 0.44% | spl-token ✓ | 2026-11-20T04:54:07Z |
| DCTY | `9hjBLBrc7WZW2H8UQvBAvG5WiTZotXUv2Bdcn4f4pump` | `3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw` | meteora | 0.0035407843 | -75.39% | $25,069,105 | $128,401 | 1.35% | token-2022 ✓ | 2026-11-20T04:54:08Z |
| VINE | `6AJcP7wuLwmRYLBNbi825wgguaPsWzPBEHcHndpRpump` | `58fzJMbX5PatnfJPqWWsqkVFPRKptkbb5r2vCw4Qq3z9` | raydium | 0.010361984 | +51.22% | $3,181,896 | $1,539,154 | 1.08% | spl-token ✓ | 2026-11-20T04:54:09Z |

## Chart data (hero pool)

- Status: **verified** · source `GeckoTerminal /networks/solana/pools/{pool}/ohlcv/minute` · fetched 2026-11-20T04:54:11Z
- FIONA · mint `B34nXKzCgsJb9ChLuSHPRpXLE3WFSWyeT8Cqkzzmpump` · pool `DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` · 5m candles
- Video window: 72 candles, 2026-11-19 21:30 → 03:25 UTC; byte-identical to the fetched rows (critic check).
- The forming candle is animated from its real open to its real close inside its real high/low; no prices outside the fetched OHLC are drawn.
- EMA7/EMA20/RSI14 computed from the real closes including pre-window history.
- Hero candidate scoring: mihao (160 candles, score -1.0), FIONA (97 candles, score 2.1), TTWO (160 candles, score -1.0), pippin (160 candles, score 0.142), DCTY (160 candles, score 0.3)

## Concept trades (simulated — labelled CONCEPT TRADES / Paper on screen)

Seed 586286 · initial capital $574.66 · final equity $2,643.16 · total P&L +$2,068.50 · ROI 359.95% · 4.60x

| # | Video t | Token | Size | Result | P&L | Equity after | Price basis |
|---|---|---|---|---|---|---|---|
| 1 | history | pippin | $162.24 | take profit 50% | +$232.58 (+143.4%) | $807.24 | concept result |
| 2 | history | mihao | $185.92 | take profit 50% | +$104.35 (+56.1%) | $911.59 | concept result |
| 3 | history | DCTY | $115.12 | take profit 50% | +$192.10 (+166.9%) | $1,103.69 | concept result |
| 4 | history | TTWO | $336.04 | take profit 50% | +$73.62 (+21.9%) | $1,177.31 | concept result |
| 5 | history | VINE | $95.02 | take profit 50% | +$55.31 (+58.2%) | $1,232.62 | concept result |
| 6 | history | pippin | $522.08 | take profit 50% | +$78.79 (+15.1%) | $1,311.41 | concept result |
| 7 | history | mihao | $516.31 | trail 40% | +$91.98 (+17.8%) | $1,403.39 | concept result |
| 8 | 1.171875 | pippin | $236.32 | take profit 50% | +$86.03 (+36.4%) | $1,489.42 | concept result |
| 9 | 4.6875 | FIONA | $218.88 | take profit 50% | +$286.74 (+131.0%) | $1,776.16 | real candle close #48 (0.00185592) |
| 10 | 7.03125 | mihao | $259.27 | -36% stop | -$92.07 (-35.5%) | $1,684.09 | concept result |
| 11 | 7.734375 | FIONA | $218.88 | trail 40% | +$330.45 (+151.0%) | $2,014.54 | real candle close #55 (0.00201636) |
| 12 | 8.4375 | DCTY | $182.28 | trail 40% | +$51.94 (+28.5%) | $2,066.48 | concept result |
| 13 | 10.3125 | TTWO | $228.76 | trail 40% | +$118.38 (+51.7%) | $2,184.86 | concept result |
| 14 | 12.65625 | VINE | $366.88 | take profit 100% | +$458.30 (+124.9%) | $2,643.16 | concept result |

Check: $574.66 + Σ P&L +$2,068.50 = $2,643.16 (integer-cent chain verified).

## On-chain executions

- none: no wallet configured in config.json -> no verified executions are shown
- No trade in this video is presented as an on-chain execution.

## Request log

| Fetched at (UTC) | OK | Endpoint |
|---|---|---|
| 2026-11-20T04:54:02Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/trending_pools` |
| 2026-11-20T04:54:02Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz` |
| 2026-11-20T04:54:03Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T04:54:04Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` |
| 2026-11-20T04:54:04Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T04:54:05Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/7qZPiJ2Lvwh9DV9gUBH2EwConBE3RUrAvGRjpN8vTjtT` |
| 2026-11-20T04:54:06Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T04:54:07Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt` |
| 2026-11-20T04:54:07Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T04:54:08Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw` |
| 2026-11-20T04:54:08Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T04:54:09Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/58fzJMbX5PatnfJPqWWsqkVFPRKptkbb5r2vCw4Qq3z9` |
| 2026-11-20T04:54:09Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-20T04:54:10Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz/ohlcv/minute` |
| 2026-11-20T04:54:11Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB/ohlcv/minute` |
| 2026-11-20T04:54:12Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/7qZPiJ2Lvwh9DV9gUBH2EwConBE3RUrAvGRjpN8vTjtT/ohlcv/minute` |
| 2026-11-20T04:54:13Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt/ohlcv/minute` |
| 2026-11-20T04:54:14Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/3gUa73kgEfZW6zj97uShGaCd4GAPjc7kd61aKkcCMqpw/ohlcv/minute` |
