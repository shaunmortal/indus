"""Robustness to doubtful readings (Fuls's fragment point, 2026-10-15).
Recompute three Mahadevan headline numbers with ALL lines vs lines with NO doubtful sign (doubtful_positions empty):
(a) END alternation (F23 corrected): stems with >=2 final signs vs length-matched shuffle null;
(b) nesting (F22): share of distinct 2-3-sign texts found verbatim inside a >=5-sign text, vs sign-shuffle null;
(c) short-stroke value distribution (F1): counts of values 1,3,7,12.
Sign list Mahadevan v3; dedupe on final token tuples."""
import csv, json, collections, random, statistics as st
B='/Users/Happy/Desktop/plugins/indus'
MERGE={int(k):v for k,v in json.load(open(f'{B}/data/model4_merges_v3.json')).items()}
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
SHORT={int(k):v for k,v in json.load(open(f'{B}/data/stroke_signs.json'))['short'].items()}
def texts(clean):
    S=set()
    for r in rows:
        if clean and r['doubtful_positions'].strip(): continue
        k=r['signs_clean'].strip()
        if k and k!='0': S.add(tuple(MERGE.get(int(t),int(t)) for t in k.split() if t!='0'))
    return S
def end_alt(T):
    d=collections.defaultdict(set)
    for t in T: d[t[:-1]].add(t[-1])
    return sum(len(v)>=2 for v in d.values())
def end_null(T,n=200):
    out=[]; byL=collections.defaultdict(list)
    for t in T: byL[len(t)].append(t)
    for s in range(n):
        rng=random.Random(s); N=set()
        for L,ts in byL.items():
            fin=[t[-1] for t in ts]; rng.shuffle(fin)
            N.update(t[:-1]+(f,) for t,f in zip(ts,fin))
        out.append(end_alt(N))
    return st.mean(out), st.pstdev(out)
def nest(T):
    short=[t for t in T if 2<=len(t)<=3]; long_=[t for t in T if len(t)>=5]
    def inside(s): return any(l[i:i+len(s)]==s for l in long_ for i in range(len(l)-len(s)+1))
    return len(short), sum(inside(s) for s in short)
def nest_null(T,n=20):
    rng=random.Random(0); out=[]
    toks=[g for t in T for g in t]
    for _ in range(n):
        rng.shuffle(toks); it=iter(toks)
        N={tuple(next(it) for _ in t) for t in T}
        a,b=nest(N); out.append(b/a)
    return st.mean(out), st.pstdev(out)
for clean in (False,True):
    T={t for t in texts(clean) if len(t)>=1}; T3={t for t in T if len(t)>=3}
    print('CLEAN' if clean else 'ALL  ','distinct texts',len(T),'>=3:',len(T3))
    m,s=end_null(T3); print('  END alternation',end_alt(T3),'null %.1f +- %.1f'%(m,s))
    a,b=nest(T); m,s=nest_null(T); print('  nesting %d/%d = %.1f%%  null %.1f%% +- %.1f%%'%(b,a,100*b/a,100*m,100*s))
    c=collections.Counter(SHORT[g] for t in T for g in set(t) if g in SHORT)  # one count per distinct text, as in F1
    print('  short-stroke values 1/3/7/12:',c[1],c[3],c[7],c[12],' all:',sorted(c.items()))
