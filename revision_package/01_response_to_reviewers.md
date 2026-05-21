# Response to Editors and Reviewers

**Manuscript:** EJVES-S-26-00485  
**Title:** Accuracy and Readability of Generative AI for Vascular Surgery Patients: A Specialist-based Evaluation Highlighting the Current Landscape of Safety Risks and Accessibility Gaps  
**Resubmission date:** [DATE]

---

We thank the Editors and all three Reviewers for their careful reading and constructive comments. All concerns have been addressed; the specific responses are provided below. We have also identified and corrected a transcription error in Table 2 discovered during revision (see "Additional correction" below), which we disclose proactively.

Changes in the revised manuscript are highlighted using track changes. Where text has been added, it appears in blue; where text has been removed, it is struck through.

---

## Additional Correction Identified During Revision

During the extension of this work for the comparator analysis, the inter-rater reliability analysis was independently re-run against the original archived data files. A transcription error was identified in Table 2 of the originally submitted manuscript. The ICC(2,k) values for **clarity** (submitted as 0.79) and **comprehensiveness** (submitted as 0.86) were incorrectly carried from the JASP output into the summary table. The correct values for both domains indicate non-estimable reliability at this sample size (n = 4 topics in the symptoms section): with negligible between-topic variance at this sample size, ICC(2,k) produced non-positive point estimates (floored to 0.00), which are not meaningfully interpretable. The accuracy ICC (0.83; 95% CI 0.08–0.99) was transcribed correctly and is unchanged.

**Table 2 has been corrected** and the corresponding sentences in the Results and Discussion have been updated accordingly (see Change Log, items C1–C3). No other table, figure, or analysis is affected: the descriptive statistics, correlation analyses, appropriateness results, and readability analyses all reproduce correctly against the original archived data.

This correction strengthens rather than weakens the manuscript's conclusions. The inability to estimate inter-rater reliability for clarity and comprehensiveness at this sample size is itself consistent with the exploratory framing that Reviewers 1 and 2 requested, and aligns with the calibration findings in the comparator methodology (where the LLM judge likewise showed insufficient reliability on those two domains — now interpretable as a consequence of absent stable human signal, not judge failure).

---

## Reviewer 1

### B1. Scope of conclusions

> *Conclusions regarding "generalist LLMs" are broader than supported by the data. The study evaluates GPT-3.5 only; conclusions should be limited accordingly or explicitly framed as applying to earlier-generation models.*

**Response:** We agree. The originally submitted manuscript referred to "generalist LLMs" in a way that implied breadth not supported by a single-model study. In the revised manuscript, initial conclusions are explicitly restricted to ChatGPT (gpt-3.5-turbo-0125). 

To directly address this limitation, we have conducted a pre-specified comparator analysis evaluating the same 16 question stems in three current-generation models: GPT-5.5, Gemini 3.5 Flash, and Claude Sonnet 4.6. These comparator results are now incorporated into the Methods, Results, and Discussion (see Change Log items R1a–R1d). This extension allows the revised conclusions to address generalist LLMs more broadly while grounding the original analysis explicitly in the GPT-3.5 context. The scoring pipeline, calibration outputs, blinded prompts, and final comparator dataset are publicly available at: https://github.com/vanalexgr/ejves-llm-judge

**Changes:** Items R1a (Methods, comparator arm subsection), R1b (Results, comparator results paragraph), R1c (Discussion, comparator integration), R1d (Conclusions, scope correction).

---

### B2. Model relevance

> *GPT-3.5 is no longer state-of-the-art. Please acknowledge this limitation clearly and discuss how newer models may differ.*

**Response:** We fully agree. The limitation is now explicitly stated in the Limitations paragraph (Change Log item R2), and the comparator analysis (see B1 above) directly evaluates three 2025/26-era models. The comparator findings show that communication-oriented domains (tone, complementarity, urgency calibration) have improved in newer models relative to the GPT-3.5 baseline, while accuracy limitations were not fully resolved, a finding that reinforces rather than undermines the paper's core message.

**Changes:** Item R2 (Limitations, GPT-3.5 model age sentence), R1a–R1d (comparator arm).

---

### B3. Sample size and representativeness

> *The use of 16 questions limits generalizability. Clarify how questions were selected and emphasize this as a key limitation.*

**Response:** Question selection is already described (lines 137–150: informed by Google Trends RSV data, expert consensus among three authors, four diseases, four question domains). A sentence has been added to the Limitations paragraph explicitly foregrounding the 16-question sample size as a key limitation (Change Log item R3).

**Changes:** Item R3 (Limitations).

---

### B4. Definition of clinical appropriateness

> *The requirement that all reviewers rate all domains ≥3 may underestimate clinically usable responses. Consider briefly justifying this threshold or discussing its impact.*

**Response:** A brief justification has been added to the Methods, Assessment of Clinical Appropriateness subsection (Change Log item R4). The strict threshold was chosen because, in a patient-safety context, any rating of 1 or 2 by any reviewer on accuracy, comprehensiveness, or clarity represents a specific clinical concern for that reviewer — and content that causes safety concern for any one expert is arguably clinically problematic regardless of others' ratings. We acknowledge this is a conservative approach that may underestimate the proportion of borderline-usable responses.

**Changes:** Item R4 (Methods, appropriateness threshold sentence).

---

### B5. Lack of comparator

> *There is no comparison with other patient information sources (e.g. online materials). A brief discussion would strengthen interpretation.*

**Response:** Rather than a comparison with external patient education materials (which would require a separate study), we have conducted a within-study comparator analysis evaluating three current-generation generalist models on the same question set (see B1 above). This comparator provides a clinically more relevant context — how has AI-generated vascular information evolved from GPT-3.5 to 2025/26 models — than a comparison with static online resources. A brief sentence acknowledging the absence of comparison with existing patient education materials and directing future work in this direction has been added to the Discussion (Change Log item R5).

**Changes:** Item R5 (Discussion, future directions sentence), R1a–R1d (comparator arm).

---

### B6. Interpretation of safety

> *Statements such as "unacceptable risk" should be moderated, as no patient-level outcomes were assessed.*

**Response:** Agreed. The phrase "unacceptable risk" has been replaced with "serious patient-safety concern" in two locations (abstract and "What This Paper Adds" section), which conveys the clinical significance of the findings without implying outcome-level evidence that was not collected (Change Log items R6a, R6b).

**Changes:** Items R6a (Abstract, line 97), R6b (What This Paper Adds, lines 48–50).

---

### B7. Readability context

> *Contextualize readability findings relative to existing patient education materials, which are often also above recommended levels.*

**Response:** A contextualising sentence has been added to the Readability Assessment section of the Discussion (Change Log item R7), acknowledging that while the 13th-grade reading level exceeds recommended thresholds, patient education materials at large are often above the 6th-grade standard, though this does not diminish the magnitude of the gap observed.

**Changes:** Item R7 (Discussion, readability paragraph).

---

### B8. Statistical interpretation

> *Given the small sample size, emphasise that analyses are exploratory.*

**Response:** The exploratory nature of the analyses was already noted in the Methods (line 241: "Correlation analyses were considered exploratory"). The corrected Table 2 (see Additional Correction above), which demonstrates non-estimable ICC for two of three subjective domains, now provides concrete evidence of the small-sample limitation that the reviewers asked to be foregrounded. A sentence has been added to the Statistical Analysis subsection (Change Log item R8) reinforcing the exploratory framing for all analyses.

**Changes:** Item R8 (Methods, Statistical Analysis).

---

### Minor points

- **Typographical errors:** Corrected throughout.
- **PAOD vs PAD:** Standardised to PAOD throughout, consistent with original systematic terminology.
- **Prompt settings:** Confirmed as default ChatGPT interface settings; this is now stated explicitly in the Methods (Change Log item Rm1).
- **Figure clarity:** Figures 2 and 3 have been reviewed and resubmitted.

---

## Reviewer 2

### Major concern 1: Italian text at lines 193–195

> *Lines 193-195 contain unedited Italian conversational text. This is entirely incompatible with peer-reviewed submission. The surrounding sentence is also incomplete.*

**Response:** We sincerely apologise for this error. An internal drafting annotation was inadvertently included in the submitted manuscript. The Italian text has been deleted and the DISCERN Q7 description has been completed in English (Change Log item R2-M1).

**Changes:** Item R2-M1 (Methods, lines 193–197, DISCERN Q7 description).

---

### Major concern 2: Abstract/Results inconsistency on urgency

> *The abstract states that no significant differences were found in tone, complementarity or urgency, but the Results section explicitly states urgency did differ significantly within symptom questions (p = 0.03, Table 4). The abstract must be corrected.*

**Response:** The Reviewer is correct. The original abstract statement was imprecise: urgency did not differ significantly when comparing symptom-type to treatment-type queries as aggregate groups (p = 0.07), but a significant difference in urgency was observed between sub-types of symptom questions (p = 0.03, Table 4). The abstract has been corrected to accurately reflect both findings (Change Log item R2-M2).

**Changes:** Item R2-M2 (Abstract, Results sentence on urgency).

---

### Major concern 3: Model version and generalisability

> *LLMs are rapidly evolving; the used model GPT-3.5 represents an outdated model. Conclusions should be exclusively applied to this model version.*

**Response:** Addressed under Reviewer 1, B1 and B2. Initial conclusions are now restricted to gpt-3.5-turbo-0125 and a comparator analysis of three current-generation models has been added.

---

### Major concern 4: Comparison with newer/other-company models

> *A comparison with other versions (and newer versions) from other companies would make sense (e.g. Claude) and would clearly benefit the overall conclusion.*

**Response:** The comparator analysis added in response to Reviewers 1 and 2 evaluates GPT-5.5, Gemini 3.5 Flash (Google), and Claude Sonnet 4.6 (Anthropic) on the same 16 question stems, directly fulfilling this request. See Change Log items R1a–R1d.

---

### Major concern 5: TRIPOD checklist

> *The authors stated they adhered to the TRIPOD Checklist. The Checklist should be added as a supplement.*

**Response:** The completed TRIPOD-LLM checklist has been prepared and is submitted as Supplementary Table 2.

---

### Minor concerns

- **Sample size as key limitation:** Acknowledged explicitly in the revised Limitations paragraph (Change Log item R3).

---

## Reviewer 3

### Revision 1: Acknowledging older ChatGPT version

> *Acknowledge that you evaluated an older ChatGPT version and discuss implications for rapidly evolving AI systems.*

**Response:** The original manuscript already specified "gpt-3.5-turbo-0125" in the Methods (line 79) and the Limitations paragraph (lines 374–376) noted that updated models could perform differently. The revised manuscript strengthens this acknowledgement with an explicit Limitations sentence (Change Log item R2) and, more substantively, with the comparator arm evaluating three current-generation models, which allows direct discussion of how performance has evolved (see B1 above).

---

### Revision 2: Granular analysis of urgency misalignment

> *Provide more granular analysis of urgency misalignment — this deserves expanded discussion with specific examples.*

**Response:** We have expanded the urgency discussion with specific response-level examples and a clinical interpretation of the two distinct failure modes — under-urgencing high-acuity conditions and over-urgencing stable enquiries (Change Log item R3-2). 

Briefly: questions about aortic aneurysm symptoms received a mean urgency score of 2.67 on the 0–4 Gilbert scale (between "urgent medical evaluation" and "non-urgent consultation"), despite the potential for these symptoms to indicate impending rupture. Conversely, natural history questions received higher urgency recommendations on average (mean 1.25 vs 2.33 for signs & symptoms questions, p = 0.03), meaning that a patient asking about long-term disease prognosis was more likely to receive an emergency referral prompt than a patient describing acute symptoms. Both failure modes carry clinical risk. The comparator analysis shows that urgency calibration improved modestly in GPT-5.5 (mean score 1.91 vs 2.10 for GPT-3.5), though systematic clinical vignette validation remains needed.

**Changes:** Item R3-2 (Discussion, urgency paragraph expansion).

---

### Revision 3: Binary appropriateness classification

> *Reconsider your binary "appropriateness" classification to capture more nuance in the data you've collected.*

**Response:** The binary appropriateness classification (requiring ≥3 across all three domains from all three reviewers) was a pre-specified primary derived endpoint, and we have retained it as such to preserve the original analysis structure. However, we acknowledge the reviewer's point. Table 5, which reports individual reviewer scores for each response and domain, already provides the continuous data underlying the binary classification and allows readers to assess granularity. A sentence directing readers to Table 5 for domain-specific score distributions has been added to the appropriateness results paragraph (Change Log item R3-3), alongside the threshold justification added in response to Reviewer 1 B4 (Change Log item R4).

**Changes:** Items R3-3 (Results, appropriateness paragraph), R4 (Methods, threshold justification).

---

---

## Additional Structural Additions

### New Table 7: Comparator Results

A new main Table 7 has been added presenting per-domain mean scores with 95% bootstrap confidence intervals for the three comparator models versus the GPT-3.5 benchmark. This table supports the new comparator Results paragraph (Change Log item R1b) and is directly cited in the Discussion (Change Log item R1c). The manuscript table count updates from 6 main + 1 supplementary to 7 main + 2 supplementary (the second supplementary table being the TRIPOD-LLM checklist, Supplementary Table 2).

### Generative AI Use Statement

In accordance with Elsevier policy on the declaration of AI use, a new section has been added after Acknowledgements (Change Log item AI1) disclosing: (1) the use of Claude Code (Anthropic) and Codex (OpenAI) for pipeline development and manuscript formatting assistance; and (2) the use of claude-opus-4-7 and gpt-5 as automated judge models within the research pipeline (the latter already described in the Methods). The statement clarifies that all scientific content, interpretations, and conclusions are the sole responsibility of the authors. No AI use statement was present in the original submission.

---

*We hope the revised manuscript satisfactorily addresses all reviewer concerns. We are grateful for the constructive and thorough peer review.*

---
