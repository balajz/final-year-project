---
tags:
  - project-idea
  - candidate
  - adhd
  - eeg
  - reliability
  - calibration
status: candidate-not-selected
---

# Candidate: Evidence-Aware ADHD Screening (Calibrated, Artifact-Audited, Abstaining)

> **Status: candidate, NOT selected standalone — ADOPTED AS A MODULE inside the C5 product layer (2026-11-16).** The abstention/calibration content of this note is now the Reliability panel of [[Candidate-C5-Reliability-Screening-Workbench]]. What is dropped from the product: nothing in the method, but the *standalone* pitch is retired (it was always rated "weakest standalone, strongest as a module"). See [[Decision-Log]] 27.

## 1. Real-World Problem
A clinician or researcher receives 1–3 minutes of scalp EEG from a child, contaminated to an unknown degree by blinks, drift, muscle and motion. Current papers return **one probability computed on one arbitrary recording segment**, with no calibration, no prevalence-aware operating point, and no statement of how much of the output is artifact. A 0.90 AUC cohort result is not usable at the point of care if the same model silently degrades to 0.74 after cleaning (see [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]).

## 2. Proposed Contribution
A **reliability layer** around ADHD-relevant EEG inference, with three testable claims:
1. **Artifact-invariance:** representations trained with artifact/quality augmentation and quality-conditioned gating retain performance under an artifact ladder (clean → realistic → injected), where standard models degrade.
2. **Participant-level calibration:** temperature/isotonic calibration + explicit PPV/NPV at 5% and 10% prevalence, plus a **decision-curve** analysis, so the output is an operating point rather than an accuracy.
3. **Selective prediction:** an "insufficient evidence" outcome driven by (a) estimated signal quality, (b) predictive uncertainty, (c) recording duration — evaluated with risk–coverage and selective-accuracy curves. The clinically valuable regime is high-coverage/high-NPV *rejection*, not perfect classification.

## 3. Why It Is Not "Model X on Dataset Y"
The supervised classifier is a **subcomponent**; the deliverable is a measurement protocol — how much of a screening claim survives artifact control, calibration, and abstention. It directly attacks the psychometric bottleneck (specificity/PPV) that the [[ADHD-Event-Locked-Connectivity-and-Leakage|vault's literature review]] identifies as the real ceiling, and it produces a reusable audit harness rather than a leaderboard entry.

## 4. Feasibility
- **Data:** ADHD-Child (121) as the primary benchmark; add at least one external cohort (e.g. ADHD-200 / Healthy Brain Network resting-state, or a second public pediatric set) for cross-dataset calibration honesty. Note: external ADHD-200 access requires a data-use agreement.
- **Compute:** small models (≤1M params) train in minutes on M-series; the artifact ladder multiplies evaluation, not training.
- **Risk:** the artifact-invariance claim may fail (models may rely on artifact structure). That failure is itself publishable as an audit result — the fallback deliverable is the harness + negative finding.

## 5. Evaluation Plan (non-negotiable hygiene)
- Nested or leave-one-site-out CV; report partition variance, not only seed variance ([[Nested-CV-and-Hyperparameter-Leakage]]).
- Participant-level primary metrics + calibration + PPV/NPV at realistic prevalence + risk–coverage.
- Artifact ladder + quality stratification + latency/throughput on CPU.
- Ablation: quality gating, augmentation, calibration, abstention each removed in turn.

## 6. Open Questions / Risks
- Is artifact-invariance learnable at 19 channels / 128 Hz, or does the cohort's information frontier (~0.79 AUROC — the current published subject-disjoint figure, Commitment 28) make the whole task too weak for a useful screening claim?
- Does the medication confound in this dataset (methylphenidate history, unknown status at acquisition) make *any* ADHD-specific claim unfalsifiable? If so, reframe as "EEG-based attention-state variability" rather than diagnosis.
- Would an event-locked formulation (see [[ADHD-Event-Locked-Connectivity-and-Leakage]]) dominate a window-based one, making the abstention layer a secondary contribution?

## 7. Decision Needed
Compare against the alternative of an **event-locked connectivity** project (opportunity 2 in [[ADHD-Event-Locked-Connectivity-and-Leakage]]) before committing. Both share the audit/data-hygiene backbone; they differ in whether the headline is *measurement reliability* or *temporal biomarker discovery*.
