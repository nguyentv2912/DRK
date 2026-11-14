# Đội Agent chăm sóc fanpage — ĐẠO ĐỨC ĐẦU TƯ (bản nâng cấp: video tự quay 90–180s)

| # | Agent | Làm gì | Đầu ra |
|---|---|---|---|
| 1 | 🔵 Ý Tưởng & Content | Gom 10 ý → lọc → chấm điểm → chọn 1; viết/viết lại caption 2 vòng biên tập | `ideas.json`, `post.md` |
| 2 | 🟡 Kịch Bản Quay | Lời thoại 90–180s (mỗi câu 1 dòng), hướng dẫn quay + bảng cảnh + teleprompter, kế hoạch edit | `kichban.txt`, `huong_dan_quay.md`, `edit_plan.json` |
| — | 🎥 **Bạn quay** | Quay theo hướng dẫn, vấp thì dừng 2 giây rồi nói lại cả câu | `raw/*.mp4` |
| 3 | 🔴 Edit Video | Bóc lời (Whisper) → tự cắt câu vấp/quay lại + khoảng lặng → khung 9:16, zoom nhịp, phụ đề to tô màu từ khoá, thẻ chữ viền vàng, nhạc nền → tự kiểm tra chất lượng | `video.mp4`, `video_cover.jpg`, `edit_log.md` |
| 4 | 🟢 Đăng & Link | (giữ nguyên) Drive → Metricool Reel, giờ vàng, link bình luận đầu | `publish.json` |
| 5 | 🟠 Trả Lời & Báo Cáo | (giữ nguyên) số liệu 7 ngày, bài học, câu trả lời bình luận mẫu | `report.md` |

Prompt chi tiết từng agent: `.claude/agents/*.md`. Điều phối: `.claude/skills/fanpage-team/SKILL.md`.

## Dùng mỗi ngày
1. **`/fanpage-team`** (hoặc `/fanpage-team <chủ đề>` / dán bài cũ cần viết lại) → nhận kịch bản + hướng dẫn quay.
2. Quay video, bỏ file vào `fanpage/runs/<ngày>/raw/` hoặc upload Google Drive.
3. **`/fanpage-team edit <link Drive>`** → nhận video đã edit, bản nháp trên Metricool, báo cáo.
   Thêm `tu-dong` để đăng thật, `thu` để chỉ edit không đăng.

## Công cụ
- `tools/edit_video.py` — `transcribe` (bóc lời có mốc từng chữ) và `render` (dựng). Cần `pip install faster-whisper`.
- `tools/make_video.py` — video chữ động không cần quay, dùng dự phòng hôm không quay được.

## Tuỳ chỉnh
`config.json` (chế độ đăng, link CTA, giờ dự phòng) · `brand.md` (giọng văn, trụ cột, điều cấm).

## Giới hạn
- Chưa tự trả lời bình luận thật (Metricool/Buffer không hỗ trợ) — Agent 5 soạn câu trả lời mẫu.
- Facebook có thể không nhận Reel dài hơn giới hạn của họ; khi đó Agent 4 tự chuyển sang đăng video thường (POST).
