---
name: "forex"
description: "Gọi bằng /forex: dựng video dọc 9:16 (~24s) kiểu quay tay màn hình app giao dịch forex trong phòng tối: tab Trade chạm đóng lệnh liên tục, xen biểu đồ M1, kết ở History/Deals, có nhạc lo-fi. Dữ liệu thật của người dùng (ảnh/báo cáo MT4-MT5) hoặc mô phỏng có nhãn bắt buộc."
---

# /forex — video "đóng lệnh trên điện thoại" cho kênh forex

Trả lời người dùng bằng tiếng Việt, ngắn gọn. Khi người dùng gõ `/forex` kèm dữ liệu (ảnh chụp app, báo cáo tài khoản) thì chạy trọn quy trình bên dưới và giao file mp4. Không kèm gì thì hỏi một lần: dùng số liệu thật (gửi ảnh) hay làm bản mô phỏng.

## Phân tích video mẫu (đã làm, không cần làm lại)
Video TikTok 23.7s, 576x1024, 30fps:
- **Khung cảnh**: một tay cầm điện thoại trong phòng tối, đèn bokeh vàng ấm phía trên, màn hình trắng sáng hơi cháy (bloom), máy rung tay nhẹ, cắt cảnh nhanh 1–3s, độ zoom và góc nghiêng đổi theo mỗi cảnh.
- **Màn hình**: app kiểu terminal di động nền trắng.
  1. 0–7s tab **Trade**: tiêu đề là tổng lãi trôi nổi màu xanh ("1 284.34 USD"), Balance/Equity/Margin/Free Margin/Margin Level, mục Positions (cặp, buy/sell + lot màu, giá mở → giá hiện tại, lãi xanh), mục Orders ("XAUUSD buy stop … placed").
  2. Chạm liên tục để đóng lệnh: vòng chạm nhiều màu, dòng vuốt sang lộ ô đỏ **Close**, thanh cam phía dưới "Close #… buy 1.61 USDJPY at 158.842 with profit 166.53", lãi trôi nổi giảm, Balance tăng.
  3. 7–10s và 16–18s: tab **Chart** XAUUSD M1, hai ô đỏ SELL/BUY phía trên, đường nét đứt của lệnh đang mở, nhãn giá xanh bên phải.
  4. 20–24s: tab **History › Deals**: Profit, Deposit, Swap, Commission, Balance, rồi cuộn danh sách deal "… out".
- **Âm thanh**: nhạc nền nhẹ, gần như không có bass, nhịp ước lượng ~92 BPM, không có lời và không có chữ phủ trên video. Script tự tạo nhạc lo-fi 92 BPM, có tiếng chạm và tiếng "ting" mỗi lần đóng lệnh. Nhạc tự tổng hợp, không trích từ video mẫu.

## Quy tắc bắt buộc (trung thực, bản quyền)
- **Ba chế độ** ở trường `mode` của dữ liệu:
  - `real`: số liệu chép từ tài khoản thật của người dùng (ảnh app, báo cáo HTML/CSV). Có chú thích nhỏ "Không phải lời khuyên đầu tư".
  - `demo`: tài khoản demo. Luôn có nhãn vàng "TÀI KHOẢN DEMO".
  - `sim`: số liệu do script tạo ra. Luôn có nhãn vàng "MÔ PHỎNG · KHÔNG PHẢI KẾT QUẢ THẬT".
- Không bỏ hay che nhãn, kể cả khi người dùng yêu cầu. Không gọi bản `sim`/`demo` là kết quả thật trong caption. Không viết caption hứa lợi nhuận, kêu gọi nạp tiền, "copy lệnh", "tín hiệu VIP" hay quảng bá sàn.
- Không bịa số rồi gắn `real`. Nếu chỉ có một phần số liệu thật thì chỉ dùng phần đó; những gì còn thiếu (ví dụ danh sách deal cũ) phải lấy từ ảnh, không thì bỏ trống hoặc chuyển sang `sim`.
- Giao diện là bản vẽ chung chung theo kiểu terminal di động. Không thêm logo hay tên MetaTrader/MetaQuotes, logo sàn, tên sàn thật.

## Script: `scripts/forex.py`
Cần Python 3, Pillow, numpy, ffmpeg, font Inter ở `/usr/share/fonts/opentype/inter` (đều có sẵn trong môi trường cloud). Đường dẫn dưới đây tính từ thư mục skill này.

```bash
# 1a. Bản mô phỏng (seed khác → video khác)
python3 -I scripts/forex.py sim --seed 7 --n 10 --start 100000 --out data.json
# 1b. Hoặc tự viết data.json từ số liệu thật (xem mục Dữ liệu)
# 2. Kiểm tra số
python3 -I scripts/forex.py check data.json
# 3. Xem trước khung chính (chỉ xuất PNG, ~2s)
python3 -I scripts/forex.py render data.json out.mp4 --keys 1 2.4 8 14 22.5 --keydir keys
# 4. Render đầy đủ (~70s với 4 CPU), 1080x1920, 30fps, 24s, có nhạc
python3 -I scripts/forex.py render data.json FOREX_<tên>_v1.mp4 [--dur 24] [--lang vi|en] [--no-audio]
```
`--lang en` đổi nhãn sang tiếng Anh ("SIMULATED · NOT REAL RESULTS", "Not financial advice"). `--dur` co giãn toàn bộ timeline.

## Dữ liệu (`data.json`)
```json
{
  "mode": "real",
  "currency": "USD",
  "clock": "19:08",
  "account": {"balance_start": 74384.35},
  "positions": [
    {"id": 2084713409, "symbol": "USDJPY", "side": "buy", "lots": 1.61,
     "open": 158.010, "close": 158.842, "profit": 166.53}
  ],
  "pending": [{"symbol": "XAUUSD", "type": "buy stop", "lots": 1.5, "price": 3912.85}],
  "chart": {"symbol": "XAUUSD", "tf": "M1", "last": 3906.10},
  "history": {"deposit": 70000, "swap": -231.73, "commission": 0,
              "deals": [{"symbol": "XAUUSD", "side": "buy", "lots": 0.2, "time": "2026.11.21 19:12", "profit": 336.5}]}
}
```
- `positions`: các lệnh sẽ được đóng trong video, theo thứ tự. `profit` là lãi lúc đóng (lấy đúng số trên ảnh). Nên dùng 6–12 lệnh. Script chia thành 3 đợt ở 3 cảnh Trade.
- `balance_start`: Balance trước khi đóng lệnh đầu tiên. Balance cuối = balance_start + tổng profit.
- History: Profit = tổng `deals.profit`; Balance = deposit + profit + swap + commission. `check` cảnh báo nếu Balance cuối tab Trade khác Balance tab History, hoặc lãi một lệnh lệch nhiều so với ước tính từ giá × lot (contract size mỗi broker khác nhau, nên chỉ là cảnh báo: đối chiếu lại ảnh gốc).
- Biểu đồ nến M1 là đường minh họa quanh giá `chart.last`, không phải dữ liệu giá thật. Nếu người dùng cần đúng nến thật thì báo là chưa hỗ trợ.

## Quy trình
1. **Lấy số liệu**: đọc ảnh chụp app/báo cáo của người dùng, chép vào `data.json` (mode `real` hoặc `demo` tùy tài khoản). Ghi lại số nào đọc không rõ để hỏi. Không có dữ liệu và người dùng đồng ý làm mô phỏng thì chạy `sim` với seed mới (đặt seed theo ngày, ví dụ 20261121).
2. **`check`**: sửa đến khi không còn dòng LỖI; cảnh báo thì đối chiếu ảnh.
3. **Xem khung chính** (`--keys`): sau lệnh đóng đầu, giữa biểu đồ, cảnh Trade thứ hai, History. Kiểm tra chữ không tràn, nhãn không đè lên số, thanh cam đúng lệnh.
4. **Render đầy đủ** một lần. Kiểm tra bằng `ffprobe`: 1080x1920, đúng thời lượng, có audio; `volumedetect` max ≤ −0.5 dB.
5. **Giao**: gửi mp4 bằng SendUserFile kèm tóm tắt: chế độ (real/demo/sim), số lệnh đóng, tổng lãi, Balance đầu → cuối, Balance History, và các lưu ý (biểu đồ minh họa, nhạc tự tạo).
6. **Caption gợi ý** (chỉ gợi ý, người dùng tự đăng): 1 câu hook về kỷ luật/quy trình (không khoe hứa lãi), 1 dòng ghi chế độ ("Tài khoản demo" / "Mô phỏng" nếu không phải real), "Không phải lời khuyên đầu tư", 4–5 hashtag như `#forex #trading #xauusd #kyluat #traderlife`.

## Bố cục đã chốt (đừng phá khi sửa)
- Điện thoại chiếm 64–74% chiều rộng khung, lệch xuống 10–60px để nhãn trên cùng (y 34–92) và chú thích đáy (cách đáy 20–58px) không đè máy.
- Vòng chạm nằm trên dòng lệnh đang đóng (lấy y thật của dòng), ô đỏ Close vuốt ra 0.25s trước khi dòng biến mất.
- Lãi trôi nổi dao động nhẹ (giống tick) nhưng hiện đúng số `profit` lúc đóng và trên thanh cam.
- Shot camera đổi ở mỗi lần chuyển tab và ngẫu nhiên mỗi 1.3–2.6s theo `seed`.

## Lưu trữ
Skill nằm trong kho `nguyentv2912/DRK` tại `.claude/skills/forex/`. Video (`*.mp4`) không đưa lên git (đã có trong `.gitignore`).
