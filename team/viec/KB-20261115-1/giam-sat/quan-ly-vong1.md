# Giám sát — KB-20261115-1 (Mùa đông – Gieo hạt, tập 1) — Vòng 1

- **Người làm:** Minh (quan-ly), soạn thay Ngọc/Phong.
- **Thang chấm:** phần kịch bản theo `team/nhan-su/kich-ban-quay/ho-so.md`; phần post/tiktok theo `team/nhan-su/y-tuong-content/ho-so.md`. Tiêu chí thời lượng được thay bằng yêu cầu riêng của anh (3–5 phút).
- **Kiểm tra yêu cầu riêng:** ĐẠO → ĐỜI (tin tuần này: CoinDesk, ETF, Bloomberg) → ĐẦU TƯ (3 bài học 2014/2018/2022): đủ. Giải thích từng ý (ETF, giảm chậm, đòn bẩy, tiền nhàn rỗi): đủ. kichban.txt sạch, không có tiêu đề phần hay ghi chú: đạt. Quét 10 từ cấm (giá, mua, bán, kiếm tiền, lãi, lỗ, lợi nhuận, vay, kèo, bắt đáy) bằng regex có ranh giới từ trên cả 5 file: **0 lần xuất hiện**.

## A. Kịch bản (kichban.txt + huong_dan_quay.md)

| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | edit_plan.json hợp lệ, trigger có nguyên văn trong lời (Chặn) | 25 | 0 | Thư mục không có edit_plan.json. Trigger chỉ được gợi ý bằng văn xuôi trong huong_dan_quay.md ("Thứ nhất / Thứ hai / Thứ ba", các thẻ chữ). |
| 2 | Thời lượng (theo yêu cầu anh: 3–5 phút) (Chặn) | 20 | 65 | 901 âm tiết, 92 câu. Đọc 200 âm tiết/phút ≈ 4:30; giọng "chậm, ấm" như hướng dẫn quay dặn (~170/phút) ≈ 5:18 chưa tính chỗ dừng. Dễ vượt 5 phút. huong_dan_quay.md ghi "877 chữ, 80 câu", không khớp số đếm. |
| 3 | Nhịp: hook, vấn đề, chuyển ý, thân, chốt, CTA | 20 | 90 | Có hook ("Nếu dạo này mở app ra…"), báo trước 3 ý, chuyển ý "Thứ nhất/hai/ba", chốt "Mùa đông là để giữ ấm trước…", CTA bình luận + Zalo + miễn trừ. Phần Đời hơi dài so với Đạo. |
| 4 | Hướng dẫn quay đủ, người không chuyên làm theo được | 20 | 90 | Checklist trước khi quay, giọng và nhịp theo từng đoạn, cử chỉ (giơ ngón tay, cầm giấy), xử lý khi vấp, minh hoạ cho Khoa, nơi nộp file. Không có mốc thời gian cho từng phần. |
| 5 | Văn nói tự nhiên, câu ≤ 20 chữ | 15 | 90 | Câu dài nhất ≤ 20 chữ (đếm bằng script: không câu nào vượt). Giọng mình/các bạn, có ví dụ đời thường. |

**Điểm A = 0 + 13 + 18 + 18 + 13,5 = 62,5 → 63** — CHƯA ĐẠT (Chặn #1 = 0%).

## B. Post/TikTok (post.md, tiktok.md, binh_luan_ghim.md)

| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | Không vi phạm điều cấm (Chặn) | 25 | 90 | 0 từ cấm; có miễn trừ; có nêu nguồn (CoinDesk 14/11, 12/11; Bloomberg 15/11) nhưng không kèm link; không nêu tên sàn/đồng tiền (tránh bôi nhọ). Biểu tượng ☯ (âm dương) dễ bị hiểu là tôn giáo/tâm linh, mà brand.md cấm nội dung tôn giáo. |
| 2 | Đúng giọng thương hiệu và đối tượng (Chặn) | 20 | 80 | Xưng mình/các bạn, giọng điềm tĩnh. Nhưng post có 5 emoji (🍂 ☯ 🏠 📈 📌) trong khi giới hạn là 3–4; 📈 (biểu đồ đi lên) lạc tông với bài mùa đông; tiktok.md gọi "bạn" chứ không phải "các bạn"; #binhan đụng tên "Đầu Tư Bình An" đang chờ anh duyệt. |
| 3 | Ý tưởng được chấm điểm có lý do | 20 | 0 | Không có ideas.json hay bảng chấm ý tưởng nào. |
| 4 | Caption đúng khung và độ dài | 20 | 55 | post.md 360 chữ, khung KENH.md là 150–250. Lời TikTok 151 ký tự, giới hạn ≤ 150. Số hashtag đúng (5/5). |
| 5 | Hook ≤ 14 chữ, có sức hút | 15 | 75 | Hook post 15 chữ ("Nếu dạo này mở app ra là thấy mệt, bài này dành cho các bạn."), hook video 16 chữ. Hook TikTok 7 chữ, đạt. |

**Điểm B = 22,5 + 16 + 0 + 11 + 11,25 = 60,75 → 61** — CHƯA ĐẠT (dưới 80, không có Chặn dưới 60).

## Kết luận
**CHƯA ĐẠT** — điểm chung 62 (trung bình A 63, B 61). Nội dung và tuân thủ yêu cầu riêng của anh đều tốt; bị trừ ở hồ sơ kỹ thuật còn thiếu và độ dài.

## Phản hồi (theo mức quan trọng)
1. Thiếu edit_plan.json (Chặn) → tạo edit_plan.json hợp lệ, mỗi trigger chép nguyên văn từ kichban.txt (ví dụ "Thứ nhất, Đạo", "ETF các bạn hiểu đơn giản là một cái quỹ", "Bài học thứ nhất", "nhóm Zalo ở bình luận ghim").
2. Kịch bản có nguy cơ vượt 5 phút (901 âm tiết, đọc chậm ≈ 5:18) → cắt còn khoảng 750–800 âm tiết (bớt đoạn kể "bạn ấy…" ở phần Đời, gộp hai câu chốt "Không ai biết…" đang lặp lại), rồi sửa số chữ/câu trong huong_dan_quay.md cho khớp.
3. Thiếu bảng chấm ý tưởng → thêm ideas.json: 3–5 ý tưởng, mỗi ý có điểm và lý do, đánh dấu ý được chọn.
4. post.md 360 chữ, vượt khung 150–250 → rút phần Đời và Đầu tư mỗi phần còn 2–3 câu, giữ câu hỏi cuối bài, miễn trừ, nguồn và hashtag. Rút lời TikTok xuống ≤ 150 ký tự.
5. Hook post 15 chữ và hook video 16 chữ, vượt mức 14 → ví dụ "Dạo này mở app ra là mệt? Bài này dành cho các bạn." Bỏ ☯ và 📈 để còn ≤ 4 emoji, đổi "bạn" thành "các bạn" trong tiktok.md, bỏ #binhan cho tới khi anh duyệt tên.

Ghi chú: chưa kiểm chứng được nội dung tin CoinDesk/Bloomberg vì file không có link. Nên thêm URL nguồn vào post.md để Hà kiểm định.
