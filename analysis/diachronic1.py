"""Diachronic test on the merged corpus (Wells/G codes, periods from HARP / Mohenjo-daro strata).
Q1: does the share of texts with stroke signs change across Harappa periods 3A -> 3B -> 3C?
Q2: does the tall/short complementary split hold within each period?
Q3: Dholavira: how many objects / distinct texts already in the corpus (hold-out planning)."""
import json, collections, re
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
bridge={int(k):v for k,v in json.load(open('data/raw/paragorth/data/derived/bridge_extended.json')).items()}
SS=json.load(open('data/stroke_signs.json')); SHORT={int(k):v for k,v in SS['short'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
def cls(w):
    for m in bridge.get(w,[]):
        if m in (99,100,101): return 'C'
        if m in TALL: return 'T'
        if m in SHORT: return 'S'
    return None
def period(r):
    t=str(r.get('time','-'))
    m=re.search(r'Period\s*(3[ABC]?(?:/C)?|[1-5])',t)
    if m:
        p=m.group(1)
        return {'3A':'3A','3B':'3B','3B/C':'3B/C','3C':'3C','3':'3?','2':'2','4':'4','5':'5','1':'1'}.get(p,p)
    return None
seen=set(); recs=[]
for r in mc:
    k=tuple(r['seq'])
    if not k or k in seen: continue
    seen.add(k); recs.append(r)
print("distinct texts in merged corpus:",len(recs))
print("\nQ1 Harappa: share of distinct texts with a stroke sign (excl. connective 2), by period")
byp=collections.defaultdict(lambda:[0,0])
for r in recs:
    if r['site']!='Harappa': continue
    p=period(r)
    if not p: continue
    byp[p][0]+=1
    if any(cls(w) in ('S','T') for w in r['seq']): byp[p][1]+=1
for p in sorted(byp): print(f"  {p:5} n={byp[p][0]:4}  with stroke={byp[p][1]:4}  {byp[p][1]/byp[p][0]:.0%}")
print("\nQ2 complementary split by period (counted item: T/S), Harappa, items with n>=8")
for p in ['3A','3B','3B/C','3C']:
    after=collections.defaultdict(collections.Counter)
    for r in recs:
        if r['site']!='Harappa' or period(r)!=p: continue
        s=r['seq']
        for a,b in zip(s,s[1:]):
            ca=cls(a); cb=cls(b)
            if ca in ('S','T') and cb not in ('S','T'): after[b][ca]+=1
    items=[(b,c['T'],c['S']) for b,c in after.items() if c['T']+c['S']>=8]
    print(f"  period {p}: "+", ".join(f"W{b}(M{bridge.get(b,['?'])[0] if bridge.get(b) else '?'}) T{t}/S{s}" for b,t,s in sorted(items,key=lambda x:-(x[1]+x[2]))[:8]))
print("\nQ3 Dholavira in merged corpus:")
dh=[r for r in mc if r['site']=='Dholavira']
print("  objects:",len(dh)," distinct texts:",len({tuple(r['seq']) for r in dh})," types:",collections.Counter(r['type'] for r in dh).most_common(6))
print("  cisi ids sample:",[r['cisi'] for r in dh[:8]])
