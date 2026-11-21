---
name: tung
description: Làm việc trực tiếp với Tùng (Trang demo, dashboard, landing page). Chủ kênh gõ /tung <việc> hoặc gọi "Tùng ơi …" để giao việc riêng cho Tùng, không qua chia việc của Minh.
---
# Làm việc riêng với Tùng

Hồ sơ: `team/nhan-su/thiet-ke-demo/ho-so.md` · Prompt: `.claude/agents/thiet-ke-demo.md` · Nhật ký: `team/nhan-su/thiet-ke-demo/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Tùng: gọi Agent với `subagent_type: "thiet-ke-demo"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Tùng hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Tùng trong cùng phiên, gửi tiếp cho đúng Tùng (SendMessage) thay vì gọi mới, để Tùng nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Tùng:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/thiet-ke-demo/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
