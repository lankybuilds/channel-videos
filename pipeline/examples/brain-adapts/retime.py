import json, subprocess, re, numpy as np
SR=48000
raw=subprocess.run(['ffmpeg','-v','error','-i','vo_raw.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
a=np.frombuffer(raw,np.float32).astype(np.float64)
log=subprocess.run(['ffmpeg','-i','vo_raw.mp3','-af','silencedetect=n=-40dB:d=0.2','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
# target pause length per gap (by where it starts)
def cap(s):
    if 2.1<s<2.2: return 0.4      # after "anything" (hook lands)
    if 7.7<s<7.8: return 0.42     # cut to Braille
    if 11.9<s<12.0: return 0.42   # cut to cabbies
    if 17.0<s<17.1: return 0.5    # power-down into the inverted scene
    if 19.7<s<19.9: return 0.6    # dramatic beat before "But"
    if 23.1<s<23.2: return 0.45   # into the closer
    return 0.28
cuts=[]
for s,e in zip(st,en):
    c=cap(s)
    if e-s>c:
        cuts.append((s+c/2, e-c/2))
out=[];prev=0;f=int(0.004*SR)
for s,e in cuts:
    seg=a[int(prev*SR):int(s*SR)].copy(); seg[-f:]*=np.linspace(1,0,f)
    if out: seg[:f]*=np.linspace(0,1,f)
    out.append(seg); prev=e
seg=a[int(prev*SR):].copy(); seg[:f]*=np.linspace(0,1,f); out.append(seg)
v=np.concatenate(out)
v.astype(np.float32).tofile('vo.f32')
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','vo.f32','-c:a','libmp3lame','-b:a','192k','vo.mp3'],check=True)
def m(t):
    sh=0
    for s,e in cuts:
        if t>=e: sh+=e-s
        elif t>s: return s-sh
    return t-sh
w=json.load(open('words.json'))
for x in w: x['w']=re.sub(r'\(\d\)','',x['w'])
for x in w: x['s']=round(m(x['s']),3); x['e']=round(m(x['e']),3)
json.dump(w,open('words_rt.json','w'))
print('new length', len(v)/SR, 'removed', sum(e-s for s,e in cuts))
