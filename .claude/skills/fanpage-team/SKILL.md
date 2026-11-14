---
name: fanpage-team
description: Chạy đội 5 agent chăm sóc fanpage ĐẠO ĐỨC ĐẦU TƯ theo 2 pha. Pha A (/fanpage-team hoặc /fanpage-team <chủ đề | nội dung nguồn>) — Ý Tưởng & Content → Kịch Bản Quay video 90–180s, rồi chờ chủ page tự quay. Pha B (/fanpage-team edit [link Drive]) — Edit Video → Đăng & Link → Trả Lời & Báo Cáo. Thêm "tu-dong" để đăng thật, "thu" để không đăng.
---
# Đội agent chăm sóc fanpage — 2 pha

```
PHA A (máy làm)                         NGƯỜI QUAY            PHA B (máy làm)
[1 Ý Tưởng & Content] → [2 Kịch Bản Quay] ──▶ quay 90–180s ──▶ [3 Edit Video] → [4 Đăng & Link] → [5 Trả Lời & Báo Cáo]
 ideas.json, post.md     kichban.txt            raw/*.mp4         video.mp4          publish.json      report.md
                         huong_dan_quay.md                        edit_log.md
                         edit_plan.json
```

## Xác định pha
- `DAY=$(TZ=Asia/Bangkok date +%F)`, `RUN=fanpage/runs/$DAY`, `mkdir -p $RUN/raw`.
- Tham số có `edit`, hoặc có link Google Drive / file video, hoặc `$RUN/raw/` đã có video **và** `$RUN/kichban.txt` tồn tại → **Pha B**. Nếu `raw/` của hôm nay trống thì tìm ngày gần nhất có `kichban.txt` mà chưa có `publish.json` và dùng `RUN` đó.
- Ngược lại → **Pha A**. Phần chữ còn lại của tham số (bỏ `thu`, `tu-dong`) = chủ đề bắt buộc hoặc nội dung nguồn cần viết lại.

## Pha A (dùng Agent tool, subagent_type tương ứng, run_in_background: false, tuần tự)
| # | subagent_type | Prompt |
|---|---|---|
| 1 | `y-tuong-content` | "run_dir=$RUN.[ Chủ đề bắt buộc / Nội dung nguồn cần viết lại: …]" |
| 2 | `kich-ban-quay` | "run_dir=$RUN. Viết lời thoại 90–180s, hướng dẫn quay, edit_plan." |

Kết thúc Pha A: commit + push `fanpage/`, rồi gửi người dùng **nguyên văn `kichban.txt`** (để đọc theo khi quay) + tóm tắt checklist quay + cách nộp video (bỏ vào `fanpage/runs/<ngày>/raw/` hoặc gửi link Drive kèm `/fanpage-team edit <link>`). Gửi kèm file `huong_dan_quay.md` bằng SendUserFile.

## Pha B
| # | subagent_type | Prompt |
|---|---|---|
| 3 | `edit-video` | "run_dir=$RUN.[ Video thô: <link/đường dẫn>]" |
| 4 | `dang-link` | "run_dir=$RUN. Đăng theo config.[ Lần này publish_mode=tu-dong.]" — bỏ qua nếu có `thu` |
| 5 | `tra-loi-bao-cao` | "run_dir=$RUN. Lập báo cáo ngày." |

Gửi video.mp4 cho người dùng xem (SendUserFile) ngay sau bước 3.

## Quy tắc chung
- Sau mỗi bước kiểm tra file đầu ra; thiếu → chạy lại bước đó 1 lần, vẫn lỗi thì dừng và báo rõ.
- Không đăng thật trừ khi `config.publish_mode == "tu-dong"` hoặc người dùng ghi `tu-dong`.
- Kết thúc mỗi pha: `git add fanpage/ && git commit` rồi push lên nhánh hiện tại (video không lên git).
- Trả lời người dùng bằng tiếng Việt, ngắn gọn: đã làm gì, việc tiếp theo của họ.
