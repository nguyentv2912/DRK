---
name: quan
description: Làm việc trực tiếp với Quân (Số liệu kênh, trả lời bình luận, báo cáo). Chủ kênh gõ /quan <việc> hoặc gọi "Quân ơi …" để giao việc riêng cho Quân, không qua chia việc của Minh.
---
# Làm việc riêng với Quân

Hồ sơ: `team/nhan-su/tra-loi-bao-cao/ho-so.md` · Prompt: `.claude/agents/tra-loi-bao-cao.md` · Nhật ký: `team/nhan-su/tra-loi-bao-cao/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Quân: gọi Agent với `subagent_type: "tra-loi-bao-cao"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Quân hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Quân trong cùng phiên, gửi tiếp cho đúng Quân (SendMessage) thay vì gọi mới, để Quân nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Quân:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/tra-loi-bao-cao/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
