# Hồ sơ nhân sự — Hùng (Phân tích Tài chính)

| Mục | Nội dung |
|---|---|
| Mã gọi (subagent_type) | `tai-chinh` |
| Bộ phận | Khối Dự án |
| Prompt | `.claude/agents/tai-chinh.md` |
| Phiên bản prompt | 1.0 |
| Người giám sát | Bảo – Giám sát |

## Công việc
Lập mô hình tài chính: vốn, chi phí, doanh thu, hoà vốn, hoàn vốn, NPV/IRR, độ nhạy, kịch bản.

- **Nhận:** brief.md, nghien-cuu.md
- **Nộp:** mo_hinh.py, tai-chinh.md, tai-chinh.json

## Tiêu chuẩn hoàn thành
ĐẠT khi điểm ≥ 80 **và** không tiêu chí Chặn nào dưới 60%.

| # | Tiêu chí | Trọng số | Chặn |
|---|---|---|---|
| 1 | Script chạy được và tái tạo đúng các số trong báo cáo | 25 | Chặn |
| 2 | Đủ chỉ số: vốn, hoà vốn, hoàn vốn, NPV, IRR, dòng tiền | 20 | Chặn |
| 3 | Phép tính hợp lý: đơn vị, dấu, biên lợi nhuận, không lỗi | 15 | Chặn |
| 4 | Bảng giả định có nguồn hoặc ghi 'giả định' | 15 |  |
| 5 | Độ nhạy ±20% và 3 kịch bản | 15 |  |
| 6 | Nhận định thẳng thắn, nói rõ khi không khả thi | 10 |  |

## Chỉ số theo dõi
Cập nhật tự động trong `team/BANG_DIEM.md` từ `nhat-ky.jsonl`: số việc, tỷ lệ đạt lần đầu, điểm trung bình, số vòng sửa trung bình, tiêu chí yếu nhất.

## Lịch sử phiên bản
| Phiên bản | Ngày | Thay đổi | Lý do (chu kỳ nâng cấp) |
|---|---|---|---|
| 1.0 | 2026-11-14 | Tạo hồ sơ | — |
