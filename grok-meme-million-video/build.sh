#!/usr/bin/env bash
# GROK MEME MILLION V1.8.4 - one-shot build: data -> scenario -> frames -> audio -> mux -> critic
# Usage: ./build.sh <reference.mp4> [seed] [--offline]
set -euo pipefail
cd "$(dirname "$0")"
REF="${1:?reference video path required}"; SEED="${2:-}"; OFFLINE="${3:-}"
mkdir -p output
[ "$OFFLINE" = "--offline" ] || python3 src/fetch_data.py
python3 src/scenario.py $SEED
# real 3D coin sprites (rendered once, cached)
if [ "$(ls assets/coins/coin_*.png 2>/dev/null | wc -l)" -lt 72 ] && command -v blender >/dev/null; then
  blender -b -P src/blender_coin.py -- assets/coins 72 512 64 >/dev/null 2>&1 || echo "blender coin render failed - vector fallback"
fi
python3 src/render.py
python3 src/audio.py
ffmpeg -nostdin -y -v error -i output/grok_meme_million_v1.8.4_silent.mp4 -i output/soundtrack.wav \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -ac 2 -movflags +faststart output/grok_meme_million_v1.8.4.mp4
python3 src/critic.py --ref "$REF"
python3 src/report.py
