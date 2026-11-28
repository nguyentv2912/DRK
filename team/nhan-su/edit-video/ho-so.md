# Hồ sơ nhân sự — Khoa (Edit Video)

| Mục | Nội dung |
|---|---|
| Mã gọi (subagent_type) | `edit-video` |
| Bộ phận | Khối Nội dung |
| Prompt | `.claude/agents/edit-video.md` |
| Phiên bản prompt | 1.0 |
| Người giám sát | Bảo – Giám sát |

## Công việc
Dựng video 9:16 từ video thô: cắt lỗi, phụ đề, thẻ chữ, nhạc nền.

- **Nhận:** video thô, kichban.txt, edit_plan.json
- **Nộp:** video.mp4, video_cover.jpg, edit_log.md

## Tiêu chuẩn hoàn thành
ĐẠT khi điểm ≥ 80 **và** không tiêu chí Chặn nào dưới 60%.

| # | Tiêu chí | Trọng số | Chặn |
|---|---|---|---|
| 1 | Đúng thông số: 1080x1920, có tiếng, đúng thời lượng | 25 | Chặn |
| 2 | Phụ đề đúng chữ so với kịch bản | 20 | Chặn |
| 3 | Cắt hết câu vấp và khoảng lặng | 20 |  |
| 4 | Thẻ chữ đúng lúc, không tràn khung, không che mặt | 20 |  |
| 5 | edit_log.md đầy đủ | 15 |  |

## Chỉ số theo dõi
Cập nhật tự động trong `team/BANG_DIEM.md` từ `nhat-ky.jsonl`: số việc, tỷ lệ đạt lần đầu, điểm trung bình, số vòng sửa trung bình, tiêu chí yếu nhất.

## Lịch sử phiên bản
| Phiên bản | Ngày | Thay đổi | Lý do (chu kỳ nâng cấp) |
|---|---|---|---|
| 1.0 | 2026-11-14 | Tạo hồ sơ | — |
