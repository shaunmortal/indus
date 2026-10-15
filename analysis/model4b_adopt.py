"""Merge adoption by prediction: starting from the M4 406-sign list, test each extra M3b candidate merge individually and greedily:
adopt if held-out bigram perplexity (5 random 80/20 splits, averaged) drops by more than the random-merge null's 2 sd."""
import csv, json, collections, math, random, statistics as st
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); base=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); base.append([int(t) for t in k.split() if t!='0'])
base=[s for s in base if s]
M4={int(k):v for k,v in json.load(open('data/model4_merges.json')).items()}
def apply(seqs,mp): return [[mp.get(t,t) for t in s] for s in seqs]
def ppl(seqs,seeds=(1,2,3,4,5)):
    out=[]
    for sd in seeds:
        rng=random.Random(sd); ix=list(range(len(seqs))); rng.shuffle(ix); cut=int(.8*len(ix))
        tr=[seqs[i] for i in ix[:cut]]; te=[seqs[i] for i in ix[cut:]]
        U=collections.Counter(w for s in tr for w in s); U['</s>']=len(tr); NN=sum(U.values()); V=len(U)+1
        B=collections.defaultdict(collections.Counter)
        for s in tr:
            for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): B[p][w]+=1
        def p1(w): return (U[w]+0.5)/(NN+0.5*V)
        def p2(p,w,D=0.75):
            c=B[p]; t=sum(c.values()); return p1(w) if not t else max(c[w]-D,0)/t+(D*len(c)/t)*p1(w)
        ll=0;m=0
        for s in te:
            for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): ll+=math.log(p2(p,w)); m+=1
        out.append(math.exp(-ll/m))
    return st.mean(out)
cur=dict(M4); seqs=apply(base,cur); p0=ppl(seqs); print(f"start (M4 406 list): ppl {p0:.2f}")
tok=collections.Counter(t for s in seqs for t in s); freq=[m for m,c in tok.items() if c>=8]
rng=random.Random(11); null=[]
for _ in range(40):
    a,b=rng.sample(freq,2); null.append(ppl(apply(seqs,{a:b}))-p0)
mu,sd=st.mean(null),st.stdev(null); thr=mu-2*sd
print(f"null single random merge: delta mean {mu:+.3f} sd {sd:.3f}; adoption threshold delta < {thr:+.3f}")
CAND=[(386,387),(389,387),(14,12),(375,387),(121,112),(15,12),(109,102),(327,326),(348,347)]
for a,b in CAND:
    a2=cur.get(a,a); b2=cur.get(b,b)
    if a2==b2: print(f"  M{a}->M{b}: already merged"); continue
    d=ppl(apply(seqs,{a2:b2}))-p0
    verdict='ADOPT' if d<thr else 'reject'
    print(f"  M{a}->M{b}: delta {d:+.3f}  {verdict}")
    if verdict=='ADOPT':
        cur[a2]=b2; seqs=apply(base,cur); p0=ppl(seqs)
json.dump({str(k):v for k,v in cur.items()},open('data/model4_merges_v2.json','w'),indent=0)
print(f"final list: {len(set(t for s in seqs for t in s))} signs, ppl {p0:.2f}")
