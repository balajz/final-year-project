---
tags:
  - research-area
  - foundation-models
  - eeg
  - ssl
---

# Brain Foundation Models (BFMs) Landscape

Synthesized from [[Shen-2026-Brain4FMs-Benchmark]].

## 1. Core Architectural Shift
Neuro-AI is transitioning from small, task-specific CNNs/RNNs to **Self-Supervised Learning (SSL) Brain Foundation Models** pretrained on massive unlabeled EEG/iEEG repositories (e.g., TUH EEG, large clinical cohorts up to 25,000 subjects).

## 2. What Currently Works Best (Empirical Hierarchy)
1. **Masked Autoencoders (AE) in Frequency / Time-Frequency Space:**
   - Top performers across clinical tasks (**REVE**, **BrainWave**, **BrainOmni**, **LaBraM**, **CBraMod**) use bidirectional masked reconstruction rather than causal autoregressive generation or augmentation-based contrastive learning.
2. **Explicit Spatial Priors over Fixed Channel Indices:**
   - Models that inject 3D/4D electrode coordinates (**REVE**), graph topology (**MBrain**), or criss-cross spatial-temporal attention (**CBraMod**) handle montage shifts and channel permutations better than 2D CNNs over fixed channel order.
3. **Hierarchical Residual Vector Quantization (RVQ):**
   - Single-layer discrete codebooks (e.g., LaBraM, Chronos-BFM) bottleneck fine-grained discriminative cues during downstream fine-tuning. Multi-layer RVQ (**BrainOmni**) preserves coarse-to-fine structure.
4. **LLM-Aligned / Decoder-Heavy Models Underperform on Classification:**
   - Large autoregressive/LLM-bridged models (**NeuroLM** 170M, **NeuroGPT-D**, **BFM** 709M) consistently lose to smaller (5M–100M) bidirectional encoders on clinical and BCI classification benchmarks.

## 3. Where Current BFMs Fail (The Real Frontier)
- **Cross-Subject Affective & Semantic Decoding:** Near-random performance on DEAP (~0.51 AUROC), SEED-IV (~0.53 AUROC), and Chisco imagined speech (~0.50 AUROC).
- **Diffuse / Subtle Neurological Conditions:** Moderate ceilings on cross-subject `ADHD-Child` (max 0.79 AUROC by REVE) and `UCSD Parkinson's` (max 0.64–0.69 AUROC).
- **Calibration & Threshold Collapse:** Under standard fine-tuning (`lr=1e-5`), many BFMs output poorly calibrated probabilities (high AUROC but collapsed F1 = 0.00 or extreme false-positive rates).

## 4. The Alignment Gap (Evidence from [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]])
- On BCIC-IV-2a, **unsupervised per-subject alignment + augmentation is worth ~14 balanced-accuracy points**, while replacing a simple conv net with a 4.9M-parameter pretrained model is worth **~2–3**.
- Consequence: **pretraining scale is a second-order lever; per-subject signal geometry is first-order.** Any BFM comparison that does not equalize preprocessing is measuring the pipeline, not the model.
- See [[Unsupervised-Alignment-Leverage]] for the decomposition experiment.

## 5. Architectural Ideas Worth Borrowing
- **Criss-cross factorization:** separate spatial (across channels at fixed time) from temporal (across time at fixed channel) attention instead of flattening all patches into one sequence. Cheap, and matches the heterogeneous structure of EEG.
- **ACPE:** channel identity depends on the *reference scheme*, not only electrode position → electrode-index absolute embeddings are fragile. A CNN over patch neighborhoods is a more portable encoding. This hazard applies to connectivity models too: CTE-Net's learned edges changed almost completely under CAR (Jaccard 0.067).
- **Bottom line:** neither idea is new (CCNet 2020, CPE 2021); the contribution is the adaptation and the breadth of evaluation. Recombination is publishable — unearned claims are not.

## 6. The Recurring Artifact Signature
- Filtering 0.3–30 Hz costs CBraMod more balanced accuracy (−2.9) than any baseline on Mumtaz2016; most scalp power above 30–40 Hz is muscle. Compare [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] losing 10 accuracy points when artifacts are removed.
- Two independent SOTA models, two datasets, same direction → treat "performance lives in an artifact-prone band" as a **default hypothesis to test**, not a corner case.

## 7. Reconciling the Two Major Benchmarks: [[Shen-2026-Brain4FMs-Benchmark]] vs. [[Liu-2026-EEG-FM-Compass-Benchmark]]
When we put the two 2026 BFM benchmarks side by side, they expose an **orthogonal experimental trade-off** that neither paper solves alone:

| Benchmark | Models & Tasks | Preprocessing Policy | Hyperparameter / Alignment Policy | Resulting Blind Spot |
|---|---|---|---|---|
| **Brain4FMs** ([[Shen-2026-Brain4FMs-Benchmark]]) | 15 BFMs × 18 datasets (heavy clinical focus: Epilepsy, AD, PD, MDD, SD, ADHD) | **Unified pipeline** across all models (bandpass/notch, resampling, z-score). | **Fixed `lr = 1e-5` backbone / `1e-4` head** for all models; **zero Euclidean Alignment (EA)**. | Under-tunes sensitive models (`CBraMod` drops to 0.64 on ADHD-Child, 0.54 on BCI-2a) and induces threshold/F1 = 0.00 collapse (`Brant`, `NeuroGPT-D`, `BIOT`). |
| **EEG-FM-Compass** ([[Liu-2026-EEG-FM-Compass-Benchmark]]) | 12 BFMs + 8 specialists × 13 datasets (heavy BCI focus + TUAB/CHB-MIT/Sleep) | **Per-model original preprocessing** (each FM uses its author pipeline). | **Individually tuned per model**, EA applied *only* to `EEGPT` and `MIRepNet`; misses `REVE` and `BrainWave`. | Confounds architecture with preprocessing pipeline (violates [[Decision-Log]] commitment 11) and suffers from in-corpus pretraining overlap (`EEGPT` 88.3% on SEED; `LUNA` 81.9% on TUAB; see [[Pretraining-Corpus-Overlap]]). |

**Bottom-Line Synthesis Across Both Benchmarks:**
1. **No Universal Frozen Encoder Exists Yet:** Both benchmarks agree that linear probing is weak and no single BFM dominates across clinical and BCI paradigms without full adaptation.
2. **Data-Budget & Alignment Dominate Model Scale:** Neither benchmark finds a parameter scaling law (5M–70M models beat 170M–709M models). Under realistic few-shot calibration (30% of one session), classical `CSP+LDA` and `EEGNet` (2K params) beat 4M–50M Foundation Models on motor imagery.
3. **The Missing Experiment:** Neither benchmark runs the clean $2 \times 2$ (`{Unified Preprocessing vs. Native Preprocessing} × {Unaligned vs. Euclidean Alignment}`) with calibrated thresholds and aperiodic 1/f controls.
