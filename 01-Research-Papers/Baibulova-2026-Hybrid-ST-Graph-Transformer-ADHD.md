---
tags:
  - research-paper
  - adhd
  - eeg
  - dynamic-connectivity
  - transformer
---

# Baibulova et al. (2026) — Hybrid Spatio-Temporal Graph Transformer for EEG-Based ADHD Detection via Network Index Modeling

- **Citation:** Baibulova, M., Mukhanova, A., Abdukarimova, A., et al. (2026). *Computers*, 15(6), 333. [DOI: 10.3390/computers15060333](https://doi.org/10.3390/computers15060333)
- **Code Repository:** [Mukhanovaa/EEG_ADHD_Dynamic_Envelope_Connectivity_Hybrid_ST_Graph_Transformer](https://github.com/Mukhanovaa/EEG_ADHD_Dynamic_Envelope_Connectivity_Hybrid_ST_Graph_Transformer/tree/main)
- **Dataset:** Kaggle redistribution (`danizo/eeg-dataset-for-adhd`) of IEEE DataPort ADHD EEG dataset by Nasrabadi et al. ([DOI: 10.21227/rzfh-zn36](https://doi.org/10.21227/rzfh-zn36)).

---

## 1. Core Problem & Formulation (Paper Findings)
- **Problem:** Subjective clinical ADHD scales lack reproducibility, while classical EEG spectral ratios (e.g., theta/beta ratio) suffer from age dependence, recording variability, and poor cross-cohort generalization.
- **Reframing:** Instead of pure binary classification, the authors formulate ADHD assessment as **[[Network-Index-Modeling]]**—learning a continuous scalar index $s \in \mathbb{R}$ from [[Dynamic-Functional-Connectivity]] sequences, trained via binary cross-entropy on $\sigma(s)$.
- **Dataset Scope:** 121 children (61 ADHD, 60 control), 19 channels (10–20 system), $f_s = 128\text{ Hz}$, recorded during a **structured visual counting task** (not resting-state), totaling 1,918,628 time samples.

## 2. Methodology
- **Artifact-Aware Preprocessing:**
  - Trend removal + median-based amplitude trimming ($\pm 6\text{ MAD}$).
  - Bandpass filtering in **theta (4–8 Hz)** and **beta (13–30 Hz)** bands.
  - **Hilbert transform amplitude-envelope correlations** (rather than raw amplitude correlations) over 4.0 s windows ($L=512$ samples, 50% overlap $\Delta=256$).
  - Sequence construction: $T=10$ consecutive windows (stride $S=5$).
  - Edge vectorization: Upper-triangular entries ($M = \frac{19 \times 18}{2} = 171$ unique undirected edges), z-score normalized using training-set statistics only.
- **Model Architecture ("Hybrid Multihead Spatio-Temporal Graph Transformer"):**
  - Dual-branch encoder operating on edge-weight sequences $E \in \mathbb{R}^{T \times 171}$:
    1. **Transformer Branch:** Linear projection + learnable positional encoding + Multi-Head Self-Attention + attention-based pooling ($g_{tr}$) for global temporal dependencies.
    2. **GRU Branch:** Recurrent encoding ($g_{rnn}$) for local sequential connectivity transitions.
  - Concatenation, normalization, dropout, and linear projection to scalar network index $s$.
- **Evaluation Protocol ([[Subject-Level-Evaluation-Hygiene]]):**
  - Strict subject-level split: 84 train / 18 validation / 19 test subjects.
  - Additional **Leave-One-Subject-Out (LOSO)** cross-validation across all 121 subjects.

## 3. Reported Results
- **Independent Test Set ($n=19$ subjects):**
  - Accuracy: 63.16% | Balanced Accuracy: 62.22% (95% CI [0.411, 0.833])
  - Sensitivity: 80.00% | Specificity: 44.44% | F1: 69.57% | AUC-ROC: 0.7444 (95% CI [0.489, 0.944])
  - Clinical operating point (assuming 10% prevalence): PPV = 0.1379, NPV = 0.9524.
- **LOSO Cross-Validation ($n=121$ subjects):**
  - Accuracy: 71.90% | Balanced Accuracy: 71.80% | Sensitivity: 82.00% | Specificity: 61.70% | F1: 74.60% | AUC-ROC: 0.7770.
- **Frequency-Band Ablation (Test Set):**
  - Theta-only AUC: 0.7333 vs. Beta-only AUC: 0.5667 vs. Combined Theta+Beta AUC: 0.7444 (theta connectivity drives almost all discriminative power).
- **Baselines:** Outperformed static linear, sparse L1 linear, global graph metrics, static GCN, spatio-temporal GCN, and standalone GRU on subject-level AUC-ROC and index separability.

## 4. Scientific Critique & Our Analysis
*(Interpretations and critical observations distinct from paper claims)*

1. **Valuable Realism vs. Inflated Literature:** The paper's strongest contribution is methodological honesty. It directly exposes why prior works claiming 93%–99% accuracy on the exact same dataset (Esas & Latifoğlu 2023; Alim & Imtiaz 2023; Bansal et al. 2021) are likely inflated by **window-level data leakage** across train/test splits. Under leak-free subject-level testing, realistic AUC-ROC drops to ~0.74–0.78.
2. **Naming vs. Architectural Reality ("Graph Transformer" Misnomer):** Despite being titled a *Graph Transformer*, the proposed hybrid model does **not** perform graph message-passing or topological attention over nodes/edges. It flattens the $19 \times 19$ connectivity matrix into a 171-dimensional vector and applies a standard temporal Transformer + GRU. Spatial graph topology is discarded in the hybrid model (unlike the Static/ST-GCN baselines, which actually used $\hat{A}$).
3. **Low Specificity & Screening Bottleneck:** At 44.44% specificity on the test set (61.70% in LOSO) and 13.79% PPV at 10% prevalence, the model produces too many false positives for standalone diagnostic use.
4. **No Stimulus/Event Synchronization:** Recordings were captured during a *visual counting task*, yet the sliding windows are completely blind to stimulus onset or behavioral response timing. Averaging/windowing across task events likely washes out transient attentional biomarkers.
5. **Internal Reporting Discrepancies & Small Test Sample:**
   - Test set has only 19 subjects, yielding massive 95% CIs (AUC [0.489, 0.944]—the lower bound crosses random chance 0.50).
   - The abstract reports distribution overlap = 0.72 and mean shift = 1.16, whereas Table 9 / Section 4.2 reports child-level overlap = 0.45 and Table 11 reports sequence-level $\Delta\mu = 6.21, d = 1.51$.
   - Figure 12/13 show a logistic regression baseline achieving 0.977 AUC on *fold-averaged* (likely window-level) CV before dropping drastically on subject-level test splits—illustrating the exact leakage gap if not careful.
6. **Single-Dataset & Tabular Limitations:** Using the Kaggle CSV (`adhd2.csv`) stripped of full clinical metadata, medication status, age/sex covariates, and ICA/artifact annotations limits clinical preprocessing and external validity.
7. **Theta dominance may be a 1/f artefact (added 2026-11-15, after [[Troendle-2026-TBR-Multiverse-HBN]]):** the theta AUC 0.733 vs beta 0.567 ablation used canonical bands on band-filtered data with no aperiodic decomposition. A steeper aperiodic exponent raises low-frequency power far more than high-frequency power, so a "theta connectivity" advantage is reproducible by 1/f geometry plus any class difference in slope (movement, impedance, age). This result must be re-derived on SpecParam-adjusted power before it is cited as oscillatory evidence. See [[Aperiodic-1f-Activity-and-Band-Ratios]].

## 5. Connections
- Related Concepts: [[Dynamic-Functional-Connectivity]], [[Network-Index-Modeling]], [[Subject-Level-Evaluation-Hygiene]], [[Aperiodic-1f-Activity-and-Band-Ratios]]
- Research Opportunities: [[ADHD-Event-Locked-Connectivity-and-Leakage]], [[Unsupervised-Alignment-Leverage]], [[Class-Correlated-Artifact-Control]]
- Direct Base-Paper Evolution Candidate: [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]
- Head-to-Head Project Synthesis: [[00-Candidate-Synthesis-and-Head-to-Head]]
- Later work on the same cohort: [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] (differentiable kernel TE, participant AUC 0.902, but preprocessing-sensitive and TIED by a plain ShallowConvNet) — analysis in [[2026-11-15-CTENet-Analysis]]
