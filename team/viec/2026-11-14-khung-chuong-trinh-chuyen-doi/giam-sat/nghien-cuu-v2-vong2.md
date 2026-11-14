# Giám sát — Lan (nghien-cuu) · Phiên bản 2 · Vòng 2

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày: 14/11/2026 · Người chấm: Bảo · Prompt nhân viên: 1.0
File chấm: `nghien-cuu.md` (195 dòng, 7 kết luận, 5 bảng A–E, 9 câu hỏi mở, 97 URL). Không xét `ban-nhap-cu/`.

## Ngoại lệ môi trường (ghi rõ)
- Trưởng nhóm Minh **duyệt ngoại lệ môi trường** cho tiêu chí #2: chấm phần Lan kiểm soát được (link đầy đủ, đúng loại nguồn, ghi rõ nguồn nào chưa có toàn văn), **không tính** việc không mở được trang gốc.
- Bằng chứng mạng bị chặn (kiểm lại vòng này): `curl` tools4skool.com, amis.misa.vn → proxy báo `connect_rejected`; vòng 1 đã kiểm help.skool.com, ruzuku.com, skoolfiles.com, circle.so, thuvienphapluat.vn, transparency.meta.com → 403.
- Nếu chấm theo hồ sơ gốc, không áp ngoại lệ: #2 tối đa 58% (trần do môi trường), dưới 60%, nên bài sẽ **CHƯA ĐẠT** dù tổng điểm là 87. Kết luận ĐẠT dưới đây **chỉ có hiệu lực nhờ ngoại lệ**. Nguồn chưa mở được trang gốc thì vẫn chưa được xếp mức tin cậy "Cao".

## Kiểm tra 5 phản hồi vòng 1
| # | Phản hồi vòng 1 | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | 12 tên miền + 2 trang không có URL | Đã sửa | Script đối chiếu cột Nguồn của mọi bảng với mục Nguồn: **0 tên miền thiếu**; 97 URL, không trùng |
| 2 | Link help center số 86 trùng | Đã sửa | Dòng 185: giải thích 86-payments-faq là đường dẫn cũ của cùng bài, chọn `86-subscriptions-faq` làm chuẩn (là đường dẫn có mục "Supported countries for payouts"); thêm bài 78, 195 |
| 3 | Phần người Việt trả USD mỏng | Đã sửa | Bảng D thêm 6 dòng: thẻ Visa/MC/Amex/Discover, không có PayPal/crypto, Apple/Google Pay mâu thuẫn, Napas thuần không dùng được, QĐ 2345 bị bãi bỏ (QĐ 2872), cách xác minh bằng thử 3–5 thẻ |
| 4 | NĐ 87/2026, NĐ 141/2026 chỉ có bài tóm tắt | Đã sửa | Dòng 132, 136 ghi "**Chưa có toàn văn**"; thêm 3–5 nguồn báo cho mỗi nghị định; câu hỏi mở 6–7 chỉ cách lấy toàn văn trên vbpl.vn |
| 5 | Mốc thời gian chung chung | Đã sửa | Dòng 11 nêu quy ước "truy cập 11/2026"; BLHS ghi "11/2015, sửa đổi 6/2017"; luật có ngày thông qua (14/6/2025, 16/6/2025) |

## Tự kiểm chứng khác
- Phép tính phí giữ đúng: 96,80 / 960,70 USD (Pro), 89,70 / 899,70 USD (Hobby), điểm hoà 1.267,6 USD.
- Không đề xuất đổi giá (dòng 6). Không hứa lợi nhuận; mẫu câu "216" an toàn giữ nguyên.

## Bảng chấm
| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | Trả lời đủ các câu hỏi nghiên cứu (Chặn) | 25 | 95 | Đủ cả 6 nhóm việc được giao; phần trả USD đã đầy đủ (bảng D, 10 dòng). Còn nhỏ: chưa có giá cộng đồng crypto Việt trên Skool (đã ghi là câu hỏi mở 9) |
| 2 | Số liệu quan trọng có nguồn gốc đã mở (link) (Chặn) — **áp ngoại lệ môi trường** | 25 | 90 | Mọi nguồn trong bảng đều có URL (0 thiếu / 97 URL). Văn bản luật dẫn thuvienphapluat/luatvietnam khi có; nguồn chưa có toàn văn đều gắn nhãn. Trừ: slug bài 78 là `78-how-to-setup-skool-subscriptions` nhưng bảng A dòng 68 gọi là "How to set up payouts", tên và đường dẫn không khớp; nguồn cuthongthai.vn bàn về thuế trung tâm dạy thêm, không khớp hẳn với chuyện bán khoá qua nền tảng nước ngoài |
| 3 | Không bịa; ghi rõ điều chưa tìm được và cách xác minh (Chặn) | 20 | 93 | Ghi "chưa tìm được" cho quy định thay QĐ 2345, tỷ lệ người VN trả phí nước ngoài; Apple Pay ghi rõ là mâu thuẫn; 9 câu hỏi mở đều có cách xác minh. Trừ: kết luận 7 nêu ngưỡng 1 tỷ đ (NĐ 141/2026) như điều chắc chắn, chưa kèm lưu ý "chưa có toàn văn" như ở bảng E |
| 4 | Ghi thời điểm và độ tin cậy từng dữ kiện | 15 | 95 | Mọi dòng đều có cả hai cột; có quy ước thời điểm rõ ràng; dòng suy luận ghi là "suy luận, 11/2026" kèm mức Thấp |
| 5 | Đúng mẫu: kết luận, bảng dữ kiện, câu hỏi mở, nguồn | 15 | 95 | 7 kết luận (đúng yêu cầu 5–7), 5 bảng, ghi chú áp dụng, 9 câu hỏi mở, mục Nguồn khớp 100% với bảng. Kết luận hơi dài (mỗi ý 3–5 gạch đầu dòng) |

**Điểm (áp ngoại lệ):** 25×0,95 + 25×0,90 + 20×0,93 + 15×0,95 + 15×0,95 = 23,75 + 22,5 + 18,6 + 14,25 + 14,25 = **93,35 ≈ 93**
(Nếu chấm theo hồ sơ gốc: #2 = 58 → 87,35 điểm, CHƯA ĐẠT vì tiêu chí Chặn dưới 60%.)

## Kết luận: **ĐẠT** (theo ngoại lệ môi trường do trưởng nhóm duyệt)
Đã xử lý đủ 5/5 phản hồi vòng 1. Không còn lỗi Chặn trong phần Lan kiểm soát được.

## Phản hồi (không bắt buộc, sửa nếu có dịp)
1. Bảng A dòng 68 ghi bài 78 là "How to set up payouts" nhưng slug là `how-to-setup-skool-subscriptions` → kiểm lại tên bài hoặc slug cho khớp nhau.
2. Kết luận 7, ý Thuế → thêm "(theo báo, chưa có toàn văn NĐ 141/2026)" cho khớp với bảng E.
3. Nguồn cuthongthai.vn (thuế trung tâm dạy thêm) không đúng trọng tâm → thay bằng nguồn bàn đúng chuyện bán khoá qua nền tảng nước ngoài, hoặc ghi là chỉ tham khảo gián tiếp.
4. Trước khi chủ dự án chốt: dữ kiện "VN có trong danh sách payout" và "3,9% khi > 900 USD" phải được mở trang gốc khi có mạng (câu hỏi mở 1–2). Ngoại lệ chỉ áp cho điểm, không thay được bước xác minh này.
