from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from anthropic import APIStatusError, RateLimitError
import httpx

from ejves_judge.judges.claude import ClaudeJudge


class _FakeToolBlock:
    type = "tool_use"

    def __init__(self, payload: dict[str, int | str]) -> None:
        self.input = payload


class _FakeAnthropicResponse:
    def __init__(self, payload: dict[str, int | str]) -> None:
        self.content = [_FakeToolBlock(payload)]
        self._request_id = "req_success"

    def model_dump(self, mode: str = "json") -> dict[str, object]:
        del mode
        return {
            "id": "msg_123",
            "usage": {
                "input_tokens": 123,
                "output_tokens": 45,
            },
        }


def _build_retryable_error(status_code: int) -> APIStatusError:
    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    response = httpx.Response(
        status_code,
        headers={"Retry-After": "2"},
        request=request,
    )
    body = {
        "type": "error",
        "error": {"type": "overloaded_error", "message": "Overloaded"},
    }
    if status_code == 429:
        return RateLimitError("rate limited", response=response, body=body)
    return APIStatusError("overloaded", response=response, body=body)


def test_claude_retries_on_429_and_529_with_retry_after() -> None:
    valid_payload = {
        "tone": 1,
        "complementarity": 1,
        "gilbert_urgency": 2,
        "accuracy": 4,
        "comprehensiveness": 4,
        "clarity": 4,
        "rationale": "This is a concise justification string for the scored response.",
    }
    create_side_effects = [
        _build_retryable_error(429),
        _build_retryable_error(529),
        _FakeAnthropicResponse(valid_payload),
    ]
    judge = ClaudeJudge(api_key="test-key", model="claude-opus-4-7")
    judge.client = SimpleNamespace(
        messages=SimpleNamespace(
            create=lambda **_: create_side_effects.pop(0)
            if not isinstance(create_side_effects[0], Exception)
            else (_ for _ in ()).throw(create_side_effects.pop(0))
        )
    )

    sleep_calls: list[float] = []
    with patch("ejves_judge.judges.claude.random.uniform", return_value=0.0):
        judge._sleep_before_retry = sleep_calls.append
        result = judge.score(
            response_id="AAA_SS1",
            prompt="prompt",
            question_group="symptoms",
        )

    assert result.request_id == "req_success"
    assert result.parsed_response.accuracy == 4
    assert sleep_calls == [2.0, 2.0]

