# Project Knowledge Base

**Calibrated, Artifact-Aware Paediatric EEG Screening via Riemannian-Tangent Spatio-Temporal Graph Learning with Selective Abstention**

---

## 1. Short Description

This knowledge base documents a research project that develops an offline, locally runnable
screening workbench for paediatric resting-state EEG. The system accepts a 19-channel recording
and produces a calibrated triage index accompanied by an explicit statement of evidential support,
including the outcome *"insufficient evidence — abstain"*. It does not emit a diagnosis.

## 2. Research Domain

- **Primary domain:** Neuro-AI / clinical decision support
- **Subdomain:** Scalp EEG signal processing and machine learning
- **Technical theme:** Robustness, calibration, and selective prediction under distributional and
  measurement confounds
- **Research classification:** Applied machine learning, measurement science, benchmark-critical
  evaluation

## 3. Core Idea

Published paediatric-EEG attention-deficit/hyperactivity disorder (ADHD) models report accuracies
between 93% and 99% under window-level splitting protocols. Under subject-disjoint evaluation the
same architecture families do not materially exceed approximately 0.79 AUROC on the 121-child
benchmark cohort used here. At realistic screening prevalence, the operating characteristic that
determines clinical usefulness is not ranking quality but the false-alarm rate: an operating point
of 80% sensitivity and 44.44% specificity generates roughly six false positives per true case at
10% prevalence.

The project holds discrimination capacity deliberately fixed and attacks the false-alarm rate
instead. It combines (i) artifact-aware selective abstention, (ii) a dual-path trait/state
decomposition that separates gain-invariant aperiodic spectral structure from aligned dynamic
connectivity, and (iii) a topology-preserving spatio-temporal graph encoder. The contribution is
calibration, artifact-awareness, and abstention — not raw discrimination.

## 4. Problem Being Addressed

Three separable failures motivate the work:

- **P-1 — Evaluation-protocol inflation.** Window-level splits place segments from the same
  participant in both training and test partitions, producing accuracy figures that do not survive
  subject-level partitioning.
- **P-2 — The false-alarm bottleneck.** At screening prevalence, specificity governs utility far
  more than AUROC; the reference baseline reaches 44.44% specificity and 13.79% positive predictive
  value at 10% prevalence.
- **P-3 — The artifact confound.** Blink, muscle, and movement artifacts differ systematically
  between clinical and control recordings; a model may learn recording quality rather than
  neurobiology and still score respectably.

## 5. Proposed Approach

A two-layer system:

- **Engine (C0) — Riemann-ST-GraphFormer with Evidence Gate.** Global joint Löwdin orthogonalised
  envelope connectivity under a runtime positive-definiteness guard; SpecParam 1/f separation
  producing a gain-invariant aperiodic exponent as node prior; dual-path trait/state fusion; a
  five-lobe, nineteen-node spatial Graph Attention (GATv2) encoder; parallel temporal Transformer
  and bidirectional GRU; calibrated output with an evidence gate.
- **Product (C5) — three-panel reliability workbench.** Panel 1 reports the calibrated index with
  prevalence-aware operating points; Panel 2 reports the reliability and abstention behaviour
  including risk–coverage curves, per-group attrition, and a connectivity-integrity line; Panel 3
  renders the cortical graph with a split-half stability metric.

## 6. Key Technical Contributions

1. **Conceptual.** Recasting paediatric EEG screening from a discrimination problem to a
   calibration-and-abstention problem, and making the artifact burden a reported quantity rather
   than a nuisance to be cleaned away.
2. **Architectural.** A dual-path trait/state decomposition that retains gain-invariant aperiodic
   structure alongside per-subject aligned dynamic connectivity, addressing the information loss
   inherent in unsupervised alignment.
3. **Algorithmic.** Global joint Löwdin orthogonalisation for envelope connectivity, which yields a
   genuine Gram matrix and is therefore positive semi-definite by construction, paired with a
   runtime spectral guard that logs correction magnitude as a data-quality signal.
4. **Methodological.** An evaluation protocol that reports artifact-only and artifact-controlled
   performance on identical folds alongside every neural result.
5. **Implementation.** A dependency-light ingestion and geometry stack operating offline on
   consumer hardware, with native multi-format support.

## 7. System Overview

```
Recording ──▶ Ingestion & Canonicalisation ──▶ AQI Scoring ──▶ Preprocessing
    │
    ├──▶ Global Joint Löwdin oAEC ──▶ SPD Guard ──▶ Riemannian Tangent Mapping ──┐
    │                                                                            │
    └──▶ SpecParam 1/f Fit ──▶ Trait Path (aperiodic exponent node priors) ──────┤
                                                                                 ▼
                                                        Dual-Path Fusion ──▶ 5-Lobe GATv2
                                                                                 │
                                     ┌───────────────────────────────────────────┘
                                     ▼
                        Parallel Temporal Encoder (Transformer + BiGRU)
                                     │
                                     ▼
                          Calibration Head ──▶ Evidence Gate
                                     │
                     ┌───────────────┼───────────────┐
                     ▼               ▼               ▼
              Panel 1          Panel 2          Panel 3
           (Screening)     (Reliability)     (Topology)
```

## 8. Directory Structure

```
Project_Knowledge_Base/
├── README.md
├── 01_Project_Overview.md
├── 02_Abstract_and_Keywords.md
├── 03_Introduction_and_Problem_Statement.md
├── 04_Research_Motivation_and_Gap.md
├── 05_Objectives_and_Contributions.md
├── 06_Proposed_Solution.md
├── 07_System_Architecture.md
├── 08_Module_Descriptions.md
├── 09_Methodology_and_Workflow.md
├── 10_Algorithms_and_Pseudocode.md
├── 11_Data_and_Information_Flow.md
├── 12_Mathematical_Foundations.md
├── 13_Technology_Stack.md
├── 14_Implementation_Plan.md
├── 15_Experimental_Design_and_Evaluation.md
├── 16_Expected_Results.md
├── 17_Applications_and_Use_Cases.md
├── 18_Limitations_and_Assumptions.md
├── 19_Future_Research_Directions.md
├── 20_Conclusion.md
├── 21_IEEE_Paper_Preparation_Notes.md
└── diagrams/
    ├── system_architecture.mmd
    ├── system_workflow.mmd
    └── data_flow.mmd
```

## 9. Document Navigation

| If you need to understand… | Read |
|---|---|
| The problem and why it matters | 03, 04 |
| What exactly is being built | 06, 07, 08 |
| How it computes | 09, 10, 12 |
| What data moves where | 11 |
| What to build it with | 13, 14 |
| How to prove it works | 15, 16 |
| What it cannot do | 18, 19 |
| How to write the paper | 21 |

## 10. Current Project Maturity

| Aspect | Status |
|---|---|
| Research framing and problem definition | **Finalised** |
| System architecture | **Finalised** |
| Mathematical formulation | **Finalised** for connectivity, geometry, and calibration; **proposed** for the evidence-gate policy |
| Core geometry implementation (`Löwdin`, SPD guard, tangent space, alignment arms) | **Implemented and validated** on synthetic and real cohort data |
| Ingestion and preprocessing | **Implemented** for all target formats |
| Spatio-temporal network (GATv2, Transformer, BiGRU) | **Designed; not yet trained** |
| Calibration and abstention layer | **Designed; not yet fitted** |
| Three-panel workbench | **Designed; not yet built** |
| Full ablation ladder | **Planned** |
| External-cohort validation | **Planned** |

## 11. Confirmed versus Proposed

**Confirmed (verified by executed code or direct data inspection).**

- The 121-subject benchmark cohort schema, channel set, sampling rate, and class balance.
- Global joint Löwdin orthogonalisation produces positive semi-definite matrices by construction.
- Pairwise-symmetrised orthogonalised envelope correlation fails positive semi-definiteness on
  band-limited segments.
- Subject-disjoint alignment arms reduce ranking performance relative to the unaligned arm on the
  benchmark cohort.
- A classifier built from recording-quality proxies alone carries appreciable discriminative
  information on the same labels.

**Proposed (designed, not yet established).**

- That the dual-path decomposition recovers the ranking capacity lost to alignment.
- That selective abstention raises specificity and positive predictive value at fixed sensitivity.
- That the spatio-temporal graph encoder outperforms flattened-vector baselines.
- That aperiodic spectral structure is gain-invariant under acquisition variation.

**Not yet specified.**

- Exact hyperparameter values for the graph and temporal encoders.
- The calibrated form of the evidence-gate decision rule.
- Definitive per-task sample sizes on the external cohort.
