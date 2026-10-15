"""F38: which tall values the cup formula (cup W700/M328 adjacent to a tall stroke) takes on tablets, against the
value-independent expectation from all tall tokens on tablets. Binomial lower tail. Merged corpus, Wells codes."""
import json,collections,math
B='/Users/Happy/Desktop/plugins/indus'
objs=json.load(open(f'{B}/data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
TALL={31:1,32:2,33:3,34:4,35:5,36:6,37:7}; CUP=700
byobj=collections.Counter(); bydist=collections.Counter(); tallT=collections.Counter(); seen=set()
for o in objs:
    s=o['seq']
    if not o['type'].startswith('TAB'): continue
    for i,g in enumerate(s):
        if g in TALL:
            adj=(i>0 and s[i-1]==CUP) or (i<len(s)-1 and s[i+1]==CUP); tallT[TALL[g]]+=1
            if adj: byobj[TALL[g]]+=1
            if adj and tuple(s) not in seen: bydist[TALL[g]]+=1
    seen.add(tuple(s))
tot=sum(tallT.values()); share=sum(byobj.values())/tot
print('tablets: tall tokens by value',dict(sorted(tallT.items())),'| with cup, by object',dict(sorted(byobj.items())),'| by distinct text',dict(sorted(bydist.items())))
for v in sorted(tallT):
    n=tallT[v]; obs=byobj[v]; exp=n*share
    p=sum(math.comb(n,k)*share**k*(1-share)**(n-k) for k in range(obs+1))
    print(f'  value {v}: {n} tokens, {obs} with cup, expected {exp:.1f}, lower-tail p={p:.2e}')
