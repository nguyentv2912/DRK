#!/usr/bin/env python3
"""Dựng video dọc 9:16 (1080x1920) từ storyboard JSON — chữ động nền đen-vàng.

Cách dùng:
    python3 fanpage/tools/make_video.py runs/2026-11-14/storyboard.json runs/2026-11-14/video.mp4

storyboard.json:
{
  "brand": "ĐẠO ĐỨC ĐẦU TƯ",
  "scenes": [
    {"text": "CHỌN KỶ LUẬT", "sub": "hay lòng tham?", "accent": "red", "sec": 3.5},
    {"kicker": "① ", "text": "ĐỦ LÀ ĐỦ", "sub": "Chạm mục tiêu thì dừng", "sec": 3}
  ]
}
- text: dòng chữ to (tự xuống dòng). Bọc *từ* để tô màu nhấn.
- accent: gold (mặc định) | red | green
- sub: dòng nhỏ bên dưới. kicker: nhãn nhỏ phía trên. sec: thời lượng cảnh.
"""
import json, math, os, random, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
GOLD, RED, GREEN, WHITE = (245, 196, 66), (255, 82, 82), (72, 220, 140), (245, 240, 230)
ACC = {"gold": GOLD, "red": RED, "green": GREEN}


def font(path, size):
    return ImageFont.truetype(path, size)


def background(seed=7):
    """Nền gradient nâu-đen + vignette + khung viền vàng (tĩnh, vẽ 1 lần)."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        for x in range(0, W, 4):
            dx, dy = (x - W / 2) / W, (y - H * 0.42) / H
            d = math.sqrt(dx * dx * 1.6 + dy * dy)
            k = max(0.0, 1 - d * 1.5)
            c = (int(14 + 52 * k), int(11 + 38 * k), int(6 + 10 * k))
            for i in range(4):
                px[x + i, y] = c
    d = ImageDraw.Draw(img)
    m = 48
    d.rounded_rectangle([m, 150, W - m, H - 150], radius=36, outline=(150, 115, 40), width=3)
    # góc trang trí
    for (x, y, sx, sy) in [(m + 30, 300, 1, 1), (W - m - 30, 300, -1, 1),
                           (m + 30, H - 300, 1, -1), (W - m - 30, H - 300, -1, -1)]:
        d.line([x, y, x + 80 * sx, y], fill=GOLD, width=4)
        d.line([x, y, x, y + 80 * sy], fill=GOLD, width=4)
    return img


def particles(n=70, seed=3):
    r = random.Random(seed)
    return [(r.uniform(0, W), r.uniform(0, H), r.uniform(1.5, 4.5), r.uniform(10, 40), r.uniform(0, 6.28))
            for _ in range(n)]


def parse_runs(text):
    """'CHỌN *KỶ LUẬT*' -> [('CHỌN ', False), ('KỶ LUẬT', True)]"""
    out, hl = [], False
    for i, part in enumerate(text.split("*")):
        if part:
            out.append((part, i % 2 == 1))
    return out


def wrap_runs(runs, f, maxw, draw):
    words = []
    for t, hl in runs:
        for w in t.split(" "):
            if w:
                words.append((w, hl))
    lines, cur = [], []
    for w in words:
        test = " ".join(x for x, _ in cur + [w])
        if cur and draw.textlength(test, font=f) > maxw:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def fit_font(runs, draw, maxw, max_lines=4):
    for size in range(150, 54, -6):
        f = font(FONT_B, size)
        lines = wrap_runs(runs, f, maxw, draw)
        if len(lines) <= max_lines and all(
                draw.textlength(" ".join(w for w, _ in ln), font=f) <= maxw for ln in lines):
            return f, lines
    f = font(FONT_B, 54)
    return f, wrap_runs(runs, f, maxw, draw)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def render_text_layer(scene, brand):
    """Lớp chữ RGBA (vẽ 1 lần mỗi cảnh, sau đó chỉ scale/alpha)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    acc = ACC.get(scene.get("accent", "gold"), GOLD)
    runs = parse_runs(scene["text"])
    if not any(hl for _, hl in runs):
        runs = [(t, True) for t, _ in runs] if scene.get("accent") else runs
    f, lines = fit_font(runs, d, W - 220)
    lh = int(f.size * 1.18)
    block_h = lh * len(lines)
    y = int(H * 0.44 - block_h / 2)
    if scene.get("kicker"):
        fk = font(FONT_B, 46)
        k = scene["kicker"]
        kw = d.textlength(k, font=fk)
        d.rounded_rectangle([W / 2 - kw / 2 - 28, y - 120, W / 2 + kw / 2 + 28, y - 46],
                            radius=37, outline=acc, width=3)
        d.text((W / 2, y - 83), k, font=fk, fill=acc, anchor="mm")
    for ln in lines:
        total = d.textlength(" ".join(w for w, _ in ln), font=f)
        x = W / 2 - total / 2
        for i, (w, hl) in enumerate(ln):
            word = w + (" " if i < len(ln) - 1 else "")
            col = acc if hl else WHITE
            d.text((x + 4, y + 5), word, font=f, fill=(0, 0, 0, 160))
            d.text((x, y), word, font=f, fill=col)
            x += d.textlength(word, font=f)
        y += lh
    if scene.get("sub"):
        fs = font(FONT_R, 50)
        sub_lines = wrap_runs([(scene["sub"], False)], fs, W - 260, d)
        y += 30
        for ln in sub_lines:
            d.text((W / 2, y), " ".join(w for w, _ in ln), font=fs, fill=(230, 220, 200), anchor="ma")
            y += 66
    # thương hiệu
    fb = font(FONT_B, 40)
    d.text((W / 2, 225), brand, font=fb, fill=GOLD, anchor="mm")
    glow = layer.filter(ImageFilter.GaussianBlur(14))
    out = Image.alpha_composite(glow, layer)
    return out


def main(sb_path, out_path):
    sb = json.load(open(sb_path, encoding="utf-8"))
    brand = sb.get("brand", "")
    scenes = sb["scenes"]
    bg = background()
    parts = particles()
    tmp = tempfile.mkdtemp(prefix="vid_")
    total = sum(float(s.get("sec", 3)) for s in scenes)
    n_frames = int(total * FPS)
    fb = font(FONT_B, 34)
    frame_i, t0 = 0, 0.0
    for si, sc in enumerate(scenes):
        dur = float(sc.get("sec", 3))
        layer = render_text_layer(sc, brand)
        nf = int(dur * FPS)
        for k in range(nf):
            t = frame_i / FPS
            lt = k / FPS
            img = bg.copy()
            d = ImageDraw.Draw(img, "RGBA")
            for (x, y, r, sp, ph) in parts:
                yy = (y - sp * t) % H
                a = int(90 + 80 * math.sin(t * 1.5 + ph))
                d.ellipse([x - r, yy - r, x + r, yy + r], fill=(245, 196, 66, a))
            # chữ: phóng to + hiện dần đầu cảnh, mờ dần cuối cảnh
            e = ease(lt / 0.45)
            fade_out = ease((dur - lt) / 0.3)
            alpha = min(e, fade_out)
            scale = 0.86 + 0.14 * e + 0.02 * (lt / dur)
            lw, lhh = int(W * scale), int(H * scale)
            L = layer.resize((lw, lhh), Image.BILINEAR)
            if alpha < 1:
                L.putalpha(L.getchannel("A").point(lambda v: int(v * alpha)))
            img.paste(L, ((W - lw) // 2, (H - lhh) // 2), L)
            # thanh tiến độ
            d = ImageDraw.Draw(img)
            d.rectangle([96, H - 200, 96 + (W - 192) * (t / total), H - 192], fill=GOLD)
            d.text((W / 2, H - 240), f"{si + 1}/{len(scenes)}", font=fb, fill=(200, 170, 90), anchor="mm")
            img.save(os.path.join(tmp, f"f{frame_i:05d}.jpg"), quality=90)
            frame_i += 1
        t0 += dur
    # nhạc nền tổng hợp nhẹ (không bản quyền): hợp âm pad + nhịp
    audio = (f"aevalsrc='0.06*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.25*t))"
             f"+0.04*sin(2*PI*164.8*t)+0.035*sin(2*PI*220*t)"
             f"+0.08*sin(2*PI*55*t)*exp(-8*mod(t,0.5))':s=44100:d={total}")
    cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-framerate", str(FPS),
           "-i", os.path.join(tmp, "f%05d.jpg"), "-f", "lavfi", "-i", audio,
           "-af", f"afade=t=in:d=1,afade=t=out:st={max(0, total - 1.5)}:d=1.5",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "medium",
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out_path]
    subprocess.run(cmd, check=True)
    # ảnh bìa
    cover = os.path.splitext(out_path)[0] + "_cover.jpg"
    Image.open(os.path.join(tmp, f"f{min(int(scenes[0].get('sec', 3) * FPS * 0.8), frame_i - 1):05d}.jpg")).save(cover, quality=92)
    subprocess.run(["rm", "-rf", tmp])
    print(f"OK {out_path} ({total:.1f}s, {n_frames} khung) + {cover}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
