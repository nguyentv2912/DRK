# Tài chính — Chương trình chuyển đổi khách hàng và Phòng ban vận hành

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người lập: Hùng (Tài chính) · Ngày 14/11/2026
Đơn vị: **triệu đồng (trđ)** nếu không ghi khác. Script: `mo_hinh.py` (chạy `python3 mo_hinh.py`, mọi số dưới đây lấy từ lần chạy này). Số liệu cho biểu đồ nằm trong `tai-chinh.json`.

> **Độ tin cậy dữ liệu.** Lan không mở được trang gốc nào vì mạng bị chặn. Mọi số lấy từ `nghien-cuu.md` (NC) vì thế có độ tin cậy **tối đa là Trung bình**. Tỷ lệ chuyển đổi của phễu, giá gói đồng hành và gói thành viên đều là **giả định** (GĐ) của Hùng, chưa có dữ liệu thực nào kiểm chứng. Lương coach và quản lý vận hành chỉ có số tham chiếu gần từ nghiên cứu vòng 2, không phải số cho đúng chức danh. Mô hình này dùng để ra quyết định có nên đi tiếp hay không và đặt chỉ tiêu. Nó không phải dự báo.

---

## 1. Nhận định (đọc trước)

1. **Lộ trình khuyến nghị là mở rộng theo cổng, và theo kịch bản cơ sở thì lộ trình này khả thi.**
   - Cần chuẩn bị **khoảng 1,32 tỷ đ**.
   - EBITDA dương từ T7. Riêng hai tháng chuyển giai đoạn (T15, T18) bị âm, sau đó dương liên tục từ **T19**.
   - **Hoàn vốn ở T26.** Luỹ kế T24 còn −78 trđ. NPV 48 tháng **+1.677 trđ**, IRR khoảng 79%/năm.
   - Đội: 8 người lúc đầu, 13 người ở T12, 25 người từ T18.
   - Kịch bản lạc quan theo cổng: vốn khoảng 1,0 tỷ, hoàn vốn T10.
2. **Tuyển theo lịch cứng (các mục 4, 6, 7 và 8) thì kịch bản cơ sở không đạt.**
   - Cần **khoảng 3,0 tỷ**. Hoà vốn vận hành T20, hoàn vốn T48. Luỹ kế T24 là **−1,97 tỷ**.
   - NPV −514 trđ, IRR khoảng 2%/năm.
   - Nguyên nhân: đội tăng gấp đôi trước khi lead kịp tăng theo. Vì vậy số liệu chính để lập kế hoạch là **lộ trình theo cổng (mục 7A)**.
3. **Ngưỡng hoà vốn phòng ban phải tính cả công suất coach.**
   - Mỗi cặp coach + trợ giảng chỉ nhận được khoảng 13,3 khách mới/tháng. Vượt mức này là phải thêm cặp.
   - Ngưỡng đúng: **19,5 khách đồng hành/tháng** (đội 10 người) cho Khởi động; **35,2** (19 người) cho Tăng trưởng; **45,9** (25 người) cho Mở rộng.
   - Các con số 15,8 và 31,6 trong bản trước là sai, vì chưa tính phần công suất này.
4. **Với 30 trđ quảng cáo/tháng, đội Khởi động chỉ đạt khoảng 12 khách/tháng, không bao giờ hoà vốn.**
   - Để đạt 19,5 khách cần **54–66 trđ/tháng**. Để đạt 25 khách cần **73–85 trđ/tháng** (CPL 60.000 đ).
   - Vì vậy **cổng mở quảng cáo nên đo bằng tỷ lệ chuyển đổi** (khách trên 1.000 lead): nó cho biết bỏ thêm tiền quảng cáo có sinh lời hay không.
   - **Cổng tuyển người nên đo bằng số khách tuyệt đối**: phải đủ khách thì mới trả được lương cho đội lớn hơn.
5. **Kết quả rất nhạy với tỷ lệ chuyển đổi và CPL.**
   - Kịch bản Thận trọng (chuyển đổi ×0,7) không bao giờ hoà vốn, kể cả khi đi theo cổng. Ở T6 khi đó chỉ có 4,7 khách/tháng, chạm mốc dừng (< 8 khách). **Dừng tại đây thì lỗ khoảng 1,44 tỷ.**
   - Doanh thu ngân hàng chưa tới 0,5% doanh thu.
   - Còn ba khoản chưa đưa vào mô hình: lương chủ dự án, kinh phí công đoàn 2%, VAT.

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
| Nhân sự | Công suất 1 **cặp** coach + trợ giảng | 40 học viên đang học (khoá 3 tháng, tức khoảng 13,3 khách mới/tháng mỗi cặp) | | giả định. Mọi giai đoạn đều xếp coach và trợ giảng theo cặp 1:1. Vượt công suất thì mô hình tự thêm cặp, áp dụng cả trong mô hình theo tháng lẫn khi tính ngưỡng hoà vốn | — |
| Nhân sự | Công suất 1 tư vấn viên | 600 | lead/tháng | giả định. Vượt thì mô hình tự thêm tư vấn viên (9 trđ + BH) | — |
| Lộ trình theo cổng | Cổng quảng cáo | ≥ 14 khách đồng hành / 1.000 lead (80% của 17,6) thì nâng quảng cáo Khởi động 30 → 70 trđ. Hạ về 30 nếu 2 tháng liền < 11,2 | | giả định | — |
| Lộ trình theo cổng | Cổng tuyển | 2 tháng liên tiếp ≥ 80% ngưỡng hoà vốn của giai đoạn kế (28,2 khách lên Tăng trưởng; 36,8 khách lên Mở rộng). Không quay lui | | giả định | — |
| Lộ trình theo cổng | Quảng cáo Tăng trưởng / Mở rộng | 100 / 130 | trđ/tháng | giả định. Khoảng ngân sách cần cho ngưỡng hoà vốn từng giai đoạn (mục 5) | — |
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

## 4. Vốn cần chuẩn bị

**Tháng 0 = tuần 0.** Toàn bộ vốn đầu tư ban đầu là khoản chi **trước T1**, tức trong tuần 0 của lộ trình. Khoản này giống nhau ở mọi kịch bản và lộ trình.

| Hạng mục (chi trong tuần 0) | trđ |
|---|---|
| Thiết bị quay dựng (máy quay, mic, đèn, phông) | 80 |
| Thiết bị cho đội khởi động (8 người × 12) | 96 |
| Pháp lý khởi tạo: luật sư rà soát nội dung, hợp đồng mẫu, ý kiến bằng văn bản cho 10 câu hỏi pháp lý. **Giả định, chưa có báo giá luật sư** | 30 |
| Lệ phí pháp nhân / bổ sung ngành nghề + tra cứu và đăng ký nhãn hiệu tên chương trình. **Giả định, cần báo giá** | 10 |
| Nhận diện, website, LMS, phễu đăng ký | 40 |
| Sản xuất bài giảng khoá nền tảng | 30 |
| Cải tạo nhỏ không gian hội thảo trong văn phòng có sẵn | 20 |
| **Cộng vốn đầu tư ban đầu (tuần 0)** | **306** |

Mô hình chưa tính lương cho người nhận việc từ tuần 0, trước T1. Nếu Quản lý vận hành vào làm sớm 2–4 tuần thì tốn thêm khoảng 15–30 trđ (giả định). Nên ký hợp đồng lao động sau khi đã qua Cổng 0, tức đã có ý kiến luật sư.

| Tổng vốn cần chuẩn bị | **Lộ trình theo cổng (khuyến nghị)** | Tuyển theo lịch |
|---|---|---|
| Vốn ban đầu (tuần 0) | 306 | 306 |
| Vốn lưu động: lỗ vận hành phải bù tới đáy dòng tiền | 711 (đáy −1.017 ở T7) | 1.840 (đáy −2.146 ở T19) |
| Quỹ dự phòng: 2 tháng chi phí cố định của đội tại tháng đáy | 298 | 862 |
| **TỔNG (cơ sở)** | **1.316** | **3.008** |
| Tổng (lạc quan) | 1.004 | 1.485 |

Quỹ dự phòng của lộ trình theo cổng được tính theo đội Khởi động. Khi lên Tăng trưởng hoặc Mở rộng thì chương trình đã có lãi vận hành, nhưng tháng chuyển giai đoạn vẫn âm khoảng 45–62 trđ. Nên giữ quỹ dự phòng này cho tới khi đội ổn định ở quy mô mới.

---

## 5. Kế hoạch phòng ban: nhân sự theo giai đoạn

| Bộ phận | Vị trí | Khởi động | Tăng trưởng | Mở rộng |
|---|---|---|---|---|
| Quản lý | Quản lý vận hành | 1 | 1 | 1 |
| Quản lý | Kế toán – hành chính | – | 1 | 1 |
| Thực thi | Coach tài chính | 1 | 2 | 4 |
| Thực thi | Trợ giảng (theo cặp 1:1 với coach) | 1 | 2 | 4 |
| Bán hàng | Trưởng nhóm bán hàng | – | 1 | 1 |
| Bán hàng | Tư vấn viên | 2 | 4 | 6 |
| CSKH | Chăm sóc khách hàng | 1 | 2 | 3 |
| Nội dung | Content creator | 1 | 2 | 2 |
| Nội dung | Video editor | 1 | 1 | 2 |
| Nội dung | Chuyên viên quảng cáo | – | 1 | 1 |
| | **Tổng người theo kế hoạch** | **8** | **17** | **25** |
| | Công suất đội kế hoạch (khách đồng hành mới/tháng) | 13,3 | 26,7 | 53,3 |
| | Lương cứng + BH doanh nghiệp (trđ/tháng) | 131,2 | 272,2 | 394,9 |

Ở bản trước, Mở rộng có 4 coach nhưng chỉ 3 trợ giảng. Bản này đã sửa thành 4 trợ giảng để khớp cách tính công suất theo cặp, nên các số của phương án tuyển theo lịch đổi nhẹ so với bản trước.

Khi số học viên hoặc số lead vượt công suất, mô hình tự thêm cặp coach + trợ giảng hoặc thêm tư vấn viên. Vì vậy số người thực tế có thể cao hơn bảng trên, ví dụ lộ trình theo cổng có 13 người ở T12. Chủ dự án nằm ngoài bảng lương.

### Hoà vốn phòng ban: có tính công suất coach

Ngưỡng được tính lặp: số cặp coach cần = làm tròn lên (3 × khách mới/tháng ÷ 40); cộng chi phí các cặp thêm vào chi phí cố định; tính lại ngưỡng; lặp cho tới khi số cặp không đổi.

| Giai đoạn | Người theo kế hoạch → **người thực tế ở ngưỡng** | Chi phí cố định/tháng | Ngưỡng nếu bỏ qua công suất (sai) | **Khách đồng hành mới cần/tháng** | Khách nền tảng đi kèm | Lead cần/tháng | **Doanh số cần/tháng** |
|---|---|---|---|---|---|---|---|
| Khởi động | 8 → **10** (thêm 1 cặp) | 204,9 | 15,8 | **19,5** | 53 | 1.105 | **312,9** |
| Tăng trưởng | 17 → **19** (thêm 1 cặp) | 370,6 | 31,6 | **35,2** | 96 | 2.000 | **565,9** |
| Mở rộng | 25 → **25** | 483,9 | 45,9 | **45,9** | 125 | 2.611 | **738,9** |

Hà tính ra ngưỡng Khởi động là 19,4. Script ra 19,46, làm tròn thành 19,5, còn doanh số 312,9 trđ thì trùng khớp.

Kinh tế đơn vị (cơ sở, trên 1.000 lead):

| Chỉ tiêu | Giá trị |
|---|---|
| Người tham dự | 400 |
| Khách nền tảng | 48 |
| Khách đồng hành | 17,6 |
| Thành viên | 9,4 |
| Doanh thu sau hoàn tiền | 283 trđ |
| Chi phí biến đổi (phí thanh toán, học liệu, hoa hồng; hoàn tiền đã trừ vào doanh thu) | 38 trđ |
| Quảng cáo, nếu mọi lead đều trả phí | 60 trđ |
| Đóng góp | 185 trđ |
| Doanh thu mỗi khách đồng hành | 16,1 trđ |
| Đóng góp mỗi khách đồng hành | 10,5 trđ |

### Ngân sách quảng cáo cần (CPL 60.000 đ, trạng thái ổn định 17,6 khách/1.000 lead)

| Mục tiêu khách đồng hành/tháng | Lead cần | Ngân sách nếu toàn bộ lead trả phí | Ngân sách khi đã có 205 lead tự nhiên (mức T6) |
|---|---|---|---|
| Ngân sách hiện tại 30 trđ → đạt **khoảng 12,4 khách** | 705 | — | 30 |
| **19,5** (hoà vốn Khởi động) | 1.105 | **66,3** | **54,1** |
| **25** (cổng cũ của kế hoạch) | 1.420 | **85,2** | **73,0** |
| 35,2 (hoà vốn Tăng trưởng) | 2.000 | 120,0 | 107,7 |

Đề xuất cách đo cổng:
- **Cổng mở quảng cáo đo bằng tỷ lệ**: đạt từ 14 khách đồng hành / 1.000 lead và CPL ≤ 60.000 đ thì nâng quảng cáo lên khoảng 70 trđ. Số khách tuyệt đối chủ yếu phụ thuộc ngân sách, nên không cho biết phễu tốt hay xấu.
- **Cổng tuyển người đo bằng số khách tuyệt đối**: 2 tháng liên tiếp đạt ≥ 80% ngưỡng hoà vốn của giai đoạn kế, tức **28 khách** để lên Tăng trưởng và **37 khách** để lên Mở rộng. Lương phải trả bằng số khách thật, không trả bằng tỷ lệ được.
- **Mốc dừng** ở T6 giữ nguyên: dưới 8 khách/tháng **và** dưới 14 khách/1.000 lead thì dừng hoặc tái cấu trúc phễu.

---

## 6. Kết quả theo năm: tuyển theo lịch (cơ sở)

Bảng này do script in ra, ở mục "BẢNG THEO NĂM CHI TIẾT". Lịch tuyển cố định: Tăng trưởng từ T7, Mở rộng từ T16.

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
| Lương cứng + BH | 2.420 | 4.370 | 4.739 | 4.739 |
| Chi phí cố định khác | 258 | 399 | 432 | 432 |
| Tuyển dụng | 166 | 119 | 60 | 60 |
| **EBITDA** | **−1.305** | **−150** | **961** | **1.234** |
| Thuế TNDN | 0 | 0 | 0 | 148 |
| Thiết bị (capex) | 108 | 96 | 0 | 0 |
| Dòng tiền | −1.413 | −246 | 961 | 1.086 |
| Luỹ kế cuối năm (gồm vốn 306) | −1.719 | −1.965 | −1.004 | +82 |

Luỹ kế theo tháng (tuyển theo lịch, cơ sở, T1→T24):
−531, −685, −796, −888, −960, −1.011, −1.355, −1.454, −1.543, −1.616, −1.672, −1.719, −1.757, −1.784, −1.800, −2.074, −2.113, −2.139, −2.146, −2.133, −2.111, −2.075, −2.025, −1.965.

Chỉ số của phương án này:

| Chỉ số | Giá trị |
|---|---|
| Hoà vốn vận hành | T20 |
| Hoàn vốn | T48 |
| NPV 48 tháng | −514 |
| IRR | khoảng 2%/năm |

---

## 7A. Lộ trình theo cổng (KHUYẾN NGHỊ CHÍNH THỨC)

Quy tắc chạy trong `mo_hinh.py`, biến `CONG`:
- T1 quảng cáo 10 trđ (thử nghiệm). Từ T2 quảng cáo 30 trđ.
- Đạt ≥ 14 khách / 1.000 lead thì quảng cáo lên 70 trđ.
- 2 tháng liên tiếp ≥ 28,2 khách thì lên Tăng trưởng (quảng cáo 100 trđ).
- 2 tháng liên tiếp ≥ 36,8 khách thì lên Mở rộng (quảng cáo 130 trđ).
- Coach, trợ giảng và tư vấn viên tự thêm khi vượt công suất.

| trđ | **Cơ sở** | Lạc quan | Thận trọng | Tham chiếu: giữ đội 8, quảng cáo 30 cả 48 tháng |
|---|---|---|---|---|
| Mở quảng cáo 70 / lên Tăng trưởng / lên Mở rộng | T6 / T15 / T18 | T4 / T7 / T9 | không đạt cổng nào | — |
| Đội T6 / T12 / T24 (người) | 9 / 13 / 25 | 13 / 29 / 32 | 8 / 8 / 8 | 8 / 10 / 11 |
| Doanh thu năm 1 / năm 2 | 3.104 / 8.546 | 8.376 / 18.165 | 765 / 1.534 | 1.935 / 4.028 |
| EBITDA năm 1 / năm 2 | −318 / +934 | +1.952 / +7.149 | −1.719 / −1.013 | −815 / +667 |
| Dòng tiền năm 3 / năm 4 | +1.312 / +1.616 | +7.388 / +7.833 | — | — |
| Đáy luỹ kế | −1.017 (T7) | −705 (T3) | — | −1.145 (T12) |
| **Tổng vốn cần** | **1.316** | **1.004** | **dừng ở T6: lỗ khoảng 1.440** (luỹ kế −1.309 + 1 tháng lương) | 1.444 |
| Hoà vốn vận hành (dương liên tục) | **T19**. Dương từ T7, chỉ âm ở 2 tháng chuyển giai đoạn T15, T18 | T4 | không đạt | T13 |
| **Hoàn vốn** | **T26** | T10 | không đạt | T29 |
| Luỹ kế T24 | **−78** | +6.627 | −3.038 (nếu không dừng) | −490 |
| NPV 48 tháng | **+1.677** | +15.297 | −3.629 (nếu không dừng) | +1.060 |
| IRR/năm | khoảng 79% | rất cao, không dùng để so sánh | n/a | khoảng 52% |

Luỹ kế theo tháng (theo cổng, cơ sở, T1→T24):
−531, −685, −796, −888, −960, −1.004, −1.017, −966, −899, −812, −714, −684, −604, −514, −684, −616, −538, −679, −595, −515, −425, −318, −202, −78.

Hà đã chạy thử phương án "giữ đội 8, quảng cáo 30" và ra T13 / T28 / −395. Script ra T13 / T29 / −490. Chênh lệch đến từ hai điểm: vốn ban đầu đã cộng thêm 10 trđ lệ phí, và mô hình tự thêm tư vấn viên khi lead vượt 600 người/tư vấn viên.

Tóm lại: so với "giữ đội 8", lộ trình theo cổng **cần ít vốn hơn và hoàn vốn sớm hơn**. Lý do là nó nâng quảng cáo ngay khi tỷ lệ chuyển đổi đã được chứng minh, rồi mới tuyển người.

## 7B. Ba kịch bản: tuyển theo lịch (để so sánh)

| | Thận trọng | Cơ sở | Lạc quan |
|---|---|---|---|
| Hệ số chuyển đổi / CPL / giá đồng hành / lead tự nhiên | ×0,7 / ×1,3 / ×0,85 / ×0,7 | ×1 | ×1,25 / ×0,85 / ×1,1 / ×1,3 |
| Hoàn tiền / tài trợ ngân hàng | 8% / 0 | 5% / 0 | 4% / 10 trđ/tháng |
| Doanh thu năm 1 / 2 / 3 / 4 | 1.074 / 2.861 / 3.539 / 3.643 | 2.684 / 7.320 / 9.166 / 9.465 | 4.936 / 13.669 / 17.273 / 17.883 |
| EBITDA năm 1 / 2 / 3 / 4 | −2.708 / −4.026 / −3.943 / −3.848 | −1.305 / −150 / +961 / +1.234 | +279 / +4.615 / +7.157 / +7.715 |
| Dòng tiền năm 1 / 2 / 3 / 4 | −2.816 / −4.122 / −3.943 / −3.848 | −1.413 / −246 / +961 / +1.086 | +43 / +3.548 / +5.725 / +6.172 |
| Luỹ kế T24 | −7.243 | −1.965 | +3.285 |
| Hoà vốn vận hành / hoàn vốn | không đạt / không đạt | T20 / T48 | T8 / T14 |
| Vốn cần chuẩn bị | **15.896 trđ nếu chạy hết 48 tháng mà không dừng** (lỗ T6 −1.309) | 3.008 | 1.485 |
| NPV 48 tháng | −11.336 | −514 | +10.285 |
| IRR/năm | n/a | khoảng 2% | khoảng 331% (không dùng để so sánh) |
| Đội tối đa | 25 | 25 | 29 |

Phương án lùi lịch tuyển cứng (Tăng trưởng từ T10, Mở rộng từ T19), kịch bản cơ sở: vốn 2.816, hoà vốn vận hành T21, hoàn vốn T47, NPV −418. Chỉ lùi lịch thì gần như không cải thiện gì. Thứ tạo khác biệt là cổng.

---

## 8. Độ nhạy ±20% (tuyển theo lịch, cơ sở)

| Biến | Hệ số | NPV 48t | Luỹ kế T24 | Vốn cần | Hoà vốn vận hành | Hoàn vốn |
|---|---|---|---|---|---|---|
| **Tỷ lệ chuyển đổi (toàn phễu)** | −20% | −5.486 | −4.378 | 7.725 | không đạt | không đạt |
| | +20% | +3.409 | +90 | 1.827 | T17 | T24 |
| **Giá gói đồng hành** | −20% | −2.903 | −3.221 | 4.222 | T35 | không đạt |
| | +20% | +1.509 | −709 | 2.364 | T17 | T30 |
| **Lương cứng tư vấn viên** | −20% | −186 | −1.742 | 2.830 | T19 | T43 |
| | +20% | −844 | −2.188 | 3.192 | T21 | không đạt |
| **Chi phí quảng cáo / lead (CPL)** | −20% | +1.745 | −692 | 2.490 | T17 | T29 |
| | +20% | −2.432 | −2.991 | 3.865 | T28 | không đạt |
| Ngân sách quảng cáo (giữ CPL) | −20% | −2.250 | −2.876 | 3.738 | T25 | không đạt |
| | +20% | +812 | −1.283 | 2.755 | T17 | T34 |
| Lead tự nhiên | −20% | −1.580 | −2.470 | 3.355 | T23 | không đạt |
| | +20% | +347 | −1.576 | 2.849 | T18 | T38 |

Xếp theo mức ảnh hưởng: tỷ lệ chuyển đổi > giá gói đồng hành ≈ CPL > ngân sách quảng cáo > lead tự nhiên > lương tư vấn viên.

Ngưỡng để hoàn vốn trong 24 tháng khi tuyển theo lịch (chỉ đổi một biến):
- chuyển đổi **+19%**;
- hoặc CPL **−30%**, khoảng 42.000 đ;
- hoặc giá gói đồng hành **+33%**, khoảng 16 trđ.

Lộ trình theo cổng đã gần đạt mức này mà không cần đổi giả định nào: luỹ kế T24 là −78, hoàn vốn T26.

---

## 9. Việc cần làm

1. **Tuần 0:**
   - Lấy báo giá luật sư (đang giả định 30 trđ) và báo giá lệ phí pháp nhân, nhãn hiệu (đang giả định 10 trđ).
   - Chỉ ký hợp đồng lao động sau khi có ý kiến luật sư.
2. **T2–T5, quảng cáo 30 trđ:** đo CPL, tỷ lệ tham dự và tỷ lệ khách/1.000 lead.
3. **Cổng quảng cáo:** đạt ≥ 14 khách / 1.000 lead và CPL ≤ 60.000 đ thì nâng quảng cáo lên khoảng 70 trđ. Khi vượt 13 khách/tháng thì tuyển cặp coach + trợ giảng thứ hai. Khi lead vượt 1.200/tháng thì tuyển tư vấn viên thứ ba.
4. **Cổng tuyển:**
   - 2 tháng liên tiếp ≥ 28 khách thì lên đội Tăng trưởng (17 người theo kế hoạch, 19 người ở ngưỡng).
   - 2 tháng liên tiếp ≥ 37 khách thì lên Mở rộng (25 người).
5. **Mốc dừng ở T6:** dưới 8 khách/tháng và dưới 14 khách/1.000 lead thì dừng. Lỗ tối đa khoảng 1,0–1,44 tỷ.
6. **Ngân hàng:** xin văn bản về tài trợ sự kiện. Hoa hồng giới thiệu không đáng kể.
7. **Kế toán xác nhận:** BH 21,5%, kinh phí công đoàn 2%, VAT của khoá học. Ngoài ra cần hạch toán lương chủ dự án: ở mức 30 trđ/tháng thì tốn thêm khoảng 0,6–0,7 tỷ trong 18 tháng.

---

## 10. File

- Script: `/home/user/DRK/team/viec/2026-11-14-khung-chuong-trinh-chuyen-doi/mo_hinh.py`
- Dữ liệu biểu đồ: `/home/user/DRK/team/viec/2026-11-14-khung-chuong-trinh-chuyen-doi/tai-chinh.json`.
  - Các khoá cũ vẫn giữ nguyên; số bên trong là bản tuyển theo lịch.
  - Khoá mới: `lo_trinh_theo_cong` (gồm tóm tắt từng kịch bản, luỹ kế, giai đoạn, số người, ngân sách quảng cáo và số khách theo tháng, mốc dừng của Thận trọng) và `ngan_sach_qc_can`.
  - `hoa_von_phong_ban` đã có thêm các trường về công suất coach.
