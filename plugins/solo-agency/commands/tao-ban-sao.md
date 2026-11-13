---
description: Tạo Bản sao AI mang gương mặt và giọng của bạn (kiến thức, quan điểm, giới hạn, thư viện video cần quay)
---

Bạn đang giúp chủ thương hiệu tạo **Bản sao AI**: trợ lý trả lời tin nhắn bằng giọng văn, kiến thức, gương mặt và giọng nói của chính họ. Hỏi **từng nhóm một**, bằng ngôn ngữ chủ đang dùng. Nếu file đã có, đọc trước và chỉ hỏi phần thiếu. Nếu `brand/` chưa có, chạy phần phỏng vấn của `/solo-agency:thiet-lap` trước.

## Phỏng vấn
1. **Chuyên môn:** lĩnh vực (ví dụ đầu tư tài chính, crypto), bao nhiêu năm kinh nghiệm, phong cách (dài hạn, giao dịch ngắn, phân tích on-chain…), bằng cấp hoặc chứng chỉ nếu có.
2. **Quan điểm cốt lõi:** 5–10 nguyên tắc chủ luôn dạy (ví dụ quản lý vốn, kỷ luật, cắt lỗ). Những điều chủ **phản đối** (ví dụ đòn bẩy cao, all-in, nhóm kéo xả).
3. **Câu chuyện:** 3 câu chuyện thật chủ hay kể: một lần thắng, một lần thua, một bài học.
4. **Xưng hô và câu giới thiệu AI.** Đề xuất mặc định: "Chào bạn, mình là trợ lý AI của <tên>, được <tên> huấn luyện để trả lời bằng kiến thức và gương mặt của <tên>. Những câu cần <tên> trực tiếp, mình sẽ chuyển lại nhé."
5. **Giới hạn:** chủ có giấy phép tư vấn đầu tư không? (Nếu không, bản sao chỉ dừng ở mức giáo dục.) Chủ có bán nhóm tín hiệu hay quản lý vốn không? (Khuyên hỏi luật sư trước.)
6. **Quyền lợi cần công khai:** tài sản chủ đang nắm giữ mà hay nhắc tới, dự án đang hợp tác, link giới thiệu (affiliate), token chủ phát hành hoặc quảng bá.
7. **Chuyển cho chủ:** khi nào bản sao phải chuyển (mặc định: số tiền lớn, thua lỗ nặng, tuyệt vọng, khiếu nại, báo chí, hợp tác). Số đường dây hỗ trợ tâm lý ở nước khách (tại Việt Nam có thể dùng Tổng đài quốc gia bảo vệ trẻ em 111 cho người dưới 18 tuổi; với người lớn, ghi số tổng đài tư vấn tâm lý chủ tin dùng).
8. **Kênh chính thức:** danh sách tài khoản thật để chống mạo danh.

## Tạo file
- `brand/ban-sao-ai.md`: nhóm 4, 5, 6, 7, 8, và ghi rõ "Bản sao AI chỉ giáo dục, không đưa lời khuyên mua bán cá nhân" (trừ khi chủ có giấy phép và đã hỏi luật sư).
- `brand/kien-thuc/chuyen-mon.md` (nhóm 1), `brand/kien-thuc/quan-diem.md` (nhóm 2), `brand/kien-thuc/cau-chuyen.md` (nhóm 3). Chủ có thể bỏ thêm bài viết, transcript video cũ vào `brand/kien-thuc/` để bản sao học.
- `content/thu-vien-video/danh-sach.md`: danh sách **20 video trả lời câu hỏi hay gặp** để chủ quay **bằng mặt thật** (rẻ nhất, chân thật nhất). Bảng: # | Câu hỏi | Tên file (`cau-01.mp4`…) | Kịch bản 30–45 giây | Đã quay?
  Gợi ý cho lĩnh vực đầu tư/crypto: crypto là gì, người mới bắt đầu thế nào, bao nhiêu tiền thì nên bắt đầu, cách giữ ví an toàn, nhận biết dự án lừa đảo, vì sao không nên dùng đòn bẩy, quản lý vốn, tâm lý FOMO, cắt lỗ, đầu tư dài hạn và lướt sóng, khóa học của chủ dạy gì, giá bao nhiêu, ai không nên học, cách liên hệ chính thức…

## Hướng dẫn tài sản gương mặt và giọng nói
Tạo `content/thu-vien-video/HUONG-DAN-QUAY.md` hướng dẫn chủ chuẩn bị:
- `mat.mp4`: 15–30 giây quay thẳng mặt, ánh sáng đều, nền gọn, miệng khép tự nhiên, ít cử động đầu, 25 khung hình/giây, dọc 9:16.
- `ref.wav`: khoảng 10–15 giây giọng nói rõ, không nhạc nền, đọc tự nhiên, kèm câu chữ chính xác của đoạn đó.
- Ba cấp độ video trả lời:
  1. **Video quay sẵn** (thư viện 20 câu): miễn phí, chân thật nhất. Nên làm đầu tiên.
  2. **Video AI theo yêu cầu**: bản sao viết `kichban.txt`, chủ chạy notebook clone giọng và khớp môi (ví dụ `kaggle/video_noi_free.ipynb`), mất khoảng 20–30 phút mỗi video trên GPU miễn phí.
  3. **Gọi video trực tiếp với avatar** (HeyGen Interactive Avatar, Tavus, D-ID…): khách nói chuyện thời gian thực với gương mặt của chủ. Tốn phí theo phút; chỉ nên dùng khi đã có khách trả tiền.
- Mọi video do AI tạo phải có dòng chữ "Video trả lời bởi trợ lý AI của <tên>".

## Kết thúc
Tóm tắt cho chủ: bản sao đã biết gì, còn thiếu gì, 3 video nên quay trước. Gợi ý chạy `/solo-agency:tra-loi-tin-nhan` với vài tin nhắn thật để thử.
