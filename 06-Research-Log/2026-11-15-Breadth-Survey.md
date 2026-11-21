---
tags:
  - research-log
  - breadth
  - problem-discovery
  - methodology
---

# Session Log: 2026-11-15 — Breadth Survey and the Problem-Space Map

## Trigger
The user pointed out that the vault did not reflect the original brief. Correct diagnosis: 43 notes in, `02-Research-Areas` held one note, and every paper, opportunity, candidate and dataset was ADHD-EEG classification. The brief names BCI, epilepsy, autism, cognitive states, wearables, caregivers and clinicians, and explicitly says *do not force every idea into disease classification*. The vault had drifted into depth in one branch without surveying the tree.

This was not a content gap that more paper notes would fix. It was a **missing map**.

## What Was Produced
| Note | Role |
|---|---|
| [[Problem-Space-Map]] | Five axes (beneficiary, modality, AI lever, target, data); where the vault sits; which quadrants are empty; the well-posedness table; rules for placing new papers |
| [[Neurological-Conditions-Landscape]] | 12 conditions ranked by well-posedness, with datasets, saturation and verdicts |
| [[BCI-Paradigms-and-Applications]] | The paradigms, datasets, performance ranges, and six genuinely open problems |
| [[Multimodal-Physiological-Signals]] | Modalities, fusion strategies and failure modes, wearable form factors |
| [[Personalization-and-Domain-Adaptation]] | Method taxonomy, the calibration-budget axis, and the metrics that matter |
| [[Clinical-Deployment-and-Workflow]] | Beneficiary table, adoption metrics, regulatory realities, the under-served project space |
| [[Assumptions-Register]] | 12 explicit assumptions with kill conditions |

## The Three Findings That Changed the Picture

**1. The ADHD vault is one cell of a five-dimensional space.** Every row of the coverage table in [[Problem-Space-Map]] §3 is the same beneficiary (researcher), the same modality (scalp EEG), the same target (ADHD), and mostly the same lever (measurement). That is not a broad exploration; it is a narrow one done well.

**2. ADHD is the second-least well-posed target we have.** Effect size and label quality, not prevalence, decide solvability. Sleep, seizure and motor imagery have large signal-visible targets with near-zero label noise. ADHD's most famous biomarker has |d| ≲ 0.2 across 576 specifications. This does not invalidate the measurement work — measurement science belongs where the field's numbers are wrong — but it invalidates any assumption that ADHD is where the *signal* is.

**3. BCI is structurally easier than diagnosis, for a reason the vault had already measured.** In a BCI the label comes from the instruction, not a clinician's judgement; per-subject calibration is the design rather than a sin. And the alignment result the vault keeps trying to apply to ADHD (+14 points) was *measured on motor imagery*. The evidence has been sitting in the wrong application.

## Decisions Recorded
- [[Decision-Log]] commitment 19: the ADHD thread is one branch; no selection before the breadth survey is reviewed and at least one candidate from a different quadrant is evaluated on the same seven criteria.
- [[Decision-Log]] commitment 20: breadth is measured by columns, not rows.
- The "which quadrant?" question is now listed above "which candidate?" in the Decision Log's open questions, because all three candidates share a cell.

## What Was Deliberately Not Done
- **No new candidate was written.** Producing one in a single session would be exactly the "idea assembled to fill a slot" failure the brief warns against. The quadrants are documented; the candidates must come from a paper or a concrete design, not from a taxonomy.
- **No prior-art search.** Assumption A3 (decoding-multiverse novelty) remains unverified for the same reason as before — it needs a real search, not a guess.
- **No deletion of ADHD material.** It is the vault's genuine strength and it still supports three live candidates.

## Open Threads Created
1. Choose one empty quadrant and evaluate a concrete candidate there — BCI calibration/illiteracy, sleep staging under wearable constraints, and reliability-gated multimodal fusion are the three strongest openings.
2. Resolve A1 explicitly in writing: is this project measurement science on an ill-posed target, or a working system on a well-posed one? Everything downstream depends on the answer.
3. Test A4 (the aperiodic fingerprint) — still the cheapest decisive experiment in the vault.
4. ~~Resolve A2 (HBN access route)~~ — **done in the same session**, see §Post-Survey Verification.

## Post-Survey Verification: HBN Access (same session)
A2 was the one assumption a single fetch could kill, so it was tested rather than carried.

**Source:** the HBN-EEG platform documentation (Shirazi, UCSD SCCN), i.e. the authors of the dataset's own data paper — not a secondary summary.

**Confirmed:** 11 BIDS releases, 2,782 subject-records, ~1.9 TB total, anonymous S3 plus NEMAR, no DUA; six HED-annotated tasks with per-trial RT/accuracy in every release; four CBCL bifactors as anonymised scores; 20-subject 100 Hz mini sets per release; a separate `nm000103` release that is research-only, not for commercial use. Cite Shirazi et al., bioRxiv 2024 (DOI 10.1101/2024.10.03.615261).

**Corrected in the vault:** `ds005513` does not exist; "OpenNeuro `ds005505`–`ds005516`" implies twelve datasets when there are eleven; Release 1 has 136 subjects, not "180+"; the subject total is 2,782, not ">2,600"; eye-tracking and per-subject electrode locations are *future*, not present.

**What changed strategically:** the HBN thread went from *blocked on paperwork* to *argued feasible on paper*. That is a better position for a brainstorming vault, and it changes what can be written: both HBN candidates can now be discussed with a real access story instead of a caveat. It also surfaced a design constraint the vault had not recorded — whether a 1,000-subject specification curve is even affordable at ~1.9 TB, and whether a clinical diagnosis exists on the BIDS route at all.

**What it did not settle:** release overlap, per-task `n` by age band, and the BIDS-R11 vs Troendle-R11 numbering question. All three stay open as questions, not tasks.

## Connections
- [[00-Project-Overview]] · [[Reading-Queue]] · [[Assumptions-Register]] · [[Decision-Log]] · [[Healthy-Brain-Network-HBN]]
