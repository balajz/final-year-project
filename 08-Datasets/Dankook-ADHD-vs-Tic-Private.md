---
tags:
  - dataset
  - adhd
  - tic-disorder
  - eeg
  - private
---

# Dankook University Hospital — ADHD vs Tic Disorder (private)

**Status: not accessible. Recorded for its design, not its data.**

## Identity
- **Source:** Dankook University Hospital, Cheonan, Republic of Korea. IRB **2020-06-013**.
- **Papers:** [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]] (only known user).
- **Why it matters anyway:** it is the only **differential-diagnosis** cohort in our vault — two symptomatic clinical groups, which matches the decision a child psychiatrist actually faces. Every other cohort we have is ADHD vs healthy.

## Acquisition
- 55 children/adolescents from a child-psychiatry outpatient clinic.
- **32-channel BioBrain-32 dry cap**, 250 Hz, International 10–20 layout. Eye movements monitored with extra electrodes. Noise-attenuated room.
- **12 min resting EEG:** EO–EC–EO–EC. Only the **second** EO and EC sessions used (6 min) — the first session is treated as unstable.
- 5 s epochs. Rejection >100 µV or <5 µV; participant dropped if >50% epochs rejected.
- Features: time series, Symlet wavelet (level 5), FFT.

## Composition
| Group | n (before) | n (after) | Sex | Age |
|---|---:|---:|---|---|
| ADHD | 34 | **21** | 24 M / 10 F (71% male) | 10.32 ± 2.34 |
| Tic disorder | 21 | **21** | 19 M / 2 F (90% male) | 9.76 ± 2.23 |

After balancing: **42 participants, 3,024 epochs.**

## Known Confounds
- **38% ADHD attrition vs 0% Tic** — and 55 × 72 = 3,960 vs 42 × 72 = 3,024 implies **zero epochs were actually rejected**, so the stated rule cannot explain the 13 exclusions. Either the accounting is wrong or the reasons are undisclosed ([[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]] critique 3).
- **Sex imbalance** 71% vs 90% male in a 2-class contrast.
- **Medication counts per group not reported.** "Some were on medication, discontinued 72 h prior." Tic patients are commonly on antipsychotics (aripiprazole / risperidone), which alter EEG.
- **Age differs** by 0.56 y; IQ matched.
- **Both classes are hyperactive** → class-correlated movement artifact is the central threat, and no artifact control was run.

## Status in Our Project
- **Adopt the formulation, discard the evidence.** ADHD vs Tic is the best problem statement in the vault; this dataset cannot support it.
- Action: search for a **public** differential-diagnosis cohort (ADHD vs ASD, ADHD vs tic/comorbid) or explicitly mark the framing as aspirational.
- Never cite its accuracy numbers as evidence for anything.

## Connections
- Papers: [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]
- Opportunities: [[Class-Correlated-Artifact-Control]]
- Concepts: [[Explanation-Stability-and-Faithfulness]], [[Subject-Level-Evaluation-Hygiene]]
