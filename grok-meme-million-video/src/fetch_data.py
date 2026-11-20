#!/usr/bin/env python3
"""GROK MEME MILLION V1.8.4 - market data layer.

Builds a verified Solana meme-token watchlist + real OHLCV for the hero pool.

Rules enforced here (see SKILL.md, section "Data provenance"):
  * Tokens are identified by mint address AND pool address, never by ticker.
  * Every watchlist pool is fetched from GeckoTerminal and cross-checked
    against DEX Screener (same pool -> same base mint, price within tolerance).
  * Each mint is checked on Solana RPC to be a real SPL / Token-2022 mint.
  * Candles are only ever real OHLCV from the hero pool. If OHLCV cannot be
    fetched, `ohlcv.status` is "unavailable" and the renderer switches to a
    clearly labelled CONCEPT CHART instead of inventing market candles.
  * Every request is logged with its UTC timestamp in data/market_snapshot.json.
"""
import json, os, sys, time, datetime as dt, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(ROOT, "config.json")))
DCFG = CFG["data"]
SOL_MINT = "So11111111111111111111111111111111111111112"
TOKEN_PROGRAMS = {"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": "spl-token",
                  "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb": "token-2022"}
UA = {"User-Agent": "grok-meme-million-video/1.8.3", "Accept": "application/json"}
LOG = []


def now_iso():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, data=None, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=dict(UA, **({"Content-Type": "application/json"} if data else {})))
            with urllib.request.urlopen(req, timeout=25) as r:
                body = json.loads(r.read())
            LOG.append({"url": url.split("?")[0] if data is None else url, "fetched_at": now_iso(), "ok": True})
            return body
        except Exception as e:  # noqa
            err = str(e)
            time.sleep(2 + 3 * i)
    LOG.append({"url": url, "fetched_at": now_iso(), "ok": False, "error": err})
    return None


def fnum(x, d=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def rpc_mint_check(mint):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getAccountInfo",
                       "params": [mint, {"encoding": "jsonParsed"}]}).encode()
    r = get(DCFG["solana_rpc"], data=body)
    try:
        v = r["result"]["value"]
        owner = v["owner"]
        info = v["data"]["parsed"]["info"]
        return {"ok": owner in TOKEN_PROGRAMS and v["data"]["parsed"]["type"] == "mint",
                "program": TOKEN_PROGRAMS.get(owner, owner), "decimals": info.get("decimals"),
                "supply_raw": info.get("supply"), "checked_at": now_iso()}
    except Exception:
        return {"ok": False, "checked_at": now_iso(), "error": "rpc unavailable or not a mint"}


def dexscreener_check(pool, mint, gt_price):
    r = get(f"https://api.dexscreener.com/latest/dex/pairs/solana/{pool}")
    pairs = (r or {}).get("pairs") or []
    if not pairs:
        return {"ok": False, "reason": "pool not found on DEX Screener", "checked_at": now_iso()}
    p = pairs[0]
    ds_price = fnum(p.get("priceUsd"))
    dev = abs(ds_price - gt_price) / gt_price if gt_price else 1
    same = p.get("pairAddress") == pool and p.get("baseToken", {}).get("address") == mint
    return {"ok": bool(same and dev <= DCFG["max_price_deviation"]), "pair_match": same,
            "price_usd": ds_price, "price_deviation": round(dev, 4),
            "liquidity_usd": fnum((p.get("liquidity") or {}).get("usd")),
            "volume_h24": fnum((p.get("volume") or {}).get("h24")),
            "price_change_h24": fnum((p.get("priceChange") or {}).get("h24")),
            "market_cap": fnum(p.get("marketCap") or p.get("fdv")),
            "image_url": (p.get("info") or {}).get("imageUrl"),
            "dex_id": p.get("dexId"), "url": p.get("url"), "checked_at": now_iso()}


def download_logo(urls, mint):
    path = os.path.join(ROOT, "assets", "logos", f"{mint}.png")
    for u in urls:
        if not u or "missing" in u:
            continue
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA["User-Agent"]})
            with urllib.request.urlopen(req, timeout=20) as r:
                raw = r.read()
            from PIL import Image
            import io
            im = Image.open(io.BytesIO(raw)).convert("RGBA").resize((128, 128), Image.LANCZOS)
            im.save(path)
            return {"file": os.path.relpath(path, ROOT), "source": u}
        except Exception:
            continue
    return None


def main():
    snap_started = now_iso()
    tp = get("https://api.geckoterminal.com/api/v2/networks/solana/trending_pools"
             "?duration=24h&include=base_token,quote_token,dex&page=1")
    if not tp:
        sys.exit("ERROR: GeckoTerminal trending_pools unavailable - refusing to build without verified data")
    inc = {(i["type"], i["id"]): i["attributes"] for i in tp.get("included", [])}
    cands, seen = [], set()
    for p in tp["data"]:
        a, rel = p["attributes"], p["relationships"]
        base = inc.get(("token", rel["base_token"]["data"]["id"]), {})
        quote = inc.get(("token", rel["quote_token"]["data"]["id"]), {})
        mint = base.get("address")
        if not mint or quote.get("address") != SOL_MINT or mint in seen:
            continue
        liq, vol = fnum(a["reserve_in_usd"]), fnum(a["volume_usd"]["h24"])
        if liq < DCFG["min_liquidity_usd"] or vol < DCFG["min_volume_h24_usd"]:
            continue
        if base.get("symbol", "").upper() in DCFG["exclude_symbols"]:
            continue
        seen.add(mint)
        cands.append({"symbol": base.get("symbol"), "name": base.get("name"), "mint": mint,
                      "pool": a["address"], "pair": a["name"], "dex": rel["dex"]["data"]["id"],
                      "price_usd": fnum(a["base_token_price_usd"]),
                      "price_change_h24": fnum(a["price_change_percentage"]["h24"]),
                      "volume_h24": vol, "liquidity_usd": liq,
                      "market_cap": fnum(a.get("market_cap_usd") or a.get("fdv_usd")),
                      "fdv_usd": fnum(a.get("fdv_usd")), "pool_created_at": a.get("pool_created_at"),
                      "gt_image": base.get("image_url"), "source": "geckoterminal.trending_pools(24h)"})
    watch = []
    for c in cands:
        if len(watch) >= DCFG["watchlist_size"]:
            break
        ds = dexscreener_check(c["pool"], c["mint"], c["price_usd"])
        rpc = rpc_mint_check(c["mint"])
        c["verify"] = {"dexscreener": ds, "solana_rpc": rpc}
        c["verified"] = bool(ds["ok"] and rpc["ok"])
        if not c["verified"]:
            print("skip (unverified):", c["symbol"], c["mint"], ds.get("reason") or ds.get("price_deviation"), rpc.get("ok"))
            continue
        c["logo"] = download_logo([c.get("gt_image"), ds.get("image_url")], c["mint"])
        watch.append(c)
        print("verified:", c["symbol"], c["pool"], c["price_usd"], c["price_change_h24"])
        time.sleep(0.6)
    if len(watch) < 3:
        sys.exit("ERROR: fewer than 3 verified tokens - refusing to render market data")

    # Hero pool: real OHLCV. Fetch candidates, pick the one whose REAL candles
    # contain the clearest tradable structure (same search the scenario uses).
    sys.path.insert(0, HERE)
    from scenario import pick_hero_trades
    hero, best, sets = None, None, []
    for c in watch[:5]:
        o = get(f"https://api.geckoterminal.com/api/v2/networks/solana/pools/{c['pool']}/ohlcv/"
                f"minute?aggregate={DCFG['ohlcv_aggregate_min']}&limit={DCFG['ohlcv_limit']}&currency=usd&token=base")
        rows = sorted(((o or {}).get("data") or {}).get("attributes", {}).get("ohlcv_list") or [], key=lambda r: r[0])
        rows = [r for r in rows if min(r[1:5]) > 0]
        fetched = now_iso()
        if len(rows) < DCFG["min_candles"]:
            sets.append({"symbol": c["symbol"], "pool": c["pool"], "candles": len(rows), "used": False})
            continue
        cs = [{"t": int(r[0]), "o": r[1], "h": r[2], "l": r[3], "c": r[4], "v": r[5]} for r in rows]
        score = pick_hero_trades(cs, return_score=True)[0]
        sets.append({"symbol": c["symbol"], "pool": c["pool"], "candles": len(rows), "score": round(score, 3)})
        if best is None or score > best:
            best, hero = score, {"symbol": c["symbol"], "mint": c["mint"], "pool": c["pool"], "candles": cs, "fetched_at": fetched}
        time.sleep(0.6)
    ohlcv = {"status": "unavailable", "candidates": sets}
    if hero:
        ohlcv = {"status": "verified", "source": "GeckoTerminal /networks/solana/pools/{pool}/ohlcv/minute",
                 "aggregate_minutes": DCFG["ohlcv_aggregate_min"], "symbol": hero["symbol"],
                 "mint": hero["mint"], "pool": hero["pool"], "fetched_at": hero["fetched_at"],
                 "candidates": sets, "candles": hero["candles"]}
    snap = {"schema": "grok-meme-million/market-snapshot@1.8.3", "network": "solana",
            "snapshot_started_at": snap_started, "snapshot_finished_at": now_iso(),
            "realtime": False,
            "note": "Point-in-time snapshot. The video labels it as a snapshot/replay, never as realtime.",
            "watchlist": watch, "hero_ohlcv": ohlcv,
            "onchain_executions": {"status": "none", "reason": "no wallet configured in config.json -> no verified executions are shown"},
            "request_log": LOG}
    out = os.path.join(ROOT, "data", "market_snapshot.json")
    json.dump(snap, open(out, "w"), indent=1)
    print("wrote", out, "hero:", ohlcv.get("symbol"), len(ohlcv.get("candles", [])), "candles")


if __name__ == "__main__":
    main()
