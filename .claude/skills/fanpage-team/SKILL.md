---
name: fanpage-team
description: Vận hành mỗi ngày kênh ĐẠO ĐỨC ĐẦU TƯ trên Facebook + TikTok. "kich-ban" (05:05 hằng ngày) — giữ kho luôn có 3 kịch bản 90–180 giây chưa quay trên Google Drive. "xu-ly" (09:17, 10:17 và 21:17) — tìm các video thô mới, tự ghép với kịch bản, edit, xếp lịch đăng Facebook Reel + TikTok (tối đa 2 bài/ngày), báo cáo. Gọi /fanpage-team kich-ban | xu-ly | <chủ đề>.
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

## Quy tắc
- Không bao giờ đăng Instagram hay TikTok/Instagram của brand 7808796 (Mr Pump). Xem `never_post_to`.
- Không đẩy video thô hay video đã edit vào repo DRK (repo công khai). Video đã edit chỉ đi qua `media_repo` và bị xoá sau khi Metricool sao chép.
- Lỗi ở bước nào → dừng các bước phụ thuộc, ghi lỗi vào dòng kết thúc để thông báo cho chủ page.
