#!/usr/bin/env python3
"""Video ngắn đội tự làm (không cần chủ kênh quay): chữ động trên nền thương hiệu,
chuyển cảnh, thanh tiến độ, nhạc nền + âm thanh hiệu ứng tự tạo. 1080×1920, 20–45 giây.

  python3 fanpage/tools/video_ngan.py SPEC.json OUT.mp4

SPEC.json:
{
  "hook": "Đừng mở app khi lòng đang nóng",            # cảnh 1 (3 giây), chữ to
  "phu": "3 điều mình học được sau những lần FOMO",    # dòng phụ dưới hook (tuỳ chọn)
  "y": [                                               # 3–5 cảnh ý chính (mỗi cảnh ~5 giây)
    {"so": "1", "dau": "Dừng lại 10 phút", "sau": "trước mọi quyết định khi tim đập nhanh"},
    {"so": "2", "dau": "...", "sau": "...", "icon": "dong_ho"}
  ],
  "trich": {"chu": "Thắng người là có sức, thắng mình mới là mạnh.", "nguon": "Lão Tử, Đạo Đức Kinh, ch. 33"},  # tuỳ chọn
  "ket": "Theo dõi Đạo Đức Đầu Tư – bình an trong đầu tư",
  "giay_moi_y": 5
}
Icon (tuỳ chọn) giống minh_hoa.py: bieu_do_tang, bieu_do_giam, dam_dong, trai_tim, dong_ho, khien, can_can, mat_troi, ngon_nen, nha.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from minh_hoa import draw_icon, sfx, SR  # noqa
from tao_anh import wrap  # noqa

W, H = 1080, 1920
BG, BG2, GOLD, WHITE, SOFT = (12, 30, 24), (24, 52, 42), (214, 178, 94), (255, 255, 255), (190, 205, 197)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FPS = 30
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def f(p, s):
    return ImageFont.truetype(p, s)


def base():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(BG[i] * (1 - t) + BG2[i] * t) for i in range(3)))
    d.rounded_rectangle((24, 24, W - 24, H - 24), radius=46, outline=GOLD, width=6)
    for cx, cy, sx, sy in [(64, 64, 1, 1), (W - 64, 64, -1, 1), (64, H - 64, 1, -1), (W - 64, H - 64, -1, -1)]:
        d.line([(cx, cy + sy * 70), (cx, cy), (cx + sx * 70, cy)], fill=GOLD, width=8)
    d.text((W / 2, 150), "ĐẠO ĐỨC ĐẦU TƯ", font=f(FB, 40), fill=GOLD, anchor="mm")
    d.text((W / 2, H - 150), "Bình an trong đầu tư", font=f(FR, 32), fill=SOFT, anchor="mm")
    return im, d


def lines(d, text, path, size, maxw, cy, fill, gap=1.3):
    fo = f(path, size)
    ls = wrap(d, text, fo, maxw)
    while len(ls) * size * gap > 700 and size > 44:
        size -= 6; fo = f(path, size); ls = wrap(d, text, fo, maxw)
    y = cy - len(ls) * size * gap / 2
    for ln in ls:
        d.text((W / 2, y), ln, font=fo, fill=fill, anchor="ma"); y += size * gap
    return y


def slide_hook(s):
    im, d = base()
    y = lines(d, s["hook"], FB, 104, W - 200, 860, WHITE)
    if s.get("phu"):
        d.line([(W / 2 - 80, y + 50), (W / 2 + 80, y + 50)], fill=GOLD, width=5)
        lines(d, s["phu"], FR, 50, W - 240, y + 170, GOLD)
    return im


def slide_y(it):
    im, d = base()
    if it.get("icon"):
        draw_icon(d, it["icon"], W / 2, 560, 150, GOLD)
    else:
        d.ellipse((W / 2 - 130, 430, W / 2 + 130, 690), fill=GOLD)
        d.text((W / 2, 560), str(it.get("so", "")), font=f(FB, 150), fill=BG, anchor="mm")
    y = lines(d, it["dau"], FB, 88, W - 200, 960, WHITE)
    if it.get("sau"):
        lines(d, it["sau"], FR, 54, W - 240, y + 150, SOFT)
    return im


def slide_trich(t):
    im, d = base()
    d.text((W / 2, 560), "“", font=f(FS, 300), fill=GOLD, anchor="mm")
    y = lines(d, t["chu"], FS, 80, W - 220, 960, WHITE)
    if t.get("nguon"):
        d.text((W / 2, y + 90), "— " + t["nguon"], font=f(FR, 40), fill=GOLD, anchor="mm")
    return im


def slide_ket(text):
    im, d = base()
    d.rounded_rectangle((140, 760, W - 140, 1160), radius=40, fill=(28, 58, 46), outline=GOLD, width=4)
    d.text((W / 2, 870), "THEO DÕI", font=f(FB, 96), fill=GOLD, anchor="mm")
    lines(d, text, FR, 46, W - 360, 1040, WHITE)
    return im


def main(spec_path, out):
    s = json.load(open(spec_path, encoding="utf-8"))
    per = float(s.get("giay_moi_y", 5))
    slides = [(slide_hook(s), 3.2)] + [(slide_y(it), per) for it in s["y"]]
    if s.get("trich"):
        slides.append((slide_trich(s["trich"]), per))
    slides.append((slide_ket(s.get("ket", "Đạo Đức Đầu Tư – bình an trong đầu tư")), 3.0))
    tmp = tempfile.mkdtemp()
    X = 0.4  # thời gian chuyển cảnh
    inputs, fc = [], []
    for i, (im, dur) in enumerate(slides):
        p = f"{tmp}/s{i}.png"; im.save(p)
        n = int((dur + X) * FPS)
        inputs += ["-loop", "1", "-t", f"{dur + X:.2f}", "-i", p]
        z = "1+0.0006*on" if i % 2 == 0 else "1.06-0.0006*on"
        fc.append(f"[{i}:v]scale=1188:2112,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                  f":d={n}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[z{i}]")
    last, t, events = "z0", slides[0][1], [(0.05, "whoosh")]
    trans = ["slideleft", "fade", "slideup", "circleopen", "fade", "slideright", "fade"]
    for i in range(1, len(slides)):
        fc.append(f"[{last}][z{i}]xfade=transition={trans[(i - 1) % len(trans)]}:duration={X}:offset={t:.2f}[x{i}]")
        events.append((t, "whoosh" if i < len(slides) - 1 else "ding"))
        last = f"x{i}"; t += slides[i][1]
    total = t + X
    # thanh tiến độ
    bar = f"{tmp}/bar.png"; Image.new("RGBA", (W, 12), GOLD + (240,)).save(bar)
    inputs += ["-i", bar]
    bi = len(slides)
    fc.append(f"[{last}][{bi}:v]overlay=x='-W+W*t/{total:.2f}':y=H-40[v]")
    # âm thanh: nhạc nền + hiệu ứng
    music = s.get("nhac") or os.path.join(ROOT, "assets", "nhac", "binh-an.mp3")
    track = np.zeros((int((total + 2) * SR), 2))
    for t0, k in events:
        a = sfx(k); i0 = int(t0 * SR); track[i0:i0 + len(a)] += a[: len(track) - i0]
    sp = f"{tmp}/sfx.raw"; (np.clip(track, -1, 1) * 32767).astype("<i2").tofile(sp)
    inputs += ["-stream_loop", "-1", "-i", music, "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", sp]
    mi, si = bi + 1, bi + 2
    fc.append(f"[{mi}:a]aresample={SR},volume=0.55,afade=t=in:d=1,afade=t=out:st={total - 2:.2f}:d=2[m];"
              f"[{si}:a]volume=0.6[e];[m][e]amix=inputs=2:duration=first:normalize=0[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                    "-t", f"{total:.2f}", "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
    cover = os.path.splitext(out)[0] + "_cover.jpg"
    slides[0][0].save(cover, quality=90)
    print(f"OK {out}: {total:.1f}s, {len(slides)} cảnh, bìa {cover}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
