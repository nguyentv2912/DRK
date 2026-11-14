# Tài chính — Chương trình chuyển đổi khách hàng và Phòng ban vận hành

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người lập: Hùng (Tài chính) · Ngày 14/11/2026
Đơn vị: **triệu đồng (trđ)** nếu không ghi khác. Script: `mo_hinh.py` (chạy `python3 mo_hinh.py`, mọi số dưới đây lấy từ lần chạy này). Số liệu cho biểu đồ nằm trong `tai-chinh.json`.

> **Độ tin cậy dữ liệu.** Lan không mở được trang gốc nào vì mạng bị chặn. Mọi số lấy từ `nghien-cuu.md` (NC) vì thế có độ tin cậy **tối đa là Trung bình**. Tỷ lệ chuyển đổi của phễu, giá gói đồng hành và gói thành viên đều là **giả định** (GĐ) của Hùng, chưa có dữ liệu thực nào kiểm chứng. Lương coach và quản lý vận hành chỉ có số tham chiếu gần từ nghiên cứu vòng 2, không phải số cho đúng chức danh. Mô hình này dùng để ra quyết định có nên đi tiếp hay không và đặt chỉ tiêu. Nó không phải dự báo.

---

## 1. Nhận định (đọc trước)

1. **Kịch bản cơ sở chưa đạt.** Muốn chạy kịch bản này cần chuẩn bị **khoảng 2,9 tỷ đ**. Chương trình **hoà vốn vận hành từ tháng 19** nhưng **phải tới tháng 44 mới hoàn vốn**. Đến tháng 24 dòng tiền luỹ kế vẫn **âm 1,81 tỷ**. NPV 48 tháng âm 233 trđ, IRR khoảng 9%/năm, tức là thấp hơn suất chiết khấu 15%. Với các giả định hiện tại, đội 24 người là quá lớn so với lượng khách mà phễu tạo ra.
2. **Kết quả phụ thuộc gần như hoàn toàn vào tỷ lệ chuyển đổi và giá mỗi lead.** Muốn hoàn vốn trong 24 tháng thì chỉ cần **một** trong ba điều sau: tỷ lệ chuyển đổi toàn phễu cao hơn giả định **17%**, hoặc CPL thấp hơn **28%**, hoặc giá gói đồng hành cao hơn **31%**. Ngược lại, nếu chuyển đổi thấp hơn 30% (kịch bản Thận trọng) thì chương trình **không bao giờ tự hoà vốn**.
3. **Doanh thu từ ngân hàng quá nhỏ để trông vào.** Hoa hồng giới thiệu chỉ khoảng 9–27 trđ/năm, chưa tới 0,5% doanh thu. Giá trị thật của ngân hàng là **uy tín và tài trợ sự kiện**, mà khoản này hiện chưa có văn bản nên kịch bản cơ sở để bằng 0.
4. **Đề xuất: mở rộng đội theo chỉ tiêu, không theo lịch.** Chỉ chuyển giai đoạn khi phễu thật đã đạt ngưỡng hoà vốn của giai đoạn kế tiếp (mục 6). Mốc dừng nên đặt ở tháng 6: nếu khi đó dưới **8 khách đồng hành/tháng** thì không tuyển thêm. Dừng ở mốc này thì tổng lỗ khoảng **1,0 tỷ** (cơ sở) đến **1,3 tỷ** (thận trọng). Nếu không đặt mốc dừng mà cứ để chạy hết 24 tháng thì lỗ có thể lên tới 7 tỷ.
5. **Chi phí chưa đưa vào mô hình:** lương của chủ dự án (đang để 0 vì anh vừa là chuyên gia chính vừa là gương mặt chương trình), kinh phí công đoàn 2%, và VAT nếu khoá học không được miễn. Ba khoản này đều làm kết quả xấu hơn.

---

## 2. Thang sản phẩm và giá

| Tầng | Gói | Giá (đ) | Căn cứ |
|---|---|---|---|
| 0. Miễn phí | Nội dung mạng xã hội + hội thảo miễn phí 2 giờ (online và tại văn phòng) + tư vấn 1:1 miễn phí 30 phút | 0 | NC: chương trình của nhà nước và ngân hàng đều miễn phí (VIFC-HCM, BIDV, Sacombank). Không thể thu phí ở tầng này |
| 1. Nhập môn | Khoá nền tảng "Quản lý tài chính cá nhân & đầu tư tài sản số an toàn" (video + 2 buổi live) | **990.000** | NC: khoá video tài chính cá nhân bán 899.000 (niêm yết 1,2 tr); mặt bằng "vài trăm nghìn đến vài triệu" (TB/Thấp) |
| 2. Cốt lõi | Chương trình đồng hành 3 tháng: lớp nhóm 8–10 người, mỗi tháng 1 buổi 1:1, lập kế hoạch tài chính cá nhân, quản trị rủi ro, pháp lý tài sản số | **12.000.000** | GĐ. Thị trường không công bố giá (coaching kiểu "liên hệ"). Có chính sách hoàn tiền (mô hình trừ 5% doanh thu) |
| 3. Gắn bó | Thành viên năm: cộng đồng, cập nhật pháp lý, hội thảo chuyên đề hằng tháng | **3.600.000/năm** | GĐ. NC: nhóm VIP quốc tế 30–200 USD/tháng (Thấp). Gói này không có tín hiệu mua bán |
| Phụ | Giới thiệu sản phẩm ngân hàng (mở tài khoản, chứng chỉ quỹ) theo hợp đồng đối tác | hoa hồng | NC: VPBank NEO khoảng 64–72 nghìn đ/tài khoản; TCBS iWealth Partner 0,4% giá trị chứng chỉ quỹ |

**Giới hạn pháp lý của doanh thu ngân hàng** (theo NC, cần luật sư xác nhận):
- Chương trình chỉ được **giới thiệu**. Không được tư vấn đầu tư chứng khoán hay chứng chỉ quỹ, vì đó là nghiệp vụ phải có giấy phép. Đại lý phân phối chứng chỉ quỹ phải là tổ chức.
- iWealth Partner là chương trình **dành cho cá nhân** được TCBS duyệt. Muốn doanh nghiệp nhận hoa hồng thì phải ký hợp đồng riêng với ngân hàng hoặc công ty chứng khoán.
- Không tư vấn bảo hiểm nếu không có chứng chỉ đại lý. Không giới thiệu sàn crypto chưa được cấp phép (NĐ 284/2026 phạt tới 200 trđ).
- Phải công khai cho học viên mọi khoản hoa hồng nhận từ đối tác.

---

## 3. Bảng giả định

| Nhóm | Giả định | Giá trị | Đơn vị | Nguồn | Độ tin cậy |
|---|---|---|---|---|---|
| Giá | Khoá nền tảng | 0,99 | trđ | NC (Finhay/Unica 899k) | TB |
| Giá | Đồng hành 3 tháng | 12,0 | trđ | giả định | — |
| Giá | Thành viên năm | 3,6 | trđ/năm | giả định (NC tham chiếu VIP 30–200 USD/tháng) | Thấp |
| Giá | Tỷ lệ gia hạn thành viên | 50% | sau 12 tháng | giả định | — |
| Phễu | Người tiếp cận → đăng ký (lead) | 2% | | giả định (chỉ dùng để ước quy mô tiếp cận) | — |
| Phễu | Đăng ký → tham dự hội thảo | 40% | | giả định | — |
| Phễu | Tham dự → mua khoá nền tảng | 12% | | giả định | — |
| Phễu | Tham dự → đặt tư vấn 1:1 | 8% | | giả định | — |
| Phễu | Tư vấn 1:1 → mua đồng hành (cùng tháng) | 25% | | giả định | — |
| Phễu | Học viên nền tảng → đồng hành (trễ 1 tháng) | 20% | | giả định | — |
| Phễu | Học xong đồng hành → thành viên (trễ 3 tháng) | 40% | | giả định | — |
| Phễu | Học viên nền tảng → thành viên | 5% | | giả định | — |
| Phễu | Ramp-up niềm tin (hệ số trên tỷ lệ mua) | T1: 0 · T2: 0,6 · T3: 0,7 · T4: 0,8 · T5: 0,85 · T6: 0,9 · T7 trở đi: 1,0 | | giả định | — |
| Phễu | Tỷ lệ hoàn tiền gói đồng hành | 5% | doanh thu | giả định | — |
| Lead | CPL (quảng cáo giáo dục tài chính, **không quảng cáo crypto**) | 60.000 | đ/lead | giả định (NC 2.7: Meta/TikTok hạn chế quảng cáo crypto) | — |
| Lead | Ngân sách quảng cáo | T1: 10 · Khởi động: 30 · Tăng trưởng: 60 · Mở rộng: 100 | trđ/tháng | giả định | — |
| Lead | Tháng 1 là tháng chuẩn bị | 10 trđ quảng cáo ở T1 là **chi phí thử nghiệm** (thử mẫu quảng cáo, đo CPL). Khoảng 167 lead thu được ở T1 không tạo khách và không được chuyển sang T2 | | giả định (thận trọng) | — |
| Lead | Lead tự nhiên (organic, giới thiệu) | 50 ở T2, tăng tuyến tính lên 900 ở T24, sau đó giữ nguyên | lead/tháng | giả định | — |
| Ngân hàng | Khách đồng hành mở tài khoản qua link | 30% × 0,068 trđ | | NC (VPBank NEO/Ecomobi) + tỷ lệ giả định | TB |
| Ngân hàng | Khách đồng hành mua chứng chỉ quỹ | 15% × 50 trđ × 0,4% | | NC (TCBS 0,4%) + tỷ lệ và giá trị giả định | TB |
| Ngân hàng | Tài trợ sự kiện | Cơ sở 0; Lạc quan 10 | trđ/tháng | giả định (chưa có văn bản) | — |
| Biến đổi | Phí thanh toán | 2% | doanh thu | giả định | — |
| Biến đổi | Học liệu, phục vụ | Đồng hành 0,3 · Nền tảng 0,05 | trđ/khách | giả định | — |
| Biến đổi | Hoa hồng tư vấn viên | 8% doanh thu đồng hành; 5% doanh thu nền tảng + thành viên | | giả định (NC: thị trường trả lương cứng + hoa hồng) | — |
| Biến đổi | Hoa hồng trưởng nhóm | 1,5% tổng doanh thu bán | | giả định | — |
| Biến đổi | Chi phí một buổi hội thảo offline | 4 | trđ/buổi | giả định. Số buổi/tháng: 4 / 8 / 12 theo giai đoạn | — |
| Cố định | Mặt bằng | **0** | | brief (văn phòng có sẵn) | — |
| Cố định | Điện nước phân bổ tăng thêm | 3 / 5 / 8 | trđ/tháng | giả định | — |
| Cố định | Phần mềm (CRM, LMS, Zoom, thiết kế) | 8 / 12 / 18 | trđ/tháng | giả định | — |
| Cố định | Pháp lý định kỳ | 5 / 5 / 6 | trđ/tháng | giả định | — |
| Cố định | Khác | 2 / 3 / 4 | trđ/tháng | giả định | — |
| Nhân sự | BH bắt buộc phía doanh nghiệp | **21,5%** lương cứng (BHXH 17,5 + BHYT 3 + BHTN 1) | | **giả định, cần kế toán xác nhận**. Mô hình coi lương đóng BH bằng lương cứng, hoa hồng không đóng BH, và chưa tính kinh phí công đoàn 2% | — |
| Nhân sự | Tuyển dụng + đào tạo người mới | 8 | trđ/người | giả định | — |
| Nhân sự | Tỷ lệ nghỉ việc (tuyển thay thế) | 30% | /năm | giả định | — |
| Nhân sự | Công suất 1 coach + 1 trợ giảng | 40 | học viên đồng hành đang học | giả định. Vượt mức này mô hình tự thêm một cặp coach + trợ giảng | — |
| Nhân sự | Lương chủ dự án | 0 | | giả định (**rủi ro: chi phí ẩn**) | — |
| Tài chính | Thuế TNDN | 20%, được chuyển lỗ | | giả định | — |
| Tài chính | Suất chiết khấu | 15% | /năm | giả định | — |
| Tài chính | Tầm mô hình | 48 tháng, không tính giá trị cuối kỳ | | giả định | — |

### Lương theo vị trí (lương cứng, trđ/tháng, TP lớn 2026)

| Vị trí | Bộ phận | Lương cứng | Nguồn | Độ tin cậy |
|---|---|---|---|---|
| Quản lý vận hành | Quản lý | 25 | NC vòng 2: trưởng phòng vận hành 13–30, mốc khoảng 21,7 (TB); tin trưởng phòng vận hành logistics HCM 40 (Thấp). Mức 25 nằm trong khoảng | TB |
| Kế toán – hành chính | Quản lý | 10 | giả định | — |
| Coach tài chính | Thực thi | 20 | NC vòng 2: giảng viên HCM trung bình 21,9 (15–30) (TB); huấn luyện viên HCM trung bình 19,0 (10–30) (Thấp). Chưa có số cho đúng chức danh coach tài chính | TB |
| Trợ giảng | Thực thi | 11 | NC: HCM trung bình 10,9; HN 13,4 | TB |
| Trưởng nhóm bán hàng | Bán hàng | 20 + 1,5% doanh thu | NC: trưởng phòng KD B2C 20–40 | Thấp |
| Tư vấn viên | Bán hàng | 9 + hoa hồng | NC: SVFC 7–20, AIA lương hỗ trợ 8–24, Chubb 12–30 (các mức này đã gồm hoa hồng). Lương cứng 9 nằm ở cận dưới | TB |
| Chăm sóc khách hàng | CSKH | 9 | NC: HCM 8–10 | Thấp–TB |
| Content creator | Nội dung | 13 | NC: 12–15 | Thấp |
| Video editor | Nội dung | 12 | NC: HCM trung bình khoảng 12 | TB |
| Chuyên viên quảng cáo | Nội dung | 15 | giả định | — |

Kiểm tra lại: thu nhập bình quân của tư vấn viên trong mô hình (lương cứng + hoa hồng) là **14,9 trđ ở T6, 16,1 ở T12 và 17,7 ở T24**. Mức này nằm trong khoảng 12–30 trđ của các tin tuyển dụng, nên hợp lý.

---

## 4. Vốn cần chuẩn bị (kịch bản cơ sở)

| Hạng mục | trđ |
|---|---|
| Thiết bị quay dựng (máy quay, mic, đèn, phông) | 80 |
| Thiết bị cho đội khởi động (8 người × 12) | 96 |
| Pháp lý khởi tạo (ngành nghề, hợp đồng mẫu, rà soát tuân thủ) | 30 |
| Nhận diện, website, LMS, phễu đăng ký | 40 |
| Sản xuất bài giảng khoá nền tảng | 30 |
| Cải tạo nhỏ không gian hội thảo trong văn phòng có sẵn | 20 |
| **Cộng vốn đầu tư ban đầu** | **296** |
| Vốn lưu động: lỗ vận hành phải bù tới đáy dòng tiền (T18), gồm cả thiết bị cho người tuyển thêm | 1.772 |
| Quỹ dự phòng (2 tháng chi phí cố định của đội Mở rộng) | 835 |
| **TỔNG VỐN CẦN CHUẨN BỊ** | **2.903** |

Đáy dòng tiền luỹ kế là **−2.068 trđ ở tháng 18**.

---

## 5. Kế hoạch phòng ban: nhân sự theo giai đoạn

| Bộ phận | Vị trí | Khởi động (T1–T6) | Tăng trưởng (T7–T15) | Mở rộng (T16 trở đi) |
|---|---|---|---|---|
| Quản lý | Quản lý vận hành | 1 | 1 | 1 |
| Quản lý | Kế toán – hành chính | – | 1 | 1 |
| Thực thi | Coach tài chính | 1 | 2 | 4 |
| Thực thi | Trợ giảng | 1 | 2 | 3 |
| Bán hàng | Trưởng nhóm bán hàng | – | 1 | 1 |
| Bán hàng | Tư vấn viên | 2 | 4 | 6 |
| CSKH | Chăm sóc khách hàng | 1 | 2 | 3 |
| Nội dung | Content creator | 1 | 2 | 2 |
| Nội dung | Video editor | 1 | 1 | 2 |
| Nội dung | Chuyên viên quảng cáo | – | 1 | 1 |
| | **Tổng người** | **8** | **17** | **24** |
| | Lương cứng + BH doanh nghiệp (trđ/tháng) | 131,2 | 272,2 | 381,5 |
| | Chi phí cố định cả phòng ban\* (trđ/tháng) | 166,8 | 332,6 | 470,3 |

\* Gồm lương + BH, chi phí cố định khác, tuyển dụng thay thế và hội thảo offline. **Không** gồm quảng cáo và hoa hồng, vì hai khoản này tính theo từng khách.

Chủ dự án là chuyên gia chính và gương mặt của chương trình, không nằm trong bảng lương. Ở kịch bản Lạc quan, công suất coach bị vượt nên mô hình tự thêm 2 cặp coach + trợ giảng, đội lên **28 người**.

### Hoà vốn phòng ban: số khách cần để nuôi đội

Kinh tế đơn vị ở trạng thái ổn định, tính trên 1.000 lead (cơ sở):

| | Giá trị |
|---|---|
| Người tham dự | 400 |
| Khách mua nền tảng | 48 |
| Khách mua đồng hành | 17,6 |
| Thành viên năm | 9,4 |
| Doanh thu (sau hoàn tiền) | 283 trđ |
| Chi phí biến đổi (phí thanh toán, học liệu, hoa hồng; hoàn tiền đã trừ vào doanh thu) | 38 trđ |
| Quảng cáo (nếu toàn bộ lead đều mua) | 60 trđ |
| Đóng góp | 185 trđ |
| Doanh thu đi kèm mỗi khách đồng hành | 16,1 trđ |
| Đóng góp mỗi khách đồng hành | 10,5 trđ |
| CAC quảng cáo mỗi khách đồng hành | 3,4 trđ |

Hoà vốn theo giai đoạn:

| Giai đoạn | Số người | Chi phí cố định/tháng | **Khách đồng hành mới cần/tháng** | Khách nền tảng đi kèm | Lead cần/tháng | **Doanh số cần/tháng** | Mô hình cơ sở đạt (cuối giai đoạn) |
|---|---|---|---|---|---|---|---|
| Khởi động | 8 | 166,8 | **15,8** | 43 | 900 | **255** | 10,5 khách (T6): chưa đủ |
| Tăng trưởng | 17 | 332,6 | **31,6** | 86 | 1.794 | **508** | 26,9 khách (T15): chưa đủ |
| Mở rộng | 24 | 470,3 | **44,7** | 122 | 2.537 | **718** | 44,8 khách (T24): vừa đủ |

Bảng này tính như thể mọi lead đều phải mua bằng quảng cáo. Thực tế có thêm lead tự nhiên, nên EBITDA chuyển dương sớm hơn một chút, ở tháng 19.

---

## 6. Kết quả theo năm (kịch bản cơ sở)

Bảng này do script in ra, ở mục "BẢNG THEO NĂM CHI TIẾT".

| trđ | Năm 1 | Năm 2 | Năm 3 | Năm 4 |
|---|---|---|---|---|
| Lead | 11.342 | 26.250 | 30.800 | 30.800 |
| Người tiếp cận (ước) | 567.083 | 1.312.500 | 1.540.000 | 1.540.000 |
| Khách nền tảng / đồng hành / thành viên | 503 / 171 / 64 | 1.260 / 451 / 252 | 1.478 / 542 / 415 | 1.478 / 542 / 498 |
| Doanh thu nền tảng | 498 | 1.247 | 1.464 | 1.464 |
| Doanh thu đồng hành (sau hoàn tiền) | 1.946 | 5.143 | 6.180 | 6.180 |
| Doanh thu thành viên | 232 | 906 | 1.495 | 1.794 |
| Doanh thu ngân hàng | 9 | 23 | 27 | 27 |
| **Tổng doanh thu** | **2.684** | **7.320** | **9.166** | **9.465** |
| Quảng cáo | 520 | 1.080 | 1.200 | 1.200 |
| Hội thảo offline | 272 | 528 | 576 | 576 |
| Chi phí biến đổi (gồm hoa hồng) | 354 | 973 | 1.199 | 1.224 |
| Lương cứng + BH | 2.420 | 4.250 | 4.578 | 4.578 |
| Chi phí cố định khác | 258 | 399 | 432 | 432 |
| Tuyển dụng | 166 | 109 | 58 | 58 |
| **EBITDA** | **−1.305 (−49%)** | **−20 (−0%)** | **1.124 (12%)** | **1.397 (15%)** |
| Thuế TNDN | 0 | 0 | 0 | 239 |
| Thiết bị (capex) | 108 | 84 | 0 | 0 |
| Dòng tiền | −1.413 | −104 | 1.124 | 1.158 |
| Luỹ kế cuối năm (gồm vốn ban đầu 296) | −1.709 | −1.813 | −690 | +468 |

Dòng tiền luỹ kế theo tháng (cơ sở, trđ, T1→T24):
−521, −675, −786, −878, −950, −1.001, −1.345, −1.444, −1.533, −1.606, −1.662, −1.709, −1.747, −1.774, −1.791, −2.030, −2.055, −2.068, −2.062, −2.036, −1.999, −1.950, −1.886, −1.813.

Hai cú lao dốc ở T7 và T16 xảy ra vì đội tăng gấp đôi trước khi lead kịp tăng theo.

**Chỉ số chính (cơ sở):**

| Chỉ số | Giá trị |
|---|---|
| Hoà vốn vận hành (EBITDA ≥ 0 và giữ được) | **T19** |
| Hoàn vốn (luỹ kế ≥ 0) | **T44** |
| NPV 48 tháng @15% | **−233 trđ** |
| IRR | **khoảng 9%/năm** |

---

## 7. Ba kịch bản

| | Thận trọng | **Cơ sở** | Lạc quan |
|---|---|---|---|
| Hệ số chuyển đổi / CPL / giá đồng hành / lead tự nhiên | ×0,7 / ×1,3 / ×0,85 / ×0,7 | ×1 | ×1,25 / ×0,85 / ×1,1 / ×1,3 |
| Hoàn tiền / tài trợ ngân hàng | 8% / 0 | 5% / 0 | 4% / 10 trđ/tháng |
| Doanh thu năm 1 / 2 / 3 / 4 | 1.074 / 2.861 / 3.539 / 3.643 | 2.684 / 7.320 / 9.166 / 9.465 | 4.936 / 13.669 / 17.273 / 17.883 |
| EBITDA năm 1 / 2 / 3 / 4 | −2.708 / −3.896 / −3.781 / −3.685 | −1.305 / −20 / +1.124 / +1.397 | +279 / +4.745 / +7.320 / +7.878 |
| Dòng tiền năm 1 / 2 / 3 / 4 | −2.816 / −3.980 / −3.781 / −3.685 | −1.413 / −104 / +1.124 / +1.158 | +43 / +3.664 / +5.856 / +6.303 |
| Luỹ kế T24 | **−7.091** | **−1.813** | **+3.412** |
| Hoà vốn vận hành | không đạt | T19 | T8 |
| Hoàn vốn | không đạt | T44 | T14 |
| Vốn cần chuẩn bị | **15.392 trđ nếu chạy hết 48 tháng mà không dừng**. Nếu dừng ở T6 thì lỗ khoảng 1.299 | **2.903** | 1.475 |
| NPV 48 tháng | −10.999 | −233 | +10.558 |
| IRR/năm | n/a | khoảng 9% | khoảng 341% (vốn bỏ ra nhỏ nên con số bị phóng đại, không nên dùng để so sánh) |
| Đội tối đa | 24 | 24 | 28 |

**Phương án lùi mốc tuyển** (giữ đội 8 người tới T9, chuyển Tăng trưởng ở T10, Mở rộng ở T19): ở kịch bản cơ sở, vốn cần giảm xuống 2.741, hoà vốn vận hành T20, hoàn vốn T43, NPV −167. Ở kịch bản lạc quan, vốn cần chỉ còn 1.051. Lùi lịch cứng chỉ cải thiện được một chút. Thứ thật sự giảm rủi ro là **mở giai đoạn theo chỉ tiêu**, xem mục 9.

---

## 8. Độ nhạy ±20% (kịch bản cơ sở)

| Biến | Hệ số | NPV 48t | Luỹ kế T24 | Vốn cần | Hoà vốn vận hành | Hoàn vốn |
|---|---|---|---|---|---|---|
| **Tỷ lệ chuyển đổi (toàn phễu)** | −20% | −5.149 | −4.226 | 7.221 | không đạt | không đạt |
| | +20% | +3.683 | +217 | 1.817 | T17 | **T23** |
| **Giá gói đồng hành** | −20% | −2.566 | −3.069 | 3.946 | T31 | không đạt |
| | +20% | +1.784 | −557 | 2.294 | T17 | T28 |
| **Lương cứng tư vấn viên** | −20% | +93 | −1.590 | 2.733 | T18 | T40 |
| | +20% | −561 | −2.036 | 3.080 | T20 | T48 |
| **Chi phí quảng cáo / lead (CPL)** | −20% | +2.020 | −540 | 2.420 | T17 | T28 |
| | +20% | −2.095 | −2.839 | 3.677 | T24 | không đạt |
| Ngân sách quảng cáo (giữ nguyên CPL) | −20% | −1.913 | −2.724 | 3.568 | T24 | không đạt |
| | +20% | +1.088 | −1.130 | 2.685 | T17 | T33 |
| Lead tự nhiên | −20% | −1.243 | −2.318 | 3.213 | T22 | không đạt |
| | +20% | +624 | −1.424 | 2.770 | T17 | T36 |

Xếp theo mức ảnh hưởng: **tỷ lệ chuyển đổi > giá gói đồng hành ≈ CPL > ngân sách quảng cáo > lead tự nhiên > lương cứng tư vấn viên**.

Lương tư vấn viên ảnh hưởng ít, nên không cần ép lương. Nên dồn sức vào chất lượng hội thảo và tư vấn 1:1. Tăng ngân sách quảng cáo có lợi chừng nào CPL còn giữ được ở mức 60.000 đ.

**Ngưỡng để hoàn vốn trong 24 tháng** (chỉ đổi một biến, các biến khác giữ như cơ sở):
- Tỷ lệ chuyển đổi **+17%**. Tương đương tham dự → đồng hành khoảng 5,6% thay vì 4,4% (hệ số tác động hai lần trên nhánh nền tảng → đồng hành).
- hoặc CPL **−28%**, tức khoảng 43.000 đ/lead.
- hoặc giá gói đồng hành **+31%**, tức khoảng 15,7 trđ.

---

## 9. Việc cần làm để kịch bản khả thi

1. **Chạy thử 3 tháng với đội 8 người**, đo các số thật: CPL, tỷ lệ tham dự, tham dự → nền tảng, tham dự → đồng hành.
   Chỉ tiêu ở T6: **≥ 16 khách đồng hành/tháng** (hoà vốn đội 8 người) và **CPL ≤ 60.000 đ**.
2. **Cổng chuyển sang Tăng trưởng (17 người):** 2 tháng liên tiếp đạt **≥ 25 khách đồng hành/tháng**, tức khoảng 80% ngưỡng 31,6.
   **Cổng chuyển sang Mở rộng (24 người):** 2 tháng liên tiếp đạt **≥ 36 khách/tháng**.
   **Mốc dừng:** nếu ở T6 có dưới 8 khách/tháng thì dừng hoặc tái cấu trúc. Lỗ tối đa khi dừng ở đây khoảng 1,0–1,3 tỷ.
3. **Tuyển theo bậc**, không tuyển gấp đôi trong một tháng. Cú lao dốc ở T7 và T16 trong mô hình là hậu quả của việc tuyển dồn.
4. **Xin xác nhận bằng văn bản với ngân hàng về tài trợ sự kiện và đồng tổ chức.** Mức 10 trđ/tháng đã cải thiện đáng kể kịch bản lạc quan. Chỉ dựa vào hoa hồng giới thiệu thì không đáng kể.
5. **Hạch toán chi phí thời gian của chủ dự án.** Nếu tính lương cho anh khoảng 30 trđ/tháng thì vốn cần tăng thêm khoảng 0,6–0,7 tỷ trong 18 tháng đầu.
6. **Nhờ kế toán xác nhận** tỷ lệ BH 21,5%, kinh phí công đoàn 2% và trạng thái VAT của khoá học.

---

## 10. File

- Script: `/home/user/DRK/team/viec/2026-11-14-khung-chuong-trinh-chuyen-doi/mo_hinh.py`
- Dữ liệu biểu đồ: `/home/user/DRK/team/viec/2026-11-14-khung-chuong-trinh-chuyen-doi/tai-chinh.json`. File gồm: dòng tiền luỹ kế 24 tháng (cơ sở và 3 kịch bản), doanh thu và chi phí theo tháng, phễu theo tháng, số người theo tháng, bảng nhân sự theo giai đoạn và bộ phận, hoà vốn phòng ban, độ nhạy, ngưỡng.
