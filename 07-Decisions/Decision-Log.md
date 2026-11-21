---
tags:
  - decisions
  - methodology
---

# Decision Log & Epistemic Guardrails

This note tracks confirmed scope decisions, methodological standards, rejected ideas, and open questions.

## Active Methodological Commitments (2026-11-15)
1. **No Premature Selection:** Competing project directions will remain open and critically evaluated until sufficient technical evidence supports selecting one.
2. **Reject Trivial "Model X on Dataset Y" Projects:** Simply training an off-the-shelf CNN/Transformer on an EEG dataset for classification does not qualify as a meaningful contribution.
3. **Strict Evaluation Hygiene:** Any physiological/EEG evaluation must account for cross-subject generalization (subject-independent splits) and realistic class imbalance/false-positive constraints.
4. **Broad Beneficiary Scope:** Solutions are not restricted to clinical disease diagnosis; tools for researchers, caregivers, neuro-rehabilitation, BCI users, and clinician workflow auditing are equally valid.

### Added after the CTE-Net analysis (2026-11-15)
5. **Nested or corrected model selection is mandatory** for any generalization claim. A configuration chosen on the mean validation score across the same folds used for reporting is treated as a mild leak ([[Nested-CV-and-Hyperparameter-Leakage]]).
6. **Separate seed variance from partition variance.** Repeated training on identical folds measures optimization stability only. Report CIs as conditional on the partition unless repeated/nested partitions were run.
7. **Participant is the evaluation unit.** Window-level metrics are descriptive; overlapping windows are never independent observations.
8. **Calibration and prevalence-aware operating points are required** for any screening-oriented claim: Brier/reliability, PPV/NPV at realistic prevalence, decision curves — not only accuracy/AUC.
9. **Complexity must be earned.** A new architecture must beat a strong simple baseline *and* an ablation of its distinctive component, otherwise the contribution is claimed as interpretability/reliability and defended on those terms.
10. **Reliability/compactness metrics need bandwidth-matched and DOF-matched controls** before any "more stable representation" claim ([[Representation-Dispersion-and-Stability]]).
11. **Equalize preprocessing before comparing architectures.** Alignment, filtering, and artifact handling must be identical across all compared models, and the *preprocessing* effect must be reported separately from the *model* effect ([[Unsupervised-Alignment-Leverage]]).
12. **Report the number of test subjects, not only seeds or folds.** Intervals computed on a handful of test subjects describe split noise; they are never evidence of generalization ([[Subject-Level-Evaluation-Hygiene]]).
13. **Never compare models by accuracy at a fixed threshold when AUC/balanced accuracy are equal.** A 7-point "accuracy win" at τ=0.5 can be pure calibration ([[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]: CNN 72.7% vs SVM 65.6%, but AUC 0.72 vs 0.72, p=0.90). Report balanced accuracy, matched specificity, and calibration.

### Added after the Kim analysis (2026-11-15)
14. **"Noise robustness" requires a class-independent artifact control plus class-conditional explanation attribution.** A performance that survives artifacts is not evidence of robustness unless (a) artifact indices alone do not predict the label, (b) accuracy is reported per signal-quality stratum, and (c) attributed channels are compared *between classes*, not against each disorder's pathology separately. Within-person artifact heterogeneity is not a valid defence — class-correlated nuisance needs only a between-group difference ([[Class-Correlated-Artifact-Control]], [[Explanation-Stability-and-Faithfulness]]).
15. **A protocol must be valid before its result is compared.** Fixed-epoch and max-over-epochs are both invalid comparisons (crippled baselines vs test peeking). If two protocols in the same paper rank models differently, neither ranking is citable; report only comparisons made under a single, valid, pre-registered selection rule ([[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]).

### Added after the TBR multiverse analysis (2026-11-15)
16. **Report attrition by group, and model the missingness.** Every exclusion criterion we have encountered (amplitude rejection, quality tier, model-fit threshold, subtype exclusion) removes the most movement-prone children, i.e. disproportionately the ADHD class. Third independent instance in this vault (Kim: 38% ADHD vs 0% Tic; Troendle: 12.6% amplitude + 45 quality + 69 fit + the entire hyperactive/impulsive group). No paper reports the group distribution of its exclusions. Any artifact or robustness claim must therefore be accompanied by (a) a per-group attrition table and (b) at least one of: inverse-probability weighting, multiple imputation, or a sensitivity analysis on the excluded participants' available features. An artifact test run on an artifact-filtered sample is biased toward "no artifact effect" ([[Troendle-2026-TBR-Multiverse-HBN]], [[Class-Correlated-Artifact-Control]]).
17. **A multiverse claim requires a permutation-of-the-multiverse null and whole-universe reporting.** Significance counts across correlated universes are not independent Bernoulli trials, and post-hoc filtering to the "most significant" subset is a garden of forking paths applied to the analysis of the multiverse. Report (a) all universes, (b) the effect-size distribution rather than p-counts, and (c) a label-permutation null re-run through the *entire* multiverse ([[Multiverse-and-Specification-Curve-Analysis]]).
18. **Never state or interpret a band-power/band-ratio result without declaring aperiodic handling and IAF policy.** Every report must say whether power is 1/f-uncorrected, SpecParam-adjusted, or aperiodic-only, and whether bands are canonical or IAF-relative — and must note that IAF-relative bands are a different physical frequency range for every child. The aperiodic exponent and offset are candidate *identity* features and may carry more subject-discriminative information than the oscillations ([[Aperiodic-1f-Activity-and-Band-Ratios]]).

### Added after the breadth review (2026-11-15)
19. **The ADHD thread is one branch, not the project.** The vault's centre of mass moved to ADHD-EEG because the first three papers were ADHD — an accident of ordering, not a decision. No direction may be selected until the breadth survey in [[Problem-Space-Map]] has been reviewed and at least one candidate from a *different* quadrant (BCI, sleep, seizure, wearable, workload, clinician workflow) has been evaluated on the same seven criteria. Corollary: any future paper that does not fit one of the five axes in [[Problem-Space-Map]] §2 is out of scope by default, and that decision is recorded rather than implied. Explicitly unresolved beliefs are tracked in [[Assumptions-Register]].
20. **Breadth is measured by columns, not rows.** Seven notes on ADHD-EEG is one cell of the problem space; one note on sleep staging is a new cell. A branch is only considered surveyed when its data access, effect size, and saturation have all been checked — not when it has been read about.

## Scope of This Vault
21. **This knowledge base is for ideation, not execution.** It exists to brainstorm, compare, criticise and connect project ideas for the final-year project. No experiments are run here, no datasets are downloaded here, no models are trained or simulated here. Consequences: (a) feasibility is *argued* from published evidence and dataset documentation, never "verified by trying it"; (b) a design that would need a decisive experiment is recorded with that experiment named and costed, not launched; (c) the vault is judged by the quality of its reasoning and the number of well-posed candidate directions it keeps alive, not by any artefact it produces. Real work happens later, elsewhere, once a direction is chosen.

### Added after the EEG-FM-Compass analysis (2026-11-15)
24. **Never compare models whose pre-training corpus contains the evaluation corpus, and never report a within-corpus result as generalization.** A downstream split computed inside a dataset that was already in the model's unsupervised pre-training set is a procedural no-op: subject-disjoint CV, nested selection, inductive evaluation and permutation nulls all pass, because the defect is in the model's weights, not in the protocol. Required for any FM claim: (a) a per-model pre-training → downstream mapping at **recording/participant** level, not dataset-name level; (b) exclusion of in-corpus datasets from every headline average **and every headline sentence**, not only from a supplementary ranking; (c) an explicit **in-corpus** label in the main table if the cell is kept; (d) acknowledgement that ComBat-style harmonisation cannot help (it is the same recordings) and that a permutation null cannot detect it (the null destroys the association it would need). Corollary: "leakage-aware ranking" that drops a whole dataset is a *ranking repair*, not a validity repair — the individual number remains uninterpretable. Compass is the worked example (EEGPT 88.31 on SEED vs 52–54 for every other FM; LUNA 81.92 on TUAB, likely a TUEG subset) ([[Pretraining-Corpus-Overlap]], [[Liu-2026-EEG-FM-Compass-Benchmark]]).
25. **A benchmark's ranking is conditional on its tuning and inclusion policy; never compare rankings across benchmarks.** Two 2026 benchmarks over overlapping model families reach opposite conclusions about pre-training objectives: [[Shen-2026-Brain4FMs-Benchmark]] (one shared `lr = 1e-5` for 15 architectures) concludes AE > contrastive and bidirectional > autoregressive; Compass (per-model tuning) concludes the objective family is not decisive. Both are internally defensible and the difference is plausibly the tuning budget itself — which means the *disagreement is a measurement of the tuning effect*, not a contradiction about EEG. Required whenever citing a benchmark: state its (a) tuning policy, (b) model-inclusion rule (Compass evaluated only the 12 of 55 FMs with public weights, and omitted both models that led the clinical benchmark), (c) aggregation rule (per-dataset best vs average rank vs pooled accuracy give three different FM-vs-specialist verdicts), and (d) date of the snapshot. Cross-benchmark model comparisons are invalid unless the same weights, preprocessing and tuning budget were used.

### Added after the Hidayah analysis (2026-11-15)
22. **Never pool data sources without declaring the sampling frame.** If class membership correlates with source — consortium, site, scanner, release batch, atlas, or pipeline generation — then source is a valid predictor of the label, and accuracy is uninterpretable until that is addressed. Required for any pooled design: (a) a per-source × per-class table, (b) **source-prediction accuracy from the same features**, (c) site-stratified or leave-one-site-out CV, or a within-source analysis with meta-analysis. Pooled sites are never extra sample size. Two corollaries: harmonisation (ComBat) is *not* a remedy, because it estimates site effects conditional on the same class variable that is confounded with site; and a label-permutation null *cannot* detect this confound, because it destroys the association it would need to test. Note that this failure survives subject-level splitting, nested CV, inductive evaluation, and every other defence in this log — it is a sampling-frame defect, not a procedural one ([[Cohort-and-Site-Confounding]], [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]]).
23. **A paper can be right about its thesis and wrong about its result.** The Hidayah paper correctly demonstrates that protocol choice inflates accuracy, and is itself undermined by a confound it never checks. Audit any paper's *inference* separately from its *method*: rigorous methodology is not evidence that the specific claim survives.

## Dataset Status
- **IEEE DataPort ADHD-Child (n=121) — demoted to benchmark/audit target** (provisional, pending user sign-off). It carries a decade of architectural variants (including at least three from the T-GARNet/CTE-Net group), a methylphenidate confound of unknown status at acquisition, no per-subject demographic linkage, and a **current published frontier of ~0.79 AUROC** under subject-disjoint evaluation (no method has materially exceeded this — see Commitment 28). Novel contribution requires calibration, artifact-awareness, abstention, external data, event-locked/behavioral alignment, or workflow tooling.
- **Open provenance conflict (RESOLVED 2026-11-15):** [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]] states the ADHD children underwent "appropriate clinical washout" before recording; [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] states medication status at acquisition was unavailable. **Resolution:** Primary descriptions of the Nasrabadi et al. (2020) IEEE DataPort dataset (`10.21227/rzfh-zn36`, Roozbeh Hospital, Tehran) state only that *"ADHD children were diagnosed by an experienced psychiatrist according to DSM-IV criteria, and had taken Ritalin (methylphenidate) for up to 6 months."* It does **not** document a verified washout protocol or per-subject medication-at-recording metadata. Geethapriya's "clinical washout" phrasing is an unverified interpolation; CTE-Net is correct that acute medication status at recording is undocumented, leaving a permanent chronic/acute Ritalin confound on the 121-child dataset.

- **Differential-diagnosis cohorts (updated 2026-11-15):** the best *formulation* encountered is ADHD **vs Tic disorder** (or transdiagnostic symptom dimensions), not ADHD vs healthy — both classes are symptomatic, which matches the real clinical decision. While [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]'s cohort is **private**, we verified that **HBN-EEG on OpenNeuro/NEMAR (`ds005505`–`ds005516`)** provides **four orthogonal psychopathology dimensions** per child derived from a bifactor model of the CBCL (**Attention, Externalizing, Internalizing, and p-factor**) directly in `participants.tsv`. This enables a public **transdiagnostic specificity contrast** (decoding `Attention` vs. `Externalizing`/`Internalizing`) without needing a private hospital cohort.
- **Healthy Brain Network (HBN) — access verified 2026-11-15.** The **HBN-EEG BIDS releases** are public: 11 releases (NEMAR `ds005505`–`ds005512`, `ds005514`–`ds005516`; `ds005513` unused), **2,782 subjects**, **~1.9 TB total**, on NEMAR or anonymously on S3 (`--no-sign-request`), **no DUA**. A separate `nm000103` release (458 subjects) is **not for commercial use**. Every release carries **6 HED-annotated tasks** with per-trial RT/accuracy — 3 passive (Resting State, Surround Suppression, Movie Watching) and 3 active (Contrast Change Detection, Sequence Learning, Symbol Search) — and **four CBCL bifactors** (p-factor, internalizing, externalizing, attention) as anonymised scores in the participant metadata. **20-subject, 100 Hz mini sets exist per release**, which is the correct vehicle for a first pass. Cite Shirazi et al., bioRxiv 2024, DOI 10.1101/2024.10.03.615261 ([[Healthy-Brain-Network-HBN]]). Caveats: eye-tracking and per-subject electrode locations are *future* additions, not present; per-task `n` varies with age band; and BIDS "R11" is not obviously the same snapshot Troendle analysed.

## Rejected Directions
- **Provisional:** another architecture recombination on the 121-child ADHD-Child cohort as the *primary* contribution (e.g., "swap the TE estimator", "add another attention block"). Rationale: ShallowConvNet ties the full 128K-parameter CTE-Net pipeline on 7/8 metrics; the residual gaps are artifact dependence, calibration, timescale, and reliability — not architecture.
- **Re-benchmarking foundation models (closed 2026-11-15).** Compass needed 24 × A800 + 8 × A100 to fine-tune 12 FMs over 13 datasets × 2 scenarios × 2 modes × 3 seeds with per-model hyperparameter search. Any design whose contribution is "compare N models on M datasets" fails criterion 4 outright, and it also fails criterion 3: the most informative result in that paper — a 25-point swing in the FM-vs-classical gap from changing only the labelled budget — required **none** of that compute. It is two columns of an existing table. If a comparison is worth making, the table already exists ([[Liu-2026-EEG-FM-Compass-Benchmark]]).
- **Theta/beta ratio as a feature (closed 2026-11-15).** Not "weak" — closed. 0/576 analytical specifications produce a significant HC-vs-ADHD-inattentive difference in two independent samples, bounding the standardised effect at roughly |d| ≲ 0.2–0.25 ([[Troendle-2026-TBR-Multiverse-HBN]]). Any TBR-based component in a future design must be justified against this result.

## Unresolved Questions
- **Which quadrant? (2026-11-15) — the question above all the others.** All three current candidates sit in the same cell of [[Problem-Space-Map]]: scalp EEG, researcher-facing, measurement lever, ill-posed target. BCI, sleep, seizure, wearable, workload and clinician-workflow quadrants have been surveyed but have **no candidate yet**. Selection is blocked on producing at least one candidate from a different quadrant (commitment 19).
- ~~**Which candidate? (2026-11-15) Three live, none selected**~~ **RESOLVED 2026-11-16:** C0 selected as engine (Commitment 26), C5 selected as product layer (Commitment 27). The three original candidates ([[Candidate-Decoding-Multiverse-Aperiodic-Audit]], [[Candidate-Event-Locked-NeuroBehavioral-HBN]], [[Candidate-Evidence-Aware-ADHD-Screening]]) are no longer competing alternatives: C1 and C3 survive as modules inside [[Candidate-C5-Reliability-Screening-Workbench]], C2 survives only if the event-locked CCD subset proves usable on HBN.
- **Data route (RESOLVED 2026-11-15):** no DUA needed. Use the NEMAR/S3 BIDS releases; start from a 20-subject 100 Hz mini set. Remaining practical questions, not access questions: do releases overlap in subjects, what is per-task `n` by age band, and which release subset is affordable at ~91–245 GB each ([[Healthy-Brain-Network-HBN]] §4–§5).
- Which primary signal modality (scalp EEG alone vs. multimodal EEG + ECG/EMG/eye-tracking/behavioral) offers the best balance of public dataset richness and novel problem formulation?
- What compute budget (local Apple Silicon M-series vs. cloud GPUs) will be the target baseline for training vs. inference?
- Is artifact-invariance learnable at 19 channels / 128 Hz, or does the cohort's information ceiling make a usable screening claim impossible? (Artifact ladder as the decisive test.)
- **Alignment transfer question (RESOLVED 2026-11-16):** Does unsupervised alignment help on ADHD-EEG? **NO — single-path alignment collapses AUROC (0.91 → 0.80) and specificity (0.88 → 0.72)** by deleting static trait differences (Trap 2). The clean negative result is confirmed; dual-path architecture is mandatory. See Commitment 31 and [[09-Verification-Pending/V-03-R3-Alignment-Harness]].
- Which headline for the project: *measurement reliability* ([[Candidate-Evidence-Aware-ADHD-Screening]]) or *event-locked temporal biomarker discovery* (opportunity 2 in [[ADHD-Event-Locked-Connectivity-and-Leakage]])? Both share the audit backbone.
- Access/licensing path for an external pediatric ADHD cohort (ADHD-200 / Healthy Brain Network) for cross-dataset calibration.
- **Resolved in principle (2026-11-15):** HBN is the access path — public, N = 1,122 analysable, pipeline published. Remaining action is the Data Usage Agreement and confirming ADHD-200 is not a better multi-site complement.
- **Gating question (RESOLVED 2026-11-16):** on the public 121-child cohort, does an **artifact-only classifier** beat chance at predicting the ADHD label? **YES — AUROC = 0.7784** (EMG 30–60 Hz + blink + variance + duration). Artifacts alone match the literature's published frontier (~0.79). Every uncleaned performance number in the literature is confirmed to be artifact-contaminated. See Commitment 31 and [[09-Verification-Pending/V-03-R3-Alignment-Harness]].
- **Sourcing question:** does a **public ADHD vs Tic/comorbid** cohort exist anywhere, or must the differential-diagnosis framing be abandoned for a public-alternative contrast (ADHD vs ASD, ADHD vs healthy-but-symptomatic controls)?
- **New gating question (2026-11-15):** is the subject-identity leak in PSD pipelines carried by the **aperiodic exponent and offset**? Test by predicting participant ID from `(χ, A)` alone on HBN; if accuracy ≫ chance, the 1/f fingerprint is real and the {aperiodic correction} × {EA} 2×2 becomes the project's core table ([[Decoding-Multiverse-and-Aperiodic-Identity]] §4).
- **New gating question (2026-11-15):** does ADHD-EEG **AUC** vary across analytical specifications the way TBR's regression coefficient does? Eight universes on a 200-subject HBN subset answer this in a week, and decide whether the decoding-multiverse is a project or a footnote ([[Decoding-Multiverse-and-Aperiodic-Identity]] §8).
- **Re-reading task (2026-11-15):** is [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]'s theta dominance (AUC 0.733 vs beta 0.567, canonical bands, no SpecParam) an aperiodic-slope effect rather than an oscillatory one? An aperiodic-corrected re-analysis is required before that result is cited again.

---

## Final Project Selection (Locked 2026-11-16)
26. **Selected Final-Year Project — `Riemann-ST-GraphFormer + Evidence Gate` ([[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]):**
    - **Base-Paper Anchor:** [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] (*Computers* 2026, 15(6), 333) on [[IEEE-DataPort-ADHD-Child-121]].
    - **Core Technical Upgrades:** (1) True 5-lobe 19-node Spatial `GATv2` + `Transformer-GRU`, (2) Symmetric Löwdin `oAEC` (echo-free + SPD-valid), (3) `SpecParam` $1/f$ aperiodic node priors $(\chi_i, A_i)$, (4) Unsupervised Riemannian tangent-space subject alignment, and (5) `AQI` + Epistemic Selective Abstention Gate.
    - **Multi-Condition Expansion (Approach A):** Unified `ADHD + ASD` dual calibrated heads (`s_ADHD`, `s_ASD`) evaluated strictly within same-machine [[Healthy-Brain-Network-HBN]] (`K-SADS` via free NITRC DUA + immediate no-DUA `CBCL` bifactors and active `CCD` task). Pooling `IEEE-121` with any external ASD dataset remains **strictly banned** (Commitment 22).
    - **Phased Execution & Publication Standard:** Phase 1 locks the `IEEE-121` 5-step ablation + `HBN` no-DUA `CBCL`/`CCD` validation (DeLong test, Nested Group 5-Fold + LOSO, Brier/ECE, PPV at 5%–10% prevalence, Risk–Coverage curve, per-group attrition); Phase 2 adds `K-SADS` `ADHD+ASD` differential screening and the interactive review dashboard.

---

## Product Layer (Locked 2026-11-16)
27. **C0 is the engine; C5 is the product — and the two are locked together.** The deliverable is [[Candidate-C5-Reliability-Screening-Workbench]], a three-panel workbench (Screening Result · Reliability/Abstention Report · Topology & Connectivity) wrapped around the Commitment-26 engine. Rationale: presented as a classifier, the project invites *"why not 95%?"* — unanswered by the field and answered by our own ceiling card; presented as a pure audit, it reads as statistics rather than engineering. The wrapper resolves both. Binding sub-rules:
    - **(a) The graded headline is specificity/PPV rescue over [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] (44.44% → X%, 13.79% → Y%), not AUROC and not the dashboard.** If a reviewer remembers the UI but not the numbers, the deliverable has failed (Commitment 9 applied).
    - **(b) C5 adds zero new training runs.** It packages experiments C0 already runs (Commitment 24/25 scope guard). Comparing many foundation models stays closed.
    - **(c) No diagnosis output.** Language is *screening index / triage / insufficient evidence*; abstention is a first-class output, never an error state (Commitment 8).
    - **(d) The 1/f identity test is a cohort-level validation finding, never a live per-recording gate.** Only AQI/blink is a live gate. The aperiodic fingerprint ([[Assumptions-Register]] A4) has no meaningful per-patient output and must not be simulated in the UI.
    - **(e) Phase 2 (`s_ASD`) is conditional, not assumed.** It requires K-SADS labels via the NITRC DUA *and* an ASD `n` large enough for subject-disjoint analysis. Phase 1 (P1a–P1c) is a complete deliverable without any third-party approval. `IEEE-121` is never pooled with external ASD data (Commitment 22).
    - **(f) UI work is blocked until the ablation ladder and risk–coverage curve are done.** The workbench is a delivery vehicle, not the contribution.
    - **(g) Input formats are `.set` / `.bdf` / `.edf` — never `.edf` only.** HBN is native EEGLAB `.set`.

---

## R1 Ceiling Framing (Resolved 2026-11-16)
28. **Retire "leak-free ceiling 0.74–0.79 AUROC". Adopt "current published frontier ~0.79 AUROC".** Risk R1 in [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] is now resolved. The findings:
    - Brain4FMs used a fixed LR = 1e-5 for all 15 models with no Euclidean Alignment (EA) and no per-model warmup. This is a deliberately conservative, protocol-equalising choice — not an optimal-tuning regime. REVE's 0.79 ± 0.07 CI is wide and likely a conservative estimate of its true capability.
    - The word **"ceiling"** implies a theoretically characterised upper bound. This bound does not exist on this cohort: the best published figure (0.79) was produced under a suboptimal tuning protocol, its split type (LOSO vs. single cross-subject split) is unconfirmed against ours, and its CI spans 0.72–0.86.
    - Calling 0.79 "our ceiling" while simultaneously arguing that foundation models underperform specialists is self-contradictory, because 0.79 belongs to a foundation model.

    **Binding rules, effective immediately:**
    - Use **"current published frontier (~0.79 AUROC, subject-disjoint)"** wherever the old ceiling phrase appeared.
    - Never write "we beat the ceiling" or "our result approaches the ceiling".
    - The correct framing in every paper-facing sentence is: *"No method — specialist or foundation — has materially exceeded ~0.79 AUROC under subject-disjoint evaluation on the 121-child ADHD-Child cohort. The project's contribution is therefore calibration, artifact-awareness, and abstention, not discrimination."*
    - The graded headline remains **specificity/PPV rescue** (Commitment 27a). AUROC is a secondary metric and must be reported, but it is never the contribution sentence.
    - **Files updated:** [[IEEE-DataPort-ADHD-Child-121]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[Candidate-C5-Reliability-Screening-Workbench]], [[Neurological-Conditions-Landscape]], [[00-Candidate-Synthesis-and-Head-to-Head]], [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]].

---

## R2 oAEC Construction & SPD Guard (Resolved 2026-11-16)
29. **Mandate joint (global) Löwdin orthogonalisation; reject pairwise-symmetrised oAEC for Riemannian processing; enforce runtime SPD guard.** Risk R2 in [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] is now resolved. Verified empirically in `scripts/r2_oaec_spd_test.py` and documented in [[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]].
    - **The Mathematical Trap:** Pairwise-symmetrised oAEC (the default in MNE-CPP and Brainstorm) averages pairwise scalars rather than forming a Gram matrix of common vectors. Under band-limited signals (alpha band, 19 channels), it fails Positive Semi-Definiteness (PSD) in up to 78% of windows (worst observed eigenvalue: −0.93). Feeding this matrix directly into Riemannian tangent space is mathematically invalid.
    - **The Verified Solution:** Joint Löwdin orthogonalisation ($X_\perp = X(X^\top X)^{-1/2}$) orthogonalises all channels simultaneously before Hilbert envelope extraction and Pearson correlation. The resulting matrix is a genuine Gram correlation matrix of real vectors, yielding 0 PSD failures across 1,200 tested windows.
    - **Runtime Guard & Transparency Rule:**
      1. Every connectivity matrix must pass through `ensure_spd()` (`scripts/spd_guard.py`), which clips eigenvalues at $\epsilon = 10^{-6}$ and records the L1 eigenvalue correction magnitude.
      2. The C5 Reliability Panel must explicitly report `n_not_psd`, raw minimum eigenvalue, and mean/max correction magnitude. Large corrections must trigger a data-quality warning rather than silent repairs.
    - **Files updated:** [[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]], [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[Candidate-C5-Reliability-Screening-Workbench]].

---

## R3 Alignment Ablation Protocol & Trap-2 Safeguard (Actionable 2026-11-16)
30. **Deploy verified 4-arm alignment ablation harness; enforce dual-path restoration rule if $\Delta\text{AUROC} < -0.05$.** Documented in [[09-Verification-Pending/V-03-R3-Alignment-Harness]].
    - **Harness Audited & Mathematically Corrected:** `scripts/r3_alignment_ablation.py` runs a 4-arm participant-level grouped 5-fold CV (`none`, `euclid`, `riemann`, `riemann_band`) using exact Kaggle/IEEE-121 CSV schema parsing and NumPy-only true Fréchet geometric mean on $\mathcal{S}_{++}^{19}$. Initial bugs (pseudo-Riemannian mean collapsing to arithmetic mean, tangent-vector double-logarithm and clipping) have been eliminated.
    - **Trap-2 Sensitivity Proven:** On synthetic trait signals, Riemannian centering eliminates static cross-channel covariance offsets, dropping AUROC by 19.6 pp (0.7917 → 0.5961). This confirms the harness is sensitive and will detect if real ADHD discriminative information is deleted by alignment.
    - **Binding Decision Rule on Real Cohort (`data/adhd2.csv`):**
      1. If $\Delta\text{AUROC} \ge -0.05$ and specificity rises: Riemannian alignment is justified as an ablation rung.
      2. If $\Delta\text{AUROC} < -0.05$: Trap 2 is triggered. The specification **must restore the dual-path trait/state decomposition** (retaining scale-invariant aperiodic exponent $\chi_i$ as node priors in `GATv2`) or restrict alignment to the `riemann_band` arm. Single-path alignment cannot proceed alone under signal deletion.
    - **Files updated:** [[09-Verification-Pending/V-03-R3-Alignment-Harness]], [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[00-Project-Overview]].

---

## R3 Real-Cohort Empirical Resolution & Gating Answer (Locked 2026-11-16)
31. **Trap 2 confirmed real on IEEE-121; lock Dual-Path Trait + State Decomposition; resolve artifact gating question.**
    - **Empirical R3 Results on IEEE-121 (`data/adhdata.csv`, 8,279 windows, grouped 5-fold CV):**
      - `none`: AUROC = 0.9055, spec@80sens = 0.8833, PPV@10% = 0.4384
      - `euclid`: AUROC = 0.8109 (−0.0946), spec@80sens = 0.7333 (−0.1500)
      - `riemann`: AUROC = 0.7995 (−0.1060), spec@80sens = 0.7167 (−0.1667)
      - `riemann_band`: AUROC = 0.7667 (−0.1388), spec@80sens = 0.6333 (−0.2500)
    - **Trap 2 Confirmed Real:** Alignment deletes the static trait signal ($> 10$ pp AUROC drop across all arms). Single-path alignment is forbidden.
    - **Mandatory Architectural Fix Locked:** The **Dual-Path Trait + State Decomposition** (Trap 2 rescue) is locked into Stage 3 of `Riemann-ST-GraphFormer`:
      1. Dynamic state-flexibility stream: operates on Riemannian-aligned sequences to track temporal transitions.
      2. Gain-invariant static trait stream: feeds unaligned scale-invariant `SpecParam` aperiodic exponent $\chi_i$ and 1/f-relative peak power directly into `GATv2` cortical nodes.
    - **Artifact Gating Question Resolved:** An artifact-only classifier (EMG 30–60 Hz + blink + amplitude variance + duration) on IEEE-121 reaches **AUROC = 0.7784**. This matches the published frontier (~0.79) without any connectivity modeling, proving that uncleaned classifiers heavily exploit artifact structure. The **Selective Abstention Gate (AQI)** is mandatory to prevent false alarms.
    - **Files updated:** [[09-Verification-Pending/V-03-R3-Alignment-Harness]], [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[IEEE-DataPort-ADHD-Child-121]], [[00-Project-Overview]].

---

## R5 Runtime Inconsistencies & Preprocessing Standards (Resolved 2026-11-16)
32. **Enforce Canonical Modern 10–20 Naming, Disjoint Frequency Bands, PREP Bad-Channel Rule, and Multi-Format Ingestion Standard.** Risk R5 in [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] is now resolved. Verified empirically via `scripts/r5_runtime_audit.py` on `data/adhdata.csv` and documented in [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]].
    - **Canonical Modern 10–20 Channel Naming:**
      - Modern names `T7, T8, P7, P8` are the single mandatory standard across all code and documentation. `data/adhdata.csv` natively uses these modern names.
      - Ingestion normalizer in `scripts/data_loader.py` automatically maps legacy names (`T3->T7, T4->T8, T5->P7, T6->P8`) and EGI HydroCel 128 channels (`E45->T7, E108->T8, E58->P7, E96->P8, E11->Fz, E129/VREF->Cz`) on load.
      - Reorder all loaded arrays to canonical order: `STANDARD_1020_19 = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7', 'T8', 'P7', 'P8', 'Fz', 'Cz', 'Pz']`.
    - **Canonical Frequency Bands & EMG/Gamma Confound:**
      - Oscillatory clinical ladder is strictly contiguous and disjoint with 0 bin overlap:
        - Delta: 0.5 – 4.0 Hz
        - Theta: 4.0 – 8.0 Hz
        - Alpha: 8.0 – 13.0 Hz
        - Beta: 13.0 – 30.0 Hz
        - Gamma: 30.0 – 45.0 Hz
      - Extrinsic artifact monitoring band:
        - EMG / Muscle Artifact: 30.0 – 60.0 Hz (deliberately spans the cortical gamma band 30.0–45.0 Hz).
      - Confound rule: High-frequency EMG ratio and gamma power share spectrum and must never be treated as independent orthogonal predictors in the model without verifying collinearity.
      - SpecParam fit range: `1.0 – 40.0 Hz` with $R^2 \ge 0.85$ goodness-of-fit quality check.
    - **Citable Bad-Channel Rule & Attrition Accounting:**
      - Naive variance thresholds (e.g. `variance > 3 SD`) are prohibited because they falsely interpolate high-variance pediatric posterior alpha channels (`O1`, `P3`).
      - The PREP / Automagic reference rule (`z > 5.0 MAD`, `r < 0.40`, `predictability < 0.75`, `flatline < 1e-10`) is mandatory.
      - Attrition threshold: When $>4$ channels (>20% of the 19-channel net) fail PREP criteria, the recording must trigger the AQI Selective Abstention Gate, and per-group attrition rates (ADHD vs Control) must be reported explicitly.
    - **Multi-Format Container Ingestion & Environment Standard:**
      - Pipeline must accept `.csv` (IEEE-121), `.set` (HBN EEGLAB), `.bdf` (BioSemi), `.edf`, and `.fif`.
      - Native zero-dependency parser provided for CSV; MNE / HDF5 dependencies require isolated PEP 668 virtual environments (`python3 -m venv .venv`).
    - **Files updated:** [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]], [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[Candidate-C5-Reliability-Screening-Workbench]], [[00-Project-Overview]].

---

## R4 Multi-Condition Scope & DUA De-risking (Resolved 2026-11-16)
33. **Establish CBCL Bifactor Specificity Contrast as Default Phase 2 Deliverable; Demote Binary ASD to Conditional Extension.** Risk R4 in [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] is now resolved. Documented in [[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]].
    - **Resolution of Contradiction:**
      - Elevating binary ASD classification to a co-equal headline contradicted the vault's own evaluation in [[Problem-Space-Map]] ("avoid as a headline") and [[Neurological-Conditions-Landscape]] (ranked 12th/12).
      - Furthermore, clinical ASD ground truth relies on K-SADS via the NITRC DUA, introducing third-party review latency that could jeopardize project completion.
    - **Primary / Default Phase 2 Target (Zero DUA Required):**
      - The default transdiagnostic deliverable on HBN-EEG is the **CBCL Bifactor Specificity Contrast** (decoding `attention` vs. proving invariance to `externalizing` and `internalizing` dimensions) under the unified AQI Selective Abstention Gate.
      - Public BIDS / S3 / NEMAR releases ship CBCL bifactors immediately with zero credentials and no DUA.
    - **Conditional Exploratory Extension:**
      - Discrete $s_{\text{ASD}}$ classification is retained strictly as an exploratory extension, executed only if the NITRC DUA is approved within the Phase 2 timeline and yields $n_{\text{ASD}} \ge 100$ usable recordings.
      - The project deliverable is 100% self-contained and ready for college defense without the DUA.
    - **Files updated:** [[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]], [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[Candidate-C5-Reliability-Screening-Workbench]], [[00-Project-Overview]].

---

## Core Track 2 ASD Promotion & Review-Brief Attribution Rules (Updated 2026-11-16)
34. **Promote Unified `ADHD + ASD` Dual-Head Screening to Core Track 2 (Superseding 27e & 33); Lock Review-Brief Attribution Rules.**
    - **Core Track 2 Co-Design (No Longer "Optional Phase 2"):** Both `s_ADHD` and `s_ASD` output heads in `C0` and both gauges in `C5` Panel 1 are co-designed as core deliverables from Day 1 on same-machine [[Healthy-Brain-Network-HBN]] (`.set`, `.bdf`, `.edf`).
    - **Built-In Schedule Insurance (Zero DUA Bottleneck):** The free [NITRC HBN DUA](https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network) is submitted at project start to unlock clinical `K-SADS` labels (`Control`, `ADHD`, `ASD`, `Comorbid`, verifying $n_{\text{ASD}} \ge 100$). In parallel, the exact same dual-head architecture runs immediately on no-DUA `HBN-EEG` `CBCL` transdiagnostic dimensions (`Attention` vs. `Externalizing` / `Internalizing`) + `CCD` task—so the workbench is 100% deliverable even if DUA turnaround is delayed.
    - **Same Honest Standard, HBN Artifact Control & Zero Pooling:** ASD and `CBCL` bifactors follow the exact same calibration, PPV (5%/10% prevalence), and `AQI` selective-abstention metrics (never headlining raw ASD AUROC), and HBN runs the same artifact-only control + release-batch stratification + `CCD`-vs-resting motion check as `IEEE-121`. Panel 2's Risk–Coverage curve must be produced on **both cohorts (`IEEE-121` and `HBN-EEG`)**. Pooling `IEEE-121` with external ASD cohorts remains strictly banned (Commitment 22).
    - **Track 2 Scientific Framing & Kill Condition (Generalisation Arm):** Scientifically, Track 2 is positioned as a **generalisation and variance-quantification arm** of Track 1's mechanism rather than an all-or-nothing "prove neural specificity" claim—testing whether `F_attention` (and `s_ASD`) decode above a stated equivalence bound (minimum detectable effect) with an explicit power calculation for usable per-task $n$. **Kill condition:** if HBN per-task $n$ is below threshold, or if `F_attention` / `s_ASD` fails to exceed the equivalence bound after artifact control, Track 2 is reported honestly as a negative generalisation result and the graded claim remains anchored on Track 1 (`IEEE-121`) + dual-cohort Risk–Coverage.
    - **Risk Register Status Correction:** `R1, R2, R4, R5` are closed; **`R3` remains open** pending execution of the Dual-Path Trait + State ablation (and `scripts/r4_artifact_only.py` / `scripts/r4_artifact_control.py` await execution).
    - **Review-Brief Attribution & Permutation Hygiene:**
      1. The `88.33%` specificity (`43.84%` PPV@10%) jump in `results/r3_ieee121.json` is explicitly attributed to the unaligned global Löwdin `oAEC` + connectivity feature set *before* `GATv2` or abstention; **Dual-Path Trait + State** is justified by R3's alignment AUROC drop (`0.9055` $\rightarrow$ `0.7995`), not by the unaligned specificity number.
      2. Unaligned `0.9055` (`0.9081 ± 0.0089`, `p = 0.005` over 200 permutations in `results/r3b_perm.json`) is treated as a feature-set baseline requiring **R4 artifact control** (`scripts/r4_artifact_only.py`, `scripts/r4_artifact_control.py`) before any neurobiological attribution, given the `0.7784` artifact-only observation.
    - **Files updated:** [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[Candidate-C5-Reliability-Screening-Workbench]], [[00-Project-Overview]].
