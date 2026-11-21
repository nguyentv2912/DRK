# Giám sát: Mai (chien-luoc), phiên bản 2, vòng 1

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày: 2026-11-14 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File chấm: ke-hoach.md (bỏ qua ban-nhap-cu/). Đối chiếu: brief.md (mục Hiện trạng), phieu-giao-viec.md, tai-chinh.md/.json (bản vòng 2), nghien-cuu.md, fanpage/KENH.md, fanpage/brand.md.

## Kiểm chứng đã làm
- **Giá không đổi:** 100 USD/tháng, 1.000 USD "đồng hành 10 năm", ebook ~1.000.000 đ đều giữ nguyên. "Gói năm" và "gói 1.000 USD cho 12 tháng" lấy từ TC, có ghi "anh quyết, không đổi giá".
- **Số so với tai-chinh.json** (đọc bằng python): phễu 3 tháng của 3 kịch bản (người theo dõi 500/1.000/2.000 → 1.500/3.091/6.305; Skool 10/25/100 → 28/72/293; HV 0,11/0,56/3,44 → 0,21/1,10/6,99; doanh thu 0,28/1,46/8,93 → 0,62/3,22/21,10 tr; lãi T1 −2,33, T2 −1,15/4,90, T3 0,30/14,92) đều khớp. Khớp thêm: 78,0 tr / 32,0; hoà vốn 2 HV; hoàn vốn T6/T15; 114/10/~1 HV T24; 269,9/22,5 tr; 2.824,4/175,7/−93,6; 22/42/90 và 26/47/102; 46/91/183 (vào Skool 2/4/8%); 84 HV (huỷ 15%); gói 1.000 USD 114/105/77, 2.645,0/3.153,1, 300,5/1.244,1, 756/866/1.177, LTV 1.254/1.095/1.059; quỹ 104,4; trả góp 2.759,1; ngưỡng thuê và tháng thuê; mốc tháng 6 là 140/2,6/3,9 và 585/18,4/42,0; ebook T3 1,6 tr; Pro từ T5.
- **Lỗi đọc ngưỡng:** `tai-chinh.json → nguong_dung` có `cd_toi_thieu: 0.025` và `huy_toi_da: 0.12`; TC mục 5b định nghĩa đây là "chuyển đổi **miễn phí mới → 100 USD** ≥ 2,5%". Đường ngưỡng dùng tỷ lệ vào Skool **0,9%**. ke-hoach.md lại ghi "theo dõi mới → Skool < 2,5%" ở dòng 32, 417 và 459. Ngoài ra `ket_qua.than_trong` = False ở cả tháng 3 và tháng 6, tức kịch bản thận trọng **không qua ngưỡng**. Vậy mà dòng 11 lấy thận trọng làm "mục tiêu 90 ngày" và viết "Dưới mốc thận trọng là đang đi theo hướng không đáng làm".
- **Đề cương:** 5 tầng (FED → VCs → Protocol & dev → KOLs & media → Retail) đúng ghi chép, đủ 1.0–1.6. Khung 6 × 6 × 6 = 216, (2×3)³, chu kỳ BTC/altcoin, lặp ở 2 chu kỳ tiếp theo đều có (2.0–2.7). Mọi phần phương pháp đều để ô [chờ anh] (25 chỗ), không tự giải nghĩa "6", "2", "3".
- **Không hứa lợi nhuận:** grep "bao lời / chắc thắng / x lần / cam kết lợi" chỉ thấy trong danh sách cấm hoặc câu miễn trừ. Có 3 phương án câu chữ cho "216" theo 3 nơi dùng và 3 phương án cho "đồng hành lợi nhuận".
- **KENH:** khung giờ 05:30 / 08:00–09:00 / 11:30 / 12:00, 7 chuyên mục, KPI 30/90 ngày (≥ 25/≥ 80 ngày, 3 giây 50/60%, bình luận 5/20) và bài ghim "Bắt đầu từ đây" đều khớp KENH.md. Có chỉ ra xung đột với điều cấm "tôn giáo" trong brand.md dòng 24.
- **Nguồn NC:** 72 giờ email, không có tên miền riêng, Buy Now, trung vị 69–99 USD, phí 1–4%, Circle ≥ 15%, About → tham gia 18–20% (Thấp), NQ 05/2025, Luật 75/2025, Luật Tín ngưỡng Điều 5, TikTok/Meta đều khớp nghien-cuu.md.
- Độ dài: 8.396 chữ (47 KB); tóm tắt 567 chữ.

## Bảng chấm

| # | Tiêu chí | Trọng số | Chặn | % | Bằng chứng |
|---|---|---|---|---|---|
| 1 | Đủ mọi phần người dùng yêu cầu | 25 | Chặn | 92 | Có đủ tóm tắt và 8 mục được giao: phễu (mục 1), Skool (2), đề cương 2 khoá + ebook (3), câu chữ an toàn (4), nội dung nối KENH (5), 2 phương án gói 1.000 USD (6), 90 ngày + KPI + ngưỡng (7), Cần anh chốt (9), thêm Rủi ro (8). Đề cương bám đúng 5 tầng và 6×6×6. Thiếu: KPI chuyển đổi miễn phí → 100 USD (đúng chỉ số dừng của TC). Cách tận dụng ngân hàng/văn phòng chỉ có ở tuần 0 và Cần anh chốt #7 |
| 2 | Số liệu khớp tai-chinh.md, không tự đổi | 20 | Chặn | 75 | Hơn 60 số đã so đều khớp json. Nhưng ngưỡng 2,5% bị gán sai chỉ số ở 3 chỗ (dòng 32, 417, 459): TC là miễn phí → 100 USD, Mai ghi là theo dõi → Skool. Dòng 11 coi thận trọng là mức "đạt", ngược với `ket_qua.than_trong = False` |
| 3 | Rủi ro, lộ trình, KPI cụ thể và đo được | 20 | | 70 | Có 5 cổng (0–4) với ngưỡng bằng số, KPI theo tháng ghi rõ sàn/tham vọng, bảng 11 rủi ro có mức, dấu hiệu sớm và cách giảm. Nhưng cổng tháng 3 đo sai tỷ lệ, bảng 7.5 không có dòng chuyển đổi miễn phí → 100 USD ≥ 2,5%, và mục tiêu 90 ngày đặt ở kịch bản mà TC nói phải đổi cách bán |
| 4 | Câu đầu mỗi phần là kết luận có số | 15 | | 80 | Mục 1 (1 video/ngày, 1 lời mời), 2 (3 hạng), 5 (7 chuyên mục, 4/7), 6 (114 so với 77–105), 7 (4 cổng) đều đạt. Mục 3 chỉ có "2 phần". Câu đầu mục 4 không có số. Mục 8 Rủi ro không có câu kết luận |
| 5 | Đánh dấu điều cần xác minh | 10 | | 90 | 25 ô [chờ anh], "cần xác minh" cho hạng Skool, cấp độ, link bio TikTok, đuôi link, tính năng miễn trừ. Có ghi độ tin cậy NC (Thấp/Trung bình), có dòng "Cần luật sư xác nhận" về nhãn quảng cáo |
| 6 | Ngắn gọn, bảng cho thứ so sánh được | 10 | | 70 | Bảng dùng tốt: 3 hạng, 2 phương án gói, 3 phương án câu chữ, KPI. Nhưng dài 8.396 chữ, ngưỡng dừng nhắc lại 4 lần (dòng 32, 417–418, 461/468, 7.5) |

**Điểm = 25×0,92 + 20×0,75 + 20×0,70 + 15×0,80 + 10×0,90 + 10×0,70 = 23 + 15 + 14 + 12 + 9 + 7 = 80**

**Kết luận: ĐẠT** (80 ≥ 80; hai tiêu chí Chặn được 92% và 75%, đều ≥ 60%). Đạt sát ngưỡng. Phản hồi 1–2 phải sửa trước khi chuyển Hà, vì cổng tháng 3 đang đo sai chỉ số.

## Phản hồi (sắp theo mức quan trọng)
1. Ngưỡng 2,5% bị gán nhầm cho "theo dõi mới → Skool" (dòng 32, 417, 459) → sửa thành "chuyển đổi thành viên miễn phí mới → 100 USD < 2,5%", và thêm "huỷ > 12%/tháng" vào cổng tháng 3 đúng như TC 5b. Nếu cần ngưỡng vào Skool thì dùng 0,9% của đường tối thiểu (`nguong_dung.ty_le_vao_skool_tuong_ung`).
2. Mục tiêu 90 ngày đặt ở mức thận trọng, trong khi TC 5b ghi thận trọng "không qua ngưỡng" ở cả tháng 3 và tháng 6 → viết lại dòng 11: sàn số lượng là 55 thành viên / 1 HV (ngưỡng) nhưng tỷ lệ phải ≥ 2,5% chuyển đổi trả phí và ≤ 12% huỷ. Nói thẳng: nếu số thật giống thận trọng (2% / 15%) thì đổi cách bán ở tháng 3. Bỏ câu "dưới mốc thận trọng là không đáng làm".
3. Bảng KPI 7.5 thiếu chỉ số dừng chính → thêm dòng "Miễn phí mới → 100 USD: ≥ 2,5% (ngưỡng) / 3% (cơ sở)". Ghi rõ dòng "Theo dõi mới → Skool" là mức kịch bản, không phải ngưỡng dừng.
4. Câu đầu mục 3, mục 4 và mục 8 thiếu kết luận có số → ví dụ mục 3 "2 phần, 15 bài (7 + 8), 25 ô chờ anh"; mục 4 "3 phương án × 3 nơi dùng"; mục 8 thêm câu kết luận nêu 5 rủi ro mức Cao và rủi ro đứng đầu.
5. Tài liệu dài (8.396 chữ) và ngưỡng dừng lặp 4 lần → giữ ngưỡng ở mục 7.4, các chỗ khác chỉ dẫn "xem 7.4". Rút ngắn mục 2.3, 5.3 và phần "Gợi ý hình minh hoạ".
