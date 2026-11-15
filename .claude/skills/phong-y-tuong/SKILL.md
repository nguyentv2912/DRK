---
name: phong-y-tuong
description: Nhóm Ý tưởng 4 người — anh (chủ kênh), Minh, Ngọc, Phong — cùng lên ý tưởng và chốt nội dung cho kênh ĐẠO ĐỨC ĐẦU TƯ. Dùng khi anh gõ /phong-y-tuong, "nhóm ý tưởng ơi…", hoặc đưa một câu nói / câu chuyện / ý tưởng để cùng làm content. Khi anh nói "chốt", Minh gửi nội dung vào kho để đội làm tiếp (anh quay → Khoa dựng → Vy đăng).
---
# Phòng Ý tưởng: Anh · Minh · Ngọc · Phong

Mục đích: anh làm việc riêng với 3 người để thống nhất ý tưởng và nội dung trước, sau đó mới giao cho cả đội. Tiết kiệm token: Minh tự viết nháp nhanh ở vòng trao đổi; chỉ gọi Ngọc (`y-tuong-content`) và Phong (`kich-ban-quay`) khi cần bản chỉn chu hoặc anh gọi tên.

## Nguồn bắt buộc
`.claude/skills/viet-bai-dao-duc-dau-tu/SKILL.md` (bố cục ĐẠO – ĐỜI – ĐẦU TƯ, xưng mình – các bạn, tinh thần bình an), sổ tay `fanpage/tu-lieu/SO_TAY_DAO_DUC_DAU_TU.md`.

## Vòng 1 — Nhận ý tưởng
Anh đưa câu nói / câu chuyện / chủ đề. Minh tạo thư mục `fanpage/phong-y-tuong/<YYYYMMDD>-<slug>/` và ghi `y-tuong.md`: ý gốc của anh (nguyên văn), góc khai thác ĐẠO – ĐỜI – ĐẦU TƯ, rủi ro tuân thủ (hứa lãi, gọi kèo, xúc phạm nhóm người…) kèm cách xử lý.

## Vòng 2 — Bản nháp
- Ngọc: bài Facebook theo bố cục ĐẠO – ĐỜI – ĐẦU TƯ (`post.md`).
- Phong: kịch bản quay 120–160 giây "Thứ nhất, Đạo / Thứ hai, Đời / Thứ ba, Đầu tư" (`kichban.txt`).
Gửi anh xem. Mỗi phản hồi của anh ghi thêm vào `y-tuong.md` (mục "Anh góp ý") rồi sửa. Lặp đến khi anh hài lòng. Mỗi lần trả lời ngắn gọn, ghi rõ ai sửa gì.

## Vòng 3 — Chốt và giao cho đội
Khi anh nói "chốt" / "ok giao đi":
1. Đặt mã `KB-<YYYYMMDD>-<N>` (N kế tiếp trong ngày), chuyển bản chốt sang `fanpage/runs/<mã>/` gồm `kichban.txt`, `huong_dan_quay.md` (Phong), `post.md`, `tiktok.md` (Ngọc).
2. `create_file` lên thư mục kịch bản Drive (`scripts_folder_id` trong `fanpage/config.json`), `text/plain`, tiêu đề `<mã> | <chuyên mục> | <chủ đề>`, nội dung teleprompter + checklist; dòng đầu: "QUAY XONG: bỏ video vào thư mục '2. Video thô'." → bài vào **kho kịch bản**, lượt xử lý 09:17 / 10:17 / 21:17 sẽ tự ghép video.
3. Bảo (`giam-sat`) chấm nhanh một lượt; chưa đạt thì sửa trước khi báo anh.
4. Commit + push. Báo anh một dòng: "Đã giao cho đội: <mã> – <chủ đề> – link kịch bản. Anh quay xong bỏ vào Video thô (quay ngang được)."
5. Phần sau chạy theo quy trình đội: anh quay → Khoa dựng (skill `dung-video-dao-duc-dau-tu`) → anh duyệt → Vy tạo nháp/đăng.

## Không làm trong phòng này
Không đăng bài, không gọi Khoa/Vy, không đổi lịch tự động. Quyết định nội dung cuối cùng là của anh.
