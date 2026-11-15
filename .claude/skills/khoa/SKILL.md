---
name: khoa
description: Làm việc trực tiếp với Khoa (Dựng video (phụ đề, nhạc, hiệu ứng, minh hoạ)). Chủ kênh gõ /khoa <việc> hoặc gọi "Khoa ơi …" để giao việc riêng cho Khoa, không qua chia việc của Minh.
---
# Làm việc riêng với Khoa

Hồ sơ: `team/nhan-su/edit-video/ho-so.md` · Prompt: `.claude/agents/edit-video.md` · Nhật ký: `team/nhan-su/edit-video/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Khoa: gọi Agent với `subagent_type: "edit-video"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Khoa hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Khoa trong cùng phiên, gửi tiếp cho đúng Khoa (SendMessage) thay vì gọi mới, để Khoa nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Khoa:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/edit-video/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
