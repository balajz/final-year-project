---
tags:
  - research-log
  - foundation-models
  - bci
  - cross-subject
---

# Session Log: 2026-11-15 — CBraMod (ICLR 2025) Analysis

## New Literature Added
- [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] — criss-cross spatial/temporal attention + ACPE, TUEG pretraining, 10 downstream tasks. Already known to us as the **0.64 AUROC** entry on `ADHD-Child` in [[Shen-2026-Brain4FMs-Benchmark]].

## The Headline Finding (not in the abstract)
The OpenReview thread contains a controlled comparison the paper never puts in a table together:

| BCIC-IV-2a, cross-subject | Balanced acc. |
|---|---|
| EEG-SimpleConv, minimal preprocessing | 0.565 |
| CBraMod, minimal preprocessing | 0.597 |
| EEG-SimpleConv + EA/mixup/subject-wise reg. | 0.722 |
| CBraMod + same | 0.741 |

**Unsupervised alignment is worth ~14 points; the foundation model is worth ~2.** This is the single most decision-relevant number we have encountered for our project, because it re-orders the entire solution space: data geometry before model capacity.

## Corroborating Evidence Collected
1. **Artifact-band tell (second independent instance).** Filtering 0.3–30 Hz costs CBraMod **−2.9** balanced accuracy on Mumtaz2016, more than any baseline (LaBraM −1.3, EEGConformer −1.1). The lost band (30–75 Hz) is dominated by muscle. Compare CTE-Net's 10-point collapse after cleaning. Two different SOTA models, two datasets, same signature → artifact dependence is **systematic**, not incidental.
2. **Leakage control that didn't rescue the claim.** TUEV/TUAB ⊂ TUEG (pretraining corpus). Removing them changed results by ≤0.0003. Useful as a template for how to *test* rather than argue leakage.
3. **"SOTA margins" are noise-level.** TUEV: CBraMod 0.6659 vs LaBraM 0.6616.
4. **Statistical thinness.** ±0.0066 reported on a **2-subject** test set (BCIC-IV-2a subjects 8–9). Seed SD ≠ generalization SD — third instance of this pattern across our three papers.
5. **Pretraining benefit is small when honestly measured.** Mixed-channel pretraining → FACED: +1.2 balanced acc. over random init (0.5351 vs 0.5232). Authors concede CBraMod is *not* "one-for-all"; it is a pretrained initialization fine-tuned per task.

## Judgment
- **Good engineering, incremental science, excellent review.** Unlike [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], the claims were forced down by reviewers rather than self-reported. Notably: an ICLR poster built from a recombination of CCNet + CPE + BIOT/LaBraM patch embeddings — so "module recombination" is not disqualifying per se. **Unsupported claims are.**
- **ACPE is the transferable idea.** Channel identity is reference-dependent (ear / average / REST / bipolar), so electrode-index embeddings are fragile. This is a real hazard for *our* connectivity work too: CTE-Net's edges changed almost completely under CAR (Jaccard 0.067).
- **On our target task it loses**: 0.64 AUROC on ADHD-Child, below a theta-envelope connectivity + GRU baseline.

## Vault Updates
- New opportunity: [[Unsupervised-Alignment-Leverage]] (2×2 decomposition, calibration-size curve, artifact interaction, interpretability trade-off).
- Standing hypothesis recorded: *the dominant cross-subject error term in pediatric ADHD EEG is per-subject signal geometry, not encoder capacity* — falsifiable with a 2×2 experiment on existing public data, no pretraining required.

## Questions to Investigate Next
- Does EA/Riemannian alignment transfer from MI (covariance-driven) to ADHD (diffuse/spectral)? If not, that is a clean negative result about task structure.
- Minimum calibration windows for stable alignment on 19-channel/128 Hz pediatric EEG?
- Does alignment improve *calibration* (ECE/Brier) as much as accuracy? If yes, it directly addresses the PPV problem — the number a clinician actually sees.
- Can the alignment gain survive the artifact ladder? (i.e. is it electrode/impedance geometry rather than neural scaling?)
