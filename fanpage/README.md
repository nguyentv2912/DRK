# Đội Agent tự động chăm sóc fanpage — ĐẠO ĐỨC ĐẦU TƯ

| # | Agent | Làm gì | File |
|---|---|---|---|
| 1 | 🔵 Tìm Ý Tưởng | Xoay vòng 5 trụ cột, tránh trùng 30 ngày, học từ báo cáo cũ | `.claude/agents/tim-y-tuong.md` |
| 2 | 🟡 Viết Bài | Caption Facebook + kịch bản cảnh video | `.claude/agents/viet-bai.md` |
| 3 | 🔴 Dựng Video | Reel 9:16 chữ động nền đen-vàng + nhạc nền | `.claude/agents/dung-video.md`, `tools/make_video.py` |
| 4 | 🟢 Đăng & Link | Video lên Google Drive → Metricool, giờ vàng, link ở bình luận đầu | `.claude/agents/dang-link.md` |
| 5 | 🟠 Trả Lời & Báo Cáo | Số liệu 7 ngày, bài học, câu trả lời bình luận mẫu | `.claude/agents/tra-loi-bao-cao.md` |

Điều phối: skill **`/fanpage-team`** (`.claude/skills/fanpage-team/SKILL.md`).

## Dùng
- `/fanpage-team` — chạy cả đội, tạo **bản nháp** trong Metricool để bạn duyệt.
- `/fanpage-team thu` — chạy thử, không đăng gì.
- `/fanpage-team tu-dong` — đăng thật lần này.
- `/fanpage-team FOMO khi thị trường tăng nóng` — ép chủ đề.

## Tuỳ chỉnh (`config.json`)
- `publish_mode`: `nhap` (an toàn, mặc định) → đổi sang `tu-dong` khi đã tin chất lượng.
- `cta_link`: link gắn ở bình luận đầu (nhóm, khoá học, affiliate).
- `preferred_hours`: giờ dự phòng khi Metricool chưa có số liệu giờ vàng.
- Giọng văn, trụ cột, điều cấm: `brand.md`.

## Mỗi ngày tạo ra
`runs/YYYY-MM-DD/`: `ideas.json`, `post.md`, `storyboard.json`, `video.mp4` (không lên git), `video_cover.jpg`, `publish.json`, `report.md`.

## Giới hạn hiện tại
- Trả lời bình luận: Metricool/Buffer chưa cho đọc–trả lời bình luận Facebook, nên Agent 5 soạn sẵn câu trả lời mẫu. Muốn tự trả lời thật cần thêm kịch bản Make (Facebook Pages → Watch comments).
- Video là dạng chữ động + nhạc tổng hợp, chưa có giọng đọc. Có thể ghép giọng clone từ `kaggle/` sau.
