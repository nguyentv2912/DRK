# Giám sát — KB-20261115-2 ("6 lời ông bà cho mùa đông crypto") — Vòng 1

- **Người làm:** Minh (quan-ly), soạn thay Ngọc/Phong. Thang chấm giống KB-20261115-1: hồ sơ kich-ban-quay cho phần kịch bản, y-tuong-content cho post/TikTok. Thời lượng chấm theo yêu cầu anh (3–5 phút).
- **Kiểm tra bằng script:** quét 10 từ cấm (giá, mua, bán, kiếm tiền, lãi, lỗ, lợi nhuận, vay, kèo, bắt đáy) theo ranh giới từ trên 7 file: 0 lần. kichban.txt không có ký tự markdown (* # [ ] _ ` >), sạch để đưa lên teleprompter. 7/7 trigger của edit_plan có nguyên văn trong kichban.txt (missing = []).
- **Đối chiếu tư liệu:** 6 câu tục ngữ khớp `fanpage/tu-lieu/TUC_NGU_DAU_TU.md`; phần thân rút từ `BAI_HOC_MUA_DONG_VIET_LIEN.md`.

## A. Kịch bản (kich-ban-quay)

| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | edit_plan.json hợp lệ, trigger nguyên văn (Chặn) | 25 | 95 | JSON đọc được; 7 trigger "Câu thứ nhất"… "Sáu câu nói, gói lại trong ba chữ" đều có trong kichban.txt. |
| 2 | Thời lượng 3–5 phút (Chặn) | 20 | 90 | 720 âm tiết: ở 200/phút ≈ 3:36, ở 170/phút ≈ 4:14. Nằm giữa khoảng. |
| 3 | Nhịp hook – vấn đề – chuyển ý – thân – chốt – CTA | 20 | 90 | Hook "Ông bà mình không biết đọc biểu đồ…", dẫn 6 câu, thân 6 phần, chốt "giữ, co, và tỉnh", câu hỏi bình luận, Zalo, miễn trừ. |
| 4 | Hướng dẫn quay | 20 | 85 | Đủ thiết bị, giọng, nhịp, minh hoạ cho Khoa. Ghi "700 chữ", đếm thực tế 720; "64 câu" khớp số dòng. |
| 5 | Văn nói, câu ≤ 20 chữ | 15 | 85 | Không câu nào quá 20 chữ. Nhưng có câu cụt bị ngắt khỏi câu chính: "Mỗi lần có một sàn sụp đổ hay bị tấn công." / "Trong một thị trường không ai biết trước ngày mai." Phần 3 và 6 bỏ mất chuyện đời của tư liệu (năm làm ăn thất bát; đi chợ gặp hàng hời), nên không đúng yêu cầu "liên hệ đời sống" bằng các phần kia. |

**Điểm A = 23,75 + 18 + 18 + 17 + 12,75 = 89,5**

## B. Post / TikTok (y-tuong-content)

| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | Không vi phạm điều cấm (Chặn) | 25 | 90 | 0 từ cấm; có miễn trừ ở post, tiktok, bình luận ghim và cuối kịch bản. Không nêu tên sàn, không có số liệu thiếu nguồn. |
| 2 | Đúng giọng thương hiệu (Chặn) | 20 | 80 | Xưng mình/các bạn. Post có 7 emoji (❄ và 1️⃣–6️⃣), brand.md giới hạn 3–4. Dòng 3️⃣ viết "con người bạn", lệch cách gọi "các bạn". |
| 3 | Ý tưởng chấm điểm có lý do | 20 | 20 | ideas.json chỉ có nguon_y_tuong, chon, tu_lieu. Không có danh sách ứng viên, không có điểm, không có lý do (KB-20261115-1 có 4 ứng viên kèm điểm và lý do). |
| 4 | Caption đúng khung và độ dài | 20 | 85 | post.md 224 chữ (khung 150–250), câu hỏi cuối, miễn trừ, 4 hashtag có #daoducdautu. TikTok: dòng chính 112 ký tự, có câu hỏi, miễn trừ, 4 hashtag. |
| 5 | Hook ≤ 14 chữ | 15 | 65 | Hook post và hook video "Ông bà mình không biết đọc biểu đồ, nhưng đã dạy mình cách qua mùa đông." dài 16 chữ, quá 14. Hook TikTok 8 chữ, đạt. |

**Điểm B = 22,5 + 16 + 4 + 17 + 9,75 = 69,25**

## Kết luận
**CHƯA ĐẠT**: điểm chung 79 (A 89,5; B 69,25; trung bình 79,4), dưới ngưỡng 80. Không tiêu chí Chặn nào dưới 60%. Phần kịch bản đạt; trượt ở phần ý tưởng/caption (ideas.json không chấm điểm, hook 16 chữ).

## Phản hồi (theo mức quan trọng)
1. ideas.json không có ứng viên chấm điểm → thêm `ung_vien` 3–4 ý (ví dụ: 6 lời ông bà; 1 câu tục ngữ/1 tập; mùa đông qua 4 mùa) mỗi ý có `diem` và `ly_do`, ghi lý do chọn ý hiện tại.
2. Hook 16 chữ → rút còn ≤ 14 chữ, ví dụ "Ông bà không đọc biểu đồ, nhưng dạy mình cách qua mùa đông." (13 chữ). Sửa đồng thời kichban.txt dòng 1 và post.md dòng 1.
3. Post 7 emoji → bỏ 1️⃣–6️⃣, thay bằng "1." … "6." hoặc gạch đầu dòng, chỉ giữ ❄ (và 📌 nếu cần). Sửa "con người bạn" thành "con người các bạn" hoặc "con người mình".
4. Phần 3 và 6 thiếu chuyện đời → thêm 1 câu đời sống: phần 3 "Ai sống đủ lâu cũng từng có năm làm ăn thất bát, có năm thuận buồm xuôi gió."; phần 6 "Đi chợ, gặp món hàng hời bất thường, các bà các mẹ thường lắc đầu." Thời lượng vẫn dưới 4:30.
5. Câu cụt → nối lại thành câu liền: "Mỗi lần có một sàn sụp đổ hay bị tấn công, người ta mới vội đi hỏi ví cá nhân là gì." (19 chữ); "Trong một thị trường không ai biết trước ngày mai, ai hứa chắc chắn là đang không nói thật." (19 chữ). Sau đó cập nhật số chữ, số câu trong huong_dan_quay.md.
