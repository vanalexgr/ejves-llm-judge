# Final Comparator Report

## Dataset Summary

- Comparator responses: 48 total (`16` question stems x `3` models)
- Comparator models: GPT-5.5, Gemini 3.5 Flash, Claude Sonnet 4.6
- Original benchmark: reconstructed GPT-3.5 study set (`16` responses)
- Final comparator accuracy process: two blinded board-certified surgeon ratings for all `48` responses, with blinded third-surgeon adjudication for `5` initially disputed rows

## Accuracy Resolution Summary

| metric                     |   value |
|:---------------------------|--------:|
| total_comparator_responses |      48 |
| dual_surgeon_agreement     |      14 |
| dual_surgeon_mean          |      29 |
| triple_surgeon_median      |       5 |
| mario_explicit_revisions   |       2 |
| third_reviewer_cases       |       5 |

## Validated Endpoints By Model

`Accuracy`, `tone`, `complementarity`, `gilbert_urgency`, and treatment-only `DISCERN Q7` are the calibration-passing comparator endpoints. Lower urgency scores indicate stronger recommendation for urgent care.

| Model             |   Accuracy |   Tone |   Complementarity |   Urgency |   DISCERN Q7 (treatment) |
|:------------------|-----------:|-------:|------------------:|----------:|-------------------------:|
| GPT-5.5           |      3.688 |  1.656 |             0.875 |     1.906 |                    3.500 |
| Gemini 3.5 Flash  |      3.719 |  1.719 |             0.844 |     2.062 |                    3.125 |
| Claude Sonnet 4.6 |      3.312 |  1.781 |             0.875 |     2.062 |                    3.188 |

## Validated Endpoints Versus Original GPT-3.5 Benchmark

Positive `vs original` values indicate improvement. For urgency, the delta is sign-flipped so positive values mean more appropriate urgency signaling than the original GPT-3.5 benchmark.

| Endpoint        | Direction        |   Original GPT-3.5 study benchmark |   GPT-5.5 |   GPT-5.5 vs original |   Gemini 3.5 Flash |   Gemini 3.5 Flash vs original |   Claude Sonnet 4.6 |   Claude Sonnet 4.6 vs original |
|:----------------|:-----------------|-----------------------------------:|----------:|----------------------:|-------------------:|-------------------------------:|--------------------:|--------------------------------:|
| Accuracy        | Higher is better |                              3.271 |     3.688 |                 0.417 |              3.719 |                          0.448 |               3.312 |                           0.042 |
| Tone            | Higher is better |                              1.312 |     1.656 |                 0.344 |              1.719 |                          0.406 |               1.781 |                           0.469 |
| Complementarity | Higher is better |                              0.792 |     0.875 |                 0.083 |              0.844 |                          0.052 |               0.875 |                           0.083 |
| Urgency         | Lower is better  |                              2.104 |     1.906 |                 0.198 |              2.062 |                          0.042 |               2.062 |                           0.042 |
| DISCERN Q7      | Higher is better |                              3.042 |     3.500 |                 0.458 |              3.125 |                          0.083 |               3.188 |                           0.146 |

## Descriptive-Only Endpoints

`Comprehensiveness` and `clarity` are retained descriptively only because calibration showed low reliability for both humans and judges on these domains.

| Model             |   Comprehensiveness |   Clarity |
|:------------------|--------------------:|----------:|
| GPT-5.5           |               4.458 |     5.000 |
| Gemini 3.5 Flash  |               4.625 |     4.979 |
| Claude Sonnet 4.6 |               4.906 |     4.906 |

## Descriptive Endpoints Versus Original GPT-3.5 Benchmark

| Endpoint          | Direction        |   Original GPT-3.5 study benchmark |   GPT-5.5 |   GPT-5.5 vs original |   Gemini 3.5 Flash |   Gemini 3.5 Flash vs original |   Claude Sonnet 4.6 |   Claude Sonnet 4.6 vs original |
|:------------------|:-----------------|-----------------------------------:|----------:|----------------------:|-------------------:|-------------------------------:|--------------------:|--------------------------------:|
| Comprehensiveness | Higher is better |                              3.917 |     4.458 |                 0.542 |              4.625 |                          0.708 |               4.906 |                           0.990 |
| Clarity           | Higher is better |                              3.771 |     5.000 |                 1.229 |              4.979 |                          1.208 |               4.906 |                           1.135 |

## Interpretation

- Accuracy was fully resolved for all `48` comparator rows. The highest mean final validated accuracy was for Gemini 3.5 Flash (3.719), with GPT-5.5 close behind (3.688). Claude Sonnet 4.6 remained closest to the original GPT-3.5 benchmark on this endpoint.
- Tone improved for all three newer models relative to the reconstructed GPT-3.5 baseline. The most balanced overall tone was seen in Claude Sonnet 4.6 (1.781).
- Complementarity was broadly stable across models; GPT-5.5 and Claude Sonnet 4.6 matched each other on average, while Gemini 3.5 Flash was slightly lower.
- Urgency signaling remained strongest for GPT-5.5 because it produced the lowest mean urgency score (1.906).
- Treatment uncertainty handling (`DISCERN Q7`) was highest for GPT-5.5 (3.500).
- Descriptively, all three newer models were clearer and more comprehensive than the original GPT-3.5 benchmark, but these two domains should not be framed as validated primary endpoints.

## Recommended Manuscript Framing

1. Present the newer models as improved communicators relative to the original GPT-3.5 benchmark on the calibration-passing judged domains.
2. Present accuracy as a human-scored endpoint, not an AI-judged endpoint.
3. State explicitly that the comparator arm combined judge scoring for calibration-passing communication domains with blinded surgeon scoring for clinical accuracy.
4. Keep `comprehensiveness` and `clarity` in supplementary or descriptive tables only, with the calibration reliability caveat.
