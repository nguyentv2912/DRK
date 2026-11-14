# Mô hình tài chính — Đầu Tư Bình An trên Skool (phiên bản 2, 24 tháng)

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người lập: Hùng – Tài chính · Mọi con số do `mo_hinh.py` tính (chạy lại: `python3 mo_hinh.py`). Đơn vị: **triệu đồng (tr)**, tỷ giá giả định 26.000 đ/USD.

## 5 kết luận chính

1. **Vốn ban đầu rất thấp: 78,0 tr**, trong đó 32,0 tr là quỹ dự phòng (tiền vẫn nằm trong tài khoản). Chi phí cố định khi chưa thuê ai chỉ ~2,1 tr/tháng + phí Skool.
2. **Hoà vốn hằng tháng chỉ cần 1 học viên trả 100 USD** (chưa thuê người, và vì công của anh không tính vào chi phí). Mỗi học viên 100 USD/tháng (≈2,60 tr) để lại ≈2,28 tr sau phí Skool Pro, phí chuyển tiền, thuế (gói Hobby: 2,10 tr). Rủi ro không nằm ở chi phí mà ở **có kéo được người trả 100 USD/tháng và giữ họ hay không**.
3. **Mốc thu nhập (lãi sau thuế, phí, lương nhân viên) — kịch bản cơ sở:** 50 tr/tháng cần ~22 học viên, 100 tr cần ~42, 200 tr cần ~90 học viên 100 USD đang hoạt động (đã tính bán kèm gói 1.000 USD và ebook). Nếu không bán được gói chuyên sâu/ebook: 26 / 47 / 102 học viên.
4. **Kịch bản cơ sở:** tháng 24 có ~191 học viên 100 USD, doanh thu 577,9 tr/tháng, lãi 472,2 tr/tháng; lãi luỹ kế 24 tháng (sau khi trừ vốn) 5.173,5 tr; hoàn vốn tháng 4. Thận trọng: ~24 học viên, lãi tháng 24 54,1 tr, hoàn vốn tháng 6. Lạc quan: ~800 học viên, lãi tháng 24 2.177,6 tr. **Biến quyết định là tỷ lệ huỷ và tỷ lệ chuyển đổi**, không phải chi phí. Lưu ý: kịch bản cơ sở cần kênh đạt ~99.004 người theo dõi và ~4.607 thành viên Skool miễn phí vào tháng 24 — đây là giả định, chưa có số thật của kênh.
5. **Gói 1.000 USD "đồng hành 10 năm" mang tiền về sớm nhưng tạo nghĩa vụ dài hạn:** 1.000 USD/120 tháng ≈ 8,3 USD/tháng, rẻ hơn 12 lần gói cơ bản. Kịch bản cơ sở: cuối tháng 24 có 538,9 tr doanh thu "chưa phục vụ" (rủi ro hoàn tiền nếu dừng). Nếu gói này bao gồm luôn khoá cơ bản và học viên chuyển sang hàng loạt (8%/tháng), tiền mặt 24 tháng trông đẹp hơn (5.652,0 so với 5.173,5 tr) nhưng người trả 100 USD tháng 24 còn ~127 (thay vì 191), doanh thu chưa phục vụ lên 2.206,8 tr, và đến tháng 60 phải phục vụ ~1.901 người so với 1.211. Đề xuất: gói 1.000 USD là **gói bổ sung**, yêu cầu duy trì thuê bao 100 USD; ghi nhận doanh thu phân bổ và trích 30% tiền thu vào quỹ phục vụ dài hạn (chờ anh chốt).

## 1. Giá (anh chốt) và giả định

| Sản phẩm | Giá | Quy đổi | Ghi chú |
|---|---|---|---|
| Khoá cơ bản (Con đường + Công thức đầu tư) | 100 USD/tháng | 2,60 tr/tháng | Thuê bao Skool |
| Khoá chuyên sâu "đồng hành 10 năm" | 1.000 USD | 26,0 tr | **Giả định: trả một lần**, là gói bổ sung (vẫn cần thuê bao 100 USD) — chờ anh |
| Ebook | 1,0 tr (≈38 USD) | — | Bản số, bán VND ngoài Skool (chuyển khoản/VietQR) — giả định |

| Giả định | Giá trị | Nguồn / lý do |
|---|---|---|
| Tỷ giá | 26.000 đ/USD | Giả định trong vùng 25.000–26.500; chờ Lan cập nhật tỷ giá ngày |
| Skool Hobby | 9 USD/tháng + 10% + 0,30 USD/giao dịch | nghien-cuu.md (tin cậy Trung bình, trích đoạn tìm kiếm — cần mở skool.com/pricing xác nhận) |
| Skool Pro | 99 USD/tháng + 2,9% + 0,30 USD/giao dịch; giao dịch > 900 USD: 3,9% + 0,30 USD (áp cho khoá 1.000 USD) | nghien-cuu.md (Trung bình, trích đoạn help.skool.com Payments FAQ). Mô hình tự chọn gói rẻ hơn mỗi tháng |
| Phí nhận tiền về VN | 2,0% | Giả định. nghien-cuu.md: payout qua Stripe Express do Skool tạo, VN có trong danh sách, về VND thứ Tư hằng tuần — chưa kiểm thử; phí quy đổi chưa rõ nên đặt 2% |
| Phí thu ebook | 1,0% | Giả định. Skool không bán file lẻ (nghien-cuu.md) → ebook bán VND qua chuyển khoản/cổng nội địa, hoặc gói thành khoá trả một lần trên Skool |
| Thuế | 7,0% doanh thu | Giả định: hộ/cá nhân kinh doanh dịch vụ 5% GTGT + 2% TNCN, tính từ đồng đầu tiên (thận trọng). nghien-cuu.md: ngưỡng không chịu thuế 500 tr/năm, báo chí nói NĐ 141/2026 nâng lên 1 tỷ — chưa đối chiếu; thuế khi bán qua nền tảng nước ngoài các nguồn mâu thuẫn. Hỏi cơ quan thuế |
| Công cụ AI, phần mềm | 1,6 tr/tháng | Giả định ~60 USD: 2 gói AI + Canva/CapCut Pro |
| Chi phí khác | 0,5 tr/tháng | Giả định: tên miền, email, họp online |
| Quảng cáo | 0,0 tr/tháng | Mặc định 0 — đầu phễu là video tự nhiên (brief) |
| Nhân công chủ dự án, đội AI, văn phòng | 0 | Brief: anh tự quay, đội AI có sẵn, hạ tầng có sẵn. Lãi trong mô hình = thu nhập của anh, chưa trừ công anh |
| Lịch ra mắt | Tháng 1 cộng đồng miễn phí; tháng 2 mở 100 USD; tháng 3 mở 1.000 USD và ebook | Giả định |
| Người theo dõi hiện có | 10.000 | Giả định — **thay bằng số thật của kênh** |
| Người theo dõi mới | 2.000/tháng, tăng 5%/tháng | Giả định: 1 video ngắn/ngày, tăng dần nhờ đều đặn (ramp-up) |
| Theo dõi mới → Skool miễn phí | 8% | Giả định: link trong hồ sơ/video, cộng đồng miễn phí, không rào cản |
| Theo dõi sẵn có → Skool miễn phí | 5% (rải 3 tháng đầu) | Giả định: lượt kêu gọi ra mắt |
| Thành viên miễn phí rời/ngủ | 5%/tháng | Giả định |
| Miễn phí mới → 100 USD (tháng đầu) | 3% | Giả định, nằm trong vùng tham khảo 2–5% (nghien-cuu.md, số SaaS); 100 USD/tháng (≈2,6 tr) cao so với thu nhập 25–40 tuổi ở VN nên lấy phía thấp |
| Kho miễn phí → 100 USD (mỗi tháng) | 0,3% | Giả định: chuyển đổi chậm nhờ nội dung + buổi live |
| Tỷ lệ huỷ 100 USD | 9%/tháng | nghien-cuu.md: cộng đồng trả phí 4–9%/tháng (TB ~5,8%; Circle: 10% là trung bình, ≥15% cần xử lý). Lấy cận trên vì giá cao với thu nhập VN và crypto biến động. Thời gian ở lại TB ≈ 11,1 tháng |
| Nâng cấp 1.000 USD | 1,5% học viên 100 USD/tháng | Giả định: ~1 trong 67 học viên/tháng; vé lớn cần tư vấn |
| Mua kèm ebook | 25% học viên 100 USD mới; 40% người mua 1.000 USD; 0,2% kho miễn phí/tháng | Giả định |
| Chiết khấu | 12%/năm | Giả định chi phí cơ hội vốn |

## 2. Vốn ban đầu

| Hạng mục | Triệu đồng | Ghi chú |
|---|---:|---|
| Thiết kế, dàn trang ebook | 8,0 | Giả định |
| Biên tập ebook | 5,0 | Giả định |
| Liên kết xuất bản qua nhà xuất bản (bắt buộc) | 15,0 | Ebook bán ra là xuất bản phẩm điện tử, cá nhân không tự xuất bản được (nghien-cuu.md). Số tiền là giả định — chờ báo giá NXB |
| Tư vấn pháp lý (điều khoản, nội dung tài chính/crypto) | 10,0 | Giả định |
| Thiết bị quay bổ sung (mic, đèn) | 5,0 | = 0 nếu anh đã đủ thiết bị |
| Nhận diện Skool, trang giới thiệu | 3,0 | Giả định |
| Quỹ dự phòng vận hành (3 tháng chi phí cố định + 1 CSKH bán thời gian) | 32,0 | Giả định |
| **Tổng** | **78,0** | |

## 3. Kết quả kịch bản cơ sở theo năm

| Chỉ tiêu (tr) | Năm 1 | Năm 2 |
|---|---:|---:|
| Doanh thu khoá 100 USD | 1.366,0 | 4.289,1 |
| Doanh thu khoá 1.000 USD (tiền thu) | 166,0 | 556,6 |
| Doanh thu ebook | 61,4 | 152,4 |
| **Tổng doanh thu** | 1.593,4 | 4.998,1 |
| Thuế | 111,5 | 349,9 |
| Lương nhân viên thuê thêm | 72,3 | 363,1 |
| Tổng chi phí (gồm thuế, phí Skool, chuyển tiền) | 317,2 | 1.022,8 |
| **Lãi (tiền mặt)** | 1.276,3 | 3.975,2 |
| Trích quỹ phục vụ gói 10 năm | 43,1 | 146,2 |
| Biên lãi | 80,1% | 79,5% |
| Học viên 100 USD cuối năm | 82 | 191 |
| Học viên 1.000 USD luỹ kế | 6 | 28 |

### Theo tháng (kịch bản cơ sở)

| Tháng | Skool free | HV 100 USD | Mua 1.000 USD | Ebook | Doanh thu | Chi phí | Lãi | Luỹ kế (sau vốn) | Gói Skool | Nhân sự |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 327 | 0 | 0,0 | 0,0 | 0,0 | 2,3 | -2,3 | -80,4 | Hobby | — |
| 2 | 634 | 11 | 0,0 | 0,0 | 28,5 | 7,8 | 20,7 | -59,6 | Hobby | — |
| 3 | 933 | 22 | 0,2 | 5,0 | 66,7 | 12,5 | 54,1 | -5,5 | Pro | — |
| 4 | 1.064 | 28 | 0,3 | 4,3 | 86,5 | 17,5 | 69,0 | 63,5 | Pro | ke_toan |
| 5 | 1.196 | 35 | 0,4 | 4,8 | 105,7 | 19,8 | 85,8 | 149,3 | Pro | ke_toan |
| 6 | 1.331 | 41 | 0,5 | 5,2 | 125,1 | 22,2 | 103,0 | 252,3 | Pro | ke_toan |
| 7 | 1.469 | 48 | 0,6 | 5,7 | 144,9 | 24,6 | 120,4 | 372,6 | Pro | ke_toan |
| 8 | 1.609 | 54 | 0,7 | 6,2 | 165,1 | 27,0 | 138,1 | 510,7 | Pro | ke_toan |
| 9 | 1.754 | 61 | 0,8 | 6,7 | 185,7 | 29,5 | 156,2 | 666,9 | Pro | ke_toan |
| 10 | 1.902 | 68 | 0,9 | 7,3 | 206,7 | 38,1 | 168,6 | 835,5 | Pro | cskh_bt, ke_toan |
| 11 | 2.054 | 75 | 1,0 | 7,8 | 228,2 | 51,6 | 176,6 | 1.012,1 | Pro | cskh_bt, dung_video, ke_toan |
| 12 | 2.211 | 82 | 1,1 | 8,4 | 250,3 | 64,2 | 186,1 | 1.198,3 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 13 | 2.373 | 90 | 1,2 | 8,9 | 273,0 | 67,0 | 205,9 | 1.404,2 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 14 | 2.540 | 98 | 1,3 | 9,5 | 296,3 | 70,0 | 226,3 | 1.630,5 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 15 | 2.713 | 106 | 1,4 | 10,2 | 320,3 | 73,0 | 247,3 | 1.877,7 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 16 | 2.892 | 114 | 1,5 | 10,8 | 345,1 | 76,2 | 268,9 | 2.146,6 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 17 | 3.078 | 122 | 1,6 | 11,5 | 370,7 | 79,4 | 291,2 | 2.437,9 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 18 | 3.271 | 131 | 1,7 | 12,2 | 397,1 | 82,8 | 314,3 | 2.752,2 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 19 | 3.472 | 140 | 1,8 | 12,9 | 424,5 | 86,3 | 338,3 | 3.090,5 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 20 | 3.681 | 150 | 1,9 | 13,6 | 452,9 | 89,9 | 363,1 | 3.453,6 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 21 | 3.898 | 159 | 2,1 | 14,4 | 482,4 | 93,6 | 388,8 | 3.842,4 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 22 | 4.124 | 169 | 2,2 | 15,2 | 513,0 | 97,5 | 415,5 | 4.257,9 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 23 | 4.360 | 180 | 2,3 | 16,1 | 544,8 | 101,5 | 443,3 | 4.701,3 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 24 | 4.607 | 191 | 2,5 | 17,0 | 577,9 | 105,7 | 472,2 | 5.173,5 | Pro | cskh_bt, chot_don, dung_video, ke_toan |

(Số học viên lẻ là trung bình kỳ vọng của mô hình, làm tròn khi hiển thị.)

## 4. Hoà vốn, hoàn vốn, NPV/IRR

| Chỉ tiêu | Thận trọng | Cơ sở | Lạc quan |
|---|---:|---:|---:|
| HV 100 USD cần để hoà vốn tháng | 2 | 1 | 1 |
| Tháng đầu tiên có lãi | 2 | 2 | 2 |
| Tháng hoàn vốn (luỹ kế ≥ 0) | 6 | 4 | 3 |
| NPV 24 tháng @12%/năm (tr) | 627,3 | 4.413,6 | 18.528,0 |
| IRR (năm) | 1.136% | 15.190% | 222.082% |

IRR rất cao vì vốn ban đầu rất nhỏ — chỉ số này không có ý nghĩa so sánh; nên nhìn số học viên và lãi tháng.

Đóng góp mỗi học viên 100 USD/tháng: gói Pro 2,28 tr, gói Hobby 2,10 tr. Chuyển Skool Hobby → Pro khi doanh thu qua Skool vượt ~1.268 USD/tháng (≈13 học viên).

### Số học viên 100 USD cần cho các mốc thu nhập (trạng thái ổn định, đã trừ lương người thuê theo ngưỡng)

| Lãi mục tiêu/tháng | Thận trọng | Cơ sở | Lạc quan | Cơ sở, không bán được 1.000 USD/ebook |
|---|---:|---:|---:|---:|
| Hoà vốn | 2 | 1 | 1 | 2 |
| 50 tr | 24 | 22 | 22 | 26 |
| 100 tr | 44 | 42 | 40 | 47 |
| 200 tr | 95 | 90 | 87 | 102 |

Khác biệt giữa các kịch bản ở đây do tỷ lệ huỷ (ảnh hưởng số người mua ebook) và tỷ lệ nâng cấp 1.000 USD.

## 5. Ba kịch bản (24 tháng)

| Biến | Thận trọng | Cơ sở | Lạc quan |
|---|---:|---:|---:|
| Người theo dõi mới tháng 1 | 1.000 | 2.000 | 3.500 |
| Tốc độ tăng người theo dõi mới/tháng | 3,0% | 5,0% | 6,0% |
| Theo dõi mới → Skool miễn phí | 5,0% | 8,0% | 10,0% |
| Miễn phí mới → 100 USD (tháng đầu) | 2,0% | 3,0% | 4,5% |
| Kho miễn phí → 100 USD (mỗi tháng) | 0,2% | 0,3% | 0,4% |
| Tỷ lệ huỷ/tháng | 15,0% | 9,0% | 6,0% |
| Nâng cấp 1.000 USD/tháng | 0,8% | 1,5% | 2,5% |
| Mua kèm ebook (HV 100 USD mới) | 15,0% | 25,0% | 35,0% |
| Người theo dõi tháng 24 | 44.426 | 99.004 | 187.855 |
| Thành viên Skool miễn phí tháng 24 | 1.203 | 4.607 | 11.262 |
| **HV 100 USD tháng 24** | 24 | 191 | 800 |
| **Doanh thu tháng 24 (tr)** | 69,5 | 577,9 | 2.560,4 |
| **Lãi tháng 24 (tr)** | 54,1 | 472,2 | 2.177,6 |
| Doanh thu năm 1 / năm 2 (tr) | 384,4 / 701,7 | 1.593,4 / 4.998,1 | 5.315,3 / 20.767,2 |
| Lãi năm 1 / năm 2 (tr) | 280,2 / 532,0 | 1.276,3 / 3.975,2 | 4.350,2 / 17.538,0 |
| **Lãi luỹ kế 24 tháng sau vốn (tr)** | 734,2 | 5.173,5 | 21.810,2 |

### Kịch bản phụ gói 1.000 USD (trên nền cơ sở)

| Phương án | HV 100 USD tháng 24 | Lãi tháng 24 (tr) | Lãi luỹ kế 24 tháng (tr) | Doanh thu chưa ghi nhận T24 (tr) | HV 100 USD tháng 60 | Người phải phục vụ T60 | Lãi tháng 60 (tr) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cơ sở: trả 1 lần, gói bổ sung | 191 | 472,2 | 5.173,5 | 538,9 | 1.211 | 1.211 | 3.145,4 |
| Trả góp 4 kỳ × 250 USD (10% bỏ ngang sau kỳ 1) | 191 | 464,8 | 5.063,4 | — | 1.211 | 1.211 | 3.102,6 |
| Gói 1.000 USD GỒM luôn khoá cơ bản (người nâng cấp ngừng trả 100 USD) | 175 | 435,7 | 4.854,1 | 538,9 | 1.095 | 1.391 | 2.878,7 |
| Gói GỒM khoá cơ bản và học viên chuyển sang hàng loạt (nâng cấp 8%/tháng) | 127 | 481,1 | 5.652,0 | 2.206,8 | 772 | 1.901 | 3.078,7 |

Cột tháng 60 chạy cùng giả định phễu đến năm thứ 5 (người theo dõi tiếp tục tăng) — chỉ để so sánh cấu trúc gói, không phải dự báo. "Người phải phục vụ" với phương án GỒM = HV 100 USD + toàn bộ người đã mua gói 10 năm (giả định họ ở lại, mức trần).

Giá trị trọn đời 1 học viên 100 USD mới (USD): gói bổ sung 1.254 (ở lại TB 11,1 tháng); gói GỒM, nâng cấp 1,5%/tháng 1.095; gói GỒM, nâng cấp 8%/tháng 1.059 — chênh lệch nhỏ về tiền, khác biệt nằm ở **số người phải phục vụ không thu phí hằng tháng trong 10 năm**.

## 6. Độ nhạy ±20% (kịch bản cơ sở)

Gốc: lãi tháng 24 = 472,2 tr; lãi luỹ kế 24 tháng = 5.173,5 tr.

| Biến | Giá trị gốc | Lãi T24 khi −20% | Lãi T24 khi +20% | Luỹ kế 24T khi −20% | Luỹ kế 24T khi +20% |
|---|---:|---:|---:|---:|---:|
| Người theo dõi mới/tháng | 2.000 | 375,5 | 562,9 | 4.208,2 | 6.152,9 |
| Tỷ lệ vào Skool miễn phí | 8,0% | 375,5 | 562,9 | 4.208,2 | 6.152,9 |
| Chuyển đổi miễn phí mới → 100 USD | 3,0% | 417,6 | 526,9 | 4.521,9 | 5.842,1 |
| Tỷ lệ huỷ/tháng | 9,0% | 524,0 | 424,1 | 5.682,4 | 4.746,0 |
| Chuyển đổi kho miễn phí → 100 USD | 0,3% | 429,7 | 514,5 | 4.761,8 | 5.599,6 |
| Tỷ lệ nâng cấp 1.000 USD | 1,5% | 462,2 | 481,9 | 5.057,9 | 5.286,0 |

Tỷ giá ±5%: lãi luỹ kế 24 tháng 4.909,3 tr (−5%) / 5.448,7 tr (+5%).

Nếu được áp ngưỡng không chịu thuế 1 tỷ đ/năm (chỉ tính thuế phần vượt — cách tính giả định, chờ cơ quan thuế): lãi luỹ kế 24 tháng Thận trọng 810,2 tr (+76,0) / Cơ sở 5.313,5 tr (+140,0) / Lạc quan 21.950,2 tr (+140,0).

### Lưới tỷ lệ huỷ × chuyển đổi — học viên 100 USD và lãi tháng 24 (tr)

Hệ số chuyển đổi nhân cả hai tỷ lệ chuyển đổi miễn phí → 100 USD của kịch bản cơ sở.

| Huỷ/tháng \ Chuyển đổi | ×0,50 (1,5%) | ×0,75 (2,2%) | ×1,00 (3,0%) | ×1,25 (3,8%) | ×1,50 (4,5%) |
|---|---:|---:|---:|---:|---:|
| 4% | 135 HV / 324,5 | 201 HV / 496,0 | 267 HV / 659,7 | 332 HV / 827,8 | 397 HV / 994,2 |
| 6% | 117 HV / 279,0 | 175 HV / 428,0 | 232 HV / 569,3 | 288 HV / 715,3 | 344 HV / 859,8 |
| 9% | 96 HV / 226,9 | 144 HV / 350,2 | 191 HV / 472,2 | 237 HV / 586,8 | 283 HV / 706,3 |
| 12% | 81 HV / 188,7 | 122 HV / 293,2 | 161 HV / 396,5 | 200 HV / 498,7 | 239 HV / 593,6 |
| 15% | 70 HV / 159,9 | 105 HV / 250,2 | 139 HV / 339,5 | 173 HV / 427,7 | 206 HV / 515,0 |
| 20% | 57 HV / 142,6 | 85 HV / 199,0 | 112 HV / 271,5 | 140 HV / 343,2 | 167 HV / 414,1 |

## 7. Khi nào mới thuê người

Quy tắc: chỉ thuê khi số liệu **tháng trước** chạm ngưỡng, và tổng lương không vượt 25% doanh thu tháng trước. Nhân viên chính thức tính thêm 21,5% chi phí bảo hiểm phía người sử dụng lao động. Lương là **giả định mặt bằng thị trường 2026**, chờ xác minh.

| Vị trí | Lương giả định (tr/tháng) | Ngưỡng thuê | Tháng thuê — Thận trọng | Cơ sở | Lạc quan |
|---|---:|---|---:|---:|---:|
| Trợ giảng/CSKH cộng đồng (bán thời gian) | 6,0 | ≥ 60 học viên trả phí (thay bằng bản toàn thời gian khi ≥ 200) | không | 10 | 5 |
| Trợ giảng/CSKH cộng đồng (toàn thời gian) | 10,0 | ≥ 200 học viên trả phí | không | không | 11 |
| Tư vấn/chốt đơn gói 1.000 USD (lương cứng + 5% hoa hồng) | 7,0 | Doanh thu ≥ 150 tr/tháng và ≥ 2.000 thành viên miễn phí | không | 12 | 6 |
| Dựng video/trợ lý nội dung | 9,0 | Doanh thu ≥ 200 tr/tháng (giải phóng thời gian anh) | không | 11 | 5 |
| CSKH cộng đồng thứ 2 | 10,0 | ≥ 500 học viên trả phí | không | không | 19 |
| Kế toán dịch vụ (thuê ngoài) | 2,5 | Doanh thu ≥ 40 tr/tháng | 10 | 4 | 3 |

"không" = trong 24 tháng chưa chạm ngưỡng, anh và đội AI tự làm. Không thuê trước doanh thu.

## 8. Gói "đồng hành 10 năm" thu một lần — rủi ro dòng tiền và cách xử lý

- **Nghĩa vụ dài hạn:** thu 1.000 USD một lần nhưng phải phục vụ 120 tháng. Doanh thu thực chất ≈ 8,3 USD/tháng/người. Nếu tiêu hết tiền thu ngay, các năm sau sẽ phục vụ không công; nếu dừng chương trình có thể phát sinh yêu cầu hoàn tiền phần chưa phục vụ.
- **Đề xuất ghi nhận:** ghi nhận ngay 20% (onboarding, tài liệu), phần 80% phân bổ đều 120 tháng. Kịch bản cơ sở: cuối tháng 24 còn **538,9 tr doanh thu chưa ghi nhận** (nghĩa vụ phải phục vụ).
- **Quỹ phục vụ dài hạn:** trích 30% tiền thực nhận (sau phí, thuế) mỗi lần bán gói 1.000 USD vào tài khoản riêng; cơ sở tháng 24 quỹ đạt **189,4 tr**. Lãi "tiêu được" = lãi tiền mặt − trích quỹ.
- **Điều khoản cần chốt (chờ anh + luật sư):** gói 1.000 USD có bao gồm khoá 100 USD không (mô hình giả định KHÔNG); "đồng hành" gồm gì cụ thể (số buổi live/năm, hỏi đáp), điều kiện chấm dứt/hoàn tiền, xử lý khi Skool đổi chính sách. Không cam kết lợi nhuận, không gọi kèo, không giữ tiền/ví hộ.
- **Thay thế an toàn hơn để anh cân nhắc:** gói 1.000 USD cho 12 tháng gia hạn được, hoặc trả góp — xem kịch bản phụ ở mục 5.

## 9. Nhận định

- Về chi phí, dự án gần như không thể lỗ nặng: vốn 78,0 tr, hoà vốn từ 1 học viên. Rủi ro thật là **doanh thu bằng 0** nếu không ai trả 100 USD/tháng.
- 100 USD/tháng (≈2,6 tr) là giá cao với người 25–40 tuổi ở VN; tỷ lệ huỷ quyết định quy mô: huỷ 4% vs 20% làm số học viên tháng 24 chênh 267 vs 112. Cần đo tỷ lệ huỷ thật ngay 2–3 tháng đầu.
- Số người theo dõi và tỷ lệ chuyển đổi là giả định — thay bằng số thật của kênh trong tháng 1 rồi chạy lại `mo_hinh.py`.
- Chưa xác minh (nghien-cuu.md mới ở mức tin cậy Trung bình/Thấp): phí Skool, payout Stripe Express về VN (phải thử 1 giao dịch thật), thuế khi bán qua nền tảng nước ngoài, chi phí liên kết xuất bản ebook. Khách trả USD còn chịu thêm ~1–4% phí đổi ngoại tệ phía thẻ — làm giá thực tế với khách cao hơn 100 USD, có thể kéo chuyển đổi xuống.
- Không cần dựng bộ máy: theo quy tắc ngưỡng, người đầu tiên (CSKH bán thời gian) chỉ thuê khi có ~60 học viên trả phí.
