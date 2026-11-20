"""Loudness (ITU-R BS.1770 via pyloudnorm) and true-peak mastering."""
import numpy as np
import pyloudnorm as pyln
from scipy.signal import resample_poly
from . import SR
from .mix import limiter
from .filters import hp


def lufs(L, R):
    return pyln.Meter(SR).integrated_loudness(np.stack([L, R], 1))


def true_peak_db(L, R):
    up = np.stack([resample_poly(L, 4, 1), resample_poly(R, 4, 1)])
    return 20 * np.log10(np.abs(up).max() + 1e-12)


def master(L, R, target_lufs=-14.0, tp_db=-1.0, margin_db=0.6):
    L, R = hp(L, 25), hp(R, 25)
    ceil = 10 ** ((tp_db - margin_db) / 20)
    for _ in range(6):
        g = 10 ** ((target_lufs - lufs(L, R)) / 20)
        L, R = limiter(L * g, R * g, ceil)
        if abs(lufs(L, R) - target_lufs) < .3:
            break
    # final true-peak guard (inter-sample)
    for _ in range(4):
        tp = true_peak_db(L, R)
        if tp <= tp_db - margin_db + .05:
            break
        ceil *= 10 ** ((tp_db - margin_db - tp) / 20)
        L, R = limiter(L, R, ceil)
    return L, R
