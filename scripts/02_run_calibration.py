from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.scoring import run_phase4  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 4 full scoring calibration.")
    parser.add_argument(
        "--input-parquet",
        default=REPO_ROOT / "data" / "processed" / "human_scores_long.parquet",
        type=Path,
        help="Phase 1 long-format parquet input.",
    )
    parser.add_argument(
        "--per-call-output-dir",
        default=REPO_ROOT / "outputs" / "phase4_scores",
        type=Path,
        help="Directory for per-call JSON artifacts.",
    )
    parser.add_argument(
        "--calibration-output-dir",
        default=REPO_ROOT / "outputs" / "calibration",
        type=Path,
        help="Directory for parquet outputs.",
    )
    parser.add_argument(
        "--provider-concurrency",
        default=3,
        type=int,
        help="Concurrent response tasks per provider.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = run_phase4(
            input_parquet=args.input_parquet,
            per_call_output_dir=args.per_call_output_dir,
            calibration_output_dir=args.calibration_output_dir,
            provider_concurrency=args.provider_concurrency,
        )
    except Exception as exc:
        print(f"Phase 4 failed: {exc}", file=sys.stderr)
        return 1

    print("Phase 4 completed.")
    print(f"Claude model requested: {summary.claude_model_requested}")
    print(f"OpenAI model requested: {summary.openai_model_requested}")
    print(f"Successful calls: {summary.successful_calls}")
    print(f"Failed calls: {summary.failed_calls}")
    if summary.failures:
        print(f"Failures: {', '.join(summary.failures)}")
    else:
        print("Failures: none")
    print(f"Total latency_seconds: {summary.total_latency_seconds:.3f}")
    print(f"Estimated cost_usd: {summary.estimated_cost_usd:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
