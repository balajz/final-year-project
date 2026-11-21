---
tags:
  - project-idea
  - candidate
  - adhd
  - eeg
  - event-locked
  - hbn
status: candidate-not-selected
---

# Candidate: Event-Locked Neuro-Behavioral Decoding Across Active vs. Passive Paradigms (HBN-EEG)

> **Status: candidate, NOT selected.** Derived from [[ADHD-Event-Locked-Connectivity-and-Leakage]], [[Shen-2026-Brain4FMs-Benchmark]], and the newly verified [HBN-EEG BIDS/HED releases](https://neuromechanist.github.io/data/hbn/).

## 1. Real-World Problem
Resting-state EEG is a weak probe for attention disorders because attention lapses are **transient and task-provoked**. Meanwhile, even when EEG is recorded during cognitive tasks (like the visual counting task in the 121-child dataset), existing ML pipelines slice blind 4-second windows that ignore stimulus onset, response latency, and error trials—washing out millisecond-scale attentional dynamics.

## 2. Newly Verified Data Lever: HBN-EEG BIDS + HED (NEMAR / S3)
Unlike the 121-child CSV (which stripped all stimulus/response timestamps), the public **HBN-EEG** releases (`ds005505`–`ds005512`, `ds005514`–`ds005516`; **no DUA**) include **6 tasks per child** with millisecond-precise **Hierarchical Event Descriptors (HED)** and behavioural button-press logs:
- **3 Passive Tasks:** Resting State (eyes open/closed cues), Surround Suppression (SSVEP flickering disks), Movie Watching.
- **3 Active Tasks:** **Contrast Change Detection (CCD)** (sustained attention + response time + feedback), **Sequence Learning**, and **Symbol Search**.
- **Built-in Targets:** Orthogonal psychopathology dimensions from the Child Behavior Checklist (CBCL: **Attention**, **Externalizing**, **Internalizing**, **p-factor**) + age/sex are included directly in the participant metadata without waiting for a restricted clinical DUA.

> **Access verified 2026-11-15** (HBN-EEG platform documentation; full detail in [[Healthy-Brain-Network-HBN]]): 11 releases, **2,782 subject-records**, **~1.9 TB total**, **91–245 GB per release**, and **20-subject / 100 Hz mini sets per release**. The mini set is the right first target — a full release does not fit a laptop workflow.

## 3. Core AI & Scientific Contribution
A **paradigm-contrast and event-synchronized neuro-behavioral architecture** that tests a concrete neuroscientific hypothesis:
1. **Passive vs. Active Paradigm Contrast:** Does cross-subject decoding of the CBCL Attention factor (and ADHD status) improve when moving from passive Resting State to event-locked active attention trials (**Contrast Change Detection** / **Symbol Search**) within the *exact same children*?
2. **Event-Locked Neural + Behavioral Fusion:** Instead of blind sliding windows, lock EEG representations (aperiodic-corrected time-frequency / dFC + Euclidean Alignment) to **stimulus onset and button-press reaction-time (RT) variability** (e.g., contrasting fast-hit, slow-hit/attentional-lapse, and false-alarm trials).
3. **Transdiagnostic Specificity Check:** Because HBN-EEG provides four orthogonal CBCL dimensions (Attention vs. Internalizing vs. Externalizing), we can test **differential specificity**—proving whether the model actually decodes *attention* deficits or merely generic psychopathology/hyperactive movement (`Externalizing`).

## 4. Why It Beats "Model X on Dataset Y"
- Solves two major vault bottlenecks simultaneously:
  1. **Event-blind windowing** ([[ADHD-Event-Locked-Connectivity-and-Leakage]] §2).
  2. **Differential diagnosis / specificity** ([[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]): instead of relying on a private hospital Tic dataset, HBN's orthogonal CBCL factors (`Attention` vs. `Externalizing` vs. `Internalizing`) let us test differential specificity on 2,000+ public subjects immediately.
- Gives a strong, constructive AI/ML engineering component (event-locked spatio-temporal encoding + behavioral RT variability modeling + cross-subject alignment) while keeping all 20 methodological guardrails from [[Decision-Log]].

## 5. Feasibility & Risks
- **Data:** Immediately downloadable, no DUA. Release 1 (`ds005505`) = **136 subjects**; later releases 134–381 each; eleven releases totalling 2,782 subject-records and ~1.9 TB. **Start from a 20-subject 100 Hz mini set**, then scale by selective S3 download rather than whole releases ([[Healthy-Brain-Network-HBN]] §5).
- **Compute:** Event-locked trials around button presses are compact (1–3 s epochs per trial), making training fast on local Apple Silicon.
- **Risk:** Active tasks introduce motor-response and eye-movement artifacts around the button press; requires strict pre-stimulus vs. post-stimulus window separation and the [[Class-Correlated-Artifact-Control]] battery.

## 6. Open Questions Before This Can Be Selected
1. **Trial counts.** How many usable CCD / Symbol Search trials per child survive rejection? Event-locked analyses die on small n.
2. **Age range per task.** HBN task batteries differ by age band; a task available for 6–11 y may be missing for 15–21 y, which would confound "paradigm" with "age."
3. **Label definition.** CBCL Attention is a *dimensional* parent-report score, not a diagnosis. A high decoding AUC on CBCL-Attention is not an ADHD classifier, and must not be reported as one.
4. **Movement.** Button presses are movement. The pre-stimulus window is the only clean one; post-response windows are contaminated by the response itself. This is the central methodological risk.
5. **Competing-candidate comparison.** Whatever advantage the active paradigm shows must be measured *within the same children* against the resting-state baseline on identical folds — otherwise it is a cohort difference, not a paradigm effect.

## 7. Competing Candidates (none selected)
- [[Candidate-Decoding-Multiverse-Aperiodic-Audit]] — specification-curve audit of decoding on the resting-state releases.
- [[Candidate-Evidence-Aware-ADHD-Screening]] — calibration/abstention framing.

## 8. Connections
- Opportunities: [[ADHD-Event-Locked-Connectivity-and-Leakage]], [[Class-Correlated-Artifact-Control]]
- Datasets: [[Healthy-Brain-Network-HBN]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Aperiodic-1f-Activity-and-Band-Ratios]]
- Decisions: [[Decision-Log]]
