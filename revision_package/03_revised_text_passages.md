# Revised Text — All Changed Passages, Ready to Apply

This file contains the final replacement text for every item in the change log, formatted for copy-paste into the Word document. Apply each passage at the line number indicated.

---

## ABSTRACT — Revised lines 85–97

Replace the existing Results and Conclusions sentences of the abstract with:

> No significant differences were found in tone or complementarity across disease categories or question types. Urgency did not differ significantly between symptom-related and treatment-related queries overall; however, urgency varied significantly across sub-types of symptom-related questions (p = 0.03), consistent with inconsistent escalation recommendations. The mean FRE was 32.3 ± 12.1 and FKGL 13.5 ± 2, corresponding to a university-level reading requirement. Symptom-related responses were more readable than treatment-related ones (FRE 38.1 ± 10.3 vs 26.4 ± 11.4; p = 0.025). Among the sixteen outputs, only seven (43.7%) were judged clinically appropriate by all reviewers; clarity was rated adequate in 81% of responses, whereas only 50% reached acceptable accuracy and 69% acceptable comprehensiveness. Treatment-related answers were particularly weak, with only 25% deemed appropriate. In symptom-related questions, misalignment of urgency recommendations emerged as a potential patient-safety concern.

> In this specialist evaluation, ChatGPT outputs related to vascular surgery were clear, but mostly clinically inappropriate and inaccurate, and required 13th-grade reading skills. The combination of low accuracy and poor accessibility presents a serious patient-safety concern for unsupervised patient education. As they stand, generalist LLMs cannot provide patient-facing information about vascular surgery. A rigorously validated, domain-specific and knowledge-locked AI system based on curated vascular guidelines may be more appropriate to ensure safety and comprehension.

---

## WHAT THIS PAPER ADDS — Revised lines 48–50

Replace:
> "This combination of factual unreliability and poor accessibility represents an unacceptable risk for unsupervised patient education."

With:
> "This combination of factual unreliability and poor accessibility represents a serious patient-safety concern for unsupervised patient education."

---

## METHODS — DISCERN Q7 section (lines 193–197)

Replace the entire passage from "D) Discussion of Uncertainty..." through "...using a five-point scale:" with:

> D) Discussion of Uncertainty (from DISCERN Q7). Specifically, we used DISCERN Question 7 ("Does the information describe the uncertainty of treatment?"), which directly evaluates whether variability, risks, or limitations of therapeutic options are acknowledged, using a five-point scale:

*(The scale definitions that follow — 1: No mention of uncertainty; 2–4: Partial or incomplete discussion; 5: Explicit acknowledgment — remain unchanged.)*

---

## METHODS — Prompt settings addition (line 151)

In the sentence about entering questions into ChatGPT, add "with default prompt settings and no system-level customisation" after "(OpenAI)".

**Full revised sentence:**
> For each clinical topic, all questions were entered manually into the ChatGPT interface by a single investigator (WD) on February 28, 2026, using the publicly available ChatGPT version 3.5 (OpenAI) with default prompt settings and no system-level customisation.

---

## METHODS — Appropriateness threshold addition (after line 224)

After "Any response receiving a score of 1 or 2 in any category by any reviewer was considered inappropriate.", add:

> This conservative threshold was selected because, in a patient-safety context, a specific clinical concern raised by any one expert reviewer about accuracy, comprehensiveness, or clarity is clinically relevant regardless of the ratings of others; it may therefore underestimate the proportion of borderline-usable responses.

---

## METHODS — Statistical Analysis addition (after line 241)

After "Correlation analyses were considered exploratory, and results are interpreted primarily based on effect sizes rather than statistical significance.", add:

> Given the small sample size (n = 16 responses), all statistical analyses in this study should be regarded as exploratory and hypothesis-generating rather than confirmatory.

---

## METHODS — New comparator arm subsection (insert after line 224, before Statistical Analysis)

Insert new subsection heading and paragraph:

> ***Comparator Analysis with Current-Generation Models***
>
> To evaluate whether the limitations identified in ChatGPT (gpt-3.5-turbo-0125) persisted in more recent models, a pre-specified comparator analysis was conducted. Responses to the same 16 question stems were collected from three current-generation generalist models — GPT-5.5, Gemini 3.5 Flash, and Claude Sonnet 4.6 — accessed through their publicly available consumer interfaces in February 2026, using identical session isolation protocols as the original study. These responses were scored using a validated two-model LLM-as-judge ensemble calibrated against the original human consensus scores; the judge was applied only to domains demonstrating sufficient calibration agreement (tone, complementarity, urgency of care, and treatment-related uncertainty [DISCERN Q7] for treatment questions). Clinical accuracy was independently evaluated by two blinded board-certified vascular surgeons, with a third surgeon adjudicating responses showing ≥2-point disagreement (5 of 48 responses). Comprehensiveness and clarity are reported descriptively, as inter-rater reliability for these domains was insufficient for validated endpoint use at this sample size.

---

## RESULTS — Inter-rater reliability (lines 251–254)

Replace:
> "Inter-rater reliability for subjective assessments was moderate to good across all evaluated domains. The ICC for accuracy demonstrated good agreement, while clarity and comprehensiveness also showed acceptable reliability, although confidence intervals were wide, reflecting the limited number of topics evaluated (Table 2)."

With:
> Inter-rater reliability was estimable only for accuracy, which demonstrated good agreement (ICC[2,k] = 0.83; 95% CI 0.08–0.99). For clarity and comprehensiveness, between-topic variance was negligible relative to rater and residual variance at this sample size (n = 4 topics), yielding non-positive ICC estimates that were not meaningfully interpretable (Table 2). These reliability analyses should therefore be regarded as exploratory.

---

## RESULTS — Appropriateness addition (after line 288)

After "Only 7 of the 16 generated outputs (43.7%), were rated as appropriate by the reviewers (Figure 2).", add:

> Table 5 reports individual reviewer scores for each response and domain, allowing assessment of domain-specific score distributions beyond the binary classification.

---

## RESULTS — New comparator paragraph (insert after line 300, before Discussion)

Insert new section heading and paragraph:

> ***Comparator Analysis***
>
> All three current-generation models demonstrated improvement over the GPT-3.5 benchmark on communication-oriented domains (Supplementary Table 2). Urgency calibration improved marginally, with mean urgency scores of 1.91 for GPT-5.5, 2.06 for Gemini 3.5 Flash, and 2.06 for Claude Sonnet 4.6, compared with 2.10 for GPT-3.5. Tone scores improved across all comparator models (range 1.66–1.78 vs 1.31 for GPT-3.5) and support for physician involvement was maintained or increased (complementarity: 0.844–0.875 vs 0.792). Human-assessed accuracy showed modest gains for GPT-5.5 (mean 3.69) and Gemini 3.5 Flash (3.72), but remained limited for Claude Sonnet 4.6 (3.31), compared with 3.27 for GPT-3.5. Treatment uncertainty scores (DISCERN Q7) also improved, particularly for GPT-5.5 (3.50 vs 3.04 for GPT-3.5). Despite these improvements, no comparator model achieved comprehensive alignment with clinical standards across all evaluated domains.

---

## DISCUSSION — Inter-rater reliability sentence (lines 312–314)

Replace:
> "Inter-rater reliability analyses demonstrated acceptable agreement across subjective domains, supporting the internal consistency of expert assessments when applied at the topic level."

With:
> Inter-rater reliability was good for accuracy but could not be reliably estimated for clarity or comprehensiveness given the small number of topics evaluated (n = 4), underscoring the exploratory nature of these analyses and the need for larger topic samples in future evaluations.

---

## DISCUSSION — Urgency paragraph, expanded (lines 330–337)

Replace the entire existing urgency paragraph:
> "Another important aspect of safety is the appropriateness of urgency recommendations. While tone, complementarity, and urgency aggregate scores did not differ significantly between symptom-related and treatment-related questions, the variability in urgency advice within symptom-related queries was a point of concern. Missing the level of urgency of aortic, carotid or peripheral arterial conditions is likely to cause severe harm to patients. Over-reassurance of patients with potentially time-critical symptoms or, conversely, unnecessary escalation in low-risk scenarios could both have harmful consequences. It is unacceptable for any system that is directly exposed to patients to fail to identify situations that require urgent specialist assessment."

With:
> Another important aspect of safety is the appropriateness of urgency recommendations. While tone, complementarity, and urgency aggregate scores did not differ significantly between symptom-related and treatment-related questions as a whole, significant variability in urgency advice was observed within symptom-related queries (p = 0.03; Table 4). At the response level, this misalignment takes two clinically distinct forms. First, questions about aortic aneurysm symptoms received a mean urgency score of 2.67 on the Gilbert scale (between "urgent medical evaluation" and "non-urgent consultation"), despite the potential for these symptoms to herald rupture — a condition requiring emergency intervention. Second, natural history questions, where patients enquire about disease prognosis rather than acute symptoms, received more urgent urgency recommendations on average (mean 1.25) than signs and symptoms questions (mean 2.33), meaning that a patient asking about long-term disease risk was more frequently directed toward emergency services than a patient describing acute symptoms. Both under-urgencing of acute presentations and over-urgencing of stable enquiries represent distinct patient-safety failure modes. Missing the level of urgency of aortic, carotid, or peripheral arterial conditions is likely to cause severe harm; equally, unnecessary escalation of low-risk enquiries risks eroding public trust in AI-generated health information. The comparator analysis showed modest improvement in urgency calibration, with GPT-5.5 achieving the lowest mean urgency score (1.91) among the evaluated models, though systematic validation against clinical vignettes with known appropriate urgency levels remains needed before any model is considered reliable on this domain.

---

## DISCUSSION — New comparator integration paragraph (insert after line 359, before Chervonski reference)

Insert:
> Our comparator analysis indicates that communication-oriented domains — including tone, complementarity, and urgency calibration — have improved in more recent models relative to the GPT-3.5 baseline. Clinical accuracy, however, while marginally improved for two of three models, continued to require blinded human review and did not show consistent gains across all evaluated models. This pattern suggests that while newer generalist LLMs communicate more carefully, the accuracy limitations underpinning the safety concerns identified in this study have not been fully resolved by model scale or architecture advances alone. These findings are consistent with emerging evidence from other surgical specialties suggesting that accuracy limitations in generalist chatbots are persistent across model generations.

---

## DISCUSSION — Readability context (after line 344)

After the sentence ending "especially those with lower literacy or non-native language skills", add:

> It should be noted that existing patient education materials are themselves frequently above recommended reading levels; however, the gap observed here — university-level output against a sixth-grade recommendation — substantially exceeds typical deviations reported in patient information research.

---

## DISCUSSION — Future directions (after line 372)

At the end of the paragraph beginning "The findings of this study should be considered when designing future AI systems...", add:

> Future comparative evaluations should also include established patient education materials as an external reference standard, enabling direct assessment of whether AI-generated information represents a meaningful advance over currently available alternatives.

---

## LIMITATIONS (lines 373–380) — Full revised paragraph

Replace the existing Limitations paragraph with:

> This study should be interpreted in view of several limitations. The primary limitation is its sample size: 16 responses from a single LLM version represent an exploratory dataset from which generalisable conclusions should be drawn cautiously. While we assessed several disease scenarios, our evaluation was by no means exhaustive. The original analysis was restricted to ChatGPT (gpt-3.5-turbo-0125), which was state-of-the-art at the time of data collection but has since been superseded. An exploratory comparator arm evaluating three current-generation models is presented; however, those responses were collected from free consumer-facing interfaces, which may not fully replicate API-level or enterprise-tier model behaviour. Furthermore, this study did not directly assess patients' perceptions or comprehension. Readability metrics, while useful, cannot capture the full complexity of health literacy or cultural context. Also, analyses were conducted at the aggregated topic level, which may obscure within-topic variability, while correlation analyses were exploratory and not adjusted for multiple comparisons.

---

## CONCLUSIONS (lines 382–388) — Addition only

After the sentence "should not be used as standalone sources of patient information.", add:

> An exploratory comparator analysis of three 2025-era generalist models suggested partial improvement in communication-oriented domains but did not resolve core accuracy limitations.

*(Remainder of Conclusions unchanged.)*

---

## TABLE 2 — Full replacement

**Table 2. Topic-level inter-rater reliability of subjective ratings (symptoms section, n = 4 topics)**

| Domain | ICC(2,k) | 95% CI |
|--------|----------|--------|
| Accuracy | 0.83 | 0.08 to 0.99 |
| Clarity | Not estimable* | — |
| Comprehensiveness | Not estimable* | — |

*At this sample size (n = 4 disease topics), between-topic variance was negligible relative to rater and residual variance, yielding non-positive ICC point estimates that are not meaningfully interpretable.

---

## Data and Code Availability Statement

Add the following as a new standalone paragraph at the end of the Methods section, before Statistical Analysis, or as a dedicated "Data Availability" section if the journal requires one:

> The scoring pipeline, calibration outputs, blinded judge prompts, and final comparator dataset are publicly available at: https://github.com/vanalexgr/ejves-llm-judge. Raw reviewer workbooks are not publicly distributed due to confidentiality; processed consensus outputs sufficient for replication of all downstream analyses are included in the repository.

Also add the URL to the response letter cover section (see `01_response_to_reviewers.md` — add under the comparator arm methods response).

---

## Supplementary Table 2: TRIPOD-LLM Checklist

The completed TRIPOD-LLM checklist is in `revision_package/supplementary_table2_tripod_llm.md`. Submit this as Supplementary Table 2.

**Reference:** Omiye JA, Gui H, Rezaei SJ, et al. TRIPOD-LLM: a reporting guideline for studies using large language models. *Nature Medicine*. 2024. https://doi.org/10.1038/s41591-024-03425-5

**Summary status:** 15/19 items fully reported; 2 partially reported (prompt stems available at GitHub but not in main text; compute resources not formally described for consumer-interface study); 2 N/A (no fine-tuning; no in-study model updates).

**One action required:** Add "(Supplementary Table 2)" after "TRIPOD-LLM checklist" at Methods line 137.

**Optional improvement flagged in checklist (item 3f):** Consider adding a supplementary table of the 16 question stems if word count permits.

---

## New Table 7 (Comparator Results) — Insert as main Table 7

The comparator arm results should appear as **main Table 7** (not supplementary), because they are directly cited in the Results and Discussion sections. The existing table count updates from 6 main + 1 supplementary to **7 main + 2 supplementary** (adding Table 7 here and Supplementary Table 2 TRIPOD checklist).

Source data: `outputs/comparator/validated_endpoint_comparison.csv` and `outputs/comparator/model_endpoint_summary.csv` in the repository. Values are means (95% bootstrap CI).

**Table 7. Comparator model results versus GPT-3.5 benchmark across validated and descriptive domains (n = 16 responses per model)**

| Domain | GPT-3.5 (original) | GPT-5.5 | Gemini 3.5 Flash | Claude Sonnet 4.6 |
|--------|--------------------|---------|-----------------|-------------------|
| Accuracy†, mean (95% CI) | 3.27 (2.93–3.66) | 3.69 (3.45–3.94) | 3.72 (3.55–3.91) | 3.31 (3.00–3.52) |
| Tone‡, mean (95% CI) | 1.31 (1.21–1.44) | 1.66 (1.47–1.81) | 1.72 (1.59–1.84) | 1.78 (1.66–1.91) |
| Complementarity‡, mean (95% CI) | 0.79 (0.70–0.90) | 0.88 (0.73–0.97) | 0.84 (0.72–0.94) | 0.88 (0.75–1.00) |
| Urgency (Gilbert scale)§, mean (95% CI) | 2.10 (1.70–2.49) | 1.91 (1.55–2.28) | 2.06 (1.53–2.50) | 2.06 (1.73–2.39) |
| DISCERN Q7‡¶, mean (95% CI) | 3.04 (2.83–3.23) | 3.50 (2.65–4.47) | 3.13 (2.25–4.13) | 3.19 (2.37–3.94) |
| Comprehensiveness*, mean (95% CI) | [see Table 5] | 4.46 (4.33–4.62) | 4.63 (4.50–4.77) | 4.91 (4.83–4.98) |
| Clarity*, mean (95% CI) | [see Table 5] | 5.00 | 4.98 (4.95–5.00) | 4.91 (4.80–4.99) |

*Comprehensiveness and clarity are reported descriptively only; inter-rater reliability for these domains was insufficient for validated endpoint use at this sample size (see Table 2).  
†Accuracy scored on a 1–5 clinical accuracy scale (higher = better). GPT-3.5 value derived from 3-surgeon consensus; comparator values from dual/triple-surgeon blinded review with adjudication for responses with ≥2-point disagreement.  
‡Higher score indicates better performance.  
§Gilbert urgency scale 0–4 (0 = emergency call, 4 = home/self-care); lower score indicates more urgent recommendation. Clinically appropriate urgency depends on question type; see text for interpretation.  
¶DISCERN Q7 scored on a 1–5 scale (higher = better); treatment questions only (n = 8 per model).  
95% CIs derived from 1,000-iteration bootstrap resampling.

---

## Generative AI Use Statement — Insert as standalone section after Acknowledgements

Elsevier policy requires a dedicated AI use disclosure. Add the following as a new section titled **"Declaration of Generative AI and AI-assisted technologies in the writing process"**:

> During the preparation of this work, the authors used Claude Code (Anthropic) and Codex (OpenAI) to assist with programming, data analysis pipeline construction, and manuscript formatting. After using these tools, the authors reviewed and edited all content as needed and take full responsibility for the integrity of the work and the accuracy of the results reported. The large language models used as automated scoring instruments within the research pipeline — claude-opus-4-7 (Anthropic) and gpt-5 (OpenAI) — are described in the Methods section as research tools; their use as judge models within the methodology is distinct from the writing-assistance uses described here.

**Change log reference:** Item AI1 (new section, after Acknowledgements).

**Note on manuscript header:** The journal submission form "Use of AI" field should also be ticked "Yes" with the same disclosure text entered in the relevant field.
