# 04 — Research Motivation and Gap

## 1. Research Motivation

### 1.1 Motivation on the Clinical Axis

Specialist assessment for paediatric neurodevelopmental conditions is scarce and expensive. A
quantitative screening adjunct that stratifies referral urgency — correctly identifying children who
need specialist evaluation while withholding judgement where evidence is insufficient — would improve
the efficiency of the referral pathway. The relevant quantity for such an instrument is not the
concordance of its ranking but the false-positive behaviour at screening prevalence, because false
positives generate unnecessary referrals and distress.

### 1.2 Motivation on the Methodological Axis

A significant portion of reported EEG-based diagnostic performance is an artefact of evaluation
protocol. If the field continues to report window-level performance, it will continue to overstate the
maturity of the technology, and deployment attempts will fail against expectations. The methodological
contribution — showing how to evaluate and how much reported performance survives honest evaluation —
is therefore of broader value than any single classifier.

### 1.3 Motivation on the Confound-Control Axis

The field lacks a routine quantification of the artifact confound. No published study on the benchmark
cohort used here reports what an artifact-only model can achieve on the same labels, or what neural
performance remains after artifact control. Without these controls, no reported discrimination can be
attributed to neurobiology with confidence. Supplying these controls is a prerequisite for any
interpretable result.

## 2. Research Gap

> **Important framing note.** The literature-gap claims below are stated as the premises the project
> operates on. Some are supported by the specific publications referenced in the project's working
> corpus; others are **preliminary assumptions that require verification against the broader academic
> literature** before they are asserted in a paper. Each claim below is labelled accordingly.

### 2.1 Gaps Established by the Project's Working Corpus

**G1 — Subject-disjoint performance frontier.**

*Claim.* Under subject-disjoint evaluation, reported ADHD-EEG discrimination on the 121-child cohort
clusters in the range 0.74–0.79 AUROC across both domain-specific models and pretrained foundation
models.

*Status.* **Established within the working corpus** (the reference baseline and a foundation-model
benchmark both report values in this range under subject-disjoint protocols). **Preliminary in the
broader literature** — a dedicated literature review is required before this is asserted as a
field-wide fact in the paper.

*Function.* Establishes that the ranking criterion is nearly saturated on this cohort and that further
discrimination gains are not the productive direction.

*Reconciliation note.* Provisional development measurements on this cohort, using a tangent-space plus
connectivity feature set, exceed this range (see `15` §12). Those values are **not** evidence against the
frontier claim: they are produced by a feature set that is itself under artifact-control review, and
artifact-proxy variables alone reach a comparable range on the same labels. Until the artifact-controlled
experiment is complete, no measured value may be used either to support or to refute G1. The frontier
statement therefore refers to the **published corpus**, not to any single in-house measurement.

**G2 — Specificity at the operating point is under-reported.**

*Claim.* The reference baseline reports 44.44% specificity and 13.79% PPV at 10% prevalence, and no
work in the corpus attempts to move these quantities directly.

*Status.* **Established** for the reference baseline; **preliminary** that "no work attempts this" as a
field-wide claim.

*Function.* Identifies the false-alarm rate as an open, under-addressed objective.

**G3 — Artifact-only performance is not routinely reported.**

*Claim.* No study in the corpus reports the achievable discrimination of an artifact-proxy model on the
same labels, or neural performance after artifact control.

*Status.* **Preliminary.** Requires a targeted literature search to confirm absence.

*Function.* Identifies the missing control experiment as a gap.

### 2.2 Preliminary Assumptions Requiring Literature Validation

**A1 — Alignment removes trait-level diagnostic structure.** The hypothesis that unsupervised
covariance alignment deletes static, between-subject diagnostic signal as well as nuisance variance.

**A2 — Aperiodic exponent is diagnostically informative for attention.** The hypothesis that the
gain-invariant 1/f exponent carries information relevant to the attention construct.

**A3 — Bifactor psychopathology dimensions are EEG-decoding-specific.** The hypothesis that attention
factors decode from EEG while externalizing/internalizing factors do not — central to the
transdiagnostic external-cohort plan.

**A4 — Neural discrimination survives artifact control.** The hypothesis that after regressing
recording-quality proxies out of the feature space, the remaining neural signal still discriminates.

These are treated as **hypotheses with kill conditions** (Section 06, 15, 16), not as established facts.

## 3. What Existing Approaches Do

| Approach class | What it does | Limitation relevant here |
|---|---|---|
| Window-level deep classifiers | Segment recording, classify segments, report segment accuracy | Inflated by near-duplicate train/test segments |
| Dynamic functional-connectivity models | Compute band-limited correlation and classify the connectivity vector | Zero-lag correlation dominated by volume conduction; flattening discards topology |
| EEG foundation models | Pretrain on large corpora, linear-probe on tasks | Costly; subject-disjoint performance not clearly above specialist models on this cohort |
| Cross-dataset pooled models | Train on multiple sites/conditions jointly | Learn acquisition hardware rather than neurobiology |

## 4. What the Proposed Project Adds

1. **An abstention-first operating model** that treats "I do not know" as a valid output with a
   measurable risk–coverage trade-off, rather than a failure mode.
2. **A dual-path trait/state architecture** that explicitly separates gain-invariant aperiodic
   structure from aligned dynamic connectivity, addressing the information-loss cost of alignment.
3. **A positive-definiteness-guaranteed connectivity construction** (global joint Löwdin) with a
   runtime spectral-integrity audit reported to the user.
4. **An evaluation protocol that quantifies the artifact confound** by reporting artifact-only and
   artifact-controlled performance on identical folds.

## 5. Gap-Supporting Work Needed

Before submission, the following must be completed to convert preliminary assumptions into
literature-validated claims:

- A systematic review of subject-disjoint ADHD-EEG results to support G1 and G2.
- A search confirming G3 (absence of routine artifact-only controls).
- A search on the diagnostic relevance of aperiodic spectral exponents in developmental populations
  (A2).
- A search on the EEG-decodability of bifactor psychopathology dimensions (A3).

This work is catalogued in `21_IEEE_Paper_Preparation_Notes.md`.
