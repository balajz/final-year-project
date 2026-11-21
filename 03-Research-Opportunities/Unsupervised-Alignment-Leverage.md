---
tags:
  - research-opportunity
  - cross-subject
  - domain-adaptation
  - alignment
  - calibration
---

# Research Opportunity: The Alignment Gap (Unsupervised Subject Alignment ≫ Pretraining Scale)

Derived from the OpenReview evidence in [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] and cross-checked against [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] / [[Shen-2026-Brain4FMs-Benchmark]].

## 1. The Observation
On BCIC-IV-2a (4-class MI, strict cross-subject), the same model improves by **~14 accuracy points** when given unsupervised per-subject alignment + augmentation, while the gap between a simple conv net and a 4.9M-parameter pretrained foundation model is **~2–3 points**:

| Condition | EEG-SimpleConv | CBraMod | Gap |
|---|---|---|---|
| Minimal preprocessing | 0.5650 | 0.5968 | +3.2 |
| + EA / mixup / subject-wise reg. | 0.7221 | 0.7405 | +1.8 |

**Interpretation:** the dominant cross-subject error term is a *per-subject signal-geometry shift* (covariance/reference/scale), not a lack of pretrained features. Pretraining is a second-order fix; alignment is a first-order fix.

### The mechanism (from [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]])
On the 121-child ADHD cohort, **static PSD features lose 21–24 accuracy points** when the split goes from segment-wise to subject-wise, while a raw-EEG CNN loses 2.5. The authors' explanation is the one that matters for us: band power encodes *stable subject traits* — electrode impedance, skull/scalp conductance, baseline spectral envelope. Those are exactly the quantities a per-subject covariance whitening removes.

Two consequences, one of them inconvenient:
- **Alignment should rescue feature-based pipelines** (PSD/SVM-style), where the identity shortcut is strongest.
- **End-to-end raw-signal models are already fairly subject-agnostic** (2.5 pp gap), so alignment may buy them much less. That predicts a *feature-dependent* alignment gain, which is a sharper and more publishable claim than "alignment helps".

### A useful consequence for our own designs
CTE-Net-style pipelines (per-window statistics → linear head) sit on the feature-based side of this divide, so their high scores should be read with the −20 pp prior in mind. Any model we build should be stress-tested by both partitionings and by a subject-identification probe on its features.

## 2. Why This Is Legitimate (and Why It Is Not Leakage)
Euclidean alignment (EA) whitens each subject's data by their **mean covariance over unlabeled windows of that subject**. No labels are used, so there is no label leakage — but it *is* transductive and requires a short unlabeled calibration/warm-up recording per subject. That assumption must be stated, and the minimum number of calibration windows must be measured (5 / 10 / 30 / all). Related: Riemannian alignment, re-centering, subject-wise normalization, test-time adaptation.

## 3. Why It Matters for ADHD Specifically
- ADHD-Child performance is **0.64** for CBraMod and ~0.79 for the best models under subject-disjoint splits (current published frontier — Commitment 28); the residual gap is dominated by between-subject covariance differences (skull thickness, electrode impedance, reference).
- Every ADHD-Child paper we have read **skips alignment entirely** and compensates with architecture.
- The vault's standing hypothesis — BFMs latch onto subject-specific spectral/amplitude signatures — predicts exactly this: alignment should recover far more than a bigger encoder.
- Alignment also targets the calibration collapse in [[BFM-Bottlenecks-and-Hybrid-Opportunities]] §2: subject-level logit shifts are the mechanism behind F1 = 0.00 on unseen subjects.

## 4. Decisive Experiments
1. **Decomposition:** on ADHD-Child, 2×2 = {no alignment, EA} × {simple conv / EEGNet-class model, pretrained encoder (CBraMod or REVE)}. Report participant-level AUC, balanced accuracy, **Brier/ECE**, and PPV at 5% prevalence.
2. **Calibration curve vs alignment windows:** performance and calibration as a function of calibration-set size (0, 5, 10, 30, 60 windows). This is the deployment-relevant curve, and nobody reports it.
3. **Artifact interaction:** does alignment still help after the artifact ladder of [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]]? If alignment's gain vanishes under aggressive cleaning (EOG regression, ICA), the "subject shift" was partly electrode/impedance artifact geometry, not neural scaling.
4. **Connectivity cost:** measure whether alignment destroys the subject-specific structure that interpretability claims rely on (top-10% edge Jaccard, per-subject TE maps). Report the trade-off explicitly — alignment may improve decoding *and* invalidate physiological interpretation.
5. **Feature-dependent gain (cheapest, most decisive):** apply EA to the 95-dim PSD pipeline of [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]] (65.6% subject-wise). If EA recovers a large share of the 24-point leakage gap, the "identity shortcut = subject covariance" mechanism is confirmed in one table. Then repeat on the raw-EEG CNN (72.7%) and compare the two gains.
6. **Subject-identification probe:** train a classifier to predict *participant ID* from features (raw, PSD, aligned PSD, TE vectors). Leakable representations should show high subject-identification accuracy; this turns "leakage" from an inference into a measurement.
7. **Artifact vs geometry, separated by the Kim result (new):** [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]] found that channel rankings from **raw** data are *more* concordant across folds than rankings from ICA-cleaned data. If stable raw-data structure is shared *across subjects*, then what alignment removes may be partly **recording geometry** (cap/reference/drift/line noise) rather than neural covariance. This sharpens experiment 3: alignment should be applied *after* the artifact ladder, and the ordering of cleaning vs alignment should be varied as a 2×2. A gain that disappears when alignment is applied after cleaning is geometry, not neurophysiology.
8. **Alignment vs aperiodic correction — which one removes identity? (new, highest value):** the `(1/f exponent, offset)` pair is a candidate subject fingerprint that EA may *not* remove, because whitening is spatial and the 1/f background is spectral. Run the 2×2 {no aperiodic correction, SpecParam-adjusted} × {no EA, EA} and report **two** outcomes per cell: participant-ID accuracy and ADHD AUC. If aperiodic correction accounts for most of the identity leak and EA accounts for a small residual, the leakage literature's mechanism is settled and the alignment literature's claim is bounded ([[Aperiodic-1f-Activity-and-Band-Ratios]] §4, [[Decoding-Multiverse-and-Aperiodic-Identity]] §4).

## 5. Novelty Assessment (honest)
- EA/Riemannian alignment is **well established in BCI** (Barachant et al.; Zanini et al.; EEG-SimpleConv's "key ingredients"). Applying it to ADHD EEG is a transfer, not a discovery.
- Defensible contribution = the **decomposition + audit**: quantifying how much of the ADHD-Child published frontier (~0.79 AUROC) is (i) subject geometry, (ii) artifact/EMG band, (iii) model capacity, and (iv) irreducible label noise — under nested CV, with calibration and an abstention curve.
- Weak version to avoid: "we applied EA and got +X%" → falls under the [[Decision-Log]] ban on trivial transfers.

## 6. Risks
- If alignment gains are small on ADHD-Child (unlike MI), the thread dies — but that is a publishable negative result about task dependence (MI is heavily covariance-driven; ADHD is diffuse/spectral).
- Transductive alignment at test time can be read as "peeking"; must be framed as **unsupervised adaptation with a calibration period**, and compared against a strict zero-shot baseline.
- The 121-child cohort is the wrong stage for a headline claim ([[Decision-Log]] dataset status) — this thread needs at least one external cohort to be taken seriously.

## 7. Connections
- Papers: [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]], [[Shen-2026-Brain4FMs-Benchmark]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]
- Opportunities: [[BFM-Bottlenecks-and-Hybrid-Opportunities]], [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]], [[ADHD-Event-Locked-Connectivity-and-Leakage]], [[Class-Correlated-Artifact-Control]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]], [[Explanation-Stability-and-Faithfulness]]
