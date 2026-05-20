from __future__ import annotations

from pathlib import Path

import pandas as pd

from ejves_judge.data_loader import (
    REVIEWER_WORKBOOKS,
    analyze_text_mismatches,
    build_human_scores_from_frames,
    collect_missing_quality_entries,
    run_phase_one,
    summarize_reconciliation,
    write_text_mismatch_report,
)


def _make_base_frame() -> pd.DataFrame:
    diseases = [
        "VARICOSE VEINS",
        "ABDOMINAL AORTIC ANEURYSM",
        "CAROTID STENOSIS",
        "PAOD",
    ]
    rows = []
    for idx, disease in enumerate(diseases, start=1):
        rows.append(
            {
                "DISEASE": disease,
                "DOMANDA 1 S.S.": f"{disease} symptoms question",
                "RISPOSTA 1 S.S.": f"{disease} symptoms response",
                "TONE ITEM QUEST (0-1-2)": idx % 3,
                "COMPL. ITEM QUEST (0-1)": 1,
                "GILBERT URGENCE (0-4)": 3,
                "ACCURATEZZA": 4,
                "COMPRENSIBILITA'": 4,
                "CHIAREZZA": 4,
                "DOMANDA 2 S.S.": f"{disease} natural history question",
                "RISPOSTA 2 S.S.": f"{disease} natural history response",
                "TONE ITEM QUEST (0-1-2).1": (idx + 1) % 3,
                "COMPL. ITEM QUEST (0-1).1": 1,
                "GILBERT URGENCE (0-4).1": 2,
                "ACCURATEZZA.1": 4,
                "COMPRENSIBILITA'.1": 4,
                "CHIAREZZA.1": 4,
                "DOMANDA 1 T.": f"{disease} medical advice question",
                "RISPOSTA 1 T": f"{disease} medical advice response",
                "TONE ITEM QUEST (0-1-2).2": idx % 3,
                "COMPL. ITEM QUEST (0-1).2": 1,
                "DISCERN (ONLY FOR T.; 1-2-3-4-5)": 4,
                "GILBERT URGENCE (0-4).2": 2,
                "ACCURATEZZA.2": 4,
                "COMPRENSIBILITA'.2": 4,
                "CHIAREZZA.2": 4,
                "DOMANDA 2 T.": f"{disease} best treatment question",
                "RISPOSTA 2 T": f"{disease} best treatment response",
                "TONE ITEM QUEST (0-1-2).3": (idx + 2) % 3,
                "COMPL. ITEM QUEST (0-1).3": 1,
                "DISCERN (ONLY FOR T.; 1-2-3-4-5).1": 5,
                "GILBERT URGENCE (0-4).3": 3,
                "ACCURATEZZA.3": 4,
                "COMPRENSIBILITA'.3": 4,
                "CHIAREZZA.3": 4,
            }
        )
    return pd.DataFrame(rows)


def _make_review_frames() -> dict[str, pd.DataFrame]:
    frames = {
        "MDO": _make_base_frame(),
        "WD": _make_base_frame(),
        "EG": _make_base_frame(),
    }
    frames["EG"].loc[0, "COMPRENSIBILITA'"] = pd.NA
    frames["WD"].loc[1, "ACCURATEZZA.2"] = 2
    frames["WD"].loc[1, "CHIAREZZA.2"] = 2
    return frames


def test_build_human_scores_shapes_and_rules() -> None:
    long_df, consensus_df = build_human_scores_from_frames(_make_review_frames())

    assert len(long_df) == 48
    assert long_df["response_id"].nunique() == 16
    assert long_df.groupby("response_id")["reviewer"].nunique().eq(3).all()
    assert long_df.loc[long_df["question_group"] == "symptoms", "discern_q7"].isna().all()
    assert long_df.loc[long_df["question_group"] == "treatment", "discern_q7"].notna().all()
    assert pd.isna(
        long_df.loc[
            (long_df["reviewer"] == "EG") & (long_df["response_id"] == "VV_SS1"),
            "comprehensiveness",
        ].iloc[0]
    )

    assert len(consensus_df) == 16
    assert "appropriate_strict" in consensus_df.columns
    vv_ss1 = consensus_df.loc[consensus_df["response_id"] == "VV_SS1"].iloc[0]
    assert bool(vv_ss1["appropriate_strict"]) is True
    aaa_t1 = consensus_df.loc[consensus_df["response_id"] == "AAA_T1"].iloc[0]
    assert bool(aaa_t1["appropriate_strict"]) is False

    missing_entries = collect_missing_quality_entries(long_df)
    assert missing_entries[0].response_id == "VV_SS1"
    assert missing_entries[0].reviewer == "EG"
    assert missing_entries[0].domain == "signs_symptoms"
    assert missing_entries[0].missing_fields == ("comprehensiveness",)


def test_build_human_scores_uses_mdo_text_when_versions_differ() -> None:
    frames = _make_review_frames()
    frames["WD"].loc[0, "RISPOSTA 1 S.S."] = "VARICOSE VEINS symptoms response extended"

    long_df, consensus_df = build_human_scores_from_frames(frames)

    assert len(long_df) == 48
    assert len(consensus_df) == 16
    assert (
        long_df.loc[long_df["response_id"] == "VV_SS1", "response_text"].unique().tolist()
        == ["VARICOSE VEINS symptoms response extended"]
    )
    response_text_per_reviewer = long_df.loc[
        long_df["response_id"] == "VV_SS1", "response_text_per_reviewer"
    ].iloc[0]
    assert response_text_per_reviewer["MDO"] == "VARICOSE VEINS symptoms response"
    assert response_text_per_reviewer["WD"] == "VARICOSE VEINS symptoms response extended"


def test_analyze_text_mismatches_reports_prefix_vs_substantive(tmp_path: Path) -> None:
    frames = _make_review_frames()
    frames["WD"].loc[0, "RISPOSTA 1 S.S."] = "VARICOSE VEINS symptoms response extended"
    frames["EG"].loc[0, "RISPOSTA 1 S.S."] = "VARICOSE VEINS symptoms response"
    frames["WD"].loc[1, "RISPOSTA 1 S.S."] = "completely different wording"

    mismatches = analyze_text_mismatches(
        frames,
        reviewer_sources={"MDO": "mdo.xlsx", "WD": "wd.xlsx", "EG": "eg.xlsx"},
    )

    mismatch_map = {mismatch.response_id: mismatch for mismatch in mismatches}
    assert mismatch_map["VV_SS1"].clean_prefix_truncation is True
    assert mismatch_map["AAA_SS1"].clean_prefix_truncation is False
    reconciliation_summary = summarize_reconciliation(mismatches)
    assert reconciliation_summary.resolved_response_truncations == ("VV_SS1",)
    assert reconciliation_summary.unresolved_response_mismatches == ("AAA_SS1",)

    report_path = write_text_mismatch_report(
        mismatches,
        raw_dir=tmp_path / "raw",
        processed_dir=tmp_path / "processed",
        reconciliation_summary=reconciliation_summary,
    )
    report_text = report_path.read_text(encoding="utf-8")
    assert "## VV_SS1" in report_text
    assert "Status after reconciliation: resolved" in report_text
    assert "## AAA_SS1" in report_text
    assert "Status after reconciliation: unresolved" in report_text


def test_run_phase_one_from_xlsx(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir()

    frames = _make_review_frames()
    for workbook in REVIEWER_WORKBOOKS:
        frames[workbook.reviewer].to_excel(
            raw_dir / workbook.filename,
            sheet_name=workbook.sheet_name,
            index=False,
        )

    long_df, consensus_df, outputs, reconciliation_summary = run_phase_one(
        raw_dir=raw_dir,
        processed_dir=processed_dir,
    )

    assert len(long_df) == 48
    assert len(consensus_df) == 16
    assert reconciliation_summary.unresolved_response_mismatches == ()
    assert reconciliation_summary.missing_scores_log_line() == (
        "Missing reviewer quality scores treated as non-failing if observed values are >=3: "
        "VV_SS1, EG, signs_symptoms (comprehensiveness)."
    )
    for path in outputs.values():
        assert path.exists()


def test_run_phase_one_reconciles_prefix_truncations(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir()

    frames = _make_review_frames()
    frames["WD"].loc[0, "RISPOSTA 1 S.S."] = "VARICOSE VEINS symptoms response extended"
    for workbook in REVIEWER_WORKBOOKS:
        frames[workbook.reviewer].to_excel(
            raw_dir / workbook.filename,
            sheet_name=workbook.sheet_name,
            index=False,
        )

    long_df, consensus_df, outputs, reconciliation_summary = run_phase_one(
        raw_dir=raw_dir,
        processed_dir=processed_dir,
    )

    assert len(long_df) == 48
    assert len(consensus_df) == 16
    assert reconciliation_summary.resolved_response_truncations == ("VV_SS1",)
    report_text = outputs["text_mismatches_report"].read_text(encoding="utf-8")
    assert "No remaining mismatches after applying reconciliation rules." in report_text
