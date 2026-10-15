"""Parse Marshall 1931 vol II 'Tabulation of Seals' (OCR). Each OCR line holds up to two table rows:
  serial | W x H (inches) | depth ft' in" | type | material | colour | - | - | SITE findno
Outputs data/marshall_seal_sizes.json. Validates join text_no = 1000+serial via depth vs IM77 level code."""
import re, csv, json, collections, statistics as st
txt=open('data/raw/books/Marshall1931_vol2_text.txt',encoding='utf-8',errors='replace').read().split('\n')
starts=[i for i,l in enumerate(txt) if 'TABULATION OF SEALS' in l.upper()]
lines=txt[starts[1]-3:starts[1]+1200]
NUM=r"[oOrIl0-9œ.:°•'·\-]{1,5}"
def fixnum(s):
    s=s.strip().replace('-','.').replace('°','.').replace(':','.').replace("'",'.').replace('•','.').replace('·','.').replace('œ','0.').replace(' ','')
    s=s.replace('o','0').replace('O','0').replace('I','1').replace('l','1')
    s=re.sub(r'^r0?s$','1.05',s); s=re.sub(r'^r',"1",s)
    s=s.replace('..','.')
    if re.fullmatch(r'0\d\d',s): s='0.'+s[1:]
    elif re.fullmatch(r'0\d',s): s='0.'+s[1:]
    elif re.fullmatch(r'1\d\d',s): s='1.'+s[1:]
    elif re.fullmatch(r'1\d',s): s='1.'+s[1:]
    elif re.fullmatch(r'\d',s): s={'1':'1.0'}.get(s,'0.'+s)
    try:
        v=float(s); return round(v,2) if 0.3<=v<=2.5 else None
    except: return None
row=re.compile(r'(?<!\d)(\d{1,3})\s*[|\[\]I]?\s*('+NUM+r')\s*[xX×]\s*('+NUM+r'|\?)\s*[|\[]?\s*(\d{1,2})?\s*[\'’′]?\s*(\d{1,2})?\s*["”″]?(?:(.{0,70}?)\b(HR|DK|VS|SD|DM|L|C|E|B|D|A|UM)\.?\s*(\d{2,5}))?')
rows={}
for l in lines:
    for m in row.finditer(l):
        ser=int(m.group(1))
        if not 1<=ser<=1000: continue
        w=fixnum(m.group(2)); h=fixnum(m.group(3)) if m.group(3)!='?' else None
        ft=int(m.group(4)) if m.group(4) and int(m.group(4))<=30 else None
        if w: rows.setdefault(ser,{'w':w,'h':h,'ft':ft,'find':(m.group(7) or '')+' '+(m.group(8) or '')})
print("parsed serials:",len(rows))
im=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
im_by={}
for r in im:
    t=int(r['text_no'])
    if 1001<=t<=1905 and r['signs_clean'].strip() not in ('','0'): im_by.setdefault(t,r)
pairs=[(rows[s]['ft'],-int(im_by[1000+s]['level'])) for s in rows if 1000+s in im_by and rows[s]['ft'] is not None and im_by[1000+s]['level'].lstrip('-').isdigit()]
print("depth pairs (Marshall ft, IM77 -level):",len(pairs))
if len(pairs)>10:
    xs=[a for a,b in pairs]; ys=[b for a,b in pairs]
    mx,my=st.mean(xs),st.mean(ys)
    r=sum((a-mx)*(b-my) for a,b in pairs)/((sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))**0.5)
    print(f"Pearson r depth vs level code = {r:.2f}")
    print("cross-tab (ft -> IM77 level codes):",{k:collections.Counter(b for a,b in pairs if a==k).most_common(3) for k in sorted(set(xs))[:8]})
json.dump({str(k):v for k,v in rows.items()},open('data/marshall_seal_sizes.json','w'),indent=0)

# ---- F12 replication on Marshall sizes (independent measurement source) ----
import random
random.seed(7)
recs=[]
for ser,v in rows.items():
    r=im_by.get(1000+ser)
    if not r or r['object_type']!='seal': continue
    h=v['h'] if v['h'] else v['w']
    area=v['w']*h*645.16  # sq in -> mm2
    seq=[int(t) for t in r['signs_clean'].split()]
    recs.append((seq,area))
print("\nMIC seals with size+text:",len(recs),"; median area mm2:",round(st.median(a for _,a in recs)))
L=lambda s:min(len(s),8)
strata={}
for i,(s_,a) in enumerate(recs): strata.setdefault(L(s_),[]).append(i)
med={k:st.median(recs[i][1] for i in v) for k,v in strata.items()}
resid=[recs[i][1]-med[L(recs[i][0])] for i in range(len(recs))]
for sign,name in [(343,'M343 handled jar'),(342,'M342 plain jar'),(161,'M161 tree'),(176,'M176')]:
    w=[resid[i] for i in range(len(recs)) if sign in recs[i][0]]; wo=[resid[i] for i in range(len(recs)) if sign not in recs[i][0]]
    if len(w)<5: print(f"{name}: n={len(w)} too few"); continue
    obs=st.mean(w)-st.mean(wo); cnt=0
    for _ in range(4000):
        ph=set()
        for k,idx in strata.items():
            m=sum(1 for i in idx if sign in recs[i][0]); ph.update(random.sample(idx,m))
        d=st.mean(resid[i] for i in ph)-st.mean(resid[i] for i in range(len(recs)) if i not in ph)
        if abs(d)>=abs(obs): cnt+=1
    print(f"{name}: n_with={len(w)} delta_resid={obs:+.0f} mm2 ({obs/st.median(a for _,a in recs):+.0%} of median) perm p={cnt/4000:.4f}")
