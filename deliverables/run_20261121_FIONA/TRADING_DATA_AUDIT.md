# Trading Data Audit — GROK MEME MILLION V1.8.4

Snapshot window: 2026-11-21T02:22:01Z → 2026-11-21T02:22:19Z (point-in-time; shown on screen as a snapshot/replay, **not realtime**).

## Verified watchlist (Solana, GeckoTerminal trending 24h → DEX Screener → Solana RPC)

| Symbol | Mint | Pool | DEX | Price USD | 24h | Vol 24h | Liquidity | DS price dev | RPC mint | Checked |
|---|---|---|---|---|---|---|---|---|---|---|
| FIONA | `B34nXKzCgsJb9ChLuSHPRpXLE3WFSWyeT8Cqkzzmpump` | `DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` | pumpswap | 0.0010414363 | -35.42% | $5,416,194 | $93,138 | 1.19% | token-2022 ✓ | 2026-11-21T02:22:02Z |
| GATO | `HsprHxBRgiVaQdRf3TnKNuZZtaX9JUSPgMFdAkk6pump` | `5E3dXLXGwmTDCokA51WYYaKttjFZBwqCoyUHBUi5gt2m` | pumpswap | 0.0029651324 | +82.84% | $684,595 | $182,905 | 5.83% | token-2022 ✓ | 2026-11-21T02:22:03Z |
| CYBERLEEK | `ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg` | `G8kgi7aUpeX8EVR8VMkrth9SKEv5BietWC33UjAiiMGh` | raydium | 0.0019726508 | +5.52% | $792,618 | $380,626 | 0.03% | spl-token ✓ | 2026-11-21T02:22:04Z |
| pippin | `Dfh5DzRgSvvCFDoYc2ciTkMrbDfRKybA4SoFbPmApump` | `8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt` | raydium | 0.017954239 | -1.65% | $5,579,677 | $3,266,923 | 0.25% | spl-token ✓ | 2026-11-21T02:22:06Z |
| mihao | `4CxjZyMNoF1p6eXHXHv1TWpS2X47CuUmLwtGe18spump` | `Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz` | pumpswap | 0.0065263162 | -10.70% | $1,634,825 | $298,355 | 0.29% | token-2022 ✓ | 2026-11-21T02:22:07Z |
| CLAUDIA | `2j5SaS7xy776qCBpyPQbZjyQSAtKiFgrwjfErthnW2ZM` | `Fe7bpDYCs74GqiCUF14HwgUMToPKV1d9mDYVX5BTohFr` | pumpswap | 0.0062959004 | +11.44% | $1,969,599 | $350,010 | 0.51% | token-2022 ✓ | 2026-11-21T02:22:08Z |

## Chart data (hero pool)

- Status: **verified** · source `GeckoTerminal /networks/solana/pools/{pool}/ohlcv/minute` · fetched 2026-11-21T02:22:11Z
- FIONA · mint `B34nXKzCgsJb9ChLuSHPRpXLE3WFSWyeT8Cqkzzmpump` · pool `DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` · 5m candles
- Video window: 72 candles, 2026-11-20 19:15 → 01:10 UTC; byte-identical to the fetched rows (critic check).
- The forming candle is animated from its real open to its real close inside its real high/low; no prices outside the fetched OHLC are drawn.
- EMA7/EMA20/RSI14 computed from the real closes including pre-window history.
- Hero candidate scoring: FIONA (160 candles, score 0.857), GATO (160 candles, score 0.354), CYBERLEEK (160 candles, score -1.0), pippin (160 candles, score -1.0), mihao (160 candles, score 0.34)

## Concept trades (simulated — labelled CONCEPT TRADES / Paper on screen)

Seed 224412 · initial capital $666.36 · final equity $4,264.72 · total P&L +$3,598.36 · ROI 540.00% · 6.40x

| # | Video t | Token | Size | Result | P&L | Equity after | Price basis |
|---|---|---|---|---|---|---|---|
| 1 | history | CYBERLEEK | $123.03 | trail 40% | +$127.45 (+103.6%) | $793.81 | concept result |
| 2 | history | pippin | $234.83 | trail 40% | +$208.27 (+88.7%) | $1,002.08 | concept result |
| 3 | history | CLAUDIA | $295.37 | take profit 50% | +$181.84 (+61.6%) | $1,183.92 | concept result |
| 4 | history | GATO | $364.79 | take profit 50% | +$196.44 (+53.9%) | $1,380.36 | concept result |
| 5 | history | mihao | $327.76 | take profit 50% | +$570.34 (+174.0%) | $1,950.70 | concept result |
| 6 | history | CYBERLEEK | $539.31 | take profit 50% | +$231.18 (+42.9%) | $2,181.88 | concept result |
| 7 | history | pippin | $356.64 | trail 40% | +$138.53 (+38.8%) | $2,320.41 | concept result |
| 8 | 1.171875 | CYBERLEEK | $387.88 | take profit 50% | +$210.62 (+54.3%) | $2,531.03 | concept result |
| 9 | 4.6875 | FIONA | $536.13 | take profit 50% | +$212.35 (+39.6%) | $2,743.38 | real candle close #49 (0.00128409) |
| 10 | 7.03125 | pippin | $567.98 | -23% stop | -$129.15 (-22.7%) | $2,614.23 | concept result |
| 11 | 7.734375 | FIONA | $536.13 | trail 40% | +$412.28 (+76.9%) | $3,026.51 | real candle close #66 (0.00162708) |
| 12 | 8.4375 | CLAUDIA | $914.36 | take profit 50% | +$166.66 (+18.2%) | $3,193.17 | concept result |
| 13 | 10.3125 | GATO | $573.25 | take profit 50% | +$468.92 (+81.8%) | $3,662.09 | concept result |
| 14 | 12.65625 | mihao | $1,175.17 | take profit 100% | +$602.63 (+51.3%) | $4,264.72 | concept result |

Check: $666.36 + Σ P&L +$3,598.36 = $4,264.72 (integer-cent chain verified).

## On-chain executions

- none: no wallet configured in config.json -> no verified executions are shown
- No trade in this video is presented as an on-chain execution.

## Request log

| Fetched at (UTC) | OK | Endpoint |
|---|---|---|
| 2026-11-21T02:22:02Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/trending_pools` |
| 2026-11-21T02:22:02Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB` |
| 2026-11-21T02:22:02Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-21T02:22:03Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/5E3dXLXGwmTDCokA51WYYaKttjFZBwqCoyUHBUi5gt2m` |
| 2026-11-21T02:22:03Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-21T02:22:04Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/G8kgi7aUpeX8EVR8VMkrth9SKEv5BietWC33UjAiiMGh` |
| 2026-11-21T02:22:04Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-21T02:22:05Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/FJk9sajdc2Q4heRPPu3yLzkmf2ZByZkpiHQLv9e2bn5A` |
| 2026-11-21T02:22:06Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-21T02:22:06Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt` |
| 2026-11-21T02:22:06Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-21T02:22:07Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz` |
| 2026-11-21T02:22:07Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-21T02:22:08Z | ✓ | `https://api.dexscreener.com/latest/dex/pairs/solana/Fe7bpDYCs74GqiCUF14HwgUMToPKV1d9mDYVX5BTohFr` |
| 2026-11-21T02:22:08Z | ✓ | `https://api.mainnet-beta.solana.com` |
| 2026-11-21T02:22:11Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/DjbLtX1HRGZZrJgJ7CwTX6SN3D7tBLiytkGwomBUwTVB/ohlcv/minute` |
| 2026-11-21T02:22:12Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/5E3dXLXGwmTDCokA51WYYaKttjFZBwqCoyUHBUi5gt2m/ohlcv/minute` |
| 2026-11-21T02:22:13Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/G8kgi7aUpeX8EVR8VMkrth9SKEv5BietWC33UjAiiMGh/ohlcv/minute` |
| 2026-11-21T02:22:15Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt/ohlcv/minute` |
| 2026-11-21T02:22:18Z | ✓ | `https://api.geckoterminal.com/api/v2/networks/solana/pools/Ho1aSG6WGH1FfXdEHrK2f4Ggt1Hoxo9s5jcLMDqeyeBz/ohlcv/minute` |
