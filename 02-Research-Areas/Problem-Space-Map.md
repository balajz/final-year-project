---
tags:
  - research-area
  - problem-discovery
  - methodology
---

# Problem-Space Map: Where a Neuro-AI Project Can Actually Live

## 1. Why This Note Exists
The first 43 notes were built one paper at a time. That produces depth in whatever branch the papers happen to fall into — here, ADHD-EEG classification — and near-zero coverage of everything else in the brief (BCI, epilepsy, autism, cognitive states, wearables, caregivers, clinicians). Depth without a map is how a project gets chosen by accident.

This note is the map. Every future paper, idea, and dataset should be placed on it, so that empty quadrants are **visible** rather than silently unconsidered.

## 2. The Five Axes
Any neuro-AI project is a point in this space. Changing one coordinate changes the entire feasibility argument.

**(a) Beneficiary** — who is better off?
`patient` · `clinician` · `caregiver` · `researcher` · `BCI user` · `healthy user` (workload, sleep, focus)

**(b) Modality**
`scalp EEG` · `iEEG/ECoG` · `wearable EEG (ear, dry, in-ear)` · `fMRI` · `fNIRS` · `MEG` · `autonomic (ECG/PPG/EDA)` · `behavioural (RT, keystroke, video)` · `multimodal`

**(c) AI lever** — what is the AI actually doing?
`representation` (SSL, foundation models) · `adaptation` (alignment, personalization, transfer) · `inference` (calibration, abstention, uncertainty) · `measurement` (audit, QC, reliability) · `interaction` (neurofeedback, closed loop) · `fusion` (multimodal)

**(d) Target** — condition or state
`epilepsy` · `sleep` · `ADHD` · `ASD` · `depression` · `MCI/dementia` · `stroke/rehab` · `Parkinson's` · `disorders of consciousness` · `pain` · `healthy cognition`

**(e) Data** — the binding constraint
`public/large` · `public/small` · `private/negotiable` · `must collect` · `none exists`

## 3. Where the Vault Currently Sits
| Thread | Beneficiary | Modality | Lever | Target | Data |
|---|---|---|---|---|---|
| Leakage / evaluation hygiene | researcher | scalp EEG | measurement | ADHD | public/large ✓ |
| Alignment leverage | researcher, BCI user | scalp EEG | adaptation | ADHD + MI | public ✓ |
| Artifact control | researcher, clinician | scalp EEG | measurement | ADHD, Tic | public + private |
| Aperiodic / TBR | researcher | scalp EEG | measurement | ADHD | public/large ✓ |
| Decoding multiverse | researcher | scalp EEG | measurement | ADHD | public/large ✓ |
| Event-locked contrast | researcher, clinician | scalp EEG | representation | ADHD (CBCL) | public/large ✓ |
| Foundation models | researcher | scalp/iEEG | representation | many | public ✓ |
| Multimodal population graph (Hidayah) | researcher | rs-fMRI + sMRI + demographics | fusion | ADHD + ASD | public/large, **pooled → confounded** |

**Read the columns.** Every row is the same beneficiary (researcher), the same modality (scalp EEG), the same target (ADHD), and mostly the same lever (measurement). That is one corner of a five-dimensional space, explored very thoroughly.

## 4. The Empty and Thin Quadrants
| Quadrant | Status | Is that a reason to enter or avoid? |
|---|---|---|
| **BCI paradigms** (MI, P300, SSVEP, ErrP, neurofeedback) | Absent from vault | **Enter.** Labels come from the paradigm, not a clinician's judgement. Effect sizes are large. Within-subject calibration is expected rather than a flaw. The vault's alignment work transfers directly, and the BCIC-IV-2a evidence is already here. |
| **Epilepsy** | Absent | **Enter with caution.** Best-posed clinical problem in EEG (unambiguous ground truth, strong signal) but heavily saturated and already FDA-cleared. Novelty must come from a workflow or edge-case contribution, not another detector. |
| **Sleep** | Absent | **Enter.** Well-posed, abundant data, real consumer deployment, and staging is a sequence problem that fits modern architectures. Under-explored relative to its importance. |
| **Autism / ASD** | Absent | **Avoid as a headline.** ABIDE's EEG signal is weak and heterogeneous; most reported effects do not replicate. **— Overridden by project decision:** [[Decision-Log]] Commitment 34 promotes a dual `s_ADHD`/`s_ASD` head to Core Track 2 for *engineering* reasons (co-designing one architecture for two label sets, with the no-DUA CBCL arm as schedule insurance). The scientific assessment above stands unchanged: **binary `s_ASD` is never headlined, never graded on raw AUROC, and carries a kill condition** (equivalence bound + power calculation). This row remains the correct reading of the literature; Commitment 34 is a delivery decision, not a retraction of it. |
| **Wearable / ear-EEG** | Absent | **Enter.** This is where the field is going and where data is scarce in the right way (hard, but collectable at small scale). |
| **Multimodal fusion** | One paper ([[Hidayah-2026-Multimodal-GNN-ADHD-ASD]]) — fMRI, and its own ablation shows the extra modality adds nothing | **Enter, but not by adding a modality for its own sake.** The open version is *artifact-aware* fusion, where the second channel measures a confound rather than adding features ([[Class-Correlated-Artifact-Control]]). |
| **Caregiver-facing** | Absent | **Open.** Underserved, but hard to evaluate rigorously. |
| **Clinician workflow / QC / abstention** | Thin (in commitments only) | **Enter.** Genuinely useful, publishable, and cheap. The vault already has the intellectual equipment. |
| **Neurofeedback / closed loop** | Absent | **Open.** Attractive but evaluation is confounded by placebo and expectancy. |
| **Healthy cognition (workload, fatigue)** | Absent | **Enter.** Strong signal, easy labels, no clinical-ethics burden, deployable. |

## 5. The Hidden Axis: Well-Posedness
The single largest determinant of whether a final-year project succeeds is not novelty. It is whether the target is **well-posed**:

| Target | Ground truth | Effect size | Label cost | Cross-subject stability | Verdict |
|---|---|---|---|---|---|
| Seizure detection | EEG-visible, unambiguous | Large | Cheap (annotated corpora) | Moderate–good | **Well-posed** |
| Sleep staging | Consensus scoring rules (AASM) | Large | Cheap | Good | **Well-posed** |
| Motor imagery | The instruction *is* the label | Large | Free | Moderate (needs calibration) | **Well-posed** |
| P300 / ErrP | Stimulus-locked, single-trial | Large | Free | Good | **Well-posed** |
| Workload / fatigue | Task manipulation | Moderate | Free | Moderate | **Mostly well-posed** |
| ADHD | Clinical interview + rating scales | **Small** (|d| ≲ 0.2 for TBR) | Expensive, subjective | Poor | **Ill-posed** |
| ASD | ADOS + clinical judgement | Small | Expensive | Poor | **Ill-posed** |
| Depression | Questionnaire | Small | Cheap but noisy | Poor | **Ill-posed** |

This table is the most important operational lesson in the vault. **The ADHD thread is the least well-posed target we have been working on**, which is exactly why every honest result in it is a null or a ceiling. That does not make the work wrong — measurement science on an ill-posed target is valuable — but it does mean the project should not be chosen on the assumption that ADHD is where the signal is.

## 6. Rules for Using This Map
1. **Place every new paper** on the five axes before writing a note. If it does not fit any axis, the paper is probably out of scope — say so and record it in [[Reading-Queue]].
2. **Breadth is measured by columns, not rows.** Seven notes on ADHD-EEG is one cell. One note on sleep staging is a new cell.
3. **Do not let a single paper choose the domain.** The vault's centre of mass moved to ADHD because the first three papers were ADHD. That is an accident of ordering, not a decision.
4. **When two quadrants compete, prefer the better-posed one** unless the ill-posed one offers a measurement contribution that transfers.

## 7. Non-Disease Directions the Brief Explicitly Invites
- **Researcher tooling:** benchmark harnesses, QC pipelines, leakage auditors, specification-curve infrastructure. Cheap, publishable, cumulative.
- **Clinician workflow:** triage, abstention, report generation, alarm reduction, second-read.
- **Caregiver support:** seizure diaries, sleep summaries, escalation guidance.
- **BCI user autonomy:** calibration-free control, error correction, session transfer.
- **Closed loop:** adaptive stimulation, neurofeedback with honest controls.

None of these requires a new disease biomarker, and all of them are defensible as engineering contributions.

## 8. Connections
- Areas: [[Neurological-Conditions-Landscape]], [[BCI-Paradigms-and-Applications]], [[Multimodal-Physiological-Signals]], [[Personalization-and-Domain-Adaptation]], [[Clinical-Deployment-and-Workflow]], [[Brain-Foundation-Models-Landscape]]
- Decisions: [[Assumptions-Register]], [[Decision-Log]]
- Candidates: [[Candidate-Decoding-Multiverse-Aperiodic-Audit]], [[Candidate-Event-Locked-NeuroBehavioral-HBN]], [[Candidate-Evidence-Aware-ADHD-Screening]]
