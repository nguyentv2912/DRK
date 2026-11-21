---
name: "claude"
description: "Gọi bằng /claude: dựng video nói chuyện dọc 9:16 (~2 phút) theo video mẫu Forex: người nói ở giữa (giọng clone F5-TTS + khớp môi LatentSync chạy free trên Kaggle), chữ to dưới ngực với từ khoá vàng/đỏ bật nảy, khung ảnh viền vàng có câu hỏi phía trên, nền mờ, cảnh cuối FOLLOW."
---

# /claude — video nói chuyện tâm lý giao dịch (theo video mẫu Forex)

Trả lời người dùng bằng tiếng Việt; lời nói và chữ trên video bằng tiếng Việt. Gọi /claude không kèm gì: dùng `kaggle/kichban.txt` + `kaggle/storyboard.md` hiện có, kiểm tra đã có `noi.mp4` chưa rồi đi tiếp bước còn thiếu, không hỏi lại.

## 0. Cú pháp
`/claude [chude="..."] [video=<link Drive noi.mp4>] [speed=1.0] [test]`
- `chude=`: viết kịch bản + storyboard mới cho chủ đề đó (mục 3), ghi đè `kichban.txt` / `storyboard.md`.
- `video=`: link Google Drive của `noi.mp4` (đã khớp môi) → nhảy thẳng tới dựng (mục 6).
- `speed=`: tốc độ đọc F5-TTS (0,9 chậm – 1,1 nhanh). `test`: chỉ làm 15 giây đầu.

## 1. Kiểm tra trước khi làm (im lặng)
- Repo: `kaggle/{kichban.txt, storyboard.md, make_nb.py, video_noi_free.ipynb, chi_khop_moi.ipynb}`. Thiếu notebook: `python3 kaggle/make_nb.py kaggle/video_noi_free.ipynb`.
- Máy này KHÔNG có GPU: clone giọng + khớp môi chỉ chạy trên Kaggle (người dùng tự bấm Run All). Claude chỉ làm kịch bản, notebook và phần dựng hậu kỳ.
- Dựng cần: ffmpeg, numpy, PIL, cv2; font có dấu tiếng Việt (ưu tiên Be Vietnam Pro / Montserrat ExtraBold, không có thì DejaVu Sans Bold). Whisper để lấy mốc thời gian từng chữ: `faster-whisper` (model small, language="vi"); không có/không có mạng thì chia thời gian theo số âm tiết mỗi câu và nói rõ là ước lượng.
- File nặng (*.mp4, *.wav, *.zip, *.mp3, output/) không đưa lên git (.gitignore đã chặn).

## 2. Quy trình tổng (4 khâu)
1) Kịch bản `kichban.txt` + `storyboard.md` (Claude).
2) Clone giọng → `giong.wav` (Kaggle, F5-TTS-Vietnamese, model hynt/F5-TTS-Vietnamese-ViVoice).
3) Khớp môi → `noi.mp4` (Kaggle, LatentSync 1.5, T4 16GB, 20 bước, guidance 1.5, deepcache).
4) Dựng theo video mẫu → `output/VIDEO_<slug>.mp4` 1080×1920 (Claude, mục 6–8).

## 3. Kịch bản (quy tắc)
- ~2 phút ≈ 280–320 chữ; mỗi câu một dòng, viết thường, số viết bằng chữ ("hai trăm", không "200"), câu ngắn ≤ 20 chữ để F5-TTS đọc đúng dấu.
- Cấu trúc như mẫu: hook 1 câu (khoảnh khắc / mâu thuẫn) → kể "mình từng…" → cú quay ("cho đến một ngày…") → câu hỏi "vậy … trông như thế nào?" → danh sách 3–4 ý "thứ nhất… thứ tư" → đảo nhận thức ("nhiều người nghĩ… nhưng không") → "hãy nhớ điều này" → câu chốt 2 vế → CTA theo dõi.
- Storyboard: bảng `# | thời gian | lời | chữ to | hình chèn/hiệu ứng`, 12–14 cảnh, mỗi cảnh 6–14 s, một cụm chữ to 2–4 từ.
- Không hứa lợi nhuận, không nêu số lãi cụ thể. Nếu có số tiền/phần trăm: thêm thẻ nhỏ "Không phải lời khuyên đầu tư".

## 4. Kaggle (người dùng làm, Claude hướng dẫn)
- Session options: GPU T4 x1, Internet On (lần đầu phải xác minh số điện thoại).
- Add Input → Upload → New Dataset: `ref.wav` (giọng mẫu ~11 s, sạch, khớp đúng `REF_TEXT` trong notebook), `mat.mp4` (clip mặt nhìn thẳng, 25 fps, ≥ 10 s, miệng không bị che), `kichban.txt`. Run All: ~10 phút cài + 20–30 phút.
- Nghe `giong.wav` trước khi khớp môi; câu đọc sai → sửa chữ trong kịch bản (viết theo cách đọc), chạy lại từ bước 3.
- Đã có giọng: dùng `chi_khop_moi.ipynb` (upload `giong.wav` + `mat.mp4`).
- Tải `noi.mp4` ở Output → Google Drive → gửi link. Claude tải bằng connector Google Drive (download_file_content) vào `output/`.
- Chỉ dùng giọng và mặt của chính người dùng (hoặc người đã đồng ý). Không clone giọng/mặt người nổi tiếng hay người khác.

## 5. Phong cách video mẫu (giữ nguyên)
Người nói ở giữa khung · chữ to dưới ngực, trắng viền đen dày, từ khoá vàng (#FFD400) hoặc đỏ (#FF3B30, cho cảm xúc tiêu cực: tham, sợ, gỡ, lỗ) · chữ bật nảy từng cụm · xen khung ảnh bo góc viền vàng, câu hỏi chữ trắng phía trên khung · nền là chính video phóng to + làm mờ · cắt nhanh/zoom nhẹ ở câu nặng · cảnh cuối FOLLOW.

## 6. Bố cục 1080×1920
- Nền: `noi.mp4` scale phủ kín 1080×1920, gaussian blur σ≈40, tối 35%.
- Người nói: scale rộng 1080 (hoặc 960 có bo góc 36 px), đặt đầu ở y≈300–420; ngực ở y≈1150.
- Chữ to: tâm y≈1300–1420, 2 dòng tối đa, cỡ 96–120 px (từ khoá 130 px), viền đen 10 px + bóng đổ; mỗi cụm 2–4 chữ theo mốc Whisper.
- Khung chèn (cảnh 2, 3, 5–9): khung 900×700 tại y≈380–1080, viền vàng 8 px, bo 28 px, đổ bóng; câu hỏi phía trên y≈300, 64 px trắng. Người nói thu nhỏ/ẩn khi khung hiện, giọng vẫn chạy.
- Checklist (cảnh 6–9): thẻ 4 dòng ①–④, ý đang nói sáng + tick vàng, ý đã qua mờ 60%.
- Vùng an toàn: không đặt chữ ở y > 1650 (thanh UI Reels/TikTok) và 0–160.

## 7. Chuyển động & thời gian
- Chữ bật: scale 0,8 → 1,08 → 1,0 trong 0,15 s, opacity 0→1 trong 0,08 s; thoát 0,1 s.
- Hook 0–6 s: zoom vào mặt 1,0 → 1,15 + chữ "CHỌN KỶ LUẬT / hay lòng tham?" (đỏ) nảy.
- Câu nặng (cảnh 4, 10): punch-in 1,0 → 1,08 trong 0,2 s, giữ, trả về; cảnh 4 thêm icon ⚠ và cắt nhanh 2 nhịp.
- Cảnh 11: "VỐN · TÂM LÝ · TỈNH TÁO" hiện lần lượt theo đúng chữ được nói. Cảnh 12: mũi tên đi lên.
- Cảnh cuối: thẻ "FOLLOW" lớn + dòng "năng lượng giao dịch mỗi ngày", giữ ≥ 2,5 s.
- Mọi mốc lấy từ Whisper word timestamps trên `giong.wav`, không dùng thời gian ước trong storyboard.

## 8. Âm thanh
Giọng là chính: loudnorm `I=-14:TP=-1.5:LRA=7` cho mạng xã hội. Nhạc nền (chỉ nhạc tự tạo hoặc có quyền dùng) ở −24 dB dưới giọng, sidechain ducking; whoosh nhẹ khi chữ to hiện, "ting" khi tick checklist. Chấp nhận −14±1,5 LUFS, true peak ≤ −1 dBTP.

## 9. Dựng (cách làm)
1) Tải `noi.mp4` → `output/`; tách `giong.wav` nếu cần (`ffmpeg -nostdin`).
2) Whisper → `output/words.json` (chữ, start, end); ghép thành cụm theo storyboard, đánh dấu từ khoá vàng/đỏ.
3) Render lớp đồ hoạ bằng PIL/cv2 theo khung (nền mờ + người + chữ + khung chèn), 30 fps, chia 4–6 đoạn render song song, chạy nền (run_in_background).
4) Ghép bằng ffmpeg: `-c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k`, mux âm thanh mục 8.
5) Trích khung ở ~1, 15, 45, 60, 90, cuối → contact sheet kiểm tra chữ chồng, lệch môi, chữ vượt vùng an toàn.
6) SendUserFile mp4.

## 10. Sự cố
- Kaggle: lỗi ffmpeg treo → đã có `-nostdin`; lỗi matplotlib → `MPLBACKEND=Agg`; hết VRAM → giảm `--inference_steps` 20 → 15 hoặc cắt kịch bản làm 2 nửa; không nhận mặt → clip mặt rõ, đủ sáng, nhìn thẳng.
- Môi lệch: kiểm tra `mat.mp4` 25 fps, giọng 16 kHz mono khi đưa vào LatentSync.
- Giọng sai dấu: sửa chữ trong kịch bản, không sửa ở hậu kỳ.
- Thiếu font/thư viện: dùng cái có, nói rõ.

## 11. Tóm tắt cuối
File, thời lượng, số cảnh, loudness, giới hạn trung thực (giọng clone + khớp môi bằng AI, mốc chữ từ Whisper hay ước lượng, chưa nghe lại bằng tai). Không kể từng bước.
