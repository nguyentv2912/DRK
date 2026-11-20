#!/usr/bin/env python3
"""GROK MEME MILLION V1.8.3 - original EDM soundtrack + synced SFX (48 kHz stereo).

Everything is synthesised here (no samples, no third-party music), so the
track is original and license-free. SFX are placed from the same event list
the renderer uses (scenario.json), so audio and picture share one clock.
"""
import json, os, sys, math
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
CFG = json.load(open(os.path.join(ROOT, "config.json")))
SR = CFG["video"]["audio_rate"]
DUR = CFG["video"]["duration"]
BPM = CFG["video"]["bpm"]
BEAT = 60 / BPM
N = int(SR * DUR)
rng = np.random.RandomState(7)


def t_(d):
    return np.arange(int(d * SR)) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, f / (SR / 2), "low", output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f / (SR / 2), "high", output="sos"), x)


def bp(x, f1, f2):
    return sosfilt(butter(2, [f1 / (SR / 2), f2 / (SR / 2)], "band", output="sos"), x)


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


class Bus:
    def __init__(self):
        self.L = np.zeros(N + SR); self.R = np.zeros(N + SR)

    def add(self, at, x, gain=1.0, pan=0.0):
        i = int(at * SR)
        if i >= N:
            return
        x = x[: N + SR - i] * gain
        l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        self.L[i:i + len(x)] += x * l * 1.414
        self.R[i:i + len(x)] += x * r * 1.414


# ---------------------------------------------------------------- instruments

def kick():
    tt = t_(.42)
    f = 46 + 110 * np.exp(-tt * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt * 7.5) + .25 * np.exp(-tt * 180) * rng.randn(len(tt))


def hat(d=.05, bright=8000):
    tt = t_(d)
    return hp(rng.randn(len(tt)), bright) * np.exp(-tt * 70)


def clap():
    tt = t_(.22)
    env = np.exp(-tt * 22) + .6 * np.exp(-((tt - .012) ** 2) / 2e-5) + .5 * np.exp(-((tt - .024) ** 2) / 2e-5)
    return bp(rng.randn(len(tt)), 900, 4200) * env


def saw(f, d, detune=0.0):
    tt = t_(d)
    return 2 * ((tt * f * (1 + detune)) % 1) - 1


def supersaw(freqs, d, cutoff):
    L = np.zeros(int(d * SR)); R = np.zeros_like(L)
    for f in freqs:
        for k, dt in enumerate((-.012, -.006, 0, .006, .012)):
            s = saw(f, d, dt) * (1 if dt == 0 else .7)
            if k % 2:
                L += s
            else:
                R += s
    return lp(L, cutoff) * .05, lp(R, cutoff) * .05


def bell(f, d=.6, decay=7):
    tt = t_(d)
    return (np.sin(2 * np.pi * f * tt) + .45 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 6) +
            .2 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 14)) * np.exp(-tt * decay) * np.minimum(1, tt * 400)


def sweep(f0, f1, d, kind="sine"):
    tt = t_(d)
    f = f0 * (f1 / f0) ** (tt / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.minimum(1, tt * 300) * np.exp(-tt * 3 / d)


def noise_sweep(d, f0, f1, rise=True):
    tt = t_(d)
    x = rng.randn(len(tt))
    out = np.zeros_like(x)
    seg = int(SR * .02)
    for i in range(0, len(x), seg):
        k = i / len(x)
        fc = f0 * (f1 / f0) ** k
        out[i:i + seg] = bp(x[i:i + seg + 400], fc * .7, min(fc * 1.4, SR / 2 - 100))[:len(out[i:i + seg])]
    env = (tt / d) ** 2 if rise else np.exp(-tt * 5 / d)
    return out * env


# --------------------------------------------------------------------- music

def music():
    m, sfx_side = Bus(), np.ones(N + SR)
    bars = int(DUR / (BEAT * 4)) + 1
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    roots = [45, 41, 36, 43]
    K = kick()
    for b in range(int(DUR / BEAT) + 1):
        at = b * BEAT
        drop_gap = 11.25 <= at < 12.55
        if not drop_gap or at < 11.6:
            m.add(at, K, .95)
            i = int(at * SR)
            env = 1 - .75 * np.exp(-t_(BEAT) * 9)
            sfx_side[i:i + len(env)] = np.minimum(sfx_side[i:i + len(env)], env)
        if b % 2 == 1 and at > 1.8 and not drop_gap:
            m.add(at, clap(), .33, .05)
        if not drop_gap:
            m.add(at + BEAT / 2, hat(.06, 7000), .20, .25)
            if at > 3.7:
                m.add(at + BEAT / 4, hat(.03, 10000), .08, -.3)
                m.add(at + 3 * BEAT / 4, hat(.03, 10000), .08, .3)
    # pads + bass + arp
    for bar in range(bars):
        at = bar * 4 * BEAT
        ch = chords[bar % 4]
        cut = 1400 if at < 3.7 else 2600 if at < 11 else 1800
        Lp, Rp = supersaw([note(n) for n in ch], 4 * BEAT, cut)
        env = np.minimum(1, t_(4 * BEAT) * 8) * np.minimum(1, (4 * BEAT - t_(4 * BEAT)) * 10)
        m.add(at, Lp * env, .9, -.6); m.add(at, Rp * env, .9, .6)
        for e in range(8):
            ta = at + e * BEAT / 2 + BEAT / 2 * (e % 2 == 0) * 0
            if ta >= DUR or (11.25 <= ta < 12.55):
                continue
            f = note(roots[bar % 4])
            bs = lp(saw(f, BEAT / 2 * .9) + .5 * np.sin(2 * np.pi * f / 2 * t_(BEAT / 2 * .9)), 380)
            m.add(ta + BEAT / 4 if e % 2 == 0 else ta, bs * np.exp(-t_(BEAT / 2 * .9) * 4), .38)
        if at >= 3.7:
            tones = ch + [ch[0] + 12, ch[1] + 12]
            for s16 in range(16):
                ta = at + s16 * BEAT / 4
                if ta >= DUR or (11.25 <= ta < 12.55):
                    continue
                n_ = tones[(s16 * 3) % len(tones)] + 12
                tt = t_(BEAT / 4)
                x = np.sign(np.sin(2 * np.pi * note(n_) * tt)) * np.exp(-tt * 22)
                x = lp(x, 3200)
                m.add(ta, x, .055, .4 if s16 % 2 else -.4)
                m.add(ta + BEAT * .75, x, .025, -.5 if s16 % 2 else .5)  # ping-pong delay
    # riser into the finale + drop + title
    m.add(11.25, noise_sweep(1.3, 400, 9000), .32, 0)
    for k in range(16):  # snare roll
        m.add(11.6 + k * (0.95 / 16), clap() * (k / 16 + .2), .25)
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t_(1.6) * 6)) / SR) * np.exp(-t_(1.6) * 2.2)
    m.add(12.55, boom, .9)
    m.add(12.55, hp(rng.randn(int(1.8 * SR)), 3000) * np.exp(-t_(1.8) * 2.6), .22)
    Lp, Rp = supersaw([note(n) for n in (57, 60, 64, 69, 72)], 2.6, 3000)
    env = np.minimum(1, t_(2.6) * 4) * np.exp(-t_(2.6) * .7)
    m.add(13.75, Lp * env, 1.0, -.7); m.add(13.75, Rp * env, 1.0, .7)
    # sidechain
    m.L[:len(sfx_side)] *= sfx_side * 1 + 0; m.R[:len(sfx_side)] *= sfx_side
    return m


def sfx(sc):
    s = Bus()
    sys.argv = sys.argv[:1]
    import render as R  # same event list & timeline as the picture
    for e in R.EVENTS:
        at = e["t"]
        s.add(at, bell(1568, .5, 9) + .7 * np.concatenate([np.zeros(int(.07 * SR)), bell(2093, .43, 9)]), .16, .2)  # iOS-style banner
        if e["type"] == "buy":
            s.add(at + .02, sweep(520, 1250, .14), .2, -.2)
        elif e["type"] == "sell":
            for k, f in enumerate((1318, 1760, 2637)):
                s.add(at + .1 + k * .06, bell(f, .7, 6), .12, (k - 1) * .4)
            s.add(at + .15, hp(rng.randn(int(.5 * SR)), 6000) * np.exp(-t_(.5) * 9), .07)
            for k in range(10):  # P&L count-up ticks
                s.add(at + .14 + k * .055, bell(3200 + 60 * k, .03, 80), .05)
        else:
            s.add(at + .02, sweep(620, 220, .32), .2)
    for at in (2.5, 9.0, 11.8):  # scene transitions
        s.add(at, noise_sweep(.55, 300, 6000, rise=False), .22, 0)
    for at in (2.65, 9.15):  # market scan sweeps
        s.add(at, sweep(900, 2400, .45) * .5, .1, .5)
    s.add(12.62, bell(2637, 1.2, 3), .14)
    s.add(13.75, bell(1760, 1.6, 2.2) + bell(2637, 1.6, 2.5), .14)
    return s


def main():
    sc = json.load(open(os.path.join(ROOT, "data", "scenario.json")))
    m, s = music(), sfx(sc)
    L = m.L[:N] * .55 + s.L[:N]
    Rr = m.R[:N] * .55 + s.R[:N]
    st = np.stack([L, Rr], 1)
    st = hp(st.T, 25).T
    fade = np.ones(N); fade[-int(.6 * SR):] = np.linspace(1, 0, int(.6 * SR)) ** 1.5
    fade[:int(.01 * SR)] = np.linspace(0, 1, int(.01 * SR))
    st *= fade[:, None]
    # gentle master: soft knee limiter, then -1 dBFS peak
    pk = np.abs(st).max()
    st = st / pk * 1.15
    st = np.tanh(st) / np.tanh(1.15)
    st *= 10 ** (-3 / 20) / np.abs(st).max()  # -3 dBFS sample peak leaves AAC true-peak headroom
    out = os.path.join(ROOT, "output", "soundtrack.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wavfile.write(out, SR, (st * 32767).astype(np.int16))
    print("wrote", out, "peak dBFS %.2f" % (20 * np.log10(np.abs(st).max())))


if __name__ == "__main__":
    main()
