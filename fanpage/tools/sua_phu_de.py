#!/usr/bin/env python3
"""Sửa chữ phụ đề sau khi máy bóc lời (faster-whisper nghe sai nhiều tiếng Việt).

  python3 fanpage/tools/sua_phu_de.py transcript.json sua.json transcript_sua.json

sua.json: {"<số thứ tự câu>": "câu đúng", ...}  — câu không có trong file giữ nguyên;
giá trị "" = bỏ hẳn câu đó (nói vấp, nói lặp) → câu bị bỏ cũng nên đưa vào cut_ranges của edit_plan.
Mốc thời gian câu giữ nguyên; chữ trong câu được chia lại theo mốc các chữ máy đã nghe.
"""
import json, sys


def main(src, fix, out):
    t = json.load(open(src, encoding="utf-8"))
    sua = {int(k): v for k, v in json.load(open(fix, encoding="utf-8")).items()}
    W, words, sents = t["words"], [], []
    for i, sen in enumerate(t["sentences"]):
        txt = sua.get(i, sen["text"])
        if not txt.strip():
            continue
        ws = [w for w in W if w["s"] >= sen["s"] - 0.05 and w["e"] <= sen["e"] + 0.05] or [{"s": sen["s"], "e": sen["e"]}]
        toks, m = txt.split(), len(ws)
        n = len(toks)
        groups = {}
        for k in range(n):
            groups.setdefault(min(m - 1, int(k * m / n)), []).append(k)
        keys = sorted(groups)
        for gi, j in enumerate(keys):
            end_w = ws[keys[gi + 1] - 1] if gi + 1 < len(keys) else ws[-1]
            s, e = ws[j]["s"], max(end_w["e"], ws[j]["s"] + 0.15)
            d = (e - s) / len(groups[j])
            for q, k in enumerate(groups[j]):
                words.append({"w": toks[k], "s": round(s + q * d, 2), "e": round(s + (q + 1) * d, 2)})
        sents.append({"s": sen["s"], "e": sen["e"], "text": txt})
    t["words"], t["sentences"] = words, sents
    json.dump(t, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"OK {out}: {len(sents)} câu, {len(words)} chữ")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
