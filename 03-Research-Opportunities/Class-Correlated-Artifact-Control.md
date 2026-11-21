---
tags:
  - research-opportunity
  - eeg
  - artifacts
  - auditing
  - evaluation
---

# Class-Correlated Artifact Control (the experiment "noise robustness" papers omit)

Derived from [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]]; extends the artifact ladder in [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]] §1.

## 1. The Distinction That Decides Everything
"Performance does not drop when artifacts are left in" admits two readings:

| Reading | Mechanism | Implication |
|---|---|---|
| **Robust** | The model ignores nuisance and reads neural signal | Good — the paper's claim |
| **Exploiting** | The nuisance carries class information, and the model reads it | Bad — the model is a movement detector |

These are **not separable without a control**, and the standard control in the literature is wrong. Papers argue that artifacts vary *within* a class ("hyperactivity is heterogeneous across individuals") and conclude the model cannot be using them. That is the wrong axis. Between-group differences in artifact *structure* need no within-person consistency at all — a group that moves more, or differently, produces a class-correlated nuisance with perfectly reproducible statistics.

## 2. Where It Bites in Our Corpus
- **Kim (ADHD vs Tic):** two hyperactive disorders → both classes noisy, but *differently* noisy. Tic severity is episodic/paroxysmal; ADHD hyperactivity is more continuous. In a 2-class contrast, **any** systematic difference in motion energy, blink rate, or muscle tone is a candidate classifier. The 34→21 ADHD attrition (38%, vs 0% for Tic) suggests the two groups' signal quality differed enough to trigger exclusions.
- **CTE-Net on ADHD-Child:** cleaning costs ~10 accuracy points (83.5→73.9), and reference choice rewrites the learned edges (Jaccard 0.067) → the "connectivity" is sensitive to exactly what cleaning removes.
- **CBraMod:** largest degradation of any baseline when 30–75 Hz (EMG band) is removed, on Mumtaz2016.

Same signature in three different models on three datasets ⇒ **artifact dependence is systematic**, not incidental. This is the current best-supported negative finding in the vault.

## 3. The Control Battery (cheap → decisive)
1. **Artifact-only classifier.** Predict the label from *artifact indices alone* — blink rate, EMG band power (30–75 Hz), motion/EMG envelope, epoch rejection rate, signal-quality index. If a 2-feature model beats chance, the label is confounded with recording quality, and every model's performance must be re-read net of it. **This is a 20-line experiment and it is almost never reported.**
2. **Quality-matched evaluation.** Stratify test participants by signal-quality index; report accuracy per stratum. Performance that lives only in the noisiest stratum is artifact-driven.
3. **Artifact counterfactual injection.** Add synthetic blinks/EMG at controlled SNR to the *clean* data of both classes. A robust model's decision is unchanged; an exploiting model's moves with the injected artifact class.
4. **Latent probe.** Predict the quality index from the model's latent space. High $R^2$ ⇒ the representation encodes recording conditions.
5. **Band ladder.** Rerun with 30–75 Hz notch (EMG), 1–4 Hz high-pass sweep (drift), and frontal-channel dropout. Report the accuracy-vs-band curve, not one number.
6. **Aperiodic decomposition.** Fit SpecParam and test whether group differences live in the **exponent/offset** rather than in oscillatory peaks. Movement steepens 1/f, so a class that moves more will show a "neural-looking" low-frequency shift without any oscillation change. See [[Aperiodic-1f-Activity-and-Band-Ratios]].
7. **Class-conditional attribution.** Importance maps computed per class and tested for difference (see [[Explanation-Stability-and-Faithfulness]] §5).

## 4. What a Pass Looks Like
- Artifact-only AUC ≈ 0.5.
- Accuracy flat across quality strata.
- Counterfactual injection moves neither class's decision more than the other's.
- Latent quality-probe $R^2$ low.
- Class-conditional attributions differ in a neurophysiologically interpretable direction.

If any of these fails, the honest contribution is **"X% of reported performance is recording quality"** — which is a publishable measurement result and, in our judgement, more useful to the field than another +1 AUC.

## 5. Why This Is a Viable Project Spine
- It is **model-agnostic** and **dataset-agnostic**: works on the public 121-child cohort (where the ladder is cheapest), on ADHD-200/HBN, and as an audit wrapper applied to *other people's* published pipelines.
- It requires no new architecture, so it dodges the rejected "architecture recombination" direction ([[Decision-Log]]).
- It converts a rhetorical worry ("is this just eyeblinks?") into a number — the missing measurement in essentially every paper we have read.
- It has a natural tool output: a **signal-quality audit + abstention** layer for clinical screening, which is a workflow contribution rather than another classifier.

## 6. Risks
- **Public data may forbid the strongest version.** If the public release is already cleaned, blinks cannot be re-injected faithfully; the control then degrades to indices + stratification + band ladder. Verify what preprocessing the release underwent before committing.
- **Quality index may be unavailable.** Then it must be estimated (e.g., from high-frequency power and kurtosis), and the estimate must itself be validated.
- **Nulls can be boring.** A clean negative ("artifacts do not carry class information here") is a real result but a thin paper; plan the second contribution (alignment or calibration) at the same time.

## 7. Connections
- Papers: [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]
- Concepts: [[Explanation-Stability-and-Faithfulness]], [[Subject-Level-Evaluation-Hygiene]]
- Opportunities: [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]], [[Unsupervised-Alignment-Leverage]]
- Session log: [[2026-11-15-Kim-GCN-Analysis]]
