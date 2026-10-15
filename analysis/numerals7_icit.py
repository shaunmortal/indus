"""Replicate Tests 2-4 on the independent ICIT/Wells transcription (G-signs) using paragorth's G->M bridge for stroke signs."""
import csv, json, collections
bridge={int(k):v for k,v in json.load(open('data/raw/paragorth/data/derived/bridge_extended.json')).items()}
SS=json.load(open('data/stroke_signs.json')); SHORT={int(k):v for k,v in SS['short'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
g2m={}
for g,ms in bridge.items():
    for m in ms:
        if m in SHORT or m in TALL: g2m.setdefault(g,m)
print("G stroke signs via bridge:",{g:m for g,m in sorted(g2m.items())})
rows=list(csv.DictReader(open('data/raw/joyboseroy_csv/indus_website_real_corpus.csv',encoding='utf-8')))
seen=set(); seqs=[]
for r in rows:
    s=[int(t[1:]) for t in r['sign_sequence'].split() if t.startswith('G') and t[1:].isdigit()]
    if not s: continue
    s=s[::-1]  # stored as seen (L-R); reading order is R-L for most -> reverse to reading order
    k=tuple(s)
    if k in seen: continue
    seen.add(k); seqs.append(s)
print("distinct ICIT texts:",len(seqs))
def cls(g):
    m=g2m.get(g)
    if m is None: return None
    if m in (99,100,101): return 'C'
    return 'T' if m in TALL else 'S'
val=lambda g: (TALL.get(g2m[g]) if cls(g)=='T' else SHORT.get(g2m[g]))
vs=collections.Counter(); vt=collections.Counter(); order=collections.Counter(); after=collections.defaultdict(collections.Counter)
for s in seqs:
    for i,t in enumerate(s):
        c=cls(t)
        if c=='S': vs[val(t)]+=1
        if c=='T': vt[val(t)]+=1
        if c in ('S','T') and i+1<len(s):
            n=s[i+1]; cn=cls(n)
            if cn in ('S','T'): order[c+cn]+=1
            elif cn is None or cn=='C': after[n][c]+=1
print("Test2 ICIT short values:",sorted(vs.items())," tall:",sorted(vt.items()))
print("Test3 ICIT compound orders:",dict(order))
print("Test4 ICIT counted items tall/short (n>=10):")
for g,c in sorted(after.items(),key=lambda x:-(x[1]['T']+x[1]['S'])):
    if c['T']+c['S']>=10: print(f"  G{g:>4} (M{bridge.get(g,['?'])[0] if bridge.get(g) else '?'}): T={c['T']:3} S={c['S']:3}")
