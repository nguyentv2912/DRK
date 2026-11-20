#!/usr/bin/env python3
"""GROK MEME MILLION V1.8.4 - original EDM soundtrack + beat-locked SFX (48 kHz stereo).

128 BPM, A minor, 8 bars = exactly 15 s. Everything is synthesised by the
`sound` package (band-limited oscillators, layered drums, convolution reverb,
sidechain, bus compression, BS.1770 loudness mastering), so the music is
original and license-free. Trade events come from the renderer's own event
list (already quantized to the 1/8-note grid in scenario.py), so picture,
music and SFX share one clock.

Outputs: output/soundtrack.wav (mastered, -14 LUFS, <= -1 dBTP) and
output/stems/{drums,bass,music,sfx}.wav.
"""
import json, os, sys
import numpy as np
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sound import SR  # noqa: E402
from sound.osc import sine, saw  # noqa: E402
from sound.filters import hp, lp, bp, tv_lp, exp_env, adsr  # noqa: E402
from sound.fx import reverb_ir, reverb, pingpong, chorus, saturate  # noqa: E402
from sound import drums as D, instruments as I  # noqa: E402
from sound.mix import Bus, sidechain_env, duck_env, compress, limiter  # noqa: E402
from sound.master import master, lufs, true_peak_db  # noqa: E402

CFG = json.load(open(os.path.join(ROOT, "config.json")))
DUR = CFG["video"]["duration"]
BPM = CFG["video"]["bpm"]
BEAT = 60 / BPM
E8 = BEAT / 2
BAR = 4 * BEAT
N = int(round(DUR * SR))
rng = np.random.RandomState(11)
prng = np.random.default_rng(11)

CHORDS = [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]]   # Am F C G
ROOTS = [45, 41, 48, 43]
HOOK = [(1, 69), (3, 72), (4, 76), (6, 74), (9, 72), (11, 69), (12, 67), (14, 69)]  # (eighth index, midi) over 2 bars


def load_events():
    sys.argv = sys.argv[:1]
    import render as R
    return R


def build(R):
    t_drop = [e["t"] for e in R.EVENTS if e["type"] == "sell"][-1]          # finale SELL = drop B
    t_end = R.END_T
    BRK0, BRK1 = 5 * BAR, 6 * BAR            # breakdown bar 6
    RIS0 = 6 * BAR                           # riser from bar 7 start to the drop
    drums, bass, music, sfx = Bus(N), Bus(N), Bus(N), Bus(N)
    K = D.kick(rng)
    kicks = []

    def in_drop(t):
        return (3 * BAR <= t < BRK0) or t >= t_drop

    # ---------------- drums
    nbeats = int(DUR / BEAT) + 1
    for b in range(nbeats):
        t = b * BEAT
        groove = (BAR <= t < BRK0) or (t_drop - 1e-6 <= t < DUR - .4)
        if groove:
            drums.add(t, K, .95); kicks.append(t)
        if (2 * BAR <= t < BRK0 or t >= t_drop) and b % 2 == 1:
            drums.add(t, D.snare(rng), .42, .04)
        if t < RIS0 or t >= t_drop:
            if t < BRK0 or t >= t_drop:
                drums.add(t + E8 + .012, D.hat(rng, vel=.9), .22, .22)  # swung offbeat 8th
            elif BRK0 <= t < BRK1:
                drums.add(t + E8, D.hat(rng, vel=.5), .12, .22)
        if 2 * BAR <= t < BRK0 or t >= t_drop:
            for k, v in ((1, .45), (3, .6)):
                drums.add(t + k * BEAT / 4 + (.008 if k == 3 else 0), D.hat(rng, vel=v), .12, -.3 if k == 1 else .3)
            if b % 4 == 3:
                drums.add(t + E8, D.hat(rng, open_=True, vel=.8), .16, .35)
        if in_drop(t) and t >= 4 * BAR:
            drums.add(t, D.ride(rng), .9, -.45)
    # riser snare roll: 1/16 -> 1/32
    t = RIS0
    while t < t_drop - .02:
        step = BEAT / 4 if t < RIS0 + (t_drop - RIS0) * .6 else BEAT / 8
        k = (t - RIS0) / (t_drop - RIS0)
        drums.add(t, D.snare(rng), .08 + .3 * k ** 1.5, (k - .5) * .4)
        t += step

    # ---------------- bass (sub + reese)
    for bar in range(8):
        t0 = bar * BAR
        r = ROOTS[bar % 4]
        if bar < 2 or 5 <= bar < 6:
            if bar >= 1:
                bass.add(t0, I.sub(r, BAR * .98) * np.linspace(.35, .12, int(BAR * .98 * SR)) if bar == 5 else I.sub(r, BAR * .98) * .3, 1.0)
            continue
        for e in range(8):
            t = t0 + e * E8
            if RIS0 <= t < t_drop:
                continue
            bass.add(t, I.sub(r, E8 * .92), .55)
            if e % 2 == 1:
                bass.add(t, I.reese(r + 12, E8 * .9, t), .42)

    # ---------------- pads (cutoff per section)
    for bar in range(8):
        t0 = bar * BAR
        cut = [900, 1700, 2200, 2400, 3200, 1400, 2600, 3400][bar]
        L, R_ = I.pad(CHORDS[bar % 4], BAR + .35, prng, cut)
        g = 1.0
        music.add2(t0, L, R_, g)
    # ---------------- pluck hook (intro) & breakdown arp
    for bar in (0, 1):
        for idx, m in HOOK:
            if idx // 8 == bar % 2:
                t = bar * BAR + (idx % 8) * E8 + (BAR if False else 0)
                t = (bar // 2) * 2 * BAR + idx * E8
                if t < 2 * BAR:
                    music.add(t, I.pluck(m, E8 * 1.6, 2600 + 900 * bar), .55, .45 if idx % 2 else -.45)
    for s16 in range(16):
        t = BRK0 + s16 * BEAT / 4
        ch = CHORDS[5 % 4] + [CHORDS[5 % 4][0] + 12]
        music.add(t, I.pluck(ch[(s16 * 3) % 4] + 12, BEAT / 4, 2000), .3, .6 if s16 % 2 else -.6)
    # ---------------- lead hook: bars 3-4 filtered, bar 5 full, drop B octave up
    def play_hook(start, bars, octave, bright, gain):
        for rep in range(bars // 2 + 1):
            for idx, m in HOOK:
                t = start + rep * 2 * BAR + idx * E8
                if t >= start + bars * BAR or t >= DUR - .3:
                    continue
                L, R_ = I.lead(m + 12 * octave, E8 * .95, prng, bright)
                music.add2(t, L, R_, gain)
    play_hook(2 * BAR, 2, 0, .45, .30)
    play_hook(4 * BAR, 1, 0, 1.0, .34)
    play_hook(t_drop, 2, 1, 1.1, .30)
    for t in (4 * BAR, t_drop):
        L, R_ = I.stab(CHORDS[0] + [69], .6, prng)
        music.add2(t, L, R_, 1.0)

    # ---------------- transitions, riser, impact, end card
    def noise_sweep(dur, f0, f1, rise=True):
        n = int(dur * SR); x = rng.randn(n)
        cut = f0 * (f1 / f0) ** (np.arange(n) / n)
        y = tv_lp(x, cut, 1.2) - tv_lp(x, cut * .45, .7)
        env = (np.arange(n) / n) ** 2 if rise else exp_env(n, 4 / dur)
        return y * env

    music.add(RIS0, noise_sweep(t_drop - RIS0, 300, 11000), .5)
    n = int((t_drop - RIS0) * SR)
    f = I.note(57) * 2 ** (np.linspace(0, 12, n) / 12)
    music.add(RIS0, lp(saw(f, n), 5000) * np.linspace(0, 1, n) ** 2 * .18, 1.0)
    boom_n = int(1.8 * SR); tb = np.arange(boom_n) / SR
    music.add(t_drop, sine(36 + 70 * np.exp(-tb * 7), boom_n) * np.exp(-tb * 2.0), 1.0)
    crash = hp(rng.randn(int(2.2 * SR)), 3500) * exp_env(int(2.2 * SR), 2.2)
    music.add(t_drop, crash, .22, -.2); music.add(t_drop + .01, crash, .22, .2)
    rev = crash[: int(1.0 * SR)][::-1] * np.linspace(0, 1, int(1.0 * SR)) ** 2
    music.add(t_drop - 1.0, rev, .18)
    L, R_ = I.pad([57, 60, 64, 69, 72, 76], DUR - t_end + .5, prng, 4200)
    music.add2(t_end, L, R_, 1.0)

    # ---------------- SFX (beat-locked: transient lands on the event frame)
    def fm_bell(f, dur=.42, ratio=3.5, index=2.2, decay=9):
        n = int(dur * SR); t = np.arange(n) / SR
        mod = np.sin(2 * np.pi * f * ratio * t) * index * np.exp(-t * 14)
        return np.sin(2 * np.pi * f * t + mod) * np.exp(-t * decay) * np.minimum(1, t * 600)

    def whoosh(dur=.5, f0=400, f1=4000):
        return noise_sweep(dur, f0, f1, rise=False) * np.hanning(int(dur * SR)) * 2.2

    def coin_grains(k=8):
        out = np.zeros(int(.45 * SR))
        for _ in range(k):
            i = rng.randint(0, int(.35 * SR)); n = int(.03 * SR); t = np.arange(n) / SR
            fq = rng.uniform(3000, 7000)
            out[i:i + n] += (np.sin(2 * np.pi * fq * t) + .5 * np.sin(2 * np.pi * fq * 2.41 * t)) * np.exp(-t * 120)
        return out

    sfx_times = []
    for e in R.EVENTS:
        at = e["t"] - .005
        sfx_times.append(e["t"])
        sfx.add(at, fm_bell(1318.5) + .8 * np.pad(fm_bell(1975.5), (int(.07 * SR), 0))[: int(.42 * SR)], .20, .15)
        if e["type"] == "buy":
            n = int(.14 * SR); t = np.arange(n) / SR
            sfx.add(at, sine(600 * (1400 / 600) ** (t / .14), n) * np.exp(-t * 14), .22, -.15)
            sfx.add(at - .06, whoosh(.18, 500, 3000), .10)
        elif e["type"] == "sell":
            for k, fq in enumerate((1318.5, 1760.0, 2637.0)):
                sfx.add(at + .05 + k * .05, fm_bell(fq, .7, 2.0, 1.2, 6), .12, (k - 1) * .4)
            sfx.add(at + .1, coin_grains(9), .07, .1)
            for k in range(10):
                sfx.add(at + .14 + k * .055, fm_bell(3200 + 60 * k, .03, 1, .2, 80), .05)
        else:
            n = int(.3 * SR); t = np.arange(n) / SR
            sfx.add(at, sine(80, n) * np.exp(-t * 12), .45)
            sfx.add(at, sine(620 * (200 / 620) ** (t / .3), n) * np.exp(-t * 6), .2)
            sfx.add(at + .02, (sine(466.2, n) + sine(440, n)) * np.exp(-t * 9), .04)
    for at, pan in ((2.5, -.5), (9.0, .5), (11.8, 0.0)):
        w = whoosh(.55, 300, 6000)
        sfx.add(at - .25, w, .26, pan)
    for at in (2.65, 9.15):
        n = int(.45 * SR); t = np.arange(n) / SR
        sfx.add(at, sine(900 * (2400 / 900) ** (t / .45), n) * np.sin(np.pi * t / .45) * .5, .12, .5)
    sfx.add(t_drop + .03, fm_bell(2637, 1.2, 2, 1, 3), .14)
    sfx.add(t_end, fm_bell(1760, 1.6, 2, 1, 2.2) + fm_bell(2637, 1.6, 2, 1, 2.5), .14)

    # ---------------- mix
    sc = sidechain_env(N, kicks, depth=.6, release=.2)
    dk = duck_env(N, sfx_times, db=-2.5)
    dL, dR = drums.out(); bL, bR = bass.out(); mL, mR = music.out(); sL, sR = sfx.out()
    dL, dR = compress(dL, dR, -16, 2.5, .08, 1.5)
    dL, dR = hp(dL, 30), hp(dR, 30)
    bL, bR = bL * sc, bR * sc
    bL, bR = saturate(bL, 1.3), saturate(bR, 1.3)
    irs = reverb_ir(2.4, .025)
    mL, mR = hp(mL, 120), hp(mR, 120)
    mL, mR = chorus(mL, .7, 2.0, 7, 0), chorus(mR, .7, 2.0, 7, 1.7)
    mL, mR = pingpong(mL, mR, 3 * BEAT / 4, .3, 4)
    mL, mR = reverb(mL, mR, irs, .38)
    mL, mR = mL * sc * dk, mR * sc * dk
    sL, sR = reverb(sL, sR, irs, .12, 600)
    stems = {"drums": (dL * .9, dR * .9), "bass": (bL * .5, bR * .5), "music": (mL * 2.6, mR * 2.6), "sfx": (sL * 1.1, sR * 1.1)}
    L = sum(v[0] for v in stems.values()); Rr = sum(v[1] for v in stems.values())
    L, Rr = compress(L, Rr, -12, 1.8, .15, 0)
    # 1/16 drop gap: music + drums cut just before the finale SELL so the drop (and its chime) hits
    gate = np.ones(N)
    g0, g1 = int((t_drop - BEAT / 4) * SR), int((t_drop - .004) * SR)
    gate[g0:g1] = np.concatenate([np.linspace(1, .08, int(.03 * SR)), np.full(g1 - g0 - int(.03 * SR), .08)])
    for k in ("drums", "bass", "music"):
        a_, b_ = stems[k]
        stems[k] = (a_ * gate, b_ * gate)
    L = sum(v[0] for v in stems.values()); Rr = sum(v[1] for v in stems.values())
    L, Rr = compress(L, Rr, -12, 1.8, .15, 0)
    fade = np.ones(N); nf = int(.4 * SR); fade[-nf:] = np.linspace(1, 0, nf) ** 1.4
    fade[: int(.008 * SR)] = np.linspace(0, 1, int(.008 * SR))
    return L * fade, Rr * fade, stems, fade


def main():
    R = load_events()
    L, Rr, stems, fade = build(R)
    tgt, tp = CFG["audio"]["target_lufs"], CFG["audio"]["true_peak_dbtp"]
    pre = lufs(L, Rr)
    mL, mR = master(L, Rr, tgt, tp)
    out = os.path.join(ROOT, "output", "soundtrack.wav")
    os.makedirs(os.path.join(ROOT, "output", "stems"), exist_ok=True)
    wavfile.write(out, SR, (np.stack([mL, mR], 1) * 32767).astype(np.int16))
    g = 10 ** ((tgt - pre) / 20)
    for k, (a, b) in stems.items():
        a, b = limiter(a * fade * g, b * fade * g, .95)
        wavfile.write(os.path.join(ROOT, "output", "stems", f"{k}.wav"), SR, (np.stack([a, b], 1) * 32767).astype(np.int16))
    print("wrote", out, f"LUFS {lufs(mL, mR):.2f}  TP {true_peak_db(mL, mR):.2f} dBTP")


if __name__ == "__main__":
    main()
