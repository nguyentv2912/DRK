"""Reverb (synthetic-IR convolution), ping-pong delay, chorus, saturation."""
import numpy as np
from scipy.signal import fftconvolve, resample_poly
from . import SR
from .filters import lp, hp


def reverb_ir(seconds=2.2, predelay=.02, rng=None, bright=6500, dark=1800):
    rng = rng or np.random.RandomState(3)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    irs = []
    for ch in range(2):
        nz = rng.randn(n)
        a, b = lp(nz, bright), lp(nz, dark)
        k = np.clip(t / seconds * 1.6, 0, 1)  # high frequencies die first
        ir = (a * (1 - k) + b * k) * np.exp(-t * 6.9 / seconds)
        ir[: int(.004 * SR)] *= np.linspace(0, 1, int(.004 * SR))
        ir = np.concatenate([np.zeros(int(predelay * SR) + ch * 37), ir])
        irs.append(ir / np.sqrt((ir ** 2).sum()))
    return irs


def reverb(L, R, irs, wet=.25, hp_f=250):
    wl = fftconvolve(hp(L, hp_f), irs[0])[: len(L)]
    wr = fftconvolve(hp(R, hp_f), irs[1])[: len(R)]
    return L + wl * wet, R + wr * wet


def pingpong(L, R, delay_s, fb=.42, n=6, tone=4500):
    d = int(delay_s * SR)
    outL, outR = L.copy(), R.copy()
    src = lp((L + R) / 2, tone)
    g = 1.0
    for k in range(1, n + 1):
        g *= fb
        sh = np.zeros_like(src); sh[d * k:] = src[: len(src) - d * k] * g
        (outL if k % 2 else outR)[:] += sh
    return outL, outR


def chorus(x, rate=.8, depth_ms=2.2, base_ms=7.0, phase=0.0):
    n = len(x)
    t = np.arange(n)
    d = (base_ms + depth_ms * np.sin(2 * np.pi * rate * t / SR + phase)) * SR / 1000
    return .7 * x + .3 * np.interp(t - d, t, x, left=0)


def saturate(x, drive=1.6):
    up = resample_poly(x, 2, 1)
    up = np.tanh(up * drive) / np.tanh(drive)
    return resample_poly(up, 1, 2)[: len(x)]
