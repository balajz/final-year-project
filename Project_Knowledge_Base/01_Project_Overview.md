# 01 — Project Overview

## 1. Research Identity

| Attribute | Value |
|---|---|
| Working title | Calibrated, Artifact-Aware Paediatric EEG Screening via Riemannian-Tangent Spatio-Temporal Graph Learning with Selective Abstention |
| Research domain | Neuro-AI / clinical decision support |
| Subdomain | Scalp EEG signal processing and machine learning |
| Primary technical theme | Calibration, artifact robustness, and selective prediction |
| Classification | Applied machine learning; measurement science; critical benchmark evaluation |
| Modality | Resting-state scalp electroencephalography (19 channels, 128 Hz) |
| Population | Paediatric neurodevelopmental screening (attention-deficit/hyperactivity disorder as the primary target construct) |

## 2. What the Project Proposes

A locally executable screening workbench that consumes a single paediatric EEG recording and emits a
calibrated triage index together with an explicit evidential statement. The system separates three
outputs that conventional classifiers conflate:

1. A **calibrated risk index** with a prevalence-aware operating point.
2. A **signal-quality verdict** that may be *"insufficient evidence — abstain"*.
3. A **reliability report** describing where in the recording the decision originated and how much
   of it survives artifact and preprocessing variation.

The system never outputs a diagnosis. It outputs a triage opinion with quantified uncertainty.

## 3. What It Does

The pipeline performs, in sequence:

1. Multi-format ingestion and canonicalisation to a fixed 19-channel montage.
2. Artifact Quality Index (AQI) scoring on the raw recording.
3. Trend removal, bad-channel identification, band separation, and aperiodic/periodic decomposition.
4. Global joint Löwdin orthogonalisation of the channel space, followed by Hilbert-envelope
   correlation to form an echo-suppressed connectivity matrix.
5. Runtime positive-definiteness auditing and spectral repair with logged correction magnitude.
6. Riemannian tangent-space projection of the connectivity manifold.
7. Dual-path feature construction: a gain-invariant trait path from the aperiodic exponent and a
   per-subject aligned state path from dynamic connectivity.
8. Spatio-temporal graph encoding over a five-lobe, nineteen-node cortical graph.
9. Calibrated classification with an evidence gate that may withhold prediction.
10. Three-panel presentation of the result, the reliability evidence, and the cortical topology.

## 4. How It Works — Conceptual Principle

The central technical premise is that **between-subject variation in EEG covariance is dominated by
non-diagnostic factors** — skull thickness, scalp impedance, electrode placement, and cortical folding.
Two mechanisms address this:

- **Geometry.** Aligning each participant's covariance matrix to a common reference removes
  first- and second-order subject-specific offsets. The project uses Riemannian (Fréchet-mean)
  re-centering and Euclidean alignment as alternative arms.
- **Gain invariance.** The aperiodic component of the power spectrum is characterised by an exponent
  that is invariant to a vertical gain offset. Retaining this quantity as a separate feature path
  preserves subject-level structure that covariance alignment would otherwise erase.

The project's architectural response to the alignment/identity trade-off is to compute **both** paths
and fuse them, rather than choosing one.

## 5. Why It Is Needed

At a screening prevalence of 5% to 10%, the clinical usefulness of a triage instrument is governed by
its false-positive behaviour. A sensitivity of 80% paired with specificity of 44.44% yields a positive
predictive value of approximately 13.79% at 10% prevalence — that is, the majority of positive
findings are false. Improving ranking quality by a small margin does not materially change this. The
project therefore targets the quantity that does: the ability to identify and withhold decisions on
recordings that cannot support one.

## 6. What Distinguishes It From Conventional Approaches

| Conventional practice | This project |
|---|---|
| Flattened connectivity vector | Five-lobe, nineteen-node spatial graph preserving cortical topology |
| Zero-lag Pearson correlation with hand-set threshold | Global joint Löwdin orthogonalised envelope connectivity with a learnable sparse edge gate |
| Raw band-power ratios | SpecParam aperiodic/periodic separation with a goodness-of-fit acceptance criterion |
| Global train-set standardisation | Dual-path trait (gain-invariant) plus state (per-subject aligned) decomposition |
| Amplitude thresholding and forced prediction | First-class artifact-aware abstention with a risk–coverage report |
| Single headline AUROC | Specificity at fixed sensitivity and positive predictive value at stated prevalence |
| Reporting neural performance alone | Artifact-only and artifact-controlled performance reported on identical folds |

## 7. Project Structure — Engine and Product

**C0 — Engine.** The signal-processing, geometry, and learning stack that produces the index. This is
where the technical contributions reside.

**C5 — Product.** The three-panel workbench that exposes the index, its reliability, and its
evidentiary basis to a non-specialist reviewer. The workbench is the delivery vehicle; the graded
claim is the numeric rescue of specificity and predictive value.

## 8. Scope Boundaries

- Not a diagnostic device and not clinically validated.
- Not a benchmark harness for third-party models.
- Not a general-purpose EEG platform: one engine, one population, one product.
- Cross-dataset pooling is prohibited; the confound of learning acquisition hardware is treated as a
  defect rather than a convenience.
- Foundation-model benchmarking is out of scope; comparison is against the reference baseline.
- Multimodal fusion is not pursued for its own sake.

## 9. Deliverable Summary

| Layer | Artefact | Grading relevance |
|---|---|---|
| Engine | Riemann-ST-GraphFormer with Evidence Gate | Technical contribution |
| Evaluation | Subject-disjoint nested cross-validation and leave-one-subject-out with permutation nulls | Scientific validity |
| Product | Three-panel offline workbench | Demonstrable engineering artefact |
| Claim | Specificity and predictive-value rescue at fixed sensitivity | The graded result |
