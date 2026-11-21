# 02 — Abstract and Keywords

## 1. Abstract

Paediatric electroencephalography (EEG) studies of attention-deficit/hyperactivity disorder (ADHD)
frequently report classification accuracies between 93% and 99%. These figures are obtained under
window-level data partitioning, in which temporally adjacent segments from the same participant are
distributed across training and test sets. Under subject-disjoint evaluation the same architecture
families do not materially exceed approximately 0.79 AUROC on public 19-channel benchmark cohorts, and
the best-performing honest implementations still exhibit high false-alarm rates: 44.44% specificity at
80% sensitivity, corresponding to a positive predictive value of 13.79% at a screening prevalence of
10%.

This project addresses the false-alarm rate directly rather than the ranking criterion. The proposed
system holds discriminative capacity approximately fixed and introduces three mechanisms. First,
**artifact-aware selective abstention** permits the model to decline prediction on recordings whose
signal quality cannot support one, and reports the resulting risk–coverage trade-off explicitly.
Second, a **dual-path trait/state decomposition** separates gain-invariant aperiodic spectral
structure — characterised by the SpecParam exponent of the 1/f component — from per-subject aligned
dynamic connectivity, so that unsupervised covariance alignment does not remove subject-level
diagnostic structure. Third, a **topology-preserving spatio-temporal encoder** operates over a
five-lobe, nineteen-node cortical graph, replacing the flattened connectivity representation of the
reference baseline.

Connectivity estimation uses global joint Löwdin orthogonalisation prior to envelope correlation. This
constructs a genuine Gram matrix of mutually orthogonalised channel vectors and is therefore positive
semi-definite by construction, in contrast to pairwise-symmetrised orthogonalised envelope correlation,
which is shown to violate positive semi-definiteness on band-limited segments. A runtime spectral guard
audits every matrix and records the magnitude of any repair as a data-quality signal, reported to the
user rather than applied silently.

Evaluation uses nested group k-fold cross-validation and leave-one-subject-out partitioning with
participant-level aggregation, permutation null distributions, and — critically — artifact-only and
artifact-controlled reference models fitted on identical folds. The primary reported quantities are
specificity at fixed 80% sensitivity and positive predictive value at 5% and 10% prevalence; AUROC is
reported as a secondary measure for comparability.

The expected contribution is a demonstrated reduction in the false-alarm rate at unchanged
discrimination, together with a quantified account of how much of the reported neural performance is
attributable to recording-quality structure rather than neurobiology. Both outcomes are informative:
if neural signal survives artifact control, the work delivers better calibration at equal
discrimination; if it does not, the work establishes that the field's reported frontier is partly an
artifact-detection ceiling.

**Keywords:** electroencephalography; ADHD; selective prediction; calibration; Riemannian geometry;
graph attention networks; artifact control; aperiodic spectral analysis.

## 2. Keywords

1. Electroencephalography (EEG)
2. Attention-deficit/hyperactivity disorder (ADHD)
3. Selective prediction and abstention
4. Probability calibration
5. Riemannian manifold learning
6. Graph attention networks
7. Artifact and confound control
8. Aperiodic spectral analysis (1/f)

## 3. IEEE Index Terms (alternative formulation)

- Biomedical signal processing
- Brain modeling
- Calibration
- Electroencephalography
- Graph neural networks
- Medical decision support systems
- Uncertainty quantification
- Reliability engineering

## 4. Abstract Construction Notes

The abstract states no experimental outcomes. Every numeric value present is either a
literature-attributed baseline figure or a prevalence assumption. The final version of the paper
abstract must additionally include: the measured specificity and predictive-value values replacing the
44.44% and 13.79% baseline, the measured AUROC delta, and the confidence intervals obtained under
repeated subject-disjoint partitioning.
