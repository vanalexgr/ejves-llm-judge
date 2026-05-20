"""Phase 5 report generation and plotting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

from .calibration import (
    ALL_ITEMS,
    HUMAN_ORDER,
    ITEM_SPECS,
    LIKERT_ITEMS,
    MANUSCRIPT_TABLE2_REFERENCE,
    MODEL_ORDER,
    ORDINAL_ITEMS,
    discretize_series,
    phase5_analysis,
)


def _format_float(value: Any, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return "NA"
    return f"{float(value):.{digits}f}"


def _display_item_name(item: str) -> str:
    return item.replace("_", " ").title().replace("Q7", "Q7")


def _display_judge_name(judge_name: str, model_strings: dict[str, str]) -> str:
    if judge_name == "claude":
        return "Claude"
    if judge_name == "openai":
        model_label = model_strings.get("openai", "OpenAI")
        return "GPT-5" if model_label.lower() == "gpt-5" else model_label
    return judge_name


def _render_markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    if frame.empty:
        return "_No rows._"
    table = frame.loc[:, columns].copy()
    return table.to_markdown(index=False)


def _save_bland_altman_plot(
    ensemble_scores: pd.DataFrame,
    human_consensus: pd.DataFrame,
    *,
    item: str,
    output_path: Path,
) -> None:
    merged = ensemble_scores[["response_id", item]].merge(
        human_consensus[["response_id", item]],
        on="response_id",
        suffixes=("_ensemble", "_human"),
        how="inner",
    )
    left = merged[f"{item}_ensemble"].astype(float)
    right = merged[f"{item}_human"].astype(float)
    average = (left + right) / 2
    difference = left - right
    mean_diff = difference.mean()
    std_diff = difference.std(ddof=1)
    loa_low = mean_diff - 1.96 * std_diff
    loa_high = mean_diff + 1.96 * std_diff

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.scatter(average, difference, color="#1f77b4")
    ax.axhline(mean_diff, color="#d62728", linestyle="--", label=f"Mean diff = {mean_diff:.2f}")
    ax.axhline(loa_low, color="#2ca02c", linestyle=":", label=f"LOA low = {loa_low:.2f}")
    ax.axhline(loa_high, color="#2ca02c", linestyle=":", label=f"LOA high = {loa_high:.2f}")
    ax.set_title(f"Bland–Altman: Ensemble vs Consensus ({_display_item_name(item)})")
    ax.set_xlabel("Average of ensemble and human consensus")
    ax.set_ylabel("Ensemble - human consensus")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def _save_confusion_matrix_plot(
    ensemble_scores: pd.DataFrame,
    human_consensus: pd.DataFrame,
    *,
    item: str,
    output_path: Path,
) -> None:
    spec = ITEM_SPECS[item]
    merged = ensemble_scores[["response_id", item]].merge(
        human_consensus[["response_id", item]],
        on="response_id",
        suffixes=("_ensemble", "_human"),
        how="inner",
    )
    left = discretize_series(merged[f"{item}_ensemble"], item)
    right = discretize_series(merged[f"{item}_human"], item)
    mask = left.notna() & right.notna()
    matrix = confusion_matrix(
        right[mask].astype(int),
        left[mask].astype(int),
        labels=spec.labels,
    )

    fig, ax = plt.subplots(figsize=(5, 4.5))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_title(f"Confusion Matrix: Ensemble vs Consensus ({_display_item_name(item)})")
    ax.set_xlabel("Ensemble (rounded category)")
    ax.set_ylabel("Human consensus (rounded category)")
    ax.set_xticks(range(len(spec.labels)))
    ax.set_yticks(range(len(spec.labels)))
    ax.set_xticklabels(spec.labels)
    ax.set_yticklabels(spec.labels)
    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            ax.text(
                column_index,
                row_index,
                str(matrix[row_index, column_index]),
                ha="center",
                va="center",
                color="black",
            )
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def _save_variance_histogram(
    variance_detail: pd.DataFrame,
    *,
    judge_name: str,
    output_path: Path,
) -> None:
    subset = variance_detail.loc[variance_detail["judge_name"].eq(judge_name)]
    counts = subset["bucket"].value_counts().reindex(
        ["exact", "off_by_1", "off_by_2_plus"],
        fill_value=0,
    )

    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    ax.bar(
        ["Exact", "Diff = 1", "Diff ≥ 2"],
        counts.values,
        color=["#2ca02c", "#ff7f0e", "#d62728"],
    )
    ax.set_title(f"Within-Judge Variance ({judge_name.title()})")
    ax.set_ylabel("Cell count")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def _generate_plots(
    *,
    analysis: dict[str, Any],
    plots_dir: Path,
) -> dict[str, str]:
    plots_dir.mkdir(parents=True, exist_ok=True)
    links: dict[str, str] = {}

    for item in LIKERT_ITEMS:
        filename = f"bland_altman_{item}.png"
        path = plots_dir / filename
        _save_bland_altman_plot(
            analysis["ensemble_scores"],
            analysis["human_consensus"],
            item=item,
            output_path=path,
        )
        links[f"bland_altman_{item}"] = f"agreement_plots/{filename}"

    for item in ORDINAL_ITEMS + LIKERT_ITEMS:
        filename = f"confusion_{item}.png"
        path = plots_dir / filename
        _save_confusion_matrix_plot(
            analysis["ensemble_scores"],
            analysis["human_consensus"],
            item=item,
            output_path=path,
        )
        links[f"confusion_{item}"] = f"agreement_plots/{filename}"

    for judge_name in MODEL_ORDER:
        filename = f"within_judge_variance_{judge_name}.png"
        path = plots_dir / filename
        _save_variance_histogram(
            analysis["within_judge_detail"],
            judge_name=judge_name,
            output_path=path,
        )
        links[f"variance_{judge_name}"] = f"agreement_plots/{filename}"

    return links


def _summary_table(analysis: dict[str, Any]) -> pd.DataFrame:
    frame = analysis["ensemble_vs_consensus"].copy()
    return frame.assign(
        rubric_item=frame["item"].map(_display_item_name),
        kappa=frame["primary_metric"].map(_format_float),
        icc_2_1=frame["icc_2_1"].map(_format_float),
        spearman_rho=frame["spearman_rho"].map(_format_float),
        interhuman_floor=frame["interhuman_primary_floor"].map(_format_float),
    )[
        [
            "rubric_item",
            "primary_metric_name",
            "kappa",
            "icc_2_1",
            "spearman_rho",
            "interhuman_floor",
            "verdict",
        ]
    ]


def _per_judge_tables(analysis: dict[str, Any]) -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {}
    for judge_name in MODEL_ORDER:
        subset = analysis["judge_vs_consensus"].loc[
            analysis["judge_vs_consensus"]["judge_name"].eq(judge_name)
        ].copy()
        tables[judge_name] = subset.assign(
            rubric_item=subset["item"].map(_display_item_name),
            kappa=subset["primary_metric"].map(_format_float),
            icc_2_1=subset["icc_2_1"].map(_format_float),
            spearman_rho=subset["spearman_rho"].map(_format_float),
            interhuman_floor=subset["interhuman_primary_floor"].map(_format_float),
        )[
            [
                "rubric_item",
                "primary_metric_name",
                "kappa",
                "icc_2_1",
                "spearman_rho",
                "interhuman_floor",
                "verdict",
            ]
        ]
    return tables


def _judge_reviewer_matrix_tables(analysis: dict[str, Any]) -> dict[str, pd.DataFrame]:
    matrix_tables: dict[str, pd.DataFrame] = {}
    pairwise = analysis["judge_vs_reviewer"]
    interhuman = analysis["interhuman_pairwise"]

    for item in ALL_ITEMS:
        rows: list[dict[str, Any]] = []
        for judge_name in MODEL_ORDER:
            row = {"Judge": _display_judge_name(judge_name, analysis["model_strings"])}
            for reviewer in HUMAN_ORDER:
                value = pairwise.loc[
                    pairwise["item"].eq(item)
                    & pairwise["judge_name"].eq(judge_name)
                    & pairwise["reviewer"].eq(reviewer),
                    "primary_metric",
                ].iloc[0]
                row[reviewer] = _format_float(value)
            human_values = interhuman.loc[interhuman["item"].eq(item), "primary_metric"]
            row["Min human-human"] = _format_float(human_values.min())
            row["Mean human-human"] = _format_float(human_values.mean())
            rows.append(row)
        matrix_tables[item] = pd.DataFrame(rows)

    return matrix_tables


def _interhuman_section_tables(analysis: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    pairwise = analysis["interhuman_pairwise"].copy()
    pairwise_table = pairwise.assign(
        rubric_item=pairwise["item"].map(_display_item_name),
        reviewer_pair=pairwise["reviewer_a"] + " vs " + pairwise["reviewer_b"],
        primary_metric=pairwise["primary_metric"].map(_format_float),
    )[
        ["rubric_item", "reviewer_pair", "primary_metric_name", "primary_metric"]
    ]

    icc = analysis["interhuman_icc"].copy()
    icc["rubric_item"] = icc["item"].map(_display_item_name)
    icc["icc_2_1"] = icc["icc_2_1"].map(_format_float)
    icc["manuscript_table2"] = icc["manuscript_table2"].map(_format_float)
    icc["delta_vs_manuscript"] = icc["delta_vs_manuscript"].map(_format_float)
    icc_table = icc[["rubric_item", "icc_2_1", "manuscript_table2", "delta_vs_manuscript"]]
    return pairwise_table, icc_table


def _interhuman_subset_section_tables(analysis: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tables: dict[str, dict[str, Any]] = {}
    for question_group in ("symptoms", "treatment"):
        pairwise = analysis["interhuman_subset"][question_group]["pairwise"].copy()
        pairwise_table = pairwise.assign(
            rubric_item=pairwise["item"].map(_display_item_name),
            reviewer_pair=pairwise["reviewer_a"] + " vs " + pairwise["reviewer_b"],
            primary_metric=pairwise["primary_metric"].map(_format_float),
        )[
            ["rubric_item", "reviewer_pair", "primary_metric_name", "primary_metric"]
        ]

        icc = analysis["interhuman_subset"][question_group]["icc"].copy()
        icc["rubric_item"] = icc["item"].map(_display_item_name)
        icc["icc_2_k"] = icc["icc_2_k"].map(_format_float)
        icc["manuscript_table2"] = icc["manuscript_table2"].map(_format_float)
        icc["delta_vs_manuscript"] = icc["delta_vs_manuscript"].map(_format_float)

        if question_group == "symptoms":
            icc_table = icc[
                ["rubric_item", "icc_type", "icc_2_k", "manuscript_table2", "delta_vs_manuscript"]
            ]
        else:
            icc_table = icc[["rubric_item", "icc_type", "icc_2_k"]]

        response_count = int(analysis["interhuman_subset"][question_group]["icc"]["response_count"].iloc[0])
        tables[question_group] = {
            "pairwise": pairwise_table,
            "icc": icc_table,
            "response_count": response_count,
        }
    return tables


def _within_judge_variance_table(analysis: dict[str, Any]) -> pd.DataFrame:
    summary = analysis["within_judge_summary"].copy()
    return summary.assign(
        judge=summary["judge_name"],
        exact=summary["exact_proportion"].map(_format_float),
        off_by_1=summary["off_by_1_proportion"].map(_format_float),
        off_by_2_plus=summary["off_by_2_plus_proportion"].map(_format_float),
    )[
        ["judge", "total_cells", "exact", "off_by_1", "off_by_2_plus"]
    ]


def _render_notable_disagreements(analysis: dict[str, Any]) -> str:
    entries = analysis["notable_disagreements"]
    if not entries:
        return "No response had an absolute ensemble-vs-consensus Likert difference of 2 or more."

    lines: list[str] = []
    lines.append(
        "Representative judge rationales below use the run closest to that judge's aggregated numeric profile."
    )
    for entry in entries:
        lines.append(f"### {entry['response_id']}")
        lines.append(f"Question: {entry['question_text']}")
        domains = ", ".join(
            f"{_display_item_name(domain['item'])} "
            f"(ensemble={domain['ensemble']:.2f}, human={domain['human_consensus']:.2f}, "
            f"|Δ|={domain['absolute_difference']:.2f})"
            for domain in entry["domains"]
        )
        lines.append(f"Domains meeting the ≥2 rule: {domains}")
        for judge_name in MODEL_ORDER:
            judge_data = entry[judge_name]
            lines.append(
                f"{judge_name.title()} rationale (model `{judge_data['model_used']}`, representative run {judge_data['representative_run_index']}):"
            )
            lines.append(judge_data["representative_rationale"] or "NA")
        lines.append("")
    return "\n\n".join(lines).strip()


def build_agreement_report(
    *,
    analysis: dict[str, Any],
    plot_links: dict[str, str],
) -> str:
    summary_table = _summary_table(analysis)
    per_judge_tables = _per_judge_tables(analysis)
    judge_reviewer_tables = _judge_reviewer_matrix_tables(analysis)
    interhuman_pairwise_table, interhuman_icc_table = _interhuman_section_tables(analysis)
    interhuman_subset_tables = _interhuman_subset_section_tables(analysis)
    variance_table = _within_judge_variance_table(analysis)

    model_strings = analysis["model_strings"]
    header = (
        "# Agreement Report\n\n"
        f"Dataset summary: 16 responses, 3 human reviewers ({', '.join(HUMAN_ORDER)}), "
        "2 judges, 3 runs per judge/response, and 96 total scored calls. "
        f"Claude model: `{model_strings.get('claude', 'NA')}`. "
        f"OpenAI model: `{model_strings.get('openai', 'NA')}`.\n\n"
        "Aggregation rules: within each judge, ordinal items use the median across 3 runs, "
        "binary complementarity uses the mode, and Likert items use the mean. Human consensus "
        "uses the same rules across the 3 reviewers. The ensemble is the mean of the two judges "
        "per response. Weighted kappa and confusion matrices use nearest-valid-category rounding "
        "when aggregation produces fractional values; ICC and Bland–Altman analyses use the raw "
        "continuous aggregates.\n"
    )

    sections: list[str] = [header]

    sections.append("## Section 1: Summary Table\n")
    sections.append(
        "Verdict logic: PASS requires the explicit CODEX threshold when one exists and also requires "
        "ensemble-vs-consensus agreement to be at least as high as the minimum pairwise inter-human "
        "agreement for the same item. REVIEW means only one criterion is met, or no explicit threshold "
        "exists and the result falls short of the inter-human floor. FAIL means both explicit criteria fail.\n"
    )
    sections.append(
        _render_markdown_table(
            summary_table,
            [
                "rubric_item",
                "primary_metric_name",
                "kappa",
                "icc_2_1",
                "spearman_rho",
                "interhuman_floor",
                "verdict",
            ],
        )
    )
    sections.append("\nPlots:")
    for item in LIKERT_ITEMS:
        sections.append(f"- Bland–Altman {_display_item_name(item)}: [{plot_links[f'bland_altman_{item}']}]({plot_links[f'bland_altman_{item}']})")
    for item in ORDINAL_ITEMS + LIKERT_ITEMS:
        sections.append(f"- Confusion matrix {_display_item_name(item)}: [{plot_links[f'confusion_{item}']}]({plot_links[f'confusion_{item}']})")

    sections.append("\n## Section 2: Per-Judge Breakdown\n")
    for judge_name in MODEL_ORDER:
        sections.append(f"### {_display_judge_name(judge_name, model_strings)}\n")
        sections.append(
            _render_markdown_table(
                per_judge_tables[judge_name],
                [
                    "rubric_item",
                    "primary_metric_name",
                    "kappa",
                    "icc_2_1",
                    "spearman_rho",
                    "interhuman_floor",
                    "verdict",
                ],
            )
        )
        sections.append("")

    sections.append("## Section 3: Judge-vs-Individual-Human Matrix\n")
    sections.append(
        "Each table reports the primary agreement metric for that rubric item: quadratic weighted kappa "
        "for ordinal/Likert items and unweighted kappa for complementarity.\n"
    )
    for item in ALL_ITEMS:
        sections.append(f"### {_display_item_name(item)}\n")
        sections.append(
            _render_markdown_table(
                judge_reviewer_tables[item],
                ["Judge", "MDO", "WD", "EG", "Min human-human", "Mean human-human"],
            )
        )
        sections.append("")

    sections.append("## Section 4: Inter-Human Reliability\n")
    sections.append("### Pairwise Human Agreement\n")
    sections.append(
        _render_markdown_table(
            interhuman_pairwise_table,
            ["rubric_item", "reviewer_pair", "primary_metric_name", "primary_metric"],
        )
    )
    sections.append("\n### ICC Comparison to Manuscript Table 2\n")
    sections.append(
        _render_markdown_table(
            interhuman_icc_table,
            ["rubric_item", "icc_2_1", "manuscript_table2", "delta_vs_manuscript"],
        )
    )
    sections.append(
        "\nNote: the recomputed human ICC(2,1) values above are derived directly from the source reviewer "
        "spreadsheets. If they differ from the manuscript values "
        f"({', '.join(f'{_display_item_name(k)}={v:.2f}' for k, v in MANUSCRIPT_TABLE2_REFERENCE.items())}), "
        "that indicates the manuscript likely used a different ICC parameterization and/or preprocessing path."
    )

    sections.append("\n## Section 4b: Symptoms-subset inter-human ICC(2,k)\n")
    sections.append(
        f"Symptoms subset: `{interhuman_subset_tables['symptoms']['response_count']}` responses with "
        "`question_group == 'symptoms'`. Treatment subset: "
        f"`{interhuman_subset_tables['treatment']['response_count']}` responses with "
        "`question_group == 'treatment'`. ICC in this subsection uses two-way random absolute agreement "
        "average measures, i.e. ICC(A,k) / ICC(2,k).\n"
    )
    sections.append("### Symptoms-only Pairwise Human Agreement\n")
    sections.append(
        _render_markdown_table(
            interhuman_subset_tables["symptoms"]["pairwise"],
            ["rubric_item", "reviewer_pair", "primary_metric_name", "primary_metric"],
        )
    )
    sections.append("\n### Symptoms-only ICC(2,k) vs Manuscript Table 2\n")
    sections.append(
        _render_markdown_table(
            interhuman_subset_tables["symptoms"]["icc"],
            ["rubric_item", "icc_type", "icc_2_k", "manuscript_table2", "delta_vs_manuscript"],
        )
    )
    sections.append(
        "\nThe manuscript comparison above is applied only to the symptoms subset, because that was the "
        "requested cross-check against Table 2."
    )
    sections.append("\n### Treatment-only Pairwise Human Agreement\n")
    sections.append(
        _render_markdown_table(
            interhuman_subset_tables["treatment"]["pairwise"],
            ["rubric_item", "reviewer_pair", "primary_metric_name", "primary_metric"],
        )
    )
    sections.append("\n### Treatment-only ICC(2,k)\n")
    sections.append(
        _render_markdown_table(
            interhuman_subset_tables["treatment"]["icc"],
            ["rubric_item", "icc_type", "icc_2_k"],
        )
    )

    sections.append("\n## Section 5: Notable Disagreements\n")
    sections.append(_render_notable_disagreements(analysis))

    sections.append("\n## Section 6: Within-Judge Variance\n")
    sections.append(
        _render_markdown_table(
            variance_table,
            ["judge", "total_cells", "exact", "off_by_1", "off_by_2_plus"],
        )
    )
    sections.append("\nPlots:")
    for judge_name in MODEL_ORDER:
        sections.append(
            f"- {_display_judge_name(judge_name, model_strings)} within-judge variance: "
            f"[{plot_links[f'variance_{judge_name}']}]({plot_links[f'variance_{judge_name}']})"
        )

    return "\n".join(sections).strip() + "\n"


def run_phase5_report(
    *,
    human_long_path: Path,
    judge_raw_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Load inputs, compute Phase 5 artifacts, and write the report and plots."""

    human_long = pd.read_parquet(human_long_path)
    judge_raw = pd.read_parquet(judge_raw_path)
    analysis = phase5_analysis(human_long=human_long, judge_raw=judge_raw)

    output_dir.mkdir(parents=True, exist_ok=True)
    plots_dir = output_dir / "agreement_plots"

    analysis["judge_aggregated"].drop(
        columns=["representative_rationale"], errors="ignore"
    ).to_parquet(output_dir / "judge_scores_aggregated.parquet", index=False)
    analysis["ensemble_scores"].to_parquet(output_dir / "ensemble_scores.parquet", index=False)

    plot_links = _generate_plots(analysis=analysis, plots_dir=plots_dir)
    report_markdown = build_agreement_report(analysis=analysis, plot_links=plot_links)
    report_path = output_dir / "agreement_report.md"
    report_path.write_text(report_markdown, encoding="utf-8")

    return {
        "report_path": report_path,
        "plots_dir": plots_dir,
        "analysis": analysis,
    }
