# 18 — Limitations and Assumptions

## 1. Known Technical Scope

| Limitation | Implication |
|---|---|
| Single modality (scalp EEG, 19 channels, 128 Hz) | Findings are specific to this recording configuration |
| Resting paradigm only | Active-task behaviour is not covered without revalidation |
| Paediatric population | No generalisation to adults |
| Moderate cohort size (121 participants) | Confidence intervals are wide; single-split values are unstable |
| Offline, single-process pipeline | Not a high-throughput clinical service |

## 2. Assumptions

**A1 — Alignment deletes trait-level diagnostic structure.** The premise that unsupervised covariance
alignment removes static between-subject diagnostic signal as well as nuisance. **Status:** hypothesis
with kill condition (H1); not established.

**A2 — Aperiodic exponent is diagnostically informative for attention.** **Status:** hypothesis (A2 in
the gap document); requires literature validation.

**A3 — Bifactor psychopathology dimensions are EEG-decoding-specific.** **Status:** hypothesis (A3);
central to the external generalisation arm and untested.

**A4 — Neural discrimination survives artifact control.** **Status:** load-bearing hypothesis (H3).

**A5 — Positive semi-definite connectivity is necessary and sufficient for the geometric operations
used.** The Riemannian operations require positive definite inputs; the design enforces this and
reports violations.

## 3. Technical Constraints

1. **Definiteness.** No matrix enters a geometric operation without passing the SPD guard.
2. **Calibration hygiene.** Calibration statistics are fitted on training folds only.
3. **Protocol.** No participant appears in more than one fold.
4. **Attribution.** A result may not be attributed to an architectural rung without the preceding rung's
   measurement.
5. **Attrition reporting.** Every exclusion is recorded with group membership.

## 4. Implementation Constraints

1. **Offline.** No inference-time network dependency.
2. **Dependency-light.** Geometry and connectivity are native NumPy, for auditability.
3. **Reproducibility.** All stochastic steps seeded; configuration hashed.

## 5. Not Yet Specified

| Item | Status |
|---|---|
| AQI scalar aggregation function | Not finalised |
| Evidence-gate threshold function | Not finalised |
| Calibration method (isotonic vs temperature) | Not selected |
| Panel 3 stability metric | Candidate: split-half ICC |
| Encoder hyperparameters | Not finalised |
| External-cohort per-task sample sizes | To be determined |

## 6. Boundary on Claims

This project does not claim that ADHD is decodable from 19-channel resting EEG. It may conclude the
opposite; both outcomes are within scope. Any claim about the neurobiological origin of a signal is
conditional on the artifact-controlled result.
