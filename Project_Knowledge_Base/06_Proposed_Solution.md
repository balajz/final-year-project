# 06 — Proposed Solution

## 1. Solution Concept

The system is organised as two layers sharing one engine.

**C0 — Riemann-ST-GraphFormer with Evidence Gate.** A signal-processing, geometric, and learning stack
that maps a multichannel recording to a calibrated probability and an evidential state.

**C5 — Reliability Workbench.** A three-panel presentation layer that exposes the index, the
reliability evidence behind it, and the cortical topology it was derived from.

The conceptual operating principle is **decision with an explicit evidence budget**. Rather than
emitting a probability always, the system estimates whether the recording supports a decision at all,
and if not, emits an abstention with the reason.

## 2. Operating Principle

Given a recording **X** ∈ ℝ^{C×N}:

1. **Assess quality before modelling.** Compute an Artifact Quality Index from band-limited power
   ratios, blink-band amplitude, and flatline/clipping detection.
2. **Suppress volume conduction geometrically.** Orthogonalise the channel space jointly across all
   channels before envelope extraction, so that subsequent correlation reflects lagged rather than
   instantaneous interaction.
3. **Separate aperiodic from periodic content.** Fit the spectral model, accept only well-fitting
   spectra, and extract the aperiodic exponent.
4. **Represent connectivity on its manifold.** Project matrices to the tangent space at a geometric
   reference so that linear operations are valid.
5. **Preserve two kinds of information.** Retain the gain-invariant trait path and the aligned state
   path, fusing them rather than discarding either.
6. **Encode topology and time.** Apply graph attention over a five-lobe cortical graph, then a
   parallel temporal encoder over window sequences.
7. **Calibrate and gate.** Map the representation to a calibrated probability; decide accept or
   abstain from the evidence index and a coverage target.
8. **Report with an audit trail.** Present the index, the risk–coverage behaviour, and the graph with
   a stability metric.

## 3. Design Rationale

| Design decision | Rationale | Alternative rejected because |
|---|---|---|
| Joint Löwdin orthogonalisation | Produces a genuine Gram matrix ⇒ positive semi-definite by construction; order-independent; symmetric | Pairwise-symmetrised orthogonalised envelope correlation averages scalars rather than forming a Gram matrix; violates positive semi-definiteness on band-limited data |
| Dual-path trait + state | Alignment necessarily removes all static between-subject structure, including diagnostic structure | Single-path alignment risks deleting the trait signal along with nuisance |
| SpecParam aperiodic exponent as node prior | Gain-invariant: invariant to vertical offset under multiplicative scaling | Raw band power conflates periodic oscillation with 1/f background and is sensitive to gain |
| Five-lobe graph | Preserves cortical topology; 19 nodes, not a 171-dimensional flattened vector | Flattening discards adjacency structure entirely |
| Selective abstention | At low prevalence, specificity governs utility; abstention is the only lever that raises specificity without lowering sensitivity | Threshold tuning trades sensitivity for specificity; abstention does not |
| Reporting artifact-only performance | Without it, no discrimination can be attributed to neurobiology | Reporting neural performance alone leaves the confound unquantified |

## 4. Hypotheses and Kill Conditions

Each hypothesis is falsifiable by a named experiment. A hypothesis whose kill condition is met is
reported as a negative result; the project is structured so that negative results remain valid
contributions.

| ID | Hypothesis | Predicted outcome | Kill condition |
|---|---|---|---|
| H1 | Alignment alone deletes trait signal; dual-path recovers it | Unaligned AUROC > aligned AUROC; dual-path restores most of the gap | If dual-path does not recover the gap, alignment is dropped and reported as harmful on this cohort |
| H2 | An artifact-only classifier achieves appreciable AUROC | Artifact proxies alone are meaningfully above chance | If artifact-only AUROC ≈ 0.5, P-3 is not a live confounder and the AQI panel loses its central justification |
| H3 | Neural signal survives artifact control | Artifact-controlled AUROC stays close to uncontrolled | If it collapses toward chance, the headline becomes "the frontier is recording-quality prediction" — still a valid contribution, but the product claim changes |
| H4 | Selective abstention raises specificity and PPV at fixed sensitivity | Risk–coverage curve rises monotonically as coverage falls | If specificity does not rise with abstention, the AQI gate is cosmetic and must be removed |
| H5 | Joint-Löwdin graphs require infrequent SPD correction | Corrections rare and small | If corrections are frequent or large, the graph panel must be demoted to low-confidence |

H3 is load-bearing: its outcome determines which of two valid theses the paper reports.

## 5. Solution Delineation — What Is and Is Not Built

**Built.**

- Multi-format ingestion with canonicalisation.
- Artifact Quality Index.
- Preprocessing: trend removal, reference bad-channel rule, band separation, spectral parameterisation.
- Joint Löwdin connectivity with SPD guard and tangent-space projection.
- Alignment arms (none / Euclidean / Riemannian / band-limited Riemannian) for ablation.
- Dual-path feature construction.
- Spatio-temporal graph encoder.
- Calibration and evidence gate.
- Three-panel workbench.
- Evaluation harness: subject-disjoint CV, permutation null, artifact controls, risk–coverage.

**Not built.**

- Any diagnostic output path.
- Multi-site pooled training.
- Multimodal input paths.
- A foundation-model benchmarking zoo.
- A caregiver-facing interface in the graded scope.

## 6. Position Relative to the Reference Baseline

The reference baseline is a hybrid spatio-temporal graph transformer with dynamic functional
connectivity for ADHD classification on the same 121-child cohort. The proposed system retains the
problem formulation and the cohort, and changes five specific things: the connectivity estimator, the
spectral decomposition, the normalisation strategy, the artifact treatment, and the reported metric.
This keeps the comparison interpretable — differences in performance are attributable to enumerated
changes rather than to a wholesale redesign.

| Dimension | Reference baseline | This project |
|---|---|---|
| Spatial representation | Flattened connectivity vector | Five-lobe 19-node graph |
| Connectivity | Zero-lag Pearson correlation, fixed threshold | Joint Löwdin orthogonalised envelope correlation + learnable sparse gate + SPD guard |
| Spectral handling | Raw band-power ratios (theta/beta) | SpecParam 1/f separation with fit acceptance criterion |
| Normalisation | Global train-set z-scoring | Dual-path trait (gain-invariant) + state (per-subject aligned) |
| Artifact handling | Amplitude thresholding; forced prediction | AQI selective abstention |
| Reported metric | Accuracy, AUROC | Specificity at fixed sensitivity, PPV at stated prevalence |
