"""Validate M5 (Wells) merges by held-out bigram perplexity on ICIT distinct texts, vs look-alike-distinct merges and random merges (M4 protocol)."""
import csv, json, collections, math, random, statistics as st
B='/Users/Happy/Desktop/plugins/indus'
corp=list(csv.DictReader(open(f'{B}/data/raw/joyboseroy_csv/indus_website_real_corpus.csv')))
seen=set(); base=[]
for r in corp:
    s=tuple(int(x[1:]) for x in r['sign_sequence'].split() if x[1:].isdigit())[::-1]
    if s and s not in seen: seen.add(s); base.append(list(s))
res=json.load(open(f'{B}/data/model5_wells_allographs.json'))
def apply(seqs,mp): return [[mp.get(t,t) for t in s] for s in seqs]
def ppl(seqs,seeds=(1,2,3,4,5)):
    out=[]
    for sd in seeds:
        rng=random.Random(sd); ix=list(range(len(seqs))); rng.shuffle(ix); cut=int(.8*len(ix))
        tr=[seqs[i] for i in ix[:cut]]; te=[seqs[i] for i in ix[cut:]]
        U=collections.Counter(w for s in tr for w in s); U['</s>']=len(tr); NN=sum(U.values()); V=len(U)+1
        Bg=collections.defaultdict(collections.Counter)
        for s in tr:
            for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): Bg[p][w]+=1
        p1=lambda w:(U[w]+0.5)/(NN+0.5*V)
        def p2(p,w,D=0.75):
            c=Bg[p]; t=sum(c.values()); return p1(w) if not t else max(c[w]-D,0)/t+(D*len(c)/t)*p1(w)
        ll=0;m=0
        for s in te:
            for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): ll+=math.log(p2(p,w)); m+=1
        out.append(math.exp(-ll/m))
    return st.mean(out)
# union-find merges from candidates (merge into the more frequent sign)
tok=collections.Counter(t for s in base for t in s)
def build(pairs):
    parent={}
    def f(x):
        while parent.get(x,x)!=x: x=parent[x]
        return x
    for a,b,*_ in pairs:
        ra,rb=f(a),f(b)
        if ra!=rb:
            keep,drop=(ra,rb) if tok[ra]>=tok[rb] else (rb,ra); parent[drop]=keep
    return {x:f(x) for x in parent}
good=build(res['allograph_candidates']); bad=build(res['lookalikes_distinct'][:len(res['allograph_candidates'])])
p0=ppl(base); pg=ppl(apply(base,good)); pb=ppl(apply(base,bad))
print(f"ICIT distinct texts {len(base)}: published list ppl {p0:.2f} | M5 allograph merges ({len(good)} signs folded) {pg:.2f} | look-alike-distinct merges ({len(bad)} folded) {pb:.2f}")
freq=[g for g,c in tok.items() if c>=15]; rng=random.Random(13); null=[]
for _ in range(40):
    pick=rng.sample(freq,2*len(good)); mp={pick[2*i]:pick[2*i+1] for i in range(len(good))}; null.append(ppl(apply(base,mp)))
print(f"random merges of same count: ppl {st.mean(null):.2f} +- {st.stdev(null):.2f} (best {min(null):.2f})")
