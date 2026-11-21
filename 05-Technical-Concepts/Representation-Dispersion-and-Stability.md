---
tags:
  - technical-concept
  - evaluation
  - representation-learning
  - reliability
---

# Representation Dispersion & Stability (Within-Subject Compactness)

Derived from the dispersion analysis in [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]].

## 1. The Quantity
For representation $z^{(\ell,r)}_{s,i}$ of window $i$ from participant $s$, stage $\ell$, repetition $r$:

$$\tilde{D}^{(\ell,r)}_s = \frac{\frac{1}{N_s}\sum_i \lVert z_{s,i} - \mu_s\rVert_2}{G^{(\ell,r)}}$$

where $G$ is the mean pairwise distance over all test windows. Averaging over seeds and comparing stages via Friedman + Wilcoxon + Holm gives a **normalized within-subject dispersion curve** across an architecture.

**What it is:** the stability with which a model re-embeds repeated windows from one child.
**What it is not:** biological neural variability, or a direct measure of "noise".

## 2. Why the Metric Is Attractive
- It captures a real failure mode: models that fingerprint *moments* rather than *persons* must be unstable across windows.
- It is architecture-agnostic, computed on held-out windows only, and cheap.
- Combined with a diagnostic-organization metric (silhouette, centroid-distance ratio) it forms a **two-axis quality space**: compactness within child vs separation across children. Neither alone is evidence of a good representation.

## 3. Confounds That Must Be Controlled (each is a plausible alternative explanation)
| Confound | Why it produces a false "improvement" | Matched control |
|---|---|---|
| **Temporal smoothing / bandwidth loss** | TE-from-pooled-conv features is a low-pass statistic; smooth features vary less within a child | Recompute dispersion for aggressively smoothed / Hilbert-enveloped **raw** EEG with matched bandwidth |
| **Shared window overlap** | 50% overlap means adjacent windows share samples; any temporally coarse feature inherits their correlation | Compare with non-overlapping windows, or report effective sample size |
| **Dimensionality / degrees of freedom** | Low intrinsic dimension compresses all distances | Random projection of raw EEG to the **same rank** as the stage; PCA-matched comparison (CTE-Net did 15/30/60 → partially mitigates) |
| **Per-stage standardization/PCA basis** | Fitting scaler + PCA separately per stage can rescale dispersion | PCA-free cosine analysis (CTE-Net did this → good) |
| **Global collapse** | A near-constant representation has ~zero dispersion | Normalization by $G$ (partially), plus **between-class** silhouette and centroid ratio (CTE-Net showed improvement, not collapse) |
| **Loss of within-subject temporal information** | Ignoring cognitive state changes also reduces dispersion | Report split-half reliability of *state-sensitive* features; check that event-related/behavioral contrasts survive |
| **Class-prior imbalance per subject** | Different label mixes shift centroids | Class-conditional dispersion; equalize window counts per participant |

## 4. Recommended Reporting Upgrade
Replace "dispersion reduced by X%" with a **reliability framing**:

1. **Split-half reliability** per participant (odd vs even windows) → Spearman–Brown corrected correlation, or ICC(2,1) on participant-level feature means.
2. **Signal-to-noise ratio** = between-subject variance / within-subject variance of the same feature (a repeated-measures ANOVA / ICC formulation).
3. **Permutation null**: randomly reassign windows to participants, recompute dispersion ratio, report where the observed value falls.
4. **Diagnostic organization** on the same axes (window silhouette, centroid silhouette, same/different ratio).
5. **Report all axes jointly** — compactness claims are only meaningful when separation and reliability move in the same direction.

## 5. Interpretation Guardrail
A representation that becomes more compact *and* more separable across classes, while retaining split-half reliability on state-sensitive features and surviving bandwidth-matched nulls, is a genuine improvement. Anything less is a **compression artifact** and should be described as such.

## 6. Connections
- Papers: [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]
- Concepts: [[Kernel-Matrix-Based-Transfer-Entropy]], [[Subject-Level-Evaluation-Hygiene]], [[Explanation-Stability-and-Faithfulness]]
- Opportunities: [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]], [[Class-Correlated-Artifact-Control]]

## 7. Note on the Third "Stability"
Three different quantities are called stability in the papers we have read, and they must not be conflated:
1. **Optimization stability** — variance across seeds on identical folds ([[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] reports ±0.0066 on 2 test subjects).
2. **Representation stability** — within-subject dispersion / split-half ICC (this note).
3. **Explanation stability** — agreement of attributions across folds ([[Explanation-Stability-and-Faithfulness]]).

Only (2) and (3) are properties of the learned mechanism; (1) is a property of the optimizer. A paper claiming "stability" should say which.
