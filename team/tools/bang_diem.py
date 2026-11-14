#!/usr/bin/env python3
"""Tổng hợp nhật ký đánh giá của mọi nhân sự → team/BANG_DIEM.md.
Dùng: python3 team/tools/bang_diem.py [thư_mục_nhân_sự] [file_ra]"""
import json, os, re, sys
from collections import Counter, defaultdict

base = sys.argv[1] if len(sys.argv) > 1 else "team/nhan-su"
out = sys.argv[2] if len(sys.argv) > 2 else "team/BANG_DIEM.md"

def ho_so(ma):
    p = os.path.join(base, ma, "ho-so.md")
    s = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    ten = re.search(r"^# Hồ sơ nhân sự — (.+)$", s, re.M)
    pb = re.search(r"Phiên bản prompt \| ([\d.]+)", s)
    return (ten.group(1) if ten else ma), (pb.group(1) if pb else "?")

rows, canh_bao = [], []
for ma in sorted(os.listdir(base)):
    nk = os.path.join(base, ma, "nhat-ky.jsonl")
    if not os.path.isfile(nk):
        continue
    ten, pb = ho_so(ma)
    recs = []
    for i, line in enumerate(open(nk, encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError:
            canh_bao.append(f"{ma}/nhat-ky.jsonl dòng {i} không phải JSON hợp lệ")
    if not recs:
        rows.append((ma, ten, pb, 0, None, None, None, "—", "—", "chưa có dữ liệu"))
        continue
    by_job = defaultdict(list)
    for r in recs:
        by_job[r.get("ma_viec", "?") + "|" + r.get("nhiem_vu", "")].append(r)
    jobs = list(by_job.values())
    first_pass = sum(1 for j in jobs if min(j, key=lambda r: r.get("vong", 1)).get("ket_qua") == "ĐẠT")
    rounds = sum(max(r.get("vong", 1) for r in j) for j in jobs) / len(jobs)
    finals = [max(j, key=lambda r: r.get("vong", 1)) for j in jobs]
    avg = sum(r.get("diem", 0) for r in recs) / len(recs)
    crit = defaultdict(list)
    for r in recs:
        for k, v in (r.get("tieu_chi") or {}).items():
            crit[k].append(v)
    weak = min(crit.items(), key=lambda kv: sum(kv[1]) / len(kv[1])) if crit else None
    weak_s = f"{weak[0]} ({sum(weak[1])/len(weak[1]):.0f}%)" if weak else "—"
    errs = Counter(e for r in recs for e in (r.get("loi_chan") or []))
    err_s = "; ".join(f"{e} ×{n}" for e, n in errs.most_common(2)) or "—"
    # xu hướng theo phiên bản
    pv = defaultdict(list)
    for r in recs:
        pv[r.get("phien_ban", "?")].append(r.get("diem", 0))
    trend = " → ".join(f"v{k}: {sum(v)/len(v):.0f}" for k, v in sorted(pv.items()))
    not_done = sum(1 for r in finals if r.get("ket_qua") != "ĐẠT")
    flag = []
    if len(jobs) >= 3 and first_pass / len(jobs) < 0.6: flag.append("đạt lần đầu < 60%")
    if any(n >= 2 for n in errs.values()): flag.append("lỗi Chặn lặp lại")
    if not_done: flag.append(f"{not_done} việc chưa đạt")
    rows.append((ma, ten, pb, len(jobs), first_pass / len(jobs), avg, rounds, weak_s, err_s, ", ".join(flag) or "ổn", trend))

L = ["# Bảng điểm đội ngũ", "", "Tự động tạo từ `team/nhan-su/*/nhat-ky.jsonl` bởi `team/tools/bang_diem.py`. Không sửa tay.", "",
     "| Nhân sự | Phiên bản | Số việc | Đạt lần đầu | Điểm TB | Vòng sửa TB | Tiêu chí yếu nhất | Lỗi Chặn hay gặp | Cảnh báo |",
     "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r[3] == 0:
        L.append(f"| {r[1]} | {r[2]} | 0 | — | — | — | — | — | chưa có dữ liệu |")
    else:
        L.append(f"| {r[1]} | {r[2]} | {r[3]} | {r[4]:.0%} | {r[5]:.0f} | {r[6]:.1f} | {r[7]} | {r[8]} | {r[9]} |")
tr = [r for r in rows if r[3]]
if tr:
    L += ["", "## Điểm trung bình theo phiên bản prompt", ""] + [f"- {r[1]}: {r[10]}" for r in tr]
need = [r for r in tr if r[9] != "ổn"]
L += ["", "## Cần đưa vào chu kỳ nâng cấp", ""] + ([f"- {r[1]}: {r[9]}" for r in need] or ["- Chưa có"])
if canh_bao:
    L += ["", "## Cảnh báo dữ liệu", ""] + [f"- {c}" for c in canh_bao]
open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"OK {out}: {len(tr)} nhân sự có dữ liệu, {len(need)} cần nâng cấp")
