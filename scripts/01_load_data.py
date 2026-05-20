from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.data_loader import run_phase_one  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 1 data extraction.")
    parser.add_argument(
        "--raw-dir",
        default=REPO_ROOT / "data" / "raw",
        type=Path,
        help="Directory containing the raw reviewer workbooks.",
    )
    parser.add_argument(
        "--processed-dir",
        default=REPO_ROOT / "data" / "processed",
        type=Path,
        help="Directory where processed outputs will be written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        long_df, consensus_df, outputs, reconciliation_summary = run_phase_one(
            raw_dir=args.raw_dir,
            processed_dir=args.processed_dir,
        )
    except Exception as exc:
        print(f"Phase 1 failed: {exc}", file=sys.stderr)
        return 1

    print("Phase 1 completed successfully.")
    print(reconciliation_summary.log_line())
    print(reconciliation_summary.missing_scores_log_line())
    print(f"Long rows: {len(long_df)}")
    print(f"Consensus rows: {len(consensus_df)}")
    print(f"Unique response_id: {long_df['response_id'].nunique()}")
    print(
        "Reviewers per response: "
        f"{sorted(long_df.groupby('response_id')['reviewer'].nunique().unique().tolist())}"
    )
    for name, path in outputs.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
