"""Synth SFX for the long-form essay, driven by element sfx tags in cues.json. Synth only, no music."""
import numpy as np
from sfx import SR, slam, bell, whoosh, pluck, tick, hit, riser, powerdown, drone, blip

PENTA = [262, 294, 330, 392, 440, 523]


def build_events(C):
    ev = []
    add = lambda at, snd: ev.append((at, snd))
    S = C['scenes']
    for i, s in enumerate(S):
        if i > 0:
            if s['trans'] == 'wipe':
                add(s['start'] - 0.14, whoosh(0.45, True, 0.42))
            elif s['inv']:
                add(s['start'] - 0.4, powerdown(0.5, 0.34))
                add(s['start'], hit(0.32))
            else:
                add(s['start'] - 0.06, whoosh(0.22, False, 0.12))
        if s['inv']:
            add(s['start'], drone(s['end'] - s['start'], 55, 0.12))
        for e in s['els']:
            tag, t = e.get('sfx'), e['t']
            if not tag:
                continue
            if tag == 'slam':
                add(t - 0.2, riser(0.2, 0.14)); add(t, slam(0.58)); add(t + 0.02, bell(523, 1.8, 0.14))
            elif tag == 'hit':
                add(t, hit(0.3))
            elif tag == 'tick':
                add(t, tick(0.1))
            elif tag.startswith('pluck') and e['k'] == 'txt':
                add(t, pluck(PENTA[int(tag[5:] or 0)] * 2, 0.5, 0.34))
            elif tag == 'pluck':
                add(t, pluck(PENTA[e.get('note', 0)] * 2, 0.5, 0.36))
                for k in range(4):
                    add(t + 0.05 + k * 0.07, tick(0.07))
            elif tag == 'long':
                add(t, riser(min(1.2, e['d']), 0.2))
            elif tag == 'count':
                n = int(e['d'] / 0.07)
                for k in range(n):
                    add(t + k * 0.07 * (1 + k / n), tick(0.08))
                add(t + e['d'] * 0.8, pluck(523, 0.6, 0.3))
            elif tag == 'strike':
                add(t, whoosh(0.25, False, 0.25)); add(t + 0.05, hit(0.25))
            elif tag == 'dots':
                add(t, tick(0.1))
                for st, n in e['steps']:
                    add(st, riser(0.5, 0.16)); add(st + 0.1, pluck(392 if n < 50 else 784, 0.7, 0.3))
            elif tag == 'boxes':
                for k, bt in enumerate(e['t']):
                    add(bt, pluck(PENTA[k] * 2, 0.4, 0.3))
                add(e['merge'] - 0.1, whoosh(0.3, True, 0.3))
            elif tag == 'gap':
                add(t, blip(880, 0.12, 0.2)); add(e['t2'], blip(1760, 0.12, 0.2))
            elif tag == 'gate':
                add(t - 0.1, whoosh(0.6, True, 0.4)); add(t, slam(0.55)); add(t + 0.02, bell(392, 2.2, 0.16))
    return ev


def render_sfx(C):
    n = int(C['dur'] * SR) + SR
    out = np.zeros(n)
    for at, snd in build_events(C):
        i = int(max(0, at) * SR)
        j = min(n, i + len(snd))
        out[i:j] += snd[:j - i]
    return out[:int(C['dur'] * SR)]
