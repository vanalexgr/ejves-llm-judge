# Phase 6 Comparator Methodology

This document records the fallback comparator-arm plan after the completed Track B calibration run. It is based on the full 96-call validation set (3 human reviewers, `claude-opus-4-7`, and `gpt-5`), not on the earlier partial Anthropic-overload run.

## Calibration Basis For The Fallback Branch

The final calibration result supports direct judge use only for the rubric items that achieved `PASS`: tone, complementarity, gilbert_urgency, discern_q7. The key decision point was accuracy. Ensemble-vs-consensus weighted kappa for accuracy was 0.128, with Claude at -0.222 and GPT-5 at 0.255. The ensemble ICC(2,1) for accuracy was 0.137, while mean pairwise inter-human accuracy agreement was 0.439. This keeps accuracy well below the human floor and shows model-direction disagreement rather than stable convergence on a shared target.

Comprehensiveness and clarity also remain unsuitable as validated comparator endpoints. Their ensemble kappas were 0.059 and -0.053, with ICC(2,1) values of 0.129 and -0.025. Because the same domains also showed poor inter-human reproducibility in the calibration set, they should be treated as descriptively unstable rather than as a model-specific failure mode.

## Comparator Scoring Scope

1. Use the same two-judge ensemble for the validated domains only: `tone`, `complementarity`, `gilbert_urgency`, and `discern_q7` for treatment responses.
2. Keep the same operational scoring pipeline for those domains: three runs per judge, per-response aggregation within judge, then judge-ensemble averaging downstream.
3. Do not use judge-produced accuracy values as the comparator endpoint. Accuracy for the comparator arm is instead assessed by Mario as a human spot-check on the 32 comparator responses.
4. Keep `comprehensiveness` and `clarity` only as descriptive supplementary outputs with an explicit reliability caveat. They should not be used as validated primary comparator outcomes.
5. Do not perform another rubric-anchoring pass for accuracy on this same calibration set. The completed rerun already showed opposite judge movement on the tightened accuracy construct, so further anchor tuning would become judge-specific and circular.

## Operational Deliverables For The Comparator Arm

- Judge-derived comparator results may be reported directly for `gilbert_urgency`, `tone`, `complementarity`, and `discern_q7`.
- Mario's single-reviewer spot-check supplies the comparator-arm accuracy assessment on the 32 responses.
- `comprehensiveness` and `clarity` may be retained in tables or supplements, but each table should state that both human and judge reliability were low in calibration and that these fields are descriptive only.
- The calibration report at `outputs/calibration/agreement_report.md` remains the audit trail justifying this restricted Phase 6 scope.

## Manuscript-Facing Interpretation

The judge acts as a calibrated instrument where the target is stable and reproducible, most clearly for urgency of care (ensemble weighted kappa 0.709). Accuracy does not meet that standard under the finalized Track B rubric. The comparator methodology therefore uses the judge where calibration succeeded and falls back to human review where the construct remained unstable or model-contested.
