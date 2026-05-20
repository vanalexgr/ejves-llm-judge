"""Prompt construction and response blinding for Phase 2."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re

from .rubric import rubric_text_for_question_group


BLINDING_REGEX = r"\b(ChatGPT|GPT[-]?\d|Claude|Gemini|Bard|OpenAI|Anthropic|Google)\b"
_BLINDING_PATTERN = re.compile(BLINDING_REGEX)

SYSTEM_PROMPT = """SYSTEM: You are a board-certified vascular surgeon evaluating an AI chatbot's
response to a patient-style question. Score the response strictly against the
rubric below. Do not infer beyond what the response actually states. If the
response does not address something, the relevant score reflects that absence,
not what you think the response should have said. Output only valid JSON
matching the schema. No commentary outside the JSON."""

CANONICAL_ACRONYMS = (
    "AAA",
    "CS",
    "PAOD",
    "VV",
    "EVAR",
    "CEA",
    "CAS",
    "TIA",
    "DVT",
    "ARB",
    "ACE",
    "PCSK9",
)


@dataclass(frozen=True)
class BlindedText:
    text: str
    substitution_count: int


@dataclass(frozen=True)
class PromptBuildResult:
    prompt: str
    response_id: str
    question_group: str
    blinding_substitution_count: int
    prompt_character_length: int


def blind_model_identifiers(response_text: str) -> BlindedText:
    """Replace model self-identifiers with a neutral placeholder."""

    blinded_text, substitution_count = _BLINDING_PATTERN.subn("[the assistant]", response_text)
    return BlindedText(text=blinded_text, substitution_count=substitution_count)


def output_format_template(question_group: str) -> str:
    """Return the JSON template shown inside the prompt."""

    payload: dict[str, object] = {
        "tone": 0,
        "complementarity": 0,
        "gilbert_urgency": 0,
    }
    if question_group == "treatment":
        payload["discern_q7"] = 1
    payload.update(
        {
            "accuracy": 1,
            "comprehensiveness": 1,
            "clarity": 1,
            "rationale": "Concise justification goes here.",
        }
    )
    return json.dumps(payload, indent=2)


def normalize_question_text(question_text: str) -> str:
    """Convert question text to sentence case while preserving canonical acronyms."""

    normalized = re.sub(r"\s+", " ", question_text).strip()
    lowered = normalized.lower()

    for acronym in CANONICAL_ACRONYMS:
        lowered = re.sub(rf"\b{re.escape(acronym.lower())}\b", acronym, lowered, flags=re.IGNORECASE)

    lowered = re.sub(r"\bi\b", "I", lowered)

    first_alpha_index = next((index for index, char in enumerate(lowered) if char.isalpha()), None)
    if first_alpha_index is not None:
        lowered = (
            lowered[:first_alpha_index]
            + lowered[first_alpha_index].upper()
            + lowered[first_alpha_index + 1 :]
        )

    if lowered and lowered[-1] not in ".!?":
        lowered += "?"
    return lowered


def build_prompt(
    *,
    response_id: str,
    question_text: str,
    response_text: str,
    question_group: str,
    domain: str,
) -> PromptBuildResult:
    """Construct the Phase 2 prompt for one reconciled response."""

    blinded = blind_model_identifiers(response_text)
    rubric_text = rubric_text_for_question_group(question_group)
    output_format = output_format_template(question_group)
    normalized_question_text = normalize_question_text(question_text)
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "USER:\n"
        f"QUESTION: {normalized_question_text}\n\n"
        "RESPONSE TO SCORE:\n"
        "---\n"
        f"{blinded.text}\n"
        "---\n\n"
        f"QUESTION CATEGORY: {question_group}  ({domain})\n\n"
        "RUBRIC:\n"
        f"{rubric_text}\n\n"
        "Replace each numeric placeholder with your integer score (within the stated range). "
        "Replace rationale with a concise justification (roughly 2–4 sentences).\n\n"
        "OUTPUT FORMAT (JSON):\n"
        f"{output_format}\n"
    )
    return PromptBuildResult(
        prompt=prompt,
        response_id=response_id,
        question_group=question_group,
        blinding_substitution_count=blinded.substitution_count,
        prompt_character_length=len(prompt),
    )
