"""Phase 6 fallback documentation for the comparator arm."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from .calibration import HUMAN_ORDER, phase5_analysis


@dataclass(frozen=True)
class Phase6FallbackContext:
    comparator_response_count: int
    third_rater_case_count: int
    claude_model: str
    openai_model: str
    ensemble_accuracy_kappa: float
    claude_accuracy_kappa: float
    openai_accuracy_kappa: float
    ensemble_accuracy_icc_2_1: float
    interhuman_accuracy_mean_pairwise: float
    interhuman_comprehensiveness_icc_2_1: float
    interhuman_clarity_icc_2_1: float
    urgency_kappa: float
    tone_kappa: float
    discern_kappa: float
    complementarity_kappa: float
    comprehensiveness_kappa: float
    clarity_kappa: float
    comprehensiveness_icc_2_1: float
    clarity_icc_2_1: float
    accuracy_verdict: str
    comprehensiveness_verdict: str
    clarity_verdict: str
    pass_items: tuple[str, ...]


def _format_float(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}"


def build_phase6_fallback_context(
    *,
    analysis: dict[str, Any],
    comparator_response_count: int = 48,
    third_rater_case_count: int = 5,
) -> Phase6FallbackContext:
    ensemble = analysis["ensemble_vs_consensus"].set_index("item")
    judge = analysis["judge_vs_consensus"].set_index(["judge_name", "item"])
    interhuman = analysis["interhuman_pairwise"]
    interhuman_icc = analysis["interhuman_icc"].set_index("item")

    desired_pass_order = ("tone", "complementarity", "gilbert_urgency", "discern_q7")
    pass_items = tuple(
        item for item in desired_pass_order if str(ensemble.loc[item, "verdict"]) == "PASS"
    )

    return Phase6FallbackContext(
        comparator_response_count=comparator_response_count,
        third_rater_case_count=third_rater_case_count,
        claude_model=analysis["model_strings"].get("claude", "claude-opus-4-7"),
        openai_model=analysis["model_strings"].get("openai", "gpt-5"),
        ensemble_accuracy_kappa=float(ensemble.loc["accuracy", "primary_metric"]),
        claude_accuracy_kappa=float(judge.loc[("claude", "accuracy"), "primary_metric"]),
        openai_accuracy_kappa=float(judge.loc[("openai", "accuracy"), "primary_metric"]),
        ensemble_accuracy_icc_2_1=float(ensemble.loc["accuracy", "icc_2_1"]),
        interhuman_accuracy_mean_pairwise=float(
            interhuman.loc[interhuman["item"].eq("accuracy"), "primary_metric"].mean()
        ),
        interhuman_comprehensiveness_icc_2_1=float(
            interhuman_icc.loc["comprehensiveness", "icc_2_1"]
        ),
        interhuman_clarity_icc_2_1=float(interhuman_icc.loc["clarity", "icc_2_1"]),
        urgency_kappa=float(ensemble.loc["gilbert_urgency", "primary_metric"]),
        tone_kappa=float(ensemble.loc["tone", "primary_metric"]),
        discern_kappa=float(ensemble.loc["discern_q7", "primary_metric"]),
        complementarity_kappa=float(ensemble.loc["complementarity", "primary_metric"]),
        comprehensiveness_kappa=float(ensemble.loc["comprehensiveness", "primary_metric"]),
        clarity_kappa=float(ensemble.loc["clarity", "primary_metric"]),
        comprehensiveness_icc_2_1=float(ensemble.loc["comprehensiveness", "icc_2_1"]),
        clarity_icc_2_1=float(ensemble.loc["clarity", "icc_2_1"]),
        accuracy_verdict=str(ensemble.loc["accuracy", "verdict"]),
        comprehensiveness_verdict=str(ensemble.loc["comprehensiveness", "verdict"]),
        clarity_verdict=str(ensemble.loc["clarity", "verdict"]),
        pass_items=pass_items,
    )


def build_phase6_comparator_methodology(context: Phase6FallbackContext) -> str:
    pass_items = ", ".join(context.pass_items)
    return f"""# Phase 6 Comparator Methodology

This document records the implemented comparator-arm methodology after the completed Track B calibration run. It is based on the full 96-call validation set ({len(HUMAN_ORDER)} human reviewers, `{context.claude_model}`, and `{context.openai_model}`), not on the earlier partial Anthropic-overload run. In this repository, **Track B** refers to the second and final calibration pass in which the accuracy anchor was tightened to penalize clinically unrepresentative but factually defensible answers. Because the revised anchor was evaluated on the same 16-response calibration set that motivated the change, Track B should be read as a stopping-and-diagnosis pass rather than as independent external validation of the revised anchor.

## Calibration Basis For The Fallback Branch

The final calibration result supports direct judge use only for the rubric items that achieved `PASS`: {pass_items}. The key decision point was accuracy. Ensemble-vs-consensus weighted kappa for accuracy was {_format_float(context.ensemble_accuracy_kappa)}, with Claude at {_format_float(context.claude_accuracy_kappa)} and GPT-5 at {_format_float(context.openai_accuracy_kappa)}. The ensemble ICC(2,1) for accuracy was {_format_float(context.ensemble_accuracy_icc_2_1)}, while mean pairwise inter-human accuracy agreement was {_format_float(context.interhuman_accuracy_mean_pairwise)}. This kept accuracy below the human agreement floor and showed model-direction disagreement rather than stable convergence on a shared target.

Comprehensiveness and clarity also remain unsuitable as validated comparator endpoints. Their ensemble kappas were {_format_float(context.comprehensiveness_kappa)} and {_format_float(context.clarity_kappa)}, with ICC(2,1) values of {_format_float(context.comprehensiveness_icc_2_1)} and {_format_float(context.clarity_icc_2_1)}. The manuscript Table 2 correction package now clarifies why: in the original symptoms-topic analysis (`n = 4` diseases), inter-rater reliability for clarity and comprehensiveness was not meaningfully estimable and would be reported as 0.00 if floored from non-positive raw ICC estimates. The response-level calibration in this repository is directionally consistent with that result, so these domains should be treated as descriptively unstable rather than as a model-specific failure mode.

Although GPT-5 alone reached {_format_float(context.openai_accuracy_kappa)} on accuracy, the protocol retained the pre-specified two-judge ensemble. Dropping Claude post hoc would have turned a failed ensemble endpoint into a model-specific tuned endpoint and would have weakened the auditability of the calibration design.

## Comparator Scoring Scope

1. Use the same two-judge ensemble for the validated domains only: `tone`, `complementarity`, `gilbert_urgency`, and `discern_q7` for treatment responses.
2. Keep the same operational scoring pipeline for those domains: three runs per judge, per-response aggregation within judge, then judge-ensemble averaging downstream.
3. Do not use judge-produced accuracy values as the comparator endpoint. Accuracy for the comparator arm is instead assessed independently and blinded by two board-certified surgeons on all {context.comparator_response_count} comparator responses.
4. For the {context.third_rater_case_count} responses with initial surgeon disagreement of at least two points, use a blinded third board-certified surgeon as adjudicator and resolve those rows by the triple-surgeon median.
5. Keep `comprehensiveness` and `clarity` only as descriptive supplementary outputs with an explicit reliability caveat. They should not be used as validated primary comparator outcomes.
6. Do not perform another rubric-anchoring pass for accuracy on this same calibration set. The completed rerun already showed opposite judge movement on the tightened accuracy construct, so further anchor tuning would become judge-specific and circular.

## Operational Deliverables For The Comparator Arm

- Judge-derived comparator results may be reported directly for `gilbert_urgency`, `tone`, `complementarity`, and `discern_q7`.
- The final comparator accuracy endpoint comes from blinded surgeon review rather than from the LLM judge: dual-surgeon agreement or mean for non-disputed rows, and triple-surgeon median for the adjudicated subset.
- `comprehensiveness` and `clarity` may be retained in tables or supplements, but each table should state that the original topic-level human reliability for these domains was not meaningfully estimable at this sample size and that the response-level judge calibration was likewise weak; these fields are descriptive only.
- The calibration report at `outputs/calibration/agreement_report.md` remains the audit trail justifying this restricted Phase 6 scope.

## Limitations To State Explicitly

- The calibration corpus consisted of original GPT-3.5 responses, whereas the comparator corpus consists of newer 2025-era models (`GPT-5.5`, `Gemini 3.5 Flash`, and `Claude Sonnet 4.6`). This means the calibration was transported across a different response-style distribution and should be interpreted as a pragmatic rather than universal validity check.
- The historical GPT-3.5 benchmark and the newer comparator arm are not perfectly measurement-equivalent: benchmark values come from the reconstructed earlier surgeon-consensus workflow, whereas comparator accuracy comes from the later dual-surgeon plus adjudication workflow. Cross-era accuracy deltas are therefore pragmatic benchmarks rather than pure like-for-like instrument comparisons.
- Accuracy is intentionally treated as a human-scored clinical endpoint rather than a judge-scored endpoint, because the tightened Track B rubric did not produce stable cross-model convergence.

## Manuscript-Facing Interpretation

The judge acts as a calibrated instrument where the target is stable and reproducible, most clearly for urgency of care (ensemble weighted kappa {_format_float(context.urgency_kappa)}). Accuracy does not meet that standard under the finalized Track B rubric. The comparator methodology therefore uses the judge where calibration succeeded and falls back to blinded surgeon review where the construct remained unstable or model-contested.
"""


def build_methods_addendum(context: Phase6FallbackContext) -> str:
    return f"""# Methods Addendum

To determine whether the LLM-as-judge pipeline could be extended to the comparator arm, we first completed a full calibration run on the original 16 GPT-3.5 vascular-surgery responses scored previously by three vascular surgeons. The calibration used a two-judge ensemble (`{context.claude_model}` and `{context.openai_model}`), with three runs per judge per response and the pre-specified aggregation and agreement procedures described in the calibration protocol. In this repository, Track B refers to the second and final calibration pass after the accuracy anchor was tightened to penalize clinically unrepresentative but factually defensible answers. Because the revised anchor was evaluated on the same 16-response calibration set that motivated the change, Track B should be interpreted as a stopping-and-diagnosis pass rather than as independent external validation of the revised anchor. After that Track B accuracy-anchor revision, the final completed run showed that urgency of care, tone, complementarity, and treatment-only DISCERN-Q7 were retained as calibration-passing judged domains, whereas accuracy did not meet the comparator-use threshold.

The decisive result was accuracy. Ensemble-vs-consensus weighted kappa for accuracy was {_format_float(context.ensemble_accuracy_kappa)}, with judge-specific kappas of {_format_float(context.claude_accuracy_kappa)} for Claude and {_format_float(context.openai_accuracy_kappa)} for GPT-5. Ensemble ICC(2,1) for accuracy was {_format_float(context.ensemble_accuracy_icc_2_1)}, compared with mean pairwise inter-human agreement of {_format_float(context.interhuman_accuracy_mean_pairwise)}. This pattern indicated that the revised accuracy construct did not converge on a stable prompt-recoverable target across judges, despite a shared prompt and schema, and therefore judge-produced accuracy values were not used as the validated comparator endpoint. Although GPT-5 alone performed better than Claude on this domain, the protocol retained the pre-specified two-judge ensemble; dropping Claude post hoc would have converted a failed ensemble endpoint into a model-specific tuned endpoint.

Accordingly, the comparator arm was restricted to judged domains that passed calibration (`tone`, `complementarity`, `gilbert_urgency`, and treatment-only `discern_q7`). Accuracy for the comparator responses was instead rated independently and blinded by two board-certified surgeons across all {context.comparator_response_count} comparator responses, with blinded third-surgeon adjudication for the {context.third_rater_case_count} rows that initially differed by at least two points. Final comparator accuracy therefore came from the dual-surgeon agreement or mean for non-disputed rows and the triple-surgeon median for adjudicated rows. Comprehensiveness and clarity were retained only as descriptive supplementary outputs because the corrected manuscript Table 2 now shows that, in the original symptoms-topic analysis (`n = 4` diseases), these domains were not meaningfully estimable under ICC(2,k) and would be reported as 0.00 if floored from non-positive raw estimates. The response-level calibration in this repository is directionally consistent with that limitation (ensemble kappas {_format_float(context.comprehensiveness_kappa)} and {_format_float(context.clarity_kappa)}; response-level inter-human ICC(2,1) values {_format_float(context.interhuman_comprehensiveness_icc_2_1)} and {_format_float(context.interhuman_clarity_icc_2_1)}), so they were not treated as validated comparator endpoints. No further rubric iteration was performed for accuracy after the completed Track B rerun, to avoid model-specific retuning or circular optimization against the same 16-response calibration set. Because the calibration corpus consisted of GPT-3.5 responses whereas the comparator corpus contains newer 2025-era models, this transport of the judge across response distributions should be read as a pragmatic external check rather than as a claim of universal judge validity. In addition, the original GPT-3.5 benchmark and the newer comparator arm are not perfectly measurement-equivalent: benchmark values come from the reconstructed earlier surgeon-consensus workflow, whereas comparator accuracy comes from the later dual-surgeon plus adjudication workflow.
"""


def write_phase6_fallback_documents(
    *,
    human_long_path: Path,
    judge_raw_path: Path,
    output_dir: Path,
    comparator_response_count: int = 48,
    third_rater_case_count: int = 5,
) -> dict[str, Path]:
    human_long = pd.read_parquet(human_long_path)
    judge_raw = pd.read_parquet(judge_raw_path)
    if len(judge_raw) != 96 or not judge_raw["status"].eq("success").all():
        raise ValueError(
            "Phase 6 fallback documents require a complete 96/96 successful calibration run."
        )
    analysis = phase5_analysis(human_long=human_long, judge_raw=judge_raw)
    context = build_phase6_fallback_context(
        analysis=analysis,
        comparator_response_count=comparator_response_count,
        third_rater_case_count=third_rater_case_count,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    methodology_path = output_dir / "phase6_comparator_methodology.md"
    addendum_path = output_dir / "methods_addendum.md"
    methodology_path.write_text(
        build_phase6_comparator_methodology(context),
        encoding="utf-8",
    )
    addendum_path.write_text(
        build_methods_addendum(context),
        encoding="utf-8",
    )
    return {
        "phase6_comparator_methodology": methodology_path,
        "methods_addendum": addendum_path,
    }
