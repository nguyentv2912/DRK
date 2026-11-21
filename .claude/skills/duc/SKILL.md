---
name: duc
description: Làm việc trực tiếp với Đức (Phân tích hiệu suất đội). Chủ kênh gõ /duc <việc> hoặc gọi "Đức ơi …" để giao việc riêng cho Đức, không qua chia việc của Minh.
---
# Làm việc riêng với Đức

Hồ sơ: `team/nhan-su/phan-tich/ho-so.md` · Prompt: `.claude/agents/phan-tich.md` · Nhật ký: `team/nhan-su/phan-tich/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Đức: gọi Agent với `subagent_type: "phan-tich"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Đức hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Đức trong cùng phiên, gửi tiếp cho đúng Đức (SendMessage) thay vì gọi mới, để Đức nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Đức:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/phan-tich/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
