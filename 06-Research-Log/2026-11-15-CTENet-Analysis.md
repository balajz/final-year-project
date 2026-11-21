---
tags:
  - research-log
  - adhd
  - connectivity
  - transfer-entropy
---

# Session Log: 2026-11-15 — CTE-Net (Sensors 2026) Analysis

## New Literature Added
- [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] (*Sensors*, Sep 2026) — Transformer contextualization + differentiable kernel transfer entropy on the **same 121-child IEEE DataPort cohort** as [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]].

## What the Paper Actually Establishes
1. **Participant-level 83.4% accuracy / 0.902 AUC**, window-level 80.9±1.7% accuracy, under 5 subject-wise folds × 10 seeds.
2. **The TE module does not significantly improve prediction** over mean pooling at participant level; removing the Transformer hurts most ($p_{\text{Holm}}=0.0117$).
3. **A 2017 ShallowConvNet ties or beats the full pipeline** on 7/8 metrics, with no significant McNemar difference.
4. **The TE representation is the most compact and most class-separable** of the four stages: −38.35% within-subject dispersion (76/120 children), stable across PCA 15/30/60 and PCA-free cosine.
5. **Preprocessing is decisive:** band-pass + quality screening drops 83.5% → 73.9% accuracy and 0.901 → 0.819 AUC. Reference choice rewrites edges (Jaccard 0.067).

## Our Synthesis
- This is a **representation-analysis paper wearing a classifier paper's clothes**. Its defensible contributions are the two-level evaluation discipline and the dispersion analysis; the architectural delta over TEKTE-Net is a Transformer front-end.
- The 0.90 AUC sits ~11 points above the best foundation model (REVE 0.79) and ~12 above the theta-envelope dFC model (0.777) on the identical cohort. Given that cleaning removes 8 AUC points, the **most parsimonious explanation is broadband/artifact structure**, not superior directed connectivity. This is now a concrete, falsifiable hypothesis (see [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]]).
- **Direction confounding:** because the Transformer output is projected back to channel space, every "channel" already contains all channels; TE asymmetry on top of that is partly manufactured by attention mixing. Accuracy therefore cannot be cited as evidence that directed connectivity is the mechanism.
- **Timescale mismatch:** TE lags are in samples of an unpublished effective rate; the swept range likely never reaches the theta cycle (125–250 ms) that dominates this cohort. Consistent with TE's weak predictive ablation and with the 81.6–89.8% spread in their own parameter sweep.
- **Reliability caveat:** top-10% edge Jaccard of 0.49 undercuts the very top-5% connectivity figures used as interpretability evidence.

## Concepts & Notes Created
- [[Kernel-Matrix-Based-Transfer-Entropy]] — estimator, TE decomposition, seven failure modes, validation checklist.
- [[Representation-Dispersion-and-Stability]] — metric definition, confound table (bandwidth, overlap, DOF, collapse), reliability upgrade (split-half ICC, permutation null).
- [[Nested-CV-and-Hyperparameter-Leakage]] — why "one config from mean validation accuracy across folds" leaks, severity scaling, correct procedures.
- [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]] — four concrete gaps with minimal decisive experiments.
- [[Candidate-Evidence-Aware-ADHD-Screening]] — candidate direction (status: not selected).

## Standing Conclusions
- The 121-child ADHD-Child cohort is **saturated**; it should be a benchmark/audit target, not the vehicle for a novel contribution.
- Model complexity is not buying accuracy on this cohort. The unresolved questions are **artifact dependence, calibration/PPV, timescale, and reliability** — not architecture.

## Questions to Investigate Next
- What does an artifact ladder actually do to a set of published ADHD-Child models? (Is there any model that *gains* when cleaned?)
- Are theta-scale, millisecond-parameterized TE features predictive where sub-theta broadband TE is not?
- Does split-half ICC tell the same story as "dispersion", or does the compactness effect vanish once bandwidth is matched?
- Access path and licensing for an external pediatric ADHD cohort (ADHD-200 / HBN) to test cross-dataset calibration.
