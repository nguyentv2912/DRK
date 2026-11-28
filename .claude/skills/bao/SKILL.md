---
name: bao
description: Làm việc trực tiếp với Bảo (Chấm điểm phần việc của nhân viên). Chủ kênh gõ /bao <việc> hoặc gọi "Bảo ơi …" để giao việc riêng cho Bảo, không qua chia việc của Minh.
---
# Làm việc riêng với Bảo

Hồ sơ: `team/nhan-su/giam-sat/ho-so.md` · Prompt: `.claude/agents/giam-sat.md` · Nhật ký: `team/nhan-su/giam-sat/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Bảo: gọi Agent với `subagent_type: "giam-sat"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Bảo hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Bảo trong cùng phiên, gửi tiếp cho đúng Bảo (SendMessage) thay vì gọi mới, để Bảo nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Bảo:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/giam-sat/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
