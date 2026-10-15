"""Parse Mahadevan 1977 Appendix V (List of Inscribed Objects) OCR: text number -> excavation number, publication plate+serial.
Then validate the MIC and FEM joins against the Marshall/Mackay table rows via excavation numbers."""
import re, json, collections
txt=open('data/raw/books/Mahadevan1977_djvu.txt',encoding='utf-8',errors='replace').read().split('\n')
seg=[t.strip() for t in txt[163900:170400] if t.strip()]
# tokens: a 4-digit text number, then maybe exc no (digits, possibly with letters), then publ like 'MIC, Pl. CIV, 38' or 'FEM, Pl. LXXXIX, 360' or 'EH, Pl. XCI, 123' or museum no.
recs={}; i=0; n=len(seg)
tn=re.compile(r'^([1-9]\d{3})[.,]?$')
pub=re.compile(r'(MIC|FEM|EH|M1C|FFM|F EM|M IC)\s*[,.]?\s*P[1lI!]?[.,]?\s*([IVXLC1lJ]+)\s*[,.]?\s*(\d{1,3})',re.I)
while i<n:
    m=tn.match(seg[i])
    if m:
        t=int(m.group(1)); exc=None; publ=None
        for j in range(i+1,min(i+6,n)):
            s=seg[j]
            if tn.match(s): break
            pm=pub.search(s)
            if pm and publ is None:
                src=pm.group(1).upper().replace(' ',''); src={'M1C':'MIC','FFM':'FEM','FEM':'FEM','MIC':'MIC','EH':'EH'}.get(src,src)
                publ=(src,pm.group(2),int(pm.group(3)))
            elif exc is None and re.fullmatch(r'[A-Z]{0,3}\s?\d{2,6}[a-z]?',s): exc=s
        if t not in recs: recs[t]={'exc':exc,'publ':publ}
    i+=1
print("text numbers parsed:",len(recs))
mic={t:r['publ'][2] for t,r in recs.items() if r['publ'] and r['publ'][0]=='MIC'}
fem={t:r['publ'][2] for t,r in recs.items() if r['publ'] and r['publ'][0]=='FEM'}
print("with MIC serial:",len(mic)," with FEM serial:",len(fem))
# hypothesis checks
print("MIC: share where serial == text_no-1000:",round(sum(1 for t,s in mic.items() if s==t-1000)/max(1,len(mic)),2),
      " sample:",sorted(mic.items())[:8])
print("FEM: share where serial == text_no-2000:",round(sum(1 for t,s in fem.items() if s==t-2000)/max(1,len(fem)),2),
      " sample:",sorted(fem.items())[:8])
# alternative: offset distribution
off=collections.Counter(t-s for t,s in fem.items()); print("FEM text-serial offsets:",off.most_common(6))
offm=collections.Counter(t-s for t,s in mic.items()); print("MIC text-serial offsets:",offm.most_common(6))
json.dump({str(t):r for t,r in recs.items()},open('data/mahadevan_appendixV.json','w'),indent=0)
