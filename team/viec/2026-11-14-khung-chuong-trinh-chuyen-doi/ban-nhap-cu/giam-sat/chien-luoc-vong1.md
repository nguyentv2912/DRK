# Giám sát — Mai (chien-luoc) · Vòng 1

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày chấm: 14/11/2026 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File nộp: `ke-hoach.md` (669 dòng, 11.291 từ). Đầu vào: `brief.md`, `nghien-cuu.md`, `tai-chinh.md`, `tai-chinh.json`.
Nhiệm vụ (phiếu #5): (A) kế hoạch đầy đủ: khung phễu, gói, uy tín, pháp lý, lộ trình, KPI, rủi ro, sơ đồ phòng ban; (B) chiến lược và kế hoạch nội dung: định vị, kênh, trụ cột, định dạng, lịch 30 ngày, nội dung theo tầng phễu, KPI, tuân thủ.

## Bảo đã tự kiểm chứng những gì
- **So số tự động** bằng script (`scratchpad/so.py`). Script trích mọi con số trong ke-hoach.md (1.230 số), rồi so với tập giá trị trong `tai-chinh.json` và `tai-chinh.md` (có xét làm tròn, đổi %, đổi trđ↔đ). Kết quả: 41 dòng có số không khớp trực tiếp. Bảo rà tay cả 41 dòng:
  - **Số nghiên cứu** (88%, 55%, 70,5%, 34%, 27%, 4%, 81/81/76/67%, Mr Pips 1.568 tỷ/2.661 bị hại, ITP 225 trđ): grep thấy đủ trong nghien-cuu.md (ví dụ dòng 14, 18, 35, 36, 42).
  - **Số hiệu văn bản** (75/2025, 05/2025, 284/2026, 125/2024, 56/2024, mã ngành 8559/8560, Điều 15a, Điều 19): có trong NC (dòng 78…).
  - **Số Mai tự suy ra** (đều ghi "Mai tính từ TC"), Bảo tính lại và thấy khớp hết:
    - Lead tự nhiên = lead − ngân sách ÷ 0,06. T2: 550 − 500 = 50; T6: 705 − 500 = 205; T7: 1.243 − 1.000 = 243; T12: 1.436 − 1.000 = 436. Nhịp tăng: (900 − 50) ÷ 22 = 38,6, ghi "~39".
    - CPL bình quân: T2 30/550 = 54.545 đ (ghi ~54.500); T6 30/705 = 42.553 (ghi ~42.600); T12 60/1.436 = 41.783 (ghi ~41.800).
    - Phễu: 400 × 12% × 20% = 9,6; 400 × 8% × 25% = 8,0; cộng 17,6, khớp `kinh_te_don_vi_1000_lead.dong_hanh`. Có 32 buổi 1:1/1.000 lead; tiếp cận 50.000 = 1.000 ÷ 2%.
    - Số 1:1/tháng: T2–T6 lần lượt 220 × 8% = 17,6 và 282 × 8% = 22,6, ghi "~18–23".
    - Công suất coach: 40 ÷ 3 = 13,3, ghi "~13 khách mới/tháng". Đội nội dung 2/4/5 khớp `nhan_su_theo_bo_phan`.
- **Số TC lấy nguyên** (2.903; T19; T44; −1.813; NPV −233; IRR 9%; +17%/−28%/+31%; 15,8/31,6/44,7; 166,8/332,6/470,3; lương từng vị trí; thu nhập TVV 14,9/16,1/17,7; bảng phễu T1–T12; luỹ kế T1–T6; doanh thu 48,8…165,2; hoa hồng ngân hàng 9–27 trđ/năm; lỗ khi dừng 1,0–1,3 tỷ; pháp lý 30 + 5–6 trđ/tháng): script khớp toàn bộ, **không có số TC nào bị đổi**.
- **Đếm lịch 30 ngày** để kiểm câu tổng ở dòng 556. Video ngắn: ngày 2, 4, 6, 9, 12, 16, 18, 20, 24, 26, đủ 10. Video dài: ngày 8, 15, 22 (3 video) cộng live ngày 29. Bài Facebook: 10. Bài nhóm: ngày 7, 14, 21, 28 (4 bài). Quà học: ngày 5, 13, 27 (3 món). Tin Zalo OA: ngày 1, 11, 17, 23, 30 (5 tin). Đếm ra khớp hết với câu tổng.
- **Kiểm hai nhận định suy luận:**
  - Dòng 26 viết: "phễu phải tốt hơn cơ sở ~2,4 lần (25 ÷ 10,5), tức gần với kịch bản Lạc quan". Kịch bản Lạc quan trong mo_hinh.py (dòng 145) chỉ có hệ số chuyển đổi ×1,25, CPL ×0,85 và lead tự nhiên ×1,3. Bảo ước khách đồng hành theo Lạc quan chỉ cao hơn cơ sở khoảng 1,6–1,8 lần. Vậy cần 2,4 lần là **vượt xa** Lạc quan, chứ không phải "gần". Thêm nữa, ở ngân sách 30 trđ (~705 lead), trạng thái ổn định chỉ cho khoảng 12,4 khách/tháng (705 × 17,6/1.000). Nghĩa là **Cổng 25 khách gần như không thể đạt nếu chưa tăng ngân sách quảng cáo**, và lộ trình chưa nói cách xử lý điểm này.
  - Dòng 298 viết rằng ở mức 16 khách/tháng thì cần thêm coach (16 × 3 = 48 > 40). Nhưng bảng Cổng 3 (dòng 396) lại ghi "16 – <25: Đội 8 tự nuôi được (hoà vốn 15,8)". Hai chỗ mâu thuẫn nhau: thêm một cặp coach thì chi phí cố định tăng, nên hoà vốn thực tế phải cao hơn 15,8.

## Bảng chấm

| # | Tiêu chí (trọng số, Chặn) | % | Bằng chứng |
|---|---|---|---|
| 1 | Đủ mọi phần người dùng yêu cầu (25, Chặn) | 95 | Phần (A) có đủ: phễu 6 tầng (§3.2), nội dung từng bước (§3.3 khoá nền tảng 6 phần + 2 live; §3.4 đồng hành 12 tuần; §3.5 thành viên), gói và giá (§3.1), uy tín gồm ngân hàng, văn phòng và bộ minh bạch (§4.1–4.4), pháp lý (§5), sơ đồ phòng ban 3 giai đoạn + vai trò + quy trình bán/CSKH + KPI bộ phận (§6), lộ trình (§7), rủi ro (§8). Phần (B) có đủ: định vị và giọng điệu (§9), 5 trụ cột có tỷ trọng (§9), kênh và định dạng (§10), nội dung theo 6 tầng (§11), **lịch 30 ngày đủ 30 dòng** cộng nhịp tuần (§12), đội và quy trình duyệt (§13), checklist tuân thủ 10 câu (§14), KPI nội dung T1–T12 (§15). Trừ nhẹ: "mô hình tài chính sơ bộ" (brief) chỉ có trong tóm tắt và rải ở các mục, không có bảng tổng 3 kịch bản và vốn để chủ dự án đọc liền một chỗ |
| 2 | Số liệu khớp tai-chinh.md, không tự đổi (20, Chặn) | 95 | So tự động 1.230 số: không có số TC nào bị đổi. Số tự suy ra đều ghi nhãn "Mai tính từ TC", và Bảo tính lại thấy đúng (lead tự nhiên, CPL bình quân, 9,6/8,0, 18–23 buổi 1:1, 13 khách/cặp coach). Trừ vì câu dòng 26 so 2,4 lần là "gần Lạc quan", diễn giải sai so với hệ số kịch bản trong TC |
| 3 | Rủi ro, lộ trình, KPI cụ thể và đo được (20) | 80 | Rủi ro có 14 dòng, mỗi dòng có mức độ, dấu hiệu sớm và cách giảm thiểu; nhiều dấu hiệu có ngưỡng số (tham dự <30%, CPL tuần >72.000 đ, hoàn tiền >5%). Lộ trình có Cổng 0–4 kèm điều kiện số; bảng số tham chiếu T1–T6 dùng để so với số thật. KPI 3 tầng (bộ phận, nội dung, nội dung bổ trợ) đều có mục tiêu. Trừ vì: (a) Cổng 25 khách gần như không đạt được với ngân sách 30 trđ (trần khoảng 12 khách) mà lộ trình không nêu bước tăng ngân sách trước cổng; (b) mâu thuẫn hoà vốn đội 8 ở mức 16 khách (dòng 298 và 396); (c) bảng rủi ro không có cột người chịu trách nhiệm; (d) nhánh "giữ đội 8, T7–T12" chỉ ghi "xét lại mỗi tháng", không có mốc số |
| 4 | Câu đầu mỗi phần là kết luận có số (15) | 75 | Đạt ở §1, §3, §5 (200 trđ), §6, §9, §10, §12, §13, §14, §15 và các mục con 3.3, 3.4. Chưa đạt: §2 (câu định vị không có số), §7 (câu đầu không có số, số nằm ở câu thứ hai), §11 (không có câu kết luận), §4 và §8 chỉ có số yếu ("ba thứ", nêu tên vụ lừa đảo mà không kèm số) |
| 5 | Đánh dấu điều cần xác minh (10) | 90 | Có khung độ tin cậy ở đầu bài: NC tối đa TB, phải đối chiếu toàn văn luật. §5.2 có 10 câu hỏi cho luật sư, kèm Cổng 0 "chưa có ý kiến luật sư thì không chạy quảng cáo". Các chỗ cần xác minh đều được đánh dấu: tra trùng nhãn hiệu, sức chứa phòng, phí Zalo OA, danh sách quốc gia của Meta/TikTok/Google, VAT/BH/công đoàn, văn bản ngân hàng (10 điểm). Nhãn "giả định Mai" được dùng nhất quán. Trừ vì checklist §14 (cột căn cứ) và câu kết luận §5 nêu điều khoản cụ thể (Điều 15a, Điều 19, mức phạt 200 trđ) như sự thật đã chắc chắn, không gắn nhãn "cần luật sư xác nhận" tại chỗ |
| 6 | Ngắn gọn, bảng cho thứ so sánh được (10) | 70 | Dùng bảng gần như cho mọi thứ so sánh được, rất tốt. Nhưng tài liệu dài 11.291 từ, có nhiều chỗ lặp: các cổng 16/25/36 lặp ở §1, §6.5, §7 và phần minh hoạ; các tỷ lệ phễu lặp ở §3.2, §6.3, §6.5. Chủ dự án sẽ khó đọc hết |

**Điểm:** 25×0,95 + 20×0,95 + 20×0,80 + 15×0,75 + 10×0,90 + 10×0,70 = 23,75 + 19 + 16 + 11,25 + 9 + 7 = **86/100**

Tiêu chí Chặn: #1 = 95%, #2 = 95% (đều ≥ 60%).

## Kết luận: **ĐẠT** (86/100)

## Phản hồi (theo mức quan trọng)
1. Cổng 25 khách không đạt được với ngân sách 30 trđ (~705 lead nhân 17,6/1.000 chỉ ra khoảng 12 khách) → ở §7 thêm một bước "tăng ngân sách quảng cáo lên X trđ khi CPL ≤ 60.000 đ và tỷ lệ phễu đạt giả định" trước Cổng 4/Tăng trưởng (nhờ Hùng chạy số), hoặc đổi cổng thành tỷ lệ chuyển đổi trên 1.000 lead thay cho số khách tuyệt đối.
2. Dòng 26 ghi "2,4 lần … gần với kịch bản Lạc quan" là sai: Lạc quan chỉ khoảng 1,6–1,8 lần cơ sở → sửa thành "vượt cả kịch bản Lạc quan, nên ngoài cải thiện phễu còn phải tăng ngân sách hoặc lead tự nhiên" (gắn với phản hồi 1).
3. Mâu thuẫn hoà vốn đội 8: dòng 298 nói 16 khách thì cần thêm coach, còn dòng 396 ghi "Đội 8 tự nuôi được (hoà vốn 15,8)" → nhờ Hùng tính hoà vốn khi có 10 người (thêm một cặp coach + trợ giảng), rồi sửa ô ở dòng 396 cho thống nhất.
4. Câu đầu các mục §2, §7, §11 (cùng §4, §8) chưa là kết luận có số → viết lại. Ví dụ §7: "Mở rộng theo 5 cổng; quyết định lớn ở cuối T6: <8 khách thì dừng, ≥25 khách × 2 tháng thì lên 17 người". Ví dụ §11: "6 tầng × 3 chủ đề mẫu; tầng 1–2 chiếm khoảng 70% số bài".
5. Tài liệu 11.291 từ, lặp nhiều → mỗi nội dung chỉ để một chỗ (cổng ở §7, tỷ lệ phễu ở §3.2), các chỗ khác dẫn chiếu; thêm cột "người chịu trách nhiệm" cho bảng rủi ro §8; gắn "(cần luật sư xác nhận)" ngay cạnh Điều 15a, Điều 19, mức phạt 200 trđ ở §5 và §14.
