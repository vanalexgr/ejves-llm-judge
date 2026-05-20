"""Rubric constants and structured output schemas for Phase 2."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


RUBRIC_TONE = """### A. Tone (QUEST item) — 0 to 2

- `0`: Fully affirmative with no limitations discussed
- `1`: Generally affirmative, cautious language
- `2`: Balanced, with limitations or alternate views presented
"""

RUBRIC_COMPLEMENTARITY = """### B. Complementarity (QUEST item) — 0 or 1

- `0`: No support for physician involvement
- `1`: Supportive of shared decision-making and physician input
"""

RUBRIC_URGENCY = """### C. Urgency of Care Recommendation (Gilbert) — 0 to 4

Assesses what level of care, if any, the response recommends. This is a categorical level, not a severity scale.

- `0`: No mention of seeking care
- `1`: Call emergency services
- `2`: Urgent medical evaluation
- `3`: Non-urgent medical consultation
- `4`: Home / self-care only
"""

RUBRIC_DISCERN = """### D. Discussion of Uncertainty (DISCERN Q7) — 1 to 5 — **TREATMENT QUESTIONS ONLY**

"Does the information describe the uncertainty of treatment?"

- `1`: No mention of uncertainty
- `2`–`4`: Partial or incomplete discussion of uncertainties
- `5`: Explicit acknowledgment of uncertainty or variability in treatment outcomes

For symptom/natural-history questions, this field must be omitted from the judge's output (not zero, not null — the schema validator should require its absence for non-treatment items).
"""

RUBRIC_LIKERT = """### E. Likert quality domains — 1 to 5 each

- **Accuracy** — clinical correctness of the response as a whole, not merely the defensibility of individual stated facts. Penalize responses that (a) present an unrepresentative clinical picture (e.g., describing typically-asymptomatic conditions as symptomatic), (b) omit prevalence or epidemiology critical for patient understanding, (c) misalign with current ESVS guidelines on diagnosis or management, or (d) could mislead a patient about clinical priorities. 1 = clinically misleading or contains major errors; 2 = factually defensible but with significant clinical gaps; 3 = factually defensible with minor clinical gaps; 4 = clinically accurate with only minor omissions; 5 = clinically accurate, balanced, and patient-appropriate.
- **Comprehensiveness** — coverage of clinically important aspects of the question. 1 = very poor (major omissions); 5 = excellent (complete coverage)
- **Clarity** — readability and structural clarity of the response for a layperson. 1 = very poor (confusing or jargon-heavy); 5 = excellent (clear and accessible)
"""

RUBRIC_APPROPRIATENESS = """### F. Derived appropriateness — binary

Appropriate iff `accuracy ≥ 3 AND comprehensiveness ≥ 3 AND clarity ≥ 3`. Compute downstream from the Likert scores; do not ask the judge to produce this directly.
"""

RUBRIC_TEXT_SYMPTOMS = "\n\n".join(
    (
        RUBRIC_TONE,
        RUBRIC_COMPLEMENTARITY,
        RUBRIC_URGENCY,
        RUBRIC_LIKERT,
    )
)

RUBRIC_TEXT_TREATMENT = "\n\n".join(
    (
        RUBRIC_TONE,
        RUBRIC_COMPLEMENTARITY,
        RUBRIC_URGENCY,
        RUBRIC_DISCERN,
        RUBRIC_LIKERT,
    )
)


class SymptomJudgeOutput(BaseModel):
    """Structured output for symptom and natural-history items."""

    model_config = ConfigDict(extra="forbid")

    tone: int = Field(ge=0, le=2)
    complementarity: int = Field(ge=0, le=1)
    gilbert_urgency: int = Field(ge=0, le=4)
    accuracy: int = Field(ge=1, le=5)
    comprehensiveness: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    rationale: str = Field(
        min_length=20,
        max_length=1500,
        description="Concise justification for the scores.",
    )


class TreatmentJudgeOutput(BaseModel):
    """Structured output for treatment items."""

    model_config = ConfigDict(extra="forbid")

    tone: int = Field(ge=0, le=2)
    complementarity: int = Field(ge=0, le=1)
    gilbert_urgency: int = Field(ge=0, le=4)
    discern_q7: int = Field(ge=1, le=5)
    accuracy: int = Field(ge=1, le=5)
    comprehensiveness: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    rationale: str = Field(
        min_length=20,
        max_length=1500,
        description="Concise justification for the scores.",
    )


def rubric_text_for_question_group(question_group: str) -> str:
    """Return the rubric text for the given question group."""

    if question_group == "symptoms":
        return RUBRIC_TEXT_SYMPTOMS
    if question_group == "treatment":
        return RUBRIC_TEXT_TREATMENT
    raise ValueError(f"Unsupported question_group: {question_group!r}")


def output_model_for_question_group(question_group: str) -> type[BaseModel]:
    """Return the correct output schema for the given question group."""

    if question_group == "symptoms":
        return SymptomJudgeOutput
    if question_group == "treatment":
        return TreatmentJudgeOutput
    raise ValueError(f"Unsupported question_group: {question_group!r}")
