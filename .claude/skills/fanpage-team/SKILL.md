---
name: fanpage-team
description: Vận hành mỗi ngày kênh ĐẠO ĐỨC ĐẦU TƯ trên Facebook + TikTok. "kich-ban" (05:05 hằng ngày) — chọn chủ đề, viết caption 2 nền tảng, viết kịch bản 90–180 giây, đưa lên Google Drive cho chủ page quay. "xu-ly" (13:17 và 21:17) — tìm video thô mới trên Drive, edit, đăng Facebook Reel + TikTok, báo cáo. Gọi /fanpage-team kich-ban | xu-ly | <chủ đề>.
---
# Vận hành kênh ĐẠO ĐỨC ĐẦU TƯ mỗi ngày

Đọc trước: `fanpage/config.json`, `fanpage/brand.md`, `fanpage/KENH.md`. Ngày giờ theo `Asia/Ho_Chi_Minh`.
Phiên chính là **trưởng nhóm**: giao việc cho nhân viên (Agent tool), sau mỗi phần việc gọi **Bảo – Giám sát** (`giam-sat`) chấm theo hồ sơ `team/nhan-su/<mã>/ho-so.md`; CHƯA ĐẠT → trả lại đúng người kèm phản hồi (tối đa 3 vòng). Chỉ trưởng nhóm gọi công cụ Google Drive (nhân viên không có).

## Chế độ `kich-ban` (05:05 mỗi ngày, hoặc khi được gọi kèm chủ đề)
1. `DAY=$(TZ=Asia/Ho_Chi_Minh date +%F)`, `RUN=fanpage/runs/$DAY`, `mkdir -p $RUN`.
2. Lịch sử chủ đề: `search_files` với `parentId = '<scripts_folder_id>'` → tên file dạng `YYYY-MM-DD | chuyên mục | chủ đề`. Ghi danh sách 30 ngày gần nhất vào `$RUN/lich-su.txt` cho Ngọc (Ngọc không đọc Drive được). Đã có kịch bản của hôm nay → dừng, không làm trùng.
3. **Ngọc** (`y-tuong-content`): "run_dir=$RUN. Chế độ fanpage. Lịch sử chủ đề ở $RUN/lich-su.txt. Chọn chủ đề theo chuyên mục của thứ hôm nay trong KENH.md[, chủ đề bắt buộc: …]. Nộp ideas.json, post.md, tiktok.md." → Bảo chấm.
4. **Phong** (`kich-ban-quay`): "run_dir=$RUN. Kịch bản 90–180 giây, hướng dẫn quay, edit_plan.json." → Bảo chấm.
5. Đưa kịch bản lên Drive: `create_file` với `parentId = scripts_folder_id`, `contentMimeType: text/plain` (để Drive đổi thành Google Doc), tiêu đề `$DAY | <chuyên mục> | <chủ đề>`, nội dung = phần teleprompter + checklist ngắn trong `huong_dan_quay.md`, đầu file ghi: "QUAY XONG: bỏ video vào thư mục '2. Video thô - bỏ video quay vào đây'".
6. Commit + push thư mục `fanpage/` nếu được (không có video). Kết thúc bằng một dòng: chủ đề hôm nay + link Google Doc (dòng này là nội dung thông báo gửi về điện thoại).

## Chế độ `xu-ly` (13:17 và 21:17 mỗi ngày, hoặc /fanpage-team xu-ly)
1. `search_files`: `parentId = '<raw_folder_id>' and mimeType contains 'video/'`. Không có file → kết thúc ngay với "Chưa có video mới." (không gọi nhân viên nào).
2. Ghép video với kịch bản: kịch bản mới nhất trong `scripts_folder` chưa được đăng (chưa có dòng `posted` trong `fanpage/memory/history.jsonl`, hoặc ngày ≥ ngày của kịch bản gần nhất đã đăng). Không có repo state cho ngày đó (phiên mới) → đọc Google Doc kịch bản bằng `read_file_content`, ghi lại `$RUN/kichban.txt`; tạo lại `edit_plan.json`, `post.md`, `tiktok.md` bằng cách giao **Phong** và **Ngọc** làm lại từ kịch bản đó (không đổi lời thoại).
3. Chia sẻ từng video thô: `share_file` `permissionId: anyoneWithLink`, `role: reader`.
4. **Khoa** (`edit-video`): "run_dir=$RUN. Video thô: <danh sách id + tên theo thứ tự>. Tải bằng drive.usercontent, edit theo edit_plan.json." → Bảo chấm. Gửi video cho người dùng bằng SendUserFile nếu phiên có công cụ đó.
5. **Vy** (`dang-link`): "run_dir=$RUN. Đăng Facebook + TikTok theo config (publish_mode)." → Bảo chấm. Kênh TikTok chưa nối đúng `daoducdautu` → Vy bỏ qua TikTok và báo; Facebook vẫn đăng.
6. Chuyển video thô đã xử lý vào `processed_folder_id` (`update_file` đổi `parentId`) — chỉ khi Vy đăng thành công ít nhất một kênh.
7. **Quân** (`tra-loi-bao-cao`): báo cáo ngày (số liệu Facebook + TikTok, KPI trong KENH.md, trả lời bình luận mẫu). **Hà** (`kiem-dinh`) rà nhanh caption và publish.json.
8. `python3 team/tools/bang_diem.py`; commit + push (không có video). Kết thúc bằng một dòng: kênh nào đã đăng lúc mấy giờ, link, việc chủ page cần làm (nếu có lỗi).

## Quy tắc
- Không bao giờ đăng Instagram hay TikTok/Instagram của brand 7808796 (Mr Pump). Xem `never_post_to`.
- Không đẩy video thô hay video đã edit vào repo DRK (repo công khai). Video đã edit chỉ đi qua `media_repo` và bị xoá sau khi Metricool sao chép.
- Lỗi ở bước nào → dừng các bước phụ thuộc, ghi lỗi vào dòng kết thúc để thông báo cho chủ page.
