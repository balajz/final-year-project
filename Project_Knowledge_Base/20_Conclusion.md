# 20 — Conclusion

This project addresses a specific and under-recognised failure mode in paediatric EEG screening:
reported discriminative performance is inflated by window-level evaluation protocols, while the quantity
that actually governs clinical usefulness — the false-alarm rate at screening prevalence — is neither
targeted nor reported. The reference implementation on the 121-child benchmark cohort achieves 44.44%
specificity at 80% sensitivity, yielding a positive predictive value of 13.79% at 10% prevalence. Under
subject-disjoint evaluation, no method in the working corpus materially exceeds approximately 0.79
AUROC on this cohort, indicating that further investment in raw discrimination is unlikely to be
productive.

The proposed system therefore holds discrimination approximately fixed and attacks the false-alarm rate
directly through three mechanisms. First, artifact-aware selective abstention permits the model to
decline prediction on recordings that cannot support one, and exposes the resulting risk–coverage
trade-off. Second, a dual-path trait/state decomposition retains gain-invariant aperiodic spectral
structure alongside per-subject aligned dynamic connectivity, so that unsupervised alignment does not
remove subject-level diagnostic structure. Third, a topology-preserving spatio-temporal graph encoder
operates over a five-lobe, nineteen-node cortical graph in place of a flattened connectivity vector.

Connectivity estimation uses global joint Löwdin orthogonalisation, which constructs a genuine Gram
matrix and is therefore positive semi-definite by construction — a property not shared by
pairwise-symmetrised orthogonalised envelope correlation. A runtime spectral guard audits every matrix
and surfaces the magnitude of any repair as a data-quality signal rather than applying it silently.

The evaluation protocol is designed to make the result interpretable and to bound the claim. It mandates
participant-level partitioning, participant-level aggregation, permutation null distributions, and —
critically — artifact-only and artifact-controlled reference models on identical folds. The primary
reported metrics are specificity at fixed sensitivity and predictive value at stated prevalence; AUROC
is secondary.

The project is structured so that its central uncertainty produces an informative result either way. If
neural discrimination survives artifact control, the work delivers improved calibration and false-alarm
behaviour at unchanged discrimination. If it does not, the work establishes that the reported frontier
on this cohort is partly an artifact-detection ceiling — a finding of comparable value to the field.

The contribution is therefore not a more accurate classifier but a more truthful one: a screening
workbench that reports what it knows, declines to report what it does not, and quantifies its own
evidentiary basis.
