# GROK × MEME COIN — BẢN NÂNG CẤP V1.8.4

Skill: `grok-meme-million-video` (giữ nguyên tên)
Đầu vào: V1.8.3 (run 2, chart FIONA): tự động 35/35, chất lượng khoảng 9,2/10
Mục tiêu: **≥ 9,5/10** so với video mẫu, và không phần nào dưới 9,0

Bản này xử lý 4 điểm yếu đã nêu:

| # | Phần | Điểm hiện tại | Mục tiêu |
|---|---|---|---|
| 1 | Hiệu ứng 3D và chuyển cảnh camera | 8,5 | 9,5 |
| 2 | Chuyển thông báo bị bóng mờ (ghosting) | 9,0 | 9,8 |
| 3 | Nhạc và âm thanh | 9,0 | 9,5 |
| 4 | Giới hạn lời/lỗ mỗi lệnh | Vi phạm (lệnh +$1,377) | Đạt 100% |

Nguyên tắc không đổi: giữ đúng giao diện app iPhone của video mẫu, giữ nguồn dữ liệu thật đã xác minh, và luôn ghi nhãn CONCEPT TRADES / Paper.

---

## PHẦN 1 — HIỆU ỨNG 3D THẬT VÀ CAMERA ĐIỆN ẢNH

### 1.1 Hiện trạng và nguyên nhân
- Cả trang app đang là **một mặt phẳng duy nhất**. Camera chỉ nghiêng và zoom tấm phẳng đó, nên không có chiều sâu giữa các lớp.
- Đồng xu là hình 2D vẽ giả độ dày bằng cách chồng nhiều hình elip. Khi xoay gần ngang, xu trông như "viên thuốc" và ánh sáng không đổi theo góc.
- Đoạn cuộn nhanh về đầu (12,0–12,6 giây) đi qua khoảng 2.400 px trong 0,78 giây, nên motion blur làm chữ nhòe gần 10 khung hình.

### 1.2 Kiến trúc mới: scene graph 2.5D nhiều lớp

Mỗi lớp được vẽ ra một surface riêng, đặt ở một độ sâu `z` riêng. Một camera 3D thật (ma trận 4×4) chiếu từng lớp.

| Lớp | z (px) | Nội dung | Ghi chú |
|---|---|---|---|
| L0 Nền | −600 | Nền #06090A, quầng sáng xanh/xanh dương, hạt bụi nhỏ | Parallax 0,25× |
| L1 Trang app | 0 | Thẻ, chart, Bots, Activity | Mặt phẳng lấy nét chính |
| L2 Nổi | +60 | Nhãn BUY/SELL, thẻ giá chart, pill P&L trên đường equity | Đổ bóng lên L1 |
| L3 Header | +120 | Số dư dính phía trên (sticky), status bar, tab bar | Không xoay theo camera để luôn đọc được |
| L4 Tiền cảnh | +260 | Thông báo, đồng xu bay, hạt sáng | Blur theo độ sâu trường ảnh (DOF) |

**Camera** (`src/camera3d.py`):
- Tham số gồm vị trí `(x, y, z)`, `yaw`, `pitch`, `fov` = 38°, và mặt phẳng lấy nét `focus_z`.
- Mỗi lớp được chiếu bằng phép biến đổi phẳng (`setPolyToPoly`) từ 4 góc đã nhân với ma trận 4×4. Cách này cho phối cảnh thật và chữ vẫn là vector sắc nét.
- Mức blur DOF của lớp: `sigma = k·|z_lớp − focus_z| / 100`, tối đa 6 px. L1 và L3 luôn có sigma = 0.

**Kịch bản camera theo từng cảnh:**

| Thời gian | Chuyển động | Biên độ |
|---|---|---|
| 0,0–2,5 | Dolly-in chậm và yaw +1,5° → 0° | z: 0 → −40 |
| 2,5–3,15 | Crane lên: pitch 0 → 5° → 0, L2/L4 tách lớp rõ | Cuộn kèm parallax |
| 3,35 / 4,75 / 7,65 | Push vào marker BUY/SELL: dolly −70, lấy nét L2 trong 0,4 s | Zoom tối đa 6% |
| 6,5–9,0 | Truck ngang ±18 px theo nhịp beat (1/2 bar) | Rất nhẹ |
| 9,0–9,65 | Cuộn xuống Bots: pitch −4°, L4 trôi 1,4× | Parallax |
| 11,8–12,6 | **Chuyển cảnh mới (xem 1.4)** | — |
| 12,6–13,7 | Orbit nhẹ quanh số dư (yaw −3° → +3°), coin burst ở L4 | — |
| 13,75–15 | Pull-back, nền app lùi xuống z −200 và blur 12 px, end card ở L4 | — |

**Giới hạn để luôn đọc được chữ (bắt buộc):**
- `|pitch|, |yaw| ≤ 6°`.
- Chữ của lớp L1 sau khi chiếu không được nhỏ hơn 92% kích thước gốc. Critic đo trực tiếp giá trị này.
- L3 (số dư, status bar, tab bar) không bao giờ bị xoay.

### 1.3 Đồng xu 3D thật: render bằng Blender thành sprite sheet

- **Cài đặt:** `apt-get install -y blender` (không cần GPU, dùng Cycles chạy CPU).
- **Script `src/blender_coin.py`:**
  - Mô hình: cylinder r = 1, dày 0,14, bevel 0,02, rìa có 120 khía.
  - Vật liệu PBR vàng: base #F4C34D, metallic 1, roughness 0,22.
  - Mặt xu: dập nổi logo Grok Bot gốc bằng displacement, hoặc logo token từ `assets/logos` làm decal phẳng có viền.
  - Ánh sáng: HDRI studio tự tạo (2 softbox và 1 rim light xanh #20D58B nhẹ) để hợp tông app.
  - Xuất 72 khung xoay 360° (mỗi khung 5°), 512×512 px, PNG nền trong suốt, kèm motion blur. Thêm 1 bộ "xu nghiêng 25°" cho cảnh bay.
  - Thời gian ước tính khoảng 4–6 phút CPU. Chỉ render một lần và cache trong `assets/coins/`.
- **Trong `render.py`:** `draw_coin()` đổi sang lấy khung sprite theo góc xoay, rồi thêm bóng đổ thật lên lớp L1. Vị trí bóng tính theo hướng nguồn sáng (−30°, 60°) và khoảng cách z.
- **Phương án dự phòng:** nếu không cài được Blender, giữ coin vector hiện tại nhưng thêm env-map giả (gradient phản chiếu xoay theo góc). Báo cáo phải ghi rõ đang dùng phương án dự phòng.

### 1.4 Thay đoạn cuộn nhanh 12,0–12,6 giây bằng "3D page fly-out"

1. **11,80–12,05 giây:** camera pull-back (z +350), trang app thu nhỏ còn khoảng 82%, pitch +5°. Lúc này cả trang hiện như một tấm thẻ nổi trên nền tối, chữ vẫn sắc nét.
2. **12,05–12,35 giây:** trang trượt dọc về đầu khi đang ở xa. Vận tốc trên màn hình chỉ còn khoảng 35% so với cuộn trực tiếp, nên chỉ cần motion blur rất nhẹ (tối đa 6 sample).
3. **12,35–12,60 giây:** push-in về Portfolio, kết thúc đúng beat drop lúc 12,55 giây.

Kết quả: không còn khung hình nhòe đặc, và đây là chuyển cảnh nổi bật nhất video.

### 1.5 Ánh sáng, bóng đổ, phản chiếu
- Một nguồn sáng chung (hướng −30°, 60°) dùng cho mọi đổ bóng: thẻ L1 lên nền, nhãn L2 lên chart, thông báo L4 lên trang.
- Phản chiếu "specular sweep" chạy qua các thẻ khi camera đổi góc. Cường độ tỉ lệ theo `yaw` (tối đa 12% alpha) và dùng blend Screen.
- Viền thẻ có gradient sáng ở cạnh hướng về nguồn sáng (rim light 1,5 px).

### 1.6 Critic bổ sung cho Phần 1
- `text_scale_min ≥ 0.92`: tỉ lệ chữ L1 sau phép chiếu.
- `readable_frames ≥ 97%`: độ sắc nét vùng chữ (Laplacian variance) không được thấp hơn 60% khung tham chiếu tĩnh.
- `coin_sprite_mode = blender | fallback`: ghi vào báo cáo.
- Có kiểm tra chiều sâu: ít nhất 3 lớp có độ dịch parallax khác nhau trong đoạn 2,5–3,15 giây (đo bằng optical flow).

---

## PHẦN 2 — CHUYỂN THÔNG BÁO KHÔNG BÓNG MỜ

### 2.1 Nguyên nhân hiện tại
- Thông báo cũ mờ dần trong 0,06 giây, thông báo mới hiện dần từ +0,067 giây. Giữa hai bước có khoảng hở, nên số dư phía trên hiện lại khoảng 30% rồi tắt.
- Biến `cover` chỉ tính quanh mốc từng sự kiện (±0,06 giây), không phải theo toàn bộ thời gian vùng thông báo đang bị chiếm.
- Khi hai thông báo cùng tồn tại, chữ của cả hai đều đọc được: lỗi ghost.

### 2.2 Thiết kế mới: Banner Manager dạng state machine (`src/banners.py`)

Mỗi thông báo đi qua các trạng thái: `IDLE → ENTERING (0,30 s) → SHOWN → STACKING (0,22 s) → GONE`, hoặc `SHOWN → EXITING (0,30 s) → GONE`.

1. **Vùng thông báo (slot):** được coi là "đang chiếm" từ lúc thông báo đầu tiên vào đến khi thông báo cuối ra hẳn, cộng thêm 0,25 giây. Trong suốt khoảng đó, chữ của số dư phía trên có alpha = 0 (không phụ thuộc từng sự kiện). Riêng lớp che nền vẫn giữ đặc 100%.
2. **Chuyển giao kiểu iOS (stack), không crossfade:**
   - Thông báo mới trượt xuống từ trên (từ L4, scale 1,12 → 1,0, spring).
   - Cùng lúc, thông báo cũ **lùi ra sau**: scale 0,94, dịch lên 14 px. Một lớp phủ tối 70% đè lên nó **trước khi** thông báo mới chạm tới, nên chữ cũ không bao giờ đọc được cùng lúc với chữ mới.
   - Sau 0,22 giây, thẻ cũ còn lại như một mép thẻ mỏng phía sau (giống stack thông báo iOS) rồi biến mất.
3. **Hàng đợi tối thiểu:** mỗi thông báo hiện rõ ít nhất 0,55 giây. Nếu sự kiện kế tiếp đến sớm hơn, sự kiện đó lùi đến beat 1/8 kế tiếp (gắn với Phần 3).
4. Các thay đổi alpha đều gom vào một `saveLayerAlpha` duy nhất cho mỗi thông báo, không còn alpha lồng nhau.

### 2.3 Sticky header
- Lớp che nền giữ đặc theo trạng thái cuộn, như bản run 2.
- Alpha của chữ: `a_text = a_scroll × (1 − slot_occupied_smooth)`, trong đó `slot_occupied_smooth` mượt dần trong 0,12 giây ở hai đầu.
- Khi một lệnh làm tăng P&L, nếu vùng thông báo đang bận thì hiệu ứng nháy của số dư được hoãn đến khi thông báo ra.

### 2.4 Critic bổ sung cho Phần 2
- **Registry ghi alpha thực tế:** `CTX` theo dõi alpha tích lũy qua các lần `saveLayerAlpha`. Mỗi chữ được ghi kèm `alpha_eff`.
- **Kiểm tra ghost text (critical):** không có hai chữ chồng lên nhau mà cả hai đều có `alpha_eff > 0,15`, ở bất kỳ lớp nào.
- **Kiểm tra bằng pixel:** trong vùng y 100–300, đếm số lần độ tương phản cạnh chữ "lóe lên" ngắn hơn 3 khung hình (hiện rồi tắt). Kết quả phải bằng 0.
- **Thời gian hiển thị:** mỗi thông báo có ít nhất 16 khung hình hiện rõ với alpha ≥ 0,95.

---

## PHẦN 3 — NHẠC VÀ ÂM THANH CHUYÊN NGHIỆP

### 3.1 Hiện trạng
- Oscillator saw tự viết không band-limited nên có răng cưa (aliasing). Arp dùng sóng vuông thô. Không có reverb, chỉ có một delay đơn giản.
- Bố cục bài 8 bar gần như lặp lại. Thiếu hook giai điệu nên chưa có "điểm nhớ".
- Master chỉ có soft-clip. Chưa đo LUFS và True Peak.
- Các sự kiện trade rơi tự do theo storyboard, không khớp với beat.

### 3.2 Engine âm thanh mới (`src/audio/` gồm nhiều module)

| Module | Nội dung |
|---|---|
| `osc.py` | Saw/square band-limited (PolyBLEP), supersaw 7 voice (detune ±18 cent, pha ngẫu nhiên, trải stereo) |
| `filters.py` | State-variable filter có cộng hưởng, envelope filter theo từng nốt; ADSR |
| `fx.py` | Reverb Freeverb (8 comb + 4 allpass) hoặc convolution với IR tự tạo; ping-pong delay 3/16; chorus; saturation (tanh, oversample 2×) |
| `drums.py` | Kick 3 lớp (sub sine 50 Hz, body 120→55 Hz, click 3 kHz); snare = clap + noise + tone 190 Hz; hats có velocity và swing 54%; open hat ở nhịp lẻ; ride trong đoạn drop |
| `instruments.py` | Bass chia 2: sub sine dưới 90 Hz + mid "reese" có LFO filter 1/4; pad; pluck; lead |
| `mix.py` | Bus drums/bass/music/SFX; EQ (HPF 30 Hz cho mọi thứ trừ kick/bass, cắt 250 Hz ở pad); sidechain mượt; glue compressor 2:1 trên bus; master limiter look-ahead 5 ms |
| `master.py` | Đo LUFS theo ITU-R BS.1770 (thư viện `pyloudnorm`), True Peak oversample 4× |

### 3.3 Bố cục bài 128 BPM, A minor (15 giây = 8 bar)

| Bar | Thời gian | Đoạn | Nội dung |
|---|---|---|---|
| 1–2 | 0,00–3,75 | Intro | Pad filter mở dần, pluck hook, kick từ bar 2, uplifter cuối bar 2 |
| 3–4 | 3,75–7,50 | Build/Groove | Bass reese, hats đủ, hook lead lần 1 (filter 2 kHz) |
| 5 | 7,50–9,38 | Drop A | Lead đủ dải, ride, chord stab |
| 6 | 9,38–11,25 | Breakdown | Bỏ kick, chỉ pad + arp nhẹ (khớp cảnh Bots/Activity) |
| 6,5–7 | 11,25–12,55 | Riser | Noise sweep, snare roll 1/16 → 1/32, pitch riser +12 bán cung |
| 7–8 | 12,55–15,00 | Drop B/Finale | Impact + sub boom, lead lên quãng 8, hợp âm mở rộng; đuôi reverb khi end card hiện |

**Hook giai điệu (lead, 2 bar, lặp lại):** A4 – C5 – E5 – D5 | C5 – A4 – G4 – A4. Mỗi nốt là 1/8 có nghỉ, đặt chủ yếu ở phách nghịch. Vòng hợp âm giữ Am – F – C – G.

### 3.4 Khớp beat (quan trọng nhất)
- Lưới thời gian là 1/8 nốt = 0,2344 giây. Mỗi `t_video` của sự kiện (BUY/SELL/STOP) được **lượng tử hóa về điểm lưới gần nhất** trong `scenario.py`. Ví dụ: 3,35 → 3,281, 4,75 → 4,688, 12,55 → 12,656 (rơi đúng downbeat của drop).
- Animation (marker, pulse, push camera) bắt đầu đúng khung chứa beat. Âm thanh SFX có tiền-transient 10 ms để đỉnh âm rơi đúng beat.
- Critic: mọi sự kiện lệch khỏi beat tối đa ±1 khung hình (33 ms).

### 3.5 Thiết kế SFX mới
- **Thông báo:** chuông FM nguyên bản (tỉ lệ carrier/modulator 1:3,5), 2 nốt E6 → B6, đuôi ngắn 0,4 giây. Mang hơi hướng iOS nhưng không sao chép âm báo của Apple.
- **BUY:** whoosh ngắn + blip đi lên (600 → 1.400 Hz) + click nhẹ.
- **SELL thắng:** "cash" gồm 3 partial kim loại + 6–10 grain tiếng xu chạm nhau (tần số ngẫu nhiên 3–7 kHz) + tick đếm P&L khớp với con số đang chạy.
- **STOP:** tiếng thud trầm 80 Hz + sweep đi xuống + một nốt hơi lệch phím (dissonant) rất nhẹ.
- **Chuyển cảnh:** whoosh có pan theo hướng camera, ngắt trước downbeat.
- Khi SFX phát, nhạc tự giảm 2–3 dB rồi hồi lại trong 120 ms.

### 3.6 Chuẩn master (critic kiểm tra critical)
- Loudness tích hợp **−14 LUFS ±1** (chuẩn TikTok/Reels).
- **True Peak ≤ −1,0 dBTP**, đo trên file AAC sau khi encode.
- Không có đoạn lặng dài quá 150 ms (trừ chủ ý ở breakdown) và không có bước nhảy âm lượng ngắn hạn quá +6 LU.
- Xuất thêm 4 stem (drums, bass, music, sfx) để bạn có thể tự mix lại.
- Tùy chọn mới `config.audio.music_file`: dùng bài nhạc có bản quyền do bạn cung cấp, khai báo BPM và downbeat đầu tiên. Khi đó hệ thống tự căn sự kiện theo beat của bài đó.

---

## PHẦN 4 — GIỚI HẠN LỜI/LỖ MỖI LỆNH

### 4.1 Quy tắc mới (đưa vào `config.json`)
```json
"trade_limits": {
  "win_usd":  [12, 999.99],
  "loss_usd": [10, 300],
  "max_share_of_total": 0.30,
  "win_pct":  [0.15, 2.50],
  "loss_pct": [-0.45, -0.10],
  "max_size_frac_of_equity": 0.45
}
```
- Mọi lệnh có |P&L| nằm trong khoảng **từ hàng chục đến hàng trăm đô** (tối đa $999.99).
- Không lệnh nào chiếm quá 30% tổng lợi nhuận, để số dư tăng dần đều, không dồn hết vào một cú.
- Tổng lợi nhuận vẫn ngẫu nhiên trong khoảng $1,000–$5,000.

### 4.2 Thuật toán phân bổ mới (thay cho cách "lệnh cuối gánh phần dư")
1. Chọn tổng lợi nhuận mục tiêu `T`. Số lệnh thắng cần ít nhất là `ceil(T / 999,99 / 0,9)`. Nếu số slot hiện có không đủ thì tăng số lệnh lịch sử, tối đa 8.
2. Các lệnh FIONA (chart thật) có % lãi **cố định từ giá nến thật**. Size của chúng được chọn sao cho `size × %lãi` nằm trong giới hạn: `size = clamp(target_i / gain, min, 0,45 × equity)`.
3. Các lệnh còn lại được phân bổ bằng **water-filling**:
   - Lấy trọng số ngẫu nhiên theo phân phối Dirichlet(α = 2), nhân với phần lợi nhuận còn thiếu.
   - Lệnh nào vượt trần thì cắt về trần và chia phần thừa cho các lệnh khác.
   - Lặp lại tối đa 20 vòng.
4. Mỗi lệnh lỗ lấy ngẫu nhiên trong $10–$300, và cộng bù phần lỗ đó vào mục tiêu của các lệnh thắng.
5. Từ P&L, tính ngược lại size và % sao cho cả hai nằm trong giới hạn. Nếu không được thì điều chỉnh size trước, sau đó mới điều chỉnh %.
6. Lệnh cuối (finale) được ưu tiên là lệnh lớn nhất nhưng vẫn ≤ $999.99, để cao trào vẫn rõ.
7. Toàn bộ tính bằng cent nguyên. Kiểm tra lại: vốn + Σ P&L = số dư cuối, khớp chính xác.

### 4.3 Critic bổ sung cho Phần 4 (critical)
- `all |pnl| ∈ [10, 999.99]`
- `max(pnl) / total ≤ 0.30`
- `size ≤ 45% equity_before` cho mọi lệnh
- Các % nằm trong khoảng cho phép
- Lệnh FIONA: % phải đúng bằng chênh lệch giá nến thật

---

## THỨ TỰ THỰC HIỆN VÀ ƯỚC TÍNH

| Bước | Việc | Thời gian ước tính |
|---|---|---|
| 1 | Phần 4: thuật toán phân bổ + critic | 10–15 phút |
| 2 | Phần 2: Banner Manager + sticky + critic ghost | 20–30 phút |
| 3 | Phần 3: engine âm thanh, bố cục bài, khớp beat, master LUFS | 45–60 phút |
| 4 | Phần 1: scene graph nhiều lớp + camera 3D + chuyển cảnh fly-out | 45–60 phút |
| 5 | Phần 1: coin Blender (cài đặt + render sprite) | 15–20 phút |
| 6 | Render, chạy critic, tự soi bằng mắt, sửa lỗi, render lại (2–3 vòng) | 20–30 phút |

Phần 4 và Phần 2 nhanh và ít rủi ro nên làm trước. Phần 3 và Phần 1 cần nghe và xem thử nhiều lần.

## ĐIỀU KIỆN NGHIỆM THU V1.8.4
- Critic tự động: tất cả hạng mục cũ (35) và mới (khoảng 12) đều đạt. Không có lỗi critical.
- Tự soi bằng mắt ở ít nhất 12 mốc thời gian, đặt cạnh video mẫu.
- Điểm từng phần: 3D ≥ 9,5; thông báo ≥ 9,8; âm thanh ≥ 9,5; tổng ≥ 9,5.
- Kỹ thuật giữ nguyên: 1080×1920, 30 fps, 450 khung hình, H.264, AAC 48 kHz stereo, đúng 15,000 giây.
- Bàn giao: MP4, preview, contact sheet, ảnh so sánh, báo cáo Visual Critic, báo cáo dữ liệu, 4 stem âm thanh, ZIP skill cập nhật, SKILL.md cập nhật (changelog 1.8.4).
