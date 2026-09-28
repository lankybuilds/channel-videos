"""Synth sound effects for the AI Music Surge short. Everything generated from scratch."""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(7)


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.003, r=None, curve=4.0):
    """attack then exponential release across n samples"""
    x = np.ones(n)
    na = max(1, int(a * SR))
    x[:na] = np.linspace(0, 1, na)
    rel = np.linspace(0, 1, n - na)
    x[na:] = np.exp(-curve * rel) * (1 - rel) ** 0.5
    return x


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype='band', fs=SR, output='sos'), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype='low', fs=SR, output='sos'), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype='high', fs=SR, output='sos'), x)


def sweep(f0, f1, d, shape='exp'):
    t = tt(d)
    if shape == 'exp':
        f = f0 * (f1 / f0) ** (t / d)
    else:
        f = f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def noise(d):
    return rng.standard_normal(int(d * SR))


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


# ---------------- instruments ----------------
def slam(big=1.0):
    d = 1.1
    t = tt(d)
    sub = sweep(140, 38, d) * np.exp(-t * 4.5)
    click = hp(noise(d), 2500) * np.exp(-t * 60) * 0.5
    body = lp(noise(d), 900) * np.exp(-t * 14) * 0.9
    x = np.tanh(2.2 * (sub * 1.2 + body + click))
    return norm(x, 0.95 * big)


def bell(f=880, d=2.2, level=0.35):
    t = tt(d)
    x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3)
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6))
    return norm(x * np.exp(-t * 2.2), level)


def whoosh(d=0.45, up=True, level=0.5):
    n = noise(d)
    t = tt(d)
    shape = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    lo, hi = (250, 6000) if up else (6000, 250)
    fc = lo * (hi / lo) ** (t / d)                 # swept one-pole low-pass
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    out = np.empty_like(n)
    y = 0.0
    for i in range(len(n)):
        y += a[i] * (n[i] - y)
        out[i] = y
    out = hp(out, 150)
    return norm(out * shape, level)


def pluck(f, d=0.5, level=0.5):
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.35 + np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    x = lp(x, 3500) * np.exp(-t * 9)
    x[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    return norm(x, level)


def tick(level=0.18):
    d = 0.03
    t = tt(d)
    return norm(hp(noise(d), 3000) * np.exp(-t * 250), level)


def key_click(level=0.13):
    d = 0.05
    t = tt(d)
    x = bp(noise(d), 1800, 6000) * np.exp(-t * 180) + 0.4 * np.sin(2 * np.pi * 180 * t) * np.exp(-t * 90)
    return norm(x, level * rng.uniform(0.75, 1.0))


def blip(f=1760, d=0.12, level=0.3):
    t = tt(d)
    return norm(np.sin(2 * np.pi * f * t) * np.exp(-t * 35), level)


def beep(f=1000, d=0.14, level=0.22):
    t = tt(d)
    e = np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.02)
    return norm(np.sin(2 * np.pi * f * t) * e, level)


def flat_tone(d=2.2, f=1000, level=0.2):
    t = tt(d)
    e = np.minimum(1, t / 0.01) * np.clip((d - t) / 0.9, 0, 1)
    return norm(np.sin(2 * np.pi * f * t) * e, level)


def riser(d=1.2, level=0.35):
    t = tt(d)
    x = sweep(180, 1400, d) * 0.5 + bp(noise(d), 800, 6000) * 0.5
    return norm(x * (t / d) ** 2.2, level)


def stab(f=220, d=0.7, level=0.45):
    t = tt(d)
    x = sum(np.sign(np.sin(2 * np.pi * f * r * t + p)) for r, p in [(1, 0), (1.5, .3), (2, .7), (1.005, 1)])
    x = lp(x, 2200) * np.exp(-t * 5)
    x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return norm(x, level)


def powerdown(d=0.9, level=0.5):
    t = tt(d)
    x = sweep(900, 40, d) * 0.8 + lp(noise(d), 600) * 0.2
    return norm(np.tanh(1.5 * x) * (1 - t / d) ** 1.5, level)


def drone(d=5.0, f=55, level=0.16):
    t = tt(d)
    x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t + 0.4)
         + 0.3 * np.sin(2 * np.pi * (f * 2.01) * t))
    x = x * (0.8 + 0.2 * np.sin(2 * np.pi * 0.7 * t))
    e = np.minimum(1, t / 0.6) * np.clip((d - t) / 0.8, 0, 1)
    return norm(x * e, level)


def letdown(level=0.35):
    """two-note falling synth for 'almost nobody is listening'"""
    a = stab(196, 0.45, 1.0)
    b = stab(147, 0.9, 1.0)
    out = np.zeros(int(1.4 * SR))
    out[:len(a)] += a
    o = int(0.32 * SR)
    out[o:o + len(b)] += b
    return norm(lp(out, 1500), level)


def hit(level=0.5):
    d = 0.5
    t = tt(d)
    x = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 12) + lp(noise(d), 2000) * np.exp(-t * 30) * 0.6
    return norm(np.tanh(2 * x), level)


def pad_pulse(d=1.0, level=0.18):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * f * t) for f in (220, 277.2, 329.6, 440))
    x *= 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 3 * t))
    e = np.minimum(1, t / 0.05) * np.clip((d - t) / 0.3, 0, 1)
    return norm(lp(x, 2500) * e, level)


# ---------------- timeline ----------------
PENTA = [262, 294, 330, 392, 440, 523]


def build_events(C):
    ev = []
    add = lambda at, snd: ev.append((at, snd))
    # scene 1: live waveform pad, then flatline beep, slam on HALF
    add(0.0, pad_pulse(max(0.3, C['slam'] - 0.25)))
    add(max(0.0, C['slam'] - 0.4), flat_tone(1.3, 1000, 0.12))
    add(C['slam'] - 0.25, riser(0.25, 0.2))
    add(C['slam'], slam(0.6))
    add(C['slam'] + 0.02, bell(660, 2.0, 0.22))
    add(C['sub'], whoosh(0.35, True, 0.22))
    # transition 1: wipe
    add(C['cut1'] - 0.12, whoosh(0.45, True, 0.45))
    # scene 2: ascending plucks per bar + tick counter, final bar stab
    for i, b in enumerate(C['bars']):
        if i < 5:
            add(b, pluck(PENTA[i] * 2, 0.5, 0.42))
            for k in range(4):
                add(b + 0.05 + k * 0.07, tick(0.1))
        else:
            add(b - 0.8, riser(0.8, 0.3))
            add(b, stab(262, 0.9, 0.5))
            add(b, hit(0.45))
    add(C['nine'], hit(0.4))
    add(C['nine'] + 0.02, bell(1046, 1.8, 0.2))
    # transition 2: power-down into the inverted scene + drone underneath
    add(C['cut2'] - 0.35, powerdown(0.5, 0.38))
    add(C['cut2'], hit(0.35))
    add(C['cut2'], drone(C['cut3'] - C['cut2'], 55, 0.13))
    add(C['big'], slam(0.55))
    add(C['big'] + 0.02, bell(523, 2.2, 0.2))
    add(C['small'], blip(1760, 0.12, 0.3))
    add(C['nobody'], letdown(0.3))
    # transition 3: cut back to black
    add(C['cut3'] - 0.1, whoosh(0.3, False, 0.35))
    # scene 4: heart monitor beeps on each R-peak, typing clicks, flatline
    k = 0
    while True:
        at = C['cut3'] + k * C['beat'] + 0.32
        if at >= C['flat']:
            break
        add(at, beep(1000, 0.12, 0.16))
        k += 1
    for (a0, a1), n in ((C['type1'], 12), (C['type2'], 27)):
        for i in range(n):
            add(a0 + (a1 - a0) * i / n, key_click(0.1))
    add(C['flat'], flat_tone(min(2.4, C['ask'] - C['flat'] + 1.2), 1000, 0.16))
    add(C['ask'], pluck(523, 0.8, 0.3))
    add(C['ask'] + 0.12, pluck(784, 0.8, 0.22))
    return ev


def render_sfx(C):
    n = int(C['dur'] * SR) + SR
    out = np.zeros(n)
    for at, s in build_events(C):
        i = int(max(0, at) * SR)
        j = min(n, i + len(s))
        out[i:j] += s[:j - i]
    return out[:int(C['dur'] * SR)]
