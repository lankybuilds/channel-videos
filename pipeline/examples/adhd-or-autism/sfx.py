"""Sound effects for 'ADHD or autism? The only way to know'. All synthesized in code, no music (owner's call)."""
# sfx_lib is a copy of pipeline/sfx.py (the shared synth helpers).
import numpy as np
from sfx_lib import SR, tt, noise, norm, lp, hp, bp, sweep, slam, bell, whoosh, pluck, tick, riser, hit, blip

rng = np.random.default_rng(11)


def bass_drop(level=0.9, d=1.6):
    t = tt(d)
    sub = sweep(90, 30, d) * np.exp(-t * 2.4)
    body = lp(noise(d), 300) * np.exp(-t * 9) * 0.6
    click = hp(noise(d), 3000) * np.exp(-t * 80) * 0.4
    return norm(np.tanh(2.5 * (sub + body + click)), level)


def deep_impact(level=0.5):
    """slow, heavy hit for the statistics scene: long sub tail, no click"""
    d = 2.6
    t = tt(d)
    sub = sweep(62, 28, d) * np.exp(-t * 1.3)
    body = lp(noise(d), 180) * np.exp(-t * 5) * 0.5
    return norm(np.tanh(1.8 * (sub + body)), level)


def glitch_burst(d=0.18, level=0.25):
    """bit-crushed digital static"""
    t = tt(d)
    x = noise(d)
    hold = 24
    x = np.repeat(x[::hold], hold)[:len(t)]
    x = np.round(x * 3) / 3
    gate = (np.sin(2 * np.pi * 38 * t) > -0.2).astype(float)
    return norm(bp(x, 400, 7000) * gate * np.exp(-t * 10), level)


def shatter(level=0.35):
    d = 0.9
    t = tt(d)
    x = hp(noise(d), 3500) * np.exp(-t * 7)
    for _ in range(14):                                  # glassy tinkles
        f = rng.uniform(2500, 6500)
        o = int(rng.uniform(0, 0.45) * SR)
        s = tt(0.25)
        g = np.sin(2 * np.pi * f * s) * np.exp(-s * 30) * rng.uniform(0.3, 0.8)
        x[o:o + len(g)] += g[:len(x) - o]
    return norm(x, level)


def scroll_flutter(d, level=0.05):
    """soft rapid clicks while the feed scrolls"""
    out = np.zeros(int(d * SR))
    k = 0.0
    while k < d - 0.05:
        c = tick(1.0)
        i = int(k * SR)
        out[i:i + len(c)] += c[:len(out) - i]
        k += 0.075
    return norm(out, level)


def build_events(C):
    ev = []
    add = lambda at, s: ev.append((max(0.0, at), s))
    # ---------- SCENE 1: hook, in motion from frame one ----------
    add(0.0, glitch_burst(0.22, 0.3))
    add(0.0, hit(0.4))
    add(C['s1b'], hit(0.3))
    add(C['s1b'], glitch_burst(0.1, 0.15))
    add(C['s1c'], slam(0.5))
    add(C['s1d'], blip(1320, 0.14, 0.1))
    # ---------- SCENE 2: the myth ----------
    add(C['cut2'] - 0.12, whoosh(0.35, True, 0.28))
    add(C['cut2'], glitch_burst(0.14, 0.18))
    add(C['m1'], tick(0.14))
    add(C['ne1'], bass_drop(0.55))                         # stamp 1
    add(C['ne1'], slam(0.35))
    add(C['m2'], tick(0.14))
    add(C['ne2'], bass_drop(0.58))                         # stamp 2
    add(C['ne2'], slam(0.35))
    add(C['m3'], blip(990, 0.12, 0.08))
    # ---------- SCENE 3: the problem ----------
    add(C['cut3'] - 0.12, whoosh(0.35, False, 0.28))
    add(C['cut3'], glitch_burst(0.14, 0.18))
    add(C['cut3'] + 0.1, scroll_flutter(C['cut4'] - C['cut3'] - 0.3, 0.05))
    n = 10
    for i in range(n):                                     # count up to 52
        add(C['c52'] + i * (C['p52'] - C['c52']) / n, tick(0.13))
    add(C['p52'], bass_drop(0.6))                          # 52% hit
    for i in range(6):
        add(C['c27'] + i * (C['p27'] - C['c27']) / 6, tick(0.11))
    add(C['p27'], hit(0.42))
    # ---------- SCENE 4: ADHD reality ----------
    add(C['cut4'] - 0.12, whoosh(0.35, True, 0.28))
    add(C['cut4'], glitch_burst(0.14, 0.18))
    add(C['cut4'] + 0.35, pluck(880, 0.3, 0.12))           # "SQUIRREL!" pop
    add(C['slash4'] - 0.05, whoosh(0.25, True, 0.35))
    add(C['slash4'] + 0.16, shatter(0.32))
    add(C['slash4'] + 0.16, hit(0.35))
    for i, k in enumerate(('a1', 'a2', 'a3', 'a4')):
        add(C[k], pluck([392, 440, 523, 587][i], 0.35, 0.12))
    # ---------- SCENE 5: autism reality ----------
    add(C['cut5'] - 0.12, whoosh(0.35, False, 0.28))
    add(C['cut5'], glitch_burst(0.14, 0.18))
    add(C['slash5'] - 0.05, whoosh(0.25, True, 0.35))
    add(C['slash5'] + 0.16, shatter(0.32))
    add(C['slash5'] + 0.16, hit(0.35))
    for i, k in enumerate(('b1', 'b2', 'b3', 'b4')):
        add(C[k], pluck([392, 440, 523, 587][i], 0.35, 0.12))
    # ---------- SCENE 6: the weight (almost silent, slow deep impacts) ----------
    add(C['cut6'], deep_impact(0.3))
    for c, p in (('c42', 'p42'), ('c37', 'p37'), ('c79', 'p79')):
        m = 5
        for i in range(m):
            add(C[c] + i * (C[p] - C[c]) / m, tick(0.06))
        add(C[p], deep_impact(0.5))
    # ---------- SCENE 7: the answer ----------
    add(C['cut7'] - 0.1, whoosh(0.3, False, 0.2))
    add(C['dont'] - 0.45, riser(0.45, 0.28))
    add(C['dont'], bass_drop(0.62, 2.2))                   # biggest impact
    add(C['dont'], slam(0.5))
    add(C['dont'], glitch_burst(0.2, 0.3))
    add(C['n1'], tick(0.14))
    add(C['pro'], hit(0.45))
    add(C['fin'], bell(523.25, 3.0, 0.16))
    return ev


def render_sfx(C):
    n = int(C['dur'] * SR) + SR * 3
    out = np.zeros(n)
    for at, s in build_events(C):
        i = int(at * SR)
        j = min(n, i + len(s))
        if i < n:
            out[i:j] += s[:j - i]
    return out[:int(C['dur'] * SR)]
