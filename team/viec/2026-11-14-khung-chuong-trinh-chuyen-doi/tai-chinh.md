# Mô hình tài chính — Đầu Tư Bình An trên Skool (phiên bản 2, 24 tháng)

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người lập: Hùng – Tài chính · Mọi con số do `mo_hinh.py` tính (chạy lại: `python3 mo_hinh.py`). Đơn vị: **triệu đồng (tr)**, tỷ giá giả định 26.000 đ/USD.

## 5 kết luận chính

1. **Vốn ban đầu rất thấp: 63,0 tr**, trong đó 32,0 tr là quỹ dự phòng (tiền vẫn nằm trong tài khoản). Chi phí cố định khi chưa thuê ai chỉ ~2,1 tr/tháng + phí Skool.
2. **Hoà vốn hằng tháng chỉ cần 1 học viên trả 100 USD** (chưa thuê người). Mỗi học viên 100 USD/tháng (≈2,60 tr) để lại ≈2,28 tr sau phí Skool Pro, phí chuyển tiền, thuế (gói Hobby: 2,11 tr). Rủi ro không nằm ở chi phí mà ở **có kéo được người trả 100 USD/tháng và giữ họ hay không**.
3. **Mốc thu nhập (lãi sau thuế, phí, lương nhân viên) — kịch bản cơ sở:** 50 tr/tháng cần ~22 học viên, 100 tr cần ~41, 200 tr cần ~90 học viên 100 USD đang hoạt động (đã tính bán kèm gói 1.000 USD và ebook). Nếu không bán được gói chuyên sâu/ebook: 26 / 47 / 102 học viên.
4. **Kịch bản cơ sở:** tháng 24 có ~161 học viên 100 USD, doanh thu 491,1 tr/tháng, lãi 397,0 tr/tháng; lãi luỹ kế 24 tháng (sau khi trừ vốn) 4.504,3 tr; hoàn vốn tháng 3. Thận trọng: ~20 học viên, lãi tháng 24 46,0 tr, hoàn vốn tháng 5. Lạc quan: ~707 học viên, lãi tháng 24 1.932,9 tr. **Biến quyết định là tỷ lệ huỷ và tỷ lệ chuyển đổi**, không phải chi phí.
5. **Gói 1.000 USD "đồng hành 10 năm" là rủi ro lớn nhất về cấu trúc:** 1.000 USD/120 tháng ≈ 8,3 USD/tháng, rẻ hơn 12 lần gói cơ bản; học viên chỉ cần ở lại 10 tháng là gói 10 năm đã rẻ hơn. Nếu gói này bao gồm luôn khoá cơ bản và học viên chuyển sang hàng loạt (8%/tháng), tiền mặt 24 tháng **trông đẹp hơn** (luỹ kế 5.114,0 tr so với 4.504,3 tr) vì thu trước, nhưng người trả 100 USD tháng 24 chỉ còn ~112 (thay vì 161), đến tháng 60 lãi tháng còn 2.727,4 tr so với 2.607,0 tr của phương án gói bổ sung, trong khi vẫn phải phục vụ người đã trả trước 10 năm. Đề xuất: gói 1.000 USD là **gói bổ sung**, yêu cầu duy trì thuê bao 100 USD; ghi nhận doanh thu phân bổ và trích 30% tiền thu vào quỹ phục vụ dài hạn (chờ anh chốt).

## 1. Giá (anh chốt) và giả định

| Sản phẩm | Giá | Quy đổi | Ghi chú |
|---|---|---|---|
| Khoá cơ bản (Con đường + Công thức đầu tư) | 100 USD/tháng | 2,60 tr/tháng | Thuê bao Skool |
| Khoá chuyên sâu "đồng hành 10 năm" | 1.000 USD | 26,0 tr | **Giả định: trả một lần**, là gói bổ sung (vẫn cần thuê bao 100 USD) — chờ anh |
| Ebook | 1,0 tr (≈38 USD) | — | Bản số, bán VND ngoài Skool (chuyển khoản/VietQR) — giả định |

| Giả định | Giá trị | Nguồn / lý do |
|---|---|---|
| Tỷ giá | 26.000 đ/USD | Giả định trong vùng 25.000–26.500; chờ Lan cập nhật tỷ giá ngày |
| Skool Hobby | 9 USD/tháng + 10% mỗi giao dịch | Thông tin công khai phổ biến — **chờ Lan xác minh** |
| Skool Pro | 99 USD/tháng + 2,9% + 0,30 USD/giao dịch | **Chờ Lan xác minh**. Mô hình tự chọn gói rẻ hơn mỗi tháng |
| Phí rút tiền về VN | 2,0% | Giả định (trung gian rút USD + chênh lệch quy đổi). Cách nhận tiền từ Skool về VN chờ Lan xác minh |
| Phí thu ebook | 1,0% | Giả định |
| Thuế | 7,0% doanh thu | Giả định: cá nhân/hộ kinh doanh dịch vụ 5% GTGT + 2% TNCN, tính từ đồng đầu tiên (thận trọng, chưa trừ ngưỡng miễn thuế doanh thu thấp). Cần kế toán xác nhận; có thể phải lập doanh nghiệp khi lớn |
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
| Miễn phí mới → 100 USD (tháng đầu) | 3% | Giả định: 100 USD/tháng (≈2,6 tr) cao so với thu nhập 25–40 tuổi ở VN nên đặt thấp (2–5% là vùng hay gặp ở cộng đồng trả phí) |
| Kho miễn phí → 100 USD (mỗi tháng) | 0,3% | Giả định: chuyển đổi chậm nhờ nội dung + buổi live |
| Tỷ lệ huỷ 100 USD | 12%/tháng | Giả định: thời gian ở lại TB ≈ 8,3 tháng; giá cao + thị trường crypto biến động dễ huỷ |
| Nâng cấp 1.000 USD | 1,5% học viên 100 USD/tháng | Giả định: ~1 trong 67 học viên/tháng; vé lớn cần tư vấn |
| Mua kèm ebook | 25% học viên 100 USD mới; 40% người mua 1.000 USD; 0,2% kho miễn phí/tháng | Giả định |
| Chiết khấu | 12%/năm | Giả định chi phí cơ hội vốn |

## 2. Vốn ban đầu

| Hạng mục | Triệu đồng | Ghi chú |
|---|---:|---|
| Thiết kế, dàn trang ebook | 8,0 | Giả định |
| Biên tập ebook | 5,0 | Giả định |
| ISBN / xuất bản (tuỳ chọn) | 0,0 | Tuỳ chọn, mặc định không làm (~15 tr nếu xuất bản có ISBN — giả định) |
| Tư vấn pháp lý (điều khoản, nội dung tài chính/crypto) | 10,0 | Giả định |
| Thiết bị quay bổ sung (mic, đèn) | 5,0 | = 0 nếu anh đã đủ thiết bị |
| Nhận diện Skool, trang giới thiệu | 3,0 | Giả định |
| Quỹ dự phòng vận hành (3 tháng chi phí cố định + 1 CSKH bán thời gian) | 32,0 | Giả định |
| **Tổng** | **63,0** | |

## 3. Kết quả kịch bản cơ sở theo năm

| Chỉ tiêu (tr) | Năm 1 | Năm 2 |
|---|---:|---:|
| Doanh thu khoá 100 USD | 1.254,5 | 3.678,1 |
| Doanh thu khoá 1.000 USD (tiền thu) | 153,6 | 482,6 |
| Doanh thu ebook | 61,2 | 151,3 |
| **Tổng doanh thu** | 1.469,4 | 4.312,0 |
| Thuế | 102,9 | 301,8 |
| Lương nhân viên thuê thêm | 55,2 | 359,4 |
| Tổng chi phí (gồm thuế, phí Skool, chuyển tiền) | 283,3 | 930,6 |
| **Lãi (tiền mặt)** | 1.186,0 | 3.381,3 |
| Trích quỹ phục vụ gói 10 năm | 39,9 | 126,8 |
| Biên lãi | 80,7% | 78,4% |
| Học viên 100 USD cuối năm | 73 | 161 |
| Học viên 1.000 USD luỹ kế | 6 | 24 |

### Theo tháng (kịch bản cơ sở)

| Tháng | Skool free | HV 100 USD | Mua 1.000 USD | Ebook | Doanh thu | Chi phí | Lãi | Luỹ kế (sau vốn) | Gói Skool | Nhân sự |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 327 | 0 | 0,0 | 0,0 | 0,0 | 2,3 | -2,3 | -65,4 | Hobby | — |
| 2 | 634 | 11 | 0,0 | 0,0 | 28,5 | 7,7 | 20,8 | -44,5 | Hobby | — |
| 3 | 933 | 22 | 0,2 | 5,0 | 65,8 | 12,4 | 53,4 | 8,9 | Pro | — |
| 4 | 1.064 | 27 | 0,3 | 4,3 | 83,9 | 17,1 | 66,8 | 75,7 | Pro | ke_toan |
| 5 | 1.196 | 33 | 0,4 | 4,8 | 100,9 | 19,1 | 81,8 | 157,4 | Pro | ke_toan |
| 6 | 1.331 | 39 | 0,5 | 5,2 | 117,9 | 21,2 | 96,7 | 254,2 | Pro | ke_toan |
| 7 | 1.469 | 44 | 0,6 | 5,7 | 135,0 | 23,2 | 111,8 | 365,9 | Pro | ke_toan |
| 8 | 1.609 | 50 | 0,6 | 6,2 | 152,2 | 25,3 | 126,9 | 492,8 | Pro | ke_toan |
| 9 | 1.754 | 55 | 0,7 | 6,7 | 169,6 | 27,4 | 142,2 | 635,0 | Pro | ke_toan |
| 10 | 1.902 | 61 | 0,8 | 7,2 | 187,2 | 29,5 | 157,7 | 792,7 | Pro | ke_toan |
| 11 | 2.054 | 67 | 0,9 | 7,8 | 205,1 | 37,6 | 167,4 | 960,2 | Pro | cskh_bt, ke_toan |
| 12 | 2.211 | 73 | 1,0 | 8,3 | 223,3 | 60,5 | 162,8 | 1.123,0 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 13 | 2.373 | 79 | 1,0 | 8,9 | 242,0 | 62,8 | 179,2 | 1.302,2 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 14 | 2.540 | 86 | 1,1 | 9,5 | 261,2 | 65,2 | 195,9 | 1.498,1 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 15 | 2.713 | 92 | 1,2 | 10,1 | 280,8 | 67,7 | 213,1 | 1.711,2 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 16 | 2.892 | 99 | 1,3 | 10,7 | 301,1 | 70,3 | 230,8 | 1.942,0 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 17 | 3.078 | 106 | 1,4 | 11,4 | 322,0 | 72,9 | 249,1 | 2.191,1 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 18 | 3.271 | 113 | 1,5 | 12,1 | 343,6 | 75,6 | 268,0 | 2.459,1 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 19 | 3.472 | 120 | 1,6 | 12,8 | 365,9 | 78,4 | 287,5 | 2.746,7 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 20 | 3.681 | 128 | 1,7 | 13,5 | 389,1 | 81,3 | 307,8 | 3.054,5 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 21 | 3.898 | 136 | 1,8 | 14,3 | 413,1 | 84,3 | 328,8 | 3.383,3 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 22 | 4.124 | 144 | 1,9 | 15,1 | 438,1 | 87,4 | 350,7 | 3.733,9 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 23 | 4.360 | 152 | 2,0 | 16,0 | 464,1 | 90,7 | 373,4 | 4.107,3 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 24 | 4.607 | 161 | 2,1 | 16,9 | 491,1 | 94,1 | 397,0 | 4.504,3 | Pro | cskh_bt, chot_don, dung_video, ke_toan |

(Số học viên lẻ là trung bình kỳ vọng của mô hình, làm tròn khi hiển thị.)

## 4. Hoà vốn, hoàn vốn, NPV/IRR

| Chỉ tiêu | Thận trọng | Cơ sở | Lạc quan |
|---|---:|---:|---:|
| HV 100 USD cần để hoà vốn tháng | 2 | 1 | 1 |
| Tháng đầu tiên có lãi | 2 | 2 | 2 |
| Tháng hoàn vốn (luỹ kế ≥ 0) | 5 | 3 | 3 |
| NPV 24 tháng @12%/năm (tr) | 560,7 | 3.851,8 | 16.883,1 |
| IRR (năm) | 1.454% | 22.061% | 387.459% |

IRR rất cao vì vốn ban đầu rất nhỏ — chỉ số này không có ý nghĩa so sánh; nên nhìn số học viên và lãi tháng.

Đóng góp mỗi học viên 100 USD/tháng: gói Pro 2,28 tr, gói Hobby 2,11 tr. Chuyển Skool Hobby → Pro khi doanh thu qua Skool vượt ~1.268 USD/tháng (≈13 học viên).

### Số học viên 100 USD cần cho các mốc thu nhập (trạng thái ổn định, đã trừ lương người thuê theo ngưỡng)

| Lãi mục tiêu/tháng | Thận trọng | Cơ sở | Lạc quan | Cơ sở, không bán được 1.000 USD/ebook |
|---|---:|---:|---:|---:|
| Hoà vốn | 2 | 1 | 1 | 2 |
| 50 tr | 23 | 22 | 21 | 26 |
| 100 tr | 44 | 41 | 39 | 47 |
| 200 tr | 94 | 90 | 86 | 102 |

Khác biệt giữa các kịch bản ở đây do tỷ lệ huỷ (ảnh hưởng số người mua ebook) và tỷ lệ nâng cấp 1.000 USD.

## 5. Ba kịch bản (24 tháng)

| Biến | Thận trọng | Cơ sở | Lạc quan |
|---|---:|---:|---:|
| Người theo dõi mới tháng 1 | 1.000 | 2.000 | 3.500 |
| Tốc độ tăng người theo dõi mới/tháng | 3,0% | 5,0% | 6,0% |
| Theo dõi mới → Skool miễn phí | 5,0% | 8,0% | 10,0% |
| Miễn phí mới → 100 USD (tháng đầu) | 2,0% | 3,0% | 4,5% |
| Kho miễn phí → 100 USD (mỗi tháng) | 0,2% | 0,3% | 0,4% |
| Tỷ lệ huỷ/tháng | 18,0% | 12,0% | 8,0% |
| Nâng cấp 1.000 USD/tháng | 0,8% | 1,5% | 2,5% |
| Mua kèm ebook (HV 100 USD mới) | 15,0% | 25,0% | 35,0% |
| Người theo dõi tháng 24 | 44.426 | 99.004 | 187.855 |
| Thành viên Skool miễn phí tháng 24 | 1.203 | 4.607 | 11.262 |
| **HV 100 USD tháng 24** | 20 | 161 | 707 |
| **Doanh thu tháng 24 (tr)** | 60,3 | 491,1 | 2.274,9 |
| **Lãi tháng 24 (tr)** | 46,0 | 397,0 | 1.932,9 |
| Doanh thu năm 1 / năm 2 (tr) | 354,4 / 612,3 | 1.469,4 / 4.312,0 | 5.035,4 / 18.703,7 |
| Lãi năm 1 / năm 2 (tr) | 262,5 / 454,0 | 1.186,0 / 3.381,3 | 4.114,2 / 15.797,3 |
| **Lãi luỹ kế 24 tháng sau vốn (tr)** | 653,5 | 4.504,3 | 19.848,5 |

### Kịch bản phụ gói 1.000 USD (trên nền cơ sở)

| Phương án | HV 100 USD tháng 24 | Lãi tháng 24 (tr) | Lãi luỹ kế 24 tháng (tr) | Doanh thu chưa ghi nhận T24 (tr) | HV 100 USD tháng 60 | Lãi tháng 60 (tr) |
|---|---:|---:|---:|---:|---:|---:|
| Cơ sở: trả 1 lần, gói bổ sung | 161 | 397,0 | 4.504,3 | 473,8 | 998 | 2.607,0 |
| Trả góp 4 kỳ × 250 USD (10% bỏ ngang sau kỳ 1) | 161 | 390,2 | 4.402,7 | — | 998 | 2.567,8 |
| Gói 1.000 USD GỒM luôn khoá cơ bản (người nâng cấp ngừng trả 100 USD) | 149 | 369,8 | 4.255,3 | 473,8 | 918 | 2.422,5 |
| Gói GỒM khoá cơ bản và học viên chuyển sang hàng loạt (nâng cấp 8%/tháng) | 112 | 425,9 | 5.114,0 | 1.986,7 | 679 | 2.727,4 |

Cột tháng 60 chạy cùng giả định phễu đến năm thứ 5 (người theo dõi tiếp tục tăng) — chỉ để so sánh cấu trúc gói, không phải dự báo.

## 6. Độ nhạy ±20% (kịch bản cơ sở)

Gốc: lãi tháng 24 = 397,0 tr; lãi luỹ kế 24 tháng = 4.504,3 tr.

| Biến | Giá trị gốc | Lãi T24 khi −20% | Lãi T24 khi +20% | Luỹ kế 24T khi −20% | Luỹ kế 24T khi +20% |
|---|---:|---:|---:|---:|---:|
| Tỷ lệ vào Skool miễn phí | 8,0% | 314,1 | 479,9 | 3.669,5 | 5.376,3 |
| Người theo dõi mới/tháng | 2.000 | 314,1 | 479,9 | 3.669,5 | 5.376,3 |
| Chuyển đổi miễn phí mới → 100 USD | 3,0% | 351,1 | 442,9 | 3.941,8 | 5.083,8 |
| Tỷ lệ huỷ/tháng | 12,0% | 455,8 | 350,2 | 5.046,1 | 4.061,1 |
| Chuyển đổi kho miễn phí → 100 USD | 0,3% | 360,5 | 433,3 | 4.142,0 | 4.881,4 |
| Tỷ lệ nâng cấp 1.000 USD | 1,5% | 388,3 | 405,5 | 4.400,8 | 4.605,4 |

Tỷ giá ±5%: lãi luỹ kế 24 tháng 4.275,1 tr (−5%) / 4.744,5 tr (+5%).

### Lưới tỷ lệ huỷ × chuyển đổi — học viên 100 USD và lãi tháng 24 (tr)

Hệ số chuyển đổi nhân cả hai tỷ lệ chuyển đổi miễn phí → 100 USD của kịch bản cơ sở.

| Huỷ/tháng \ Chuyển đổi | ×0,50 (1,5%) | ×0,75 (2,2%) | ×1,00 (3,0%) | ×1,25 (3,8%) | ×1,50 (4,5%) |
|---|---:|---:|---:|---:|---:|
| 6% | 117 HV / 279,4 | 175 HV / 428,5 | 232 HV / 570,0 | 288 HV / 716,2 | 344 HV / 860,9 |
| 9% | 96 HV / 227,3 | 144 HV / 350,7 | 191 HV / 472,9 | 237 HV / 587,6 | 283 HV / 707,2 |
| 12% | 81 HV / 189,0 | 122 HV / 293,6 | 161 HV / 397,0 | 200 HV / 499,3 | 239 HV / 594,4 |
| 15% | 70 HV / 160,2 | 105 HV / 250,6 | 139 HV / 339,9 | 173 HV / 428,3 | 206 HV / 515,7 |
| 18% | 62 HV / 154,9 | 92 HV / 217,4 | 122 HV / 295,9 | 151 HV / 373,6 | 180 HV / 450,4 |
| 24% | 49 HV / 123,2 | 73 HV / 170,1 | 97 HV / 233,2 | 121 HV / 295,6 | 144 HV / 357,3 |

## 7. Khi nào mới thuê người

Quy tắc: chỉ thuê khi số liệu **tháng trước** chạm ngưỡng, và tổng lương không vượt 25% doanh thu tháng trước. Nhân viên chính thức tính thêm 21,5% chi phí bảo hiểm phía người sử dụng lao động. Lương là **giả định mặt bằng thị trường 2026**, chờ xác minh.

| Vị trí | Lương giả định (tr/tháng) | Ngưỡng thuê | Tháng thuê — Thận trọng | Cơ sở | Lạc quan |
|---|---:|---|---:|---:|---:|
| Trợ giảng/CSKH cộng đồng (bán thời gian) | 6,0 | ≥ 60 học viên trả phí (thay bằng bản toàn thời gian khi ≥ 200) | không | 11 | 5 |
| Trợ giảng/CSKH cộng đồng (toàn thời gian) | 10,0 | ≥ 200 học viên trả phí | không | không | 11 |
| Tư vấn/chốt đơn gói 1.000 USD (lương cứng + 5% hoa hồng) | 7,0 | Doanh thu ≥ 150 tr/tháng và ≥ 2.000 thành viên miễn phí | không | 12 | 6 |
| Dựng video/trợ lý nội dung | 9,0 | Doanh thu ≥ 200 tr/tháng (giải phóng thời gian anh) | không | 12 | 5 |
| CSKH cộng đồng thứ 2 | 10,0 | ≥ 500 học viên trả phí | không | không | 21 |
| Kế toán dịch vụ (thuê ngoài) | 2,5 | Doanh thu ≥ 40 tr/tháng | 13 | 4 | 3 |

"không" = trong 24 tháng chưa chạm ngưỡng, anh và đội AI tự làm. Không thuê trước doanh thu.

## 8. Gói "đồng hành 10 năm" thu một lần — rủi ro dòng tiền và cách xử lý

- **Nghĩa vụ dài hạn:** thu 1.000 USD một lần nhưng phải phục vụ 120 tháng. Doanh thu thực chất ≈ 8,3 USD/tháng/người. Nếu tiêu hết tiền thu ngay, các năm sau sẽ phục vụ không công; nếu dừng chương trình có thể phát sinh yêu cầu hoàn tiền phần chưa phục vụ.
- **Đề xuất ghi nhận:** ghi nhận ngay 20% (onboarding, tài liệu), phần 80% phân bổ đều 120 tháng. Kịch bản cơ sở: cuối tháng 24 còn **473,8 tr doanh thu chưa ghi nhận** (nghĩa vụ phải phục vụ).
- **Quỹ phục vụ dài hạn:** trích 30% tiền thực nhận (sau phí, thuế) mỗi lần bán gói 1.000 USD vào tài khoản riêng; cơ sở tháng 24 quỹ đạt **166,7 tr**. Lãi "tiêu được" = lãi tiền mặt − trích quỹ.
- **Điều khoản cần chốt (chờ anh + luật sư):** gói 1.000 USD có bao gồm khoá 100 USD không (mô hình giả định KHÔNG); "đồng hành" gồm gì cụ thể (số buổi live/năm, hỏi đáp), điều kiện chấm dứt/hoàn tiền, xử lý khi Skool đổi chính sách. Không cam kết lợi nhuận, không gọi kèo, không giữ tiền/ví hộ.
- **Thay thế an toàn hơn để anh cân nhắc:** gói 1.000 USD cho 12 tháng gia hạn được, hoặc trả góp — xem kịch bản phụ ở mục 5.

## 9. Nhận định

- Về chi phí, dự án gần như không thể lỗ nặng: vốn 63,0 tr, hoà vốn từ 1 học viên. Rủi ro thật là **doanh thu bằng 0** nếu không ai trả 100 USD/tháng.
- 100 USD/tháng (≈2,6 tr) là giá cao với người 25–40 tuổi ở VN; tỷ lệ huỷ quyết định quy mô: huỷ 6% vs 24% làm số học viên tháng 24 chênh 232 vs 97. Cần đo tỷ lệ huỷ thật ngay 2–3 tháng đầu.
- Số người theo dõi và tỷ lệ chuyển đổi là giả định — thay bằng số thật của kênh trong tháng 1 rồi chạy lại `mo_hinh.py`.
- Chưa xác minh: phí Skool, cách rút tiền Skool về VN, thuế cá nhân kinh doanh online. Đây là 3 điểm có thể làm lệch 5–15% doanh thu thực nhận.
- Không cần dựng bộ máy: theo quy tắc ngưỡng, người đầu tiên (CSKH bán thời gian) chỉ thuê khi có ~60 học viên trả phí.
