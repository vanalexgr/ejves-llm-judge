from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.comparator import (  # noqa: E402
    build_dual_accuracy_review_table,
    build_dual_accuracy_summary,
    build_phase6_results_with_dual_accuracy,
    load_mario_accuracy_review,
    load_vga_accuracy_review,
    write_dual_accuracy_workbook,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge Mario and VGA accuracy reviews for the comparator arm."
    )
    parser.add_argument(
        "--reference-parquet",
        default=REPO_ROOT / "outputs" / "comparator" / "ensemble_scores.parquet",
        type=Path,
        help="Reference comparator parquet with response metadata.",
    )
    parser.add_argument(
        "--mario-review",
        required=True,
        type=Path,
        help="Mario accuracy review file (.csv or .xlsx).",
    )
    parser.add_argument(
        "--vga-review",
        required=True,
        type=Path,
        help="VGA accuracy review file (.csv or .xlsx).",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "comparator",
        type=Path,
        help="Directory for merged accuracy outputs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        reference = pd.read_parquet(args.reference_parquet)
        expected_response_ids = set(reference["response_id"].astype(str))
        mario_review = load_mario_accuracy_review(
            args.mario_review,
            expected_response_ids=expected_response_ids,
        )
        vga_review = load_vga_accuracy_review(
            args.vga_review,
            expected_response_ids=expected_response_ids,
        )
        merged_reviews = build_dual_accuracy_review_table(
            reference_frame=reference,
            mario_review=mario_review,
            vga_review=vga_review,
        )
        summary, by_model = build_dual_accuracy_summary(merged_reviews)
        provisional_results = build_phase6_results_with_dual_accuracy(
            ensemble_scores=reference,
            dual_accuracy_reviews=merged_reviews,
        )
    except Exception as exc:
        print(f"Dual accuracy merge failed: {exc}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    merged_csv = args.output_dir / "dual_accuracy_reviews.csv"
    merged_parquet = args.output_dir / "dual_accuracy_reviews.parquet"
    workbook_path = args.output_dir / "dual_accuracy_reviews.xlsx"
    adjudication_csv = args.output_dir / "accuracy_adjudication_needed.csv"
    provisional_csv = args.output_dir / "comparator_results_dual_human_provisional.csv"
    provisional_parquet = args.output_dir / "comparator_results_dual_human_provisional.parquet"

    merged_reviews.to_csv(merged_csv, index=False)
    merged_reviews.to_parquet(merged_parquet, index=False)
    merged_reviews.loc[
        merged_reviews["human_accuracy_resolution_status"].eq("adjudication_needed")
    ].to_csv(adjudication_csv, index=False)
    provisional_results.to_csv(provisional_csv, index=False)
    provisional_results.to_parquet(provisional_parquet, index=False)
    write_dual_accuracy_workbook(
        summary=summary,
        by_model=by_model,
        merged_reviews=merged_reviews,
        output_path=workbook_path,
    )

    exact_agree = int(merged_reviews["human_accuracy_resolution_status"].eq("exact_agreement").sum())
    diff_1 = int(merged_reviews["human_accuracy_resolution_status"].eq("minor_disagreement").sum())
    diff_ge_2 = int(merged_reviews["human_accuracy_resolution_status"].eq("adjudication_needed").sum())
    weighted_kappa = float(
        summary.loc[summary["metric"].eq("quadratic_weighted_kappa"), "value"].iloc[0]
    )

    print("Dual accuracy merge completed.")
    print(f"Merged rows: {len(merged_reviews)}")
    print(f"Exact agreement: {exact_agree}")
    print(f"Difference of 1: {diff_1}")
    print(f"Difference of 2+: {diff_ge_2}")
    print(f"Quadratic weighted kappa: {weighted_kappa:.3f}")
    print(f"Merged review workbook: {workbook_path}")
    print(f"Adjudication sheet CSV: {adjudication_csv}")
    print(f"Provisional comparator results: {provisional_parquet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
