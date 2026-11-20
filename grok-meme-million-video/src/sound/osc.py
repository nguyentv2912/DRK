"""Band-limited oscillators (PolyBLEP) and a 7-voice stereo supersaw."""
import numpy as np
from . import SR


def _phase(freq, n, ph0=0.0):
    f = np.broadcast_to(np.asarray(freq, float), (n,))
    return (ph0 + np.cumsum(f) / SR) % 1.0, f / SR


def _blep(t, dt):
    y = np.zeros_like(t)
    m = t < dt
    x = t[m] / dt[m]
    y[m] = x + x - x * x - 1
    m2 = t > 1 - dt
    x = (t[m2] - 1) / dt[m2]
    y[m2] = x * x + x + x + 1
    return y


def saw(freq, n, ph0=0.0):
    t, dt = _phase(freq, n, ph0)
    return 2 * t - 1 - _blep(t, dt)


def square(freq, n, ph0=0.0, pw=0.5):
    t, dt = _phase(freq, n, ph0)
    t2 = (t + (1 - pw)) % 1.0
    return (2 * t - 1 - _blep(t, dt)) - (2 * t2 - 1 - _blep(t2, dt))


def sine(freq, n, ph0=0.0):
    t, _ = _phase(freq, n, ph0)
    return np.sin(2 * np.pi * t)


def supersaw(freq, n, rng, voices=7, cents=18.0, spread=1.0):
    """Stereo supersaw: detuned voices, random phases, voices panned across the field."""
    L = np.zeros(n); R = np.zeros(n)
    det = np.linspace(-cents, cents, voices)
    for k, c in enumerate(det):
        v = saw(np.asarray(freq) * 2 ** (c / 1200), n, rng.random())
        pan = spread * (k / (voices - 1) * 2 - 1)
        g = 1.0 if c == 0 else 0.62
        L += v * g * np.cos((pan + 1) * np.pi / 4)
        R += v * g * np.sin((pan + 1) * np.pi / 4)
    return L / voices * 1.6, R / voices * 1.6
