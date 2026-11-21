---
tags:
  - technical-concept
  - evaluation
  - data-leakage
---

# Subject-Level Evaluation Hygiene (Preventing Data Leakage in EEG)

## The Core Pitfall
EEG recordings from a single participant exhibit high autocorrelation, subject-specific skull/scalp conductivity, and persistent background spectral signatures. If an EEG recording is segmented into overlapping 2–4 second windows and **randomly split** (e.g., 80/20 window-level split or standard k-fold CV), windows from the same person appear in both training and test sets.

## Consequence
The model learns **subject identity** (fingerprinting) rather than **condition biomarkers**. This routinely produces artificially inflated accuracies (93%–99%+) that collapse to 60%–75% on unseen individuals.

## Evidence from Literature
- As highlighted in [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], prior deep learning studies on the IEEE DataPort ADHD dataset (Esas & Latifoğlu 2023; Alim & Imtiaz 2023; Bansal et al. 2021) reported 93%–99% accuracy using sample-level splits.
- Under strict **subject-level splitting** and **Leave-One-Subject-Out (LOSO)** validation on the same dataset, AUC-ROC drops to **0.7444** (test) and **0.7770** (LOSO).
- **Cautionary case:** [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] reports ±0.0066 balanced-accuracy SD on a **2-subject** test set (BCIC-IV-2a subjects 8–9). Tight seed intervals on near-zero test samples quantify optimization noise, not generalization. Always report the number of *test subjects*, not only the number of seeds.

## Non-Negotiable Rules for Our Project
1. All train/validation/test partitions must be strictly **subject-disjoint** (or **LOSO / GroupKFold by subject**).
2. Feature standardization ($\mu_{train}, \sigma_{train}$), PCA, and threshold tuning must be fit **exclusively on training subjects**.
3. Report subject-level (not just window-level) metrics, confidence intervals, and operating-point trade-offs (Sensitivity, Specificity, PPV/NPV under realistic prevalence).
4. **Model selection must not see the test fold.** A single configuration chosen on the average validation score across the same folds used for reporting is a mild leak — see [[Nested-CV-and-Hyperparameter-Leakage]].
5. **Seed variance ≠ partition variance.** Repeating training on identical folds measures optimization stability only; generalization uncertainty requires repeated or nested partitions, and CIs conditional on one split must be labelled as such.
6. **Window-level metrics are descriptive, never primary.** Overlapping windows are not independent observations; aggregate to the participant before making any claim.

## The Quantified Leakage Gap (best available evidence)
From [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]: identical 121-child cohort, identical folds, only the *partitioning unit* changes. 4 s non-overlapping epochs, 10-fold in both protocols.

| Model family | Features | Segment-wise (leaky) | Subject-wise (honest) | Gap |
|---|---|---|---|---|
| SVM | PSD (95-dim) | 90.0% (AUC 0.96) | 65.6% (AUC 0.72) | **−24.4 pp** |
| Random Forest | PSD | 86.3% | 65.1% | **−21.2 pp** |
| Logistic Regression | PSD | 73.8% | 59.9% | −13.9 pp |
| CNN–BiLSTM | raw EEG | 72.5% | 65.7% | −6.9 pp |
| LSTM | raw EEG | 65.3% | 61.6% | −3.7 pp (n.s.) |
| CNN | raw EEG | 75.2% | 72.7% | −2.5 pp (n.s.) |

**Two lessons, both mechanical:**
1. **The leak is bigger for feature-based pipelines.** Static spectral descriptors (band power) encode subject identity — impedance, skull conductance, baseline spectral envelope — so a leaky split lets the classifier match *people*, not conditions.
2. **A small leakage gap does not redeem a model.** In this table the CNN's honest AUC (0.72) equals the SVM's honest AUC (0.72); the apparent 7-point accuracy advantage is a decision-threshold artifact (recall 88.0/specificity 53.4 vs 68.0/62.5). Equal AUC ⇒ equal discrimination; report balanced accuracy or matched-specificity operating points, never raw accuracy at τ=0.5 alone.

The mechanism in (1) is exactly what per-subject covariance alignment removes — see [[Unsupervised-Alignment-Leverage]].

### A second, specific identity channel (new, 2026-11-15)
The aperiodic **1/f exponent and offset** are stable within a person, variable across people, and shift *every* band power coherently — the profile of a fingerprint. Band-power features therefore encode identity twice: through electrode/skull geometry (removed by alignment) and through the individual spectral background (not removed by alignment). Testable with a single cheap probe — predict participant ID from `(exponent, offset)` alone. See [[Aperiodic-1f-Activity-and-Band-Ratios]] §4 and [[Decoding-Multiverse-and-Aperiodic-Identity]].

## 6. Related Failures of the Same Family
- **Explanation leakage:** channel attributions derived from rankings pooled across folds, then validated on those folds ([[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]) — same circularity, applied to XAI rather than to accuracy.
- **Artifact leakage:** a model that "survives" uncleaned data may be reading the uncleaned data's class-correlated statistics, not the neural signal ([[Class-Correlated-Artifact-Control]]).
