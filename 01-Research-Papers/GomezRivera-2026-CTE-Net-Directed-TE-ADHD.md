---
tags:
  - research-paper
  - adhd
  - eeg
  - connectivity
  - transfer-entropy
  - transformer
  - representation-learning
---

# Gomez-Rivera et al. (2026) — CTE-Net: Transformer-Contextualized Directed Transfer Entropy for Pediatric ADHD

- **Citation:** Gomez-Rivera, A., Pastrana-Cortés, J.D., Álvarez-Meza, A.M., Gil-Gonzalez, J., Cárdenas-Peña, D. (2026). *Sensors*, 26(18), 5786. [DOI: 10.3390/s26185786](https://doi.org/10.3390/s26185786)
- **Code repository:** **Not reported.** Public data but no code release → independent replication requires re-implementation.
- **Dataset:** IEEE DataPort "EEG data for ADHD/control children" (Nasrabadi et al., [DOI: 10.21227/rzfh-zn36](https://doi.org/10.21227/rzfh-zn36)). This is the **same 121-child cohort** used by [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] and the `ADHD-Child` task in [[Shen-2026-Brain4FMs-Benchmark]]. One ADHD child dropped at random → 60 ADHD / 60 control.

---

## 1. Core Problem & Formulation (Paper Findings)
- **Problem:** ADHD has no standalone neurophysiological marker; spectral markers (theta/beta ratio) generalize poorly. Connectivity markers are usually **linear and undirected** (coherence, envelope correlation) or **handcrafted and decoupled** from the classifier.
- **Second problem (the paper's real novelty):** EEG **within-subject variability**. Windows from the same child differ because of attention fluctuations and nonstationarity. A good representation should (a) preserve ADHD–control separation and (b) compress within-subject fluctuations.
- **Formulation:** End-to-end model predicting ADHD from a **342-dim vector of directed Transfer Entropy (TE) coefficients** (19×18 ordered pairs, self-connections removed). All information the classifier sees is TE.
- **Claimed contributions:** (i) Transformer + depthwise temporal filter + Takens embedding + differentiable kernel TE in one trainable pipeline; (ii) multi-stage analysis of within-subject representation dispersion; (iii) subject-independent protocol with ablations, paired tests, and case-level connectivity inspection.

## 2. Methodology
- **Cohort/task:** 120 children (7–12 y), 19 channels (10–20), $f_s = 128$ Hz, earlobe (A1/A2) reference, visual counting task (cartoon scenes, variable recording length). ADHD group had ≤6 months methylphenidate history; **medication status at acquisition unknown**.
- **Windowing:** 4 s / 512 samples, 50% overlap (2 s shift) → 8213 windows, median 64 per child (IQR 51.75–77).
- **Preprocessing:** deliberately **none** — no artifact rejection, no ICA, no band-pass, no band decomposition.
- **Architecture (128,578 params, ≈0.49 MiB FP32):**
  1. Token = one time sample of all 19 channels → linear projection to $d$ dims → $L$ Transformer blocks → project back to channel space $X_f \in \mathbb{R}^{C\times T}$. **No positional encoding** (intentional: attention is used as content-based global mixing, not temporal encoding).
  2. Channel-wise depthwise conv → ReLU → AvgPool → BN → $\Phi \in \mathbb{R}^{C\times T_\phi}$.
  3. Takens delay embedding of source past ($D_x$), target past ($D_y$), target present; trainable bias-free linear projections.
  4. Gram matrices with a **rational quadratic kernel** ($a=\ell=\alpha_{RQ}=1$); **matrix-based Rényi entropy** ($\alpha_R = 2$) with trace normalization; TE from the standard four-entropy decomposition.
  5. Head: `342 → dense → ReLU → dropout → logit` (sigmoid). Loss: BCE.
- **Selected TE hyperparameters:** $D_x=6$, $D_y=1$, $\tau=2$, $\mu=2$ (search: $D\in[1,10]$, $\tau\in[1,5]$, $\mu\in[0,10]$; 20 Optuna trials).
- **Protocol:** 5 fixed stratified **group** folds (24 held-out children each), 10 random training seeds → 50 models. One config chosen by **mean validation accuracy across the 5 folds**, then frozen. Window-level metrics = mean±SD over seeds. Participant-level = mean of per-seed metrics over the 120 out-of-fold children, 95% CI from 5000 **participant-level** stratified bootstrap; exact McNemar on seed-consensus decisions. Wilcoxon+Holm for seed-level. Friedman+Wilcoxon+Holm (+matched rank-biserial) for representation stages.
- **Baselines:** EEGNet, ShallowConvNet, T-GARNet, IMC-BGT, MultiStream — same folds, same 20-trial budget, same early stopping.

## 3. Reported Results
- **Window-level:** Acc **80.9 ± 1.7%**, Precision **82.7 ± 2.1%**, Sensitivity **84.2 ± 2.3%**.
- **Participant-level:** Acc **83.4%** (95% CI 78.2–88.2), ROC-AUC **90.2%** (85.1–94.6).
- **Comparisons — the honest part:** ShallowConvNet leads **7 of 8** metrics at both levels. Exact McNemar finds **no significant difference** vs EEGNet, ShallowConvNet, T-GARNet, IMC-BGT; only **MultiStream** is significantly beaten. At seed level only the precision gap vs ShallowConvNet survives Holm.
- **Ablation:** remove Transformer → largest drop, significant on all three metrics ($p_{\text{Holm}}=0.0117$) and at participant level. Replace TE with **temporal mean pooling** → drops, but seed-level significant only for accuracy ($p_{\text{Holm}}=0.0410$) and **no participant-level difference**.
- **Representation stages:** 30 PCs, standardized per stage-fold. TE stage gives best window silhouette, best centroid silhouette, lowest same/different centroid-distance ratio (Friedman $p\le3\times10^{-6}$; EEG vs TE $p_{\text{Holm}}=0.0117$).
- **Within-subject dispersion:** TE lowest; **median −38.35%** vs raw EEG, reduced in **76/120** children; Wilcoxon $p_{\text{Holm}}=1.09\times10^{-4}$; Friedman $\chi^2(3)=69.11$, $p=6.62\times10^{-15}$. Robust across PCA 15/30/60 and PCA-free cosine distance (median −37% to −45%).
- **TE stability:** coefficient range −0.0801 to 0.5156; **10.06% negative**; per-window vs participant-mean Spearman **0.743** (0.733–0.753); top-10% Jaccard **0.492** (0.474–0.509).
- **Robustness:** 358/8213 windows (4.36%) flagged post hoc; excluding them moves metrics ≤0.51 pp; flagged fraction uncorrelated with predicted probability ($\rho=0.062$, $p=0.503$). **But band-pass + quality screening drops participant accuracy 83.5% → 73.9% and AUC 90.1% → 81.9%.** Common average reference keeps accuracy but changes learned edges ($\rho=0.070$, Jaccard 0.067).
- **TE-parameter sensitivity:** 11 configurations, validation accuracy 81.63–89.78% (median 86.20%) — several alternatives beat the selected config.

## 4. Scientific Critique & Our Analysis
*(Our inference, not paper claims.)*

1. **The contribution is representational, not predictive.** By the authors' own ablation, the TE module adds no significant participant-level accuracy over mean pooling, and a stock 2017-era ShallowConvNet ties or beats the full pipeline. The defensible claim is "TE gives a compact, inspectable representation at no predictive cost" — not "TE improves ADHD classification". Credit: they state this openly rather than hiding it.
2. **Hyperparameter selection is not nested → residual optimism.** One configuration was chosen by averaging validation accuracy **across all five folds**. For fold $k$, that selection used labels from children who are test subjects in other folds (each child is validation in some fold and test in another). This is mild but real [[Nested-CV-and-Hyperparameter-Leakage]]. They acknowledge it and defer nested CV to future work.
3. **CIs are conditional on a single partition.** All 10 seeds reuse **identical** folds, so the bootstrap captures participant sampling but not partition/split variance. With $n=120$ and 24 test children per fold, the honest uncertainty around "83.4%" is wider than reported (cf. repeated/nested CV variance).
4. **Direction confounding inside the architecture.** The Transformer output is projected back to channel space, so every row of $X_f$ already contains information from **all** channels. TE is then estimated "from $c$ to $c'$" on signals that are individually all-channel mixtures. Directed asymmetry is therefore partly an artifact of the attention mixing, not evidence of directed information flow between electrodes. The paper's caveat ("learned representation space") does not name this specific circularity. **Consequence: the classifier's accuracy cannot be used as evidence that directed connectivity is the discriminative mechanism** — especially since the head sees *only* TE, so TE can act as a generic high-capacity window statistic.
5. **TE lags are reported in samples, not milliseconds, and the search space may be sub-theta.** $\tau\in[1,5]$, $\mu\in[0,10]$ in units of the **pooled** $\Phi$ time base, whose effective rate is never stated. If $\Phi$ runs at 128 Hz, the explored lags are 7.8–78 ms, i.e. **shorter than one theta cycle (125–250 ms)** — the band that dominates this dataset per [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]. If pooling by 8, $\mu=2$ is ~125 ms. Without the effective rate, the physiological meaning of the selected lag is unverifiable. Also $D_y=1$ makes this a **single-lag** predictive test, not multi-lag TE.
6. **"Dispersion reduction" is confounded with temporal smoothing / bandwidth loss.** TE features are built from depthwise conv + pooling + Takens embedding: an inherently low-pass, coarse statistic. Adjacent 4 s windows also share 50% of their samples. A smoother representation will show lower within-subject dispersion **by construction**, without being more "reliable" or more diagnostic. Their normalization by global mean pairwise distance and the improved silhouettes argue against *total* collapse, but the right control is **bandwidth- and DOF-matched**: e.g. heavily smoothed/enveloped raw EEG, random projections of matched rank, and a **split-half reliability (ICC)** framing. See [[Representation-Dispersion-and-Stability]].
7. **Preprocessing sensitivity is the biggest red flag in the paper.** Removing artifacts and band-limiting costs **10 accuracy points / 8 AUC points**. The most parsimonious explanation is that a meaningful share of the 0.90 AUC comes from **broadband amplitude and artifact structure** (blinks, drift, muscle), not from neural coupling. This also explains why 0.90 AUC sits ~11 points above the best foundation model (REVE, 0.79) and the theta-envelope dFC model (0.777) on the identical cohort. Their post hoc screen was too weak to settle this (no ICA, no EOG regression, no EMG).
8. **Interpretability claims are weakened by their own stability numbers.** Top-10% Jaccard of 0.49 means roughly half of the "strongest connections" change between a window and the participant mean, yet Figures 5–6 display the **top 5%** edges as subject-level findings. Reference choice (CAR vs earlobe) changes edge structure almost completely (Jaccard 0.067). Together: the connectivity maps are **not yet stable, reference-invariant objects**.
9. **Missing ablations that would isolate the claimed mechanism.** No comparison against (a) TE computed once on **raw, non-contextualized** signals and fed to the same head, (b) **fixed/untrained** TE features, (c) channel-shuffled or phase-randomized surrogates (direction null), (d) Transformer replaced by a cheap channel-mixing MLP/layer. Without (a)–(c) "differentiable TE" is not shown to beat "TE as fixed preprocessing", which is exactly the gap the paper claims to close.
10. **Scientific-value / saturation problem.** Architecturally this is TEKTE-Net (ref. [32], Takens-based kernel TE for motor imagery) + a Transformer front-end, applied to a dataset already carrying dozens of papers (including two by the same group: T-GARNet, and a temporal-attention/convolutional-tokenization paper). The 121-child cohort is **saturated**; incremental module recombination on it cannot establish generalizable neurophysiology.
11. **No calibration, no prevalence-aware operating point.** No Brier/reliability curve, no PPV/NPV at 5% prevalence, no decision-curve analysis, no abstention. For a screening claim this is the metric that matters (compare [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD|Baibulova]] PPV 0.138 at 10% prevalence).
12. **Estimator statistics under-reported.** TE per window is estimated from ~$O(10^2)$ **autocorrelated** Takens anchors inside 4 s; bias/variance of the matrix entropy estimator is never quantified, yet 10% of coefficients are negative and the parameter sweep spans 8 validation points. The TE numbers should be read as noisy features, not calibrated information-theoretic quantities.

### What is genuinely good and worth emulating
- **Two-level inference done correctly:** window-level = descriptive, participant-level = primary, seeds explicitly declared as *not* clinical observations.
- Bootstrap CIs with the **participant** as resampling unit, and the same resampled indices applied across seeds.
- **Negative results reported** (TE ablation not significant; no difference vs 4 baselines; cleaning destroys performance; reference changes edges).
- Component-wise ablation, parameter sensitivity, multiple-comparison correction, effect sizes.
- A **transferable idea**: analyzing *where* in the pipeline a representation becomes stable is more informative than one more accuracy point.

## 5. Connections
- Related Papers: [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Shen-2026-Brain4FMs-Benchmark]]
- Related Concepts: [[Kernel-Matrix-Based-Transfer-Entropy]], [[Representation-Dispersion-and-Stability]], [[Nested-CV-and-Hyperparameter-Leakage]], [[Subject-Level-Evaluation-Hygiene]], [[Dynamic-Functional-Connectivity]]
- Opportunities: [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]], [[ADHD-Event-Locked-Connectivity-and-Leakage]]
- Session log: [[2026-11-15-CTENet-Analysis]]
