# Final Comparator Report

## Dataset Summary

- Comparator responses: 48 total (`16` question stems x `3` models)
- Comparator models: GPT-5.5, Gemini 3.5 Flash, Claude Sonnet 4.6
- Comparator collection mode: free consumer-facing model interfaces, copied into the scoring pipeline before judge evaluation
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

`Accuracy`, `tone`, `complementarity`, `gilbert_urgency`, and treatment-only `DISCERN Q7` are the calibration-passing comparator endpoints. Lower urgency scores indicate stronger recommendation for urgent care. Table entries below are mean scores with bootstrap 95% confidence intervals.

| Model             | Accuracy               | Tone                   | Complementarity        | Urgency                | DISCERN Q7 (treatment)   |
|:------------------|:-----------------------|:-----------------------|:-----------------------|:-----------------------|:-------------------------|
| GPT-5.5           | 3.688 (3.452 to 3.939) | 1.656 (1.469 to 1.812) | 0.875 (0.734 to 0.969) | 1.906 (1.546 to 2.283) | 3.500 (2.655 to 4.470)   |
| Gemini 3.5 Flash  | 3.719 (3.546 to 3.906) | 1.719 (1.594 to 1.844) | 0.844 (0.719 to 0.938) | 2.062 (1.531 to 2.500) | 3.125 (2.247 to 4.125)   |
| Claude Sonnet 4.6 | 3.312 (3.000 to 3.516) | 1.781 (1.656 to 1.906) | 0.875 (0.750 to 1.000) | 2.062 (1.734 to 2.391) | 3.188 (2.372 to 3.941)   |

## Validated Endpoints Versus Original GPT-3.5 Benchmark

Positive `vs original` values indicate improvement. For urgency, the delta is sign-flipped so positive values mean more appropriate urgency signaling than the original GPT-3.5 benchmark.

Detailed 95% bootstrap confidence intervals for these benchmark deltas are included in `validated_endpoint_comparison.csv` and `comparator_summary_tables.xlsx`.

| Endpoint        | Direction        |   Original GPT-3.5 study benchmark | Original GPT-3.5 study benchmark 95% CI   |   GPT-5.5 | GPT-5.5 95% CI   |   GPT-5.5 vs original | GPT-5.5 vs original 95% CI   |   Gemini 3.5 Flash | Gemini 3.5 Flash 95% CI   |   Gemini 3.5 Flash vs original | Gemini 3.5 Flash vs original 95% CI   |   Claude Sonnet 4.6 | Claude Sonnet 4.6 95% CI   |   Claude Sonnet 4.6 vs original | Claude Sonnet 4.6 vs original 95% CI   |
|:----------------|:-----------------|-----------------------------------:|:------------------------------------------|----------:|:-----------------|----------------------:|:-----------------------------|-------------------:|:--------------------------|-------------------------------:|:--------------------------------------|--------------------:|:---------------------------|--------------------------------:|:---------------------------------------|
| Accuracy        | Higher is better |                              3.271 | 2.927 to 3.657                            |     3.688 | 3.452 to 3.939   |                 0.417 | 0.010 to 0.902               |              3.719 | 3.546 to 3.906            |                          0.448 | 0.082 to 0.886                        |               3.312 | 3.000 to 3.516             |                           0.042 | -0.380 to 0.459                        |
| Tone            | Higher is better |                              1.312 | 1.208 to 1.438                            |     1.656 | 1.469 to 1.812   |                 0.344 | 0.108 to 0.583               |              1.719 | 1.594 to 1.844            |                          0.406 | 0.265 to 0.610                        |               1.781 | 1.656 to 1.906             |                           0.469 | 0.317 to 0.604                         |
| Complementarity | Higher is better |                              0.792 | 0.697 to 0.896                            |     0.875 | 0.734 to 0.969   |                 0.083 | -0.125 to 0.251              |              0.844 | 0.719 to 0.938            |                          0.052 | -0.156 to 0.208                       |               0.875 | 0.750 to 1.000             |                           0.083 | -0.062 to 0.266                        |
| Urgency         | Lower is better  |                              2.104 | 1.697 to 2.490                            |     1.906 | 1.546 to 2.283   |                 0.198 | -0.320 to 0.761              |              2.062 | 1.531 to 2.500            |                          0.042 | -0.547 to 0.677                       |               2.062 | 1.734 to 2.391             |                           0.042 | -0.453 to 0.474                        |
| DISCERN Q7      | Higher is better |                              3.042 | 2.833 to 3.230                            |     3.500 | 2.655 to 4.470   |                 0.458 | -0.407 to 1.250              |              3.125 | 2.247 to 4.125            |                          0.083 | -0.826 to 1.084                       |               3.188 | 2.372 to 3.941             |                           0.146 | -0.604 to 0.803                        |

## Descriptive-Only Endpoints

`Comprehensiveness` and `clarity` are retained descriptively only because the corrected manuscript Table 2 indicates that, at the original symptoms-topic sample size (`n = 4` diseases), human ICC(2,k) for these domains was not meaningfully estimable; the response-level judge calibration in this repository was likewise weak. These table entries are descriptive only and should not be cited as validated endpoints.

| Model             | Status                          | Comprehensiveness      | Clarity                |
|:------------------|:--------------------------------|:-----------------------|:-----------------------|
| GPT-5.5           | Descriptive only; not validated | 4.458 (4.328 to 4.615) | 5.000 (5.000 to 5.000) |
| Gemini 3.5 Flash  | Descriptive only; not validated | 4.625 (4.504 to 4.766) | 4.979 (4.948 to 5.000) |
| Claude Sonnet 4.6 | Descriptive only; not validated | 4.906 (4.828 to 4.979) | 4.906 (4.802 to 4.990) |

## Descriptive Endpoints Versus Original GPT-3.5 Benchmark

| Endpoint          | Direction        |   Original GPT-3.5 study benchmark | Original GPT-3.5 study benchmark 95% CI   | Status                          |   GPT-5.5 | GPT-5.5 95% CI   |   GPT-5.5 vs original | GPT-5.5 vs original 95% CI   |   Gemini 3.5 Flash | Gemini 3.5 Flash 95% CI   |   Gemini 3.5 Flash vs original | Gemini 3.5 Flash vs original 95% CI   |   Claude Sonnet 4.6 | Claude Sonnet 4.6 95% CI   |   Claude Sonnet 4.6 vs original | Claude Sonnet 4.6 vs original 95% CI   |
|:------------------|:-----------------|-----------------------------------:|:------------------------------------------|:--------------------------------|----------:|:-----------------|----------------------:|:-----------------------------|-------------------:|:--------------------------|-------------------------------:|:--------------------------------------|--------------------:|:---------------------------|--------------------------------:|:---------------------------------------|
| Comprehensiveness | Higher is better |                              3.917 | 3.697 to 4.136                            | Descriptive only; not validated |     4.458 | 4.328 to 4.615   |                 0.542 | 0.270 to 0.755               |              4.625 | 4.504 to 4.766            |                          0.708 | 0.462 to 0.953                        |               4.906 | 4.828 to 4.979             |                           0.990 | 0.760 to 1.203                         |
| Clarity           | Higher is better |                              3.771 | 3.604 to 3.990                            | Descriptive only; not validated |     5.000 | 5.000 to 5.000   |                 1.229 | 1.020 to 1.417               |              4.979 | 4.948 to 5.000            |                          1.208 | 1.026 to 1.417                        |               4.906 | 4.802 to 4.990             |                           1.135 | 0.911 to 1.302                         |

## Interpretation

- Accuracy was fully resolved for all `48` comparator rows. The highest mean final validated accuracy was for Gemini 3.5 Flash (3.719), with GPT-5.5 close behind (3.688). Claude Sonnet 4.6 remained closest to the original GPT-3.5 benchmark on this endpoint.
- Tone improved for all three newer models relative to the reconstructed GPT-3.5 baseline. The most balanced overall tone was seen in Claude Sonnet 4.6 (1.781).
- Complementarity was broadly stable across models; GPT-5.5 and Claude Sonnet 4.6 matched each other on average, while Gemini 3.5 Flash was slightly lower.
- Urgency signaling remained strongest for GPT-5.5 because it produced the lowest mean urgency score (1.906).
- Treatment uncertainty handling (`DISCERN Q7`) was highest for GPT-5.5 (3.500).
- Descriptively, all three newer models were clearer and more comprehensive than the original GPT-3.5 benchmark, but these two domains should not be framed as validated primary endpoints. The corrected Table 2 interpretation is that the original human topic-level signal for these constructs was itself unstable or non-estimable at this sample size.

## Measurement And Review Process Caveats

- Mixed measurement arms apply across time: the original GPT-3.5 benchmark uses the reconstructed historical human-consensus ratings, whereas comparator accuracy uses the later dual-surgeon plus adjudication workflow. These benchmark comparisons are therefore pragmatic rather than perfectly instrument-equivalent.
- VGA served as one of the two comparator-arm accuracy raters and is disclosed here as a board-certified surgeon rather than as an independent historical reviewer from the original study set. The mitigation was full blinding to model identity during the initial scoring round, followed by third-rater adjudication for the rows with large disagreement.
- Mario made `2` explicit post-round score revisions after reviewing the rationale set. Those revisions were retained in the audit trail rather than silently overwritten, and both rows remained inside the disagreement-managed workflow instead of being used to bypass adjudication.
- The `5/48` adjudication cases represent a 10.4% third-review rate. This should be interpreted as an expected signal-detection feature of the clinical accuracy workflow, not as evidence that the adjudication process failed.

## Recommended Manuscript Framing

1. Present the newer models as improved communicators relative to the original GPT-3.5 benchmark on the calibration-passing judged domains.
2. Present accuracy as a human-scored endpoint, not an AI-judged endpoint.
3. State explicitly that the comparator arm combined judge scoring for calibration-passing communication domains with blinded surgeon scoring for clinical accuracy.
4. State explicitly that tone, complementarity, and DISCERN-Q7 were floor-passing domains with more modest absolute agreement than urgency, so they should be read as usable-with-caution rather than as strong psychometric validations.
5. Keep `comprehensiveness` and `clarity` in supplementary or descriptive tables only, with the corrected Table 2 caveat that the original topic-level human reliability for these constructs was not meaningfully estimable at this sample size.
