---
name: fanpage-team
description: Chạy đội 5 agent tự động chăm sóc fanpage ĐẠO ĐỨC ĐẦU TƯ mỗi ngày — Tìm Ý Tưởng → Viết Bài → Dựng Video → Đăng & Link → Trả Lời & Báo Cáo. Dùng khi người dùng gõ /fanpage-team hoặc yêu cầu "chạy đội agent fanpage hôm nay". Tham số tuỳ chọn: "thu" (chạy thử, không đăng), "tu-dong" (đăng thật thay vì nháp), hoặc một chủ đề cụ thể.
---
# Đội agent chăm sóc fanpage hằng ngày

```
[Tìm Ý Tưởng] → [Viết Bài] → [Dựng Video] → [Đăng & Link] → [Trả Lời & Báo Cáo]
 ideas.json     post.md        video.mp4      publish.json     report.md
                storyboard.json
```

## Chuẩn bị
1. `DAY=$(TZ=Asia/Bangkok date +%F)`; `RUN=fanpage/runs/$DAY`; `mkdir -p $RUN`. Nếu `$RUN/publish.json` có `"status": "ok"` thì hôm nay đã đăng → chỉ chạy Agent 5 (trừ khi người dùng bảo làm thêm bài).
2. Đọc tham số:
   - có chữ `thu` → **chạy thử**: bỏ qua Agent 4, ghi rõ trong báo cáo.
   - có chữ `tu-dong` → truyền cho Agent 4 rằng lần này được đăng thật (ghi đè `publish_mode`).
   - phần còn lại (nếu có) → chủ đề bắt buộc, truyền cho Agent 1.

## Chạy tuần tự (mỗi bước chờ bước trước xong, dùng Agent tool với subagent_type tương ứng, run_in_background: false)
| # | subagent_type | Prompt gửi đi |
|---|---|---|
| 1 | `tim-y-tuong` | "run_dir=$RUN. Chọn chủ đề hôm nay.[ Chủ đề bắt buộc: …]" |
| 2 | `viet-bai` | "run_dir=$RUN. Viết caption và storyboard từ ideas.json." |
| 3 | `dung-video` | "run_dir=$RUN. Render và kiểm tra video." |
| 4 | `dang-link` | "run_dir=$RUN. Đăng theo config.[ Lần này publish_mode=tu-dong.]" |
| 5 | `tra-loi-bao-cao` | "run_dir=$RUN. Lập báo cáo ngày." |

Sau mỗi bước: kiểm tra file đầu ra tồn tại. Thiếu → chạy lại bước đó 1 lần, vẫn thiếu thì dừng và báo lỗi rõ ràng (không chạy tiếp bước sau).

## Kết thúc
- `git add fanpage/ && git commit -m "Fanpage: bài ngày $DAY"` rồi push lên nhánh hiện tại (video .mp4 đã bị .gitignore, chỉ lưu trên Drive).
- Trả lời người dùng bằng tiếng Việt, ngắn: chủ đề, giờ đăng, chế độ (nháp/tự đăng), link duyệt Metricool, 3 số liệu chính, việc cần làm.
