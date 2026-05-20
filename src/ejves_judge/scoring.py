"""Phase 4 scoring orchestration."""

from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import time
from typing import Any

import pandas as pd
from dotenv import load_dotenv

from .judges.base import BaseJudge
from .judges.claude import ClaudeJudge
from .judges.openai import OpenAIJudge
from .prompt_builder import build_prompt


OPENAI_PRICING = {
    "input_per_million": 1.25,
    "cached_input_per_million": 0.125,
    "output_per_million": 10.0,
}
ANTHROPIC_PRICING = {
    "input_per_million": 5.0,
    "output_per_million": 25.0,
}
ANTHROPIC_PROVIDER_CONCURRENCY = 1


@dataclass(frozen=True)
class ScoreTarget:
    response_id: str
    question_group: str
    domain: str
    question_text: str
    response_text: str
    prompt: str


@dataclass(frozen=True)
class Phase4Summary:
    successful_calls: int
    failed_calls: int
    failures: tuple[str, ...]
    total_latency_seconds: float
    estimated_cost_usd: float
    openai_model_requested: str
    claude_model_requested: str


def load_score_targets(input_parquet: Path) -> list[ScoreTarget]:
    long_df = pd.read_parquet(input_parquet)
    response_rows = (
        long_df[
            ["response_id", "question_group", "domain", "question_text", "response_text"]
        ]
        .drop_duplicates(subset=["response_id"])
        .sort_values("response_id", kind="stable")
        .reset_index(drop=True)
    )
    if len(response_rows) != 16:
        raise ValueError(f"Expected 16 unique responses, found {len(response_rows)}.")

    targets: list[ScoreTarget] = []
    for row in response_rows.itertuples(index=False):
        prompt_result = build_prompt(
            response_id=row.response_id,
            question_text=row.question_text,
            response_text=row.response_text,
            question_group=row.question_group,
            domain=row.domain,
        )
        targets.append(
            ScoreTarget(
                response_id=row.response_id,
                question_group=row.question_group,
                domain=row.domain,
                question_text=row.question_text,
                response_text=row.response_text,
                prompt=prompt_result.prompt,
            )
        )
    return targets


def _json_path(output_dir: Path, judge_name: str, response_id: str, run_index: int) -> Path:
    return output_dir / f"{judge_name}_{response_id}_run{run_index}.json"


def _extract_error_payload(exc: Exception) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "error_type": exc.__class__.__name__,
        "error_message": str(exc),
    }
    response = getattr(exc, "response", None)
    if response is not None:
        try:
            payload["response_text"] = response.text
        except Exception:
            pass
        try:
            payload["status_code"] = response.status_code
        except Exception:
            pass
    request_id = getattr(exc, "request_id", None)
    if request_id:
        payload["request_id"] = request_id
    return payload


def _create_failure_payload(
    *,
    judge: BaseJudge,
    target: ScoreTarget,
    run_index: int,
    latency_seconds: float,
    exc: Exception,
) -> dict[str, Any]:
    error_payload = _extract_error_payload(exc)
    return {
        "status": "failed",
        "judge_name": judge.judge_name,
        "response_id": target.response_id,
        "question_group": target.question_group,
        "run_index": run_index,
        "model_used": judge.model,
        "latency_seconds": latency_seconds,
        "request_id": error_payload.get("request_id"),
        "request_payload": judge.build_logged_request_payload(
            prompt=target.prompt,
            question_group=target.question_group,
        ),
        "raw_response": error_payload,
        "parsed_response": None,
        "error": error_payload,
        "cache_hit": False,
    }


def _run_or_load_single_call(
    *,
    judge: BaseJudge,
    target: ScoreTarget,
    run_index: int,
    output_dir: Path,
) -> dict[str, Any]:
    artifact_path = _json_path(output_dir, judge.judge_name, target.response_id, run_index)
    if artifact_path.exists():
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
        payload["cache_hit"] = True
        return payload

    started = time.perf_counter()
    try:
        result = judge.score(
            response_id=target.response_id,
            prompt=target.prompt,
            question_group=target.question_group,
        )
        payload = {
            "status": "success",
            **result.to_json_dict(),
            "run_index": run_index,
            "cache_hit": False,
        }
    except Exception as exc:  # pragma: no cover - live API failure handling
        payload = _create_failure_payload(
            judge=judge,
            target=target,
            run_index=run_index,
            latency_seconds=time.perf_counter() - started,
            exc=exc,
        )

    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


async def _run_provider_pool(
    *,
    judge: BaseJudge,
    targets: list[ScoreTarget],
    output_dir: Path,
    concurrency: int,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency)

    async def run_target(target: ScoreTarget) -> list[dict[str, Any]]:
        async with semaphore:
            target_records: list[dict[str, Any]] = []
            for run_index in range(1, 4):
                payload = await asyncio.to_thread(
                    _run_or_load_single_call,
                    judge=judge,
                    target=target,
                    run_index=run_index,
                    output_dir=output_dir,
                )
                target_records.append(payload)
            return target_records

    provider_batches = await asyncio.gather(*(run_target(target) for target in targets))
    return [payload for batch in provider_batches for payload in batch]


def _raw_records_to_dataframe(records: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for record in records:
        parsed = record.get("parsed_response") or {}
        usage = (record.get("raw_response") or {}).get("usage", {})
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        cached_input_tokens = None
        if "input_tokens_details" in usage:
            cached_input_tokens = (usage.get("input_tokens_details") or {}).get("cached_tokens")
        elif "cache_read_input_tokens" in usage:
            cached_input_tokens = usage.get("cache_read_input_tokens")

        row = {
            "judge_name": record.get("judge_name"),
            "response_id": record.get("response_id"),
            "question_group": record.get("question_group"),
            "run_index": record.get("run_index"),
            "status": record.get("status"),
            "cache_hit": record.get("cache_hit", False),
            "model_used": record.get("model_used"),
            "latency_seconds": record.get("latency_seconds"),
            "request_id": record.get("request_id"),
            "error_type": (record.get("error") or {}).get("error_type"),
            "error_message": (record.get("error") or {}).get("error_message"),
            "request_payload": json.dumps(record.get("request_payload"), ensure_ascii=True),
            "raw_response": json.dumps(record.get("raw_response"), ensure_ascii=True),
            "input_tokens": input_tokens,
            "cached_input_tokens": cached_input_tokens,
            "output_tokens": output_tokens,
            "tone": parsed.get("tone"),
            "complementarity": parsed.get("complementarity"),
            "gilbert_urgency": parsed.get("gilbert_urgency"),
            "discern_q7": parsed.get("discern_q7"),
            "accuracy": parsed.get("accuracy"),
            "comprehensiveness": parsed.get("comprehensiveness"),
            "clarity": parsed.get("clarity"),
            "rationale": parsed.get("rationale"),
            "artifact_path": record.get("artifact_path"),
        }
        rows.append(row)

    df = pd.DataFrame(rows).sort_values(
        ["judge_name", "response_id", "run_index"], kind="stable"
    ).reset_index(drop=True)
    int_columns = [
        "run_index",
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "tone",
        "complementarity",
        "gilbert_urgency",
        "discern_q7",
        "accuracy",
        "comprehensiveness",
        "clarity",
    ]
    for column in int_columns:
        if column in df.columns:
            df[column] = df[column].astype("Int64")
    return df


def _aggregate_group(group: pd.DataFrame) -> pd.Series:
    has_failure = (~group["status"].eq("success")).any()
    result: dict[str, Any] = {
        "all_runs_successful": not has_failure,
        "successful_run_count": int(group["status"].eq("success").sum()),
    }
    score_columns = [
        "tone",
        "complementarity",
        "gilbert_urgency",
        "discern_q7",
        "accuracy",
        "comprehensiveness",
        "clarity",
    ]
    ordinal_columns = ["tone", "complementarity", "gilbert_urgency", "discern_q7"]
    mean_columns = ["accuracy", "comprehensiveness", "clarity"]

    for column in score_columns:
        values = group[column].dropna()
        if has_failure or values.empty:
            result[f"{column}_aggregated"] = pd.NA
        elif column in ordinal_columns:
            result[f"{column}_aggregated"] = float(values.median())
        else:
            result[f"{column}_aggregated"] = float(values.astype("Float64").mean())
    return pd.Series(result)


def _aggregated_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    grouped = raw_df.groupby(["judge_name", "response_id", "question_group"], sort=True, dropna=False)
    aggregated = grouped.apply(_aggregate_group).reset_index()
    return aggregated.sort_values(["judge_name", "response_id"], kind="stable").reset_index(drop=True)


def _estimate_openai_cost(raw_response: dict[str, Any]) -> float:
    usage = raw_response.get("usage") or {}
    input_tokens = usage.get("input_tokens") or 0
    cached_tokens = ((usage.get("input_tokens_details") or {}).get("cached_tokens")) or 0
    output_tokens = usage.get("output_tokens") or 0
    uncached_tokens = max(input_tokens - cached_tokens, 0)
    return (
        uncached_tokens * OPENAI_PRICING["input_per_million"]
        + cached_tokens * OPENAI_PRICING["cached_input_per_million"]
        + output_tokens * OPENAI_PRICING["output_per_million"]
    ) / 1_000_000


def _estimate_anthropic_cost(raw_response: dict[str, Any]) -> float:
    usage = raw_response.get("usage") or {}
    input_tokens = usage.get("input_tokens") or 0
    output_tokens = usage.get("output_tokens") or 0
    return (
        input_tokens * ANTHROPIC_PRICING["input_per_million"]
        + output_tokens * ANTHROPIC_PRICING["output_per_million"]
    ) / 1_000_000


def estimate_cost_usd(records: list[dict[str, Any]]) -> float:
    total = 0.0
    for record in records:
        if record.get("status") != "success":
            continue
        raw_response = record.get("raw_response") or {}
        if record.get("judge_name") == "openai":
            total += _estimate_openai_cost(raw_response)
        elif record.get("judge_name") == "claude":
            total += _estimate_anthropic_cost(raw_response)
    return total


async def run_phase4_async(
    *,
    input_parquet: Path,
    per_call_output_dir: Path,
    calibration_output_dir: Path,
    provider_concurrency: int = 3,
) -> Phase4Summary:
    load_dotenv(Path.cwd() / ".env")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not anthropic_api_key:
        raise ValueError("Missing ANTHROPIC_API_KEY.")
    if not openai_api_key:
        raise ValueError("Missing OPENAI_API_KEY.")

    targets = load_score_targets(input_parquet)
    per_call_output_dir.mkdir(parents=True, exist_ok=True)
    calibration_output_dir.mkdir(parents=True, exist_ok=True)

    openai_model = OpenAIJudge.discover_gpt5_model(api_key=openai_api_key)
    claude_judge = ClaudeJudge(api_key=anthropic_api_key, model="claude-opus-4-7")
    openai_judge = OpenAIJudge(api_key=openai_api_key, model=openai_model)
    claude_concurrency = max(1, min(provider_concurrency, ANTHROPIC_PROVIDER_CONCURRENCY))

    provider_results = await asyncio.gather(
        _run_provider_pool(
            judge=claude_judge,
            targets=targets,
            output_dir=per_call_output_dir,
            concurrency=claude_concurrency,
        ),
        _run_provider_pool(
            judge=openai_judge,
            targets=targets,
            output_dir=per_call_output_dir,
            concurrency=provider_concurrency,
        ),
    )
    records = [payload for provider_batch in provider_results for payload in provider_batch]
    if len(records) != 96:
        raise ValueError(f"Expected 96 call records, found {len(records)}.")

    for record in records:
        record["artifact_path"] = str(
            _json_path(
                per_call_output_dir,
                record["judge_name"],
                record["response_id"],
                int(record["run_index"]),
            )
        )

    raw_df = _raw_records_to_dataframe(records)
    aggregated_df = _aggregated_dataframe(raw_df)
    raw_path = calibration_output_dir / "judge_scores_raw.parquet"
    aggregated_path = calibration_output_dir / "judge_scores_aggregated.parquet"
    raw_df.to_parquet(raw_path, index=False)
    aggregated_df.to_parquet(aggregated_path, index=False)

    successful_calls = int(raw_df["status"].eq("success").sum())
    failed_rows = raw_df.loc[raw_df["status"] != "success", ["judge_name", "response_id", "run_index"]]
    failures = tuple(
        f"{row.judge_name}:{row.response_id}:run{row.run_index}" for row in failed_rows.itertuples(index=False)
    )
    total_latency = float(raw_df["latency_seconds"].fillna(0).sum())
    estimated_cost = estimate_cost_usd(records)

    return Phase4Summary(
        successful_calls=successful_calls,
        failed_calls=len(failures),
        failures=failures,
        total_latency_seconds=total_latency,
        estimated_cost_usd=estimated_cost,
        openai_model_requested=openai_model,
        claude_model_requested="claude-opus-4-7",
    )


def run_phase4(
    *,
    input_parquet: Path,
    per_call_output_dir: Path,
    calibration_output_dir: Path,
    provider_concurrency: int = 3,
) -> Phase4Summary:
    return asyncio.run(
        run_phase4_async(
            input_parquet=input_parquet,
            per_call_output_dir=per_call_output_dir,
            calibration_output_dir=calibration_output_dir,
            provider_concurrency=provider_concurrency,
        )
    )
