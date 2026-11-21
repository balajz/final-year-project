---
tags:
  - research-log
  - foundation-models
  - benchmark
---

# Session Log: 2026-11-15 — Brain4FMs Benchmark & Cross-Paper Synthesis

## New Literature Added
- [[Shen-2026-Brain4FMs-Benchmark]] (*Brain4FMs: A Benchmark of Foundation Models for Electrical Brain Signals*, ZJU & CAS).

## Major Cross-Paper Discovery
- `ADHD_Child` (Motie Nasrabadi et al., 2020) in [[Shen-2026-Brain4FMs-Benchmark]] (Table 13) is the **exact same 121-subject dataset** used in [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]].
- Comparing the two papers head-to-head under strict cross-subject splits reveals a critical insight:
  - **Baibulova et al. (2026) lightweight Hilbert-envelope dFC model:** 0.7444 test AUROC / **0.7770 LOSO AUROC** (71.9% Acc).
  - **15 Brain Foundation Models (Brain4FMs Table 13):** Only **REVE (0.79 AUROC, 71% Acc)** and **BrainWave (0.78 AUROC, 71% Acc)** match it. Well-known BFMs like **LaBraM (0.66)**, **CBraMod (0.64)**, **EEGPT (0.67)**, **MBrain (0.69)**, and **BIOT (0.55)** fall substantially behind!
- **Why this happens:** Brain4FMs' PSD probing (Table 38) shows BFMs primarily latch onto **beta ($\beta$) spectral power**, whereas Baibulova et al. showed that **theta ($\theta$) inter-channel envelope synchronization** is the dominant connectivity driver (0.7333 AUROC alone vs 0.5667 for beta connectivity).

## Other Critical Findings Recorded
- Mapped the 15-model BFM taxonomy and empirical hierarchy in [[Brain-Foundation-Models-Landscape]].
- Logged 4 concrete research opportunities in [[BFM-Bottlenecks-and-Hybrid-Opportunities]]:
  1. Fusing BFM local spectral representations with explicit dynamic functional connectivity.
  2. Fixing cross-subject decision-boundary & F1 calibration collapse in BFMs.
  3. Addressing the complete failure of BFMs on cross-subject affective/BCI tasks (DEAP, SEED-IV, BCI-2a) via personalization or multimodal signals.
  4. Lightweight physiological priors vs. bloated LLM-style EEG models (NeuroLM/BFM).

## Second-Pass Update (Re-Read Against [[Liu-2026-EEG-FM-Compass-Benchmark]] & 9-Paper Vault)
- **Why `CBraMod` ranks #1 in EEG-FM-Compass yet scores 0.64 on `ADHD-Child` and 0.54 on `BCI-2a` in Brain4FMs:** Brain4FMs equalized preprocessing across all 15 models (good) but forced a single untuned learning rate (`lr = 1e-5` backbone / `1e-4` head) and omitted Euclidean Alignment (EA). Conversely, EEG-FM-Compass tuned each model individually (good) but allowed each FM to run its own author preprocessing (violating [[Decision-Log]] commitment 11).
- **Aperiodic 1/f Signature in Appendix G (Tables 36–38):** Brain4FMs' linear PSD probe shows near-ceiling predictability at the spectral extremes ($\delta$ at $r_d^n \approx 0.85\text{–}1.0$ and $\alpha/\beta$ at $0.80\text{–}1.0$) while $\theta$ predictability drops to $0.00$ across multiple clinical cohorts (`ADFD`, `SD-28`, `ADHD-Adult`). Because band PSD was computed *without* `SpecParam` 1/f removal, frozen BFM embeddings are heavily encoding the broadband **aperiodic offset and exponent $(\chi, A)$** ([[Aperiodic-1f-Activity-and-Band-Ratios]], [[Decoding-Multiverse-and-Aperiodic-Identity]]).
- **Pretraining-Corpus Overlap Contrast ([[Pretraining-Corpus-Overlap]]):** In EEG-FM-Compass, `EEGPT` hits 88.31% on `SEED` (in-corpus) while all out-of-corpus models sit at 52%–54%. In Brain4FMs, on `SEED-IV` and `DEAP`, every single BFM sits at **0.45–0.57 AUROC** (`Kappa ≈ 0.00`), confirming that zero-shot cross-subject emotion decoding is unsolved once in-corpus memorization is removed.
