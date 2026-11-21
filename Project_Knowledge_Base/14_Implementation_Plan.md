# 14 — Implementation Plan

## 1. Strategy

Development proceeds in dependency order: geometry and ingestion first (they are testable in isolation
and underpin everything), then representation, then learning, then the product layer. Each phase has a
hard exit gate; the next phase does not begin until the gate is met. This ordering is deliberate — the
product layer is the most visible and the least scientifically necessary, so it is placed last to
prevent it from consuming the schedule.

## 2. Phase Breakdown

### Phase 0 — Foundation

**Deliverables.**

- Canonical montage definition and bidirectional channel mapping.
- Multi-format ingestion including median imputation and provenance recording.
- Band definitions: delta 0.5–4, theta 4–8, alpha 8–13, beta 13–30, gamma 30–45 Hz.
- Reference bad-channel rule implementation.

**Exit gate.** Reads every supported format; produces a canonical 19×N matrix with a provenance record;
the bad-channel rule reproduces the reference thresholds.

### Phase 1a — Geometry and Spectral Stack

**Deliverables.**

- Joint Löwdin orthogonalisation.
- Hilbert envelope correlation.
- SPD guard with integrity statistics.
- Fréchet mean and tangent projection.
- Alignment arms (none / Euclidean / Riemannian / band-limited Riemannian).
- SpecParam fit with R² acceptance.

**Exit gate.** Connectivity matrices are positive semi-definite by construction; the guard records zero
silent violations; alignment arms execute on real cohort data; the spectral fit produces exponent arrays
with recorded acceptance.

### Phase 1b — Baselines and Ablation Ladder

**Deliverables.**

- Reference-baseline reproduction under subject-disjoint protocol.
- Artifact-only model.
- Artifact-controlled neural model.
- Alignment ablation.
- Five-rung ablation ladder: joint Löwdin → spectral priors → dual-path → five-lobe GATv2 → AQI gate.
- Evaluation harness: nested group k-fold, leave-one-subject-out, permutation null, participant-level
  aggregation, risk–coverage computation.

**Exit gate.** All hypotheses (H1–H5) have a measured answer; the ladder isolates the contribution of
each rung; the risk–coverage curve is produced.

### Phase 1c — Learning Components

**Deliverables.**

- Dual-path fusion layer.
- Five-lobe GATv2 spatial encoder.
- Parallel Transformer + BiGRU temporal encoder.
- Calibration layer and evidence gate.

**Exit gate.** Models train under the fixed protocol; calibration is fitted on training folds only;
gate decisions are reproducible from the seed and configuration.

### Phase 1d — Product Layer

**Deliverables.**

- Result-record schema.
- Three-panel workbench: screening, reliability, topology.
- Risk–coverage rendering; per-group attrition table; window timeline; reproducibility badge;
  connectivity-integrity line.
- Split-half stability metric on Panel 3.

**Exit gate.** Runs offline on the benchmark cohort and on an external `.set` mini-set; every panel is
populated from the record alone.

### Phase 2 — External Generalisation Arm

**Deliverables.**

- External-cohort ingestion and artefact-control replication.
- Bifactor dimension decoding with an equivalence bound and a power calculation.
- Dual-cohort risk–coverage reporting.

**Exit gate.** Either a positive generalisation result or a reported negative result with the stated
power; in both cases the graded claim remains anchored on the primary cohort.

## 3. Testing Strategy

| Level | Test type | Criterion |
|---|---|---|
| Unit — connectivity | Definiteness property test | All constructed matrices positive semi-definite |
| Unit — guard | Correction accounting | Recorded corrections equal applied corrections |
| Unit — geometry | Round-trip test | Log then exp returns the original matrix within tolerance |
| Unit — spectral | Synthetic recovery | Known exponent recovered from synthetic spectra |
| Unit — ingestion | Format equivalence | Same recording in two formats yields identical canonical matrix |
| Integration — pipeline | End-to-end determinism | Same seed and input yield byte-identical result record |
| Statistical — evaluation | Null calibration | Permutation null centred at 0.5 |
| Protocol — leakage | Group disjointness assertion | No participant appears in two folds |

## 4. Validation Methodology

1. **Structural validation** on synthetic signals with known properties (definiteness, exponent recovery,
   alignment behaviour).
2. **Cohort validation** on the benchmark dataset under subject-disjoint partitioning.
3. **Confound validation** via artifact-only and artifact-controlled models on identical folds.
4. **Generalisation validation** on the external cohort.

## 5. Risk-Managed Sequencing Rules

1. No product-layer work until the ablation ladder (Phase 1b) is complete.
2. No external-cohort work until the primary cohort results are stable under repeated partitioning.
3. No architectural additions beyond the specified five rungs.
4. Every phase publishes its result record; a phase without a record is not complete.

## 6. Reproducibility Requirements

- All seeds recorded.
- Configuration files hashed into every result.
- Model checkpoints hashed.
- Environment lock file maintained.
- Every reported number traceable to a result file.
