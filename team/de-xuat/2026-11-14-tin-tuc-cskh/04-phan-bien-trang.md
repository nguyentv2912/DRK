# Phản biện của Trang — đề xuất bổ sung nhân sự 14/11/2026 (Linh, Thảo, sửa Ngọc/Phong/Quân/Vy)

Vai đọc: biên tập viên tài chính, chuyên gia quản trị cộng đồng, người rà tuân thủ nội dung tài chính ở Việt Nam và quy định nội dung của Facebook/TikTok.
Phạm vi: chỉ đọc file 00–03 và bối cảnh, không sửa file nào. Các nhận định pháp lý dưới đây là để rà soát rủi ro, **không thay cho ý kiến luật sư**. Những chỗ cần đối chiếu văn bản gốc được ghi "cần xác minh".

Kết luận ngắn: hướng đi đúng và đã nói thật về giới hạn công cụ. Nhưng **chưa nên duyệt nguyên trạng**. Có 3 lỗi sẽ làm hỏng ngay ngày đầu chạy: (1) công cụ làm ảnh chưa có, và kho media ghi đè làm mất ảnh; (2) số giá lấy qua WebSearch/WebFetch không đủ tin cậy cho một bài in số lên ảnh; (3) dữ liệu khách hàng sẽ bị commit vào repo công khai. Thêm vào đó là mâu thuẫn với thương hiệu "không bình luận mã cụ thể", và lịch chạy mới chưa được nối vào skill `fanpage-team`.

---

## Bảng tổng hợp

| # | File | Mức | Vấn đề | Đề xuất sửa |
|---|---|---|---|---|
| 1 | 01, 03 (Vy) | cao | `fanpage/tools/the_tin_tuc.py` không tồn tại. `media_repo.py put` mỗi lần tạo nhánh mồ côi rồi force push, nên đưa 3 ảnh thì chỉ ảnh cuối còn link. Lượt video 09:17 gọi `clear` còn có thể xoá ảnh trước khi Metricool chép | Viết công cụ trước khi duyệt. Sửa `media_repo` cho đưa nhiều file một lần. Vy chỉ `clear` khi mọi bài trong ngày đã ở `static.metricool.com`. Chưa có công cụ thì tạm đăng 1 ảnh |
| 2 | 01 | cao | Giá BTC/ETH/SOL lấy qua WebSearch (đoạn trích cũ) hoặc WebFetch (mô hình nhỏ tóm tắt lại, trang CoinGecko dựng bằng JS) dễ sai. Số lấy lúc 04:40 nhưng 07:30 mới đăng | Mỗi số phải khớp ≤ 1% giữa 2 nguồn độc lập. Ảnh ghi rõ "Số liệu lúc 04:40". Không đủ điều kiện thì bỏ số tuyệt đối. Xin chủ kênh mở 2 host API |
| 3 | 01, 03, KENH | cao | KENH.md ghi "Không làm: bình luận mã cụ thể", nhưng bản tin ngày nào cũng có bảng giá 3 coin tô xanh/đỏ kèm chỉ số Sợ hãi & Tham lam, trông như bảng tín hiệu. SOL còn đụng xung đột lợi ích với dự án Mr Pump (Solana) cùng brand Metricool | Chỉ giữ BTC + tổng vốn hoá (ETH là tuỳ chọn), bỏ SOL. Chỉ số Sợ hãi & Tham lam kèm chú thích "nhiệt kế cảm xúc, không phải tín hiệu". Cấm nhắc Mr Pump/memecoin Solana. Ghi ngoại lệ có điều kiện vào KENH.md |
| 4 | 01 | cao | Rủi ro pháp lý và nền tảng: tên "BẢN TIN SÁNG" dễ bị coi là "báo hoá"/đóng vai báo chí (NĐ 147/2024, Đ.36 k.7 — cần xác minh). Dịch lại bài Reuters/Bloomberg có thể vi phạm bản quyền. Tin hack sàn có thể thành bôi nhọ. Bối cảnh thí điểm sàn được cấp phép (NQ 05/2025/NQ-CP — cần xác minh). Boost bài crypto trên Meta phải xin phép | Đổi tên thành "NHÌN LẠI THỊ TRƯỜNG 24H". Viết thành ghi chú tổng hợp có dẫn nguồn. Mỗi nguồn trích tối đa 1 câu. Tin sàn chỉ đưa điều sàn hoặc cơ quan chức năng đã xác nhận. Không boost. Không nêu tên sàn kèm lời khen chê |
| 5 | 02 | cao | Thảo ghi `fanpage/cham-soc/<ngày>.md` có tên người bình luận, nội dung tin nhắn, ảnh chụp, trong khi repo DRK **công khai** và có commit + push. Rủi ro theo luật bảo vệ dữ liệu cá nhân (NĐ 13/2023; Luật BVDLCN 2025 — cần xác minh hiệu lực) và mất lòng tin | Ẩn danh bắt buộc. Không lưu ảnh chụp. Thư mục `cham-soc/` đưa vào `.gitignore` hoặc lưu Drive riêng. Thêm tiêu chí chặn |
| 6 | 00, 03, skill | cao | Lịch 04:40 và 21:00 chưa có chế độ nào trong `fanpage-team`. Ai gọi Bảo, ai đăng lúc 07:30? Linh và Thảo chưa có `ho-so.md`. `publish_mode: tu-dong` nghĩa là bài tin tài chính sẽ tự lên mà không người nào duyệt | Thêm chế độ `tin-tuc` và `cham-soc` vào skill. Tạo hồ sơ. 14 ngày đầu cho bản tin chạy chế độ nháp. Bảo chấm trễ sau 06:45 thì bỏ bản tin hôm đó, không đăng muộn |
| 7 | 03 (Ngọc, Phong) | cao | Kho giữ 3 kịch bản, quay trễ 1–3 ngày, tin lấy từ 3 ngày gần nhất, nên khi lên sóng sự kiện có thể đã 6–7 ngày. "Tuần này" sẽ sai nếu đăng sang tuần sau. Con số giá trong video thì cũ nhanh nhất | Video không đọc giá. Chỉ dùng biên độ đã làm tròn kèm mốc tháng ("giữa tháng mười một"). Thêm trường `su_kien` vào `ideas.json` làm nguồn duy nhất cho Phong |
| 8 | 02 | cao | Người thua lỗ nặng, có ý định tự hại hoặc là nạn nhân lừa đảo chỉ được "chuyển chủ kênh", chờ tới 21:00. Chưa có kịch bản cho lừa đảo "lấy lại tiền" (recovery scam) | Dấu hiệu nguy hiểm thì báo chủ kênh **ngay trong lượt** kèm câu trả lời an toàn soạn sẵn. Nạn nhân lừa đảo thì hướng dẫn trình báo công an, cảnh báo "dịch vụ lấy lại tiền" |
| 9 | 02 | trung bình | Cam kết "trả lời trong 2 giờ" không làm được ở giai đoạn 1, vì Thảo chỉ chạy khi chủ kênh dán. "21:00, sau Quân" sai giờ vì Quân chạy trong lượt 21:17. Mô tả có ghi TikTok nhưng giai đoạn 2 (Make) chỉ có Facebook | Đo theo cái kiểm soát được. Dời lịch sang sau Quân trong lượt 21:17. Sửa mô tả |
| 10 | 01 | trung bình | "Nguồn đã mở" chưa kiểm được: Reuters/Bloomberg có paywall nên sẽ bị lách bằng đoạn trích. Chưa có quy tắc kiểm hạn tin, tin dự thảo, tin cuối tuần | Lưu URL + giờ truy cập + ngày đăng của nguồn. Tin cũ hơn 36 giờ thì bỏ. Ghi trạng thái "đề xuất/dự thảo/đã ban hành". Có quy tắc riêng cho Chủ Nhật/Thứ Hai |
| 11 | 01 | trung bình | Tiêu chí chấm chưa đo đúng: "số trên ảnh trùng số trong bài" chấm bằng mắt dễ sót. Chưa có tiêu chí chặn cho tin cũ và tên sàn/dự án. "Mức độ ảnh hưởng" mở cửa cho dự đoán | Sinh ảnh và bài từ cùng một `so-lieu.json`. Thêm 2 tiêu chí chặn. Đổi thành "liên quan tới nhà đầu tư cá nhân" |
| 12 | 01 | trung bình | "Có skill 3 bước thì làm theo skill đó" có thể đè lên danh sách cấm và quy tắc nguồn | Ghi rõ thứ tự ưu tiên: brand.md + quy tắc nguồn > skill > khung tạm |
| 13 | 00, 03 | trung bình | Chủ kênh yêu cầu "fanpage 1–2 bài/ngày". Thêm bản tin 07:30 thì Facebook thành 2–3 bài/ngày. Ảnh bìa ghi "20:00 mỗi tối" | Hỏi chủ kênh trước. Đề xuất mặc định: bản tin Thứ Hai–Thứ Sáu, cuối tuần nghỉ hoặc làm 1 bản "nhìn lại tuần" |
| 14 | 03 (Quân, Vy) | trung bình | Mẫu `report.md` của Quân vẫn có mục "Trả lời bình luận gợi ý". Ngọc chọn câu hỏi Thứ Bảy từ `report.md`. Hai người cùng sửa `faq_replies.md`. Bài ảnh nhiều media trên Metricool chưa được kiểm (config mới kiểm REEL). Bản tin ghi vào `history.jsonl` sẽ làm nhiễu bước lọc trùng của Ngọc | Sửa đồng bộ prompt Quân, Ngọc và hồ sơ. Một người giữ FAQ. Vy thử 1 bản nháp POST nhiều ảnh. Thêm trường `loai` vào history |
| 15 | 02 | trung bình | Tiêu chí "phát hiện đúng spam/lừa đảo" là tiêu chí chặn nhưng Bảo không có gì để đối chiếu. Giai đoạn 2 tự trả lời cả "hỏi kiến thức" là quá rộng | Lập bộ 20 bình luận mẫu có đáp án. Giai đoạn 2 chỉ tự trả lời lời khen, tự ẩn bình luận có link lạ; mọi câu hỏi đều chờ duyệt |
| 16 | 01, 02 | thấp | Bài 150–300 chữ trong khi brand ghi 150–250. Mẫu FAQ hứa "link tài liệu ở bình luận ghim" nhưng `cta_link` đang trống | Thống nhất 180–280 chữ cho bản tin (ngoại lệ ghi trong prompt). Sửa mẫu FAQ |

---

## A. Rủi ro xuyên suốt (ảnh hưởng nhiều file)

### A1. Lịch chạy mới chưa nối vào hệ thống (#6) — cao
**Vấn đề.** Skill `fanpage-team` hiện chỉ có `kich-ban` (05:05) và `xu-ly` (09:17/10:17/21:17). File 03 thêm mốc 04:40, 07:30 và 21:00, nhưng không nói chế độ nào gọi Linh, ai gọi Bảo chấm, ai gọi Vy đăng. Linh và Thảo cũng chưa có `team/nhan-su/<mã>/ho-so.md`, trong khi Bảo chấm theo hồ sơ.
**Vì sao quan trọng.** Thiếu phần này thì prompt có hay đến đâu cũng không chạy. Còn một rủi ro nữa: `publish_mode = tu-dong` sẽ cho bài tin tài chính tự lên sóng lúc 07:30 khi chủ kênh còn ngủ. Sai một con số là sai công khai, có ảnh làm bằng chứng.
**Đoạn đề xuất (thêm vào `fanpage-team/SKILL.md`):**
> ## Chế độ `tin-tuc` (04:40 mỗi ngày)
> 1. Giao **Linh** (`tin-tuc-thi-truong`): "Ngày <YYYY-MM-DD>. Viết ban-tin.md, so-lieu.json, post.md, ảnh." → Bảo chấm theo `team/nhan-su/tin-tuc-thi-truong/ho-so.md`.
> 2. Hạn chót: 06:45 chưa ĐẠT → **không đăng bản tin hôm nay** (không đăng muộn, không đăng bản chưa đạt). `ban-tin.md` nội bộ vẫn giữ cho Ngọc.
> 3. ĐẠT → **Vy** hẹn đăng Facebook POST 07:30. 14 ngày đầu luôn `draft: true` (bất kể `publish_mode`); chủ kênh duyệt trên Metricool. Sau 14 ngày không lỗi số liệu, chủ kênh mới quyết định cho tự đăng.
> ## Chế độ `cham-soc` (chạy cuối lượt `xu-ly` 21:17, sau Quân; hoặc khi chủ kênh dán bình luận)
> Giao **Thảo** (`cham-soc-khach-hang`) → Bảo chấm.

Kèm theo: tạo `team/nhan-su/tin-tuc-thi-truong/ho-so.md` và `team/nhan-su/cham-soc-khach-hang/ho-so.md`, chép bảng tiêu chí đã sửa (mục B5, C6) vào đó.

### A2. Số bài mỗi ngày khác yêu cầu gốc (#13) — trung bình
**Vấn đề.** Chủ kênh yêu cầu "fanpage 1–2 bài/ngày". Đề xuất thêm bản tin 07:30 "không tính vào giới hạn 2 video", nên Facebook có tới 3 bài/ngày. Ảnh bìa trong KENH.md ghi "20:00 mỗi tối".
**Vì sao quan trọng.** Bài ảnh tin tức thường được ít tương tác hơn video nói chuyện. Đăng dày có thể kéo tương tác trung bình của trang xuống và ăn bớt lượt tiếp cận của Reel, mà Reel mới là sản phẩm chính trong KPI 90 ngày. Quan trọng hơn: đây là quyết định của chủ kênh, đội không nên tự quyết.
**Đề xuất (thêm vào 00-tong-quan.md, mục "Cần chủ kênh chọn"):**
> Bản tin sáng làm cho Facebook có thể lên 3 bài/ngày. Chọn một: (a) bản tin mỗi ngày; (b) **Thứ Hai–Thứ Sáu**, Thứ Bảy/Chủ Nhật nghỉ, Chủ Nhật thay bằng 1 bài "Nhìn lại tuần" (khuyến nghị); (c) bản tin thay chỗ khung trưa khi kho video trống.

### A3. Mâu thuẫn với thương hiệu "không bình luận mã cụ thể" (#3) — cao
**Vấn đề.** KENH.md: "Không làm: gọi kèo, khoe lãi, hứa lợi nhuận, **bình luận mã cụ thể**". Linh phải in mỗi sáng giá và % 24h của BTC, ETH, SOL, tô xanh/đỏ, cạnh chỉ số Sợ hãi & Tham lam. Dù không viết chữ "mua", bố cục đó trông giống hệt bảng tín hiệu của các kênh gọi kèo. Người đọc 22–45 tuổi "từng thua vì cảm xúc" sẽ coi nó là tín hiệu vào lệnh. Riêng SOL: brand Metricool 7808796 còn nối với dự án **Mr Pump (Solana)**. Ngày nào cũng đưa SOL lên trang "đạo đức đầu tư" là xung đột lợi ích, chỉ cần một người phát hiện là mất uy tín.
**Vì sao quan trọng.** Định vị kênh là tài sản lớn nhất. Một trang tâm lý mà sáng nào cũng có bảng giá thì sẽ trượt dần thành trang tín hiệu.
**Đoạn đề xuất — thay mục "Số liệu nền" trong file 01:**
> - Số liệu nền (tối đa 4 số): giá BTC và % 24h; tổng vốn hoá thị trường crypto và % 24h; chỉ số Sợ hãi & Tham lam (ghi kèm chú thích "nhiệt kế cảm xúc của đám đông — không phải tín hiệu mua/bán"); tuỳ chọn ETH. **Không đưa SOL hay bất kỳ altcoin nào vào bảng số.** Không bao giờ nhắc Mr Pump, memecoin hay dự án trên Solana mà chủ kênh có liên quan.
> - Tin về một coin/dự án cụ thể chỉ được đưa khi đó là sự kiện hệ thống (hack, sàn sập, cơ quan quản lý xử lý), và viết ở góc rủi ro/bài học, không nhận xét giá.

**Thêm vào KENH.md (mục Không làm):**
> Ngoại lệ duy nhất: bài "Nhìn lại thị trường 24h" được nêu giá BTC, tổng vốn hoá và chỉ số tâm lý như dữ kiện có nguồn, không nhận định, không dự đoán, luôn đi kèm một bài học kỷ luật.

---

## B. File 01 — Linh, Biên tập tin tức thị trường

### B1. Công cụ ảnh và kho media (#1) — cao
**Vấn đề.**
- Prompt bảo "Dùng `fanpage/tools/the_tin_tuc.py`" nhưng trong `fanpage/tools/` chỉ có `edit_video.py`, `khop_kich_ban.py`, `make_video.py`, `media_repo.py`. Không có công cụ thì Linh sẽ tự viết PIL mỗi sáng: mỗi ngày một kiểu, dễ lỗi font tiếng Việt (máy hiện chỉ có DejaVu), không ổn định nhận diện.
- `media_repo.py put` mỗi lần tạo **nhánh mồ côi mới rồi force push**, và chỉ nhận 1 file. Đưa `anh-1`, `anh-2`, `anh-3` lần lượt thì chỉ `anh-3` còn link. Ngoài ra lượt `xu-ly` 09:17 có `put` video mới và `clear`, nên nếu Metricool chưa chép ảnh bản tin thì ảnh sẽ mất.
**Vì sao quan trọng.** Ngày chạy đầu tiên bài ảnh sẽ hỏng hoặc chỉ còn 1 ảnh, và Vy không có cách nào biết trước.
**Đề xuất.**
1. Viết và kiểm thử `the_tin_tuc.py` **trước khi duyệt**: đầu vào `so-lieu.json` (xem B5), đầu ra 1080x1350 PNG, font hỗ trợ tiếng Việt (nên đưa font Be Vietnam Pro hoặc Noto Sans, giấy phép OFL, vào `fanpage/tools/fonts/`).
2. Sửa `media_repo.py`: `put` nhận nhiều file trong một commit (`put <f1> <f2> <f3> --prefix tin-<ngày>`).
3. Thêm vào prompt Vy:
> Chỉ chạy `media_repo.py clear` khi **mọi** bài hẹn đăng trong ngày (kể cả bản tin 07:30) đã có media `static.metricool.com`. Bản tin nhiều ảnh: đưa tất cả ảnh trong **một** lệnh `put`.
4. Tạm thời, khi chưa sửa xong: bản tin chỉ có **1 ảnh** (bảng thị trường + bài học hôm nay).

### B2. Độ tin cậy và thời điểm của số liệu (#2) — cao
**Vấn đề.** File 00 ghi API giá bị chặn. Đi đường vòng có hai cách, cả hai đều yếu: đoạn trích WebSearch thường là giá cũ từ vài giờ đến vài ngày; WebFetch trả về bản do mô hình nhỏ tóm tắt, mà trang CoinGecko/CMC dựng bằng JavaScript, nên "số đọc được" có thể là số được tóm tắt sai. Số lấy lúc 04:40 nhưng 07:30 mới lên; crypto chạy 24/7 nên ba giờ có thể chênh vài phần trăm. Chuyên gia biên tập tài chính luôn ghi **thời điểm chốt số** và đối chiếu chéo.
**Vì sao quan trọng.** Số in trên ảnh không sửa được sau khi đăng. Sai một lần thì người đọc soi mãi, mà kênh lại sống bằng chữ "tỉnh táo".
**Đoạn đề xuất — thay đoạn "Chỉ lấy từ trang đã mở và đọc…":**
> - Mỗi số phải lấy từ **2 nguồn độc lập** (vd. CoinGecko và CoinMarketCap, hoặc trang sàn lớn), mở bằng WebFetch, lệch nhau ≤ 1%. Ghi cả hai giá trị, giờ lấy và URL vào `so-lieu.json`. Đoạn trích của WebSearch **không** được tính là nguồn số.
> - Không có 2 nguồn khớp → không in số tuyệt đối; chỉ viết xu hướng có nguồn ("BTC giảm hơn 5% trong 24 giờ, theo CoinDesk").
> - Ảnh và bài luôn ghi "Số liệu lúc HH:MM dd/mm (giờ VN)". Không viết "hiện tại", "lúc này".
> - Số tròn theo quy ước: giá BTC tròn đến hàng trăm USD, % lấy 1 chữ số thập phân, vốn hoá viết "nghìn tỷ USD" với 2 chữ số.

**Kiến nghị gửi chủ kênh (ghi trong 00):** mở 2 host `api.coingecko.com`, `api.alternative.me` thì bài này đáng tin hơn hẳn. Đây là việc nên làm **trước** khi bật tự đăng.

### B3. Pháp lý, nền tảng, bản quyền (#4) — cao
**Vấn đề.**
- **"BẢN TIN SÁNG"**: NĐ 147/2024/NĐ-CP (Điều 36 khoản 7) cấm người dùng mạng xã hội sản xuất nội dung dưới hình thức phóng sự, điều tra, phỏng vấn báo chí, và cơ quan quản lý đang xử lý tình trạng "báo hoá" (cần xác minh văn bản gốc). Một fanpage cá nhân mỗi sáng ra "bản tin" có tiêu đề kiểu báo là đang đứng gần vạch đó.
- **Bối cảnh Việt Nam**: thị trường tài sản mã hoá đang thí điểm, chỉ tổ chức được cấp phép mới được cung cấp dịch vụ (NQ 05/2025/NQ-CP — cần xác minh trạng thái tại thời điểm đăng). Bài nhắc sàn chưa được cấp phép theo hướng trung tính hoặc tích cực có thể bị hiểu là quảng bá.
- **Bôi nhọ**: brand.md cấm "bôi nhọ sàn cụ thể", nhưng tin "sàn X bị hack" là tin sàn cụ thể. Không có quy tắc thì sớm muộn sẽ viết suy đoán ("sàn X có dấu hiệu gian lận").
- **Bản quyền**: tóm tắt sự kiện thì được, dịch lại nguyên đoạn bài Reuters/Bloomberg/CoinDesk thì không.
- **Meta/TikTok**: đăng tự nhiên về crypto trên Facebook không bị cấm, nhưng **quảng cáo** (gồm cả boost bài) về crypto phải được Meta cho phép trước. TikTok cấm nội dung thương mại/branded quảng bá crypto từ 2021, và có tiêu chuẩn riêng cho For You feed. Prompt đã ghi "Không đăng TikTok" cho bản tin, đúng, nên giữ.
**Đoạn đề xuất — thêm mục "0. Ranh giới pháp lý & nền tảng" ngay đầu file 01:**
> - Tiêu đề bài: "NHÌN LẠI THỊ TRƯỜNG 24H — dd/mm" (không dùng "bản tin", "tin nóng", "độc quyền", "phóng sự"). Viết như ghi chú tổng hợp của một nhà đầu tư, có dẫn nguồn; không phỏng vấn, không tự điều tra, không đưa tin chưa có nguồn công khai.
> - Mỗi nguồn trích nguyên văn tối đa 1 câu, đặt trong ngoặc kép, kèm tên nguồn. Còn lại viết lại bằng lời của mình.
> - Tin về sàn/dự án cụ thể: chỉ nêu điều sàn, dự án hoặc cơ quan chức năng **đã công bố**, kèm nguồn; không suy đoán nguyên nhân, không gán động cơ, không dùng tính từ đánh giá ("lừa đảo", "sập", "uy tín") khi nguồn chưa dùng.
> - Không nêu tên sàn theo hướng giới thiệu, so sánh, khen. Tin pháp lý Việt Nam: ghi đúng tên văn bản, số hiệu, trạng thái (dự thảo / đã ban hành / có hiệu lực từ …).
> - Không đề xuất boost/quảng cáo bài này. Không đăng TikTok.

### B4. Nguồn "đã mở", tin cũ, ngày nghỉ (#10) — trung bình
**Vấn đề.** Reuters và Bloomberg thường chặn hoặc có paywall nên WebFetch không mở được. "Nguồn đã mở" sẽ âm thầm thành "đoạn trích tìm kiếm". Chưa có quy tắc về **ngày đăng của nguồn**: WebSearch rất hay trả tin của tuần trước. Dữ liệu dòng tiền ETF thường công bố sau khi thị trường Mỹ đóng cửa nên lúc 04:40 có thể chưa có. Cuối tuần gần như không có tin vĩ mô hay ETF.
**Đoạn đề xuất — thay đoạn "Mỗi sự kiện ≥ 1 nguồn đã mở…":**
> - "Đã mở" = WebFetch đọc được nội dung bài. Ghi vào `ban-tin.md` cho từng tin: URL, ngày giờ đăng của nguồn, giờ bạn truy cập. Không mở được (paywall) → tìm bài cùng sự kiện ở nguồn mở được; không có → ghi "chưa xác nhận" hoặc bỏ.
> - Chỉ dùng tin có ngày đăng trong **36 giờ** trước giờ chạy. Tin cũ hơn chỉ được nhắc như bối cảnh, ghi rõ ngày.
> - Ghi trạng thái cho tin chính sách: đề xuất / dự thảo / đã thông qua / có hiệu lực.
> - Dòng tiền ETF: dùng số của **ngày giao dịch gần nhất đã công bố** và ghi ngày đó; không có thì bỏ.
> - Thứ Hai: gom tin từ 18:00 Thứ Sáu. Ít hơn 3 tin đạt chuẩn → bài ngắn 2 tin, không độn tin yếu.

### B5. Tiêu chí chấm và cách làm cho số khớp (#11) — trung bình
**Vấn đề.** "Số trên ảnh trùng số trong bài" đang dựa vào Bảo soi mắt. Cách làm của tòa soạn chuyên nghiệp là **một nguồn dữ liệu duy nhất**: bảng số sinh ra cả đồ hoạ lẫn bài viết. Thiếu hai tiêu chí chặn quan trọng: tin cũ, và nêu tên sàn/dự án theo hướng khen chê. "Mức độ ảnh hưởng" trong bản tin nội bộ là cửa ngõ cho dự đoán ("ảnh hưởng mạnh tới giá").
**Đoạn đề xuất — thêm vào mục 2:**
> Ghi `fanpage/tin-tuc/<ngày>/so-lieu.json` trước tiên: `{"chot_luc": "HH:MM", "so": [{"ten": "BTC", "gia": ..., "pct_24h": ..., "nguon": ["url1","url2"]}], "tin": [{"tieu_de": "", "nguon": "", "url": "", "dang_luc": ""}], "bai_hoc": ""}`. Ảnh sinh từ file này bằng `the_tin_tuc.py`; số trong `post.md` chép từ file này, không gõ tay.
> Thay "mức độ ảnh hưởng" bằng "**vì sao nhà đầu tư cá nhân nên biết**" (rủi ro, quyền lợi, thói quen), không nói ảnh hưởng tới giá.

**Bảng tiêu chí đề xuất (thay bảng cũ):**
| Tiêu chí | Trọng số | Chặn |
|---|---|---|
| Mỗi số có 2 nguồn khớp ≤ 1% và giờ chốt; mỗi tin có URL, ngày đăng ≤ 36 giờ | 25 | Chặn |
| Không dự đoán giá, không khuyến nghị, không altcoin trong bảng số, có miễn trừ | 20 | Chặn |
| Tin về sàn/dự án chỉ nêu điều đã công bố; không khen chê; trích ≤ 1 câu mỗi nguồn | 10 | Chặn |
| Ảnh và bài cùng sinh từ `so-lieu.json` (Bảo đối chiếu tự động) | 10 | Chặn |
| Bài học kỷ luật rút ra cụ thể, dùng được (không phải câu chung chung) | 15 | |
| Cấu trúc 3 bước, 180–280 chữ, dễ đọc trên điện thoại | 10 | |
| Góc đúc kết cho Ngọc/Phong có `su_kien` đủ trường | 5 | |
| Ảnh rõ, đúng nhận diện, font tiếng Việt không lỗi | 5 | |

Lý do giảm "góc đúc kết" từ 15 xuống 5: giá trị của nó được đo ở đầu ra của Ngọc rồi (mục D1). Lý do tăng trọng số "bài học": đó là điều làm bản tin này khác 100 trang tin crypto khác.

### B6. Thứ tự ưu tiên khi có skill "3 bước" (#12) — trung bình
**Vấn đề.** "Nếu có skill … làm theo skill đó cho phần viết bài". Skill nằm trên máy chủ kênh, chưa ai đọc. Nếu skill có mẫu kiểu "CTA chốt đơn", "link nhóm", hay độ dài khác, thì Linh sẽ theo skill.
**Đoạn đề xuất:**
> Nếu có `.claude/skills/bai-dang-3-buoc/SKILL.md`: dùng **cấu trúc và kỹ thuật viết** của skill. Khi skill mâu thuẫn với `brand.md`, mục 0 và quy tắc nguồn của prompt này thì **brand.md và prompt này thắng**. Ghi mâu thuẫn gặp phải vào cuối `ban-tin.md` để trưởng nhóm sửa.

### B7. Độ dài (#16) — thấp
Brand.md quy định caption 150–250 chữ, bản tin cho 150–300. Đề xuất ghi rõ ngoại lệ: "Bài nhìn lại thị trường: 180–280 chữ (ngoại lệ so với brand.md vì có 3–5 tin)." Như vậy Hà kiểm định không chấm sai.

### Điều tốt nên giữ ở file 01
- "Không có số tin cậy → không đưa số đó" và "tin chỉ có 1 nguồn yếu → ghi 'chưa xác nhận' hoặc bỏ": đúng chuẩn biên tập, giữ nguyên câu chữ.
- Danh sách bỏ: "tin đồn, tin dự án tự PR, 'coin X sắp x10', nội dung tài trợ": rất đúng.
- Câu mở vai "chính xác trước, hấp dẫn sau" và "tin tức là chất liệu để giữ kỷ luật, không phải lý do để vào lệnh": đây là la bàn cho Linh, nên giữ.
- Chạy 04:40, trước lượt kịch bản 05:05: thứ tự đúng.
- "Không dùng ảnh/logo/biểu đồ chụp của báo khác": chặn được rủi ro bản quyền ảnh.
- "Không đăng TikTok" cho bản tin: đúng, vì TikTok khắt khe với nội dung tài chính dạng tin, và ảnh tĩnh cũng không hợp nền tảng.
- Ví dụ góc đúc kết "BTC giảm 8% → bài học về đòn bẩy" đúng kiểu nối tin với trụ cột thương hiệu.

---

## C. File 02 — Thảo, Quản lý & Chăm sóc khách hàng

### C1. Dữ liệu cá nhân trong repo công khai (#5) — cao
**Vấn đề.** Thảo ghi `fanpage/cham-soc/<ngày>.md` và cập nhật `faq_replies.md`. Cả `fanpage/` được commit + push lên `github.com/.../DRK`, mà skill ghi rõ đây là "repo công khai". Nội dung chủ kênh dán sẽ có tên Facebook, nội dung tin nhắn riêng, số tiền thua lỗ, có khi cả số điện thoại hay ví. `.gitignore` chỉ chặn `*.jpg/*.mp4`, không chặn `.md` hay `.png`.
**Vì sao quan trọng.** Đưa tin nhắn riêng của người theo dõi lên mạng công khai là vi phạm nghiêm trọng về bảo vệ dữ liệu cá nhân (NĐ 13/2023/NĐ-CP; Luật Bảo vệ dữ liệu cá nhân 2025 — cần xác minh ngày hiệu lực và mức phạt). Với một kênh dạy "cảnh giác", lộ chuyện này là sụp uy tín.
**Đoạn đề xuất — thêm mục "Bảo mật dữ liệu người theo dõi (không ngoại lệ)":**
> - Không ghi tên, ảnh đại diện, số điện thoại, email, địa chỉ ví, số tiền cụ thể, hay bất kỳ chi tiết nào nhận ra được người viết. Thay bằng mã: `BL-<ngày>-<n>` (bình luận), `TN-<ngày>-<n>` (tin nhắn). Câu hỏi đưa sang Ngọc phải viết lại thành câu chung ("Một bạn hỏi: …").
> - Không lưu ảnh chụp màn hình vào repo. Đọc xong thì thôi.
> - File chi tiết ghi ở `fanpage/cham-soc/` — thư mục này **phải** nằm trong `.gitignore` (trưởng nhóm kiểm trước lượt đầu). Thứ duy nhất được commit: số đếm theo loại và câu hỏi đã ẩn danh.
> - Tài khoản lừa đảo/mạo danh là ngoại lệ: được ghi tên hiển thị và link hồ sơ để chủ kênh báo cáo, nhưng chỉ trong file không commit.

### C2. Người đang khủng hoảng và nạn nhân lừa đảo (#8) — cao
**Vấn đề.** Prompt có "người đang khủng hoảng vì thua lỗ nặng → chuyển chủ kênh, kèm gợi ý lời động viên và khuyên tìm hỗ trợ", nhưng: (a) không phân biệt "buồn vì lỗ" với "có dấu hiệu muốn tự hại"; (b) lượt tổng hợp tới 21:00 mới chạy; (c) "tìm hỗ trợ" không cụ thể; (d) không có kịch bản cho nạn nhân bị lừa. Với nạn nhân lừa đảo, rủi ro lớn nhất là bị lừa lần hai bởi "dịch vụ lấy lại tiền" (recovery scam), và những kẻ này thường bình luận ngay dưới bài của trang.
**Đoạn đề xuất — thay mục 3:**
> 3. **Báo chủ kênh NGAY trong lượt đang chạy** (dòng đầu tiên của câu trả lời, ghi "KHẨN"), không chờ tổng hợp tối:
>    - Có dấu hiệu muốn tự hại, tuyệt vọng ("không muốn sống", "hết đường"): soạn câu trả lời ngắn, ấm, không giảng đạo lý, không bàn tiền; mời nhắn tin riêng; khuyên gọi ngay người thân hoặc đường dây hỗ trợ tâm lý / cấp cứu 115 (chủ kênh xác minh và ghi số đường dây hỗ trợ tâm lý vào `faq_replies.md` một lần).
>    - Nạn nhân lừa đảo: thể hiện cảm thông; khuyên lưu bằng chứng (giao dịch, tin nhắn) và **trình báo cơ quan công an nơi cư trú**; cảnh báo rõ: "Bất kỳ ai nhận 'lấy lại tiền' với phí trước đều là lừa đảo lần hai." Không giới thiệu luật sư, dịch vụ, nhóm nào.
>    - Đe doạ, pháp lý, báo chí, hợp tác có tiền: không trả lời, chỉ báo chủ kênh.
> - Bình luận chào mời "lấy lại tiền", "hỗ trợ rút tiền", "inbox mình chỉ cách": phân loại **Lừa đảo**, đề nghị ẩn + chặn + báo cáo, soạn 1 bình luận cảnh báo ghim dưới bài.

Thêm cho mạo danh: "Gặp trang/tài khoản mạo danh Đạo Đức Đầu Tư → soạn sẵn nội dung để chủ kênh báo cáo mạo danh qua công cụ báo cáo của Facebook/TikTok, và đề xuất bài ghim: 'Page không bao giờ nhắn tin trước, không có nhóm VIP, không nhận tiền ủy thác'."

### C3. Cam kết thời gian và lịch chạy (#9) — trung bình
**Vấn đề.**
- "Mọi người hỏi đều được trả lời tử tế trong 2 giờ (08:00–22:00)": ở giai đoạn 1 Thảo chỉ làm khi chủ kênh dán, nên thời gian phản hồi phụ thuộc chủ kênh. Đặt mục tiêu không kiểm soát được thì Bảo không chấm được.
- "Hằng ngày (21:00, sau Quân)": Quân chạy trong lượt `xu-ly` 21:17, tức **sau** 21:00. Thảo sẽ đọc báo cáo trống.
- Mô tả có ghi "fanpage và TikTok", nhưng giai đoạn 2 với Make (Facebook Pages) không đọc được bình luận TikTok.
**Đoạn đề xuất:**
> Mục tiêu: (giai đoạn 1) mỗi lô bình luận chủ kênh dán được trả về **đủ câu trả lời soạn sẵn trong cùng lượt**, xếp theo mức ưu tiên (KHẨN → lừa đảo → câu hỏi → khen). (Giai đoạn 2, khi có dữ liệu) ≥ 90% bình luận Facebook có câu hỏi được trả lời trong 12 giờ.
> Lịch: chạy cuối lượt 21:17, sau Quân.
> Mô tả: "…bình luận, tin nhắn Facebook (TikTok: chỉ khi chủ kênh dán)".

### C4. Đồng bộ FAQ và mẫu trả lời (#14, #16) — trung bình
**Vấn đề.** Sau khi sửa, Quân vẫn có quyền "bổ sung loại bình luận mới vào faq_replies.md" (prompt Quân mục 2) và Thảo cũng vậy: hai người cùng ghi một file. Trong FAQ hiện tại, mẫu "Hỏi học ở đâu" hứa "Link tài liệu mình để ở bình luận ghim" trong khi `cta_link` trống, tức là hứa điều không có. Mẫu "Than thua lỗ" mở bằng lời khuyên hành động ("Tạm nghỉ… cắt lỗ") trước khi đồng cảm, nên đối với người đang đau sẽ nghe lạnh lùng.
**Đề xuất.**
> Thảo là người **duy nhất** sửa `faq_replies.md`. Quân chỉ ghi câu hỏi mới vào report, Thảo gom lại. Mỗi lần sửa: không xoá dòng cũ, thêm cột "cập nhật dd/mm".
> Sửa mẫu "Hỏi học ở đâu": "Bạn theo dõi page nhé, mỗi ngày có 1 bài về kỷ luật. Bạn muốn tìm hiểu phần nào trước — tâm lý hay quản lý vốn?"

### C5. Giai đoạn 2 tự động — thu hẹp phạm vi tự trả lời (#15) — trung bình
**Vấn đề.** Cho tự trả lời "hỏi kiến thức có sẵn trong FAQ" thì một mô hình phân loại sai sẽ đăng công khai câu trả lời sai ngữ cảnh. Chẳng hạn "cắt lỗ ở đâu?" bị hiểu là hỏi kiến thức trong khi người hỏi đang muốn được chỉ lệnh. Messenger còn có quy tắc cửa sổ 24 giờ cho tin nhắn của trang.
**Đoạn đề xuất:**
> Giai đoạn 2 chỉ tự động: (a) trả lời lời khen bằng 1 trong 5 mẫu xoay vòng; (b) **ẩn** (không xoá) bình luận chứa link lạ, số điện thoại, "inbox", "lấy lại tiền", rồi ghi vào danh sách để chủ kênh xem lại. Mọi câu hỏi, kể cả có trong FAQ, đều soạn sẵn và chờ chủ kênh bấm duyệt. Không tự gửi tin nhắn Messenger.

### C6. Tiêu chí chấm của Thảo (#15) — trung bình
**Vấn đề.** "Phát hiện đúng spam, lừa đảo, mạo danh" là tiêu chí chặn nhưng Bảo không có đáp án để đối chiếu. Chưa có tiêu chí cho bảo mật dữ liệu và xử lý khẩn.
**Đề xuất:** tạo `team/nhan-su/cham-soc-khach-hang/bo-kiem-tra.md`: 20 bình luận mẫu (đã ẩn danh) có đáp án phân loại, gồm 3 lừa đảo "lấy lại tiền", 2 mạo danh, 1 dấu hiệu tự hại, 3 hỏi kèo trá hình. Bảo chạy bộ này mỗi khi prompt Thảo đổi.
| Tiêu chí | Trọng số | Chặn |
|---|---|---|
| Không tư vấn đầu tư, không hứa lợi nhuận, không xin thông tin nhạy cảm | 25 | Chặn |
| Không lưu dữ liệu nhận diện cá nhân vào file được commit | 15 | Chặn |
| Trường hợp KHẨN (tự hại, nạn nhân lừa đảo, đe doạ) được báo ngay, câu trả lời an toàn | 15 | Chặn |
| Phân loại đúng ≥ 18/20 trên bộ kiểm tra; không bỏ sót lừa đảo/mạo danh | 15 | Chặn |
| Câu trả lời đúng giọng kênh, ngắn, đồng cảm trước khi khuyên | 15 | |
| FAQ cập nhật; câu hỏi hay (đã ẩn danh) chuyển cho Ngọc | 15 | |

### Điều tốt nên giữ ở file 02
- "**Không bao giờ hỏi mật khẩu, mã OTP, khoá ví, số tài khoản**": in đậm như hiện tại, giữ nguyên.
- Tách rõ giai đoạn 1 (chủ kênh dán) và giai đoạn 2 (Make): nói thật về giới hạn, không hứa quá khả năng.
- Danh sách 7 loại phân loại, nhất là có tách riêng "Hỏi 'mua coin gì'" và "Lừa đảo/mạo danh": đúng thực tế kênh crypto Việt Nam.
- Danh sách "chuyển lên chủ kênh, không tự trả lời" (đe doạ, pháp lý, báo chí, hợp tác có tiền): đúng.
- Vòng khép kín "câu hỏi hay → Ngọc → video Thứ Bảy": biến chăm sóc khách hàng thành nguồn nội dung. Đây là điểm mạnh nhất của file.
- Không cấp công cụ đăng bài cho Thảo: đúng, vì giảm rủi ro tự trả lời sai.

---

## D. File 03 — Sửa Ngọc, Phong, Quân, Vy

### D1. Tin cũ đi vào video và nguồn số cho Phong (#7) — cao
**Vấn đề.** Kho luôn có 3 kịch bản chưa quay, mỗi kịch bản viết cho "ngày đăng dự kiến" là hôm nay + k − 1, chủ kênh quay trễ 1–3 ngày, và Ngọc lấy sự kiện "trong 3 ngày gần nhất". Cộng lại, sự kiện có thể đã 6–7 ngày khi lên sóng. "Tuần này" sẽ sai khi video đăng sang tuần sau. Con số giá ("BTC giảm 8%") là thứ cũ nhanh nhất, và người xem sẽ bình luận "số sai rồi". Thêm nữa: Phong được bảo "con số chỉ lấy từ bản tin của Linh", nhưng Phong chỉ được giao `ideas.json` + `post.md`, không có đường dẫn tới bản tin, và cũng chưa có trường dữ liệu nào để chép. Ngọc vẫn còn bước (c) "1–2 lượt WebSearch về chuyện thị trường", nên sẽ có hai nguồn số có thể lệch nhau.
**Đoạn đề xuất — thay phần Ngọc:**
> - Thay bước (c) của Phần A bằng: đọc `fanpage/tin-tuc/<3 ngày gần nhất>/ban-tin.md`; chỉ WebSearch thêm khi bản tin không có. Không tự lấy số từ nơi khác.
> - Dùng sự kiện → ghi vào `ideas.json`: `"su_kien": {"mo_ta": "", "ngay": "YYYY-MM-DD", "nguon": "", "url": "", "so_lieu": "biên độ đã làm tròn, vd 'hơn 5%'", "con_dung_neu_dang_sau": 7}`. Sự kiện mà sau 7 ngày nghe đã cũ (vd. "giá hôm qua") → không dùng cho video, để cho bản tin.
> - Sự kiện chỉ là mở đầu (~20%), phần chính là bài học dùng lâu. Video không nêu giá cụ thể, chỉ nêu biên độ làm tròn.

**Thay phần Phong:**
> - Hook mở bằng sự kiện thì dùng mốc tuyệt đối, ngắn: "giữa tháng mười một", "đầu tháng này", "mới đây". **Không dùng** "hôm nay", "hôm qua", "tuần này".
> - Số chỉ lấy từ `ideas.json → su_kien.so_lieu`, viết bằng chữ, làm tròn xuống ("hơn năm phần trăm"); không đọc giá coin. Thêm thẻ chữ nguồn trong `edit_plan.json`: `{"trigger": "<cụm có thật>", "text": "NGUỒN: COINDESK, 12/11", "accent": "gold", "sec": 2.5}`.

### D2. Ngọc: giữ kỷ luật chọn chủ đề — tốt, chỉ thêm tiêu chí đo
Phần "giữ chuyên mục theo thứ, ưu tiên đúc kết từ sự kiện nếu có góc phù hợp" là **đúng**: không để tin tức phá lịch trụ cột. Nên thêm vào hồ sơ Ngọc 1 tiêu chí (không chặn, 10 điểm): "Nếu dùng sự kiện: có `su_kien` đủ trường, dùng mốc thời gian không lỗi thời, sự kiện ≤ 20% nội dung." Còn yêu cầu gốc "đúc kết hằng ngày" thì nên đo nhẹ: mỗi tuần **ít nhất 2/7** kịch bản có liên hệ sự kiện, không bắt buộc ngày nào cũng có. Bắt ngày nào cũng gắn tin sẽ ép ghép gượng và làm video mau cũ.

### D3. Quân và Thứ Bảy (#14) — trung bình
**Vấn đề.** File 03 chỉ ghi một dòng "chuyển phần soạn trả lời sang Thảo", nhưng không sửa: (a) mục 2 trong prompt Quân (soạn 5 câu mẫu + cập nhật FAQ); (b) mẫu `report.md` có mục "Trả lời bình luận gợi ý cho bài hôm nay" và bảng "5 dòng" agent; (c) Ngọc Thứ Bảy "lấy câu hỏi hay nhất từ `report.md` gần nhất", trong khi câu hỏi giờ nằm ở chỗ Thảo; (d) hồ sơ Quân vẫn ghi "soạn trả lời bình luận".
**Đoạn đề xuất:**
> Quân: xoá mục 2; trong report.md thay mục "Trả lời bình luận gợi ý" bằng "Câu hỏi mới thấy trong số liệu (chuyển Thảo)"; bảng agent thêm dòng "Nhìn lại thị trường (Linh)". Thêm số liệu bài 07:30: lượt tiếp cận, tương tác, so với trung bình bài video, để chủ kênh quyết định sau 30 ngày có giữ bản tin hay không.
> Ngọc (Thứ Bảy): lấy câu hỏi từ file tổng hợp **đã ẩn danh** mới nhất của Thảo; không có thì lấy từ report.md.
> Sửa `team/nhan-su/tra-loi-bao-cao/ho-so.md` cho khớp.

### D4. Vy: bài ảnh chưa được kiểm, lịch sử bị nhiễu (#14) — trung bình
**Vấn đề.** `config.json` mới chỉ ghi đã kiểm REEL nháp. Bài Facebook `type: POST` với 2–3 ảnh qua Metricool chưa ai thử. Vy đang ghi mọi bài vào `history.jsonl` dạng `{date, pillar, topic}`, và Ngọc dùng file này để "bỏ ý trùng 30 ngày". Bản tin hằng ngày sẽ làm nhiễu bộ lọc đó. Quy tắc "khung có bài #daoducdautu là khung bận" thì vẫn an toàn vì 07:30 không phải khung trưa hay tối, nhưng nên ghi rõ để tránh hiểu sai.
**Đoạn đề xuất — thay phần Vy:**
> - Bản tin ảnh: Facebook `type: POST`, `media` = các URL ảnh từ **một** lệnh `media_repo put`, giờ cố định 07:30, không dùng `post_slots`, không tính vào giới hạn 2 video, không đăng TikTok. Khung 07:30 không làm khung trưa/tối thành "bận".
> - Trước khi dùng thật: tạo 1 bài nháp POST 3 ảnh và xác nhận Metricool nhận đủ ảnh, ghi vào `config.json` (mục `verify`).
> - `history.jsonl`: thêm `"loai": "ban-tin"` (video là `"loai": "video"`). Ngọc chỉ lọc trùng trên `loai = video`.

### D5. Lịch chạy mới — xem A1
Phần "Lịch chạy mới" trong 03 cần được chuyển thành chế độ trong skill (A1). Thêm giờ hạn chót 06:45 và quy tắc "trễ thì bỏ, không đăng muộn".

### Điều tốt nên giữ ở file 03
- "Sự kiện chỉ là mở đầu (khoảng 20%), phần chính vẫn là bài học dùng được lâu": đúng, đây là câu bảo vệ định vị.
- Phong tránh "hôm nay/hôm qua" vì kịch bản có thể quay trễ 1–3 ngày: phát hiện đúng vấn đề, chỉ cần đẩy thêm một bước như D1.
- "Con số chỉ lấy từ bản tin của Linh": nguyên tắc một nguồn sự thật là đúng, chỉ thiếu đường ống dữ liệu (`su_kien`).
- Linh 04:40 trước 05:05: thứ tự đúng.
- Ví dụ "Thứ Ba – Quản trị rủi ro + sàn X bị hack → không để hết tài sản trên sàn": đúng mẫu nối tin vào trụ cột.

---

## E. File 00 — Tổng quan
**Tốt, nên giữ:** liệt kê thật các giới hạn (API giá bị chặn, Metricool/Buffer không đọc được bình luận, skill 3 bước chưa có trong repo). Chủ kênh biết trước điều gì làm được và điều gì chưa.
**Bổ sung đề xuất** (thêm mục "Trước khi duyệt cần có"):
> 1. `fanpage/tools/the_tin_tuc.py` + font tiếng Việt, và `media_repo.py put` nhiều file (B1).
> 2. `fanpage/cham-soc/` trong `.gitignore` (C1).
> 3. Chế độ `tin-tuc`, `cham-soc` trong skill + 2 hồ sơ nhân sự (A1).
> 4. Chủ kênh chọn: tần suất bản tin (A2); mở 2 host API giá (B2); 14 ngày đầu bản tin ở chế độ nháp (A1); số đường dây hỗ trợ tâm lý để ghi vào FAQ (C2).
> 5. Chép skill "Bài Đăng 3 Bước" vào repo để Trang rà trước khi Linh dùng (B6).

---

## Ghi chú nguồn đã tra
- NĐ 147/2024/NĐ-CP, Điều 36 khoản 7 (cấm sản xuất nội dung dạng phóng sự, điều tra, phỏng vấn báo chí trên mạng xã hội): https://lsvn.vn/khong-loi-dung-mang-xa-hoi-de-san-xuat-noi-dung-duoi-hinh-thuc-phong-su-dieu-tra-phong-van-bao-chi-a150793.html — cần đối chiếu văn bản gốc.
- TikTok cấm quảng bá crypto dạng branded content từ 2021; chính sách quảng cáo dịch vụ tài chính: https://ads.tiktok.com/help/article/tiktok-ads-policy-financial-services ; https://decrypt.co/75661
- NQ 05/2025/NQ-CP (thí điểm thị trường tài sản mã hoá), NĐ 13/2023/NĐ-CP và Luật Bảo vệ dữ liệu cá nhân 2025: dẫn theo hiểu biết chuyên môn, **chưa tra lại văn bản trong lượt này**, cần xác minh trước khi đưa vào prompt chính thức.
