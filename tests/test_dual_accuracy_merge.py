from __future__ import annotations

from pathlib import Path

import pandas as pd

from ejves_judge.comparator import (
    build_accuracy_adjudication_table,
    build_blinded_third_reviewer_packet,
    build_dual_accuracy_review_table,
    build_dual_accuracy_summary,
    build_final_accuracy_review_table,
    build_revised_dual_accuracy_review_table,
    extract_requested_revised_accuracy,
    load_accuracy_review,
)


def _reference_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "response_id": "AAA_SS1_chatgpt_free",
                "source_model": "chatgpt_free",
                "disease": "AAA",
                "domain": "signs_symptoms",
                "question_group": "symptoms",
                "question_text": "Which are the signs of AAA?",
                "response_text": "AAA may be silent or cause abdominal pain.",
            },
            {
                "response_id": "AAA_T1_claude_free",
                "source_model": "claude_free",
                "disease": "AAA",
                "domain": "medical_advice",
                "question_group": "treatment",
                "question_text": "Which is the risk of rupture of an AAA?",
                "response_text": "Risk depends on size and symptoms.",
            },
        ]
    )


def test_load_accuracy_review_detects_header_row_in_xlsx(tmp_path: Path) -> None:
    path = tmp_path / "review.xlsx"
    raw = pd.DataFrame(
        [
            ["Column1", "Column2", "Column3"],
            ["response_id", "mario_accuracy", "mario_accuracy_notes"],
            ["AAA_SS1_chatgpt_free", 4, ""],
            ["AAA_T1_claude_free", 3, "note"],
        ]
    )
    raw.to_excel(path, index=False, header=False)

    review = load_accuracy_review(
        path,
        score_column="mario_accuracy",
        notes_column="mario_accuracy_notes",
        expected_response_ids={"AAA_SS1_chatgpt_free", "AAA_T1_claude_free"},
    )

    assert review["mario_accuracy"].tolist() == [4, 3]
    assert review["response_id"].tolist() == ["AAA_SS1_chatgpt_free", "AAA_T1_claude_free"]


def test_build_dual_accuracy_review_table_flags_adjudication_needed() -> None:
    reference = _reference_frame()
    mario = pd.DataFrame(
        {
            "response_id": ["AAA_SS1_chatgpt_free", "AAA_T1_claude_free"],
            "mario_accuracy": pd.Series([4, 5], dtype="Int64"),
            "mario_accuracy_notes": [pd.NA, pd.NA],
        }
    )
    vga = pd.DataFrame(
        {
            "response_id": ["AAA_SS1_chatgpt_free", "AAA_T1_claude_free"],
            "vga_accuracy": pd.Series([3, 2], dtype="Int64"),
            "vga_accuracy_notes": [pd.NA, pd.NA],
        }
    )

    merged = build_dual_accuracy_review_table(
        reference_frame=reference,
        mario_review=mario,
        vga_review=vga,
    )
    summary, by_model = build_dual_accuracy_summary(merged)

    statuses = merged.set_index("response_id")["human_accuracy_resolution_status"].to_dict()
    assert statuses["AAA_SS1_chatgpt_free"] == "minor_disagreement"
    assert statuses["AAA_T1_claude_free"] == "adjudication_needed"
    assert pd.isna(
        merged.loc[merged["response_id"].eq("AAA_T1_claude_free"), "validated_accuracy"].iloc[0]
    )
    assert int(summary.loc[summary["metric"].eq("adjudication_needed"), "value"].iloc[0]) == 1
    assert set(by_model["source_model"]) == {"chatgpt_free", "claude_free"}


def test_extract_requested_revised_accuracy_detects_explicit_rescore() -> None:
    assert extract_requested_revised_accuracy("I want to rate again as 4") == 4
    assert extract_requested_revised_accuracy("No change from my previous rating.") is None


def test_build_accuracy_adjudication_table_applies_mario_requested_revision() -> None:
    reference = _reference_frame()
    mario = pd.DataFrame(
        {
            "response_id": ["AAA_SS1_chatgpt_free", "AAA_T1_claude_free"],
            "mario_accuracy": pd.Series([4, 5], dtype="Int64"),
            "mario_accuracy_notes": [pd.NA, pd.NA],
        }
    )
    vga = pd.DataFrame(
        {
            "response_id": ["AAA_SS1_chatgpt_free", "AAA_T1_claude_free"],
            "vga_accuracy": pd.Series([3, 3], dtype="Int64"),
            "vga_accuracy_notes": [pd.NA, pd.NA],
        }
    )
    merged = build_dual_accuracy_review_table(
        reference_frame=reference,
        mario_review=mario,
        vga_review=vga,
    )
    mario_rationale = pd.DataFrame(
        {
            "response_id": ["AAA_T1_claude_free"],
            "mario_rationale_score": pd.Series([5], dtype="Int64"),
            "mario_rationale": ["I want to rate again as 4"],
        }
    )
    vga_rationale = pd.DataFrame(
        {
            "response_id": ["AAA_T1_claude_free"],
            "vga_rationale_score": pd.Series([3], dtype="Int64"),
            "vga_rationale": ["Still a 3 because of omissions."],
        }
    )

    adjudication = build_accuracy_adjudication_table(
        dual_accuracy_reviews=merged,
        mario_rationale=mario_rationale,
        vga_rationale=vga_rationale,
    )
    revised = build_revised_dual_accuracy_review_table(merged, adjudication)
    blinded = build_blinded_third_reviewer_packet(adjudication)

    assert adjudication["mario_requested_revised_accuracy"].iloc[0] == 4
    assert bool(adjudication["would_resolve_after_mario_revision"].iloc[0]) is True
    assert revised.loc[revised["response_id"].eq("AAA_T1_claude_free"), "mario_accuracy"].iloc[0] == 4
    assert (
        revised.loc[revised["response_id"].eq("AAA_T1_claude_free"), "human_accuracy_resolution_status"].iloc[0]
        == "minor_disagreement"
    )
    assert "source_model" not in blinded.columns
    assert "response_id" not in blinded.columns


def test_build_final_accuracy_review_table_uses_third_reviewer_median() -> None:
    reference = _reference_frame()
    mario = pd.DataFrame(
        {
            "response_id": ["AAA_SS1_chatgpt_free", "AAA_T1_claude_free"],
            "mario_accuracy": pd.Series([4, 5], dtype="Int64"),
            "mario_accuracy_notes": [pd.NA, pd.NA],
        }
    )
    vga = pd.DataFrame(
        {
            "response_id": ["AAA_SS1_chatgpt_free", "AAA_T1_claude_free"],
            "vga_accuracy": pd.Series([3, 3], dtype="Int64"),
            "vga_accuracy_notes": [pd.NA, pd.NA],
        }
    )
    merged = build_dual_accuracy_review_table(
        reference_frame=reference,
        mario_review=mario,
        vga_review=vga,
    )
    adjudication = build_accuracy_adjudication_table(
        dual_accuracy_reviews=merged,
        mario_rationale=pd.DataFrame(
            {
                "response_id": ["AAA_T1_claude_free"],
                "mario_rationale_score": pd.Series([5], dtype="Int64"),
                "mario_rationale": ["I want to rate again as 4"],
            }
        ),
        vga_rationale=pd.DataFrame(
            {
                "response_id": ["AAA_T1_claude_free"],
                "vga_rationale_score": pd.Series([3], dtype="Int64"),
                "vga_rationale": ["Still 3"],
            }
        ),
    )
    revised = build_revised_dual_accuracy_review_table(merged, adjudication)
    third = pd.DataFrame(
        {
            "response_id": ["AAA_T1_claude_free"],
            "third_reviewer_accuracy": pd.Series([2], dtype="Int64"),
            "third_reviewer_notes": ["Rationale"],
        }
    )

    final = build_final_accuracy_review_table(
        revised_dual_accuracy_reviews=revised,
        adjudication_table=adjudication,
        third_reviewer_review=third,
    )

    row = final.loc[final["response_id"].eq("AAA_T1_claude_free")].iloc[0]
    assert row["final_validated_accuracy"] == 3
    assert row["final_accuracy_source"] == "triple_surgeon_median"
    assert row["final_accuracy_resolution_status"] == "triple_surgeon_resolved"
