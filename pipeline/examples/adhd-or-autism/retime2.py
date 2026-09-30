"""Trim pauses in the take, then speed it up slightly (pitch kept) so the video lands near 60 s."""
import json, subprocess, re, sys, numpy as np
SR = 48000
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
raw = subprocess.run(['ffmpeg','-v','error','-i','vo_raw.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
a = np.frombuffer(raw, np.float32).astype(np.float64)
log = subprocess.run(['ffmpeg','-i','vo_raw.mp3','-af','silencedetect=n=-40dB:d=0.2','-f','null','-'],capture_output=True,text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
SCENE = [9.0, 18.9, 29.85, 43.28, 55.15, 65.88]   # gaps before a new scene
def cap(s):
    if 67.8 < s < 68.0: return 0.75                # the beat before "You DON'T"
    if any(abs(s - x) < 0.1 for x in SCENE): return 0.42
    if 68.9 < s < 69.9: return 0.4                 # let "You don't" land
    return 0.26
cuts = []
for s, e in zip(st, en):
    c = cap(s)
    if e - s > c: cuts.append((s + c / 2, e - c / 2))
out = []; prev = 0; f = int(0.004 * SR)
for s, e in cuts:
    seg = a[int(prev*SR):int(s*SR)].copy(); seg[-f:] *= np.linspace(1, 0, f)
    if out: seg[:f] *= np.linspace(0, 1, f)
    out.append(seg); prev = e
seg = a[int(prev*SR):].copy(); seg[:f] *= np.linspace(0, 1, f); out.append(seg)
v = np.concatenate(out)
v.astype(np.float32).tofile('vo_trim.f32')
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','vo_trim.f32',
                '-af', f'atempo={TEMPO}', '-c:a','libmp3lame','-b:a','192k','vo.mp3'], check=True)
def m(t):
    sh = 0
    for s, e in cuts:
        if t >= e: sh += e - s
        elif t > s: return (s - sh) / TEMPO
    return (t - sh) / TEMPO
w = json.load(open('words.json'))
for x in w: x['w'] = re.sub(r'\(\d\)', '', x['w']); x['s'] = round(m(x['s']), 3); x['e'] = round(m(x['e']), 3)
json.dump(w, open('words_rt.json', 'w'))
print('trimmed', round(len(v)/SR, 2), 'final', round(len(v)/SR/TEMPO, 2), 'removed', round(sum(e-s for s, e in cuts), 2))
