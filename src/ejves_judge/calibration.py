"""Phase 5 calibration analysis utilities."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any
import warnings

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

try:  # pragma: no cover - optional dependency in some environments
    import pingouin as pg
except Exception:  # pragma: no cover - fallback path
    pg = None


ORDINAL_ITEMS: tuple[str, ...] = ("tone", "gilbert_urgency", "discern_q7")
BINARY_ITEMS: tuple[str, ...] = ("complementarity",)
LIKERT_ITEMS: tuple[str, ...] = ("accuracy", "comprehensiveness", "clarity")
ALL_ITEMS: tuple[str, ...] = ORDINAL_ITEMS + BINARY_ITEMS + LIKERT_ITEMS

MODEL_ORDER: tuple[str, ...] = ("claude", "openai")
HUMAN_ORDER: tuple[str, ...] = ("MDO", "WD", "EG")
MANUSCRIPT_TABLE2_REFERENCE: dict[str, float] = {
    "accuracy": 0.83,
    "clarity": 0.79,
    "comprehensiveness": 0.86,
}


@dataclass(frozen=True)
class ItemSpec:
    name: str
    kind: str
    min_value: int
    max_value: int
    primary_metric_name: str
    explicit_threshold: float | None = None

    @property
    def labels(self) -> list[int]:
        return list(range(self.min_value, self.max_value + 1))


ITEM_SPECS: dict[str, ItemSpec] = {
    "tone": ItemSpec(
        name="tone",
        kind="ordinal",
        min_value=0,
        max_value=2,
        primary_metric_name="weighted_kappa_quadratic",
    ),
    "complementarity": ItemSpec(
        name="complementarity",
        kind="binary",
        min_value=0,
        max_value=1,
        primary_metric_name="kappa_unweighted",
    ),
    "gilbert_urgency": ItemSpec(
        name="gilbert_urgency",
        kind="ordinal",
        min_value=0,
        max_value=4,
        primary_metric_name="weighted_kappa_quadratic",
        explicit_threshold=0.5,
    ),
    "discern_q7": ItemSpec(
        name="discern_q7",
        kind="ordinal",
        min_value=1,
        max_value=5,
        primary_metric_name="weighted_kappa_quadratic",
    ),
    "accuracy": ItemSpec(
        name="accuracy",
        kind="likert",
        min_value=1,
        max_value=5,
        primary_metric_name="weighted_kappa_quadratic",
        explicit_threshold=0.6,
    ),
    "comprehensiveness": ItemSpec(
        name="comprehensiveness",
        kind="likert",
        min_value=1,
        max_value=5,
        primary_metric_name="weighted_kappa_quadratic",
        explicit_threshold=0.5,
    ),
    "clarity": ItemSpec(
        name="clarity",
        kind="likert",
        min_value=1,
        max_value=5,
        primary_metric_name="weighted_kappa_quadratic",
        explicit_threshold=0.5,
    ),
}


def stable_mode(values: pd.Series) -> float | pd.NA:
    """Return the deterministic mode, breaking ties toward the smaller value."""

    observed = values.dropna()
    if observed.empty:
        return pd.NA
    counts = observed.value_counts(dropna=True)
    top_count = counts.iloc[0]
    top_values = sorted(float(value) for value, count in counts.items() if count == top_count)
    return top_values[0]


def round_half_up(value: float) -> int:
    """Round positive score values away from .5 toward the upper category."""

    return int(math.floor(float(value) + 0.5))


def discretize_value(value: float | int | pd.NA, item: str) -> int | pd.NA:
    """Map aggregated numeric values back onto the original rubric scale."""

    if pd.isna(value):
        return pd.NA
    spec = ITEM_SPECS[item]
    numeric = float(value)
    if spec.kind == "binary":
        return int(numeric >= 0.5)
    rounded = round_half_up(numeric)
    return int(min(max(rounded, spec.min_value), spec.max_value))


def discretize_series(values: pd.Series, item: str) -> pd.Series:
    return values.apply(lambda value: discretize_value(value, item)).astype("Int64")


def _aggregate_item(values: pd.Series, item: str) -> float | pd.NA:
    observed = values.dropna()
    if observed.empty:
        return pd.NA

    spec = ITEM_SPECS[item]
    if spec.kind == "ordinal":
        return float(observed.median())
    if spec.kind == "binary":
        return stable_mode(observed)
    return float(observed.astype(float).mean())


def aggregate_human_consensus(human_long: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the three human raters into one consensus row per response."""

    meta_columns = [
        "response_id",
        "disease",
        "domain",
        "question_group",
        "question_text",
        "response_text",
    ]
    rows: list[dict[str, Any]] = []
    for _, group in human_long.sort_values("response_id", kind="stable").groupby(
        "response_id", sort=False
    ):
        row = {column: group[column].iloc[0] for column in meta_columns}
        for item in ALL_ITEMS:
            row[item] = _aggregate_item(group[item], item)
        rows.append(row)

    return pd.DataFrame(rows).sort_values("response_id", kind="stable").reset_index(drop=True)


def _representative_rationale(
    group: pd.DataFrame,
    *,
    aggregated_scores: dict[str, float | pd.NA],
) -> tuple[int | pd.NA, str | pd.NA]:
    score_columns = [item for item in ALL_ITEMS if group[item].notna().any()]
    if not score_columns:
        return pd.NA, pd.NA

    best_index: int | None = None
    best_distance: float | None = None
    for row in group.itertuples(index=False):
        distance = 0.0
        for item in score_columns:
            value = getattr(row, item)
            target = aggregated_scores[item]
            if pd.isna(value) or pd.isna(target):
                continue
            distance += abs(float(value) - float(target))

        run_index = int(row.run_index)
        candidate = (distance, run_index)
        if best_distance is None or candidate < (best_distance, best_index or run_index):
            best_distance = distance
            best_index = run_index

    if best_index is None:
        return pd.NA, pd.NA

    chosen = group.loc[group["run_index"].eq(best_index)].iloc[0]
    rationale = chosen["rationale"]
    return best_index, rationale if pd.notna(rationale) else pd.NA


def aggregate_judge_runs(judge_raw: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the three runs for each judge/response slot."""

    rows: list[dict[str, Any]] = []
    group_columns = ["judge_name", "response_id", "question_group"]
    for (judge_name, response_id, question_group), group in judge_raw.sort_values(
        ["judge_name", "response_id", "run_index"], kind="stable"
    ).groupby(group_columns, sort=False):
        row: dict[str, Any] = {
            "judge_name": judge_name,
            "response_id": response_id,
            "question_group": question_group,
            "model_used": group["model_used"].mode(dropna=True).iloc[0],
            "all_runs_successful": bool(group["status"].eq("success").all()),
            "successful_run_count": int(group["status"].eq("success").sum()),
        }
        aggregated_scores: dict[str, float | pd.NA] = {}
        for item in ALL_ITEMS:
            aggregated_scores[item] = _aggregate_item(group[item], item)
            row[f"{item}_aggregated"] = aggregated_scores[item]

        representative_run_index, representative_rationale = _representative_rationale(
            group,
            aggregated_scores=aggregated_scores,
        )
        row["representative_run_index"] = representative_run_index
        row["representative_rationale"] = representative_rationale
        rows.append(row)

    return pd.DataFrame(rows).sort_values(
        ["judge_name", "response_id"], kind="stable"
    ).reset_index(drop=True)


def build_ensemble_scores(
    judge_aggregated: pd.DataFrame,
    human_consensus: pd.DataFrame,
) -> pd.DataFrame:
    """Average the two judges into one ensemble row per response."""

    rows: list[dict[str, Any]] = []
    meta = human_consensus.set_index("response_id")
    for response_id, group in judge_aggregated.groupby("response_id", sort=True):
        row: dict[str, Any] = {
            "response_id": response_id,
            "question_group": group["question_group"].iloc[0],
            "disease": meta.loc[response_id, "disease"],
            "domain": meta.loc[response_id, "domain"],
            "question_text": meta.loc[response_id, "question_text"],
            "response_text": meta.loc[response_id, "response_text"],
        }
        for item in ALL_ITEMS:
            values = group[f"{item}_aggregated"].dropna().astype(float)
            row[item] = float(values.mean()) if not values.empty else pd.NA
        rows.append(row)

    return pd.DataFrame(rows).sort_values("response_id", kind="stable").reset_index(drop=True)


def _manual_icc_a_1(score_table: pd.DataFrame) -> float:
    complete = score_table.dropna()
    if complete.shape[0] < 2 or complete.shape[1] < 2:
        return float("nan")

    matrix = complete.to_numpy(dtype=float)
    n_targets, n_raters = matrix.shape
    row_means = matrix.mean(axis=1)
    col_means = matrix.mean(axis=0)
    grand_mean = matrix.mean()

    msr = n_raters * ((row_means - grand_mean) ** 2).sum() / (n_targets - 1)
    msc = n_targets * ((col_means - grand_mean) ** 2).sum() / (n_raters - 1)
    mse = (
        (matrix - row_means[:, None] - col_means[None, :] + grand_mean) ** 2
    ).sum() / ((n_targets - 1) * (n_raters - 1))

    denominator = msr + (n_raters - 1) * mse + n_raters * (msc - mse) / n_targets
    if denominator == 0:
        return float("nan")
    return float((msr - mse) / denominator)


def _manual_icc_a_k(score_table: pd.DataFrame) -> float:
    complete = score_table.dropna()
    if complete.shape[0] < 2 or complete.shape[1] < 2:
        return float("nan")

    matrix = complete.to_numpy(dtype=float)
    n_targets, n_raters = matrix.shape
    row_means = matrix.mean(axis=1)
    col_means = matrix.mean(axis=0)
    grand_mean = matrix.mean()

    msr = n_raters * ((row_means - grand_mean) ** 2).sum() / (n_targets - 1)
    msc = n_targets * ((col_means - grand_mean) ** 2).sum() / (n_raters - 1)
    mse = (
        (matrix - row_means[:, None] - col_means[None, :] + grand_mean) ** 2
    ).sum() / ((n_targets - 1) * (n_raters - 1))

    denominator = msr + (msc - mse) / n_targets
    if denominator == 0:
        return float("nan")
    return float((msr - mse) / denominator)


def icc_absolute_agreement(
    score_table: pd.DataFrame,
    *,
    average_measures: bool = False,
) -> float:
    """Return ICC(A,1) or ICC(A,k) for a complete score matrix."""

    complete = score_table.dropna()
    if complete.shape[0] < 2 or complete.shape[1] < 2:
        return float("nan")

    if pg is not None:  # pragma: no branch - preferred path once dependency exists
        long_df = complete.reset_index().melt(
            id_vars=complete.index.name or "index",
            var_name="raters",
            value_name="scores",
        )
        long_df = long_df.rename(columns={complete.index.name or "index": "targets"})
        try:
            icc_df = pg.intraclass_corr(
                data=long_df,
                targets="targets",
                raters="raters",
                ratings="scores",
                nan_policy="omit",
            )
            icc_type = "ICC(A,k)" if average_measures else "ICC(A,1)"
            return float(icc_df.loc[icc_df["Type"].eq(icc_type), "ICC"].iloc[0])
        except (AssertionError, ValueError, ZeroDivisionError):
            # Pingouin rejects some sparse but still usable complete matrices.
            # Fall back to the local implementation so partial reruns can still
            # generate agreement summaries instead of aborting the report.
            pass

    if average_measures:
        return _manual_icc_a_k(complete)
    return _manual_icc_a_1(complete)


def pingouin_icc_table(score_table: pd.DataFrame) -> pd.DataFrame:
    """Return the full pingouin ICC table or a manual minimal fallback."""

    complete = score_table.dropna()
    if complete.shape[0] < 2 or complete.shape[1] < 2:
        return pd.DataFrame(columns=["Type", "ICC"])

    if pg is None:  # pragma: no cover - fallback only
        return pd.DataFrame({"Type": ["ICC(A,1)"], "ICC": [icc_absolute_agreement(complete)]})

    long_df = complete.reset_index().melt(
        id_vars=complete.index.name or "index",
        var_name="raters",
        value_name="scores",
    )
    long_df = long_df.rename(columns={complete.index.name or "index": "targets"})
    try:
        return pg.intraclass_corr(
            data=long_df,
            targets="targets",
            raters="raters",
            ratings="scores",
            nan_policy="omit",
        )
    except (AssertionError, ValueError, ZeroDivisionError):
        return pd.DataFrame(
            {
                "Type": ["ICC(A,1)", "ICC(A,k)"],
                "ICC": [
                    _manual_icc_a_1(complete),
                    _manual_icc_a_k(complete),
                ],
            }
        )


def safe_weighted_kappa(left: pd.Series, right: pd.Series, item: str) -> float:
    spec = ITEM_SPECS[item]
    mask = left.notna() & right.notna()
    if mask.sum() == 0:
        return float("nan")

    left_values = discretize_series(left[mask], item).astype(int)
    right_values = discretize_series(right[mask], item).astype(int)
    weights = None if spec.kind == "binary" else "quadratic"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return float(
            cohen_kappa_score(
                left_values,
                right_values,
                labels=spec.labels,
                weights=weights,
            )
        )


def safe_spearman(left: pd.Series, right: pd.Series) -> float:
    mask = left.notna() & right.notna()
    if mask.sum() < 2:
        return float("nan")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        statistic = spearmanr(left[mask].astype(float), right[mask].astype(float)).statistic
    return float(statistic) if statistic is not None else float("nan")


def bland_altman_stats(left: pd.Series, right: pd.Series) -> tuple[float, float, float]:
    mask = left.notna() & right.notna()
    if mask.sum() < 2:
        return float("nan"), float("nan"), float("nan")

    diff = left[mask].astype(float) - right[mask].astype(float)
    mean_diff = float(diff.mean())
    std_diff = float(diff.std(ddof=1))
    loa_low = mean_diff - 1.96 * std_diff
    loa_high = mean_diff + 1.96 * std_diff
    return mean_diff, loa_low, loa_high


def score_table_for_icc(
    left: pd.Series,
    right: pd.Series,
    *,
    left_name: str,
    right_name: str,
) -> pd.DataFrame:
    frame = pd.DataFrame({left_name: left, right_name: right})
    frame.index.name = "target"
    return frame


def agreement_row(
    *,
    item: str,
    left_values: pd.Series,
    right_values: pd.Series,
) -> dict[str, Any]:
    spec = ITEM_SPECS[item]
    mask = left_values.notna() & right_values.notna()
    left_clean = left_values[mask].astype(float)
    right_clean = right_values[mask].astype(float)
    row: dict[str, Any] = {
        "item": item,
        "n": int(mask.sum()),
        "primary_metric_name": spec.primary_metric_name,
        "primary_metric": safe_weighted_kappa(left_values, right_values, item),
        "spearman_rho": safe_spearman(left_clean, right_clean),
        "icc_2_1": float("nan"),
        "mean_signed_difference": float("nan"),
        "loa_low": float("nan"),
        "loa_high": float("nan"),
    }
    if spec.kind == "likert":
        icc_table = score_table_for_icc(left_clean, right_clean, left_name="left", right_name="right")
        row["icc_2_1"] = icc_absolute_agreement(icc_table)
        (
            row["mean_signed_difference"],
            row["loa_low"],
            row["loa_high"],
        ) = bland_altman_stats(left_clean, right_clean)
    return row


def compare_frames(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    *,
    left_label: str,
    right_label: str,
    left_item_columns: dict[str, str] | None = None,
    right_item_columns: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Compute item-level agreement statistics for two response-level frames."""

    left_item_columns = left_item_columns or {item: item for item in ALL_ITEMS}
    right_item_columns = right_item_columns or {item: item for item in ALL_ITEMS}
    left_frame = left_df[["response_id"] + [left_item_columns[item] for item in ALL_ITEMS]].rename(
        columns={left_item_columns[item]: f"left__{item}" for item in ALL_ITEMS}
    )
    right_frame = right_df[
        ["response_id"] + [right_item_columns[item] for item in ALL_ITEMS]
    ].rename(columns={right_item_columns[item]: f"right__{item}" for item in ALL_ITEMS})
    merged = left_frame.merge(right_frame, on="response_id", how="inner")

    rows: list[dict[str, Any]] = []
    for item in ALL_ITEMS:
        row = agreement_row(
            item=item,
            left_values=merged[f"left__{item}"],
            right_values=merged[f"right__{item}"],
        )
        row["left_label"] = left_label
        row["right_label"] = right_label
        rows.append(row)

    return pd.DataFrame(rows)


def judge_vs_consensus_metrics(
    judge_aggregated: pd.DataFrame,
    human_consensus: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for judge_name, group in judge_aggregated.groupby("judge_name", sort=False):
        left_map = {item: f"{item}_aggregated" for item in ALL_ITEMS}
        comparison = compare_frames(
            group,
            human_consensus,
            left_label=judge_name,
            right_label="human_consensus",
            left_item_columns=left_map,
        )
        comparison["judge_name"] = judge_name
        rows.append(comparison)
    return pd.concat(rows, ignore_index=True)


def ensemble_vs_consensus_metrics(
    ensemble_scores: pd.DataFrame,
    human_consensus: pd.DataFrame,
) -> pd.DataFrame:
    return compare_frames(
        ensemble_scores,
        human_consensus,
        left_label="ensemble",
        right_label="human_consensus",
    )


def judge_vs_reviewer_metrics(
    judge_aggregated: pd.DataFrame,
    human_long: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    left_map = {item: f"{item}_aggregated" for item in ALL_ITEMS}
    reviewer_frames = {
        reviewer: human_long.loc[human_long["reviewer"].eq(reviewer)].copy()
        for reviewer in HUMAN_ORDER
    }
    for judge_name, group in judge_aggregated.groupby("judge_name", sort=False):
        for reviewer in HUMAN_ORDER:
            comparison = compare_frames(
                group,
                reviewer_frames[reviewer],
                left_label=judge_name,
                right_label=reviewer,
                left_item_columns=left_map,
            )
            comparison["judge_name"] = judge_name
            comparison["reviewer"] = reviewer
            rows.append(comparison)
    return pd.concat(rows, ignore_index=True)


def interhuman_pairwise_metrics(human_long: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    reviewer_frames = {
        reviewer: human_long.loc[human_long["reviewer"].eq(reviewer)].copy()
        for reviewer in HUMAN_ORDER
    }
    for reviewer_a, reviewer_b in (("MDO", "WD"), ("MDO", "EG"), ("WD", "EG")):
        comparison = compare_frames(
            reviewer_frames[reviewer_a],
            reviewer_frames[reviewer_b],
            left_label=reviewer_a,
            right_label=reviewer_b,
        )
        comparison["reviewer_a"] = reviewer_a
        comparison["reviewer_b"] = reviewer_b
        rows.append(comparison)
    return pd.concat(rows, ignore_index=True)


def interhuman_min_primary(interhuman_pairwise: pd.DataFrame) -> dict[str, float]:
    return (
        interhuman_pairwise.groupby("item", sort=False)["primary_metric"]
        .min()
        .to_dict()
    )


def interhuman_icc_summary(human_long: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in LIKERT_ITEMS:
        score_table = human_long.pivot(index="response_id", columns="reviewer", values=item)
        icc_table = pingouin_icc_table(score_table)
        icc_a_1 = float(icc_table.loc[icc_table["Type"].eq("ICC(A,1)"), "ICC"].iloc[0])
        manuscript_value = MANUSCRIPT_TABLE2_REFERENCE.get(item)
        rows.append(
            {
                "item": item,
                "icc_2_1": icc_a_1,
                "manuscript_table2": manuscript_value,
                "delta_vs_manuscript": (
                    icc_a_1 - manuscript_value if manuscript_value is not None else float("nan")
                ),
            }
        )
    return pd.DataFrame(rows)


def subset_interhuman_reliability(
    human_long: pd.DataFrame,
    *,
    question_group: str,
) -> dict[str, pd.DataFrame]:
    """Recompute inter-human pairwise agreement and ICC on one question-group subset."""

    subset = human_long.loc[human_long["question_group"].eq(question_group)].copy()
    if subset.empty:
        raise ValueError(f"No human rows found for question_group={question_group!r}.")

    pairwise = interhuman_pairwise_metrics(subset).assign(
        question_group=question_group,
        response_count=int(subset["response_id"].nunique()),
    )

    icc_rows: list[dict[str, Any]] = []
    response_count = int(subset["response_id"].nunique())
    for item in LIKERT_ITEMS:
        score_table = subset.pivot(index="response_id", columns="reviewer", values=item)
        icc_a_k = icc_absolute_agreement(score_table, average_measures=True)
        manuscript_value = MANUSCRIPT_TABLE2_REFERENCE.get(item)
        compare_to_manuscript = question_group == "symptoms"
        icc_rows.append(
            {
                "question_group": question_group,
                "response_count": response_count,
                "item": item,
                "icc_type": "ICC(A,k)",
                "icc_2_k": icc_a_k,
                "manuscript_table2": manuscript_value if compare_to_manuscript else float("nan"),
                "delta_vs_manuscript": (
                    icc_a_k - manuscript_value
                    if compare_to_manuscript and manuscript_value is not None
                    else float("nan")
                ),
            }
        )

    icc = pd.DataFrame(icc_rows)
    return {"pairwise": pairwise, "icc": icc}


def within_judge_variance(judge_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    detail_rows: list[dict[str, Any]] = []
    for (judge_name, response_id), group in judge_raw.groupby(
        ["judge_name", "response_id"], sort=False
    ):
        for item in ALL_ITEMS:
            observed = group[item].dropna()
            if observed.empty:
                continue
            score_span = float(observed.max() - observed.min())
            if score_span == 0:
                bucket = "exact"
            elif score_span == 1:
                bucket = "off_by_1"
            else:
                bucket = "off_by_2_plus"
            detail_rows.append(
                {
                    "judge_name": judge_name,
                    "response_id": response_id,
                    "item": item,
                    "score_span": score_span,
                    "bucket": bucket,
                }
            )

    detail_df = pd.DataFrame(detail_rows).sort_values(
        ["judge_name", "response_id", "item"], kind="stable"
    )
    summary_rows: list[dict[str, Any]] = []
    for judge_name, group in detail_df.groupby("judge_name", sort=False):
        total = len(group)
        exact = int(group["bucket"].eq("exact").sum())
        off_by_1 = int(group["bucket"].eq("off_by_1").sum())
        off_by_2_plus = int(group["bucket"].eq("off_by_2_plus").sum())
        summary_rows.append(
            {
                "judge_name": judge_name,
                "total_cells": total,
                "exact_count": exact,
                "off_by_1_count": off_by_1,
                "off_by_2_plus_count": off_by_2_plus,
                "exact_proportion": exact / total if total else float("nan"),
                "off_by_1_proportion": off_by_1 / total if total else float("nan"),
                "off_by_2_plus_proportion": off_by_2_plus / total if total else float("nan"),
            }
        )
    summary_df = pd.DataFrame(summary_rows).sort_values("judge_name", kind="stable")
    return detail_df.reset_index(drop=True), summary_df.reset_index(drop=True)


def notable_disagreements(
    *,
    ensemble_scores: pd.DataFrame,
    human_consensus: pd.DataFrame,
    judge_aggregated: pd.DataFrame,
) -> list[dict[str, Any]]:
    merged = ensemble_scores.merge(
        human_consensus[
            [
                "response_id",
                "question_text",
                "response_text",
                "accuracy",
                "comprehensiveness",
                "clarity",
            ]
        ],
        on=["response_id", "question_text", "response_text"],
        suffixes=("_ensemble", "_human"),
        how="inner",
    )

    rationale_lookup = {
        (row.judge_name, row.response_id): {
            "model_used": row.model_used,
            "representative_run_index": row.representative_run_index,
            "representative_rationale": row.representative_rationale,
            "accuracy": row.accuracy_aggregated,
            "comprehensiveness": row.comprehensiveness_aggregated,
            "clarity": row.clarity_aggregated,
        }
        for row in judge_aggregated.itertuples(index=False)
    }

    disagreements: list[dict[str, Any]] = []
    for row in merged.itertuples(index=False):
        domains: list[dict[str, Any]] = []
        for item in LIKERT_ITEMS:
            ensemble_value = float(getattr(row, f"{item}_ensemble"))
            human_value = float(getattr(row, f"{item}_human"))
            delta = ensemble_value - human_value
            if abs(delta) >= 2:
                domains.append(
                    {
                        "item": item,
                        "ensemble": ensemble_value,
                        "human_consensus": human_value,
                        "absolute_difference": abs(delta),
                    }
                )
        if not domains:
            continue

        disagreements.append(
            {
                "response_id": row.response_id,
                "question_text": row.question_text,
                "response_text": row.response_text,
                "domains": domains,
                "claude": rationale_lookup[("claude", row.response_id)],
                "openai": rationale_lookup[("openai", row.response_id)],
            }
        )
    return disagreements


def verdict_for_item(
    *,
    item: str,
    primary_metric: float,
    interhuman_floor: float | None,
) -> str:
    spec = ITEM_SPECS[item]
    meets_threshold = (
        True
        if spec.explicit_threshold is None or math.isnan(primary_metric)
        else primary_metric >= spec.explicit_threshold
    )
    meets_human_floor = (
        True
        if interhuman_floor is None or (isinstance(interhuman_floor, float) and math.isnan(interhuman_floor))
        else primary_metric >= interhuman_floor
    )

    if spec.explicit_threshold is None:
        return "PASS" if meets_human_floor else "REVIEW"
    if meets_threshold and meets_human_floor:
        return "PASS"
    if meets_threshold or meets_human_floor:
        return "REVIEW"
    return "FAIL"


def phase5_analysis(
    *,
    human_long: pd.DataFrame,
    judge_raw: pd.DataFrame,
) -> dict[str, Any]:
    """Compute all derived Phase 5 tables from the parquet inputs."""

    human_consensus = aggregate_human_consensus(human_long)
    judge_aggregated = aggregate_judge_runs(judge_raw)
    ensemble_scores = build_ensemble_scores(judge_aggregated, human_consensus)

    ensemble_vs_consensus = ensemble_vs_consensus_metrics(ensemble_scores, human_consensus)
    judge_vs_consensus = judge_vs_consensus_metrics(judge_aggregated, human_consensus)
    judge_vs_reviewer = judge_vs_reviewer_metrics(judge_aggregated, human_long)
    interhuman_pairwise = interhuman_pairwise_metrics(human_long)
    interhuman_floor = interhuman_min_primary(interhuman_pairwise)
    interhuman_icc = interhuman_icc_summary(human_long)
    interhuman_subset = {
        "symptoms": subset_interhuman_reliability(human_long, question_group="symptoms"),
        "treatment": subset_interhuman_reliability(human_long, question_group="treatment"),
    }
    variance_detail, variance_summary = within_judge_variance(judge_raw)
    disagreements = notable_disagreements(
        ensemble_scores=ensemble_scores,
        human_consensus=human_consensus,
        judge_aggregated=judge_aggregated,
    )

    ensemble_vs_consensus = ensemble_vs_consensus.assign(
        interhuman_primary_floor=ensemble_vs_consensus["item"].map(interhuman_floor),
    )
    ensemble_vs_consensus["verdict"] = ensemble_vs_consensus.apply(
        lambda row: verdict_for_item(
            item=row["item"],
            primary_metric=float(row["primary_metric"]),
            interhuman_floor=row["interhuman_primary_floor"],
        ),
        axis=1,
    )

    judge_vs_consensus = judge_vs_consensus.assign(
        interhuman_primary_floor=judge_vs_consensus["item"].map(interhuman_floor),
    )
    judge_vs_consensus["verdict"] = judge_vs_consensus.apply(
        lambda row: verdict_for_item(
            item=row["item"],
            primary_metric=float(row["primary_metric"]),
            interhuman_floor=row["interhuman_primary_floor"],
        ),
        axis=1,
    )

    model_strings = (
        judge_aggregated.groupby("judge_name", sort=False)["model_used"]
        .agg(lambda values: ", ".join(sorted(set(values))))
        .to_dict()
    )

    return {
        "human_consensus": human_consensus,
        "judge_aggregated": judge_aggregated,
        "ensemble_scores": ensemble_scores,
        "ensemble_vs_consensus": ensemble_vs_consensus,
        "judge_vs_consensus": judge_vs_consensus,
        "judge_vs_reviewer": judge_vs_reviewer,
        "interhuman_pairwise": interhuman_pairwise,
        "interhuman_icc": interhuman_icc,
        "interhuman_subset": interhuman_subset,
        "within_judge_detail": variance_detail,
        "within_judge_summary": variance_summary,
        "notable_disagreements": disagreements,
        "model_strings": model_strings,
        "interhuman_primary_floor": interhuman_floor,
    }
