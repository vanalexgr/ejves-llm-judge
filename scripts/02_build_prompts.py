from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.prompt_builder import build_prompt  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 2 prompt generation.")
    parser.add_argument(
        "--input-parquet",
        default=REPO_ROOT / "data" / "processed" / "human_scores_long.parquet",
        type=Path,
        help="Phase 1 long-format parquet input.",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "phase2_prompts",
        type=Path,
        help="Directory where prompt text files and manifest will be written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input_parquet.exists():
        print(f"Phase 2 failed: missing input parquet: {args.input_parquet}", file=sys.stderr)
        return 1

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    long_df = pd.read_parquet(args.input_parquet)
    responses_df = (
        long_df[
            [
                "response_id",
                "question_group",
                "domain",
                "question_text",
                "response_text",
            ]
        ]
        .drop_duplicates(subset=["response_id"])
        .sort_values("response_id", kind="stable")
        .reset_index(drop=True)
    )

    if len(responses_df) != 16:
        print(
            f"Phase 2 failed: expected 16 unique responses, found {len(responses_df)}.",
            file=sys.stderr,
        )
        return 1

    manifest: list[dict[str, object]] = []
    for row in responses_df.itertuples(index=False):
        result = build_prompt(
            response_id=row.response_id,
            question_text=row.question_text,
            response_text=row.response_text,
            question_group=row.question_group,
            domain=row.domain,
        )
        prompt_path = output_dir / f"{row.response_id}.txt"
        prompt_path.write_text(result.prompt, encoding="utf-8")
        manifest.append(
            {
                "response_id": result.response_id,
                "question_group": result.question_group,
                "blinding_substitution_count": result.blinding_substitution_count,
                "prompt_character_length": result.prompt_character_length,
            }
        )

    manifest_path = output_dir / "prompts_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Phase 2 completed successfully.")
    print(f"Prompt count: {len(manifest)}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
