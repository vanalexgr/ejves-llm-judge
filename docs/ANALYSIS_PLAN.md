# Comparator Analysis Plan

This file describes how the final comparator outputs should be summarized in the manuscript and reviewer materials.

## Final Analysis Dataset

Use [outputs/comparator/comparator_results.parquet](/home/vga/Documents/New project 5/outputs/comparator/comparator_results.parquet) as the canonical final comparator dataset.

It contains:

- `48` comparator responses
- `16` matched vascular question stems
- `3` models:
  - `GPT-5.5`
  - `Gemini 3.5 Flash`
  - `Claude Sonnet 4.6`
- fully resolved human `validated_accuracy`

## Primary Comparator Endpoints

These are the endpoints that should be emphasized in the main manuscript results:

- `validated_accuracy`
- `validated_tone`
- `validated_complementarity`
- `validated_gilbert_urgency`
- `validated_discern_q7` for treatment responses only

Interpretation:

- higher is better for `accuracy`, `tone`, `complementarity`, and `DISCERN Q7`
- lower is better for `gilbert_urgency`, because lower scores reflect stronger escalation to appropriate care

## Descriptive-Only Endpoints

These may be shown in a supplementary or descriptive table, but should not be framed as calibration-validated primary outcomes:

- `descriptive_comprehensiveness`
- `descriptive_clarity`

## Benchmark Comparison

Compare the 3 newer comparator models against the reconstructed original GPT-3.5 study benchmark from [data/processed/human_scores_consensus.parquet](/home/vga/Documents/New project 5/data/processed/human_scores_consensus.parquet).

For benchmark summaries, use the reconstructed consensus **mean** columns:

- `accuracy_mean`
- `tone_mean`
- `complementarity_mean`
- `gilbert_urgency_mean`
- `discern_q7_mean`
- `comprehensiveness_mean`
- `clarity_mean`

This keeps the benchmark on the same averaged-score scale as the comparator outputs.

## Recommended Tables

### Main table

Per-model means for:

- Accuracy
- Tone
- Complementarity
- Urgency
- DISCERN Q7 (treatment questions only)

### Benchmark comparison table

For each validated endpoint:

- original GPT-3.5 benchmark mean
- each newer model mean
- delta vs original

For urgency, deltas should be sign-flipped in presentation so that positive values mean improvement relative to the original GPT-3.5 benchmark.

### Descriptive table

Per-model means for:

- Comprehensiveness
- Clarity

With explicit note that these are descriptive-only because calibration reliability was low for both humans and judges.

### Accuracy resolution table

Report:

- dual-surgeon exact-agreement rows
- dual-surgeon mean rows
- triple-surgeon adjudication rows

## Core Manuscript Claim

The final paper should present the newer models as:

- improved or contemporary comparators relative to the original GPT-3.5 benchmark on the calibration-passing communication domains
- still requiring blinded surgeon review for clinical accuracy

The paper should **not** claim that the LLM judge validated accuracy or that it can replace surgeon judgment on the clinical endpoint.
