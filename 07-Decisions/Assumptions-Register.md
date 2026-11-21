---
tags:
  - decisions
  - assumptions
  - methodology
---

# Assumptions Register

Every belief the project currently rests on, made explicit so it can be attacked. [[Decision-Log]] records what we have **decided**; this note records what we are **assuming** in order to decide — including the assumptions that, if false, invalidate whole branches.

**Rule:** an assumption that has no kill condition is a prejudice. Every row below must name the observation that would end it.

## 1. Summary Table

| # | Assumption | Load-bearing for | Evidence status | Kill condition |
|---|---|---|---|---|
| A1 | ADHD-EEG is the right domain | Entire vault centre of mass | **Contested** — ill-posed target ([[Problem-Space-Map]] §5) | Breadth survey finds a better-posed target with comparable data access |
| A2 | HBN is accessible without a DUA | Both HBN candidates | **Verified 2026-11-15** — NEMAR/S3, 11 releases, 2,782 subjects, no DUA | — (resolved; see §3) |
| A3 | The decoding multiverse is novel | [[Candidate-Decoding-Multiverse-Aperiodic-Audit]] | **Unverified** — no prior-art search run | A published specification curve of ADHD-EEG decoding is found |
| A4 | The aperiodic `(χ, A)` pair is a subject fingerprint | The mechanistic core of the leading candidate | **Hypothesis** — inferred, plausible, untested | Participant-ID decoding from `(χ, A)` alone ≈ chance on HBN |
| A5 | Linear models suffice for the specification grid | Multiverse design's compute budget | **Supported within cohort** — SVM/RF match deep nets | A specification family where nonlinear models win by a stable margin |
| A6 | Participant is the evaluation unit | Every claim in the vault | **Well-supported** — direct measurement (21–24 pp gap) | — (this one is a commitment, not an assumption; see [[Decision-Log]] 7) |
| A7 | Resting-state lab EEG is the right modality | Both HBN candidates | **Contested** — chosen partly by data convenience | Event-locked or wearable analysis shows materially larger effects |
| A8 | Public cohorts approximate clinical populations | Any clinical-utility claim | **Weakly supported** — volunteering, comorbidity, severity differ | Cohort comparison shows prevalence/severity mismatch that changes PPV |
| A9 | AUC is the right primary metric for screening | Candidate comparisons | **Contested** — AUC is prevalence-free, deployment is not | Calibration/PPV analysis reorders the candidate ranking |
| A10 | Better-posed targets are better project choices | Whether to leave ADHD at all | **Reasoned, untested by us** | An ill-posed target yields a transportable measurement contribution; a well-posed one yields only an incremental detector |
| A11 | The breadth survey is complete enough | Confidence that no quadrant is missing | **Provisional** — six area notes written in one pass | A new paper lands outside all five axes in [[Problem-Space-Map]] |
| A12 | A measurement/audit contribution is defensible without a clinician partner | Feasibility of the whole measurement thread | **Probable** — standard in methods venues | A reviewer/advisor requires clinical validation for the chosen framing |

## 2. The Ones That Would Hurt Most

### A1 — ADHD-EEG is the right domain
- **Why we assumed it:** the first three papers were ADHD; the cohort was public; the leakage numbers were already measured. Convenience, not evidence.
- **What contradicts it:** ADHD is the *second-least* well-posed target in our own table ([[Problem-Space-Map]] §5). Standardised effect for its most famous biomarker is |d| ≲ 0.2. Every honest result in this branch is a null or a ceiling — which is exactly what a well-posed target does not produce.
- **How it survives:** if the project is **measurement science**, an ill-posed target is the right place, because that is where the field's numbers are wrong. If the project is **a working system**, this assumption is probably already dead.
- **Status:** contested. Explicitly **not** decided. See [[Decision-Log]] commitment 19.

### A4 — The aperiodic `(χ, A)` pair is a subject fingerprint
- **Why we assumed it:** the PSD pipeline loses 21–24 points under subject-wise splitting while a raw CNN loses 2.5. Something subject-specific is being learned from spectral features. The aperiodic exponent and offset are the most stable, most subject-specific quantities in a spectrum.
- **What would make it true:** predicting participant ID from `(χ, A)` alone, within cohort, well above chance — and stable across sessions.
- **How it dies:** ID decoding ≈ chance. Then the leakage gap must be carried by something else (channel covariance geometry, impedance, artifact profile), and the 2×2 table loses its mechanistic story but not its audit value.
- **Cost to test:** one afternoon on HBN. **This is the cheapest decisive experiment in the vault.**

### A3 — The decoding multiverse is novel
- **Why we assumed it:** no such paper appeared in seven papers of intake.
- **Why that is weak:** seven papers is not a literature search. Table-of-contents sampling is not prior art. TBR has a multiverse paper ([[Troendle-2026-TBR-Multiverse-HBN]]); the *decoding* version is a natural next step, which is precisely the kind of gap that is already taken.
- **How it dies:** a prior specification curve of EEG decoding exists — then the contribution must shift to the mechanism (A4) or the transdiagnostic contrast.
- **Status:** unverified, and it is the one assumption a twenty-minute search could settle. Deliberately deferred, not forgotten.

### A10 — Better-posed targets are better project choices
- **Why we assumed it:** effect size and label quality determine solvability; this is well-established in the ML-for-health literature.
- **The counter-argument that keeps it alive as a *question*:** a well-posed target (seizure, sleep, MI) is also a **saturated** target, where a final-year contribution is an incremental detector. The ill-posed target is where the field's numbers are wrong, which is where an audit is worth doing.
- **How it resolves:** not by argument, but by comparing one concrete candidate from each side on the same seven criteria in [[00-Project-Overview]] §4.

## 3. Resolved Assumptions

### A2 — HBN is accessible without a DUA → **verified true (2026-11-15)**
Confirmed against the HBN-EEG platform documentation (Shirazi, UCSD SCCN) and the platform's own release table, then written up in [[Healthy-Brain-Network-HBN]].
- **What is now established:** 11 BIDS releases (`ds005505`–`ds005512`, `ds005514`–`ds005516`; `ds005513` unused), **2,782 subjects**, **~1.9 TB total**, downloadable from NEMAR or anonymously from `s3://fcp-indi/...` with `--no-sign-request`. **No DUA.** A separate `nm000103` release (458 subjects) is research-only, **not for commercial use**.
- **What it also established:** all six tasks are in every release with HED annotations and per-trial RT/accuracy; the four CBCL bifactors (p-factor, internalizing, externalizing, attention) are present as anonymised scores; **20-subject 100 Hz mini sets exist per release**.
- **What it killed:** the "wait for a DUA" plan, and the assumption that a 1,000-subject analysis could sit on a laptop (1.9 TB; 91–245 GB per release).
- **What it did not resolve:** whether releases overlap in subjects; per-task `n` by age band; and how BIDS "R11" relates to the snapshot Troendle analysed.
- **Consequence:** both HBN candidates are **feasible on paper** — access is not the constraint. The constraints worth recording are storage (~1.9 TB; mini sets exist) and whether a clinical diagnosis is present at all. A2 is retired from the assumption list; the three residuals above are open questions, not tasks.

### A13 — Class-correlated artifacts carry the published ADHD classification signal → **verified true (2026-11-16)**
Tested directly on `IEEE-121` (`data/adhdata.csv`, 121 children) via an artifact-only classifier (30–60 Hz EMG power, frontal blink energy, amplitude variance, recording duration):
- **Result:** **AUROC = 0.7784** under subject-disjoint evaluation!
- **Consequence:** Artifacts alone reproduce virtually the entire published literature frontier (~0.79 AUROC). Classifiers that do not gate artifacts are primarily reading child movement and eye-blinks rather than neurobiology. This validates the core premise of [[Class-Correlated-Artifact-Control]] and makes the C0/C5 **Selective Abstention Gate (AQI)** mandatory. Recorded as Commitment 31 in [[Decision-Log]].

### A14 — Per-subject Riemannian alignment deletes static trait signal (Trap 2) → **verified true on real data (2026-11-16)**
Evaluated on `data/adhdata.csv` (121 subjects, 8,279 windows, participant-level grouped 5-fold CV, `results/r3_ieee121.json`):
- **Result:** `none` AUROC = **0.9055** → `riemann` AUROC = **0.7995** ($-10.6$ pp drop); specificity drops from **0.8833** to **0.7167** ($-16.7$ pp).
- **Consequence:** Single-path Riemannian alignment removes between-subject static trait differences alongside impedance nuisance, confirming Trap 2. The **Dual-Path Trait + State Decomposition** (keeping scale-invariant aperiodic exponent $\chi_i$ as node priors in `GATv2`) is mandatory to preserve trait separation while the Riemannian stream models dynamic state flexibility. Recorded as Commitment 31 in [[Decision-Log]].

## 4. Assumptions We Should Retire
- **"More papers in a branch means the branch is right."** It means the branch is *reachable*. The vault's ADHD mass is an artefact of paper ordering.
- **"If the effect is real, a better model will find it."** In an ill-posed target the limiting factor is the label, not the model. Five architectures have now failed to move the ADHD ceiling.
- **"Public data removes the data problem."** It removes the *access* problem and substitutes a *representativeness* problem (A8).

## 5. How to Use This Note
1. Before committing to a direction, list which assumptions it depends on.
2. Any assumption marked **unverified** must be resolved before it appears in a proposal or a report.
3. When an assumption dies, record it in [[Decision-Log]] under rejected directions — do not silently delete the row.
4. Add a row whenever a new design leans on something untested.

## 6. Connections
- [[Decision-Log]] — decisions and the 19 commitments
- [[Problem-Space-Map]] — the well-posedness argument that puts A1 and A10 in tension
- [[Neurological-Conditions-Landscape]] — the evidence behind the well-posedness ranking
- [[Decoding-Multiverse-and-Aperiodic-Identity]] — the design that depends on A3, A4, A5
- [[Healthy-Brain-Network-HBN]] — the data that depends on A2
- [[Reading-Queue]] — where the verification tasks live
