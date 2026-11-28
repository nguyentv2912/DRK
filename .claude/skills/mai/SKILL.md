---
name: mai
description: Làm việc trực tiếp với Mai (Kế hoạch, chiến lược, lộ trình, KPI). Chủ kênh gõ /mai <việc> hoặc gọi "Mai ơi …" để giao việc riêng cho Mai, không qua chia việc của Minh.
---
# Làm việc riêng với Mai

Hồ sơ: `team/nhan-su/chien-luoc/ho-so.md` · Prompt: `.claude/agents/chien-luoc.md` · Nhật ký: `team/nhan-su/chien-luoc/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Mai: gọi Agent với `subagent_type: "chien-luoc"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Mai hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Mai trong cùng phiên, gửi tiếp cho đúng Mai (SendMessage) thay vì gọi mới, để Mai nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Mai:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/chien-luoc/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
