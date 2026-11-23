---
name: fanpage-team
description: Vận hành mỗi ngày kênh ĐẠO ĐỨC ĐẦU TƯ trên Facebook + TikTok (5 bài/ngày: 2 video + 3 ảnh/chữ). "ke-hoach-tuan" (Chủ Nhật) — 21 bài ảnh/chữ cho tuần tới chờ anh duyệt; "len-lich-tuan" — lên lịch tuần đã duyệt. "kich-ban" (05:05 hằng ngày) — giữ kho luôn có 3 kịch bản 90–180 giây chưa quay trên Google Drive. "xu-ly" (09:17, 10:17 và 21:17) — tìm các video thô mới, tự ghép với kịch bản, edit, xếp lịch đăng Facebook Reel + TikTok (tối đa 2 bài/ngày), báo cáo. Gọi /fanpage-team kich-ban | xu-ly | <chủ đề>.
---
# Vận hành kênh ĐẠO ĐỨC ĐẦU TƯ mỗi ngày

Đọc trước: `fanpage/config.json`, `fanpage/brand.md`, `fanpage/KENH.md`. Ngày giờ theo `Asia/Ho_Chi_Minh`.
Phiên chính là **trưởng nhóm**: giao việc cho nhân viên (Agent tool), sau mỗi phần việc gọi **Bảo – Giám sát** (`giam-sat`) chấm theo hồ sơ `team/nhan-su/<mã>/ho-so.md`; CHƯA ĐẠT → trả lại đúng người kèm phản hồi (tối đa 3 vòng). Chỉ trưởng nhóm gọi công cụ Google Drive (nhân viên không có).

## Chế độ `kich-ban` (05:05 mỗi ngày, hoặc khi được gọi) — giữ kho luôn có 3 kịch bản chưa quay
Chủ kênh có thể quay 2–3 video một ngày, nên luôn phải có sẵn kịch bản.
1. `search_files` với `parentId = '<scripts_folder_id>'` và không phải thư mục → các kịch bản **chưa quay** (tên `KB-YYYYMMDD-N | chuyên mục | chủ đề`). Thêm `search_files` trong `scripts_done_folder_id` → các kịch bản **đã quay**. Ghi cả hai danh sách (30 ngày gần nhất) vào `fanpage/runs/lich-su.txt` cho Ngọc.
2. `can_viet = script_buffer (3) − số kịch bản chưa quay`. Bằng 0 → kết thúc: "Kho đang có 3 kịch bản chưa quay." Có chủ đề bắt buộc từ người dùng → viết thêm 1 bài dù kho đã đủ.
3. Với mỗi bài cần viết (lần lượt, bài sau tránh trùng chủ đề và chuyên mục với bài trước): mã `KB-<ngày hôm nay YYYYMMDD>-<N>` (N tiếp theo trong ngày), `RUN=fanpage/runs/<mã>`.
   - Chuyên mục: bài thứ k lấy chuyên mục của **ngày đăng dự kiến** (hôm nay + k − 1 theo lịch trong KENH.md).
   - **Ngọc** (`y-tuong-content`): "run_dir=$RUN. Chế độ fanpage. Lịch sử ở fanpage/runs/lich-su.txt. Chuyên mục: … Nộp ideas.json, post.md, tiktok.md." → Bảo chấm.
   - **Phong** (`kich-ban-quay`): "run_dir=$RUN. Kịch bản 90–180 giây, hướng dẫn quay, edit_plan.json." → Bảo chấm.
   - `create_file` lên `scripts_folder_id`, `contentMimeType: text/plain`, tiêu đề `<mã> | <chuyên mục> | <chủ đề>`, nội dung = teleprompter + checklist ngắn; dòng đầu: "QUAY XONG: bỏ video vào thư mục '2. Video thô'. Không cần đặt tên file."
4. Commit + push `fanpage/`. Kết thúc bằng một dòng: "Kho có <n> kịch bản chưa quay: <danh sách mã + chủ đề + link>".

## Chế độ `xu-ly` (09:17, 10:17 và 21:17 mỗi ngày — có thể có nhiều video)
1. `search_files`: `parentId = '<raw_folder_id>' and mimeType contains 'video/'`. Không có → kết thúc "Chưa có video mới."
2. Tải về và ghép với kịch bản:
   - `share_file` từng video (anyoneWithLink, reader) rồi `curl` về `fanpage/runs/raw-<ngày>/` (cách tải trong config).
   - Lấy danh sách kịch bản chưa quay (scripts_folder, không tính "Đã quay"). Với kịch bản không có thư mục `fanpage/runs/<mã>/` trong repo: đọc Google Doc bằng `read_file_content`, ghi `fanpage/runs/<mã>/kichban.txt`.
   - Mỗi video: `python3 fanpage/tools/edit_video.py transcribe <video> <video>.json --model small`, rồi `python3 fanpage/tools/khop_kich_ban.py <video>.json fanpage/runs/*/kichban.txt` (chỉ các kịch bản chưa quay).
   - `chac_chan: true` → gán video cho kịch bản đó. Nhiều file cùng khớp một kịch bản → là các đoạn của một video, ghép theo thứ tự tên file. Không chắc chắn → **không xử lý video đó**, ghi vào dòng kết thúc để chủ kênh xem (có thể là quay ngoài kịch bản).
3. Với mỗi kịch bản có video (theo thứ tự mã KB tăng dần), `RUN=fanpage/runs/<mã>`:
   - Thiếu `edit_plan.json`, `post.md`, `tiktok.md` (phiên mới) → giao **Phong** tạo lại edit_plan từ kichban.txt và **Ngọc** viết lại caption (không đổi lời thoại) → Bảo chấm.
   - Chép transcript vào `$RUN/transcript.json`. **Khoa** (`edit-video`): "run_dir=$RUN. Video thô đã tải: <đường dẫn>. transcript.json đã có, không cần bóc lời lại." → Bảo chấm.
4. **Vy** (`dang-link`): đưa danh sách các `$RUN` đã edit xong theo thứ tự; Vy xếp mỗi video vào khung trống sớm nhất (tối đa 2 bài/ngày, video dư sang các ngày sau) → Bảo chấm.
5. Video đã hẹn đăng thành công ít nhất một kênh → chuyển video thô vào `processed_folder_id` và chuyển Google Doc kịch bản vào `scripts_done_folder_id` (`update_file` đổi `parentId`).
6. **Quân** báo cáo; **Hà** rà nhanh caption và publish.json. Chủ Nhật lượt 21:17: gọi **Trang** (`phan-bien`) chế độ A cho cả tuần. `python3 team/tools/bang_diem.py`; commit + push (không có video).
7. Kết thúc bằng một dòng: mỗi video → mã kịch bản, kênh, giờ hẹn đăng; video không ghép được (nếu có); kho còn mấy kịch bản chưa quay.

## Chế độ `ke-hoach-tuan` (Chủ Nhật 05:05, hoặc khi được gọi) — 21 bài ảnh/chữ cho tuần tới
Kế hoạch gốc: `team/viec/2026-11-23-he-thong-dang-bai/ke-hoach.md`. Mã tuần `T-<YYYYMMDD của Thứ Hai>`, `RUN=fanpage/tuan/<mã>`.
1. Quân (`tra-loi-bao-cao`) lấy số liệu 7 ngày qua (Metricool), chọn top 5 bài → `RUN/so-lieu.md`.
2. Ngọc (`y-tuong-content`, theo skill `viet-bai-dao-duc-dau-tu` và sổ tay) viết `RUN/ke-hoach.json`: 21 bài = 7 ngày × 3 khung (06:30, 09:30, 17:00) theo tỷ lệ tuần: 4 chữ nền màu (Metricool không đăng được nền màu của Facebook → làm thành ảnh bằng `tao_anh.py` loại `nen_mau`), 4 chữ ngắn, 3 chữ dài, 4 ảnh trích dẫn, 2 infographic, 2 album, (+2 bài chữ thay chỗ nếu thiếu ý). Mỗi bài: `ngay, gio, loai, text (caption), anh (spec cho tao_anh.py nếu có)`. Có 3 bài làm lại từ top 5, 2 bài "chép mô hình" (không chép chữ) từ bài thắng cùng ngách. Mỗi ngày khác dạng, không lặp chủ đề với 14 ngày gần nhất.
3. Tùng/trưởng nhóm chạy `python3 fanpage/tools/tao_anh.py <spec> RUN/anh/` cho các bài có ảnh. Ảnh không mặt người → được commit.
4. Bảo chấm + Trang rà (không hứa lãi, không mã/coin, không số tiền trên ảnh, không câu "like nếu đồng ý", không nhắc thương hiệu lớn). Sửa xong mới gửi anh.
5. `create_file` lên `weekly_plan_folder_id` (text/plain → Google Doc; thay mọi ký tự ngoài BMP như 🏠📈📌 bằng [icon …] trước khi tải lên, nếu không Doc hiện chữ 'ð'): Google Doc "KẾ HOẠCH TUẦN <dd/mm–dd/mm> – CHỜ DUYỆT" (bảng 21 bài: ngày, giờ, dạng, caption, link ảnh trên GitHub) + tải ảnh lên cùng thư mục. Kết thúc một dòng: "Kế hoạch tuần chờ anh duyệt: <link>. Duyệt: đổi tên file thành '… – ĐÃ DUYỆT' hoặc nhắn 'duyệt tuần'."

## Chế độ `len-lich-tuan` (mỗi lượt 05:05 kiểm tra; hoặc khi anh nhắn "duyệt tuần")
Tìm trong `weekly_plan_folder_id` file "KẾ HOẠCH TUẦN … – ĐÃ DUYỆT" chưa có `RUN/da-len-lich.json`. Có → Vy (`dang-link`) xếp lịch từng bài ảnh/chữ lên Facebook qua Metricool đúng ngày giờ (ảnh qua `media_repo` hoặc link raw GitHub của `RUN/anh/`), ghi `RUN/da-len-lich.json`, đổi nội dung báo cáo: "Đã lên lịch <n>/21 bài tuần <mã>". Anh sửa trong Doc trước khi đổi tên thì lấy nội dung chữ trong Doc làm chuẩn, nhưng khôi phục biểu tượng từ ke-hoach.json (Doc thay biểu tượng 4-byte như 🏠📈📌 bằng [icon …] vì Google Doc hiển thị lỗi).

## Chế độ `video-ngan` (05:05 mỗi ngày) — đội TỰ LÀM và TỰ ĐĂNG 1 video ngắn, không gửi anh duyệt (anh chốt 23/11)
Video không có mặt anh: chữ động trên nền thương hiệu, nhạc nền, âm thanh hiệu ứng (`fanpage/tools/video_ngan.py`). `RUN=fanpage/runs/VN-<YYYYMMDD>`.
1. Ngọc (`y-tuong-content`, theo skill `viet-bai-dao-duc-dau-tu` + sổ tay) chọn 1 chủ đề không trùng 14 ngày gần nhất (kể cả bài ảnh/chữ trong `fanpage/tuan/`), viết `RUN/spec.json` (hook ≤ 10 chữ, 3 ý ngắn ≤ 8 chữ + dòng phụ ≤ 14 chữ, trích dẫn kinh điển đúng xuất xứ nếu có, theo mạch Đạo – Đời – Đầu tư) và `RUN/post.md` (caption Facebook 60–120 chữ + câu "Theo dõi page…" + miễn trừ + hashtag có #daoducdautu), `RUN/tiktok.md`.
2. Khoa (`edit-video`) chạy `python3 fanpage/tools/video_ngan.py RUN/spec.json RUN/video.mp4`, xem 3 khung hình (đầu, giữa, cuối) — chữ không tràn, không lỗi dấu.
3. Bảo (`giam-sat`) chấm + Trang (`phan-bien`) rà nhanh: không hứa lãi, không mã/coin/số tiền, không trùng ý tuần. CHƯA ĐẠT → sửa (tối đa 2 vòng); vẫn chưa đạt → KHÔNG đăng, báo lỗi.
4. Vy (`dang-link`) đăng **tự động** (không nháp) Facebook Reel khung 11:30 hôm nay (TikTok cùng giờ nếu brand TikTok đã xác nhận đúng daoducdautu). Nếu khung 11:30 đã có video anh quay thì dời sang khung trống kế tiếp, tối đa 2 video/ngày.
5. Ghi `RUN/ket-qua.json`, commit `RUN/` (trừ video.mp4). Báo một dòng: "Video ngắn hôm nay: <chủ đề> – <giờ đăng>".

## Quy tắc
- Không bao giờ đăng Instagram hay TikTok/Instagram của brand 7808796 (Mr Pump). Xem `never_post_to`.
- Không đẩy video thô hay video đã edit vào repo DRK (repo công khai). Video đã edit chỉ đi qua `media_repo` và bị xoá sau khi Metricool sao chép.
- Lỗi ở bước nào → dừng các bước phụ thuộc, ghi lỗi vào dòng kết thúc để thông báo cho chủ page.
