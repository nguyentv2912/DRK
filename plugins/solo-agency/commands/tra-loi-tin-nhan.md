---
description: Bản sao AI trả lời tin nhắn khách bằng chữ và video gương mặt của bạn; tự rà soát tuân thủ trước khi đưa bạn duyệt
argument-hint: <dán tin nhắn khách, hoặc đường dẫn file>
---

Xử lý các tin nhắn sau:

$ARGUMENTS

Nếu trống, yêu cầu chủ dán tin nhắn (tên khách, kênh, nội dung) hoặc chỉ đường dẫn file.

1. Giao cho subagent `ai-twin` soạn trả lời chữ và chọn hình thức video cho từng tin nhắn.
2. Giao kết quả cho subagent `compliance-reviewer` rà soát. Mục nào bị "SỬA RỒI GỬI" thì trả lại `ai-twin` sửa một lần, theo đúng câu đề xuất.
3. Khách đã mua cần hỗ trợ thì giao thêm cho `customer-care`. Khách muốn mua khóa học hoặc dịch vụ thì giao thêm cho `sales-consultant` soạn bước tiếp theo.
4. Báo cho chủ theo thứ tự:
   - **Cần bạn xử lý trực tiếp** (thua lỗ nặng, tuyệt vọng, khiếu nại, số tiền lớn, nghi lừa đảo).
   - **Sẵn sàng gửi:** trả lời chữ kèm video có sẵn.
   - **Cần tạo video:** danh sách thư mục `outbox/video/...` có `kichban.txt`, kèm hướng dẫn: tải `kichban.txt`, `ref.wav`, `mat.mp4` lên Kaggle rồi chạy notebook tạo video.
5. Hỏi chủ duyệt: tất cả, từng mục, hoặc sửa. Chưa được duyệt thì không gửi gì ra ngoài.
