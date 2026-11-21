#!/usr/bin/env python3
"""Tạo hồ sơ nhân sự team/nhan-su/<mã>/ (ho-so.md + nhat-ky.jsonl). Chạy lại không ghi đè hồ sơ đã có."""
import os
C = True  # tiêu chí Chặn
NS = [
 ("nghien-cuu","Lan","Nghiên cứu","Khối Dự án","Tra cứu thị trường, đối thủ, giá, số liệu ngành, pháp lý cho dự án được giao.",
  "Câu hỏi nghiên cứu, brief.md","nghien-cuu.md",
  [("Trả lời đủ các câu hỏi nghiên cứu",25,C),("Số liệu quan trọng có nguồn gốc đã mở (link)",25,C),("Không bịa; ghi rõ điều chưa tìm được và cách xác minh",20,C),("Ghi thời điểm và độ tin cậy từng dữ kiện",15,False),("Đúng mẫu: kết luận, bảng dữ kiện, câu hỏi mở, nguồn",15,False)]),
 ("tai-chinh","Hùng","Phân tích Tài chính","Khối Dự án","Lập mô hình tài chính: vốn, chi phí, doanh thu, hoà vốn, hoàn vốn, NPV/IRR, độ nhạy, kịch bản.",
  "brief.md, nghien-cuu.md","mo_hinh.py, tai-chinh.md, tai-chinh.json",
  [("Script chạy được và tái tạo đúng các số trong báo cáo",25,C),("Đủ chỉ số: vốn, hoà vốn, hoàn vốn, NPV, IRR, dòng tiền",20,C),("Phép tính hợp lý: đơn vị, dấu, biên lợi nhuận, không lỗi",15,C),("Bảng giả định có nguồn hoặc ghi 'giả định'",15,False),("Độ nhạy ±20% và 3 kịch bản",15,False),("Nhận định thẳng thắn, nói rõ khi không khả thi",10,False)]),
 ("chien-luoc","Mai","Chiến lược & Kế hoạch","Khối Dự án","Viết kế hoạch kinh doanh, mô hình kinh doanh, SWOT, rủi ro, lộ trình, KPI, điều kiện nhân rộng.",
  "brief.md, nghien-cuu.md, tai-chinh.md","ke-hoach.md",
  [("Đủ mọi phần người dùng yêu cầu",25,C),("Số liệu khớp tai-chinh.md, không tự đổi",20,C),("Rủi ro, lộ trình, KPI cụ thể và đo được",20,False),("Câu đầu mỗi phần là kết luận có số",15,False),("Đánh dấu điều cần xác minh",10,False),("Ngắn gọn, bảng cho thứ so sánh được",10,False)]),
 ("thiet-ke-demo","Tùng","Thiết kế Demo","Khối Dự án","Dựng trang HTML tương tác: demo dự án, máy tính tài chính, dashboard, landing page.",
  "brief.md, ke-hoach.md, tai-chinh.json","demo.html",
  [("Logic tính khớp mô hình tài chính (kiểm bằng node)",25,C),("Tuân thủ quy tắc trang (CDN, theme sáng/tối, không alert/iframe)",20,C),("Chạy tốt ở 400px, không cuộn ngang",20,False),("Đủ nội dung yêu cầu",20,False),("Thiết kế theo chủ đề, không rập khuôn",15,False)]),
 ("y-tuong-content","Ngọc","Ý tưởng & Content","Khối Nội dung","Chọn ý tưởng, viết hook và caption mạng xã hội.",
  "brief.md (hoặc fanpage/brand.md khi làm fanpage)","ideas.json, post.md",
  [("Không vi phạm điều cấm của brief/thương hiệu",25,C),("Đúng giọng thương hiệu và đối tượng",20,C),("Ý tưởng được chấm điểm có lý do",20,False),("Caption đúng khung và độ dài",20,False),("Hook ≤ 14 chữ, có sức hút",15,False)]),
 ("kich-ban-quay","Phong","Kịch bản Quay","Khối Nội dung","Viết lời thoại video 90–180 giây, hướng dẫn quay, kế hoạch edit.",
  "ideas.json, post.md","kichban.txt, huong_dan_quay.md, edit_plan.json",
  [("edit_plan.json hợp lệ, mọi trigger có nguyên văn trong lời thoại",25,C),("Thời lượng ước tính 90–180 giây",20,C),("Đúng nhịp: hook, vấn đề, chuyển ý, thân, chốt, CTA",20,False),("Hướng dẫn quay đủ, người không chuyên làm theo được",20,False),("Văn nói tự nhiên, câu ≤ 20 chữ",15,False)]),
 ("edit-video","Khoa","Edit Video","Khối Nội dung","Dựng video 9:16 từ video thô: cắt lỗi, phụ đề, thẻ chữ, nhạc nền.",
  "video thô, kichban.txt, edit_plan.json","video.mp4, video_cover.jpg, edit_log.md",
  [("Đúng thông số: 1080x1920, có tiếng, đúng thời lượng",25,C),("Phụ đề đúng chữ so với kịch bản",20,C),("Cắt hết câu vấp và khoảng lặng",20,False),("Thẻ chữ đúng lúc, không tràn khung, không che mặt",20,False),("edit_log.md đầy đủ",15,False)]),
 ("dang-link","Vy","Đăng & Phân phối","Khối Kênh","Lên lịch đăng, lưu media, gắn link — chỉ trên kênh được phép.",
  "post.md, video.mp4, brief.md/config","publish.json",
  [("Chỉ đăng đúng kênh được phép trong brief/config",30,C),("Đúng chế độ nháp hay tự đăng",25,C),("Media và link hoạt động",20,False),("Giờ đăng ở tương lai và hợp lý",15,False),("publish.json đầy đủ",10,False)]),
 ("tra-loi-bao-cao","Quân","Cộng đồng & Báo cáo","Khối Kênh","Lấy số liệu kênh, rút bài học, soạn trả lời bình luận, viết báo cáo.",
  "publish.json, số liệu kênh","report.md",
  [("Số liệu thật, không bịa, ghi rõ khi thiếu",30,C),("Bài học hành động được, dựa trên số",20,False),("Câu trả lời mẫu đúng giọng thương hiệu",20,False),("So sánh với kỳ trước",15,False),("Đúng mẫu báo cáo",15,False)]),
 ("kiem-dinh","Hà","Kiểm định Chất lượng","Chất lượng","Rà sản phẩm cuối của cả nhóm trước khi bàn giao.",
  "toàn bộ hồ sơ việc","kiem-dinh.md",
  [("Lỗi báo ra là lỗi thật, không bỏ sót lỗi nghiêm trọng",25,C),("Đủ các mục kiểm theo danh sách",25,False),("Tự tính lại các số quan trọng",20,False),("Phân mức lỗi hợp lý",15,False),("Kết luận rõ ĐẠT / CHƯA ĐẠT",15,False)]),
 ("giam-sat","Bảo","Giám sát","Chất lượng","Chấm từng phần việc của từng nhân viên theo tiêu chí trong hồ sơ, quyết định đạt hay làm lại, ghi nhật ký.",
  "hồ sơ nhân viên, file nộp","giam-sat/<mã>-vong<N>.md, dòng nhật ký",
  [("Chấm đúng thang tiêu chí và công thức điểm",30,C),("Có bằng chứng cho từng điểm",25,False),("Phản hồi cụ thể, sửa được",25,False),("Nhất quán giữa các lần chấm",20,False)]),
 ("phan-tich","Đức","Phân tích Hiệu suất","Hội đồng Cải tiến","Phân tích nhật ký và bảng điểm, tìm điểm yếu, đề xuất nâng cấp dựa trên dữ liệu.",
  "nhat-ky.jsonl, BANG_DIEM.md, file giám sát","nang-cap/<chu-kỳ>/phan-tich.md",
  [("Đề xuất dựa trên dữ liệu nhật ký, có bằng chứng",30,C),("Chỉ ra nguyên nhân gốc trong prompt",25,False),("Đoạn prompt sửa viết sẵn, cụ thể",25,False),("Có chỉ số đo hiệu quả chu kỳ sau",20,False)]),
 ("phan-bien","Trang","Phản biện","Hội đồng Cải tiến","Phản biện prompt, sản phẩm và đề xuất nâng cấp theo chuẩn chuyên gia.",
  "prompt, sản phẩm, phan-tich.md","nang-cap/<chu-kỳ>/phan-bien.md",
  [("Mỗi phản biện kèm đề xuất thay thế cụ thể",30,C),("Dựa trên chuẩn nghề, không cảm tính",25,False),("Phản biện đủ các đề xuất của Đức",25,False),("Phát hiện mâu thuẫn hoặc điểm mù thật",20,False)]),
]
base = "team/nhan-su"
for ma, ten, vai, khoi, nv, vao, ra, tc in NS:
    d = os.path.join(base, ma); os.makedirs(d, exist_ok=True)
    nk = os.path.join(d, "nhat-ky.jsonl")
    if not os.path.exists(nk): open(nk, "w").close()
    p = os.path.join(d, "ho-so.md")
    if os.path.exists(p): continue
    assert sum(w for _, w, _ in tc) == 100, ma
    rows = "\n".join(f"| {i+1} | {t} | {w} | {'Chặn' if c else ''} |" for i, (t, w, c) in enumerate(tc))
    open(p, "w", encoding="utf-8").write(f"""# Hồ sơ nhân sự — {ten} ({vai})

| Mục | Nội dung |
|---|---|
| Mã gọi (subagent_type) | `{ma}` |
| Bộ phận | {khoi} |
| Prompt | `.claude/agents/{ma}.md` |
| Phiên bản prompt | 1.0 |
| Người giám sát | Bảo – Giám sát{' (đánh giá bởi trưởng nhóm)' if ma=='giam-sat' else ''} |

## Công việc
{nv}

- **Nhận:** {vao}
- **Nộp:** {ra}

## Tiêu chuẩn hoàn thành
ĐẠT khi điểm ≥ 80 **và** không tiêu chí Chặn nào dưới 60%.

| # | Tiêu chí | Trọng số | Chặn |
|---|---|---|---|
{rows}

## Chỉ số theo dõi
Cập nhật tự động trong `team/BANG_DIEM.md` từ `nhat-ky.jsonl`: số việc, tỷ lệ đạt lần đầu, điểm trung bình, số vòng sửa trung bình, tiêu chí yếu nhất.

## Lịch sử phiên bản
| Phiên bản | Ngày | Thay đổi | Lý do (chu kỳ nâng cấp) |
|---|---|---|---|
| 1.0 | 2026-11-14 | Tạo hồ sơ | — |
""")
print("OK", len(NS), "hồ sơ")
