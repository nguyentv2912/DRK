# Giám sát — Lan (nghien-cuu) · Phiên bản 2 · Vòng 1

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày: 14/11/2026 · Người chấm: Bảo · Prompt nhân viên: 1.0
File chấm: `nghien-cuu.md` (144 dòng, 7 kết luận, 5 bảng A–E, 8 câu hỏi mở, 73 URL). Không xét `ban-nhap-cu/`.

## Tự kiểm chứng
- Mở link: `curl` mọi nguồn thử (help.skool.com, ruzuku.com, skoolfiles.com, circle.so, thuvienphapluat.vn, transparency.meta.com) đều trả `CONNECT tunnel failed, response 403`. Xác nhận **môi trường chặn mạng**, không phải do Lan.
- Tính lại phí: Pro 100 − 2,9 − 0,30 = **96,80** ✓; 1.000 − 39 − 0,30 = **960,70** ✓ (áp 3,9%); Hobby 89,70 / 899,70 ✓; điểm hoà 90 / 0,071 = **1.267,6 USD** ≈ 13 thành viên ✓ (khớp `tai-chinh.md` dòng 119).
- Đối chiếu nguồn trong bảng với "Danh sách nguồn" (script): **12 tên miền được dẫn trong bảng nhưng không có URL** ở danh sách: bravo.com.vn, tracuuphapluat.net, hethongphapluat.com, luatdanviet.com.vn, cuthongthai.vn, investing.com, megadigital.ai, forkast.news, agrowth.io, ninjapromo.io, communipass.com, slobodskyi.com. Ngoài ra "stickyhive.ai/blog (churn Skool)" và "skoolmakers.com/communities" không có URL cụ thể.
- Mã bài help center: `article/86-payments-faq` và `article/86-subscriptions-faq` cùng số 86 nhưng khác slug, chắc chắn có một link sai. Dữ kiện payout/VN (kết luận 3) dựa vào link này.
- Giá anh chốt: không đề xuất đổi giá (dòng 4, kết luận 4 chỉ nêu vị trí giá so với thị trường) ✓. Không hứa lợi nhuận; phần "216 lần" đúng hướng brief ✓.

## Bảng chấm
| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | Trả lời đủ các câu hỏi nghiên cứu (Chặn) | 25 | 90 | Đủ 6 nhóm câu hỏi: phí/gói/%/cách thu/payout VN/tiếng Việt/giới hạn (bảng A, 25 dòng); 10+ cộng đồng Skool + khoá VN (bảng B); churn & chuyển đổi (C); trả USD (D); pháp lý crypto, ebook, thuế, Phật–Nho–Đạo (E + ghi chú); mẫu câu "216" (dòng 115–120). Thiếu: phần "người Việt trả USD" mới có số thẻ + phí đổi ngoại tệ, chưa nói Skool nhận phương thức nào (thẻ Visa/Master, Apple/Google Pay?), thẻ ghi nợ nội địa/Napas có dùng được không, hạn mức thanh toán quốc tế phải bật. |
| 2 | Số liệu quan trọng có nguồn gốc đã mở (link) (Chặn) | 25 | 50 | Không mở được trang gốc nào — trần do môi trường (proxy 403, đã kiểm), Lan ghi rõ ở dòng 6 và 137. Lỗi riêng: 12 tên miền trong bảng không có URL; link help.skool.com số 86 trùng cho 2 bài khác nhau; NQ 05, Luật 75/2025 có link toàn văn, nhưng NĐ 87/2026, NĐ 141/2026 chỉ dẫn bài tóm tắt. |
| 3 | Không bịa; ghi rõ điều chưa tìm được và cách xác minh (Chặn) | 20 | 90 | Ghi "Chưa tìm được" (D dòng 85, E dòng 92), "chưa xác minh" cho điều khoản thu tiền ngoài Skool, mâu thuẫn gói năm, affiliate; 8 câu hỏi mở đều có cách xác minh cụ thể (kiểm thử giao dịch 1 USD, hỏi NXB, hỏi chi cục thuế). Trừ điểm: link bài 86 trùng số khiến dữ kiện "VN có trong danh sách payout" chưa truy được; tỷ giá 26.000 đ là giả định chưa tra (đã gắn nhãn). |
| 4 | Ghi thời điểm và độ tin cậy từng dữ kiện | 15 | 88 | Mọi dòng có cột Thời điểm + Độ tin cậy; không xếp "Cao" có lý do. Còn mốc mơ hồ: nhiều dòng chỉ ghi "2026", "chưa rõ ngày" (dòng 33), "–" (BLHS dòng 97). |
| 5 | Đúng mẫu: kết luận, bảng dữ kiện, câu hỏi mở, nguồn | 15 | 90 | Có 7 kết luận (yêu cầu 5–7), 5 bảng, câu hỏi mở, danh sách nguồn theo nhóm, mục ghi chú áp dụng. Trừ: danh sách nguồn không khớp bảng (12 miền thiếu). Độ dài 144 dòng < ~250 nhưng bảng dày, không thiếu nội dung nên không trừ thêm. |

**Điểm:** 25×0,90 + 25×0,50 + 20×0,90 + 15×0,88 + 15×0,90 = 22,5 + 12,5 + 18,0 + 13,2 + 13,5 = **79,7 ≈ 80**

## Kết luận: **CHƯA ĐẠT**
Tiêu chí Chặn #2 = 50% (< 60%). Trần do môi trường là 58% (cùng mức đã áp cho các vòng trước khi không còn lỗi riêng); 8 điểm còn lại là lỗi của Lan và sửa được ngay. Lưu ý cho trưởng nhóm: dù sửa hết, tiêu chí #2 vẫn kẹt ở 58% vì môi trường; cần quyết định cho mở mạng hoặc chấp nhận ngoại lệ có ghi chú.

## Phản hồi (sắp theo mức quan trọng)
1. 12 tên miền dẫn trong bảng không có URL ở "Danh sách nguồn" (bravo.com.vn, tracuuphapluat.net, hethongphapluat.com, luatdanviet.com.vn, cuthongthai.vn, investing.com, megadigital.ai, forkast.news, agrowth.io, ninjapromo.io, communipass.com, slobodskyi.com) + stickyhive.ai/blog, skoolmakers.com/communities → thêm URL đầy đủ cho từng cái, hoặc xoá khỏi bảng nếu không còn link.
2. `help.skool.com/article/86-payments-faq` và `article/86-subscriptions-faq` cùng số 86 → tìm lại đúng mã bài cho từng trang (đặc biệt bài có danh sách nước payout gồm Việt Nam) và sửa ở bảng A dòng 24–26, 37–38 và mục Nguồn.
3. Phần người Việt trả USD còn mỏng → bổ sung: Skool nhận phương thức thanh toán nào; thẻ ghi nợ nội địa/Napas có trả được không; người mua phải bật thanh toán quốc tế/hạn mức; mỗi dòng có nguồn + độ tin cậy (hoặc ghi "chưa tìm được" + cách xác minh).
4. NĐ 87/2026 và NĐ 141/2026 chỉ dẫn bài tóm tắt → tìm link văn bản (thuvienphapluat.vn/vbpl.vn) hoặc ghi rõ "chưa có toàn văn" trong cột Nguồn.
5. Mốc thời gian chung chung ("2026", "chưa rõ ngày", "–") → ghi tháng/năm của trang hoặc văn bản (BLHS 2015 sửa đổi 2017; bài help center: ngày cập nhật nếu trích đoạn có).
