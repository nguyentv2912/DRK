# Mô hình tài chính — Đầu Tư Bình An trên Skool (phiên bản 2, 24 tháng)

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người lập: Hùng – Tài chính · Mọi con số do `mo_hinh.py` tính (chạy lại: `python3 mo_hinh.py`). Đơn vị: **triệu đồng (tr)**, tỷ giá giả định 26.000 đ/USD.

## 5 kết luận chính

1. **Vốn ban đầu rất thấp: 78,0 tr**, trong đó 32,0 tr là quỹ dự phòng (tiền vẫn nằm trong tài khoản). Chi phí cố định khi chưa thuê ai chỉ ~2,1 tr/tháng + phí Skool.
2. **Hoà vốn hằng tháng: 2 học viên trả 100 USD nếu chỉ có khoá cơ bản** (chưa thuê người; công của anh không tính vào chi phí). Mỗi học viên 100 USD/tháng (≈2,60 tr) để lại ≈2,28 tr sau phí Skool Pro, phí chuyển tiền, thuế (gói Hobby: 2,10 tr). Rủi ro không nằm ở chi phí mà ở **có kéo được người trả 100 USD/tháng và giữ họ hay không**.
3. **Mốc thu nhập (lãi sau thuế, phí, lương nhân viên) — kịch bản cơ sở:** 50 tr/tháng cần ~22 học viên, 100 tr cần ~42, 200 tr cần ~90 học viên 100 USD đang hoạt động (đã tính bán kèm gói 1.000 USD và ebook). Nếu không bán được gói chuyên sâu/ebook: 26 / 47 / 102 học viên.
4. **Kịch bản cơ sở là kịch bản tham vọng:** tháng 24 có ~114 học viên 100 USD, doanh thu 346,3 tr/tháng, lãi 269,9 tr/tháng; lãi luỹ kế 24 tháng (sau khi trừ vốn) 2.824,4 tr; hoàn vốn tháng 6. Thận trọng: ~10 học viên, lãi tháng 24 22,5 tr, hoàn vốn tháng 15. Lạc quan: ~627 học viên, lãi tháng 24 1.697,6 tr. **Không đáng làm** (ít người xem, chuyển đổi thấp, huỷ cao): chỉ ~1 học viên, lãi tháng 24 0,3 tr — không đủ trả công anh; ngưỡng dừng/đổi cách bán ở tháng 3 và 6 xem mục 5b. **Biến quyết định là tỷ lệ huỷ và tỷ lệ chuyển đổi**, không phải chi phí. Lưu ý: kịch bản cơ sở cần kênh đạt ~89.004 người theo dõi và ~2.786 thành viên Skool miễn phí vào tháng 24 — đây là giả định, chưa có số thật của kênh.
5. **Gói 1.000 USD "đồng hành 10 năm" mang tiền về sớm nhưng tạo nghĩa vụ dài hạn:** 1.000 USD/120 tháng ≈ 8,3 USD/tháng, rẻ hơn 12 lần gói cơ bản. Kịch bản cơ sở: cuối tháng 24 có 300,5 tr doanh thu "chưa phục vụ" (rủi ro hoàn tiền nếu dừng). Nếu gói này bao gồm luôn khoá cơ bản và học viên chuyển sang hàng loạt (8%/tháng), tiền mặt 24 tháng trông đẹp hơn (3.153,1 so với 2.824,4 tr) nhưng người trả 100 USD tháng 24 còn ~77 (thay vì 114), doanh thu chưa phục vụ lên 1.244,1 tr, và đến tháng 60 phải phục vụ ~1.177 người so với 756. Đề xuất: gói 1.000 USD là **gói bổ sung**, yêu cầu duy trì thuê bao 100 USD; ghi nhận doanh thu phân bổ và trích 30% tiền thu vào quỹ phục vụ dài hạn (chờ anh chốt).

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
| Thuế | 7,0% doanh thu | Giả định: hộ/cá nhân kinh doanh dịch vụ 5% GTGT + 2% TNCN, tính từ đồng đầu tiên (thận trọng). Skool là "merchant of record" tự xử lý VAT ở vùng áp dụng (nghien-cuu.md) → phần 5% GTGT có thể trùng; độ nhạy 2% vs 7% ở mục 6. nghien-cuu.md: ngưỡng không chịu thuế 500 tr/năm, báo chí nói NĐ 141/2026 nâng lên 1 tỷ — chưa đối chiếu; thuế khi bán qua nền tảng nước ngoài các nguồn mâu thuẫn. Hỏi cơ quan thuế |
| Công cụ AI, phần mềm | 1,6 tr/tháng | Giả định ~60 USD: 2 gói AI + Canva/CapCut Pro |
| Chi phí khác | 0,5 tr/tháng | Giả định: tên miền, email, họp online |
| Quảng cáo | 0,0 tr/tháng | Mặc định 0 — đầu phễu là video tự nhiên (brief) |
| Nhân công chủ dự án, đội AI, văn phòng | 0 | Brief: anh tự quay, đội AI có sẵn, hạ tầng có sẵn. Lãi trong mô hình = thu nhập của anh, chưa trừ công anh |
| Lịch ra mắt | Tháng 1 cộng đồng miễn phí; tháng 2 mở 100 USD; tháng 3 mở 1.000 USD và ebook | Giả định |
| Người theo dõi hiện có | 0 | Mặc định 0 — **chờ số thật**: kênh đang xây lại (KENH.md). Nhập số thật vào `nguoi_theo_doi_dau` rồi chạy lại |
| Người theo dõi mới | 2.000/tháng, tăng 5%/tháng | Giả định: 1 video ngắn/ngày, tăng dần nhờ đều đặn (ramp-up) |
| Theo dõi mới → Skool miễn phí | 5,0% | Giả định. Có rào cản: Skool không có giao diện tiếng Việt, phải tạo tài khoản, video ngắn khó gắn link (nghien-cuu.md). Thận trọng 2,5%, không đáng làm 2%; độ nhạy 2%/4%/8% ở mục 6 |
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
| Doanh thu khoá 100 USD | 658,6 | 2.493,8 |
| Doanh thu khoá 1.000 USD (tiền thu) | 78,5 | 322,7 |
| Doanh thu ebook | 31,0 | 90,7 |
| **Tổng doanh thu** | 768,1 | 2.907,1 |
| Thuế | 53,8 | 203,5 |
| Lương nhân viên thuê thêm | 17,5 | 205,6 |
| Tổng chi phí (gồm thuế, phí Skool, chuyển tiền) | 160,4 | 612,4 |
| **Lãi (tiền mặt)** | 607,7 | 2.294,7 |
| Trích quỹ phục vụ gói 10 năm | 20,1 | 84,4 |
| Biên lãi | 79,1% | 78,9% |
| Học viên 100 USD cuối năm | 44 | 114 |
| Học viên 1.000 USD luỹ kế | 3 | 15 |

### Theo tháng (kịch bản cơ sở)

| Tháng | Skool free | HV 100 USD | Mua 1.000 USD | Ebook | Doanh thu | Chi phí | Lãi | Luỹ kế (sau vốn) | Gói Skool | Nhân sự |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 100 | 0 | 0,0 | 0,0 | 0,0 | 2,3 | -2,3 | -80,4 | Hobby | — |
| 2 | 197 | 3 | 0,0 | 0,0 | 8,9 | 4,0 | 4,9 | -75,5 | Hobby | — |
| 3 | 293 | 7 | 0,1 | 1,6 | 21,1 | 6,2 | 14,9 | -60,5 | Hobby | — |
| 4 | 390 | 11 | 0,1 | 1,9 | 32,4 | 8,3 | 24,1 | -36,5 | Hobby | — |
| 5 | 487 | 14 | 0,2 | 2,2 | 44,0 | 9,9 | 34,1 | -2,4 | Pro | — |
| 6 | 585 | 18 | 0,2 | 2,6 | 55,9 | 13,8 | 42,0 | 39,6 | Pro | ke_toan |
| 7 | 684 | 22 | 0,3 | 2,9 | 68,2 | 15,3 | 52,8 | 92,5 | Pro | ke_toan |
| 8 | 785 | 27 | 0,3 | 3,2 | 80,8 | 16,9 | 63,9 | 156,4 | Pro | ke_toan |
| 9 | 886 | 31 | 0,4 | 3,6 | 93,8 | 18,4 | 75,4 | 231,8 | Pro | ke_toan |
| 10 | 990 | 35 | 0,4 | 4,0 | 107,1 | 20,0 | 87,1 | 318,9 | Pro | ke_toan |
| 11 | 1.096 | 40 | 0,5 | 4,3 | 120,9 | 21,7 | 99,2 | 418,1 | Pro | ke_toan |
| 12 | 1.204 | 44 | 0,6 | 4,7 | 135,1 | 23,4 | 111,6 | 529,7 | Pro | ke_toan |
| 13 | 1.314 | 49 | 0,6 | 5,1 | 149,6 | 25,2 | 124,4 | 654,2 | Pro | ke_toan |
| 14 | 1.428 | 54 | 0,7 | 5,5 | 164,7 | 27,0 | 137,7 | 791,8 | Pro | ke_toan |
| 15 | 1.544 | 59 | 0,8 | 5,9 | 180,2 | 28,9 | 151,3 | 943,1 | Pro | ke_toan |
| 16 | 1.664 | 65 | 0,8 | 6,3 | 196,2 | 30,8 | 165,4 | 1.108,4 | Pro | ke_toan |
| 17 | 1.788 | 70 | 0,9 | 6,8 | 212,7 | 38,8 | 173,9 | 1.282,3 | Pro | cskh_bt, ke_toan |
| 18 | 1.916 | 76 | 1,0 | 7,2 | 229,8 | 51,8 | 178,0 | 1.460,3 | Pro | cskh_bt, dung_video, ke_toan |
| 19 | 2.048 | 82 | 1,1 | 7,7 | 247,5 | 54,0 | 193,5 | 1.653,8 | Pro | cskh_bt, dung_video, ke_toan |
| 20 | 2.185 | 88 | 1,1 | 8,2 | 265,8 | 66,2 | 199,7 | 1.853,5 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 21 | 2.327 | 94 | 1,2 | 8,7 | 284,8 | 68,6 | 216,2 | 2.069,7 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 22 | 2.474 | 101 | 1,3 | 9,2 | 304,5 | 71,1 | 233,5 | 2.303,2 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 23 | 2.627 | 107 | 1,4 | 9,8 | 325,0 | 73,7 | 251,3 | 2.554,5 | Pro | cskh_bt, chot_don, dung_video, ke_toan |
| 24 | 2.786 | 114 | 1,5 | 10,3 | 346,3 | 76,4 | 269,9 | 2.824,4 | Pro | cskh_bt, chot_don, dung_video, ke_toan |

(Số học viên lẻ là trung bình kỳ vọng của mô hình, làm tròn khi hiển thị.)

## 4. Hoà vốn, hoàn vốn, NPV/IRR

| Chỉ tiêu | Không đáng làm | Thận trọng | Cơ sở (tham vọng) | Lạc quan |
|---|---:|---:|---:|---:|
| HV 100 USD cần để hoà vốn tháng | 2 | 2 | 1 | 1 |
| Tháng đầu tiên có lãi | 19 | 3 | 2 | 2 |
| Tháng hoàn vốn (luỹ kế ≥ 0) | chưa hoàn vốn | 15 | 6 | 3 |
| NPV 24 tháng @12%/năm (tr) | -92,9 | 137,7 | 2.394,5 | 13.969,4 |
| IRR (năm) | -93% | 137% | 2.978% | 62.356% |

IRR rất cao vì vốn ban đầu rất nhỏ — chỉ số này không có ý nghĩa so sánh; nên nhìn số học viên và lãi tháng.

Đóng góp mỗi học viên 100 USD/tháng: gói Pro 2,28 tr, gói Hobby 2,10 tr. Chuyển Skool Hobby → Pro khi doanh thu qua Skool vượt ~1.268 USD/tháng (≈13 học viên).

### Số học viên 100 USD cần cho các mốc thu nhập (trạng thái ổn định, đã trừ lương người thuê theo ngưỡng)

| Lãi mục tiêu/tháng | Không đáng làm | Thận trọng | Cơ sở (tham vọng) | Lạc quan | Cơ sở, chỉ có khoá cơ bản |
|---|---:|---:|---:|---:|---:|
| Hoà vốn | 2 | 2 | 1 | 1 | 2 |
| 50 tr | 24 | 24 | 22 | 22 | 26 |
| 100 tr | 45 | 44 | 42 | 40 | 47 |
| 200 tr | 97 | 95 | 90 | 87 | 102 |

Khác biệt giữa các kịch bản ở đây do tỷ lệ huỷ (ảnh hưởng số người mua ebook) và tỷ lệ nâng cấp 1.000 USD.

## 5. Bốn kịch bản (24 tháng)

Kịch bản cơ sở là **kịch bản tham vọng** (giả định kênh tăng đều 24 tháng, chưa có số thật). Kế hoạch nên bám thận trọng; "không đáng làm" dùng để đặt ngưỡng dừng ở mục 5b.

| Biến | Không đáng làm | Thận trọng | Cơ sở (tham vọng) | Lạc quan |
|---|---:|---:|---:|---:|
| Người theo dõi mới tháng 1 | 500 | 1.000 | 2.000 | 3.500 |
| Tốc độ tăng người theo dõi mới/tháng | 0,0% | 3,0% | 5,0% | 6,0% |
| Theo dõi mới → Skool miễn phí | 2,0% | 2,5% | 5,0% | 8,0% |
| Miễn phí mới → 100 USD (tháng đầu) | 1,0% | 2,0% | 3,0% | 4,5% |
| Kho miễn phí → 100 USD (mỗi tháng) | 0,1% | 0,2% | 0,3% | 0,4% |
| Tỷ lệ huỷ/tháng | 20,0% | 15,0% | 9,0% | 6,0% |
| Nâng cấp 1.000 USD/tháng | 0,5% | 0,8% | 1,5% | 2,5% |
| Mua kèm ebook (HV 100 USD mới) | 10,0% | 15,0% | 25,0% | 35,0% |
| Người theo dõi tháng 24 | 12.000 | 34.426 | 89.004 | 177.855 |
| Thành viên Skool miễn phí tháng 24 | 139 | 525 | 2.786 | 8.894 |
| **HV 100 USD tháng 24** | 1 | 10 | 114 | 627 |
| **Doanh thu tháng 24 (tr)** | 3,2 | 30,5 | 346,3 | 2.008,8 |
| **Lãi tháng 24 (tr)** | 0,3 | 22,5 | 269,9 | 1.697,6 |
| Doanh thu năm 1 / năm 2 (tr) | 15,4 / 33,8 | 97,0 / 283,1 | 768,1 / 2.907,1 | 3.758,1 / 16.076,8 |
| Lãi năm 1 / năm 2 (tr) | -15,3 / -0,3 | 51,1 / 202,6 | 607,7 / 2.294,7 | 3.056,8 / 13.504,5 |
| **Lãi luỹ kế 24 tháng sau vốn (tr)** | -93,6 | 175,7 | 2.824,4 | 16.483,3 |

### Kịch bản phụ gói 1.000 USD (trên nền cơ sở)

| Phương án | HV 100 USD tháng 24 | Lãi tháng 24 (tr) | Lãi luỹ kế 24 tháng (tr) | Doanh thu chưa ghi nhận T24 (tr) | HV 100 USD tháng 60 | Người phải phục vụ T60 | Lãi tháng 60 (tr) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cơ sở: trả 1 lần, gói bổ sung | 114 | 269,9 | 2.824,4 | 300,5 | 756 | 756 | 1.944,4 |
| Trả góp 4 kỳ × 250 USD (10% bỏ ngang sau kỳ 1) | 114 | 265,2 | 2.759,1 | — | 756 | 756 | 1.917,6 |
| Gói 1.000 USD GỒM luôn khoá cơ bản (người nâng cấp ngừng trả 100 USD) | 105 | 248,9 | 2.645,0 | 300,5 | 683 | 866 | 1.778,2 |
| Gói GỒM khoá cơ bản và học viên chuyển sang hàng loạt (nâng cấp 8%/tháng) | 77 | 279,0 | 3.153,1 | 1.244,1 | 482 | 1.177 | 1.915,9 |

Cột tháng 60 chạy cùng giả định phễu đến năm thứ 5 (người theo dõi tiếp tục tăng) — chỉ để so sánh cấu trúc gói, không phải dự báo. "Người phải phục vụ" với phương án GỒM = HV 100 USD + toàn bộ người đã mua gói 10 năm (giả định họ ở lại, mức trần).

Giá trị trọn đời 1 học viên 100 USD mới (USD): gói bổ sung 1.254 (ở lại TB 11,1 tháng); gói GỒM, nâng cấp 1,5%/tháng 1.095; gói GỒM, nâng cấp 8%/tháng 1.059 — chênh lệch nhỏ về tiền, khác biệt nằm ở **số người phải phục vụ không thu phí hằng tháng trong 10 năm**.

### 5b. Ngưỡng dừng / đổi cách bán (đo bằng số thật)

Ngưỡng lấy theo mức của kịch bản **thận trọng** tại cùng thời điểm: thấp hơn thận trọng nghĩa là đang đi theo hướng "không đáng làm".

| Chỉ số | Tháng | Không đáng làm | Thận trọng | Cơ sở (tham vọng) | Lạc quan |
|---|---:|---:|---:|---:|---:|
| Thành viên Skool miễn phí | 3 | 28 | 72 | 293 | 819 |
| HV 100 USD đang trả | 3 | 0,2 | 1,1 | 7,0 | 29,8 |
| Lãi tháng (tr) | 3 | -1,8 | 0,3 | 14,9 | 78,5 |
| Thành viên Skool miễn phí | 6 | 52 | 140 | 585 | 1.656 |
| HV 100 USD đang trả | 6 | 0,4 | 2,6 | 18,4 | 81,7 |
| Lãi tháng (tr) | 6 | -1,3 | 3,9 | 42,0 | 208,0 |

- **Mốc tháng 3 — đổi cách bán** nếu Skool miễn phí < 70 người **hoặc** < 1 học viên trả 100 USD: thêm thu VND (chuyển khoản/QR rồi mời vào Skool), hướng dẫn vào Skool bằng tiếng Việt, buổi live miễn phí để chốt, cân nhắc gói năm. Giá anh chốt giữ nguyên trừ khi anh quyết khác.
- **Mốc tháng 6 — dừng mở rộng / xem lại mô hình** nếu < 3 học viên trả phí, **hoặc** tỷ lệ huỷ thực > 15%/tháng, **hoặc** lãi < 10 tr/tháng: không thuê người, không chi quảng cáo; trình anh phương án đổi giá/định dạng (gói năm, khoá trả một lần) trước khi làm tiếp.
- Ở mức "không đáng làm", tiền không mất nhiều (vốn nhỏ) nhưng **thời gian của anh** là chi phí chính bị mất.

## 6. Độ nhạy ±20% (kịch bản cơ sở)

Gốc: lãi tháng 24 = 269,9 tr; lãi luỹ kế 24 tháng = 2.824,4 tr.

| Biến | Giá trị gốc | Lãi T24 khi −20% | Lãi T24 khi +20% | Luỹ kế 24T khi −20% | Luỹ kế 24T khi +20% |
|---|---:|---:|---:|---:|---:|
| Người theo dõi mới/tháng | 2.000 | 209,4 | 330,4 | 2.267,2 | 3.414,3 |
| Tỷ lệ vào Skool miễn phí | 5,0% | 209,4 | 330,4 | 2.267,2 | 3.414,3 |
| Chuyển đổi miễn phí mới → 100 USD | 3,0% | 236,1 | 303,7 | 2.445,6 | 3.188,9 |
| Tỷ lệ huỷ/tháng | 9,0% | 302,9 | 242,2 | 3.081,0 | 2.603,7 |
| Chuyển đổi kho miễn phí → 100 USD | 0,3% | 245,4 | 294,2 | 2.611,0 | 3.030,7 |
| Tỷ lệ nâng cấp 1.000 USD | 1,5% | 263,9 | 275,7 | 2.758,7 | 2.877,6 |

Tỷ giá ±5%: lãi luỹ kế 24 tháng 2.672,0 tr (−5%) / 2.965,9 tr (+5%).

Nếu được áp ngưỡng không chịu thuế 1 tỷ đ/năm (chỉ tính thuế phần vượt — cách tính giả định, chờ cơ quan thuế): lãi luỹ kế 24 tháng Không đáng làm -90,2 tr (+3,4) / Thận trọng 202,3 tr (+26,6) / Cơ sở (tham vọng) 2.948,2 tr (+123,8) / Lạc quan 16.623,3 tr (+140,0).

**Tỷ lệ theo dõi mới → Skool miễn phí (nền cơ sở):**

| Tỷ lệ vào Skool | HV 100 USD tháng 24 | Lãi tháng 24 (tr) | Lãi luỹ kế 24 tháng (tr) |
|---:|---:|---:|---:|
| 2% | 46 | 114,6 | 1.078,8 |
| 4% | 91 | 209,4 | 2.267,2 |
| 8% | 183 | 451,4 | 4.607,6 |

**Thuế 2% (chỉ TNCN, nếu VAT đã do Skool thu) vs 7%** — lãi luỹ kế 24 tháng (tr):

| Thuế | Không đáng làm | Thận trọng | Cơ sở (tham vọng) | Lạc quan |
|---|---:|---:|---:|---:|
| 7% (mặc định) | -93,6 | 175,7 | 2.824,4 | 16.483,3 |
| 2% | -91,1 | 194,7 | 3.008,2 | 17.475,0 |

Cả hai cách chưa được cơ quan thuế xác nhận; mô hình giữ 7% cho thận trọng.

### Lưới tỷ lệ huỷ × chuyển đổi — học viên 100 USD và lãi tháng 24 (tr)

Hệ số chuyển đổi nhân cả hai tỷ lệ chuyển đổi miễn phí → 100 USD của kịch bản cơ sở.

| Huỷ/tháng \ Chuyển đổi | ×0,50 (1,5%) | ×0,75 (2,2%) | ×1,00 (3,0%) | ×1,25 (3,8%) | ×1,50 (4,5%) |
|---|---:|---:|---:|---:|---:|
| 4% | 79 HV / 177,8 | 119 HV / 278,8 | 157 HV / 378,9 | 196 HV / 478,1 | 234 HV / 570,2 |
| 6% | 69 HV / 163,3 | 104 HV / 240,8 | 137 HV / 328,5 | 171 HV / 415,2 | 204 HV / 501,2 |
| 9% | 58 HV / 139,8 | 86 HV / 196,7 | 114 HV / 269,9 | 142 HV / 342,3 | 170 HV / 414,0 |
| 12% | 49 HV / 127,1 | 73 HV / 163,8 | 97 HV / 226,2 | 121 HV / 287,9 | 144 HV / 349,0 |
| 15% | 43 HV / 110,2 | 63 HV / 155,6 | 84 HV / 192,8 | 105 HV / 246,4 | 125 HV / 299,4 |
| 20% | 35 HV / 89,7 | 52 HV / 125,3 | 68 HV / 152,6 | 85 HV / 196,3 | 101 HV / 239,6 |

## 7. Khi nào mới thuê người

Quy tắc: chỉ thuê khi số liệu **tháng trước** chạm ngưỡng, và tổng lương không vượt 25% doanh thu tháng trước. Nhân viên chính thức tính thêm 21,5% chi phí bảo hiểm phía người sử dụng lao động. Lương là **giả định mặt bằng thị trường 2026**, chờ xác minh.

| Vị trí | Lương giả định (tr/tháng) | Ngưỡng thuê | Tháng thuê — Không đáng làm | Thận trọng | Cơ sở (tham vọng) | Lạc quan |
|---|---:|---|---:|---:|---:|---:|
| Trợ giảng/CSKH cộng đồng (bán thời gian) | 6,0 | ≥ 60 học viên trả phí (thay bằng bản toàn thời gian khi ≥ 200) | không | không | 17 | 6 |
| Trợ giảng/CSKH cộng đồng (toàn thời gian) | 10,0 | ≥ 200 học viên trả phí | không | không | không | 13 |
| Tư vấn/chốt đơn gói 1.000 USD (lương cứng + 5% hoa hồng) | 7,0 | Doanh thu ≥ 150 tr/tháng và ≥ 2.000 thành viên miễn phí | không | không | 20 | 9 |
| Dựng video/trợ lý nội dung | 9,0 | Doanh thu ≥ 200 tr/tháng (giải phóng thời gian anh) | không | không | 18 | 6 |
| CSKH cộng đồng thứ 2 | 10,0 | ≥ 500 học viên trả phí | không | không | không | 23 |
| Kế toán dịch vụ (thuê ngoài) | 2,5 | Doanh thu ≥ 40 tr/tháng | không | không | 6 | 4 |

"không" = trong 24 tháng chưa chạm ngưỡng, anh và đội AI tự làm. Không thuê trước doanh thu.

## 8. Gói "đồng hành 10 năm" thu một lần — rủi ro dòng tiền và cách xử lý

- **Nghĩa vụ dài hạn:** thu 1.000 USD một lần nhưng phải phục vụ 120 tháng. Doanh thu thực chất ≈ 8,3 USD/tháng/người. Nếu tiêu hết tiền thu ngay, các năm sau sẽ phục vụ không công; nếu dừng chương trình có thể phát sinh yêu cầu hoàn tiền phần chưa phục vụ.
- **Đề xuất ghi nhận:** ghi nhận ngay 20% (onboarding, tài liệu), phần 80% phân bổ đều 120 tháng. Kịch bản cơ sở: cuối tháng 24 còn **300,5 tr doanh thu chưa ghi nhận** (nghĩa vụ phải phục vụ).
- **Quỹ phục vụ dài hạn:** trích 30% tiền thực nhận (sau phí, thuế) mỗi lần bán gói 1.000 USD vào tài khoản riêng; cơ sở tháng 24 quỹ đạt **104,4 tr**. Lãi "tiêu được" = lãi tiền mặt − trích quỹ.
- **Điều khoản cần chốt (chờ anh + luật sư):** gói 1.000 USD có bao gồm khoá 100 USD không (mô hình giả định KHÔNG); "đồng hành" gồm gì cụ thể (số buổi live/năm, hỏi đáp), điều kiện chấm dứt/hoàn tiền, xử lý khi Skool đổi chính sách. Không cam kết lợi nhuận, không gọi kèo, không giữ tiền/ví hộ.
- **Thay thế an toàn hơn để anh cân nhắc:** gói 1.000 USD cho 12 tháng gia hạn được, hoặc trả góp — xem kịch bản phụ ở mục 5.

## 9. Nhận định

- Về chi phí, dự án gần như không thể lỗ nặng: vốn 78,0 tr, hoà vốn từ 1 học viên. Rủi ro thật là **doanh thu bằng 0** nếu không ai trả 100 USD/tháng.
- 100 USD/tháng (≈2,6 tr) là giá cao với người 25–40 tuổi ở VN; tỷ lệ huỷ quyết định quy mô: huỷ 4% vs 20% làm số học viên tháng 24 chênh 157 vs 68. Cần đo tỷ lệ huỷ thật ngay 2–3 tháng đầu.
- Số người theo dõi và tỷ lệ chuyển đổi là giả định — thay bằng số thật của kênh trong tháng 1 rồi chạy lại `mo_hinh.py`.
- Chưa xác minh (nghien-cuu.md mới ở mức tin cậy Trung bình/Thấp): phí Skool, payout Stripe Express về VN (phải thử 1 giao dịch thật), thuế khi bán qua nền tảng nước ngoài, chi phí liên kết xuất bản ebook. Khách trả USD còn chịu thêm ~1–4% phí đổi ngoại tệ phía thẻ — làm giá thực tế với khách cao hơn 100 USD, có thể kéo chuyển đổi xuống.
- Không cần dựng bộ máy: theo quy tắc ngưỡng, người đầu tiên (CSKH bán thời gian) chỉ thuê khi có ~60 học viên trả phí.
