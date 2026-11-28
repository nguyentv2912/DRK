# Kiểm định LẦN 2 — 2026-11-14-khung-chuong-trinh-chuyen-doi

Người kiểm: Hà – Kiểm định · Ngày 14/11/2026 (lần 2)
Hồ sơ đã đọc: `brief.md`, `phieu-giao-viec.md`, `kiem-dinh.md` lần 1, `mo_hinh.py`, `tai-chinh.md`, `tai-chinh.json`, `ke-hoach.md` (vòng 2), `giam-sat/*.md`.
Hà không sửa file của người khác. `mo_hinh.py` được chạy trên **bản sao trong thư mục tạm** (scratchpad), không ghi đè `tai-chinh.json` đã nộp.

## Kết luận: **ĐẠT**
Không còn lỗi mức Chặn. Còn **2 lỗi Nên sửa** và **5 Gợi ý**. Cả hai lỗi Nên sửa đều không làm sai hướng quyết định. Lỗi #1 làm kết quả **thận trọng hơn** thực tế khoảng 2 tháng hoàn vốn.

---

## 1. Hai lỗi Chặn lần 1: đã hết

| Lỗi lần 1 | Trạng thái | Hà kiểm chứng |
|---|---|---|
| #1 Ngưỡng hoà vốn phòng ban chưa tính công suất coach (`hoa_von_phong_ban()`) | **Đã sửa** | Hà tự tính lặp bằng Python, độc lập với script: số cặp coach = ceil(3 × khách/tháng ÷ 40); chi phí 1 cặp = (20 + 11) × 1,215 + 0,4 tuyển thay thế = 38,1 trđ. Kết quả: Khởi động 204,9 trđ → **19,46 khách** (+1 cặp, 10 người, doanh số 312,8–312,9); Tăng trưởng 370,7 → **35,2** (+1 cặp, 19 người, 566,0); Mở rộng 483,9 → **45,95** (đủ 4 cặp, 25 người, 738,9). Khớp `tai-chinh.json` → `hoa_von_phong_ban` và bảng mục 5 của tai-chinh.md. Mở rộng đổi từ 44,7 lên 45,9 vì đã thêm trợ giảng thứ 4 (lỗi #9 lần 1). Con số 19,4 ở lần 1 là do Hà làm tròn xuống; 19,5 là đúng |
| #2 Cổng 3 / KPI / sơ đồ trong ke-hoach.md dùng ngưỡng 15,8 | **Đã sửa** | Không còn "15,8 / 31,6 / 44,7 / 2.903 / 296 / T44" ở ke-hoach.md (chỉ còn số 15,8 = khách nền tảng T2, đúng). §1, §6 (bảng 6.1, sơ đồ, quy tắc công suất), §6.5, §7.1 (mốc công suất "vượt 13,3 khách → thêm cặp", cổng tuyển 28 / 37 = 80% của 35,2 / 45,9) và Gợi ý hình 2, 4, 5 đều dùng số mới |

**Lộ trình theo cổng (khuyến nghị)** — Hà kiểm chứng:
- Bản sao `mo_hinh.py` chạy thành công. JSON sinh ra **giống hệt** `tai-chinh.json` đã nộp.
- Hà tính lại độc lập từ dòng tiền theo tháng: NPV 48 tháng @15%/năm = **+1.677,2**; luỹ kế T24 = **−78**, T25 = −16, T26 = **+83** → hoàn vốn **T26**; đáy **−1.017 ở T7**. Đúng.
- Quỹ dự phòng = 2 × chi phí cố định thực tại T7 (đội 11 người): 131,2 + 37,7 (cặp coach) + 10,9 (tư vấn viên thứ 3) + 18 = 197,8 × 2 = **396**. Tổng vốn 306 + 711 + 396 = **1.413**. Đúng.
- Logic cổng: T5 đạt 14,03 khách/1.000 lead → quảng cáo 70 từ T6. T13 = 28,5 và T14 = 29,2 (≥ 28,2) → Tăng trưởng từ T15. T16 = 39,4 và T17 = 40,0 (≥ 36,8) → Mở rộng từ T18. Đội 9 / 11 / 13 người ở T6 / T7 / T12 khớp công suất (T7: 47,7 học viên đang học > 40; T12: 81,5 > 80; T6: 1.371 lead > 1.200). Đúng.
- Nhãn độ nhạy: chuyển đổi −5% → hoàn vốn **T31**, −10% → **T41** (NPV +21), −20% → không hoàn vốn. Khớp output script, tai-chinh.md mục 1 và 8A, ke-hoach.md §1.

## 2. Số trong ke-hoach.md so với tai-chinh.json bản mới: **khớp**

Đã đối chiếu: vốn 1.413 (306 + 711 + 396); đáy −1.017 (T7); EBITDA dương từ T7, liên tục từ T19; hoàn vốn T26; luỹ kế T24 −78; NPV +1.677; IRR ~79%; đội 9/13/25; tuyển theo lịch 3.008 / T20 / T48 / −514 / −1.965; Lạc quan 1.004 / T10 / +6.627 / +15.297; Thận trọng dừng T6, lỗ ~1.440 (−1.309 + 131); tham chiếu "giữ đội 8" 1.519 / T29; doanh thu và EBITDA năm 1–2 của cả 4 cột; ngưỡng 19,5 / 35,2 / 45,9; chi phí cố định 204,9 / 370,6 / 483,9; doanh số 312,9 / 565,9 / 738,9; ngân sách quảng cáo cần 54–66 / 73–85 / 108–120 trđ; 12,4 khách ở 30 trđ; bảng §7.3 và §15 (lead, tham dự, nền tảng, đồng hành, doanh thu, EBITDA, luỹ kế T1–T12) khớp `khuyen_nghi.theo_thang_24t`. Phép tính phụ của Mai đúng: CPL bình quân T2 = 30 ÷ 550 = 54.545 đ, T6 = 70 ÷ 1.371 = 51.058 đ; lead tự nhiên T3 = 50 + 850/22 = 88,6; số bài trong lịch 30 ngày (10 video ngắn, 3 video dài + 1 live, 10 bài Facebook, 4 bài nhóm, 3 quà học, 5 tin Zalo; Nhận biết + Quan tâm = 12 + 9 = 21/30 ngày). Lệch duy nhất là làm tròn luỹ kế T8 (xem Gợi ý #4).

## 3. Các lỗi Nên sửa / Gợi ý lần 1

| Lỗi lần 1 | Trạng thái |
|---|---|
| #3 "gần với kịch bản Lạc quan" | **Đã sửa.** Câu "2,4 lần" đã bỏ. §1 nói rõ 30 trđ quảng cáo chỉ ra ~12,4 khách, cần 54–66 trđ cho 19,5 khách; cổng quảng cáo chuyển sang đo bằng tỷ lệ |
| #4 Lộ trình khuyến nghị chưa mô hình hoá | **Đã sửa.** `CONG` trong `mo_hinh.py`, tai-chinh.md mục 7A, khoá `khuyen_nghi` và `lo_trinh_theo_cong` trong JSON. Có cả phương án tham chiếu "giữ đội 8" (T13 / T29 / −490; chênh với số thử của Hà lần 1 đã được giải thích đúng: +10 trđ lệ phí và thêm tư vấn viên) |
| #5 Tuần 0 | **Đã sửa.** "Tháng 0 = tuần 0"; thêm dòng lệ phí pháp nhân + nhãn hiệu 10 trđ (ghi "cần báo giá"); 30 trđ luật sư ghi "chưa có báo giá"; ghi 15–30 trđ nếu quản lý vận hành vào sớm; Cổng 0 "chỉ ký hợp đồng lao động sau ý kiến luật sư" (đồng thời xử lý Gợi ý #10) |
| #6 Mr Pips | **Đã sửa.** §1, §8, §9, §12 ngày 22, §13 đều dùng "bị cáo buộc", "đang xét xử", bắt buộc luật sư duyệt. Bài ngày 10 đổi sang dấu hiệu chung theo cảnh báo của Bộ Công an, không nêu tên vụ |
| #7 Thiếu phiếu chấm Mai | **Đã có** `giam-sat/chien-luoc-vong1.md` (ĐẠT 86/100). Lưu ý ở Gợi ý #5 |
| #9 Cặp coach – trợ giảng | **Đã sửa.** Mở rộng 4 coach + 4 trợ giảng; ghi rõ "cặp 1:1" ở tai-chinh.md mục 3, 5 và ke-hoach.md §6.1 |
| #11 "người nổi tiếng của kênh" | **Đã sửa.** §5.2 câu 7 viết trung tính |

## 4. Không lẫn dự án: **đạt**
Không tìm thấy số liệu, thương hiệu hay kênh nào từ `fanpage/`, `ong-rung/`, `kaggle/` hay kênh Đạo Đức Đầu Tư trong ke-hoach.md, tai-chinh.md, mo_hinh.py, tai-chinh.json.

## 5. Đủ yêu cầu của brief: **đạt**
Khung phễu 6 tầng (§3.2), nội dung từng bước (§3.3–3.5), gói và giá (§3.1), uy tín với ngân hàng và văn phòng (§4), pháp lý (§5), mô hình tài chính sơ bộ (§1 + tai-chinh.md), lộ trình và KPI (§6.5, §7, §15). Yêu cầu bổ sung: kế hoạch tài chính phòng ban (tai-chinh.md mục 5: nhân sự theo giai đoạn, lương thị trường có nguồn, chi phí, doanh số và lead cần, hoà vốn có công suất) và chiến lược + kế hoạch nội dung (§9–15: định vị, giọng điệu, trụ cột, kênh, nội dung theo tầng phễu, lịch 30 ngày, đội và quy trình, tuân thủ, KPI). Không có câu hứa lợi nhuận; mọi điều khoản luật đều gắn "cần luật sư xác nhận".

---

## 6. Bảng lỗi lần 2

| # | Mức | Vị trí (file, mục) | Vấn đề | Cách sửa |
|---|---|---|---|---|
| 1 | Nên sửa | `mo_hinh.py` hàm `chay()` dòng 322–324 (`moi = max(0, so_nguoi(gd_ten) - so_nguoi(gd_truoc))`) | Lúc chuyển giai đoạn, số người mới được tính theo đội **kế hoạch** cũ (8, 17), không trừ các cặp coach và tư vấn viên đã tự thêm. Ở T15, đội thực tế 13 → 19 (cần 6 người) nhưng mô hình tính tuyển 9; ở T18, 19 → 25 (cần 6) nhưng tính 8. Mô hình vì thế thừa ~5 lượt tuyển (8 trđ/lượt) và 5 máy (12 trđ/máy), tức khoảng 100 trđ. Hà sửa thử trên bản sao: vốn vẫn 1.413, nhưng hoàn vốn **T24** (thay vì T26), luỹ kế T24 **+51** (thay vì −78), NPV +1.785. Lỗi này làm số **thận trọng hơn**, không làm sai quyết định | Hùng: trừ `2 × them_truoc + them_tvv_truoc` khỏi `so_nguoi(gd_truoc)` khi tính `moi`, rồi chạy lại và cập nhật số ở tai-chinh.md, JSON, ke-hoach.md. Nếu không kịp, chỉ cần thêm một câu: "chi phí tuyển lúc chuyển giai đoạn đang tính dư ~100 trđ, nên hoàn vốn T26 là số thận trọng" |
| 2 | Nên sửa | `ke-hoach.md` §10, câu "Phân bổ quảng cáo đề xuất… trong tổng ngân sách TC 10 / 30 / 60 / 100 trđ/tháng" | Đây là ngân sách của phương án **tuyển theo lịch**. Lộ trình khuyến nghị dùng 10 (T1) / 30 / 70 (sau cổng) / 100 (Tăng trưởng) / 130 (Mở rộng) | Mai: đổi thành "10 / 30 → 70 / 100 / 130 trđ/tháng (lộ trình theo cổng, TC 7A)" |
| 3 | Gợi ý | `ke-hoach.md` §7.3, đoạn "Nguồn:" | Câu "các cột lead, tham dự, nền tảng, doanh thu và EBITDA **chưa có trong JSON**… đề nghị Hùng xuất thêm" đã lỗi thời: JSON bản mới đã có các cột này ở `khuyen_nghi.theo_thang_24t` (Hà đã đối chiếu, khớp). Tương tự ở §15 | Đổi nguồn thành `tai-chinh.json` → `khuyen_nghi.theo_thang_24t`, bỏ câu đề nghị |
| 4 | Gợi ý | `tai-chinh.md` mục 7A (luỹ kế theo tháng) và `ke-hoach.md` §7.3 dòng T8 | Luỹ kế T8 = −966,5: tai-chinh.md ghi −966, ke-hoach.md ghi −967 | Thống nhất một cách làm tròn |
| 5 | Gợi ý | Thư mục `giam-sat/` | Phiếu chấm mới nhất là `tai-chinh-vong2.md` (10:26) và `chien-luoc-vong1.md` (10:15). Bản vòng 2 của Mai (14:04) và bản sửa cuối của Hùng (14:05) chưa có phiếu chấm riêng | Trưởng nhóm: nếu quy trình yêu cầu, cho Bảo chấm nhanh vòng 2 trước khi bàn giao |
| 6 | Gợi ý | `tai-chinh.md` mục 5 (sau bảng hoà vốn) và mục 7A (sau bảng 4 năm) | Hai câu nhắc "Hà tính ra…", "Hà đã chạy thử…" là ghi chú nội bộ giữa các vòng kiểm định, không cần trong bản giao chủ dự án | Bỏ hoặc chuyển thành chú thích "đối chiếu kiểm định" |
| 7 | Gợi ý | `nghien-cuu.md`; khung độ tin cậy ở đầu tai-chinh.md và ke-hoach.md (giữ từ Gợi ý #8 lần 1) | Nghiên cứu vẫn ở mức "chưa đạt do môi trường". Mọi số thị trường, pháp lý tối đa độ tin cậy TB | Khi bàn giao giữ nguyên cảnh báo; luật sư đối chiếu toàn văn trước khi dùng với khách |

**Tổng lần 2: Chặn 0 · Nên sửa 2 · Gợi ý 5.**

---

## Phụ lục — Tóm tắt kiểm định lần 1 (14/11/2026)

Kết luận lần 1: **CHƯA ĐẠT** (Chặn 2 · Nên sửa 5 · Gợi ý 4).
- Chặn #1: `hoa_von_phong_ban()` không tính cặp coach thêm khi vượt 40 học viên/cặp. Ngưỡng 15,8 / 31,6 phải là ~19,5 (10 người) / 35,2 (19 người).
- Chặn #2: ke-hoach.md dùng ngưỡng 15,8 ở Cổng 3, KPI, sơ đồ, gợi ý hình.
- Nên sửa: #3 so sánh "gần Lạc quan" sai; #4 lộ trình khuyến nghị chưa mô hình hoá; #5 chi phí tuần 0 chưa rõ; #6 Mr Pips cần "bị cáo buộc"; #7 thiếu phiếu chấm Mai.
- Gợi ý: #8 độ tin cậy nghiên cứu; #9 Mở rộng 4 coach / 3 trợ giảng; #10 ký hợp đồng lao động sau Cổng 0; #11 "người nổi tiếng của kênh".
- Lần 1 xác nhận đúng: tổng vốn 2.903 (phương án tuyển theo lịch, bản cũ), NPV −233, lương + BH 131,2, lead tự nhiên, CPL bình quân, nguồn số thị trường có link trong nghien-cuu.md, không lẫn dự án.
