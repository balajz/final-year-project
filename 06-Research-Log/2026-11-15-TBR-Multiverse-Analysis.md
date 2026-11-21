---
tags:
  - research-log
  - adhd
  - multiverse
  - biomarker
  - aperiodic
  - methodology
---

# Session Log: 2026-11-15 — TBR Multiverse Analysis (Seventh Paper)

## New Literature Added
- [[Troendle-2026-TBR-Multiverse-HBN]] — HBN (N = 1,122) + Zurich validation (N = 237); 576 analytical specifications; TBR, IAF, SpecParam.

## Why This One Is Different
This is the **first paper in the vault whose methods I would defend in review.** Six papers taught us what to distrust; this one shows what rigorous looks like — pre-specified specification space, public code, objective quality tiers, bootstrap for imbalance, dimensional replication, and an honest effect-size figure that undercuts its own significance claims. It also proves that **a rigorous null is publishable**, which materially de-risks our direction.

## The Result, Precisely
- **HC vs ADHD-inattentive main effect: 0 / 576 universes.** With 465 vs 228 subjects, a single test has ~96% power at *d* = 0.3 (~70% at *d* = 0.2), so this bounds the effect at roughly **|d| ≲ 0.2–0.25** (a power-based bound; no formal TOST was run). That is stronger than the paper claims — closer to an equivalence result than a failure to reject.
- **HC vs ADHD-combined: 11 / 576** (1.91%), all positive.
- Everything else is an **interaction with IAF, age, gender** — and it appears only under IAF-relative bands + uncorrected/aperiodic-only power. Under canonical bands + aperiodic adjustment, it vanishes.
- The mechanism is shown directly: `r(IAF, power)` = **−0.17** (canonical) → **−0.70** (IAF-relative). Defining a band relative to IAF injects IAF into the outcome.
- Effect sizes are **small everywhere**, including where interactions are frequent.

**Conclusion we accept:** TBR is not a standalone ADHD marker. Closed as a feature.

## Where the Paper Fails Its Own Standard (four real problems)
1. **Post-hoc subsetting.** The 46/48 and 37/48 "robust" numbers come from filtering the multiverse to the universes with the most significant results, then reporting the proportion within that subset. That is a garden of forking paths applied to the analysis of the multiverse — descriptively useful, evidentially empty.
2. **Binomial test on correlated universes.** 576 universes share the same subjects; positive correlation widens the sampling distribution of "number significant," making the 5% binomial baseline anti-conservative exactly where robustness is claimed.
3. **p-counts instead of effect sizes.** Their own Cohen's *d* figure shows small effects even in the "robust" subsets, but the tables report only significance counts.
4. **No discrimination test.** The clinical claim they rebut (86% sensitivity / 98% specificity) is about classification; every result is a regression coefficient. **The figure the clinical claim requires — a specification curve of AUC under subject-disjoint folds — is absent.**

And one interpretive problem that matters for us:
5. **"Aperiodic-adjusted" is treated as ground truth.** SpecParam's own fit is artefact-sensitive; the paper cites this and then does not control for movement. So "the effect vanishes after 1/f correction" means "no *periodic* difference above the fitted background," which is not the same as "no group difference."

## The Two Ideas This Paper Generated
### (a) The missing multiverse: audit *decoding*, not coefficients
Nobody has done a specification-curve analysis of ADHD-EEG **AUC**. That is the audit the clinical claim actually requires, it forces subject-disjoint folds inside every universe, and it is cheap — linear models on static features. → [[Decoding-Multiverse-and-Aperiodic-Identity]]

### (b) The aperiodic identity fingerprint
`(exponent χ, offset A)` are stable within a person, variable across people, and shift every band power coherently — the exact profile of an identity feature. Hypothesis: **the 21–24 pp PSD leakage gap is largely a 1/f fingerprint, not oscillatory power.** Two cheap tests: predict participant ID from `(χ, A)` alone; then run the 2×2 {aperiodic correction} × {EA} on both subject-ID accuracy and ADHD AUC. → [[Aperiodic-1f-Activity-and-Band-Ratios]] §4

This is the single most valuable experiment in the vault: it links the leakage literature (Geethapriya), the alignment literature (Wang/CBraMod), and the aperiodic literature (this paper) in one table.

## Consequences for Existing Vault Claims
1. **Baibulova's theta dominance must be re-read.** Theta AUC 0.733 vs beta 0.567, canonical bands, no SpecParam. Under this paper's mechanism, that theta "connectivity" is a prime candidate for aperiodic-slope contamination. Concrete re-analysis of an existing result, not a new dataset.
2. **The PSD leakage gap gains a mechanism.** [[Subject-Level-Evaluation-Hygiene]] has the magnitude (21–24 pp) and attributed it to impedance/skull/spectral envelope. This paper supplies the specific quantity: the 1/f exponent and offset.
3. **The artifact thesis gains a spectral form.** Movement → steeper 1/f → higher apparent theta. Same class-correlated artifact, different measurement channel. → [[Class-Correlated-Artifact-Control]]
4. **Differential attrition is now a three-paper pattern.** Kim: 38% of ADHD vs 0% of Tic dropped. This paper: 197 (12.6%) dropped on amplitude, 45 on quality, 69 on SpecParam fit, and the entire hyperactive/impulsive group (n = 85) excluded — the most movement-prone children, disproportionately ADHD, with no group breakdown reported. → new commitment 16.

## Dataset Status Change
**HBN is now proven viable.** N = 1,122 analysable, subtyped, with SWAN severity, public, with a published preprocessing pipeline and code (OSF u5yxv). The vault has been treating HBN as an aspiration; it is now the **leading candidate primary cohort**, and it removes the "no accessible non-saturated dataset" blocker.

Residual caveats: 280 medicated participants (varied but not randomised), ADHD diagnosis by K-SADS with published reliability (usable as a label-noise ceiling), and the same age-composition/movement confounds as everything else.

## Synthesis Across Seven Papers
| Claim | Status |
|---|---|
| ADHD is decodable from resting EEG at AUC ≈ 0.9 | Not supported — 0.74–0.79 is the honest ceiling; 0.9 appears only with minimal cleaning or pooled windows |
| Architecture is the lever | Refuted four times (ShallowConvNet ≈ CTE-Net; CNN > CNN–BiLSTM; CBraMod < theta-GRU; Kim's two tables disagree) |
| TBR is a diagnostic marker | Refuted (0/576, \|d\| ≲ 0.2–0.25) |
| Sub-band power is oscillatory | Unresolved and probably false as stated — 1/f and IAF dominate |
| The lever is subject geometry + artifact + calibration | Still the leading hypothesis, now with a named mechanism (1/f fingerprint) |
| Analytic choice matters as much as architecture | **New, and now the strongest single claim in the vault** |

## Next Actions (in order)
1. The decisive test, if this direction is ever built, is the **falsifier** in [[Decoding-Multiverse-and-Aperiodic-Identity]] §8: 8 universes on a 200-subject HBN subset. If all AUC ∈ [0.48, 0.55], the multiverse variation story is dead and the fingerprint test becomes primary. Recorded here as a design fact, not as work to do now ([[Decision-Log]] commitment 21).
2. Run **T1**: subject-ID accuracy from `(χ, A)` on 100 subjects.
3. Resolve the HBN data-access route and confirm the SpecParam implementation.
4. Re-read Baibulova's theta result with an aperiodic lens.
