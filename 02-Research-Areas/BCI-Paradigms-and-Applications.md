---
tags:
  - research-area
  - bci
  - eeg
  - paradigms
---

# BCI Paradigms & Applications

The most under-covered direction in this vault, and the one with the strongest structural advantage: in a BCI, **the label comes from the experimental design, not from a clinician's judgement.**

## 1. Why BCI Is Structurally Easier Than Diagnosis
| Property | Clinical diagnosis (ADHD/ASD) | BCI paradigm |
|---|---|---|
| Label source | Interview, rating scale, judgement | The instruction given to the participant |
| Label noise | High, and heterogeneous across sites | Near zero (participant may fail to comply, but the label is still true) |
| Effect size | Small (|d| ≲ 0.2) | Large (μ/β ERD, P300 amplitude) |
| Acceptable to be subject-specific | No — must generalise | **Yes — per-user calibration is the normal design** |
| Failure mode | "The model learned the site" | "This user is BCI-illiterate" (an honest, measurable outcome) |

That last row is the key asymmetry. In diagnosis, subject-specific training is a sin. In BCI, it is the specification. Many of the vault's fiercest methodological constraints ([[Subject-Level-Evaluation-Hygiene]]) become easier to satisfy because the *within-subject* result is itself the target.

## 2. The Paradigms
| Paradigm | Signal | Typical performance | Latency | Calibration | Saturation |
|---|---|---|---|---|---|
| **Motor imagery (MI)** | μ/β event-related desynchronisation over sensorimotor cortex | 70–85% 2-class; ~60–70% 4-class | 2–4 s per decision | 20–40 trials/class | High but not exhausted |
| **P300 / ERP speller** | Positive deflection ~300 ms post-oddball | 90%+ character accuracy with averaging | ~2–3 s per character | Minutes | High (mature product space) |
| **SSVEP** | Steady-state response at flicker frequency | 90%+ with CCA-based decoders | <1 s | Minimal | High; limited by fatigue/photosensitivity |
| **cVEP** | Code-modulated visual evoked potential | Very high, short windows | <0.5 s | Minimal | Moderate |
| **ErrP** | Error-related potentials after a mistake | 70–85% single-trial | Post-decision | Small | Low — **under-explored** |
| **Passive BCI / workload** | Frontal theta, parietal alpha, aperiodic slope | Moderate | Continuous | None | **Low — open** |
| **Neurofeedback** | Volitional modulation of a band | Contested | Training-dependent | Substantial | High but weak evidence |
| **Imagined speech** | Sensorimotor/auditory cortex patterns | Near chance cross-subject | — | — | Open and hard |
| **Affective BCI** | Frontal asymmetry, spectral | Near chance cross-subject (DEAP ~0.51) | — | — | Open and hard |

## 3. Datasets (confidence: ✓ established, ~ verify)
- **BCI Competition IV 2a** ✓ — 9 subjects, 4 MI classes, 22 EEG + 3 EOG, 250 Hz. The vault already uses it ([[Unsupervised-Alignment-Leverage]]: +14 points from alignment).
- **BCI Competition IV 2b** ✓ — 9 subjects, 2-class MI, 3 bipolar channels. Small-channel, harder.
- **PhysioNet EEGMMIDB** ✓ — 109 subjects, 64 channels, 160 Hz, real + imagined movement. Large, but many subjects are noisy; useful for cross-subject scaling.
- **BCI Competition III / IVa** ✓ — 5 subjects, asynchronous MI.
- **SSVEP benchmark datasets (Nakanishi et al.)** ~ — 35 subjects, 40 targets.
- **ErrP datasets** ~ — several small ones; fragmented and not standardised.
- **DEAP** ✓ — 32 subjects, 40 music videos, 32 EEG + peripheral, 128 Hz. Affective; cross-subject performance near chance.
- **SEED / SEED-IV** ✓ — 15 subjects, film clips, 62 channels. Emotion; within-subject strong, cross-subject weak.

## 4. The Genuinely Open Problems
1. **Calibration-free / calibration-light BCI.** Every real system needs a per-user warm-up. How few trials suffice, and can alignment + transfer remove the warm-up entirely? This is the deployment form of [[Personalization-and-Domain-Adaptation]], and the vault already has the mechanism.
2. **BCI illiteracy prediction.** 15–30% of users cannot produce usable MI signals. Predicting *who* before a session — from resting EEG, aperiodic parameters, or a short calibration — is a useful, tractable, and rarely attempted problem.
3. **Cross-session transfer.** Non-stationarity across days is worse than across subjects. Most benchmarks are single-session, which is why reported numbers do not survive deployment.
4. **Error correction via ErrP.** A decoder that detects its own mistakes is more valuable than a slightly more accurate decoder. Under-explored relative to its practical value.
5. **Passive BCI for workload/fatigue.** Strong signal, immediate application (operators, drivers, students), no clinical ethics burden, and the aperiodic/1-f work transfers directly.
6. **Closed-loop / adaptive stimulation.** DBS, tACS, adaptive neurofeedback. Attractive but evaluation is confounded by placebo and expectancy — needs sham controls.

## 5. Why the Vault Should Care
- The alignment evidence (+14 points) was *measured on MI*, yet the vault has been trying to apply it to ADHD. **BCI is where that evidence was actually generated**, and where it is most likely to hold.
- BCI gives the vault's measurement tools (leakage audit, artifact control, calibration curves, specification curves) a target with large effect sizes — which means a positive result is achievable, not just a rigorous null.
- The brief explicitly names BCI. It has been absent from 43 notes.

## 6. Risks
- **Saturation at the benchmark level.** BCI-IV-2a has thousands of papers. Novelty must come from a deployment constraint (calibration, sessions, illiteracy), not from a decoder.
- **Hardware dependence.** Real BCI needs an amplifier; public datasets remove that requirement but also remove the deployment realism.
- **Small-n.** Most BCI datasets are 9–15 subjects. This is a genuine limit on statistical claims and must be stated.
- **Ethical framing.** Assistive BCI raises consent and autonomy questions that a final-year report may not be equipped to address seriously — pick applications where this is not the central issue (workload, error correction) if that is a concern.

## 7. Connections
- [[Problem-Space-Map]] · [[Neurological-Conditions-Landscape]] · [[Personalization-and-Domain-Adaptation]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Unsupervised-Alignment-Leverage]], [[Aperiodic-1f-Activity-and-Band-Ratios]]
- Papers: [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]], [[Shen-2026-Brain4FMs-Benchmark]]
