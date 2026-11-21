# 21 — IEEE Paper Preparation Notes

> This section is operational guidance for manuscript preparation. It is separate from the project
> description and contains no project claims.

## 1. Paper Structure Mapping

| IEEE section | Source documents | Notes |
|---|---|---|
| Title | 02 | Working title in `02`; shorten for camera-ready |
| Abstract | 02 §1 | Must add measured specificity/PPV values replacing the 44.44%/13.79% baseline |
| Index Terms | 02 §3 | Choose 5–8; align with the venue's taxonomy |
| Introduction | 03 §1–2, 04 §1 | Motivate through the false-alarm bottleneck, not through accuracy |
| Related Work | *To be written from verified literature* | See §3 below; do NOT invent |
| Problem Formulation | 03 §3, 12 §10 | Formal objective with the bounded-AUROC constraint |
| Proposed Methodology | 06, 09, 10 | Emphasise the dual-path and Löwdin contributions |
| System Architecture | 07, diagrams | Include the Mermaid architecture as a rendered figure |
| Algorithm Design | 10 | Algorithms 1–2 are the strongest novel content |
| Implementation | 13, 14 | Note the NumPy-native constraint as a reproducibility feature |
| Experimental Setup | 15 §1–11 | State the protocol before any result |
| Results and Discussion | 15 §12, 16 | Provisional values must be replaced by final runs |
| Conclusion | 20 | Do not overstate |
| Future Work | 19 | Prioritise the artifact-controlled experiment |

## 2. Claims Requiring Literature Citations

Each claim below must be supported by a verified reference before submission. None may be asserted from
memory.

| # | Claim | Where used |
|---|---|---|
| L1 | Reported EEG-ADHD accuracy is commonly 93–99% under window-level splitting | Intro, Gap |
| L2 | Subject-disjoint performance clusters near 0.74–0.79 AUROC on this cohort | Gap G1 |
| L3 | The reference baseline reports 44.44% specificity and 13.79% PPV at 10% prevalence | Problem P-2 |
| L4 | Zero-lag correlation is dominated by volume conduction | Background |
| L5 | Orthogonalised envelope correlation mitigates instantaneous leakage | Background |
| L6 | Covariance matrices form a Riemannian manifold under the affine-invariant metric | Background |
| L7 | The Fréchet mean is the geometrically correct average on that manifold | Method |
| L8 | The aperiodic exponent is invariant to multiplicative gain | Method |
| L9 | The 1/f model with periodic components is a valid spectral description of EEG | Method |
| L10 | Graph attention is effective for EEG topology | Method |
| L11 | At low prevalence, PPV is dominated by specificity | Problem P-2 |
| L12 | Artifact burden differs systematically between clinical and control paediatric recordings | Problem P-3 |

**Status of the corpus.** The project's working corpus contains the reference baseline and a
foundation-model benchmark on the same cohort, both reporting values in the subject-disjoint range. A
systematic literature review is required for L1, L5, L6, L7, L8, L10, and L12 before submission.

## 3. Related Work — Construction Guidance

Do not fabricate a Related Work section. Build it from verified sources in four clusters:

1. **EEG-ADHD classification and its evaluation protocols.** Establish the window-versus-subject split
   gap (L1, L2).
2. **Connectivity estimation and volume conduction.** Orthogonalisation, envelope correlation, leakage
   suppression (L4, L5).
3. **Riemannian geometry for EEG.** Tangent space, alignment, domain adaptation (L6, L7).
4. **Calibration, selective prediction, and abstention.** Risk–coverage, conformal and selective
   methods, PPV at low prevalence (L11).

Each cluster should end with the gap the project fills.

## 4. Claims Requiring Experimental Validation

| # | Claim | Experiment |
|---|---|---|
| V1 | Dual-path recovers alignment loss | H1, ablation R3 |
| V2 | Abstention raises specificity and PPV | H4, risk–coverage |
| V3 | Artifact-only performance is appreciable | H2, artifact-only model |
| V4 | Neural signal survives artifact control | H3, artifact-controlled model |
| V5 | Five-lobe graph outperforms flattened features | Ablation R4 |
| V6 | Joint Löwdin reduces definiteness violations to zero | H5, guard statistics |
| V7 | Mechanism transfers to an external cohort | External arm |

## 5. Research Hypotheses (restated for the manuscript)

H1 alignment deletes trait signal / dual-path recovers it · H2 artifact-only carries signal · H3 neural
signal survives artifact control · H4 abstention raises specificity and PPV · H5 joint Löwdin needs
rare corrections. Each is stated with an explicit kill condition in `06_Proposed_Solution.md` §4.

## 6. Recommended Evaluation Metrics (manuscript order)

1. Specificity at Se = 0.80 (primary)
2. PPV at 5% and 10% (primary)
3. Risk–coverage curves (primary for H4)
4. AUROC with DeLong test vs baseline (secondary)
5. AUPRC (secondary)
6. Brier score and ECE (secondary, calibration)
7. NPV at 5% and 10% (secondary)
8. SPD integrity statistics (secondary, reliability)

## 7. Required Comparative Studies

| Study | Purpose | Mandatory |
|---|---|---|
| Reference-baseline reproduction under this protocol | Fair comparison | Yes |
| Alignment ablation (none / Euclidean / Riemannian / band-limited) | H1 attribution | Yes |
| Artifact-only model | H2, confound floor | Yes |
| Artifact-controlled neural model | H3, attribution | Yes — load-bearing |
| Ablation ladder R0–R5 | Component attribution | Yes |
| External-cohort replication | Transfer | Yes (generalisation arm) |
| Trained-encoder vs linear probe | Is the encoder earning its complexity | Recommended |

## 8. Proposed Figures and Tables

**Figures.**

| # | Content | Source |
|---|---|---|
| F1 | System architecture diagram | `diagrams/system_architecture.mmd` |
| F2 | End-to-end workflow | `diagrams/system_workflow.mmd` |
| F3 | Data flow | `diagrams/data_flow.mmd` |
| F4 | Risk–coverage curves (IEEE-121 and external) | Panel 2 output |
| F5 | Connectivity-integrity distribution (n_not_psd, min eigenvalue) | SPD guard output |
| F6 | Window-level quality timeline with abstained segments | Panel 2 output |
| F7 | Nineteen-node lobe graph coloured by exponent, with stability | Panel 3 output |
| F8 | Calibration reliability diagram | Calibration output |
| F9 | Permutation null with the observed value marked | Evaluation output |

**Tables.**

| # | Content |
|---|---|
| T1 | Comparison against the reference baseline (all metrics) |
| T2 | Ablation ladder R0–R5 with attribution |
| T3 | Alignment ablation (four arms) |
| T4 | Artifact-paired results (neural / artifact-only / artifact-controlled) |
| T5 | Per-group attrition |
| T6 | External-cohort replication |
| T7 | Coverage sweep (specificity, PPV, retained fraction) |

## 9. Information Remaining Unspecified

| Item | Impact on manuscript |
|---|---|
| AQI aggregation function | Methods section cannot be finalised |
| Evidence-gate threshold function | Algorithm block incomplete |
| Calibration method selection | Methods section incomplete |
| Panel 3 stability metric | Figure F7 cannot be finalised |
| Encoder hyperparameters | Reproducibility statement incomplete |
| External-cohort per-task n | Statistical power statement incomplete |
| Final measured values (X, Y, Z) | Abstract and Results cannot be finalised |

## 10. Manuscript Integrity Checklist

- [ ] Every numeric value traceable to a result artefact
- [ ] Provisional values in `15` §12 regenerated under the frozen configuration
- [ ] No value attributed to an architectural rung without the preceding rung's measurement
- [ ] No specificity gain attributed to abstention if it was produced by the feature set
- [ ] Every neural AUROC accompanied by its artifact-only and artifact-controlled counterparts
- [ ] AUROC never headlined
- [ ] All literature claims backed by verified references
- [ ] Limitations section mirrors `18` honestly
- [ ] Reproducibility statement complete (seeds, config hashes, environment)
- [ ] No claim of clinical validity
