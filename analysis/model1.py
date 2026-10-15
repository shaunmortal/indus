"""Phase 4.1-4.2: our own structure model, no sounds, no dictionary.
Data: WORK set only (data/holdout/work.json; the sealed hold-out is never opened). Internal split 80/20 by text.
1. Sign profile = [position distribution (first/mid/last/sole), length-normalised position, left-neighbour class dist, right-neighbour class dist] built iteratively.
2. K-means into K function classes (unsupervised).
3. Models for masked-sign prediction on held-out 20%: unigram; sign bigram (Kneser-Ney-lite); class-bigram + within-class unigram (our slot grammar). Metric: top-1 accuracy and perplexity.
"""
import json, random, collections, math
import numpy as np
random.seed(42); np.random.seed(42)
work=json.load(open('data/holdout/work.json'))
texts=[tuple(r['seq']) for r in work if r['seq']]
random.shuffle(texts); cut=int(len(texts)*0.8); train=texts[:cut]; test=texts[cut:]
print("work texts:",len(texts)," train",len(train)," test",len(test))
V=sorted({w for t in train for w in t}); idx={w:i for i,w in enumerate(V)}
# ---- 1. profiles ----
def profiles(train,cls=None,K=None):
    n=len(V); P=np.zeros((n,4)); L=np.zeros((n,1)); Lc=np.zeros((n,K if cls is not None else n)); Rc=np.zeros((n,K if cls is not None else n))
    for t in train:
        m=len(t)
        for i,w in enumerate(t):
            a=idx[w]
            P[a,0 if m==1 else 1 if i==0 else 3 if i==m-1 else 2]+=1
            L[a,0]+= (i/(m-1)) if m>1 else 0.5
            if i>0: Lc[a, cls[idx[t[i-1]]] if cls is not None else idx[t[i-1]]]+=1
            if i<m-1: Rc[a, cls[idx[t[i+1]]] if cls is not None else idx[t[i+1]]]+=1
    cnt=P.sum(1,keepdims=True)+1e-9
    P=P/cnt; L=L/cnt; Lc=Lc/(Lc.sum(1,keepdims=True)+1e-9); Rc=Rc/(Rc.sum(1,keepdims=True)+1e-9)
    return np.hstack([P*3,L*2,Lc,Rc]), cnt.ravel()
def kmeans(X,K,w,iters=50):
    C=X[np.random.choice(len(X),K,replace=False)].copy()
    for _ in range(iters):
        d=((X[:,None,:]-C[None,:,:])**2).sum(2); a=d.argmin(1)
        for k in range(K):
            if (a==k).any(): C[k]=np.average(X[a==k],axis=0,weights=w[a==k])
    return a
K=12
X,cnt=profiles(train); a=kmeans(X,K,cnt)
for it in range(3):   # refine with class-neighbour features
    X,cnt=profiles(train,cls=a,K=K); a=kmeans(X,K,cnt)
# ---- 2. report classes ----
bridge={int(k):v['M'][0] for k,v in json.load(open('data/bridge_WM.json')).items() if v['M']}
print("\nfunction classes (K=%d): top signs by frequency, with position profile"%K)
for k in range(K):
    members=sorted([(cnt[i],V[i]) for i in range(len(V)) if a[i]==k],reverse=True)
    tot=sum(c for c,_ in members)
    pp=np.average(X[a==k][:, :4]/3,axis=0,weights=cnt[a==k])
    print(f"  class {k:2}: {len(members):3} signs, {int(tot):5} tokens | sole/first/mid/last = {pp[0]:.2f}/{pp[1]:.2f}/{pp[2]:.2f}/{pp[3]:.2f} | "+", ".join(f"W{w}(M{bridge.get(w,'?')})" for _,w in members[:6]))
# ---- 3. prediction on held-out 20% ----
cls={V[i]:int(a[i]) for i in range(len(V))}
uni=collections.Counter(w for t in train for w in t); N=sum(uni.values())
big=collections.defaultdict(collections.Counter)
for t in train:
    for p,w in zip(('<s>',)+t,t+('</s>',)): big[p][w]+=1
cbig=collections.defaultdict(collections.Counter)   # class bigram
for t in train:
    cs=('<s>',)+tuple(cls[w] for w in t)+('</s>',)
    for p,w in zip(cs,cs[1:]): cbig[p][w]+=1
inclass=collections.defaultdict(collections.Counter)
for w,c in uni.items(): inclass[cls[w]][w]+=c
def p_uni(w): return (uni[w]+0.5)/(N+0.5*len(V))
def p_big(p,w,lam=0.6):
    d=big[p]; return lam*((d[w])/(sum(d.values())) if d else 0)+(1-lam)*p_uni(w)
def p_cls(p,w,lam=0.6):
    pc=cls.get(p,'<s>') if p!='<s>' else '<s>'; c=cls[w]
    d=cbig[pc]; pcls=(d[c]+0.1)/(sum(d.values())+0.1*(K+1))
    pin=(inclass[c][w]+0.1)/(sum(inclass[c].values())+0.1*len(inclass[c]))
    return lam*pcls*pin+(1-lam)*p_uni(w)
def evaluate(pf,name):
    ll=0; n=0; top=0
    for t in test:
        prev='<s>'
        for w in t:
            if w not in idx: prev=w; continue
            probs={v:pf(prev,v) for v in V}; z=sum(probs.values())
            ll+=math.log(probs[w]/z); n+=1
            if max(probs,key=probs.get)==w: top+=1
            prev=w
    print(f"  {name:28} perplexity={math.exp(-ll/n):7.1f}  top1={top/n:.1%}  (n={n})")
print("\nheld-out next-sign prediction (20% of work set):")
evaluate(lambda p,w:p_uni(w),"unigram baseline")
evaluate(p_big,"sign bigram")
evaluate(p_cls,"class bigram x in-class (ours)")
evaluate(lambda p,w:0.5*p_big(p,w)+0.5*p_cls(p,w),"mixture bigram+class")
json.dump({str(V[i]):int(a[i]) for i in range(len(V))},open('data/model1_classes.json','w'),indent=0)
