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
    build_final_accuracy_review_table,
    build_final_accuracy_summary,
    build_phase6_results_with_final_accuracy,
    load_third_accuracy_review,
    write_dual_accuracy_workbook,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Finalize comparator accuracy after third-reviewer adjudication."
    )
    parser.add_argument(
        "--ensemble-parquet",
        default=REPO_ROOT / "outputs" / "comparator" / "ensemble_scores.parquet",
        type=Path,
        help="Ensemble comparator parquet.",
    )
    parser.add_argument(
        "--adjudication-master-parquet",
        default=REPO_ROOT / "outputs" / "comparator" / "accuracy_adjudication_master.parquet",
        type=Path,
        help="Adjudication master parquet from the previous step.",
    )
    parser.add_argument(
        "--revised-dual-parquet",
        default=REPO_ROOT / "outputs" / "comparator" / "dual_accuracy_reviews_mario_revised.parquet",
        type=Path,
        help="Revision-aware dual human review parquet.",
    )
    parser.add_argument(
        "--third-review",
        required=True,
        type=Path,
        help="Third reviewer workbook or CSV.",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "comparator",
        type=Path,
        help="Directory for final resolved outputs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        ensemble_scores = pd.read_parquet(args.ensemble_parquet)
        adjudication_master = pd.read_parquet(args.adjudication_master_parquet)
        revised_dual = pd.read_parquet(args.revised_dual_parquet)
        third_review = load_third_accuracy_review(
            args.third_review,
            expected_response_ids=set(adjudication_master["response_id"].astype(str)),
        )
        final_reviews = build_final_accuracy_review_table(
            revised_dual_accuracy_reviews=revised_dual,
            adjudication_table=adjudication_master,
            third_reviewer_review=third_review,
        )
        summary, by_model = build_final_accuracy_summary(final_reviews)
        final_results = build_phase6_results_with_final_accuracy(
            ensemble_scores=ensemble_scores,
            final_accuracy_reviews=final_reviews,
        )
    except Exception as exc:
        print(f"Final adjudication merge failed: {exc}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    final_reviews_csv = args.output_dir / "dual_accuracy_reviews_final.csv"
    final_reviews_parquet = args.output_dir / "dual_accuracy_reviews_final.parquet"
    final_reviews_workbook = args.output_dir / "dual_accuracy_reviews_final.xlsx"
    final_results_csv = args.output_dir / "comparator_results_final_human_accuracy.csv"
    final_results_parquet = args.output_dir / "comparator_results_final_human_accuracy.parquet"
    canonical_results_csv = args.output_dir / "comparator_results.csv"
    canonical_results_parquet = args.output_dir / "comparator_results.parquet"

    final_reviews.to_csv(final_reviews_csv, index=False)
    final_reviews.to_parquet(final_reviews_parquet, index=False)
    final_results.to_csv(final_results_csv, index=False)
    final_results.to_parquet(final_results_parquet, index=False)
    final_results.to_csv(canonical_results_csv, index=False)
    final_results.to_parquet(canonical_results_parquet, index=False)
    write_dual_accuracy_workbook(
        summary=summary,
        by_model=by_model,
        merged_reviews=final_reviews,
        output_path=final_reviews_workbook,
    )

    by_source_model_dir = args.output_dir / "by_source_model"
    by_source_model_dir.mkdir(parents=True, exist_ok=True)
    for source_model, group in final_results.groupby("source_model", sort=True):
        model_dir = by_source_model_dir / str(source_model)
        model_dir.mkdir(parents=True, exist_ok=True)
        group.to_parquet(model_dir / "comparator_results.parquet", index=False)
        group.to_csv(model_dir / "comparator_results.csv", index=False)

    triple_cases = int(final_reviews["third_reviewer_used"].fillna(False).sum())
    mean_accuracy = float(final_reviews["final_validated_accuracy"].astype(float).mean())

    print("Final adjudication merge completed.")
    print(f"Final review rows: {len(final_reviews)}")
    print(f"Third-reviewer adjudication cases used: {triple_cases}")
    print(f"Mean final validated accuracy: {mean_accuracy:.3f}")
    print(f"Final reviews workbook: {final_reviews_workbook}")
    print(f"Canonical comparator results: {canonical_results_parquet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
