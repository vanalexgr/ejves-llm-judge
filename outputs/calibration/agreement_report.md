# Agreement Report

Dataset summary: 16 responses, 3 human reviewers (MDO, WD, EG), 2 judges, 3 runs per judge/response, and 96 total scored calls. Claude model: `claude-opus-4-7`. OpenAI model: `gpt-5`.

Aggregation rules: within each judge, ordinal items use the median across 3 runs, binary complementarity uses the mode, and Likert items use the mean. Human consensus uses the same rules across the 3 reviewers. The ensemble is the mean of the two judges per response. Weighted kappa and confusion matrices use nearest-valid-category rounding when aggregation produces fractional values; ICC and Bland–Altman analyses use the raw continuous aggregates.

## Section 1: Summary Table

Verdict logic: PASS requires the explicit CODEX threshold when one exists and also requires ensemble-vs-consensus agreement to be at least as high as the minimum pairwise inter-human agreement for the same item. REVIEW means only one criterion is met, or no explicit threshold exists and the result falls short of the inter-human floor. FAIL means both explicit criteria fail. Because some inter-human floors are negative, a PASS verdict should be read as a rule-based calibration pass rather than as a blanket psychometric endorsement; absolute agreement can still be modest, especially for tone and other floor-only domains.

Key stopping signal for accuracy: after the Track B anchor revision, Claude and GPT-5 moved in opposite directions (weighted κ = -0.222 vs 0.255), indicating that the revised rubric did not produce a stable convergent target across judges. Further tuning was therefore stopped to avoid circular optimisation on the same 16-response calibration set.

| rubric_item       | primary_metric_name      |   kappa | kappa_95_ci     | icc_2_1   | icc_2_1_95_ci   |   spearman_rho |   interhuman_floor | verdict   |
|:------------------|:-------------------------|--------:|:----------------|:----------|:----------------|---------------:|-------------------:|:----------|
| Tone              | weighted_kappa_quadratic |   0.2   | -0.144 to 0.529 | NA        | NA              |          0.311 |             -0.308 | PASS      |
| Gilbert Urgency   | weighted_kappa_quadratic |   0.709 | -0.022 to 0.971 | NA        | NA              |          0.58  |              0.147 | PASS      |
| Discern Q7        | weighted_kappa_quadratic |   0.308 | -0.193 to 0.637 | NA        | NA              |          0.232 |             -0.778 | PASS      |
| Complementarity   | kappa_unweighted         |   0.294 | -0.110 to 0.793 | NA        | NA              |          0.303 |             -0.12  | PASS      |
| Accuracy          | weighted_kappa_quadratic |   0.128 | -0.386 to 0.622 | 0.137     | -0.459 to 0.542 |         -0.017 |              0.195 | FAIL      |
| Comprehensiveness | weighted_kappa_quadratic |   0.059 | -0.345 to 0.434 | 0.129     | -0.196 to 0.308 |          0.17  |             -0.198 | REVIEW    |
| Clarity           | weighted_kappa_quadratic |  -0.053 | -0.233 to 0.125 | -0.025    | -0.197 to 0.151 |         -0.113 |             -0.278 | REVIEW    |

Plots:
- Bland–Altman Accuracy: [agreement_plots/bland_altman_accuracy.png](agreement_plots/bland_altman_accuracy.png)
- Bland–Altman Comprehensiveness: [agreement_plots/bland_altman_comprehensiveness.png](agreement_plots/bland_altman_comprehensiveness.png)
- Bland–Altman Clarity: [agreement_plots/bland_altman_clarity.png](agreement_plots/bland_altman_clarity.png)
- Confusion matrix Tone: [agreement_plots/confusion_tone.png](agreement_plots/confusion_tone.png)
- Confusion matrix Gilbert Urgency: [agreement_plots/confusion_gilbert_urgency.png](agreement_plots/confusion_gilbert_urgency.png)
- Confusion matrix Discern Q7: [agreement_plots/confusion_discern_q7.png](agreement_plots/confusion_discern_q7.png)
- Confusion matrix Accuracy: [agreement_plots/confusion_accuracy.png](agreement_plots/confusion_accuracy.png)
- Confusion matrix Comprehensiveness: [agreement_plots/confusion_comprehensiveness.png](agreement_plots/confusion_comprehensiveness.png)
- Confusion matrix Clarity: [agreement_plots/confusion_clarity.png](agreement_plots/confusion_clarity.png)

## Section 2: Per-Judge Breakdown

### Claude

| rubric_item       | primary_metric_name      |   kappa | kappa_95_ci     | icc_2_1   | icc_2_1_95_ci   |   spearman_rho |   interhuman_floor | verdict   |
|:------------------|:-------------------------|--------:|:----------------|:----------|:----------------|---------------:|-------------------:|:----------|
| Tone              | weighted_kappa_quadratic |   0.31  | -0.153 to 0.709 | NA        | NA              |          0.313 |             -0.308 | PASS      |
| Gilbert Urgency   | weighted_kappa_quadratic |   0.653 | -0.041 to 0.950 | NA        | NA              |          0.58  |              0.147 | PASS      |
| Discern Q7        | weighted_kappa_quadratic |   0.125 | -0.600 to 0.818 | NA        | NA              |          0.178 |             -0.778 | PASS      |
| Complementarity   | kappa_unweighted         |   0.294 | -0.110 to 0.793 | NA        | NA              |          0.303 |             -0.12  | PASS      |
| Accuracy          | weighted_kappa_quadratic |  -0.222 | -0.511 to 0.186 | -0.294    | -0.694 to 0.092 |         -0.3   |              0.195 | FAIL      |
| Comprehensiveness | weighted_kappa_quadratic |   0.048 | -0.325 to 0.396 | 0.016     | -0.468 to 0.262 |         -0.06  |             -0.198 | REVIEW    |
| Clarity           | weighted_kappa_quadratic |  -0.077 | -0.299 to 0.165 | -0.038    | -0.297 to 0.197 |         -0.158 |             -0.278 | REVIEW    |

### GPT-5

| rubric_item       | primary_metric_name      |   kappa | kappa_95_ci      | icc_2_1   | icc_2_1_95_ci   |   spearman_rho |   interhuman_floor | verdict   |
|:------------------|:-------------------------|--------:|:-----------------|:----------|:----------------|---------------:|-------------------:|:----------|
| Tone              | weighted_kappa_quadratic |   0.2   | -0.144 to 0.529  | NA        | NA              |          0.244 |             -0.308 | PASS      |
| Gilbert Urgency   | weighted_kappa_quadratic |   0.709 | -0.022 to 0.971  | NA        | NA              |          0.58  |              0.147 | PASS      |
| Discern Q7        | weighted_kappa_quadratic |   0.257 | -0.156 to 0.615  | NA        | NA              |          0.37  |             -0.778 | PASS      |
| Complementarity   | kappa_unweighted         |   0.294 | -0.110 to 0.793  | NA        | NA              |          0.303 |             -0.12  | PASS      |
| Accuracy          | weighted_kappa_quadratic |   0.255 | -0.120 to 0.694  | 0.376     | -0.101 to 0.666 |          0.202 |              0.195 | REVIEW    |
| Comprehensiveness | weighted_kappa_quadratic |   0.215 | 0.000 to 0.443   | 0.209     | -0.022 to 0.347 |          0.374 |             -0.198 | REVIEW    |
| Clarity           | weighted_kappa_quadratic |  -0.122 | -0.246 to -0.037 | -0.013    | -0.158 to 0.092 |         -0.014 |             -0.278 | REVIEW    |

## Section 3: Judge-vs-Individual-Human Matrix

Each table reports the primary agreement metric for that rubric item: quadratic weighted kappa for ordinal/Likert items and unweighted kappa for complementarity. Negative values mean the judge moved against the human reference standard rather than merely adding random noise.

### Tone

| Judge   |   MDO | MDO 95% CI      |     WD | WD 95% CI       |    EG | EG 95% CI       |   Min human-human |   Mean human-human |
|:--------|------:|:----------------|-------:|:----------------|------:|:----------------|------------------:|-------------------:|
| Claude  |  0.25 | -0.226 to 0.748 | -0.161 | -0.540 to 0.165 | 0.333 | 0.021 to 0.586  |            -0.308 |             -0.061 |
| GPT-5   |  0.5  | 0.074 to 0.871  | -0.091 | -0.540 to 0.250 | 0.25  | -0.061 to 0.444 |            -0.308 |             -0.061 |

### Gilbert Urgency

| Judge   |   MDO | MDO 95% CI      |    WD | WD 95% CI      |    EG | EG 95% CI       |   Min human-human |   Mean human-human |
|:--------|------:|:----------------|------:|:---------------|------:|:----------------|------------------:|-------------------:|
| Claude  | 0.603 | -0.041 to 1.000 | 0.399 | 0.070 to 0.690 | 0.492 | -0.177 to 0.887 |             0.147 |              0.329 |
| GPT-5   | 0.65  | -0.022 to 1.000 | 0.413 | 0.055 to 0.697 | 0.54  | -0.177 to 0.963 |             0.147 |              0.329 |

### Discern Q7

| Judge   |   MDO | MDO 95% CI      |    WD | WD 95% CI       |     EG | EG 95% CI        |   Min human-human |   Mean human-human |
|:--------|------:|:----------------|------:|:----------------|-------:|:-----------------|------------------:|-------------------:|
| Claude  | 0.458 | -0.002 to 0.661 |  0.1  | -0.290 to 0.462 | -0.375 | -0.789 to -0.031 |            -0.778 |             -0.262 |
| GPT-5   | 0.574 | -0.060 to 0.808 | -0.07 | -0.386 to 0.209 | -0.593 | -0.908 to -0.129 |            -0.778 |             -0.262 |

### Complementarity

| Judge   |   MDO | MDO 95% CI     |     WD | WD 95% CI       |    EG | EG 95% CI       |   Min human-human |   Mean human-human |
|:--------|------:|:---------------|-------:|:----------------|------:|:----------------|------------------:|-------------------:|
| Claude  |  0.59 | 0.000 to 1.000 | -0.103 | -0.306 to 0.000 | 0.259 | -0.217 to 0.692 |             -0.12 |              0.012 |
| GPT-5   |  0.59 | 0.000 to 1.000 | -0.103 | -0.306 to 0.000 | 0.259 | -0.217 to 0.692 |             -0.12 |              0.012 |

### Accuracy

| Judge   |    MDO | MDO 95% CI      |     WD | WD 95% CI       |     EG | EG 95% CI       |   Min human-human |   Mean human-human |
|:--------|-------:|:----------------|-------:|:----------------|-------:|:----------------|------------------:|-------------------:|
| Claude  | -0.111 | -0.410 to 0.125 | -0.259 | -0.458 to 0.124 | -0.163 | -0.369 to 0.088 |             0.195 |              0.439 |
| GPT-5   |  0.189 | -0.193 to 0.454 |  0.298 | -0.052 to 0.648 |  0.241 | -0.085 to 0.581 |             0.195 |              0.439 |

### Comprehensiveness

| Judge   |   MDO | MDO 95% CI      |     WD | WD 95% CI       |    EG | EG 95% CI       |   Min human-human |   Mean human-human |
|:--------|------:|:----------------|-------:|:----------------|------:|:----------------|------------------:|-------------------:|
| Claude  | 0.036 | -0.166 to 0.163 | -0.176 | -0.411 to 0.086 | 0.247 | -0.231 to 0.694 |            -0.198 |             -0.064 |
| GPT-5   | 0.109 | -0.022 to 0.258 |  0.025 | -0.342 to 0.280 | 0.507 | 0.144 to 0.766  |            -0.198 |             -0.064 |

### Clarity

| Judge   |    MDO | MDO 95% CI      |     WD | WD 95% CI       |     EG | EG 95% CI       |   Min human-human |   Mean human-human |
|:--------|-------:|:----------------|-------:|:----------------|-------:|:----------------|------------------:|-------------------:|
| Claude  |  0.2   | -0.200 to 0.478 | -0.302 | -0.505 to 0.088 |  0.13  | 0.023 to 0.211  |            -0.278 |             -0.085 |
| GPT-5   | -0.067 | -0.333 to 0.341 | -0.045 | -0.333 to 0.163 | -0.016 | -0.088 to 0.068 |            -0.278 |             -0.085 |

## Section 4: Inter-Human Reliability

### Pairwise Human Agreement

| rubric_item       | reviewer_pair   | primary_metric_name      |   primary_metric | primary_metric_95_ci   |
|:------------------|:----------------|:-------------------------|-----------------:|:-----------------------|
| Tone              | MDO vs WD       | weighted_kappa_quadratic |            0.125 | -0.355 to 0.619        |
| Gilbert Urgency   | MDO vs WD       | weighted_kappa_quadratic |            0.191 | -0.163 to 0.573        |
| Discern Q7        | MDO vs WD       | weighted_kappa_quadratic |           -0.174 | -0.474 to 0.000        |
| Complementarity   | MDO vs WD       | kappa_unweighted         |           -0.103 | -0.231 to 0.000        |
| Accuracy          | MDO vs WD       | weighted_kappa_quadratic |            0.636 | 0.367 to 0.806         |
| Comprehensiveness | MDO vs WD       | weighted_kappa_quadratic |           -0.069 | -0.392 to 0.212        |
| Clarity           | MDO vs WD       | weighted_kappa_quadratic |           -0.278 | -0.462 to 0.019        |
| Tone              | MDO vs EG       | weighted_kappa_quadratic |            0     | -0.458 to 0.276        |
| Gilbert Urgency   | MDO vs EG       | weighted_kappa_quadratic |            0.65  | -0.022 to 1.000        |
| Discern Q7        | MDO vs EG       | weighted_kappa_quadratic |           -0.778 | -0.904 to -0.124       |
| Complementarity   | MDO vs EG       | kappa_unweighted         |            0.259 | -0.262 to 0.673        |
| Accuracy          | MDO vs EG       | weighted_kappa_quadratic |            0.195 | 0.031 to 0.307         |
| Comprehensiveness | MDO vs EG       | weighted_kappa_quadratic |            0.076 | -0.086 to 0.173        |
| Clarity           | MDO vs EG       | weighted_kappa_quadratic |            0.077 | -0.175 to 0.262        |
| Tone              | WD vs EG        | weighted_kappa_quadratic |           -0.308 | -0.580 to -0.091       |
| Gilbert Urgency   | WD vs EG        | weighted_kappa_quadratic |            0.147 | -0.345 to 0.554        |
| Discern Q7        | WD vs EG        | weighted_kappa_quadratic |            0.165 | 0.010 to 0.333         |
| Complementarity   | WD vs EG        | kappa_unweighted         |           -0.12  | -0.333 to 0.000        |
| Accuracy          | WD vs EG        | weighted_kappa_quadratic |            0.485 | 0.177 to 0.689         |
| Comprehensiveness | WD vs EG        | weighted_kappa_quadratic |           -0.198 | -0.586 to 0.055        |
| Clarity           | WD vs EG        | weighted_kappa_quadratic |           -0.053 | -0.299 to 0.166        |

### ICC Comparison to Manuscript Table 2

| rubric_item       |   icc_2_1 | icc_2_1_95_ci   |   manuscript_table2 |   delta_vs_manuscript |
|:------------------|----------:|:----------------|--------------------:|----------------------:|
| Accuracy          |     0.446 | 0.221 to 0.538  |                0.83 |                -0.384 |
| Comprehensiveness |    -0.061 | -0.181 to 0.076 |                0    |                -0.061 |
| Clarity           |    -0.067 | -0.216 to 0.089 |                0    |                -0.067 |

Note: the manuscript Table 2 was later corrected. The symptoms-topic JASP analysis retains Accuracy at 0.83, but Clarity and Comprehensiveness are now treated as non-estimable at that sample size (0.00 if floored from non-positive raw ICC estimates). The response-level ICC(2,1) values above are reconstructed directly from the source reviewer spreadsheets across the 16 response-level items, so they are an audit-side calibration view rather than a strict reprint of the manuscript's topic-level Table 2.

## Section 4b: Symptoms-subset inter-human ICC(2,k)

Symptoms subset: `8` responses with `question_group == 'symptoms'`. Treatment subset: `8` responses with `question_group == 'treatment'`. ICC in this subsection uses two-way random absolute agreement average measures, i.e. ICC(A,k) / ICC(2,k). The originally submitted manuscript Table 2, however, was based on a symptoms-topic JASP file with `n = 4` disease topics rather than these 8 response-level symptom items, so the comparison is contextual rather than a one-to-one numeric reproduction.

### Symptoms-only Pairwise Human Agreement

| rubric_item       | reviewer_pair   | primary_metric_name      | primary_metric   | primary_metric_95_ci   |
|:------------------|:----------------|:-------------------------|:-----------------|:-----------------------|
| Tone              | MDO vs WD       | weighted_kappa_quadratic | 0.059            | -0.500 to 0.660        |
| Gilbert Urgency   | MDO vs WD       | weighted_kappa_quadratic | 0.297            | 0.000 to 0.643         |
| Discern Q7        | MDO vs WD       | weighted_kappa_quadratic | NA               | NA                     |
| Complementarity   | MDO vs WD       | kappa_unweighted         | 0.000            | 0.000 to 0.000         |
| Accuracy          | MDO vs WD       | weighted_kappa_quadratic | 0.636            | 0.000 to 0.897         |
| Comprehensiveness | MDO vs WD       | weighted_kappa_quadratic | -0.116           | -0.342 to 0.679        |
| Clarity           | MDO vs WD       | weighted_kappa_quadratic | -0.273           | -0.545 to 0.439        |
| Tone              | MDO vs EG       | weighted_kappa_quadratic | 0.176            | -0.360 to 0.667        |
| Gilbert Urgency   | MDO vs EG       | weighted_kappa_quadratic | 0.669            | -0.158 to 1.000        |
| Discern Q7        | MDO vs EG       | weighted_kappa_quadratic | NA               | NA                     |
| Complementarity   | MDO vs EG       | kappa_unweighted         | 0.143            | -0.421 to 0.879        |
| Accuracy          | MDO vs EG       | weighted_kappa_quadratic | 0.043            | -0.167 to 0.273        |
| Comprehensiveness | MDO vs EG       | weighted_kappa_quadratic | -0.055           | -0.296 to 0.189        |
| Clarity           | MDO vs EG       | weighted_kappa_quadratic | -0.130           | -0.631 to 0.123        |
| Tone              | WD vs EG        | weighted_kappa_quadratic | -0.130           | -0.491 to 0.282        |
| Gilbert Urgency   | WD vs EG        | weighted_kappa_quadratic | 0.247            | 0.000 to 0.569         |
| Discern Q7        | WD vs EG        | weighted_kappa_quadratic | NA               | NA                     |
| Complementarity   | WD vs EG        | kappa_unweighted         | 0.000            | 0.000 to 0.000         |
| Accuracy          | WD vs EG        | weighted_kappa_quadratic | 0.419            | 0.000 to 0.706         |
| Comprehensiveness | WD vs EG        | weighted_kappa_quadratic | -0.222           | -0.485 to 0.176        |
| Clarity           | WD vs EG        | weighted_kappa_quadratic | 0.032            | -0.267 to 0.435        |

### Symptoms-only ICC(2,k) vs Manuscript Table 2

| rubric_item       | icc_type   |   icc_2_k | icc_2_k_95_ci   |   manuscript_table2 |   delta_vs_manuscript |
|:------------------|:-----------|----------:|:----------------|--------------------:|----------------------:|
| Accuracy          | ICC(A,k)   |     0.667 | -0.000 to 0.838 |                0.83 |                -0.163 |
| Comprehensiveness | ICC(A,k)   |    -0.889 | -2.393 to 0.159 |                0    |                -0.889 |
| Clarity           | ICC(A,k)   |    -0.485 | -1.676 to 0.010 |                0    |                -0.485 |

The corrected manuscript interpretation is that Accuracy remained estimable and good at the symptoms-topic level (ICC[2,k] = 0.83), whereas Clarity and Comprehensiveness were effectively non-estimable at that sample size (reported as 0.00 if floored from non-positive raw estimates). The response-level subset shown above is still useful as a calibration stress test, but it should not be read as a literal recreation of the manuscript Table 2 workflow.

### Treatment-only Pairwise Human Agreement

| rubric_item       | reviewer_pair   | primary_metric_name      |   primary_metric | primary_metric_95_ci   |
|:------------------|:----------------|:-------------------------|-----------------:|:-----------------------|
| Tone              | MDO vs WD       | weighted_kappa_quadratic |            0.333 | 0.000 to 1.000         |
| Gilbert Urgency   | MDO vs WD       | weighted_kappa_quadratic |           -0.086 | -0.403 to 0.375        |
| Discern Q7        | MDO vs WD       | weighted_kappa_quadratic |           -0.174 | -0.474 to 0.000        |
| Complementarity   | MDO vs WD       | kappa_unweighted         |           -0.143 | -0.333 to 0.000        |
| Accuracy          | MDO vs WD       | weighted_kappa_quadratic |            0.636 | 0.000 to 0.871         |
| Comprehensiveness | MDO vs WD       | weighted_kappa_quadratic |           -0.071 | -0.613 to 0.167        |
| Clarity           | MDO vs WD       | weighted_kappa_quadratic |           -0.214 | -0.574 to 0.167        |
| Tone              | MDO vs EG       | weighted_kappa_quadratic |           -0.556 | -1.000 to 0.000        |
| Gilbert Urgency   | MDO vs EG       | weighted_kappa_quadratic |            0.6   | 0.000 to 1.000         |
| Discern Q7        | MDO vs EG       | weighted_kappa_quadratic |           -0.778 | -0.904 to -0.124       |
| Complementarity   | MDO vs EG       | kappa_unweighted         |            0.385 | 0.000 to 1.000         |
| Accuracy          | MDO vs EG       | weighted_kappa_quadratic |            0.259 | 0.131 to 0.310         |
| Comprehensiveness | MDO vs EG       | weighted_kappa_quadratic |            0.115 | 0.008 to 0.193         |
| Clarity           | MDO vs EG       | weighted_kappa_quadratic |            0.192 | 0.010 to 0.367         |
| Tone              | WD vs EG        | weighted_kappa_quadratic |           -0.333 | -0.580 to 0.000        |
| Gilbert Urgency   | WD vs EG        | weighted_kappa_quadratic |           -0.306 | -0.529 to 0.000        |
| Discern Q7        | WD vs EG        | weighted_kappa_quadratic |            0.165 | 0.010 to 0.333         |
| Complementarity   | WD vs EG        | kappa_unweighted         |           -0.231 | -0.600 to 0.000        |
| Accuracy          | WD vs EG        | weighted_kappa_quadratic |            0.4   | -0.058 to 0.520        |
| Comprehensiveness | WD vs EG        | weighted_kappa_quadratic |           -0.358 | -0.594 to 0.000        |
| Clarity           | WD vs EG        | weighted_kappa_quadratic |           -0.5   | -0.849 to 0.000        |

### Treatment-only ICC(2,k)

| rubric_item       | icc_type   |   icc_2_k | icc_2_k_95_ci   |
|:------------------|:-----------|----------:|:----------------|
| Accuracy          | ICC(A,k)   |     0.713 | 0.220 to 0.776  |
| Comprehensiveness | ICC(A,k)   |    -0.202 | -0.879 to 0.219 |
| Clarity           | ICC(A,k)   |    -0.273 | -1.071 to 0.184 |

## Section 5: Notable Disagreements

No response had an absolute ensemble-vs-consensus Likert difference of 2 or more.

## Section 6: Within-Judge Variance

| judge   |   total_cells |   exact |   off_by_1 |   off_by_2_plus |
|:--------|--------------:|--------:|-----------:|----------------:|
| claude  |           104 |   0.904 |      0.087 |           0.01  |
| openai  |           104 |   0.74  |      0.24  |           0.019 |

Plots:
- Claude within-judge variance: [agreement_plots/within_judge_variance_claude.png](agreement_plots/within_judge_variance_claude.png)
- GPT-5 within-judge variance: [agreement_plots/within_judge_variance_openai.png](agreement_plots/within_judge_variance_openai.png)
