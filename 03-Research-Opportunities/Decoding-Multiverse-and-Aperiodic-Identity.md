---
tags:
  - research-opportunity
  - adhd
  - eeg
  - multiverse
  - decoding
  - aperiodic
  - candidate
---

# Research Opportunity: A Multiverse of *Decoding* Performance + the Aperiodic Identity Fingerprint

**Status: candidate, not selected.** Derived from [[Troendle-2026-TBR-Multiverse-HBN]], fused with [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]] and [[Unsupervised-Alignment-Leverage]].

## 1. The Gap (one sentence)
Every multiverse analysis in this literature audits an **association**; nobody has audited **discrimination** — so the claim clinicians actually care about ("this test detects ADHD") has never been subjected to specification-curve analysis.

## 2. Why the Gap Is Real and Consequential
- The FDA-adjunct TBR device rests on Monastra's **86% sensitivity / 98% specificity** — a claim about classification.
- Troendle et al. rebut it with **regression coefficients** (group-mean differences), which is a different estimand. A null mean difference and a usable classifier are not logically equivalent; and conversely a "significant" mean difference is not a usable classifier. The literature has repeatedly confused the two (we logged this as [[Decision-Log]] commitment 13 and again in [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]).
- Every ADHD-EEG decoding paper in our vault reports one pipeline, one split, one AUC. We have no idea whether those AUCs are stable across defensible analytic choices — and the two pieces of evidence we do have (PSD pipeline losing 24 pp to a split change; Kim's two protocols reversing the winner) suggest they are not.

**The research question:** *How much of the reported ADHD-EEG decoding performance is a property of the brain, and how much is a property of the analyst?*

## 3. Study Design

### 3.1 Data
- **Primary: HBN** (public, Release 11+) — 1,122 analysable participants, subtyped, with SWAN severity. Proven usable by Troendle et al., whose preprocessing code is public (OSF u5yxv).
- **Replication: the 121-child IEEE DataPort cohort** — not as a headline, but as a *different-hardware* replication of the specification-curve shape (19ch/128 Hz vs 128ch/250 Hz).
- Optional third: ADHD-200 for a multi-site check.

### 3.2 Specification space (~80–160 universes, all cheap)
| Dimension | Levels |
|---|---|
| Spectral representation | uncorrected band power · SpecParam-adjusted power · aperiodic-only (χ, A) · log θ/β |
| Band policy | canonical · IAF-relative |
| Resting condition | eyes open · eyes closed |
| ROI | frontal · central · posterior · global |
| Alignment | none · Euclidean alignment (per-subject covariance whitening) |
| Classifier | logistic regression (L2) · shrinkage LDA · linear SVM |

*Deliberately no deep learning in the primary grid.* Linear models on static features are (a) the pipelines where the leakage gap is largest, (b) fast enough to run the whole multiverse thousands of times for permutation nulls, and (c) the honest baseline any deep model must beat ([[Decision-Log]] commitment 9).

### 3.3 Protocol inside **every** universe
- **Subject-disjoint** partitions only: leave-one-subject-out, or repeated stratified group 5-fold.
- All preprocessing, feature selection, and thresholding fit **inside** the training fold.
- **Participant-level** metrics only (aggregate epochs → one score per child).

### 3.4 Metrics per universe
Primary: **participant-level AUC**.
Secondary: balanced accuracy at matched 80% specificity; sensitivity at 90% specificity; **Brier score / ECE**; **PPV at 5% prevalence** (commitment 8).

### 3.5 Controls (this is where the project earns its keep)
1. **Permutation of the multiverse** — shuffle labels, re-run all universes, get the null distribution of the *maximum* and *median* AUC. Fixes the correlated-universe problem in [[Multiverse-and-Specification-Curve-Analysis]] §3.
2. **Age as a positive control.** Age is strongly decodable from EEG (IAF, 1/f geometry). If the pipeline cannot decode age, the pipeline is broken. If it can decode age but not ADHD, that is a meaningful, reportable result.
3. **Subject-identification probe** — predict participant ID from each representation (see §4).
4. **Artifact indices as a competing classifier** — see [[Class-Correlated-Artifact-Control]] §3.1.
5. **Label-noise ceiling** — estimate the Bayes-error floor from inter-rater diagnostic agreement in HBN (K-SADS has published reliability); report how far the best universe is from that ceiling.

## 4. The Mechanistic Core: the Aperiodic Identity Fingerprint
*(Our hypothesis, not established.)*

> The 21–24 pp subject-identity leak in PSD→SVM pipelines is carried largely by the **aperiodic exponent and offset**, not by oscillatory power.

Rationale: χ and A are stable within a person, variable across people, and shift every band power coherently — exactly the profile of a fingerprint. See [[Aperiodic-1f-Activity-and-Band-Ratios]] §4.

**Two cheap decisive tests:**
- **T1 (identity):** predict participant ID from just `(χ, A)`. If accuracy ≫ chance, the fingerprint exists.
- **T2 (leak decomposition):** on the same folds, compare subject-ID accuracy and ADHD AUC for four representations: {raw PSD, aperiodic-adjusted PSD} × {no alignment, EA}. If (i) aperiodic correction kills subject-ID accuracy and (ii) EA kills what remains, the leak is fully explained by two mechanisms and the paper has a clean three-line result.

This 2×2 is the single table that connects the leakage literature, the alignment literature, and the aperiodic literature. It is the most valuable experiment in the vault right now.

## 5. Expected Outcomes (all publishable)
| Outcome | Interpretation |
|---|---|
| AUC flat across universes, near chance | ADHD is not decodable from resting EEG at this sample size — a strong, useful negative, and the ceiling is now documented |
| AUC varies widely with analytic choice | The literature's spread is analyst-driven — specification curve becomes the field's calibration tool |
| A few universes reach 0.75+ | Identify *what they share*; then test whether that shared choice is a confound (usually it is) |
| Aperiodic-only features decode above chance | The "biomarker" is 1/f geometry — either E/I balance or movement. Both are interesting; the artifact battery decides which |
| Age decodes, ADHD does not | The pipeline works; the diagnostic signal is absent. Cleanest possible negative |

## 6. Novelty (honest)
- Multiverse/specification-curve analysis is established (Steegen 2016; Simonsohn 2020; Del Giudice & Gangestad 2021).
- EEG decoding is established. Subject-level evaluation is established. SpecParam is established.
- **Novel:** the *combination* — a specification-curve analysis of **decoding** rather than association, with subject-disjoint folds enforced inside every universe, aperiodic decomposition as a specification dimension, EA as a specification dimension, and a **permutation-of-the-multiverse null**. Plus the fingerprint test in §4.
- **What we must not claim:** a new biomarker, a new architecture, or SOTA. This is a measurement/audit contribution and must be defended as one (commitment 9).

## 7. Feasibility
- **Compute:** linear models on static features. 160 universes × 10-fold group CV × 1,000 permutations is a few GPU-free hours. Runs on the laptop.
- **Data:** HBN is public; the pipeline is published.
- **Timeline:** pipeline + feature extraction ~2 weeks; multiverse + nulls ~1 week; fingerprint experiment ~3 days; write-up ~3 weeks.
- **Dependencies:** HBN data access agreement; SpecParam (Python `specparam` package exists); a decision on how to handle the SWAN/severity dimensional analysis.

## 8. Risks and How to Kill It Early
| Risk | Early test | Kill criterion |
|---|---|---|
| All universes are near chance → boring flat line | Run 8 universes in week 1 on a 200-subject subset | If AUC ∈ [0.48, 0.55] in all 8, the "variation" story dies; pivot to the fingerprint test as the primary result |
| Subject-ID probe is near chance → no fingerprint | T1 on 100 subjects | If subject-ID accuracy ≈ chance from `(χ, A)`, the mechanism is wrong; pivot to alignment-only |
| Reviewers call it "just a null" | Pre-register the framework contribution | Need at least one positive claim: either the fingerprint, or the specification curve's explanatory power over the literature's spread |
| HBN preprocessing choices bake in artifacts | Re-run with Troendle's pipeline vs a minimal pipeline as a specification dimension | If conclusions flip on preprocessing, that is the finding — report it |
| Scope creep into deep models | Fixed: linear only in the primary grid | Adding a CNN is a separate, later paper |

## 9. Why This Is Now the Leading Candidate
It is the only direction in the vault that:
- uses a **public** cohort at scale (HBN, N = 1,122) instead of a saturated or private one;
- requires **no new architecture** (sidesteps the rejected direction);
- has a **published precedent for the method** and a **published precedent for the venue** (a rigorous null in a strong journal);
- converts the vault's seven-paper critique into one measurement;
- and has a **cheap falsifier** (§8, first row) that can be run before committing.

## 10. Connections
- Papers: [[Troendle-2026-TBR-Multiverse-HBN]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]
- Concepts: [[Multiverse-and-Specification-Curve-Analysis]], [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Opportunities: [[Class-Correlated-Artifact-Control]], [[Unsupervised-Alignment-Leverage]], [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]]
- Session log: [[2026-11-15-TBR-Multiverse-Analysis]]
