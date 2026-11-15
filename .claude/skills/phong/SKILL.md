---
name: phong
description: Làm việc trực tiếp với Phong (Kịch bản quay video 90–180 giây). Chủ kênh gõ /phong <việc> hoặc gọi "Phong ơi …" để giao việc riêng cho Phong, không qua chia việc của Minh.
---
# Làm việc riêng với Phong

Hồ sơ: `team/nhan-su/kich-ban-quay/ho-so.md` · Prompt: `.claude/agents/kich-ban-quay.md` · Nhật ký: `team/nhan-su/kich-ban-quay/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Phong: gọi Agent với `subagent_type: "kich-ban-quay"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Phong hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Phong trong cùng phiên, gửi tiếp cho đúng Phong (SendMessage) thay vì gọi mới, để Phong nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Phong:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/kich-ban-quay/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
