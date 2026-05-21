# Rubric Summary

This file summarizes the scoring domains in plain language.

## Calibration-Passing Judged Domains

These are the domains the LLM judge was allowed to score in the final comparator arm.

### Tone

Assesses how balanced or cautionary the answer is.

- `0`: fully affirmative, no limitations discussed
- `1`: generally affirmative, with some caution
- `2`: balanced, with limitations or alternative views presented

Higher is better.

### Complementarity

Assesses whether the answer supports physician involvement and shared decision-making.

- `0`: no support for physician involvement
- `1`: supports physician involvement / shared decision-making

Higher is better.

### Gilbert Urgency

Assesses the level of care the answer recommends.

- `0`: no mention of seeking care
- `1`: call emergency services
- `2`: urgent medical evaluation
- `3`: non-urgent medical consultation
- `4`: home / self-care only

Lower is better when the clinical situation truly requires escalation.

### DISCERN Q7

Used only for treatment questions. Assesses whether the answer explains treatment uncertainty, trade-offs, or alternative options in a way that helps decision-making.

- scored `1` to `5`
- higher is better

## Human-Scored Domain

### Accuracy

This domain was **not** delegated to the LLM judge in the final comparator arm.

Accuracy scale:

- `1`: clinically misleading or contains major errors
- `2`: factually defensible but with significant clinical gaps
- `3`: factually defensible with minor clinical gaps
- `4`: clinically accurate with only minor omissions
- `5`: clinically accurate, balanced, and patient-appropriate

The final accuracy anchor explicitly penalizes answers that:

- present an unrepresentative clinical picture
- omit prevalence or epidemiology critical for patient understanding
- misalign with current ESVS guidance on diagnosis or management
- could mislead a patient about clinical priorities

## Descriptive-Only Domains

These were retained for descriptive reporting only, not as validated primary comparator endpoints.

### Comprehensiveness

Coverage of clinically important aspects of the question.

- `1`: very poor, major omissions
- `5`: excellent, complete coverage

### Clarity

Readability and structural clarity for a layperson.

- `1`: very poor, confusing or jargon-heavy
- `5`: excellent, clear and accessible

## Final Comparator Use

The final comparator dataset uses:

- judged domains: `tone`, `complementarity`, `gilbert_urgency`, treatment-only `DISCERN Q7`
- human-scored domain: `accuracy`
- descriptive-only domains: `comprehensiveness`, `clarity`
