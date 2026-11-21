# 19 — Future Research Directions

## 1. Signal and Geometry

- **Adaptive connectivity.** Replacing the fixed band partition with data-driven or data-driven band
  boundaries.
- **High-order topology.** Beyond pairwise connectivity to motif or simplex structure in the
  connectivity manifold.
- **Learning on the manifold directly.** Encoders that respect the Riemannian geometry rather than
  projecting to tangent space and applying Euclidean networks.
- **Robust spectral parameterisation.** Extending the aperiodic/periodic fit to higher-order or
  time-resolved (e.g. moving-window) forms.

## 2. Architecture

- **Uncertainty-aware heads.** Explicit predictive-uncertainty estimation as an input to the evidence
  gate.
- **Personalised operating points.** Fitting the coverage target to site-level prevalence rather than a
  fixed 5%/10%.
- **Multi-task decoding.** Attention and co-occurring dimensions jointly, with shared geometry.

## 3. Evaluation and Measurement

- **Cross-site replication.** Evaluating whether the abstention mechanism transfers across sites with
  different artifact statistics.
- **Longitudinal validity.** Whether the index is stable across repeated recordings of the same child.
- **Equivalence testing.** Formal tests that non-target dimensions are *not* decoded, with stated power.

## 4. Application

- **Other developmental populations.** Externalising and internalising constructs as primary targets.
- **Active-task screening.** CCD and other task-locked paradigms.
- **Scale.** Larger cohorts to tighten the confidence intervals that limit the current evaluation.

## 5. Product and Deployment

- **Caregiver-facing summaries** (aspirational; requires evaluation machinery).
- **Continuous calibration monitoring** as new recordings arrive.
- **Edge deployment** to lower-resource clinical settings.

## 6. Research Questions Opened by the Project

1. What fraction of the reported frontier on this cohort is recording quality rather than neurobiology?
2. Is the alignment/identity trade-off general, and does a gain-invariant trait path recover it
   reliably?
3. Does selective abstention transfer across cohorts, or is the gate's benefit cohort-specific?
4. Is the aperiodic exponent a stable, diagnostically informative trait marker in developmental EEG?

## 7. Prioritisation

Highest priority future work: the artifact-controlled experiment (the load-bearing H3), followed by the
dual-cohort risk–coverage transfer, followed by formal equivalence testing for the transdiagnostic arm.
These three complete the scientific claim; the remaining directions are extensions.
