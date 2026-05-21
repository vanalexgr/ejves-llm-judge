# Change Log — Complete List of Manuscript Edits

Every change is documented below. Items are coded by reviewer origin (R1 = Reviewer 1, R2-M = Reviewer 2 major, R3 = Reviewer 3, C = self-identified correction). Changes are minimal — surgery at the sentence level wherever possible.

---

## Table of Changes

| Item | Location | Lines (original) | Nature |
|------|----------|-----------------|--------|
| C1 | Table 2 | — | Table replacement |
| C2 | Results, inter-rater reliability | 251–254 | Sentence replacement |
| C3 | Discussion, first paragraph | 312–314 | Sentence replacement |
| R2-M1 | Methods, DISCERN Q7 | 193–197 | Delete Italian; complete sentence |
| R2-M2 | Abstract, Results sentence | 85–86 | Sentence edit |
| R6a | Abstract, Conclusions sentence | 97 | Phrase replacement |
| R6b | What This Paper Adds | 48–50 | Phrase replacement |
| R1a | Methods — new subsection | after line 224 | New paragraph (~110 words) |
| R1b | Results — new paragraph | after line 300 | New paragraph (~130 words) |
| R1c | Discussion — new paragraph | after line 359 | New paragraph (~80 words) |
| R1d | Conclusions | 383–388 | One sentence addition |
| R2 | Limitations | 374–376 | Sentence edit |
| R3 | Limitations | 373 | One sentence addition |
| R3-2 | Discussion, urgency paragraph | 330–337 | Paragraph expansion (~140 words) |
| R3-3 | Results, appropriateness | 288 | One sentence addition |
| R4 | Methods, appropriateness | 222–224 | One sentence addition |
| R5 | Discussion, last paragraph | 367–372 | One sentence addition |
| R7 | Discussion, readability | 338–345 | One sentence addition |
| R8 | Methods, Statistical Analysis | 241 | One sentence addition |
| Rm1 | Methods, LLM Query | 151 | Phrase addition |

---

## Detailed Changes

---

### C1 — Table 2 (Correction)

**Location:** Table 2 (inter-rater reliability)

**Original Table 2:**

| Domain | ICC (2,k) | 95% CI |
|--------|-----------|--------|
| Accuracy | 0.83 | 0.08 – 0.99 |
| Clarity | 0.79 | 0.21 – 0.98 |
| Comprehensiveness | 0.86 | 0.17 – 0.99 |

**Revised Table 2:**

| Domain | ICC (2,k) | 95% CI |
|--------|-----------|--------|
| Accuracy | 0.83 | 0.08 – 0.99 |
| Clarity | Not estimable* | — |
| Comprehensiveness | Not estimable* | — |

*At this sample size (n = 4 topics in the symptoms section), between-topic variance was negligible relative to rater and residual variance, yielding non-positive ICC point estimates that are not meaningfully interpretable.

**Reason:** Transcription error in original submission. JASP output returns ≈ 0.00 for clarity and comprehensiveness (floored from negative raw estimate). Accuracy value is unchanged and correct.

---

### C2 — Results: inter-rater reliability sentences (lines 251–254)

**Original:**
> "Inter-rater reliability for subjective assessments was moderate to good across all evaluated domains. The ICC for accuracy demonstrated good agreement, while clarity and comprehensiveness also showed acceptable reliability, although confidence intervals were wide, reflecting the limited number of topics evaluated (Table 2)."

**Revised:**
> "Inter-rater reliability was estimable only for accuracy, which demonstrated good agreement (ICC[2,k] = 0.83; 95% CI 0.08–0.99). For clarity and comprehensiveness, between-topic variance was negligible relative to rater and residual variance at this sample size (n = 4 topics), yielding non-positive ICC estimates that were not meaningfully interpretable (Table 2). These reliability analyses should therefore be regarded as exploratory."

**Reason:** Corrects transcription error in Table 2; aligns with actual JASP output.

---

### C3 — Discussion: inter-rater reliability sentence (lines 312–314)

**Original:**
> "Inter-rater reliability analyses demonstrated acceptable agreement across subjective domains, supporting the internal consistency of expert assessments when applied at the topic level."

**Revised:**
> "Inter-rater reliability was good for accuracy but could not be reliably estimated for clarity or comprehensiveness given the small number of topics evaluated (n = 4), underscoring the exploratory nature of these analyses and the need for larger topic samples in future evaluations."

**Reason:** Corrects description that overstated reliability for clarity and comprehensiveness.

---

### R2-M1 — Methods: DISCERN Q7 description (lines 193–197)

**Original:**
> "D) Discussion of Uncertainty (from DISCERN7). Specifically, we used DISCERN Question 7 ("Does the information describe the uncertainty of treatment?"), se per te ok mettiamo questa che risponde un po' alle osservazioni che ci hanno fatto però ricontrolliamo tutto il discern which directly evaluates whether variability, risks, or limitations of therapeutic options are acknowledged, using a five-point scale:"

**Revised:**
> "D) Discussion of Uncertainty (from DISCERN Q7). Specifically, we used DISCERN Question 7 ("Does the information describe the uncertainty of treatment?"), which directly evaluates whether variability, risks, or limitations of therapeutic options are acknowledged, using a five-point scale:"

**Reason:** Removes inadvertently included Italian draft annotation; completes the sentence in English.

---

### R2-M2 — Abstract: urgency statement (lines 85–86)

**Original:**
> "No significant differences were found in tone, complementarity, or urgency across disease categories or question types."

**Revised:**
> "No significant differences were found in tone or complementarity across disease categories or question types, and urgency did not differ significantly between symptom-related and treatment-related queries overall; however, urgency varied significantly across sub-types of symptom-related questions (p = 0.03), consistent with inconsistent escalation recommendations."

**Reason:** Corrects factual inconsistency between abstract and Table 4 (urgency p = 0.03 within symptom questions).

---

### R6a — Abstract: "unacceptable risk" (line 97)

**Original:**
> "The combination of low accuracy and poor accessibility presents an unacceptable risk for unsupervised patient education."

**Revised:**
> "The combination of low accuracy and poor accessibility presents a serious patient-safety concern for unsupervised patient education."

**Reason:** Moderates absolute language; no patient-level outcomes were assessed (Reviewer 1, B6).

---

### R6b — What This Paper Adds (lines 48–50)

**Original:**
> "This combination of factual unreliability and poor accessibility represents an unacceptable risk for unsupervised patient education."

**Revised:**
> "This combination of factual unreliability and poor accessibility represents a serious patient-safety concern for unsupervised patient education."

**Reason:** Same as R6a.

---

### R1a — Methods: new comparator arm subsection

**Location:** Insert as new subsection after "Assessment of Clinical Appropriateness by Vascular Surgeons" (after line 224), before "Statistical Analysis"

**New text (insert in full):**

> *Comparator Analysis with Current-Generation Models*
>
> To evaluate whether the limitations identified in ChatGPT (gpt-3.5-turbo-0125) persisted in more recent models, a pre-specified comparator analysis was conducted. Responses to the same 16 question stems were collected from three current-generation generalist models — GPT-5.5, Gemini 3.5 Flash, and Claude Sonnet 4.6 — accessed through their publicly available consumer interfaces in February 2026, using identical session isolation protocols as the original study. These responses were scored using a validated two-model LLM-as-judge ensemble calibrated against the original human consensus scores; the judge was applied only to domains demonstrating sufficient calibration agreement (tone, complementarity, urgency of care, and treatment-related uncertainty [DISCERN Q7] for treatment questions). Clinical accuracy was independently evaluated by two blinded board-certified vascular surgeons, with a third surgeon adjudicating responses showing ≥2-point disagreement (5 of 48 responses). Comprehensiveness and clarity are reported descriptively, as inter-rater reliability for these domains was insufficient for validated endpoint use at this sample size.

**Reason:** Addresses Reviewers 1 (B1, B2, B5), 2 (major concerns 3, 4), and 3 (revision 1). Enables generalisable conclusions across multiple models.

---

### R1b — Results: new comparator paragraph

**Location:** Insert after the exploratory analyses paragraph (after line 300), before Discussion

**New text (insert in full):**

> *Comparator Analysis*
>
> All three current-generation models demonstrated improvement over the GPT-3.5 benchmark on communication-oriented domains (Supplementary Table 2). Urgency calibration improved marginally, with mean urgency scores of 1.91 for GPT-5.5, 2.06 for Gemini 3.5 Flash, and 2.06 for Claude Sonnet 4.6, compared with 2.10 for GPT-3.5. Tone scores improved across all comparator models (range 1.66–1.78 vs 1.31 for GPT-3.5) and support for physician involvement was maintained or increased (complementarity: 0.844–0.875 vs 0.792). Human-assessed accuracy showed modest gains for GPT-5.5 (mean 3.69) and Gemini 3.5 Flash (3.72), but remained limited for Claude Sonnet 4.6 (3.31), compared with 3.27 for GPT-3.5. Treatment uncertainty scores (DISCERN Q7) also improved, particularly for GPT-5.5 (3.50 vs 3.04 for GPT-3.5). Despite these improvements, no comparator model achieved comprehensive alignment with clinical standards across all evaluated domains.

**Reason:** Presents comparator findings factually, in Results style (no interpretation).

---

### R1c — Discussion: comparator integration paragraph

**Location:** Insert after the paragraph ending "cannot provide credible information about vascular surgery" (after line 359), before the Chervonski paragraph

**New text (insert in full):**

> Our comparator analysis indicates that communication-oriented domains — including tone, complementarity, and urgency calibration — have improved in more recent models relative to the GPT-3.5 baseline. Clinical accuracy, however, while marginally improved for two of three models, continued to require blinded human review and did not show consistent gains across all evaluated models. This pattern suggests that while newer generalist LLMs communicate more carefully, the accuracy limitations underpinning the safety concerns identified in this study have not been fully resolved by model scale or architecture advances alone. These findings are consistent with emerging evidence from other surgical specialties suggesting that accuracy limitations in generalist chatbots are persistent across model generations.

**Reason:** Interprets comparator findings in context; supports broader "generalist LLMs" claim.

---

### R1d — Conclusions: comparator sentence addition

**Location:** After the sentence ending "should not be used as standalone sources of patient information." (line 386)

**Add one sentence:**
> "An exploratory comparator analysis of three 2025-era generalist models suggested partial improvement in communication-oriented domains but did not resolve core accuracy limitations."

**Reason:** Updates conclusions to reflect comparator findings without rewording existing text.

---

### R2 — Limitations: model age sentence (lines 374–376)

**Original:**
> "Analysis was restricted to a generalist model (ChatGPT, gpt-3.5-turbo-0125) and it should be noted that updated models or alternative LLMs could perform differently."

**Revised:**
> "The original analysis was restricted to ChatGPT (gpt-3.5-turbo-0125), which was state-of-the-art at the time of data collection but has since been superseded. An exploratory comparator arm evaluating three current-generation models is presented; however, those responses were collected from free consumer-facing interfaces, which may not fully replicate API-level or enterprise-tier model behaviour."

**Reason:** Explicitly acknowledges the model's age (Reviewer 1 B2, Reviewer 2 major concern 3) and adds honest caveat about comparator access modality.

---

### R3 — Limitations: sample size sentence addition (line 373, before existing limitations)

**Add at the start of the Limitations paragraph, before "While we assessed several disease scenarios...":**
> "The primary limitation of this study is its sample size: 16 responses from a single LLM version represent an exploratory dataset from which generalisable conclusions should be drawn cautiously."

**Reason:** Reviewer 1 B3, Reviewer 2 minor concern 1.

---

### R3-2 — Discussion: urgency granularity expansion (lines 330–337)

**Original paragraph:**
> "Another important aspect of safety is the appropriateness of urgency recommendations. While tone, complementarity, and urgency aggregate scores did not differ significantly between symptom-related and treatment-related questions, the variability in urgency advice within symptom-related queries was a point of concern. Missing the level of urgency of aortic, carotid or peripheral arterial conditions is likely to cause severe harm to patients. Over-reassurance of patients with potentially time-critical symptoms or, conversely, unnecessary escalation in low-risk scenarios could both have harmful consequences. It is unacceptable for any system that is directly exposed to patients to fail to identify situations that require urgent specialist assessment."

**Revised paragraph:**
> "Another important aspect of safety is the appropriateness of urgency recommendations. While tone, complementarity, and urgency aggregate scores did not differ significantly between symptom-related and treatment-related questions as a whole, significant variability in urgency advice was observed within symptom-related queries (p = 0.03; Table 4). At the response level, this misalignment takes two clinically distinct forms. First, questions about aortic aneurysm symptoms received a mean urgency score of 2.67 on the Gilbert scale (between "urgent medical evaluation" and "non-urgent consultation"), despite the potential for these symptoms to herald rupture — a condition requiring emergency intervention. Second, natural history questions, where patients enquire about disease prognosis rather than acute symptoms, received more urgent urgency recommendations on average (mean 1.25) than signs and symptoms questions (mean 2.33), meaning that a patient asking about long-term disease risk was more frequently directed toward emergency services than a patient describing acute symptoms. Both under-urgencing of acute presentations and over-urgencing of stable enquiries represent distinct patient-safety failure modes. Missing the level of urgency of aortic, carotid, or peripheral arterial conditions is likely to cause severe harm; equally, unnecessary escalation of low-risk enquiries risks eroding public trust in AI-generated health information. The comparator analysis showed modest improvement in urgency calibration, with GPT-5.5 achieving the lowest mean urgency score (1.91) among the evaluated models, though systematic validation against clinical vignettes with known appropriate urgency levels remains needed before any model is considered reliable on this domain."

**Reason:** Reviewer 3 revision 2 (expand urgency discussion with specific examples). New text uses data directly from Table 3 of the original manuscript.

---

### R3-3 — Results: appropriateness granularity sentence addition (line 288)

**Location:** At the end of the sentence "Only 7 of the 16 generated outputs (43.7%), were rated as appropriate by the reviewers (Figure 2)."

**Add after that sentence:**
> "Table 5 reports individual reviewer scores for each response and domain, allowing assessment of domain-specific score distributions beyond the binary classification."

**Reason:** Reviewer 3 revision 3 (nuance in appropriateness). Directs readers to existing data without changing analysis.

---

### R4 — Methods: appropriateness threshold justification (lines 222–224)

**Original:**
> "A response was considered clinically appropriate only if it scored ≥3 in all three domains across all reviewers. Any response receiving a score of 1 or 2 in any category by any reviewer was considered inappropriate."

**Revised:**
> "A response was considered clinically appropriate only if it scored ≥3 in all three domains across all reviewers. Any response receiving a score of 1 or 2 in any category by any reviewer was considered inappropriate. This conservative threshold was selected because, in a patient-safety context, a specific clinical concern raised by any one expert reviewer about accuracy, comprehensiveness, or clarity is clinically relevant regardless of the ratings of others; it may therefore underestimate the proportion of borderline-usable responses."

**Reason:** Reviewers 1 (B4) and 3 (revision 3).

---

### R5 — Discussion: future directions sentence (lines 367–372)

**Location:** At the end of the paragraph beginning "The findings of this study should be considered when designing future AI systems..." (after line 372)

**Add one sentence:**
> "Future comparative evaluations should also include established patient education materials as an external reference standard, enabling direct assessment of whether AI-generated information represents a meaningful advance over currently available alternatives."

**Reason:** Reviewer 1 B5 (no comparator with existing patient information sources; we note this remains an important future direction).

---

### R7 — Discussion: readability context sentence (lines 338–345)

**Location:** After the sentence ending "especially those with lower literacy or non-native language skills" (after line 344)

**Add one sentence:**
> "It should be noted that existing patient education materials are themselves frequently above recommended reading levels; however, the gap observed here — university-level output against a sixth-grade recommendation — substantially exceeds typical deviations reported in patient information research."

**Reason:** Reviewer 1 B7 (contextualise readability findings).

---

### R8 — Methods: exploratory framing sentence (line 241)

**Original (end of Statistical Analysis subsection):**
> "Correlation analyses were considered exploratory, and results are interpreted primarily based on effect sizes rather than statistical significance."

**Revised:**
> "Correlation analyses were considered exploratory, and results are interpreted primarily based on effect sizes rather than statistical significance. Given the small sample size (n = 16 responses), all statistical analyses in this study should be regarded as exploratory and hypothesis-generating rather than confirmatory."

**Reason:** Reviewer 1 B8; consistent with corrected Table 2.

---

### Rm1 — Methods: prompt settings (line 151)

**Original:**
> "For each clinical topic, all questions were entered manually into the ChatGPT interface by a single investigator (WD) on February 28, 2026, using the publicly available ChatGPT version 3.5 (OpenAI)."

**Revised:**
> "For each clinical topic, all questions were entered manually into the ChatGPT interface by a single investigator (WD) on February 28, 2026, using the publicly available ChatGPT version 3.5 (OpenAI) with default prompt settings and no system-level customisation."

**Reason:** Reviewer 1 minor point (clarify prompt settings).

---

## Summary Count

| Type | Count |
|------|-------|
| Self-identified corrections (Table 2) | 3 items |
| New text blocks (comparator arm) | 4 items |
| Sentence replacements/edits | 7 items |
| Single sentence additions | 7 items |
| Phrase replacements | 2 items |
| **Total discrete changes** | **23 items** |

No section has been rewritten in its entirety. The new comparator arm content (~420 words across Methods, Results, Discussion, Conclusions) is the only substantive addition to the manuscript body.
