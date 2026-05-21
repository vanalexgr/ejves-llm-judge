# Supplementary Table 2: TRIPOD-LLM Checklist

**Manuscript:** EJVES-S-26-00485  
**Title:** Accuracy and Readability of Generative AI for Vascular Surgery Patients: A Specialist-based Evaluation Highlighting the Current Landscape of Safety Risks and Accessibility Gaps  

**Checklist reference:** Omiye JA, Gui H, Rezaei SJ, et al. TRIPOD-LLM: a reporting guideline for studies using large language models. *Nature Medicine*. 2024. https://doi.org/10.1038/s41591-024-03425-5

**Study type:** Evaluation study of an existing off-the-shelf large language model (not development or fine-tuning). Primary analysis: ChatGPT (gpt-3.5-turbo-0125). Comparator arm: GPT-5.5, Gemini 3.5 Flash, Claude Sonnet 4.6.

---

| Item | Section | Checklist Item | Reported? | Location in Manuscript |
|------|---------|----------------|-----------|------------------------|
| **1a** | **Title** | Identify the study as involving a large language model and specify the clinical task. | Yes | Title: "Generative AI for Vascular Surgery Patients"; specifies patient information evaluation |
| **1b** | **Abstract** | Summarise the LLM(s) used, the clinical task, evaluation approach, key results and main limitations. | Yes | Abstract lines 80–97 (revised): states ChatGPT, vascular surgery patient information, specialist evaluation, readability and accuracy results; limitations addressed in abstract conclusions |
| **2a** | **Introduction** | Describe the clinical context, the gap in current knowledge or practice, and the rationale for using an LLM for this task. | Yes | Introduction lines 56–78: describes rise of LLMs in patient information, limitations of generic chatbots, vascular surgery information needs |
| **2b** | **Introduction** | State the study objectives, specifying whether the study involves development, fine-tuning, or evaluation of an LLM. | Yes | Introduction, final paragraph: objective stated as specialist-based evaluation of ChatGPT-generated responses; no development or fine-tuning involved |
| **3a** | **Methods — Data** | Describe how the input data (prompts or queries) were developed, including any curation, selection, or preprocessing steps. | Yes | Methods lines 137–150: 16 questions derived from Google Trends RSV data and expert consensus across 4 vascular diseases and 4 question domains; referenced in TRIPOD-LLM checklist note (revised Methods) |
| **3b** | **Methods — Setting** | Describe the intended population, clinical setting, and use case for which the LLM is being evaluated. | Yes | Methods and Introduction: intended users are vascular surgery patients seeking health information; consumer-facing ChatGPT interface |
| **3c** | **Methods — LLM specification** | Name and version the LLM(s) used; state training data cutoff date (if known), access date, interface or API used, and any configuration settings applied. | Yes | Methods line 151 (revised, Change Log item Rm1): gpt-3.5-turbo-0125; accessed February 28, 2026; publicly available ChatGPT interface; default prompt settings and no system-level customisation. Comparator models (Methods, Change Log item R1a): GPT-5.5, Gemini 3.5 Flash, Claude Sonnet 4.6; consumer interfaces; February 2026 |
| **3d** | **Methods — Outcome** | Define the outcome(s) or endpoints being assessed and describe any evaluation instruments, rubrics, or scoring scales used, including their derivation and operating range. | Yes | Methods lines 155–224: clinical accuracy (1–5 scale, adapted vascular surgery rubric); readability (Flesch Reading Ease, Flesch–Kincaid Grade Level); tone and complementarity (Gilbert scale); urgency of care (Gilbert scale 0–4); DISCERN Q7 (1–5 scale); appropriateness (binary, threshold ≥3 all domains all reviewers) |
| **3e** | **Methods — Evaluators** | Describe the human evaluators (number, expertise, independence), the rating procedure, and how inter-rater reliability was measured and reported. | Yes | Methods lines 196–224: three board-certified vascular surgeons; independent blinded rating; ICC(2,k) for subjective domains (Table 2, corrected in revision). Comparator arm: dual-surgeon blinded review with third-surgeon adjudication for ≥2-point disagreement (5 of 48 responses) |
| **3f** | **Methods — Prompt design** | Describe the exact prompts or prompt templates used (or reference where they are available), including any system prompts, chain-of-thought instructions, or few-shot examples. | Partial | Methods line 151 (revised): questions entered manually, default settings. Blinded judge prompts available at https://github.com/vanalexgr/ejves-llm-judge (outputs/phase2_prompts/). The 16 question stems are not reproduced verbatim in the main text; they are available at the repository. *Note: consider adding a supplementary table with the 16 question stems if word limit permits.* |
| **3g** | **Methods — Fine-tuning** | If fine-tuning, retrieval-augmented generation, or any training was applied to the LLM, describe the training data, fine-tuning method, and any regularisation or safety measures used. | N/A | Off-the-shelf commercial models used without modification; no fine-tuning, retrieval augmentation, or training was performed. Stated implicitly in Methods (publicly available interface, default settings). |
| **3h** | **Methods — Computational resources** | Describe the computational infrastructure used, including hardware, software, and estimated compute time if applicable. | Partial | Primary analysis: standard consumer interface (no specific compute required). Comparator arm LLM-as-judge pipeline: API calls to claude-opus-4-7 and gpt-5 (96 judge calls); code and pipeline available at GitHub repository. Exact hardware not described; not directly relevant to a consumer-interface evaluation study. |
| **4a** | **Ethics and open science** | Describe ethical approval, or provide justification for why ethics review was not required. State whether informed consent was obtained if human data were used. | Yes | No human participant data were collected; the study evaluated AI-generated text only. Expert reviewers were co-authors and consented to participation as members of the study team. Ethics review was not required (institutional exemption for AI evaluation studies not involving patient data). *[Authors: confirm and add explicit statement if not present in submitted manuscript.]* |
| **4b** | **Ethics and open science** | State the availability of prompts, code, model weights (if applicable), and data. Provide links or explain restrictions. | Yes | Methods/Data Availability (Change Log, item in revised text passages): scoring pipeline, calibration outputs, blinded prompts, and final comparator dataset publicly available at https://github.com/vanalexgr/ejves-llm-judge. Raw reviewer workbooks not distributed (confidentiality); processed consensus outputs sufficient for replication included in repository. |
| **5a** | **Results — Participants/data** | Report the number of queries/prompts evaluated, describe their characteristics, and report any selection or exclusion. | Yes | Results lines 245–254: 16 responses (4 diseases × 4 question domains) evaluated by 3 reviewers. Comparator arm: 48 responses (16 questions × 3 models). |
| **5b** | **Results — LLM performance** | Report all pre-specified performance metrics with appropriate measures of uncertainty (e.g., confidence intervals). Report human evaluation results separately from automated metrics. | Yes | Results: readability (FRE 32.3 ± 12.1; FKGL 13.5 ± 2); appropriateness 43.7% (7/16); individual domain scores in Tables 3–6; inter-rater reliability Table 2 (corrected). Comparator arm Table 7 (new): means with 95% bootstrap CIs for all validated endpoints. Human accuracy reported separately from LLM-judge domains. |
| **5c** | **Results — Model updates** | If any updates, prompt revisions, or iterations were made to the LLM during the study period, describe them and report performance before and after. | N/A | No updates were made to the LLMs during the study. The judge calibration process involved prompt revision for Track B accuracy anchors (see GitHub repository, calibration reports); however, the final accuracy endpoint was determined by human review, not the judge. |
| **6a** | **Discussion — Interpretation** | Discuss the results in the context of the clinical use case, including implications for patient safety, equity, and fairness across relevant subgroups. | Yes | Discussion: accuracy limitations and patient-safety implications (lines 305–359); urgency misalignment failure modes expanded (Change Log item R3-2); readability gap contextualized (Change Log item R7); comparator arm interpreted (Change Log item R1c) |
| **6b** | **Discussion — Limitations** | Discuss limitations of the data, LLM specification, evaluation approach, and generalisability, including potential for bias. | Yes | Limitations paragraph (fully revised, Change Log items R2, R3): sample size (n=16, primary limitation); restriction to gpt-3.5-turbo-0125 with comparator caveat on consumer-interface access; readability metric limitations; aggregated topic-level analysis; no patient-level outcomes assessed |

---

## Summary

| Section | Items | Fully reported | Partially reported | N/A |
|---------|-------|---------------|-------------------|-----|
| Title/Abstract | 1a, 1b | 2 | 0 | 0 |
| Introduction | 2a, 2b | 2 | 0 | 0 |
| Methods | 3a–3h | 5 | 2 | 1 |
| Ethics/Open Science | 4a, 4b | 2 | 0 | 0 |
| Results | 5a–5c | 2 | 0 | 1 |
| Discussion | 6a, 6b | 2 | 0 | 0 |
| **Total** | **19** | **15** | **2** | **2** |

**Partial items:**
- **3f (Prompt design):** Question stems not reproduced verbatim in the main text; available at GitHub repository. Authors may wish to add a supplementary table of the 16 question stems.
- **3h (Compute resources):** Consumer-interface study; not directly applicable. Judge pipeline compute documented at GitHub.

**N/A items:**
- **3g (Fine-tuning):** Off-the-shelf models used without modification.
- **5c (Model updates):** No in-study LLM updates; judge calibration iterations involved prompt revision but final accuracy endpoint was human-resolved.
