"""Shared judge interfaces and retry logic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from pathlib import Path
import time
from typing import Any, TypeVar

from pydantic import BaseModel

from ejves_judge.rubric import output_model_for_question_group


ScoredResponse = BaseModel
ScoreModelT = TypeVar("ScoreModelT", bound=BaseModel)


@dataclass(frozen=True)
class JudgeResult:
    judge_name: str
    response_id: str
    question_group: str
    model_used: str
    latency_seconds: float
    request_id: str | None
    request_payload: dict[str, Any]
    raw_response: dict[str, Any]
    parsed_response: BaseModel

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "judge_name": self.judge_name,
            "response_id": self.response_id,
            "question_group": self.question_group,
            "model_used": self.model_used,
            "latency_seconds": self.latency_seconds,
            "request_id": self.request_id,
            "request_payload": self.request_payload,
            "raw_response": self.raw_response,
            "parsed_response": self.parsed_response.model_dump(mode="json"),
        }

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_json_dict(), indent=2), encoding="utf-8")


class BaseJudge(ABC):
    """Abstract judge client."""

    judge_name: str

    def __init__(self, *, model: str) -> None:
        self.model = model

    def score(self, *, response_id: str, prompt: str, question_group: str) -> JudgeResult:
        model_cls = output_model_for_question_group(question_group)
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
        model_cls = output_model_for_question_group(question_group)
        return self._build_logged_request_payload(prompt=prompt, model_cls=model_cls)

    def _call_with_retries(
        self,
        *,
        response_id: str,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> tuple[dict[str, Any], str | None, str, dict[str, Any], dict[str, Any]]:
        delay_seconds = 1.0
        last_error: Exception | None = None
        max_attempts = self._max_retry_attempts()
        for attempt in range(1, max_attempts + 1):
            try:
                return self._invoke(
                    response_id=response_id,
                    prompt=prompt,
                    model_cls=model_cls,
                )
            except Exception as exc:  # pragma: no cover - exercised in live calls
                last_error = exc
                if not self._is_retryable_error(exc) or attempt == max_attempts:
                    raise
                self._sleep_before_retry(
                    self._retry_delay_seconds(
                        exc=exc,
                        attempt=attempt,
                        base_delay_seconds=delay_seconds,
                    )
                )
                delay_seconds *= 2
        raise RuntimeError(f"Exhausted retries for {response_id}") from last_error

    def _max_retry_attempts(self) -> int:
        return 3

    def _retry_delay_seconds(
        self,
        *,
        exc: Exception,
        attempt: int,
        base_delay_seconds: float,
    ) -> float:
        del exc, attempt
        return base_delay_seconds

    def _sleep_before_retry(self, delay_seconds: float) -> None:
        time.sleep(delay_seconds)

    @abstractmethod
    def _invoke(
        self,
        *,
        response_id: str,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> tuple[dict[str, Any], str | None, str, dict[str, Any], dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def _is_retryable_error(self, exc: Exception) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _build_logged_request_payload(
        self,
        *,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> dict[str, Any]:
        raise NotImplementedError
