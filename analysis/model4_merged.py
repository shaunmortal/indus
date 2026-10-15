"""M4: corrected sign list = Mahadevan + M3 merges. Rerun core statistics on IM77 distinct texts before/after:
 unique signs, hapax share, unigram/conditional entropy, bigram held-out perplexity, top fixed compounds, F5 value distribution."""
import csv, json, collections, math, random
MERGE={98:97, 67:59,70:59,72:59, 344:343,345:343, 389:387, 348:347, 327:326, 15:12, 109:102}
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); base=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); base.append([int(t) for t in k.split() if t!='0'])
base=[s for s in base if s]
merged=[[MERGE.get(t,t) for t in s] for s in base]
def stats(seqs,name):
    tok=collections.Counter(t for s in seqs for t in s); N=sum(tok.values())
    H1=-sum(c/N*math.log2(c/N) for c in tok.values())
    big=collections.Counter(); uni=collections.Counter()
    for s in seqs:
        for a,b in zip(s,s[1:]): big[(a,b)]+=1; uni[a]+=1
    nb=sum(big.values()); H2=-sum(c/nb*math.log2(c/uni[a]) for (a,_),c in big.items())
    hap=sum(1 for c in tok.values() if c==1)
    # held-out bigram perplexity (fixed split)
    random.seed(5); ix=list(range(len(seqs))); random.shuffle(ix); cut=int(.8*len(ix))
    tr=[seqs[i] for i in ix[:cut]]; te=[seqs[i] for i in ix[cut:]]
    U=collections.Counter(w for s in tr for w in s); U['</s>']=len(tr); NN=sum(U.values()); V=len(U)+1
    B=collections.defaultdict(collections.Counter)
    for s in tr:
        for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): B[p][w]+=1
    def p1(w): return (U[w]+0.5)/(NN+0.5*V)
    def p2(p,w,D=0.75):
        c=B[p]; t=sum(c.values())
        return p1(w) if not t else max(c[w]-D,0)/t+(D*len(c)/t)*p1(w)
    ll=0;m=0
    for s in te:
        for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): ll+=math.log(p2(p,w)); m+=1
    ppl=math.exp(-ll/m)
    # top compounds
    foll=collections.defaultdict(collections.Counter)
    for s in seqs:
        for a,b in zip(s,s[1:]): foll[a][b]+=1
    fx=sorted([(foll[a].most_common(1)[0][1]/sum(foll[a].values()),a,foll[a].most_common(1)[0][0],sum(foll[a].values())) for a in foll if sum(foll[a].values())>=20],reverse=True)[:6]
    print(f"\n== {name}: texts {len(seqs)}, tokens {N}, unique signs {len(tok)}, hapax {hap} ({hap/len(tok):.0%})")
    print(f"   unigram entropy {H1:.2f} bits, conditional entropy {H2:.2f} bits, held-out bigram ppl {ppl:.1f}")
    print("   strongest compounds:",", ".join(f"M{a}->M{b} {sh:.0%} (n={n})" for sh,a,b,n in fx))
    return tok
t0=stats(base,"Mahadevan 417 (as published)"); t1=stats(merged,"Mahadevan + M3 merges (406)")
print("\nmerged sign token counts:",{f"M{k}":t1[k] for k in sorted(set(MERGE.values()))})
json.dump(MERGE,open('data/model4_merges.json','w'),indent=0)

# ---- controls: (a) merge the LOOK-ALIKE-BUT-DISTINCT pairs instead; (b) random merges of the same count (null distribution)
import contextlib, io
def ppl_of(seqs):
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): stats(seqs,"x")
    import re; return float(re.search(r'bigram ppl ([\d.]+)',buf.getvalue()).group(1))
BAD={343:342,344:342,345:342,106:96,150:149,211:153,109:89,336:328,293:287,391:389}
bad=[[BAD.get(t,t) for t in s] for s in base]
print(f"\nCONTROL: merging look-alike-but-distinct pairs ({len(BAD)} merges): ppl {ppl_of(bad):.1f}  (published 29.0, M3 merges 26.3)")
tokc=collections.Counter(t for s in base for t in s); freq=[m for m,c in tokc.items() if c>=15]
null=[]
rng=random.Random(9)
for _ in range(60):
    pick=rng.sample(freq,2*len(MERGE)); rm={pick[2*i]:pick[2*i+1] for i in range(len(MERGE))}
    null.append(ppl_of([[rm.get(t,t) for t in s] for s in base]))
import statistics as st
print(f"NULL: {len(MERGE)} random merges among signs with >=15 tokens: ppl mean {st.mean(null):.1f} sd {st.stdev(null):.1f} min {min(null):.1f}")
