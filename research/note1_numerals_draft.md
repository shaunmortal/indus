# Stroke signs in the Indus script are not a number system
### Ayush Kumar (India), with computational assistance from Claude. Draft v0.2, 15 October 2026.

## Claim
The short and tall vertical-stroke signs of the Indus script, usually read as numerals (ones and tens, or ones and a measure), do not behave like a number system in the Mahadevan 1977 corpus. They behave like two separate classes of formulaic signs. Four tests, all on distinct texts (2,409 distinct sign sequences; duplicates collapsed), all reproducible from `analysis/numerals*.py` and the open IM77 export.

## Data
Mahadevan 1977 / IDF-80 corpus, machine-readable export (indusscript.in, Roja Muthiah Research Library), 3,916 lines, 2,906 texts, 14,153 sign tokens, with site, object type and reading order. Stroke-sign inventory read from Mahadevan's own drawings (`data/stroke_signs.json`): short strokes 1-12 including two- and three-tier layouts (M97-M122), tall strokes 1-5 (M86-M96). The two-short-stroke sign (M99/M100, 649 tokens, 96% text-medial) is excluded as a connective: what follows it has cosine similarity 0.00-0.10 to what follows the 3-, 4-, 5- and 7-stroke signs.

## Test 1: numerals are not concentrated on accounting objects
Share of distinct texts containing a stroke sign: seals 56%, sealings 40%, miniature tablets 41%, pottery graffiti 46%, copper tablets 48%. If strokes recorded quantities, they should cluster on sealings and tablets. They cluster, if anywhere, on personal seals.

## Test 2: values are not distributed like quantities
Distinct-text counts, short strokes: 1 = 153, 3 = 114, 4 = 54, 5 = 34, 6 = 30, 7 = 64, 8 = 7, 9 = 4, 10 = 1, 12 = 52. Quantities decline monotonically (Benford-like). Here 7 and 12 are peaks: 12 (the three-tier 4-4-4 sign M121) outnumbers 8, 9 and 10 combined by four to one. Tall strokes: 1 = 134, 2 = 249, 3 = 182; 2 and 3 beat 1. These are favoured numbers, the signature of names and formulae.

## Test 3: no place value
If tall = tens and short = ones (Wells), compound numeral groups would have one fixed order and no tall-tall or short-short compounds. Observed adjacent numeral pairs on distinct texts: tall-short 17, short-tall 9, tall-tall 12, short-short 32.

## Test 4: tall and short strokes count different things
Signs that follow a stroke group, distinct texts, tall vs short: M211 42 vs 2, M328 20 vs 0, M60 13 vs 0, M244 11 vs 0, M284 11 vs 0; M287 0 vs 25, M25 0 vs 10, M190 1 vs 13, M162 6 vs 38, M169 5 vs 36. If tall strokes were tens of the same unit, every item counted in tens would also appear with ones. Instead the two stroke classes have nearly disjoint complements.

## Test 5 (partial): layout is a sign, not a style
Three short strokes in a row (M102, 151 tokens) is productive: its commonest follower takes 15%. Three short strokes as 2-over-1 (M103, 30 tokens) is bound: followed by M403 in 27 of 28 cases, at Mohenjo-daro (6/6) and Harappa (18/18), on seals, sealings and tablets, and on 11 of 12 distinct texts. Mahadevan numbered them separately; sign lists that merge layouts of the same count erase this.
(An apparent gradient of tall-stroke count with M328 proved to be a duplication artefact of Harappa tablets and is withdrawn.)

## Replication on an independent transcription
Tests 2-4 repeated on the ICIT/Wells corpus (Yajnadevam digitization, 1,918 distinct texts, G-sign numbers mapped to Mahadevan via the paragorth bridge; sequences reversed to reading order). Values: short 1 = 140, 3 = 116, 4 = 55, 5 = 30, 6 = 28, 7 = 46, 8 = 6, 12 = 36; tall 1 = 131, 2 = 227, 3 = 151. Compound orders: short-short 27, tall-tall 21, tall-short 21, short-tall 8. Complements: tall-only G520/M211 (40 vs 3), G226/M60 (13 vs 1); short-only G900/M287 (0 vs 23), G390/M161 (3 vs 47), G407/M169 (1 vs 16). The two corpora were transcribed by different scholars from different sign lists; the pattern is the same.

## Where each stroke class lives (two-sided objects)
Objects with two inscribed sides (Mahadevan corpus: 218 miniature tablets, 196 sealings) separate the two classes physically. Stroke signs sit on side 2 (tablets 79% vs 20%; sealings 65% vs 15%); the jar closer sits on side 1; side 1 is longer and more varied (105 vs 59 distinct texts on tablets), side 2 short and repetitive. Side-2 stroke signs are almost all tall (38 tall vs 8 short on distinct texts) and are followed by the cup sign M328: the Harappa formula "tall-N + cup", N = 3 (111 lines), 2 (74), 4 (50), 1 (7). Single-sided seals carry tall and short strokes in equal measure (421 vs 384) followed by a different set of signs. The tall-stroke formula is the administrative line on the reverse of a tablet; short strokes belong inside the name-like text on the obverse and on seals.

## A physical correlate
On 876 steatite square seals with measured faces (ICIT), controlling for site, text length and animal, one sign predicts seal size: the handled jar M343 (Wells 741), a mid-text sign, sits on seals about 25% smaller (delta -172 mm2, stratified permutation p = 0.0003, the only one of 36 signs to pass Bonferroni). The plain jar closer M342 has no size effect. Stroke value does not track size (tall rho = +0.12, p = 0.08; short rho = -0.04): if strokes were ranks, higher ranks do not buy larger seals.

## The "tens" that are not there
Parpola's decimal reading makes inverted semicircles the tens. In the Mahadevan corpus the semicircle signs (M312-M315: one, two, three and a stack of arcs) occur 2, 2, 1 and 1 times on distinct texts. The decimal system rests on six tokens. By contrast the jar and cup signs with strokes drawn inside them (M329, M330, M344, M345: 7, 7, 33, 41 tokens) are mid-text or initial elements on seals, never closers; the stroke count inside them is part of a word, not a quantity attached to it.

## Where the stroke signs sit in the only reproducible grammar
A stability-selected clustering of sign function (73 frequent signs, 20 resamples per K) supports exactly three classes: openers (M267, M391 and seven others), closers (the jar M342, M161, M176, M211, the cup M328 and eight others) and a core of 51 signs. Both stroke classes sit in the core; the cup that follows tall strokes on tablet reverses is a closer. Finer classes do not survive resampling (adjusted Rand 0.31 at twelve classes against 0.59 at three), so this note claims nothing finer.

## What this does and does not show
It does not say what the stroke signs mean. It says that the standard reading "stroke group = number of the following item" fails four independent tests on the only full open corpus, and that at least one layout distinction is lexical. Any decipherment that assigns numeric values to these signs must first explain Tests 1-4.

## Reproducibility
Code: `analysis/numerals1.py` to `numerals6.py`. Data: IM77 export (Mahadevan 1977, via indusscript.in; redistributed in github.com/paragorth/Indus- under MIT with attribution). Sign drawings: indusscript.in/assets/images/{0-417}.png.

## To do before circulation
- Compare with Mukhopadhyay 2019 (22 NUM signs; strokes precede CROP signs) sign by sign.
