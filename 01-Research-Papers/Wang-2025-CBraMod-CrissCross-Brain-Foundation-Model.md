---
tags:
  - research-paper
  - foundation-models
  - eeg
  - ssl
  - transformer
  - bci
  - cross-subject
---

# Wang et al. (2025) — CBraMod: Criss-Cross Brain Foundation Model for EEG Decoding

- **Citation:** Wang, J., Zhao, S., Luo, Z., Zhou, Y., Jiang, H., Li, S., Li, T., Pan, G. (2025). *ICLR 2025* (Poster). [OpenReview 5836](https://openreview.net/forum?id=...)
- **Code:** [wjq-learning/CBraMod](https://github.com/wjq-learning/CBraMod) — released, with TUEG pretrained weights.
- **Pretraining:** TUH EEG Corpus (TUEG), ~27,000 h, fixed **19 channels**, 1 s patches, masked patch reconstruction.
- **Size:** ~4.88M params (per [[Shen-2026-Brain4FMs-Benchmark]]); reported as more efficient than BIOT/LaBraM.
- **In our vault already:** `ADHD-Child` task in [[Shen-2026-Brain4FMs-Benchmark]] → **AUROC 0.64 ± ?, Acc 0.64** — i.e. *below* Baibulova's lightweight theta-envelope dFC model (0.777 LOSO).

---

## 1. Core Claim (Paper)
- Existing EEG foundation models flatten all patches into one sequence and run full self-attention, ignoring that **spatial and temporal dependencies in EEG are heterogeneous** (same-channel or same-latency patches are more related than arbitrary cross pairs).
- **Criss-cross transformer:** two parallel attention families — *spatial* attention across channels at a fixed time patch, *temporal* attention across time at a fixed channel — with a 4:4 head split. Cost scales better than full attention.
- **ACPE (Asymmetric Conditional Positional Encoding):** a CNN over patch neighborhoods replaces electrode-index absolute embeddings, motivated by the fact that channel identity depends on the *reference scheme* (ear / average / REST / bipolar), not only on electrode position.
- **Patch embedding:** time-domain CNN branch + FFT-then-linear frequency branch, concatenated.
- Evaluated on up to 10 downstream tasks / 12 datasets; claims SOTA "across a wide range of tasks."

## 2. What the Review Thread Actually Reveals
*(Extracted from OpenReview; these numbers are more informative than the abstract.)*

**a) The alignment gap dwarfs the pretraining gap.** BCIC-IV-2a, 4-class, strict cross-subject (train 1–5, val 6–7, **test 8–9**):

| Method | BCIC-IV-2a balanced acc. (no alignment/"key ingredients") | LOSO with alignment + mixup + subject-wise reg. |
|---|---|---|
| EEGNet | 0.4482 ± 0.0094 | — |
| EEGConformer | 0.4696 ± 0.0106 | — |
| BIOT | 0.4748 ± 0.0093 | — |
| LaBraM | 0.4869 ± 0.0085 | — |
| **CBraMod** | **0.5138 ± 0.0066** | — |
| EEG-SimpleConv | 0.5650 ± 0.0989 | **0.7221 ± 0.0768** |
| **CBraMod** | 0.5968 ± 0.0816 | **0.7405 ± 0.0635** |

> **Reading:** unsupervised per-subject alignment + augmentation is worth **~14 accuracy points**; the foundation model over a simple conv net is worth **~2–3 points**. See [[Unsupervised-Alignment-Leverage]].

**b) Pretraining-corpus leakage was real, and fixing it changed almost nothing.** TUEV and TUAB are subsets of TUEG. Re-pretraining with those subsets removed: TUEV 0.6671 → 0.6659, TUAB 0.8289 → 0.8249. So the leakage did not inflate these particular numbers — but it also means the "SOTA" margins (e.g. 0.6659 vs LaBraM 0.6616 on TUEV) are **~0.4 points**, i.e. noise-level.

**c) High-frequency / EMG tell.** Reviewer k8cX asked for 0.3–30 Hz filtering on Mumtaz2016 (depression). CBraMod had the **largest drop of all models** (balanced acc. 0.9560 → 0.9268, −2.9; AUROC 0.9921 → 0.9826), vs LaBraM −1.3 and EEGConformer −1.1. The reviewer's interpretation: most power above 30–40 Hz in scalp EEG is muscle. This is the **second independent instance** of a high-performing model concentrating its edge in a band dominated by non-neural signal — cf. the preprocessing collapse of [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]].

**d) "Foundation model" is really "pretrained initialization."** Fine-tuned fully per task; pretrained on a fixed 19-channel montage. The authors explicitly concede: *"we have not asserted that CBraMod is a one-for-all model."* Reviewer m8H6's structural objection stands, though its experimental counter (mixed-channel pretraining → FACED) yielded only **+1.2 balanced acc. over random initialization** (0.5351 vs 0.5232) — albeit from small corpora, not TUEG.

**e) Statistical hygiene is thin exactly where it matters.** ±0.0066 on a **2-subject test set** (BCIC-IV-2a subjects 8–9). Those intervals describe seed variance on one split, not generalization. Same failure mode as [[Nested-CV-and-Hyperparameter-Leakage]] documents.

**f) Baselines were inherited, not chosen.** BIOT/LaBraM baselines were defended as "the baselines used by the SOTA papers" — which propagates the earlier papers' weak-baseline problem rather than fixing it. Reviewer iYYg had to supply the MI literature (EEGSym, TIDNet, ATCNet, EEG-SimpleConv) himself.

## 3. Our Assessment
- **Engineering: solid, incremental.** Criss-cross attention comes from CCNet (Huang et al., 2020); ACPE from Conditional Positional Encodings (Chu et al., 2021); patch embedding from BIOT/LaBraM. It is a careful recombination — and it was accepted, which is a useful calibration point: **recombination is not disqualifying; unsupported claims are.** The difference between this and [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] is evaluation breadth and a review process that forced the claims down to size.
- **Scientifically: the paper's most important result is the one its authors resisted** — that alignment and preprocessing geometry move the needle far more than pretraining scale. Every claim about "strong capability and generalizability" should be read through table (a).
- **For ADHD specifically: it loses.** On the one task we care about, `ADHD-Child`, CBraMod is 0.64 AUROC — below a Hilbert-envelope theta connectivity model with a GRU. Consistently, the vault's hypothesis is that BFMs latch onto local spectral power, not cross-channel coupling.
- **The review thread is itself a reusable artifact.** It is a public, adversarial audit of "SOTA on 12 datasets" claims, and it surfaces three transferable lessons: (i) equalize preprocessing before comparing architectures; (ii) check whether performance lives in an artifact-prone band; (iii) never report seed-SD on a 2-subject test set.

## 4. Positives Worth Keeping
- ACPE's argument — channel identity is reference-dependent, so electrode-index embeddings are fragile — is correct and applies to *any* model we build (including connectivity models whose edges are reference-dependent; cf. CTE-Net's Jaccard 0.067 under CAR).
- Criss-cross factorization is a cheap, sensible inductive bias for 19×T tensors, and a plausible lightweight alternative to full attention in a compact model.
- Full code + weights + per-task baselines in the appendix is the reproducibility standard we should match.
- They ran the **leakage-removal control** rather than arguing about it.

## 5. Connections
- Papers: [[Shen-2026-Brain4FMs-Benchmark]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]
- Areas: [[Brain-Foundation-Models-Landscape]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Opportunities: [[Unsupervised-Alignment-Leverage]], [[BFM-Bottlenecks-and-Hybrid-Opportunities]], [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]]
- Session log: [[2026-11-15-CBraMod-Analysis]]
