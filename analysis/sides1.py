"""Two-sided objects in IM77: is there a division of labour between sides? (e.g. side 1 = name, side 2 = numeral+unit)
Uses side / line fields. Distinct texts per object."""
import csv, json, collections
SS=json.load(open('data/stroke_signs.json')); SHORT={int(k):v for k,v in SS['short'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
NUM=set(SHORT)|set(TALL); NUM-= {99,100,101}
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
obj=collections.defaultdict(dict)
for r in rows:
    s=r['signs_clean'].strip()
    if not s or s=='0': continue
    obj[(r['text_no'],r['object_type'])].setdefault(r['side'],[]).append([int(t) for t in s.split()])
multi={k:v for k,v in obj.items() if len(v)>=2}
print("objects with >=2 inscribed sides:",len(multi)," by type:",collections.Counter(k[1] for k in multi).most_common(5))
def hasnum(lines): return any(t in NUM for l in lines for t in l)
def jarfinal(lines): return any(l[-1]==342 for l in lines)
for typ in ['miniature tablet','sealing','copper tablet','seal']:
    ks=[k for k in multi if k[1]==typ]
    if len(ks)<10: continue
    both=sum(1 for k in ks if hasnum(multi[k]['1']) and hasnum(multi[k]['2'])) if all('1' in multi[k] and '2' in multi[k] for k in ks[:1]) else None
    s1=[k for k in ks if '1' in multi[k] and '2' in multi[k]]
    n1=sum(1 for k in s1 if hasnum(multi[k]['1'])); n2=sum(1 for k in s1 if hasnum(multi[k]['2']))
    nb=sum(1 for k in s1 if hasnum(multi[k]['1']) and hasnum(multi[k]['2'])); nn=sum(1 for k in s1 if not hasnum(multi[k]['1']) and not hasnum(multi[k]['2']))
    j1=sum(1 for k in s1 if jarfinal(multi[k]['1'])); j2=sum(1 for k in s1 if jarfinal(multi[k]['2']))
    L1=sum(len(l) for k in s1 for l in multi[k]['1'])/max(1,len(s1)); L2=sum(len(l) for k in s1 for l in multi[k]['2'])/max(1,len(s1))
    print(f"\n{typ}: objects with sides 1&2 = {len(s1)}")
    print(f"  numeral on side1 {n1} ({n1/len(s1):.0%}), side2 {n2} ({n2/len(s1):.0%}); both {nb}, neither {nn}  -> exactly one side {len(s1)-nb-nn} ({(len(s1)-nb-nn)/len(s1):.0%})")
    print(f"  jar-final side1 {j1} ({j1/len(s1):.0%}), side2 {j2} ({j2/len(s1):.0%});  mean signs side1 {L1:.1f}, side2 {L2:.1f}")
    # distinct side-2 texts vs side-1 texts (is one side more repetitive = formula?)
    d1=len({tuple(map(tuple,multi[k]['1'])) for k in s1}); d2=len({tuple(map(tuple,multi[k]['2'])) for k in s1})
    print(f"  distinct side1 texts {d1}/{len(s1)}, distinct side2 texts {d2}/{len(s1)}")
