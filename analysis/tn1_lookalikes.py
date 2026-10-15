"""Image similarity: 42 TN base signs vs Mahadevan signs with >=15 tokens (same features as M3: centred crop, 32x32, flip-invariant cosine)."""
import json, csv, collections, glob, os
import numpy as np
from PIL import Image
B='/Users/Happy/Desktop/plugins/indus'
def feat(path):
    im=Image.open(path).convert('RGBA'); bg=Image.new('RGBA',im.size,'white'); bg.paste(im,mask=im)
    g=np.array(bg.convert('L'),dtype=float); ink=g<128; ys,xs=np.where(ink)
    if len(xs)==0: return None
    crop=ink[ys.min():ys.max()+1, xs.min():xs.max()+1]
    v=np.array(Image.fromarray((crop*255).astype(np.uint8)).resize((32,32),Image.BILINEAR),dtype=float).ravel(); return v/(np.linalg.norm(v)+1e-9)
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
tok=collections.Counter(int(t) for r in rows for t in r['signs_clean'].split() if t!='0')
M=[m for m in range(1,418) if tok[m]>=15]
FM=np.array([feat(f'{B}/data/raw/signs_im77/{m}.png') for m in M]); FMf=np.array([f.reshape(32,32)[:,::-1].ravel() for f in FM])
tn={}
for p in sorted(glob.glob(f'{B}/data/raw/tngraffiti/bv-signs/base*_int*.png')):
    g=int(os.path.basename(p).split('_')[0][4:]); f=feat(p)
    if f is not None: tn[g]=f
T=sorted(tn); FT=np.array([tn[g] for g in T])
S=np.maximum(FT@FM.T, FT@FMf.T)
# M3 background: image-sim distribution among Indus pairs had median 0.33, 95th pct 0.60, 99th 0.77
best={}
print("TN base sign -> best Indus look-alikes (image cosine); M3 scale: median 0.33, top-5% 0.60, top-1% 0.77")
for i,g in enumerate(T):
    idx=np.argsort(-S[i])[:3]; best[g]=[(int(M[j]),round(float(S[i,j]),2)) for j in idx]
    print(f"  TN{g:>2}: "+", ".join(f"M{m}({s})" for m,s in best[g]))
strong=sum(1 for g in T if best[g][0][1]>=0.60); very=sum(1 for g in T if best[g][0][1]>=0.77)
print(f"\nTN signs with an Indus look-alike >=0.60: {strong}/42; >=0.77: {very}/42")
json.dump({str(g):best[g] for g in T},open(f'{B}/data/tn_lookalikes.json','w'),indent=0)
