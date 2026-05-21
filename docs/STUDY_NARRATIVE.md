# Study Narrative

This repository documents a vascular-surgery LLM evaluation workflow built in two stages.

First, the original study dataset was reconstructed from the archived reviewer spreadsheets. That yielded the canonical 16 GPT-3.5 responses, together with the original three-surgeon ratings in long format and reconstructed consensus outputs. Those files live in [data/processed](/home/vga/Documents/New project 5/data/processed).

Second, an LLM-as-judge pipeline was calibrated on those same 16 responses before it was allowed to score newer comparator models. The calibration used two API judge models, `claude-opus-4-7` and `gpt-5`, with three runs per judge per response. The central question was not whether the judges were “good in general,” but whether they reproduced surgeon consensus reliably enough on each rubric domain to be used downstream.

The calibration result was mixed. `Tone`, `complementarity`, `gilbert_urgency`, and treatment-only `DISCERN Q7` passed calibration well enough to be used in the comparator arm. `Accuracy` did not. After the final Track B calibration pass, the accuracy anchor had been tightened to penalize clinically unrepresentative but factually defensible answers, yet the two judge models still moved in different directions rather than converging on a stable common target. That is why the project does not use the judge for the final comparator accuracy endpoint.

The comparator arm contains 48 responses: 16 vascular question stems answered by 3 newer models, `GPT-5.5`, `Gemini 3.5 Flash`, and `Claude Sonnet 4.6`. For these responses, the judge pipeline was used only on the calibration-passing domains: `tone`, `complementarity`, `gilbert_urgency`, and treatment-only `DISCERN Q7`. `Comprehensiveness` and `clarity` were retained as descriptive-only outputs because both human and judge reliability were low in calibration. `Accuracy` was reserved for blinded human review.

The final comparator accuracy endpoint is fully resolved. Two blinded board-certified surgeons rated all 48 comparator responses independently. Mario then made 2 explicit score revisions after reviewing the rationale set. The 5 rows that still had at least a 2-point initial disagreement were sent to a blinded third board-certified surgeon for adjudication. The final comparator dataset therefore uses dual-surgeon agreement or mean for 43 rows and a triple-surgeon median for the 5 adjudicated rows.

The practical interpretation is straightforward. This repository does **not** argue that AI judges can replace surgeons. It argues something narrower and more defensible: the judge can be used as a calibrated instrument on some communication-oriented domains, but clinical accuracy still required blinded surgeon review in the comparator arm.
