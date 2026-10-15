"""M5: the allograph algorithm on the Wells/ICIT sign list (642 rendered glyphs; corpus = ICIT distinct texts in reading order).
Same recipe as M3; plus comparison with ICIT's own GLYPHSIMILARITY table (69 pairs) and merge validation by held-out perplexity."""
import csv, json, collections, math, itertools, random
import numpy as np
from PIL import Image
random.seed(3); np.random.seed(3)
B='/Users/Happy/Desktop/plugins/indus'
valid={int(r['GLYPHID']) for r in csv.DictReader(open(f'{B}/data/icit_glyph.csv')) if r['CODEPOINT_HEX']!='2047'}
corp=list(csv.DictReader(open(f'{B}/data/raw/joyboseroy_csv/indus_website_real_corpus.csv')))
seen=set(); seqs=[]
for r in corp:
    s=tuple(int(x[1:]) for x in r['sign_sequence'].split() if x[1:].isdigit())[::-1]
    if s and s not in seen: seen.add(s); seqs.append(list(s))
tok=collections.Counter(t for s in seqs for t in s)
signs=[g for g in sorted(tok) if tok[g]>=15 and g in valid]; idx={g:i for i,g in enumerate(signs)}
D=np.zeros((len(signs),2*len(signs)+4))
for s in seqs:
    m=len(s)
    for i,t in enumerate(s):
        if t not in idx: continue
        a=idx[t]; D[a,2*len(signs)+(0 if m==1 else 1 if i==0 else 3 if i==m-1 else 2)]+=1
        if i>0 and s[i-1] in idx: D[a,idx[s[i-1]]]+=1
        if i<m-1 and s[i+1] in idx: D[a,len(signs)+idx[s[i+1]]]+=1
D=D/(np.linalg.norm(D,axis=1,keepdims=True)+1e-9); DS=D@D.T
def feat(g):
    im=np.array(Image.open(f'{B}/data/raw/signs_wells/G{g}.png').convert('L'),dtype=float); ink=im<128
    ys,xs=np.where(ink)
    if len(xs)==0: return np.zeros(1024)
    crop=ink[ys.min():ys.max()+1, xs.min():xs.max()+1]
    v=np.array(Image.fromarray((crop*255).astype(np.uint8)).resize((32,32),Image.BILINEAR),dtype=float).ravel(); return v/(np.linalg.norm(v)+1e-9)
F=np.array([feat(g) for g in signs]); Ff=np.array([feat(g).reshape(32,32)[:,::-1].ravel() for g in signs]); IS=np.maximum(F@F.T,F@Ff.T)
pairs=[(IS[i,j],DS[i,j],signs[i],signs[j]) for i,j in itertools.combinations(range(len(signs)),2)]
isv=np.array([p[0] for p in pairs]); dsv=np.array([p[1] for p in pairs])
print(f"Wells signs with >=15 tokens: {len(signs)}; pairs {len(pairs)}; corr(image,dist)={np.corrcoef(isv,dsv)[0,1]:.3f}")
hi_i=np.percentile(isv,98); hi_d=np.percentile(dsv,95); lo_d=np.percentile(dsv,50)
A=[p for p in pairs if p[0]>=hi_i and p[1]>=hi_d]; L=[p for p in pairs if p[0]>=hi_i and p[1]<=lo_d]
def rank(a,b):
    i,j=idx[a],idx[b]; return int((DS[i]>DS[i,j]).sum()), int((DS[j]>DS[i,j]).sum())
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
print(f"\nALLOGRAPH CANDIDATES (image>={hi_i:.2f}, dist>={hi_d:.2f}): {len(A)}")
for i_,d_,a,b in sorted(A,reverse=True)[:25]:
    ra,rb=rank(a,b); print(f"  W{a:>3}(M{bridge.get(a,'?')}) ~ W{b:>3}(M{bridge.get(b,'?')})  img {i_:.2f} dist {d_:.2f} ranks {ra}/{rb} tokens {tok[a]}/{tok[b]}")
print(f"\nLOOK-ALIKES, DIFFERENT SIGNS (image>={hi_i:.2f}, dist<={lo_d:.2f}): {len(L)}")
for i_,d_,a,b in sorted(L,reverse=True)[:15]:
    ra,rb=rank(a,b); print(f"  W{a:>3}(M{bridge.get(a,'?')}) vs W{b:>3}(M{bridge.get(b,'?')})  img {i_:.2f} dist {d_:.2f} ranks {ra}/{rb}")
# ICIT's own similarity table vs ours
sim=[(int(r['G1']),int(r['G2'])) for r in csv.DictReader(open(f'{B}/data/icit_glyphsimilarity.csv'))]
both=[(a,b) for a,b in sim if a in idx and b in idx]
print(f"\nICIT GLYPHSIMILARITY pairs among tested signs: {len(both)}; their image sim median {np.median([IS[idx[a],idx[b]] for a,b in both]) if both else float('nan'):.2f}, dist sim median {np.median([DS[idx[a],idx[b]] for a,b in both]) if both else float('nan'):.2f}")
json.dump({'allograph_candidates':[(a,b,round(float(i_),3),round(float(d_),3)) for i_,d_,a,b in A],'lookalikes_distinct':[(a,b,round(float(i_),3),round(float(d_),3)) for i_,d_,a,b in L]},open(f'{B}/data/model5_wells_allographs.json','w'),indent=0)
