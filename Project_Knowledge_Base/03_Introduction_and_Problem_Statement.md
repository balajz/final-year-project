# 03 — Introduction and Problem Statement

## 1. Domain Context

Electroencephalography measures scalp potential differences at millisecond resolution using an array
of electrodes placed according to the international 10–20 system. It is non-invasive, inexpensive
relative to neuroimaging, and tolerable for paediatric populations, which makes it an attractive
substrate for developmental screening instruments.

Paediatric neurodevelopmental assessment — in particular for ADHD — is a natural target for
EEG-based decision support. Diagnosis currently relies on structured clinical interview and informant
rating scales, both of which are subjective and resource-intensive. A quantitative adjunct that
stratifies referral urgency would have practical value in settings where specialist assessment is
scarce.

The technical substrate is a multichannel time series. For a subject *s* with *C* channels sampled at
rate *f_s* over duration *T*, the recording is a matrix **X** ∈ ℝ^{C×N} with N = f_s·T samples. The
canonical analysis object is not the raw time series but a derived representation: a symmetric positive
definite covariance or correlation matrix **C** ∈ 𝒮_{++}^{C} capturing inter-electrode structure, and a
set of spectral descriptors capturing oscillatory and aperiodic content.

## 2. Technical Background Required

**Spectral decomposition.** EEG power spectra are well described as the superposition of a small number
of oscillatory peaks upon a broadband 1/f-like background. Mathematically, the model is
L(f) + Σₙ Gₙ(f), where L(f) = b − log(f^χ) is the aperiodic component in log-power space and Gₙ are
Gaussian-shaped periodic components. The exponent χ is a subject-level property of neural
organisation and, importantly, is invariant to a multiplicative gain applied to the signal — a
property exploited by the design described in this repository.

**Connectivity and volume conduction.** Inter-electrode correlation at zero lag is strongly influenced
by volume conduction: a single deep source projects to many electrodes simultaneously, producing
spurious instantaneous correlation. Orthogonalisation of the channel space before envelope extraction
suppresses this instantaneous leakage, allowing correlation to reflect genuinely lagged envelope
interaction.

**Covariance geometry.** The set of symmetric positive definite matrices forms a Riemannian manifold
under the affine-invariant metric rather than a vector space. Arithmetic averaging of covariance
matrices is not geometrically meaningful; the Fréchet (geometric) mean and the associated tangent-space
projection are required for linear models to operate on this object.

**Distribution shift across subjects.** Covariance structure varies substantially between individuals
for reasons unrelated to pathology: skull thickness, scalp impedance, electrode placement error, and
cortical folding. This between-subject offset dominates within-subject variation and degrades
cross-subject transfer.

## 3. Problem Statement

### 3.1 Primary Problem

Paediatric EEG screening models are evaluated and reported in a manner that overstates their
discriminative capacity and understates their false-alarm behaviour, so that reported performance does
not predict behaviour at a clinically relevant operating point.

### 3.2 Component Failures

**P-1 — Evaluation-protocol inflation.**

*Mechanism.* Datasets are partitioned at the level of short segments rather than participants.
Adjacent segments from the same recording share noise, artifact, and individual-specific spectral
structure. When such segments straddle the partition boundary, the test set contains near-duplicates of
training data.

*Consequence.* Reported accuracy reaches 93%–99%, while subject-disjoint evaluation of the same
architecture families yields approximately 0.74–0.79 AUROC. The gap is attributable to protocol, not
to modelling.

*Required remedy.* Participant-level partitioning with aggregation of predictions to the participant
level before any metric is computed.

**P-2 — The false-alarm bottleneck.**

*Mechanism.* Screening prevalence is low (5%–10%). At low prevalence, positive predictive value is
dominated by specificity. The relationship is

    PPV = (Se·π) / (Se·π + (1−Sp)(1−π))

where Se is sensitivity, Sp is specificity, and π is prevalence.

*Quantification.* At Se = 0.80, Sp = 0.4444, π = 0.10, the expression yields PPV ≈ 0.1379. That is,
86.2% of positive findings are false. At Sp = 0.90 the same sensitivity yields PPV ≈ 0.4706.

*Consequence.* A one-point AUROC improvement at constant specificity produces essentially no clinical
change. A ten-point specificity improvement produces a large one. The optimization target is
misaligned with the clinical objective.

*Required remedy.* Report and optimize specificity at fixed sensitivity and predictive value at stated
prevalence, not AUROC alone.

**P-3 — The artifact confound.**

*Mechanism.* Resting EEG in children is contaminated by ocular, muscular, and movement artifacts.
These artifacts are not randomly distributed with respect to clinical status: children who move more
produce longer, noisier recordings, and such children are disproportionately represented in the
clinical group. Recording duration and signal quality therefore carry diagnostic information
independently of neurobiology.

*Consequence.* A model can attain respectable apparent performance by learning recording-quality
structure. Reported "neural" discrimination may be partly artifact detection.

*Required remedy.* Measure artifact-only performance on identical folds, and measure
artifact-controlled neural performance, and report all three quantities together.

### 3.3 Problem Statement, Formal

Given a labelled cohort 𝒟 = {(**X**ᵢ, yᵢ, sᵢ)} where **X**ᵢ is a multichannel recording, yᵢ ∈ {0,1} the
clinical label, and sᵢ the participant index, the objective is to construct a predictor
f: **X** → (p̂, τ) mapping a recording to a calibrated probability p̂ and an evidential state
τ ∈ {accept, abstain}, such that:

1. Partitioning respects participant identity: no sᵢ appears in more than one fold.
2. Metrics are computed on participant-level aggregates, not segment-level predictions.
3. Specificity at Se = 0.80 and PPV at π ∈ {0.05, 0.10} are maximized subject to AUROC change being
   bounded, i.e. the improvement is attributable to calibration and abstention, not to a change in
   underlying discrimination.
4. The contribution of artifact structure is quantified: performance of an artifact-only model and of
   an artifact-controlled neural model on identical folds is reported alongside the primary result.

## 4. Precise Problem Scope

**In scope.**

- Resting-state, 19-channel, 128 Hz paediatric EEG.
- Binary attention-related screening index and an abstention state.
- Single-cohort evaluation with a planned external generalisation arm.
- Subject-disjoint protocol with participant-level aggregation.

**Out of scope.**

- Clinical diagnosis or differential diagnosis.
- Multi-site pooled training.
- Other modalities (fMRI, structural MRI, genomic, behavioural) as model inputs.
- Generalisation to adult populations or to non-resting paradigms without revalidation.

## 5. Practical Implications

If left unaddressed, the three failures above produce a specific practical hazard: an instrument
reporting high accuracy in the literature but generating six false alarms per true positive in
deployment. In a screening context this produces unnecessary referrals, caregiver anxiety, and
misallocation of scarce specialist capacity. The problem is therefore not purely methodological; it
determines whether such instruments are usable at all.
