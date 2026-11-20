"""Static and time-varying filters, envelopes."""
import numpy as np
from scipy.signal import butter, sosfilt, lfilter
from . import SR


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR / 2 - 200) / (SR / 2), "low", output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f / (SR / 2), "high", output="sos"), x)


def bp(x, f1, f2, order=2):
    return sosfilt(butter(order, [f1 / (SR / 2), min(f2, SR / 2 - 200) / (SR / 2)], "band", output="sos"), x)


def _rbj_lp(fc, q):
    w0 = 2 * np.pi * min(max(fc, 20), SR / 2 - 500) / SR
    al = np.sin(w0) / (2 * q)
    cw = np.cos(w0)
    b = np.array([(1 - cw) / 2, 1 - cw, (1 - cw) / 2])
    a = np.array([1 + al, -2 * cw, 1 - al])
    return b / a[0], a / a[0]


def tv_lp(x, cutoff, q=0.9, block=128):
    """Resonant low-pass whose cutoff follows an envelope (block-wise, state carried)."""
    cutoff = np.broadcast_to(np.asarray(cutoff, float), x.shape)
    y = np.empty_like(x)
    zi = np.zeros(2)
    for i in range(0, len(x), block):
        b, a = _rbj_lp(float(cutoff[i]), q)
        y[i:i + block], zi = lfilter(b, a, x[i:i + block], zi=zi)
    return y


def peak_eq(x, f, gain_db, q=1.0):
    A = 10 ** (gain_db / 40); w0 = 2 * np.pi * f / SR; al = np.sin(w0) / (2 * q); cw = np.cos(w0)
    b = np.array([1 + al * A, -2 * cw, 1 - al * A]); a = np.array([1 + al / A, -2 * cw, 1 - al / A])
    return lfilter(b / a[0], a / a[0], x)


def adsr(n, a=.005, d=.1, s=.7, r=.1):
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    ns = max(0, n - na - nd - nr)
    env = np.concatenate([np.linspace(0, 1, max(na, 1)), np.linspace(1, s, max(nd, 1)), np.full(ns, s), np.linspace(s, 0, max(nr, 1))])
    return np.pad(env, (0, max(0, n - len(env))))[:n]


def exp_env(n, rate):
    return np.exp(-np.arange(n) / SR * rate)
