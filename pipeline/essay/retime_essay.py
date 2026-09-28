import json, subprocess, re, numpy as np
SR=48000
raw=subprocess.run(['ffmpeg','-v','error','-i','vo_raw.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
a=np.frombuffer(raw,np.float32).astype(np.float64)
log=subprocess.run(['ffmpeg','-i','vo_raw.mp3','-af','silencedetect=n=-40dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
L=json.load(open('lines_raw.json'))
SECTION_STARTS={'First, think about what it used to take.','So are people actually using this?','But here is where it gets wild.','Now, let\'s be honest.'}
BEATS={'Artificial intelligence.','The gate is gone.','What are YOU going to build?','remember the numbers.'}
def cap(s,e):
    mid=(s+e)/2
    for i in range(1,len(L)):
        if L[i-1]['e']-0.15<=mid<=L[i]['s']+0.15:
            if L[i]['text'] in SECTION_STARTS: return 1.1
            if L[i]['text'] in BEATS: return 0.85
            return 0.6
    return 0.32
cuts=[]
for s,e in zip(st,en):
    c=cap(s,e)
    if e-s>c: cuts.append((s+c/2,e-c/2))
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
for l in L:
    l['s']=round(m(l['s']),3); l['e']=round(m(l['e']),3)
    for x in l['words']: x['s']=round(m(x['s']),3); x['e']=round(m(x['e']),3)
json.dump(L,open('lines.json','w'))
print('new length', len(v)/SR, 'removed', sum(e-s for s,e in cuts), 'cuts', len(cuts))
