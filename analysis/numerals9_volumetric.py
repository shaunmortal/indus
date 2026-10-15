"""Wells 2015 ch.4-5 reads 'V + number' (cup W700/M328 + tall strokes) on Harappa tablets and pots as volumes.
Test on the merged corpus (5,369 objects, Wells codes, CISI object classes): if tall-N is a quantity, its value profile
should differ across object classes (pots of many sizes vs mass-produced tablets); if it is a formula, one favoured value
recurs everywhere. Also: texts shared verbatim between pots and tablets (Wells fig. 5.4)."""
import json, collections
B='/Users/Happy/Desktop/plugins/indus'
objs=json.load(open(f'{B}/data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
TALL={31:1,32:2,33:3,34:4,35:5}; CUP=700
def cls(t):
    return {'SEAL:S':'square seal','SEAL:R':'round seal','TAB:B':'moulded tablet','TAB:I':'incised tablet','TAB:C':'copper tablet','POT:T:g':'pot graffito','POT:T:s':'pot stamped','TAG':'tag'}.get(t,t)
freq=collections.Counter(g for o in objs for g in o['seq']); print('tall code freq',{w:freq[w] for w in TALL},'cup',freq[CUP])
cup=collections.defaultdict(collections.Counter); anyw=collections.defaultdict(collections.Counter); seen=set()
texts_by_cls=collections.defaultdict(set)
for o in objs:
    s=o['seq']; c=cls(o['type']); key=(c,tuple(s))
    texts_by_cls[c].add(tuple(s))
    if key in seen: continue
    seen.add(key)
    for i,g in enumerate(s):
        if g in TALL:
            anyw[c][TALL[g]]+=1
            if (i>0 and s[i-1]==CUP) or (i<len(s)-1 and s[i+1]==CUP): cup[c][TALL[g]]+=1
def show(d,title):
    print('\n'+title); print('%-16s'%'class','  '.join('N=%d'%n for n in range(1,6)),' total  mode')
    for c,k in sorted(d.items(),key=lambda x:-sum(x[1].values())):
        tot=sum(k.values())
        if tot>=8: print('%-16s'%c,'  '.join('%3d'%k[n] for n in range(1,6)),' %4d'%tot,'  ',max(k,key=k.get))
show(cup,'tall-N adjacent to cup (distinct texts per class)'); show(anyw,'tall-N anywhere (distinct texts per class)')
pots=texts_by_cls['pot graffito']|texts_by_cls['pot stamped']; tabs=texts_by_cls['moulded tablet']|texts_by_cls['incised tablet']
sh=pots&tabs; print('\ndistinct pot texts',len(pots),'tablet texts',len(tabs),'shared verbatim',len(sh))
print('shared examples (Wells codes, reading order):',sorted(sh,key=len,reverse=True)[:12])
withtall=[t for t in sh if any(g in TALL for g in t)]; print('shared texts containing a tall stroke:',len(withtall),withtall[:8])

# --- part 2: by text length, pots vs seals permutation on share of N>=4; short strokes by class; pots by site
import random
SS=json.load(open(f'{B}/data/stroke_signs.json')); SHORT={int(k):v for k,v in SS['short'].items()}
br=json.load(open(f'{B}/data/bridge_WM.json')); W2M={int(w):v['M'][0] for w,v in br.items() if v['M']}
WSHORT={w:SHORT[m] for w,m in W2M.items() if m in SHORT}
def cls3(t): return {'SEAL:S':'seal','SEAL:R':'seal','TAB:B':'tablet','TAB:I':'tablet','POT:T:g':'pot','POT:T:s':'pot'}.get(t)
rec=collections.defaultdict(lambda:collections.defaultdict(collections.Counter)); sh=collections.defaultdict(collections.Counter)
site=collections.defaultdict(collections.Counter); seen=set()
for o in objs:
    c=cls3(o['type']); s=tuple(o['seq'])
    if not c or (c,s) in seen: continue
    seen.add((c,s)); L='len1' if len(s)==1 else ('len2' if len(s)==2 else 'len3+')
    for g in set(s):
        if g in TALL:
            rec[c][L][TALL[g]]+=1
            if c=='pot' and len(s)>=2: site[o['site']][TALL[g]]+=1
        if g in WSHORT and len(s)>=2: sh[c][WSHORT[g]]+=1
print('\ntall-N by class and text length [N=1..5], share N>=4')
for c in ('pot','tablet','seal'):
    for L in ('len1','len2','len3+'):
        k=rec[c][L]; tot=sum(k.values())
        if tot: print(' %-7s %-5s'%(c,L),[k[n] for n in range(1,6)],'tot',tot,' %.0f%%'%(100*(k[4]+k[5])/tot))
a=[rec['pot']['len3+'][n] for n in range(1,6)]; b=[rec['seal']['len3+'][n] for n in range(1,6)]
obs=abs((a[3]+a[4])/sum(a)-(b[3]+b[4])/sum(b)); pool=[n for n in range(5) for _ in range(a[n])]+[n for n in range(5) for _ in range(b[n])]
rng=random.Random(0); cnt=0
for _ in range(5000):
    rng.shuffle(pool); A=pool[:sum(a)]; Bb=pool[sum(a):]
    if abs(sum(x>=3 for x in A)/len(A)-sum(x>=3 for x in Bb)/len(Bb))>=obs: cnt+=1
print('pots vs seals (len>=3), diff in share N>=4: %.3f, perm p=%.4f'%(obs,cnt/5000))
print('short-stroke values (texts >=2):',{c:(dict(sorted(sh[c].items())),'share>=7 %.0f%%'%(100*sum(v for n,v in sh[c].items() if n>=7)/max(1,sum(sh[c].values())))) for c in ('pot','tablet','seal')})
print('pot tall-N by site:',{s:[k[n] for n in range(1,6)] for s,k in sorted(site.items(),key=lambda x:-sum(x[1].values()))[:4]})
