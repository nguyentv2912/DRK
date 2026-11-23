# Cài và nhân bản

## Cài dùng ngay
Giải nén ZIP đầy đủ. Sao chép thư mục `text-overlay-thanh` vào `~/.codex/skills/` hoặc `$CODEX_HOME/skills/` nếu biến này được cấu hình; không ghi đè một skill cùng tên đang có mà chưa kiểm tra. Mở chat mới nếu skill chưa xuất hiện.

Gọi: `$text-overlay-thanh làm 1 video test, dùng tiêu đề số 1 và tài nguyên đi kèm.`
Hoặc: `$text-overlay-thanh dùng tiêu đề [nội dung], video [file], nhạc [file], dựng 1 bản test giống mẫu.`

Để chạy engine ngoài Codex: dùng Python 3.10+, cài `pip install -r requirements.txt` trong virtualenv riêng hoặc target riêng. Dùng ffmpeg có sẵn, hoặc binary do imageio-ffmpeg cung cấp. Không cài toàn hệ thống khi không cần. `example-plan.json` có đường dẫn tương đối được resolve từ chính file plan nên có thể chuyển máy.

## Nhân bản cho người khác
1. Dùng ZIP nhẹ để tránh mang theo thư viện cá nhân; hoặc sao chép bản đầy đủ nếu muốn giữ tài sản và có quyền chia sẻ.
2. Đổi tên thư mục và `name:` trong SKILL.md thành tên lowercase-hyphen dưới 64 ký tự, ví dụ `text-overlay-linh`.
3. Đổi display_name, short_description và `$text-overlay-thanh` trong default_prompt của `agents/openai.yaml` sang tên mới.
4. Thay tài nguyên, sửa font/màu/vị trí/duration trong plan; viết lại references/inputs.md và decisions.md nếu đổi chủ sở hữu để không đưa lựa chọn riêng của Thanh thành yêu cầu của người mới. Có thể giữ phần mẫu phong cách như tư liệu tham khảo.
5. Tạo một bản test với nguồn mới, kiểm tra rồi mới cho phép batch. Nếu skill-creator có sẵn, chạy quick_validate.py; kiểm tra engine với --prepare-only và render thật ít nhất một video.

Không cần tên file nhạc giống Thanh; không cần truy cập Drive của Thanh. Engine nhận đường dẫn bất kỳ, kể cả khoảng trắng và ký tự tiếng Việt. Không đóng gói URL download tạm, binary ffmpeg nền tảng cụ thể, thư viện Python đã cài hoặc dữ liệu bí mật.
