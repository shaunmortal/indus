"""Kober grid: paradigmatic alternation at text END and text START.
For every prefix (text minus last sign) that occurs with >=2 different final signs, record the alternating final signs.
Build a substitution graph among finals (edge weight = number of shared prefixes). Compare with a null where final signs are
shuffled across texts of equal length (keeps prefixes and final-sign frequencies). Same for initial signs with shared suffixes.
Sign list: Mahadevan v3. Distinct texts, length >= 3."""
import csv, json, collections, random, itertools, statistics as st
B='/Users/Happy/Desktop/plugins/indus'
MERGE={int(k):v for k,v in json.load(open(f'{B}/data/model4_merges_v3.json')).items()}
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); T=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); T.append(tuple(MERGE.get(int(t),int(t)) for t in k.split() if t!='0'))
T=[t for t in T if len(t)>=3]
def grid(T,end=True):
    d=collections.defaultdict(set)
    for t in T:
        if end: d[t[:-1]].add(t[-1])
        else: d[t[1:]].add(t[0])
    alt={k:v for k,v in d.items() if len(v)>=2}
    edges=collections.Counter()
    for k,v in alt.items():
        for a,b in itertools.combinations(sorted(v),2): edges[(a,b)]+=1
    return alt,edges
def shuffled(T,end=True,seed=0):
    rng=random.Random(seed); byL=collections.defaultdict(list)
    for t in T: byL[len(t)].append(t)
    out=[]
    for L,ts in byL.items():
        fin=[t[-1] if end else t[0] for t in ts]; rng.shuffle(fin)
        out+=[(t[:-1]+(f,)) if end else ((f,)+t[1:]) for t,f in zip(ts,fin)]
    return out
for end,name in [(True,'END (closers)'),(False,'START (openers)')]:
    alt,edges=grid(T,end)
    nulls=[len(grid(shuffled(T,end,s),end)[0]) for s in range(30)]
    print(f"\n== {name}: prefixes/suffixes with >=2 alternants: {len(alt)} | shuffled null {st.mean(nulls):.1f} +- {st.stdev(nulls):.1f}")
    # distinct texts covered
    cov=sum(len(v) for v in alt.values()); print(f"   texts in alternation sets: {cov} of {len(T)}")
    top=edges.most_common(12); print("   strongest substitution pairs (shared stems):",[(f"M{a}~M{b}",c) for (a,b),c in top])
    # degree: which signs alternate with most partners
    deg=collections.Counter()
    for (a,b),c in edges.items(): deg[a]+=1; deg[b]+=1
    print("   most substitutable signs (distinct partners):",deg.most_common(10))
    # example stems with 3+ alternants
    ex=sorted(alt.items(),key=lambda kv:-len(kv[1]))[:5]
    print("   stems with most alternants:",[('-'.join('M%d'%x for x in k),sorted(v)) for k,v in ex])
