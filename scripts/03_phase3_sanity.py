from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

import pandas as pd
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ejves_judge.judges.claude import ClaudeJudge  # noqa: E402
from ejves_judge.judges.openai import OpenAIJudge  # noqa: E402
from ejves_judge.prompt_builder import build_prompt  # noqa: E402


def _load_cached_result(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 3 sanity checks.")
    parser.add_argument(
        "--input-parquet",
        default=REPO_ROOT / "data" / "processed" / "human_scores_long.parquet",
        type=Path,
        help="Phase 1 long-format parquet input.",
    )
    parser.add_argument(
        "--output-dir",
        default=REPO_ROOT / "outputs" / "phase3_sanity",
        type=Path,
        help="Directory where the sanity-check artifacts will be written.",
    )
    return parser.parse_args()


def _load_prompt_row(input_parquet: Path, response_id: str = "AAA_SS1") -> dict[str, str]:
    long_df = pd.read_parquet(input_parquet)
    rows = (
        long_df[
            ["response_id", "question_group", "domain", "question_text", "response_text"]
        ]
        .drop_duplicates(subset=["response_id"])
        .set_index("response_id")
    )
    if response_id not in rows.index:
        raise ValueError(f"Missing response_id in Phase 1 parquet: {response_id}")
    row = rows.loc[response_id]
    return {
        "response_id": response_id,
        "question_group": str(row["question_group"]),
        "domain": str(row["domain"]),
        "question_text": str(row["question_text"]),
        "response_text": str(row["response_text"]),
    }


def _print_result(label: str, result) -> None:
    parsed = result.parsed_response.model_dump(mode="json")
    rationale = parsed.pop("rationale")
    print(f"{label} model: {result.model_used}")
    print(f"{label} latency_seconds: {result.latency_seconds:.3f}")
    print(f"{label} parsed_scores: {json.dumps(parsed, ensure_ascii=True)}")
    print(f"{label} rationale: {rationale}")


def _print_cached_result(label: str, payload: dict[str, object]) -> None:
    parsed = dict(payload["parsed_response"])
    rationale = parsed.pop("rationale")
    print(f"{label} model: {payload['model_used']}")
    print(f"{label} latency_seconds: {payload['latency_seconds']:.3f}")
    print(f"{label} parsed_scores: {json.dumps(parsed, ensure_ascii=True)}")
    print(f"{label} rationale: {rationale}")


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt_row = _load_prompt_row(args.input_parquet)
    prompt_result = build_prompt(**prompt_row)

    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not anthropic_api_key:
        print("Phase 3 failed: missing ANTHROPIC_API_KEY.", file=sys.stderr)
        return 1
    if not openai_key:
        print("Phase 3 failed: missing OPENAI_API_KEY.", file=sys.stderr)
        return 1

    claude_output_path = output_dir / f"claude_{prompt_row['response_id']}.json"
    cached_claude = _load_cached_result(claude_output_path)
    if cached_claude is not None:
        _print_cached_result("Claude", cached_claude)
    else:
        claude_judge = ClaudeJudge(api_key=anthropic_api_key, model="claude-opus-4-7")
        claude_result = claude_judge.score(
            response_id=prompt_row["response_id"],
            prompt=prompt_result.prompt,
            question_group=prompt_row["question_group"],
        )
        claude_result.write_json(claude_output_path)
        _print_result("Claude", claude_result)

    openai_model = OpenAIJudge.discover_gpt5_model(api_key=openai_key)
    openai_judge = OpenAIJudge(api_key=openai_key, model=openai_model)
    openai_output_path = output_dir / f"openai_{prompt_row['response_id']}.json"
    cached_openai = _load_cached_result(openai_output_path)
    if cached_openai is not None:
        _print_cached_result("OpenAI", cached_openai)
    else:
        openai_result = openai_judge.score(
            response_id=prompt_row["response_id"],
            prompt=prompt_result.prompt,
            question_group=prompt_row["question_group"],
        )
        openai_result.write_json(openai_output_path)
        _print_result("OpenAI", openai_result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
