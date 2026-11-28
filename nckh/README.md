# Nhóm Nghiên cứu Khoa học (NCKH)
Đội riêng, bản sao theo mô hình đội AI hiện có nhưng **chỉ gồm các vai chính của một đề tài nghiên cứu**. Gọi bằng `/nckh <đề tài>` hoặc "nhóm nghiên cứu ơi…".

| Thành viên | Mã gọi | Nhiệm vụ chính |
|---|---|---|
| **An – Chủ nhiệm đề tài** | (phiên chính, skill `nckh`) | Nhận đề tài, lập brief, phân công, giữ tiến độ, bàn giao |
| Thư – Tổng quan tài liệu | `nckh-tong-quan` | Tìm, đọc, tổng hợp công trình đã công bố; khoảng trống; danh mục APA có DOI đã kiểm |
| Khánh – Phương pháp & Thiết kế | `nckh-phuong-phap` | Câu hỏi, giả thuyết, thiết kế, mẫu & cỡ mẫu, công cụ đo, đạo đức nghiên cứu |
| Nam – Dữ liệu & Thống kê | `nckh-du-lieu` | Làm sạch, phân tích bằng code tái lập; bảng, biểu đồ, nhật ký phân tích |
| Hạnh – Viết báo cáo khoa học | `nckh-viet-bai` | Đề cương, báo cáo, bài báo IMRaD, APA; chỉ dùng số và tài liệu đã kiểm |
| Tuệ – Phản biện độc lập | `nckh-phan-bien` | Bình duyệt như hội đồng/tạp chí: chấm 7 tiêu chí, vấn đề lớn/nhỏ, khuyến nghị |
| Ngân – Liêm chính & Kiểm định | `nckh-liem-chinh` | Khớp số liệu–code, trích dẫn có thật, đạo văn, đạo đức, đúng mẫu nộp |

## Quy trình
```
Đề tài ─▶ An (brief) ─▶ Thư (tổng quan) ─▶ Khánh (phương pháp) ─▶ Hạnh (đề cương) ─▶ Tuệ (phản biện ≤2 vòng)
        ─▶ [anh thu dữ liệu] ─▶ Nam (phân tích) ─▶ Hạnh (báo cáo/bài báo) ─▶ Tuệ ─▶ Ngân (ĐẠT) ─▶ bàn giao
```

## Thư mục mỗi đề tài: `nckh/de-tai/<YYYY-MM-DD-slug>/`
brief.md · tong-quan.md · phuong-phap.md · cong-cu/ · de-cuong-hoan-chinh.md · phan-bien-*.md · du-lieu/ (chỉ dữ liệu ẩn danh) · code/ · ket-qua.md · bang-bieu/ · bao-cao.md / bai-bao.md

## Nguyên tắc
Không bịa tài liệu hay số liệu · mọi số từ code · trích dẫn đã mở nguồn · bảo vệ người tham gia · repo công khai nên không đưa dữ liệu định danh lên repo · mỗi đề tài độc lập.
