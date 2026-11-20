# Trading Data Audit — GROK MEME MILLION V1.8.3

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

Seed 586286 · initial capital $522.61 · final equity $4,175.16 · total P&L +$3,652.55 · ROI 698.91% · 7.99x

| # | Video t | Token | Size | Result | P&L | Equity after | Price basis |
|---|---|---|---|---|---|---|---|
| 1 | history | pippin | $116.50 | trail 40% | +$188.26 (+161.6%) | $710.87 | concept result |
| 2 | history | mihao | $250.01 | trail 40% | +$128.34 (+51.3%) | $839.21 | concept result |
| 3 | history | DCTY | $164.95 | trail 40% | +$56.76 (+34.4%) | $895.97 | concept result |
| 4 | history | TTWO | $196.84 | take profit 50% | +$207.34 (+105.3%) | $1,103.31 | concept result |
| 5 | history | VINE | $412.18 | take profit 50% | +$134.57 (+32.6%) | $1,237.88 | concept result |
| 6 | 1.25 | pippin | $222.66 | trail 40% | +$93.80 (+42.1%) | $1,331.68 | concept result |
| 7 | 4.75 | FIONA | $199.75 | take profit 50% | +$261.68 (+131.0%) | $1,593.36 | real candle close #48 (0.00185592) |
| 8 | 6.95 | mihao | $264.92 | -25% stop | -$75.56 (-28.5%) | $1,517.80 | concept result |
| 9 | 7.65 | FIONA | $199.75 | trail 40% | +$301.56 (+151.0%) | $1,819.36 | real candle close #55 (0.00201636) |
| 10 | 8.45 | DCTY | $551.73 | take profit 50% | +$458.17 (+83.0%) | $2,277.53 | concept result |
| 11 | 10.35 | TTWO | $685.41 | trail 40% | +$520.29 (+75.9%) | $2,797.82 | concept result |
| 12 | 12.55 | VINE | $990.62 | take profit 100% | +$1,377.34 (+139.0%) | $4,175.16 | concept result |

Check: $522.61 + Σ P&L +$3,652.55 = $4,175.16 (integer-cent chain verified).

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
