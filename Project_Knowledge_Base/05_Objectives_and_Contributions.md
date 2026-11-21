# 05 — Objectives and Contributions

## 1. Primary Objective

Construct and evaluate a calibrated, artifact-aware paediatric EEG screening workbench that rescues
specificity and positive predictive value at fixed sensitivity relative to the reference baseline,
under strict subject-disjoint evaluation, without depending on improved raw discrimination.

## 2. Secondary Objectives (specific and measurable)

| # | Objective | Success criterion |
|---|---|---|
| O1 | Reproduce the reference baseline under subject-disjoint protocol | Reproduce its reported operating point (approximately 63.16% accuracy / 0.7444 test AUROC / 0.7770 leave-one-subject-out AUROC; 44.44% specificity) |
| O2 | Implement and verify the positive-definiteness-guaranteed connectivity construction | Zero silent manifold violations; all corrections logged and reported |
| O3 | Measure the alignment–signal trade-off | Rank ordering of the unaligned, Euclidean-aligned, and Riemannian-aligned arms established on the cohort |
| O4 | Demonstrate the dual-path recovery | Aligned-plus-trait-path AUROC recovers a defined fraction of the loss incurred by alignment alone |
| O5 | Measure the artifact confound | Artifact-only and artifact-controlled AUROC quantified on identical folds |
| O6 | Demonstrate selective-abstention benefit | Specificity and PPV rise as coverage falls, reflected in the risk–coverage curve |
| O7 | Deliver the offline workbench | Three-panel report on `.set`, `.bdf`, `.edf`, and `.csv` inputs on consumer hardware |
| O8 | External generalisation arm | The abstention/calibration mechanism transfers to a second, public, same-machine cohort |

## 3. Novelty and Contributions

> **Disclosure.** Novelty here is claimed relative to the reference baseline and to the practices the
> project critiques. Whether each contribution is novel in the broader field is established only after
> the literature gap work in `04_Research_Motivation_and_Gap.md` is completed. No contribution is
> asserted as literature-proven novel.

### 3.1 Conceptual Contributions

- **C1. Recasting screening as a calibration-and-abstention problem.** Restating the objective from
  maximising discrimination to maximising clinically useful decision behaviour at fixed discrimination.
- **C2. Treating the artifact burden as a measured quantity.** Elevating the artifact confound from a
  preprocessing nuisance to a first-class, reported axis of the system.
- **C3. An unlosable outcome structure.** Defining the research so that both a positive and a negative
  artifact-control result constitute valid, publishable contributions.

### 3.2 Architectural Contributions

- **C4. Dual-path trait/state decomposition.** Retaining gain-invariant aperiodic structure alongside
  aligned dynamic connectivity to address the information-loss cost of unsupervised alignment.
- **C5. Five-lobe spatial graph encoder.** Replacing the flattened connectivity vector with a
  topology-preserving graph over the 10–20 montage, with a learnable sparse edge gate.

### 3.3 Algorithmic Contributions

- **C6. Global joint Löwdin orthogonalised envelope connectivity.** A construction that yields a true
  Gram matrix and is therefore positive semi-definite by construction, contrasted with
  pairwise-symmetrised orthogonalised envelope correlation, which is shown to violate positive
  semi-definiteness on band-limited segments.
- **C7. Runtime spectral-integrity guard.** Eigenvalue clipping at a fixed floor with the magnitude of
  every repair logged and surfaced to the user as a data-quality signal.

### 3.4 Methodological Contributions

- **C8. Artifact-paired evaluation.** Mandating artifact-only and artifact-controlled reference models
  on identical folds for every reported neural result.
- **C9. Participant-level, null-informed reporting.** Repeated subject-disjoint partitioning with a
  permutation null distribution and a reproducibility hash on every output.

### 3.5 Implementation Contributions

- **C10. Dependency-light, offline geometry stack.** A NumPy-native implementation of Löwdin
  orthogonalisation, the Fréchet mean, and tangent-space projection that runs on consumer hardware
  without a clinical-analysis framework.
- **C11. Canonical multi-format ingestion.** Automatic remapping of legacy and 128-channel net naming
  conventions to a canonical 19-channel montage across `.set`, `.bdf`, `.edf`, `.csv`, and `.fif`
  inputs.

## 4. What Is NOT Claimed

- Not a claim that ADHD is decodable from 19-channel resting EEG (the project may conclude the
  opposite).
- Not a claim of clinical validity or regulatory approval.
- Not a claim of superiority over foundation models in general — only a comparison against a stated
  baseline under a stated protocol.
- Not a claim that the specificity improvement is attributable to any single architectural element
  until the ablation ladder isolates it.
