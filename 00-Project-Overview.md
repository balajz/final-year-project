---
tags:
  - overview
  - neuro-ai
  - final-year-project
---

# Final-Year Project: AI for Brain and Neurological Applications

## 1. Overall Objective
Identify and build a technically rigorous, innovative final-year engineering project at the intersection of neuroscience, brain/physiological signals, and artificial intelligence. The goal is to solve a meaningful real-world problem for researchers, clinicians, caregivers, or individuals—moving beyond simple "apply Model X to Dataset Y" disease classification.

## 2. Current Stage
- **Canonical statement:** [[00-Project-Statement]] — the single self-consistent specification of the project (problem, idea, hypotheses with kill conditions, evaluation protocol, graded claim, phases, risks). **Where the overview or any candidate note disagrees with it, the Project Statement wins.**
- **Stage:** **FINAL PROJECT LOCKED** (2026-11-16) — Ready for Phase 1 Implementation
- **Status:** Selected final-year project: [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] (**Riemann-ST-GraphFormer + Evidence Gate**, upgrading [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] on [[IEEE-DataPort-ADHD-Child-121]] + unified **ADHD + ASD** differential screening on [[Healthy-Brain-Network-HBN]]). Recorded as Commitment 26 in [[Decision-Log]].
- **Deliverable & framing (locked 2026-11-16):** the project ships as **[[Candidate-C5-Reliability-Screening-Workbench]]** — the same C0 engine wrapped in a three-panel screening/reliability/audit workbench. **C0 is the AI core; C5 is the product.** The graded headline is the specificity/PPV rescue over the base paper (44.44% → X%, 13.79% → Y%), *not* the dashboard, and *not* AUROC. Recorded as Commitment 27. The workbench never outputs a diagnosis, abstention is a first-class output, and no new training runs are added.
- **What this vault is:** a thinking artifact. It exists to generate, compare, criticise and connect project ideas — reading, critique, judgement calls. It is **not** an execution log: nothing here is trained, downloaded, simulated, or benchmarked. Feasibility and novelty are argued on paper and recorded as reasoning, not demonstrated as results. Anything phrased like a task is a *question to be answered from literature or argument*, not an instruction to run code.
- **Mode:** Breadth survey open, **two blockers cleared**.
  1. **HBN access is verified:** NEMAR/S3, no DUA, 11 releases, 2,782 subject-records, 20-subject mini sets — so both HBN candidates are runnable on paper, limited by storage (1.9 TB) and per-task `n`, not permission.
  2. **Commitment 19 (non-ADHD candidate) is unblocked:** [[Liu-2026-EEG-FM-Compass-Benchmark]] supplied the 13-dataset BCI/FM benchmark evidence and yielded [[Candidate-Session-Shift-BCI-Calibration]] in the BCI quadrant.
- **Nine papers analyzed** — seven inside the scalp-EEG → researcher-facing → measurement-lever → ADHD cell, one in multimodal rs-fMRI/sMRI ([[Hidayah-2026-Multimodal-GNN-ADHD-ASD]]), and one cross-paradigm EEG Foundation Model benchmark across 13 BCI/clinical datasets ([[Liu-2026-EEG-FM-Compass-Benchmark]]). Across all three threads, the same thesis holds: **the evaluation frame, data/calibration budget, and preprocessing/alignment choice move EEG results as much as or more than model architecture.** Four candidates + one base-paper upgrade anchor are now on the table: **base-paper evolution (`Riemann-ST-GraphFormer`)** ([[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]), **decoding-multiverse audit** ([[Candidate-Decoding-Multiverse-Aperiodic-Audit]]), **event-locked paradigm contrast** ([[Candidate-Event-Locked-NeuroBehavioral-HBN]]), **calibration/abstention** ([[Candidate-Evidence-Aware-ADHD-Screening]]), and **cross-session BCI calibration exchange-rate audit** ([[Candidate-Session-Shift-BCI-Calibration]]), synthesized head-to-head in [[00-Candidate-Synthesis-and-Head-to-Head]]. Next: stress-test and lock the architectural math, ablation ladder, and HBN cross-cohort bridge for the leading **Baibulova Base-Paper Upgrade (`C0 + C2`)**.

## 3. Core Research Scope
- **Domains of Interest:** EEG signal processing, Brain-Computer Interfaces (BCI), epilepsy/seizures, ADHD, autism (ASD), cognitive states, neurological behavior, wearable/physiological signals, and adjacent neuro-AI areas.
- **Methodological Focus:** Self-supervised learning (SSL), EEG foundation models, Graph Neural Networks (GNNs), multimodal learning, signal processing, personalization/domain adaptation, and Explainable AI (XAI).

## 4. Evaluation & Selection Criteria
Every candidate project idea in `04-Project-Ideas` is evaluated against seven strict criteria:
1. **Real-World Problem:** Clearly defined user/clinical/research pain point (not just an academic benchmark metric).
2. **Meaningful AI Contribution:** AI is central to solving a technical bottleneck (e.g., cross-subject generalization, artifact robustness, label scarcity, personalization).
3. **Defensible Novelty:** Genuine architectural, algorithmic, or workflow contribution rather than gluing existing tools together.
4. **Practical Implementation Strategy:** Achievable within a final-year timeline and local/cloud compute constraints.
5. **Dataset & Data Feasibility:** Accessible, high-quality public datasets (e.g., TUH EEG, CHB-MIT, SEED, Sleep-EDF, BCI Competition) or realistic acquisition protocols.
6. **Rigorous Evaluation Methodology:** Subject-independent splits (avoiding data leakage), clinically or practically meaningful metrics (e.g., False Alarm Rate per hour, calibration time, interpretability fidelity).
7. **Post-College Extensibility:** Potential to evolve into an open-source research tool, publication, or clinical/consumer prototype.

## 5. Scientific Guardrails & Epistemic Rules
- **Separate Evidence from Hypothesis:** Clearly distinguish empirical findings reported in papers from our own architectural hypotheses and project ideas.
- **Guard Against Leakage:** Challenge any paper or baseline that uses random window-level splits instead of strict patient-/subject-independent splits.
- **Beyond Binary Classification:** Prioritize clinical workflow bottlenecks, assistive tools, signal quality/artifact auditing, continual adaptation, and human-in-the-loop decision support over black-box diagnostic claims.

## 6. Vault Index & Navigation
- **01-Research-Papers:** Summaries, methodologies, limitations, and citations of reviewed literature ([[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Shen-2026-Brain4FMs-Benchmark]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]], [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]], [[Troendle-2026-TBR-Multiverse-HBN]], [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]], [[Liu-2026-EEG-FM-Compass-Benchmark]]).
- **02-Research-Areas:** Domain overviews and the problem-space map ([[Problem-Space-Map]] — **start here**, five axes and the well-posedness argument; [[Neurological-Conditions-Landscape]], [[BCI-Paradigms-and-Applications]], [[Multimodal-Physiological-Signals]], [[Personalization-and-Domain-Adaptation]], [[Clinical-Deployment-and-Workflow]], [[Brain-Foundation-Models-Landscape]]).
- **03-Research-Opportunities:** Identified research gaps, technical bottlenecks, and underexplored intersections ([[Decoding-Multiverse-and-Aperiodic-Identity]], [[ADHD-Event-Locked-Connectivity-and-Leakage]], [[BFM-Bottlenecks-and-Hybrid-Opportunities]], [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]], [[Unsupervised-Alignment-Leverage]], [[Class-Correlated-Artifact-Control]]).
- **04-Project-Ideas:** **C0 selected as engine (Commitment 26), C5 selected as product layer (Commitment 27)**; the remaining candidates stay live as modules or fallbacks. Compare in [[00-Candidate-Synthesis-and-Head-to-Head]]. Engine: [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]. **Product: [[Candidate-C5-Reliability-Screening-Workbench]]** (*start here for the deliverable*). Modules/fallbacks: [[Candidate-Decoding-Multiverse-Aperiodic-Audit]], [[Candidate-Event-Locked-NeuroBehavioral-HBN]], [[Candidate-Evidence-Aware-ADHD-Screening]], [[Candidate-Session-Shift-BCI-Calibration]].
- **05-Technical-Concepts:** Core signal processing, ML architectures, and evaluation concepts ([[Dynamic-Functional-Connectivity]], [[Subject-Level-Evaluation-Hygiene]], [[Network-Index-Modeling]], [[Kernel-Matrix-Based-Transfer-Entropy]], [[Representation-Dispersion-and-Stability]], [[Nested-CV-and-Hyperparameter-Leakage]], [[Cohort-and-Site-Confounding]], [[Multiverse-and-Specification-Curve-Analysis]], [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Explanation-Stability-and-Faithfulness]], [[Pretraining-Corpus-Overlap]], [[Paper-Triage-Checklist]]).
- **06-Research-Log:** Chronological synthesis of brainstorming sessions ([[2026-11-15-Initialization]], [[2026-11-15-Baibulova2026-Analysis]], [[2026-11-15-Brain4FMs-Analysis]], [[2026-11-15-CTENet-Analysis]], [[2026-11-15-CBraMod-Analysis]], [[2026-11-15-Geethapriya-Analysis]], [[2026-11-15-Kim-GCN-Analysis]], [[2026-11-15-TBR-Multiverse-Analysis]], [[2026-11-15-ABFR-KAN-Triage]], [[2026-11-15-Breadth-Survey]], [[2026-11-15-Hidayah-GNN-Analysis]], [[2026-11-15-EEGFM-Compass-Analysis]]).
- **07-Decisions:** Record of accepted commitments, rejected paths, and finalized choices ([[Decision-Log]] — 33 commitments; [[Assumptions-Register]] — what the project assumes and what would kill each assumption).
- **09-Verification-Pending:** Claims under external review. The register ([[09-Verification-Pending/V-01-Risk-Register-2026-11-16]]) holds risks with kill conditions — **2 CLOSED, 3 DE-RISKED & ARCHITECTURALLY LOCKED**:
  - [[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]]: oAEC/PSD mathematically verified; global Löwdin + `ensure_spd()` guard enforced (**Closed**, Commitment 29).
  - [[09-Verification-Pending/V-03-R3-Alignment-Harness]]: Real-data alignment drop verified (0.9055 → 0.7995, consistent with Trap 2); Dual-Path Trait/State architecture locked as safeguard; artifact-only classifier hit 0.8089 ± 0.0664 AUROC (`scripts/r4_artifact_only.py`) confirming AQI abstention gate necessity (**De-risked**, Commitments 30, 31).
  - [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]]: Modern channel names verified (`T7, T8, P7, P8`); contiguous oscillatory ladder locked (`4–8, 8–13, 13–30 Hz`); EMG/gamma spectral confound surfaced; PREP bad-channel reference rule locked; multi-format loader implemented in `scripts/data_loader.py` (**De-risked**, Commitment 32).
  - [[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]]: Multi-condition Phase 2 de-risked from third-party DUA: public CBCL bifactor specificity contrast is primary/default; binary $s_{\text{ASD}}$ retained as conditional exploratory extension (**De-risked**, Commitment 33).
- **08-Datasets:** Cohort cards — identity, acquisition, confounds, access, project status ([[Healthy-Brain-Network-HBN]], [[IEEE-DataPort-ADHD-Child-121]], [[Dankook-ADHD-vs-Tic-Private]], [[ADHD-200]]).
- **Workflow:** [[Reading-Queue]] — intake log, active re-analysis tasks, and the pending verification list.

## 7. Current Position in the Problem Space
Full map and reasoning: [[Problem-Space-Map]]. Summary of coverage:

| Quadrant | Covered? | Candidate? |
|---|---|---|
| ADHD-EEG measurement / evaluation | **Thoroughly** (7 papers, 6 opportunities) | **3 candidates** |
| Brain foundation models | Area note + 3 papers (Brain4FMs, CBraMod, Compass) | Feeds existing candidates |
| BCI paradigms (MI, P300, SSVEP, ErrP) | Area note + Compass benchmark | **1 candidate** ([[Candidate-Session-Shift-BCI-Calibration]]) |
| Sleep staging | Area note + Compass sleep tasks | **No — gap** |
| Seizure detection | Area note + Compass CHB-MIT/TUSZ | No (deliberately; saturated) |
| Epilepsy forecasting, ASD, depression | Surveyed, judged ill-posed | No (deliberately) |
| Wearables / ear-EEG | Area note only | **No — gap** |
| Multimodal fusion | 1 paper (fMRI); its own ablation says the added modality does nothing | **No — gap** |
| Personalization / adaptation | Area note + alignment evidence | Core lever of [[Candidate-Session-Shift-BCI-Calibration]] |
| Clinician workflow / abstention | Area note | **Entered — becomes the C5 product layer** ([[Candidate-C5-Reliability-Screening-Workbench]]) |
| Caregiver-facing tools | Named only | **No — gap** (Phase 3 aspiration at most) |

**Reading of the table:** the ADHD measurement quadrant supplies the engine (C0) and the BCI adaptation quadrant supplied candidate C4, unblocking commitment 19. The **clinician workflow / QC quadrant is now occupied** by the C5 product layer: it is cheap, publishable, and it is what carries the project's measurable clinical claim. Sleep/wearable and artifact-aware multimodal fusion remain open gaps, deliberately untouched ([[Candidate-C5-Reliability-Screening-Workbench]] §5).

