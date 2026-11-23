#!/usr/bin/env python3
"""Tạo ảnh bài đăng theo thương hiệu Đạo Đức Đầu Tư (1080×1350, nền xanh đậm, viền vàng kim).

  python3 fanpage/tools/tao_anh.py SPEC.json OUT_DIR

SPEC.json là một bài hoặc danh sách bài:
{"loai": "trich_dan", "ten": "t2-1", "chu": "Tiền là công cụ tạo lựa chọn; đừng biến nó thành chủ nhân.", "nguon": "Đạo Đức Đầu Tư"}
{"loai": "nen_mau",   "ten": "t2-2", "chu": "Hôm nay bạn đứng ngoài được một lần FOMO chưa?"}
{"loai": "infographic","ten": "t3-1", "tieu_de": "TOÁN HỌC CỦA THUA LỖ",
   "dong": [["Giảm 20%", "cần +25%"], ["Giảm 50%", "cần +100%"], ["Giảm 80%", "cần +400%"]], "chu_thich": "Giữ vốn trước khi tìm lãi."}
{"loai": "album", "ten": "t4-album", "tieu_de": "5 DẤU HIỆU BẠN ĐANG FOMO",
   "trang": [["1", "Mua vì sợ lỡ", "chứ không vì hiểu"], ["2", "…", "…"]], "ket": "Lưu lại để soi mình mỗi tuần."}
Ảnh không có số tiền, không có tên coin/mã. Ra file PNG: <ten>.png (album: <ten>-1.png, -2.png…).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG, BG2 = (12, 30, 24), (20, 46, 37)
GOLD, WHITE, SOFT = (214, 178, 94), (255, 255, 255), (190, 205, 197)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def f(p, s):
    return ImageFont.truetype(p, s)


def canvas(bg=BG):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    for y in range(H):  # chuyển màu nhẹ
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(bg[i] * (1 - t) + BG2[i] * t) for i in range(3)))
    d.rounded_rectangle((28, 28, W - 28, H - 28), radius=40, outline=GOLD, width=5)
    d.rounded_rectangle((42, 42, W - 42, H - 42), radius=32, outline=GOLD + (0,), width=1)
    for cx, cy, sx, sy in [(70, 70, 1, 1), (W - 70, 70, -1, 1), (70, H - 70, 1, -1), (W - 70, H - 70, -1, -1)]:
        d.line([(cx, cy + sy * 60), (cx, cy), (cx + sx * 60, cy)], fill=GOLD, width=7)
    d.text((W / 2, H - 92), "ĐẠO ĐỨC ĐẦU TƯ", font=f(FB, 30), fill=GOLD, anchor="mm")
    d.text((W / 2, H - 58), "Bình an trong đầu tư", font=f(FR, 22), fill=SOFT, anchor="mm")
    return im, d


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    return lines + ([cur] if cur else [])


def fit(d, text, path, maxw, maxh, start=84, minsize=40, gap=1.32):
    s = start
    while s >= minsize:
        fo = f(path, s); ls = wrap(d, text, fo, maxw)
        if len(ls) * s * gap <= maxh:
            return fo, ls, s
        s -= 4
    fo = f(path, minsize)
    return fo, wrap(d, text, fo, maxw), minsize


def block(d, lines, fo, size, cy, fill, gap=1.32):
    y = cy - len(lines) * size * gap / 2
    for ln in lines:
        d.text((W / 2, y), ln, font=fo, fill=fill, anchor="ma"); y += size * gap
    return y


def trich_dan(p):
    im, d = canvas()
    d.text((W / 2, 250), "“", font=f(FS, 220), fill=GOLD, anchor="mm")
    fo, ls, s = fit(d, p["chu"], FS, W - 220, 560, 76)
    y = block(d, ls, fo, s, 640, WHITE)
    if p.get("nguon"):
        d.line([(W / 2 - 60, y + 40), (W / 2 + 60, y + 40)], fill=GOLD, width=3)
        d.text((W / 2, y + 85), p["nguon"], font=f(FR, 34), fill=GOLD, anchor="mm")
    return [im]


def nen_mau(p):
    im, d = canvas((92, 58, 24))
    fo, ls, s = fit(d, p["chu"], FB, W - 220, 700, 92)
    block(d, ls, fo, s, 640, WHITE)
    return [im]


def infographic(p):
    im, d = canvas()
    fo, ls, s = fit(d, p["tieu_de"], FB, W - 200, 180, 66, 44, 1.2)
    block(d, ls, fo, s, 200, GOLD, 1.2)
    rows = p.get("dong", [])
    top, bot = 330, H - 300
    rh = (bot - top) / max(1, len(rows))
    for i, (a, b) in enumerate(rows):
        y0 = top + i * rh + 10
        d.rounded_rectangle((90, y0, W - 90, y0 + rh - 20), radius=24, fill=(28, 58, 46), outline=GOLD, width=2)
        cy = y0 + (rh - 20) / 2
        d.text((140, cy), a, font=f(FB, 46), fill=WHITE, anchor="lm")
        d.text((W - 140, cy), b, font=f(FB, 46), fill=GOLD, anchor="rm")
    if p.get("chu_thich"):
        fo, ls, s = fit(d, p["chu_thich"], FR, W - 220, 110, 38, 28)
        block(d, ls, fo, s, H - 210, SOFT)
    return [im]


def album(p):
    out = []
    im, d = canvas()
    fo, ls, s = fit(d, p["tieu_de"], FB, W - 200, 520, 96)
    block(d, ls, fo, s, 560, GOLD)
    d.text((W / 2, 1000), "Lướt sang để xem →", font=f(FR, 40), fill=SOFT, anchor="mm")
    out.append(im)
    for so, dau, sau in p.get("trang", []):
        im, d = canvas()
        d.ellipse((W / 2 - 90, 190, W / 2 + 90, 370), fill=GOLD)
        d.text((W / 2, 280), str(so), font=f(FB, 110), fill=BG, anchor="mm")
        fo, ls, s = fit(d, dau, FB, W - 200, 330, 80, 48)
        y = block(d, ls, fo, s, 600, WHITE)
        if sau:
            fo, ls, s2 = fit(d, sau, FR, W - 220, 260, 48, 32)
            block(d, ls, fo, s2, y + 140, SOFT)
        out.append(im)
    if p.get("ket"):
        im, d = canvas()
        fo, ls, s = fit(d, p["ket"], FS, W - 220, 500, 72)
        block(d, ls, fo, s, 620, WHITE)
        out.append(im)
    return out


KIND = {"trich_dan": trich_dan, "nen_mau": nen_mau, "infographic": infographic, "album": album}


def main(spec, outdir):
    data = json.load(open(spec, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    for p in data if isinstance(data, list) else [data]:
        ims = KIND[p["loai"]](p)
        names = [f"{p['ten']}.png"] if len(ims) == 1 else [f"{p['ten']}-{i + 1}.png" for i in range(len(ims))]
        for im, n in zip(ims, names):
            im.save(os.path.join(outdir, n), optimize=True)
        print("OK", p["ten"], len(ims), "ảnh")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
