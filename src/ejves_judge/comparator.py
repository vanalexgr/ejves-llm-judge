"""Restricted Phase 6 comparator scoring pipeline."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import json
import os
from pathlib import Path
import time
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

from .judges.base import JudgeResult
from .judges.claude import ClaudeJudge
from .judges.openai import OpenAIJudge
from .prompt_builder import blind_model_identifiers, normalize_question_text
from .rubric import RUBRIC_COMPLEMENTARITY, RUBRIC_DISCERN, RUBRIC_TONE, RUBRIC_URGENCY
from .scoring import (
    ANTHROPIC_PROVIDER_CONCURRENCY,
    _aggregated_dataframe,
    _json_path,
    _raw_records_to_dataframe,
    _run_provider_pool,
    estimate_cost_usd,
)


VALID_SOURCE_MODELS = ("claude_free", "chatgpt_free", "gemini_free")
DOMAIN_TO_QUESTION_GROUP = {
    "signs_symptoms": "symptoms",
    "natural_history": "symptoms",
    "medical_advice": "treatment",
    "best_treatment": "treatment",
}
REQUIRED_INPUT_COLUMNS = (
    "response_id",
    "disease",
    "domain",
    "question_text",
    "response_text",
    "source_model",
)
VALIDATED_JUDGE_ITEMS = ("tone", "complementarity", "gilbert_urgency", "discern_q7")
DESCRIPTIVE_JUDGE_ITEMS = ("comprehensiveness", "clarity")

COMPARATOR_SYSTEM_PROMPT = """SYSTEM: You are a board-certified vascular surgeon evaluating an AI chatbot's
response to a patient-style question for the comparator arm of a vascular
surgery study. Accuracy is assessed separately by a human vascular surgeon and
is not part of this scoring task. Score only the domains requested in the
rubric below. Do not infer beyond what the response actually states. Output only
valid JSON matching the schema. No commentary outside the JSON."""

COMPARATOR_RUBRIC_QUALITY = """### E. Descriptive quality domains — 1 to 5 each

- **Comprehensiveness** — coverage of clinically important aspects of the question. 1 = very poor (major omissions); 5 = excellent (complete coverage)
- **Clarity** — readability and structural clarity of the response for a layperson. 1 = very poor (confusing or jargon-heavy); 5 = excellent (clear and accessible)

These two domains are recorded descriptively only in Phase 6 and are not validated primary comparator endpoints.
"""


@dataclass(frozen=True)
class ComparatorPromptBuildResult:
    prompt: str
    response_id: str
    question_group: str
    blinding_substitution_count: int
    prompt_character_length: int


@dataclass(frozen=True)
class ComparatorTarget:
    response_id: str
    source_model: str
    disease: str
    domain: str
    question_group: str
    question_text: str
    response_text: str
    prompt: str
    blinding_substitution_count: int


@dataclass(frozen=True)
class Phase6Summary:
    response_count: int
    successful_calls: int
    failed_calls: int
    failures: tuple[str, ...]
    total_latency_seconds: float
    estimated_cost_usd: float
    openai_model_requested: str
    claude_model_requested: str
    mario_review_sheet_path: Path


class ComparatorSymptomJudgeOutput(BaseModel):
    """Structured output for comparator symptom and natural-history items."""

    model_config = ConfigDict(extra="forbid")

    tone: int = Field(ge=0, le=2)
    complementarity: int = Field(ge=0, le=1)
    gilbert_urgency: int = Field(ge=0, le=4)
    comprehensiveness: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    rationale: str = Field(
        min_length=20,
        max_length=1500,
        description="Concise justification for the scores.",
    )


class ComparatorTreatmentJudgeOutput(BaseModel):
    """Structured output for comparator treatment items."""

    model_config = ConfigDict(extra="forbid")

    tone: int = Field(ge=0, le=2)
    complementarity: int = Field(ge=0, le=1)
    gilbert_urgency: int = Field(ge=0, le=4)
    discern_q7: int = Field(ge=1, le=5)
    comprehensiveness: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    rationale: str = Field(
        min_length=20,
        max_length=1500,
        description="Concise justification for the scores.",
    )


def comparator_output_model_for_question_group(question_group: str) -> type[BaseModel]:
    if question_group == "symptoms":
        return ComparatorSymptomJudgeOutput
    if question_group == "treatment":
        return ComparatorTreatmentJudgeOutput
    raise ValueError(f"Unsupported question_group: {question_group!r}")


def comparator_rubric_text_for_question_group(question_group: str) -> str:
    blocks = [RUBRIC_TONE, RUBRIC_COMPLEMENTARITY, RUBRIC_URGENCY]
    if question_group == "treatment":
        blocks.append(RUBRIC_DISCERN)
    elif question_group != "symptoms":
        raise ValueError(f"Unsupported question_group: {question_group!r}")
    blocks.append(COMPARATOR_RUBRIC_QUALITY)
    return "\n\n".join(blocks)


def comparator_output_format_template(question_group: str) -> str:
    payload: dict[str, object] = {
        "tone": 0,
        "complementarity": 0,
        "gilbert_urgency": 0,
    }
    if question_group == "treatment":
        payload["discern_q7"] = 1
    payload.update(
        {
            "comprehensiveness": 1,
            "clarity": 1,
            "rationale": "Concise justification goes here.",
        }
    )
    return json.dumps(payload, indent=2)


def build_comparator_prompt(
    *,
    response_id: str,
    question_text: str,
    response_text: str,
    question_group: str,
    domain: str,
) -> ComparatorPromptBuildResult:
    blinded = blind_model_identifiers(response_text)
    rubric_text = comparator_rubric_text_for_question_group(question_group)
    output_format = comparator_output_format_template(question_group)
    normalized_question_text = normalize_question_text(question_text)
    prompt = (
        f"{COMPARATOR_SYSTEM_PROMPT}\n\n"
        "USER:\n"
        f"QUESTION: {normalized_question_text}\n\n"
        "RESPONSE TO SCORE:\n"
        "---\n"
        f"{blinded.text}\n"
        "---\n\n"
        f"QUESTION CATEGORY: {question_group}  ({domain})\n\n"
        "RUBRIC:\n"
        f"{rubric_text}\n\n"
        "Accuracy is intentionally omitted from this task because it is assigned separately by a "
        "human vascular surgeon.\n"
        "Replace each numeric placeholder with your integer score (within the stated range). "
        "Replace rationale with a concise justification (roughly 2–4 sentences).\n\n"
        "OUTPUT FORMAT (JSON):\n"
        f"{output_format}\n"
    )
    return ComparatorPromptBuildResult(
        prompt=prompt,
        response_id=response_id,
        question_group=question_group,
        blinding_substitution_count=blinded.substitution_count,
        prompt_character_length=len(prompt),
    )


def load_comparator_input(input_csv: Path) -> pd.DataFrame:
    frame = pd.read_csv(input_csv)
    missing_columns = [column for column in REQUIRED_INPUT_COLUMNS if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Missing required comparator columns: {missing_columns}")

    data = frame.copy()
    for column in REQUIRED_INPUT_COLUMNS:
        data[column] = data[column].astype(str).str.strip()
        if data[column].eq("").any():
            raise ValueError(f"Comparator column {column!r} contains blank values.")

    if data["response_id"].duplicated().any():
        duplicates = data.loc[data["response_id"].duplicated(keep=False), "response_id"].tolist()
        raise ValueError(f"Comparator response_id values must be unique. Duplicates: {duplicates}")

    data["source_model"] = data["source_model"].str.lower()
    invalid_source_models = sorted(set(data["source_model"]) - set(VALID_SOURCE_MODELS))
    if invalid_source_models:
        raise ValueError(
            f"Unsupported source_model values: {invalid_source_models}. "
            f"Expected one of {VALID_SOURCE_MODELS}."
        )

    data["domain"] = data["domain"].str.lower()
    invalid_domains = sorted(set(data["domain"]) - set(DOMAIN_TO_QUESTION_GROUP))
    if invalid_domains:
        raise ValueError(
            f"Unsupported domain values: {invalid_domains}. "
            f"Expected one of {sorted(DOMAIN_TO_QUESTION_GROUP)}."
        )

    data["question_group"] = data["domain"].map(DOMAIN_TO_QUESTION_GROUP)
    data = data.sort_values(["source_model", "response_id"], kind="stable").reset_index(drop=True)
    return data


def build_comparator_targets(input_frame: pd.DataFrame) -> list[ComparatorTarget]:
    targets: list[ComparatorTarget] = []
    for row in input_frame.itertuples(index=False):
        prompt_result = build_comparator_prompt(
            response_id=row.response_id,
            question_text=row.question_text,
            response_text=row.response_text,
            question_group=row.question_group,
            domain=row.domain,
        )
        targets.append(
            ComparatorTarget(
                response_id=row.response_id,
                source_model=row.source_model,
                disease=row.disease,
                domain=row.domain,
                question_group=row.question_group,
                question_text=row.question_text,
                response_text=row.response_text,
                prompt=prompt_result.prompt,
                blinding_substitution_count=prompt_result.blinding_substitution_count,
            )
        )
    return targets


def comparator_target_frame(targets: list[ComparatorTarget]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "response_id": target.response_id,
                "source_model": target.source_model,
                "disease": target.disease,
                "domain": target.domain,
                "question_group": target.question_group,
                "question_text": target.question_text,
                "response_text": target.response_text,
                "blinding_substitution_count": target.blinding_substitution_count,
            }
            for target in targets
        ]
    ).sort_values(["source_model", "response_id"], kind="stable").reset_index(drop=True)


class _ComparatorJudgeMixin:
    def score(self, *, response_id: str, prompt: str, question_group: str) -> JudgeResult:
        model_cls = comparator_output_model_for_question_group(question_group)
        started = time.perf_counter()
        raw_response, request_id, model_used, request_payload, parsed = self._call_with_retries(
            response_id=response_id,
            prompt=prompt,
            model_cls=model_cls,
        )
        latency = time.perf_counter() - started
        validated = model_cls.model_validate(parsed)
        return JudgeResult(
            judge_name=self.judge_name,
            response_id=response_id,
            question_group=question_group,
            model_used=model_used,
            latency_seconds=latency,
            request_id=request_id,
            request_payload=request_payload,
            raw_response=raw_response,
            parsed_response=validated,
        )

    def build_logged_request_payload(self, *, prompt: str, question_group: str) -> dict[str, Any]:
        model_cls = comparator_output_model_for_question_group(question_group)
        return self._build_logged_request_payload(prompt=prompt, model_cls=model_cls)


class ComparatorClaudeJudge(_ComparatorJudgeMixin, ClaudeJudge):
    """Claude wrapper using the restricted Phase 6 schema."""


class ComparatorOpenAIJudge(_ComparatorJudgeMixin, OpenAIJudge):
    """OpenAI wrapper using the restricted Phase 6 schema."""


def build_mario_accuracy_review_sheet(input_frame: pd.DataFrame) -> pd.DataFrame:
    review = input_frame[
        [
            "response_id",
            "source_model",
            "disease",
            "domain",
            "question_group",
            "question_text",
            "response_text",
        ]
    ].copy()
    review["mario_accuracy"] = pd.Series([pd.NA] * len(review), dtype="Int64")
    review["mario_accuracy_notes"] = pd.NA
    review["accuracy_reviewer"] = "Mario"
    review["accuracy_role"] = "validated_endpoint"
    return review


def load_mario_accuracy_review(review_csv: Path, *, expected_response_ids: set[str]) -> pd.DataFrame:
    review = pd.read_csv(review_csv)
    required_columns = {"response_id", "mario_accuracy"}
    missing = required_columns - set(review.columns)
    if missing:
        raise ValueError(f"Missing required Mario review columns: {sorted(missing)}")

    review = review.copy()
    review["response_id"] = review["response_id"].astype(str).str.strip()
    missing_ids = sorted(expected_response_ids - set(review["response_id"]))
    extra_ids = sorted(set(review["response_id"]) - expected_response_ids)
    if missing_ids or extra_ids:
        raise ValueError(
            f"Mario review response_id mismatch. Missing={missing_ids}, extra={extra_ids}"
        )

    review["mario_accuracy"] = pd.to_numeric(review["mario_accuracy"], errors="coerce").astype("Int64")
    invalid_scores = review.loc[
        review["mario_accuracy"].notna() & ~review["mario_accuracy"].between(1, 5),
        "mario_accuracy",
    ]
    if not invalid_scores.empty:
        raise ValueError(
            f"Mario accuracy scores must be integers 1-5. Invalid values: {invalid_scores.tolist()}"
        )
    return review


def build_phase6_ensemble_scores(
    judge_aggregated: pd.DataFrame,
    target_meta: pd.DataFrame,
) -> pd.DataFrame:
    meta = target_meta.set_index("response_id")
    score_items = ("tone", "complementarity", "gilbert_urgency", "discern_q7", "comprehensiveness", "clarity")
    rows: list[dict[str, Any]] = []
    for response_id, group in judge_aggregated.groupby("response_id", sort=True):
        row: dict[str, Any] = {
            "response_id": response_id,
            "source_model": meta.loc[response_id, "source_model"],
            "disease": meta.loc[response_id, "disease"],
            "domain": meta.loc[response_id, "domain"],
            "question_group": meta.loc[response_id, "question_group"],
            "question_text": meta.loc[response_id, "question_text"],
            "response_text": meta.loc[response_id, "response_text"],
        }
        for item in score_items:
            values = group[f"{item}_aggregated"].dropna().astype(float)
            row[item] = float(values.mean()) if not values.empty else pd.NA
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["source_model", "response_id"], kind="stable").reset_index(drop=True)


def build_phase6_results(
    *,
    ensemble_scores: pd.DataFrame,
    mario_review: pd.DataFrame | None,
) -> pd.DataFrame:
    results = ensemble_scores.copy()
    results["accuracy_source"] = "mario_review_pending"
    results["mario_accuracy"] = pd.Series([pd.NA] * len(results), dtype="Int64")
    results["mario_accuracy_notes"] = pd.NA
    if mario_review is not None:
        keep_columns = ["response_id", "mario_accuracy"]
        if "mario_accuracy_notes" in mario_review.columns:
            keep_columns.append("mario_accuracy_notes")
        results = results.drop(columns=["mario_accuracy", "mario_accuracy_notes"]).merge(
            mario_review[keep_columns],
            on="response_id",
            how="left",
        )
        results["accuracy_source"] = "Mario"

    results["validated_tone"] = results["tone"]
    results["validated_complementarity"] = results["complementarity"]
    results["validated_gilbert_urgency"] = results["gilbert_urgency"]
    results["validated_discern_q7"] = results["discern_q7"]
    results["descriptive_comprehensiveness"] = results["comprehensiveness"]
    results["descriptive_clarity"] = results["clarity"]
    return results


def write_source_model_slices(
    *,
    raw_df: pd.DataFrame,
    judge_aggregated: pd.DataFrame,
    ensemble_scores: pd.DataFrame,
    phase6_results: pd.DataFrame,
    output_dir: Path,
) -> None:
    by_model_dir = output_dir / "by_source_model"
    by_model_dir.mkdir(parents=True, exist_ok=True)
    for source_model in sorted(ensemble_scores["source_model"].dropna().unique()):
        model_dir = by_model_dir / source_model
        model_dir.mkdir(parents=True, exist_ok=True)
        response_ids = set(ensemble_scores.loc[ensemble_scores["source_model"].eq(source_model), "response_id"])
        raw_df.loc[raw_df["response_id"].isin(response_ids)].to_parquet(
            model_dir / "judge_scores_raw.parquet",
            index=False,
        )
        judge_aggregated.loc[judge_aggregated["response_id"].isin(response_ids)].to_parquet(
            model_dir / "judge_scores_aggregated.parquet",
            index=False,
        )
        ensemble_scores.loc[ensemble_scores["source_model"].eq(source_model)].to_parquet(
            model_dir / "ensemble_scores.parquet",
            index=False,
        )
        phase6_results.loc[phase6_results["source_model"].eq(source_model)].to_parquet(
            model_dir / "comparator_results.parquet",
            index=False,
        )


async def run_phase6_async(
    *,
    input_csv: Path,
    per_call_output_dir: Path,
    output_dir: Path,
    provider_concurrency: int = 3,
    mario_review_output_path: Path | None = None,
    mario_review_input_path: Path | None = None,
) -> Phase6Summary:
    load_dotenv(Path.cwd() / ".env")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not anthropic_api_key:
        raise ValueError("Missing ANTHROPIC_API_KEY.")
    if not openai_api_key:
        raise ValueError("Missing OPENAI_API_KEY.")

    input_frame = load_comparator_input(input_csv)
    targets = build_comparator_targets(input_frame)
    target_meta = comparator_target_frame(targets)

    per_call_output_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    openai_model = ComparatorOpenAIJudge.discover_gpt5_model(api_key=openai_api_key)
    claude_judge = ComparatorClaudeJudge(api_key=anthropic_api_key, model="claude-opus-4-7")
    openai_judge = ComparatorOpenAIJudge(api_key=openai_api_key, model=openai_model)
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
    expected_calls = len(targets) * 2 * 3
    if len(records) != expected_calls:
        raise ValueError(f"Expected {expected_calls} call records, found {len(records)}.")

    for record in records:
        record["artifact_path"] = str(
            _json_path(
                per_call_output_dir,
                record["judge_name"],
                record["response_id"],
                int(record["run_index"]),
            )
        )

    raw_df = _raw_records_to_dataframe(records).merge(
        target_meta,
        on=["response_id", "question_group"],
        how="left",
    )
    judge_aggregated = _aggregated_dataframe(raw_df).merge(
        target_meta,
        on=["response_id", "question_group"],
        how="left",
    )
    ensemble_scores = build_phase6_ensemble_scores(judge_aggregated, target_meta)

    mario_review_sheet = build_mario_accuracy_review_sheet(input_frame)
    mario_review_path = mario_review_output_path or (output_dir / "mario_accuracy_review.csv")
    mario_review_sheet.to_csv(mario_review_path, index=False)

    mario_review_complete = None
    if mario_review_input_path is not None:
        mario_review_complete = load_mario_accuracy_review(
            mario_review_input_path,
            expected_response_ids=set(input_frame["response_id"]),
        )
    phase6_results = build_phase6_results(
        ensemble_scores=ensemble_scores,
        mario_review=mario_review_complete,
    )

    raw_path = output_dir / "judge_scores_raw.parquet"
    aggregated_path = output_dir / "judge_scores_aggregated.parquet"
    ensemble_path = output_dir / "ensemble_scores.parquet"
    pending_results_path = output_dir / "comparator_results.parquet"
    raw_df.to_parquet(raw_path, index=False)
    judge_aggregated.to_parquet(aggregated_path, index=False)
    ensemble_scores.to_parquet(ensemble_path, index=False)
    phase6_results.to_parquet(pending_results_path, index=False)
    write_source_model_slices(
        raw_df=raw_df,
        judge_aggregated=judge_aggregated,
        ensemble_scores=ensemble_scores,
        phase6_results=phase6_results,
        output_dir=output_dir,
    )

    successful_calls = int(raw_df["status"].eq("success").sum())
    failed_rows = raw_df.loc[raw_df["status"] != "success", ["judge_name", "response_id", "run_index"]]
    failures = tuple(
        f"{row.judge_name}:{row.response_id}:run{row.run_index}"
        for row in failed_rows.itertuples(index=False)
    )
    total_latency = float(raw_df["latency_seconds"].fillna(0).sum())
    estimated_cost = estimate_cost_usd(records)

    return Phase6Summary(
        response_count=len(targets),
        successful_calls=successful_calls,
        failed_calls=len(failures),
        failures=failures,
        total_latency_seconds=total_latency,
        estimated_cost_usd=estimated_cost,
        openai_model_requested=openai_model,
        claude_model_requested="claude-opus-4-7",
        mario_review_sheet_path=mario_review_path,
    )


def prepare_phase6_inputs(
    *,
    input_csv: Path,
    output_dir: Path,
    mario_review_output_path: Path | None = None,
) -> Path:
    input_frame = load_comparator_input(input_csv)
    output_dir.mkdir(parents=True, exist_ok=True)
    mario_review_sheet = build_mario_accuracy_review_sheet(input_frame)
    mario_review_path = mario_review_output_path or (output_dir / "mario_accuracy_review.csv")
    mario_review_sheet.to_csv(mario_review_path, index=False)
    return mario_review_path


def run_phase6(
    *,
    input_csv: Path,
    per_call_output_dir: Path,
    output_dir: Path,
    provider_concurrency: int = 3,
    mario_review_output_path: Path | None = None,
    mario_review_input_path: Path | None = None,
) -> Phase6Summary:
    return asyncio.run(
        run_phase6_async(
            input_csv=input_csv,
            per_call_output_dir=per_call_output_dir,
            output_dir=output_dir,
            provider_concurrency=provider_concurrency,
            mario_review_output_path=mario_review_output_path,
            mario_review_input_path=mario_review_input_path,
        )
    )
