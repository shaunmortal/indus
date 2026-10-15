"""Unified corrected sign list v1: union-find over Mahadevan and Wells signs using
 (a) bridge_WM (W<->M, 165 signs), (b) M4b merges (Mahadevan v2), (c) M5c merges (Wells v2).
Report clusters, conflicts (merges supported on one corpus only or contradicted), and validate implied cross-corpus merges by perplexity."""
import json, csv, collections, math, random, statistics as st
B='/Users/Happy/Desktop/plugins/indus'
bridge={int(k):v['M'] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
Mm={int(k):v for k,v in json.load(open(f'{B}/data/model4_merges_v2.json')).items()}
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v2.json')).items()}
parent={}
def find(x):
    while parent.get(x,x)!=x: x=parent[x]
    return x
def union(a,b,why,log):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[rb]=ra; log.append((a,b,why))
log=[]
for w,ms in bridge.items():
    for m in ms: union(f"W{w}",f"M{m}",'bridge',log)
for a,b in Mm.items(): union(f"M{a}",f"M{b}",'M4b',log)
for a,b in Wm.items(): union(f"W{a}",f"W{b}",'M5c',log)
clusters=collections.defaultdict(set)
for x in list(parent)+[f"W{w}" for w in bridge]+[f"M{m}" for ms in bridge.values() for m in ms]: clusters[find(x)].add(x)
multi={k:v for k,v in clusters.items() if len([x for x in v if x.startswith('M')])>1 or len([x for x in v if x.startswith('W')])>1}
print("unified clusters with >1 node:",len(multi))
for k,v in sorted(multi.items(),key=lambda kv:-len(kv[1]))[:25]:
    ms=sorted(x for x in v if x[0]=='M'); ws=sorted(x for x in v if x[0]=='W'); print("  ",'+'.join(ms),'|','+'.join(ws))
# implied merges: M-signs in one cluster that M4b did NOT merge -> implied by Wells side; and vice versa
impliedM={}; impliedW={}
for k,v in multi.items():
    ms=[int(x[1:]) for x in v if x[0]=='M']; ws=[int(x[1:]) for x in v if x[0]=='W']
    if len(ms)>1:
        tgt=min(ms,key=lambda m:0)  # placeholder, choose most frequent below
        for m in ms[1:]: impliedM[m]=ms[0]
    if len(ws)>1:
        for w in ws[1:]: impliedW[w]=ws[0]
json.dump({'clusters':{k:sorted(v) for k,v in multi.items()},'log':log},open(f'{B}/data/unified_signs_v1.json','w'),indent=0)
# ---- validate implied merges on each corpus (only those NOT already in that corpus's own v2 merges)
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); im=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); im.append([int(t) for t in k.split() if t!='0'])
im=[s for s in im if s]
corp=list(csv.DictReader(open(f'{B}/data/raw/joyboseroy_csv/indus_website_real_corpus.csv')))
seen=set(); ic=[]
for r in corp:
    s=tuple(int(x[1:]) for x in r['sign_sequence'].split() if x[1:].isdigit())[::-1]
    if s and s not in seen: seen.add(s); ic.append(list(s))
def apply(seqs,mp): return [[mp.get(t,t) for t in s] for s in seqs]
def ppl(seqs,seeds=(1,2,3,4,5)):
    out=[]
    for sd in seeds:
        rng=random.Random(sd); ix=list(range(len(seqs))); rng.shuffle(ix); cut=int(.8*len(ix))
        tr=[seqs[i] for i in ix[:cut]]; te=[seqs[i] for i in ix[cut:]]
        U=collections.Counter(w for s in tr for w in s); U['</s>']=len(tr); NN=sum(U.values()); V=len(U)+1
        Bg=collections.defaultdict(collections.Counter)
        for s in tr:
            for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): Bg[p][w]+=1
        p1=lambda w:(U[w]+0.5)/(NN+0.5*V)
        def p2(p,w,D=0.75):
            c=Bg[p]; t=sum(c.values()); return p1(w) if not t else max(c[w]-D,0)/t+(D*len(c)/t)*p1(w)
        ll=0;m=0
        for s in te:
            for p,w in zip(('<s>',)+tuple(s),tuple(s)+('</s>',)): ll+=math.log(p2(p,w)); m+=1
        out.append(math.exp(-ll/m))
    return st.mean(out)
def resolve(mp):
    def r(x):
        seen=set()
        while x in mp and x not in seen: seen.add(x); x=mp[x]
        return x
    return {k:r(k) for k in mp}
Mv2=resolve(Mm); Wv2=resolve(Wm)
tokM=collections.Counter(t for s in apply(im,Mv2) for t in s); tokW=collections.Counter(t for s in apply(ic,Wv2) for t in s)
newM={}; newW={}
for k,v in multi.items():
    ms=[int(x[1:]) for x in v if x[0]=='M']; ws=[int(x[1:]) for x in v if x[0]=='W']
    ms=sorted(set(Mv2.get(m,m) for m in ms),key=lambda m:-tokM[m]); ws=sorted(set(Wv2.get(w,w) for w in ws),key=lambda w:-tokW[w])
    for m in ms[1:]: newM[m]=ms[0]
    for w in ws[1:]: newW[w]=ws[0]
print(f"\nimplied NEW merges beyond each corpus's own v2: Mahadevan {len(newM)} {sorted(newM.items())[:12]}; Wells {len(newW)} {sorted(newW.items())[:12]}")
pM0=ppl(apply(im,Mv2)); pM1=ppl(apply(apply(im,Mv2),newM)); pW0=ppl(apply(ic,Wv2)); pW1=ppl(apply(apply(ic,Wv2),newW))
print(f"IM77: v2 ppl {pM0:.2f} -> with implied merges {pM1:.2f}   | ICIT: v2 ppl {pW0:.2f} -> with implied merges {pW1:.2f}")
# per-merge test of implied merges (adopt if beats 2sd null)
for name,seqs,base_mp,new in [('IM77',im,Mv2,newM),('ICIT',ic,Wv2,newW)]:
    s0=apply(seqs,base_mp); p0=ppl(s0); tok=collections.Counter(t for s in s0 for t in s); freq=[g for g,c in tok.items() if c>=15]
    rng=random.Random(29); null=[ppl(apply(s0,{a:b}))-p0 for a,b in (rng.sample(freq,2) for _ in range(30))]; thr=st.mean(null)-2*st.stdev(null)
    print(f"\n{name} implied merges, threshold {thr:+.3f}:")
    for a,b in sorted(new.items()):
        d=ppl(apply(s0,{a:b}))-p0; print(f"  {a}->{b}: {d:+.3f} {'ADOPT' if d<thr else 'reject'}")
