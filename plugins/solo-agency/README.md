# Solo Agency: phòng ban AI cho doanh nghiệp một người

Một plugin Claude Code gồm 10 "nhân sự" AI, giúp một người vận hành cả agency xây thương hiệu cá nhân.

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
| Bản sao AI | `ai-twin` | Trả lời tin nhắn bằng giọng, gương mặt và kiến thức của bạn |
| Kiểm soát Tuân thủ | `compliance-reviewer` | Rà nội dung tài chính, crypto: không hứa lợi nhuận, không tư vấn cá nhân, có công khai AI |

## Cài đặt (1 phút)

Trong Claude Code, mở thư mục dự án của bạn rồi gõ:

```
/plugin marketplace add nguyentv2912/DRK
/plugin install solo-agency@drk
```

Sau đó khởi động lại Claude Code.

## Bắt đầu

1. `/solo-agency:thiet-lap`: trả lời phỏng vấn để tạo hồ sơ thương hiệu trong `brand/`. Mọi phòng ban đều đọc hồ sơ này, nên mỗi người cài sẽ có một phòng ban mang đúng giọng của mình.
2. `/solo-agency:ke-hoach-tuan`: kế hoạch tuần gồm 5 video, lịch đăng 7 ngày và danh sách lead cần follow-up.
3. `/solo-agency:giao-viec <mục tiêu>`: giao việc lớn cho cả phòng ban. Ví dụ: `/solo-agency:giao-viec ra mắt khóa học Canva cơ bản giá 399k trong 14 ngày`.
4. `/solo-agency:tra-loi-binh-luan <dán bình luận>`: soạn trả lời bình luận hàng loạt.
5. `/solo-agency:bao-cao tuan`: báo cáo hiệu quả và 3 việc nên làm tiếp.
6. `/solo-agency:tao-ban-sao`: tạo Bản sao AI của bạn (chuyên môn, quan điểm, câu chuyện, giới hạn) và danh sách 20 video trả lời cần quay sẵn.
7. `/solo-agency:tra-loi-tin-nhan <dán tin nhắn>`: Bản sao AI trả lời bằng chữ, kèm video có sẵn hoặc kịch bản để tạo video gương mặt bạn; tự rà soát tuân thủ trước khi đưa bạn duyệt.

### Bản sao AI trả lời bằng video gương mặt của bạn

| Cấp | Cách làm | Chi phí | Thời gian |
|---|---|---|---|
| 1. Thư viện video quay sẵn | Bạn quay 20 video trả lời câu hỏi hay gặp; bản sao chọn đúng video để gửi | Miễn phí | Gửi ngay |
| 2. Video AI theo yêu cầu | Bản sao viết `kichban.txt`, bạn chạy notebook clone giọng và khớp môi trên Kaggle | Miễn phí (GPU Kaggle) | 20–30 phút/video |
| 3. Gọi video trực tiếp | Avatar thời gian thực (HeyGen Interactive, Tavus, D-ID…) | Tính phí theo phút | Trực tiếp |

Video do AI tạo luôn kèm dòng chữ "Video trả lời bởi trợ lý AI của <tên>".

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
- **Tài chính và crypto chỉ ở mức giáo dục:** bản sao không bảo ai mua hay bán gì, không hứa lợi nhuận, không nhận giữ tiền, không bao giờ hỏi seed phrase. Muốn bán dịch vụ tư vấn cá nhân, nhóm tín hiệu hay quản lý vốn thì hỏi luật sư trước.
- **Minh bạch về AI:** khi khách hỏi, trợ lý nói thật nó là AI (có thể chỉnh trong `brand/thuong-hieu.md`).
- **Bảo mật:** không xin mật khẩu, OTP hay số thẻ. Không đưa dữ liệu khách lên nội dung công khai.

## Giới hạn hiện tại

- Trả lời bình luận tự động 24/7 trên Facebook/TikTok cần nối API của từng nền tảng (ví dụ qua Make.com). Bản này soạn trả lời để bạn duyệt rồi đăng.
- Video: phòng ban viết kịch bản và storyboard; dựng video dùng quy trình riêng của bạn.

## Nhân bản cho người khác

Người khác chỉ cần chạy 2 lệnh ở phần Cài đặt rồi `/solo-agency:thiet-lap` với thông tin của họ. Muốn sửa phòng ban (thêm người, đổi quy trình), hãy fork repo, sửa file trong `plugins/solo-agency/agents/` hoặc `commands/`, rồi chia sẻ repo của bạn.
