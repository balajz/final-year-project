---
tags:
  - technical-concept
  - xai
  - reliability
  - evaluation
---

# Explanation Stability & Faithfulness (XAI Metrics That Actually Test Something)

Derived from the explanation analysis in [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]; cross-referenced against the SHAP analysis in [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]].

## 1. Two Different Questions, Routinely Conflated
| Question | Name | Failure it catches |
|---|---|---|
| Does the explanation **agree across runs/folds**? | **Stability** (reliability) | The model is finding different channels each time → no learned mechanism |
| Does the explanation **actually drive the prediction**? | **Faithfulness** (fidelity) | The explanation is a plausible-looking post-hoc story unrelated to the computation |
| Does the explanation match **known neurophysiology**? | **Plausibility** | The explanation is stable and faithful but biologically meaningless |

Stability (Kim's Kendall's W) says nothing about faithfulness. A model that has learned a single artifact channel will produce a *highly stable* explanation for it. **Stability is necessary, never sufficient.**

## 2. Why Stability Alone Is a Trap for Artifact Claims
Kim et al. report Kendall's W = 0.149 / 0.224 / 0.280 across 7 CV runs and treat it as evidence of "noise-robust interpretability," because raw and denoised data highlight the same occipital + right-frontal channels.

Three alternative explanations survive:
1. **Artifact-driven stability.** ICA removes subject-specific components; what remains shared across subjects in raw data is often *common recording structure* (drift, line noise, cap geometry, common-reference field). A stable explanation can therefore be stable *because* it is artifact-driven.
2. **Topography bias.** Attributed importance is mapped through cap geometry. Neighboring electrodes share variance, so any smooth attribution method will produce regional agreement independent of mechanism.
3. **Task-shared structure.** Both classes are hyperactive children resting in the same room; whatever distinguishes "child in a hospital" from "child at rest" is shared by both classes and cannot be discriminative.

The design that would rule these out is in [[Class-Correlated-Artifact-Control]].

## 3. What Each Metric Buys You
- **Kendall's W** (coefficient of concordance): agreement of channel *rankings* across raters (folds/seeds). Range 0–1; report the **permutation baseline W**, not just the χ² p-value — with n=32 items, W≈0.15 can be "significant" while barely above chance.
- **Rank correlation across conditions** (Spearman ρ between raw and denoised rankings): the direct test of "same channels with and without noise." If both lists exist in a table, compute it; do not eyeball the top-10.
- **Deletion / insertion curves**: remove the top-k attributed features and measure the drop in the *model's* output; compare with a random-k control. This is faithfulness and it is cheap.
- **Sufficiency / comprehensiveness** (ERASER-style, adapted to channels): does the attributed subset alone reproduce the prediction, and does removing it destroy it?
- **Label-permutation control**: retrain on shuffled labels; a faithful explainer of a null model should produce diffuse, unstable attributions. If it produces the same topography, the attribution is prior-driven.

## 4. The Independence Violation to Watch
Kim's 7 CV runs share training subjects (each fold holds out 3 + 3; the rest overlap). Kendall's W assumes **independent raters**, so the χ² null is invalid and the agreement is inflated relative to a genuinely independent replication. The correct design is **disjoint-fold explanations** or nested-CV explanations scored on held-out subjects.

## 5. Class-Conditional Attribution (the missing analysis)
For a two-disorder contrast, the relevant question is not "which channels matter" but "which channels matter **for the difference**." Report attributions separately per class, then test whether the class-conditional maps differ (permutation test on the attribution distance). A fronto-occipital map shared by ADHD and Tic is, by construction, not the discriminative feature — yet validating it against *each disorder's* pathology is the standard move in this literature. That validation is logically independent of the classification claim.

## 6. Minimum Reporting Standard for Our Project
1. Stability: W (or ICC) with permutation baseline, computed on **disjoint** folds, plus raw-vs-clean rank correlation.
2. Faithfulness: deletion/insertion curves with random-k controls.
3. Specificity: label-permutation and class-conditional comparison.
4. Plausibility: last, and explicitly labelled as interpretive, not evidential.
5. Never present a topography as validation of a mechanism without (1)–(3).

## 7. Connections
- Papers: [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Representation-Dispersion-and-Stability]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Opportunities: [[Class-Correlated-Artifact-Control]]
