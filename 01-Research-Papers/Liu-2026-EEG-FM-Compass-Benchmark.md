---
tags:
  - research-paper
  - foundation-models
  - benchmark
  - bci
  - eeg
  - ssl
  - leakage
---

# Liu et al. (2026) — EEG-FM-Compass: Progress, Benchmarking and Future Directions for EEG Foundation Models

- **Authors:** Dingkun Liu, Yuheng Chen, Zhu Chen, Zhenyao Cui, Yaozhi Wen, Jiayu An, Jingwei Luo, Dongrui Wu.
- **Venue:** *National Science Review*, nwag466, DOI [10.1093/nsr/nwag466](https://doi.org/10.1093/nsr/nwag466). Published 2026-08-03. Review + benchmark, special topic *Brain-Computer Intelligence*.
- **Scope:** surveys **55 EEG foundation models** into one design taxonomy, then benchmarks **12 open-source FMs + 8 specialist baselines** over **13 datasets / 9 BCI paradigms**, in **two scenarios** (cross-subject LOSO; within-subject few-shot) × **two adaptation modes** (full fine-tuning; linear probing).
- **Code:** `github.com/Dingkun0817/EEG-FM-Benchmark` — *"will be available"* at time of publication.

> **Why this paper matters more than its headline.** It is the first paper in this vault that is *horizontal* — it crosses the problem-space map instead of sitting in one cell. Every previous paper was scalp EEG → researcher → measurement → ADHD. This one supplies the empirical anchor for the BCI quadrant ([[Problem-Space-Map]] §4), which had zero papers behind it.

---

## 1. What the Paper Does

Three research questions:

- **Q1** — Can EEG FMs extract *generalizable* representations that adapt easily to new tasks?
- **Q2** — Do EEG FMs *consistently and significantly* beat specialist models trained from scratch on just the fine-tuning data?
- **Q3** — Do EEG FMs show *scaling-law* behaviour with model size?

The two scenarios are the design contribution, and they are the right two:

| Scenario | What it measures | Labelled data used | Deployment analogue |
|---|---|---|---|
| **LOSO** (cross-subject) | zero-calibration transfer, same device + paradigm | all trials from the training subjects | a clinic that owns a labelled corpus for this task |
| **within-subject few-shot** | rapid personalization | ~1/20–1/100 of the LOSO set, from the target user | a new user with a short calibration block |

For the MI/P300 datasets the few-shot set is **30% of one session** from the target subject (MI), 10%/5% of one session (P300), one video per class (SEED), 10% of one subject's data (Sleep-EDFx), and "first seizure + 10 min pre-ictal" for CHB-MIT. TUAB has no few-shot setting because each subject carries one diagnostic label.

---

## 2. Paper Claims (as stated by the authors)

1. **Linear probing is frequently insufficient** → pre-trained encoders are not yet usable as frozen feature extractors; task-specific full-parameter adaptation remains necessary.
2. **Specialist models remain competitive** → no EEG FM "consistently and significantly" outperforms a from-scratch CNN; the Nemenyi test puts CBraMod in the same non-significant group as EEGNet, ShallowConv, Conformer, Deformer and LMDA.
3. **No scaling-law behaviour** → no monotonic relation between parameter count and downstream rank in the current data regime.
4. **The pre-training objective family is not decisive** → raw-signal, token and codebook objectives all span the ranking, with overlapping ranges.
5. **Euclidean alignment (EA) helps most models** on BCIC-IV-2a (7/8 models improve; BENDR −3.08).
6. **Paradigm-specific FMs are a viable direction** → MIRepNet (MI-only) is SOTA on all three MI datasets.
7. **Leakage-aware ranking preserves the top order** → excluding downstream datasets that appeared in a model's pre-training does not change which FMs lead.

---

## 3. The Numbers Worth Keeping

**Field shape.** 55 FMs; 16.4% published 2024, **67.3% in 2025–26**; 90.9% general-purpose; 80.0% scalp EEG; **83.6% Transformer**; 50% of studies resample to 200 Hz, 34.1% to 250/256 Hz. Parameter counts span ~0.16M (Neuro-GPT) to ~7B (UniMind), pre-training corpora 115 h to 61,415 h.

**Headline ranks.** CBraMod (4.0M) is the best FM at average rank **6.56**; **EEGNet (≈2K parameters) is second**; the top six FMs are CBraMod 4.0M, Neuro-GPT 0.16M, LaBraM 5.8M, EEGMamba 3.3M, BENDR 4.0M, BIOT-6D 3.2M — i.e. *no* size ordering. Specialists take **16 first-place and 47 top-3 placements** across the 25 scenario cells; EEGNet alone has the most top-1 finishes.

**Cost.** EEGPT: **361 GFLOPs** per forward pass vs **0.35** for EEGNet at 4 s / 10 channels (≈10³×), and 46× lower fine-tuning throughput.

**LOSO, full fine-tuning — best model per dataset** (chance in brackets):

| Dataset | Paradigm | Best FM | Best specialist | Winner |
|---|---|---|---|---|
| BNCI2014001 | MI 4-class [25] | CBraMod 53.03 | EEGNet 44.97 | FM (+8.1) |
| BNCI2014004 | MI 2-class [50] | Neuro-GPT 77.70 | EEGNet 76.38 | FM (+1.3) |
| BNCI2015001 | MI 3-class [33] | CBraMod/BIOT 63.94 | ShallowConv 63.89 | tie |
| BNCI2014009 | P300 [50] | CBraMod 77.30 | LMDA 78.45 | specialist |
| BNCI2014008 | P300 [50] | CBraMod 69.91 | EEGNet 72.29 | specialist |
| CHB-MIT | seizure [50] | BENDR 75.50 | ShallowConv 80.18 | specialist |
| TUAB | abnormal [50] | **LUNA 81.92** | Deformer 81.48 | FM *— in-corpus, see §4.3* |
| Sleep-EDFx | sleep 5-class [20] | CBraMod 72.30 | Deformer 78.73 | specialist |
| SEED | emotion 3-class [33] | **EEGPT 88.31** | ShallowConv 53.41 | FM *— in-corpus, see §4.3* |
| Nakanishi2015 | SSVEP [~2.5] | BENDR 92.94 | Deformer 97.18 (TRCA 94.07) | specialist |
| EEGMat | workload | LaBraM 75.15 | TSception 74.10 | FM (+1.1) |
| Things-EEG2 | visual 2-way [50] | Neuro-GPT 80.28 | LMDA 78.72 | FM (+1.6) |
| SEED-VIG | fatigue (RMSE↓) | TFM 0.2283 | ShallowConv 0.2290 | FM (marginal) |

**Count: FMs take 8/13 per-dataset bests, specialists 5.** Read that against the abstract.

**The inversion the authors do not headline.** On the three MI datasets, the FM-vs-classical gap *reverses* when the labelled budget shrinks:

| Dataset | LOSO: CBraMod − CSP+LDA | Few-shot: CBraMod − CSP+LDA | Swing |
|---|---|---|---|
| BNCI2014001 | **+14.84** (53.03 vs 38.19) | **−10.28** (50.34 vs 60.62) | 25.1 |
| BNCI2014004 | +2.21 (75.45 vs 73.24) | −1.81 (77.39 vs 79.20) | 4.0 |
| BNCI2015001 | +7.05 (63.47 vs 56.42) | −5.59 (70.30 vs 75.89) | 12.6 |
| BNCI2014009 (P300) | +12.16 (77.30 vs 65.14) | +2.40 (56.85 vs 54.45) | 9.8 |
| BNCI2014008 (P300) | +11.22 (69.91 vs 58.69) | +1.35 (58.00 vs 56.65) | 9.9 |

Five for five, monotone, same direction, on the paper's own numbers. **The value of pre-training is a function of how much labelled same-paradigm data you already have** — and at the calibration budget the paper itself calls "realistic deployment," a 2011-era spatial-filter pipeline (CSP+LDA) beats the best 4M-parameter foundation model on 3/3 MI tasks. The abstract says "specialists remain competitive"; the table says *they win when labels are scarce*.

---

## 4. Critique

### 4.1 The fairness claim fails on preprocessing — the vault's own commitment 11
Each FM is run with **its original implementation's preprocessing**, and EA is applied **only** to EEGPT and MIRepNet "to avoid representation-space mismatch." The authors defend this as deployment realism ("what you get if you download it"), which is legitimate — but then the experiment cannot support the scientific claims (Q1, Q3) that are drawn from it. The ranking measures **model × pipeline × tokenizer × tuning**, and the paper never reports the pipeline effect separately. The irony is sharp: Compass diagnoses the field's inconsistent preprocessing in §1 and then cannot equalize it in its own benchmark. Any claim of the form "model class A beats model class B" from this table is a claim about as-shipped bundles.

*What would fix it:* run each FM twice — original preprocessing and a common pipeline — and report the difference as a variance component. That single table would have been the paper's most valuable contribution.

### 4.2 The linear-probing conclusion is confounded by asymmetric tuning
Full fine-tuning is "individually tuned" per model; the text never says the linear probe was tuned per model × dataset (layer choice, pooling, regularization, class weighting). If the tuned arm beats the untuned arm, that is partly a protocol result. A frozen encoder also needs its normalization statistics to match the probe's input distribution, and the paper's own EA caveat shows it knows this. The conclusion ("pre-trained representations are not universal") is *probably* right — it agrees with [[Shen-2026-Brain4FMs-Benchmark]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], and the ADHD ceiling — but the evidence presented is weaker than the claim. A **commitment 23** instance: correct thesis, under-supported result.

### 4.3 Pre-training–downstream overlap is treated as a ranking nuisance, not a validity threat
Datasets used in a model's pre-training are marked in Tables 2–3, and Table S51 recomputes rankings after dropping them. The paper concludes the top order is preserved. That is a repair of the *ranking*, not of the *numbers*. Two specific problems:

- **TUAB is very likely drawn from TUEG**, the corpus LUNA was pre-trained on *exclusively* (plus Siena). If so, LUNA's 81.92 on TUAB is a within-corpus result at the participant level, not cross-subject generalization — and the paper headlines it: *"LUNA attained state-of-the-art performance on TUAB but failed to generalize effectively to paradigms beyond clinical applications."* The sentence explains the failure by scope and never mentions that the success may be memorization. **Confidence: high on the direction, unverified on the recording-level overlap** — see [[Pretraining-Corpus-Overlap]] for the check.
- **SEED**: EEGPT 88.31 and LaBraM 79.18 sit against 52–54 for every other FM and 53.41 for the best specialist. A 35-point gap on a 3-class emotion task, where cross-subject emotion decoding is the field's canonical failure (Brain4FMs: SEED-IV AUROC ≈ 0.53), is not a representation result. It is the signature of in-corpus evaluation. The paper's marker convention should say so explicitly; as written, a reader sees "EEGPT solves SEED."

This is a **new leakage class** for the vault — corpus-provenance leakage — distinct from procedural leakage (splits) and sampling-frame leakage (site). Written up as [[Pretraining-Corpus-Overlap]] and codified as commitment 24.

### 4.4 Clinical tasks are scored with a decoding metric, not a clinical one
CHB-MIT is scored by **balanced accuracy over segments**. Seizure detection is an event-detection problem: sensitivity at a fixed false-alarm rate per 24 h, detection latency, patient-level aggregation. A detector with 80% BCA is either unusable or excellent depending entirely on alarm rate, and this table cannot distinguish the two. Same for TUAB: subject-level diagnosis, segment-level metric, no statement of how segments are pooled to a patient decision. Commitment 8 (calibration, prevalence-aware operating points) is not met anywhere in the clinical half. The benchmark answers *"can a model separate epochs?"* — a real question, but not the one the clinic asks.

Secondary: TUAB is abnormal-vs-normal, and **abnormal EEGs are dirtier** (sicker patients, more movement, more EMG). With no signal-quality baseline and no per-quality stratum, an 80% BCA is compatible with a quality detector. The artifact-only baseline that [[Class-Correlated-Artifact-Control]] demands is absent from all 13 datasets.

### 4.5 The scaling-law test is under-identified
Q3 is answered by correlating parameter count with average rank **across models that differ simultaneously in corpus (115 h → 61,415 h), objective, tokenizer, channel handling, backbone and tuning**. That is not a scaling test; it is a cross-sectional correlation with every confounder left in. Identification comes from **within-family** sweeps, and the paper evaluates one size for LaBraM (5.8M, of 5.8/46/369M), BENDR, CBraMod, EEGMamba, BIOT, LUNA, SingLEM. The only within-family pair is BrainOmni Tiny vs Base, where Base is worse on most tasks.

**Therefore:** "no evidence of scaling in the tested range, with a design that cannot detect one" is defensible. **"EEG FMs do not exhibit scaling laws"** is not, and that is the sentence that will be cited. The vault should also note the paper's own confound: a 4M model trained on 27,062 h beating a 1B model is a statement about **data-per-parameter**, not about size.

### 4.6 The FM-vs-specialist verdict is aggregation-dependent
- FMs take **8/13** per-dataset bests under LOSO full fine-tuning (§3 table).
- Specialists take **16 first-place finishes across 25 scenario cells**, and the abstract reports this.
- CBraMod has the **best average rank** (6.56); EEGNet is second.

Three aggregations, three different stories. "Average decoding accuracy" pooled across 13 datasets whose chance levels run 20%–50% and whose ceilings run 50%–98% is not a quantity — a 1-point gain on Nakanishi2015 (chance ~2.5%) and a 1-point gain on Sleep-EDFx (chance 20%) are not commensurable, and pooling them lets the high-accuracy SSVEP/P300 tasks dominate. The correct summary is a per-dataset paired comparison with dataset as the unit, or a mixed model; rank aggregation is acceptable but must be the only one reported, and the per-dataset winners must be reported alongside it. As written, the direction ("FMs are not yet dominant") is probably right and the statistic that supports it is not interpretable.

### 4.7 Non-significance is not parity
The Nemenyi post-hoc puts CBraMod in the same non-significant group as five specialists, and the paper reads this as statistical support for "FMs do not consistently outperform specialists." The *claim* is correct in form (no evidence of superiority). Two cautions: (a) the critical-difference test is conservative, and 25 scenario cells from 13 datasets share recordings, splits and subjects, so the independence assumption under the Friedman/Nemenyi construction is violated — correlated blocks are not independent replicates; (b) "not significant" must never be reported downstream as "equivalent." The vault's rule: absence of evidence of superiority is the finding; equivalence is not.

### 4.8 Survivorship in model inclusion
12 of 55 models had public weights, and the two best clinical performers in [[Shen-2026-Brain4FMs-Benchmark]] — **REVE and BrainWave** — are absent here. So are Brant, NeuroLM, FoME, Gram and ALFEE. Models that release weights are a non-random subset. Consequence: **the two benchmarks' "best model" conclusions cannot be compared at all**, because they evaluate almost disjoint model sets. The meta-conclusion (FMs are not yet dominant) survives because both agree; the model-level ranking does not transport.

### 4.9 Small protocols, unstated selection rule
"All results are averaged over three random seeds... performance on the test set at the final epoch of fine-tuning," with hyperparameters "individually tuned." It is not stated (a) what data the tuning used, (b) whether the final epoch was chosen by validation, (c) how many test subjects each LOSO fold had, (d) whether few-shot adaptation windows overlap the test windows. Per-subject results are in the supplement, which partially satisfies commitment 12 — but the main text reports no test-subject counts, no partition variance, and no per-subject confidence intervals. Per commitment 15, an unstated selection rule means small differences (≤2 points) are not citable; the large ones (the MI inversion, the SEED gap) are.

### 4.10 Reproduction cost puts the paper out of scope as a template
24 × A800 + 8 × A100, 12 FMs × 13 datasets × 2 scenarios × 2 modes × 3 seeds, plus per-model hyperparameter search. This is a paper to **cite**, not to extend, and it sets a hard floor on "benchmark many FMs" as a project shape. It also demonstrates the field's cost structure: the most informative result in the paper (the MI inversion) required none of that compute — it is two columns of an existing table.

### 4.11 What the paper gets right, and it is a lot
- **The scenario pair is the correct decomposition** and it is stated honestly: both LOSO and few-shot correspond to real deployments, and the authors say so rather than claiming one is "the" setting.
- **Refusing one shared learning rate across 15 architectures** is the correct response to Brain4FMs' most damaging weakness (fixed `lr = 1e-5`, which produced F1 = 0.00 collapses). This is the better-designed of the two benchmarks.
- **The leakage-aware ranking exists at all** — most benchmarks do not check.
- **Per-subject supplements** respect the participant-as-unit principle.
- **The EA ablation is reported against interest** (BENDR gets worse). That is the honest form of an alignment result.
- **A deflationary result is more useful than another SOTA table**, and the paper's taxonomy (Table 1: 55 models × scope × modality × data scale × compute × parameters) is the durable artefact. Tables 2–3 are a dated snapshot; Table 1 is a map.

---

## 5. Where This Paper Sits on the Problem-Space Map

| Axis | Value |
|---|---|
| Beneficiary | **BCI user** + researcher (first BCI-beneficiary paper in the vault) |
| Modality | scalp EEG (iEEG only inside the surveyed models) |
| AI lever | representation + adaptation + measurement (benchmark) — **all three at once** |
| Target | MI, P300, SSVEP, sleep, seizure/abnormal, emotion, fatigue, workload, visual decoding — **crosses 9 targets** |
| Data | public/large ✓ |

It is the first **horizontal** entry: it does not occupy a cell, it sweeps a row of the map. That is what the vault needed and did not have.

---

## 6. Project-Relevance Verdict

**Relevance: very high — as evidence, not as a model.**

1. **It anchors the BCI quadrant empirically.** The BCI area note previously rested on argument and one alignment figure. It now has 13 datasets, 9 paradigms, a documented protocol ladder, and a cost table.
2. **It independently corroborates the vault's central hypothesis** — third modality-independent instance: on MI, the classical-vs-foundation gap moves 25 accuracy points from a *data-budget* change alone. The vault's phrasing has been "the evaluation frame beats the model"; Compass adds "and the calibration budget is part of the evaluation frame."
3. **It supplies the missing cell for a new candidate.** Compass evaluates {across subject, same session} and {same subject, same session}. The deployment condition it invokes — same user, new day, new cap placement — is **neither**, and is exactly the condition Euclidean alignment was designed for. See [[Candidate-Session-Shift-BCI-Calibration]].
4. **It constrains what a final-year project can be.** No candidate may require re-benchmarking many FMs. Commitment 2 already banned "Model X on Dataset Y"; this paper makes "Model X on 13 datasets" equally infeasible.

**What not to do with it:** do not cite 88.31 on SEED or 81.92 on TUAB as generalization; do not cite "no scaling laws" as established; do not cite the Nemenyi group as equivalence; do not use "average decoding accuracy" pooled across datasets as a number.

---

## 7. Connections

- **Papers:** [[Shen-2026-Brain4FMs-Benchmark]] (the clinical counterpart, and the disagreement in §6 of [[Brain-Foundation-Models-Landscape]]), [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] (CBraMod is the top FM here; alignment evidence originates there)
- **Areas:** [[BCI-Paradigms-and-Applications]] · [[Brain-Foundation-Models-Landscape]] · [[Problem-Space-Map]] · [[Clinical-Deployment-and-Workflow]] · [[Personalization-and-Domain-Adaptation]]
- **Concepts:** [[Pretraining-Corpus-Overlap]] (new, from §4.3) · [[Subject-Level-Evaluation-Hygiene]] · [[Unsupervised-Alignment-Leverage]] · [[Nested-CV-and-Hyperparameter-Leakage]]
- **Opportunities:** [[Unsupervised-Alignment-Leverage]] (corroborated) · [[BFM-Bottlenecks-and-Hybrid-Opportunities]] (deflationary update)
- **Candidate:** [[Candidate-Session-Shift-BCI-Calibration]] (derived from §3 inversion + §4.9 protocol gap)
- **Log:** [[2026-11-15-EEGFM-Compass-Analysis]]
- **Decisions:** [[Decision-Log]] 24–25 · [[Assumptions-Register]] A13
