# Kiểm định cuối — phiên bản 2 (Đầu Tư Bình An trên Skool)

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người kiểm: Hà – Kiểm định · 14/11/2026
Phạm vi: brief.md (mục "Hiện trạng chủ dự án"), nghien-cuu.md, mo_hinh.py, tai-chinh.md, tai-chinh.json, ke-hoach.md; đối chiếu fanpage/KENH.md, fanpage/brand.md. Không đọc ban-nhap-cu/.

## Kết luận: **CHƯA ĐẠT** — 1 lỗi Chặn, 5 lỗi Nên sửa, 9 Gợi ý

Sửa lỗi Chặn #1 (3–4 chỗ trong ke-hoach.md, 1 câu trong tai-chinh.md) là đạt. Các phần khác đạt.

## Đã kiểm, đạt
| Hạng mục | Kết quả |
|---|---|
| Giá anh chốt | 100 USD/tháng, 1.000 USD, ebook ~1.000.000 đ, Skool: giống nhau ở cả 4 file. Không ai đổi giá. Trả góp 4 × 250 USD, gói 12 tháng, gói năm đều ghi là phương án để anh quyết |
| Chạy lại mo_hinh.py | Chạy trên bản sao: tai-chinh.json và tai-chinh.md sinh ra **giống từng byte** bản đang nộp |
| Số ke-hoach ↔ TC/JSON | Khớp: vốn 78,0 tr (32,0 dự phòng); hoà vốn 2 HV; hoàn vốn T6 / T15; T24 114 / 10 / ~1 HV; lãi T24 269,9 / 22,5; luỹ kế 2.824,4 / 175,7 / −93,6; mốc 22/42/90 và 26/47/102; bảng phễu tháng 1–3 cả 3 kịch bản; mốc tháng 6 (140 / 2,6 / 3,9 và 585 / 18,4 / 42,0); bảng phương án A/B mục 6; quỹ 104,4 tr; tháng thuê 6/17/18/20; Hobby→Pro 1.268 USD, tháng 5 |
| Tự tính lại | Đóng góp 1 HV: Pro 2,284 tr, Hobby 2,104 tr ✓ · Điểm hoà Hobby–Pro 90/0,071 = 1.267,6 USD ✓ · 1.000 USD qua Pro nhận 960,70 USD ✓ · Hoà vốn Hobby (2,1 + 0,234)/2,104 = 1,11 → 2 HV ✓ · Thời gian ở lại 1/0,09 = 11,1 tháng ✓ · 1.000/120 = 8,3 USD ✓ |
| Số tự tính của Mai | 1.000 + 100 × 120 = 13.000 USD ✓ · 100 người × 45 phút = 75 giờ/năm ✓ (xem Gợi ý #9 về phạm vi) · 15 người mua luỹ kế cuối năm 2 ✓ (JSON 15,4) |
| Đề cương | Đúng 5 tầng theo thứ tự FED → VCs → Protocol/Dev → KOLs/Media → Retail; Phần 2 ghi đúng 6 × 6 × 6 = 216, (2 × 3)³, chu kỳ BTC + altcoin, lặp 2 chu kỳ. Toàn bộ cột ĐẦU TƯ là [chờ anh]; đội không tự viết phương pháp |
| Tuân thủ | "216" chỉ gọi là khung chu kỳ, có 3 phương án câu chữ; không hứa lợi nhuận cho học viên; không có tên sàn nào (đã tìm Binance, OKX, Bybit, Remitano…); quy tắc không gọi kèo, không giữ tiền/ví; câu miễn trừ cho video, Skool, trang bán; quy tắc dùng Phật – Nho – Đạo tôn trọng, không dùng hình tượng tôn giáo, nêu xung đột với brand.md để anh duyệt |
| Nguồn | nghien-cuu.md có link cho từng dữ kiện, ghi độ tin cậy, nói rõ giới hạn tra cứu; tai-chinh.md ghi giả định cho từng số |
| Không lẫn dự án | Không thấy số của ban-nhap-cu/ (990.000 đ, 12 triệu, 3,6 triệu, 1,4 tỷ, đội 10 người). Dữ kiện kênh (giờ 05:30/08:00/11:30/12:00, 7 chuyên mục, KPI 30 ngày, quay 2–3 kịch bản/ngày, miễn trừ) khớp KENH.md và brand.md |
| Chính tả | Không thấy chữ thiếu dấu, câu cụt hay tiêu đề trùng |

## Danh sách lỗi

| # | Mức | Vị trí | Vấn đề | Cách sửa |
|---|---|---|---|---|
| 1 | **Chặn** | ke-hoach.md: Tóm tắt dòng "Hai mốc dừng"; mục 7.4 Cổng 3; mục 8 dòng "Ít người vào Skool"; Tóm tắt dòng "Mục tiêu 90 ngày" và tiêu đề bảng 7.5 | **Ghi sai chỉ số của mốc dừng.** Trong mo_hinh.py/JSON (`nguong_dung.cd_toi_thieu` = 0,025), 2,5% là ngưỡng **chuyển đổi miễn phí mới → 100 USD** (trung bình của 2% thận trọng và 3% cơ sở; tai-chinh.md 5b dòng "phải xét kèm tỷ lệ"). Mai lại ghi thành "chuyển đổi vào Skool < 2,5%" / "theo dõi mới → Skool < 2,5%". Đường tối thiểu của TC tương ứng tỷ lệ vào Skool chỉ **0,9%**. Hệ quả: anh sẽ đo sai chỉ số khi quyết định đổi cách bán. Thêm nữa, ke-hoach gọi thận trọng là "mức sàn" và viết "dưới mốc thận trọng là đi theo hướng không đáng làm", trong khi TC 5b kết luận **thận trọng cũng không qua ngưỡng** (chuyển đổi 2% < 2,5%, huỷ 15% > 12%): nếu số thật giống thận trọng thì đổi cách bán ngay ở tháng 3 | Thay "chuyển đổi vào Skool / theo dõi mới → Skool < 2,5%" bằng "**chuyển đổi miễn phí mới → 100 USD < 2,5%**" ở Tóm tắt, 7.4 và mục 8 (mục 8 có thể giữ 2,5% làm dấu hiệu sớm nhưng ghi là giả định thận trọng, không phải ngưỡng TC). Thêm vào 7.5 một dòng KPI "Miễn phí mới → 100 USD: ≥ 2,5% (ngưỡng)". Sửa câu mục tiêu 90 ngày: số thận trọng (72 thành viên, ~1 HV) là **mốc số lượng**; muốn qua cổng còn phải có chuyển đổi ≥ 2,5% và huỷ ≤ 12%. Hùng: ở tai-chinh.md 5b dòng "Mốc tháng 3" ghi rõ "chuyển đổi **miễn phí mới → 100 USD** < 2,5%" (sửa chuỗi trong mo_hinh.py rồi chạy lại) |
| 2 | Nên sửa | ke-hoach.md mục 5.3, ý tưởng #9 | "Nước mềm nhưng mài mòn đá" ghi xuất xứ Đạo Đức Kinh ch. 8. Ch. 8 là "Thượng thiện nhược thuỷ" (nước làm lợi vạn vật, không tranh). Ý "mềm thắng cứng" nằm ở **ch. 78** ("thiên hạ mạc nhu nhược ư thuỷ, nhi công kiên cường giả mạc chi năng thắng") và ch. 43. brand.md cấm trích sai câu nói | Đổi xuất xứ thành "Đạo Đức Kinh ch. 78", hoặc giữ ch. 8 và đổi hook cho đúng ý ch. 8 |
| 3 | Nên sửa | tai-chinh.md mục 1, dòng "Thuế"; mo_hinh.py dòng 39 (chú thích) | Dẫn nghien-cuu.md là "ngưỡng không chịu thuế 500 tr/năm, báo chí nói NĐ 141/2026 nâng lên 1 tỷ — chưa đối chiếu". Bản nghien-cuu.md hiện tại (sửa vòng 2) ghi NĐ 141/2026 (29/4/2026) nâng ngưỡng lên 1 tỷ, áp dụng từ 1/1/2026 (tin cậy Trung bình, chưa có toàn văn). Hai file mô tả nguồn khác nhau | Sửa câu dẫn: "nghien-cuu.md: NĐ 141/2026 nâng ngưỡng lên 1 tỷ đ/năm (chưa có toàn văn)". Giữ 7% làm mặc định thận trọng là hợp lý, không cần đổi số |
| 4 | Nên sửa | ke-hoach.md mục 3.4 (dòng "Mỗi năm", "Mỗi lần chuyển pha") và mục 4.4 "Cần luật sư xác nhận" | Buổi 1:1 "review danh mục" và buổi "chuyển pha… chốt lời/giảm rủi ro" là hoạt động cá nhân hoá, dễ bị coi là tư vấn đầu tư. Việc này chưa có trong danh sách cần luật sư xác nhận | Thêm vào 4.4 và 7.1 (Pháp lý): "Luật sư xác nhận ranh giới giáo dục / tư vấn cho buổi 1:1 review danh mục và buổi chuyển pha". Thêm câu cố định khi mở buổi: "Học viên tự quyết, không có khuyến nghị mua/bán" |
| 5 | Nên sửa | ke-hoach.md mục 3.2 bài 2.5; Gợi ý hình #5 | Bài 2.1 còn hỏi anh "10 năm gồm mấy chu kỳ", nhưng bài 2.5 ("chu kỳ 2 và 3") và hình 5 ("chu kỳ 1–2–3") đã ngầm hiểu là 3 chu kỳ. Ghi chép của anh chỉ nói "lặp lại ở 2 chu kỳ tiếp theo" | Ghi rõ "[chờ anh: nếu hiểu là 3 chu kỳ]" ở 2.5 và hình 5, hoặc viết trung tính "các chu kỳ tiếp theo" |
| 6 | Nên sửa | tai-chinh.md mục 5b, dòng "Mốc tháng 3" | Chữ "chuyển đổi < 2,5%" không nói là chuyển đổi nào; đây là gốc của lỗi #1 | Ghi rõ "chuyển đổi miễn phí mới → 100 USD" (đi kèm sửa #1) |
| 7 | Gợi ý | ke-hoach.md mục 5.1, câu "Không lặp trụ cột 2 ngày liền — lịch trên đã thoả" | Đúng với chuyên mục KENH. Nhưng lớp dẫn dắt lặp: ĐỜI Năm–Sáu, ĐẠO Chủ Nhật–Thứ Hai | Ghi "thoả theo chuyên mục KENH", hoặc đổi lớp dẫn dắt của Thứ Sáu |
| 8 | Gợi ý | ke-hoach.md mục 7.5, cột Tháng 2 (≥ 55%, ≥ 10 bình luận) | Ghi nguồn KENH, nhưng KENH chỉ có mốc 30 ngày và 90 ngày | Ghi "nội suy từ KENH" |
| 9 | Gợi ý | ke-hoach.md mục 3.4, dòng "Năng lực phục vụ" | Phép tính 75 giờ/năm chỉ tính buổi 1:1 hằng năm. Chưa tính buổi định hướng 1:1 khi vào (45 phút/người) và buổi chuyển pha | Thêm buổi định hướng và buổi chuyển pha, hoặc ghi rõ phạm vi của phép tính |
| 10 | Gợi ý | ke-hoach.md mục 1, Bước 2 | Ghi "bài ghim 'Bắt đầu từ đây' có sẵn (KENH)". KENH ghi bài này là kế hoạch, "5 video nền tảng (sau tuần 2)" | Đổi "có sẵn" thành "theo kế hoạch KENH" |
| 11 | Gợi ý | ke-hoach.md mục 3.2 bài 2.0, mục 5.3 #4 | Luận Ngữ 13.17 nguyên văn là "Dục tốc **tắc** bất đạt, kiến tiểu lợi tắc đại sự bất thành" | Bổ sung chữ "tắc" khi đưa lên slide hoặc ebook |
| 12 | Gợi ý | ke-hoach.md mục 3.2 bài 2.2 | Đặt "Âm – dương" cạnh bài "Đọc công thức 6 × 6 × 6" có thể bị hiểu là đội gợi ý "2" = âm dương, tức là diễn giải phương pháp thay anh | Thêm "(chỉ là lớp Đạo, không ngụ ý nghĩa của số 2)" hoặc chờ anh giảng xong mới chọn câu Đạo |
| 13 | Gợi ý | tai-chinh.md mục 9, câu đầu | "Dự án gần như không thể lỗ nặng" là câu khẳng định | Đổi thành "Rủi ro mất tiền nhỏ (vốn 78,0 tr); chi phí chính nếu thất bại là thời gian của anh" |
| 14 | Gợi ý | mo_hinh.py (JSON `cp_chuyen_tien` tháng 1 = −4.680 đ ở mọi kịch bản) | Phí chuyển tiền bị âm khi doanh thu bằng 0. Ảnh hưởng không đáng kể | Kẹp `max(0, …)` |
| 15 | Gợi ý | nghien-cuu.md, Kết luận 1 và 7 | Có khoảng hở "≤ 899 USD" / "> 900 USD". Kết luận 7 viết chắc "theo NĐ 141/2026… không chịu thuế", trong khi bảng E ghi chưa có toàn văn | Ghi "≤ 900 / > 900 USD" theo nguồn. Thêm "(chưa có toàn văn)" ở Kết luận 7 |

Ghi chú: phương án "gói 1.000 USD cho 12 tháng" (TC mục 8, ke-hoach mục 6) và "gói năm" (mốc tháng 3) làm thay đổi thời hạn "10 năm" mà anh đã chốt. Cả hai đều đã ghi rõ là để anh quyết, nên không tính là lỗi.

## Tóm tắt số lỗi
- Chặn: 1 (#1)
- Nên sửa: 5 (#2–#6)
- Gợi ý: 9 (#7–#15)

---

# Lần 2 — kiểm lại sau khi sửa (14/11/2026)

## Kết luận lần 2: **ĐẠT** — 0 lỗi Chặn, 0 lỗi Nên sửa, 4 Gợi ý còn lại (không chặn bàn giao)

## Chạy lại mô hình
- Chạy lại mo_hinh.py trên bản sao: tai-chinh.json và tai-chinh.md sinh ra **giống từng byte** bản đang nộp.
- Sửa phí âm làm vài số đổi nhẹ ở tai-chinh.md: luỹ kế tháng 13 từ 654,2 thành 654,1 tr; NPV thận trọng từ 137,7 thành 137,6 tr; IRR lạc quan từ 62.356% thành 62.351%. ke-hoach.md **không dẫn** các số này. Mọi số chính khác giữ nguyên.
- Đối chiếu lại ke-hoach ↔ JSON: tất cả khớp. Gồm: vốn 78,0 tr; hoà vốn 2 HV; hoàn vốn tháng 6 và 15; số tháng 24 (114 / 10 / ~1 HV; 269,9 / 22,5 tr; 2.824,4 / 175,7 / −93,6 tr); bảng phễu tháng 1–3; ngưỡng 55 / 1 / 110 / 3 / 6,2 tr; `cd_toi_thieu` 2,5%, `huy_toi_da` 12%; `ket_qua` (thận trọng không qua cả 2 cổng); bảng phương án A/B; quỹ 104,4 tr; 1.268 USD; tháng thuê 6/17/18/20. Câu "5/11 rủi ro mức Cao" ở mục 8 đúng: đếm lại có 5 dòng Cao trên tổng 11 dòng.

## Trạng thái từng lỗi lần 1
| # | Lỗi lần 1 | Trạng thái | Ghi chú kiểm |
|---|---|---|---|
| 1 | Chặn: ghi sai chỉ số mốc dừng | **Đã sửa** | Tóm tắt, 7.4, 7.5, mục 8 đều ghi "miễn phí mới → 100 USD ≥ 2,5%" và "huỷ ≤ 12%". "Theo dõi → Skool" được ghi là giả định, không phải ngưỡng. Có ghi rõ thận trọng không qua cổng. Khớp `nguong_dung` trong JSON |
| 2 | Xuất xứ "nước mài mòn đá" (ch. 8) | Đã sửa | Ý tưởng này đã bỏ (5.3 còn 5 ý tưởng). Ch. 8 còn dùng ở bài 2.4 với đúng câu "Thượng thiện nhược thuỷ" |
| 3 | Câu dẫn thuế 500 tr / 1 tỷ | Đã sửa | tai-chinh.md dẫn đúng NĐ 141/2026, 1 tỷ, ghi "chưa có toàn văn" |
| 4 | 1:1 review danh mục / chuyển pha chưa có trong việc cần luật sư | Đã sửa | Đã thêm ở 4.4 (mục 1) và 7.1 |
| 5 | Ngầm hiểu 3 chu kỳ | Đã sửa | Bài 2.5, mục lục và hình 5 đều để [chờ anh] |
| 6 | Câu "chuyển đổi" mơ hồ ở TC 5b | Đã sửa | Ghi rõ "thành viên miễn phí mới → khoá 100 USD" kèm huỷ ≤ 12% |
| 7 | Lớp dẫn dắt lặp ngày liền | Đã sửa | Lịch mới: ĐẠO – ĐẦU TƯ – ĐẠO – ĐỜI – ĐẠO – ĐẦU TƯ – ĐỜI, không lặp ngày liền, kể cả Chủ Nhật → Thứ Hai. Tỷ lệ vẫn 3/2/2 |
| 8 | KPI tháng 2 nội suy | Đã sửa | Ghi "tháng 2 nội suy" |
| 9 | Phép tính 75 giờ 1:1 chỉ tính buổi hằng năm | **Còn** (Gợi ý) | Mục 3.4 giữ nguyên. Không chặn: đã ghi rõ giả định, và với 15 người mua thì sức anh vẫn đủ |
| 10 | Bài ghim "có sẵn" | Đã sửa | Ghi "KENH lên kế hoạch ghim sau tuần 2, chưa có sẵn", trước đó dùng bình luận ghim |
| 11 | Thiếu chữ "tắc" trong Luận Ngữ 13.17 | Đã sửa | |
| 12 | "Âm – dương" ở bài 2.2 | Đã sửa | Cột ĐẠO của bài 2.2 đổi thành [chờ anh] |
| 13 | Câu "không thể lỗ nặng" | Đã sửa | Đổi thành "lỗ xấu nhất 93,6 tr, chưa tính công anh"; khớp JSON |
| 14 | Phí chuyển tiền âm | Đã sửa | `max(0.0, …)`; giá trị nhỏ nhất của `cp_chuyen_tien` = 0 |
| 15 | nghien-cuu: khoảng hở 899/900 USD, NĐ 141 viết chắc | **Còn** (Gợi ý) | Lần này Lan không được giao sửa. Không ảnh hưởng số |

## Lỗi mới do sửa
| # | Mức | Vị trí | Vấn đề | Cách sửa |
|---|---|---|---|---|
| 16 | Gợi ý | ke-hoach.md mục 7.5, câu đầu "thận trọng (mức sàn) / cơ sở" | Tóm tắt và 7.4 nay định nghĩa "sàn" là 55 thành viên / 1 học viên, còn 72 là số của kịch bản thận trọng. Gọi cả cột thận trọng là "mức sàn" dễ làm nhầm 72 với sàn | Đổi thành "thận trọng / cơ sở (tham vọng); sàn và ngưỡng xem 7.4" |
| 17 | Gợi ý | ke-hoach.md mục 3.4, đoạn "Tận dụng văn phòng và ngân hàng hỗ trợ" (mới) | Nội dung hợp brief: không bịa tên đối tác, chỉ nêu tên ngân hàng khi có văn bản. Riêng ý mời chuyên gia ngân hàng nói trong live nên ghi thêm: không giới thiệu sản phẩm đầu tư hay crypto | Thêm 1 vế: "chỉ nói quản lý tài chính cá nhân, không giới thiệu sản phẩm đầu tư/crypto" |

Rà lại các điểm tuân thủ sau khi sửa: không thêm tên sàn; không thêm câu hứa lợi nhuận; giá anh chốt giữ nguyên ở cả 4 file; không có số từ ban-nhap-cu/; dữ kiện kênh vẫn khớp KENH.md và brand.md; chính tả ổn.

## Tóm tắt số lỗi lần 2
- Chặn: 0
- Nên sửa: 0
- Gợi ý: 4 (#9, #15 còn từ lần 1; #16, #17 mới)
