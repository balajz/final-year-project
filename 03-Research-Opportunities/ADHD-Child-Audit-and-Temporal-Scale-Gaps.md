---
tags:
  - research-opportunity
  - adhd
  - eeg
  - connectivity
  - auditing
  - transfer-entropy
---

# Research Opportunities: ADHD-Child Audit & Temporal-Scale Gaps

Derived from critical analysis of [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], cross-checked against [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] and [[Shen-2026-Brain4FMs-Benchmark]].

Context: on the same 121-child cohort, reported performance now spans 0.74 (Baibulova LOSO), 0.79 (REVE / BrainWave, Brain4FMs protocol — fixed LR = 1e-5, no EA, wide CI ±0.07), 0.90 (CTE-Net participant AUC) and 99% (leakage-inflated early papers). **The spread is the research question**, not the last decimal of accuracy. Note: 0.79 is the **current published frontier** under subject-disjoint evaluation, not a theoretical ceiling — the Brain4FMs protocol was deliberately conservative (see [[Decision-Log]] Commitment 28).

## 1. Artifact-Dependence Audit (highest value, cheapest)
- **Evidence:** CTE-Net with no preprocessing → 83.5% participant accuracy / 0.901 AUC. With band-pass + quality screening → **73.9% / 0.819**. Removing artifacts costs ~10 accuracy points. Reference choice almost completely rewrites the learned edges (Jaccard 0.067).
- **Independent corroboration:** [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] loses more balanced accuracy than any baseline when 30–75 Hz is filtered out (−2.9 on Mumtaz2016), a band dominated by EMG. Two different SOTA models, two datasets, same signature → artifact dependence is **systematic**.
- **Reading:** a substantial part of reported ADHD-Child performance is likely **broadband amplitude / ocular / drift structure**, not neural coupling. No paper on this cohort currently separates the two.
- **Decisive experiment:** an *artifact ladder* — (a) aggressive cleaning + ICA/EOG regression, (b) targeted counterfactual injection of blinks/EMG at controlled SNR, (c) frontal-only vs posterior-only vs artifact-channel-dropped input, (d) stratification of test participants by signal-quality index, (e) prediction of the quality index itself from the model's latent space. If performance survives (a) and does not track (d)/(e), the signal is neural; otherwise report the gap.
- **Why it matters:** clinicians and reviewers care far more about "how much of this is eyeblinks?" than about +1% AUC. This is an auditing contribution, not another classifier.

## 2. Temporal-Scale Mismatch in Directed TE
- **Evidence:** CTE-Net's TE lags are reported in **samples of a pooled signal whose effective rate is unpublished**; the swept range is $\tau\in[1,5]$, $\mu\in[0,10]$. Meanwhile theta (4–8 Hz, period 125–250 ms) carries almost all the discriminative connectivity in this cohort (Baibulova: theta AUC 0.733 vs beta 0.567), and CTE-Net's own TE ablation adds no significant participant-level accuracy over mean pooling — consistent with a TE module observing the wrong timescale.
- **Opportunity:** **band-resolved, millisecond-parameterized TE**. Estimate TE on analytic envelopes of theta/alpha/beta, parameterize lags in ms with a physiologically motivated grid, and optionally learn a lag *distribution* (soft-argmax over lag) instead of a single $\mu$. Report an explicit lag-recovery sanity check on a synthetic coupled oscillator where ground-truth direction and lag are known.
- **Mandatory caveat added 2026-11-15:** [[Troendle-2026-TBR-Multiverse-HBN]] shows that a theta-range power difference can be produced entirely by the aperiodic 1/f background shifting in slope, with no oscillatory change. Baibulova's theta dominance (AUC 0.733 vs beta 0.567) used canonical bands with no SpecParam correction, so **it may be a 1/f effect**. Any theta-based claim must be replicated on aperiodic-adjusted power before it is used. See [[Aperiodic-1f-Activity-and-Band-Ratios]].
- **Minimal decisive experiment:** same architecture, three variants — broadband TE (CTE-Net), theta-envelope TE, synthetic-lag-validated TE — evaluated under identical nested folds.

## 3. Reliability Metric Needs Bandwidth-Matched Nulls
- **Evidence:** the "−38.35% within-subject dispersion" headline can be produced by any temporally smoothed representation. CTE-Net's controls (PCA 15/30/60, cosine without PCA, global-distance normalization) address geometry but **not temporal bandwidth**.
- **Opportunity:** a small, reusable **representation-reliability harness**: split-half ICC, between/within-subject variance ratio, permutation null, and a bandwidth-matched smoothed-EEG baseline. Report compactness and class separation jointly.
- **See:** [[Representation-Dispersion-and-Stability]] for the full confound table.

## 4. Parsimony & Mechanism Ablations Missing From the Literature
- **Evidence:** ShallowConvNet — a 2017 architecture — matches or beats a 128K-parameter attention + Takens-embedding + kernel-entropy pipeline on 7 of 8 metrics. No paper on this cohort reports (a) learnable vs fixed TE, (b) Transformer vs cheap channel-mixing layer, (c) TE-only vs surrogate-connectivity features.
- **Opportunity/standard:** any claim that "differentiable connectivity helps" must beat a strong simple baseline **and** a fixed-TE variant under nested CV. Otherwise the contribution is interpretability, and must be defended as such.

## 5. Feature × Model Decomposition of the Leakage Gap
- **Evidence:** [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]] shows PSD features lose 21–24 accuracy points under subject-wise splits while a raw-EEG CNN loses 2.5. But the classical models saw PSD and the deep models saw raw EEG, so **feature type and model family are entangled**.
- **Opportunity:** a 2×2 design — {PSD, raw} × {linear/kernel, deep MLP/CNN} — on matched folds, plus a **subject-identification probe** (predict participant ID from each representation). That converts "leakage" from an inference into a measured property of a representation.
- **Why it matters:** it tells us *which* of our feature spaces are subject-fingerprints, which is the precondition for deciding whether alignment is the right fix.

## 6. Structural Consequence for Our Project
- The 121-child ADHD-Child cohort is **saturated** with architectural variants (2021–2026, including at least three from the CTE-Net/T-GARNet group). It should serve as a **benchmark and audit target**, not as the vehicle for a novel contribution.
- Novel work needs one of: external/multi-site data, event-locked or behavioral alignment ([[ADHD-Event-Locked-Connectivity-and-Leakage]]), personalization/calibration, or workflow-level tooling (quality auditing, abstention, uncertainty).

## 7. Connections
- Papers: [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Shen-2026-Brain4FMs-Benchmark]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]
- Concepts: [[Kernel-Matrix-Based-Transfer-Entropy]], [[Representation-Dispersion-and-Stability]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Related opportunities: [[ADHD-Event-Locked-Connectivity-and-Leakage]], [[BFM-Bottlenecks-and-Hybrid-Opportunities]], [[Unsupervised-Alignment-Leverage]]
- Session logs: [[2026-11-15-CTENet-Analysis]], [[2026-11-15-Geethapriya-Analysis]]
