#!/usr/bin/env python3
"""Ghép video thô với kịch bản bằng cách so lời nói (transcript) với lời thoại.

  python3 fanpage/tools/khop_kich_ban.py <transcript.json> <kichban_A.txt> [<kichban_B.txt> ...]

In ra JSON: điểm khớp (0–1) của từng kịch bản, kịch bản khớp nhất và có chắc chắn không.
Điểm = tỷ lệ cụm 3 chữ liên tiếp của lời thoại xuất hiện trong lời nói (bỏ dấu câu, chữ thường).
Chắc chắn khi điểm cao nhất ≥ 0.25 và hơn điểm thứ hai ≥ 0.10.
"""
import json, re, sys, unicodedata


def toks(s):
    s = unicodedata.normalize("NFC", s).lower()
    return re.sub(r"[^\w\s]", " ", s).split()


def grams(ws, n=3):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def main(tr_path, scripts):
    tr = json.load(open(tr_path, encoding="utf-8"))
    spoken = grams(toks(" ".join(w["w"] for w in tr.get("words", []))))
    res = []
    for p in scripts:
        g = grams(toks(open(p, encoding="utf-8").read()))
        res.append({"kich_ban": p, "diem": round(len(g & spoken) / len(g), 3) if g else 0.0})
    res.sort(key=lambda r: -r["diem"])
    best = res[0] if res else None
    second = res[1]["diem"] if len(res) > 1 else 0.0
    sure = bool(best and best["diem"] >= 0.25 and best["diem"] - second >= 0.10)
    print(json.dumps({"khop_nhat": best["kich_ban"] if best else None, "chac_chan": sure, "diem": res},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
