# Kiểm định — 2026-11-14-khung-chuong-trinh-chuyen-doi

Người kiểm: Hà – Kiểm định · Ngày 14/11/2026
Hồ sơ đã đọc: `phieu-giao-viec.md`, `brief.md`, `nghien-cuu.md`, `mo_hinh.py`, `tai-chinh.md`, `tai-chinh.json`, `ke-hoach.md`, `giam-sat/*.md`.
Hà không sửa file của người khác. `mo_hinh.py` được chạy trên **bản sao trong thư mục tạm**, để không ghi đè `tai-chinh.json` đã nộp.

## Kết luận: **CHƯA ĐẠT**
Có 2 lỗi mức Chặn, 5 lỗi Nên sửa và 4 Gợi ý. Cả 2 lỗi Chặn cùng một gốc: **ngưỡng hoà vốn phòng ban chưa tính chi phí coach thêm khi vượt công suất**. Ngưỡng này lại là chỉ tiêu dùng để ra quyết định ở Cổng 3 của kế hoạch.

---

## 1. Hà đã tự kiểm chứng những gì

- **Chạy lại mô hình:** bản sao `mo_hinh.py` chạy thành công. JSON sinh ra **giống hệt** `tai-chinh.json` đã nộp.
- **Số khớp giữa các file** (output script = tai-chinh.md = ke-hoach.md): vốn ban đầu 296; tổng vốn 2.903; đáy −2.068 (T18); hoà vốn vận hành T19; hoàn vốn T44; luỹ kế T24 −1.813; NPV −233; IRR ~9%; chi phí cố định 166,8 / 332,6 / 470,3; ngưỡng 15,8 / 31,6 / 44,7; phễu T1–T6 (lead 167→705, đồng hành 0→10,5); ngưỡng +17% / −28% / +31%; thu nhập tư vấn viên 14,9 / 16,1 / 17,7. Tất cả đều khớp.
- **Hà tự tính lại bằng Python:**
  - Tổng vốn = 2.068,4 (đáy) + 835,0 (dự phòng) = 2.903,5 → 2.903. Đúng.
  - Lương + BH đội 8 người = 108 × 1,215 = 131,2. Đúng.
  - NPV 48 tháng @15%/năm tính độc lập = −233,2. Đúng.
  - Lead tự nhiên T6 = 50 + 850 × 4/22 = 204,5 → 205; T12 = 436. CPL bình quân T2 = 30 trđ ÷ 550 = 54.545 đ; T7 = 48.270 đ. Đúng.
  - "2,4 lần" = 25 ÷ 10,5 = 2,38. Đúng.
  - "Chuyển đổi thấp hơn 30% thì không bao giờ hoà vốn": chỉ đổi riêng hệ số chuyển đổi ×0,7 thì EBITDA vẫn âm suốt 48 tháng (cao nhất −108,9 trđ). Nhận định đúng.
- **Nguồn:** các số thị trường và pháp lý quan trọng trong ke-hoach.md (88%, ~55%, 70,5%, 34%, 27%, 4%, 81/76/67%, Mr Pips 1.568 tỷ/2.661 bị hại, NĐ 284/2026 phạt tới 200 trđ, Luật 75/2025, ITP 225 trđ, mốc 28/10/2026) đều có trong nghien-cuu.md kèm link. Số giả định đều ghi "giả định", "GĐ" hoặc "giả định Mai".
- **Không lẫn dự án:** không tìm thấy số liệu hay thương hiệu nào từ `fanpage/`, `ong-rung/` hay kênh Đạo Đức Đầu Tư.
- **Đủ yêu cầu của brief:** khung phễu, nội dung từng bước, gói và giá, uy tín (ngân hàng, văn phòng), pháp lý, mô hình tài chính, lộ trình, KPI, kế hoạch tài chính phòng ban và chiến lược + kế hoạch nội dung (định vị, kênh, trụ cột, định dạng, lịch 30 ngày, nội dung theo tầng phễu, KPI, tuân thủ). Có đủ.

---

## 2. Hai điểm Mai nêu

### (a) Công suất coach và ngưỡng hoà vốn 15,8: **CHƯA tính coach thêm**

- Mô hình theo tháng trong `chay()` (mo_hinh.py dòng 289–298) **có** tự thêm cặp coach + trợ giảng khi số học viên đang học vượt 40. Ở kịch bản cơ sở, tải coach cao nhất là 39,4 nên không phát sinh cặp thêm. Ở kịch bản Lạc quan có thêm 1–2 cặp. Phần này đúng.
- Hàm `hoa_von_phong_ban()` (dòng 405–423), nơi sinh ra con số 15,8 / 31,6 / 44,7, **không** kiểm tra công suất. Nó chia chi phí cố định của đội gốc cho 10,53 trđ đóng góp mỗi khách.
- Ở 15,8 khách mới/tháng và khoá học 3 tháng, số học viên đang học là 47,5, vượt mức 40 của 1 cặp coach (≈13,3 khách mới/tháng). Vậy phải thêm 1 cặp coach + trợ giảng với chi phí (20 + 11) × 1,215 = 37,7 trđ/tháng, cộng 0,4 trđ tuyển thay thế = 38,1 trđ/tháng.

Ngưỡng hoà vốn tính lại có công suất (Python, lặp tới khi số cặp coach ổn định):

| Giai đoạn | Ngưỡng cũ | Học viên đang học ở ngưỡng cũ / công suất | Cặp thêm | **Ngưỡng đúng (khách đồng hành mới/tháng)** | Số người | Doanh số cần/tháng | Lead cần/tháng |
|---|---|---|---|---|---|---|---|
| Khởi động | 15,8 | 47,5 / 40 | +1 | **19,4** | 10 | 312,9 trđ (cũ 254,7) | 1.105 (cũ 900) |
| Tăng trưởng | 31,6 | 94,7 / 80 | +1 | **35,2** | 19 | 565,9 trđ (cũ 507,8) | 2.000 (cũ 1.794) |
| Mở rộng | 44,7 | 134,0 / 160 | 0 | **44,7** (không đổi) | 24 | 718,2 trđ | 2.537 |

Hệ quả: dải "16 – <25: đội 8 tự nuôi được" ở Cổng 3 của ke-hoach.md sai. Trong khoảng 16–19,4 khách/tháng, đội (lúc này đã thành 10 người) **vẫn lỗ**. Câu ở mục 6.1 ("mô hình TC tự cộng thêm cặp coach khi vượt mức") đúng với mô hình theo tháng, nhưng không đúng với con số 15,8 mà kế hoạch đang dùng.

### (b) Chi phí "tuần 0" trước T1: **Phần lớn đã có, nhưng chưa ghi rõ và còn thiếu vài dòng nhỏ**

- Vốn ban đầu 296 trđ được tính ở **tháng 0**, tức trước T1. Khoảng này trùng với tuần 0. Các việc tuần 0 trong lộ trình đều có hạng mục tương ứng:
  - Pháp nhân, mã ngành, hợp đồng mẫu, ý kiến luật sư 10 câu → "Pháp lý khởi tạo" 30 trđ. Mai ghi rõ ở mục 5.2.
  - Nhận diện, website, LMS → 40 trđ.
  - Thiết bị → 80 + 96 trđ.
- T1 gánh đủ lương 8 người (131,2), chi phí tuyển 8 người (65,6) và 10 trđ quảng cáo. Như vậy việc tuyển người cũng đã có chi phí.
- Phần còn thiếu:
  1. tai-chinh.md không ghi "tháng 0 = tuần 0". Người đọc không biết khoản nào phải chi trước T1.
  2. Chưa có dòng lệ phí thành lập/đổi ngành nghề pháp nhân và tra cứu/đăng ký nhãn hiệu tên chương trình (ke-hoach mục 2.3 yêu cầu tra trước khi chốt tên). Hà chưa tra được mức phí nên không ghi số.
  3. Việc 30 trđ đủ cho ý kiến luật sư **bằng văn bản** về 10 câu chỉ là giả định, chưa có báo giá.
  4. Nếu Quản lý vận hành hay người nào khác phải nhận việc từ tuần 0 (2–4 tuần) thì có thêm khoảng 15–30 trđ lương. Mô hình chưa tính khoản này (Hà tự ước, giả định).
- Các khoản thiếu nhỏ so với quỹ dự phòng 835 trđ, nên Hà xếp mức **Nên sửa**, không phải Chặn.

---

## 3. Bảng lỗi

| # | Mức | Vị trí (file, mục) | Vấn đề | Cách sửa |
|---|---|---|---|---|
| 1 | **Chặn** | `mo_hinh.py` hàm `hoa_von_phong_ban()` dòng 405–423; `tai-chinh.md` mục 5 (bảng "Hoà vốn theo giai đoạn"), mục 9 ý 1–2; `tai-chinh.json` → `hoa_von_phong_ban` | Ngưỡng hoà vốn 15,8 / 31,6 chưa tính cặp coach + trợ giảng thêm khi số học viên đang học vượt 40/cặp. Ngưỡng đúng là **19,4 khách/tháng (10 người, doanh số 312,9 trđ)** và **35,2 khách/tháng (19 người, 565,9 trđ)**. Mở rộng giữ 44,7. Chỉ tiêu T6 "≥16 khách = hoà vốn đội 8" vì thế sai | Hùng: trong `hoa_von_phong_ban()` lặp tính số cặp coach cần = ceil(3 × khách/tháng ÷ 40), cộng chi phí cặp thêm vào chi phí cố định rồi tính lại. Cập nhật bảng mục 5, chỉ tiêu mục 9 và JSON; ghi thêm cột "số người thực tế ở ngưỡng" |
| 2 | **Chặn** | `ke-hoach.md` mục 1 ý 3–4; mục 6.1 (sơ đồ Khởi động, đoạn công suất); mục 6.5 KPI Ban quản lý; mục 7 bảng Cổng 3 (dòng "16 – <25") và cổng lên đội 17; Gợi ý hình 2 và 4 | Cổng quyết định dùng ngưỡng 15,8 và ghi "đội 8 tự nuôi được" trong dải 16–25. Thực tế, từ ~13,3 khách/tháng đội đã phải thêm coach, và phải đạt ≥19,4 mới hoà vốn. Cổng lên đội 17 (25 = 80% của 31,6) cũng phải tính lại theo ngưỡng 35,2 | Mai: sau khi Hùng chạy lại, đổi Cổng 3 thành: <8 dừng / 8–<19,4 giữ đội, sửa phễu / ≥19,4 hoà vốn (đội 10 người). Thêm mốc phụ "≥13 khách/tháng → tuyển cặp coach thứ 2". Đặt lại cổng lên đội 17 theo ngưỡng mới, ví dụ 80% × 35,2 ≈ 28 (giả định Mai, cần ghi rõ). Sửa đồng bộ cả 6 vị trí |
| 3 | Nên sửa | `ke-hoach.md` mục 1 ý 4 | Câu "phễu thật phải tốt hơn cơ sở ~2,4 lần, **tức gần với kịch bản Lạc quan**" chưa đúng. Kịch bản Lạc quan ở T6 chỉ đạt **17,9** khách. Cổng 25 khách ở T6 cao hơn cả Lạc quan (Lạc quan chỉ vượt 25 từ T7, khi đã tăng quảng cáo lên 60 trđ) | Sửa thành: "cao hơn cả kịch bản Lạc quan (17,9 khách ở T6)". Nên nói thẳng rằng với 30 trđ quảng cáo/tháng, việc qua cổng 25 trước T7 rất khó |
| 4 | Nên sửa | `tai-chinh.md` mục 7 và 9; `ke-hoach.md` mục 7 | Lộ trình mà kế hoạch khuyến nghị (giữ đội 8 nếu đạt 8–16 khách, mở rộng theo cổng) **chưa được mô hình hoá**. Các số vốn và hoàn vốn đang trích (2.903; T44) là của phương án tuyển theo lịch. Hà chạy thử trên bản sao (giữ đội Khởi động suốt 48 tháng, có tự thêm coach, cơ sở): hoà vốn vận hành **T13**, hoàn vốn **T28**, luỹ kế T24 **−395 trđ**. Số này chỉ để tham khảo, không phải số chính thức | Hùng: thêm kịch bản "giữ đội 8 + mở theo cổng" vào `mo_hinh.py`, in vốn cần, hoà vốn, hoàn vốn. Mai: dùng số này cho lộ trình khuyến nghị |
| 5 | Nên sửa | `tai-chinh.md` mục 4 "Vốn cần chuẩn bị"; `ke-hoach.md` mục 7 dòng "Tuần 0" | Điểm (b): chưa ghi rõ khoản nào chi trong tuần 0. Thiếu dòng lệ phí pháp nhân và tra cứu/đăng ký nhãn hiệu. Mức 30 trđ cho ý kiến luật sư bằng văn bản 10 câu chưa có báo giá. Chưa tính lương nếu có người nhận việc từ tuần 0 | Hùng: ghi "vốn ban đầu = chi trong tuần 0 (trước T1)" và tách dòng lệ phí pháp nhân + nhãn hiệu (ghi "cần báo giá"). Mai: ghi ai làm việc tuần 0 và có trả lương hay không |
| 6 | Nên sửa | `ke-hoach.md` mục 1 ý 6, mục 8 (dòng rủi ro 1), mục 9 trụ cột 3, mục 12 ngày 10 | Gọi Mr Pips là "vụ lừa đảo" và lên bài "Giải phẫu vụ Mr Pips". Theo NC, vụ này **đang xét xử, chưa có tin tuyên án**. Khẳng định trước bản án có rủi ro pháp lý (danh dự, uy tín) | Dùng chữ "bị cáo buộc lừa đảo", "vụ án đang xét xử". Bài ngày 10 bắt buộc qua luật sư như quy tắc mục 13 đã nêu, hoặc thay bằng vụ đã có bản án |
| 7 | Nên sửa | Thư mục `giam-sat/` | Phiếu giao việc bước 6 yêu cầu `giam-sat/chien-luoc-vong1.md` (Bảo chấm phần của Mai), nhưng **chưa có file này**. Ngoài ra, phiếu chấm Hùng vòng 1 không phát hiện lỗi công suất ở mục #1 | Trưởng nhóm: cho Bảo chấm ke-hoach.md trước khi bàn giao |
| 8 | Gợi ý | `nghien-cuu.md` (toàn bộ); `giam-sat/nghien-cuu-vong3.md` | Nghiên cứu "CHƯA ĐẠT, chỉ do môi trường" (không mở được trang gốc). Mọi số thị trường và pháp lý tối đa ở mức tin cậy TB. Ba file đã ghi rõ điều này | Khi bàn giao, giữ nguyên cảnh báo. Mọi điều khoản luật phải được luật sư đối chiếu toàn văn trước khi dùng với khách |
| 9 | Gợi ý | `mo_hinh.py` NHAN_SU "Mở rộng"; `ke-hoach.md` mục 6.1, 6.5 | Giai đoạn Mở rộng có 4 coach nhưng chỉ 3 trợ giảng, trong khi công suất được định nghĩa theo "cặp coach + trợ giảng" | Ghi rõ công suất tính theo coach, hoặc cho số trợ giảng bằng số coach |
| 10 | Gợi ý | `ke-hoach.md` mục 7 (Tuần 0 → T1) | Nếu Cổng 0 trễ (chưa có ý kiến luật sư) mà 8 người đã nhận việc từ T1 thì lương 131 trđ/tháng vẫn phải trả trong khi chưa được chạy quảng cáo | Chỉ ký hợp đồng lao động sau khi qua Cổng 0, hoặc ghi rõ phương án hoãn T1 |
| 11 | Gợi ý | `ke-hoach.md` mục 5.2 câu 7 | Cụm "chủ dự án (người nổi tiếng của kênh)" là giả định chưa xác minh, và nhắc tới kênh mà brief nói không dùng | Viết trung tính: "khi chủ dự án tự giới thiệu khoá học của mình trên kênh cá nhân" |

**Tổng: Chặn 2 · Nên sửa 5 · Gợi ý 4.**

## 4. Điều kiện để ĐẠT
1. Hùng sửa lỗi #1 (ngưỡng hoà vốn có tính công suất coach), chạy lại script và cập nhật tai-chinh.md + JSON.
2. Mai sửa lỗi #2 (Cổng 3, KPI, sơ đồ, gợi ý hình) theo số mới của Hùng.
3. Nên làm cùng lúc #3–#7. Riêng #7 cần Bảo chấm ke-hoach.md.
