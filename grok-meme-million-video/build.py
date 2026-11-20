#!/usr/bin/env python3
"""GROK MEME MILLION V1.8.4 - cross-platform one-shot build (Windows / macOS / Linux).

    python build.py                       # fresh data, random seed
    python build.py --seed 777            # same numbers again
    python build.py --offline             # reuse data/market_snapshot.json
    python build.py --ref path/to/ref.mp4 # compare with a reference video (default: bundled stills)

Steps: data -> scenario -> (coin sprites if missing) -> frames -> audio -> mux -> critic -> reports.
Exit code 1 if the Visual Critic rejects the build.
"""
import argparse, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
VER = "1.8.4"


def run(*cmd):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--ref")
    ap.add_argument("--jobs", type=int, default=os.cpu_count())
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH (Windows: winget install Gyan.FFmpeg)")
    os.makedirs(os.path.join(ROOT, "output"), exist_ok=True)
    if not a.offline:
        run(PY, "src/fetch_data.py")
    run(PY, "src/scenario.py", *([str(a.seed)] if a.seed is not None else []))
    coins = [f for f in os.listdir(os.path.join(ROOT, "assets", "coins")) if f.endswith(".png")] if os.path.isdir(os.path.join(ROOT, "assets", "coins")) else []
    if len(coins) < 72 and shutil.which("blender"):
        run("blender", "-b", "-P", "src/blender_coin.py", "--", "assets/coins", "72", "448", "64")
    run(PY, "src/render.py", "--jobs", str(a.jobs))
    run(PY, "src/audio.py")
    run("ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f"output/grok_meme_million_v{VER}_silent.mp4", "-i", "output/soundtrack.wav",
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", f"output/grok_meme_million_v{VER}.mp4")
    crit = subprocess.run([PY, "src/critic.py", *(["--ref", a.ref] if a.ref else [])], cwd=ROOT)
    run(PY, "src/report.py")
    print("\nDone:", os.path.join(ROOT, "output", f"grok_meme_million_v{VER}.mp4"))
    sys.exit(crit.returncode)


if __name__ == "__main__":
    main()
