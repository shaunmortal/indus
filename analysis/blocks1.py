"""Block inventory and coverage. A block = a contiguous 2-4 sign string occurring as a unit in >=5 distinct seal texts.
Greedy longest-match tiling of each text with blocks; measure token coverage and the number of blocks needed, vs a bigram-sampled null corpus."""
import json, collections, random
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
mc=json.load(open(f'{B}/data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
T=sorted({tuple(Wm.get(w,w) for w in r['seq']) for r in mc if r['type'] in ('SEAL:S','SEAL:R') and len(r['seq'])>=3})
def inventory(T,minc=5):
    c=collections.Counter()
    for t in T:
        seen=set()
        for L in (2,3,4):
            for i in range(len(t)-L+1): seen.add(t[i:i+L])
        for b in seen: c[b]+=1
    return {b:n for b,n in c.items() if n>=minc}
def tile(t,blocks):
    i=0; out=[]
    while i<len(t):
        for L in (4,3,2):
            if i+L<=len(t) and t[i:i+L] in blocks: out.append(t[i:i+L]); i+=L; break
        else: out.append((t[i],)); i+=1
    return out
def stats(T,blocks):
    cov=0; tok=0; nb=[]
    for t in T:
        tl=tile(t,blocks); tok+=len(t); cov+=sum(len(b) for b in tl if len(b)>1); nb.append(len(tl))
    return cov/tok, sum(nb)/len(nb)
blocks=inventory(T); cov,nb=stats(T,blocks)
print(f"distinct seal texts: {len(T)}; blocks (2-4 signs, >=5 texts): {len(blocks)}; token coverage by blocks: {cov:.0%}; mean units per text: {nb:.2f} (mean length {sum(len(t) for t in T)/len(T):.2f})")
# null: bigram-sampled texts of the same lengths
big=collections.defaultdict(collections.Counter)
for t in T:
    for a,b in zip(('<s>',)+t,t): big[a][b]+=1
uni=collections.Counter(w for t in T for w in t)
rng=random.Random(5); covs=[]; nbs=[]; nblk=[]
for _ in range(10):
    S=[]
    for t in T:
        s=[]; p='<s>'
        for _ in range(len(t)):
            ch=big[p] if big[p] else uni; w=rng.choices(list(ch),weights=list(ch.values()))[0]; s.append(w); p=w
        S.append(tuple(s))
    bl=inventory(S); c,n=stats(S,bl); covs.append(c); nbs.append(n); nblk.append(len(bl))
import statistics as st
print(f"bigram-null corpora: blocks {st.mean(nblk):.0f} +- {st.stdev(nblk):.0f}; coverage {st.mean(covs):.0%} +- {st.stdev(covs):.1%}; units/text {st.mean(nbs):.2f}")
print("\nmost frequent blocks:")
for b,n in sorted(blocks.items(),key=lambda kv:-kv[1])[:20]: print(f"  {n:3}  "+'-'.join(f"W{w}(M{bridge.get(w,'?')})" for w in b))
json.dump({'-'.join(map(str,b)):n for b,n in blocks.items()},open(f'{B}/data/blocks_v1.json','w'),indent=0)
