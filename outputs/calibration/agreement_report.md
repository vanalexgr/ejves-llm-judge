# Agreement Report

Dataset summary: 16 responses, 3 human reviewers (MDO, WD, EG), 2 judges, 3 runs per judge/response, and 96 total scored calls. Claude model: `claude-opus-4-7`. OpenAI model: `gpt-5`.

Aggregation rules: within each judge, ordinal items use the median across 3 runs, binary complementarity uses the mode, and Likert items use the mean. Human consensus uses the same rules across the 3 reviewers. The ensemble is the mean of the two judges per response. Weighted kappa and confusion matrices use nearest-valid-category rounding when aggregation produces fractional values; ICC and Bland–Altman analyses use the raw continuous aggregates.

## Section 1: Summary Table

Verdict logic: PASS requires the explicit CODEX threshold when one exists and also requires ensemble-vs-consensus agreement to be at least as high as the minimum pairwise inter-human agreement for the same item. REVIEW means only one criterion is met, or no explicit threshold exists and the result falls short of the inter-human floor. FAIL means both explicit criteria fail.

| rubric_item       | primary_metric_name      |   kappa | icc_2_1   |   spearman_rho |   interhuman_floor | verdict   |
|:------------------|:-------------------------|--------:|:----------|---------------:|-------------------:|:----------|
| Tone              | weighted_kappa_quadratic |   0.2   | NA        |          0.311 |             -0.308 | PASS      |
| Gilbert Urgency   | weighted_kappa_quadratic |   0.709 | NA        |          0.58  |              0.147 | PASS      |
| Discern Q7        | weighted_kappa_quadratic |   0.308 | NA        |          0.232 |             -0.778 | PASS      |
| Complementarity   | kappa_unweighted         |   0.294 | NA        |          0.303 |             -0.12  | PASS      |
| Accuracy          | weighted_kappa_quadratic |   0.128 | 0.137     |         -0.017 |              0.195 | FAIL      |
| Comprehensiveness | weighted_kappa_quadratic |   0.059 | 0.129     |          0.17  |             -0.198 | REVIEW    |
| Clarity           | weighted_kappa_quadratic |  -0.053 | -0.025    |         -0.113 |             -0.278 | REVIEW    |

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

| rubric_item       | primary_metric_name      |   kappa | icc_2_1   |   spearman_rho |   interhuman_floor | verdict   |
|:------------------|:-------------------------|--------:|:----------|---------------:|-------------------:|:----------|
| Tone              | weighted_kappa_quadratic |   0.31  | NA        |          0.313 |             -0.308 | PASS      |
| Gilbert Urgency   | weighted_kappa_quadratic |   0.653 | NA        |          0.58  |              0.147 | PASS      |
| Discern Q7        | weighted_kappa_quadratic |   0.125 | NA        |          0.178 |             -0.778 | PASS      |
| Complementarity   | kappa_unweighted         |   0.294 | NA        |          0.303 |             -0.12  | PASS      |
| Accuracy          | weighted_kappa_quadratic |  -0.222 | -0.294    |         -0.3   |              0.195 | FAIL      |
| Comprehensiveness | weighted_kappa_quadratic |   0.048 | 0.016     |         -0.06  |             -0.198 | REVIEW    |
| Clarity           | weighted_kappa_quadratic |  -0.077 | -0.038    |         -0.158 |             -0.278 | REVIEW    |

### GPT-5

| rubric_item       | primary_metric_name      |   kappa | icc_2_1   |   spearman_rho |   interhuman_floor | verdict   |
|:------------------|:-------------------------|--------:|:----------|---------------:|-------------------:|:----------|
| Tone              | weighted_kappa_quadratic |   0.2   | NA        |          0.244 |             -0.308 | PASS      |
| Gilbert Urgency   | weighted_kappa_quadratic |   0.709 | NA        |          0.58  |              0.147 | PASS      |
| Discern Q7        | weighted_kappa_quadratic |   0.257 | NA        |          0.37  |             -0.778 | PASS      |
| Complementarity   | kappa_unweighted         |   0.294 | NA        |          0.303 |             -0.12  | PASS      |
| Accuracy          | weighted_kappa_quadratic |   0.255 | 0.376     |          0.202 |              0.195 | REVIEW    |
| Comprehensiveness | weighted_kappa_quadratic |   0.215 | 0.209     |          0.374 |             -0.198 | REVIEW    |
| Clarity           | weighted_kappa_quadratic |  -0.122 | -0.013    |         -0.014 |             -0.278 | REVIEW    |

## Section 3: Judge-vs-Individual-Human Matrix

Each table reports the primary agreement metric for that rubric item: quadratic weighted kappa for ordinal/Likert items and unweighted kappa for complementarity.

### Tone

| Judge   |   MDO |     WD |    EG |   Min human-human |   Mean human-human |
|:--------|------:|-------:|------:|------------------:|-------------------:|
| Claude  |  0.25 | -0.161 | 0.333 |            -0.308 |             -0.061 |
| GPT-5   |  0.5  | -0.091 | 0.25  |            -0.308 |             -0.061 |

### Gilbert Urgency

| Judge   |   MDO |    WD |    EG |   Min human-human |   Mean human-human |
|:--------|------:|------:|------:|------------------:|-------------------:|
| Claude  | 0.603 | 0.399 | 0.492 |             0.147 |              0.329 |
| GPT-5   | 0.65  | 0.413 | 0.54  |             0.147 |              0.329 |

### Discern Q7

| Judge   |   MDO |    WD |     EG |   Min human-human |   Mean human-human |
|:--------|------:|------:|-------:|------------------:|-------------------:|
| Claude  | 0.458 |  0.1  | -0.375 |            -0.778 |             -0.262 |
| GPT-5   | 0.574 | -0.07 | -0.593 |            -0.778 |             -0.262 |

### Complementarity

| Judge   |   MDO |     WD |    EG |   Min human-human |   Mean human-human |
|:--------|------:|-------:|------:|------------------:|-------------------:|
| Claude  |  0.59 | -0.103 | 0.259 |             -0.12 |              0.012 |
| GPT-5   |  0.59 | -0.103 | 0.259 |             -0.12 |              0.012 |

### Accuracy

| Judge   |    MDO |     WD |     EG |   Min human-human |   Mean human-human |
|:--------|-------:|-------:|-------:|------------------:|-------------------:|
| Claude  | -0.111 | -0.259 | -0.163 |             0.195 |              0.439 |
| GPT-5   |  0.189 |  0.298 |  0.241 |             0.195 |              0.439 |

### Comprehensiveness

| Judge   |   MDO |     WD |    EG |   Min human-human |   Mean human-human |
|:--------|------:|-------:|------:|------------------:|-------------------:|
| Claude  | 0.036 | -0.176 | 0.247 |            -0.198 |             -0.064 |
| GPT-5   | 0.109 |  0.025 | 0.507 |            -0.198 |             -0.064 |

### Clarity

| Judge   |    MDO |     WD |     EG |   Min human-human |   Mean human-human |
|:--------|-------:|-------:|-------:|------------------:|-------------------:|
| Claude  |  0.2   | -0.302 |  0.13  |            -0.278 |             -0.085 |
| GPT-5   | -0.067 | -0.045 | -0.016 |            -0.278 |             -0.085 |

## Section 4: Inter-Human Reliability

### Pairwise Human Agreement

| rubric_item       | reviewer_pair   | primary_metric_name      |   primary_metric |
|:------------------|:----------------|:-------------------------|-----------------:|
| Tone              | MDO vs WD       | weighted_kappa_quadratic |            0.125 |
| Gilbert Urgency   | MDO vs WD       | weighted_kappa_quadratic |            0.191 |
| Discern Q7        | MDO vs WD       | weighted_kappa_quadratic |           -0.174 |
| Complementarity   | MDO vs WD       | kappa_unweighted         |           -0.103 |
| Accuracy          | MDO vs WD       | weighted_kappa_quadratic |            0.636 |
| Comprehensiveness | MDO vs WD       | weighted_kappa_quadratic |           -0.069 |
| Clarity           | MDO vs WD       | weighted_kappa_quadratic |           -0.278 |
| Tone              | MDO vs EG       | weighted_kappa_quadratic |            0     |
| Gilbert Urgency   | MDO vs EG       | weighted_kappa_quadratic |            0.65  |
| Discern Q7        | MDO vs EG       | weighted_kappa_quadratic |           -0.778 |
| Complementarity   | MDO vs EG       | kappa_unweighted         |            0.259 |
| Accuracy          | MDO vs EG       | weighted_kappa_quadratic |            0.195 |
| Comprehensiveness | MDO vs EG       | weighted_kappa_quadratic |            0.076 |
| Clarity           | MDO vs EG       | weighted_kappa_quadratic |            0.077 |
| Tone              | WD vs EG        | weighted_kappa_quadratic |           -0.308 |
| Gilbert Urgency   | WD vs EG        | weighted_kappa_quadratic |            0.147 |
| Discern Q7        | WD vs EG        | weighted_kappa_quadratic |            0.165 |
| Complementarity   | WD vs EG        | kappa_unweighted         |           -0.12  |
| Accuracy          | WD vs EG        | weighted_kappa_quadratic |            0.485 |
| Comprehensiveness | WD vs EG        | weighted_kappa_quadratic |           -0.198 |
| Clarity           | WD vs EG        | weighted_kappa_quadratic |           -0.053 |

### ICC Comparison to Manuscript Table 2

| rubric_item       |   icc_2_1 |   manuscript_table2 |   delta_vs_manuscript |
|:------------------|----------:|--------------------:|----------------------:|
| Accuracy          |     0.446 |                0.83 |                -0.384 |
| Comprehensiveness |    -0.061 |                0.86 |                -0.921 |
| Clarity           |    -0.067 |                0.79 |                -0.857 |

Note: the recomputed human ICC(2,1) values above are derived directly from the source reviewer spreadsheets. If they differ from the manuscript values (Accuracy=0.83, Clarity=0.79, Comprehensiveness=0.86), that indicates the manuscript likely used a different ICC parameterization and/or preprocessing path.

## Section 4b: Symptoms-subset inter-human ICC(2,k)

Symptoms subset: `8` responses with `question_group == 'symptoms'`. Treatment subset: `8` responses with `question_group == 'treatment'`. ICC in this subsection uses two-way random absolute agreement average measures, i.e. ICC(A,k) / ICC(2,k).

### Symptoms-only Pairwise Human Agreement

| rubric_item       | reviewer_pair   | primary_metric_name      | primary_metric   |
|:------------------|:----------------|:-------------------------|:-----------------|
| Tone              | MDO vs WD       | weighted_kappa_quadratic | 0.059            |
| Gilbert Urgency   | MDO vs WD       | weighted_kappa_quadratic | 0.297            |
| Discern Q7        | MDO vs WD       | weighted_kappa_quadratic | NA               |
| Complementarity   | MDO vs WD       | kappa_unweighted         | 0.000            |
| Accuracy          | MDO vs WD       | weighted_kappa_quadratic | 0.636            |
| Comprehensiveness | MDO vs WD       | weighted_kappa_quadratic | -0.116           |
| Clarity           | MDO vs WD       | weighted_kappa_quadratic | -0.273           |
| Tone              | MDO vs EG       | weighted_kappa_quadratic | 0.176            |
| Gilbert Urgency   | MDO vs EG       | weighted_kappa_quadratic | 0.669            |
| Discern Q7        | MDO vs EG       | weighted_kappa_quadratic | NA               |
| Complementarity   | MDO vs EG       | kappa_unweighted         | 0.143            |
| Accuracy          | MDO vs EG       | weighted_kappa_quadratic | 0.043            |
| Comprehensiveness | MDO vs EG       | weighted_kappa_quadratic | -0.055           |
| Clarity           | MDO vs EG       | weighted_kappa_quadratic | -0.130           |
| Tone              | WD vs EG        | weighted_kappa_quadratic | -0.130           |
| Gilbert Urgency   | WD vs EG        | weighted_kappa_quadratic | 0.247            |
| Discern Q7        | WD vs EG        | weighted_kappa_quadratic | NA               |
| Complementarity   | WD vs EG        | kappa_unweighted         | 0.000            |
| Accuracy          | WD vs EG        | weighted_kappa_quadratic | 0.419            |
| Comprehensiveness | WD vs EG        | weighted_kappa_quadratic | -0.222           |
| Clarity           | WD vs EG        | weighted_kappa_quadratic | 0.032            |

### Symptoms-only ICC(2,k) vs Manuscript Table 2

| rubric_item       | icc_type   |   icc_2_k |   manuscript_table2 |   delta_vs_manuscript |
|:------------------|:-----------|----------:|--------------------:|----------------------:|
| Accuracy          | ICC(A,k)   |     0.667 |                0.83 |                -0.163 |
| Comprehensiveness | ICC(A,k)   |    -0.889 |                0.86 |                -1.749 |
| Clarity           | ICC(A,k)   |    -0.485 |                0.79 |                -1.275 |

The manuscript comparison above is applied only to the symptoms subset, because that was the requested cross-check against Table 2.

### Treatment-only Pairwise Human Agreement

| rubric_item       | reviewer_pair   | primary_metric_name      |   primary_metric |
|:------------------|:----------------|:-------------------------|-----------------:|
| Tone              | MDO vs WD       | weighted_kappa_quadratic |            0.333 |
| Gilbert Urgency   | MDO vs WD       | weighted_kappa_quadratic |           -0.086 |
| Discern Q7        | MDO vs WD       | weighted_kappa_quadratic |           -0.174 |
| Complementarity   | MDO vs WD       | kappa_unweighted         |           -0.143 |
| Accuracy          | MDO vs WD       | weighted_kappa_quadratic |            0.636 |
| Comprehensiveness | MDO vs WD       | weighted_kappa_quadratic |           -0.071 |
| Clarity           | MDO vs WD       | weighted_kappa_quadratic |           -0.214 |
| Tone              | MDO vs EG       | weighted_kappa_quadratic |           -0.556 |
| Gilbert Urgency   | MDO vs EG       | weighted_kappa_quadratic |            0.6   |
| Discern Q7        | MDO vs EG       | weighted_kappa_quadratic |           -0.778 |
| Complementarity   | MDO vs EG       | kappa_unweighted         |            0.385 |
| Accuracy          | MDO vs EG       | weighted_kappa_quadratic |            0.259 |
| Comprehensiveness | MDO vs EG       | weighted_kappa_quadratic |            0.115 |
| Clarity           | MDO vs EG       | weighted_kappa_quadratic |            0.192 |
| Tone              | WD vs EG        | weighted_kappa_quadratic |           -0.333 |
| Gilbert Urgency   | WD vs EG        | weighted_kappa_quadratic |           -0.306 |
| Discern Q7        | WD vs EG        | weighted_kappa_quadratic |            0.165 |
| Complementarity   | WD vs EG        | kappa_unweighted         |           -0.231 |
| Accuracy          | WD vs EG        | weighted_kappa_quadratic |            0.4   |
| Comprehensiveness | WD vs EG        | weighted_kappa_quadratic |           -0.358 |
| Clarity           | WD vs EG        | weighted_kappa_quadratic |           -0.5   |

### Treatment-only ICC(2,k)

| rubric_item       | icc_type   |   icc_2_k |
|:------------------|:-----------|----------:|
| Accuracy          | ICC(A,k)   |     0.713 |
| Comprehensiveness | ICC(A,k)   |    -0.202 |
| Clarity           | ICC(A,k)   |    -0.273 |

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
