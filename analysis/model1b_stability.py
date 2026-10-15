"""Stability-selected number of function classes. For K in {3,4,5,6,8,12}: 20 runs with different random 80% subsamples of the
work set (Wells v3 list) and seeds; stability = mean pairwise Adjusted Rand Index between runs over frequent signs (>=20 tokens).
Then report the classes at the most stable K, from a consensus (co-association) clustering."""
import json, random, collections, itertools
import numpy as np
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
work=json.load(open(f'{B}/data/holdout/work.json'))
texts=[tuple(Wm.get(w,w) for w in r['seq']) for r in work if r['seq']]
allV=collections.Counter(w for t in texts for w in t); FREQ=[w for w,c in allV.items() if c>=20]; fi={w:i for i,w in enumerate(FREQ)}
def profiles(train,V,idx,cls=None,K=None):
    n=len(V); P=np.zeros((n,4)); L=np.zeros((n,1)); d=K if cls is not None else n; Lc=np.zeros((n,d)); Rc=np.zeros((n,d))
    for t in train:
        m=len(t)
        for i,w in enumerate(t):
            if w not in idx: continue
            a=idx[w]; P[a,0 if m==1 else 1 if i==0 else 3 if i==m-1 else 2]+=1; L[a,0]+=(i/(m-1)) if m>1 else 0.5
            if i>0 and t[i-1] in idx: Lc[a, cls[idx[t[i-1]]] if cls is not None else idx[t[i-1]]]+=1
            if i<m-1 and t[i+1] in idx: Rc[a, cls[idx[t[i+1]]] if cls is not None else idx[t[i+1]]]+=1
    cnt=P.sum(1,keepdims=True)+1e-9
    return np.hstack([P/cnt*3,L/cnt*2,Lc/(Lc.sum(1,keepdims=True)+1e-9),Rc/(Rc.sum(1,keepdims=True)+1e-9)]), cnt.ravel()
def kmeans(X,K,w,rng,iters=50):
    C=X[rng.choice(len(X),K,replace=False)].copy()
    for _ in range(iters):
        a=((X[:,None,:]-C[None,:,:])**2).sum(2).argmin(1)
        for k in range(K):
            if (a==k).any(): C[k]=np.average(X[a==k],axis=0,weights=w[a==k])
    return a
def run(K,seed):
    rng=np.random.default_rng(seed); r=random.Random(seed); sub=r.sample(texts,int(.8*len(texts)))
    X,cnt=profiles(sub,FREQ,fi); a=kmeans(X,K,cnt,rng)
    for _ in range(3): X,cnt=profiles(sub,FREQ,fi,cls=a,K=K); a=kmeans(X,K,cnt,rng)
    return a
def ari(a,b):
    n=len(a); from collections import Counter
    def comb2(x): return x*(x-1)/2
    ct=Counter(zip(a,b)); A=Counter(a); Bc=Counter(b)
    s=sum(comb2(v) for v in ct.values()); sa=sum(comb2(v) for v in A.values()); sb=sum(comb2(v) for v in Bc.values()); N=comb2(n)
    exp=sa*sb/N; mx=(sa+sb)/2
    return (s-exp)/(mx-exp) if mx!=exp else 1.0
print(f"frequent signs: {len(FREQ)}")
best=None; runs_by_K={}
for K in [3,4,5,6,8,12]:
    runs=[run(K,s) for s in range(20)]; runs_by_K[K]=runs
    aris=[ari(runs[i],runs[j]) for i,j in itertools.combinations(range(20),2)]
    m=float(np.mean(aris)); print(f"K={K:2}: mean pairwise ARI {m:.3f} (sd {np.std(aris):.3f})")
    if best is None or m>best[1]: best=(K,m)
K=best[0]; print(f"\nmost stable K = {K}")
# consensus: co-association matrix -> agglomerative-ish via kmeans on co-association rows
runs=runs_by_K[K]; n=len(FREQ); CO=np.zeros((n,n))
for a in runs: CO+= (a[:,None]==a[None,:])
CO/=len(runs); rng=np.random.default_rng(0); cnt=np.array([allV[w] for w in FREQ],float)
cons=kmeans(CO,K,cnt,rng)
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
X,_=profiles(texts,FREQ,fi)
print("consensus classes:")
out={}
for k in range(K):
    mem=sorted([(allV[FREQ[i]],FREQ[i]) for i in range(n) if cons[i]==k],reverse=True); pp=np.average(X[cons==k][:,:4]/3,axis=0,weights=cnt[cons==k])
    print(f"  class {k}: {len(mem)} signs, {int(sum(c for c,_ in mem))} tokens | sole/first/mid/last {pp[0]:.2f}/{pp[1]:.2f}/{pp[2]:.2f}/{pp[3]:.2f} | "+", ".join(f"W{w}(M{bridge.get(w,'?')})" for _,w in mem[:10]))
    out[k]=[w for _,w in mem]
json.dump({'K':K,'classes':out},open(f'{B}/data/model1b_consensus_classes.json','w'))
