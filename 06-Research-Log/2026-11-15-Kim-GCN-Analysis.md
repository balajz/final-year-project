---
tags:
  - research-log
  - adhd
  - tic-disorder
  - xai
  - artifacts
  - gcn
---

# Session Log: 2026-11-15 — Kim et al. GCN / PGExplainer Analysis (Sixth Paper)

## New Literature Added
- [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]] — IEEE Access 2025. **Private** Dankook University Hospital cohort (55 children; 34 ADHD / 21 Tic; 32ch @ 250 Hz; IRB 2020-06-013). Not usable as our primary dataset.

## Why This Paper Matters Despite Its Flaws
It is the first paper in the vault that asks the **right clinical question**: ADHD *vs Tic disorder*, not ADHD vs healthy. That is the decision a child psychiatrist actually faces, and it is the only 2-class contrast we have seen where both classes are symptomatic. The vault's default framing (disease vs healthy, on a saturated 121-child cohort) is weaker than this one.

**Decision: import the formulation, discard the evidence.** Any version of it we build needs a public differential-diagnosis cohort; the Kim dataset is private and license-unreachable.

## The Two Tables Contradict Each Other — and Both Are Invalid
| Protocol | Winner | Problem |
|---|---|---|
| Fixed 100 epochs (Table 1) | GCN+FFT 85.46 vs 1D-CNN+FFT 47.41 (**+38 pp**) | Baselines untuned/under-trained at a fixed epoch count; comparison measures training schedule, not architecture |
| "Max accuracy over epochs" (Table 2) | 1D-CNN 92.82 vs GCN 92.07 | Maximum over the held-out fold's epoch trajectory = **test-set peeking** |

The abstract's "at least 20% higher accuracy than any other neural network model" is a statement about Table 1 only, and Table 1 is an artifact of crippling the baselines. Table 2 reverses the ranking. **Neither table supports a model comparison** — the paper's headline claim does not survive its own supplementary protocol.

This is a clean, teachable case for [[Paper-Triage-Checklist]]: two protocols, opposite winners, no seed repetitions, 36 cells, one reported winner, SD ≈ 17–34 pp.

## The Attribution of Attrition Is Impossible as Stated
- 34 ADHD → 21 ADHD (38% dropped); 21 Tic → 21 Tic (0% dropped).
- But 55 × 72 = 3,960 and 42 × 72 = 3,024 exactly ⇒ **zero epochs rejected** by the stated >100 µV / <5 µV rule.
- Therefore the stated >50%-epoch-rejection rule cannot have produced the 13 exclusions. Either the accounting is wrong or the exclusions were for unreported reasons.
- Direction of bias is the worst possible one: if the rule did operate, it removed the **noisiest ADHD children** — exactly the cases a noise-robustness claim must survive. New commitment logged (14).

## The Claim That Fails Most Instructively: "Noise-Robust Interpretability"
Their argument: important channels are the same with and without ICA ⇒ the model reads neural structure. Problems, in order of severity:

1. **Wrong axis.** They defend against the artifact explanation by noting hyperactivity is heterogeneous *across individuals*. Class-correlated artifact needs no within-person consistency — it needs a between-group difference in motion/blink/EMG statistics, which two hyperactive disorders almost certainly have. → [[Class-Correlated-Artifact-Control]].
2. **No rank correlation computed.** Table 3 contains both raw and denoised rankings; the raw-vs-denoised agreement is asserted *visually*. (Top-10 cumulative-scoring: Oz, O1, O2, Pz, P3, P4 overlap; AF4, C4, P8, T8 vs F4, T7, F7 differ.)
3. **Stability was low and the null was invalid.** W = 0.149–0.280, called "significantly consistent" on a χ² test that assumes independent raters — but the 7 CV runs share training subjects. → [[Explanation-Stability-and-Faithfulness]].
4. **The validation target is shared, not discriminative.** The highlighted fronto-occipital pattern is documented in *both* disorders (their own citations say so). A shared feature cannot be the discriminative one. Validating a *discriminative* explanation against *each disorder's* pathology is a category error.

## The One Genuinely Interesting Result
Rankings from **raw** data were *more* concordant across folds than rankings from **denoised** data (higher W, more often above the permutation baseline). The authors offer two explanations (over-aggressive ICA; denoising amplifies subject-specific structure). A third fits our vault better:

> ICA removes components that are shared across subjects. What remains stable across folds in raw data may therefore be a **common artifact/recording structure**, not a common neural one.

That is falsifiable with the battery in [[Class-Correlated-Artifact-Control]] §3, and if true it inverts the paper's central claim: their "noise-robust interpretability" is stable *because* it is artifact-driven.

## Channel Pruning Reproduces the Leakage Pattern
Rankings "from all CV runs" aggregate across every fold, then are evaluated on those same folds → circular. That variant shows a significant accuracy-vs-channels trend (F = 13.6–21.6, p ≤ 0.001). The **honest per-fold variant shows no significant trend** (p = 0.46 / 0.13 / 0.073). The paper concludes the leaky variant is "more effective." This is a textbook instance of [[Nested-CV-and-Hyperparameter-Leakage]], now with a second independent example.

## What It Adds to the Vault
1. **Differential-diagnosis framing** — the best problem statement we have, now recorded as a candidate axis.
2. **Paired raw/denoised design** — the artifact ladder, independently invented (matches [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]] §1).
3. **Quantified XAI stability** — first paper in the vault to report a reliability statistic for explanations; the metric and its pitfalls are now formalized.
4. **A third artifact-dependence datapoint** (with CTE-Net and CBraMod) ⇒ the pattern is systematic.
5. **A testable inversion:** stable raw-data attributions may be artifact-stable.

## Synthesis Across Six Papers
- The **leakage gap is quantified** (PSD −21/−24 pp; raw CNN −2.5 pp).
- **Architecture is not the lever** (four independent instances now: ShallowConvNet ≈ CTE-Net; CNN > CNN–BiLSTM; CBraMod < theta-GRU; Kim's own two tables contradict).
- **The levers are:** per-subject signal geometry (alignment), artifact/EMG band control, class-conditional attribution, honest partitions, participant-level calibration.
- **New:** the *formulation* is also a lever. ADHD-vs-Tic ≫ ADHD-vs-healthy in clinical value, and it may be more tractable because both classes are symptomatic (the "both are noisy" objection is a feature if artifact control is done properly).

## Next Question
Two candidates, both cheap and both on public data:
1. Does **Euclidean alignment** recover the PSD pipeline's 24-point leak on the 121-child cohort? ([[Unsupervised-Alignment-Leverage]])
2. Does an **artifact-only classifier** beat chance on the public ADHD cohort — i.e. is the label already confounded with recording quality? ([[Class-Correlated-Artifact-Control]] §3.1)

(2) is cheaper and it gates everything else: if the answer is yes, every alignment/AUC number we have collected needs re-reading. Run (2) first.
