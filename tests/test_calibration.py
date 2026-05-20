from __future__ import annotations

import math

import pandas as pd

from ejves_judge.calibration import (
    aggregate_human_consensus,
    discretize_value,
    icc_absolute_agreement,
    stable_mode,
    subset_interhuman_reliability,
)


def test_stable_mode_breaks_ties_toward_lower_value() -> None:
    series = pd.Series([1, 0, 1, 0], dtype="Int64")
    assert stable_mode(series) == 0.0


def test_discretize_value_rounds_half_up_and_thresholds_binary() -> None:
    assert discretize_value(3.5, "accuracy") == 4
    assert discretize_value(2.49, "accuracy") == 2
    assert discretize_value(0.5, "complementarity") == 1
    assert discretize_value(0.49, "complementarity") == 0


def test_icc_absolute_agreement_is_one_for_identical_columns() -> None:
    score_table = pd.DataFrame(
        {
            "rater_a": [1.0, 2.0, 3.0, 4.0],
            "rater_b": [1.0, 2.0, 3.0, 4.0],
        },
        index=pd.Index(["A", "B", "C", "D"], name="target"),
    )
    assert math.isclose(icc_absolute_agreement(score_table), 1.0, rel_tol=1e-9)
    assert math.isclose(
        icc_absolute_agreement(score_table, average_measures=True),
        1.0,
        rel_tol=1e-9,
    )


def test_icc_absolute_agreement_handles_small_complete_matrix() -> None:
    score_table = pd.DataFrame(
        {
            "rater_a": [3.0, 4.0],
            "rater_b": [3.0, 4.0],
        },
        index=pd.Index(["A", "B"], name="target"),
    )
    assert math.isclose(icc_absolute_agreement(score_table), 1.0, rel_tol=1e-9)
    assert math.isclose(
        icc_absolute_agreement(score_table, average_measures=True),
        1.0,
        rel_tol=1e-9,
    )


def test_aggregate_human_consensus_uses_mean_median_and_mode() -> None:
    frame = pd.DataFrame(
        [
            {
                "response_id": "AAA_SS1",
                "disease": "AAA",
                "domain": "signs_symptoms",
                "question_group": "symptoms",
                "question_text": "Q",
                "response_text": "R",
                "reviewer": "MDO",
                "tone": 0,
                "gilbert_urgency": 3,
                "discern_q7": pd.NA,
                "complementarity": 1,
                "accuracy": 3,
                "comprehensiveness": 4,
                "clarity": 5,
            },
            {
                "response_id": "AAA_SS1",
                "disease": "AAA",
                "domain": "signs_symptoms",
                "question_group": "symptoms",
                "question_text": "Q",
                "response_text": "R",
                "reviewer": "WD",
                "tone": 1,
                "gilbert_urgency": 2,
                "discern_q7": pd.NA,
                "complementarity": 1,
                "accuracy": 4,
                "comprehensiveness": 5,
                "clarity": 4,
            },
            {
                "response_id": "AAA_SS1",
                "disease": "AAA",
                "domain": "signs_symptoms",
                "question_group": "symptoms",
                "question_text": "Q",
                "response_text": "R",
                "reviewer": "EG",
                "tone": 2,
                "gilbert_urgency": 1,
                "discern_q7": pd.NA,
                "complementarity": 0,
                "accuracy": 5,
                "comprehensiveness": 3,
                "clarity": 3,
            },
        ]
    )

    consensus = aggregate_human_consensus(frame).iloc[0]
    assert consensus["tone"] == 1.0
    assert consensus["gilbert_urgency"] == 2.0
    assert consensus["complementarity"] == 1.0
    assert math.isclose(consensus["accuracy"], 4.0)
    assert math.isclose(consensus["comprehensiveness"], 4.0)
    assert math.isclose(consensus["clarity"], 4.0)


def test_subset_interhuman_reliability_filters_question_group() -> None:
    rows = []
    for question_group, response_ids in {
        "symptoms": ["AAA_SS1", "AAA_SS2", "CS_SS1"],
        "treatment": ["AAA_T1", "AAA_T2", "CS_T1"],
    }.items():
        for score, response_id in enumerate(response_ids, start=3):
            for reviewer in {"MDO": 4, "WD": 4, "EG": 4}:
                rows.append(
                    {
                        "response_id": response_id,
                        "disease": "AAA",
                        "domain": "signs_symptoms" if question_group == "symptoms" else "medical_advice",
                        "question_group": question_group,
                        "question_text": "Q",
                        "response_text": "R",
                        "reviewer": reviewer,
                        "tone": 1,
                        "gilbert_urgency": 2,
                        "discern_q7": 3 if question_group == "treatment" else pd.NA,
                        "complementarity": 1,
                        "accuracy": score,
                        "comprehensiveness": score,
                        "clarity": score,
                    }
                )

    frame = pd.DataFrame(rows)
    symptoms = subset_interhuman_reliability(frame, question_group="symptoms")
    treatment = subset_interhuman_reliability(frame, question_group="treatment")

    assert set(symptoms["pairwise"]["question_group"]) == {"symptoms"}
    assert set(treatment["pairwise"]["question_group"]) == {"treatment"}
    assert set(symptoms["icc"]["icc_type"]) == {"ICC(A,k)"}
    assert set(treatment["icc"]["icc_type"]) == {"ICC(A,k)"}
    assert all(
        math.isclose(value, 1.0, rel_tol=1e-9)
        for value in symptoms["icc"]["icc_2_k"].tolist()
    )
