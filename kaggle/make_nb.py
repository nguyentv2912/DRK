import json, sys

def md(s): return {"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")}
def code(s): return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")}

REF_TEXT = ("làm sao để chúng ta có thể tăng hai trăm lần tài sản của mình trong vòng mười năm, "
            "thì đây là một cái công thức mà sau mười năm đầu tư vào thị trường tài sản mới")

cells = [
md("""
# Video nói chuyện miễn phí: clone giọng + khớp môi

**Trước khi chạy (làm 1 lần):**
1. Bên phải màn hình → **Session options** → *Accelerator*: **GPU T4 x1** · *Internet*: **On**
   (lần đầu Kaggle bắt xác minh số điện thoại mới bật được Internet).
2. Bấm **+ Add Input → Upload → New Dataset**, kéo vào 3 file rồi Create:
   - `ref.wav` — giọng mẫu ~11 giây
   - `mat.mp4` — clip mặt 25fps
   - `kichban.txt` — kịch bản (viết số bằng chữ, mỗi câu một dòng)
3. Bấm **Run All**. Lần đầu mất ~10 phút cài đặt, sau đó ~20–30 phút cho video 2 phút.

**Kết quả** nằm ở thanh bên phải → *Output* (`/kaggle/working`):
`giong.wav` (giọng clone) và **`noi.mp4`** (video đã khớp môi) → tải về, bỏ vào Google Drive, gửi link cho Claude.
"""),
md("## 1. Cấu hình"),
code(f'''
import glob, os, subprocess, textwrap
def find(name):
    hits = glob.glob(f"/kaggle/input/**/{{name}}", recursive=True)
    assert hits, f"Không thấy {{name}} trong /kaggle/input — kiểm tra lại bước Add Input"
    return hits[0]

REF_AUDIO = find("ref.wav")
FACE_VIDEO = find("mat.mp4")
SCRIPT_FILE = find("kichban.txt")

# Lời nói đúng của ref.wav (viết thường). Đổi nếu bạn thay giọng mẫu khác.
REF_TEXT = "{REF_TEXT}"

SPEED = 1.0        # 0.9 = chậm hơn, 1.1 = nhanh hơn
TEST_ONLY = False  # True = chỉ làm 15 giây đầu để thử
W = "/kaggle/working"
print(REF_AUDIO, FACE_VIDEO, SCRIPT_FILE, sep="\\n")
!nvidia-smi --query-gpu=name,memory.total --format=csv
'''),
md("## 2. Cài đặt (2 môi trường riêng để không xung đột thư viện)"),
code('''
%%bash
set -e
cd /kaggle/temp 2>/dev/null || mkdir -p /kaggle/temp && cd /kaggle/temp
pip install -q uv
export UV_LINK_MODE=copy
# --- F5-TTS tiếng Việt (clone giọng) ---
[ -d F5-TTS-Vietnamese ] || git clone -q --depth 1 https://github.com/nguyenthienhy/F5-TTS-Vietnamese
[ -d f5env ] || uv venv -q -p 3.10 f5env
uv pip install -q -p f5env/bin/python torch==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121
uv pip install -q -p f5env/bin/python -e ./F5-TTS-Vietnamese
f5env/bin/huggingface-cli download hynt/F5-TTS-Vietnamese-ViVoice --local-dir f5model >/dev/null
cp f5model/config.json f5model/vocab.txt
# --- LatentSync 1.5 (khớp môi, chạy được trên T4 16GB) ---
[ -d LatentSync ] || git clone -q --depth 1 https://github.com/bytedance/LatentSync
[ -d lsenv ] || uv venv -q -p 3.10 lsenv
uv pip install -q -p lsenv/bin/python -r LatentSync/requirements.txt --index-strategy unsafe-best-match
cd LatentSync
../lsenv/bin/huggingface-cli download ByteDance/LatentSync-1.5 whisper/tiny.pt latentsync_unet.pt --local-dir checkpoints >/dev/null
ls -la checkpoints checkpoints/whisper
echo "CAI DAT XONG"
'''),
md("## 3. Clone giọng → `giong.wav`"),
code('''
import re, unicodedata
text = open(SCRIPT_FILE, encoding="utf-8").read()
text = unicodedata.normalize("NFC", text).lower()
text = re.sub(r"\\s*\\n+\\s*", ". ", text).strip()
text = re.sub(r"\\.\\s*\\.", ".", text)
if TEST_ONLY:
    text = " ".join(text.split()[:45])
open("/kaggle/temp/gen.txt", "w", encoding="utf-8").write(text)
print(len(text.split()), "chữ →", text[:300], "...")

T = "/kaggle/temp"
cmd = [f"{T}/f5env/bin/f5-tts_infer-cli", "--model", "F5TTS_Base",
       "--ref_audio", REF_AUDIO, "--ref_text", REF_TEXT,
       "--gen_file", f"{T}/gen.txt", "--speed", str(SPEED),
       "--vocoder_name", "vocos",
       "--vocab_file", f"{T}/f5model/vocab.txt", "--ckpt_file", f"{T}/f5model/model_last.pt",
       "--output_dir", W, "--output_file", "giong_raw.wav"]
subprocess.run(cmd, check=True, cwd=f"{T}/F5-TTS-Vietnamese")
# chuẩn hoá âm lượng
!ffmpeg -nostdin -v error -y -i {W}/giong_raw.wav -af loudnorm=I=-16:TP=-1.5 -ar 44100 {W}/giong.wav
import IPython.display as ipd
!ffprobe -v error -show_entries format=duration -of csv=p=0 {W}/giong.wav
ipd.display(ipd.Audio(f"{W}/giong.wav"))
'''),
md("""
👂 **Nghe thử ở trên.** Nếu câu nào đọc sai dấu: sửa chữ trong `kichban.txt` (viết đúng cách đọc, tách câu ngắn hơn),
upload lại dataset rồi chạy lại từ bước 3. Hài lòng rồi mới sang bước 4.
"""),
md("## 4. Khớp môi → `noi.mp4`"),
code('''
%%bash
set -e
export MPLBACKEND=Agg
cd /kaggle/temp/LatentSync
ffmpeg -nostdin -v error -y -i /kaggle/working/giong.wav -ar 16000 -ac 1 /kaggle/temp/giong16k.wav
time ../lsenv/bin/python -m scripts.inference \\
  --unet_config_path configs/unet/stage2.yaml \\
  --inference_ckpt_path checkpoints/latentsync_unet.pt \\
  --inference_steps 20 --guidance_scale 1.5 --enable_deepcache \\
  --video_path "$(find /kaggle/input -name mat.mp4 | head -1)" \\
  --audio_path /kaggle/temp/giong16k.wav \\
  --video_out_path /kaggle/temp/noi_raw.mp4
# ghép lại giọng chất lượng cao 44.1kHz thay cho bản 16kHz
ffmpeg -nostdin -v error -y -i /kaggle/temp/noi_raw.mp4 -i /kaggle/working/giong.wav -map 0:v -map 1:a \\
  -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest /kaggle/working/noi.mp4
ls -lh /kaggle/working
echo "XONG — tải noi.mp4 ở mục Output bên phải"
'''),
code('''
from IPython.display import Video
Video(f"{W}/noi.mp4", embed=True, width=360)
'''),
]

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
json.dump(nb, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
