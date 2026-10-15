# Wells 2015 (Archaeopress) — what the free sample tells us (2026-10-15)

Source: publisher sample PDF (17 pp: front matter, contents, lists of figures/tables, preface, introduction pp. 1-3). Saved as data/raw/books/Wells2015_sample.pdf (not in git). The sign list (ch. 2, pp. 13-22) is NOT in the sample. Book: 158 pp, GBP 25 paperback incl. PDF / GBP 16 PDF; not open access.

Corpus behind the book (preface): 3,903 artifacts, 4,794 texts, 17,650 sign occurrences, 695 signs (the ICIT state of 2009-2015). Our Wells corpus: 2,543 objects, 592 signs -> our copy is a SUBSET/SNAPSHOT (question put to Fuls 2026-10-15).

Chapters that map onto our results:
- Ch. 2 sign list; fig. 2.3 "five largest allographic sets"; fig. 2.4 graphemic vs allographic variation of signs 155/156/158. -> our §3 (allograph test M3-M5). Check whether 155/156/158 are among our adopted merges.
- Ch. 3 syntax; fig. 3.7 positions of ICTM (initial/connective/terminal/medial) -> our K=3 classes (M1b).
- Ch. 4 "Tablets, Pots and the Volumetric System of Harappa" (tables 4.1-4.2 Purana Qila vessel volumes) -> our F8 (two-sided tablets, tall-N + cup M328 formula). Wells reads these as quantities; we find a fixed formula with favoured N=3.
- Ch. 5 "Numerals" (fig. 5.1 basic stroke numerals; tables 5.1-5.3 right-adjacent collocations of short-linear, short-stacked, long-linear strokes; fig. 5.5 fish+numeral; fig. 5.6 numerals with sign 740 [jar]; fig. 5.7 sign 900 as positional-notation numeral; fig. 5.8 sign 055) -> our §2 (F1/F2/F5/F15/F16/F20). Direct counterpart; our complement-disjointness result is the same table computed on everything.
- Ch. 6 Proto-Dravidian readings, Dholavira signboard toponym (figs 6.8-6.11). Not engaged.
- App. I automated segmentation (z-score, multivariate) -> our F21/F30 (blocks add nothing beyond bigram).
- App. II positional analysis (Fuls): normalised positions, post-terminal signs, sign 550 bimodal -> our opener/closer classes.
- App. III power law classification (G = -1.347) -> not engaged.

Action taken: paper v0.4 §2 now cites Wells 2015 ch. 4-5 as the claim tested; References section added to the paper.
Open: buy Wells 2015 PDF (GBP 16) if budget allows, to check sign 155/156/158 and tables 5.1-5.3 against our numbers. Ayush's call.

## Check (2026-10-15): Wells fig. 2.4 set 155/156/158 against our distributional test
Distinct Wells texts (1,918); context vector = left+right neighbours; cosine percentile among all pairs of signs with freq >= 20 (median 0.27, 95th pct 0.70).
- 155-156: cos 0.69 (94th pct); 155-158: 0.63 (91st); 156-158: 0.67 (93rd). All three in the top decile, i.e. distributionally compatible with allography, but 155 has only 5 tokens and none of the three pairs reached our adoption rule (image similarity x 2-sd perplexity gain).
- 156-151: cos 0.92 (100th pct), our top allograph candidate for 156 (not adopted either; perplexity gain below 2 sd).
- 140-158 (our look-alike-distinct pair): cos 0.18 (38th pct) -> confirmed distinct.
- 31-32 (merged in Wells v3): cos 0.71 (95th pct); Wells fig. 5.3 treats 031/032 as numerals with syllabic use -> consistent with our 'interchangeable' result.
Reading: Wells's hand-picked allograph examples are the kind our test rates as similar-but-unproven; nothing contradicts either side. Decide after reading the chapter.
