---
name: ngoc
description: Làm việc trực tiếp với Ngọc (Ý tưởng & bài viết Facebook/TikTok). Chủ kênh gõ /ngoc <việc> hoặc gọi "Ngọc ơi …" để giao việc riêng cho Ngọc, không qua chia việc của Minh.
---
# Làm việc riêng với Ngọc

Hồ sơ: `team/nhan-su/y-tuong-content/ho-so.md` · Prompt: `.claude/agents/y-tuong-content.md` · Nhật ký: `team/nhan-su/y-tuong-content/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Ngọc: gọi Agent với `subagent_type: "y-tuong-content"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Ngọc hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Ngọc trong cùng phiên, gửi tiếp cho đúng Ngọc (SendMessage) thay vì gọi mới, để Ngọc nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Ngọc:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/y-tuong-content/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
