---
name: trang
description: Làm việc trực tiếp với Trang (Phản biện, góp ý nâng cấp). Chủ kênh gõ /trang <việc> hoặc gọi "Trang ơi …" để giao việc riêng cho Trang, không qua chia việc của Minh.
---
# Làm việc riêng với Trang

Hồ sơ: `team/nhan-su/phan-bien/ho-so.md` · Prompt: `.claude/agents/phan-bien.md` · Nhật ký: `team/nhan-su/phan-bien/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Trang: gọi Agent với `subagent_type: "phan-bien"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Trang hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Trang trong cùng phiên, gửi tiếp cho đúng Trang (SendMessage) thay vì gọi mới, để Trang nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Trang:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/phan-bien/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
