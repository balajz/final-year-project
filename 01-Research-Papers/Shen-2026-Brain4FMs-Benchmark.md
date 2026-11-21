---
tags:
  - research-paper
  - foundation-models
  - benchmark
  - eeg
  - ieeg
  - ssl
---
	
# Shen et al. (2026) — Brain4FMs: A Benchmark of Foundation Models for Electrical Brain Signals

- **Authors:** Fanqi Shen, Enhong Yang, Jiahe Li, Junru Chen, Xiaoran Pan, Zhizhang Yuan, Li Meng, Yang Yang (Zhejiang University & CAS).
- **Code Repository:** [Brain4FMs Anonymous Repo](https://anonymous.4open.science/r/Brain4FMs-85B8)
- **Scope:** Unified self-supervised learning (SSL) taxonomy and standardized cross-subject benchmark evaluating **15 Brain Foundation Models (BFMs)** across **18 public EEG/iEEG datasets** (22 tasks spanning Disease Diagnosis, Sleep Staging, Communication/BCI, and Affective Computing).

---

## 1. Unified SSL Taxonomy for Brain Foundation Models
The paper unifies BFM pretraining under an operator formulation $\mathcal{L}_{\text{sum}} = \mathcal{L}(\mathcal{G}(\mathcal{Q}(\mathcal{F}(\mathcal{T}_{d,s}(\mathcal{X}_{src}), \mathcal{M}))), \mathcal{F}(\mathcal{T}_{d,s}(\mathcal{X}_{tgt})), \mathcal{N})$ and categorizes the 15 benchmarked models into three paradigms:

### A. Contrastive-Based Methods
- **Augmentation Contrast:** SppEEGNet (138K, time), BIOT (3.19M, time+freq).
- **Contrastive Predictive Coding (CPC):** BENDR (3.97M, time+freq), MBrain (8.34M, EEG/iEEG, time+freq+space via GNN+CPC).
- **Cross-Modal Contrast:** MulEEG, SleepFM, Brant-X (discussed in taxonomy).

### B. Generative-Based Methods
- **Autoregressive (AR):** NeuroGPT (79.62M, time+freq; evaluated as encoder-only `NeuroGPT-E` and encoder-decoder `NeuroGPT-D`).
- **Autoencoder / Masked Reconstruction (AE):**
  - Brant (196.10M, iEEG, time+freq+space)
  - BFM (708.96M, EEG, time, Chronos tokenizer)
  - BrainBERT (43.18M, iEEG, time+freq)
  - CBraMod (4.88M, EEG, time+freq+space, criss-cross spatial-temporal attention)
  - LaBraM (5.80M, EEG, time+freq+space, VQ-VAE Fourier codebook during pretraining)
  - BrainWave (102.13M, EEG+iEEG, time+freq+space, pretrained on >16,000 subjects)
  - REVE (69.19M, EEG, time+space, 4D anatomical positional embeddings, pretrained on 25,000 subjects)
  - BrainOmni (32.71M, EEG/MEG, time+freq+space, multi-layer Residual Vector Quantization RVQ)

### C. Other Advanced / Hybrid / Instruction-Tuned Methods
- **Hybrid (Generative + Contrastive):** EEGPT-1 (51.04M, EEG, time+space).
- **Generative + Adversarial / LLM-aligned:** NeuroLM (169.60M, EEG, VQ tokens + domain-adversarial text alignment).

---

## 2. Empirical Findings Across the 5 Research Questions (Paper Findings)

1. **Q1 — Data Composition & Modality Transfer:**
   - Strong modality specificity: iEEG-only models (e.g., Brant) excel on iEEG epilepsy (MAYO 0.92 AUROC, FNUSA 0.87) but collapse on scalp EEG epilepsy (CHB-MIT 0.55 AUROC, F1 = 0.00).
   - Joint EEG+iEEG pretraining (**BrainWave**) achieves the highest scalp/intracranial transfer on epilepsy (MAYO 0.98, FNUSA 0.92, CHB-MIT 0.90 AUROC).
   - Large-scale scalp EEG pretraining with 4D spatial coordinates (**REVE**) dominates many scalp clinical/motor tasks (ADFD 0.84 AUROC, MDD-64 0.97, ADHD-Child 0.79, ISRUC Sleep 0.92, EEGMMIDB Motor 0.82).
   - **Catastrophic Failure on Affective & Imagined Speech Decoding:** On DEAP (emotion), SEED-IV (emotion), BCI-2a (4-class motor imagery), and Chisco (39-class imagined speech), **every single BFM fails under cross-subject evaluation** (DEAP AUROC ~0.45–0.52; SEED-IV AUROC ~0.48–0.57; Chisco AUROC ~0.50, Acc ~3–5% = random chance).

2. **Q2 — SSL Paradigm Comparison:**
   - **Generative (AE) > Contrastive:** AE-based models produce much higher inter-/intra-class separation ($R_{cls}$) and lower boundary error rates ($LMER$) than contrastive models.
   - **Within Contrastive, CPC > Augmentation:** MBrain (CPC + graph) consistently beats augmentation-contrast models (BIOT, SppEEGNet), as generic time/channel perturbations introduce boundary noise under cross-subject shift.
   - **Within Generative, Bidirectional AE > Unidirectional AR (and Encoder > Decoder):** `NeuroGPT-E` (encoder-only) drastically outperforms `NeuroGPT-D` (encoder-decoder) across almost all classification tasks (e.g., CHB-MIT 0.78 vs 0.61 AUROC; EEGMMIDB-R 0.77 vs 0.50). Causal decoding hurts window-level classification.

3. **Q3 — Spatial Structure Sensitivity (Channel Permutation Tests):**
   - Shuffling channel order in train/val while testing on unshuffled data reveals that **task biology dictates spatial sensitivity**: Epilepsy (CHB-MIT) suffers massive AUROC drops when channels are shuffled (e.g., BrainWave drops from 0.90 to 0.59), whereas Alzheimer's (ADFD) and ADHD-Child show much smaller drops for topology-aware models because their biomarkers are more globally distributed or fronto-parietally diffuse.
   - Models using CNNs over fixed channel order (BrainWave) break under channel permutation, whereas models with explicit spatial/graph embeddings (BrainOmni, MBrain, REVE) are more resilient.

4. **Q4 — Frequency Information Representation:**
   - Linear probing of frozen fine-tuned encoders for band-wise PSD ($r_b^n$) shows that BFMs adaptively emphasize clinically relevant bands: $\alpha$ and $\gamma_l$ predictability correlates with Alzheimer's (ADFD) ranking; $\beta$ and $\gamma_l$ (and $\alpha$ in children) correlate with ADHD performanceranking.

5. **Q5 — Codebook Discretization:**
   - Generic time-series tokenizers (BFM/Chronos) and single-layer VQ-VAE codebooks (LaBraM) suffer from poor class separation ($DR \approx 0.001–0.038$ without codebook fine-tuning). LaBraM actually **discards its codebook during fine-tuning** because keeping discrete quantization bottlenecks discriminative cues.
   - **Multi-layer Residual Vector Quantization (RVQ)** in **BrainOmni** preserves high token entropy while progressively improving class separation across residual layers 1 to 4.

---

## 3. Direct Synthesis & Cross-Check with [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]
*(Critical synthesis connecting our knowledge base)*

1. **Independent Confirmation of the ADHD-Child Ceiling (~0.78–0.79 AUROC):**
   - `ADHD_Child` in Brain4FMs is the **exact same dataset** (Motie Nasrabadi et al., 2020, $n=121$ children, 19 channels, 128 Hz) used by [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]!
   - Under Brain4FMs' standardized cross-subject split (Table 13):
     - **REVE:** AUROC = **0.79 ± 0.07**, Acc = **0.71 ± 0.04**, F1 = 0.74
     - **BrainWave:** AUROC = **0.78 ± 0.04**, Acc = **0.71 ± 0.04**, F1 = 0.74
     - **BrainOmni:** AUROC = 0.71 ± 0.09, Acc = 0.62 ± 0.07
     - **MBrain:** AUROC = 0.69 ± 0.11, Acc = 0.63 ± 0.08
     - **EEGPT:** AUROC = 0.67 ± 0.13, Acc = 0.64 ± 0.10
     - **LaBraM / CBraMod:** AUROC = 0.66 / 0.64, Acc = 0.64 / 0.64
     - **BIOT:** AUROC = 0.55 ± 0.05 (severe threshold calibration skew: Acc 0.75, F2 0.93)
   - **Insight:** Baibulova et al.'s lightweight domain-specific dynamic connectivity model achieved **0.7444 test / 0.7770 LOSO AUROC (71.9% Acc)**—matching 70M–100M parameter foundation models (REVE 0.79, BrainWave 0.78) and **beating** LaBraM (0.66), CBraMod (0.64), EEGPT (0.67), and BIOT (0.55) on the exact same cohort!

2. **The Theta vs. Beta Tension in ADHD-Child:**
   - In [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], **theta (4–8 Hz)** envelope connectivity was far more predictive (AUC 0.7333) than **beta (13–30 Hz)** connectivity (AUC 0.5667), whereas beta *power* showed uniform positive shifts across frontal/midline channels.
   - In Brain4FMs (Section 3.3.4 & Table 38), linear PSD probing of BFM embeddings showed that **beta ($\beta$), alpha ($\alpha$), and low-gamma ($\gamma_l$) power predictability** correlated positively with BFM ranking on ADHD-Child.
   - **Hypothesis:** BFMs rely heavily on local spectral power (where beta power dominates in ADHD), whereas inter-regional phase/envelope *synchronization* alterations in ADHD occur primarily in the slow theta band—information that patch-level BFM encoders may under-exploit unless explicitly modeled as cross-channel dynamic coupling.

3. **Methodological Weaknesses of Brain4FMs to Watch Out For:**
   - **Fixed Hyperparameter Starvation (`lr = 1e-5` for all backbones):** Brain4FMs forces a single fixed learning rate ($10^{-5}$ backbone, $10^{-4}$ head) across 15 wildly different architectures (from 138K CNNs to 708M Transformers). Models like BIOT, CBraMod, and LaBraM often require specific warmup/layer-decay schedules, which explains why several models collapse to majority-class prediction (e.g., F1 = 0.00 on CHB-MIT or Dep-BDI for Brant/NeuroGPT-D, or BIOT predicting all-ones on CHB-MIT with Acc 0.29 and AUROC 0.56).
   - **ADHD-Adult Anomaly (2 channels, 0.96 AUROC vs. 19 channels, 0.79 AUROC in ADHD-Child):** Almost every model hits 0.95–0.96 AUROC on `ADHD-Adult` (2 channels) while struggling at 0.55–0.79 on `ADHD-Child` (19 channels). This strongly suggests dataset-specific acquisition artifacts or paradigm differences in `ADHD-Adult` rather than adult ADHD being "easier" biologically.
   - **Parkinson's (UCSD) Near-Random Performance:** On UCSD-OFF/ON, every BFM scores ~0.44–0.69 AUROC (most ~0.50–0.60), showing that resting-state PD diagnosis from scalp EEG remains poorly solved by current foundation models.

---

## 4. Re-Evaluation After [[Liu-2026-EEG-FM-Compass-Benchmark]] & Our 9-Paper Vault Synthesis
*(Added 2026-11-15 — what changes when we read Brain4FMs alongside EEG-FM-Compass, Troendle's TBR Multiverse, and the Pretraining-Corpus Overlap rules)*

1. **Two Benchmarks, Two Opposite Design Flaws (Brain4FMs vs. EEG-FM-Compass):**
   - **Brain4FMs** equalizes the *preprocessing pipeline* across all 15 models (satisfying [[Decision-Log]] commitment 11), **but** forces a single fixed learning rate (`1e-5` backbone / `1e-4` head) with no Euclidean Alignment (EA) and no per-model warmup. That causes severe calibration and boundary collapse (`F1 = 0.00` on CHB-MIT, EEGMat, Dep-BDI).
   - **EEG-FM-Compass** ([[Liu-2026-EEG-FM-Compass-Benchmark]]) does the exact opposite: it individually tunes each FM's hyperparameters, **but** lets each model run its own author-shipped preprocessing and applies EA to only 2 models (`EEGPT`, `MIRepNet`).
   - **The Consequence:** This explains why **`CBraMod`** looks mediocre in Brain4FMs (`0.64 AUROC` on `ADHD-Child`, `0.54` on `BCI-2a`, `0.55` on `ADFD`) yet emerges as the **#1 ranked Foundation Model** across 13 datasets in EEG-FM-Compass! Brain4FMs starved `CBraMod` with a fixed `1e-5` learning rate and omitted EA.
2. **Pretraining–Corpus Overlap ([[Pretraining-Corpus-Overlap]]) Explains the "Easy" vs. "Hard" Tasks:**
   - In Appendix B, Brain4FMs admits that several models pretrained on **TUEG/TUH** (Obeid & Picone, 2016), **SEED**, or **BCI Competition IV**, and explicitly notes: *"Brain4FMs evaluates models as released under unified protocols rather than re-pretraining leave-dataset-out variants."*
   - Even with partial overlap on `SEED-IV` and `BCI-2a`, Brain4FMs' standardized pipeline yields **near-random cross-subject transfer (`0.50–0.57 AUROC` on SEED-IV; `0.50–0.61 AUROC` on BCI-2a)**, confirming that without in-corpus memorization or per-subject alignment (EA), foundation models do **not** solve cross-subject emotion or motor imagery zero-shot.
3. **Re-Reading Table 38 (PSD Predictability) Through the Aperiodic 1/f Lens ([[Aperiodic-1f-Activity-and-Band-Ratios]]):**
   - Look closely at Appendix G (Tables 36–38): across almost every model and every clinical dataset (`ADFD`, `Dep-122`, `SD-28`, `MDD-64`, `ADHD-Child`), the normalized predictability of **delta ($r_d^n \approx 0.85\text{–}1.00$)** and **alpha/beta ($r_a^n, r_b^n \approx 0.80\text{–}1.00$)** is near ceiling, while **theta ($r_t^n$) is frequently 0.00** on `ADFD`, `SD-28`, and `ADHD-Adult`.
   - Because Brain4FMs computed band-wise PSD *without* `SpecParam` aperiodic decomposition, linear heads predicting canonical band power from frozen BFM embeddings are largely reading the **broadband 1/f offset and exponent $(\chi, A)$** (which anchors delta at the low end and beta/low-gamma at the high end). This directly supports our vault's mechanistic hypothesis in [[Decoding-Multiverse-and-Aperiodic-Identity]].
4. **Disjoint Top Performers Across the Two Benchmarks:**
   - Brain4FMs' top two clinical models — **REVE** (69M, 25,000 subjects) and **BrainWave** (102M, >16,000 EEG+iEEG subjects) — were **not included** in [[Liu-2026-EEG-FM-Compass-Benchmark]] (which only tested 12 models with public weights at the time). Any thesis claim about "the current state of EEG Foundation Models" must synthesize *both* benchmarks rather than citing either one alone.

---

## 5. Connections
- Related Papers: [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Liu-2026-EEG-FM-Compass-Benchmark]], [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]], [[Troendle-2026-TBR-Multiverse-HBN]]
- Related Areas & Concepts: [[Brain-Foundation-Models-Landscape]], [[Subject-Level-Evaluation-Hygiene]], [[Dynamic-Functional-Connectivity]], [[Pretraining-Corpus-Overlap]], [[Aperiodic-1f-Activity-and-Band-Ratios]]
- Research Opportunities & Candidates: [[BFM-Bottlenecks-and-Hybrid-Opportunities]], [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]], [[Decoding-Multiverse-and-Aperiodic-Identity]], [[00-Candidate-Synthesis-and-Head-to-Head]]
