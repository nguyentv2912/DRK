---
name: dung-video-dao-duc-dau-tu
description: Dựng video cho kênh ĐẠO ĐỨC ĐẦU TƯ từ video thô chủ kênh quay (dọc hoặc ngang) thành video dọc 9:16 hoàn chỉnh — phụ đề, thẻ chữ, nhạc nền, khung viền, tấm minh hoạ nhân vật/trích dẫn/icon, chớp sáng chuyển ý, âm thanh hiệu ứng. Dùng khi chủ kênh gửi video quay xong, hoặc khi Khoa (edit-video) dựng video hằng ngày.
---
# Dựng video Đạo Đức Đầu Tư

Mọi hiệu ứng, nhạc và âm thanh đều **tự tạo bằng công cụ trong repo** → không lo bản quyền. Video mẫu đã duyệt cấu hình: `fanpage/runs/KB-20261115-DOI-AI/` (`edit_plan.json`, `minh_hoa.json`).

## 1. Lấy video thô
- Video nằm trong thư mục Drive "Video thô" (`raw_folder_id` trong `fanpage/config.json`). File lớn (hàng trăm MB) chỉ tải được khi **chủ kênh tự mở** "Bất kỳ ai có đường liên kết" vài phút — đội KHÔNG tự đổi quyền chia sẻ. Tải: `curl -L -o raw.mp4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`, xong nhắc chủ kênh chuyển lại "Bị hạn chế".
- Video có mặt/giọng chủ kênh: KHÔNG commit vào repo DRK (repo công khai). Làm việc trong thư mục tạm.

## 2. Bóc lời và sửa phụ đề
- `python3 fanpage/tools/edit_video.py transcribe raw.mp4 transcript.json --model small`
- Máy nghe sai nhiều ("bình an" → "bình na", "AI" → "H.I."). **Bắt buộc** sửa từng câu theo lời chủ kênh thật sự nói (đối chiếu `kichban.txt`), giữ mốc thời gian câu, chia lại mốc chữ trong câu. Mẫu script sửa: xem cách làm ở lần dựng 15/11 (thay `sentences[i].text`, phân bổ lại `words`).

## 3. Dựng lớp 1 — `edit_video.py render`
`python3 fanpage/tools/edit_video.py render raw.mp4 transcript.json edit_plan.json video.mp4`
- Cắt khoảng lặng, xen zoom 100/108%, phụ đề to tô màu từ khoá, thẻ chữ viền vàng (hook đầu video, ①②③ theo "Thứ nhất / Thứ hai / Thứ ba", CTA cuối).
- **Nhạc nền:** `fanpage/assets/nhac/binh-an.mp3` (piano êm Am–F–C–G, tự tạo bằng `fanpage/tools/tao_nhac.py OUT.mp3 90 SEED` — đổi SEED để có bài khác), `music_volume` 0.22, tự hạ khi có giọng nói.
- **Quay ngang:** `"layout": "split"` → nửa dưới khuôn mặt chủ kênh, nửa trên nền xanh của kênh cho thẻ chữ và tấm minh hoạ, phụ đề nằm ở đường nối có vạch vàng. Chỉnh `crop_x` nếu mặt lệch.
- Thẻ chữ không được chồng nhau: thẻ ý cuối phải kết thúc trước CTA (bỏ hoặc rút `sec`).

## 4. Dựng lớp 2 — `minh_hoa.py` (hiệu ứng, frame, minh hoạ, âm thanh)
`python3 fanpage/tools/minh_hoa.py video.mp4 transcript.json edit_plan.json minh_hoa.json video_final.mp4`
- **Frame:** khung viền vàng kép bo góc + 4 góc trang trí, thanh tiến độ vàng chạy ở đáy.
- **Tấm minh hoạ** (bật theo `trigger` = cụm lời nói thật, trượt lên + mờ dần; liệt kê theo đúng thứ tự trong video):
  - `nhan_vat`: 2–8 vòng tròn nhân vật/nhiệm vụ, chủ kênh màu vàng (`"me": true`), có mũi tên nếu là dòng chảy (`"arrows": true`).
  - `trich_dan`: câu trích lớn + nguồn — dùng cho phần **ĐẠO** (trích Phật/Nho/Đạo đúng xuất xứ) và câu đúc kết.
  - `minh_hoa`: icon vẽ + 1–2 dòng chữ. Icon: bieu_do_tang, bieu_do_giam, dam_dong, trai_tim, dong_ho, khien, can_can, mat_troi, ngon_nen, nha.
- **Chớp sáng** (`"flash": true`) ở đầu mỗi phần Đạo / Đời / Đầu tư.
- **Âm thanh hiệu ứng** (`"sfx": true`, tự tổng hợp): whoosh khi thẻ chữ bật, pop khi tấm nhân vật bật, ding khi tấm trích dẫn/icon bật.

## 5. Khung chuẩn theo bố cục Đạo – Đời – Đầu tư
| Mốc | Thẻ chữ (edit_plan) | Tấm minh hoạ (minh_hoa) |
|---|---|---|
| 0–4s | hook_title (đỏ) | `nhan_vat` hoặc `minh_hoa` giới thiệu chủ đề |
| "Thứ nhất, Đạo" | ① + tên ý | `trich_dan` câu kinh điển, flash |
| "Thứ hai, Đời" | ② | `minh_hoa` icon chuyện đời (nha, dong_ho, dam_dong…), flash |
| "Thứ ba, Đầu tư" | ③ | `minh_hoa` bieu_do_* / khien / can_can, flash |
| Đúc kết | — | `trich_dan` câu thương hiệu |
| Cuối | CTA "THEO DÕI" | — |

## 6. Giao và đăng
- Nén ≤ 60MB (`-crf 25`), xem lại 4 khung hình (đầu, ①, ③, cuối) trước khi gửi chủ kênh.
- Cấp 1: gửi chủ kênh xem trước → duyệt → Vy tạo **nháp** Metricool (`publish_mode: nhap`). Chưa nối TikTok @daoducdautu thì chỉ Facebook.
- Không hứa lợi nhuận, không nêu mã/coin trên thẻ chữ và tấm minh hoạ; ví dụ tình huống phải ghi giả định.
