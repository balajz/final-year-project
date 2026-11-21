---
tags:
  - research-paper
  - adhd
  - tic-disorder
  - eeg
  - gcn
  - xai
  - noise-robustness
---

# Kim et al. (2025) — Noise-Robust GCN for ADHD vs Tic Disorder

- **Citation:** Kim, D., Lee, Y., Shin, S., Kim, K.M., Kim, D., Choi, S.-I. *Noise-robust and Interpretable EEG Classification of Hyperactive Disorders Using Graph Convolutional Network.* IEEE Access, 2025. [DOI: 10.1109/ACCESS.2025.3626160](https://doi.org/10.1109/ACCESS.2025.3626160)
- **Code:** none reported.
- **Dataset:** **private** — Dankook University Hospital, Korea. 55 children/adolescents (34 ADHD, 21 Tic disorder), 32 channels, 250 Hz, resting state (EO–EC–EO–EC, second EO+EC used = 6 min), 5 s epochs. After attrition: **42 (21/21)**, 3,024 epochs. IRB 2020-06-013. *Not publicly available → not usable as our primary dataset.*

---

## 1. Core Problem (Paper) — and the best framing in our vault
Most EEG-ADHD work is **disease vs healthy**, which is not the decision a clinician faces. This paper classifies **ADHD vs Tic disorder** — two hyperactive conditions that are genuinely confusable in child psychiatry. That is the right kind of question, and it is the reason this paper is worth reading despite its execution.

Three claims:
1. **Noise robustness** — GCNs survive without artifact removal, because neighborhood aggregation dilutes single-channel noise.
2. **Interpretability** — PGExplainer on the channel graph yields stable important channels, and they are the *same* with and without denoising.
3. **Efficiency** — use those rankings to prune channels and find a "maximally efficient model."

## 2. Methods
- Raw condition: band-pass + 60 Hz notch only. Denoised condition: ICA + ADJUST (+ manual). **Paired design — the right instinct.**
- Epochs: 5 s; reject >100 µV or <5 µV; drop participant if >50% epochs rejected; then balance classes to 21/21.
- Features: time series, Symlet wavelet (level 5), FFT.
- Models: MLP, 1D-CNN, GCN (GraphSAGE, max-pool aggregator), GAT, LMDA, EEGNet — 6 models × 3 features × 2 noise conditions = 36 cells.
- CV: "leave-one-pair-out", actually **7-fold group CV with 3 ADHD + 3 Tic per fold** (21 = 3×7).
- **Two training protocols:** (a) fixed **100 epochs**, no early stopping — justified as needed for consistent PGExplainer models; (b) early stopping, reporting **max accuracy over epochs**.
- Explanations: PGExplainer edge masks → three node-ranking algorithms (incremental-growing / iterative-pruning / cumulative-scoring); stability via **Kendall's W + chi-square**, with a permutation baseline.

## 3. Results
**Table 1 (fixed 100 epochs):** GCN + FFT is the only non-chance cell — 85.46 ± 17.47 denoised, **69.13 ± 26.71 raw**. Next best denoised: MLP+FFT 62.13, 1D-CNN+wavelet 61.50. Everything else ≈50% (GCN+time-series denoised = **36.23%**, below chance).

**Table 2 ("max accuracy"):** 1D-CNN+FFT **92.82 ± 8.43** (denoised), GCN+FFT 92.07 ± 16.50, GAT 90.83, MLP 89.04.

**Explanation stability:** Kendall's W = 0.149 (incremental), 0.224 (pruning), 0.280 (cumulative) — all "significant" by χ². Rankings highlight **occipital + right prefrontal** channels in both raw and denoised data.

**Channel pruning:** accuracy rises with channel count for rankings pooled across all CV folds (ANOVA F = 13.6, p = 0.0005); the leak-free per-fold ranking shows **no significant trend** (p = 0.46–0.13).

## 4. Scientific Critique & Our Analysis
*(Our inference, not paper claims.)*

1. **The paper's own two tables contradict each other, and the ranking fully reverses.** Table 1: GCN+FFT 85.46 vs 1D-CNN+FFT 47.41 (**+38 pp**). Table 2: 1D-CNN 92.82 vs GCN 92.07 (**CNN slightly ahead**). Same features, opposite conclusions. The cleanest reading is symmetric and damning: **Table 1 is an honest protocol with invalid training** (fixed 100 epochs, no schedule, no per-model tuning — the MLP/CNN baselines are crippled), and **Table 2 is valid training with an invalid protocol** ("max over epochs" on the held-out fold is test-set peeking). Neither table supports a model comparison. The abstract's "at least 20% higher accuracy than any other neural network model" is a property of Table 1 alone, and it is an artifact of under-training the baselines.
2. **The noise-robustness test cannot distinguish robustness from exploitation.** "Accuracy does not drop without ICA" is equally consistent with "the model reads the artifact." For *hyperactive* disorders the artifact is plausibly **class-correlated** (tic severity vs ADHD subtype differ in movement), and class-correlated nuisance needs no individual consistency — which is exactly the hand-wave offered ("hyperactive behavior varies across individuals"). Wrong axis: artifacts must be tested for *between-group* structure, not within-person variability. See [[Class-Correlated-Artifact-Control]].
3. **Attrition is unexplained and biased in the worst direction.** 34 ADHD → 21 ADHD (**38% dropped**), 21 Tic → 21 Tic (0% dropped). Yet 55 × 72 = 3,960 and 42 × 72 = 3,024 exactly — i.e. **not one epoch was rejected**, so the stated >50%-rejection rule cannot have dropped 13 children. Either the accounting is wrong or the exclusions were for undisclosed reasons. If the rule did operate as described, it removed the *noisiest* ADHD children — precisely the cases a noise-robustness claim must survive.
4. **Uncontrolled confounds in a two-clinical-group design.** Sex: ADHD 24M/10F (71% male) vs Tic 19M/2F (**90% male**). Medication: "some were on medication, discontinued 72 h prior" — **counts per group not reported**, and tic patients are commonly on antipsychotics (aripiprazole/risperidone) which alter EEG. Age differs slightly (10.32 vs 9.76). In a 2-class clinical contrast these are sufficient to produce high accuracy without any disorder-specific signal, and none is analysed.
5. **The independence unit is 6 children, not 3,024 epochs.** Each 7-fold test set contains 3 ADHD + 3 Tic subjects × ~72 five-second epochs. Reported SDs of **17–34 pp** are consistent with an estimate resting on six people. Pooled epoch accuracy, no per-subject aggregation, no CIs on participant-level accuracy.
6. **The interpretability validation is logically misdirected.** The task is to *separate* ADHD from Tic, but the highlighted fronto-occipital pattern is **shared by both classes** — and the cited literature says both disorders involve frontal (and occipital) regions. A shared feature cannot be the discriminative one. Validating a *discriminative* explanation against *each disorder's* pathology is the wrong test; class-conditional attributions (importance of the *difference*) are required.
7. **Explanation stability is weak and under-tested.** W = 0.15–0.28 is called "significantly consistent"; significance with k=7 raters and n=32 items says little when W < 0.3. The 7 rankings are not independent (overlapping training data), violating the χ² null. And the central claim — "same channels with and without noise" — is supported only *visually*: the actual raw-vs-denoised rank correlation is never computed, even though Table 3 contains both lists. (Eyeballing the cumulative-scoring top-10: Oz, O1, O2, Pz, P3, P4 overlap, but AF4/C4/P8/T8 vs F4/T7/F7 differ.)
8. **Channel pruning selects on the test folds and the leak is reported as a win.** Rankings "from all CV runs" aggregate information across every fold, then are evaluated on those same folds → circular. The honest per-fold variant shows **no significant accuracy trend** (p = 0.13–0.46). The paper concludes the leaky variant is "more effective." This is the exact failure mode in [[Nested-CV-and-Hyperparameter-Leakage]].
9. **36 cells, one winner, no multiplicity control, no seeds.** With SD ≈ 20 pp, the best of 36 cells is expected to look good by chance. No repeated initializations per cell, so the accuracy-vs-channels curve is unfiltered noise.
10. **Efficiency is asserted, not tested.** "Maximally efficient" is chosen by eye from a noisy curve with no equivalence test against the full-channel model, and no measured latency/power/FLOPs trade-off.

## 5. What Is Genuinely Valuable (and why we should keep this paper)
- **The differential-diagnosis formulation is the best in our vault.** ADHD vs Tic is a real, high-stakes clinical decision; ADHD vs healthy is not. This alone is worth importing into our project framing — with a public cohort.
- **The paired raw/denoised design is the artifact ladder, independently invented.** Their instinct matches [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]] §1; their execution just lacks the decisive control.
- **They noticed that k-fold inflates and said so** (their k-fold supplement has 1D-CNN winning). Rare and correct.
- **Kendall's W with a permutation baseline for explanation stability** — almost nobody quantifies XAI reliability; see [[Explanation-Stability-and-Faithfulness]].
- **One genuinely interesting result:** rankings derived from **raw** data are *more* concordant across folds than from denoised data (higher W, more often above chance). Their explanations: over-aggressive ICA, or denoising amplifying subject-specific structure. A third explanation is more interesting and fits our vault: **ICA removes the components that are shared across subjects; what remains stable in raw data may be a common artifact structure.** If so, their "noise-robust interpretability" is stable *because* it is artifact-driven — and that is testable.
- Honest reporting of enormous SDs and of counter-arguments (over-cleaning may remove signal).

## 6. Connections
- Papers: [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]]
- Concepts: [[Explanation-Stability-and-Faithfulness]], [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Opportunities: [[Class-Correlated-Artifact-Control]], [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]]
- Session log: [[2026-11-15-Kim-GCN-Analysis]]
