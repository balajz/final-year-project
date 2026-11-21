---
tags:
  - project-idea
  - synthesis
  - brainstorming
  - comparison
  - decision-matrix
status: active-brainstorming
---

# Final-Year Project Brainstorming: Head-to-Head Synthesis & Honest Critique

> **Scope Rule ([[Decision-Log]] Commitment 21):** This note is pure conceptual brainstorming, architectural critique, and trade-off analysis on paper. Nothing here is executed, simulated, or trained.

## 1. Where Our Collective Knowledge Stands Right Now

Across 9 deeply audited papers, 25 methodological commitments ([[Decision-Log]]), 12 explicit assumptions with kill conditions ([[Assumptions-Register]]), and the 5-axis [[Problem-Space-Map]], our brainstorming has uncovered **four hard empirical truths** that kill 90% of standard student/academic neuro-AI projects:

1. **The Evaluation Frame & Calibration Budget Beat the Model Architecture (4x Confirmed):**
   - On `ADHD-Child (n=121)`, a lightweight 2-layer `ShallowConvNet` ties complex 128K-parameter directed transfer-entropy Graph Transformers ([[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]), and giant Brain Foundation Models (`LaBraM` 0.66, `CBraMod` 0.64, `BIOT` 0.55) lose to domain-specific baselines (0.74–0.78 AUROC, [[Shen-2026-Brain4FMs-Benchmark]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]).
   - Moving from segment-wise to subject-disjoint splits drops PSD-SVM accuracy by **21–24 percentage points** ([[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]) and fMRI GNN accuracy by **11–15 points** ([[Hidayah-2026-Multimodal-GNN-ADHD-ASD]]).
   - In BCI motor imagery ([[Liu-2026-EEG-FM-Compass-Benchmark]]), shrinking the fine-tuning budget from full-session to a realistic 30% calibration block **flips the Foundation Model vs. CSP+LDA advantage by 25 accuracy points** (+14.8 pp → −10.3 pp).
2. **Unsupervised Alignment Beats Pretraining Scale:**
   - Per-subject Euclidean/Riemannian Alignment on unlabeled windows buys **+14 accuracy points** on BCIC-IV-2a, whereas scaling to a 4.9M-parameter pretrained Foundation Model buys **+2–3 points** ([[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]], [[Unsupervised-Alignment-Leverage]]).
3. **Classic Psychiatric Rest-EEG Biomarkers Are Ill-Posed and Artifact-Confounded:**
   - Theta/Beta Ratio (TBR) shows **0/576 significant specifications** ($|d| \lesssim 0.2$) on HBN ([[Troendle-2026-TBR-Multiverse-HBN]]), and standard quality/amplitude exclusions disproportionately discard the most hyperactive ADHD children (38% ADHD attrition vs. 0% Tic in [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]; [[Class-Correlated-Artifact-Control]]).
4. **Foundation Model Benchmarks Suffer From Pretraining-Corpus Overlap & Calibration Collapse:**
   - Several headline FM wins (`EEGPT` 88.3% on SEED; `LUNA` 81.9% on TUAB) evaluate inside datasets that were already in the unsupervised pretraining corpus ([[Pretraining-Corpus-Overlap]]), and cross-subject logit shifts cause **F1 = 0.00 calibration collapse** at $\tau = 0.5$ even when AUROC looks respectable ([[BFM-Bottlenecks-and-Hybrid-Opportunities]]).

---

## 2. The Core Fork in the Road (Assumption A1)

Before picking a project, you have to answer **one philosophical question** ([[Assumptions-Register]] A1 & A10):

- **Path A — Measurement Science & Methodological Auditing on an Ill-Posed Clinical Target (ADHD / HBN-EEG):**
  - *What you build:* An auditing framework, specification-curve engine, or event-locked paradigm contrast that proves *why* published clinical EEG numbers disagree and separates 1/f subject identity + movement artifacts from true attentional dynamics.
  - *Why it wins:* Reviewers and researchers love rigorous measurement papers that explain a field-wide failure mode; HBN-EEG (`ds005505`–`ds005516`, 2,782 subjects, no DUA) gives massive public scale.
  - *The honest risk:* Your final headline accuracy will be **0.55–0.78 AUROC** (or a negative/null biomarker finding). If your college review panel expects a flashy "92% accurate working product demo," you must frame the deliverable as an **Automated EEG Reliability & Leakage Auditing Platform** rather than a diagnostic classifier.
- **Path B — Calibration & Adaptation Engineering on a Well-Posed Target (BCI / Sleep / Wearable):**
  - *What you build:* A zero-shot / few-shot calibration protocol, session-shift adapter, or reliability-gated decoder where ground-truth labels are unambiguous and effect sizes are large.
  - *Why it wins:* Positive results are achievable (75%–90%+ accuracy), the user pain point is immediate ("save 15 minutes of BCI recalibration every morning" or "stage sleep reliably on a 2-channel headband"), and it feels like a concrete engineering system.
  - *The honest risk:* Classic BCI/sleep datasets have smaller subject counts ($N = 9$ to $54$ for cross-session MI; $N = 197$ for Sleep-EDF) and heavier prior art on cross-session transfer, requiring a sharp protocol angle.

---

## 3. Head-to-Head Scorecard: The Base-Paper Upgrade + Vault Candidates

> **Status note (2026-11-16):** the selection is settled — **C0 is the engine (Commitment 26) and C5 is the product layer (Commitment 27)**, specified in [[Candidate-C5-Reliability-Screening-Workbench]]. The `[SELECTED]` marker on C0 and `[NEW SYNTHESIS]` (C5) are now historical labels; C1, C2, C3 and C4 remain live only as modules inside C5 or as fallbacks if a gating test fails ([[09-Verification-Pending/V-01-Risk-Register-2026-11-16]]).

| Candidate | Quadrant & Target | Core Thesis / Deliverable | Data & Compute Feasibility | Defensible Novelty | Main Vulnerability / Kill Condition |
|---|---|---|---|---|---|
| **C0. [SELECTED BASE-PAPER UPGRADE] Topology-Aware Riemannian ST-GraphFormer & Calibrated Dual-Index (ADHD + ASD)** ([[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]) | **ADHD + ASD Multi-Condition Decision Support** (Upgrading [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] on IEEE-121 + Same-Machine HBN-EEG) | Fixes all 6 flaws in Baibulova et al. (2026) (`ST-GATv2`, echo-free `oAEC`, `SpecParam 1/f` node priors, `Riemannian alignment`, `AQI abstention`) and adds **Approach A ASD + ADHD Differential Screening** on unified HBN-EEG hardware (`s_ADHD` + `s_ASD` dual calibrated heads, zero cross-dataset pooling). | **Very High.** Official base-paper GitHub code + 121-child CSV ready today; HBN-EEG 10–20 subset + free NITRC DUA for K-SADS ASD/ADHD labels. | **Very High.** Beats a May 2026 base paper on its own benchmark while solving real-world ADHD+ASD differential screening on unified hardware. | Must strictly avoid pooling `IEEE-121` with external ASD cohorts; requires clean ablation ladder on `IEEE-121` first before HBN multi-label expansion. |
| **C1. Decoding Multiverse & Aperiodic Identity Audit** ([[Candidate-Decoding-Multiverse-Aperiodic-Audit]]) | **ADHD Measurement** (HBN-EEG + IEEE-121) | Audits ~160 decoding pipelines (`SpecParam 1/f` × `IAF` × `EA` × `artifact strata`) + tests the $2\times2$ hypothesis that the 24 pp leakage gap is a personal **1/f spectral fingerprint $(\chi, A)$**. | **High.** Public S3/NEMAR HBN mini-sets + full releases; linear models run on laptop CPU. | **High.** First specification curve of *decoding/PPV* (not regression) + mechanistic 1/f identity decomposition. | May read as "a statistical audit rather than an AI system" to an engineering jury if all universes cluster at 0.55–0.70 AUROC. |
| **C2. Event-Locked Active vs. Passive Neuro-Behavioral Decoding** ([[Candidate-Event-Locked-NeuroBehavioral-HBN]]) | **ADHD Representation** (HBN-EEG 6-task HED) | Contrasts passive Resting State vs. active event-locked **Contrast Change Detection (CCD)** & **Symbol Search** within the *same children*, fusing pre-stimulus EEG with reaction-time variability across 4 orthogonal CBCL factors. | **High.** HED event markers + CBCL bifactors (`Attention` vs. `Externalizing`) verified in public HBN BIDS. | **Very High.** Solves event-blind windowing and transdiagnostic specificity in one clean within-subject design. | Button-press motor/ocular artifacts around trial events can masquerade as attention signal unless pre-stimulus windows are strictly isolated. |
| **C3. Evidence-Aware Screening & Selective Abstention Layer** ([[Candidate-Evidence-Aware-ADHD-Screening]]) | **Clinician Workflow / QC** (ADHD-Child + HBN) | Wraps EEG inference in an **artifact-invariance ladder**, prevalence-aware PPV calibration (5%–10% prevalence), and **risk–coverage selective abstention** ("insufficient evidence" when EMG/blink load is high). | **Very High.** Lightweight wrapper around existing encoders; fast on M-series Mac. | **Moderate standalone; Strongest as a module.** Best combined with C0, C1, C2, or C5 rather than pitched alone. | Current published frontier on 19-ch ADHD-Child (~0.79 AUROC, no method has materially exceeded this — Commitment 28) limits standalone discrimination impact if not paired with C0 or HBN; the contribution is calibration/PPV, which is exactly what C3 provides. |
| **C4. Session-Shift BCI Calibration Exchange-Rate Audit** ([[Candidate-Session-Shift-BCI-Calibration]]) | **BCI Adaptation** (BCIC-IV-2a/2b, OpenBMI 54-subj) | Quantifies the **calibration exchange rate $k^*$**: how many labeled new-day calibration trials does 3 minutes of unlabeled Euclidean/Riemannian alignment + aperiodic drift tracking replace — for both CSP+LDA and Foundation Models (`CBraMod`). | **Very High.** Small datasets, zero DUA, runs on laptop; directly extends [[Liu-2026-EEG-FM-Compass-Benchmark]]'s 25-point inversion finding. | **Moderate–High.** "Alignment vs. $k$-shot crossover for FMs vs. classical decoders across sessions" + BCI-illiteracy failure prediction. | Cross-session Riemannian transfer has heavy prior art; novelty relies on the **FM-vs-classical calibration crossover** and session-ID precondition. |
| **C5. [SELECTED — PRODUCT LAYER, 2026-11-16] Unified Neuro-Reliability & Screening Workbench ("EEG-Prism / AuditBench")** ([[Candidate-C5-Reliability-Screening-Workbench]]) | **Researcher + Clinician Tooling** (Cross-Quadrant: HBN + BCI-2a + IEEE-121) | Combines the C0 engine with the C3 abstention/calibration module and the C1 audit backbone into an interactive, model-agnostic **EEG Screening & BCI Reliability Workbench**: any `.set`/`.bdf`/`.edf`/BIDS cohort or model checkpoint is audited for (1) **Subject-ID & 1/f Fingerprint Leakage** *(cohort-level audit finding only — never a live per-recording gate)*, (2) **Class-Correlated Artifact Attribution**, (3) *(dropped from the product)* alignment vs calibration crossover is an appendix result when BCI data are in hand, (4) **Selective Abstention & Prevalence-Adjusted PPV**. | **Very High.** Plays directly to strong backend/CLI + web systems engineering while preserving 100% of the vault's scientific rigor. | **Very High.** Turns a "negative result about noisy EEG papers" into a **positive, reusable software + measurement contribution**. | Scope management: must lock the 4 audit modules cleanly so it doesn't become a sprawling kitchen-sink benchmark. |
| **C6. [NEW SYNTHESIS] Reliability-Gated Multimodal Sleep / Wearable Staging Under Sensor Dropout** | **Sleep & Wearable Quadrant** (Sleep-EDF Expanded, $N=197$) | Fills the empty **Sleep + Multimodal** quadrant in [[Problem-Space-Map]]: trains a sequence model across `EEG + EOG + EMG` with **signal-quality-gated fusion and missing-modality dropout**, quantifying how well single-channel forehead/ear-EEG approximates full PSG and when the system should abstain due to motion/impedance drift. | **High.** Sleep-EDF is public, large (197 whole nights), well-posed (AASM ground truth), and naturally multimodal. | **High.** Directly tests reliability-gated fusion and lab-to-wearable distillation on a high-SNR target. | Requires opening a new dataset pipeline (Sleep-EDF) outside the 9 papers already dissected in the vault. |

---

## 4. Honest Recommendation: How to Pick Your Winner

If we look strictly at **what gives you both a bulletproof college thesis defense (taking a 2026 base paper to the next level) AND a standout research contribution**, here are the four clearest ways to lock the project today:

1. **Option 1 (The College Base-Paper Powerhouse: `C0 + C2 + C1-Lite` — Integrated Baibulova Upgrade):**
   - **Anchor:** [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] (*Computers* 2026, 15(6), 333) + [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]].
   - **How it works:** Reproduce Baibulova et al.'s official GitHub baseline on the 121-child IEEE DataPort dataset (`63.16%` test accuracy, `0.7444` test AUROC, `0.7770` LOSO AUROC, `44.44%` specificity, `13.79%` PPV), then execute a **5-stage engineering & scientific ablation ladder**:
     1. *Connectivity & $1/f$ Fix:* Replace zero-lag Pearson + fixed $\theta=0.40$ with **volume-conduction-free oAEC/wPLI + differentiable sparse edge gating** AND **SpecParam $1/f$ aperiodic node priors $(\chi_i, A_i)$** (answering whether their "theta dominance" is oscillatory or $1/f$ slope).
     2. *Subject Alignment Fix (Dual-Path Required):* Deploy **unsupervised Riemannian tangent-space centering** to isolate within-subject dynamic state trajectories, while preserving static trait differences via **unaligned SpecParam aperiodic node priors** (Trap 2 rescue, Commitment 31; single-path alignment alone collapses AUROC 0.9055 → 0.7995 on real IEEE-121 data).
     3. *Architectural Fix:* Replace their flattened 171-D upper-triangular vector with **true 19-node Spatial Graph Attention (GATv2 + 3D electrode coordinates)** before the dual Transformer + GRU temporal streams.
     4. *Clinical Screening Fix:* Add the **Artifact Quality Index (AQI) + Selective Abstention Gate** (from C3) so blink-contaminated frontal (`Fp1-O1`) sequences abstain rather than trigger false alarms, raising PPV at 10% prevalence.
     5. *External Cohort & Event-Locked Validation (Fulfilling Baibulova §6 Future Work):* Validate the learned continuous Network Index $s^{(i)}$ on **HBN-EEG (10–20 montage)** against continuous **CBCL Attention vs. Externalizing scores** across passive resting vs. active event-locked **Contrast Change Detection (CCD)** windows.
2. **Option 2 (The "Best of Both Worlds" Systems + Measurement Workbench: `C5 = C0/C1 + C3 + C4`):**
   - Package the **Aperiodic Identity + Alignment $2\times2$ Decomposition** and the **Riemann-ST-GraphFormer** inside a reusable **EEG Reliability & Selective-Abstention Workbench**, evaluated on both ADHD (`IEEE-121` + `HBN`) and Cross-Session Motor Imagery BCI (`BCIC-IV-2a/2b` calibration exchange rate $k^*$).
3. **Option 3 (The Pure Cognitive-Paradigm Discovery Thesis: `C2 + C3` on HBN-EEG):**
   - Focus 100% on HBN-EEG's 6 HED-annotated tasks, contrasting passive Resting State against event-locked **Contrast Change Detection (CCD)** and **Symbol Search** within the exact same children.
4. **Option 4 (The Pure BCI Adaptation & Foundation-Model Thesis: `C4`):**
   - Leave psychiatric labels behind and measure the exact **calibration-trial crossover curve ($k^*$)** between Foundation Models (`CBraMod` / `LaBraM`) and classical Riemannian/CSP decoders across sessions on `BCIC-IV-2a/2b` and `OpenBMI (54 subjects)`.

## 5. Connections
- [[00-Project-Overview]] · [[Problem-Space-Map]] · [[Decision-Log]] · [[Assumptions-Register]]
- [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] · [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]
- [[Candidate-Decoding-Multiverse-Aperiodic-Audit]] · [[Candidate-Event-Locked-NeuroBehavioral-HBN]] · [[Candidate-Evidence-Aware-ADHD-Screening]] · [[Candidate-Session-Shift-BCI-Calibration]]
