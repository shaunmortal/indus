# Search map: everything tried so far (maintained; last update 2026-10-16)

Purpose: the standing order requires that a final verdict, whichever way, come with a complete map of what was searched. This file is that map. Details and numbers live in STATE.md (findings F1-F35, M1-M5, U1) and the reports in research/.

## A. Methods applied to the corpus itself (closed unless marked)
| Route | What was done | Verdict |
|---|---|---|
| Statistical key-fitting / dictionary hits | Inherited: Garg 2026 shows wrong keys beat the true key even on a planted language; Raghavendra 2026 refutes entropy-only language arguments | closed, do not pursue |
| Strokes as a number system | F1/F2/F5/F8/F15/F16/F20/F33/F34 on two transcriptions | not a number system on seals/tablets; pottery suggestive only (F33) |
| Kober-style paradigms (alternating endings) | F23 (retracted), corrected: alternation at chance (64 vs 58.6 +- 2.4); F32 robust to doubtful readings | no closed paradigm; no welded endings |
| Allographs / sign list | M3-M5, U1: image x distribution test validated by held-out perplexity; Mahadevan v3 (401), Wells v3 (586); bridge 176 signs | done; lists frozen |
| Function classes / grammar depth | M1b (K=3 only stable), M2 (bigram-deep), F21/F30 (blocks add nothing) | opener + core + closer, nothing finer |
| Physical correlates | F12 (M343 on smaller seals; the 1930s 're-analysis' uses the same measurements, F36; no support on the small independent metric subset, F37), F13, F14 (no sign x animal), F17 (no drift), F18, F19 (round-seal lexicon), F24 (no site dialect), F27 | shape and size correlate; emblem, site, date do not |
| What the texts are | F22, F25, F26 (96% unique), F28/F29 (title blocks, opener formulae), title_blocks_v1 (replicated) | personal identifiers: opener formula + individual + title block + closer |
| Tamil Nadu graffiti continuity | F31 (look-alikes do not behave alike, p = 0.51) | closed (side test) |
| Third side of incised tablets (circle-dots, untranscribed) | F40: 17 plate readings; 5/7 match the stroke count; values only 2-3 | open: transcribe all C sides (CISI vol. 1 pp. 223-233), then test |
| Hold-out / registry | 30% sealed (SHA-256 public), P1-P16 frozen, score_registry.py | ready; waiting for new inscriptions |

## B. Anchor routes (one object joining Indus signs to a readable script or a quantity)
| Place / source | Checked how | Result |
|---|---|---|
| Ur: Gadd 1932; UE III (Legrain 1936), UE IV, UE VII, UE X (Legrain 1951) | Gadd PDF; UE X and UE III read page by page via archive.org loan; UE IV/VII by paragorth | no Indus-sign impression on any tablet/bulla/sealing; hybrid-back seals (UE X 636-650) carry no signs; one ambiguous object U.17355 (Cat. 623) -> photo request drafted |
| Kish, Umma 2017 surface seal, Paris BnF seal, Nippur/Tell Asmar material | agent sweeps (research/umma_paris_seals.md, gulf_iran_sealings.md) | cuneiform-only or Indus-only; nothing bilingual |
| Failaka (Kjaerum 1983; F3/F6; 2025 temple finds) | literature sweep; Richter-Ushanas 'bilingual' traced | 2005 'bilingual' is fringe and the object unidentified; 2025 seals uncatalogued -> watch |
| Bahrain, Oman (Salut ST1 stamped jar, Ras al-Jinz), Iran (Susa text O, Konar Sandal, Tepe Yahya), Central Asia | agent sweeps (research/hybrid_seals_new_finds.md) | no object with Indus signs + readable script; Susa text O = aberrant Linear Elamite; both photos viewed 2026-10-16: no Indus-specific forms, closed |
| Museum collections abroad, finds 2018-2026 | agent sweep | zero new Indus-inscribed objects abroad since 2018 |
| India: Dholavira (Bisht 2015), Rakhigarhi 2011-26, Karanpura, Lothal L-56, Kanmer, Bhirrana, Farmana | reports/news sweeps (research/india_finds_2010-2026.md); L-56 checked on the CISI plate | Dholavira already in ICIT; Rakhigarhi seals unpublished; Karanpura's 4 objects already in corpus; L-56 Indus-only |
| Weights as a numeric anchor (PNAS 2021 dataset) | download blocked (publisher/PMC interstitial); literature note research/numerals_weights_lit.md | open: needs the xlsx via browser |
| Two-sided tablets (tall-N + cup formula) as quantities | F15, F33, F38, F39, P6/P16/P17; Wells's three Purana Qila pots (H-370-372) located in the corpus | formula with values {2,3,4}, never 5, rarely 1; value varies per issue within {2,3,4}; not shown to be counts |

## C. People and data access
| Who / what | Status |
|---|---|
| Dr Andreas Fuls (ICIT) | replied 2026-10-15: ICIT closed; our copy is an unauthorised, outdated snapshot without the completeness flag; asked for the export to be removed (decision pending with Ayush) |
| Dr Dennys Frenez | emailed 2026-10-15 (paper + correction); no reply yet; follow-up planned 2026-10-29 |
| Dr Nisha Yadav | no public address; via introduction |
| Prof. Asko Parpola (CISI editor) | emailed 2026-10-17 (helsinki.fi bounced; resent to his public gmail address) with the F40 observation; asked for vol. 3 plates of three-sided tablets |
| Wells 2015, Fuls 2022/2023 volumes | not on hand (sample PDF only); sign-list and table comparisons prepared (F34, note_wells2015_toc.md) |
| CISI vol. 3.1 (2010) | not on hand (only the 17-page front matter); needed for F33 pottery readings and the F40 three-sided tablets; scan request sent to the ASI library 2026-10-17; purchase option ~US$190 |

## D. Open watch (next sweep 2027-01)
Failaka F6 2025 seals; Rakhigarhi ASI seals; Konar Sandal; Tamil Nadu prize rules; any Gulf/Iran/Iraq find with Indus signs; U.17355 photo.
