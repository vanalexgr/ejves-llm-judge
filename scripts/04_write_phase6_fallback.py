from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.phase6_fallback import write_phase6_fallback_documents  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write comparator methodology and Methods addendum from the completed calibration run."
    )
    parser.add_argument(
        "--human-long-path",
        default=REPO_ROOT / "data" / "processed" / "human_scores_long.parquet",
        type=Path,
        help="Phase 1 long-format human parquet.",
    )
    parser.add_argument(
        "--judge-raw-path",
        default=REPO_ROOT / "outputs" / "calibration" / "judge_scores_raw.parquet",
        type=Path,
        help="Completed Phase 4 raw judge parquet.",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "calibration",
        type=Path,
        help="Directory for the generated Markdown outputs.",
    )
    parser.add_argument(
        "--accuracy-spotcheck-count",
        default=48,
        type=int,
        help="Number of comparator responses included in the blinded human accuracy workflow.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        paths = write_phase6_fallback_documents(
            human_long_path=args.human_long_path,
            judge_raw_path=args.judge_raw_path,
            output_dir=args.output_dir,
            comparator_response_count=args.accuracy_spotcheck_count,
        )
    except Exception as exc:
        print(f"Phase 6 fallback documentation failed: {exc}", file=sys.stderr)
        return 1

    print("Phase 6 fallback documentation completed.")
    for label, path in paths.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
