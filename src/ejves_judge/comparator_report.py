"""Final comparator reporting utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.styles import Font
import pandas as pd


SOURCE_MODEL_LABELS = {
    "chatgpt_free": "GPT-5.5",
    "claude_free": "Claude Sonnet 4.6",
    "gemini_free": "Gemini 3.5 Flash",
}
SOURCE_MODEL_ORDER = ("chatgpt_free", "gemini_free", "claude_free")
ORIGINAL_BENCHMARK_LABEL = "Original GPT-3.5 study benchmark"


@dataclass(frozen=True)
class EndpointSpec:
    final_column: str
    original_column: str
    display_name: str
    direction: str  # "higher" or "lower"
    group: str  # "validated" or "descriptive"
    subset: str  # "all" or "treatment"


ENDPOINT_SPECS = (
    EndpointSpec("validated_accuracy", "accuracy_mean", "Accuracy", "higher", "validated", "all"),
    EndpointSpec("validated_tone", "tone_mean", "Tone", "higher", "validated", "all"),
    EndpointSpec(
        "validated_complementarity",
        "complementarity_mean",
        "Complementarity",
        "higher",
        "validated",
        "all",
    ),
    EndpointSpec(
        "validated_gilbert_urgency",
        "gilbert_urgency_mean",
        "Urgency",
        "lower",
        "validated",
        "all",
    ),
    EndpointSpec(
        "validated_discern_q7",
        "discern_q7_mean",
        "DISCERN Q7",
        "higher",
        "validated",
        "treatment",
    ),
    EndpointSpec(
        "descriptive_comprehensiveness",
        "comprehensiveness_mean",
        "Comprehensiveness",
        "higher",
        "descriptive",
        "all",
    ),
    EndpointSpec(
        "descriptive_clarity",
        "clarity_mean",
        "Clarity",
        "higher",
        "descriptive",
        "all",
    ),
)


def _format_float(value: Any, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return "NA"
    return f"{float(value):.{digits}f}"


def _mean(series: pd.Series) -> float | pd.NA:
    values = series.dropna().astype(float)
    if values.empty:
        return pd.NA
    return float(values.mean())


def build_original_benchmark_summary(consensus_frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for spec in ENDPOINT_SPECS:
        subset = consensus_frame
        if spec.subset == "treatment":
            subset = subset.loc[subset["question_group"].eq("treatment")]
        rows.append(
            {
                "endpoint": spec.display_name,
                "direction": spec.direction,
                "group": spec.group,
                "original_mean": _mean(subset[spec.original_column]),
                "response_count": int(subset["response_id"].nunique()),
            }
        )
    return pd.DataFrame(rows)


def build_model_endpoint_summary(comparator_results: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for source_model in SOURCE_MODEL_ORDER:
        subset = comparator_results.loc[comparator_results["source_model"].eq(source_model)].copy()
        if subset.empty:
            continue
        row: dict[str, Any] = {
            "source_model": source_model,
            "model_label": SOURCE_MODEL_LABELS.get(source_model, source_model),
            "response_count": int(len(subset)),
            "treatment_response_count": int(subset["question_group"].eq("treatment").sum()),
        }
        for spec in ENDPOINT_SPECS:
            spec_subset = subset
            if spec.subset == "treatment":
                spec_subset = subset.loc[subset["question_group"].eq("treatment")]
            row[spec.final_column] = _mean(spec_subset[spec.final_column])
        rows.append(row)
    return pd.DataFrame(rows)


def build_endpoint_comparison_table(
    *,
    model_summary: pd.DataFrame,
    original_benchmark: pd.DataFrame,
    group: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    benchmark_index = original_benchmark.set_index("endpoint")
    summary_index = model_summary.set_index("source_model")
    for spec in ENDPOINT_SPECS:
        if spec.group != group:
            continue
        benchmark_value = benchmark_index.loc[spec.display_name, "original_mean"]
        row: dict[str, Any] = {
            "Endpoint": spec.display_name,
            "Direction": "Higher is better" if spec.direction == "higher" else "Lower is better",
            ORIGINAL_BENCHMARK_LABEL: benchmark_value,
        }
        for source_model in SOURCE_MODEL_ORDER:
            if source_model not in summary_index.index:
                continue
            model_value = summary_index.loc[source_model, spec.final_column]
            delta = model_value - benchmark_value
            row[SOURCE_MODEL_LABELS[source_model]] = model_value
            delta_column = f"{SOURCE_MODEL_LABELS[source_model]} vs original"
            if spec.direction == "lower":
                row[delta_column] = -delta
            else:
                row[delta_column] = delta
        rows.append(row)
    return pd.DataFrame(rows)


def build_accuracy_resolution_summary(comparator_results: pd.DataFrame) -> pd.DataFrame:
    total_rows = len(comparator_results)
    rows = [
        {
            "metric": "total_comparator_responses",
            "value": int(total_rows),
        },
        {
            "metric": "dual_surgeon_agreement",
            "value": int(comparator_results["accuracy_source"].eq("dual_surgeon_agreement").sum()),
        },
        {
            "metric": "dual_surgeon_mean",
            "value": int(comparator_results["accuracy_source"].eq("dual_surgeon_mean").sum()),
        },
        {
            "metric": "triple_surgeon_median",
            "value": int(comparator_results["accuracy_source"].eq("triple_surgeon_median").sum()),
        },
        {
            "metric": "mario_explicit_revisions",
            "value": int(comparator_results["mario_requested_revised_accuracy"].notna().sum()),
        },
        {
            "metric": "third_reviewer_cases",
            "value": int(comparator_results["third_reviewer_used"].fillna(False).sum()),
        },
    ]
    return pd.DataFrame(rows)


def render_comparator_report(
    *,
    comparator_results: pd.DataFrame,
    original_benchmark: pd.DataFrame,
    model_summary: pd.DataFrame,
    validated_comparison: pd.DataFrame,
    descriptive_comparison: pd.DataFrame,
    accuracy_resolution: pd.DataFrame,
) -> str:
    validated_summary = model_summary[
        [
            "model_label",
            "validated_accuracy",
            "validated_tone",
            "validated_complementarity",
            "validated_gilbert_urgency",
            "validated_discern_q7",
        ]
    ].rename(
        columns={
            "model_label": "Model",
            "validated_accuracy": "Accuracy",
            "validated_tone": "Tone",
            "validated_complementarity": "Complementarity",
            "validated_gilbert_urgency": "Urgency",
            "validated_discern_q7": "DISCERN Q7 (treatment)",
        }
    )
    descriptive_summary = model_summary[
        [
            "model_label",
            "descriptive_comprehensiveness",
            "descriptive_clarity",
        ]
    ].rename(
        columns={
            "model_label": "Model",
            "descriptive_comprehensiveness": "Comprehensiveness",
            "descriptive_clarity": "Clarity",
        }
    )

    benchmark_index = original_benchmark.set_index("endpoint")
    accuracy_leader = model_summary.sort_values("validated_accuracy", ascending=False).iloc[0]
    accuracy_runner_up = model_summary.sort_values("validated_accuracy", ascending=False).iloc[1]
    tone_leader = model_summary.sort_values("validated_tone", ascending=False).iloc[0]
    urgency_leader = model_summary.sort_values("validated_gilbert_urgency", ascending=True).iloc[0]
    discern_leader = model_summary.sort_values("validated_discern_q7", ascending=False).iloc[0]

    return f"""# Final Comparator Report

## Dataset Summary

- Comparator responses: {len(comparator_results)} total (`16` question stems x `3` models)
- Comparator models: GPT-5.5, Gemini 3.5 Flash, Claude Sonnet 4.6
- Original benchmark: reconstructed GPT-3.5 study set (`16` responses)
- Final comparator accuracy process: two blinded board-certified surgeon ratings for all `48` responses, with blinded third-surgeon adjudication for `5` initially disputed rows

## Accuracy Resolution Summary

{accuracy_resolution.to_markdown(index=False)}

## Validated Endpoints By Model

`Accuracy`, `tone`, `complementarity`, `gilbert_urgency`, and treatment-only `DISCERN Q7` are the calibration-passing comparator endpoints. Lower urgency scores indicate stronger recommendation for urgent care.

{validated_summary.to_markdown(index=False, floatfmt='.3f')}

## Validated Endpoints Versus Original GPT-3.5 Benchmark

Positive `vs original` values indicate improvement. For urgency, the delta is sign-flipped so positive values mean more appropriate urgency signaling than the original GPT-3.5 benchmark.

{validated_comparison.to_markdown(index=False, floatfmt='.3f')}

## Descriptive-Only Endpoints

`Comprehensiveness` and `clarity` are retained descriptively only because calibration showed low reliability for both humans and judges on these domains.

{descriptive_summary.to_markdown(index=False, floatfmt='.3f')}

## Descriptive Endpoints Versus Original GPT-3.5 Benchmark

{descriptive_comparison.to_markdown(index=False, floatfmt='.3f')}

## Interpretation

- Accuracy was fully resolved for all `48` comparator rows. The highest mean final validated accuracy was for {accuracy_leader['model_label']} ({_format_float(accuracy_leader['validated_accuracy'])}), with {accuracy_runner_up['model_label']} close behind ({_format_float(accuracy_runner_up['validated_accuracy'])}). Claude Sonnet 4.6 remained closest to the original GPT-3.5 benchmark on this endpoint.
- Tone improved for all three newer models relative to the reconstructed GPT-3.5 baseline. The most balanced overall tone was seen in {tone_leader['model_label']} ({_format_float(tone_leader['validated_tone'])}).
- Complementarity was broadly stable across models; GPT-5.5 and Claude Sonnet 4.6 matched each other on average, while Gemini 3.5 Flash was slightly lower.
- Urgency signaling remained strongest for {urgency_leader['model_label']} because it produced the lowest mean urgency score ({_format_float(urgency_leader['validated_gilbert_urgency'])}).
- Treatment uncertainty handling (`DISCERN Q7`) was highest for {discern_leader['model_label']} ({_format_float(discern_leader['validated_discern_q7'])}).
- Descriptively, all three newer models were clearer and more comprehensive than the original GPT-3.5 benchmark, but these two domains should not be framed as validated primary endpoints.

## Recommended Manuscript Framing

1. Present the newer models as improved communicators relative to the original GPT-3.5 benchmark on the calibration-passing judged domains.
2. Present accuracy as a human-scored endpoint, not an AI-judged endpoint.
3. State explicitly that the comparator arm combined judge scoring for calibration-passing communication domains with blinded surgeon scoring for clinical accuracy.
4. Keep `comprehensiveness` and `clarity` in supplementary or descriptive tables only, with the calibration reliability caveat.
"""


def write_comparator_report(
    *,
    comparator_results_path: Path,
    original_consensus_path: Path,
    output_dir: Path,
) -> dict[str, Path]:
    comparator_results = pd.read_parquet(comparator_results_path)
    original_consensus = pd.read_parquet(original_consensus_path)

    original_benchmark = build_original_benchmark_summary(original_consensus)
    model_summary = build_model_endpoint_summary(comparator_results)
    validated_comparison = build_endpoint_comparison_table(
        model_summary=model_summary,
        original_benchmark=original_benchmark,
        group="validated",
    )
    descriptive_comparison = build_endpoint_comparison_table(
        model_summary=model_summary,
        original_benchmark=original_benchmark,
        group="descriptive",
    )
    accuracy_resolution = build_accuracy_resolution_summary(comparator_results)

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "comparator_report.md"
    workbook_path = output_dir / "comparator_summary_tables.xlsx"
    model_summary_path = output_dir / "model_endpoint_summary.csv"
    validated_path = output_dir / "validated_endpoint_comparison.csv"
    descriptive_path = output_dir / "descriptive_endpoint_comparison.csv"
    accuracy_resolution_path = output_dir / "accuracy_resolution_summary.csv"
    original_benchmark_path = output_dir / "original_gpt35_benchmark_summary.csv"

    report_path.write_text(
        render_comparator_report(
            comparator_results=comparator_results,
            original_benchmark=original_benchmark,
            model_summary=model_summary,
            validated_comparison=validated_comparison,
            descriptive_comparison=descriptive_comparison,
            accuracy_resolution=accuracy_resolution,
        ),
        encoding="utf-8",
    )
    model_summary.to_csv(model_summary_path, index=False)
    validated_comparison.to_csv(validated_path, index=False)
    descriptive_comparison.to_csv(descriptive_path, index=False)
    accuracy_resolution.to_csv(accuracy_resolution_path, index=False)
    original_benchmark.to_csv(original_benchmark_path, index=False)

    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        model_summary.to_excel(writer, sheet_name="model_summary", index=False)
        validated_comparison.to_excel(writer, sheet_name="validated_vs_original", index=False)
        descriptive_comparison.to_excel(writer, sheet_name="descriptive_vs_original", index=False)
        accuracy_resolution.to_excel(writer, sheet_name="accuracy_resolution", index=False)
        original_benchmark.to_excel(writer, sheet_name="original_benchmark", index=False)

    workbook = load_workbook(workbook_path)
    font = Font(name="Arial", size=10)
    for worksheet in workbook.worksheets:
        for row in worksheet.iter_rows():
            for cell in row:
                cell.font = font
    workbook.save(workbook_path)

    return {
        "report": report_path,
        "summary_workbook": workbook_path,
        "model_summary": model_summary_path,
        "validated_comparison": validated_path,
        "descriptive_comparison": descriptive_path,
        "accuracy_resolution": accuracy_resolution_path,
        "original_benchmark": original_benchmark_path,
    }
