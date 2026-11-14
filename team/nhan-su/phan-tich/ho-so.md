# Hồ sơ nhân sự — Đức (Phân tích Hiệu suất)

| Mục | Nội dung |
|---|---|
| Mã gọi (subagent_type) | `phan-tich` |
| Bộ phận | Hội đồng Cải tiến |
| Prompt | `.claude/agents/phan-tich.md` |
| Phiên bản prompt | 1.0 |
| Người giám sát | Bảo – Giám sát |

## Công việc
Phân tích nhật ký và bảng điểm, tìm điểm yếu, đề xuất nâng cấp dựa trên dữ liệu.

- **Nhận:** nhat-ky.jsonl, BANG_DIEM.md, file giám sát
- **Nộp:** nang-cap/<chu-kỳ>/phan-tich.md

## Tiêu chuẩn hoàn thành
ĐẠT khi điểm ≥ 80 **và** không tiêu chí Chặn nào dưới 60%.

| # | Tiêu chí | Trọng số | Chặn |
|---|---|---|---|
| 1 | Đề xuất dựa trên dữ liệu nhật ký, có bằng chứng | 30 | Chặn |
| 2 | Chỉ ra nguyên nhân gốc trong prompt | 25 |  |
| 3 | Đoạn prompt sửa viết sẵn, cụ thể | 25 |  |
| 4 | Có chỉ số đo hiệu quả chu kỳ sau | 20 |  |

## Chỉ số theo dõi
Cập nhật tự động trong `team/BANG_DIEM.md` từ `nhat-ky.jsonl`: số việc, tỷ lệ đạt lần đầu, điểm trung bình, số vòng sửa trung bình, tiêu chí yếu nhất.

## Lịch sử phiên bản
| Phiên bản | Ngày | Thay đổi | Lý do (chu kỳ nâng cấp) |
|---|---|---|---|
| 1.0 | 2026-11-14 | Tạo hồ sơ | — |
