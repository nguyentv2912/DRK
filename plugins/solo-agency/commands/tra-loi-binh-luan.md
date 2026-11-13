---
description: Phân loại và soạn trả lời cho một loạt bình luận hoặc tin nhắn (dán vào hoặc chỉ đường dẫn file)
argument-hint: <dán bình luận, hoặc đường dẫn file CSV/TXT>
---

Giao cho subagent `community-manager` xử lý lô bình luận sau:

$ARGUMENTS

Nếu trống, yêu cầu chủ dán bình luận (mỗi dòng gồm tên người bình luận và nội dung) hoặc chỉ đường dẫn file xuất từ nền tảng.

Sau khi nhận kết quả:
1. Cho chủ xem bảng trả lời đề xuất, gom các mục **Chuyển chủ** lên đầu.
2. Tin nhắn riêng của khách đã mua thì giao thêm cho `customer-care`. Lead nóng thì giao cho `sales-consultant` soạn tin nhắn riêng.
3. Hỏi chủ duyệt: tất cả, từng mục, hoặc sửa. Đã duyệt thì lưu bản cuối vào `outbox/` để chủ dán lên nền tảng (hoặc gửi bằng công cụ đã kết nối, nếu có).
