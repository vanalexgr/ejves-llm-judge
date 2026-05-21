from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.comparator_report import write_comparator_report  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the final comparator report and manuscript-ready summary tables."
    )
    parser.add_argument(
        "--comparator-results",
        default=REPO_ROOT / "outputs" / "comparator" / "comparator_results.parquet",
        type=Path,
        help="Final comparator parquet with resolved human accuracy.",
    )
    parser.add_argument(
        "--original-consensus",
        default=REPO_ROOT / "data" / "processed" / "human_scores_consensus.parquet",
        type=Path,
        help="Original reconstructed GPT-3.5 consensus parquet.",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "comparator",
        type=Path,
        help="Directory for the generated report and summary tables.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        outputs = write_comparator_report(
            comparator_results_path=args.comparator_results,
            original_consensus_path=args.original_consensus,
            output_dir=args.output_dir,
        )
    except Exception as exc:
        print(f"Comparator report generation failed: {exc}", file=sys.stderr)
        return 1

    print("Comparator report generation completed.")
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
