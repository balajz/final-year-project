---
tags:
  - research-paper
  - adhd
  - asd
  - fmri
  - multimodal
  - gnn
  - leakage
  - methodology
---

# Hidayah, Wiharto & Suryani (2026) — Multimodal ChebGCN for ADHD/ASD/HC with Leakage-Aware Evaluation

- **Citation:** Hidayah, C., Wiharto, & Suryani, E. (2026). *A Multimodal Graph Neural Network for Multiclass ADHD and ASD Classification with Leakage-Aware Evaluation.* Journal of Electronics, Electromedical Engineering, and Medical Informatics (JEEEMI), 8(4), 1354–1370. [DOI: 10.35882/jeeemi.v7i3.948](https://doi.org/10.35882/jeeemi.v7i3.948)
- **Affiliations:** Universitas Sebelas Maret, Surakarta, Indonesia.
- **Provenance flags:** the DOI encodes `v7i3` while the header says Vol. 8 No. 4; received April 2025 → accepted June 2025 → "available online 27 June 2025" → copyright 2026 in an October 2026 issue. The timeline and the volume/DOI disagree. Not disqualifying, but **verify the version of record before quoting a number.**
- **Code:** "available from the corresponding author upon reasonable request." No repository. Single seed (42).

---

## 1. The Paper's Claim
Multimodal population-graph learning — dynamic functional connectivity from rs-fMRI, subcortical volumes from sMRI, and demographics — distinguishes ADHD, ASD and healthy controls. The real argument is methodological: **the evaluation protocol, not the model, drives reported accuracy.** Three protocols that progressively close leakage routes produce 85.5% → 80.7% → 70.9% on the three-class task, and the authors conclude that "leakage-aware evaluation" should be standard.

## 2. What They Actually Did
- **Cohorts:** 188 ADHD (ADHD-200), 188 ASD (ABIDE I), 188 HC (94 from each), N = 564. Subjects included only with complete rs-fMRI + sMRI + phenotype; **no imputation**, no motion exclusion, no nuisance regression, no QC. Binary tasks draw HC from the same cohort as the disorder.
- **rs-fMRI:** PCP fMRIPrep derivatives → AAL 116 ROIs → z-scored → sliding window (**30 volumes, step 15**) → per-window Pearson FC → upper triangle (**6,670 edges**) → "temporal stability" per edge = exponential kernel over consecutive-window differences, σ = 1, normalised by (P−1).
- **sMRI:** 45 FreeSurfer subcortical volumes → mRMR (mutual-information quotient).
- **Feature selection:** DFS (learned input-layer weights with elastic net) for fMRI; mRMR for sMRI; candidate counts 400–800 and 10–40, chosen on a validation split.
- **Graph:** one kNN + Gaussian-similarity population graph per modality (nodes = subjects), demographic graph by attribute matching; separate normalised Laplacians; 2-layer ChebGCN (order 2, hidden 64, dropout 0.3), adaptive learnable modality weights, full-batch Adam.
- **The three settings:**
  - **S1** transductive graph + global feature selection (both leaks open).
  - **S2** inductive graph per fold + global feature selection (graph leak closed).
  - **S3** inductive graph built inside each fold + feature selection fitted on training subjects only.
- **Metrics:** accuracy, macro-F1, AUC; mean ± SD over stratified 10-fold CV with a t-based 95% CI across folds. Wilcoxon signed-rank + Holm–Bonferroni for modality ablations.

## 3. The Numbers
| Task | S1 | S2 | S3 | S1→S2 | S2→S3 |
|---|---:|---:|---:|---:|---:|
| HC vs ADHD vs ASD | 85.5 | 80.7 | **70.9** | −4.8 | −9.8 |
| HC vs ASD | 92.5 | 85.9 | **81.7** | −6.6 | −4.2 |
| HC vs ADHD | 90.4 | 86.7 | **79.3** | −3.7 | −7.4 |

- In S3, unimodal three-class accuracy collapses: **rs-fMRI 54.6%, sMRI 53.7%**, rs-fMRI+demo 63.7%, and the full multimodal 70.9%.
- **Multimodal vs rs-fMRI+demo is not significant** (Holm-adjusted p = 0.25, r = 0.499). Adding sMRI to fMRI+demographics fails.
- Learned fusion weights in S3 are near-uniform, with **demographics highest** in the multiclass (0.346) and HC-vs-ASD (0.337) tasks.
- Confusion matrix (best fold only): ADHD 18/19 correct, ASD 16/19, **HC 6/18 wrong** — the authors read this as "heterogeneous controls."

## 4. What Is Genuinely Good
1. **The protocol ladder is the right instrument.** Three rungs, same pipeline, same folds, one variable changed at a time — legible in a way that eight-universe multiverses often are not. This is a better teaching artefact than most specification curves.
2. **They report the drop.** The field's habitual move is to publish the S1 number; they publish all three and lead with the gap.
3. **Train-only normalisation, fold-wise selection, per-fold graphs** in S3 — the mechanical hygiene is mostly correct, and the algorithm is specified well enough to reimplement.
4. **Honest limitations:** no ComBat, internal CV only, best-fold confusion matrix, no biological validation of selected features, code on request only. They say the quiet parts out loud.
5. Internal arithmetic checks out where it can: 6,670 = C(116, 2); site-wise subject counts in Tables 1–2 sum to 188 per class.

## 5. Critique

### 5.1 The three-class task is confounded by construction — and this is fatal to its headline
ADHD comes only from ADHD-200; ASD only from ABIDE; HC from both. **Class is nearly collinear with consortium of origin**, and therefore with scanner, sequence, TR, preprocessing pipeline, screening instrument, age range and site mix. A model that reaches 85.5% three-class accuracy may be doing nothing but consortium identification, and the paper never runs the one control that would settle it: **predict dataset-of-origin from the same features.**

This is the paper's own thesis applied one level up. It audits *protocol* leakage while remaining silent on *cohort* leakage — the kind no amount of nested CV can remove, because it is in the sampling design, not the code.

The same confound explains their most puzzling finding. They report HC as the hardest class (6/18 wrong) and interpret it as "heterogeneous feature representations." But HC is the **only class drawn from two distributions**; ADHD is one distribution, ASD is one. Mixed-source controls being hardest is exactly what a consortium-signal reading predicts. The observation is evidence *for* the confound, read as evidence for a neuroscience claim ([[Cohort-and-Site-Confounding]]).

### 5.2 The binary tasks are cleaner, but their own tables still show a site–class confound
The fix for multiclass is to draw HC from the same cohort as the disorder — they do that. But site is not controlled:

- **ADHD-200 (Table 1):** Pittsburgh contributes 0 ADHD / 39 HC; WashU 0 / 11. If Table 1 is the included sample, **50 of 188 HC (27%) come from sites contributing no ADHD cases at all.**
- **ABIDE (Table 2):** Leuven 26 ASD / 1 HC; KKI 12 / 0; NYU 37 / 0. **75 of 188 ASD (40%) come from sites contributing no HC.**

Site is therefore decodable and class-correlated *within* the binary tasks. No site-stratified CV, no leave-one-site-out, no site covariate, no per-site reporting. The "inductive" protocol closes subject overlap and leaves site overlap wide open.

### 5.3 Completeness-driven selection is a site filter
Inclusion requires complete rs-fMRI + sMRI + phenotype, with no imputation. sMRI availability differs by site, so this criterion selects *sites* as much as subjects. No table compares included vs excluded participants per site — the same attrition defect we have now logged three times ([[Decision-Log]] 16), here with a site dimension.

### 5.4 The S3 "inductive" model builds a graph over the test set
Algorithm 1 constructs `A_train`, `A_val` **and `A_test`**, then applies the model to the test subjects using `L_test`. If the test graph is built by kNN over the test subjects' own features, message passing happens **among test subjects**, so a prediction depends on which other children happen to share that fold. Predictions are not independent, per-subject deployment is impossible, and the fold-to-fold CI is measuring composition as well as partition noise.

If instead inference is per-node singleton, a 2-hop ChebGCN aggregating over an empty neighbourhood degenerates to an MLP on concatenated features — and the graph does nothing.

Either way, one of the paper's two central claims ("fully inductive," "the graph helps") must be false. The disambiguating experiment is cheap: permute which subjects share a test fold and check prediction invariance.

### 5.5 No motion control — stated as if it were neutral
"no additional motion-based exclusion, nuisance regression, or quality-control procedures were applied." Head motion is the best-documented confound in ADHD-200 and ABIDE, and it differs by group. Motion inflates apparent FC dynamics, which is precisely what a **temporal-stability** feature measures. The novel feature is therefore a plausible motion meter, and motion is class-correlated. This is the single largest threat to the biological reading of the result, and it is disclosed but not analysed.

### 5.6 Windows are indexed in volumes, not seconds — across sites with different TRs
The window is 30 *time points*. ADHD-200 and ABIDE sites use different TRs, so 30 volumes is a different physical duration at every site (roughly 60–90 s). "Temporal stability" is computed at a site-dependent timescale, and the number of windows differs by site as well.

This is the fMRI analogue of the vault's IAF/band commitment ([[Decision-Log]] 18): **a feature defined in sample units across a heterogeneous acquisition is not one feature.** It should be stated in seconds and reported per site.

### 5.7 The one hyperparameter that defines the feature is never justified
σ = 1 in the exponential kernel is fixed, not swept, not derived, and not sensitivity-tested — while the entire novelty claim rests on that kernel. Feature counts get five candidates and validation selection; σ gets nothing.

### 5.8 They ran the decomposition and didn't state it
| Task | Inductive effect (S1→S2) | Fold-wise FS effect (S2→S3) |
|---|---:|---:|
| Multiclass | 4.8 pp | **9.8 pp** |
| HC vs ASD | **6.6 pp** | 4.2 pp |
| HC vs ADHD | 3.7 pp | **7.4 pp** |

In two of three tasks **feature-selection leakage costs about twice as much as graph transduction**. That is the paper's most transferable finding and it appears only implicitly, as an artefact of a table a reader must difference by hand.

### 5.9 Statistical inference on correlated folds
Wilcoxon signed-rank across 10 folds treats folds as independent samples. They are not — training sets overlap by 90%. The test is anti-conservative; the "95% CI" from Eq. 20 is a partition-noise interval, not a generalisation interval ([[Decision-Log]] 6, 12). Three of five comparisons report **exactly r = 0.886**, which is what a rank statistic does when a few fold differences dominate; it is descriptive, not evidential.

### 5.10 Internal inconsistency in the feature counts
Table 3 fixes the rs-fMRI candidate grid at **[400, 500, 600, 700, 800]** and Algorithm 1 draws `c` from that grid. But S3's "optimal rs-fMRI feature numbers" are reported as **103, 220 and 252** — all outside the grid. Either the grid differed in S3 (undocumented) or the reported values come from a different selection path. This is a reproducibility defect that needs author clarification before any S3 number is reused.

### 5.11 The proposed remedy would not fix the problem
They suggest ComBat for the site confound. ComBat estimates site effects *conditional on the protected variables*. When site is nearly collinear with class, it has little information with which to separate them, and it can remove real signal, distend the residual, or — worst case — manufacture separation. For this confound the correct remedies are design-level: match the classes on site, run within-site analyses and meta-analyse, or use leave-one-site-out CV. **Harmonisation is not a substitute for a confounded sampling frame** ([[Cohort-and-Site-Confounding]]).

### 5.12 Novelty is a conjunction of components, and the efficiency claim is unmeasured
The contributions are: adapt existing temporal-stability features with a simplified kernel, combine two existing selectors, and integrate three modalities into an existing ChebGCN. The defensible contribution is the evaluation ladder, which is methodological. The "improves computational efficiency" claim has no runtime or memory measurement attached.

## 6. What Survives (what I would cite)
- **Protocol choice is worth 11–15 accuracy points** on the same pipeline and the same folds, in a modality entirely different from ours.
- The decomposition: **feature-selection leakage ≳ transduction leakage** (roughly 2:1 in two of three tasks).
- A clean three-rung template, better suited to a written report than an eight-universe grid.
- A negative result about multimodal-by-default: **sMRI adds nothing over rs-fMRI + demographics** (p = 0.25), and unimodal sMRI is ~54% three-class.
- A well-documented failure mode for pooled cohorts ([[Cohort-and-Site-Confounding]]).

## 7. Relevance to Our Project
**Verdict: not a competitor — it is external corroboration plus a warning label.**

- **Not a competitor.** fMRI, not EEG; ADHD-200 and ABIDE are the two most-mined neuroimaging datasets in existence; the architecture is assembled from prior work by the same group. Nothing here is a direction we should enter.
- **It corroborates the vault's central claim in a second modality.** Our EEG audit measured 21–24 pp from a split-unit change (PSD/SVM) and 2.5 pp for an end-to-end model. This paper measures 11–15 pp from a protocol change. Different signal, different cohort, same magnitude, same lesson: **the evaluation frame moves results more than the model does.** That is now two independent domains.
- **The 2:1 decomposition suggests a mechanism worth carrying over:** leakage concentrates in *high-dimensional hand-engineered feature spaces*, and end-to-end learned representations leak less. Our vault already hints at this (PSD leaks, raw CNN does not). It is a testable generalisation, and it strengthens the aperiodic-fingerprint hypothesis, since hand-crafted spectral features are exactly where subject identity lives ([[Aperiodic-1f-Activity-and-Band-Ratios]]).
- **HBN is structurally immune to the condition that undermines this paper.** All HBN subjects come from one consortium, one lab and one acquisition protocol, so class is not collinear with institution — even across releases. That is a genuine comparative advantage of our primary cohort over the ADHD-200 + ABIDE default, and worth stating in any proposal ([[Healthy-Brain-Network-HBN]]).
- **The HC-is-hardest trap generalises to us.** Any design that pools cohorts — including our Tier-2 ADHD-200 plan, or mixing HBN releases — makes "control" a mixture while disorders are single-source. The transdiagnostic contrast on HBN avoids it; a pooled multi-dataset replication would not.
- **It also updates the ADHD-200 card.** Pooling ADHD-200 sites for a novel claim is now demonstrably a site-confounding exercise, not a scaling exercise ([[ADHD-200]]).

## 8. Open Questions
1. Does dataset-of-origin decode from the same features at near-ceiling accuracy? (The control they omitted.)
2. Is inference per-node or over a test-only graph? If the latter, "inductive" is mislabelled.
3. Why are S3's optimal feature counts outside the declared grid?
4. Is the temporal-stability feature correlated with framewise displacement? If yes, the paper's signal is motion.
5. What happens under leave-one-site-out CV?

## 9. Connections
- Concepts: [[Cohort-and-Site-Confounding]] (new), [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]], [[Multiverse-and-Specification-Curve-Analysis]]
- Areas: [[Multimodal-Physiological-Signals]], [[Problem-Space-Map]], [[Neurological-Conditions-Landscape]]
- Datasets: [[ADHD-200]], [[Healthy-Brain-Network-HBN]]
- Log: [[2026-11-15-Hidayah-GNN-Analysis]]
