---
tags:
  - research-opportunity
  - adhd
  - eeg
  - generalization
---

# Research Opportunities: Event-Locked Connectivity & Honest EEG Generalization

Derived from critical analysis of [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]].

## 1. True Graph-Topology-Preserving Spatio-Temporal Modeling
- **Gap:** Baibulova et al. (2026) flatten the $19 \times 19$ connectivity matrix into a 171-D vector for their Transformer+GRU, losing explicit node/electrode spatial topology. Meanwhile, their GCN baseline loses edge-level attention.
- **Opportunity:** Investigate architectures that genuinely preserve both spatial graph structure (e.g., dynamic graph attention over 10–20 electrode coordinates) and multi-scale temporal dynamics, while testing whether true graph structure actually beats vectorized edges under strict [[Subject-Level-Evaluation-Hygiene]].

## 2. Task-/Stimulus-Synchronized Dynamic Connectivity
- **Gap:** Even when EEG is recorded during a cognitive task (such as visual counting in the IEEE DataPort ADHD dataset), sliding-window dFC is typically computed blindly without aligning windows to stimulus presentation, response times, or error trials.
- **Opportunity:** Aligning dynamic connectivity transitions to behavioral/cognitive events—or modeling EEG alongside behavioral/response-time streams—could isolate transient attentional lapses that blind sliding windows average out.

## 3. Addressing the Cross-Subject Generalization Ceiling (AUC ~0.74–0.78)
- **Observation:** Under leak-free evaluation, single-modality scalp EEG connectivity alone hits a performance ceiling (~63%–72% accuracy, 44%–62% specificity) with wide confidence intervals on small cohorts.
- **Opportunity:** Rather than chasing marginal +2% accuracy gains on a 121-subject CSV, explore:
  - Self-supervised pretraining / EEG foundation models for better cross-subject representations.
  - Domain adaptation / test-time personalization to handle inter-subject variability.
  - Multimodal fusion (e.g., EEG + behavioral/eye-tracking/physiological wearables) or workflow-oriented tools (e.g., artifact/quality auditing, uncertainty quantification, human-in-the-loop triage) where ~80% sensitivity + high NPV is genuinely useful.

## 4. Temporal-Scale Calibration of Directed Connectivity
- **Gap:** Directed-connectivity estimates are usually parameterized by *sample* lags whose effective sampling rate is unpublished, and the swept ranges often never reach the theta cycle (125–250 ms) that carries most ADHD-relevant coupling on this cohort.
- **Opportunity:** Millisecond-parameterized, band-resolved TE (analytic-envelope inputs, lag distributions rather than a single lag), validated by lag recovery on synthetic coupled oscillators before being applied to EEG.
- **Detail:** [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]] (also covers artifact-dependence auditing and bandwidth-matched reliability controls, motivated by [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]).
