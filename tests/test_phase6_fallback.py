from __future__ import annotations

from ejves_judge.phase6_fallback import (
    Phase6FallbackContext,
    build_methods_addendum,
    build_phase6_comparator_methodology,
)


def _context() -> Phase6FallbackContext:
    return Phase6FallbackContext(
        comparator_response_count=48,
        third_rater_case_count=5,
        claude_model="claude-opus-4-7",
        openai_model="gpt-5",
        ensemble_accuracy_kappa=0.1282051282,
        claude_accuracy_kappa=-0.2222222222,
        openai_accuracy_kappa=0.2549019608,
        ensemble_accuracy_icc_2_1=0.1368935690,
        interhuman_accuracy_mean_pairwise=0.4386104693,
        interhuman_comprehensiveness_icc_2_1=-0.060606,
        interhuman_clarity_icc_2_1=-0.066566,
        urgency_kappa=0.7094972067,
        tone_kappa=0.2,
        discern_kappa=0.3076923077,
        complementarity_kappa=0.2941176471,
        comprehensiveness_kappa=0.0588235294,
        clarity_kappa=-0.0526315789,
        comprehensiveness_icc_2_1=0.129359,
        clarity_icc_2_1=-0.025245,
        accuracy_verdict="FAIL",
        comprehensiveness_verdict="REVIEW",
        clarity_verdict="REVIEW",
        pass_items=("tone", "gilbert_urgency", "discern_q7", "complementarity"),
    )


def test_phase6_comparator_methodology_includes_scope_and_metrics() -> None:
    text = build_phase6_comparator_methodology(_context())
    assert "48 comparator responses" in text
    assert "0.128" in text
    assert "-0.222" in text
    assert "tone`, `complementarity`, `gilbert_urgency`, and `discern_q7`" in text
    assert "Do not perform another rubric-anchoring pass for accuracy" in text


def test_methods_addendum_is_manuscript_facing() -> None:
    text = build_methods_addendum(_context())
    assert "claude-opus-4-7" in text
    assert "gpt-5" in text
    assert "weighted kappa for accuracy was 0.128" in text
    assert "rated independently and blinded by two board-certified surgeons" in text
    assert "blinded third-surgeon adjudication for the 5 rows" in text
    assert "No further rubric iteration was performed for accuracy" in text
