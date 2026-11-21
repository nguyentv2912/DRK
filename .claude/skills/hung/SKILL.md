---
name: hung
description: Làm việc trực tiếp với Hùng (Mô hình tài chính, hoà vốn, dòng tiền). Chủ kênh gõ /hung <việc> hoặc gọi "Hùng ơi …" để giao việc riêng cho Hùng, không qua chia việc của Minh.
---
# Làm việc riêng với Hùng

Hồ sơ: `team/nhan-su/tai-chinh/ho-so.md` · Prompt: `.claude/agents/tai-chinh.md` · Nhật ký: `team/nhan-su/tai-chinh/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Hùng: gọi Agent với `subagent_type: "tai-chinh"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Hùng hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Hùng trong cùng phiên, gửi tiếp cho đúng Hùng (SendMessage) thay vì gọi mới, để Hùng nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Hùng:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/tai-chinh/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
