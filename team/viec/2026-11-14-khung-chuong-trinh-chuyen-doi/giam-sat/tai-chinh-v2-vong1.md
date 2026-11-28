# Giám sát — Hùng (tai-chinh) · Phiên bản 2 · Vòng 1

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày: 2026-11-14 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File chấm: mo_hinh.py, tai-chinh.md, tai-chinh.json (bỏ qua ban-nhap-cu/)

## Kiểm chứng đã làm
- Sao lưu tai-chinh.md/.json, chạy lại `python3 mo_hinh.py` (rc=0) → **tai-chinh.md giống hệt từng byte; tai-chinh.json bằng nhau khi so dạng dict**.
- Giá không đổi: `gia_co_ban_usd 100.0`, `gia_chuyen_sau_usd 1000.0`, `gia_ebook_vnd 1_000_000` (khớp brief mục "Những gì đã chốt").
- Phí Skool khớp nghien-cuu.md dòng 23–25, 29–30: Hobby 9 USD + 10% + 0,30; Pro 99 USD + 2,9% + 0,30; > 900 USD là 3,9% + 0,30; điểm hoà Hobby–Pro ~1.268 USD; 1.000 USD → 960,7 USD.
- Tính tay: đóng góp 1 HV gói Pro (100 − 3,2) × 0,98 − 7 = 87,86 USD × 26.000 = 2,28 tr (khớp); Hobby 2,10 tr (khớp). Quỹ dự phòng 3 × (2,1 + 2,574 + 6,0) = 32,0 tr (khớp). Lương năm 1 = 22,5 + 18 + 21,87 + 8,5 + 1,43 = 72,3 tr (khớp).
- Người theo dõi T24: 10.000 + 2.000 × Σ1,05^k (k=0..23) = 99.004 (khớp). Kết luận 4 ghi rõ "đây là giả định, chưa có số thật của kênh".
- Thử thêm: hoà vốn với 1 HV **không** có bán kèm = **−0,23 tr/tháng**; có bán kèm chỉ +0,07 tr (dựa vào 0,013 người mua gói 1.000 USD mỗi tháng). Kịch bản cơ sở bỏ 10.000 người theo dõi sẵn có → 183 HV T24 (ít nhạy). Tỷ lệ vào Skool 2% thay vì 8% → 54 HV, lãi T24 135,6 tr.
- fanpage/KENH.md: kênh đang "Xây dựng lại", không có số người theo dõi, KPI ghi "đo mốc tuần đầu" → con số 10.000 người theo dõi sẵn có không có căn cứ.

## Bảng chấm

| # | Tiêu chí | Trọng số | Chặn | % | Bằng chứng |
|---|---|---|---|---|---|
| 1 | Script chạy được và tái tạo đúng các số trong báo cáo | 25 | Chặn | 95 | Chạy lại rc=0, md giống hệt từng byte, json bằng nhau; các phép tính tay ở trên đều khớp |
| 2 | Đủ chỉ số: vốn, hoà vốn, hoàn vốn, NPV, IRR, dòng tiền | 20 | Chặn | 95 | Vốn 78,0 tr (mục 2); hoà vốn và tháng hoàn vốn 6/4/3; NPV 627,3/4.413,6/18.528,0; IRR kèm ghi chú "không có ý nghĩa so sánh"; dòng tiền 24 tháng (mục 3) |
| 3 | Phép tính hợp lý: đơn vị, dấu, biên lợi nhuận, không lỗi | 15 | Chặn | 85 | Phí, đơn vị, dấu đều đúng. Trừ điểm: tiêu đề "Hoà vốn chỉ cần 1 học viên" dựa vào 0,013 người mua gói 1.000 USD/tháng, nếu chỉ có khoá cơ bản thì 1 HV lỗ 0,23 tr. Thuế 7% gồm 5% GTGT trong khi nghien-cuu.md dòng 36 nói Skool là merchant of record xử lý VAT, có thể tính trùng (đã ghi là thận trọng) |
| 4 | Bảng giả định có nguồn hoặc ghi 'giả định' | 15 | | 75 | Mọi tham số đều có nguồn hoặc ghi "giả định", tách riêng trong `P`/`KICH_BAN`. Nhưng lý do của giả định phễu yếu: 10.000 người theo dõi sẵn có không có căn cứ (KENH.md: kênh đang xây lại); "8% theo dõi mới → Skool, không rào cản" ngược với nghien-cuu.md (Skool không có giao diện tiếng Việt, phải tạo tài khoản ngoài); mức chuyển đổi 3% lấy từ SaaS giá thấp, trong khi 100 USD/tháng thuộc nhóm giá cao quốc tế và khoá crypto VN chỉ 59.000–2.500.000 đ một lần (nghien-cuu.md dòng 13) |
| 5 | Độ nhạy ±20% và 3 kịch bản | 15 | | 80 | Đủ 3 kịch bản, độ nhạy ±20% cho 6 biến, tỷ giá ±5%, lưới huỷ × chuyển đổi 6×5, kịch bản phụ gói 1.000 USD. Thiếu: cả 3 kịch bản dùng chung 10.000 người theo dõi sẵn có; không có độ nhạy cho tỷ lệ vào Skool ở mức thấp (2–3%); lưới giữ nguyên lượng truy cập của kịch bản cơ sở |
| 6 | Nhận định thẳng thắn, nói rõ khi không khả thi | 10 | | 75 | Nói thẳng "rủi ro thật là doanh thu bằng 0", IRR vô nghĩa, 99.004 là giả định, phải đo huỷ thật trong 2–3 tháng đầu. Nhưng kịch bản thận trọng vẫn lãi luỹ kế 734 tr, không có kịch bản nào cho thấy khi nào thì không đáng làm; kết luận 2 "1 học viên" nghe lạc quan hơn thực tế; không nói rằng kịch bản cơ sở (578 tr doanh thu/tháng ở T24) là tham vọng so với mặt bằng giá VN |

**Điểm = 25×0,95 + 20×0,95 + 15×0,85 + 15×0,75 + 15×0,80 + 10×0,75 = 23,75 + 19 + 12,75 + 11,25 + 12 + 7,5 = 86,25 ≈ 86**

**Kết luận: ĐẠT** (86 ≥ 80, cả 3 tiêu chí Chặn đều ≥ 85%).

## Phản hồi (sắp theo mức quan trọng)
1. Giả định phễu chưa có căn cứ cho một kênh đang xây lại → đặt `nguoi_theo_doi_dau` = 0 (hoặc ô "chờ số thật") làm mặc định cho kịch bản thận trọng, ghi lý do lấy KENH.md ("đo mốc tuần đầu").
2. Tỷ lệ 8% người theo dõi mới vào Skool ghi là "không rào cản", ngược với nghien-cuu.md (giao diện tiếng Anh, tài khoản ngoài) → hạ kịch bản thận trọng xuống khoảng 2–3%, sửa lý do, và thêm dòng độ nhạy cho tỷ lệ vào Skool 2%/4%/8% (2% → 54 HV, lãi T24 135,6 tr).
3. Kết luận 2 "hoà vốn chỉ cần 1 học viên" → viết lại thành "2 học viên chỉ với khoá cơ bản (1 HV lỗ ~0,23 tr/tháng); 1 HV chỉ hoà vốn khi tính phần bán kèm trung bình".
4. Chưa có kịch bản "không đáng làm" → thêm một dòng hoặc một ô trong lưới ghép lượng truy cập thấp + chuyển đổi thấp + huỷ cao, nêu ngưỡng (ví dụ < X HV sau 6 tháng) để anh quyết định dừng hoặc đổi giá; gọi rõ kịch bản cơ sở là tham vọng so với mặt bằng giá khoá crypto VN.
5. Thuế 7% có thể tính trùng GTGT với phần Skool đã thu (merchant of record) → ghi chú thêm ở dòng Thuế, kèm độ nhạy thuế 2% so với 7% để anh hỏi kế toán.
