# Solo Agency: phòng ban AI cho doanh nghiệp một người

Một plugin Claude Code gồm 8 "nhân sự" AI, giúp một người vận hành cả agency xây thương hiệu cá nhân.

| Phòng ban | Agent | Việc chính |
|---|---|---|
| Sản xuất Video | `video-producer` | Ý tưởng, kịch bản, hook, storyboard |
| Nội dung và Đăng bài | `social-publisher` | Lịch nội dung, caption, lên lịch qua Buffer/Metricool |
| Cộng đồng | `community-manager` | Phân loại và trả lời bình luận |
| Chăm sóc Khách hàng | `customer-care` | Hỗ trợ sau bán, khiếu nại, FAQ |
| Tư vấn Bán hàng | `sales-consultant` | Tư vấn, xử lý từ chối, follow-up, phễu |
| IT và Website | `web-developer` | Landing page bán hàng chuyển đổi |
| Đào tạo | `course-creator` | Khóa học, bài giảng, quiz, workbook |
| Phân tích Số liệu | `data-analyst` | Báo cáo tuần/tháng, đề xuất |

## Cài đặt (1 phút)

Trong Claude Code, mở thư mục dự án của bạn rồi gõ:

```
/plugin marketplace add nguyentv2912/drk
/plugin install solo-agency@drk
```

Sau đó khởi động lại Claude Code.

## Bắt đầu

1. `/solo-agency:thiet-lap`: trả lời phỏng vấn để tạo hồ sơ thương hiệu trong `brand/`. Mọi phòng ban đều đọc hồ sơ này, nên mỗi người cài sẽ có một phòng ban mang đúng giọng của mình.
2. `/solo-agency:ke-hoach-tuan`: kế hoạch tuần gồm 5 video, lịch đăng 7 ngày và danh sách lead cần follow-up.
3. `/solo-agency:giao-viec <mục tiêu>`: giao việc lớn cho cả phòng ban. Ví dụ: `/solo-agency:giao-viec ra mắt khóa học Canva cơ bản giá 399k trong 14 ngày`.
4. `/solo-agency:tra-loi-binh-luan <dán bình luận>`: soạn trả lời bình luận hàng loạt.
5. `/solo-agency:bao-cao tuan`: báo cáo hiệu quả và 3 việc nên làm tiếp.

Bạn cũng có thể gọi thẳng từng nhân sự, ví dụ: "nhờ web-developer làm landing page cho gói coaching".

## Thư mục làm việc

```
brand/       hồ sơ thương hiệu: giọng văn, sản phẩm, chính sách, kênh, FAQ
content/     video, bài đăng, lịch nội dung
outbox/      mọi thứ sắp gửi ra ngoài, chờ bạn duyệt
customers/   lead và lịch sử hỗ trợ (nên đưa vào .gitignore)
website/     landing page
courses/     khóa học
reports/     báo cáo
```

## Nguyên tắc an toàn

- **Bạn duyệt trước khi gửi.** Phòng ban chỉ soạn nháp vào `outbox/`. Bài đăng, tin nhắn cho khách, hoàn tiền hay giảm giá đều cần bạn duyệt.
- **Không bịa:** không bịa số liệu, lời chứng thực, kết quả hay khan hiếm giả. Chỗ thiếu bằng chứng được đánh dấu `[CẦN SỐ LIỆU THẬT]`.
- **Minh bạch về AI:** khi khách hỏi, trợ lý nói thật nó là AI (có thể chỉnh trong `brand/thuong-hieu.md`).
- **Bảo mật:** không xin mật khẩu, OTP hay số thẻ. Không đưa dữ liệu khách lên nội dung công khai.

## Giới hạn hiện tại

- Trả lời bình luận tự động 24/7 trên Facebook/TikTok cần nối API của từng nền tảng (ví dụ qua Make.com). Bản này soạn trả lời để bạn duyệt rồi đăng.
- Video: phòng ban viết kịch bản và storyboard; dựng video dùng quy trình riêng của bạn.

## Nhân bản cho người khác

Người khác chỉ cần chạy 2 lệnh ở phần Cài đặt rồi `/solo-agency:thiet-lap` với thông tin của họ. Muốn sửa phòng ban (thêm người, đổi quy trình), hãy fork repo, sửa file trong `plugins/solo-agency/agents/` hoặc `commands/`, rồi chia sẻ repo của bạn.
