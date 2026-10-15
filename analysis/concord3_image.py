"""Bridge growth by image + distribution: for each frequent Wells sign without a Mahadevan match, rank the 418 Mahadevan
drawings by glyph similarity (32x32 ink, flip-invariant) and by context similarity (neighbour distributions, Wells side
mapped to M codes through the existing bridge). Calibrate both scores on the 153 known bridge pairs; accept a candidate
only if it is the top image match, its scores sit inside the known-pair range (>= 25th percentile on both) and the
runner-up image score is clearly lower. Writes data/bridge_new_candidates_v2.json (for Ayush/Claude to eyeball)."""
import json, csv, collections, numpy as np
from PIL import Image
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
def featM(m):
    im=Image.open(f'{B}/data/raw/signs_im77/{m}.png').convert('RGBA'); bg=Image.new('RGBA',im.size,'white'); bg.paste(im,mask=im)
    return _f(np.array(bg.convert('L'),dtype=float)<128)
def featW(g): return _f(np.array(Image.open(f'{B}/data/raw/signs_wells/G{g}.png').convert('L'),dtype=float)<128)
def _f(ink):
    ys,xs=np.where(ink)
    if len(xs)==0: return np.zeros(1024)
    crop=ink[ys.min():ys.max()+1, xs.min():xs.max()+1]
    v=np.array(Image.fromarray((crop*255).astype(np.uint8)).resize((32,32),Image.BILINEAR),dtype=float).ravel(); return v/(np.linalg.norm(v)+1e-9)
import os
Ms=sorted(int(f[:-4]) for f in os.listdir(f'{B}/data/raw/signs_im77') if f.endswith('.png'))
FM=np.array([featM(m) for m in Ms]); FMf=np.array([featM(m).reshape(32,32)[:,::-1].ravel() for m in Ms])
def imsim(g):
    v=featW(g); return np.maximum(FM@v, FMf@v)
# contexts
W=[[Wm.get(int(x[1:]),int(x[1:])) for x in r['sign_sequence'].split()] for r in csv.DictReader(open(f'{B}/data/raw/joyboseroy_csv/indus_website_real_corpus.csv'))]
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
M=[[int(t) for t in r['signs_clean'].split() if t!='0'] for r in rows if r['signs_clean'].strip() not in ('','0')]
def ctx(seqs,mapf):
    C=collections.defaultdict(collections.Counter)
    for s in seqs:
        for i,g in enumerate(s):
            C[g][('L',mapf(s[i-1]) if i>0 else 'B')]+=1; C[g][('R',mapf(s[i+1]) if i<len(s)-1 else 'E')]+=1
    return C
CW=ctx(W,lambda w:bridge.get(w,'?')); CM=ctx(M,lambda m:m)
def cos(a,b):
    d=sum(a[k]*b[k] for k in a); return d/(np.sqrt(sum(v*v for v in a.values())*sum(v*v for v in b.values()))+1e-9)
freqW=collections.Counter(g for s in W for g in s)
# calibration on known pairs
known=[(w,m) for w,m in bridge.items() if os.path.exists(f'{B}/data/raw/signs_wells/G{w}.png') and m in Ms and freqW[w]>=10]
ki=[float(imsim(w)[Ms.index(m)]) for w,m in known]; kd=[cos(CW[w],CM[m]) for w,m in known]
ti,td=np.percentile(ki,25),np.percentile(kd,25)
print(f'known pairs {len(known)}: image sim median {np.median(ki):.2f} (25th {ti:.2f}); dist sim median {np.median(kd):.2f} (25th {td:.2f})')
out=[]
for w,n in freqW.most_common():
    if w in bridge or w==0 or n<10 or not os.path.exists(f'{B}/data/raw/signs_wells/G{w}.png'): continue
    s=imsim(w); order=np.argsort(-s)[:3]
    cands=[(Ms[i],round(float(s[i]),3),round(cos(CW[w],CM[Ms[i]]),3)) for i in order]
    top=cands[0]; accept= top[1]>=ti and top[2]>=td and (top[1]-cands[1][1])>=0.03
    out.append(dict(W=w,tokens=n,candidates=cands,accept=bool(accept)))
    print(f'W{w:>4} n={n:>3}  '+'  '.join(f'M{m}(img {i} dist {d})' for m,i,d in cands)+('   <-- ACCEPT' if accept else ''))
json.dump(dict(calibration=dict(known_pairs=len(known),image_25th=float(ti),dist_25th=float(td)),candidates=out),open(f'{B}/data/bridge_new_candidates_v2.json','w'),indent=1)
print('accepted',sum(o['accept'] for o in out),'of',len(out))
