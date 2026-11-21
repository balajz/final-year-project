---
tags:
  - research-area
  - personalization
  - domain-adaptation
  - calibration
---

# Personalization & Domain Adaptation

The deployment form of the vault's alignment thread. Named in the brief as a core method area; previously present only as a single opportunity note.

## 1. The Problem It Solves
Cross-subject and cross-session variability is the dominant error term in EEG decoding. The vault has the quantitative version of this claim:

- On BCIC-IV-2a, unsupervised per-subject alignment is worth **~14 accuracy points**, while swapping a simple conv net for a 4.9M-parameter foundation model is worth **~2–3** ([[Unsupervised-Alignment-Leverage]]).
- On the 121-child ADHD cohort, PSD features lose **21–24 points** when the split becomes subject-wise; a raw CNN loses **2.5** ([[Subject-Level-Evaluation-Hygiene]]).
- Session-to-session drift is typically *worse* than subject-to-subject drift, and is almost never benchmarked.

## 2. The Taxonomy
| Method | Requires | Data needed | Risk |
|---|---|---|---|
| **Subject-specific model** | Train per person | Many trials per person | Does not generalise; often the honest ceiling |
| **Per-subject normalisation** | Mean/std per channel | A few seconds | Removes scale, not geometry |
| **Euclidean / Riemannian alignment** | Mean covariance per subject | Unlabelled windows | **Transductive** — must be declared |
| **Domain-adversarial training** | Multiple source subjects | Large | Unstable; can remove diagnostic signal |
| **Test-time adaptation** | Unlabelled target data | Streaming | Legitimate only if framed as adaptation, not zero-shot |
| **Few-shot / meta-learning** | A handful of labelled trials per user | Small | Overfits with tiny support sets |
| **Continual learning** | Sequential sessions | Growing | Catastrophic forgetting |
| **Federated learning** | Multiple sites, data stays local | Infrastructure | Communication cost, non-IID clients |
| **Unsupervised personalisation** | Only unlabelled target data | Cheap | Hard to evaluate — no target labels |

## 3. The Axis Everyone Ignores: Calibration Budget
"Personalisation improves performance" is not a useful claim. The useful claim is a **curve**: performance as a function of calibration cost.

| Budget | Typical protocol | Question |
|---|---|---|
| 0 (zero-shot) | No target data | Is the model usable out of the box? |
| 5–10 windows | ~30 s of resting data | Can alignment alone fix it? |
| 20–40 trials | ~5 min of task | Standard BCI calibration |
| Full session | Labelled target data | Upper bound (supervised adaptation) |

Report the curve, not one point. This is the deployment-relevant metric, and it is rarely published.

## 4. Metrics That Actually Matter
- **Time-to-competence** — how long until the user reaches a usable performance level.
- **Performance at fixed calibration budget** — not at the best budget.
- **Negative transfer rate** — how often adaptation makes a subject *worse*. This is systematically underreported and is the single most important safety property.
- **Forgetting** — performance on earlier sessions after adapting to a new one.
- **Calibration robustness** — what happens when the calibration data is noisy or from a bad session.

## 5. Where This Connects to the Vault
1. **Alignment ≈ personalisation.** The Euclidean-alignment result is the cheapest personalisation method and the vault already has its effect size.
2. **The 1/f fingerprint** ([[Aperiodic-1f-Activity-and-Band-Ratios]] §4) predicts *which* personalisation is needed: if identity lives in `(χ, A)`, then aperiodic-aware normalisation may be a cheaper fix than full covariance alignment.
3. **Commitment 11** (equalise preprocessing before comparing architectures) is really a personalisation-budget rule: any comparison that gives one model more adaptation than another is measuring adaptation.
4. **Calibration and abstention** ([[Clinical-Deployment-and-Workflow]]) are the same problem seen from the clinician's side.

## 6. Open Problems Worth a Project
1. **Zero-calibration decoding** using only unsupervised structure — how far can it go before supervised calibration is required?
2. **Which personalisation, at what cost** — a head-to-head of normalisation vs alignment vs adaptation at matched budgets, on the same folds. Nobody has published this comparison cleanly.
3. **Negative-transfer prediction** — can we tell *before* adapting whether adaptation will help or hurt this subject? This is a genuinely novel and practically valuable question.
4. **Cross-device adaptation** — train on one amplifier, deploy on another.
5. **Privacy-preserving personalisation** — on-device adaptation without uploading EEG.

## 7. Risks
- **Transductive leakage framing.** Using unlabelled test-subject data to compute alignment is not label leakage, but it *is* transductive, and reviewers will ask. Declare it, and always report the strictly zero-shot baseline alongside.
- **Tiny per-subject data.** With 5 minutes per user, "adaptation" can be indistinguishable from "fitting noise." Report variance across users, not just the mean.
- **Benchmark monoculture.** Almost all adaptation results come from MI datasets. Whether they transfer to diffuse targets (ADHD, sleep, workload) is an open question — and a publishable negative result if they do not.

## 8. Connections
- [[Problem-Space-Map]] · [[BCI-Paradigms-and-Applications]] · [[Clinical-Deployment-and-Workflow]]
- Opportunities: [[Unsupervised-Alignment-Leverage]], [[Class-Correlated-Artifact-Control]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Aperiodic-1f-Activity-and-Band-Ratios]]
- Candidates: [[Candidate-Decoding-Multiverse-Aperiodic-Audit]]
