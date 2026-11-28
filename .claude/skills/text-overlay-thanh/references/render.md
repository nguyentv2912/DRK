# Engine portable

Python 3.10+, Pillow, fonttools, imageio-ffmpeg. `render.py --plan <json> --output <folder> [--prepare-only] [--batch] [--overwrite]`.

Plan là một object, hoặc list object khi batch. Mỗi mục có:
- `title`, `main`, `supporting`: chữ hiển thị; main/supporting phải giữ nội dung title (chỉ khác hoa thường). Có thể chỉ nhập title để tất cả chữ trắng; nên chọn main/supporting thủ công theo cụm nghĩa.
- `video`, `music`, `font`: đường dẫn tuyệt đối hoặc tương đối từ file plan. Font mặc định lấy từ assets/fonts trong skill.
- `duration` mặc định 15, `width` 1080, `height` 1920, `fps` 30; width/height phải chẵn.
- `font_size` 76, `min_font_size` 44, `support_ratio` 0.72, `text_width` 960, `max_text_height` 410, `anchor` 2/3 (tâm cụm chữ theo chiều cao), `y` tùy chọn để ghi đè, `main_line_gap` −4, `support_line_gap` 4.
- `main_color` white, `support_color` #EBFF2D, `stroke` 4, `shadow_alpha` 135.
- `crop_x`, `crop_y`: biểu thức ffmpeg cho tâm crop nếu cần, mặc định (iw-ow)/2 và (ih-oh)/2.
- `id`: tên đầu ra, chỉ chữ/số/gạch ngang/gạch dưới.

Lệnh mẫu từ thư mục skill:
```
python scripts/render.py --plan example-plan.json --output /duong-dan/test
python scripts/render.py --plan example-plan.json --output /duong-dan/preview --prepare-only
```

Script tạo overlay.png, plan.json, preview đầu/giữa/cuối, MP4 và qc.json cho mục đầu. List nhiều mục vẫn chỉ render mục đầu nếu thiếu --batch. `--batch` chỉ dùng sau yêu cầu rõ từ người dùng. File output đã tồn tại thì dừng, trừ khi --overwrite được chỉ định cho bản sửa.

Dừng khi thiếu nguồn, glyph thiếu, main/supporting đổi nội dung title, chữ không vừa vùng, hoặc ffmpeg thất bại; không xuất chữ mất dấu hay cố rút gọn nội dung. Chuẩn hóa nhạc −18 LUFS, peak −2 dBTP, fade đầu/cuối; bỏ audio của footage. Clip ngắn tự loop, cần báo cho người dùng. Decode và volumedetect hỗ trợ QA nhưng không thay kiểm tra thị giác/nghe. Metadata codec/duration lưu trong qc.json.
