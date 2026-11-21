---
tags:
  - research-area
  - epilepsy
  - sleep
  - asd
  - adhd
  - datasets
---

# Neurological Conditions Landscape (EEG-Addressable, Ranked by Well-Posedness)

Confidence markers: **✓** well-established · **~** approximate, verify before relying on it.

## 1. The Ranking That Matters
Ordered by *how well-posed the AI problem is*, not by prevalence or clinical importance.

| # | Target | EEG signature | Ground truth | Data | Saturation | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Sleep staging** | Stage-specific spectra, spindles, K-complexes, slow waves | AASM rules, high inter-rater agreement | Abundant ✓ | Moderate | Best-posed; deployment real |
| 2 | **Seizure detection** | Rhythmic spike-wave, evolving amplitude/frequency | EEG-visible, unambiguous | Abundant ✓ | **Very high** | Well-posed but crowded + FDA-cleared devices |
| 3 | **Motor imagery / BCI** | μ/β ERD-ERS over sensorimotor cortex | The instruction is the label | Abundant ✓ | High | Well-posed; calibration is legitimate |
| 4 | **Sleep disorders (apnea, narcolepsy)** | Respiratory coupling, sleep architecture | PSG + respiratory channels | Abundant ✓ | Moderate | Well-posed, needs multimodal |
| 5 | **Disorders of consciousness** | Perturbational complexity, spectral slowing | Behavioural scale + follow-up | Small | Low | Clinically important, hard |
| 6 | **MCI / dementia** | Slowing, reduced alpha, aperiodic steepening | Neuropsychological + follow-up | Moderate ~ | Moderate | Prognosis is hard, detection easier |
| 7 | **Parkinson's** | Slowing, beta excess, aperiodic changes | Clinical diagnosis | Moderate ~ | Low–moderate | Moderate |
| 8 | **Stroke / rehab BCI** | Motor cortex reorganisation | Motor assessment scales | **Small, fragmented** | Low | Attractive, data-starved |
| 9 | **Epilepsy forecasting** (pre-ictal) | Contested pre-ictal state | Seizure timing | Abundant | High but contested | Ill-posed — effects may not exist |
| 10 | **Depression** | Frontal alpha asymmetry, theta | Questionnaire | Moderate ✓ | High | Ill-posed; asymmetry does not replicate well |
| 11 | **ADHD** | Theta/beta (refuted), aperiodic slope, connectivity | Clinical interview + scales | Large ✓ | Very high | **Ill-posed** — see §3 |
| 12 | **ASD** | Long-range connectivity, spectral | ADOS + clinical | Large ✓ | High | **Ill-posed** — weak, heterogeneous effects |

## 2. The Four Worth Detailed Consideration

### Sleep staging
- **Why well-posed:** the AASM scoring manual gives explicit rules; inter-scorer agreement is high; the signal is strong; night-long recordings give thousands of epochs per subject.
- **Datasets:** Sleep-EDF Expanded ✓ (~197 whole-night PSG recordings), SHHS ~ (thousands of participants, research access), MASS ~, CAP ~, plus consumer headband corpora from industry.
- **What is still open:** cross-cohort generalization across montages and hardware; **wearable/ear-EEG staging** (single-channel, noisy); staging as a sequence/structured-prediction problem rather than per-epoch classification; calibration and confidence for home use; comorbidity-aware staging.
- **Why it fits a final-year project:** public data, clear metric (per-stage F1, Cohen's κ), real deployment path, and the "audit/robustness" toolkit from this vault transfers intact.

### Seizure detection
- **Why well-posed:** the event is visible in the signal, and annotation is a judgement about the same signal the model sees.
- **Datasets:** CHB-MIT ✓ (23 paediatric patients, 23 ch, 256 Hz), TUH EEG Seizure Corpus ✓, EPILEPSIAE ~ (275 patients, long-term), SeizeIT1/2 ~ (wearable).
- **Why it is a trap:** decades of papers and cleared products (NeuroPace, Empatica's Embrace, Persyst). A better detector is not a contribution. The open problems are **false-alarm rate per patient-day on wearable hardware**, **cross-patient transfer with no calibration**, **uncertainty and abstention**, and **seizure *type* classification** rather than presence.
- **Honest verdict:** only enter with a workflow or wearable-continuous angle, never as "another detector."

### ADHD (the vault's current centre)
- **Why ill-posed:** the label is a clinical judgement, not a measurement; effects are small (TBR standardised effect |d| ≲ 0.2 across 576 specifications — [[Troendle-2026-TBR-Multiverse-HBN]]); comorbidity is the norm; medication is confounded; ~75% of real-world cases carry comorbidities that most studies exclude.
- **Datasets:** HBN ✓ ([[Healthy-Brain-Network-HBN]]), ADHD-200 ~, the 121-child IEEE cohort ✓ ([[IEEE-DataPort-ADHD-Child-121]]), private Dankook ([[Dankook-ADHD-vs-Tic-Private]]).
- **What is genuinely open:** measurement reliability, artifact/analytic dependence, calibration and abstention, differential specificity against other psychopathology, and event-locked dynamics. Not "a better classifier."
- **Honest verdict:** good place for **measurement science**, bad place for **biomarker discovery**.

### Autism (ASD)
- **Why ill-posed for EEG:** the diagnosis is behavioural; EEG findings are heterogeneous and frequently fail to replicate; cohorts differ by age, IQ, comorbidity and site.
- **Datasets:** ABIDE I ✓ (~1,112 datasets, 17 sites) / ABIDE II ✓ (~1,114) — but note that rs-fMRI is the primary modality and the EEG subset is smaller and less standardised. EU-AIMS ~.
- **Honest verdict:** not a good headline target. Only viable as a *specificity control* (does a model decode attention, or generic psychopathology?) — which is exactly what the CBCL factors in HBN make possible.

## 3. The Structural Lesson
Effect size and label quality, not prevalence, decide whether an AI problem is solvable. Epilepsy and sleep have large, unambiguous, signal-visible targets. ADHD, ASD and depression have small, judgement-based, patient-reported targets. Most published ADHD-EEG accuracy above 0.85 comes from leakage or a confound; the current published frontier under subject-disjoint evaluation is **~0.79 AUROC** (no method — specialist or foundation — has materially exceeded this, [[Decision-Log]] Commitment 28, [[Subject-Level-Evaluation-Hygiene]]).

**Consequence for project choice:** if the goal is a working, deployable AI system, prefer a well-posed target. If the goal is a measurement contribution, an ill-posed target is the right place — because that is where the field's numbers are wrong.

## 4. Adjacent Targets Worth Noting
- **Pain:** no reliable EEG marker; effect sizes tiny. Avoid.
- **Addiction / craving:** small literature, weak labels.
- **Schizophrenia:** P300/MMN abnormalities are real but not diagnostic.
- **TBI / concussion:** return-to-play is a real market, evidence is contested.
- **Healthy cognition (workload, fatigue, drowsiness):** strong signal, free labels, immediate deployment; band-power and aperiodic features work well; under-served in the literature relative to commercial interest.

## 5. Connections
- [[Problem-Space-Map]] · [[BCI-Paradigms-and-Applications]] · [[Multimodal-Physiological-Signals]]
- Datasets: [[Healthy-Brain-Network-HBN]], [[IEEE-DataPort-ADHD-Child-121]], [[ADHD-200]], [[Dankook-ADHD-vs-Tic-Private]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]], [[Aperiodic-1f-Activity-and-Band-Ratios]]
