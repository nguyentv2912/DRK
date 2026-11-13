---
description: Thiết lập phòng ban AI cho thương hiệu của bạn (chạy 1 lần đầu tiên, hoặc khi muốn cập nhật hồ sơ)
---

Bạn đang thiết lập **Solo Agency**, phòng ban AI cho một doanh nghiệp một người. Hãy phỏng vấn chủ doanh nghiệp rồi tạo bộ hồ sơ thương hiệu mà mọi phòng ban sẽ đọc.

## Bước 1: Phỏng vấn
Hỏi **từng nhóm một** (không hỏi dồn), bằng ngôn ngữ chủ đang dùng. Nếu thư mục `brand/` đã có, đọc trước và chỉ hỏi phần còn thiếu hoặc chủ muốn sửa.

1. **Bạn là ai:** tên thương hiệu, lĩnh vực chuyên môn, câu chuyện ngắn, điều làm bạn khác biệt.
2. **Khách hàng:** ai, độ tuổi, nghề nghiệp, nỗi đau lớn nhất, mong muốn lớn nhất, họ ở nền tảng nào.
3. **Giọng thương hiệu:** xưng hô (tôi/mình/anh/em…), 3 tính từ mô tả giọng, từ hay dùng, từ cấm dùng, có dùng emoji không. Khi khách hỏi "có phải bot không" thì trả lời thế nào (khuyến nghị: nói thật là trợ lý AI của thương hiệu).
4. **Sản phẩm/dịch vụ:** tên, giá, quyền lợi, ai nên mua, ai không nên mua, chương trình ưu đãi đang chạy, link thanh toán/đăng ký.
5. **Chính sách:** đổi trả, hoàn tiền, bảo hành, thời gian phản hồi, kênh liên hệ.
6. **Kênh:** TikTok, Facebook, Instagram, YouTube, X, Zalo, email, website… Mỗi kênh: link, tần suất đăng, giờ đăng. Có cho phép tự động đăng không (khuyến nghị: không, duyệt từng bài).
7. **FAQ:** 5–10 câu khách hay hỏi kèm câu trả lời.
8. **Mục tiêu 90 ngày:** ví dụ số người theo dõi, số lead, doanh thu.

## Bước 2: Tạo file
Tạo các file sau (tiêu đề và mục bằng tiếng Việt). Thông tin chủ chưa trả lời thì ghi `[CHƯA CÓ]`, không tự bịa:

- `brand/thuong-hieu.md`: nhóm 1, 2, 3 và 8.
- `brand/san-pham.md`: nhóm 4.
- `brand/chinh-sach.md`: nhóm 5.
- `brand/kenh.md`: nhóm 6, có dòng `tu_dong_dang: khong` (hoặc `co` nếu chủ chọn).
- `brand/faq.md`: nhóm 7.

Tạo thêm các thư mục làm việc, mỗi thư mục có một file `.gitkeep`: `content/video/`, `content/bai-dang/`, `content/lich/`, `outbox/`, `customers/`, `website/`, `courses/`, `reports/`.

Tạo `customers/leads.md` với bảng trống: Ngày | Tên | Kênh | Nhu cầu | Trạng thái | Hẹn liên hệ lại.

## Bước 3: Chào phòng ban
Giới thiệu ngắn 8 nhân sự và việc đầu tiên mỗi người có thể làm ngay cho thương hiệu này. Gợi ý chủ chạy tiếp `/solo-agency:ke-hoach-tuan`.

Nhắc chủ rằng `customers/` có thể chứa thông tin khách hàng. Nếu chia sẻ thư mục này công khai thì nên thêm `customers/` vào `.gitignore`.
