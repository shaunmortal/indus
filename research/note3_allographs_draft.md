# Looking alike is not behaving alike: an objective allograph test for the Indus sign list
### Ayush Kumar (India), with computational assistance from Claude. Draft v0.1, 15 October 2026.

## Problem
Three sign lists are in use (Mahadevan 417, Parpola about 400, Wells 676) and they disagree on which drawings are variants of one sign. Every count in the field depends on that decision, and it has been made by eye.

## Method
For each pair of Mahadevan signs with at least 15 tokens (104 signs, 5,356 pairs): (1) image similarity, the cosine between centred, cropped, 32x32 binarised drawings, flip-invariant; (2) distributional similarity, the cosine between profiles of left neighbour, right neighbour and position built on 2,409 distinct texts. Two signs are allograph candidates when both are high (image in the top 2%, distribution in the top 5%); they are look-alikes that are different signs when image is high and distribution is at or below the median. A mutual-nearest-neighbour check in distribution space is applied to candidates. Code: `analysis/model3_allographs.py`.

## Results
1. Across all pairs, image similarity and distributional similarity are uncorrelated: r = 0.05 against a permutation null of 0.00 +/- 0.05. How a sign looks says almost nothing about how it is used.
2. Fifteen allograph candidates. The strongest are mutual nearest neighbours: one short stroke drawn high or low (M97/M98: image 1.00, distribution 0.93, ranks 2/1), the fish variants M59/M67/M70/M72 (image 0.88-0.96, distribution 0.89-0.97, M70/M72 ranks 1/1), the handled jars M343/M344/M345 (M343/M344 ranks 1/1), M387/M389 (ranks 2/1), M347/M348, M326/M327, M12/M15, M102/M109.
3. Forty-one look-alikes that are different signs. The plain jar M342 against the handled jars M343/M344/M345: image 0.91-0.97, distribution 0.34-0.38, ranks 28-93 apart. Five tall against five short strokes (M96/M106): image 1.00, distribution 0.51. M149/M150: 0.94 against 0.17. Three tall strokes against six short in two rows (M89/M109): 0.91 against 0.58. The cup M328 against M336.

## Validation by prediction
Merging the eleven allograph pairs into a 406-sign list lowers held-out bigram perplexity on distinct texts from 29.0 to 26.3. Merging ten look-alike-but-distinct pairs instead gives 28.5. Sixty random merges of eleven frequent pairs give 28.6 +/- 0.3 (best 27.4). The algorithm's merges make the corpus more predictable by about seven standard deviations more than arbitrary merges do; the look-alike merges do no better than chance. Conditional entropy moves from 3.42 to 3.38 bits; hapax share is unchanged (29%).

## Adoption rule
Further candidates are adopted one at a time only if the held-out perplexity drop (five random 80/20 splits) beats a single-random-merge null by two standard deviations (threshold -0.136). Under this rule M14/M12 (-0.167) and M375/M387 (-0.182) are adopted; M386/M387 (-0.098) and the multi-tier stroke pair M121/M112 (-0.049) are not. The resulting list has 404 signs and perplexity 26.9 against about 29 for the published 417.

## Consequences
- Mahadevan over-split M97/M98 and the fish and handled-jar variants; the corrected list has 406 signs.
- Parpola's and Wells's practice of treating stroke groups of equal count as one numeral regardless of height or layout merges signs that the corpus keeps apart (M96/M106, M89/M109, and M102/M103 shown separately in note 1).
- The plain jar closer and the handled jar are different signs with different slots (closer vs mid-text), a distinction that matters for the seal-size result of note 2.
- The same procedure can be run on Wells's 676-sign list and, with photographs, on CISI, to produce a sign list that is defended by prediction rather than by eye.

## Limits
Drawings are Mahadevan's normalised forms, not photographs; rare signs (under 15 tokens) are untested; the distribution profile is bigram-level, which note 1 and `analysis/model2.py` show is the depth the corpus supports.
