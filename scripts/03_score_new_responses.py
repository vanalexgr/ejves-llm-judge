from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.comparator import prepare_phase6_inputs, run_phase6  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the restricted Phase 6 comparator pipeline."
    )
    parser.add_argument(
        "--input-csv",
        required=True,
        type=Path,
        help="Comparator response CSV with response_id, disease, domain, question_text, response_text, source_model.",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "comparator",
        type=Path,
        help="Directory for comparator outputs.",
    )
    parser.add_argument(
        "--per-call-output-dir",
        default=REPO_ROOT / "outputs" / "comparator" / "phase6_scores",
        type=Path,
        help="Directory for per-call JSON artifacts.",
    )
    parser.add_argument(
        "--provider-concurrency",
        default=3,
        type=int,
        help="Concurrent response tasks per provider.",
    )
    parser.add_argument(
        "--mario-review-output",
        type=Path,
        default=None,
        help="Optional explicit output path for Mario's accuracy review CSV.",
    )
    parser.add_argument(
        "--mario-review-input",
        type=Path,
        default=None,
        help="Optional completed Mario accuracy review CSV to merge into the final comparator results.",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="Validate the comparator CSV and write Mario's review sheet without making API calls.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.prepare_only:
            mario_review_path = prepare_phase6_inputs(
                input_csv=args.input_csv,
                output_dir=args.output_dir,
                mario_review_output_path=args.mario_review_output,
            )
            print("Phase 6 preparation completed.")
            print(f"Mario review sheet: {mario_review_path}")
            return 0

        summary = run_phase6(
            input_csv=args.input_csv,
            per_call_output_dir=args.per_call_output_dir,
            output_dir=args.output_dir,
            provider_concurrency=args.provider_concurrency,
            mario_review_output_path=args.mario_review_output,
            mario_review_input_path=args.mario_review_input,
        )
    except Exception as exc:
        print(f"Phase 6 failed: {exc}", file=sys.stderr)
        return 1

    print("Phase 6 completed.")
    print(f"Claude model requested: {summary.claude_model_requested}")
    print(f"OpenAI model requested: {summary.openai_model_requested}")
    print(f"Comparator responses: {summary.response_count}")
    print(f"Successful calls: {summary.successful_calls}")
    print(f"Failed calls: {summary.failed_calls}")
    if summary.failures:
        print(f"Failures: {', '.join(summary.failures)}")
    else:
        print("Failures: none")
    print(f"Mario review sheet: {summary.mario_review_sheet_path}")
    print(f"Total latency_seconds: {summary.total_latency_seconds:.3f}")
    print(f"Estimated cost_usd: {summary.estimated_cost_usd:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

