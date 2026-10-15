"""Semicircle signs (Parpola's 'tens' candidates) and stroke-in-cup ligatures, read from Mahadevan drawings:
 M312 = 1 arc, M313 = 2 arcs, M314 = 3 arcs, M315 = stack of ~7 arcs, M298 = 4 nested parentheses
 M329 = U with 2 strokes inside, M330 = U with 3 inside, M344 = jar(342) with 2 inside, M345 = jar with 3 inside.
Tests: frequency; what follows arcs; do arcs combine with strokes in a fixed order (tens+ones)? Distinct texts."""
import csv, json, collections
SS=json.load(open('data/stroke_signs.json')); SHORT={int(k):v for k,v in SS['short'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
ARC={312:1,313:2,314:3,315:7}; LIG={329:'U+2',330:'U+3',344:'jar+2',345:'jar+3'}
SS['arc']=ARC; SS['ligature_strokes_inside']=LIG; json.dump(SS,open('data/stroke_signs.json','w'),indent=1)
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); seqs=[]; objs=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); seqs.append([int(t) for t in k.split()]); objs.append(r['object_type'])
tok=collections.Counter(t for s in seqs for t in s)
print("arc signs (distinct-text tokens):",{f"M{m}({v} arcs)":tok[m] for m,v in ARC.items()}, " M298:",tok[298])
print("ligatures:",{f"M{m}({l})":tok[m] for m,l in LIG.items()}, "  plain U M328:",tok[328]," plain jar M342:",tok[342])
NUMS=set(SHORT)|set(TALL); NUMS-={99,100,101}
foll=collections.defaultdict(collections.Counter); prev=collections.defaultdict(collections.Counter); pos=collections.defaultdict(collections.Counter)
for s in seqs:
    for i,t in enumerate(s):
        if t in ARC or t in LIG:
            pos[t]['first' if i==0 else 'last' if i==len(s)-1 else 'mid']+=1
            if i+1<len(s): foll[t][s[i+1]]+=1
            if i>0: prev[t][s[i-1]]+=1
for t in list(ARC)+list(LIG):
    print(f"\nM{t}: pos={dict(pos[t])} after={foll[t].most_common(5)} before={prev[t].most_common(5)}")
# arc + stroke adjacency (tens+ones hypothesis)
adj=collections.Counter()
for s in seqs:
    for a,b in zip(s,s[1:]):
        if a in ARC and b in NUMS: adj['arc THEN stroke']+=1
        if a in NUMS and b in ARC: adj['stroke THEN arc']+=1
        if a in ARC and b in ARC: adj['arc arc']+=1
print("\narc/stroke adjacency:",dict(adj))
# object types for ligatures vs plain
for t in [328,329,330,342,344,345]:
    c=collections.Counter(o for s,o in zip(seqs,objs) if t in s); print(f"M{t} object types:",c.most_common(4))
