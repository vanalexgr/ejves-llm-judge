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
    build_accuracy_adjudication_table,
    build_blinded_third_reviewer_packet,
    build_dual_accuracy_review_table,
    build_dual_accuracy_summary,
    build_phase6_results_with_dual_accuracy,
    build_revised_dual_accuracy_review_table,
    load_mario_accuracy_rationale,
    load_mario_accuracy_review,
    load_vga_accuracy_rationale,
    load_vga_accuracy_review,
    write_accuracy_adjudication_workbook,
    write_third_reviewer_packet_workbook,
    write_dual_accuracy_workbook,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare revision-aware adjudication outputs for dual human accuracy review."
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
        "--mario-rationale",
        required=True,
        type=Path,
        help="Mario rationale file for adjudication cases (.csv or .xlsx).",
    )
    parser.add_argument(
        "--vga-rationale",
        required=True,
        type=Path,
        help="VGA rationale file for adjudication cases (.csv or .xlsx).",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "comparator",
        type=Path,
        help="Directory for adjudication outputs.",
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
        adjudication_ids = set(
            merged_reviews.loc[
                merged_reviews["human_accuracy_resolution_status"].eq("adjudication_needed"),
                "response_id",
            ]
        )
        mario_rationale = load_mario_accuracy_rationale(
            args.mario_rationale,
            expected_response_ids=adjudication_ids,
        )
        vga_rationale = load_vga_accuracy_rationale(
            args.vga_rationale,
            expected_response_ids=adjudication_ids,
        )
        adjudication_table = build_accuracy_adjudication_table(
            dual_accuracy_reviews=merged_reviews,
            mario_rationale=mario_rationale,
            vga_rationale=vga_rationale,
        )
        revised_reviews = build_revised_dual_accuracy_review_table(
            dual_accuracy_reviews=merged_reviews,
            adjudication_table=adjudication_table,
        )
        revised_summary, revised_by_model = build_dual_accuracy_summary(revised_reviews)
        revised_provisional = build_phase6_results_with_dual_accuracy(
            ensemble_scores=reference,
            dual_accuracy_reviews=revised_reviews,
        )
        blinded_packet = build_blinded_third_reviewer_packet(adjudication_table)
    except Exception as exc:
        print(f"Adjudication preparation failed: {exc}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    adjudication_csv = args.output_dir / "accuracy_adjudication_master.csv"
    adjudication_parquet = args.output_dir / "accuracy_adjudication_master.parquet"
    adjudication_workbook = args.output_dir / "accuracy_adjudication_master.xlsx"
    third_reviewer_csv = args.output_dir / "accuracy_third_reviewer_packet.csv"
    third_reviewer_workbook = args.output_dir / "accuracy_third_reviewer_packet.xlsx"
    revised_csv = args.output_dir / "dual_accuracy_reviews_mario_revised.csv"
    revised_parquet = args.output_dir / "dual_accuracy_reviews_mario_revised.parquet"
    revised_workbook = args.output_dir / "dual_accuracy_reviews_mario_revised.xlsx"
    revised_provisional_csv = (
        args.output_dir / "comparator_results_dual_human_mario_revised_provisional.csv"
    )
    revised_provisional_parquet = (
        args.output_dir / "comparator_results_dual_human_mario_revised_provisional.parquet"
    )

    adjudication_table.to_csv(adjudication_csv, index=False)
    adjudication_table.to_parquet(adjudication_parquet, index=False)
    blinded_packet.to_csv(third_reviewer_csv, index=False)
    revised_reviews.to_csv(revised_csv, index=False)
    revised_reviews.to_parquet(revised_parquet, index=False)
    revised_provisional.to_csv(revised_provisional_csv, index=False)
    revised_provisional.to_parquet(revised_provisional_parquet, index=False)

    write_accuracy_adjudication_workbook(
        adjudication_table=adjudication_table,
        output_path=adjudication_workbook,
    )
    write_third_reviewer_packet_workbook(
        third_reviewer_packet=blinded_packet,
        output_path=third_reviewer_workbook,
    )
    write_dual_accuracy_workbook(
        summary=revised_summary,
        by_model=revised_by_model,
        merged_reviews=revised_reviews,
        output_path=revised_workbook,
    )

    revised_unresolved = int(
        revised_reviews["human_accuracy_resolution_status"].eq("adjudication_needed").sum()
    )
    revisions_applied = int(adjudication_table["mario_revision_applied"].sum())

    print("Adjudication preparation completed.")
    print(f"Original adjudication cases: {len(adjudication_table)}")
    print(f"Mario explicit score revisions detected: {revisions_applied}")
    print(f"Remaining >=2 disagreements after Mario revisions: {revised_unresolved}")
    print(f"Adjudication master workbook: {adjudication_workbook}")
    print(f"Third reviewer packet workbook: {third_reviewer_workbook}")
    print(f"Revision-aware merged reviews: {revised_workbook}")
    print(f"Revision-aware provisional results: {revised_provisional_parquet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
