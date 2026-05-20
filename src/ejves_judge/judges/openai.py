"""OpenAI judge implementation."""

from __future__ import annotations

from typing import Any

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError
from pydantic import BaseModel

from .base import BaseJudge, ScoreModelT


class OpenAIJudge(BaseJudge):
    judge_name = "openai"

    def __init__(self, *, api_key: str, model: str) -> None:
        super().__init__(model=model)
        self.client = OpenAI(api_key=api_key)

    @classmethod
    def discover_gpt5_model(cls, *, api_key: str) -> str:
        client = OpenAI(api_key=api_key)
        model_ids = sorted(model.id for model in client.models.list())
        if "gpt-5" in model_ids:
            return "gpt-5"

        preferred = [
            model_id
            for model_id in model_ids
            if model_id.startswith("gpt-5") and "mini" not in model_id and "nano" not in model_id
        ]
        if preferred:
            return preferred[0]

        fallback = [model_id for model_id in model_ids if "gpt-5" in model_id]
        if fallback:
            return fallback[0]

        raise ValueError(f"No GPT-5 family model found. Available models inspected: {model_ids[:50]}")

    def _invoke(
        self,
        *,
        response_id: str,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> tuple[dict[str, Any], str | None, str, dict[str, Any], dict[str, Any]]:
        request_payload = self._build_api_request_payload(prompt=prompt, model_cls=model_cls)
        response = self.client.responses.parse(**request_payload)
        parsed = response.output_parsed
        if parsed is None:
            raise ValueError(f"OpenAI response for {response_id} did not contain parsed output.")
        return (
            response.model_dump(mode="json"),
            getattr(response, "_request_id", None),
            self.model,
            self._build_logged_request_payload(prompt=prompt, model_cls=model_cls),
            parsed.model_dump(mode="json"),
        )

    def _is_retryable_error(self, exc: Exception) -> bool:
        if isinstance(exc, (RateLimitError, APIConnectionError, APITimeoutError)):
            return True
        if isinstance(exc, APIStatusError):
            return exc.status_code == 429 or exc.status_code >= 500
        return False

    def _build_api_request_payload(
        self,
        *,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> dict[str, Any]:
        return {
            "model": self.model,
            "input": prompt,
            "text_format": model_cls,
        }

    def _build_logged_request_payload(
        self,
        *,
        prompt: str,
        model_cls: type[ScoreModelT],
    ) -> dict[str, Any]:
        return {
            "model": self.model,
            "input": prompt,
            "text_format": model_cls.__name__,
        }
