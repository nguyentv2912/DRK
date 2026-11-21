# Giám sát — KB-20261116-1…6 (6 video ngắn "6 lời ông bà") — quan-ly (Minh soạn thay Ngọc/Phong) — vòng 1

Ngày: 2026-11-16 · Người chấm: Bảo · Hồ sơ: kich-ban-quay (A) + y-tuong-content (B), thay tiêu chí thời lượng bằng yêu cầu anh (~1 phút).
Kiểm chứng bằng script: đếm âm tiết, câu, câu dài nhất, khớp trigger, quét 10 từ cấm (theo ranh giới từ, NFC) trên cả 42 file.

| Mã | Âm tiết (ghi trong HDQ) | Câu thực / ghi | Câu dài nhất | Trigger khớp | Từ cấm |
|---|---|---|---|---|---|
| 1 | 208 (208) | 20 / 19 | 20 | 2/2 | 0 |
| 2 | 215 (215) | 19 / 17 | 18 | 2/2 | 0 |
| 3 | 204 (204) | 18 / 17 | 16 | 2/2 | 0 |
| 4 | 221 (221) | 19 / 19 | 19 | 2/2 | 0 |
| 5 | 223 (223) | 20 / 18 | 18 | 2/2 | 0 |
| 6 | 216 (216) | 20 / 17 | 17 | 2/2 | 0 |

## A. Kịch bản quay
| # | Tiêu chí | TS | % | Bằng chứng |
|---|---|---|---|---|
| 1 | edit_plan hợp lệ, trigger nguyên văn (Chặn) | 25 | 90 | 6 JSON hợp lệ, 12/12 trigger có nguyên văn trong kichban.txt. Khối `keywords` chép y hệt cho cả 6: mỗi bản 4–5/6 từ khoá không có trong lời thoại; "kỷ luật" không xuất hiện ở bản nào. |
| 2 | Thời lượng ~1 phút (yêu cầu anh) (Chặn) | 20 | 85 | 204–223 âm tiết, ở tốc độ 2,84–3,33 âm tiết/giây (cùng mức dùng cho KB-20261115-2) ra khoảng 61–79 giây. Bản 4 và 5 có thể vượt 1:15. |
| 3 | Nhịp hook–vấn đề–chuyển ý–thân–chốt–CTA | 20 | 85 | Mở bằng câu ông bà và câu móc, rồi giải nghĩa, "Mình kể các bạn nghe…", câu chuyện, bài học, câu hỏi bình luận, miễn trừ. Bản 2 vào thân không có câu chuyển ý rõ. Card 2 bản 4 hiện ở câu "lọc", trong khi nội dung thẻ ("VIẾT RA…") nằm ở câu sau. |
| 4 | Hướng dẫn quay đủ | 20 | 75 | Cả 6 dùng chung một mẫu, không chia cảnh theo đoạn. "Quay dọc 9:16 hoặc ngang" để ngỏ, trong khi đã đặt crop_x. Số câu ghi lệch 1–3 câu ở 5/6 bản. Không mở được link slide (artifact) để đối chiếu số slide 3–8. |
| 5 | Văn nói, câu ≤ 20 chữ | 15 | 90 | Câu dài nhất 20 chữ (bản 1, câu "Ngày xưa, mùa gặt nào…"), đúng ngưỡng. Giọng kể tự nhiên, xưng "mình" và gọi "các bạn". |
A = 22,5 + 17 + 17 + 15 + 13,5 = **85**

## B. Ý tưởng / nội dung
| # | Tiêu chí | TS | % | Bằng chứng |
|---|---|---|---|---|
| 1 | Không vi phạm điều cấm (Chặn) | 25 | 85 | Quét 42 file: 0 lần xuất hiện của giá/mua/bán/kiếm tiền/lãi/lỗ/lợi nhuận/vay/kèo/bắt đáy. Còn sát nghĩa ở 3 chỗ: bản 2 "mượn thêm vốn" (cùng nghĩa với vay); bản 6 "hứa trả gần hai mươi phần trăm mỗi năm", "cam kết hoàn vốn" (trích lại để cảnh báo); bản 4 "chỉ dùng tiền nhàn rỗi, mỗi tháng tích lũy một phần cố định" gần thành gợi ý hành động đầu tư. |
| 2 | Đúng giọng thương hiệu | 20 | 90 | Giọng ông bà, ấm, không hô hào. Có miễn trừ ở kịch bản, post, tiktok, bình luận ghim. |
| 3 | Ý tưởng được chấm điểm có lý do | 20 | 50 | Mỗi ideas.json chỉ có 1 ứng viên, điểm 9, lý do chép y hệt cho cả 6 ("Anh yêu cầu trực tiếp…"). Không có phương án so sánh và không có lý do riêng cho từng câu chuyện. |
| 4 | Caption đúng khung và độ dài | 20 | 85 | Post ngắn có chủ ý: đủ câu ông bà, tóm tắt câu chuyện, bài học, câu hỏi, Zalo, miễn trừ, hashtag, 1 emoji. Post 4 lặp ý: "Bài học mùa đông: Viết ra bài học mùa đông." |
| 5 | Hook ≤ 14 chữ | 15 | 90 | Câu mở là câu ông bà, 4–8 chữ. Câu móc thứ hai 8–12 chữ. Hook TikTok là câu ông bà, đạt. |
B = 21,25 + 18 + 10 + 17 + 13,5 = **79,75**

## Kết luận
Điểm chung (A+B)/2 = 82,4, làm tròn **82**. Không tiêu chí Chặn nào dưới 60%. **ĐẠT**.

## Phản hồi (sắp theo mức quan trọng, không có lỗi chặn)
1. ideas.json: 1 ứng viên, lý do chép chung → mỗi bản thêm 2–3 phương án câu chuyện khác, chấm điểm, ghi lý do riêng vì sao chọn câu chuyện này.
2. Từ sát nghĩa từ cấm → bản 2 đổi "mượn thêm vốn" thành "dùng sàn nhân quy mô lệnh lên"; bản 4 bỏ "tiền nhàn rỗi/tích lũy một phần cố định", thay bằng thói quen ("mỗi tuần chỉ xem tài khoản một lần"); bản 6 giữ các lời hứa trích dẫn nhưng nói rõ "đây là câu kẻ lừa hay dùng".
3. edit_plan keywords chép chung → mỗi bản chỉ giữ từ khoá có trong lời thoại của bản đó; bỏ "kỷ luật" hoặc đưa từ này vào lời thoại.
4. Hướng dẫn quay → chốt một khung hình (dọc 9:16); sửa số câu cho đúng (20/19/18/19/20/20); ghi 3 đoạn quay (câu ông bà, câu chuyện, bài học + CTA) kèm cảm xúc cho từng đoạn.
5. Thời lượng bản 4 và 5 (221–223 âm tiết) → cắt 1–2 câu để giữ dưới khoảng 1:10. Post 4: sửa câu lặp "Bài học mùa đông: Viết ra bài học mùa đông".
