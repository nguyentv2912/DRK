---
name: nang-cap-doi-ngu
description: Chu kỳ nâng cấp đội nhân viên AI. Dùng khi người dùng gõ /nang-cap-doi-ngu hoặc yêu cầu "đánh giá / nâng cấp đội ngũ", và tự chạy khi bảng điểm có nhân viên bị cảnh báo hoặc sau mỗi 5 việc hoàn thành. Hội đồng cải tiến (Đức – Phân tích, Trang – Phản biện) phân tích dữ liệu giám sát, phản biện; trưởng nhóm quyết định và sửa prompt, tăng phiên bản trong hồ sơ.
---
# Chu kỳ nâng cấp đội ngũ (trưởng nhóm điều phối)

```
nhật ký giám sát ─▶ bảng điểm ─▶ Đức phân tích ∥ Trang phản biện ─▶ Trang phản biện đề xuất của Đức
     ─▶ trưởng nhóm quyết định ─▶ sửa prompt + tiêu chí ─▶ tăng phiên bản ─▶ đo lại ở chu kỳ sau
```

## 1. Chuẩn bị
- `python3 team/tools/bang_diem.py` → đọc `team/BANG_DIEM.md`.
- Mã chu kỳ `YYYY-MM-DD-cN`, thư mục `team/nang-cap/<mã-chu-kỳ>/`.
- Chọn nhân viên đưa vào chu kỳ: có cảnh báo trong bảng điểm + nhân viên người dùng nêu tên + nhân viên có phản hồi xấu từ người dùng. Không ai có dữ liệu → chỉ chạy Trang phản biện prompt (rà soát định kỳ), ghi rõ "chưa có dữ liệu hiệu suất".

## 2. Hội đồng làm việc
- Gọi song song: `phan-tich` (Đức) và `phan-bien` (Trang) với mã chu kỳ + danh sách nhân viên.
- Sau khi có `phan-tich.md`, gọi `phan-bien` lần nữa để Trang phản biện từng đề xuất của Đức (ghi thêm vào `phan-bien.md`).

## 3. Trưởng nhóm quyết định — `team/nang-cap/<mã-chu-kỳ>/quyet-dinh.md`
Bảng: Nhân sự | Vấn đề | Bằng chứng | Đề xuất (Đức/Trang) | Quyết định (Áp dụng / Sửa lại / Bác bỏ) | Lý do | Chỉ số đo ở chu kỳ sau.
Nguyên tắc: sửa nguyên nhân gốc, không chỉ triệu chứng; mỗi chu kỳ tối đa 3 thay đổi cho một nhân viên để đo được tác dụng; không để prompt phình quá dài (gộp, thay thế thay vì chỉ thêm); không tạo xung đột với nhân viên khác.

## 4. Áp dụng
- Sửa `.claude/agents/<mã>.md` (prompt) và/hoặc bảng **Tiêu chuẩn hoàn thành** trong `team/nhan-su/<mã>/ho-so.md` (trọng số vẫn tổng 100).
- Tăng **Phiên bản prompt** trong hồ sơ (1.0 → 1.1; đổi lớn vai trò → 2.0) và thêm dòng **Lịch sử phiên bản** (ngày, thay đổi, mã chu kỳ).
- Từ nay Bảo ghi `phien_ban` mới vào nhật ký → bảng điểm so được trước/sau.
- Commit: "Nâng cấp đội ngũ <mã-chu-kỳ>: <tên các nhân viên>" rồi push.

## 5. Báo cáo người dùng
Ngắn gọn: ai được nâng cấp, sửa gì, vì sao (1 bằng chứng), đo hiệu quả bằng chỉ số nào. Thay đổi lớn về vai trò hoặc thêm/bớt nhân viên → hỏi người dùng trước khi áp dụng.

## 6. Kiểm tra hiệu quả ở chu kỳ sau
So điểm theo phiên bản trong bảng điểm. Phiên bản mới kém hơn sau ≥ 3 lần chấm → hoàn tác bằng git và ghi lý do vào lịch sử phiên bản.
