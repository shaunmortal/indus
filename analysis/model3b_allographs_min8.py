"""M3: allograph detection. For every pair of Mahadevan signs:
  image similarity  = cosine of downsampled, centred, binarised drawings (plus horizontally flipped variant, max)
  distribution sim  = cosine of (left-neighbour + right-neighbour + position) profiles on IM77 distinct texts
Report: pairs with HIGH image sim and HIGH distribution sim (allograph candidates: merging is safe)
        pairs with HIGH image sim and LOW distribution sim (look-alikes that behave differently: keep separate)
Baselines: distribution of both sims over all pairs; permutation of sign labels for the distribution sim."""
import csv, json, collections, math, itertools, random
import numpy as np
from PIL import Image
random.seed(3)
B='/Users/Happy/Desktop/plugins/indus'
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); seqs=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); seqs.append([int(t) for t in k.split()])
tok=collections.Counter(t for s in seqs for t in s if t)
signs=[m for m in range(1,418) if tok[m]>=8]
idx={m:i for i,m in enumerate(signs)}
# distribution profiles
D=np.zeros((len(signs),2*len(signs)+4))
for s in seqs:
    m=len(s)
    for i,t in enumerate(s):
        if t not in idx: continue
        a=idx[t]; D[a,2*len(signs)+(0 if m==1 else 1 if i==0 else 3 if i==m-1 else 2)]+=1
        if i>0 and s[i-1] in idx: D[a,idx[s[i-1]]]+=1
        if i<m-1 and s[i+1] in idx: D[a,len(signs)+idx[s[i+1]]]+=1
D=D/(np.linalg.norm(D,axis=1,keepdims=True)+1e-9); DS=D@D.T
# image features
def feat(m):
    im=Image.open(f'{B}/data/raw/signs_im77/{m}.png').convert('RGBA'); bg=Image.new('RGBA',im.size,'white'); bg.paste(im,mask=im)
    g=np.array(bg.convert('L'),dtype=float); ink=(g<128)
    ys,xs=np.where(ink)
    if len(xs)==0: return np.zeros(32*32)
    crop=ink[ys.min():ys.max()+1, xs.min():xs.max()+1]
    pil=Image.fromarray((crop*255).astype(np.uint8)).resize((32,32),Image.BILINEAR)
    v=np.array(pil,dtype=float).ravel(); return v/(np.linalg.norm(v)+1e-9)
F=np.array([feat(m) for m in signs]); Ff=np.array([feat(m).reshape(32,32)[:,::-1].ravel() for m in signs])
IS=np.maximum(F@F.T, F@Ff.T)
pairs=[(IS[i,j],DS[i,j],signs[i],signs[j]) for i,j in itertools.combinations(range(len(signs)),2)]
isv=np.array([p[0] for p in pairs]); dsv=np.array([p[1] for p in pairs])
print(f"signs with >=8 tokens: {len(signs)}; pairs: {len(pairs)}")
print(f"image sim: median {np.median(isv):.2f}, 95th pct {np.percentile(isv,95):.2f}, 99th {np.percentile(isv,99):.2f}")
print(f"distrib sim: median {np.median(dsv):.2f}, 95th {np.percentile(dsv,95):.2f}, 99th {np.percentile(dsv,99):.2f}")
# correlation between image and distribution similarity (do look-alikes behave alike?)
r=np.corrcoef(isv,dsv)[0,1]
null=[]
for _ in range(200):
    perm=np.random.permutation(len(signs)); null.append(np.corrcoef(isv,np.array([DS[perm[i],perm[j]] for i,j in itertools.combinations(range(len(signs)),2)]))[0,1])
print(f"corr(image sim, distribution sim) = {r:.3f}; permutation null mean {np.mean(null):.3f} sd {np.std(null):.3f}")
hi_i=np.percentile(isv,98); hi_d=np.percentile(dsv,95); lo_d=np.percentile(dsv,50)
A=[p for p in pairs if p[0]>=hi_i and p[1]>=hi_d]; L=[p for p in pairs if p[0]>=hi_i and p[1]<=lo_d]
print(f"\nALLOGRAPH CANDIDATES (image >= {hi_i:.2f} AND distribution >= {hi_d:.2f}): {len(A)}")
for i_,d_,a,b in sorted(A,reverse=True)[:20]: print(f"  M{a:>3} ~ M{b:>3}  image {i_:.2f} dist {d_:.2f}  tokens {tok[a]}/{tok[b]}")
print(f"\nLOOK-ALIKES THAT BEHAVE DIFFERENTLY (image >= {hi_i:.2f} AND distribution <= {lo_d:.2f}): {len(L)}")
for i_,d_,a,b in sorted(L,reverse=True)[:20]: print(f"  M{a:>3} vs M{b:>3}  image {i_:.2f} dist {d_:.2f}  tokens {tok[a]}/{tok[b]}")
json.dump({'allograph_candidates':[(a,b,round(float(i_),3),round(float(d_),3)) for i_,d_,a,b in A],'lookalikes_distinct':[(a,b,round(float(i_),3),round(float(d_),3)) for i_,d_,a,b in L]},open(f'{B}/data/model3b_allographs_min8.json','w'),indent=0)

# ---- sanity: within-sign rank. For a pair (a,b), where does DS[a,b] rank among all DS[a,*] and DS[b,*]? True allographs should be each other's top-few neighbours.
def rank_of(a,b):
    i,j=idx[a],idx[b]; ra=int((DS[i]>DS[i,j]).sum()); rb=int((DS[j]>DS[i,j]).sum()); return ra,rb
print("\nmutual-neighbour rank check (0 = nearest neighbour):")
for i_,d_,a,b in sorted(A,reverse=True)[:15]:
    ra,rb=rank_of(a,b); print(f"  M{a:>3} ~ M{b:>3}: rank in a's list {ra:3}, in b's list {rb:3}  {'MUTUAL-TOP3' if ra<=3 and rb<=3 else ''}")
print("look-alike distinct pairs, same check (expect large ranks):")
for i_,d_,a,b in sorted(L,reverse=True)[:8]:
    ra,rb=rank_of(a,b); print(f"  M{a:>3} vs M{b:>3}: ranks {ra:3} / {rb:3}")
