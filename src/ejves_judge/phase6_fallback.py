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
    comparator_response_count: int = 32,
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

This document records the fallback comparator-arm plan after the completed Track B calibration run. It is based on the full 96-call validation set ({len(HUMAN_ORDER)} human reviewers, `{context.claude_model}`, and `{context.openai_model}`), not on the earlier partial Anthropic-overload run.

## Calibration Basis For The Fallback Branch

The final calibration result supports direct judge use only for the rubric items that achieved `PASS`: {pass_items}. The key decision point was accuracy. Ensemble-vs-consensus weighted kappa for accuracy was {_format_float(context.ensemble_accuracy_kappa)}, with Claude at {_format_float(context.claude_accuracy_kappa)} and GPT-5 at {_format_float(context.openai_accuracy_kappa)}. The ensemble ICC(2,1) for accuracy was {_format_float(context.ensemble_accuracy_icc_2_1)}, while mean pairwise inter-human accuracy agreement was {_format_float(context.interhuman_accuracy_mean_pairwise)}. This keeps accuracy well below the human floor and shows model-direction disagreement rather than stable convergence on a shared target.

Comprehensiveness and clarity also remain unsuitable as validated comparator endpoints. Their ensemble kappas were {_format_float(context.comprehensiveness_kappa)} and {_format_float(context.clarity_kappa)}, with ICC(2,1) values of {_format_float(context.comprehensiveness_icc_2_1)} and {_format_float(context.clarity_icc_2_1)}. Because the same domains also showed poor inter-human reproducibility in the calibration set, they should be treated as descriptively unstable rather than as a model-specific failure mode.

## Comparator Scoring Scope

1. Use the same two-judge ensemble for the validated domains only: `tone`, `complementarity`, `gilbert_urgency`, and `discern_q7` for treatment responses.
2. Keep the same operational scoring pipeline for those domains: three runs per judge, per-response aggregation within judge, then judge-ensemble averaging downstream.
3. Do not use judge-produced accuracy values as the comparator endpoint. Accuracy for the comparator arm is instead assessed by Mario as a human spot-check on the {context.comparator_response_count} comparator responses.
4. Keep `comprehensiveness` and `clarity` only as descriptive supplementary outputs with an explicit reliability caveat. They should not be used as validated primary comparator outcomes.
5. Do not perform another rubric-anchoring pass for accuracy on this same calibration set. The completed rerun already showed opposite judge movement on the tightened accuracy construct, so further anchor tuning would become judge-specific and circular.

## Operational Deliverables For The Comparator Arm

- Judge-derived comparator results may be reported directly for `gilbert_urgency`, `tone`, `complementarity`, and `discern_q7`.
- Mario's single-reviewer spot-check supplies the comparator-arm accuracy assessment on the {context.comparator_response_count} responses.
- `comprehensiveness` and `clarity` may be retained in tables or supplements, but each table should state that both human and judge reliability were low in calibration and that these fields are descriptive only.
- The calibration report at `outputs/calibration/agreement_report.md` remains the audit trail justifying this restricted Phase 6 scope.

## Manuscript-Facing Interpretation

The judge acts as a calibrated instrument where the target is stable and reproducible, most clearly for urgency of care (ensemble weighted kappa {_format_float(context.urgency_kappa)}). Accuracy does not meet that standard under the finalized Track B rubric. The comparator methodology therefore uses the judge where calibration succeeded and falls back to human review where the construct remained unstable or model-contested.
"""


def build_methods_addendum(context: Phase6FallbackContext) -> str:
    return f"""# Methods Addendum

To determine whether the LLM-as-judge pipeline could be extended to the comparator arm, we first completed a full calibration run on the original 16 GPT-3.5 vascular-surgery responses scored previously by three vascular surgeons. The calibration used a two-judge ensemble (`{context.claude_model}` and `{context.openai_model}`), with three runs per judge per response and the pre-specified aggregation and agreement procedures described in the calibration protocol. After the Track B accuracy-anchor revision, the final completed run showed that urgency of care, tone, complementarity, and treatment-only DISCERN-Q7 were retained as usable judged domains, whereas accuracy did not meet the comparator-use threshold.

The decisive result was accuracy. Ensemble-vs-consensus weighted kappa for accuracy was {_format_float(context.ensemble_accuracy_kappa)}, with judge-specific kappas of {_format_float(context.claude_accuracy_kappa)} for Claude and {_format_float(context.openai_accuracy_kappa)} for GPT-5. Ensemble ICC(2,1) for accuracy was {_format_float(context.ensemble_accuracy_icc_2_1)}, compared with mean pairwise inter-human agreement of {_format_float(context.interhuman_accuracy_mean_pairwise)}. This pattern indicated that the revised accuracy construct did not converge on a stable prompt-recoverable target across judges, despite a shared prompt and schema, and therefore judge-produced accuracy values were not used as the validated comparator endpoint.

Accordingly, the comparator arm was restricted to judged domains that passed calibration (`tone`, `complementarity`, `gilbert_urgency`, and treatment-only `discern_q7`). Accuracy for the comparator responses was instead assigned by Mario as a focused human spot-check on {context.comparator_response_count} comparator responses. Comprehensiveness and clarity were retained only as descriptive supplementary outputs because calibration showed low reliability for both humans and judges on these domains (ensemble kappas {_format_float(context.comprehensiveness_kappa)} and {_format_float(context.clarity_kappa)}; inter-human ICC(2,1) values {_format_float(context.interhuman_comprehensiveness_icc_2_1)} and {_format_float(context.interhuman_clarity_icc_2_1)}, respectively). No further rubric iteration was performed for accuracy after the completed Track B rerun, to avoid model-specific retuning or circular optimization against the same 16-response calibration set.
"""


def write_phase6_fallback_documents(
    *,
    human_long_path: Path,
    judge_raw_path: Path,
    output_dir: Path,
    comparator_response_count: int = 32,
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
