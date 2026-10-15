# What the objects say: physical correlates of Indus signs
### Ayush Kumar (India), with computational assistance from Claude. Draft v0.1, 15 October 2026.

## Claim
Indus sign content is independent of almost every physical variable we can measure on the objects: animal emblem, excavation area, stratigraphic period, material. It is not independent of two: the SHAPE of the seal and the SIZE of the seal. The method is the same throughout: distinct objects, strata by site and text length (and object class where relevant), permutation of labels within strata, Bonferroni over all tests. Code: `analysis/size1-6.py`, `icon1.py`, `space1.py`, `material1.py`, `diachronic1.py`.

## Data
ICIT/Wells corpus (yajnadevam open database: 2,543 objects; 2,305 with measured width, height, thickness; 1,622 with iconography; 2,375 with CISI numbers) and the merged corpus of 5,369 objects with excavation area, period and object class (CISI metadata). Mahadevan 1977 corpus for replication where fields exist.

## 1. Seal size (positive)
876 steatite square seals with a measured face and a text, after site x text-length strata of at least five. Text length drives area (2 signs: median 467 mm2; 8 signs: 1,049 mm2), so every test is within length. Of 36 signs with 30 or more occurrences, one survives Bonferroni: the handled jar M343 (Wells 741), delta -172 mm2 on a median of about 700, p = 0.0003; still p = 0.0007 after adding animal to the strata. It holds at Mohenjo-daro (length 5-6: 619 vs 778; 7+: 869 vs 983) and Harappa (515 vs 713; 713 vs 1,452). M343 is a mid-text sign (151 of 176 in Mahadevan), preceded by M123 or M209, and co-occurs with the plain jar closer M342 on 56 of 94 seals. The closer itself has no size effect (713 vs 713). Stroke values do not track size (tall rho +0.12, p = 0.08; short -0.04). Unicorn seals are slightly larger (+92 mm2, p = 0.014), gaur seals smaller (-179, p = 0.012), seals without an animal smaller still (-255, p = 0.008).

Independent check. The 1931 and 1938 excavation reports tabulate seal dimensions (Marshall vol. II; Mackay vol. I). Mahadevan's text numbers are 1000 + MIC serial and 2000 + FEM serial (Appendix V), so the tables join to texts without the ICIT database. OCR parsing recovered 107 MIC and 278 FEM seals with text. Pooled, strata by source and length: M343 n = 33, delta -86 mm2 (-15%), one-sided p = 0.11; the plain jar again null. The direction holds, the magnitude is smaller and the test is not significant; whether the ICIT measurements derive from these same tables is unknown. The size result is therefore suggestive, not established, pending full parsing of the three excavation catalogues.

## 2. Seal shape (positive)
1,049 square vs 201 round seals, site x length strata, 121 tests. Round-favoured: M169 (ratio 4.0, p < 0.0005), W154 (3.0), M387 (3.0), one short stroke M97 (1.8, p = 0.002). Square-only: M343 (102 of 102), M161 (120 of 124), M402 (51 of 52). Per site, M169 is on 10.5% of round seals at Mohenjo-daro, 7.3% at Harappa, 6.2% at Lothal against 0.6%, 1.3%, 0% of square seals; M387 13%, 16%, 3% vs 1%, 4%, 2%; M343 0.5%, 0%, 0% vs 9.7%, 7.6%, 5.6%. The round-seal tradition carries its own small lexicon at every site, and the small-seal sign of section 1 belongs only to the square tradition.

## 3. Animal emblem (null)
1,032 seals with a recorded animal. Testing the rarer animals against the unicorn default, 21 animal x sign pairs with five or more observations: best gaur x M8, 7 vs 2.5 expected, p = 0.011; nothing passes Bonferroni (0.0024). Confirms, on a second corpus and coding, that no sign is tied to an emblem.

## 4. Excavation area (null)
Mohenjo-daro, 1,258 objects across eight areas (DK-G South 554, HR 201, DK-G North 120, DK-C 99, VS 95, DK-E 66, DK-B 63, DK-G 60); 225 tests; none passes Bonferroni (best p = 0.006). Harappa, 1,133 objects across five mounds; 113 tests; one survivor, M176 on Mound F (107 vs 87 expected, ratio 1.23), the mound of the oldest excavations, so a recording confound cannot be excluded. Signs are city-wide. No quarter, workshop or family signature appears in text content.

## 5. Period (null)
Mohenjo-daro Intermediate (401) vs Late (317): 76 tests, none passes (best tall-2 M87 in Late, p = 0.0015). Harappa 3B (530) vs 3C (412): none (best p = 0.016). Share of texts with stroke signs is flat across Harappa periods (31%, 31%, 38%). The repertoire did not drift measurably over the urban phases.

## 6. Material and object class
Material (steatite vs unrecorded): nothing. Incised tablets favour tall-2 M87 (27 vs 17, p = 0.001), the docket formula of note 1.

## Reading
Seal texts were not tied to where the seal was found, to its emblem or to its date. They were tied to what kind of seal it was and how large. That is the profile of personal names and titles carried by people, not of place or commodity labels. The two positive correlates give the first non-textual handles on two signs: M343 marks a cheaper square seal; M169 and M387 mark the round tradition.

## To do before circulation
- Replicate the size result on an independent measurement source (Marshall 1931 / Mackay 1938 catalogues).
- Check whether the Mound F / M176 survivor disappears when Vats' material is separated from HARP material.
- Hold-out (966 texts, hash published 2026-10-15) remains unread; none of the above used it as a prediction target.
