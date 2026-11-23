# Mẫu và thiết kế

Mẫu gốc: video dọc 576×1024, 30 fps, 87.47 giây. Đầu video có “9 CHUYỂN ĐỘNG ĐƠN GIẢN” chữ trắng đậm, dòng vàng “giúp giảm ngay ‘đau’ lưng dưới”, viền đen/bóng tối. Tiêu đề nằm khoảng 1/4 phía trên. Có thêm dòng CTA phía dưới và các dòng hướng dẫn về sau; **yêu cầu mới chỉ dùng tiêu đề**, nên không sao chép CTA, hướng dẫn hay watermark TikTok của mẫu.

Bản test: 1080×1920, 15 giây; bản đầu đặt y=155; yêu cầu mới đặt tâm cụm chữ ở 2/3 chiều cao (y≈1280 ở 1920px), tọa độ đầu cụm tự tính từ chiều cao chữ. Main trắng uppercase, supporting vàng #EBFF2D giữ nguyên nội dung. TT Commons Pro ExtraBold cỡ 76/54 px, viền 4 px, bề rộng 960 px. Nền bóng đen mềm chỉ sau khu vực tiêu đề. Chữ vàng có tỷ lệ 0.72; bước dòng chính bằng font_size−4 và bước dòng vàng bằng support_size+4, giúp hai phần gần nhau. Cỡ chữ tự giảm khi cần nhưng phải kiểm tra khả năng đọc. Các thông số này là khởi điểm có thể đổi, không phải mẫu đã được duyệt.

Nhạc dùng file người dùng cung cấp, bỏ âm thanh gốc footage; normalize khoảng −18 LUFS/peak −2 dBTP, fade-in 0.4 s và fade-out 1 s. Không thêm voice hoặc tiếng gõ. Nếu clip ngắn hơn đầu ra, loop khi hợp lý và nêu rõ; có thể chọn clip dài hơn để tránh điểm nối lặp. Crop giữa là mặc định engine, thay tâm crop nếu che chủ thể.

Font đi kèm đã kiểm tra glyph cho danh sách tiêu đề hiện tại, nhưng font không giống hoàn toàn font condensed trong mẫu. Mỗi font thay thế phải kiểm tra toàn bộ ký tự trước render.

Chỉnh sửa mới nhất của người dùng: “Phần chữ màu vàng cho khoảng cách gần hơn chút, nhỏ hơn 1 chút để tạo nổi bật key chính. Đưa thấp xuống 2/3 video”. Cỡ 72% và tâm 2/3 là cách triển khai của trợ lý; chưa có phản hồi duyệt bản sửa.
