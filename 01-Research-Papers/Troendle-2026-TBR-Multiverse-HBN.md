---
tags:
  - research-paper
  - adhd
  - eeg
  - multiverse
  - biomarker
  - aperiodic
  - methodology
---

# Tröndle et al. (2026) — Theta/Beta Ratio Under a Multiverse Analysis (HBN + Validation)

- **Citation:** *Theta beta ratio in attention deficit hyperactivity disorder using a multiverse analysis.* 2026. **Author list not supplied in the excerpt** — the OSF/Shiny handle `dstrze`, the Zurich/Grisons validation cohort (Müller, Münger), and self-citation of Tröndle & Langer (2026) indicate the Tröndle / University of Zurich psychiatric-neurometrics group. **Verify the author list and venue before citing.**
- **Code:** https://osf.io/u5yxv — full analysis code, extracted EEG features, and demographic model data. Live ShinyApps for all three samples.
- **Datasets:**
  - **HBN** (Child Mind Institute, public, Release 11) — **N = 1,499 → 1,122 final** (228 HC / 429 ADHD-combined / 465 ADHD-inattentive). 128ch EGI, 250 Hz, Cz reference, <40 kΩ, 5 min EO–EC.
  - **Validation** (Brain and Trauma Foundation Grisons, Switzerland) — **N = 381 → 237 final** (107 HC / 46 combined / 84 inattentive). 19ch NeuroAmp, 500→250 Hz, linked earlobes, **<5 kΩ**, 8 min EO/EC.
  - Both public-access; HBN is downloadable, validation available on request.

---

## 1. Core Problem
The theta/beta ratio (TBR) is the most commercially entrenched EEG "biomarker" in child psychiatry — it underpins an **FDA-cleared adjunctive ADHD assessment device** on the strength of Monastra et al.'s 86% sensitivity / 98% specificity. Meta-analyses since then show shrinking effect sizes. The field's explanation has been "methodological heterogeneity," asserted but never quantified.

This paper quantifies it. **576 analytical specifications** (2 resting condition × 2 reference × 2 band definition × 3 aperiodic handling × 6 ROI × 2 comorbidity × 2 medication) × 8 regression models, per group contrast, in two independent samples. Plus a 144-universe replication, a 1,000-iteration bootstrap for group-size imbalance, and a dimensional (SWAN) version.

## 2. Methods (the parts that matter)
- **Preprocessing:** Automagic + PREP bad-channel detection + 0.5 Hz high-pass + ZapLine line noise + ICA on 2 Hz-high-passed copy → IClabel (p > 0.8 = artifact) → back-project. Objective quality tiers (good/ok/bad) with published thresholds. **This is the most defensible preprocessing chain in our vault, and it is fully specified.**
- **Segments:** 2 s, first/last segment of each block discarded, 90 µV amplitude rejection, participant excluded if >60% trials rejected.
- **Spectral:** FFT 1–40 Hz, Hanning window. Three feature types per epoch set: relative (1/f-uncorrected) power, **SpecParam aperiodic-adjusted power** (R² ≥ 0.85 filter), and **the isolated aperiodic component**.
- **IAF:** peak in 7–14 Hz on aperiodic-adjusted EC posterior spectra.
- **Bands:** canonical (θ 4–8, β 13–30) vs IAF-relative (θ = IAF−6…IAF−4, β = IAF+2…30).
- **Model:** `TBR ~ Group * Age * Gender * IAF`, all terms reported, two contrasts (HC vs inattentive, HC vs combined).
- **Inference:** count of universes with p < 0.05, one-sided binomial test vs a 5% chance baseline, specification curves, possibility-space plots, bootstrap, dimensional replication.

## 3. Results
**The headline null is real and strong.**
- HC vs ADHD-inattentive main effect: **0 / 576** universes significant (HBN); 2 positive / 11 negative of 144 (validation).
- HC vs ADHD-combined main effect: 11 / 576 positive (1.91%), 0 negative (HBN); 1 / 2 of 144 (validation).
- The **group-only** universes (no covariates) are also null — so this is not a covariate-adjustment artifact.
- Cohen's *d* is **small in every subspace**, including the subspaces where interactions are frequent.

**What *is* significant is conditional and mechanical.**
- The action is in `Group × IAF`, `Group × Age × IAF`, `Group × Gender × IAF`.
- These appear almost exclusively under **IAF-relative bands + uncorrected or aperiodic-only power**; they vanish under **canonical bands + aperiodic-adjusted power**.
- The mechanism is demonstrated directly: `r(IAF, power)` is **−0.17** with canonical bands, **−0.70** with IAF-relative bands, and **+0.11** for aperiodic-adjusted power. Defining a band relative to IAF mechanically injects IAF into the outcome.
- Post-hoc subsets: 46/48 universes significant for `IN × IAF` (IAF-relative + aperiodic signal + comorbidities included).

**Aperture note:** groups do **not** differ in IAF overall (HC vs combined p = 0.122; HC vs inattentive p = 0.275). The only IAF difference is inattentive > combined (p = 0.001). So IAF is a *moderator*, not a group marker.

**Dimensional replication:** SWAN total scores give the same pattern (0% positive main effect, 23.26% negative `SWAN × IAF`).

## 4. Scientific Critique & Our Analysis
*(Our inference, not the paper's claims. Items 1–3 are credit; 4–12 are problems.)*

1. **Credit: the null is stronger than the authors claim.** With 465 vs 228 subjects, a single two-sample test has ~96% power to detect *d* = 0.3 and ~70% for *d* = 0.2. Zero significant universes across 576 specifications therefore bounds the true standardised main effect at roughly **|d| ≲ 0.2–0.25** for the full-sample universes (less power in the small comorbid/medication subgroups). Strictly this is a power-based bound, not a formal equivalence test — a TOST or Bayes factor per universe was not run — but the direction is unambiguous: **the abstract's "no evidence for robust main effects" undersells the result.** "No moderate effect can exist in this cohort" is the correct statement, and it is the strongest null in the ADHD-EEG literature.
2. **Credit: the IAF-relative band artefact is demonstrated, not asserted.** The r = −0.17 → −0.70 shift is the cleanest mechanical demonstration in the ADHD EEG literature that a "band ratio" can be an IAF measurement in disguise. This generalises far beyond TBR.
3. **Credit: the multiverse actually varies the things that matter** (aperiodic handling, IAF policy, reference, ROI) rather than perfuming a single pipeline. And the group-size bootstrap, dimensional replication, and public code are genuinely above field standard. **This is the first paper in the vault whose methods we would defend in review.**
4. **The post-hoc "possibility space" is circular.** The 46/48 and 37/48 numbers come from *filtering the multiverse to the subset with the most significant results* and then reporting the proportion within that subset. That is a garden of forking paths applied to the analysis of the multiverse. The descriptive value is real (it identifies which choices matter); the evidential value is nil, and comparing those proportions to a 5% binomial threshold is doubly circular.
5. **The binomial test treats correlated universes as independent.** All 576 universes reuse the same subjects; specifications are nested and highly correlated. Positive correlation widens the true sampling distribution of "number significant," so the binomial test is anti-conservative precisely where the paper claims robustness. **The correct control — which the paper omits — is a label permutation pushed through the entire multiverse**, giving the null distribution of *proportion significant* while preserving correlation structure. (This also fixes item 4.) That control is cheap and it is the single methodological upgrade we should adopt ourselves.
6. **The summary statistic is a p-value count, not an effect size.** Magnitude, sign stability, and CI width are discarded. Simonsohn's joint-inference bootstrap (which they cite but do not run) would give a single multiverse-adjusted p-value. As written, "significant in 46/48 universes" and "|d| ≈ 0.1 in 46/48 universes" are indistinguishable in the reported tables — and their own effect-size figure shows the latter.
7. **No discrimination test — and the paper's central clinical claim is about discrimination.** The FDA-adjunct claim it rebuts is a claim about **sensitivity and specificity** (Monastra's 86/98). Every result here is a *regression coefficient*, i.e. a group-mean difference. A null mean difference and a useful classifier are not mutually exclusive in general, and the paper never computes AUC, balanced accuracy, or a subject-level operating point. The decisive figure — **a specification curve of AUC for TBR-as-classifier under subject-disjoint folds** — is missing, and it is the figure the clinical claim actually requires. *This is the gap we should fill; see §6.*
8. **"Aperiodic-adjusted" is not a neutral ground truth.** The paper treats aperiodic-adjusted power as the clean specification and reads the vanishing effect there as evidence of no real signal. But SpecParam's own aperiodic fit is artifact-sensitive — heart, eye and muscle activity steepen 1/f — which the authors cite and then do not control. The correct claim is conditional: *given aperiodic correction, no periodic TBR difference.* Whether that equals "no ADHD effect" depends entirely on whether the aperiodic difference is neural (E/I balance) or artifactual, which the design cannot decide.
9. **Their most-replicated effects live in exactly the artifact-suspect channel.** Aperiodic slope, aperiodic-only power, uncorrected power, and IAF-relative bands are all maximally exposed to broad-band contamination. The paper notes that children with ADHD move more (Dziemian et al., 2022) and that this steepens 1/f — then analyses slope without measuring movement. This is the same failure mode as [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]: the confound is acknowledged in prose and never operationalised. → [[Class-Correlated-Artifact-Control]]
10. **IAF-relative bands are not bands.** For a child with IAF = 8 Hz, "theta" = 2–4 Hz, i.e. delta. The specification therefore compares *different physical frequencies in different children*, and because IAF rises with age, it is also age-coupled. Any `Group × IAF` interaction computed this way is partly a statement about spectral geometry, not about a fixed physiological oscillation.
11. **Differential attrition is large and unreported by group.** 197 HBN subjects (12.6%) were dropped for >60% epochs above 90 µV; 45 for poor quality; 69 for SpecParam R²; and the entire hyperactive/impulsive-only group (n = 85) was excluded as "insufficient sample size." These are the **most movement-prone children**, disproportionately ADHD. The group distribution of every exclusion is absent. This is the **third independent instance** of differential attrition by class in our vault (Kim: 38% ADHD vs 0% Tic; the 121-child cohort's unequal per-subject epoch counts). It biases the artifact test in the direction of "no artifact effect." → new commitment 16.
12. **"Two independent samples" is generous.** Different hardware and impedance (128ch/40 kΩ vs 19ch/5 kΩ) is a genuine strength. But both are European, both resting-state, both from the same research ecosystem, and the validation sample's 139 methylphenidate users have **no recorded washout duration** — the same provenance gap as our 121-child cohort. Also: HBN's inattentive group is *oldest* (10.99) while the validation sample's HC group is *oldest* (14.49), so the age × IAF interaction replicates across opposite age orderings — arguably reassuring, but it also means the "same" interaction may not have the same cause.
13. **Minor:** theta/beta is a ratio of two noisy power estimates and is heavy-tailed; a log-ratio would be better behaved. They standardise the outcome but never transform it. Also unstated whether Age/IAF are mean-centred, which determines whether the reported "main effects" are at the mean or at 0 years / 0 Hz — resolved in practice by the group-only universes but worth checking in the code.

## 5. What Is Genuinely Valuable
- **A defensible null.** This is the paper that should end "TBR as a standalone ADHD biomarker" in our project's reasoning, and it does so with two samples, 576 specifications, and public code. It also demonstrates that **a rigorous null is publishable in a strong venue** — strategically important, because it de-risks the audit framing I have been recommending.
- **A public, specified, reusable pipeline** for HBN (Automagic → PREP → ZapLine → IClabel → SpecParam) with objective quality tiers. We had no agreed preprocessing standard; we now do, and it comes with code.
- **HBN as a viable primary cohort.** The vault has been treating HBN as an aspiration ([[Decision-Log]] unresolved question). This paper proves it works at N = 1,122 with ADHD subtyping and SWAN severity scores.
- **The aperiodic/IAF confound, quantified.** This is a new axis of subject-level nuisance that our leakage and alignment notes did not contain.
- **A template for how to report a negative result** credibly: specification curves, possibility spaces, bootstrap, dimensional replication, public code.

## 6. What It Changes For Us
1. **TBR is now closed as a feature.** Not "weak" — closed. Do not build on theta/beta.
2. **Baibulova's theta dominance needs re-reading.** [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] reports theta AUC 0.733 vs beta 0.567 using canonical bands, with no SpecParam correction. Under this paper's mechanism, that theta "connectivity" signal is a plausible candidate for aperiodic-slope contamination. **This is a concrete, high-value re-analysis of an existing vault result.**
3. **The PSD leakage gap gains a new mechanism.** [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]] loses 21–24 pp because band power encodes stable subject traits. This paper supplies the missing candidate: **the aperiodic exponent and offset are themselves stable, highly individual traits** that shift all band powers coherently. If so, the "subject fingerprint" in a PSD pipeline is largely a 1/f fingerprint — which is a sharp, cheap, testable claim (subject-identification accuracy from `(exponent, offset)` alone).
4. **Our project spine changes shape.** Not "find the biomarker." Not "beat the architecture." The publishable object is **measurement science for ADHD EEG**: a specification-curve audit of *decoding* performance, not of regression coefficients. → [[Decoding-Multiverse-and-Aperiodic-Identity]]

## 7. Connections
- Papers: [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]
- Concepts: [[Multiverse-and-Specification-Curve-Analysis]], [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Opportunities: [[Decoding-Multiverse-and-Aperiodic-Identity]], [[Class-Correlated-Artifact-Control]], [[Unsupervised-Alignment-Leverage]]
- Session log: [[2026-11-15-TBR-Multiverse-Analysis]]
