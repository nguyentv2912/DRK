---
name: vy
description: Làm việc trực tiếp với Vy (Lên lịch đăng Facebook/TikTok qua Metricool). Chủ kênh gõ /vy <việc> hoặc gọi "Vy ơi …" để giao việc riêng cho Vy, không qua chia việc của Minh.
---
# Làm việc riêng với Vy

Hồ sơ: `team/nhan-su/dang-link/ho-so.md` · Prompt: `.claude/agents/dang-link.md` · Nhật ký: `team/nhan-su/dang-link/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Vy: gọi Agent với `subagent_type: "dang-link"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Vy hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Vy trong cùng phiên, gửi tiếp cho đúng Vy (SendMessage) thay vì gọi mới, để Vy nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Vy:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/dang-link/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
