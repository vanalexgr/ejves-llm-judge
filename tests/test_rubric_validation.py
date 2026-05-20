from __future__ import annotations

import pytest
from pydantic import ValidationError

from ejves_judge.rubric import (
    SymptomJudgeOutput,
    TreatmentJudgeOutput,
    output_model_for_question_group,
    rubric_text_for_question_group,
)


def test_question_group_selects_correct_schema_and_rubric() -> None:
    assert output_model_for_question_group("symptoms") is SymptomJudgeOutput
    assert output_model_for_question_group("treatment") is TreatmentJudgeOutput
    assert "DISCERN" not in rubric_text_for_question_group("symptoms")
    assert "DISCERN" in rubric_text_for_question_group("treatment")
    assert "Derived appropriateness" not in rubric_text_for_question_group("symptoms")
    assert "Derived appropriateness" not in rubric_text_for_question_group("treatment")


def test_symptom_schema_forbids_discern() -> None:
    with pytest.raises(ValidationError):
        SymptomJudgeOutput(
            tone=1,
            complementarity=1,
            gilbert_urgency=3,
            discern_q7=4,
            accuracy=4,
            comprehensiveness=4,
            clarity=4,
            rationale="Reason one. Reason two.",
        )


def test_treatment_schema_requires_discern() -> None:
    with pytest.raises(ValidationError):
        TreatmentJudgeOutput(
            tone=1,
            complementarity=1,
            gilbert_urgency=3,
            accuracy=4,
            comprehensiveness=4,
            clarity=4,
            rationale="Reason one. Reason two.",
        )


def test_rationale_must_meet_length_bounds() -> None:
    with pytest.raises(ValidationError):
        SymptomJudgeOutput(
            tone=1,
            complementarity=1,
            gilbert_urgency=3,
            accuracy=4,
            comprehensiveness=4,
            clarity=4,
            rationale="Too short.",
        )

    with pytest.raises(ValidationError):
        TreatmentJudgeOutput(
            tone=1,
            complementarity=1,
            gilbert_urgency=3,
            discern_q7=4,
            accuracy=4,
            comprehensiveness=4,
            clarity=4,
            rationale="x" * 1501,
        )
