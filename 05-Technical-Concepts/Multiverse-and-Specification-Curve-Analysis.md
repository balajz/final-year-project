---
tags:
  - technical-concept
  - methodology
  - statistics
  - reproducibility
  - evaluation
---

# Multiverse & Specification-Curve Analysis (Researcher Degrees of Freedom, Quantified)

Derived from [[Troendle-2026-TBR-Multiverse-HBN]]; connects to [[Nested-CV-and-Hyperparameter-Leakage]] and [[Subject-Level-Evaluation-Hygiene]].

## 1. What It Is
Instead of running one pipeline and reporting one p-value, enumerate **every defensible combination** of analytical choices (reference, filter, band definition, ROI, covariate set, inclusion criteria) and report the *distribution* of results across the resulting **universes**.

- **Specification curve:** sort the universes by effect size, plot each estimate with its CI, and beneath it a barcode of the choices that produced it (Simonsohn, Simmons & Nelson 2020).
- **Possibility space:** the 2-D map of which choice combinations produce significant vs null results.
- **Inference across the multiverse:** Simonsohn et al.'s joint bootstrap — resample subjects, recompute the *whole* multiverse, count the fraction of resamples in which the median effect is at least as extreme. Gives one multiverse-adjusted p-value.

**Core insight:** the multiverse does not *create* flexibility, it *reveals* it. A finding that survives all defensible specifications is strong; a finding that exists in 3 of 576 is a specification artefact. Crucially, **a uniformly null multiverse is also informative** — it bounds the effect size.

## 2. Why It Fits Our Vault Exactly
Every critique we have written is a single-path version of this problem: one paper chose one preprocessing, one split, one threshold, and reported one number. Multiverse analysis is the **generalised form of the audit** we have been doing paper-by-paper. It also converts our rhetorical worry ("this could be an artefact of their choices") into a measured quantity.

## 3. Failure Modes (the paper we learned it from has several)
| Failure | Why it invalidates the claim | Fix |
|---|---|---|
| **Post-hoc subsetting** | Filtering the multiverse to the universes that were significant, then reporting the proportion within that subset | Report whole-multiverse proportions; use subsets only descriptively, never as evidence |
| **Binomial test on correlated universes** | Universes share subjects; the count of significant results is over-dispersed relative to Binomial(n, 0.05) → p-values too small | **Permute the group label and re-run the entire multiverse**; use that distribution as the null |
| **p-count as the outcome** | Discards magnitude; "significant in 46/48" can coexist with |d| = 0.1 | Report median effect + IQR across universes, plus the effect-size distribution |
| **Maximal interaction model, reported term-by-term** | Lower-order terms become conditional effects at reference covariate values, not marginal effects | Include covariate-free universes (as Troendle et al. do) or report marginal means |
| **Treating one specification as ground truth** | "Aperiodic-adjusted" is assumed clean; it is itself artefact-sensitive | Never privilege one universe as truth; report the ordering of universes and what it implies |
| **Computational blow-up** | 576 × nested CV × deep models is infeasible | Use cheap, fast models (linear/kernel on static features); the *metric* is the contribution, not the model |

## 4. The Missing Generalisation: Decoding Multiverses
Every published multiverse we have found audits an **association** (a regression coefficient). Nobody audits **discrimination** — a specification curve of AUC / balanced accuracy / calibration for a classifier. That is the natural target for us, because:
1. It is what the clinical claim actually is ("this detects ADHD").
2. It forces **subject-disjoint folds inside every universe** (removing the leakage path entirely).
3. It lets us express the effect of analytic choice in the units clinicians care about (AUC points, sensitivity at fixed specificity).
4. It is cheap: 24–72 universes × nested group CV × logistic regression on band-power/aperiodic features is minutes on a laptop.

→ [[Decoding-Multiverse-and-Aperiodic-Identity]]

## 5. Minimum Reporting Standard for Our Project
1. Pre-register the specification space and the universe count; justify each dimension from the literature (not from the results).
2. Report **all** universes; never a filtered subset as the headline.
3. Report the effect/performance distribution, not only p-value counts.
4. Include a **permutation-of-the-multiverse null**.
5. Include at least one degenerate specification (e.g. no covariate adjustment) so conditional effects can be compared to marginal ones.
6. Release code and the universe table.

## 6. Connections
- Papers: [[Troendle-2026-TBR-Multiverse-HBN]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]], [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]
- Concepts: [[Nested-CV-and-Hyperparameter-Leakage]], [[Subject-Level-Evaluation-Hygiene]], [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Paper-Triage-Checklist]]
- Opportunities: [[Decoding-Multiverse-and-Aperiodic-Identity]]
