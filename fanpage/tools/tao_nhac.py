#!/usr/bin/env python3
"""Tạo nhạc nền êm, không bản quyền (tự tổng hợp) cho video Đạo Đức Đầu Tư.
  python3 fanpage/tools/tao_nhac.py OUT.mp3 [GIÂY=90] [SEED=1]
Hợp âm Am–F–C–G, 72 bpm: lớp pad ấm + nốt piano rải nhẹ + tiếng vang. Ghi mp3 qua ffmpeg.
"""
import subprocess, sys, os, numpy as np

SR = 44100


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a, r):
    e = np.ones(n)
    ai, ri = int(a * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, ai)
    e[-ri:] *= np.linspace(1, 0, ri)
    return e


def pad(freqs, dur):
    t = np.arange(int(dur * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.003 * t) + 0.2 * np.sin(2 * np.pi * 2 * f * t)
            for f in freqs)
    return x / len(freqs) * env(len(t), dur * 0.35, dur * 0.35)


def pluck(f, dur=1.6):
    t = np.arange(int(dur * SR)) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t))
    return x * np.exp(-3.2 * t) * env(len(t), 0.005, 0.2)


def main(out, secs=90, seed=1):
    rng = np.random.default_rng(seed)
    beat = 60 / 72
    bar = 4 * beat
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    n = int(secs * SR) + SR * 4
    L = np.zeros(n)
    t0 = 0.0
    k = 0
    while t0 < secs:
        ch = chords[k % 4]
        s = int(t0 * SR)
        p = pad([note(m - 12) for m in ch], bar * 1.25)
        L[s:s + len(p)] += 0.32 * p[: n - s]
        bass = pluck(note(ch[0] - 24), bar) * 0.5
        L[s:s + len(bass)] += bass[: n - s]
        for b in range(8):  # nốt rải mỗi nửa phách
            if rng.random() < 0.72:
                m = ch[rng.integers(0, 3)] + 12 * rng.integers(0, 2)
                pl = pluck(note(m)) * (0.16 + 0.08 * rng.random())
                ps = s + int(b * beat / 2 * SR)
                L[ps:ps + len(pl)] += pl[: max(0, n - ps)]
        t0 += bar
        k += 1
    for d, g in [(0.23, 0.35), (0.37, 0.25), (0.61, 0.15)]:  # tiếng vang
        sh = int(d * SR)
        L[sh:] += g * L[:-sh]
    R = np.roll(L, int(0.012 * SR))
    st = np.stack([L, R], 1)[: int(secs * SR)]
    st = st / np.max(np.abs(st)) * 0.6
    raw = out + ".raw"
    (st * 32767).astype("<i2").tofile(raw)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", raw,
                    "-af", "lowpass=f=6000,afade=t=in:d=1", "-b:a", "128k", out], check=True)
    os.remove(raw)
    print("OK", out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 90, int(sys.argv[3]) if len(sys.argv) > 3 else 1)
