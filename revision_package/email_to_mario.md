**To:** Mario  
**Subject:** EJVES revision package — ready for final manuscript edits and submission  
**Attachments:** 01_response_to_reviewers.docx, 02_change_log.docx, 03_revised_text_passages.docx, supplementary_table2_tripod_llm.docx

---

Dear Mario,

I am sending you the complete revision package for our EJVES manuscript (EJVES-S-26-00485). Everything needed for submission is in the four attached documents. Below is a summary of what has been done and a step-by-step list of what you need to do in the Word manuscript before submitting.

**What has been done**

We have addressed all three reviewers' comments. The major additions are:

1. **Comparator analysis.** We ran the same 16 question stems through GPT-5.5, Gemini 3.5 Flash, and Claude Sonnet 4.6 and scored them using the LLM judge pipeline (which you helped calibrate). You adjudicated the disputed accuracy cases — those results are now incorporated into the manuscript. The scoring code and outputs are publicly available on GitHub (https://github.com/vanalexgr/ejves-llm-judge).

2. **Table 2 correction.** During the revision, I re-ran the inter-rater reliability analysis against the original archived data and found a transcription error: the clarity (0.79) and comprehensiveness (0.86) ICC values in the submitted Table 2 were incorrect. The correct result at n = 4 topics is non-estimable for both domains. Accuracy (0.83; 95% CI 0.08–0.99) is unchanged and was transcribed correctly. The corrected Table 2 and updated Results/Discussion sentences are in `03_revised_text_passages.docx`. I have framed this proactively in the response letter — it actually strengthens the paper.

3. **Point-to-point response letter.** All reviewer comments are addressed in `01_response_to_reviewers.docx`. Please read through it; you may want to adjust the tone of one or two responses before submission.

4. **TRIPOD-LLM checklist** (Supplementary Table 2). Completed in `supplementary_table2_tripod_llm.docx`. Please check item **4a (Ethics)** and confirm the ethics statement matches what was approved for this study — the checklist currently says review was not required as no patient data were collected, but please verify this is accurate for your institution.

**What you need to do in the Word manuscript**

Open the original manuscript Word file and work through `03_revised_text_passages.docx` section by section. Every change is documented with the exact original text and exact replacement text, so it is straightforward copy-paste editing. The changes are:

1. **Abstract** — replace the Results and Conclusions sentences (lines 85–97) with the revised versions; includes the urgency correction and "serious patient-safety concern" phrase.

2. **"What This Paper Adds"** — one phrase replacement: "unacceptable risk" → "serious patient-safety concern".

3. **Methods, line 151** — add "with default prompt settings and no system-level customisation" after "(OpenAI)".

4. **Methods, lines 193–197** — delete the Italian text; replace with the clean English sentence (DISCERN Q7 description).

5. **Methods, lines 222–224** — add the appropriateness threshold justification sentence.

6. **Methods, line 137** — add "(Supplementary Table 2)" after "TRIPOD-LLM checklist".

7. **Methods — new subsection** — insert the "Comparator Analysis with Current-Generation Models" paragraph before the Statistical Analysis section.

8. **Methods, line 241** — add the exploratory framing sentence at the end of Statistical Analysis.

9. **Results, lines 251–254** — replace the inter-rater reliability sentences (Table 2 correction).

10. **Results, line 288** — add one sentence directing readers to Table 5 for domain-specific score distributions.

11. **Results — new paragraph** — insert the "Comparator Analysis" results paragraph before the Discussion.

12. **Discussion, lines 312–314** — replace the inter-rater reliability interpretation sentence.

13. **Discussion, lines 330–337** — replace the entire urgency paragraph with the expanded version (includes AAA examples and the comparator urgency improvement note).

14. **Discussion, after line 344** — add the readability context sentence.

15. **Discussion, after line 359** — insert the new comparator interpretation paragraph.

16. **Discussion, after line 372** — add the future directions sentence on patient education materials.

17. **Limitations** — replace the entire paragraph with the revised version.

18. **Conclusions** — add one sentence after "should not be used as standalone sources of patient information."

19. **Table 2** — replace with the corrected version (Accuracy: 0.83 [0.08–0.99]; Clarity: Not estimable*; Comprehensiveness: Not estimable*; with footnote).

20. **New Table 7** — insert the comparator results table (means with 95% CIs for all five validated domains plus descriptive comprehensiveness and clarity). Full table layout and all footnotes are in `03_revised_text_passages.docx`.

21. **Update the manuscript cover page** — change "Number of tables: 6; Supplementary tables: 1" to "Number of tables: 7; Supplementary tables: 2".

22. **After Acknowledgements — new section** — add the Generative AI Use Statement (text in `03_revised_text_passages.docx`, item AI1). This is mandatory per Elsevier policy.

**Supplementary materials to prepare**

- **Supplementary Table 1**: unchanged, resubmit as-is.
- **Supplementary Table 2**: the TRIPOD-LLM checklist (`supplementary_table2_tripod_llm.docx`). Please check item 4a (ethics) before submitting.

**When submitting via the journal portal**

- Upload the revised manuscript with track changes enabled (additions in blue, deletions struck through).
- Upload `01_response_to_reviewers.docx` as the point-to-point response letter.
- Upload Supplementary Table 2 (TRIPOD-LLM) as a new supplementary file.
- In the submission form, tick **"Yes"** in the AI use field and paste in the declaration text from `03_revised_text_passages.docx` (item AI1).

The change log (`02_change_log.docx`) is for your reference only — it documents every discrete edit with original and revised text, in case you want to double-check any individual change. You do not need to submit it.

Please let me know if anything is unclear. Thank you for handling the final manuscript and submission.

Best regards,  
Alex
