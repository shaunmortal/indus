"""Provenance of ICIT seal dimensions (F36): are they the 1930s catalogue measurements (inches) converted to mm?
(1) share of ICIT widths that are exact multiples of 0.05 inch; (2) direct join of ICIT seals to Marshall/Mackay seals
through IM77 (same site, identical sign sequence, unique on both sides) and |ICIT width - catalogue width x 25.4|."""
import json,csv,statistics as st
B='/Users/Happy/Desktop/plugins/indus'
seals=list(csv.DictReader(open(f'{B}/data/icit_seal.csv'))); sites={r['SITEID']:r for r in csv.DictReader(open(f'{B}/data/icit_site.csv'))}
sitename={k:(v.get('NAME') or v.get('SITE') or list(v.values())[1]) for k,v in sites.items()}
W=[(r['SEALID'],sitename.get(r['SITEID'],'?'),float(r['WIDTH'])) for r in seals if float(r['WIDTH'] or 0)>0 and float(r['WIDTH'])<200]
def inchy(x,step=1.27,tol=0.02): q=x/step; return abs(q-round(q))<tol/step
for s in ('Mohenjo-daro','Harappa','Lothal','Dholavira','Kalibangan'):
    ws=[w for _,site,w in W if site==s]; print(f'{s:12s} n={len(ws):4d} width = k x 0.05 in: {sum(inchy(w) for w in ws)/len(ws):.0%}  width = k x 0.5 mm: {sum(abs(w*2-round(w*2))<0.04 for w in ws)/len(ws):.0%}')
mar={int(k):v for k,v in json.load(open(f'{B}/data/marshall_seal_sizes.json')).items()}; mac={int(k):v for k,v in json.load(open(f'{B}/data/mackay_seal_sizes.json')).items()}
cat={}
for r in csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')):
    if r['object_type']!='seal' or r['signs_clean'].strip() in ('','0'): continue
    tn=int(r['text_no']); v=mar.get(tn-1000) if 1000<tn<2000 else mac.get(tn-2000) if 2000<tn<3000 else None
    if v and v['w']: cat.setdefault((r['site'],tuple(int(t) for t in r['signs_clean'].split())),[]).append(v['w']*25.4)
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
corp={r['inscription_id'][1:]:r for r in csv.DictReader(open(f'{B}/data/raw/joyboseroy_csv/indus_website_real_corpus.csv'))}
pairs=[]
for sid,site,w in W:
    r=corp.get(sid)
    if not r: continue
    seq=tuple(bridge.get(int(x[1:]),-1) for x in r['sign_sequence'].split())[::-1]
    v=cat.get(({'Mohenjo-daro':'Mohenjodaro'}.get(site,site),seq))
    if v and len(v)==1: pairs.append((w,v[0]))
d=[abs(a-b) for a,b in pairs]
print(f'joined seals {len(pairs)}: median |diff| {st.median(d):.2f} mm; within 0.3 mm {100*sum(x<=0.3 for x in d)/len(d):.0f}%; within 1 mm {100*sum(x<=1 for x in d)/len(d):.0f}%')
