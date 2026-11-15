#!/usr/bin/env python3
"""Lớp hiệu ứng thứ hai cho video đã dựng (sau edit_video.py render):
khung viền + góc trang trí, thanh tiến độ, tấm minh hoạ bật theo lời nói,
chớp sáng chuyển phần, và âm thanh hiệu ứng (whoosh / ding / pop) tự tổng hợp, không bản quyền.

  python3 fanpage/tools/minh_hoa.py VIDEO_DUNG.mp4 transcript.json edit_plan.json minh_hoa.json OUT.mp4

minh_hoa.json:
{
  "layout": "split",                       # bỏ đi nếu video quay dọc (tấm nằm dưới); "split" = tấm nằm nửa trên
  "theme": {"accent": [214,178,94], "bg": [12,30,24]},
  "sfx": true,                             # whoosh khi thẻ chữ edit_plan bật, ding/pop khi tấm minh hoạ bật
  "panels": [
    {"type": "nhan_vat", "trigger": "thứ nhất", "sec": 8, "title": "① GIAO VIỆC 1 CÂU", "arrows": true, "flash": true,
     "items": [{"name": "ANH", "role": "Ra lệnh", "me": true}, {"name": "MINH", "role": "Chia việc"}]},
    {"type": "trich_dan", "trigger": "người xưa dạy", "sec": 7, "title": "☯ ĐẠO",
     "text": "Thắng người là có sức, thắng mình mới là mạnh.", "source": "Đạo Đức Kinh, ch. 33"},
    {"type": "minh_hoa", "trigger": "đám đông", "sec": 6, "icon": "dam_dong", "title": "NGƯỢC ĐÁM ĐÔNG",
     "text": "nhưng có kế hoạch"}
  ]
}
Icon cho "minh_hoa": bieu_do_tang, bieu_do_giam, dam_dong, trai_tim, dong_ho, khien, can_can, mat_troi, ngon_nen, nha.
"trigger" là cụm lời nói thật (sau khi sửa transcript); hoặc "at" = giây trên video gốc.
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from edit_video import keep_segments, remap, find_trigger, FONT_B, FONT_R  # noqa

W, H = 1080, 1920
SR = 48000
GREEN = (46, 150, 112)


def font(path, size):
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------------ khung, thanh tiến độ
def frame_png(path, acc):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 18, W - 18, H - 18), radius=46, outline=acc + (230,), width=6)
    d.rounded_rectangle((30, 30, W - 30, H - 30), radius=38, outline=acc + (90,), width=2)
    for cx, cy, sx, sy in [(60, 60, 1, 1), (W - 60, 60, -1, 1), (60, H - 60, 1, -1), (W - 60, H - 60, -1, -1)]:
        d.line([(cx, cy + sy * 70), (cx, cy), (cx + sx * 70, cy)], fill=acc + (255,), width=8)
        d.ellipse((cx + sx * 14 - 7, cy + sy * 14 - 7, cx + sx * 14 + 7, cy + sy * 14 + 7), fill=acc + (255,))
    im.save(path)


def solid_png(path, w, h, rgba):
    Image.new("RGBA", (w, h), rgba).save(path)


# ------------------------------------------------------------------ icon vẽ tay
def draw_icon(d, name, cx, cy, s, acc):
    a = acc + (255,)
    wht = (255, 255, 255, 255)
    if name in ("bieu_do_tang", "bieu_do_giam"):
        up = name == "bieu_do_tang"
        vals = [0.3, 0.45, 0.4, 0.6, 0.55, 0.8] if up else [0.8, 0.65, 0.7, 0.45, 0.5, 0.25]
        bw = s * 0.22
        for i, v in enumerate(vals):
            x = cx - s + i * s * 0.38
            top = cy + s * 0.8 - v * s * 1.6
            col = GREEN + (255,) if (vals[i] >= vals[i - 1] if i else up) else (196, 72, 60, 255)
            d.line([(x + bw / 2, top - s * 0.12), (x + bw / 2, cy + s * 0.8 + s * 0.05)], fill=col, width=4)
            d.rectangle((x, top, x + bw, top + s * 0.3), fill=col)
        d.line([(cx - s, cy + s * 0.9), (cx + s, cy + s * 0.9)], fill=wht, width=4)
    elif name == "dam_dong":
        for i, (dx, dy, r) in enumerate([(-0.7, 0.15, 0.3), (0.7, 0.15, 0.3), (0, 0, 0.38)]):
            x, y = cx + dx * s, cy + dy * s
            col = a if i == 2 else (200, 210, 205, 230)
            d.ellipse((x - r * s * 0.6, y - s * 0.75, x + r * s * 0.6, y - s * 0.75 + r * s * 1.2), fill=col)
            d.pieslice((x - r * s * 1.2, y - s * 0.05, x + r * s * 1.2, y + s * 1.2), 180, 360, fill=col)
    elif name == "trai_tim":
        r = s * 0.5
        d.ellipse((cx - s, cy - s * 0.7, cx, cy + s * 0.3), fill=a)
        d.ellipse((cx, cy - s * 0.7, cx + s, cy + s * 0.3), fill=a)
        d.polygon([(cx - s * 0.97, cy - s * 0.05), (cx + s * 0.97, cy - s * 0.05), (cx, cy + s)], fill=a)
    elif name == "dong_ho":
        d.ellipse((cx - s, cy - s, cx + s, cy + s), outline=a, width=10)
        d.line([(cx, cy), (cx, cy - s * 0.65)], fill=wht, width=9)
        d.line([(cx, cy), (cx + s * 0.45, cy + s * 0.2)], fill=wht, width=9)
        for k in range(12):
            ang = k * math.pi / 6
            d.ellipse((cx + math.sin(ang) * s * 0.82 - 5, cy - math.cos(ang) * s * 0.82 - 5,
                       cx + math.sin(ang) * s * 0.82 + 5, cy - math.cos(ang) * s * 0.82 + 5), fill=a)
    elif name == "khien":
        d.polygon([(cx, cy - s), (cx + s * 0.85, cy - s * 0.6), (cx + s * 0.7, cy + s * 0.4), (cx, cy + s),
                   (cx - s * 0.7, cy + s * 0.4), (cx - s * 0.85, cy - s * 0.6)], fill=a)
        d.line([(cx - s * 0.35, cy), (cx - s * 0.05, cy + s * 0.3), (cx + s * 0.4, cy - s * 0.3)], fill=wht, width=12)
    elif name == "can_can":
        d.line([(cx, cy - s * 0.9), (cx, cy + s * 0.8)], fill=a, width=10)
        d.line([(cx - s, cy - s * 0.6), (cx + s, cy - s * 0.6)], fill=a, width=10)
        d.rectangle((cx - s * 0.5, cy + s * 0.8, cx + s * 0.5, cy + s * 0.95), fill=a)
        for sx in (-1, 1):
            x = cx + sx * s
            d.line([(x, cy - s * 0.6), (x - s * 0.3, cy + s * 0.1)], fill=wht, width=4)
            d.line([(x, cy - s * 0.6), (x + s * 0.3, cy + s * 0.1)], fill=wht, width=4)
            d.chord((x - s * 0.35, cy - s * 0.15, x + s * 0.35, cy + s * 0.35), 0, 180, fill=wht)
    elif name == "mat_troi":
        d.ellipse((cx - s * 0.5, cy - s * 0.5, cx + s * 0.5, cy + s * 0.5), fill=a)
        for k in range(10):
            ang = k * math.pi / 5
            d.line([(cx + math.cos(ang) * s * 0.65, cy + math.sin(ang) * s * 0.65),
                    (cx + math.cos(ang) * s, cy + math.sin(ang) * s)], fill=a, width=9)
    elif name == "ngon_nen":
        d.rectangle((cx - s * 0.3, cy - s * 0.1, cx + s * 0.3, cy + s), fill=wht)
        d.ellipse((cx - s * 0.22, cy - s * 0.85, cx + s * 0.22, cy - s * 0.15), fill=a)
    elif name == "nha":
        d.polygon([(cx - s, cy - s * 0.05), (cx, cy - s), (cx + s, cy - s * 0.05)], fill=a)
        d.rectangle((cx - s * 0.7, cy - s * 0.05, cx + s * 0.7, cy + s * 0.9), fill=wht)
        d.rectangle((cx - s * 0.18, cy + s * 0.35, cx + s * 0.18, cy + s * 0.9), fill=a)
    else:
        d.ellipse((cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6), fill=a)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    return lines + ([cur] if cur else [])


# ------------------------------------------------------------------ tấm minh hoạ
def panel_png(path, p, acc, bg):
    ph = 380
    im = Image.new("RGBA", (W, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 0, W - 40, ph - 6), radius=34, fill=bg + (228,), outline=acc + (255,), width=4)
    if p.get("title"):
        d.text((W / 2, 46), p["title"], font=font(FONT_B, 42), fill=acc + (255,), anchor="mm")
    kind = p.get("type", "nhan_vat")
    if kind == "trich_dan":
        f = font(FONT_B, 50)
        lines = wrap(d, "“" + p.get("text", "") + "”", f, W - 200)[:3]
        y = 95 + (3 - len(lines)) * 30
        for ln in lines:
            d.text((W / 2, y), ln, font=f, fill=(255, 255, 255, 255), anchor="ma"); y += 66
        if p.get("source"):
            d.text((W / 2, ph - 50), "— " + p["source"], font=font(FONT_R, 30), fill=acc + (255,), anchor="mm")
    elif kind == "minh_hoa":
        draw_icon(d, p.get("icon", ""), 230, 205, 110, acc)
        f = font(FONT_B, 54)
        lines = wrap(d, p.get("text", ""), f, W - 520)[:3]
        y = 205 - len(lines) * 33
        for ln in lines:
            d.text((400, y), ln, font=f, fill=(255, 255, 255, 255), anchor="la"); y += 66
    else:
        items = p.get("items", [])
        n = max(1, len(items))
        slot = (W - 120) / n
        r = min(62, int(slot * 0.36))
        for i, it in enumerate(items):
            cx, cy = 60 + slot * (i + 0.5), 165
            on, me = it.get("on", True), it.get("me", False)
            fill = (acc + (255,)) if (on and me) else (GREEN + (255,) if on else (70, 82, 76, 200))
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=(255, 255, 255, 200 if on else 80), width=3)
            if it.get("icon_ve"):
                draw_icon(d, it["icon_ve"], cx, cy, r * 0.6, (255, 255, 255))
            else:
                lab = it.get("icon") or it["name"][0]
                d.text((cx, cy), lab, font=font(FONT_B, int(r * 0.9)), fill=(255, 255, 255, 255 if on else 140), anchor="mm")
            col = (255, 255, 255, 255) if on else (200, 210, 205, 130)
            d.text((cx, cy + r + 30), it["name"], font=font(FONT_B, 30 if n <= 5 else 24), fill=col, anchor="mm")
            d.text((cx, cy + r + 66), it.get("role", ""), font=font(FONT_R, 25 if n <= 5 else 19),
                   fill=(acc + (255,)) if on else (190, 200, 195, 110), anchor="mm")
            if p.get("arrows") and i < n - 1:
                ax = cx + slot / 2
                d.polygon([(ax - 14, cy - 16), (ax + 14, cy), (ax - 14, cy + 16)], fill=acc + (255,))
    im.save(path)


# ------------------------------------------------------------------ âm thanh hiệu ứng
def sfx(kind):
    if kind == "whoosh":
        n = int(0.45 * SR); t = np.arange(n) / SR
        x = np.random.default_rng(3).standard_normal(n)
        k = np.linspace(0.02, 0.35, n)  # lọc thông thấp mở dần
        y = np.zeros(n); acc = 0.0
        for i in range(n):
            acc += k[i] * (x[i] - acc); y[i] = acc
        y *= np.sin(np.pi * t / t[-1]) ** 2 * 1.6
    elif kind == "ding":
        n = int(1.2 * SR); t = np.arange(n) / SR
        y = (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 2637 * t) + 0.3 * np.sin(2 * np.pi * 1975 * t))
        y *= np.exp(-4 * t) * 0.35
    else:  # pop
        n = int(0.12 * SR); t = np.arange(n) / SR
        y = np.sin(2 * np.pi * (900 - 2500 * t) * t) * np.exp(-30 * t) * 0.6
    return np.stack([y, y], 1)


def build_sfx(events, dur, path):
    track = np.zeros((int((dur + 2) * SR), 2))
    for t0, kind in events:
        s = sfx(kind); i = int(t0 * SR)
        track[i:i + len(s)] += s[: len(track) - i]
    track = np.clip(track, -1, 1)
    (track * 32767).astype("<i2").tofile(path + ".raw")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", path + ".raw", path],
                   check=True)


# ------------------------------------------------------------------ ghép
def main(video, tr_json, plan_json, mh_json, out):
    tr, plan, mh = (json.load(open(f)) for f in (tr_json, plan_json, mh_json))
    _, segs = keep_segments(tr["words"], plan.get("cut_ranges", []), plan.get("max_pause", 0.45), tr["duration"])
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", video]).decode())
    th = mh.get("theme", {})
    acc, bg = tuple(th.get("accent", [214, 178, 94])), tuple(th.get("bg", [12, 30, 24]))
    split = mh.get("layout") == "split" or plan.get("layout") == "split"
    tmp = tempfile.mkdtemp()
    frame_png(f"{tmp}/frame.png", acc)
    solid_png(f"{tmp}/bar.png", W, 10, acc + (235,))
    solid_png(f"{tmp}/flash.png", W, H, (255, 255, 255, 255))
    inputs = ["-i", video, "-i", f"{tmp}/frame.png", "-i", f"{tmp}/bar.png",
              "-loop", "1", "-t", f"{dur:.3f}", "-i", f"{tmp}/flash.png"]
    filters = ["[0:v][1:v]overlay=0:0[v1]", f"[v1][2:v]overlay=x='-W+W*t/{dur:.3f}':y=H-34[v2]"]
    last, k, after, events, flashes = "v2", 4, 0.0, [], []
    # whoosh cho thẻ chữ của edit_plan (hook, các ý, CTA)
    if plan.get("hook_title"):
        events.append((0.05, "whoosh"))
    a2 = 0.0
    for c in plan.get("cards", []):
        src = c.get("at") if "at" in c else find_trigger(tr["words"], c.get("trigger", ""), a2)
        if src is not None:
            a2 = src; events.append((max(0, remap(src, segs) - 0.15), "whoosh"))
    for i, p in enumerate(mh.get("panels", [])):
        if "at" in p:
            t0 = remap(p["at"], segs)
        else:
            src = find_trigger(tr["words"], p["trigger"], after)
            if src is None:
                print("không thấy trigger:", p["trigger"]); continue
            after = src; t0 = remap(src, segs)
        t1 = min(dur - 4, t0 + p.get("sec", 7))
        png = f"{tmp}/p{i}.png"; panel_png(png, p, acc, bg)
        inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-i", png]
        y = p.get("y", 470 if split else 1450)
        filters.append(f"[{k}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.3:alpha=1,fade=t=out:st={t1 - 0.3:.2f}:d=0.3:alpha=1[p{i}]")
        filters.append(f"[{last}][p{i}]overlay=0:'{y}+40*max(0,1-(t-{t0:.2f})/0.3)':enable='between(t,{t0:.2f},{t1:.2f})'[v{k}]")
        last = f"v{k}"; k += 1
        events.append((t0, "ding" if p.get("type") in ("trich_dan", "minh_hoa") else "pop"))
        if p.get("flash"):
            flashes.append(t0)
        print(f"tấm {i}: {p.get('title', p.get('text', ''))[:40]} {t0:.1f}s → {t1:.1f}s")
    for j, t0 in enumerate(flashes):
        filters.append(f"[3:v]format=rgba,colorchannelmixer=aa=0.55,fade=t=in:st={t0 - 0.08:.2f}:d=0.08:alpha=1,"
                       f"fade=t=out:st={t0:.2f}:d=0.25:alpha=1[fl{j}]")
        filters.append(f"[{last}][fl{j}]overlay=0:0:enable='between(t,{t0 - 0.08:.2f},{t0 + 0.25:.2f})'[f{j}]")
        last = f"f{j}"
    amap = "0:a"
    if mh.get("sfx", True) and events:
        sp = f"{tmp}/sfx.wav"; build_sfx(events, dur, sp)
        inputs += ["-i", sp]
        filters.append(f"[{k}:a]volume={mh.get('sfx_volume', 0.5)}[sx];[0:a][sx]amix=inputs=2:duration=first:normalize=0[aout]")
        amap = "[aout]"
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", f"[{last}]",
           "-map", amap, "-c:v", "libx264", "-crf", "25", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
           "-movflags", "+faststart", "-t", f"{dur:.3f}", out]
    subprocess.run(cmd, check=True)
    print("OK", out, f"({len(events)} âm thanh hiệu ứng, {len(flashes)} chớp sáng)")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    main(*sys.argv[1:])
