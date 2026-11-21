---
tags:
  - dataset
  - adhd
  - eeg
  - public
  - benchmark
---

# IEEE DataPort ADHD-Child (121 children)

**Status: demoted — benchmark and audit target only. Not a vehicle for a novel contribution.**

## Identity
- **Source:** Motie Nasrabadi et al., IEEE DataPort. [DOI: 10.21227/rzfh-zn36](https://doi.org/10.21227/rzfh-zn36).
- **Also known as:** `ADHD-Child` in the Brain4FMs benchmark ([[Shen-2026-Brain4FMs-Benchmark]]), the "ADHD-Child" cohort in [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]].

## Acquisition
- **121 children (61 ADHD / 60 control)**, 7–12 y.
- **19 channels**, 10–20 system, **128 Hz**, linked-earlobe (A1/A2) reference.
- **Paradigm:** structured **visual counting task** (cartoon scenes), NOT resting state. Variable recording length; 1,918,628 total samples.
- CTE-Net drops one ADHD child at random → 60 / 60.
- **Epoch counts:** 4,173 non-overlapping 4 s epochs (Geethapriya); 8,213 50%-overlap 2 s windows (CTE-Net).
- **Per-subject epochs:** ADHD 38.2 ± 5.4 vs control 30.7 ± 4.8 → pooled epoch metrics structurally overweight ADHD.

## Known Confounds
| Confound | Status |
|---|---|
| **Medication at acquisition** | **UNRESOLVED PROVENANCE CONFLICT** — [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]] says "appropriate clinical washout"; [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] says "unavailable". CTE-Net reports ≤6 months methylphenidate history. Resolve against IEEE DataPort primary documentation before citing either. |
| **No demographic linkage** | Age/sex/IQ not released per subject → no covariate adjustment, no stratification. |
| **No artifact annotations** | No ICA/EOG/motion markers, so artifacts cannot be regressed or audited directly. |
| **Unequal epochs per subject** | Requires participant-level aggregation before any claim ([[Subject-Level-Evaluation-Hygiene]]). |
| **Saturation** | Dozens of papers 2021–2026, including ≥3 from the CTE-Net/T-GARNet group alone. |

## The Numbers to Remember
- Current published frontier: **~0.79 AUROC** under subject-disjoint evaluation (REVE, Brain4FMs protocol; Baibulova LOSO 0.777; Geethapriya after subject-level aggregation). No method — specialist or foundation — has materially exceeded this figure. The contribution is therefore **calibration, artifact-awareness, and abstention, not discrimination**. See [[Decision-Log]] Commitment 28.
- **Why "frontier" not "ceiling":** Brain4FMs fixed LR = 1e-5 for all 15 models with no Euclidean Alignment — a suboptimal protocol that likely underestimates what a well-tuned REVE could achieve. The 0.79 ± 0.07 CI is wide; the split protocol (LOSO vs. single cross-subject split) is unconfirmed against ours. Using "ceiling" implies a well-characterised upper bound. It is not. Use "current published frontier" in all writing.
- **Artifact-only classifier (measured 2026-11-16):** **0.7784 AUROC** under subject-disjoint evaluation using only 30–60 Hz EMG power, frontal blink energy, amplitude variance, and duration. Artifacts alone explain virtually the entire published frontier (~0.79). Classifiers that do not gate artifacts are primarily detecting child movement and blinks. See [[Decision-Log]] Commitment 31 and [[09-Verification-Pending/V-03-R3-Alignment-Harness]].
- **Alignment ablation on this cohort (measured 2026-11-16):** `none` **0.9055**, `euclid` **0.8109**, `riemann` **0.7995**, `riemann_band` **0.7667**. Per-subject alignment deletes static trait differences (Trap 2 confirmed), mandating the dual-path trait/state architecture.
- Leakage gap, same folds, only the partition unit changed: **PSD/SVM −24.4 pp, PSD/RF −21.2 pp, raw CNN −2.5 pp**.
- CTE-Net cleaning experiment: **83.5% → 73.9%** accuracy when artifacts are removed.
- 93–99% figures in the 2021–2023 literature come from window-level splits.

## Status in Our Project
- **Use for:** the **engine benchmark** for the locked project — Base-Paper reproduction (Baseline 0), the 5-step ablation ladder, and the specificity/PPV rescue claim that is the graded headline of [[Candidate-C5-Reliability-Screening-Workbench]].
- **Also use for:** cheap falsifiers, leakage-mechanism replication, the artifact ladder, the aperiodic-identity 2×2 (it is the cohort where the leak is already measured).
- **Do not use for:** the primary *bio*logical claim, another architecture, any headline that requires clinical utility, or as a peer cohort alongside HBN (pooling is banned, Commitment 22).
- It is the right place to run the 8-universe pilot because the pipeline and the leakage numbers already exist.
- **Framing rule (Commitment 28, resolved 2026-11-16):** do **not** write "we beat the ceiling" or "our result approaches the ceiling". Write: *"no method has materially exceeded ~0.79 AUROC under subject-disjoint evaluation on this cohort; the contribution is calibration, artifact-awareness and abstention, not discrimination."* The word "ceiling" is retired — use "current published frontier". See [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] R1 (resolved).

## Connections
- Papers: [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Shen-2026-Brain4FMs-Benchmark]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Opportunities: [[Class-Correlated-Artifact-Control]], [[Decoding-Multiverse-and-Aperiodic-Identity]]
- Datasets: [[Healthy-Brain-Network-HBN]]
