from __future__ import annotations

from pathlib import Path

import pandas as pd

from ejves_judge.comparator import (
    build_comparator_prompt,
    build_mario_accuracy_review_sheet,
    comparator_output_model_for_question_group,
    load_comparator_input,
    prepare_phase6_inputs,
)


def _comparator_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "response_id": "AAA_SS1_CLAUDE",
                "disease": "AAA",
                "domain": "signs_symptoms",
                "question_text": "what are symptoms of aaa",
                "response_text": "AAA may cause abdominal pain.",
                "source_model": "claude_free",
            },
            {
                "response_id": "AAA_T1_GPT",
                "disease": "AAA",
                "domain": "medical_advice",
                "question_text": "what should I do for aaa",
                "response_text": "Talk to your doctor about treatment options.",
                "source_model": "chatgpt_free",
            },
        ]
    )


def test_load_comparator_input_assigns_question_group(tmp_path: Path) -> None:
    input_path = tmp_path / "comparator.csv"
    _comparator_frame().to_csv(input_path, index=False)

    loaded = load_comparator_input(input_path)

    assert loaded["source_model"].tolist() == ["chatgpt_free", "claude_free"]
    assert (
        loaded.set_index("response_id")["question_group"].to_dict()
        == {
            "AAA_SS1_CLAUDE": "symptoms",
            "AAA_T1_GPT": "treatment",
        }
    )


def test_build_comparator_prompt_omits_accuracy_and_mentions_human_review() -> None:
    prompt = build_comparator_prompt(
        response_id="AAA_SS1_CLAUDE",
        question_text="what are symptoms of aaa",
        response_text="ChatGPT says AAA may cause abdominal pain.",
        question_group="symptoms",
        domain="signs_symptoms",
    ).prompt

    assert "Accuracy is assessed separately by a human vascular surgeon" in prompt
    assert '"accuracy"' not in prompt
    assert '"comprehensiveness"' in prompt
    assert '"clarity"' in prompt


def test_comparator_output_model_excludes_accuracy_field() -> None:
    symptoms_schema = comparator_output_model_for_question_group("symptoms").model_json_schema()
    treatment_schema = comparator_output_model_for_question_group("treatment").model_json_schema()

    assert "accuracy" not in symptoms_schema["properties"]
    assert "accuracy" not in treatment_schema["properties"]
    assert "discern_q7" not in symptoms_schema["properties"]
    assert "discern_q7" in treatment_schema["properties"]


def test_build_mario_accuracy_review_sheet_has_expected_columns() -> None:
    sheet = build_mario_accuracy_review_sheet(_comparator_frame().assign(question_group=["symptoms", "treatment"]))

    assert sheet.columns.tolist() == [
        "response_id",
        "source_model",
        "disease",
        "domain",
        "question_group",
        "question_text",
        "response_text",
        "mario_accuracy",
        "mario_accuracy_notes",
        "accuracy_reviewer",
        "accuracy_role",
    ]
    assert sheet["accuracy_reviewer"].tolist() == ["Mario", "Mario"]


def test_prepare_phase6_inputs_writes_mario_sheet(tmp_path: Path) -> None:
    input_path = tmp_path / "comparator.csv"
    _comparator_frame().to_csv(input_path, index=False)

    mario_sheet_path = prepare_phase6_inputs(
        input_csv=input_path,
        output_dir=tmp_path / "outputs",
    )
    written = pd.read_csv(mario_sheet_path)

    assert len(written) == 2
    assert set(written["response_id"]) == {"AAA_SS1_CLAUDE", "AAA_T1_GPT"}
    assert "mario_accuracy" in written.columns
