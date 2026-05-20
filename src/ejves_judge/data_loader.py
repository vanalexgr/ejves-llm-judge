"""Phase 1 data loading and harmonization."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import html
import math
import re

import pandas as pd


@dataclass(frozen=True)
class ReviewerWorkbook:
    reviewer: str
    filename: str
    sheet_name: str
    filename_aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class BlockSpec:
    code: str
    domain: str
    question_group: str
    question_col: str
    response_col: str
    tone_col: str
    complementarity_col: str
    discern_col: str | None
    urgency_col: str
    accuracy_col: str
    comprehensiveness_col: str
    clarity_col: str


@dataclass(frozen=True)
class TextVersion:
    response_id: str
    reviewer: str
    source_name: str
    question_text: str
    normalized_question_text: str
    response_text: str
    normalized_response_text: str


@dataclass(frozen=True)
class TextMismatch:
    response_id: str
    question_text_mismatch: bool
    response_text_mismatch: bool
    longest_reviewers: tuple[str, ...]
    clean_prefix_truncation: bool | None
    versions: tuple[TextVersion, ...]


@dataclass(frozen=True)
class CanonicalText:
    question_text: str
    response_text: str
    response_text_per_reviewer: dict[str, str]


@dataclass(frozen=True)
class MissingScoreAuditEntry:
    response_id: str
    reviewer: str
    domain: str
    missing_fields: tuple[str, ...]


@dataclass(frozen=True)
class ReconciliationSummary:
    resolved_response_truncations: tuple[str, ...]
    wd_question_variations: tuple[str, ...]
    unresolved_response_mismatches: tuple[str, ...]
    missing_quality_entries: tuple[MissingScoreAuditEntry, ...] = ()

    def log_line(self) -> str:
        response_count = len(self.resolved_response_truncations)
        response_label = (
            "response-text truncation" if response_count == 1 else "response-text truncations"
        )
        if response_count:
            response_part = (
                f"Reconciled {response_count} {response_label}: "
                f"{', '.join(self.resolved_response_truncations)}."
            )
        else:
            response_part = f"Reconciled 0 {response_label}."

        question_count = len(self.wd_question_variations)
        question_label = (
            "question-phrasing variation" if question_count == 1 else "question-phrasing variations"
        )
        if question_count:
            question_part = (
                f" Used WD's question text for {question_count} {question_label}: "
                f"{', '.join(self.wd_question_variations)}."
            )
        else:
            question_part = " Used WD's question text for 0 question-phrasing variations."

        return response_part + question_part

    def missing_scores_log_line(self) -> str:
        if not self.missing_quality_entries:
            return (
                "Missing reviewer quality scores treated as non-failing if observed values are >=3: none."
            )

        details = "; ".join(
            f"{entry.response_id}, {entry.reviewer}, {entry.domain} ({', '.join(entry.missing_fields)})"
            for entry in self.missing_quality_entries
        )
        return (
            "Missing reviewer quality scores treated as non-failing if observed values are >=3: "
            f"{details}."
        )


REVIEWER_WORKBOOKS: tuple[ReviewerWorkbook, ...] = (
    ReviewerWorkbook(
        "MDO",
        "db__1__Mario_12_08.xlsx",
        "revisore MDO",
        filename_aliases=("db (1)_Mario 12.08.xlsx",),
    ),
    ReviewerWorkbook(
        "WD",
        "db_wd.xlsx",
        "revisore WD",
        filename_aliases=("db wd.xlsx",),
    ),
    ReviewerWorkbook(
        "EG",
        "db_ai_rev_eg.xlsx",
        "revisore EG",
        filename_aliases=("db ai_rev eg.xlsx",),
    ),
)

BLOCK_SPECS: tuple[BlockSpec, ...] = (
    BlockSpec(
        code="SS1",
        domain="signs_symptoms",
        question_group="symptoms",
        question_col="DOMANDA 1 S.S.",
        response_col="RISPOSTA 1 S.S.",
        tone_col="TONE ITEM QUEST (0-1-2)",
        complementarity_col="COMPL. ITEM QUEST (0-1)",
        discern_col=None,
        urgency_col="GILBERT URGENCE (0-4)",
        accuracy_col="ACCURATEZZA",
        comprehensiveness_col="COMPRENSIBILITA'",
        clarity_col="CHIAREZZA",
    ),
    BlockSpec(
        code="SS2",
        domain="natural_history",
        question_group="symptoms",
        question_col="DOMANDA 2 S.S.",
        response_col="RISPOSTA 2 S.S.",
        tone_col="TONE ITEM QUEST (0-1-2).1",
        complementarity_col="COMPL. ITEM QUEST (0-1).1",
        discern_col=None,
        urgency_col="GILBERT URGENCE (0-4).1",
        accuracy_col="ACCURATEZZA.1",
        comprehensiveness_col="COMPRENSIBILITA'.1",
        clarity_col="CHIAREZZA.1",
    ),
    BlockSpec(
        code="T1",
        domain="medical_advice",
        question_group="treatment",
        question_col="DOMANDA 1 T.",
        response_col="RISPOSTA 1 T",
        tone_col="TONE ITEM QUEST (0-1-2).2",
        complementarity_col="COMPL. ITEM QUEST (0-1).2",
        discern_col="DISCERN (ONLY FOR T.; 1-2-3-4-5)",
        urgency_col="GILBERT URGENCE (0-4).2",
        accuracy_col="ACCURATEZZA.2",
        comprehensiveness_col="COMPRENSIBILITA'.2",
        clarity_col="CHIAREZZA.2",
    ),
    BlockSpec(
        code="T2",
        domain="best_treatment",
        question_group="treatment",
        question_col="DOMANDA 2 T.",
        response_col="RISPOSTA 2 T",
        tone_col="TONE ITEM QUEST (0-1-2).3",
        complementarity_col="COMPL. ITEM QUEST (0-1).3",
        discern_col="DISCERN (ONLY FOR T.; 1-2-3-4-5).1",
        urgency_col="GILBERT URGENCE (0-4).3",
        accuracy_col="ACCURATEZZA.3",
        comprehensiveness_col="COMPRENSIBILITA'.3",
        clarity_col="CHIAREZZA.3",
    ),
)

DISEASE_ORDER: tuple[str, ...] = ("VV", "AAA", "CS", "PAOD")
DISEASE_ALIASES: dict[str, set[str]] = {
    "VV": {"VV", "VARICOSE VEINS"},
    "AAA": {"AAA", "ABDOMINAL AORTIC ANEURYSM"},
    "CS": {"CS", "CAROTID STENOSIS"},
    "PAOD": {"PAOD", "PERIPHERAL ARTERIAL OCCLUSIVE DISEASE"},
}

LONG_INDEX_COLUMNS: list[str] = [
    "response_id",
    "disease",
    "domain",
    "question_group",
    "question_text",
    "response_text",
]
SCORE_COLUMNS: list[str] = [
    "tone",
    "complementarity",
    "gilbert_urgency",
    "discern_q7",
    "accuracy",
    "comprehensiveness",
    "clarity",
]
QUALITY_COLUMNS: list[str] = ["accuracy", "comprehensiveness", "clarity"]


def _normalize_whitespace(value: object) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _string_or_raise(value: object, *, field_name: str, response_id: str, reviewer: str) -> str:
    normalized = _normalize_whitespace(value)
    if not normalized:
        raise ValueError(
            f"Missing {field_name} for reviewer={reviewer}, response_id={response_id}."
        )
    return str(value).strip()


def _coerce_optional_int(
    value: object,
    *,
    field_name: str,
    response_id: str,
    reviewer: str,
    required: bool,
) -> int | pd.NA:
    if pd.isna(value) or _normalize_whitespace(value) == "":
        if required:
            raise ValueError(
                f"Missing {field_name} for reviewer={reviewer}, response_id={response_id}."
            )
        return pd.NA

    try:
        numeric = pd.to_numeric(pd.Series([value]), errors="raise").iloc[0]
    except Exception as exc:  # pragma: no cover - defensive branch
        raise ValueError(
            f"Invalid numeric value for {field_name} in reviewer={reviewer}, "
            f"response_id={response_id}: {value!r}"
        ) from exc

    if pd.isna(numeric):
        if required:
            raise ValueError(
                f"Missing {field_name} for reviewer={reviewer}, response_id={response_id}."
            )
        return pd.NA

    return int(numeric)


def _mode_or_na(values: pd.Series) -> int | pd.NA:
    observed = values.dropna()
    if observed.empty:
        return pd.NA
    modes = observed.mode(dropna=True)
    return int(sorted(int(value) for value in modes)[0])


def _strip_column_names(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned.columns = [
        column.strip() if isinstance(column, str) else column for column in cleaned.columns
    ]
    return cleaned.dropna(axis=0, how="all").dropna(axis=1, how="all")


def _required_columns() -> set[str]:
    columns: set[str] = set()
    for block in BLOCK_SPECS:
        columns.update(
            {
                block.question_col,
                block.response_col,
                block.tone_col,
                block.complementarity_col,
                block.urgency_col,
                block.accuracy_col,
                block.comprehensiveness_col,
                block.clarity_col,
            }
        )
        if block.discern_col:
            columns.add(block.discern_col)
    return columns


def _validate_columns(frame: pd.DataFrame, *, reviewer: str) -> None:
    missing = sorted(column for column in _required_columns() if column not in frame.columns)
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"Reviewer {reviewer} is missing required columns: {missing_str}")


def _non_empty_rows(frame: pd.DataFrame) -> pd.DataFrame:
    content_columns = [block.question_col for block in BLOCK_SPECS] + [
        block.response_col for block in BLOCK_SPECS
    ]
    mask = frame[content_columns].notna().any(axis=1)
    trimmed = frame.loc[mask].reset_index(drop=True)
    if len(trimmed) != 4:
        raise ValueError(
            f"Expected exactly 4 disease rows after trimming, found {len(trimmed)} rows."
        )
    return trimmed


def _detect_diseases(frame: pd.DataFrame) -> list[str]:
    detected: list[str] = []
    for _, row in frame.iterrows():
        row_tokens = {
            _normalize_whitespace(value).upper()
            for value in row.tolist()
            if _normalize_whitespace(value)
        }
        disease_code = None
        for candidate, aliases in DISEASE_ALIASES.items():
            if row_tokens.intersection(aliases):
                disease_code = candidate
                break
        detected.append(disease_code or "")

    if len(set(detected)) == 4 and all(detected):
        return detected
    return list(DISEASE_ORDER)


def _read_reviewer_sheet(workbook: ReviewerWorkbook, raw_dir: Path) -> pd.DataFrame:
    path = _resolve_workbook_path(workbook, raw_dir)
    frame = pd.read_excel(path, sheet_name=workbook.sheet_name, engine="openpyxl")
    frame = _strip_column_names(frame)
    _validate_columns(frame, reviewer=workbook.reviewer)
    return _non_empty_rows(frame)


def _resolve_workbook_path(workbook: ReviewerWorkbook, raw_dir: Path) -> Path:
    path = None
    candidate_names = (workbook.filename, *workbook.filename_aliases)
    for candidate_name in candidate_names:
        candidate_path = raw_dir / candidate_name
        if candidate_path.exists():
            path = candidate_path
            break

    if path is None:
        candidates = ", ".join(str(raw_dir / name) for name in candidate_names)
        raise FileNotFoundError(f"Missing raw input file. Tried: {candidates}")

    return path


def _prepare_review_frames(
    review_frames: dict[str, pd.DataFrame],
) -> tuple[dict[str, pd.DataFrame], list[str]]:
    missing_reviewers = {workbook.reviewer for workbook in REVIEWER_WORKBOOKS} - set(review_frames)
    if missing_reviewers:
        missing = ", ".join(sorted(missing_reviewers))
        raise ValueError(f"Missing reviewer frames: {missing}")

    prepared: dict[str, pd.DataFrame] = {}
    canonical_diseases: list[str] | None = None

    for workbook in REVIEWER_WORKBOOKS:
        frame = _strip_column_names(review_frames[workbook.reviewer])
        _validate_columns(frame, reviewer=workbook.reviewer)
        frame = _non_empty_rows(frame)
        detected_diseases = _detect_diseases(frame)
        if canonical_diseases is None:
            canonical_diseases = detected_diseases
        elif detected_diseases != canonical_diseases:
            raise ValueError(
                f"Disease row order mismatch for reviewer {workbook.reviewer}: "
                f"{detected_diseases} != {canonical_diseases}"
            )
        prepared[workbook.reviewer] = frame

    return prepared, canonical_diseases or list(DISEASE_ORDER)


def _collect_text_versions(
    review_frames: dict[str, pd.DataFrame],
    *,
    reviewer_sources: dict[str, str] | None = None,
) -> dict[str, list[TextVersion]]:
    prepared_frames, diseases = _prepare_review_frames(review_frames)
    versions_by_response_id: dict[str, list[TextVersion]] = {}

    for workbook in REVIEWER_WORKBOOKS:
        frame = prepared_frames[workbook.reviewer]
        source_name = (
            reviewer_sources.get(workbook.reviewer, workbook.filename)
            if reviewer_sources
            else workbook.filename
        )

        for row_index, disease in enumerate(diseases):
            row = frame.iloc[row_index]
            for block in BLOCK_SPECS:
                response_id = f"{disease}_{block.code}"
                question_text = _string_or_raise(
                    row[block.question_col],
                    field_name="question_text",
                    response_id=response_id,
                    reviewer=workbook.reviewer,
                )
                response_text = _string_or_raise(
                    row[block.response_col],
                    field_name="response_text",
                    response_id=response_id,
                    reviewer=workbook.reviewer,
                )
                versions_by_response_id.setdefault(response_id, []).append(
                    TextVersion(
                        response_id=response_id,
                        reviewer=workbook.reviewer,
                        source_name=source_name,
                        question_text=question_text,
                        normalized_question_text=_normalize_whitespace(question_text),
                        response_text=response_text,
                        normalized_response_text=_normalize_whitespace(response_text),
                    )
                )

    return versions_by_response_id


def _canonical_texts_from_reconciliation(
    versions_by_response_id: dict[str, list[TextVersion]],
) -> dict[str, CanonicalText]:
    canonical_texts: dict[str, CanonicalText] = {}
    reviewer_rank = {workbook.reviewer: index for index, workbook in enumerate(REVIEWER_WORKBOOKS)}

    for response_id, versions in versions_by_response_id.items():
        ordered_versions = sorted(
            versions,
            key=lambda version: reviewer_rank.get(version.reviewer, len(reviewer_rank)),
        )
        wd_version = next(
            (version for version in ordered_versions if version.reviewer == "WD"),
            ordered_versions[0],
        )
        longest_response_length = max(
            len(version.normalized_response_text) for version in ordered_versions
        )
        longest_response_version = next(
            version
            for version in ordered_versions
            if len(version.normalized_response_text) == longest_response_length
        )
        canonical_texts[response_id] = CanonicalText(
            question_text=wd_version.question_text,
            response_text=longest_response_version.response_text,
            response_text_per_reviewer={
                version.reviewer: version.response_text for version in ordered_versions
            },
        )

    return canonical_texts


def _extract_records(
    frame: pd.DataFrame,
    *,
    reviewer: str,
    diseases: list[str],
    canonical_texts: dict[str, CanonicalText],
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []

    for row_index, disease in enumerate(diseases):
        row = frame.iloc[row_index]
        for block in BLOCK_SPECS:
            response_id = f"{disease}_{block.code}"
            canonical_text = canonical_texts[response_id]
            question_text = canonical_text.question_text
            response_text = canonical_text.response_text

            discern_required = block.question_group == "treatment"
            discern_value = (
                _coerce_optional_int(
                    row[block.discern_col],
                    field_name="discern_q7",
                    response_id=response_id,
                    reviewer=reviewer,
                    required=discern_required,
                )
                if block.discern_col
                else pd.NA
            )

            record = {
                "response_id": response_id,
                "disease": disease,
                "domain": block.domain,
                "question_group": block.question_group,
                "question_text": question_text,
                "response_text": response_text,
                "response_text_per_reviewer": dict(canonical_text.response_text_per_reviewer),
                "reviewer": reviewer,
                "tone": _coerce_optional_int(
                    row[block.tone_col],
                    field_name="tone",
                    response_id=response_id,
                    reviewer=reviewer,
                    required=True,
                ),
                "complementarity": _coerce_optional_int(
                    row[block.complementarity_col],
                    field_name="complementarity",
                    response_id=response_id,
                    reviewer=reviewer,
                    required=True,
                ),
                "gilbert_urgency": _coerce_optional_int(
                    row[block.urgency_col],
                    field_name="gilbert_urgency",
                    response_id=response_id,
                    reviewer=reviewer,
                    required=True,
                ),
                "discern_q7": discern_value,
                "accuracy": _coerce_optional_int(
                    row[block.accuracy_col],
                    field_name="accuracy",
                    response_id=response_id,
                    reviewer=reviewer,
                    required=True,
                ),
                "comprehensiveness": _coerce_optional_int(
                    row[block.comprehensiveness_col],
                    field_name="comprehensiveness",
                    response_id=response_id,
                    reviewer=reviewer,
                    required=False,
                ),
                "clarity": _coerce_optional_int(
                    row[block.clarity_col],
                    field_name="clarity",
                    response_id=response_id,
                    reviewer=reviewer,
                    required=True,
                ),
            }
            records.append(record)

    return records


def build_human_scores_from_frames(
    review_frames: dict[str, pd.DataFrame],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    prepared_frames, canonical_diseases = _prepare_review_frames(review_frames)
    text_versions = _collect_text_versions(prepared_frames)
    canonical_texts = _canonical_texts_from_reconciliation(text_versions)
    long_records: list[dict[str, object]] = []

    for workbook in REVIEWER_WORKBOOKS:
        long_records.extend(
            _extract_records(
                prepared_frames[workbook.reviewer],
                reviewer=workbook.reviewer,
                diseases=canonical_diseases,
                canonical_texts=canonical_texts,
            )
        )

    long_df = pd.DataFrame(long_records).sort_values(
        ["response_id", "reviewer"], kind="stable"
    ).reset_index(drop=True)

    for column in SCORE_COLUMNS:
        long_df[column] = long_df[column].astype("Int64")

    _validate_phase_one_outputs(long_df)
    consensus_df = _build_consensus(long_df)
    return long_df, consensus_df


def _validate_phase_one_outputs(long_df: pd.DataFrame) -> None:
    response_count = long_df["response_id"].nunique()
    if response_count != 16:
        raise ValueError(f"Expected 16 unique response_id values, found {response_count}.")

    reviewer_counts = long_df.groupby("response_id")["reviewer"].nunique()
    if not reviewer_counts.eq(3).all():
        bad = reviewer_counts[~reviewer_counts.eq(3)].to_dict()
        raise ValueError(f"Expected exactly 3 reviewers per response. Found: {bad}")

    symptom_discern = long_df.loc[
        long_df["question_group"] == "symptoms", "discern_q7"
    ]
    treatment_discern = long_df.loc[
        long_df["question_group"] == "treatment", "discern_q7"
    ]
    if not symptom_discern.isna().all():
        raise ValueError("DISCERN values must be absent for symptom-group rows.")
    if treatment_discern.isna().any():
        raise ValueError("DISCERN values must be present for all treatment-group rows.")


def _build_consensus(long_df: pd.DataFrame) -> pd.DataFrame:
    grouped = long_df.groupby(LONG_INDEX_COLUMNS, dropna=False, sort=True)[SCORE_COLUMNS]
    consensus = grouped.apply(_aggregate_consensus).reset_index()

    quality_mask = (
        long_df[QUALITY_COLUMNS].ge(3) | long_df[QUALITY_COLUMNS].isna()
    ).all(axis=1)
    appropriate = (
        long_df.assign(_appropriate=quality_mask)
        .groupby(LONG_INDEX_COLUMNS, dropna=False, sort=True)["_appropriate"]
        .all()
        .rename("appropriate_strict")
        .reset_index()
    )

    merged = consensus.merge(appropriate, on=LONG_INDEX_COLUMNS, how="left")
    return merged.sort_values("response_id", kind="stable").reset_index(drop=True)


def _aggregate_consensus(group: pd.DataFrame) -> pd.Series:
    metrics: dict[str, object] = {}
    for column in SCORE_COLUMNS:
        series = group[column]
        metrics[f"{column}_mean"] = series.astype("Float64").mean()
        metrics[f"{column}_mode"] = _mode_or_na(series)
    return pd.Series(metrics)


def collect_missing_quality_entries(long_df: pd.DataFrame) -> tuple[MissingScoreAuditEntry, ...]:
    missing_entries: list[MissingScoreAuditEntry] = []
    for _, row in long_df.iterrows():
        missing_fields = tuple(
            column for column in QUALITY_COLUMNS if pd.isna(row[column])
        )
        if not missing_fields:
            continue
        missing_entries.append(
            MissingScoreAuditEntry(
                response_id=str(row["response_id"]),
                reviewer=str(row["reviewer"]),
                domain=str(row["domain"]),
                missing_fields=missing_fields,
            )
        )

    return tuple(
        sorted(
            missing_entries,
            key=lambda entry: (entry.response_id, entry.reviewer, entry.domain),
        )
    )


def load_review_frames(
    raw_dir: Path | str,
) -> tuple[dict[str, pd.DataFrame], dict[str, str]]:
    raw_path = Path(raw_dir)
    frames: dict[str, pd.DataFrame] = {}
    reviewer_sources: dict[str, str] = {}

    for workbook in REVIEWER_WORKBOOKS:
        resolved_path = _resolve_workbook_path(workbook, raw_path)
        reviewer_sources[workbook.reviewer] = resolved_path.name
        frames[workbook.reviewer] = _read_reviewer_sheet(workbook, raw_path)

    return frames, reviewer_sources


def _analyze_text_mismatch(
    response_id: str,
    versions: list[TextVersion],
) -> TextMismatch | None:
    unique_questions = {version.normalized_question_text for version in versions}
    unique_responses = {version.normalized_response_text for version in versions}
    question_text_mismatch = len(unique_questions) > 1
    response_text_mismatch = len(unique_responses) > 1

    if not question_text_mismatch and not response_text_mismatch:
        return None

    longest_length = max(len(version.normalized_response_text) for version in versions)
    longest_versions = [
        version for version in versions if len(version.normalized_response_text) == longest_length
    ]
    longest_texts = {version.normalized_response_text for version in longest_versions}
    longest_reviewers = tuple(version.reviewer for version in longest_versions)

    clean_prefix_truncation: bool | None
    if not response_text_mismatch:
        clean_prefix_truncation = None
    elif len(longest_texts) != 1:
        clean_prefix_truncation = False
    else:
        longest_text = longest_versions[0].normalized_response_text
        clean_prefix_truncation = all(
            version.normalized_response_text == longest_text
            or (
                len(version.normalized_response_text) < len(longest_text)
                and longest_text.startswith(version.normalized_response_text)
            )
            for version in versions
        )

    return TextMismatch(
        response_id=response_id,
        question_text_mismatch=question_text_mismatch,
        response_text_mismatch=response_text_mismatch,
        longest_reviewers=longest_reviewers,
        clean_prefix_truncation=clean_prefix_truncation,
        versions=tuple(versions),
    )


def analyze_text_mismatches(
    review_frames: dict[str, pd.DataFrame],
    *,
    reviewer_sources: dict[str, str] | None = None,
) -> list[TextMismatch]:
    versions_by_response_id = _collect_text_versions(
        review_frames,
        reviewer_sources=reviewer_sources,
    )
    mismatches = []
    for response_id, versions in sorted(versions_by_response_id.items()):
        mismatch = _analyze_text_mismatch(response_id, versions)
        if mismatch is not None:
            mismatches.append(mismatch)
    return mismatches


def summarize_reconciliation(mismatches: list[TextMismatch]) -> ReconciliationSummary:
    resolved_response_truncations = sorted(
        mismatch.response_id
        for mismatch in mismatches
        if mismatch.response_text_mismatch and mismatch.clean_prefix_truncation is True
    )
    wd_question_variations = sorted(
        mismatch.response_id for mismatch in mismatches if mismatch.question_text_mismatch
    )
    unresolved_response_mismatches = sorted(
        mismatch.response_id
        for mismatch in mismatches
        if mismatch.response_text_mismatch and mismatch.clean_prefix_truncation is False
    )
    return ReconciliationSummary(
        resolved_response_truncations=tuple(resolved_response_truncations),
        wd_question_variations=tuple(wd_question_variations),
        unresolved_response_mismatches=tuple(unresolved_response_mismatches),
    )


def _tail_text(text: str, *, size: int = 100) -> str:
    return text[-size:] if len(text) > size else text


def _escape_markdown(text: str) -> str:
    return html.escape(text).replace("|", "\\|")


def _render_tail_table(versions: tuple[TextVersion, ...]) -> str:
    header = "| " + " | ".join(
        f"{version.reviewer} ({len(version.normalized_response_text)})" for version in versions
    ) + " |"
    separator = "|" + "|".join(["---"] * len(versions)) + "|"
    values = "| " + " | ".join(
        _escape_markdown(_tail_text(version.normalized_response_text)) or "&nbsp;"
        for version in versions
    ) + " |"
    return "\n".join((header, separator, values))


def render_text_mismatch_report(
    mismatches: list[TextMismatch],
    *,
    raw_dir: Path | str,
    reconciliation_summary: ReconciliationSummary,
) -> str:
    raw_path = Path(raw_dir)
    clean_prefix_count = len(reconciliation_summary.resolved_response_truncations)
    substantive_count = len(reconciliation_summary.unresolved_response_mismatches)
    question_variation_count = len(reconciliation_summary.wd_question_variations)

    lines = [
        "# Text Reconciliation Report",
        "",
        f"Source directory: `{raw_path}`",
        "Lengths and tails below use whitespace-normalized `response_text` values.",
        "",
        f"- Mismatched response_id values: {len(mismatches)}",
        f"- Resolved response-text truncations via longest-version rule: {clean_prefix_count}",
        f"- Resolved question-phrasing variations via WD canonical question text: {question_variation_count}",
        f"- Remaining unresolved response mismatches: {substantive_count}",
        "",
    ]

    if not mismatches:
        lines.append("No text mismatches detected across reviewer files.")
        return "\n".join(lines) + "\n"

    if substantive_count == 0:
        lines.append("No remaining mismatches after applying reconciliation rules.")
        lines.append("")

    reviewer_rank = {workbook.reviewer: index for index, workbook in enumerate(REVIEWER_WORKBOOKS)}

    for mismatch in mismatches:
        ordered_versions = tuple(
            sorted(
                mismatch.versions,
                key=lambda version: reviewer_rank.get(version.reviewer, len(reviewer_rank)),
            )
        )
        longest_text = max(
            ordered_versions,
            key=lambda version: len(version.normalized_response_text),
        ).normalized_response_text
        lines.extend(
            [
                f"## {mismatch.response_id}",
                "",
                f"- Question text mismatch: {'yes' if mismatch.question_text_mismatch else 'no'}",
                f"- Response text mismatch: {'yes' if mismatch.response_text_mismatch else 'no'}",
                "- Longest reviewer(s): "
                + (
                    ", ".join(mismatch.longest_reviewers)
                    if mismatch.longest_reviewers
                    else "n/a"
                ),
                "- Clean prefix truncation: "
                + (
                    "yes"
                    if mismatch.clean_prefix_truncation is True
                    else "no"
                    if mismatch.clean_prefix_truncation is False
                    else "n/a"
                ),
                f"- WD canonical question text selected: {'yes' if mismatch.question_text_mismatch else 'n/a'}",
                f"- Status after reconciliation: "
                + (
                    "resolved"
                    if not (
                        mismatch.response_text_mismatch and mismatch.clean_prefix_truncation is False
                    )
                    else "unresolved"
                ),
                "",
                "| Reviewer | File | Length | Is longest | Prefix of longest |",
                "|---|---|---:|---|---|",
            ]
        )

        for version in ordered_versions:
            response_length = len(version.normalized_response_text)
            is_longest = "yes" if response_length == len(longest_text) else "no"
            if version.normalized_response_text == longest_text:
                prefix_status = "same"
            elif longest_text.startswith(version.normalized_response_text):
                prefix_status = "yes"
            else:
                prefix_status = "no"
            lines.append(
                f"| {version.reviewer} | `{version.source_name}` | {response_length} | "
                f"{is_longest} | {prefix_status} |"
            )

        lines.extend(
            [
                "",
                "### Last 100 Characters By Reviewer",
                "",
                _render_tail_table(ordered_versions),
                "",
            ]
        )

    return "\n".join(lines) + "\n"


def write_text_mismatch_report(
    mismatches: list[TextMismatch],
    *,
    raw_dir: Path | str,
    processed_dir: Path | str,
    reconciliation_summary: ReconciliationSummary,
) -> Path:
    output_dir = Path(processed_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "text_mismatches.md"
    report_path.write_text(
        render_text_mismatch_report(
            mismatches,
            raw_dir=raw_dir,
            reconciliation_summary=reconciliation_summary,
        ),
        encoding="utf-8",
    )
    return report_path


def load_human_scores(raw_dir: Path | str) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames, _ = load_review_frames(raw_dir)
    return build_human_scores_from_frames(frames)


def save_human_scores(
    long_df: pd.DataFrame,
    consensus_df: pd.DataFrame,
    *,
    processed_dir: Path | str,
    report_path: Path | None = None,
) -> dict[str, Path]:
    output_dir = Path(processed_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "human_scores_long_parquet": output_dir / "human_scores_long.parquet",
        "human_scores_long_csv": output_dir / "human_scores_long.csv",
        "human_scores_consensus_parquet": output_dir / "human_scores_consensus.parquet",
        "human_scores_consensus_csv": output_dir / "human_scores_consensus.csv",
    }
    if report_path is not None:
        outputs["text_mismatches_report"] = report_path

    long_df.to_parquet(outputs["human_scores_long_parquet"], index=False)
    long_df.to_csv(outputs["human_scores_long_csv"], index=False)
    consensus_df.to_parquet(outputs["human_scores_consensus_parquet"], index=False)
    consensus_df.to_csv(outputs["human_scores_consensus_csv"], index=False)
    return outputs


def run_phase_one(
    *,
    raw_dir: Path | str,
    processed_dir: Path | str,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Path], ReconciliationSummary]:
    frames, reviewer_sources = load_review_frames(raw_dir)
    mismatches = analyze_text_mismatches(frames, reviewer_sources=reviewer_sources)
    reconciliation_summary = summarize_reconciliation(mismatches)
    report_path = write_text_mismatch_report(
        mismatches,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        reconciliation_summary=reconciliation_summary,
    )
    if reconciliation_summary.unresolved_response_mismatches:
        unresolved = ", ".join(reconciliation_summary.unresolved_response_mismatches)
        raise ValueError(f"Unresolved substantive response-text mismatches remain: {unresolved}")

    long_df, consensus_df = build_human_scores_from_frames(frames)
    missing_quality_entries = collect_missing_quality_entries(long_df)
    reconciliation_summary = replace(
        reconciliation_summary,
        missing_quality_entries=missing_quality_entries,
    )
    outputs = save_human_scores(
        long_df,
        consensus_df,
        processed_dir=processed_dir,
        report_path=report_path,
    )
    return long_df, consensus_df, outputs, reconciliation_summary
