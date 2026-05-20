from __future__ import annotations

from ejves_judge.prompt_builder import (
    BLINDING_REGEX,
    blind_model_identifiers,
    build_prompt,
    normalize_question_text,
)


def test_blinding_regex_replaces_expected_identifiers() -> None:
    blinded = blind_model_identifiers("ChatGPT and Gemini are mentioned. GPT-4 appears too.")
    assert blinded.substitution_count == 3
    assert "[the assistant]" in blinded.text


def test_symptom_prompt_omits_discern() -> None:
    result = build_prompt(
        response_id="AAA_SS1",
        question_text="WHAT ARE THE SYMPTOMS OF AN AAA",
        response_text="ChatGPT says you should seek care.",
        question_group="symptoms",
        domain="signs_symptoms",
    )
    assert "DISCERN" not in result.prompt
    assert '"discern_q7"' not in result.prompt
    assert "Derived appropriateness" not in result.prompt
    assert '"tone": 0' in result.prompt
    assert '"accuracy": 1' in result.prompt
    assert "Replace each numeric placeholder with your integer score" in result.prompt
    assert "Replace rationale with a concise justification (roughly 2–4 sentences)." in result.prompt
    assert '"rationale": "Concise justification goes here."' in result.prompt
    assert "QUESTION: What are the symptoms of an AAA?" in result.prompt
    assert result.blinding_substitution_count == 1
    assert result.prompt_character_length == len(result.prompt)


def test_treatment_prompt_includes_discern() -> None:
    result = build_prompt(
        response_id="AAA_T1",
        question_text="WHAT TREATMENT SHOULD I GET FOR AAA",
        response_text="This is a treatment answer.",
        question_group="treatment",
        domain="medical_advice",
    )
    assert "DISCERN" in result.prompt
    assert '"discern_q7"' in result.prompt
    assert BLINDING_REGEX in BLINDING_REGEX
    assert "Derived appropriateness" not in result.prompt
    assert '"discern_q7": 1' in result.prompt
    assert "QUESTION: What treatment should I get for AAA?" in result.prompt


def test_normalize_question_text_preserves_acronyms() -> None:
    assert normalize_question_text("WHAT IS THE RISK OF RUPTURE OF AN AAA") == (
        "What is the risk of rupture of an AAA?"
    )
    assert normalize_question_text("best treatment for paod after EVAR") == (
        "Best treatment for PAOD after EVAR?"
    )
