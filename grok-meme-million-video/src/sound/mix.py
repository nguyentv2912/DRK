"""Buses, sidechain, compressor, look-ahead limiter."""
import numpy as np
from scipy.ndimage import minimum_filter1d, uniform_filter1d
from scipy.signal import lfilter
from . import SR


class Bus:
    def __init__(self, n):
        self.L = np.zeros(n + SR * 3); self.R = np.zeros(n + SR * 3); self.n = n

    def add(self, at, x, gain=1.0, pan=0.0):
        i = int(round(at * SR))
        if i >= self.n or i < -len(x):
            return
        if i < 0:
            x = x[-i:]; i = 0
        x = x[: len(self.L) - i] * gain
        self.L[i:i + len(x)] += x * np.cos((pan + 1) * np.pi / 4) * 1.4142
        self.R[i:i + len(x)] += x * np.sin((pan + 1) * np.pi / 4) * 1.4142

    def add2(self, at, L, R, gain=1.0):
        i = int(round(at * SR))
        if i >= self.n:
            return
        m = min(len(L), len(self.L) - i)
        self.L[i:i + m] += L[:m] * gain; self.R[i:i + m] += R[:m] * gain

    def out(self):
        return self.L[: self.n], self.R[: self.n]


def sidechain_env(n, hits, depth=.7, release=.18):
    env = np.ones(n)
    k = np.arange(int(release * 2.2 * SR)) / SR
    shape = 1 - depth * np.exp(-k / (release / 3)) * np.clip(k / .004, 0, 1) - depth * (k < .004)
    shape = np.clip(shape, 1 - depth, 1)
    for h in hits:
        i = int(h * SR)
        m = min(len(shape), n - i)
        if m > 0:
            env[i:i + m] = np.minimum(env[i:i + m], shape[:m])
    return env


def duck_env(n, times, db=-2.5, hold=.15, attack=.01, release=.12):
    env = np.ones(n); g = 10 ** (db / 20)
    for t in times:
        a, h, r = int((t - attack) * SR), int((t + hold) * SR), int((t + hold + release) * SR)
        a = max(a, 0)
        if a >= n:
            continue
        env[a:min(h, n)] = np.minimum(env[a:min(h, n)], g)
        if h < n:
            m = min(r, n) - h
            env[h:h + m] = np.minimum(env[h:h + m], np.linspace(g, 1, m))
    return uniform_filter1d(env, int(.004 * SR))


def compress(L, R, thr_db=-18, ratio=2.0, release=.12, makeup_db=0.0):
    lev = np.maximum(np.abs(L), np.abs(R))
    a = np.exp(-1 / (release * SR))
    env = lfilter([1 - a], [1, -a], lev)
    env_db = 20 * np.log10(env + 1e-9)
    over = np.maximum(0, env_db - thr_db)
    g = 10 ** ((-over * (1 - 1 / ratio) + makeup_db) / 20)
    return L * g, R * g


def limiter(L, R, ceiling, look=.005):
    n = int(look * SR)
    pk = np.maximum(np.abs(L), np.abs(R))
    need = np.minimum(1.0, ceiling / (pk + 1e-12))
    g = minimum_filter1d(need, 2 * n + 1)
    g = uniform_filter1d(g, n * 2 + 1)
    g = np.minimum(g, minimum_filter1d(need, 2 * n + 1))
    return L * g, R * g
