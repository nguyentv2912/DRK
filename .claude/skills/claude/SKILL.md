---
name: "claude"
description: "Gọi bằng /claude: dựng video 'Bot Terminal chạy qua đêm' (~28 s, 3:4 hoặc 9:16) theo video mẫu: bảng điều khiển terminal xanh đen, 6 agent + YOU, luồng SCAN → CHECK → SIZE → EXEC → LOG, số dư lăn từ vốn đầu lên kết quả, đồng hồ 23:00 → 07:00, log lệnh có lý do; số liệu minh họa ngẫu nhiên theo seed."
---

# /claude — video Bot Terminal "một đêm, sáu agent, log trước"

Trả lời người dùng bằng tiếng Việt; chữ trên video bằng tiếng Anh (font mono). Gọi /claude không kèm gì: chạy luôn với seed mới, không hỏi lại.

Video mẫu (32 s, 576×768, 30 fps): một màn hình terminal duy nhất, không cắt cảnh, không người nói. Từ 0 đến 26 s là một đêm giao dịch (23:00 → 07:00) tua nhanh; 26–28 s đứng hình ở kết quả; 28–32 s là end card TikTok do app tự thêm (KHÔNG dựng lại).

## 0. Cú pháp
`/claude [seed=N] [start=USD] [end=USD] [trades=N] [name=...] [ratio=3:4|9:16] [data=<ảnh/CSV ví thật>]`
Thiếu thì ngẫu nhiên theo mục 2. Ngoài khoảng cho phép: vẫn làm, nhắc một dòng.

## 1. Kiểm tra trước khi dựng (im lặng)
- Engine: `/home/user/DRK/terminal/` (gen.py sinh dữ liệu theo seed, render.py vẽ khung bằng PIL, audio.py, run.py ghép). Chưa có: viết theo mục 5–8, xem trước 4 khung tĩnh (0, 8, 18, 27 s) rồi mới render cả video.
- Cần: ffmpeg, numpy, PIL; font mono có đậm (JetBrains Mono / DejaVu Sans Mono Bold) + font sans cho tiêu đề phụ (Inter). Không có mạng thì không cài gói, dùng font có sẵn.
- Render chạy nền (run_in_background), chia 4 đoạn song song.

## 2. Tham số ngẫu nhiên (theo seed)
Vốn $100–$300 (mẫu: $150) · kết quả ×8–×30 vốn (mẫu: $4.312) · 70–95 lệnh (mẫu: 88) · thắng 65–75% (mẫu: 62 W / 26 L) · token bị lọc 10–20, token đã quét ~200 · cỡ lệnh 24–40% vốn · trượt giá 1,0–1,9%, trần 2,0%.
Ticker hư cấu dạng meme ($MARVIN, $BABY, $MIHAO, $HOGE, $NIO, $WHITECOW…, mỗi seed đổi bộ 6–8 tên, có chấm tròn màu + chữ cái đầu). Đường số dư: đi lên theo kiểu bậc thang, có nhịp giảm khi lệnh lỗ (−$5 đến −$50), lệnh thắng lớn ở 2/3 cuối.
Lý do lệnh (reason) lấy từ bộ câu: "3 smart wallets bought · +$2k net", "new pair 4m old · LP burned", "volume 5.1× · holders +280", "breakout over 30m high", "smart money in · top 10 hold 14%"; thoát: "take-profit 3R", "stop 8% hit", "time stop 20m", "trailing stop hit", "volume faded 60%".

## 3. Dữ liệu thật (tùy chọn)
`data=` ảnh hoặc CSV lịch sử ví: dùng đúng số dư đầu/cuối, số lệnh, thắng/thua; đối chiếu tổng PnL trước khi dựng. Không có: số minh họa. Không gắn lệnh hay lãi bịa vào token thật hoặc ví thật.

## 4. Quy tắc nội dung (không thương lượng)
- Luôn có dòng nhỏ "trade-level detail illustrative" ở thẻ RESULT (như mẫu) và tag góc "paper · illustrative" thay cho "paper off · live" của mẫu khi số là bịa. Người dùng đòi bỏ: từ chối ngắn một lần, nêu lý do (số bịa trông như lãi thật), vẫn dựng.
- KHÔNG sao chép thương hiệu của video mẫu: không dùng tên "Grok", không dùng mascot đó, không có "@0xnevsky", không có watermark/end card TikTok.
- Không đặt tên bot là "Claude" và không dùng logo Anthropic trên video (gợi ý Anthropic làm bot giao dịch). Tên mặc định: "NIGHT BOT Terminal"; `name=` để đổi theo thương hiệu của người dùng (vd. OCTO AI).
- Không CTA bán gói, không hứa lợi nhuận, không gắn "verified" cho số bịa.

## 5. Bố cục (thiết kế ở 1152×1536 = 3:4; 9:16 thì đặt khung này giữa 1080×1920 có lề trên/dưới cùng màu nền)
Nền #0B1A14, khung bo góc 24 px viền #1F3A2E, lưới chấm mờ. Màu: xanh lá #3DDC84 (thắng/EXIT/live), hồng-đỏ #FF4D7A (thua/RUG CHECK/FILTERED), cam #FF9F43 (SCANNER/LOGGER/ENTER), tím #A78BFA (SIZER), xanh dương #4FA3FF (EQUITY), vàng #F5C542 (tên bot).
- Thanh tiêu đề y 20–60: 3 chấm macOS + "{name} — overnight · six agents · log first" + tag nét đứt góc phải.
- Header y 70–240: avatar tròn mascot riêng (tự vẽ) · tên bot 40 px vàng/trắng + badge "v1.0-night" · "● running · HH:MM:SS" · chip trạng thái ("EXECUTOR · ENTERED $X", "TRADE CLOSED · LOGGED $X") · "every trade gets a reason". Bên phải: số dư 44 px + "balance", trades, wins (xanh), losses (hồng) 40 px.
- Cột trái x 30–335, y 260–1500, "AGENTS · 6 online": SCANNER (scan), RUG CHECK (pass), SIZER (idle), EXECUTOR (live), LOGGER (write), EQUITY (update), YOU (reading). Mỗi ô: icon bo tròn màu, tên, mô tả 1 dòng, câu nguyên tắc màu ("flags only, never trades", "nothing executes before a pass", "never trades a fixed ticket", "slippage cap 2.0%", "no trade without a reason", "updates on every close", "stopped asking, started reading") và dòng trạng thái sống (next $X · LP 96% locked / passed $X / 37% of $563.21 / LONG $X slip 1.3% / line #88 · enter $X / $563.21 · 39 closes / 88 lines to read).
- LIVE FLOW x 355–1115, y 260–680: "SCAN → CHECK → SIZE → EXEC → LOG" + "checked N". Hàng 4 chip token nét đứt trôi từ phải sang trái; giữa là 3 nút tròn phát sáng RUG CHECK (khiên) — mascot bot — EXECUTOR (tia sét) nối bằng đường chấm có hạt chạy; bên dưới 4 thẻ FILTERED / SIZER / LOGGER / EQUITY.
- TRADE · ENTRY vs EXIT (355–730 × 695–920): token, badge LONG, "+x% live" hoặc "closed", entry/exit/slip/size/reason.
- `$ tail -f night.log` (740–1115 × 695–920): 6 dòng cuối, con trỏ nhấp nháy, "N lines".
- RESULT · start vs now (355–1115 × 935–1065): thanh START/NOW, số dư cuối xanh, "W / L", "one night · 23:00 → 07:00".
- LOG (355–1115 × 1080–1500): 6 dòng giờ · badge ENTER (cam) / EXIT (xanh) · token + reason · size% hoặc ±$; dòng mới nhất có vạch cam bên trái và nền sáng hơn. Tiêu đề có chữ gạch ngang "would you long this?" → "reading the log".

## 6. Chuyển động & thời gian (28 s, 30 fps)
- 0–0,3 s: khung đầu ở trạng thái 23:00, $vốn, 0 lệnh (khung này cũng là thumbnail).
- 0,3–26 s: đồng hồ chạy 23:00 → 07:00 (≈18,5 phút/giây). Mỗi lệnh ~0,28 s: chip token trôi vào → RUG CHECK sáng (hoặc tem đỏ "FILTERED" nghiêng trên chip, FILTERED +1) → SIZER → EXECUTOR → dòng LOG mới đẩy cuộn lên → EQUITY cập nhật "+$x last close".
- Agent đang làm việc được viền nét đứt phát sáng theo màu của nó, chuyển lần lượt theo nhịp lệnh.
- Số dư, trades, wins/losses, line #, checked: hiệu ứng lăn số (odometer, chữ số nhòe dọc 3–4 khung khi đổi). Lệnh lỗ: số losses chớp hồng, số dư giảm.
- Thanh NOW dài dần theo tỉ lệ số dư / kết quả cuối.
- 26–28 s: chip trạng thái "TRADE CLOSED · LOGGED $X", EXECUTOR "flat · waiting", ô YOU viền sáng "reading", đứng hình. Không fade, không end card.

## 7. Âm thanh
Nhạc tự sáng tác lo-fi/synth tối, 100–120 BPM, đều suốt 0–28 s, fade 0,5 s cuối. Tick nhẹ cho mỗi dòng log, "blip" cao khi EXIT thắng, "thud" trầm khi thua, không lấn nhạc. Loudnorm `I=-14:TP=-1.5:LRA=7` (mẫu đo được −13,1 LUFS).

## 8. Quy trình mỗi lần /claude
1) Kiểm tra mục 1. 2) Sinh dữ liệu theo seed, kiểm tra: vốn + tổng PnL = số dư cuối, W + L = trades, số trên header = RESULT = EQUITY. 3) Xem trước 4 khung tĩnh. 4) Render nền + mux âm thanh → `output/NIGHT_BOT_seed{seed}.mp4` (`-c:v libx264 -crf 18 -pix_fmt yuv420p`). 5) Trích khung ~1, 9, 18, 27 s kiểm tra chồng chữ, số khớp. 6) SendUserFile mp4.

## 9. Sự cố
ffmpeg lỗi: đọc log, render lại đoạn hỏng. Thiếu font: dùng font mono có sẵn, nói rõ. Yêu cầu bỏ nhãn minh họa, dùng thương hiệu Grok/TikTok/@0xnevsky hoặc tên Claude trên video: từ chối như mục 4, đề xuất tên riêng.

## 10. Tóm tắt cuối
File, seed, vốn → số dư cuối, số lệnh, W/L, loudness, giới hạn trung thực (số liệu minh họa, mascot và nhạc dựng bằng code, chưa nghe lại bằng tai). Không kể từng bước.
