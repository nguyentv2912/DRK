#!/usr/bin/env python3
"""Edit video nói chuyện (talking-head) thành Reel 9:16 hoàn chỉnh.

2 lệnh:
  1) Bóc lời có mốc thời gian từng chữ (faster-whisper, tiếng Việt):
     python3 fanpage/tools/edit_video.py transcribe RAW.mp4 transcript.json [--model small]
  2) Dựng:
     python3 fanpage/tools/edit_video.py render RAW.mp4 transcript.json edit_plan.json OUT.mp4

Bản dựng làm những việc sau:
  - cắt khoảng lặng (jump cut) và các đoạn hỏng do agent đánh dấu trong edit_plan.cut_ranges
  - cắt khung dọc 1080x1920, xen kẽ zoom 100% / 108% mỗi lần cắt cho nhịp nhanh
  - phụ đề to 2–4 chữ/lần, hiệu ứng nảy, tô màu từ khoá
  - thẻ chữ viền vàng (hook đầu video, các ý chính, CTA cuối video) bật lên đúng lúc người nói nhắc tới
  - chuẩn hoá âm lượng giọng nói + nhạc nền nhỏ phía dưới

edit_plan.json:
{
  "hook_title": "CHỌN KỶ LUẬT HAY LÒNG THAM?",      # thẻ tiêu đề 3.5s đầu video
  "keywords": {"kỷ luật": "gold", "lòng tham": "red", "cắt lỗ": "green"},
  "cards": [                                         # thẻ ý chính, bật khi nói tới trigger
    {"trigger": "thứ nhất", "kicker": "①", "text": "ĐỦ LÀ ĐỦ", "accent": "gold", "sec": 3.5},
    {"at": 42.0, "text": "TỈNH NGỘ LÀ GÌ?", "sec": 3}   # hoặc mốc thời gian (trên video gốc)
  ],
  "cut_ranges": [[12.4, 18.9]],                      # đoạn bỏ (giây, video gốc): nói vấp, quay lại
  "cta": {"text": "THEO DÕI", "sub": "ĐẠO ĐỨC ĐẦU TƯ — kỷ luật mỗi ngày", "sec": 3.5},
  "crop_x": 0.5,          # vị trí khung dọc theo chiều ngang (0 = trái, 1 = phải)
  "max_pause": 0.45,      # khoảng lặng dài hơn thế này sẽ bị cắt
  "music_volume": 0.07,
  "brand": "ĐẠO ĐỨC ĐẦU TƯ"
}
"""
import json, os, re, subprocess, sys, tempfile, unicodedata

W, H, FPS = 1080, 1920, 30
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
RGB = {"gold": (245, 196, 66), "red": (255, 82, 82), "green": (72, 220, 140), "white": (245, 240, 230)}


def ass_color(name):
    r, g, b = RGB.get(name, RGB["gold"])
    return f"&H{b:02X}{g:02X}{r:02X}&"


def norm(s):
    s = unicodedata.normalize("NFC", s).lower()
    return re.sub(r"[^\w\s]", "", s).strip()


def run(cmd):
    subprocess.run(cmd, check=True)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:stream_side_data=rotation:format=duration",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    st = j["streams"][0]
    w, h = st["width"], st["height"]
    rot = 0
    for sd in st.get("side_data_list", []) or []:
        rot = int(sd.get("rotation", 0) or 0)
    if abs(rot) in (90, 270):
        w, h = h, w
    return w, h, float(j["format"]["duration"])


# ---------------------------------------------------------------- transcribe
def transcribe(raw, out_json, model="small"):
    from faster_whisper import WhisperModel
    import numpy as np
    # đọc âm thanh bằng ffmpeg (tránh lỗi phiên bản PyAV), 16 kHz mono float32
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", raw, "-vn", "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    m = WhisperModel(model, device="auto", compute_type="int8")
    segs, info = m.transcribe(audio, language="vi", word_timestamps=True, vad_filter=True,
                              beam_size=5, condition_on_previous_text=False)
    words, sentences = [], []
    for s in segs:
        sentences.append({"s": round(s.start, 2), "e": round(s.end, 2), "text": s.text.strip()})
        for w in s.words or []:
            t = w.word.strip()
            if t:
                words.append({"w": t, "s": round(w.start, 2), "e": round(w.end, 2)})
    json.dump({"duration": info.duration, "sentences": sentences, "words": words},
              open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {out_json}: {len(sentences)} câu, {len(words)} chữ, {info.duration:.1f}s")


# ---------------------------------------------------------------- timeline
def keep_segments(words, cut_ranges, max_pause, duration):
    def cut(w):
        mid = (w["s"] + w["e"]) / 2
        return any(a <= mid <= b for a, b in cut_ranges)
    kept = [w for w in words if not cut(w)]
    segs = []
    for w in kept:
        s, e = max(0, w["s"] - 0.12), min(duration, w["e"] + 0.18)
        if segs and s - segs[-1][1] <= max_pause and not any(
                segs[-1][1] <= a <= s or segs[-1][1] <= b <= s for a, b in cut_ranges):
            segs[-1][1] = max(segs[-1][1], e)
        elif segs and s <= segs[-1][1]:
            segs[-1][1] = max(segs[-1][1], e)
        else:
            segs.append([s, e])
    segs = [s for s in segs if s[1] - s[0] >= 0.25]
    return kept, segs


def remap(t, segs):
    acc = 0.0
    for a, b in segs:
        if t < a:
            return acc
        if t <= b:
            return acc + (t - a)
        acc += b - a
    return acc


# ---------------------------------------------------------------- subtitles
def chunk_words(words, max_words=4, max_chars=20):
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        text = " ".join(x["w"] for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (len(cur) >= max_words or len(text) >= max_chars or re.search(r"[.,!?;:…]$", w["w"])
               or (nxt and nxt["s"] - w["e"] > 0.3))
        if brk or nxt is None:
            chunks.append(cur)
            cur = []
    return chunks


def colorize(text_upper, keywords):
    """Tô màu từ khoá trong 1 dòng phụ đề (so khớp không phân biệt hoa thường)."""
    spans = []
    low = text_upper.lower()
    for kw, col in sorted(keywords.items(), key=lambda x: -len(x[0])):
        for m in re.finditer(re.escape(kw.lower()), low):
            if not any(m.start() < e and m.end() > s for s, e, _ in spans):
                spans.append((m.start(), m.end(), col))
    out, pos = "", 0
    for s, e, col in sorted(spans):
        out += text_upper[pos:s] + "{\\c" + ass_color(col) + "}" + text_upper[s:e] + "{\\c&HFFFFFF&}"
        pos = e
    return out + text_upper[pos:]


def ts(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def write_ass(words, segs, keywords, path, total):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,7,3,2,80,80,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    chunks = chunk_words(words)
    for i, ch in enumerate(chunks):
        s = remap(ch[0]["s"], segs)
        e = remap(ch[-1]["e"], segs) + 0.05
        if i + 1 < len(chunks):
            e = min(max(e, s + 0.35), remap(chunks[i + 1][0]["s"], segs))
        e = min(e, total)
        if e - s < 0.1:
            continue
        text = " ".join(w["w"] for w in ch).upper().rstrip(",;:")
        txt = "{\\fscx78\\fscy78\\t(0,90,\\fscx104\\fscy104)\\t(90,160,\\fscx100\\fscy100)}" + colorize(text, keywords)
        lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Sub,,0,0,0,,{txt}")
    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
    return len(lines)


# ---------------------------------------------------------------- cards
def card_png(path, text, kicker="", sub="", accent="gold", y_center=520):
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    acc = RGB.get(accent, RGB["gold"])
    maxw = W - 260
    size = 104
    while size > 52:
        f = ImageFont.truetype(FONT_B, size)
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if cur and d.textlength(t, font=f) > maxw:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        if len(lines) <= 3 and all(d.textlength(l, font=f) <= maxw for l in lines):
            break
        size -= 6
    lh = int(size * 1.2)
    fk, fs = ImageFont.truetype(FONT_B, 72), ImageFont.truetype(FONT_R, 44)
    h = lh * len(lines) + (95 if kicker else 0) + (70 if sub else 0) + 90
    top = y_center - h // 2
    box = [70, top, W - 70, top + h]
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle(box, radius=40, outline=acc + (200,), width=14)
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=40, fill=(18, 13, 6, 225), outline=acc, width=5)
    y = top + 45
    if kicker:
        d.text((W / 2, y + 30), kicker, font=fk, fill=acc, anchor="mm")
        y += 95
    for l in lines:
        d.text((W / 2 + 3, y + 4), l, font=f, fill=(0, 0, 0, 180), anchor="ma")
        d.text((W / 2, y), l, font=f, fill=acc, anchor="ma")
        y += lh
    if sub:
        d.text((W / 2, y + 10), sub, font=fs, fill=(235, 225, 205), anchor="ma")
    img.save(path)


def find_trigger(words, phrase, after):
    target = norm(phrase).split()
    toks = [norm(w["w"]) for w in words]
    for i in range(len(toks) - len(target) + 1):
        if words[i]["s"] < after:
            continue
        if toks[i:i + len(target)] == target:
            return words[i]["s"]
    return None


# ---------------------------------------------------------------- render
def render(raw, transcript, plan_path, out):
    tr = json.load(open(transcript, encoding="utf-8"))
    plan = json.load(open(plan_path, encoding="utf-8"))
    sw, sh, dur = probe(raw)
    kept, segs = keep_segments(tr["words"], plan.get("cut_ranges", []), plan.get("max_pause", 0.45), dur)
    if not segs:
        sys.exit("Không có đoạn nói nào để dựng (transcript trống?)")
    total = sum(b - a for a, b in segs)
    tmp = tempfile.mkdtemp(prefix="edit_")

    # khung dọc
    if sw / sh > W / H:
        cw, ch = int(sh * W / H) // 2 * 2, sh
        cx = int((sw - cw) * float(plan.get("crop_x", 0.5)))
        base = f"crop={cw}:{ch}:{cx}:0,scale={W}:{H}"
    else:
        base = f"scale={W}:-2,crop={W}:{H}" if sw / sh < W / H else f"scale={W}:{H}"
    zooms = [1.0, 1.08]

    # 1) từng đoạn giữ lại
    listf = os.path.join(tmp, "list.txt")
    with open(listf, "w") as lf:
        for i, (a, b) in enumerate(segs):
            z = zooms[i % 2]
            vf = base + (f",scale={int(W * z) // 2 * 2}:{int(H * z) // 2 * 2},crop={W}:{H}" if z != 1 else "")
            vf += f",setsar=1,fps={FPS}"
            d = b - a
            af = f"aresample=48000,afade=t=in:d=0.03,afade=t=out:st={max(0, d - 0.04):.3f}:d=0.04"
            p = os.path.join(tmp, f"s{i:04d}.mp4")
            run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-i", raw, "-t", f"{d:.3f}",
                 "-vf", vf, "-af", af, "-ac", "2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                 "-c:a", "aac", "-b:a", "192k", p])
            lf.write(f"file '{p}'\n")
    cat = os.path.join(tmp, "cat.mp4")
    run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listf,
         "-c", "copy", cat])
    _, _, total = probe(cat)

    # 2) phụ đề
    ass = os.path.join(tmp, "subs.ass")
    n_sub = write_ass(kept, segs, plan.get("keywords", {}), ass, total)

    # 3) thẻ chữ
    overlays = []  # (png, start, end)
    if plan.get("hook_title"):
        p = os.path.join(tmp, "c_hook.png")
        card_png(p, plan["hook_title"], accent=plan.get("hook_accent", "red"))
        overlays.append((p, 0.0, 3.5))
    after = 0.0
    for k, c in enumerate(plan.get("cards", [])):
        t_raw = c.get("at")
        if t_raw is None:
            t_raw = find_trigger(kept, c["trigger"], after)
            if t_raw is None:
                print(f"! Không thấy trigger '{c['trigger']}' — bỏ thẻ '{c['text']}'")
                continue
        after = t_raw + 0.1
        s = remap(t_raw, segs)
        p = os.path.join(tmp, f"c{k:02d}.png")
        card_png(p, c["text"], c.get("kicker", ""), c.get("sub", ""), c.get("accent", "gold"))
        overlays.append((p, s, min(total, s + float(c.get("sec", 3.5)))))
    cta = plan.get("cta")
    if cta:
        p = os.path.join(tmp, "c_cta.png")
        card_png(p, cta["text"], sub=cta.get("sub", ""), accent=cta.get("accent", "gold"))
        overlays.append((p, max(0, total - float(cta.get("sec", 3.5))), total))
    # thương hiệu góc trên
    from PIL import Image, ImageDraw, ImageFont
    bp = os.path.join(tmp, "brand.png")
    bi = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bi)
    bd.text((W / 2 + 2, 152), plan.get("brand", ""), font=ImageFont.truetype(FONT_B, 40), fill=(0, 0, 0, 170), anchor="mm")
    bd.text((W / 2, 150), plan.get("brand", ""), font=ImageFont.truetype(FONT_B, 40), fill=RGB["gold"], anchor="mm")
    bi.save(bp)

    # 4) ghép cuối: phụ đề + thẻ + nhạc nền
    inputs = ["-i", cat, "-loop", "1", "-i", bp]
    for p, _, _ in overlays:
        inputs += ["-loop", "1", "-i", p]
    vol = float(plan.get("music_volume", 0.07))
    music = (f"aevalsrc='{vol}*(0.6*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.25*t))"
             f"+0.5*sin(2*PI*164.8*t)+0.4*sin(2*PI*220*t)+0.9*sin(2*PI*55*t)*exp(-8*mod(t,0.5)))'"
             f":s=48000:c=stereo:d={total:.2f}")
    inputs += ["-f", "lavfi", "-i", music]
    mi = 2 + len(overlays)
    ass_esc = ass.replace("\\", "/").replace(":", "\\:")
    fc = [f"[0:v][1:v]overlay=0:0:shortest=1[v0]"]
    last = "v0"
    for k, (_, s, e) in enumerate(overlays):
        nxt = f"v{k + 1}"
        fc.append(f"[{last}][{k + 2}:v]overlay=0:0:shortest=1:enable='between(t,{s:.2f},{e:.2f})'[{nxt}]")
        last = nxt
    fc.append(f"[{last}]ass='{ass_esc}'[vout]")
    fc.append(f"[0:a]highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
              f"loudnorm=I=-15:TP=-1.5:LRA=9[voice]")
    fc.append(f"[{mi}:a]afade=t=in:d=1,afade=t=out:st={max(0, total - 2):.2f}:d=2[mus]")
    fc.append("[voice][mus]amix=inputs=2:duration=first:normalize=0[aout]")
    run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium",
         "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
    cover = os.path.splitext(out)[0] + "_cover.jpg"
    run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", "1.5", "-i", out, "-frames:v", "1", "-q:v", "2", cover])
    subprocess.run(["rm", "-rf", tmp])
    removed = dur - total
    print(f"OK {out}: {total:.1f}s (gốc {dur:.1f}s, cắt {removed:.1f}s), {len(segs)} đoạn, "
          f"{n_sub} dòng phụ đề, {len(overlays)} thẻ chữ, bìa {cover}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "transcribe":
        model = a[a.index("--model") + 1] if "--model" in a else "small"
        transcribe(a[1], a[2], model)
    elif len(a) == 5 and a[0] == "render":
        render(*a[1:])
    else:
        sys.exit(__doc__)
