---
tags:
  - research-area
  - multimodal
  - wearable
  - eeg
---

# Multimodal Physiological Signals & Wearables

Named in the brief, absent from the vault until now.

## 1. The Modalities
| Modality | What it measures | Sampling | Cost | EEG-specific role |
|---|---|---|---|---|
| **EEG** | Cortical potentials | 128–1000 Hz | Low–moderate | Target signal |
| **EOG** | Eye movement / blinks | 128–250 Hz | Low | **Nuisance and signal** (gaze, sleep onset) |
| **EMG** | Muscle activity | 250–2000 Hz | Low | Nuisance for EEG; signal for sleep, stress, effort |
| **ECG / HRV** | Cardiac rhythm | 250–500 Hz | Low | Arousal, stress, sleep, seizure-associated tachycardia |
| **PPG / SpO₂** | Pulse, oxygenation | 25–100 Hz | Very low | Sleep apnea, wearable-friendly |
| **EDA** | Skin conductance | 4–32 Hz | Very low | Sympathetic arousal |
| **Respiration** | Breathing rate/effort | 1–32 Hz | Low | Sleep staging, panic, apnea |
| **Accelerometer** | Movement | 25–100 Hz | ~zero (in phone/watch) | **The artifact covariate that should be measured and never is** |
| **Behavioural** | Reaction time, accuracy, keystrokes | Event-based | Free | The label in most cognitive paradigms |

## 2. Why Multimodal Is the Obvious Next Step Here
The vault's central empirical finding is that **artifacts and analytic choices dominate ADHD-EEG results** ([[Class-Correlated-Artifact-Control]], [[Troendle-2026-TBR-Multiverse-HBN]]). Almost every one of those confounds is *directly measurable* with a cheap second channel:
- Movement → accelerometer
- Muscle → EMG
- Blinks → EOG
- Arousal → HRV/EDA

A model that predicts the label from EEG **and** reports how much of its decision is explained by the accelerometer is a qualitatively better artifact control than any post-hoc cleaning ladder. That is a concrete, cheap, high-value use of multimodality that does not require fusion architecture research.

> **The one multimodal paper in the vault is a caution, not a template.** [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]] fuses rs-fMRI + sMRI + demographics on ADHD-200 and ABIDE; in its strictest setting, adding sMRI to fMRI + demographics is **not** significant, unimodal sMRI is ~54% three-class, and the highest fusion weight lands on demographics — which is plausibly a cohort/site proxy ([[Cohort-and-Site-Confounding]]). Fusion can add parameters, cost and confounds without adding information. Always report per-modality ablations and a single-modality baseline.

## 3. Fusion Strategies (and their failure modes)
| Strategy | How | Failure mode |
|---|---|---|
| **Early / feature-level** | Concatenate features | Scale mismatch; one modality dominates |
| **Intermediate** | Joint embedding, attention across modalities | Needs more data than a final-year project usually has |
| **Late / decision-level** | Weighted average of per-modality predictions | Ignores cross-modal interactions |
| **Gated / reliability-aware** | Learn per-sample modality weights | **Underexplored and most practically useful** — it degrades gracefully when a sensor fails |
| **Distillation** | Train on rich multimodal data, deploy on cheap single modality | Requires paired data; teacher's confounds are inherited |
| **Missing-modality training** | Random dropout of modalities during training | Should be standard, rarely is |

**Modality collapse** is the characteristic failure: the model uses one channel and ignores the rest, so the extra sensors add cost without adding information. Always report per-modality ablations and a single-modality baseline.

## 4. Wearable Form Factors
| Form | Channels | Signal quality | Maturity | Notes |
|---|---|---|---|---|
| **Ear-EEG (in-ear / behind-ear)** | 1–4 | Moderate | Emerging | Best comfort/quality trade-off; sleep and seizure monitoring |
| **Dry-electrode headband** | 2–8 | Moderate | Commercial | Consumer sleep/focus devices |
| **Behind-the-ear + mastoid** | 2–6 | Moderate–good | Emerging | Hearing-aid integration path |
| **Textile/cap dry arrays** | 8–32 | Moderate | Research | Higher channel count, worse contact |
| **Single-channel forehead** | 1 | Low | Consumer | Mostly useless for anything subtle; useful for sleep staging |

The hard problems are **motion artifact**, **electrode–skin impedance drift over hours**, **user compliance**, and **the absence of a reference** (a single ear channel has no spatial information at all).

## 5. Datasets (confidence: ✓ established, ~ verify)
- **WESAD** ✓ — 15 subjects, wrist + chest (EDA, ECG, PPG, temperature, accelerometer) under stress/amusement/baseline. Multimodal but no EEG.
- **DEAP** ✓ — EEG + peripheral (GSR, HR, respiration, temperature, video) during affective video. One of the few true EEG+autonomic sets.
- **Sleep-EDF Expanded** ✓ — EEG + EOG + EMG + respiration, whole nights. Multimodal by construction.
- **HBN** ✓ — EEG plus a large behavioural/psychiatric battery; possibly other physiological streams (verify).
- **SHHS** ~ — polysomnography at scale, research access.
- **ABCD** ~ — very large, longitudinal, includes some physiological measures; access is restricted.
- **UK Biobank** ~ — wearable accelerometer at scale; not EEG.
- **PhysioNet challenge corpora** ~ — several multimodal ICU/wearable sets.

## 6. Open Problems Worth a Project
1. **Artifact-aware decoding** — use a second channel as a *measured confound* rather than an additional feature. (Cheapest, most defensible, ties directly into the vault.)
2. **Reliability-gated fusion** — down-weight a modality when its quality drops. Deployable, poorly studied.
3. **Distillation to a wearable** — can a lab-grade 128-channel result be approximated by an ear-EEG? This is a real product question and a clean experimental design.
4. **Missing-modality robustness** — train with dropout so that a device losing a sensor degrades rather than fails.
5. **Cross-device generalization** — train on one amplifier, test on another. Almost never reported, and it is the reason most published models do not transfer.

## 7. Risks
- **Paired multimodal EEG data is scarce.** Most public multimodal sets are either EEG-only or autonomic-only; true synchronised EEG+wearable corpora are rare and usually proprietary.
- **Synchronisation and clock drift** between devices is a real engineering burden that eats project time.
- **Fusion can hide a weak target.** A multimodal model on an ill-posed target produces a better-looking number, not a better answer.

## 8. Connections
- [[Problem-Space-Map]] · [[Neurological-Conditions-Landscape]] · [[Clinical-Deployment-and-Workflow]]
- Opportunities: [[Class-Correlated-Artifact-Control]] — multimodal sensing is the cleanest way to satisfy commitment 14
- Concepts: [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Subject-Level-Evaluation-Hygiene]]
