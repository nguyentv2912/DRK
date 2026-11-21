# Phản biện — phiên bản 2 (Đầu Tư Bình An trên Skool)

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người phản biện: Trang · 14/11/2026
Đã đọc: brief.md, phieu-giao-viec.md, nghien-cuu.md, tai-chinh.md, mo_hinh.py, ke-hoach.md, kiem-dinh.md, bao-cao.md, giam-sat/*-v2-*.md, gop-y.jsonl cũ của 6 người.

## 1. Lần này đã tránh được lỗi phiên bản 1 chưa?
**Phần lớn là có.** Minh đã hỏi hiện trạng trước khi giao việc (brief mục "Hiện trạng chủ dự án"). Giá 100 USD / 1.000 USD / ~1 triệu, tên chương trình, Skool, thông điệp ĐẠO + ĐỜI + ĐẦU TƯ giữ nguyên ở cả 4 file (Hà đã kiểm). Có 25 ô [chờ anh], đội không tự viết phương pháp "6 × 6 × 6".
**Còn 3 chỗ chưa sạch:**
- Đội vẫn tự thiết kế phần ruột của "đồng hành 10 năm": lịch 1:1, live quý, buổi chuyển pha (ke-hoach 3.4), gói A/B, trả góp, "gói 12 tháng thay cho 10 năm" (mục 6). Các mục này có ghi "để anh chốt", nhưng **con số trên trang đầu (114 học viên, 2.824,4 tr) phụ thuộc phương án A do Hùng chọn** ("Hùng đề xuất Phương án A", ke-hoach mục 6), và tóm tắt không nói điều đó.
- 9 câu hỏi cho anh để ở cuối bài. Trong đó câu #1 (A/B), #2 (đồng hành gồm gì) và #8 (số người theo dõi thật) làm đổi kết quả mô hình. Ba câu này nên hỏi **trước khi** Hùng chạy mô hình, giống như hỏi hiện trạng.
- Ý gốc "giới thiệu cho uy tín hơn" (ngân hàng, văn phòng) bị rơi khỏi phiếu giao việc v2. Bảo hai lần chấm là "mỏng". Bản cuối chỉ có 1 đoạn ở 3.4.

## 2. Lỗi ngưỡng 2,5% gắn nhầm chỉ số: nguyên nhân gốc và chỗ cần chuẩn hoá
- **Gốc nằm ở Hùng:** mô hình có **hai** tỷ lệ chuyển đổi: `cd_free_sang_tra_phi_thang_dau` 3% và `cd_free_sang_tra_phi_ton` 0,3%/tháng (mo_hinh.py dòng 70–71), lại thêm `ty_le_vao_skool_moi`. Nhưng dòng "Mốc tháng 3" ở 5b chỉ ghi "chuyển đổi < 2,5%" (kiem-dinh #6: "đây là gốc của lỗi #1"). Không có chỗ nào định nghĩa tử số, mẫu số, thời gian đo và cách đo trên Skool.
- **Mai chép số mà không chép nghĩa:** ở lần 1, bảng "Đã kiểm, đạt" của Hà ghi "Số ke-hoach ↔ TC/JSON: Khớp", cùng lúc lỗi #1 là Chặn. Con số 2,5% đúng, chỉ có chỉ số đi kèm là sai. Vậy kiểm khớp số không bắt được lỗi về nghĩa.
- **Bảo chấm Hùng vòng 2 tiêu chí 3 = 92% mà không thấy nhãn mơ hồ.** Sau khi bắt lỗi ở Mai, Bảo cũng không mở lại phiếu Hùng. Phải đến Hà #6 thì Hùng mới sửa. Đây là lần thứ 2 lỗi "ngược dòng" lặp lại (gop-y giam-sat ngày 14/11 đã nêu).
- **Chuẩn hoá (một quy ước, áp vào 5 nơi):** dùng chung một **"từ điển chỉ số"**.
  - `tai-chinh.md`: JSON có khối `dinh_nghia_chi_so`. Mỗi ngưỡng/KPI ghi tên, tử số, mẫu số, thời gian đo, khoá JSON và cách đo trên Skool. Mọi câu ngưỡng trong .md dẫn đúng tên đó.
  - `chien-luoc.md`: bảng KPI/ngưỡng lấy từ khối này, ghi kèm khoá JSON. Không tự diễn giải lại.
  - `giam-sat.md` và `kiem-dinh.md`: thêm mục kiểm "khớp nghĩa": mỗi ngưỡng dẫn chéo giữa các file phải cùng tử số và mẫu số, khớp con số thôi là chưa đủ.
  - `giao-viec`: phiếu ghi Hùng giao từ điển chỉ số trước khi Mai viết KPI.
  - **Sửa ở prompt của Hùng là chính.** Đây là chỗ sinh ra chỉ số; sửa ở các khâu sau chỉ là lưới đỡ.

## 3. Góp ý từng người (tối đa 3)

### Lan – Nghiên cứu
- **Giữ:** có các dữ kiện dùng thẳng để ra quyết định: Napas nội địa không trả được, Skool không bán file lẻ, email 72 giờ, Stripe Express do Skool tạo, "phải thử giao dịch thật". Có ghi rõ ngoại lệ môi trường.
1. **Thiếu dữ kiện đỡ giả định lớn nhất của mô hình** (cao, prompt). Hùng dựa vào chuyển đổi 3% và huỷ 9%, trong khi kết luận 5 tự ghi 2–5% là "số của ngành SaaS". Giá cộng đồng crypto tiếng Việt trả phí theo tháng vẫn để ở câu hỏi mở 9. Đây là lần thứ 2: v1 cũng thiếu giá đối thủ nội địa. → Nên hỏi Hùng 2–3 giả định nhạy nhất trước, rồi dồn công tìm số gần nhất cho đúng các giả định đó (nhóm Telegram/Discord/Facebook trả phí tiếng Việt). Không tìm được thì đưa kế hoạch xác minh 1 tuần.
2. **Kết luận chưa có dòng "dùng cho:"** (thấp, prompt). Grep ra 0 lần, dù gop-y v1 đã đề xuất. Khoảng hở 899/900 USD ở kết luận 1 vẫn còn (kiem-dinh #15).

### Hùng – Tài chính
- **Giữ:** có kịch bản "không đáng làm" và ngưỡng dừng tháng 3/6. Nghĩa vụ 10 năm có quỹ phục vụ 30% và ghi nhận doanh thu 20/80. Chạy cả A lẫn B. Chạy lại ra file giống từng byte. Người theo dõi sẵn có = 0, ghi "chờ số thật".
1. **Chỉ số không có định nghĩa, gây ra lỗi 2,5%** (cao, prompt). Xem mục 2. Thêm `dinh_nghia_chi_so` và kiểm cuối script: mọi khoá trong `nguong_dung` phải có định nghĩa.
2. **Ngưỡng tháng 3 quyết bằng mẫu quá nhỏ** (trung-bình, prompt). 2,5% của 28–72 thành viên mới là 0,7–1,8 người, sàn chỉ là "≥ 1 học viên". Kết quả đạt hay trượt lúc này phần lớn do may rủi. → Đặt cỡ mẫu tối thiểu (ví dụ ≥ 100 thành viên mới luỹ kế) trước khi xét tỷ lệ. Chưa đủ mẫu thì cổng là "chưa kết luận", không phải "đổi cách bán".

### Mai – Chiến lược
- **Giữ:** 25 ô [chờ anh], 3 phương án câu chữ "216". Quy tắc dùng Phật – Nho – Đạo có nêu xung đột với brand.md để anh duyệt. Video chỉ mời vào cộng đồng miễn phí, vì TikTok cấm nội dung tài chính có thương hiệu.
1. **Chép ngưỡng mà không kiểm định nghĩa** (cao, prompt). Bảo vòng 1 và Hà lần 1 (Chặn #1) cùng bắt lỗi này. Đây là lần thứ 2 Mai chép số TC mà không kiểm nghĩa (v1: mâu thuẫn công suất). → Bảng KPI lấy thẳng từ `nguong_dung`/`dinh_nghia_chi_so`, ghi khoá JSON. Có KPI nào không có trong TC thì ghi "giả định của Mai".
2. **Vẫn dài: 8.232 chữ, tóm tắt 567 chữ** (cao, tiêu chí). Lần thứ 2 (v1 12.818 chữ). Bảo nhắc nhưng bài chỉ ngắn đi 2%, vẫn 90 điểm. → Hồ sơ: tiêu chí 6 đổi thành Chặn, có trần đo được (trang đầu ≤ 400 chữ, thân ≤ 4.000 chữ, phần còn lại đưa vào phụ lục).
3. **Còn ghi chú nội bộ trong tài liệu cho anh** (trung-bình, prompt): "Hùng đề xuất Phương án A", các nhãn (TC)/(NC) dày đặc. Lần thứ 2. → Thay bằng "đội đề xuất" và chú thích nguồn ở cuối bài.

### Hà – Kiểm định
- **Giữ:** tự chạy lại mô hình và tự tính lại số. Bắt được trích sai Đạo Đức Kinh (ch. 8 / ch. 78) và Luận Ngữ 13.17, ranh giới tư vấn của buổi 1:1. Ghi được nguyên nhân gốc (#6), tức đã áp dụng gop-y cũ.
1. **Danh mục kiểm chỉ khớp số, không khớp nghĩa** (trung-bình, prompt). Bằng chứng: lần 1 ghi "Khớp" ở bảng đạt mà vẫn có Chặn #1. → Thêm mục bắt buộc "ngưỡng/KPI liên file: cùng tử số, mẫu số, khoá JSON".
2. **Không xét độ dài và khả năng dùng của tài liệu** (trung-bình, prompt). Bài 8.232 chữ vẫn qua, không có dòng nào nói về độ dài. Gop-y v1 đã nêu, đây là lần thứ 2.

### Bảo – Giám sát
- **Giữ:** đọc JSON bằng python khi chấm Mai. Ngoại lệ môi trường cho Lan có trưởng nhóm duyệt và ghi cả điểm theo hồ sơ gốc. Không mở vòng chấm thừa. Đã áp dụng gop-y cũ.
1. **Lỗi ngược dòng lặp lại lần 2** (cao, tiêu chí). Bảo thấy lỗi gốc từ TC khi chấm Mai mà không chấm lại Hùng. → Hồ sơ giam-sat thêm tiêu chí Chặn "không bỏ lọt lỗi gốc ở khâu trước". Prompt: thấy lỗi bắt nguồn từ file khác thì mở vòng N+1 cho người đó.
2. **Lỗi chỉ số quyết định mà vẫn ĐẠT 80** (cao, tiêu chí). Ngưỡng dừng sai chỉ số, Hà xếp Chặn, còn Bảo cho tiêu chí 2 = 75% (Chặn ≥ 60%) nên vẫn ĐẠT. → Quy tắc: sai giá anh chốt, sai ngưỡng dừng hay sai KPI quyết định thì tiêu chí đó bằng 0, tức tự động CHƯA ĐẠT.

### Minh – Quản lý
- **Giữ:** hỏi hiện trạng, bảng "Những gì đã chốt", cấm dùng ban-nhap-cu. Báo cáo nói thẳng phần còn mở và 2 dữ kiện phải thử bằng giao dịch thật.
1. **Brief chồng lớp, tự mâu thuẫn** (trung-bình, prompt). Brief vẫn giữ "Sản phẩm cuối: gói sản phẩm và giá đề xuất" và "không lấy số liệu kênh Đạo Đức Đầu Tư", trong khi mục v2 ghi "được dùng kênh" và giá đã chốt. Đội phải dựa vào câu "ưu tiên hơn" để biết đọc theo phần nào. → Khi hiện trạng làm đổi việc thì viết lại brief sạch, chuyển bản cũ vào ban-nhap-cu/.
2. **Phiếu v2 làm rơi ý gốc và thiếu hợp đồng giữa các khâu** (cao, prompt). Mất ý "uy tín (ngân hàng, văn phòng)". Không ghi định nghĩa chỉ số dùng chung Hùng → Mai. Vẫn chưa ghi độ dài tối đa, lần thứ 2 (gop-y v1). → Phiếu thêm 3 thứ: bảng "từng câu trong yêu cầu gốc → ai làm", cột "định nghĩa dùng chung", và độ dài tối đa cho mỗi file.
3. **Hỏi câu chặn quá muộn, xếp thứ tự kiểm chồng nhau** (trung-bình, prompt). Câu #1, #2, #8 làm đổi mô hình nhưng chỉ được hỏi sau khi làm xong. Chặn #1 của Hà lần 1 trùng đúng chỗ Bảo vòng 1 đã báo, tức Hà kiểm trên bản chưa sửa nên tốn thêm một lượt. → Gửi anh ≤ 3 câu chặn trước khi Hùng chạy mô hình. Chỉ chuyển Hà khi Bảo đã ĐẠT và phản hồi bắt buộc đã sửa xong.

## 4. Ba góp ý quan trọng nhất
1. **Chuẩn hoá "từ điển chỉ số"**, sửa ở prompt Hùng là chính, rồi đến Mai, Bảo, Hà và phiếu giao việc. Đây là nguyên nhân gốc của lỗi 2,5%.
2. **Bảo: lỗi chỉ số quyết định thì tự động CHƯA ĐẠT, và lỗi ngược dòng thì phải chấm lại khâu trước.** Cả hai đều đã lặp lần 2.
3. **Minh: hỏi ≤ 3 câu chặn (A/B, nội dung đồng hành, số thật của kênh) trước khi dựng mô hình.** Phiếu giữ đủ ý gốc "uy tín" và ghi độ dài tối đa. Chỉ khi đó lỗi v1 (đội tự quyết thay anh) mới được chặn hết.
