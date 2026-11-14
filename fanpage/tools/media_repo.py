#!/usr/bin/env python3
"""Kho tạm cho video đã edit, để Metricool lấy qua link công khai.

  python3 fanpage/tools/media_repo.py put  <video.mp4> <ten-file.mp4>   → in ra URL công khai
  python3 fanpage/tools/media_repo.py clear                             → xoá mọi video khỏi kho
  python3 fanpage/tools/media_repo.py check <url>                        → kiểm tra URL tải được (HTTP 200, dung lượng)

Kho = repo trong fanpage/config.json ("media_repo"), nhánh mồ côi "media" bị ghi đè (force push)
mỗi lần, nên lịch sử chỉ giữ video mới nhất; 'clear' đẩy một commit rỗng để gỡ video.
Giới hạn GitHub: mỗi file < 100 MB (nên giữ video < 90 MB).
"""
import json, os, subprocess, sys, tempfile, shutil

CFG = json.load(open(os.path.join(os.path.dirname(__file__), "..", "config.json"), encoding="utf-8"))
REPO = CFG["media_repo"]
BRANCH = "media"


def git(*a, cwd):
    subprocess.run(["git", *a], cwd=cwd, check=True)


def fresh_repo():
    d = tempfile.mkdtemp(prefix="media_")
    git("init", "-q", cwd=d)
    git("checkout", "-q", "--orphan", BRANCH, cwd=d)
    git("config", "user.name", "Doi AI Dao Duc Dau Tu", cwd=d)
    git("config", "user.email", "noreply@example.com", cwd=d)
    git("remote", "add", "origin", f"https://github.com/{REPO}.git", cwd=d)
    return d


def push(d, msg):
    git("add", "-A", cwd=d)
    git("commit", "-q", "--allow-empty", "-m", msg, cwd=d)
    for i in range(4):
        r = subprocess.run(["git", "push", "-q", "-f", "origin", BRANCH], cwd=d)
        if r.returncode == 0:
            return
        subprocess.run(["sleep", str(2 ** (i + 1))])
    sys.exit("Đẩy lên kho media thất bại (kiểm tra repo đã tạo và phiên có quyền push).")


def put(src, name):
    size = os.path.getsize(src) / 1e6
    if size > 95:
        sys.exit(f"Video {size:.0f} MB > 95 MB — nén lại (tăng crf) rồi thử lại.")
    d = fresh_repo()
    os.makedirs(os.path.join(d, "v"), exist_ok=True)
    shutil.copy(src, os.path.join(d, "v", name))
    push(d, f"video {name}")
    shutil.rmtree(d)
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/v/{name}"
    print(url)


def clear():
    d = fresh_repo()
    open(os.path.join(d, "README.md"), "w").write("Kho tạm video — trống.\n")
    push(d, "clear")
    shutil.rmtree(d)
    print("Đã xoá video khỏi kho media.")


def check(url):
    out = subprocess.run(["curl", "-sSIL", "-m", "30", url], capture_output=True, text=True).stdout
    code = [l for l in out.splitlines() if l.startswith("HTTP/")]
    size = [l for l in out.splitlines() if l.lower().startswith("content-length")]
    print(code[-1] if code else "không phản hồi", size[-1] if size else "")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["put"] and len(a) == 3: put(a[1], a[2])
    elif a[:1] == ["clear"]: clear()
    elif a[:1] == ["check"] and len(a) == 2: check(a[1])
    else: sys.exit(__doc__)
