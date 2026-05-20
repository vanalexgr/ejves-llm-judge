# Text Reconciliation Report

Source directory: `.`
Lengths and tails below use whitespace-normalized `response_text` values.

- Mismatched response_id values: 3
- Resolved response-text truncations via longest-version rule: 1
- Resolved question-phrasing variations via WD canonical question text: 2
- Remaining unresolved response mismatches: 0

No remaining mismatches after applying reconciliation rules.

## AAA_T1

- Question text mismatch: no
- Response text mismatch: yes
- Longest reviewer(s): WD
- Clean prefix truncation: yes
- WD canonical question text selected: n/a
- Status after reconciliation: resolved

| Reviewer | File | Length | Is longest | Prefix of longest |
|---|---|---:|---|---|
| MDO | `db (1)_Mario 12.08.xlsx` | 253 | no | yes |
| WD | `db wd.xlsx` | 439 | yes | same |
| EG | `db ai_rev eg.xlsx` | 260 | no | yes |

### Last 100 Characters By Reviewer

| MDO (253) | WD (439) | EG (260) |
|---|---|---|
| vidual health factors. Generally, the risk of rupture increases as the size of the aneurysm expands. | monitor AAA regularly through imaging tests and follow medical advice to manage the risk of rupture. | health factors. Generally, the risk of rupture increases as the size of the aneurysm expands. An AAA |

## PAOD_SS2

- Question text mismatch: yes
- Response text mismatch: no
- Longest reviewer(s): MDO, WD, EG
- Clean prefix truncation: n/a
- WD canonical question text selected: yes
- Status after reconciliation: resolved

| Reviewer | File | Length | Is longest | Prefix of longest |
|---|---|---:|---|---|
| MDO | `db (1)_Mario 12.08.xlsx` | 1773 | yes | same |
| WD | `db wd.xlsx` | 1773 | yes | same |
| EG | `db ai_rev eg.xlsx` | 1773 | yes | same |

### Last 100 Characters By Reviewer

| MDO (1773) | WD (1773) | EG (1773) |
|---|---|---|
| 1-3%, but this rate increases significantly in those with severe disease or additional risk factors. | 1-3%, but this rate increases significantly in those with severe disease or additional risk factors. | 1-3%, but this rate increases significantly in those with severe disease or additional risk factors. |

## PAOD_T1

- Question text mismatch: yes
- Response text mismatch: no
- Longest reviewer(s): MDO, WD, EG
- Clean prefix truncation: n/a
- WD canonical question text selected: yes
- Status after reconciliation: resolved

| Reviewer | File | Length | Is longest | Prefix of longest |
|---|---|---:|---|---|
| MDO | `db (1)_Mario 12.08.xlsx` | 2705 | yes | same |
| WD | `db wd.xlsx` | 2705 | yes | same |
| EG | `db ai_rev eg.xlsx` | 2705 | yes | same |

### Last 100 Characters By Reviewer

| MDO (2705) | WD (2705) | EG (2705) |
|---|---|---|
| o develop a personalized plan can help you manage symptoms and improve your overall vascular health. | o develop a personalized plan can help you manage symptoms and improve your overall vascular health. | o develop a personalized plan can help you manage symptoms and improve your overall vascular health. |

