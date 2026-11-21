---
tags:
  - research-log
  - triage
  - fmri
  - asd
  - kan
---

# Session Log: 2026-11-15 — Triage of Ward & Imran (2026) ABFR-KAN

- **Paper:** Ward, T., & Imran, A. (2026). *ABFR-KAN: Kolmogorov-Arnold Networks for Functional Brain Analysis*. MELBA 2026 / MIDL 2025 extension (`arXiv:2601.00416v2`, [DOI: 10.59275/j.melba.2026-cbeb](https://doi.org/10.59275/j.melba.2026-cbeb)).
- **Code:** [tbwa233/ABFR-KAN](https://github.com/tbwa233/ABFR-KAN)
- **Intake Scope:** Abstract + Section 1 (Introduction) only. Full methods/results not yet reviewed.

## Pass 0 Triage (per [[Paper-Triage-Checklist]])
- **Modality & Cohort:** Resting-state fMRI (rs-fMRI) on ABIDE I (281 subjects) and ABIDE II (211 subjects) for ASD vs. NC classification.
- **Core Idea:**
  1. **Atlas-free functional representation:** Randomly sample fixed grey-matter "anchor patches" shared across subjects, then sample multi-scale patches per subject and compute FC against those anchors—avoiding pre-defined anatomical atlas bias.
  2. **Architecture swap:** Replace standard MLP layers inside a Transformer with Kolmogorov–Arnold Networks (KANs, learnable spline activations on edges).
- **Verdict:** **Hold at Triage (do not promote to `01-Research-Papers` unless full Results/Ablations are inspected).**
  - Outside our primary modality (rs-fMRI vs. EEG) and outside our leading direction ([[Decoding-Multiverse-and-Aperiodic-Identity]]).
  - **Transferable concept:** Anchor-based / atlas-free FC representation parallels montage-agnostic spatial representations in EEG (e.g., REVE's 4D coordinates in [[Shen-2026-Brain4FMs-Benchmark]]).
  - **Red flags to verify if we read further:**
    1. *Subsetting of ABIDE:* ABIDE I has >1,100 subjects total, yet only 281 are used (and 211 in ABIDE II)—need to check exclusion criteria for differential attrition ([[Decision-Log]] commitment 16).
    2. *KAN vs. MLP fairness:* Spline-based KANs have different parameter counts and effective capacity than MLPs; need parameter-matched and hyperparameter-tuned MLP baselines.
    3. *Cross-site / motion confounds:* ABIDE is notorious for site effects and head-motion differences between ASD and controls ([[Class-Correlated-Artifact-Control]]).
