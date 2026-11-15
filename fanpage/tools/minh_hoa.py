#!/usr/bin/env python3
"""Lớp hiệu ứng thứ hai cho video đã dựng: khung viền thương hiệu, thanh tiến độ,
và các tấm minh hoạ (nhân vật / nhiệm vụ) bật lên khi người nói nhắc tới.

  python3 fanpage/tools/minh_hoa.py VIDEO_DUNG.mp4 transcript.json edit_plan.json minh_hoa.json OUT.mp4

minh_hoa.json:
{
  "theme": {"accent": [214,178,94], "bg": [12,30,24]},
  "panels": [
    {"trigger": "thứ nhất", "sec": 8, "title": "① GIAO VIỆC 1 CÂU",
     "items": [{"name":"ANH","role":"Ra lệnh","on":true,"me":true},
               {"name":"MINH","role":"Chia việc","on":true}], "arrows": true}
  ]
}
"trigger" là cụm lời nói (giống thẻ chữ trong edit_plan); hoặc dùng "at" = giây trên video gốc.
Mốc thời gian được đổi sang video đã dựng bằng đúng cách cắt của edit_video.py.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from edit_video import keep_segments, remap, find_trigger, FONT_B, FONT_R  # noqa

W, H = 1080, 1920


def font(path, size):
    return ImageFont.truetype(path, size)


def frame_png(path, acc):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 18, W - 18, H - 18), radius=46, outline=acc + (230,), width=6)
    d.rounded_rectangle((30, 30, W - 30, H - 30), radius=38, outline=acc + (90,), width=2)
    im.save(path)


def bar_png(path, acc):
    im = Image.new("RGBA", (W, 10), acc + (235,))
    im.save(path)


def panel_png(path, p, acc, bg):
    items = p.get("items", [])
    n = max(1, len(items))
    ph = 360
    im = Image.new("RGBA", (W, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 0, W - 40, ph - 6), radius=34, fill=bg + (225,), outline=acc + (255,), width=4)
    d.text((W / 2, 46), p.get("title", ""), font=font(FONT_B, 42), fill=acc + (255,), anchor="mm")
    slot = (W - 120) / n
    r = min(62, int(slot * 0.36))
    for i, it in enumerate(items):
        cx, cy = 60 + slot * (i + 0.5), 160
        on, me = it.get("on", True), it.get("me", False)
        fill = (acc + (255,)) if (on and me) else ((46, 150, 112, 255) if on else (70, 82, 76, 200))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=(255, 255, 255, 200 if on else 80), width=3)
        label = it.get("icon") or it["name"][0]
        d.text((cx, cy), label, font=font(FONT_B, int(r * 0.9)), fill=(255, 255, 255, 255 if on else 140), anchor="mm")
        col = (255, 255, 255, 255) if on else (200, 210, 205, 130)
        d.text((cx, cy + r + 30), it["name"], font=font(FONT_B, 30 if n <= 5 else 24), fill=col, anchor="mm")
        d.text((cx, cy + r + 66), it.get("role", ""), font=font(FONT_R, 25 if n <= 5 else 19),
               fill=(acc + (255,)) if on else (190, 200, 195, 110), anchor="mm")
        if p.get("arrows") and i < n - 1:
            ax = cx + slot / 2
            d.polygon([(ax - 14, cy - 16), (ax + 14, cy), (ax - 14, cy + 16)], fill=acc + (255,))
    im.save(path)


def main(video, tr_json, plan_json, mh_json, out):
    tr, plan, mh = (json.load(open(f)) for f in (tr_json, plan_json, mh_json))
    _, segs = keep_segments(tr["words"], plan.get("cut_ranges", []), plan.get("max_pause", 0.45), tr["duration"])
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", video]).decode())
    th = mh.get("theme", {})
    acc, bg = tuple(th.get("accent", [214, 178, 94])), tuple(th.get("bg", [12, 30, 24]))
    tmp = tempfile.mkdtemp()
    frame_png(f"{tmp}/frame.png", acc)
    bar_png(f"{tmp}/bar.png", acc)
    inputs, filters, last, after = ["-i", video, "-i", f"{tmp}/frame.png", "-i", f"{tmp}/bar.png"], [], "0:v", 0.0
    filters.append(f"[{last}][1:v]overlay=0:0[v1]"); last = "v1"
    filters.append(f"[{last}][2:v]overlay=x='-W+W*t/{dur:.3f}':y=H-34[v2]"); last = "v2"
    k = 3
    for i, p in enumerate(mh.get("panels", [])):
        if "at" in p:
            t0 = remap(p["at"], segs)
        else:
            src = find_trigger(tr["words"], p["trigger"], after)
            if src is None:
                print("không thấy trigger:", p["trigger"]); continue
            after = src
            t0 = remap(src, segs)
        t1 = min(dur - 4, t0 + p.get("sec", 7))
        png = f"{tmp}/p{i}.png"; panel_png(png, p, acc, bg)
        inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-i", png]
        y = p.get("y", 1470)
        filters.append(f"[{k}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.3:alpha=1,fade=t=out:st={t1-0.3:.2f}:d=0.3:alpha=1[p{i}]")
        filters.append(f"[{last}][p{i}]overlay=0:{y}:enable='between(t,{t0:.2f},{t1:.2f})'[v{k}]")
        last = f"v{k}"; k += 1
        print(f"tấm {i}: {p.get('title','')} {t0:.1f}s → {t1:.1f}s")
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", f"[{last}]",
           "-map", "0:a", "-c:v", "libx264", "-crf", "25", "-preset", "medium", "-c:a", "copy",
           "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("OK", out)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    main(*sys.argv[1:])
