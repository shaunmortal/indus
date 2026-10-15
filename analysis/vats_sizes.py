"""Parse Vats 1940 EH vol I 'Tabulation of Seals' (OCR token stream): plate running no., size W x H (in), level (ft' in"), type, colour, mound, find no.
Join: IM77 text_no = 4000 + EH running number (Mahadevan Appendix V convention; EH main series ends at 713 -> 4713). Validate by level. Then pooled replication MIC+FEM+EH."""
import re, json, csv, statistics as st, random, collections
txt=open('data/raw/books/Vats1940_vol1_text.txt',encoding='utf-8',errors='replace').read().split('\n')
toks=[t.strip() for t in txt[42780:57500] if t.strip()]
def num(s):
    s=s.replace('-','.').replace('*','.').replace('°','.').replace(':','.').replace("'",'.').replace('•','.').replace('·','.').replace('o','0').replace('O','0').replace('l','1').replace('I','1')
    s=re.sub(r'^r','1',s); s=s.replace('..','.')
    if re.fullmatch(r'[12]\d\d',s): s=s[0]+'.'+s[1:]
    elif re.fullmatch(r'0\d\d?',s): s='0.'+s[1:]
    elif re.fullmatch(r'[1-9]\d',s): s=s[0]+'.'+s[1:]
    elif re.fullmatch(r'\d',s): s='1.0' if s=='1' else '0.'+s
    try:
        v=float(s); return round(v,2) if 0.3<=v<=2.5 else None
    except: return None
SZ=re.compile(r"^([oO0-9rIl.:°'•·\-\*]{1,5})\s*[xX×]\s*([oO0-9rIl.:°'•·\-\*]{1,5})$")
rows={}; i=0; n=len(toks)
while i<n-3:
    if re.fullmatch(r'\d{1,3}',toks[i]) and 1<=int(toks[i])<=760:
        ser=int(toks[i]); j=i+1; m=None
        for j in range(i+1,min(i+4,n)):
            m=SZ.match(toks[j].replace(' ',''))
            if m: break
        if m:
            w=num(m.group(1)); h=num(m.group(2))
            if w and h:
                seg=' '.join(toks[j+1:j+12])
                lv=re.search(r"\b(?:(\d{1,2})|([IVX]{1,4}))\s*[\'’′]?\s*(\d{1,2})?\s*[\"”″\']*",seg)
                ft=None
                if 'surface' in seg.lower(): ft=0
                elif lv:
                    if lv.group(1): ft=int(lv.group(1))
                    elif lv.group(2): ft={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12}.get(lv.group(2))
                mound=re.search(r'\b(AB|F|D|E|ET|G|H|J)\b',seg)
                if ser not in rows: rows[ser]={'w':w,'h':h,'ft':ft,'mound':mound.group(1) if mound else '','seg':seg[:50]}
                i=j+1; continue
    i+=1
print("EH serials parsed:",len(rows),"range",min(rows),max(rows))
print("sample:",[(k,rows[k]['w'],rows[k]['h'],rows[k]['ft'],rows[k]['mound']) for k in sorted(rows)[:8]])
json.dump({str(k):v for k,v in rows.items()},open('data/vats_seal_sizes.json','w'),indent=0)
im=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
im_by={}
for r in im:
    if r['signs_clean'].strip() not in ('','0') and r['object_type']=='seal': im_by.setdefault(int(r['text_no']),r)
pairs=[(v['ft'],-int(im_by[4000+s]['level'])) for s,v in rows.items() if 4000+s in im_by and v['ft'] is not None and im_by[4000+s]['level'].lstrip('-').isdigit()]
print("depth pairs:",len(pairs)," exact:",round(sum(1 for a,b in pairs if a==b)/max(1,len(pairs)),2)," within1:",round(sum(1 for a,b in pairs if abs(a-b)<=1)/max(1,len(pairs)),2))
print("cross-tab:",{k:collections.Counter(b for a,b in pairs if a==k).most_common(3) for k in sorted(set(a for a,_ in pairs))[:10]})
