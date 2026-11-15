---
name: lan
description: Làm việc trực tiếp với Lan (Nghiên cứu thị trường, pháp lý, có nguồn). Chủ kênh gõ /lan <việc> hoặc gọi "Lan ơi …" để giao việc riêng cho Lan, không qua chia việc của Minh.
---
# Làm việc riêng với Lan

Hồ sơ: `team/nhan-su/nghien-cuu/ho-so.md` · Prompt: `.claude/agents/nghien-cuu.md` · Nhật ký: `team/nhan-su/nghien-cuu/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Lan: gọi Agent với `subagent_type: "nghien-cuu"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Lan hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Lan trong cùng phiên, gửi tiếp cho đúng Lan (SendMessage) thay vì gọi mới, để Lan nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Lan:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/nghien-cuu/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
