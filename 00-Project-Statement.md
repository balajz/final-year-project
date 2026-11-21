---
tags:
  - project-specification
  - project-statement
  - c0
  - c5
  - canonical
status: canonical-specification
version: 2.0
---

# Project Statement — Calibrated, Artifact-Aware Paediatric EEG Screening Workbench

> **This note is the canonical, self-consistent statement of the project.** It supersedes earlier prose in
> the vault wherever the two disagree. It contains **no experimental results** — every number below is
> either *published* (attributed) or *a target to be measured*. Results live in `results/` and are
> referenced, never restated here (see §9).
>
> Companion notes: engine = [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] (C0);
> product = [[Candidate-C5-Reliability-Screening-Workbench]] (C5).

---

## 1. One-Sentence Statement

We build an offline, locally runnable screening workbench that takes one child's 19-channel resting EEG and
returns a **calibrated triage index with an explicit statement of how much evidence supports it** — including
the answer *"insufficient evidence — abstain"* — rather than a diagnostic label.

## 2. Extended Statement (the paragraph a committee reads)

Published paediatric-EEG ADHD models report 93–99% accuracy, yet none of those figures survive
subject-disjoint evaluation; the figures that do survive cluster around 0.74–0.79 AUROC, and the base paper
for this project (Baibulova et al., 2026) lands there honestly — at 0.7444 test AUROC, with a specificity of
**44.44%** and a **13.79%** PPV at 10% prevalence. The field has spent a decade improving the *ranking* of
children; nobody has spent it improving the *confidence* of the answer. This project takes the base paper's
own honest operating point and asks a different question: **can we hold discrimination fixed and rescue the
false-alarm rate by knowing when the recording does not support a decision?** The deliverable is therefore a
workbench, not a classifier: a 3-panel interface that shows the index, the reliability of that index, and the
cortical evidence behind it, with abstention as a first-class outcome rather than a failure mode.

## 3. The Problem, Stated Precisely

Three distinct failures, separated because they require three distinct solutions.

**P-1 — The leakage illusion.** Window-level splits put 4-second segments from the same child in both train
and test, inflating accuracy to 93–99%. Under subject-disjoint splits the same architectures collapse to
0.74–0.79 AUROC. This is a *reporting* failure, and it is why the project must fix its evaluation protocol
before anything else.

**P-2 — The false-alarm bottleneck.** At a screening prevalence of 5–10%, specificity governs clinical
usefulness far more than AUROC. A model with 80% sensitivity and 44.44% specificity generates roughly six
false positives for every true case at 10% prevalence. Any proposal that improves AUROC by two points while
leaving specificity at 44% has improved the wrong quantity. **This is the quantity the project is graded on.**

**P-3 — The artifact confound.** Resting EEG in children carries blink, muscle, and movement artifacts that
differ systematically between clinical and control recordings — recordings for children who move more are
longer, noisier, and more likely to be the clinical ones. A model can therefore learn *recording quality*
rather than *neurobiology* and score respectably. The project treats this not as a nuisance to clean away but
as a quantity to **measure and report**.

## 4. Why This Problem Is Open (the gap, stated without overclaiming)

- **No method has materially exceeded ~0.79 AUROC on the 121-child cohort under subject-disjoint evaluation.**
  This is a *description of the current published frontier*, not a theoretically established ceiling; the best
  published figure was produced under a deliberately conservative, untuned protocol, so the frontier is soft.
- **Specificity at the clinical operating point is almost never reported as a head-to-head quantity.** Papers
  report AUROC and accuracy; the base paper reports 44.44% specificity and it is the weakest number in its
  table — and nobody has tried to move it.
- **Artifact sensitivity is virtually never quantified.** No paper in this cohort's literature reports what an
  artifact-only classifier can achieve on the same labels. This is the single most important missing control
  in the field.

> **Framing rule (binding).** Write *"current published frontier (~0.79 AUROC, subject-disjoint)"*. Never
> write "ceiling", never write "we beat" it, never write "we approach" it. See [[Decision-Log]] 28.

## 5. The Proposed Idea (what we actually build)

Two layers, one contribution.

### 5.1 The engine (C0) — Riemann-ST-GraphFormer with Evidence Gate

A compact, topology-aware model that replaces the base paper's weakest architectural choices:

| Base paper | This project | Why |
|---|---|---|
| Flattened 171-D connectivity vector | **5-lobe, 19-node spatial graph** (GATv2) | Preserves cortical topology; 5M-parameter budget, not 100M |
| Zero-lag Pearson correlation, hard 0.40 threshold | **Global joint Löwdin orthogonalised envelope connectivity (oAEC)** + learnable sparse gate + runtime SPD guard | Zero-lag correlation is dominated by volume conduction; joint Löwdin removes the echo while remaining positive-definite by construction |
| Raw theta/beta power ratios | **SpecParam 1/f separation** (1–40 Hz, R² ≥ 0.85) → aperiodic exponent χ as node prior | Separates periodic oscillation from background 1/f static; χ is invariant to vertical gain offset |
| Global train-set z-scoring | **Dual-path: trait (gain-invariant χ) + state (per-subject aligned connectivity)** | Global z-scoring is defeated by inter-subject skull/impedance variation |
| Amplitude thresholding, forced predictions | **Artifact Quality Index (AQI) selective abstention** | A prediction on a corrupted segment is worse than no prediction |

**The dual-path design is not decoration.** Per-subject Riemannian alignment is the standard fix for
between-subject covariance drift, but alignment necessarily removes *all* static between-subject structure —
including any static, trait-level diagnostic signal, not only impedance nuisance. Retaining a gain-invariant
χ path alongside the aligned state path is the architectural response to that trade-off. **Whether the
trade-off is real and whether dual-path recovers it is the project's central empirical question** (§6, H1).

### 5.2 The product (C5) — the 3-panel workbench

| Panel | Contents | What it answers |
|---|---|---|
| **1. Screening Result** | Calibrated index, matched operating point, **PPV at 5% and 10% prevalence**, abstention state, one plain-language sentence | *What does the tool say?* |
| **2. Reliability Report** | Risk–coverage curve, per-group attrition table, window-level abstention timeline, reproducibility hash, connectivity-integrity line (`n_not_psd`, min raw eigenvalue, correction magnitude) | *How much should I trust it?* |
| **3. Topology View** | 19-node 5-lobe scalp graph coloured by χ, pruned by the learned gate, **with a split-half stability metric** | *What is the evidence made of?* |

Panel 2 is the differentiator and the graded artefact. Panel 1 is table stakes. Panel 3 ships only if it
carries a stability metric.

## 6. Hypotheses (stated before measurement, each with a kill condition)

An assumption without a kill condition is a wish. Each hypothesis below is falsifiable by a named experiment.

| # | Hypothesis | Predicted outcome | **Kill condition** |
|---|---|---|---|
| **H1** | Alignment alone deletes trait-level signal, and dual-path recovers it | Unaligned AUROC > aligned AUROC; dual-path restores most of the gap | If dual-path does **not** recover the gap, drop alignment entirely and report alignment as harmful on this cohort |
| **H2** | An artifact-only classifier achieves appreciable AUROC on the same labels | Artifact proxies alone reach meaningfully above 0.5 | If artifact-only AUROC ≈ 0.5, P-3 is not a live confounder and the AQI panel loses its central justification |
| **H3** | Neural signal survives artifact control | AUROC after regressing artifact proxies out stays close to the uncontrolled value | If it collapses toward chance, the headline becomes *"the frontier is recording-quality prediction"* — still publishable, but the product claim changes |
| **H4** | Selective abstention raises specificity and PPV at fixed sensitivity | Risk–coverage curve shows specificity rising as coverage falls, monotonically | If specificity does not rise with abstention, the AQI gate is cosmetic and must be removed |
| **H5** | oAEC graphs require SPD correction infrequently under joint Löwdin | Corrections rare and small | If corrections are frequent or large, the graph panel must be demoted to low-confidence |

**H3 is the load-bearing hypothesis.** If it fails, the project's contribution inverts from "better
screening" to "the field's numbers are artifacts" — a stronger claim, but a different one. The specification
must therefore be written so that *both* outcomes are acceptable deliverables. That is the definition of a
viable project.

## 7. Evaluation Protocol (fixed before any result is reported)

1. **Splits.** Nested Group 5-fold CV *and* Leave-One-Subject-Out. Participants never straddle a split.
   Window-level splits are used only for internal diagnostics and are never reported as performance.
2. **Aggregation.** Probabilities aggregate to **participant level** before any metric is computed. Metrics
   are reported at subject level only.
3. **Primary metric.** **Specificity at fixed 80% sensitivity**, and **PPV at 5% and 10% prevalence**.
4. **Secondary metric.** AUROC, always reported, never headlined (§8).
5. **Uncertainty.** Every headline number carries a spread over repeated splits *and* a permutation-null
   p-value. A point estimate without a null distribution is not a result.
6. **Artifact control.** Every reported neural AUROC is accompanied by the artifact-only AUROC on identical
   folds and the artifact-controlled AUROC. No exception.
7. **Attrition.** A per-group attrition table accompanies every exclusion rule. Reported always.
8. **Statistics.** DeLong's test against the base-paper baseline for AUROC differences.

## 8. What Is Graded, and What Is Not

**Graded (the contribution sentence):**

> At fixed 80% sensitivity on the 121-child cohort under subject-disjoint evaluation, the base paper's
> 44.44% specificity and 13.79% PPV-at-10%-prevalence are moved to **X% and Y%** by artifact-aware
> abstention together with the dual-path trait/state decomposition, while AUROC moves by **≤ Z** — locating
> the remaining headroom in *calibration and abstention*, not discrimination.

**Not graded:** dashboard polish, AUROC magnitude, parameter count, feature count, number of ablation rungs.

**AUROC is never the headline.** It is a secondary quantity reported for comparability. A project that
improves AUROC and not specificity has, by this specification's own definition, failed.

## 9. Where Results Live (and why they are not in this document)

This note is a **specification**, not a log. Numbers enter the vault only when a script under `scripts/`
has produced them and a file exists under `results/`. Verified results are recorded in
`09-Verification-Pending/` and referenced by name.

Current status of the evidence base: see [[V-01-Risk-Register-2026-11-16]].
Directly relevant: [[V-02-R2-RESOLVED-oAEC-SPD]],
[[V-03-R3-Alignment-Harness]].

## 10. Scope Boundaries (what this project is not)

- Not a diagnostic device, not clinically validated, not a clinician replacement.
- Not a benchmark harness for other groups' models.
- Not a general EEG platform — one engine, one population, one product.
- **No cross-dataset pooling.** IEEE-121 is never pooled with any external ASD cohort; the confound of
  learning acquisition hardware is explicitly rejected.
- **No foundation-model zoo.** Comparison is C0 against the base-paper baseline. One optional frozen-encoder
  probe is permitted as an appendix if it requires no additional training.
- **No multimodal fusion for its own sake.**
- Not evidence that ADHD is measurable from 19-channel EEG. The project may conclude the opposite; that
  remains a valid and publishable outcome.

## 11. Phased Delivery, With Hard Gates

| Phase | Deliverable | Gate to proceed |
|---|---|---|
| **P1a** | Engine + CLI on IEEE-121; base-paper reproduction | Reproduces the base paper's reported operating point under subject-disjoint CV |
| **P1b** | 5-rung ablation ladder + risk–coverage curve | Ablation runs under Nested Group 5-fold; H1–H5 each have a measured answer |
| **P1c** | 3-panel local web workbench on IEEE-121 + HBN mini-set | Runs offline on both `.set` and `.csv`; stability metric present on Panel 3 |
| **P2** | Transdiagnostic specificity contrast on public HBN CBCL bifactors | Optional; needs no third-party approval |
| **P2-ext** | Binary ASD extension | Only if NITRC DUA is approved **and** n_ASD ≥ ~100 |
| **P3** | Caregiver summary mode | Aspirational; out of scope for grading |

**Schedule insurance.** P1a–P1c alone constitute a complete, defensible deliverable. P2 needs no approval.
**No phase depends on a third-party Data Usage Agreement.** This is the standing guarantee that the project
cannot be blocked by an external party.

## 12. Risks, Registrable and Open

| # | Risk | Status | Kill test |
|---|---|---|---|
| SR1 | Frontier framing defeats the specialist claim | **Resolved** — retire "ceiling", use "frontier"; headline is calibration/PPV | — |
| SR2 | oAEC positive-definiteness asserted rather than established | **Resolved** — joint Löwdin; `ensure_spd()` guard mandatory | — |
| SR3 | Alignment deletes trait signal | **Open** — consistent with the hypothesis; dual-path recovery untested | H1 |
| SR4 | Artifact confound inflates neural performance | **Open** — artifact-only performance being measured | H2, H3 |
| SR5 | ASD scope contradiction and DUA dependency | **Resolved** — P2 decoupled from DUA; binary ASD demoted to optional | — |
| SR6 | Runtime traps (channel names, band overlap, bad-channel rules) | **Resolved** — canonical 19-channel order, unified loader, PREP reference rule | — |
| SR7 | Abstention mistaken for a malfunction by a jury | **Open** — mitigation is Panel 2 on the same screen | H4 |
| SR8 | Dashboard consumes the schedule | **Open** — hard rule: no UI work until P1b completes | — |

**Note on SR3/SR4.** These are *deliberately open*. A specification whose central risk is closed before
measurement is a specification that has stopped being honest. Both have named experiments and both have
acceptable outcomes defined in §6.

## 13. One-Paragraph Defence (memorise this)

*"Paediatric EEG screening models report 93–99% accuracy, but under subject-disjoint evaluation none exceeds
about 0.79 AUROC, and the best honest implementation still produces a 44% specificity — which at screening
prevalence means six false alarms per true case. The field has optimised ranking and ignored confidence. We
hold discrimination deliberately fixed and attack the false-alarm rate instead: an artifact-aware abstention
gate plus a dual-path trait/state model, delivered as a workbench that reports its own reliability and is
allowed to refuse. We measure, rather than assume, how much of the published performance is recording quality.
If the neural signal survives artifact control we deliver better calibration at the same discrimination; if
it does not, we have shown that the field's frontier is partly an artifact — and both are defensible
outcomes, which is why the project cannot fail to produce a result."*

---

## 14. Connections

- **Engine:** [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]
- **Product:** [[Candidate-C5-Reliability-Screening-Workbench]]
- **Decisions:** [[Decision-Log]] (Commitments 27–33)
- **Risks:** [[V-01-Risk-Register-2026-11-16]]
- **Datasets:** [[IEEE-DataPort-ADHD-Child-121]], [[Healthy-Brain-Network-HBN]]
- **Base paper:** [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]
- **Field context:** [[Shen-2026-Brain4FMs-Benchmark]], [[Problem-Space-Map]]
