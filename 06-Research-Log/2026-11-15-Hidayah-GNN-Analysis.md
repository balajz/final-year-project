---
tags:
  - research-log
  - fmri
  - multimodal
  - leakage
  - methodology
---

# Session Log: 2026-11-15 — Hidayah et al. (2026), Multimodal GNN with Leakage-Aware Evaluation

## What Arrived
A multimodal fMRI paper: ChebGCN over population graphs (rs-fMRI dynamic-FC stability + sMRI volumes + demographics) for ADHD/ASD/HC, evaluated under three protocols that progressively close leakage routes. 564 subjects, 10-fold CV, 14.6 pp drop from loosest to strictest protocol ([note](Hidayah-2026-Multimodal-GNN-ADHD-ASD)).

## The One-Sentence Reading
**It is right about its thesis and wrong about its result.** The thesis — that protocol choice dominates reported performance — is supported by its own ladder. The result — that the framework has "genuine discriminative capability" — is confounded by consortium and site, and the evidence is visible in the paper's own demographic tables.

That combination is worth keeping as a cautionary example: a paper can correctly diagnose one class of leakage while being undermined by a larger one it never looks for. Rigour about method does not guarantee validity of inference.

## What Changed in Our Thinking

**1. A second modality confirms the vault's central claim.** We measured 21–24 pp from changing the split unit (hand-crafted PSD), and 2.5 pp for an end-to-end model. This paper measures 11–15 pp from changing the protocol, on fMRI. Different signal, different cohort, same magnitude. The claim "the evaluation frame moves results more than the model does" is no longer an EEG finding; it is general.

**2. A decomposition worth carrying over:** feature-selection leakage ≈ 2× transduction leakage in two of three tasks. Combined with our own PSD-vs-CNN contrast, the pattern is **leakage concentrates in high-dimensional hand-engineered feature spaces.** That is now a testable generalisation across two modalities, and it makes the aperiodic-fingerprint hypothesis more plausible — hand-crafted spectral features are exactly where subject identity would live.

**3. A new concept note:** [[Cohort-and-Site-Confounding]]. Not previously in the vault in any form. It is a *sampling-frame* confound, so it survives every procedural defence we have codified — subject-level splits, nested CV, inductive evaluation, even permutation nulls (which destroy the very association they would need to detect).

**4. A new guardrail (commitment 22):** when pooling sources, report source-prediction accuracy, and never treat pooled sites as extra sample size.

**5. HBN's comparative advantage became articulable.** One consortium, one lab, one protocol → class is not collinear with institution. That is a *structural* argument for our primary cohort that has nothing to do with sample size, and it is now written down.

**6. A negative result for multimodal-by-default.** In the strictest setting, adding sMRI to rs-fMRI + demographics is not significant (p = 0.25), and unimodal sMRI is ~54% three-class. "Multimodal" in the title is doing less work than the title implies. Worth remembering when we are tempted to add a second modality for its own sake.

## What Did Not Change
- No new candidate. fMRI, and ADHD-200/ABIDE are the most-mined neuroimaging corpora available; there is no direction here for us to enter.
- No revision to the three live candidates. This paper neither kills nor promotes one.
- The breadth gap stands: BCI, sleep, wearables, caregiver tools still have no candidate.

## Things Not To Do With This Paper
- Do not cite **85.5%** as evidence that multimodal GNNs classify ADHD/ASD well. It is a consortium classifier.
- Do not cite the **79.3%** HC-vs-ADHD figure either without noting the site confound and the missing motion control.
- Do not treat the "leakage-aware" label as a guarantee. It closed two routes and left a larger one open — which is, unintentionally, the best argument in the paper for why leakage auditing needs to be *systematic* rather than *targeted at the routes you already thought of*.

## Follow-Ups Worth Keeping (reading/reasoning only)
1. Does source-prediction accuracy exist anywhere for ADHD-200 or ABIDE? If published, it would quantify the ceiling on every pooled study.
2. Does any paper run leave-one-site-out CV on ADHD-200 with a strict protocol? That would give us the real multi-site ceiling.
3. Is there a published correlation between temporal-stability/FC-variability features and framewise displacement? If yes, the "stability" literature needs re-reading.

## Connections
- [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]] · [[Cohort-and-Site-Confounding]] · [[Multimodal-Physiological-Signals]]
- [[Decision-Log]] 22 · [[Problem-Space-Map]] · [[ADHD-200]] · [[Healthy-Brain-Network-HBN]]
