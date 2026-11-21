---
tags:
  - research-log
  - adhd
  - leakage
  - evaluation
---

# Session Log: 2026-11-15 — Geethapriya & Pattabiraman Leakage Audit

## New Literature Added
- [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]] — six model families, two protocols, identical folds, same 121-child cohort as everything else we have read.

## The Result
| Feature type | Segment-wise | Subject-wise | Gap |
|---|---|---|---|
| PSD + SVM/RF | 86.3–90.0% | 65.1–65.6% | **−21 to −24 pp** |
| Raw EEG + CNN | 75.2% | 72.7% | −2.5 pp |

This is now the vault's **quantitative anchor for leakage**: we no longer need to argue the magnitude, only cite it. Added as a table to [[Subject-Level-Evaluation-Hygiene]].

## What It Adds Beyond the Existing Notes
1. **A mechanism, not just a warning.** Band power encodes stable subject traits (impedance, skull conductance, baseline spectral envelope). Those are exactly what per-subject covariance alignment removes → [[Unsupervised-Alignment-Leverage]] now has a causal story, and a cheap decisive test (align the 95-dim PSD pipeline; see how much of the 24-point gap returns).
2. **A prediction that cuts the other way.** Raw-signal CNNs lose only 2.5 pp, i.e. they are already fairly subject-agnostic. So the alignment gain should be **feature-dependent**, larger for PSD-style pipelines than for end-to-end models. That is a sharper claim than "alignment helps".
3. **Corroboration of the corpus.** 4,173 non-overlapping epochs and per-subject counts (ADHD 38.2 ± 5.4, control 30.7 ± 4.8) reconcile with CTE-Net's 8,213 50%-overlap windows. The two papers are describing the same data correctly.

## Where the Paper Fails Its Own Thesis
- **Threshold artifact.** CNN 72.7% vs SVM 65.6% is *not* better discrimination: AUC 0.72 vs 0.72 (DeLong p=0.90). The gap is recall 88.0/specificity 53.4 vs 68.0/62.5. Balanced accuracy 70.7 vs 65.3. This is now [[Decision-Log]] commitment 13.
- **No participant-level metric** on 121 held-out children — the one thing a leakage paper must report. Pooled epoch metrics also overweight ADHD (more epochs per child) *and* flatter a high-recall model.
- **Feature × model confound.** PSD/SVM vs raw/CNN, so "handcrafted features leak, deep learning doesn't" is not identified. Needs a 2×2 plus subject-identification probes.
- **Paired tests that are not paired.** Wilcoxon across folds of *different* partitions; DeLong on 4,173 correlated epochs. Both misstate uncertainty.
- **Seed stability again.** 5 seeds → 72.5 ± 0.5 while fold SD is 9.3 (CI 66.0–79.4 on 12-subject folds). Third independent instance of the same confusion.
- **SHAP without a null.** Channel-level |SHAP| averaged over time, no error bars, no permuted-label control, and a fronto-central pattern that a generic attention-task representation would also produce. Fp1/Fp2 not being top-4 weakens a blink explanation but does not establish group-specificity.
- **Missing the models that set the ceiling:** EEGNet/ShallowConvNet deferred; CTE-Net not cited; Baibulova's 0.777 LOSO not compared.

## Provenance Conflict Logged
Washout claim here vs "medication status unavailable" in [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]. Recorded in [[Decision-Log]] as an open item — resolve against IEEE DataPort primary documentation before citing either.

## Synthesis Across Five Papers
The vault now has a consistent story on this cohort:
- **0.74–0.79 AUC** is what honest, participant-level, leak-free evaluation yields (Baibulova, REVE, BrainWave, this paper after aggregation).
- **0.90 AUC** appears when preprocessing is minimal and/or windows are pooled (CTE-Net) — and CTE-Net's own cleaning experiment reproduces the drop.
- **Architecture is not the lever** (ShallowConvNet ties CTE-Net; CNN beats CNN–BiLSTM; CBraMod loses to a theta-envelope GRU).
- **The levers are** per-subject signal geometry (alignment), artifact/EMG band control, participant-level calibration, and honest partitions.

## Next Question
Does Euclidean alignment recover the PSD pipeline's 24-point leak? That single table would connect the leakage literature, the alignment literature, and this cohort — and it is cheap enough to run before choosing a final-year direction.
