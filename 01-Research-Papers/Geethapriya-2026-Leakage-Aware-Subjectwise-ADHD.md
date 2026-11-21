---
tags:
  - research-paper
  - adhd
  - eeg
  - leakage
  - evaluation
  - xai
---

# Geethapriya & Pattabiraman (2026) — Leakage-Aware Subject-Independent ADHD Classification

- **Citation:** Geethapriya, M., Pattabiraman, K. *Subject-independent classification of ADHD from pediatric EEG: a leakage-aware deep learning framework with interpretable neurophysiological mapping.* PMC13680413 / PMID 42903275 (open access).
- **Code:** No repository reported.
- **Dataset:** IEEE DataPort Nasrabadi cohort — **121 children (61 ADHD / 60 control)**, 19 ch, 128 Hz, linked-earlobe reference, visual counting task. 4,173 non-overlapping 4 s epochs.
- **In our vault:** same cohort as [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], and the `ADHD-Child` task of [[Shen-2026-Brain4FMs-Benchmark]]. Fourth paper on the same 121 children.

---

## 1. Core Claim (Paper)
Two protocols on **identical fold assignments**, six model families:
- **Protocol A** — segment-wise 10-fold (epochs shuffled across folds; the leaky practice).
- **Protocol B** — subject-wise 10-fold (12 children per fold, stratified 6 ADHD + 6 control).

Headline: hand-engineered **PSD features are catastrophically leak-prone** (SVM 90.0% → 65.6%, −24.4 pp), whereas a **raw-EEG 1D CNN is resilient** (75.2% → 72.7%, −2.5 pp, n.s.). DeepSHAP on the CNN localizes importance to F3/Fz/F4/Cz, argued to match ADHD neurophysiology.

## 2. Methods
- Bandpass 0.5–50 Hz (4th-order Butterworth) + 50 Hz notch; per-channel z-score fit on the **training partition only** (correct).
- 4 s **non-overlapping** epochs (stricter than CTE-Net's 50% overlap), artifact-screened.
- Features: Welch PSD, 5 bands × 19 ch = **95-dim**.
- Models: LR (ℓ2), RF (500 trees), SVM-RBF (nested 3-fold grid over C, γ); LSTM (2×64), CNN (3×Conv1D, k=7, 32/64/64, ~0.15M params), CNN–BiLSTM (~0.19M). Deep hyperparameters **fixed a priori**, not tuned per fold.
- Stats: Wilcoxon signed-rank + Bonferroni across 6 models; DeLong for AUC.

## 3. Results (verbatim)

| Model | Protocol A acc. | Protocol B acc. | Gap (pp) | B AUC |
|---|---|---|---|---|
| SVM (PSD) | 90.0 ± 1.3 | 65.6 ± 4.9 | **−24.4** (p<0.001) | 0.72 |
| Random Forest | 86.3 ± 1.2 | 65.1 ± 6.2 | **−21.2** (p<0.001) | 0.70 |
| Logistic Regression | 73.8 ± 1.6 | 59.9 ± 4.7 | −13.9 (p<0.01) | 0.63 |
| CNN–BiLSTM | 72.5 ± 6.7 | 65.7 ± 6.8 | −6.9 (p≈0.05) | 0.74 |
| LSTM | 65.3 ± 2.7 | 61.6 ± 7.7 | −3.7 (n.s.) | 0.63 |
| **CNN** | 75.2 ± 5.6 | **72.7 ± 9.3** | **−2.5** (n.s.) | **0.72** |

- CNN pooled: precision 0.705, **recall 0.880**, **specificity 0.534**, F1 0.783, AUC 0.72.
- 5 seeds → 72.5 ± 0.5 (vs fold SD 9.3).
- DeLong: CNN vs CNN–BiLSTM Z=0.48, p=0.63; **CNN vs SVM Z=0.12, p=0.90** (AUC 0.72 vs 0.72).
- DeepSHAP mean |value|: F3 0.095, Fz 0.092, F4 0.088, Cz 0.086; T3–T6 0.043–0.052; O1/O2 0.041/0.040.

**Cross-check with the vault:** 4,173 non-overlapping epochs ≈ half of CTE-Net's 8,213 (50%-overlap) windows — consistent. Per-subject counts (ADHD 38.2 ± 5.4, control 30.7 ± 4.8) also match CTE-Net's medians once overlap is removed. The corpus numbers corroborate each other.

## 4. Scientific Critique & Our Analysis
*(Our inference, not paper claims.)*

1. **The "CNN beats SVM" result is a threshold artifact.** DeLong gives **identical AUC (0.72 vs 0.72, p=0.90)**, i.e. equal discrimination. The 7.1-point accuracy gap comes entirely from operating point: CNN recall 88.0 / specificity 53.4 vs SVM recall 68.0 / specificity 62.5. Balanced accuracy is 70.7 vs 65.3, and under a matched-specificity or Youden-optimal threshold the gap shrinks to a few points. Reporting accuracy at τ=0.5 for models with different calibration is not a model comparison — it is a calibration comparison in disguise. The paper never reports balanced accuracy, ECE, or Brier.
2. **No participant-level metric — in a paper about subject-level rigor.** 121 held-out children are available; the authors report only pooled epoch metrics, which they concede "assign proportionally more weight to participants with higher counts." ADHD children have *more* epochs (38.2 vs 30.7) and the CNN has 88% ADHD recall → pooled accuracy is structurally optimistic relative to a per-subject average. Aggregating ~34 epoch probabilities per child would also *raise* AUC materially. This is the exact rule the vault enforces ([[Subject-Level-Evaluation-Hygiene]] rule 7) — and its absence means the paper's "honest ceiling" (0.72) is an epoch-level floor, not a participant-level estimate.
3. **Feature type and model family are confounded.** Classical models see 95 PSD features; deep models see raw EEG. The claim "hand-engineered features leak, deep learning does not" is therefore not identified. The decisive control is a 2×2: {PSD, raw} × {SVM/RF, deep MLP/CNN}. A deep MLP on PSD would isolate feature-driven leakage; a linear model on raw would isolate model-driven leakage. They gesture at this (subject-identification probes) as future work — correct instinct, missing experiment.
4. **Tuning asymmetry.** SVM got nested 3-fold grid search; deep models got fixed hyperparameters and were never tuned to exploit identity. Defensible for avoiding validation overfitting (they argue this explicitly), but it means the comparison is "tuned-pipeline-A" vs "unedited-pipeline-B". A fixed-hyperparameter SVM or a tuned CNN would be the fair pair.
5. **The paired tests don't pair.** Wilcoxon compares Protocol A and B accuracies by fold index, but the two protocols partition *differently* — fold 3 of A has no relationship to fold 3 of B, and the 10 values are not independent. The p<0.001 is not a valid test of the gap; a subject-level bootstrap would be. Same for DeLong on **pooled epoch predictions**: 4,173 epochs from 121 children are strongly correlated, so the independence assumption is violated (this happens to make the non-significant comparisons conservative, but the method is wrong).
6. **Seed stability is mistaken for uncertainty.** "5 seeds → 72.5 ± 0.5" next to fold SD of 9.3 is the cleanest illustration yet that seed variance measures optimization noise. The 95% CI across folds for the CNN spans **66.0–79.4** — a 13-point interval on 12-subject test folds.
7. **The exact baselines that matter are absent.** EEGNet and ShallowConvNet are explicitly deferred. But ShallowConvNet is the model that ties the full CTE-Net pipeline on this cohort, and Baibulova's theta-envelope dFC reaches 0.777 LOSO. So the paper's benchmark is below the known ceiling *and* unconnected to the models that define it. It also does not cite CTE-Net.
8. **SHAP without a null.** Channel-level |SHAP| averaged over 512 samples, no error bars, log-scaled bar chart, no permuted-label retraining and no class-conditional attribution. A fronto-central pattern is also exactly what a *generic attention-task* representation would produce — both groups perform the same visual counting task, so channel importance need not be group-discriminative. The claim "conforms to neurophysiological expectations" is plausible-but-unfalsified, not evidence. Note the partial counter-argument: Fp1/Fp2 are *not* in the top four, which weakens a pure blink explanation — but the full 19-channel vector and an artifact-channel control are needed to make that argument.
9. **Dataset-provenance conflict (important for the vault).** This paper states ADHD children "had received methylphenidate with **appropriate clinical washout** prior to recording." [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] states medication status at acquisition was **unavailable**, and the vault's [[Decision-Log]] records the confound as unresolved. Both cannot be right. Must be settled against the primary IEEE DataPort documentation before any paper of ours cites either version — the answer changes whether this cohort's ADHD signal is partly a medication signal.
10. **Novelty is a re-measurement, not a discovery.** The leakage gap was already quantified (0.744–0.777 vs 93–99%) in the papers we reviewed. The contribution here is the *family-wise* decomposition on matched folds — genuinely useful, but it is corroboration of a known phenomenon, published in 2026, on a saturated cohort.

## 5. What This Paper Genuinely Establishes (and why we should cite it)
- **Quantified leakage magnitude by feature type on matched folds** — the best single table we have for [[Subject-Level-Evaluation-Hygiene]]. Reuse it instead of re-deriving.
- **A mechanism:** static spectral descriptors (band power) encode *subject identity* — impedance, skull conductance, baseline spectral envelope. This is precisely the quantity that per-subject covariance alignment removes, which is direct support for [[Unsupervised-Alignment-Leverage]].
- **A nuance that cuts against a naive alignment story:** end-to-end raw-signal models lose only 2.5 pp, i.e. raw convolutions are already fairly subject-agnostic. So alignment may matter far more for feature-based pipelines than for end-to-end models — testable, and a plausible reason the CTE-Net-style results (features computed on raw windows, linear head) sit closer to the leaky regime.
- **Correct hygiene in the details:** non-overlapping epochs, scaler fit on training folds only, subject-level stratification, honest CIs spanning 13 points, explicit statement that 72.7% is not diagnostic.
- **A clean negative result on hybrid complexity:** CNN > CNN–BiLSTM under subject-wise CV, consistent with everything else we have read.

## 6. Connections
- Papers: [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Shen-2026-Brain4FMs-Benchmark]], [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]], [[Representation-Dispersion-and-Stability]]
- Opportunities: [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]], [[Unsupervised-Alignment-Leverage]]
- Session log: [[2026-11-15-Geethapriya-Analysis]]
