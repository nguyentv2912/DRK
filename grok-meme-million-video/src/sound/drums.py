"""Layered drums."""
import numpy as np
from . import SR
from .filters import hp, bp, lp, exp_env
from .osc import sine


def kick(rng):
    n = int(.5 * SR); t = np.arange(n) / SR
    sub = sine(50, n) * np.exp(-t * 5.0)
    f = 55 + 70 * np.exp(-t * 32)
    body = sine(f, n) * np.exp(-t * 9)
    click = hp(rng.randn(n), 2500) * np.exp(-t * 260) * .5
    k = .55 * sub + .9 * body + click
    return np.tanh(k * 1.4) / np.tanh(1.4)


def snare(rng):
    n = int(.32 * SR); t = np.arange(n) / SR
    tone = sine(190 * (1 + .25 * np.exp(-t * 40)), n) * np.exp(-t * 22) * .5
    noise = bp(rng.randn(n), 1200, 9000) * np.exp(-t * 16)
    clap = np.zeros(n)
    for d in (0, .009, .018, .027):
        i = int(d * SR); e = np.exp(-np.arange(n - i) / SR * 60)
        clap[i:] += bp(rng.randn(n - i), 900, 3500) * e * .6
    return tone + .7 * noise + clap


def hat(rng, open_=False, vel=1.0):
    n = int((.32 if open_ else .05) * SR); t = np.arange(n) / SR
    x = hp(rng.randn(n), 7500)
    return x * np.exp(-t * (9 if open_ else 75)) * vel


def ride(rng):
    n = int(.9 * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for f in (3150, 4620, 5310, 6870, 8120, 9440):
        x += np.sign(np.sin(2 * np.pi * f * t + rng.random() * 6))
    return hp(x, 5000) * np.exp(-t * 4.5) * .12
