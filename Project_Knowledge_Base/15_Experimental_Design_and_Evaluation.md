# 15 — Experimental Design and Evaluation

> This section specifies the evaluation plan. It contains the protocol and the metrics definitions.
> Measured values, where they exist, are confined to Section 12 and are explicitly labelled as
> provisional.

## 1. Experimental Objectives

| ID | Objective | Corresponding hypothesis |
|---|---|---|
| E1 | Establish the subject-disjoint baseline operating point | — (reference reproduction) |
| E2 | Measure the alignment–signal trade-off | H1 |
| E3 | Quantify artifact-only discriminability | H2 |
| E4 | Quantify artifact-controlled neural discriminability | H3 |
| E5 | Measure abstention benefit on specificity and PPV | H4 |
| E6 | Assess connectivity-matrix integrity | H5 |
| E7 | Isolate the contribution of each architectural rung | — (ablation) |
| E8 | Test transfer of the abstention/calibration mechanism | — (generalisation) |

## 2. Partitioning Protocol

**Primary.** Nested group k-fold cross-validation with k = 5. Grouping is by participant; no participant
appears in more than one fold. Hyperparameters are selected in an inner loop; the outer loop provides
unbiased estimates.

**Secondary.** Leave-one-subject-out. Provides a low-bias estimate at high computational cost; used to
confirm that the k-fold result is not an artefact of fold construction.

**Aggregation.** Window-level predictions are averaged to participant level **before** any metric is
computed. Window-level metrics may be computed for internal diagnostics but are never reported as
performance.

**Repetition.** The primary protocol is repeated across multiple random partitions to obtain a
distribution rather than a point estimate.

**Explicit exclusion.** Window-level splitting is prohibited in any reported result.

## 3. Test Scenarios

| Scenario | Purpose |
|---|---|
| S1 — Primary cohort, subject-disjoint k-fold | Main result |
| S2 — Primary cohort, leave-one-subject-out | Confirmatory result |
| S3 — Alignment arms | Trade-off measurement |
| S4 — Artifact-only model | Confound quantification |
| S5 — Artifact-controlled neural model | Attribution of neural performance |
| S6 — Coverage sweep | Risk–coverage behaviour |
| S7 — External cohort, same architecture | Generalisation |
| S8 — Bifactor dimension decoding | Transdiagnostic specificity |

## 4. Baselines and Comparators

| Comparator | Role | Notes |
|---|---|---|
| Reference baseline | Primary comparison | Hybrid spatio-temporal graph transformer with dynamic functional connectivity on the same cohort; reports 63.16% accuracy, 0.7444 test AUROC, 0.7770 leave-one-subject-out AUROC, 44.44% specificity, 13.79% PPV at 10% prevalence |
| Unaligned geometry arm | Ablation | Isolates the effect of alignment |
| Artifact-only model | Negative control | Establishes the confound floor |
| Artifact-controlled neural model | Attribution control | Establishes neural contribution |
| Majority-class predictor | Sanity floor | Confirms metrics behave under class imbalance |

Comparisons are made under identical folds. No comparison is made against models evaluated under a
different partitioning protocol.

## 5. Evaluation Metrics

**Primary (graded).**

| Metric | Definition | Prevalence |
|---|---|---|
| Specificity at Se = 0.80 | 1 − false-positive rate at the operating point achieving 80% sensitivity | — |
| PPV at 5% | (Se·π) / (Se·π + (1−Sp)(1−π)) | π = 0.05 |
| PPV at 10% | as above | π = 0.10 |

**Secondary.**

| Metric | Purpose |
|---|---|
| AUROC | Comparability with published work; never headlined |
| AUPRC | Informative under class imbalance |
| Accuracy, balanced accuracy | Reference to baseline reporting |
| Brier score | Calibration quality |
| Expected calibration error | Calibration reliability |
| Risk–coverage curve | Abstention behaviour |
| NPV at 5% and 10% | Rule-out utility |

**Uncertainty.**

| Quantity | Method |
|---|---|
| Confidence intervals | Bootstrap over participants |
| Significance of AUROC difference | DeLong's test |
| Significance of observed discrimination | Permutation null over participant labels on identical folds |
| Stability | Distribution over repeated partitions |

## 6. Ablation Ladder

Each rung adds exactly one element to the preceding rung, so attribution is unambiguous.

| Rung | Cumulative configuration | Question answered |
|---|---|---|
| R0 | Reference baseline reproduction | What does the baseline achieve under this protocol? |
| R1 | + Joint Löwdin oAEC + SPD guard | Does the connectivity estimator matter? |
| R2 | + SpecParam aperiodic node priors | Does the spectral decomposition matter? |
| R3 | + Dual-path trait/state | Does retaining gain-invariant structure recover alignment loss? |
| R4 | + Five-lobe GATv2 | Does topology-aware encoding matter? |
| R5 | + AQI abstention gate | Does abstention raise specificity and PPV? |

**Attribution rule.** No result may be attributed to rung R_n without the R_{n−1} measurement. In
particular, the specificity gain observed at R1 must be attributed to the connectivity and feature set,
not to the architecture introduced at R4.

## 7. Confound-Control Design

This is the component that distinguishes the evaluation from conventional practice.

1. **Artifact-only model.** Logistic regression on recording-quality proxies (duration, blink-band
   amplitude, muscle-band ratio, global amplitude). Fitted on identical folds.
2. **Artifact-controlled neural model.** Either (a) regress the proxies out of the neural feature space
   before fitting, or (b) stratify the cohort by proxy value and evaluate within strata.
3. **Mandatory joint reporting.** Neural AUROC, artifact-only AUROC, and artifact-controlled AUROC are
   reported together in the same table. A neural result reported without its artifact control is
   considered incomplete.

**Interpretation rule.**

- If artifact-controlled neural AUROC ≈ neural AUROC ≫ artifact-only AUROC → neural signal is real.
- If neural AUROC ≈ artifact-only AUROC ≫ artifact-controlled AUROC → the result is largely recording
  quality.
- If all three ≈ 0.5 → no usable signal.

## 8. Connectivity-Integrity Measurement

For every evaluated window, record `n_not_psd`, raw minimum eigenvalue, and L1 correction magnitude.
Report aggregate statistics and their correlation with performance. If corrections are frequent or
large, the graph-based results are reported as low-confidence.

## 9. Validation Methodology

| Level | Method |
|---|---|
| Structural | Synthetic signals with analytically known properties |
| Protocol | Assertion that folds are participant-disjoint |
| Null | Permutation distribution centred at 0.5 |
| Confound | Artifact-only and artifact-controlled comparators |
| Transfer | External cohort under the same architecture |

## 10. Reproducibility Considerations

- Fixed seeds recorded per run.
- Configuration hash and checkpoint hash in every result record.
- Environment lock file.
- Deterministic ordering of file discovery.
- Feature caches stored with their generating configuration hash.
- Every reported number traceable to a result artefact.

## 11. Threats to Validity

| Threat | Mitigation |
|---|---|
| Fold-construction variance at moderate n | Repeated partitioning; report distribution, not a single split |
| Artifact confounding | Artifact-paired evaluation |
| Inclusion-criteria creep | Thresholds frozen before test evaluation |
| Attrition bias from artifact exclusion | Per-group attrition table mandatory |
| Optimistic hyperparameter selection | Nested inner loop |
| Multiple comparisons across metrics | Pre-specify primary metrics; treat the rest as secondary |

## 12. Provisional Measured Values (Not Final)

> The following values were obtained during development on the 121-subject benchmark cohort. They are
> reported to document the current state, not as established results. They must be regenerated under
> the final frozen configuration before appearing in a paper.

| Quantity | Provisional value | Configuration |
|---|---|---|
| Unaligned AUROC (repeated grouped 5-fold, 10 repeats) | 0.9081 ± 0.0089, range 0.8981–0.9306 | Tangent + band-connectivity features, logistic regression |
| Permutation null (200 permutations) | mean 0.488, sd 0.067, 95th percentile 0.596, max 0.666; p = 0.005 | Identical folds |
| Euclidean-alignment arm AUROC | 0.8109 | Same feature set |
| Riemannian-alignment arm AUROC | 0.7995 | Same feature set |
| Band-limited Riemannian arm AUROC | 0.7667 | Same feature set |
| Artifact-only AUROC (repeated grouped 5-fold) | 0.8089 ± 0.0664, range 0.5779–0.9259 | Duration, frontal variance, frontal delta power, muscle-band power, total variance |
| Correlation between muscle-band ratio and gamma power | −0.049 | Feature diagnostics |

**Interpretation constraints — binding on all downstream reporting.**

1. **No architectural attribution.** The unaligned 0.9081 is a *feature-set* baseline. It must not be
   attributed to the dual-path decomposition, the graph encoder, or the abstention gate, none of which
   are present in that configuration.
2. **No neurobiological attribution.** The artifact-only value (0.8089 ± 0.0664) is close enough to the
   neural value that the confound is live. Until the artifact-controlled experiment is completed, the
   neural value may not be described as reflecting neurobiology.
3. **No frontier refutation.** These provisional values do not contradict the published frontier
   (approximately 0.74–0.79 AUROC). They measure a different, unvalidated configuration, and the
   artifact floor is unexplained. The frontier claim refers to the published corpus.
4. **Instability warning.** The artifact-only range across repeated partitions (0.5779–0.9259) shows that
   a single-split estimate can appear far higher than its mean. Any single-split number is therefore
   uninformative on its own and must be reported with its partition distribution.
5. **Status.** All values in this subsection are provisional development measurements and must be
   regenerated under the frozen final configuration before appearing in a manuscript.
