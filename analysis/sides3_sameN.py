"""F39: on two-sided tablets/sealings (IM77, side field), does the same side-1 text always carry the same side-2 tall value?
Receipt model: N varies freely per object. Fixed-issue model: N constant per side-1 text. Null: N shuffled within object type."""
import csv,json,collections,random
B='/Users/Happy/Desktop/plugins/indus'
TALL={int(k):v for k,v in json.load(open(f'{B}/data/stroke_signs.json'))['tall'].items()}
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
obj=collections.defaultdict(dict)
for r in rows:
    if r['object_type'] not in ('miniature tablet','sealing','copper tablet') or r['signs_clean'].strip() in ('','0'): continue
    obj[(r['text_no'],r['object_type'])].setdefault(r['side'],[]).append(tuple(int(t) for t in r['signs_clean'].split() if t!='0'))
def N_of(lines):
    v=[TALL[g] for l in lines for g in l if g in TALL]; return v[0] if len(v)==1 else None
pairs=[(k[1],tuple(v['1'][0]),N_of(v['2'])) for k,v in obj.items() if '1' in v and '2' in v and N_of(v['2'])]
grp=collections.defaultdict(list)
for t,s1,n in pairs: grp[(t,s1)].append(n)
multi={k:v for k,v in grp.items() if len(v)>=2}; same=sum(1 for v in multi.values() if len(set(v))==1)
print(f'two-sided objects {len(pairs)}; side-1 texts on >=2 objects {len(multi)}; N identical on all objects {same} ({same/len(multi):.0%})')
for k,v in sorted(multi.items(),key=lambda x:-len(x[1]))[:6]: print('  ',k,collections.Counter(v))
rng=random.Random(1); vals=collections.defaultdict(list)
for t,s1,n in pairs: vals[t].append(n)
cnt=0; R=2000
for _ in range(R):
    it={t:iter(rng.sample(v,len(v))) for t,v in vals.items()}; g2=collections.defaultdict(list)
    for t,s1,n in pairs: g2[(t,s1)].append(next(it[t]))
    if sum(1 for v in g2.values() if len(v)>=2 and len(set(v))==1)>=same: cnt+=1
print(f'null P(identical >= {same}) = {cnt/R:.4f}')

# --- mould-deduplicated version: one object per (type, side-1 text, side-2 text); same-N then needs >=2 different side-2 texts
ded={}
for t,s1,n in pairs: pass
objs2={}
for k,v in obj.items():
    if '1' in v and '2' in v and N_of(v['2']): objs2[(k[1],tuple(v['1'][0]),tuple(v['2'][0]))]=N_of(v['2'])
pairs2=[(t,s1,n) for (t,s1,s2),n in objs2.items()]
grp2=collections.defaultdict(list)
for t,s1,n in pairs2: grp2[(t,s1)].append(n)
multi2={k:v for k,v in grp2.items() if len(v)>=2}; same2=sum(1 for v in multi2.values() if len(set(v))==1)
print(f'DEDUPED by (side-1, side-2) text: objects {len(pairs2)}; side-1 texts with >=2 distinct side-2 texts {len(multi2)}; same N on all {same2} ({same2/len(multi2):.0%})')
vals2=collections.defaultdict(list)
for t,s1,n in pairs2: vals2[t].append(n)
cnt=0
for _ in range(R):
    it={t:iter(rng.sample(v,len(v))) for t,v in vals2.items()}; g2=collections.defaultdict(list)
    for t,s1,n in pairs2: g2[(t,s1)].append(next(it[t]))
    if sum(1 for v in g2.values() if len(v)>=2 and len(set(v))==1)>=same2: cnt+=1
print(f'deduped null P(identical >= {same2}) = {cnt/R:.3f}')
