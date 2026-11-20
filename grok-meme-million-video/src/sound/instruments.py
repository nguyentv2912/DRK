"""Bass, pad, pluck, lead, stab."""
import numpy as np
from . import SR
from .osc import saw, sine, supersaw, square
from .filters import tv_lp, adsr, lp, exp_env


def note(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def sub(m, dur):
    n = int(dur * SR)
    return sine(note(m), n) * adsr(n, .004, .05, .9, .03)


def reese(m, dur, t0=0.0):
    n = int(dur * SR); f = note(m)
    x = saw(f * 2 ** (-9 / 1200), n) + saw(f * 2 ** (9 / 1200), n, .37)
    tt = t0 + np.arange(n) / SR
    cut = 420 + 380 * (0.5 + 0.5 * np.sin(2 * np.pi * tt / (60 / 128)))  # 1/4-note LFO
    return tv_lp(x * .5, cut, q=1.4) * adsr(n, .006, .1, .85, .04)


def pad(chord, dur, rng, cutoff=1800):
    n = int(dur * SR)
    L = np.zeros(n); R = np.zeros(n)
    for m in chord:
        l, r = supersaw(note(m), n, rng, voices=7, cents=14, spread=1.0)
        L += l; R += r
    env = adsr(n, .25, .4, .85, .35)
    return tv_lp(L, cutoff, .7) * env * .22, tv_lp(R, cutoff, .7) * env * .22


def pluck(m, dur, cut_peak=4200):
    n = int(dur * SR)
    x = saw(note(m), n) * .6 + square(note(m) * 2, n) * .2
    env_f = 300 + cut_peak * exp_env(n, 18)
    return tv_lp(x, env_f, 1.6) * adsr(n, .002, .12, .25, .08)


def lead(m, dur, rng, bright=1.0):
    n = int(dur * SR)
    L, R = supersaw(note(m), n, rng, voices=7, cents=16, spread=.7)
    env_f = 900 + 5200 * bright * (.35 + .65 * exp_env(n, 7))
    e = adsr(n, .006, .15, .7, .06)
    return tv_lp(L, env_f, 1.1) * e, tv_lp(R, env_f, 1.1) * e


def stab(chord, dur, rng):
    n = int(dur * SR)
    L = np.zeros(n); R = np.zeros(n)
    for m in chord:
        l, r = supersaw(note(m), n, rng, voices=5, cents=20)
        L += l; R += r
    f = 400 + 6000 * exp_env(n, 14)
    e = adsr(n, .002, .18, .0, .05)
    return tv_lp(L, f, 1.2) * e * .3, tv_lp(R, f, 1.2) * e * .3
