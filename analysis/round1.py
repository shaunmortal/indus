"""Round-seal lexicon: how do round-seal texts differ structurally from square-seal texts at the SAME sites?
length, jar-closer share, opener share, numeral share, co-occurrence partners of M169/M387, distinct-text repetition."""
import json, collections, statistics as st
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
bridge={int(k):v['M'][0] for k,v in json.load(open('data/bridge_WM.json')).items() if v['M']}
HOME={'Mohenjo-daro','Harappa','Lothal','Dholavira','Kalibangan','Chanhu-daro'}
seen=set(); R=[]
for r in mc:
    if r['type'] in ('SEAL:S','SEAL:R') and r['seq'] and r['site'] in HOME:
        k=(tuple(r['seq']),r['type'],r['site'])
        if k in seen: continue
        seen.add(k); R.append((tuple(r['seq']),r['type'],r['site'],r.get('symbol','')))
sq=[x for x in R if x[1]=='SEAL:S']; rd=[x for x in R if x[1]=='SEAL:R']
print(f"home-site distinct texts: square {len(sq)}, round {len(rd)}")
def share(items,f): return sum(1 for x in items if f(x[0]))/len(items)
OPEN={817,820,861}; JAR=740; PERSON={90,91}; NUMS={1,3,4,5,13,16,17,18,31,32,33,35,55}
for name,f in [("mean length",None),("jar-final 740",lambda s:s[-1]==JAR),("opener 817/820/861 initial",lambda s:s[0] in OPEN),
               ("contains a stroke numeral",lambda s:any(w in NUMS for w in s)),("person/twins 90/91",lambda s:any(w in PERSON for w in s)),
               ("contains M169 (W407)",lambda s:407 in s),("contains M387 (W806)",lambda s:806 in s),("contains M343 (W741)",lambda s:741 in s),("contains fish W220",lambda s:220 in s)]:
    if f is None: print(f"  {name:28} square {st.mean(len(x[0]) for x in sq):.2f}  round {st.mean(len(x[0]) for x in rd):.2f}")
    else: print(f"  {name:28} square {share(sq,f):5.1%}  round {share(rd,f):5.1%}")
print("\nanimal on round seals:",collections.Counter(x[3].split(':')[0] or 'none' for x in rd).most_common(6))
print("animal on square seals:",collections.Counter(x[3].split(':')[0] or 'none' for x in sq).most_common(6))
# partners of M169 / M387 on round seals vs square
for w,name in [(407,'M169'),(806,'M387')]:
    for typ,items in [('round',rd),('square',sq)]:
        c=collections.Counter(); pos=collections.Counter()
        for s,_,_,_ in items:
            if w in s:
                i=s.index(w); pos['first' if i==0 else 'last' if i==len(s)-1 else 'mid']+=1
                for o in s:
                    if o!=w: c[o]+=1
        if sum(pos.values()): print(f"{name} on {typ}: n={sum(pos.values())} pos={dict(pos)} partners={[('W%d(M%s)'%(o,bridge.get(o,'?')),k) for o,k in c.most_common(5)]}")
# top round-seal texts
print("\nmost frequent round-seal texts:",collections.Counter(x[0] for x in rd).most_common(6))
