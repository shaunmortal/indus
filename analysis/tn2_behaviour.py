"""Do TN look-alikes behave like their Indus look-alikes? For each TN base-base co-occurrence pair (a,b), map a->LA(a), b->LA(b) (best Indus look-alike)
and ask how often LA(a) and LA(b) are ADJACENT in Indus texts (symmetric adjacency count, Mahadevan v3 list, distinct texts).
Statistic: weighted mean of Indus adjacency PMI over TN pair occurrences (pairs whose both members have a look-alike >=0.60).
Null: 2000 random re-assignments of look-alikes drawn from Indus signs with matched token frequency (same frequency decile)."""
import json, csv, collections, random, math, statistics as st
B='/Users/Happy/Desktop/plugins/indus'
MERGE={int(k):v for k,v in json.load(open(f'{B}/data/model4_merges_v3.json')).items()}
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); T=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); T.append([MERGE.get(int(t),int(t)) for t in k.split() if t!='0'])
tok=collections.Counter(t for s in T for t in s); N=sum(tok.values())
adj=collections.Counter()
for s in T:
    for a,b in zip(s,s[1:]): adj[(a,b)]+=1; adj[(b,a)]+=1
def pmi(a,b):
    c=adj[(a,b)]
    if c==0: return 0.0
    return math.log2(c*N/(2*tok[a]*tok[b]))
LA={int(k):v[0] for k,v in json.load(open(f'{B}/data/tn_lookalikes.json')).items()}
good={g:MERGE.get(m,m) for g,(m,s) in LA.items() if s>=0.60}
bb=json.load(open(f'{B}/data/raw/tngraffiti/tn_base_base_pairs.json'))
pairs=[]
for k,n in bb.items():
    a,b=map(int,k.split('+'))
    if a in good and b in good and a!=b: pairs.append((good[a],good[b],n))
W=sum(n for _,_,n in pairs)
def score(mapping):
    return sum(n*pmi(mapping[a],mapping[b]) for a,b,n in pairs)/W, sum(n for a,b,n in pairs if adj[(mapping[a],mapping[b])]>0)/W
ident={m:m for m in set(good.values())}
obs_pmi,obs_adj=score(ident)
# frequency-matched null: for each look-alike Indus sign, draw a random Indus sign from the same frequency decile
freq_sorted=sorted([m for m in tok if tok[m]>=15],key=lambda m:tok[m]); dec={}
for i,m in enumerate(freq_sorted): dec[m]=i*10//len(freq_sorted)
buckets=collections.defaultdict(list)
for m,d in dec.items(): buckets[d].append(m)
rng=random.Random(7); nulls_p=[]; nulls_a=[]
for _ in range(2000):
    mp={m:rng.choice(buckets[dec.get(m,0)]) for m in ident}
    p,a=score(mp); nulls_p.append(p); nulls_a.append(a)
print(f"TN base-base pair occurrences usable (both look-alikes >=0.60): {W} across {len(pairs)} pair types; distinct Indus look-alikes {len(ident)}")
print(f"observed: mean Indus PMI of look-alike pairs = {obs_pmi:+.3f}; share attested adjacent in Indus = {obs_adj:.1%}")
print(f"null (frequency-matched random look-alikes): PMI {st.mean(nulls_p):+.3f} +- {st.stdev(nulls_p):.3f} (z={(obs_pmi-st.mean(nulls_p))/st.stdev(nulls_p):+.2f}); adjacent share {st.mean(nulls_a):.1%} +- {st.stdev(nulls_a):.1%} (z={(obs_adj-st.mean(nulls_a))/st.stdev(nulls_a):+.2f})")
print("p(one-sided, observed >= null):",sum(1 for p in nulls_p if p>=obs_pmi)/len(nulls_p))
# strongest TN pairs and their Indus counterpart adjacency
print("\ntop TN pairs -> Indus look-alike pair: Indus adjacency count")
for a,b,n in sorted(pairs,key=lambda x:-x[2])[:10]:
    ta=[g for g in good if good[g]==a][0]; tb=[g for g in good if good[g]==b][0]
    print(f"  TN{ta}+TN{tb} ({n}x) -> M{a}+M{b}: adjacent {adj[(a,b)]}x in Indus, PMI {pmi(a,b):+.2f}")
