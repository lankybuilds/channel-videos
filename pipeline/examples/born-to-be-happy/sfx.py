"""Music + sound effects for 'Born to be happy?'. All synthesized in code."""
import numpy as np
from sfx_lib import (SR, tt, noise, norm, lp, hp, bp, sweep, slam, bell, whoosh, pluck, tick,
                     riser, hit, powerdown, blip)

rng = np.random.default_rng(3)
A_MIN = [110.0, 130.81, 164.81]            # A minor (tense first half)
F_MAJ = [87.31, 130.81, 174.61, 220.0]     # F major
C_MAJ = [130.81, 164.81, 196.0, 261.63]    # C major
G_MAJ = [98.0, 146.83, 196.0, 246.94]


def fade(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e


def pad(freqs, d, level, bright=2500, a=0.4, r=0.8):
    t = tt(d)
    x = np.zeros_like(t)
    for f in freqs:
        for det in (-0.25, 0.0, 0.3):             # detuned saw-ish stack
            ph = 2 * np.pi * (f + det) * t + rng.uniform(0, 6)
            x += np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    x = lp(x, bright)
    return norm(x * fade(len(t), a, r), level)


def heartbeat_pulse(d, bpm, level, f=48):
    """low 'lub-dub' sub pulse"""
    n = int(d * SR)
    out = np.zeros(n)
    beat = 60 / bpm
    k = 0
    while k * beat < d:
        for off, amp in ((0.0, 1.0), (0.22, 0.6)):
            i = int((k * beat + off) * SR)
            s = tt(0.35)
            thump = np.sin(2 * np.pi * f * s * (1 + 0.6 * np.exp(-s * 30))) * np.exp(-s * 14) * amp
            j = min(n, i + len(thump))
            if i < n: out[i:j] += thump[:j - i]
        k += 1
    return norm(out, level)


def drone_high(d, level):
    t = tt(d)
    x = np.sin(2 * np.pi * 880 * t) * 0.5 + np.sin(2 * np.pi * 1318.5 * t) * 0.3
    return norm(x * (0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * t)) * fade(len(t), 0.8, 1.0), level)


def bass_drop(level=0.9):
    d = 1.6
    t = tt(d)
    sub = sweep(90, 30, d) * np.exp(-t * 2.4)
    body = lp(noise(d), 300) * np.exp(-t * 9) * 0.6
    click = hp(noise(d), 3000) * np.exp(-t * 80) * 0.4
    return norm(np.tanh(2.5 * (sub + body + click)), level)


def thud(level=0.5, f=70):
    d = 0.5
    t = tt(d)
    x = np.sin(2 * np.pi * f * t * (1 + np.exp(-t * 40))) * np.exp(-t * 11) + lp(noise(d), 1200) * np.exp(-t * 40) * 0.5
    return norm(np.tanh(2 * x), level)


def shimmer(d, level):
    t = tt(d)
    x = np.zeros_like(t)
    for f in (1046.5, 1318.5, 1568.0, 2093.0):
        x += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * (0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(2, 5) * t))
    return norm(x * fade(len(t), 1.2, 1.5), level)


def arp(start, d, notes, step, level):
    out = []
    k = 0
    while k * step < d:
        out.append((start + k * step, pluck(notes[k % len(notes)], 0.4, level)))
        k += 1
    return out


def build_events(C):
    ev = []
    add = lambda at, s: ev.append((at, s))
    D = C['dur']
    # ---------- MUSIC ----------
    # tense first half: low heartbeat pulse + dark pad, until the 51 million lands
    tense_end = C['mil'] + 0.3
    add(0.0, heartbeat_pulse(tense_end, 76, 0.55))
    add(0.0, pad(A_MIN, tense_end + 0.6, 0.22, 1400, a=0.05, r=0.9))
    # saddest moment: almost silence, one faint high tone
    add(C['mil'] + 0.4, drone_high(C['cut4'] - C['mil'] - 0.3, 0.035))
    # the turn: music kicks back stronger (major, faster pulse)
    b = C['cut4']
    add(b, heartbeat_pulse(C['cut7'] - b, 100, 0.5, f=55))
    add(b, pad(F_MAJ, C['cut5'] - b + 0.8, 0.26, 2200, a=0.02, r=0.8))
    add(C['cut5'], pad(C_MAJ, C['cut6'] - C['cut5'] + 0.8, 0.28, 2800, a=0.3, r=0.8))
    add(C['cut6'], pad(G_MAJ, C['cut7'] - C['cut6'] + 0.2, 0.3, 3200, a=0.3, r=0.25))
    ev += arp(C['cut5'] + 0.2, C['cut7'] - C['cut5'] - 0.4, [523.25, 659.25, 783.99, 659.25], 0.3, 0.12)
    # split-second silence, then hope pad and the final swell to the peak
    add(C['hope'], pad(F_MAJ, C['final'] - C['hope'] + 0.6, 0.24, 2400, a=0.4, r=0.6))
    add(C['final'] - 1.0, riser(1.0, 0.22))
    add(C['final'], pad([130.81, 196.0, 261.63, 329.63, 392.0], D - C['final'], 0.42, 4200, a=0.25, r=1.8))
    add(C['final'], shimmer(D - C['final'], 0.12))
    # ---------- SFX ----------
    for i in range(6):                                   # counter ticks
        add(C['cnt2'] + i * (C['half'] - C['cnt2']) / 6, tick(0.12))
    add(C['cut2'] - 0.1, whoosh(0.35, True, 0.3))
    add(C['half'], bass_drop(0.42))                      # HIT 1
    add(C['cut3'] - 0.1, whoosh(0.35, False, 0.25))
    for i in range(8):
        add(C['cnt3'] + i * (C['mil'] - C['cnt3']) / 8, tick(0.12))
    add(C['mil'], bass_drop(0.45))                        # HIT 2
    add(C['gray'], bell(220, 2.4, 0.12))
    add(C['cut4'] - 0.35, riser(0.35, 0.25))
    add(C['cut4'], bass_drop(0.48))                       # HIT 3 (white flip)
    add(C['cut4'], hit(0.5))
    add(C['brain'], whoosh(0.5, True, 0.18))
    for i in range(6):
        add(C['change'] + i * 0.16, blip(1320 + 180 * i, 0.1, 0.12))
    add(C['cut5'] - 0.1, whoosh(0.3, False, 0.3))
    for i in range(7):
        add(C['cnt5'] + i * (C['pct70'] - C['cnt5']) / 7, tick(0.12))
    add(C['pct70'], bass_drop(0.42))                     # HIT 4
    add(C['pct90'], hit(0.35))
    add(C['fill'], bell(880, 2.6, 0.16))
    add(C['proven'], thud(0.6, 60))
    for k, key in enumerate(('ag1', 'ag2', 'ag3')):
        add(C[key], thud(0.32 + 0.04 * k, 80 + 10 * k))
    add(C['final'], bass_drop(0.5))                      # biggest impact
    add(C['final'] + 0.02, bell(523.25, 3.5, 0.2))
    return ev


def render_sfx(C):
    n = int(C['dur'] * SR) + SR
    out = np.zeros(n)
    for at, s in build_events(C):
        i = int(max(0, at) * SR)
        j = min(n, i + len(s))
        if i < n: out[i:j] += s[:j - i]
    return out[:int(C['dur'] * SR)]
