# Đội ngũ

```
 Bạn giao việc
      │
      ▼
 ┌─────────────┐   phiếu giao việc    ┌──────────────────────────────────────────────┐
 │ MINH–QUẢN LÝ│ ───────────────────▶ │ NHÂN VIÊN (mỗi bạn một hồ sơ, một công việc) │
 └─────────────┘                      │ Lan · Hùng · Mai · Tùng · Ngọc · Phong ·     │
   ▲       ▲                          │ Khoa · Vy · Quân · Hà                        │
   │       │                          └──────────────────────┬───────────────────────┘
   │       │ ĐẠT / làm lại (≤ 3 vòng)                         │ nộp việc
   │       └──────────────── BẢO – GIÁM SÁT ◀────────────────┘ chấm theo tiêu chí trong hồ sơ
   │                              │ ghi nhật ký
   │                              ▼
   │                     team/nhan-su/<mã>/nhat-ky.jsonl ──▶ team/BANG_DIEM.md
   │                                                              │
   │   đề xuất nâng cấp       HỘI ĐỒNG CẢI TIẾN                   │
   └───────────────────── Đức – Phân tích hiệu suất ◀─────────────┘
                          Trang – Phản biện
```

| Nhân viên | Mã gọi | Bộ phận | Công việc | Hồ sơ |
|---|---|---|---|---|
| **Minh – Quản lý** | (phiên chính) | Điều hành | Nhận việc từ bạn, phân công, giám sát tiến độ, bàn giao, nâng cấp đội | [hồ sơ](nhan-su/quan-ly/ho-so.md) |
| Lan – Nghiên cứu | `nghien-cuu` | Dự án | Thị trường, đối thủ, giá, pháp lý — có nguồn | [hồ sơ](nhan-su/nghien-cuu/ho-so.md) |
| Hùng – Tài chính | `tai-chinh` | Dự án | Vốn, hoà vốn, hoàn vốn, NPV/IRR, độ nhạy | [hồ sơ](nhan-su/tai-chinh/ho-so.md) |
| Mai – Chiến lược & Kế hoạch | `chien-luoc` | Dự án | Kế hoạch, mô hình kinh doanh, rủi ro, lộ trình, KPI | [hồ sơ](nhan-su/chien-luoc/ho-so.md) |
| Tùng – Thiết kế Demo | `thiet-ke-demo` | Dự án | Trang tương tác, máy tính tài chính, dashboard | [hồ sơ](nhan-su/thiet-ke-demo/ho-so.md) |
| Ngọc – Ý tưởng & Content | `y-tuong-content` | Nội dung | Ý tưởng, hook, caption | [hồ sơ](nhan-su/y-tuong-content/ho-so.md) |
| Phong – Kịch bản Quay | `kich-ban-quay` | Nội dung | Kịch bản video 90–180s, hướng dẫn quay | [hồ sơ](nhan-su/kich-ban-quay/ho-so.md) |
| Khoa – Edit Video | `edit-video` | Nội dung | Dựng video 9:16 từ video thô | [hồ sơ](nhan-su/edit-video/ho-so.md) |
| Vy – Đăng & Phân phối | `dang-link` | Kênh | Lên lịch đăng, media, link | [hồ sơ](nhan-su/dang-link/ho-so.md) |
| Quân – Cộng đồng & Báo cáo | `tra-loi-bao-cao` | Kênh | Số liệu kênh, trả lời bình luận | [hồ sơ](nhan-su/tra-loi-bao-cao/ho-so.md) |
| Hà – Kiểm định | `kiem-dinh` | Chất lượng | Rà sản phẩm cuối của cả nhóm | [hồ sơ](nhan-su/kiem-dinh/ho-so.md) |
| **Bảo – Giám sát** | `giam-sat` | Chất lượng | Chấm từng phần việc: xong hay làm lại | [hồ sơ](nhan-su/giam-sat/ho-so.md) |
| **Đức – Phân tích hiệu suất** | `phan-tich` | Hội đồng cải tiến | Phân tích bảng điểm, tìm nguyên nhân, đề xuất | [hồ sơ](nhan-su/phan-tich/ho-so.md) |
| **Trang – Phản biện** | `phan-bien` | Hội đồng cải tiến | Phản biện từng nhân viên sau mỗi việc (ghi `gop-y.jsonl`) và phản biện đề xuất nâng cấp | [hồ sơ](nhan-su/phan-bien/ho-so.md) |

## Hồ sơ nhân sự
Mỗi bạn có thư mục `team/nhan-su/<mã>/`:
- `ho-so.md` — công việc, nhận gì, nộp gì, **tiêu chuẩn hoàn thành** (tiêu chí có trọng số, tiêu chí Chặn), phiên bản prompt, lịch sử nâng cấp.
- `nhat-ky.jsonl` — mỗi lần Bảo chấm là một dòng: việc, vòng, điểm, đạt hay không, lỗi.
- `gop-y.jsonl` — góp ý của Trang sau mỗi việc: vấn đề, bằng chứng, cách làm tốt hơn.
- Prompt làm việc: `.claude/agents/<mã>.md`.

**ĐẠT** = điểm ≥ 80 và không tiêu chí Chặn nào dưới 60%. Chưa đạt thì làm lại, tối đa 3 vòng.

## Vòng cải tiến
- `team/BANG_DIEM.md` (tạo bằng `python3 team/tools/bang_diem.py`): tỷ lệ đạt lần đầu, điểm TB, số vòng sửa, tiêu chí yếu nhất, lỗi lặp lại, điểm theo từng phiên bản prompt.
- Chu kỳ nâng cấp (`/nang-cap-doi-ngu`, hoặc tự chạy khi có cảnh báo / sau mỗi 5 việc): Đức phân tích ∥ Trang phản biện → trưởng nhóm quyết định → sửa prompt và tiêu chí → tăng phiên bản → chu kỳ sau đo lại, kém hơn thì hoàn tác.
- Hồ sơ mỗi chu kỳ: `team/nang-cap/<ngày>-cN/` (phan-tich.md, phan-bien.md, quyet-dinh.md).

## Dự án độc lập
Mỗi việc bạn giao được mở **hồ sơ mới** `team/viec/<ngày>-<tên-việc>/` với `brief.md` riêng. Nhân viên chỉ làm trên hồ sơ đó và dữ kiện tra cứu mới, không lấy số liệu hay thương hiệu từ dự án cũ (fanpage, mật ong rừng, trung tâm kỹ năng…). Muốn dùng lại dự án cũ, bạn chỉ cần nói rõ, ví dụ "dựa trên dự án mật ong".

## Cách giao việc
- Gõ `/giao-viec <mô tả công việc>` hoặc cứ nói việc cần làm. Trưởng nhóm sẽ trả về **phiếu giao việc** (ai làm gì, chạy song song hay nối tiếp), rồi tự điều phối đến khi bàn giao.
- Ví dụ: `/giao-viec Lập kế hoạch mở quán cà phê sách 80 m² ở Hội An, vốn tối đa 800 triệu, có demo tính hoàn vốn`
  → Lan (giá thuê, đối thủ, giấy phép) ∥ Hùng (mô hình tài chính) → Mai (kế hoạch) ∥ Tùng (demo) → Hà (kiểm định) → doc + trang demo.
