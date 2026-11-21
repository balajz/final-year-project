---
tags:
  - technical-concept
  - evaluation
  - data-leakage
  - cross-validation
---

# Nested CV & Hyperparameter Selection Leakage

Companion to [[Subject-Level-Evaluation-Hygiene]]. That note covers **splitting by subject**; this one covers the second, subtler leak: **splitting by model-selection round**.

## 1. The Failure Mode
Cross-validation is only unbiased if everything that influenced the model — architecture, hyperparameters, thresholds, epoch count, feature basis — was chosen **without seeing the test fold**.

Common violation: run 5-fold CV, compute validation accuracy in every fold, pick the configuration that maximizes the **mean** validation accuracy, then report test metrics from that same CV run.

Why it leaks: because each participant is test in one fold, the selection objective depends (weakly) on the labels of the test participants of *other* folds. The reported test scores are therefore **optimistically biased** — usually by 1–3 points, and much more when the search space is large or the cohort small.

This is exactly the residual issue in [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]: one config from 20 Optuna trials, scored on mean validation accuracy across the five predefined folds, then frozen and evaluated on those folds.

## 2. Severity Scales With
- Number of trials × number of validation subjects (search pressure)
- Cohort size ($n=120$ → 24 test children per fold)
- Whether the same folds are reused for every seed (CTE-Net: yes → removes partition variance)

## 3. Correct Procedures
1. **Nested CV:** inner loop (hyperparameter search) inside each outer training partition; outer test partition untouched until the end. Cost ≈ $k_{outer} \times k_{inner} \times$ trials.
2. **Cheap alternative — held-out final test:** do all selection on a CV/train pool, freeze, evaluate **once** on a never-touched subject set. Report that single number as primary.
3. **Repeated CV with different partitions:** gives partition variance; nest the bootstrapping over both participants and partitions.
4. **Pre-registration of the search space** and reporting the **selection surface** (validation accuracy distribution across trials), not only the winner.

## 4. Reporting Checklist
- [ ] Where was each decision (arch, LR, epochs, threshold, PCA dim, TE lags) made?
- [ ] Are reported CIs conditional on a single partition? Say so explicitly.
- [ ] Is the number of models trained ≥ number of reported scores? (10 seeds × 5 folds = 50 fits; the participant-level metric is still one partition.)
- [ ] If selection is not nested, quantify the optimism: e.g. re-run the top-$k$ configs and report spread.
- [ ] Distinguish **seed variance** (optimization) from **partition variance** (generalization). Only the latter supports clinical claims.

## 5. Connection to the Vault's Guardrails
The [[Decision-Log]] now requires nested or explicitly corrected selection for any generalisation claim. Seed-level Wilcoxon tests are treated as **optimization stability**, never as evidence of clinical generalization — the position CTE-Net itself adopts, which is the correct one.

## 6. Connections
- Papers: [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Representation-Dispersion-and-Stability]]
