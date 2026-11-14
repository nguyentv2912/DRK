# Giám sát — Hùng (tai-chinh) — Vòng 2

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người chấm: Bảo – Giám sát · Ngày 14/11/2026 · Phiên bản prompt: 1.0
Lý do vòng 2: kiem-dinh.md lỗi Chặn #1 (hoà vốn chưa tính công suất coach), Nên sửa #4, #5, Gợi ý #9; giam-sat/chien-luoc-vong1.md phản hồi 1 (cổng 25 khách với ngân sách 30 trđ).
File nộp: `mo_hinh.py`, `tai-chinh.md`, `tai-chinh.json`.

## Kiểm chứng đã làm
- Chạy `mo_hinh.py` trên **bản sao** trong scratchpad (không đụng file nộp): rc=0. `tai-chinh.json` sinh ra **giống hệt từng byte** bản đã nộp (`cmp` không khác).
- So số output với tai-chinh.md: vốn ban đầu 306; tổng vốn theo cổng 1.316 / theo lịch 3.008 / lạc quan 1.004 và 1.485; đáy −1.017 (T7); HV T19, hoàn vốn T26, luỹ kế T24 −78, NPV +1.677, IRR 79%; mốc mở QC/lên TT/lên MR T6/T15/T18; đội 9/13/25; DT năm 1/2 3.104/8.546; dòng tiền năm 3/4 1.312/1.616 (tự tính từ rows); giữ đội 8: 1.444, T13/T29/−490, NPV 1.060; Thận trọng dừng T6: 4,7 khách, lỗ 1.440; ngân sách QC cần 66,3/54,1 – 85,2/73,0 – 120/107,7; 12,4 khách ở 30 trđ; toàn bộ bảng độ nhạy, 3 kịch bản theo lịch, lùi mốc tuyển. **Tất cả khớp.**
- Tự tính lại hoà vốn Khởi động có công suất: CP cố định gốc 131,2 + 18 + 8×0,3/12×8 + 4×4 = 166,8; cặp coach+TG = 31×1,215 + 2×0,3/12×8 = 38,1 → (166,8 + 38,1)/10,53 = **19,46** khách, cần ceil(3×19,46/40) = 2 cặp (ổn định với +1 cặp). Doanh số 19,46×16,08 = 312,9. Khớp script.
- Đối chiếu số Hà: (a) 19,4 so với 19,46 → chỉ là làm tròn, doanh số 312,9 trùng. (b) Mở rộng 44,7 → 45,9: do sửa 3→4 trợ giảng (+11×1,215 = 13,4 trđ ÷ 10,53 ≈ +1,27 khách). Hợp lý. (c) Giữ đội 8: Bảo chạy lại trên bản sao, bỏ 10 trđ lệ phí → T13/T29/−480; bỏ thêm cơ chế tự thêm tư vấn viên → **T13/T28/−395, trùng đúng số Hà**. Giải thích chênh lệch của Hùng đúng và được kiểm chứng.
- Đọc code `hoa_von_phong_ban()` (lặp tới khi số cặp ổn định) và `chay(cong=...)` (cổng QC theo tỷ lệ/1.000 lead có độ trễ, cổng tuyển 2 tháng ≥ 80% ngưỡng, tự thêm coach/TVV, chi phí tuyển khi chuyển giai đoạn). Logic đúng như mô tả trong md.
- Kiểm tra thêm (Bảo tự chạy, không có trong báo cáo): độ nhạy của **lộ trình theo cổng** — chuyển đổi ×0,8: vốn 2.003, HV T23, **không hoàn vốn**, NPV −1.256; ×0,95: hoàn vốn T31, NPV +976; CPL ×1,2: hoàn vốn T34, NPV +500; giá đồng hành ×0,8: không hoàn vốn, NPV −708. Tỷ lệ T5 = 14,03 khách/1.000 lead, chỉ vừa qua cổng 14,0.
- Quỹ dự phòng theo cổng = 2 × (131,2 + 18) = 298,4, tức đội 8 gốc; nhưng tại tháng đáy T7 đội thực tế là 11 người (+1 cặp coach, +1 TVV ≈ +48,6 trđ/tháng) → dự phòng thực ≈ 396, tổng vốn ≈ 1,41 tỷ thay vì 1,32.

## Năm việc được giao
| Việc | Kết quả |
|---|---|
| (1) Hoà vốn có công suất coach | Đã sửa, có lặp, bảng mục 5 có cột người thực tế ở ngưỡng, JSON thêm trường. 19,5/35,2/45,9 |
| (2) Mô hình hoá lộ trình theo cổng | Đã có `CONG`, 3 kịch bản + tham chiếu giữ đội 8, đủ vốn/HV/hoàn vốn/NPV/IRR/luỹ kế |
| (3) Ngân sách QC cần + cách đo cổng | Đã có bảng ngân sách và đề xuất: cổng QC đo tỷ lệ, cổng tuyển đo số khách tuyệt đối, mốc dừng |
| (4) Tuần 0, lệ phí, luật sư | "Tháng 0 = tuần 0", dòng lệ phí 10 trđ (GĐ, cần báo giá), luật sư 30 trđ chưa có báo giá, lương tuần 0 15–30 trđ ghi chú |
| (5) Cặp coach–TG Mở rộng | 4/4, có ghi chú tác động |

## Bảng chấm
| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | Script chạy được và tái tạo đúng các số trong báo cáo (Chặn) | 25 | 95 | rc=0, JSON trùng byte; mọi số kiểm ở trên khớp md. Trừ nhẹ: dòng tiền năm 3/4 của lộ trình theo cổng không in ra console, phải tự tính từ rows |
| 2 | Đủ chỉ số: vốn, hoà vốn, hoàn vốn, NPV, IRR, dòng tiền (Chặn) | 20 | 95 | Lộ trình theo cổng có đủ vốn, đáy, HV, hoàn vốn, NPV, IRR, luỹ kế T1–T24, dòng tiền năm; theo lịch giữ đủ như vòng 1. Trừ: chưa có bảng dòng tiền theo năm đầy đủ (4 năm, các dòng chi phí) cho phương án khuyến nghị như mục 6 |
| 3 | Phép tính hợp lý: đơn vị, dấu, biên lợi nhuận, không lỗi (Chặn) | 15 | 85 | Hoà vốn có công suất tự tính lại khớp (19,46); số Hà tái tạo được chính xác. Lỗi: quỹ dự phòng lộ trình theo cổng tính theo đội 8 gốc trong khi đội ở tháng đáy T7 là 11 người → thiếu ≈ 97 trđ (tổng vốn ≈ 1,41 thay vì 1,32 tỷ); md có ghi "tính theo đội Khởi động" nhưng trái với định nghĩa "chi phí cố định của đội tại tháng đáy" |
| 4 | Bảng giả định có nguồn hoặc ghi 'giả định' | 15 | 85 | Mọi giả định mới (cổng 14/1.000, 80% ngưỡng, QC 70/100/130, lệ phí 10, 1 tháng lương khi dừng, lương tuần 0) đều ghi GĐ. Lương coach/QLVH đã dùng NC vòng 2 (TB). Còn: coach vẫn chưa có số cho đúng chức danh (đã nói rõ) |
| 5 | Độ nhạy ±20% và 3 kịch bản | 15 | 75 | 3 kịch bản có cho cả hai lộ trình. Nhưng độ nhạy ±20% chỉ chạy cho phương án tuyển theo lịch (mục 8), **không có cho lộ trình khuyến nghị**. Bảo chạy thử: chuyển đổi −20% thì lộ trình theo cổng không hoàn vốn, NPV −1.256 — thông tin quyết định bị thiếu |
| 6 | Nhận định thẳng thắn, nói rõ khi không khả thi | 10 | 80 | Nói thẳng: theo lịch không đạt, 30 trđ không bao giờ hoà vốn, Thận trọng phải dừng lỗ 1,44 tỷ, ba khoản chưa tính. Trừ: câu "theo kịch bản cơ sở thì lộ trình này khả thi" chưa nói rằng chỉ cần chuyển đổi −5% là hoàn vốn lùi tới T31, −20% là không hoàn vốn, và cổng QC ở T6 mở nhờ tỷ lệ T5 = 14,03, sát ngưỡng 14,0 |

**Điểm = 25×0,95 + 20×0,95 + 15×0,85 + 15×0,85 + 15×0,75 + 10×0,80 = 23,75 + 19 + 12,75 + 12,75 + 11,25 + 8 = 87,5 → 88/100.**
Tiêu chí Chặn: 95 / 95 / 85, không tiêu chí nào dưới 60%.

## Kết luận: **ĐẠT** (88/100)
Lỗi Chặn của Hà đã được sửa đúng và kiểm chứng độc lập. Cả 5 việc được giao đều hoàn thành. Các điểm dưới đây là Nên sửa, không chặn bàn giao.

## Phản hồi (theo mức quan trọng)
1. Lộ trình khuyến nghị chưa có độ nhạy ±20% → chạy bảng độ nhạy (chuyển đổi, giá, CPL, ngân sách, lead tự nhiên, lương TVV) trên `chay(cong=CONG, ...)`, đưa vào mục 8 làm bảng chính; bảng theo lịch chuyển xuống làm tham chiếu.
2. Câu "lộ trình này khả thi" ở mục 1 ý 1 quá chắc → thêm ngay sau đó: chuyển đổi −5% thì hoàn vốn ~T31, −20% thì không hoàn vốn (vốn ~2,0 tỷ); cổng QC ở T6 mở nhờ tỷ lệ T5 = 14,03, sát ngưỡng 14,0 (số do script in ra).
3. Quỹ dự phòng lộ trình theo cổng tính theo đội 8 gốc → tính bằng chi phí cố định thực tế của tháng đáy (có cặp coach và TVV thêm, ≈ 197 trđ/tháng). Tổng vốn khuyến nghị sẽ lên khoảng 1,41 tỷ; cập nhật mục 1, 4, 7A và JSON.
4. Phương án khuyến nghị chưa có bảng theo năm đầy đủ → in "BẢNG THEO NĂM CHI TIẾT" cho lộ trình theo cổng (cơ sở), gồm dòng tiền năm 3/4, và đưa vào mục 7A.
5. Các khoá gốc của `tai-chinh.json` (tong_von_can_chuan_bi = 3.008, hoan_von_thang = 48…) vẫn là phương án theo lịch, dễ bị lấy nhầm khi vẽ biểu đồ → thêm khoá cấp cao `khuyen_nghi` trỏ tới số của lộ trình theo cổng, hoặc đổi tên các khoá cũ thành `..._theo_lich`.
