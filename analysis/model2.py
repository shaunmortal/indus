"""Phase 4.2: does any structure beyond sign-bigram exist that a model can exploit? Compare on held-out texts:
 unigram | bigram (abs. discount) | trigram (abs. discount, backoff) | class-trigram interpolated with sign-bigram, K in {8,20,40}.
Train/dev/test = 70/10/20 of the WORK set. Lambdas tuned on dev. Metric: perplexity per token incl. </s>."""
import json, random, collections, math
import numpy as np
random.seed(7); np.random.seed(7)
work=json.load(open('data/holdout/work.json')); texts=[tuple(r['seq']) for r in work if r['seq']]
random.shuffle(texts); n=len(texts); train=texts[:int(.7*n)]; dev=texts[int(.7*n):int(.8*n)]; test=texts[int(.8*n):]
V=sorted({w for t in train for w in t}); idx={w:i for i,w in enumerate(V)}; Vs=set(V)
END='</s>'
def ngrams(ts,k):
    c=collections.defaultdict(collections.Counter)
    for t in ts:
        s=('<s>',)*(k-1)+tuple(w if w in Vs else '<unk>' for w in t)+(END,)
        for i in range(k-1,len(s)): c[s[i-k+1:i]][s[i]]+=1
    return c
uni=collections.Counter(w for t in train for w in t); uni[END]=len(train); uni['<unk>']=1; N=sum(uni.values()); VV=len(uni)
B=ngrams(train,2); T=ngrams(train,3)
def p1(w): return (uni[w]+0.5)/(N+0.5*VV)
def pad(ctx_counts,w,backoff,D=0.75):
    c=ctx_counts; tot=sum(c.values())
    if not tot: return backoff
    return max(c[w]-D,0)/tot + (D*len(c)/tot)*backoff
def p2(p,w): return pad(B[(p,)],w,p1(w))
def p3(pp,p,w): return pad(T[(pp,p)],w,p2(p,w))
def ppl(pf,ts):
    ll=0;m=0
    for t in ts:
        s=('<s>','<s>')+tuple(w if w in Vs else '<unk>' for w in t)+(END,)
        for i in range(2,len(s)): ll+=math.log(pf(s[i-2],s[i-1],s[i])); m+=1
    return math.exp(-ll/m)
print(f"train {len(train)} dev {len(dev)} test {len(test)} | vocab {len(V)}")
print(f"unigram  ppl test={ppl(lambda a,b,w:p1(w),test):.1f}")
print(f"bigram   ppl test={ppl(lambda a,b,w:p2(b,w),test):.1f}")
print(f"trigram  ppl test={ppl(p3,test):.1f}")
# class-based: cluster by left/right neighbour distributions (Brown-style via k-means on bigram rows)
def classes(K):
    M=np.zeros((len(V),2*len(V)+2))
    for (p,),c in B.items():
        if p in idx:
            for w,k in c.items():
                if w in idx: M[idx[p],idx[w]]+=k
    for (p,),c in B.items():
        for w,k in c.items():
            if w in idx and p in idx: M[idx[w],len(V)+idx[p]]+=k
    for i,w in enumerate(V): M[i,-2]=B[('<s>',)][w]; M[i,-1]=B[(w,)][END]
    M=M/(M.sum(1,keepdims=True)+1e-9)
    C=M[np.random.choice(len(V),K,replace=False)].copy(); wts=np.array([uni[w] for w in V],float)
    for _ in range(40):
        a=((M[:,None,:]-C[None,:,:])**2).sum(2).argmin(1)
        for k in range(K):
            if (a==k).any(): C[k]=np.average(M[a==k],axis=0,weights=wts[a==k])
    cl={V[i]:int(a[i]) for i in range(len(V))}; cl['<s>']=K; cl[END]=K+1; cl['<unk>']=K+2
    return cl
for K in [8,20,40]:
    cl=classes(K)
    CT=collections.defaultdict(collections.Counter); CB=collections.defaultdict(collections.Counter); inc=collections.defaultdict(collections.Counter)
    for t in train:
        s=('<s>','<s>')+tuple(w if w in Vs else '<unk>' for w in t)+(END,)
        for i in range(2,len(s)):
            CT[(cl[s[i-2]],cl[s[i-1]])][cl[s[i]]]+=1; CB[(cl[s[i-1]],)][cl[s[i]]]+=1
    for w,c in uni.items(): inc[cl[w]][w]+=c
    def pc(pp,p,w):
        c=cl[w]; pcl=pad(CT[(cl[pp],cl[p])],c,pad(CB[(cl[p],)],c,(sum(inc[c].values())+1)/(N+K+3)))
        pin=(inc[c][w]+0.1)/(sum(inc[c].values())+0.1*len(inc[c]))
        return pcl*pin
    best=None
    for lam in [0.1,0.2,0.3,0.4,0.5,0.6,0.7]:
        f=lambda a,b,w,lam=lam: lam*pc(a,b,w)+(1-lam)*p3(a,b,w)
        d=ppl(f,dev)
        if best is None or d<best[0]: best=(d,lam,f)
    print(f"class-trigram K={K:2} alone ppl test={ppl(pc,test):.1f} | interpolated with trigram (lam={best[1]}) ppl test={ppl(best[2],test):.1f}")
