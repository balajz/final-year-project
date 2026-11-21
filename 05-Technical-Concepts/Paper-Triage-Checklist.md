---
tags:
  - technical-concept
  - methodology
  - literature-review
---

# Paper Triage Checklist (Intake Rubric)

Used for every new paper before it earns a note in `01-Research-Papers`. Purpose: keep analyses comparable, and stop the vault from accumulating "Model X on Dataset Y" entries that cannot become a project.

## Pass 0 — Is it worth a full note? (30 seconds)
- [ ] Does it contribute something other than a new block in a classifier? (dataset, task formulation, evaluation method, failure analysis, deployment constraint)
- [ ] Is the evaluation subject-disjoint, or does it need a leakage warning before anything else?
- [ ] Does it touch one of our open questions? (artifact dependence, calibration/PPV, timescale, reliability, personalization, event-locking)
- If all three are "no" → record one line in the session log and move on.

## Pass 1 — Extract (paper note sections 1–3)
- **Citation / code / dataset.** Code released? Dataset public and named, or "a private cohort"?
- **Problem formulation.** Classification, regression/index, detection, or workflow tool?
- **Method.** Only what is *load-bearing* — the one idea that would be lost if omitted.
- **Numbers, verbatim.** Accuracy, sensitivity, specificity, AUC, **PPV/NPV**, CIs, n, and the unit of evaluation.
- **Protocol.** Split type, fold count, seed count, selection procedure, thresholding.

## Pass 2 — Interrogate (section 4) — red flags in priority order
1. **Leakage:** window-level splits, scaler/PCA fit on all data, threshold or hyperparameters tuned on test → [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]].
2. **Artifact dependence:** no ICA/EOG/EMG handling on scalp EEG; performance reported without a cleaning-sensitivity check.
3. **Parsimony:** does a simple baseline tie or beat the contribution? If yes, the claim must be re-scoped to interpretability/reliability.
4. **Mechanism vs statistic:** does accuracy actually identify the claimed mechanism, or could the feature act as a generic window statistic? (see direction confounding in [[Kernel-Matrix-Based-Transfer-Entropy]]).
5. **Unpublished physical units:** lags in samples, filter cutoffs implied but unstated, effective sampling rate after pooling.
6. **Stability:** are the interpretability artefacts (edges, maps, saliency) stable across windows/subjects/references?
7. **Calibration & operating point:** Brier/reliability, PPV at realistic prevalence, decision curve, abstention.
8. **Confounds:** medication, age, sex, comorbidity, site — acknowledged, controlled, or ignored?
9. **Statistics:** multiple comparisons corrected? effect sizes? are seeds being treated as clinical units?
10. **Reproducibility:** code, hyperparameter table, compute budget, exact fold assignment.

## Pass 3 — Project relevance (section 5)
- What **decisive experiment** would this paper make possible or necessary?
- Does it supply a **dataset, task, or evaluation axis** we lack?
- Does it strengthen or weaken our **provisional dataset demotion** (121-child ADHD-Child = benchmark/audit only)?
- Draft one sentence: *"If this is true, then our project should ___."*

## Pass 4 — Log
- One file in `06-Research-Log` per session, linking every new note.
- Update `03-Research-Opportunities` only with **falsifiable** gaps (each with a minimal experiment).
- Touch `07-Decisions` only when a constraint or rejection actually changes.

## Connections
- [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]], [[Representation-Dispersion-and-Stability]], [[Kernel-Matrix-Based-Transfer-Entropy]]
- Applied to: [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Shen-2026-Brain4FMs-Benchmark]]
