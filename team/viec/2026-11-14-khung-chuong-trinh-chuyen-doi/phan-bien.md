# Phản biện sau việc — 2026-11-14-khung-chuong-trinh-chuyen-doi

Người phản biện: Trang – Phản biện · Ngày 14/11/2026
Đã đọc: brief.md, phieu-giao-viec.md, nghien-cuu.md, mo_hinh.py, tai-chinh.md, ke-hoach.md, kiem-dinh.md (lần 1 + 2), giam-sat/* (7 phiếu), bao-cao.md, prompt `.claude/agents/{nghien-cuu,tai-chinh,chien-luoc,giam-sat,kiem-dinh}.md`, hồ sơ của 5 nhân viên.

## Ba góp ý quan trọng nhất của cả việc
1. **Lỗi công suất coach lọt qua Bảo vì Bảo kiểm lại bằng chính công thức của Hùng.** Bảo còn thấy triệu chứng ở bài của Mai nhưng không quay lại hạ điểm Hùng. Gốc ở hai prompt: prompt Hùng chỉ bắt kiểm "biên lợi nhuận, đơn vị, dấu", không bắt kiểm ràng buộc vận hành. Prompt Bảo không có quy tắc "lỗi phát hiện ở khâu sau thì mở lại phiếu khâu trước". (Hùng, Bảo · cao)
2. **Kế hoạch 12.818 từ không hợp với người đọc.** Tóm tắt dài 797 từ nhưng không nói gì về khung chương trình, tức thứ anh hỏi. Tài liệu còn chứa ghi chú nội bộ ("Lan không mở được…", "Giám sát đánh giá…", "Vòng 2…"). Tiêu chí "Ngắn gọn" chỉ nặng 10 điểm và không phải tiêu chí Chặn, nên bài dài thêm 13,5% sau phản hồi vẫn được 91. (Mai, Hà · cao)
3. **Tiêu chí 2 của Lan trộn hai việc: lỗi của người làm và giới hạn của môi trường.** Vì vậy có 2 vòng chấm thừa (vòng 2, vòng 3) không thể đổi kết quả. Trong khi đó, chỗ hụt lớn nhất về nội dung là **giá đối thủ nội địa có thu phí chỉ có 1 mức** (Unica). Giá gói đồng hành 12 trđ của Hùng đặt trên nền đó, vậy mà chỗ này không bị chấm Chặn. (Lan, Bảo · cao)

---

## Hùng – Tài chính (tai-chinh)

**Điều tốt cần giữ:** script tái tạo JSON giống từng byte. Mô hình hoá lộ trình theo cổng (`CONG`) có độ trễ và mốc dừng. Có phương án tham chiếu "giữ đội 8" và giải thích chênh lệch với số của Hà, Bảo đã chạy lại và khớp. Nhận định thẳng: vòng 1 ghi rõ "kịch bản cơ sở chưa đạt", NPV −233.

**G1 — Ràng buộc công suất chỉ áp ở một đường code (cao, sửa ở prompt).**
- Vấn đề: `chay()` có tự thêm cặp coach khi vượt 40 học viên, nhưng `hoa_von_phong_ban()` vòng 1 tính trên đội 8 cố định. Kết quả: hoà vốn 15,8 khách, tức 47 học viên đang học, vượt công suất 40 của một cặp coach.
- Bằng chứng: kiem-dinh.md, Phụ lục lần 1, Chặn #1 ("Ngưỡng 15,8 / 31,6 phải là ~19,5 (10 người) / 35,2 (19 người)"). Lỗi còn lại của lần 2 có **cùng gốc**: `moi = max(0, so_nguoi(gd_ten) - so_nguoi(gd_truoc))` lấy đội kế hoạch thay cho đội thực tế, làm dư ~100 trđ chi phí tuyển (kiem-dinh.md lần 2, Nên sửa #1). Lỗi này vẫn nằm trong bản đã bàn giao.
- Chuyên gia sẽ làm khác: một mô hình chỉ có **một nguồn trạng thái** cho số người. Mọi chỉ số (hoà vốn, dự phòng, chi phí tuyển) đều đọc từ đó. Kèm **phép thử bất biến**: chạy mô hình ở đúng số khách hoà vốn thì EBITDA phải ≈ 0, và đội phải đủ phục vụ số khách đó.
- Đề xuất đoạn prompt (thêm vào bước 3): "Kiểm ràng buộc vận hành: công suất (khách/người), số người, tuyển. Mỗi ràng buộc viết **một hàm dùng chung**, mọi chỉ số gọi cùng hàm đó. Cuối script tự chạy `assert`: (a) ở ngưỡng hoà vốn, EBITDA tháng ≈ 0 với đội đủ công suất; (b) số người tuyển mới = đội tháng này − đội thực tế tháng trước."

**G2 — Phương án khuyến nghị chỉ được mô hình hoá sau khi Hà yêu cầu (trung bình, sửa ở prompt).**
- Bằng chứng: vòng 1 chỉ có phương án tuyển theo lịch (vốn 2.903, NPV −233). Lộ trình theo cổng, là phương án cuối cùng được khuyến nghị, chỉ xuất hiện sau Nên sửa #4 của Hà. Độ nhạy ±20% cho phương án này cũng chỉ có sau khi Bảo tự chạy (tai-chinh-vong2, tiêu chí 5 = 75%).
- Chuyên gia sẽ làm khác: khi phương án cơ sở không đạt, chuyên gia không dừng ở câu "không khả thi". Họ mô hình hoá luôn phương án sửa và chạy độ nhạy trên **phương án được khuyến nghị**, không chỉ trên phương án bị bác.
- Đề xuất đoạn prompt (sửa bước 4): "Nếu kịch bản cơ sở không khả thi: đề xuất ≥1 phương án thay đổi, **chạy nó trong script**, và đặt bảng độ nhạy ±20% trên phương án được khuyến nghị."

**G3 — Ghi chú nội bộ và lỗi đã biết còn nằm trong bản giao (thấp, sửa ở prompt).**
- Bằng chứng: tai-chinh.md mục 5 và 7A có câu "Hà tính ra…", "Hà đã chạy thử…" (kiem-dinh lần 2, Gợi ý #6). Bao-cao.md ghi lỗi tuyển trùng "để Hùng sửa nếu chủ dự án muốn". Lỗi này chỉ cần sửa 1 dòng mà Hà đã chỉ sẵn.
- Đề xuất: "Lỗi đã có cách sửa một dòng thì sửa trước khi bàn giao. Không ghi tên người kiểm hay số vòng trong tai-chinh.md; lịch sử sửa để ở phiếu giám sát."

**Tiêu chí chấm (hồ sơ):** tiêu chí 3 "Phép tính hợp lý: đơn vị, dấu, biên lợi nhuận" đo sai trọng tâm. Đề xuất đổi thành "Phép tính hợp lý **và ràng buộc vận hành nhất quán** (công suất, số người, tuyển áp cho mọi chỉ số; có phép thử bất biến)", giữ Chặn.

---

## Bảo – Giám sát (giam-sat)

**Điều tốt cần giữ:** chạy lại script trên bản sao và so từng byte. Viết script so 1.344 số giữa ke-hoach.md và tai-chinh.json. Ở vòng 2 Hùng, Bảo tự chạy độ nhạy cho lộ trình theo cổng và tự tìm ra lỗi dự phòng (thiếu ≈97 trđ) mà Hà chưa nêu. Bảo cũng tách rõ "do môi trường" với "lỗi của Lan" trong từng dòng chấm.

**G1 — Kiểm chứng kiểu "tính lại cùng công thức" nên không bắt được lỗi logic (cao, sửa ở prompt).**
- Bằng chứng: tai-chinh-vong1.md ghi "Hoà vốn phòng ban Khởi động: 131,2 + 18 + 1,6 + 16 = 166,8; chia cho 10,53 = 15,8 khách. Đúng." Cùng phiếu, tiêu chí 3 lại cho 88% với lời khen "Có kiểm tra công suất coach". Chỉ cần nhân 15,8 × 3 = 47 học viên > 40 là thấy lỗi.
- Chuyên gia sẽ làm khác: người kiểm toán mô hình kiểm theo hai hướng. Hướng thứ nhất là **tái tạo**: số có khớp code không. Hướng thứ hai là **phản biện**: kết quả có khả thi ngoài đời không. Câu hỏi của hướng thứ hai: ở ngưỡng này đội có đủ người phục vụ không, tư vấn viên có kịp gọi số lead đó không.
- Đề xuất đoạn prompt (thêm vào bước 2): "Với mô hình tài chính: ngoài tái tạo số, làm ≥2 phép thử khả thi **độc lập với công thức của nhân viên**, ví dụ khách × thời gian phục vụ ≤ công suất đội, lead ≤ năng lực tư vấn viên. Có thử mới cho tiêu chí 'phép tính hợp lý' trên 80%."

**G2 — Thấy triệu chứng ở khâu sau nhưng không mở lại phiếu khâu trước (cao, sửa ở prompt).**
- Bằng chứng: chien-luoc-vong1.md, phản hồi 3: "Mâu thuẫn hoà vốn đội 8: dòng 298 nói 16 khách thì cần thêm coach, còn dòng 396 ghi 'Đội 8 tự nuôi được (hoà vốn 15,8)' → nhờ Hùng tính hoà vốn khi có 10 người". Lỗi này được xếp phản hồi #3 của Mai. Phiếu của Hùng vẫn giữ ĐẠT 92. Đến Hà mới nâng thành Chặn.
- Đề xuất: "Nếu khi chấm người B mà thấy lỗi gốc từ người A đã ĐẠT, ghi vào phiếu của B mục 'Lỗi ngược dòng', báo trưởng nhóm, và chấm lại A (vòng N+1) **trước khi** B sửa."

**G3 — Chấm thêm vòng dù đã biết điểm bị trần, và không giữ được lời mình đã nói về độ dài (trung bình, sửa ở tiêu chí).**
- Bằng chứng: nghien-cuu-vong1.md đã viết "Nếu vòng 2 vẫn không mở được tên miền nào thì sửa nội dung cũng không thể đưa tiêu chí 2 lên trên 60%". Sau đó vẫn có vòng 2 và vòng 3, kết quả 82 → 84, vẫn CHƯA ĐẠT. Với Mai, vòng 1 yêu cầu rút gọn. Vòng 2 tài liệu dài thêm 1.527 từ, tiêu chí 6 xuống 65%, nhưng điểm tổng vẫn lên 91 vì tiêu chí này chỉ nặng 10 điểm.
- Đề xuất: (a) prompt: "Khi mọi lỗi còn lại đều do môi trường, kết luận ngay 'CHẶN BỞI MÔI TRƯỜNG', không mở vòng mới, trừ khi môi trường đã đổi." (b) Hồ sơ Bảo: tiêu chí 4 "Nhất quán" thêm ý: phản hồi bắt buộc của vòng trước mà không được sửa thì không cho điểm tối đa tiêu chí liên quan. Hồ sơ Bảo nên có thêm tiêu chí Chặn mới: "Không bỏ lọt lỗi Chặn mà khâu sau phát hiện".

**Tiêu chí chấm (hồ sơ Bảo):** hiện chỉ đo hình thức chấm (đúng thang, có bằng chứng, phản hồi sửa được, nhất quán). Không tiêu chí nào đo **độ nhạy phát hiện lỗi**. Đề xuất thêm tiêu chí "Tỷ lệ lỗi Chặn bị khâu sau (Hà) phát hiện mà Bảo đã cho ĐẠT", nặng 20 điểm, là tiêu chí Chặn. Lấy dữ liệu từ kiem-dinh.md.

---

## Lan – Nghiên cứu (nghien-cuu)

**Điều tốt cần giữ:** báo rõ WebFetch bị chặn ngay đầu file. Tự hạ trần độ tin cậy xuống TB. Khi hai nguồn lệch thì nêu cả hai (17 và 21 triệu; 220 và 122,2 tỷ USD). Sinh mục Nguồn tự động, khớp 130/130 link. Phát hiện trang MOF có ngày đăng lệch với nội dung và ghi lại.

**G1 — Giá đối thủ, dữ kiện quyết định nhiều nhất, gần như trống (cao, sửa ở prompt).**
- Bằng chứng: nghien-cuu-vong3.md, tiêu chí 1: "Giá đối thủ nội địa có thu phí vẫn chỉ có 1 mức". Các giá còn lại là Inflearn (Hàn Quốc) và hai chương trình miễn phí. Giá gói đồng hành 12 trđ và gói thành viên 3,6 trđ là giả định của Hùng (ke-hoach.md dòng 9). Theo bảng 8A, độ nhạy giá −20% làm phương án không hoàn vốn.
- Chuyên gia sẽ làm khác: khi không mở được trang, chuyên gia đổi cách lấy dữ liệu. Có thể tìm trích đoạn landing page, nhóm Facebook, tin tuyển "học viên" có ghi học phí. Nếu vẫn không có, họ đưa ra **kế hoạch xác minh cụ thể cho chủ dự án**: gọi hỏi giá 5 đơn vị (mystery shopping), kèm mẫu câu hỏi. Ngoài ra họ xếp mức ưu tiên tìm kiếm theo câu "số nào quyết định giá và vốn".
- Đề xuất đoạn prompt (thêm vào bước 1): "Đánh dấu 2–3 câu hỏi nhỏ **quyết định tài chính** (giá, tỷ lệ chuyển đổi, lương). Dành phần lớn công sức cho các câu này. Nếu vẫn thiếu, ghi kế hoạch xác minh chủ dự án làm được trong 1 tuần (ai hỏi, hỏi ai, mẫu câu)."

**G2 — Tiêu chí 2 không phân biệt giới hạn môi trường (cao, sửa ở tiêu chí).**
- Bằng chứng: vòng 1/2/3 có tiêu chí 2 lần lượt 45 → 55 → 58%. Bảo ghi "trần do môi trường 55–60%" và "Lan không còn lỗi nào tự sửa được". Kết luận CHƯA ĐẠT dù tổng điểm đã 84. Bảng điểm vì thế ghi Lan "không đạt" vì lý do ngoài khả năng của Lan, làm sai dữ liệu cho chu kỳ nâng cấp.
- Trả lời câu hỏi của trưởng nhóm: **có, nên phân biệt**, nhưng không được làm số chưa xác minh trông như đã xác minh. Đề xuất tách tiêu chí 2 thành:
  - 2a "Mọi số quan trọng có link cụ thể tới bài gốc, truy vết được; không dùng 'qua tìm kiếm'" (15, Chặn). Đây là phần Lan làm được.
  - 2b "Đã mở nguồn gốc và ghi 'đã mở ngày…'" (10). Nếu môi trường chặn và đã có bằng chứng (lệnh lỗi 403), chấm **N/A**, chia trọng số cho 2a.
  - Thêm trạng thái kết quả thứ ba: **"ĐẠT – CHƯA XÁC MINH NGUỒN"**. Mọi số giữ trần TB, và trưởng nhóm phải chuyển cảnh báo xuống các khâu sau. Trong `nhat-ky.jsonl` thêm trường `"gioi_han_moi_truong": true` để bảng điểm không tính vào tỷ lệ đạt lần đầu.

**G3 — Nghiên cứu dài 6.175 từ với 130 link, nhưng phần lớn không phục vụ quyết định (thấp, sửa ở prompt).**
- Bằng chứng: kết luận 1 có các số Chainalysis 4/151, 220 tỷ USD, 17 triệu người. Đây là các số "thị trường lớn", không đổi được quyết định giá hay vốn nào trong tai-chinh.md. Trong khi đó giá đối thủ và lương coach đúng chức danh vẫn "chưa tìm được".
- Đề xuất: "Mỗi kết luận chính ghi thêm một dòng 'dùng cho:' (tài chính/kế hoạch, ô nào). Dữ kiện không dùng cho đâu thì để ở phụ lục."

---

## Mai – Chiến lược & Kế hoạch (chien-luoc)

**Điều tốt cần giữ:** khớp số với TC gần như tuyệt đối (1.344 số, không đổi số nào). Bảng cổng ở §7.1 có ngưỡng, thời điểm xét, hành động và mốc dừng kèm mức lỗ. Lịch 30 ngày đếm khớp với câu tổng. Xử lý pháp lý thận trọng: dùng "bị cáo buộc" cho Mr Pips, câu nào cũng gắn "cần luật sư xác nhận". Nêu thẳng "Chưa có văn bản thì không được nói 'ngân hàng đứng sau'".

**G1 — 12.818 từ là quá dài cho người đọc; tóm tắt không trả lời câu anh hỏi (cao, sửa ở prompt).**
- Bằng chứng: ke-hoach.md có 717 dòng và 15 mục. Tóm tắt §1 (dòng 17–59) dài 797 từ, gồm 6 ý: vốn, tuyển theo lịch, quảng cáo, độ nhạy, ngân hàng, rủi ro. **Không ý nào nói khung chương trình**: thang 990k → 12 trđ → 3,6 trđ/năm, phễu 6 tầng. Đó lại là câu đầu tiên của yêu cầu gốc ("cái khung chương trình để dành cho những khách hàng… chuyển đổi"). Chủ dự án giao việc bằng tin nhắn giọng nói, khó có khả năng đọc 13 nghìn từ.
- Chuyên gia sẽ làm khác: tư vấn chiến lược viết **memo 1 trang** theo nguyên tắc kim tự tháp: kết luận, 3 lý do, các việc anh cần quyết tuần này. Thân bài ≤ 4.000 từ. Chi tiết (lịch 30 ngày, KPI tháng, mô tả vị trí) đưa sang phụ lục hoặc tài liệu riêng. Ở đây nên có hai tài liệu: (1) Kế hoạch chương trình, (2) Kế hoạch nội dung, vì người dùng hai tài liệu này khác nhau (chủ dự án và đội nội dung).
- Đề xuất đoạn prompt (thêm vào Cách làm): "Trang đầu ≤ 400 từ, gồm: trả lời đúng câu hỏi gốc của người dùng (nguyên văn), con số quyết định, ≤5 việc người đọc phải quyết kèm hạn. Thân bài ≤ 4.000 từ. Phần dài hơn đưa vào phụ lục hoặc tách file. Đếm từ trước khi nộp."

**G2 — Ghi chú quy trình nội bộ nằm trong tài liệu gửi khách hàng (trung bình, sửa ở prompt).**
- Bằng chứng: ke-hoach.md dòng 8–10: "Lan không mở được trang gốc nào vì mạng bị chặn… Giám sát đánh giá phần nghiên cứu 'chưa đạt do môi trường'… **Vòng 2 (14/11/2026).** Bản này đã cập nhật theo mô hình vòng 2 của Hùng." Ngoài ra còn 9 chỗ nhắc Hà/Bảo/Lan/vòng. Chủ dự án cần biết "độ tin cậy TB, luật cần luật sư đối chiếu", không cần biết ai chấm ai.
- Đề xuất: "Không ghi tên nhân viên, vòng chấm hay ký hiệu nội bộ (TC, NC, tên khoá JSON) trong thân bài. Độ tin cậy viết bằng ngôn ngữ của người đọc. Nguồn kỹ thuật để ở chú thích cuối."

**G3 — Thấy số TC mâu thuẫn với logic vận hành nhưng vẫn chép nguyên (trung bình, sửa ở prompt).**
- Bằng chứng: vòng 1, dòng 298 Mai viết 16 khách thì cần thêm coach, còn dòng 396 vẫn ghi "Đội 8 tự nuôi được (hoà vốn 15,8)" (chien-luoc-vong1.md, phản hồi 3). Quy tắc "lấy nguyên số từ tai-chinh.md, không tự đổi" khiến Mai chép số sai thay vì báo lỗi.
- Đề xuất: "Không tự đổi số TC. Nhưng nếu số TC mâu thuẫn với một ràng buộc trong chính kế hoạch (công suất, ngân sách, lịch), ghi '⚠ cần Hùng xác nhận' tại chỗ và báo trưởng nhóm ngay trong phần Trả về."

**Tiêu chí chấm (hồ sơ):** tiêu chí 6 "Ngắn gọn" (10 điểm, không Chặn) đo sai mức quan trọng. Đề xuất: (a) thêm tiêu chí Chặn "Trang đầu trả lời đúng câu hỏi gốc, ≤400 từ, người đọc ra quyết định được chỉ từ trang đó" (15); (b) tiêu chí 6 đặt ngưỡng đo được: "thân bài ≤4.000 từ hoặc ≤ mức trưởng nhóm ghi trong phiếu". Bớt trọng số tiêu chí 4 (câu đầu mỗi phần) từ 15 xuống 10 để bù.

---

## Hà – Kiểm định (kiem-dinh)

**Điều tốt cần giữ:** đây là khâu bắt lỗi giá trị nhất của việc này. Hà tính độc lập (ceil(3 × khách ÷ 40), chi phí 1 cặp 38,1 trđ), **không dùng lại công thức của Hùng**, nhờ vậy bắt được lỗi Chặn mà Bảo đã cho qua. Lần 2 còn tìm ra lỗi tuyển trùng ~100 trđ và nói rõ hướng ảnh hưởng ("làm số thận trọng hơn, không làm sai quyết định"). Chạy trên bản sao, không sửa file người khác.

**G1 — Danh mục kiểm không có mục "dùng được cho người đọc" (trung bình, sửa ở prompt).**
- Bằng chứng: kiem-dinh.md có mục 5 "Đủ yêu cầu của brief: đạt", nhưng không nhắc đến độ dài 12.818 từ. Tóm tắt không nói về khung chương trình, và ghi chú nội bộ ở đầu ke-hoach.md cũng không được nêu. Hà chỉ nêu ghi chú nội bộ ở tai-chinh.md (Gợi ý #6).
- Đề xuất: thêm vào danh mục kiểm: "Người đọc trong brief đọc trang đầu có trả lời được câu hỏi gốc không; độ dài có hợp không; có ghi chú nội bộ không. Vi phạm = Nên sửa."

**G2 — Thấy hai lỗi cùng một gốc nhưng không chỉ ra gốc chung (thấp, sửa ở prompt).**
- Bằng chứng: Chặn #1 lần 1 (hoà vốn dùng đội cố định) và Nên sửa #1 lần 2 (tuyển dùng đội kế hoạch) đều do số người không có một nguồn trạng thái. Hà báo hai lỗi riêng, mỗi lỗi một cách sửa vá.
- Đề xuất: "Khi ≥2 lỗi có chung nguyên nhân, ghi thêm dòng 'Nguyên nhân gốc' và cách sửa tận gốc, để Trang/Đức đưa vào chu kỳ nâng cấp."

---

## Ngoài danh sách — ghi cho trưởng nhóm (Minh)
- Lan bị chấm 3 vòng, dù ngay vòng 1 Bảo đã báo trước rằng các vòng sau không đổi được kết quả. Lẽ ra nên chọn hướng (a) hoặc (b) Bảo đề xuất ngay sau vòng 1.
- Mai được giao 2 sản phẩm (kế hoạch chương trình và kế hoạch nội dung) trong một file mà phiếu giao việc không ghi giới hạn độ dài. Nên ghi trần độ dài và người đọc của từng file vào phiếu.
- Bàn giao khi còn lỗi đã biết cách sửa một dòng (tuyển trùng ~100 trđ, hoàn vốn T24 thay T26). Nên bắt sửa trước khi giao, vì số hoàn vốn là con số anh sẽ nhớ.
