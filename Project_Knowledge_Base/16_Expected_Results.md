# 16 — Expected Results

> This section states anticipated outcomes and clearly separates **expectations** (not yet demonstrated)
> from the **provisional measurements** recorded in `15_Experimental_Design_and_Evaluation.md` §12.

## 1. Expected Outcome Structure

The project is designed so that the outcome is informative regardless of the sign of its central result.
Two headline outcomes are anticipated, distinguished by the H3 result (does neural signal survive
artifact control?).

### Outcome A — Neural signal survives artifact control

**Predicted.** Artifact-controlled neural AUROC remains close to the uncontrolled value while
artifact-only AUROC is substantially lower. Selective abstention raises specificity and PPV at fixed
sensitivity.

**Reported contribution.** A calibrated screening workbench that improves the false-alarm behaviour of
the reference baseline at unchanged discrimination, with a quantified account of the neural origin of
the signal.

### Outcome B — Neural signal does not survive artifact control

**Predicted.** Artifact-controlled neural AUROC collapses toward chance while artifact-only AUROC is
appreciable.

**Reported contribution.** An empirical demonstration that the reported frontier on this cohort is
largely recording-quality prediction. The workbench then becomes a measurement instrument for the
artifact burden rather than a classifier, and the abstention gate is its principal value.

## 2. Specific Expectations by Metric

| Metric | Expected behaviour | Constraint |
|---|---|---|
| Specificity at Se = 0.80 | Rise above the baseline's 44.44% as the abstention gate and feature set are added | Must rise without lowering sensitivity below the fixed operating point |
| PPV at 10% | Rise above the baseline's 13.79% | Consistent with the specificity change |
| AUROC | Bounded change (≤ Z relative to baseline); not expected to be the contribution | Reported, not headlined |
| Brier / ECE | Improve with the calibration layer | Monitored on training-fold calibration |
| Risk–coverage | Monotonically improving specificity as coverage falls | Required for H4 |
| SPD integrity | Corrections rare and small under joint Löwdin | Required for H5 |

## 3. Expected Magnitudes (Qualitative)

- **Specificity.** The reference baseline achieves 44.44% at 80% sensitivity. A combined improvement
  from a better feature set and selective abstention is expected to raise this materially; the exact
  value is a measured outcome and is deliberately left unquantified here.
- **AUROC.** Expected to move only slightly; any large change must be explained as a feature-set effect
  or a protocol effect, never attributed to the abstention gate alone.

## 4. Anticipated Benefits

1. **Operational.** Fewer false referrals at a fixed referral-sensitivity target.
2. **Methodological.** A reusable, artifact-paired evaluation protocol for EEG screening.
3. **Interpretability.** Per-window quality timelines and a stability-metric-carrying graph panel.
4. **Reproducibility.** Every result carries a ledger; every matrix carries integrity statistics.

## 5. Distinguishing Expectation from Demonstration

- **Demonstrated (provisional).** Joint Löwdin connectivity is positive semi-definite; alignment arms
  reduce ranking performance relative to the unaligned arm; an artifact-only model carries appreciable
  discriminative information; unaligned discrimination exceeds the permutation null at p = 0.005 on the
  provisional feature set.
- **Expected, not yet demonstrated.** Dual-path recovery of alignment loss; abstention raising
  specificity and PPV; the spatio-temporal encoder outperforming the flattened baseline; transfer to the
  external cohort; specificity improvement attributable to specific rungs.

Nothing in this section is a claim of a completed experimental conclusion. Values that have been
measured are labelled in the evaluation document; all others are hypotheses awaiting the fixed-configuration
run.
