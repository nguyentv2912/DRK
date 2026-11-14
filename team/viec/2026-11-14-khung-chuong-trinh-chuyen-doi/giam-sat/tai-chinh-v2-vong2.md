# Giám sát — Hùng (tai-chinh) · Phiên bản 2 · Vòng 2

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày: 2026-11-14 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File chấm: mo_hinh.py, tai-chinh.md, tai-chinh.json (bỏ qua ban-nhap-cu/). Đối chiếu với 5 phản hồi vòng 1 (giam-sat/tai-chinh-v2-vong1.md).

## Kiểm chứng đã làm
- Sao lưu tai-chinh.md, tai-chinh.json, ke-hoach.md rồi chạy lại `python3 mo_hinh.py` (rc=0). Kết quả: **tai-chinh.md giống hệt từng byte (cmp)**, **tai-chinh.json bằng nhau khi so dạng dict**, ke-hoach.md không bị script đụng tới.
- Giá anh chốt không đổi: `gia_co_ban_usd 100.0`, `gia_chuyen_sau_usd 1000.0`, `gia_ebook_vnd 1_000_000` (mo_hinh.py dòng 23–25); JSON `gia` = 100 / 1000 / 1.000.000 đ; khớp brief dòng 59–61. Mục 5b ghi "Giá anh chốt giữ nguyên trừ khi anh quyết khác".
- Tính tay người theo dõi T24 của kịch bản cơ sở khi không có người theo dõi sẵn: 2.000 × Σ1,05^k (k=0..23) = 2.000 × 44,502 = 89.004 (khớp kết luận 4 và bảng mục 5).
- Độ nhạy ±20% "người theo dõi mới" và "tỷ lệ vào Skool" ra số giống nhau (209,4 / 330,4) là đúng, vì cả hai đều nhân vào cùng một dòng phễu khi người theo dõi sẵn có = 0. Dòng 4% trong bảng tỷ lệ vào Skool = 209,4, khớp mức −20%.
- JSON `nguong_dung`: tỷ lệ vào Skool tương ứng 0,94%, T3 ≥ 55 thành viên miễn phí / ≥ 1 HV; T6 ≥ 110 / ≥ 3 HV / lãi ≥ 6,2 tr; chuyển đổi ≥ 2,5%; huỷ ≤ 12%. Kết quả qua ngưỡng: không đáng làm và thận trọng đều trượt, cơ sở và lạc quan đạt; khớp bảng 5b.

## Đối chiếu 5 phản hồi vòng 1
| # | Phản hồi vòng 1 | Đã sửa? | Bằng chứng |
|---|---|---|---|
| 1 | Người theo dõi sẵn có = 0 | Đã sửa | `"nguoi_theo_doi_dau": 0` kèm chú thích "kenh dang xay lai (KENH.md) - CHO SO THAT" (dòng 64); bảng giả định ghi "Mặc định 0 — chờ số thật" |
| 2 | Tỷ lệ vào Skool thận trọng 2–3% + độ nhạy 2/4/8% | Đã sửa | Thận trọng 2,5%, không đáng làm 2%, cơ sở 5%; lý do viết lại thành "Có rào cản: Skool không có giao diện tiếng Việt…"; bảng 2%/4%/8% → 46/91/183 HV, lãi T24 114,6/209,4/451,4 tr |
| 3 | Câu hoà vốn "2 học viên nếu chỉ có khoá cơ bản" | Đã sửa | Kết luận 2: "Hoà vốn hằng tháng: 2 học viên trả 100 USD nếu chỉ có khoá cơ bản"; bảng mốc có cột "Cơ sở, chỉ có khoá cơ bản" (hoà vốn 2); mục 9 cũng sửa theo |
| 4 | Kịch bản "không đáng làm" + ngưỡng dừng tháng 3/6 | Đã sửa | Kịch bản thứ 4: 1 HV, lãi T24 0,3 tr, luỹ kế −93,6 tr, chưa hoàn vốn; mục 5b có ngưỡng T3 (đổi cách bán) và T6 (dừng mở rộng); kịch bản cơ sở gọi rõ là "tham vọng" |
| 5 | Ghi chú thuế trùng VAT + độ nhạy 2% vs 7% | Đã sửa | Dòng Thuế ghi Skool là merchant of record nên phần 5% GTGT có thể trùng; bảng 2% vs 7% cho cả 4 kịch bản (ví dụ cơ sở 3.008,2 so với 2.824,4 tr) |

## Bảng chấm

| # | Tiêu chí | Trọng số | Chặn | % | Bằng chứng |
|---|---|---|---|---|---|
| 1 | Script chạy được và tái tạo đúng các số trong báo cáo | 25 | Chặn | 95 | rc=0; md giống hệt từng byte, json bằng nhau; người theo dõi T24, độ nhạy và ngưỡng 5b khớp giữa md, json và tính tay |
| 2 | Đủ chỉ số: vốn, hoà vốn, hoàn vốn, NPV, IRR, dòng tiền | 20 | Chặn | 95 | Vốn 78,0 tr; hoà vốn 2/2/1/1; hoàn vốn chưa/15/6/3; NPV −92,9/137,7/2.394,5/13.969,4; IRR kèm ghi chú "không có ý nghĩa so sánh"; dòng tiền 24 tháng |
| 3 | Phép tính hợp lý: đơn vị, dấu, biên lợi nhuận, không lỗi | 15 | Chặn | 92 | Đã sửa câu hoà vốn, có ghi chú thuế có thể trùng. Còn một điểm nhỏ: ngưỡng số lượng ở 5b lấy từ đường có tỷ lệ vào Skool 0,94%, thấp hơn cả kịch bản "không đáng làm" (2%), nên ngưỡng số lượng lỏng; việc phân loại thực chất do ngưỡng tỷ lệ quyết định (thận trọng có 72 ≥ 55 thành viên nhưng vẫn trượt vì chuyển đổi 2%) |
| 4 | Bảng giả định có nguồn hoặc ghi 'giả định' | 15 | | 88 | Người theo dõi 0 (chờ số thật, có lý do từ KENH.md); lý do tỷ lệ vào Skool khớp nghien-cuu.md; chuyển đổi 3% ghi "lấy phía thấp" vì giá cao so với thu nhập VN. Còn: 3% vẫn dựa vào số SaaS, chưa đối chiếu với giá khoá crypto VN 59.000–2.500.000 đ trả một lần |
| 5 | Độ nhạy ±20% và 3 kịch bản | 15 | | 92 | 4 kịch bản; ±20% cho 6 biến; tỷ giá ±5%; tỷ lệ vào Skool 2/4/8%; thuế 2% so với 7%; ngưỡng miễn thuế; lưới huỷ × chuyển đổi 6×5; kịch bản phụ gói 1.000 USD. Lưới vẫn chỉ chạy trên lượng truy cập của kịch bản cơ sở |
| 6 | Nhận định thẳng thắn, nói rõ khi không khả thi | 10 | | 90 | Gọi cơ sở là "tham vọng", khuyên lập kế hoạch theo thận trọng; nói rõ thận trọng không qua ngưỡng, phải đổi cách bán ở tháng 3; "không đáng làm" mất chủ yếu thời gian của anh |

**Điểm = 25×0,95 + 20×0,95 + 15×0,92 + 15×0,88 + 15×0,92 + 10×0,90 = 23,75 + 19 + 13,8 + 13,2 + 13,8 + 9 = 92,55 ≈ 93**

**Kết luận: ĐẠT** (93 ≥ 80, cả 3 tiêu chí Chặn đều ≥ 92%). Đã sửa đủ cả 5 phản hồi vòng 1; giá anh chốt không đổi; md và json khớp script.

## Phản hồi (không bắt buộc, sắp theo mức quan trọng)
1. Ngưỡng số lượng ở 5b lấy từ đường có tỷ lệ vào Skool 0,94% nên lỏng hơn cả "không đáng làm" → ghi thêm một câu trong 5b rằng tín hiệu quyết định là ngưỡng tỷ lệ (chuyển đổi ≥ 2,5%, huỷ ≤ 12%), còn ngưỡng số lượng chỉ là mức sàn.
2. Chuyển đổi 3% vẫn lấy từ số SaaS → thêm một câu so với mặt bằng khoá crypto VN trả một lần (nghien-cuu.md dòng 13), để anh thấy rủi ro của mô hình thuê bao 100 USD/tháng.
3. Lưới huỷ × chuyển đổi chỉ chạy trên lượng truy cập của kịch bản cơ sở → nếu còn thời gian, thêm một lưới nhỏ trên nền thận trọng (nên bám kịch bản này khi lập kế hoạch).
