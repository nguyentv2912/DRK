# Giám sát: Mai (chien-luoc), phiên bản 2, vòng 2

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày: 2026-11-14 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File chấm: ke-hoach.md (bản sửa 23:44, bỏ qua ban-nhap-cu/). Đối chiếu: phản hồi vòng 1 (giam-sat/chien-luoc-v2-vong1.md), tai-chinh.md/.json, nghien-cuu.md, KENH.md.

## Kiểm chứng 5 phản hồi vòng 1
| # | Phản hồi vòng 1 | Đã sửa? | Bằng chứng |
|---|---|---|---|
| 1 | Ngưỡng 2,5% gắn nhầm cho theo dõi → Skool | Có | Dòng 11, 381, 413, 429 và 461 ghi "chuyển đổi thành viên miễn phí mới → 100 USD < 2,5% hoặc huỷ > 12%", khớp json `nguong_dung.cd_toi_thieu = 0.025`, `huy_toi_da = 0.12`. Dòng 426 ghi rõ tỷ lệ vào Skool là "giả định, không phải ngưỡng". Dòng 460: 2,5% vào Skool chỉ dùng làm dấu hiệu rủi ro, so với giả định thận trọng |
| 2 | Mục tiêu 90 ngày đặt ở mức thận trọng | Có | Dòng 11: mục tiêu là qua cổng tháng 3 (2 tỷ lệ + sàn 55/1). Dòng 11 và 415 nói thận trọng "đủ sàn nhưng không qua ngưỡng tỷ lệ", khớp `ket_qua.than_trong = {thang_3: False, thang_6: False}`. Câu "dưới mốc thận trọng là không đáng làm" đã bỏ |
| 3 | KPI thiếu chỉ số dừng | Có | Dòng 429 "Miễn phí mới → 100 USD ≥ 2,5% (ngưỡng) / 3% (cơ sở)", dòng 430 "Huỷ ≤ 12% (ngưỡng) / 9% (cơ sở)" |
| 4 | Câu đầu mục 3, 4, 8 thiếu số | Có, còn 2 lỗi đếm | Mục 3 (dòng 161): "15 bài (7 + 8), ~8 tuần, 15 ô [chờ anh]". Đếm lại: 7 ô ở 3.1 + 8 ô ở 3.2 = 15, đúng. Mục 4 (dòng 249): "3 phương án, 7 điều cấm, **1 câu miễn trừ cố định**", trong khi 4.3 có 3 câu (video / Skool / trang bán 1.000 USD). Mục 8 (dòng 455): "**5/10** rủi ro mức Cao", trong khi bảng có **11** dòng (5 Cao, 6 Trung bình) |
| 5 | Dài và lặp ngưỡng | Một phần | Ngưỡng chỉ còn đầy đủ ở 7.4, tóm tắt (dòng 32), 7.5 và mục 8 đều ghi "xem 7.4". Gợi ý hình đã rút còn 5 dòng ngắn. Nhưng tổng độ dài chỉ giảm 8.396 → 8.232 chữ (−2%). 2.3 (12 dòng) và 5.3 (10 ý tưởng) chưa rút |

Kiểm lại phần không đổi: giá 100 USD / 1.000 USD / ~1 triệu giữ nguyên. Các số TC ở tóm tắt, mục 1, 6, 7.5, 7.6 không đổi so với vòng 1, đã khớp json. Đề cương vẫn bám 5 tầng và 6×6×6, tổng 25 ô [chờ anh]. Không có câu hứa lợi nhuận.

## Bảng chấm

| # | Tiêu chí | Trọng số | Chặn | % | Bằng chứng |
|---|---|---|---|---|---|
| 1 | Đủ mọi phần người dùng yêu cầu | 25 | Chặn | 95 | Đủ tóm tắt và 8 mục, đã thêm KPI chuyển đổi trả phí và huỷ. Phần tận dụng ngân hàng/văn phòng vẫn mỏng (tuần 0 + Cần anh chốt #7) |
| 2 | Số liệu khớp tai-chinh.md, không tự đổi | 20 | Chặn | 92 | Ngưỡng 5b đọc đúng chỉ số. Thận trọng "không qua" khớp json. Còn 2 số đếm nội bộ sai: "5/10" (thực tế 11 rủi ro), "1 câu miễn trừ" (thực tế 3) |
| 3 | Rủi ro, lộ trình, KPI cụ thể và đo được | 20 | | 90 | 5 cổng, cổng 3–4 quyết bằng 2 tỷ lệ có số. KPI tách ngưỡng / cơ sở. Rủi ro có dấu hiệu sớm gắn đúng ngưỡng |
| 4 | Câu đầu mỗi phần là kết luận có số | 15 | | 88 | Cả 8 mục đều mở bằng kết luận có số. Trừ điểm vì 2 con số đếm sai ở mục 4 và mục 8 |
| 5 | Đánh dấu điều cần xác minh | 10 | | 90 | Như vòng 1: 25 ô [chờ anh], các mục "cần xác minh", ghi độ tin cậy NC, có dòng cần luật sư |
| 6 | Ngắn gọn, bảng cho thứ so sánh được | 10 | | 72 | Hết lặp ngưỡng, gợi ý hình đã gọn. Nhưng tài liệu chỉ ngắn đi 2%, 2.3 và 5.3 chưa rút |

**Điểm = 25×0,95 + 20×0,92 + 20×0,90 + 15×0,88 + 10×0,90 + 10×0,72 = 23,75 + 18,4 + 18 + 13,2 + 9 + 7,2 = 89,55 ≈ 90**

**Kết luận: ĐẠT** (90 ≥ 80; hai tiêu chí Chặn được 95% và 92%). Lỗi vòng 1 về ngưỡng dừng đã sửa hết.

## Phản hồi (sắp theo mức quan trọng, sửa nhanh trước khi chuyển Hà)
1. Dòng 455 "5/10 rủi ro mức Cao" sai, bảng có 11 rủi ro → sửa thành "5/11".
2. Dòng 249 "1 câu miễn trừ cố định" sai, 4.3 có 3 câu → sửa thành "3 câu miễn trừ cố định (video, Skool, trang bán 1.000 USD)".
3. Tài liệu vẫn dài (8.232 chữ) → rút 2.3 còn các nghi thức chính, 5.3 còn 5 ý tưởng (số 1, 2, 3, 5, 10), phần còn lại đưa vào kho kịch bản của đội content.
4. Cách tận dụng ngân hàng hỗ trợ và văn phòng chỉ có ở tuần 0 và Cần anh chốt → thêm 2–3 dòng ở mục 1 hoặc 2 (ví dụ live offline tại văn phòng cho học viên 1.000 USD; ghi tên ngân hàng chỉ khi có văn bản đồng ý).
