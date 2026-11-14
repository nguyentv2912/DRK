# Giám sát — Hùng (tai-chinh) · Vòng 1

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày chấm: 14/11/2026 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File nộp: `mo_hinh.py`, `tai-chinh.md`, `tai-chinh.json`. Nhiệm vụ: (A) mô hình tài chính chương trình, (B) kế hoạch tài chính phòng ban, (C) 3 kịch bản và độ nhạy ±20%.

## Bảo đã tự kiểm chứng những gì
- **Chạy lại script trong bản sao** ở thư mục tạm (không đụng file nộp): `python3 mo_hinh.py` trả rc=0. JSON sinh ra **giống hệt** `tai-chinh.json` đã nộp (`a==b → True`).
- **So số in ra với tai-chinh.md:** vốn ban đầu 296, vốn lưu động 1.772, dự phòng 835, tổng vốn 2.903, đáy −2.068 (T18), hoà vốn vận hành T19, hoàn vốn T44, luỹ kế T24 −1.813, NPV −233, IRR 9%. Năm 1/2/3: DT 2.684/7.320/9.166, EBITDA −1.305/−20/1.124. Hoà vốn phòng ban 166,8/332,6/470,3 trđ → 15,8/31,6/44,7 khách. Cả 3 kịch bản, phương án lùi mốc tuyển, 12 dòng độ nhạy và 3 ngưỡng (+17%, −28%, +31%) đều khớp. Thu nhập tư vấn viên 14,9/16,1/17,7 cũng khớp.
- **Số không in ra mà Bảo tự tính lại từ hàm `chay()`:** bảng theo năm mục 6 (lead 11.342/26.250, khách 503/171/64 và 1.260/451/252, doanh thu từng dòng, năm 4 DT 9.465, EBITDA 1.397, dòng tiền 1.158, luỹ kế +468): khớp hết. Thận trọng DT 1.074/2.861, EBITDA −2.708/−3.896, lỗ T6 −1.299: khớp. Lạc quan DT 4.936/13.669, EBITDA +279/+4.745: khớp. Mốc dừng 1,0 tỷ (cơ sở, T6 −1.001) và 1,3 tỷ (thận trọng): khớp.
- **Tự tính lại số quan trọng:**
  - Tổng vốn = 2.068 (đáy) + 835 (dự phòng) = 2.903. Dự phòng = 2 × (381,5 + 36 CP khác của Mở rộng) = 835. Đúng.
  - Hoà vốn phòng ban Khởi động: 131,2 lương+BH + 18 CP khác + 8×30%/12×8 = 1,6 tuyển thay thế + 4×4 = 16 hội thảo = 166,8; chia cho 10,53 trđ đóng góp/khách đồng hành = 15,8 khách. Đúng.
  - NPV tính độc lập từ dòng tiền 48 tháng, chiết khấu 15%/năm quy về tháng, ra −233,2. Đúng. IRR 9% < 15% nhất quán với NPV âm.
  - Hoàn vốn: luỹ kế T43 = −19,1, T44 = +77,0, nên là T44. Hoà vốn vận hành: EBITDA T18 = −13,0, T19 = +6,9. Đúng.
  - Ngưỡng +17%: tham dự → đồng hành = 8%×25%×1,17 + 12%×1,17×20%×1,17 = 5,63% (md ghi khoảng 5,6%). CPL 60k×0,72 = 43k. Giá 12×1,31 = 15,7. Đúng.
- **Lương so với nghien-cuu.md (bản vòng 2):** Trợ giảng 11 (NC 10,9), CSKH 9 (NC 8–10), Content 13 (NC 12–15), Video editor 12 (NC ~12), Trưởng nhóm 20 (NC 20–40) đều khớp. **Lệch nguồn:** NC vòng 2 đã có số cho Coach (giảng viên HCM TB 21,9, khoảng 15–30; huấn luyện viên TB 19,0, dòng 121–122) và Quản lý vận hành (trưởng phòng vận hành 13–30, mốc ~21,7, dòng 126). Nhưng Hùng vẫn ghi "NC chưa tìm được" (mo_hinh.py dòng 93; md dòng 85) và tham chiếu Coach bằng "CV phân tích TC 18" (md dòng 87). Câu mở đầu md dòng 6 còn nói lương QLVH và Coach "đều là giả định". Tư vấn viên ghi "NC: 7–12" (md dòng 90), trong khi NC dòng 114 ghi SVFC 7–20, AIA 8–24, Chubb 12–30. Bản thân các mức 25, 20 và 9 vẫn nằm trong khoảng NC, nên kết quả không đổi. Lỗi nằm ở phần dẫn nguồn.

## Bảng chấm

| # | Tiêu chí (trọng số, Chặn) | % | Bằng chứng |
|---|---|---|---|
| 1 | Script chạy được và tái tạo đúng các số trong báo cáo (25, Chặn) | 95 | rc=0. JSON tái tạo giống hệt bản nộp. Mọi số trong md đều khớp output hoặc khớp kết quả `chay()`. Bị trừ nhẹ vì vài số trong md (bảng năm mục 6, số liệu năm của các kịch bản) không do script in ra, phải tự tính mới đối chiếu được. Ngoài ra luỹ kế T23 ghi −1.887, còn JSON là −1.886,5 (chỉ khác ở làm tròn) |
| 2 | Đủ chỉ số: vốn, hoà vốn, hoàn vốn, NPV, IRR, dòng tiền (20, Chặn) | 95 | Có đủ vốn (chi tiết + lưu động + dự phòng), hoà vốn vận hành, hoàn vốn, NPV 48t, IRR, dòng tiền tháng/năm/luỹ kế. Phần phòng ban có đủ: nhân sự 3 giai đoạn, lương + BH, chi phí cố định, doanh số cần, hoà vốn phòng ban. Bị trừ vì bảng mục 6 để trống các dòng chi tiết của năm 3–4 |
| 3 | Phép tính hợp lý: đơn vị, dấu, biên lợi nhuận, không lỗi (15, Chặn) | 88 | Đơn vị trđ nhất quán, dấu đúng, các số tự tính đều khớp. Có kiểm tra công suất coach và lead/tư vấn viên. Bị trừ vì: (a) 167 lead của T1 (đã tốn 10 trđ quảng cáo) không được tính chuyển đổi và cũng không chuyển sang T2; (b) bảng kinh tế đơn vị (md dòng 152) ghi chi phí biến đổi "gồm hoàn tiền", nhưng hoàn tiền đã trừ vào doanh thu (script dòng 385), nên nhãn sai; (c) thuế TNDN tính trên EBITDA, chưa trừ khấu hao thiết bị (ảnh hưởng nhỏ, theo hướng thận trọng) |
| 4 | Bảng giả định có nguồn hoặc ghi 'giả định' (15) | 80 | Có bảng giả định đầy đủ với cột nguồn và độ tin cậy, mỗi dòng đều ghi NC hoặc "giả định". Bị trừ vì nguồn lương Coach và QLVH dùng bản NC cũ ("NC chưa tìm được") dù NC vòng 2 đã có 2–3 nguồn mỗi vị trí. Khoảng lương tư vấn viên "7–12" cũng không đúng với NC |
| 5 | Độ nhạy ±20% và 3 kịch bản (15) | 95 | Có 3 kịch bản ghi rõ hệ số. Độ nhạy chạy 6 biến × ±20% trên 5 chỉ số, có xếp hạng mức ảnh hưởng, có tính ngưỡng hoàn vốn 24 tháng và phương án lùi mốc tuyển. Bị trừ nhẹ vì ô "Vốn cần chuẩn bị" của kịch bản Thận trọng ghi "không giới hạn" thay vì ghi con số 15.392 mà script tính (cho 48 tháng) |
| 6 | Nhận định thẳng thắn, nói rõ khi không khả thi (10) | 100 | Mục 1 nói rõ "Kịch bản cơ sở chưa đạt": NPV âm, IRR dưới suất chiết khấu, đội 24 người quá lớn, Thận trọng "không bao giờ tự hoà vốn", doanh thu ngân hàng không đáng kể. Có cổng chuyển giai đoạn, mốc dừng ở T6 kèm mức lỗ tối đa, và nêu chi phí ẩn (lương chủ dự án, KPCĐ, VAT) |

**Điểm:** 25×0,95 + 20×0,95 + 15×0,88 + 15×0,80 + 15×0,95 + 10×1,00 = 23,75 + 19 + 13,2 + 12 + 14,25 + 10 = **92,2 → 92/100**

Các tiêu chí Chặn: 95 / 95 / 88, đều ≥ 60.

## Kết luận: **ĐẠT** (92/100)

## Phản hồi (theo mức quan trọng, không bắt buộc sửa trước khi chuyển Mai)
1. Nguồn lương Coach và Quản lý vận hành dùng bản nghiên cứu cũ → cập nhật cột nguồn theo nghien-cuu.md vòng 2: Coach có giảng viên HCM TB 21,9 (15–30) và HLV TB 19,0; QLVH có trưởng phòng vận hành 13–30, mốc ~21,7. Sửa ở mo_hinh.py dòng 93–94, md dòng 85, 87 và câu "đều là giả định" ở md dòng 6.
2. Khoảng lương tư vấn viên "NC: 7–12" không đúng với nguồn → đổi thành "NC: SVFC 7–20, AIA lương hỗ trợ 8–24, Chubb 12–30 (gồm hoa hồng)".
3. Bảng kinh tế đơn vị ghi chi phí biến đổi "gồm hoàn tiền" → bỏ chữ "hoàn tiền" (vì đã trừ vào doanh thu), hoặc ghi "doanh thu sau hoàn tiền".
4. Lead T1 mất trắng (167 lead, 10 trđ) → hoặc chuyển số lead này sang T2, hoặc ghi rõ trong bảng giả định rằng T1 là tháng chuẩn bị và quảng cáo T1 là chi phí thử nghiệm, không tạo khách.
5. Bảng năm mục 6 và số liệu năm của các kịch bản không do script in ra → cho script in luôn các dòng này và điền nốt năm 3–4. Ô vốn Thận trọng nên ghi "15.392 trđ nếu chạy hết 48 tháng không dừng".
