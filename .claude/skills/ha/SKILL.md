---
name: ha
description: Làm việc trực tiếp với Hà (Kiểm định sản phẩm cuối). Chủ kênh gõ /ha <việc> hoặc gọi "Hà ơi …" để giao việc riêng cho Hà, không qua chia việc của Minh.
---
# Làm việc riêng với Hà

Hồ sơ: `team/nhan-su/kiem-dinh/ho-so.md` · Prompt: `.claude/agents/kiem-dinh.md` · Nhật ký: `team/nhan-su/kiem-dinh/nhat-ky.jsonl`

1. Chuyển nguyên văn yêu cầu của anh cho Hà: gọi Agent với `subagent_type: "kiem-dinh"`. Không lập phiếu giao việc, không gọi thêm nhân viên khác (trừ khi anh yêu cầu).
2. Bối cảnh tự đủ trong prompt: yêu cầu nguyên văn, thư mục làm việc (việc kênh: `fanpage/runs/<mã>/`; dự án khác: `team/viec/<mã>/` có brief.md), file liên quan anh nhắc tới. Nếu Hà hỏi lại, chuyển câu hỏi cho anh.
3. Nếu anh đang trao đổi tiếp với Hà trong cùng phiên, gửi tiếp cho đúng Hà (SendMessage) thay vì gọi mới, để Hà nhớ ngữ cảnh.
4. Trả lời anh ngắn gọn, mở đầu "Hà:", kèm file kết quả. Bảo chấm chỉ khi anh yêu cầu hoặc khi kết quả sẽ được đăng/giao cho người khác.
5. Ghi một dòng vào `team/nhan-su/kiem-dinh/nhat-ky.jsonl`: ngày, việc anh giao riêng, file nộp.
