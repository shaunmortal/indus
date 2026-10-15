"""Anchor-readiness drill: if ONE element (title block, closer, opener formula, single sign) were read from an anchor,
how many distinct seal texts and tokens would it touch? Ranks what is worth hunting in bilingual/anchor material. (F35)"""
import json,collections
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
mc=json.load(open(f'{B}/data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
T={tuple(Wm.get(w,w) for w in r['seq']) for r in mc if r['type'].startswith('SEAL') and len(r['seq'])>=3}
ntok=sum(len(t) for t in T); print('distinct seal texts',len(T),'tokens',ntok)
tb=json.load(open(f'{B}/data/title_blocks_v1.json'))['blocks']
def touch(b):
    hit=[t for t in T if any(t[i:i+len(b)]==b for i in range(len(t)-len(b)+1))]; return len(hit),sum(len(t) for t in hit)
out={'title_blocks':[],'signs':[],'openers':[],'closers':[]}
for x in tb[:8]:
    n,tk=touch(tuple(x['block_W'])); out['title_blocks'].append((x['block_W'],x['block_M'],n,round(n/len(T),3),tk)); print(f"block W{x['block_W']} / M{x['block_M']}: {n} texts ({n/len(T):.1%}), {tk} tokens")
for w,n in collections.Counter(w for t in T for w in set(t)).most_common(12): out['signs'].append((w,bridge.get(w),n,round(n/len(T),3))); print(f"sign W{w}/M{bridge.get(w)}: {n} texts ({n/len(T):.1%})")
for b,n in collections.Counter(t[:2] for t in T).most_common(6): out['openers'].append((list(b),n,round(n/len(T),3))); print(f"opener W{b}: {n} ({n/len(T):.1%})")
for w,n in collections.Counter(t[-1] for t in T).most_common(6): out['closers'].append((w,bridge.get(w),n,round(n/len(T),3))); print(f"closer W{w}/M{bridge.get(w)}: {n} ({n/len(T):.1%})")
json.dump(out,open(f'{B}/data/anchor_drill_v1.json','w'),indent=1)
