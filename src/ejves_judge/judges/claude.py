"""Anthropic judge implementation."""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import random
from typing import Any

from anthropic import Anthropic, APIConnectionError, APIStatusError, APITimeoutError, RateLimitError
from pydantic import BaseModel

from .base import BaseJudge, ScoreModelT


class ClaudeJudge(BaseJudge):
    judge_name = "claude"

    def __init__(self, *, api_key: str, model: str = "claude-opus-4-7") -> None:
        super().__init__(model=model)
        self.client = Anthropic(api_key=api_key)

    def _invoke(
        self,
        *,
        response_id: str,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> tuple[dict[str, Any], str | None, str, dict[str, Any], dict[str, Any]]:
        request_payload = self._build_api_request_payload(prompt=prompt, model_cls=model_cls)
        response = self.client.messages.create(**request_payload)
        tool_block = next(
            (block for block in response.content if getattr(block, "type", None) == "tool_use"),
            None,
        )
        if tool_block is None:
            raise ValueError(f"Anthropic response for {response_id} did not contain tool_use output.")
        parsed_payload = dict(tool_block.input)
        return (
            response.model_dump(mode="json"),
            getattr(response, "_request_id", None),
            self.model,
            self._build_logged_request_payload(prompt=prompt, model_cls=model_cls),
            parsed_payload,
        )

    def _is_retryable_error(self, exc: Exception) -> bool:
        if isinstance(exc, (RateLimitError, APIConnectionError, APITimeoutError)):
            return True
        if isinstance(exc, APIStatusError):
            return exc.status_code == 429 or exc.status_code >= 500
        return False

    def _max_retry_attempts(self) -> int:
        return 6

    def _retry_delay_seconds(
        self,
        *,
        exc: Exception,
        attempt: int,
        base_delay_seconds: float,
    ) -> float:
        del attempt
        retry_after_seconds = self._retry_after_seconds(exc)
        jitter_seconds = random.uniform(0.0, base_delay_seconds * 0.25)
        return max(retry_after_seconds or 0.0, base_delay_seconds + jitter_seconds)

    def _retry_after_seconds(self, exc: Exception) -> float | None:
        response = getattr(exc, "response", None)
        headers = getattr(response, "headers", None)
        if not headers:
            return None

        retry_after = headers.get("retry-after") or headers.get("Retry-After")
        if not retry_after:
            return None

        retry_after = retry_after.strip()
        try:
            return max(float(retry_after), 0.0)
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(retry_after)
            except (TypeError, ValueError, IndexError, OverflowError):
                return None
            if retry_at.tzinfo is None:
                retry_at = retry_at.replace(tzinfo=timezone.utc)
            return max((retry_at - datetime.now(timezone.utc)).total_seconds(), 0.0)

    def _build_api_request_payload(
        self,
        *,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> dict[str, Any]:
        return {
            "model": self.model,
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}],
            "tools": [
                {
                    "name": "submit_score",
                    "description": "Return the scored rubric JSON.",
                    "input_schema": model_cls.model_json_schema(),
                }
            ],
            "tool_choice": {"type": "tool", "name": "submit_score"},
        }

    def _build_logged_request_payload(
        self,
        *,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> dict[str, Any]:
        return {
            "model": self.model,
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}],
            "tools": [
                {
                    "name": "submit_score",
                    "description": "Return the scored rubric JSON.",
                    "input_schema": model_cls.model_json_schema(),
                }
            ],
            "tool_choice": {"type": "tool", "name": "submit_score"},
        }
