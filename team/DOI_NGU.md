# Đội ngũ

```
                         ┌──────────────┐
          Bạn giao việc ─▶│  TRƯỞNG NHÓM │── phiếu giao việc ─▶ bàn giao sản phẩm
                         └──────┬───────┘
     ┌──────────────┬──────────┼───────────┬──────────────┐
  KHỐI DỰ ÁN     KHỐI DỰ ÁN   KHỐI NỘI DUNG  KHỐI KÊNH     CHẤT LƯỢNG
  Lan  Nghiên cứu  Mai Chiến lược  Ngọc Ý tưởng   Vy   Đăng         Hà Kiểm định
  Hùng Tài chính   Tùng Demo       Phong Kịch bản  Quân Báo cáo
                                   Khoa Edit video
```

| Nhân viên | Mã gọi | Chuyên môn | Giao nộp |
|---|---|---|---|
| Lan – Nghiên cứu | `nghien-cuu` | Thị trường, đối thủ, giá, pháp lý — có nguồn và độ tin cậy | `nghien-cuu.md` |
| Hùng – Tài chính | `tai-chinh` | Vốn, hoà vốn, hoàn vốn, NPV/IRR, độ nhạy, 3 kịch bản | `mo_hinh.py`, `tai-chinh.md`, `tai-chinh.json` |
| Mai – Chiến lược & Kế hoạch | `chien-luoc` | Kế hoạch, mô hình kinh doanh, SWOT, rủi ro, lộ trình, KPI, nhân rộng | `ke-hoach.md` |
| Tùng – Thiết kế Demo | `thiet-ke-demo` | Trang HTML tương tác, máy tính tài chính, dashboard | `demo.html` |
| Ngọc – Ý tưởng & Content | `y-tuong-content` | Ý tưởng, hook, caption | `ideas.json`, `post.md` |
| Phong – Kịch bản Quay | `kich-ban-quay` | Kịch bản video 90–180s, hướng dẫn quay | `kichban.txt`, `huong_dan_quay.md`, `edit_plan.json` |
| Khoa – Edit Video | `edit-video` | Dựng video 9:16 từ video thô | `video.mp4` |
| Vy – Đăng & Phân phối | `dang-link` | Lên lịch Metricool, Google Drive, link | `publish.json` |
| Quân – Cộng đồng & Báo cáo | `tra-loi-bao-cao` | Số liệu kênh, trả lời bình luận | `report.md` |
| Hà – Kiểm định | `kiem-dinh` | Rà số liệu, nguồn, chính tả, đủ yêu cầu | `kiem-dinh.md` |

## Dự án độc lập
Mỗi việc bạn giao được mở **hồ sơ mới** `team/viec/<ngày>-<tên-việc>/` với `brief.md` riêng. Nhân viên chỉ làm trên hồ sơ đó và dữ kiện tra cứu mới, không lấy số liệu hay thương hiệu từ dự án cũ (fanpage, mật ong rừng, trung tâm kỹ năng…). Muốn dùng lại dự án cũ, bạn chỉ cần nói rõ, ví dụ "dựa trên dự án mật ong".

## Cách giao việc
- Gõ `/giao-viec <mô tả công việc>` hoặc cứ nói việc cần làm. Trưởng nhóm sẽ trả về **phiếu giao việc** (ai làm gì, chạy song song hay nối tiếp), rồi tự điều phối đến khi bàn giao.
- Ví dụ: `/giao-viec Lập kế hoạch mở quán cà phê sách 80 m² ở Hội An, vốn tối đa 800 triệu, có demo tính hoàn vốn`
  → Lan (giá thuê, đối thủ, giấy phép) ∥ Hùng (mô hình tài chính) → Mai (kế hoạch) ∥ Tùng (demo) → Hà (kiểm định) → doc + trang demo.
