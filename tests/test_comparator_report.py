from __future__ import annotations

import pandas as pd

from ejves_judge.comparator_report import (
    ORIGINAL_BENCHMARK_LABEL,
    build_endpoint_comparison_table,
    build_model_endpoint_summary,
    build_original_benchmark_summary,
)


def test_build_original_benchmark_summary_uses_consensus_mean_columns() -> None:
    consensus = pd.DataFrame(
        [
            {
                "response_id": "AAA_SS1",
                "question_group": "symptoms",
                "tone_mean": 1.0,
                "complementarity_mean": 1.0,
                "gilbert_urgency_mean": 2.0,
                "discern_q7_mean": pd.NA,
                "accuracy_mean": 3.0,
                "comprehensiveness_mean": 4.0,
                "clarity_mean": 4.0,
            },
            {
                "response_id": "AAA_T1",
                "question_group": "treatment",
                "tone_mean": 2.0,
                "complementarity_mean": 0.5,
                "gilbert_urgency_mean": 3.0,
                "discern_q7_mean": 4.0,
                "accuracy_mean": 5.0,
                "comprehensiveness_mean": 3.0,
                "clarity_mean": 5.0,
            },
        ]
    )

    summary = build_original_benchmark_summary(consensus).set_index("endpoint")

    assert summary.loc["Accuracy", "original_mean"] == 4.0
    assert summary.loc["DISCERN Q7", "original_mean"] == 4.0
    assert summary.loc["DISCERN Q7", "response_count"] == 1


def test_build_endpoint_comparison_table_flips_urgency_delta_direction() -> None:
    comparator = pd.DataFrame(
        [
            {
                "source_model": "chatgpt_free",
                "response_id": "AAA_SS1_chatgpt_free",
                "question_group": "symptoms",
                "validated_accuracy": 4.0,
                "validated_tone": 2.0,
                "validated_complementarity": 1.0,
                "validated_gilbert_urgency": 1.0,
                "validated_discern_q7": pd.NA,
                "descriptive_comprehensiveness": 4.0,
                "descriptive_clarity": 5.0,
            },
            {
                "source_model": "chatgpt_free",
                "response_id": "AAA_T1_chatgpt_free",
                "question_group": "treatment",
                "validated_accuracy": 4.0,
                "validated_tone": 2.0,
                "validated_complementarity": 1.0,
                "validated_gilbert_urgency": 1.0,
                "validated_discern_q7": 3.0,
                "descriptive_comprehensiveness": 4.0,
                "descriptive_clarity": 5.0,
            },
        ]
    )
    consensus = pd.DataFrame(
        [
            {
                "response_id": "AAA_SS1",
                "question_group": "symptoms",
                "tone_mean": 1.0,
                "complementarity_mean": 1.0,
                "gilbert_urgency_mean": 2.0,
                "discern_q7_mean": pd.NA,
                "accuracy_mean": 3.0,
                "comprehensiveness_mean": 4.0,
                "clarity_mean": 4.0,
            },
            {
                "response_id": "AAA_T1",
                "question_group": "treatment",
                "tone_mean": 1.0,
                "complementarity_mean": 1.0,
                "gilbert_urgency_mean": 2.0,
                "discern_q7_mean": 2.0,
                "accuracy_mean": 3.0,
                "comprehensiveness_mean": 4.0,
                "clarity_mean": 4.0,
            },
        ]
    )

    benchmark = build_original_benchmark_summary(consensus)
    model_summary = build_model_endpoint_summary(comparator)
    validated = build_endpoint_comparison_table(
        model_summary=model_summary,
        original_benchmark=benchmark,
        group="validated",
    ).set_index("Endpoint")

    assert validated.loc["Accuracy", ORIGINAL_BENCHMARK_LABEL] == 3.0
    assert validated.loc["Accuracy", "GPT-5.5 vs original"] == 1.0
    assert validated.loc["Urgency", "GPT-5.5 vs original"] == 1.0
