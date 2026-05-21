# Plain-Language Summary

This project asks a practical clinical-methods question: can an AI judge be used to score vascular chatbot answers in the same way that surgeons would score them?

The short answer is: **only partly**.

I first reconstructed the original study dataset of 16 GPT-3.5 vascular responses and the three-surgeon scoring that went with it. I then tested a two-model AI judging system against that historical surgeon reference standard. The AI judge performed best on urgency of care and was usable, with caution, on some communication-oriented domains such as tone, support for physician involvement, and discussion of treatment uncertainty. It did **not** perform well enough on clinical accuracy.

That failure on accuracy is an important result, not a nuisance. Even after tightening the accuracy rubric, the two AI judges moved in opposite directions rather than converging. That means the system was not recovering a stable target for accuracy, so I stopped tuning and did not let the AI judge control the final accuracy endpoint.

The comparator arm therefore used a mixed design:

- the AI judge scored the domains that passed calibration well enough for limited downstream use
- surgeons scored clinical accuracy directly

For the newer comparator set, I collected 48 responses in total: 16 vascular question stems answered by 3 newer models:

- `GPT-5.5`
- `Gemini 3.5 Flash`
- `Claude Sonnet 4.6`

Clinical accuracy on those 48 responses was rated in a blinded human workflow by two board-certified surgeons, with a third board-certified surgeon adjudicating the 5 cases with larger disagreement. So the final comparator accuracy endpoint is fully human-resolved.

The current bottom line is:

- newer models are generally better communicators than the original GPT-3.5 benchmark
- urgency of care is the strongest and most defensible AI-judged domain
- tone, complementarity, and treatment uncertainty can be used, but with caution
- clinical accuracy still required surgeon review

There is one further nuance. During revision, the original manuscript's Table 2 was corrected: clarity and comprehensiveness were not reliably estimable in the small original topic-level human analysis. That means weak AI-judge performance on those domains should not be interpreted as a pure model failure. The human ground truth for those constructs was itself unstable at that sample size.

So the central conclusion is not that AI can replace surgeons. It is that **AI judging works where the construct is stable and reproducible, and fails or becomes uninterpretable where the human target is unstable or where clinical accuracy remains too important to delegate.**

Key files:

- Main comparator results: [outputs/comparator/comparator_report.md](outputs/comparator/comparator_report.md)
- Calibration audit trail: [outputs/calibration/agreement_report.md](outputs/calibration/agreement_report.md)
- Final comparator dataset: [outputs/comparator/comparator_results.parquet](outputs/comparator/comparator_results.parquet)
- Narrative methods summary: [docs/STUDY_NARRATIVE.md](docs/STUDY_NARRATIVE.md)
