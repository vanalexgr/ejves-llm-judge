# Study Narrative

This repository documents a vascular-surgery LLM evaluation workflow built in two stages.

First, the original study dataset was reconstructed from the archived reviewer spreadsheets. That yielded the canonical 16 GPT-3.5 responses, together with the original three-surgeon ratings in long format and reconstructed consensus outputs. Those files live in [data/processed](/home/vga/Documents/New project 5/data/processed).

Second, an LLM-as-judge pipeline was calibrated on those same 16 responses before it was allowed to score newer comparator models. The calibration used two API judge models, `claude-opus-4-7` and `gpt-5`, with three runs per judge per response. The central question was not whether the judges were “good in general,” but whether they reproduced surgeon consensus reliably enough on each rubric domain to be used downstream.

The calibration result was mixed. `Tone`, `complementarity`, `gilbert_urgency`, and treatment-only `DISCERN Q7` passed calibration well enough to be used in the comparator arm. `Accuracy` did not. After the final Track B calibration pass, the accuracy anchor had been tightened to penalize clinically unrepresentative but factually defensible answers, yet the two judge models still moved in different directions rather than converging on a stable common target. That is why the project does not use the judge for the final comparator accuracy endpoint.

The comparator arm contains 48 responses: 16 vascular question stems answered by 3 newer models, `GPT-5.5`, `Gemini 3.5 Flash`, and `Claude Sonnet 4.6`. These comparator responses were collected from the models' free consumer-facing interfaces and then copied into the evaluation pipeline. For these responses, the judge pipeline was used only on the calibration-passing domains: `tone`, `complementarity`, `gilbert_urgency`, and treatment-only `DISCERN Q7`. `Comprehensiveness` and `clarity` were retained as descriptive-only outputs because the later Table 2 correction showed that, in the original symptoms-topic analysis (`n = 4` diseases), those constructs were not meaningfully estimable under ICC(2,k); the response-level judge calibration in this repository was likewise weak on both. `Accuracy` was reserved for blinded human review.

The final comparator accuracy endpoint is fully resolved. Two blinded board-certified surgeons rated all 48 comparator responses independently. Mario then made 2 explicit score revisions after reviewing the rationale set. The 5 rows that still had at least a 2-point initial disagreement were sent to a blinded third board-certified surgeon for adjudication. The final comparator dataset therefore uses dual-surgeon agreement or mean for 43 rows and a triple-surgeon median for the 5 adjudicated rows.

The practical interpretation is straightforward. This repository does **not** argue that AI judges can replace surgeons. It argues something narrower and more defensible: the judge can be used as a calibrated instrument on some communication-oriented domains, but clinical accuracy still required blinded surgeon review in the comparator arm.

## Important Caveats

- The calibration dataset is small (`n = 16` responses), so all agreement estimates should be interpreted with uncertainty rather than as fixed population values.
- The calibration pass/fail rule was floor-based. That means some domains, especially `tone`, passed because the judge exceeded the pre-specified inter-human floor even though absolute agreement remained modest.
- The original GPT-3.5 benchmark and the newer comparator arm are not perfectly measurement-equivalent. Historical benchmark values come from the reconstructed earlier human-review workflow, whereas comparator accuracy comes from a later dual-surgeon plus adjudication process.
- VGA served as one of the comparator-arm blinded accuracy raters and is disclosed here as a board-certified surgeon, not as one of the original historical raters.
- The calibration corpus consisted of older GPT-3.5 responses, whereas the comparator corpus contains newer 2025/26-era model responses. That transport across response distributions is a practical external check, not proof of universal judge validity.
