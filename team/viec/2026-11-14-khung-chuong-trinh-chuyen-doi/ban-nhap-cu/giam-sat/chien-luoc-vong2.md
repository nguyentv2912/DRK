# Giám sát — Mai (chien-luoc) · Vòng 2

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày chấm: 14/11/2026 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File nộp: `ke-hoach.md` (717 dòng, 12.818 từ; vòng 1 là 669 dòng, 11.291 từ). Đầu vào bản mới: `tai-chinh.md`, `tai-chinh.json` (các khoá `khuyen_nghi`, `lo_trinh_theo_cong`, `ngan_sach_qc_can`, `hoa_von_phong_ban`), `mo_hinh.py`. Đã đọc thêm: `giam-sat/chien-luoc-vong1.md`, `kiem-dinh.md`.

## Bảo đã tự kiểm chứng những gì
- **So số tự động** bằng script `so2.py` (lưu trong scratchpad). Script trích 1.344 số trong ke-hoach.md, rồi so với mọi giá trị trong tai-chinh.json, tai-chinh.md, nghien-cuu.md và brief.md (có xét làm tròn và đổi đơn vị). Có 8 dòng lệch. Rà tay cả 8: đều là CPL bình quân Mai tự tính (T2 30/550 = 54.545; T3 50.934; T4 47.847; T6 51.057; T8 48.343; T9 47.081; T12 43.668, khớp với số "~" đã ghi), cộng −967 là làm tròn của −966,5. **Không có số TC nào bị đổi.**
- **Các số chính, đối chiếu từng số:**
  - Vốn 1.413 (JSON `khuyen_nghi.tong_von` 1.412,9) = 306 + 711 + 396.
  - Đáy −1.017 ở T7. Hoà vốn vận hành T19, EBITDA dương từ T7. Hoàn vốn T26. Luỹ kế T24 −78. NPV +1.677, IRR 79%.
  - Đội 9/13/25 (`so_nguoi_24t`). Lạc quan 1.004/T10, đội 13/29/32. Thận trọng dừng T6, 4,7 khách, lỗ ~1.440.
  - Tuyển theo lịch: 3.008 / T20 / T48 / −514, doanh thu năm 1/2 là 2.684/7.320, EBITDA −1.305/−150, luỹ kế T24 −1.965 (`kich_ban.Cơ sở`).
  - Tham chiếu "giữ đội 8": 1.519 / T29 (TC mục 7B).
- **Ngưỡng và cổng:**
  - Ngưỡng 19,5 / 35,2 / 45,9; đội 10/19/25; chi phí cố định 204,9 / 370,6 / 483,9; doanh số 312,9 / 565,9 / 738,9; công suất 13,3 / 26,7 / 53,3. Khớp `hoa_von_phong_ban`.
  - Lương + BH 131,2 / 272,2 / 394,9. Bảo tính lại từ lương từng vị trí × 1,215: 108 / 224 / 325 trđ ra đúng các số này.
  - Cổng quảng cáo ≥14/1.000 lead (14,03 ở T5); hạ ngân sách khi 2 tháng liền dưới 11,2 (mo_hinh.py dòng 198, 261). Cổng tuyển 28 (TC 28,2) và 37 (TC 36,8), khớp `nguong_cong_khach_thang`. Mốc dừng <8 khách và <14/1.000 lead, lỗ 1,0–1,44 tỷ (TC dòng 404).
  - Ngân sách quảng cáo cần 54–66 / 73–85 / 108–120 trđ, khớp `ngan_sach_qc_can`.
- **Độ nhạy:** −5% → T31 và CPL +20% → T34 đều khớp TC 8A. **Chưa có −10% → T41** (Hùng vừa thêm).
- **Bảng §7.3 T1–T12:** so cả 10 cột với `khuyen_nghi.theo_thang_24t`, khớp toàn bộ. Bảng §15 có tiếp cận, lead quảng cáo, lead tự nhiên, khách/1.000 lead; tính lại thấy đúng (ví dụ T5 9,3/666 = 14,0; T6 15,3/1.371 = 11,2).
- **Số cũ:** grep `2.903`, `T44`, `1.316`, `31,6`, `44,7`, `−233`, `−1.813` đều không còn. "15,8" chỉ còn là số khách nền tảng T2, không phải ngưỡng. "T19" là hoà vốn vận hành mới, đúng TC. Câu "2,4 lần… gần Lạc quan" và dải "16 – <25 đội 8 tự nuôi được" đã bỏ.
- **Đếm lịch 30 ngày lại:** Nhận biết 12 ngày + Quan tâm 9 ngày = 21/30, khớp câu đầu §11. Video ngắn 10, video dài 3 + 1 live, bài Facebook 10, bài nhóm 4, quà học 3, tin Zalo OA 5, khớp dòng 605. Có 14 rủi ro, trong đó 5 ở mức Cao trở lên, khớp câu đầu §8.
- **Số người theo bộ phận:** Mở rộng có 4 coach và 4 trợ giảng, khớp mo_hinh.py dòng 114 (Hùng đã sửa lỗi Gợi ý #9 của Hà). Cộng số người trong ba sơ đồ ra 8 / 17 / 25.

## Phản hồi vòng 1 và lỗi của Hà liên quan Mai

| Mục | Đã xử lý? | Bằng chứng |
|---|---|---|
| V1-1 Cổng 25 khách không đạt ở 30 trđ | Có | §1 ý 3 (12,4 khách; cần 54–66 / 73–85 trđ); §7.1 cổng quảng cáo đo bằng tỷ lệ, tăng 30 → 70 trđ |
| V1-2 "2,4 lần gần Lạc quan" | Có | Đã bỏ câu này; §1 ý 4 dùng số Lạc quan/Thận trọng theo cổng |
| V1-3 Mâu thuẫn hoà vốn đội 8 | Có | §6.1 bảng ngưỡng có công suất; §7.1 thêm "Mốc công suất 13,3" |
| V1-4 Câu đầu §2, §4, §7, §8, §11 | Có | Dòng 62, 192, 406, 466, 541 đều là kết luận có số |
| V1-5 Dài/lặp; cột người chịu trách nhiệm; nhãn luật sư | Một phần | Có cột người chịu trách nhiệm (§8). Có nhãn luật sư ở dòng 252, 258, 262, 648, 653, 654. Dòng 40 khai báo nguyên tắc "chỉ ghi một chỗ". **Nhưng tài liệu dài thêm 1.527 từ.** Bảng §7.3 và §15 vẫn lặp 4 cột (lead, tham dự, nền tảng, đồng hành) |
| Hà #2 (Chặn) Cổng 3, KPI, sơ đồ, hình | Có | Cả 6 vị trí đã dùng 19,5/35,2/45,9. Cổng tuyển 28/37 có ghi nguồn TC 28,2/36,8. Hình 2 và 5 đã cập nhật |
| Hà #3 Lạc quan | Có | Như V1-2 |
| Hà #4 Dùng số lộ trình theo cổng | Có | Toàn bộ số chính lấy từ `khuyen_nghi`; tuyển theo lịch chỉ để so sánh |
| Hà #5 Tuần 0 | Có | Dòng 430: ai làm (chủ dự án + luật sư), 306 trđ gồm 30 + 10 (cần báo giá), 15–30 trđ nếu QLVH vào sớm |
| Hà #6 Mr Pips | Có | Dùng "bị cáo buộc / đang xét xử" ở dòng 38, 466, 470, 595. Ngày 10 đã đổi chủ đề. Ngày 22 bắt buộc qua luật sư |
| Hà #10 Hợp đồng sau Cổng 0 | Có | Dòng 412 |
| Hà #11 "Người nổi tiếng của kênh" | Có | Dòng 276 viết trung tính |

## Bảng chấm

| # | Tiêu chí (trọng số, Chặn) | % | Bằng chứng |
|---|---|---|---|
| 1 | Đủ mọi phần người dùng yêu cầu (25, Chặn) | 100 | Mọi phần của vòng 1 vẫn còn. Phần thiếu ở vòng 1 nay đã có: bảng "Mô hình tài chính sơ bộ" gom một chỗ, 4 kịch bản (dòng 42–56), kèm vốn ban đầu ở tuần 0 và các chi phí chưa có trong mô hình |
| 2 | Số liệu khớp tai-chinh.md, không tự đổi (20, Chặn) | 90 | 1.344 số, không số TC nào bị đổi; số chính đều đúng bản mới. Trừ vì: (a) dòng 533 ghi ngân sách quảng cáo "10 / 30 / 60 / 100", đây là mức của phương án tuyển theo lịch, còn phương án chính là 10 / 30 / 70 / 100 / 130; (b) dòng 200 ghi hoa hồng ngân hàng "9–27 trđ/năm", lấy từ bảng tuyển theo lịch (TC dòng 233), còn lộ trình theo cổng là 10–33 (TC dòng 298); (c) chưa đưa −10% → T41, NPV ≈ +21 (số Hùng vừa thêm, cho thấy biên an toàn mỏng); (d) dòng 455 và 674 ghi "các cột này chưa có trong JSON", nay đã có ở `khuyen_nghi.theo_thang_24t` (số vẫn khớp) |
| 3 | Rủi ro, lộ trình, KPI cụ thể và đo được (20) | 92 | Cả 4 điểm trừ của vòng 1 đã sửa. Mọi cổng/mốc đều có ngưỡng số, thời điểm xét, hành động và kết quả theo cơ sở (§7.1). Rủi ro có cột người chịu trách nhiệm. Bảng T1–T12 dùng để so với số thật. Trừ nhẹ: câu đầu §7 ghi "1 cổng pháp lý, 1 cổng quảng cáo, 1 mốc dừng, 2 cổng tuyển", nhưng bảng có thêm Cổng 1 và Mốc công suất (7 dòng) |
| 4 | Câu đầu mỗi phần là kết luận có số (15) | 88 | 15/15 mục lớn có câu kết luận có số (đã sửa §2, §4, §7, §8, §11). Trừ vì nhiều mục con chưa có câu kết luận (3.1, 3.2, 4.1–4.3, 6.2–6.5, 7.1–7.3) |
| 5 | Đánh dấu điều cần xác minh (10) | 95 | Đã gắn "cần luật sư xác nhận" ngay tại Điều 15a, Điều 19, mức phạt 200 trđ (§5, §14). Có ghi "cần báo giá" cho lệ phí và luật sư, "TC ghi 28,2/36,8" cho số Mai làm tròn. Trừ nhẹ: §14 câu 3 và câu 5 vẫn nêu Luật 75/2025 mà không có nhãn tại chỗ |
| 6 | Ngắn gọn, bảng cho thứ so sánh được (10) | 65 | Bảng vẫn dùng tốt, có thêm nguyên tắc dẫn chiếu (dòng 40, 387). Nhưng phản hồi vòng 1 là phải rút gọn, vậy mà tài liệu tăng từ 11.291 lên 12.818 từ (+13,5%). §7.3 và §15 lặp 4 cột của cùng 12 tháng. §1 ý 4 còn lặp chi tiết cổng T6 của §7 |

**Điểm:** 25×1,00 + 20×0,90 + 20×0,92 + 15×0,88 + 10×0,95 + 10×0,65 = 25 + 18 + 18,4 + 13,2 + 9,5 + 6,5 = **90,6 → 91/100**

Tiêu chí Chặn: #1 = 100%, #2 = 90% (đều ≥ 60%).

## Kết luận: **ĐẠT** (91/100)

## Phản hồi còn lại (theo mức quan trọng)
1. Dòng 533 ghi ngân sách "10 / 30 / 60 / 100 trđ/tháng" theo phương án tuyển theo lịch → sửa thành mức của lộ trình theo cổng: 10 (T1) / 30 / 70 (sau cổng quảng cáo) / 100 (Tăng trưởng) / 130 (Mở rộng).
2. Dòng 200 ghi hoa hồng ngân hàng "9–27 trđ/năm" theo phương án tuyển theo lịch → đổi sang số của lộ trình theo cổng, 10–33 trđ/năm (TC dòng 298).
3. §1 ý 4 thiếu số độ nhạy Hùng vừa thêm → thêm "−10% thì hoàn vốn T41, NPV chỉ còn ~+21 trđ" cạnh dòng −5% → T31.
4. Dòng 455 và 674 ghi "chưa có trong JSON" → sửa nguồn thành `tai-chinh.json` → `khuyen_nghi.theo_thang_24t`, và bỏ đề nghị Hùng xuất thêm cột.
5. Tài liệu dài thêm 1.527 từ → gộp §15 vào §7.3, chỉ giữ ở §15 các cột riêng của nội dung (tiếp cận, lead quảng cáo/tự nhiên, CPL bình quân); bỏ câu cổng T6 ở §1 ý 4, chỉ để dẫn chiếu §7; sửa câu đầu §7 cho khớp số dòng của bảng cổng.
