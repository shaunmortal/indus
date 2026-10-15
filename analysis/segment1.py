"""Phase 4.3: unsupervised segmentation of texts into multi-sign UNITS, validated by prediction.
Method: on the TRAIN split (IM77 distinct texts, sign list v3), compute PMI and count for adjacent pairs; iteratively merge the
pair with highest (count>=min_count, PMI>=thr) into a unit token (BPE-like on bigrams with PMI gate). After each round of merges
evaluate held-out bits-per-SIGN (so segmentations are comparable). Keep merging while held-out bits-per-sign improves.
Output: the learned unit lexicon (fixed compounds / 'words') and how much they help."""
import csv, json, collections, math, random
MERGE={int(k):v for k,v in json.load(open('data/model4_merges_v3.json')).items()}
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); base=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); base.append(tuple(MERGE.get(int(t),int(t)) for t in k.split() if t!='0'))
base=[s for s in base if s]
random.seed(42); random.shuffle(base); cut=int(.8*len(base)); train=base[:cut]; test=base[cut:]
def apply(seqs,units):
    # greedy left-to-right longest-match of unit tuples (max len 4)
    out=[]
    for s in seqs:
        i=0; t=[]
        while i<len(s):
            m=None
            for L in (4,3,2):
                if i+L<=len(s) and s[i:i+L] in units: m=L; break
            if m: t.append(s[i:i+m]); i+=m
            else: t.append((s[i],)); i+=1
        out.append(tuple(t))
    return out
def bits_per_sign(tr,te):
    U=collections.Counter(w for s in tr for w in s); U['</s>']=len(tr); N=sum(U.values()); V=len(U)+1
    B=collections.defaultdict(collections.Counter)
    for s in tr:
        for p,w in zip(('<s>',)+s,s+('</s>',)): B[p][w]+=1
    p1=lambda w:(U[w]+0.5)/(N+0.5*V)
    def p2(p,w,D=0.75):
        c=B[p]; t=sum(c.values()); return p1(w) if not t else max(c[w]-D,0)/t+(D*len(c)/t)*p1(w)
    ll=0; nsign=0
    for s in te:
        for p,w in zip(('<s>',)+s,s+('</s>',)): ll+=math.log2(p2(p,w))
        nsign+=sum(len(u) for u in s)+1
    return -ll/nsign
units=set(); tr=apply(train,units); te=apply(test,units); best=bits_per_sign(tr,te); print(f"baseline bits/sign (sign bigram): {best:.3f}")
lex=[]
for rnd in range(40):
    tr=apply(train,units)
    uni=collections.Counter(u for s in tr for u in s); big=collections.Counter((a,b) for s in tr for a,b in zip(s,s[1:])); N=sum(uni.values())
    cands=[]
    for (a,b),c in big.items():
        if c<8 or len(a)+len(b)>4: continue
        pmi=math.log2(c*N/(uni[a]*uni[b])); cands.append((pmi*math.log(c),pmi,c,a,b))
    cands.sort(reverse=True)
    improved=False
    for score,pmi,c,a,b in cands[:5]:
        trial=set(units); trial.add(a+b)
        v=bits_per_sign(apply(train,trial),apply(test,trial))
        if v<best-0.002:
            units=trial; best=v; lex.append((a+b,c,round(pmi,2),round(v,3))); improved=True; break
    if not improved: break
print(f"units learned: {len(units)}; final bits/sign {best:.3f}")
print("unit lexicon (unit, train count, PMI, bits/sign after):")
for u,c,pmi,v in lex: print("  "+'-'.join('M%d'%x for x in u), c, pmi, v)
json.dump([list(u) for u in units],open('data/segment1_units.json','w'))
