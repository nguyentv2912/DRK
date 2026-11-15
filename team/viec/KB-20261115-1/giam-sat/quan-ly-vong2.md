# Giám sát — KB-20261115-1 (Mùa đông – Gieo hạt, tập 1) — Vòng 2

- **Người làm:** Minh (quan-ly), soạn thay Ngọc/Phong. Thang chấm giữ như vòng 1: kich-ban-quay cho phần kịch bản, y-tuong-content cho post/TikTok, thời lượng theo yêu cầu anh (3–5 phút).
- **Kiểm tra lại:** quét 10 từ cấm trên 7 file: 0 lần xuất hiện. kichban.txt vẫn sạch. Mạch ĐẠO → ĐỜI → ĐẦU TƯ giữ nguyên.
- **Emoji ☯ 🏠 📈:** đã kiểm chứng, `.claude/skills/viet-bai-dao-duc-dau-tu/SKILL.md` dòng 17 quy định bố cục ☯ ĐẠO → 🏠 ĐỜI → 📈 ĐẦU TƯ. Chấp nhận, không trừ điểm (rút lại góp ý vòng 1 về hai emoji này).
- **Nguồn tin:** `fanpage/phong-y-tuong/20261115-ban-tin-crypto/nguon.md` có URL CoinDesk 12/11, 14/11 và Bloomberg 15/11, khớp với post.md.

## A. Kịch bản

| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | edit_plan.json hợp lệ, trigger nguyên văn (Chặn) | 25 | 95 | JSON đọc được. 6 trigger ("Thứ nhất, Đạo"… "Bài học thứ ba, từ mùa đông năm 2022") đều có nguyên văn trong kichban.txt (script: missing = []). |
| 2 | Thời lượng 3–5 phút (Chặn) | 20 | 85 | 850 âm tiết. Ở 200/phút ≈ 4:15; ở 170/phút (đọc chậm) ≈ 5:00. Nằm trong khoảng, sát trần nếu đọc rất chậm. |
| 3 | Nhịp hook – vấn đề – chuyển ý – thân – chốt – CTA | 20 | 90 | Giữ đủ như vòng 1. |
| 4 | Hướng dẫn quay | 20 | 85 | Số chữ đã sửa thành 850, khớp. Hướng dẫn ghi "73 câu" nhưng script đếm được 86 câu (tách theo dấu . ? ! :). |
| 5 | Văn nói, câu ≤ 20 chữ | 15 | 85 | Một câu dài 21 chữ: "Năm đó, một sàn giao dịch từng lớn nhất thế giới sụp đổ, rất nhiều người bị kẹt tài sản gần mười năm." |

**Điểm A = 23,75 + 17 + 18 + 17 + 12,75 = 88,5**

## B. Post / TikTok

| # | Tiêu chí | Trọng số | % | Bằng chứng |
|---|---|---|---|---|
| 1 | Không vi phạm điều cấm (Chặn) | 25 | 75 | Post sạch, có miễn trừ và nguồn. Nhưng tiktok.md vòng 2 **đã mất câu miễn trừ** (vòng 1 có "Chia sẻ, không phải lời khuyên đầu tư."). Caption có bàn chuyện vốn (đòn bẩy, tiền nhàn rỗi), mà brand.md bắt buộc miễn trừ, KENH.md cũng yêu cầu "miễn trừ ngắn" cho TikTok. |
| 2 | Đúng giọng thương hiệu (Chặn) | 20 | 85 | Mình/các bạn ở cả hai file, đã bỏ #binhan. ☯ 🏠 📈 theo skill. Tổng 5 emoji, vẫn nhỉnh hơn mức 3–4 do có thêm 🍂 và 📌. |
| 3 | Ý tưởng chấm điểm có lý do | 20 | 90 | ideas.json có 4 ứng viên, mỗi ứng viên có điểm và lý do, ghi rõ ý được chọn và nguồn tin. |
| 4 | Caption đúng khung và độ dài | 20 | 80 | post.md 235 chữ (khung 150–250). Lời TikTok 133 ký tự, 4 hashtag. Thiếu miễn trừ ở TikTok. |
| 5 | Hook ≤ 14 chữ | 15 | 90 | Hook post 12 chữ. Hook video đếm được 14 chữ (Minh báo là 12), vẫn đạt mức ≤ 14. Hook TikTok 8 chữ. |

**Điểm B = 18,75 + 17 + 18 + 16 + 13,5 = 83,25**

## Kết luận
**ĐẠT** — điểm chung 86 (A 88,5; B 83,25). Không tiêu chí Chặn nào dưới 60%.

## Phản hồi (nên sửa trước khi đăng)
1. tiktok.md mất câu miễn trừ → thêm lại "Chia sẻ, không phải lời khuyên đầu tư." (vẫn trong khoảng ≤ 150 ký tự nếu rút gọn câu hỏi).
2. Câu 21 chữ ở bài học 2014 → tách đôi: "Năm đó, một sàn giao dịch từng lớn nhất thế giới sụp đổ." / "Rất nhiều người bị kẹt tài sản gần mười năm."
3. huong_dan_quay.md ghi 73 câu, đếm thực tế 86 → sửa lại cho khớp.
