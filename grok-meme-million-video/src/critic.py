#!/usr/bin/env python3
"""GROK MEME MILLION V1.8.3 - automated Visual Critic.

Compares the render with the reference video and gates delivery.
Exit code 1 = REJECTED (critical defect). Writes output/critic_report.{json,md}
plus output/compare_sheet.png (reference vs. new at 8 matched timestamps).
"""
import json, os, sys, subprocess, math, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "output")
CFG = json.load(open(os.path.join(ROOT, "config.json")))
SC = json.load(open(os.path.join(ROOT, "data", "scenario.json")))
SNAP = json.load(open(os.path.join(ROOT, "data", "market_snapshot.json")))
W, H, FPS, DUR = CFG["video"]["width"], CFG["video"]["height"], CFG["video"]["fps"], CFG["video"]["duration"]
NFR = int(FPS * DUR)
TS = [0.6, 2.0, 3.6, 4.9, 7.0, 8.4, 10.6, 13.2, 14.7]


def ffprobe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", p], capture_output=True, text=True)
    return json.loads(r.stdout)


def frames_gray(p, w=135, h=240):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", p, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)


def grab(p, t, w=None):
    vf = ["-vf", f"scale={w}:-2"] if w else []
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1", *vf, "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    import io
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def inter(a, b, pad=0):
    return not (a[2] <= b[0] + pad or a[0] >= b[2] - pad or a[3] <= b[1] + pad or a[1] >= b[3] - pad)


def visual_stats(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    g = a.mean(2)
    gx = np.abs(np.diff(g, axis=1)).mean(); gy = np.abs(np.diff(g, axis=0)).mean()
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]
    green = ((gg > r + 40) & (gg > b + 10)).mean()
    red = ((r > gg + 50) & (r > b + 30)).mean()
    return {"luma": float(g.mean()), "edge_density": float(gx + gy), "green_share": float(green), "red_share": float(red),
            "dark_share": float((g < 30).mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=os.path.join(OUT, "grok_meme_million_v1.8.3.mp4"))
    ap.add_argument("--ref", required=True)
    a = ap.parse_args()
    crit, warn, checks = [], [], []

    def check(name, ok, detail, critical=True):
        checks.append({"check": name, "pass": bool(ok), "critical": critical, "detail": detail})
        if not ok:
            (crit if critical else warn).append(f"{name}: {detail}")

    # ---- A. technical
    pr = ffprobe(a.video)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    au = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
    check("resolution 1080x1920", (v["width"], v["height"]) == (1080, 1920), f'{v["width"]}x{v["height"]}')
    check("frame rate 30", v["r_frame_rate"] == "30/1", v["r_frame_rate"])
    check("codec H.264", v["codec_name"] == "h264", v["codec_name"])
    nb = int(v.get("nb_read_frames", 0))
    check("frame count 450 (no missing frames)", nb == NFR, f"{nb} frames")
    dur = float(pr["format"]["duration"])
    check("duration 15.0 s", abs(dur - DUR) < 0.05, f"{dur:.3f}s")
    check("audio AAC stereo 48 kHz", au is not None and au["codec_name"] == "aac" and au["sample_rate"] == "48000" and au["channels"] == 2,
          f'{au and au["codec_name"]} {au and au["sample_rate"]} {au and au["channels"]}ch')

    # ---- B. frozen / duplicated frames
    fr = frames_gray(a.video)
    d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
    dup = int((d < 0.02).sum())
    run, worst = 0, 0
    for x in d:
        run = run + 1 if x < 0.08 else 0
        worst = max(worst, run)
    check("no duplicated frames", dup == 0, f"{dup} near-identical consecutive pairs; min diff {d.min():.3f}")
    check("no frozen stretch > 0.5 s", worst < 15, f"longest low-motion run {worst} frames")

    # ---- C. layout registry (text overlap / clipping / chart labels / markers)
    reg = json.load(open(os.path.join(OUT, "layout_registry.json")))
    overlaps, offscreen, outbox, label_hits, small = [], [], [], [], []
    seen_buy = seen_sell = 0
    live_frames = 0
    min_px = 999
    for fi, items in reg.items():
        fi = int(fi)
        texts = [x for x in items if x["rect"] and x["kind"] not in ("icon",)]
        for x in texts:
            r = x["rect"]
            hpx = x.get("size") or 99
            if x["kind"] != "title" and r[1] > 0 and r[3] < H:
                min_px = min(min_px, hpx)
            if r[3] > 0 and r[1] < H and (r[0] < -1 or r[2] > W + 1):
                offscreen.append((fi, x["text"]))
            cbox = x.get("container")
            if cbox and cbox[1] >= 0 and cbox[3] <= H and (r[0] < cbox[0] - 2 or r[2] > cbox[2] + 2):
                outbox.append((fi, x["text"]))
        by_layer = {}
        for x in texts:
            if 0 < x["rect"][3] and x["rect"][1] < H and x["layer"] not in ("banner_out", "page_anim"):
                by_layer.setdefault(x["layer"], []).append(x)
        for lay, xs in by_layer.items():
            for i in range(len(xs)):
                for j in range(i + 1, len(xs)):
                    if inter(xs[i]["rect"], xs[j]["rect"], pad=3):
                        overlaps.append((fi, lay, xs[i]["text"], xs[j]["text"]))
        cs = next((x for x in items if x["kind"] == "candles"), None)
        if cs:
            pl = cs["plot"]
            if 0 < pl[1] < H:
                live_frames += 1
            labels = [x for x in texts if x["kind"] == "chart_label"]
            tri = next((x for x in items if x["kind"] == "triangles"), {"tris": []})["tris"]
            for lb in labels:
                for cr in cs["candles"] + tri:
                    if inter(lb["rect"], cr, pad=1):
                        label_hits.append((fi, lb["text"]))
                        break
            if 0 < pl[1] < H and 0 < pl[3] < H:
                seen_buy += "BUY" in cs["markers_visible"]
                seen_sell += "SELL" in cs["markers_visible"]
    check("no overlapping text (same layer)", len(overlaps) == 0, f"{len(overlaps)} overlaps" + (f", e.g. {overlaps[:3]}" if overlaps else ""))
    check("no horizontally clipped text", len(offscreen) == 0, f"{len(offscreen)} cases" + (f", e.g. {offscreen[:3]}" if offscreen else ""))
    check("text inside its card/pill", len(outbox) == 0, f"{len(outbox)} cases" + (f", e.g. {outbox[:3]}" if outbox else ""))
    check("BUY/SELL labels never cover candles or markers", len(label_hits) == 0, f"{len(label_hits)} hits")
    check("chart visible", live_frames >= 150, f"{live_frames} frames with the candle plot on screen")
    check("BUY marker visible", seen_buy >= 30, f"{seen_buy} frames")
    check("SELL marker visible", seen_sell >= 30, f"{seen_sell} frames")
    check("minimum on-screen font size >= 22 px", min_px >= 22, f"smallest font {min_px:.0f} px (1080x1920 native)")

    # ---- D. calculations
    cap, fin = SC["initial_capital_c"], SC["final_equity_c"]
    chain = cap
    ok = True
    for t in SC["trades"]:
        ok &= t["equity_before_c"] == chain
        chain += t["pnl_c"]
        ok &= t["equity_after_c"] == chain
        ok &= abs(t["pct"] - t["pnl_c"] / t["size_c"]) < 1e-9
    check("equity chain = capital + sum(trade P&L)", ok and chain == fin, f"${cap/100:.2f} + ${(fin-cap)/100:.2f} = ${fin/100:.2f}")
    check("ROI and multiple", abs(SC["roi_pct"] - (fin - cap) / cap * 100) < 1e-9 and abs(SC["multiple"] - fin / cap) < 1e-9,
          f"ROI {SC['roi_pct']:.2f}% · {SC['multiple']:.2f}x")
    lo, hi = CFG["scenario"]["initial_capital_range"]
    check("initial capital in $500-$700", lo * 100 <= cap <= hi * 100, f"${cap/100:.2f}")
    lo, hi = CFG["scenario"]["final_profit_range"]
    check("final profit in $1,000-$5,000", lo * 100 <= fin - cap <= hi * 100, f"${(fin-cap)/100:.2f}")
    mags = [abs(t["pnl_c"]) / 100 for t in SC["trades"]]
    check("trade results tens-hundreds of $", all(8 <= m <= 1500 for m in mags), f"min ${min(mags):.2f}, max ${max(mags):.2f}", critical=False)
    final_txt = "$" + f"{fin/100:,.2f}"
    last = reg[str(NFR - 1)]
    check("final equity shown on last frame", any(x["text"] == final_txt for x in last), final_txt)
    early = [x["text"] for fi in range(0, 300) for x in reg[str(fi)] if x["text"] == final_txt]
    check("final profit not revealed early (<10 s)", len(early) == 0, f"{len(early)} early occurrences")

    # ---- E. provenance
    wl = SNAP["watchlist"]
    check("watchlist verified by mint+pool (DEX Screener + RPC)", all(w["verified"] and w["verify"]["dexscreener"]["pair_match"] and w["verify"]["solana_rpc"]["ok"] for w in wl),
          f"{len(wl)} tokens: " + ", ".join(f"{w['symbol']}({w['mint'][:4]}…/{w['pool'][:4]}…)" for w in wl))
    oh = SNAP["hero_ohlcv"]
    if SC["real_chart"]:
        src = {c["t"]: c for c in oh["candles"]}
        same = all(src.get(c["t"]) == c for c in SC["hero"]["candles"])
        check("chart candles are byte-identical real OHLCV", same, f"{len(SC['hero']['candles'])} candles from {oh['source']} pool {oh['pool']}")
        hc = SC["hero"]["candles"]
        okp = all(abs(t["price"] - hc[t["idx"]]["c"]) < 1e-15 for t in SC["trades"] if t.get("hero"))
        check("hero trade prices = real candle closes", okp, "entry/exit at candle closes")
    else:
        alltxt = {x["text"] for fi in reg for x in reg[fi]}
        check("concept chart clearly labelled", "CONCEPT / SOL" in alltxt, "no OHLCV -> concept chart")
    check("snapshot not presented as realtime", SNAP["realtime"] is False, f"snapshot {SNAP['snapshot_finished_at']}")
    bad = sorted({x["text"] for fi in reg for x in reg[fi] if any(k in x["text"].lower() for k in ("realtime", "real-time", "live price", "verified execution", "on-chain fill"))})
    check("no unsupported live/on-chain claims in UI text", not bad, f"{bad}")
    lab_frames = sum(1 for fi in reg if any(k in x["text"] for x in reg[fi] for k in ("CONCEPT", "concept", "Paper", "paper")))
    check("concept/paper labelling on screen", lab_frames >= NFR * 0.95, f"{lab_frames}/{NFR} frames")
    check("on-chain executions separated", SNAP["onchain_executions"]["status"] in ("none", "verified"), SNAP["onchain_executions"]["reason"])

    # ---- F. audio sync (onset within window of every event)
    wav = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", a.video, "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
    xs = np.frombuffer(wav, np.float32).reshape(-1, 2)
    peak = np.abs(xs).max()
    x = xs.mean(1)
    hpx = x - np.convolve(x, np.ones(24) / 24, "same")
    win = 480
    e = np.sqrt(np.convolve(hpx ** 2, np.ones(win) / win, "same"))
    sync = []
    for ev in json.load(open(os.path.join(OUT, "timeline.json")))["events"]:
        i0 = int(ev["t"] * 48000)
        before = e[max(0, i0 - 9600):i0 - 480].mean()
        after = e[i0:i0 + 7200].max()
        sync.append({"t": ev["t"], "type": ev["type"], "rise_db": round(20 * math.log10((after + 1e-9) / (before + 1e-9)), 1)})
    check("SFX onset at every trade event", all(s["rise_db"] > 3 for s in sync), "; ".join(f'{s["t"]}s {s["type"]} +{s["rise_db"]}dB' for s in sync))
    check("audio not clipping", peak < 0.999, f"peak {20*math.log10(peak):.2f} dBFS")

    # ---- G. reference comparison + contact sheets
    rpr = ffprobe(a.ref)
    rdur = float(rpr["format"]["duration"])
    pairs = []
    font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 26)
    sheet = Image.new("RGB", (len(TS) * 380, 2 * 680 + 80), (8, 10, 11))
    dr = ImageDraw.Draw(sheet)
    for k, t in enumerate(TS):
        tr = t * rdur / DUR
        ri = grab(a.ref, tr).resize((312, 680))
        ni = grab(a.video, t).resize((382, 680)).crop((35, 0, 347, 680))
        sheet.paste(ri, (k * 380 + 34, 40)); sheet.paste(grab(a.video, t).resize((382, 680)), (k * 380, 720 + 40))
        dr.text((k * 380 + 34, 6), f"REF {tr:.1f}s", fill=(160, 173, 183), font=font)
        dr.text((k * 380 + 34, 726), f"NEW {t:.1f}s", fill=(32, 213, 139), font=font)
        rs, ns = visual_stats(grab(a.ref, tr, 540)), visual_stats(grab(a.video, t, 540))
        pairs.append({"t_new": t, "t_ref": round(tr, 2), "ref": rs, "new": ns})
    sheet.save(os.path.join(OUT, "compare_sheet.png"))
    agg = {k: (np.mean([p["ref"][k] for p in pairs]), np.mean([p["new"][k] for p in pairs])) for k in pairs[0]["ref"]}
    dens = agg["edge_density"][1] / agg["edge_density"][0]
    check("visual density close to reference (0.6-1.6x)", 0.6 <= dens <= 1.6, f"edge density ratio {dens:.2f}", critical=False)
    check("dark premium palette like reference", abs(agg["dark_share"][1] - agg["dark_share"][0]) < .2,
          f"dark share ref {agg['dark_share'][0]:.2f} vs new {agg['dark_share'][1]:.2f}", critical=False)

    # contact sheet of the new render (16 frames)
    cs = Image.new("RGB", (8 * 270, 2 * 480), (0, 0, 0))
    for k in range(16):
        t = k * DUR / 16 + .45
        cs.paste(grab(a.video, t).resize((270, 480)), ((k % 8) * 270, (k // 8) * 480))
    cs.save(os.path.join(OUT, "contact_sheet.png"))
    grab(a.video, 13.3).save(os.path.join(OUT, "preview_1080x1920.png"))
    grab(a.video, 5.0).save(os.path.join(OUT, "preview_live_1080x1920.png"))

    n_ok = sum(c["pass"] for c in checks)
    score = round(10 - 1.5 * len(crit) - 0.3 * len(warn), 1)
    rep = {"video": os.path.basename(a.video), "reference": os.path.basename(a.ref), "verdict": "REJECTED" if crit else "ACCEPTED",
           "auto_score": score, "checks_passed": f"{n_ok}/{len(checks)}", "critical": crit, "warnings": warn, "checks": checks,
           "audio_sync": sync, "reference_comparison": {"timestamps": pairs, "means": {k: {"ref": round(v[0], 3), "new": round(v[1], 3)} for k, v in agg.items()}},
           "min_text_px": round(min_px, 1)}
    json.dump(rep, open(os.path.join(OUT, "critic_report.json"), "w"), indent=1)
    print(json.dumps({k: rep[k] for k in ("verdict", "auto_score", "checks_passed", "critical", "warnings")}, indent=1))
    sys.exit(1 if crit else 0)


if __name__ == "__main__":
    main()
