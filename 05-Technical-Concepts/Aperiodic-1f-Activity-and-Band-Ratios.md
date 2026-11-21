---
tags:
  - technical-concept
  - eeg
  - signal-processing
  - aperiodic
  - spectral
---

# Aperiodic 1/f Activity & Band Ratios (why theta/beta is not a theta measurement)

Derived from [[Troendle-2026-TBR-Multiverse-HBN]]; affects the reading of [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] and [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]].

## 1. The Decomposition
An EEG power spectrum is conventionally written

$$P(f) = \underbrace{\frac{A}{f^{\chi}}}_{\text{aperiodic}} \;+\; \underbrace{\sum_k P_k \exp\!\left(-\frac{(f-\mu_k)^2}{2\sigma_k^2}\right)}_{\text{periodic (oscillatory peaks)}}$$

- **χ (exponent / slope)** — typically 0.8–1.3 in adults, steeper in children; putatively tracks excitation/inhibition balance.
- **A (offset)** — broadband scale; tracks overall signal amplitude, impedance, and gain.
- **Peaks** — genuine oscillations (alpha, theta, beta) sitting *on top of* the 1/f background.

**A band "power" is almost always a mixture of both.** Integrating 4–8 Hz captures both the oscillatory theta peak *and* the 1/f background at those frequencies. A ratio like θ/β therefore divides one mixture by another mixture.

## 2. Why Band Ratios Are Fragile
1. **The 1/f background dominates low frequencies.** Any change in slope χ alters theta power far more than beta power (because 4–8 Hz sits where $f^{-\chi}$ is steep). A 0.1 shift in exponent can mimic a 20% "theta increase" with no change in oscillation.
2. **The exponent is artefact-sensitive.** Eye movements, heartbeat, muscle (EMG) and sweating all have their own spectral shapes that flatten or steepen the fitted 1/f. Movement therefore *impersonates* a neural parameter. This is the class-correlated artefact problem in spectral clothing → [[Class-Correlated-Artifact-Control]].
3. **The exponent is developmentally dynamic.** χ and A both change with age, so any group differing in age composition differs in 1/f — with no neural difference required.
4. **Individual alpha frequency (IAF) moves the peaks.** If bands are fixed, a slow-IAF child's alpha leaks into "theta." If bands are defined *relative to IAF*, then (a) the band is a different physical frequency for every child, and (b) IAF is injected directly into the outcome. Troendle et al. show `r(IAF, power)` goes from −0.17 (canonical) to −0.70 (IAF-relative).
5. **Ratios have heavy tails.** θ/β is a ratio of two noisy non-negative estimates; small β denominators produce large outliers. Log-ratios are far better behaved.

## 3. The Three Specifications (and what each one actually tests)
| Specification | Removes | Tests |
|---|---|---|
| **Uncorrected (relative) power** | nothing | the *mixture* — what a conventional pipeline measures |
| **Aperiodic-adjusted power** | fitted 1/f | the *periodic* component only — but the removal is only as good as the fit, and the fit absorbs artefact |
| **Aperiodic component only** | the peaks | the *slope/offset* — i.e. the putative E/I or artefact parameter |

**The critical asymmetry:** removing the aperiodic component removes *both* the neural 1/f and the artefactual 1/f. So "the effect disappears after aperiodic correction" does **not** establish "there is no group difference" — only "there is no difference in the periodic component above the fitted background." If the background difference is neural, you have just deleted the signal; if it is artifactual, you have correctly deleted it. **The design cannot tell you which, so it must measure movement directly (EMG/accelerometer) rather than infer.**

## 4. The Fingerprint Hypothesis (our inference — testable)
The aperiodic exponent and offset are:
- stable within a person across sessions,
- highly variable across people,
- broadband (they shift *every* band power coherently).

That is the profile of an **identity feature**, which predicts a specific, checkable claim:

> The 21–24 pp subject-identity leak in PSD/SVM pipelines ([[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]) is carried largely by `(exponent, offset)`, not by oscillatory power.

**Cheap test:** train a classifier to predict *participant ID* from two features — `(χ, A)` — on the same cohort. If subject-identification accuracy is far above chance, the fingerprint is real; then re-run the ADHD classifier on aperiodic-adjusted features and see how much of the leakage gap closes. This single experiment links the leakage literature, the alignment literature, and this paper.

## 5. Practical Rules for Our Pipeline
1. Always report **both** uncorrected and SpecParam-adjusted results; never one alone.
2. Fit SpecParam over a wide range (1–40 Hz) and report fit quality (R²) and per-subject rejection counts **by group**.
3. Prefer **canonical bands** for physiological claims and IAF-relative bands only as a sensitivity analysis — never as the primary definition, and never without stating the physical frequency range it implies per child.
4. Use **log**-ratios, not ratios.
5. Report χ and A as **outcomes in their own right**, not just as nuisances — they may be the actual discriminative quantity, and that is a finding, not a failure.
6. Never interpret a band-power difference as "oscillatory" without an aperiodic-corrected replication.

## 6. Connections
- Papers: [[Troendle-2026-TBR-Multiverse-HBN]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]
- Concepts: [[Multiverse-and-Specification-Curve-Analysis]], [[Subject-Level-Evaluation-Hygiene]], [[Kernel-Matrix-Based-Transfer-Entropy]]
- Opportunities: [[Decoding-Multiverse-and-Aperiodic-Identity]], [[Class-Correlated-Artifact-Control]], [[Unsupervised-Alignment-Leverage]]
