# EJVES LLM Judge Pipeline

This repository contains the code, processed data, prompts, calibration outputs, and final comparator-arm artifacts for an LLM-as-judge pipeline built around the EJVES vascular ChatGPT study.

## Scope

The project has two linked goals:

1. Reconstruct the original 16-response GPT-3.5 study dataset from the archived human reviewer spreadsheets.
2. Calibrate a two-judge ensemble (`claude-opus-4-7` and `gpt-5`) against the original human consensus before applying only the calibration-passing parts of the rubric to a newer comparator set.

## What Is In The Repository

- `src/ejves_judge/`
  Core package for data loading, rubric definitions, prompt generation, judge clients, calibration analysis, report generation, Phase 6 fallback documentation, and restricted comparator scoring.
- `scripts/`
  CLI entrypoints for each project phase.
- `tests/`
  Focused regression tests for the loader, prompt builder, judge retry logic, calibration analysis, and restricted comparator workflow.
- `data/processed/`
  Long-format and consensus-format human review outputs reconstructed from the archived reviewer spreadsheets.
- `outputs/phase2_prompts/`
  The 16 blinded judge prompts generated from the canonical study responses.
- `outputs/calibration/`
  Calibration reports, agreement plots, aggregated judge outputs, and manuscript-facing fallback documentation.
- `outputs/comparator/`
  Comparator-arm outputs for 48 newer responses: 16 vascular questions answered by `GPT-5.5`, `Gemini 3.5 Flash`, and `Claude Sonnet 4.6`.
- `docs/`
  Plain-language study narrative, rubric summary, and comparator analysis plan for collaborators and reviewers.

## Comparator Model Naming

The public-facing comparator labels are:

- `chatgpt_free` = `GPT-5.5`
- `gemini_free` = `Gemini 3.5 Flash`
- `claude_free` = `Claude Sonnet 4.6`

## Current Status

- Phase 1: complete
- Phase 2: complete
- Phase 3 sanity check: complete
- Phase 4 calibration run: complete (`96/96` successful judge calls)
- Phase 5 agreement analysis/report: complete
- Phase 6 restricted comparator scoring: complete, including final human accuracy adjudication

The comparator pipeline deliberately does **not** use the judge for the final `accuracy` endpoint. Calibration showed that urgency, tone, complementarity, and treatment-only DISCERN-Q7 were calibration-passing judged domains, but accuracy did not validate strongly enough for unsupervised use. For that reason, the comparator arm keeps:

- judge outputs for the calibration-passing domains `tone`, `complementarity`, `gilbert_urgency`, and treatment-only `discern_q7`
- descriptive-only judge outputs for `comprehensiveness` and `clarity`
- blinded surgeon review for `accuracy`

The final human accuracy workflow is:

- two independent blinded board-certified surgeon ratings on all `48` comparator responses
- explicit Mario rescoring on `2` disputed rows
- blinded third-surgeon adjudication on the `5` rows that initially differed by at least two points
- final resolved comparator accuracy stored in `outputs/comparator/comparator_results.parquet`

## Key Calibration Findings

The completed calibration run supports direct judge use only on the domains that passed calibration. The decisive failure point was `accuracy`, which remained below the inter-human agreement floor after the finalized Track B accuracy-anchor revision. The manuscript-facing summary of that decision is in:

- `outputs/calibration/agreement_report.md`
- `outputs/calibration/phase6_comparator_methodology.md`
- `outputs/calibration/methods_addendum.md`
- `outputs/comparator/comparator_report.md`
- `docs/STUDY_NARRATIVE.md`

## Reproducibility Notes

The repository includes generated artifacts so reviewers can inspect results directly without re-running API calls. The `.env` file is intentionally excluded from version control because it contains provider credentials.

To run the test suite locally:

```bash
PYTHONPATH=src python3 -m pytest -q
```

To score a comparator CSV after credentials are configured:

```bash
python3 scripts/03_score_new_responses.py --input-csv outputs/comparator/comparator_input_template_48rows.csv
```

To regenerate the final comparator report from the resolved adjudicated dataset:

```bash
python3 scripts/08_generate_comparator_report.py
```

## Project Name

Python package name: `ejves-llm-judge`
