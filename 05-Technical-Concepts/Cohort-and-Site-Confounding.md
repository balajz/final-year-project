---
tags:
  - technical-concept
  - methodology
  - leakage
  - evaluation
  - multimodal
---

# Cohort and Site Confounding

Derived from [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]]. The failure mode in which **the label is correlated with where the data came from**, so a model can be accurate without being about the disorder.

## 1. The Definition
If class membership correlates with acquisition source — consortium, site, scanner, protocol version, release batch, atlas, preprocessing pipeline — then source is a valid predictor of the label. A classifier can learn *institution* and report it as *pathology*. Nothing is wrong with the code. Subject-level splitting is correct. Nested CV is correct. The confound is in the sampling frame, and it survives every procedural fix.

This is the same logical structure as [[Class-Correlated-Artifact-Control]] — a nuisance variable that differs between groups — but at the level of acquisition infrastructure rather than the participant's body. It is harder to see because it is not in the signal, it is in the metadata you never plotted.

## 2. Why the Usual Defences Fail
| Defence | Why it does not work here |
|---|---|
| Subject-level splits | Site is constant within subject and shared across many subjects; splitting by subject does not split by site |
| Nested CV / fold-wise selection | Removes *selection* leakage, not *sampling* confounding |
| Train-only normalisation | Per-subject normalisation cannot remove a between-site offset shared by a whole class |
| Inductive evaluation | Closes graph/test overlap, leaves site overlap untouched |
| A permutation null | Destroys the site–label association along with the signal, so it can indicate "no effect" while the model was in fact reading site — a false reassurance |
| More data | Makes the confound *more* decodable, not less |

The permutation null point deserves emphasis because it is counter-intuitive: a label-permutation test is designed to answer "could this pipeline produce this accuracy from noise?" It is not designed to answer "could this pipeline produce this accuracy from metadata?" Those are different questions, and only a **source-prediction control** answers the second.

## 3. The Forms It Takes
| Form | Example | Where we have met it |
|---|---|---|
| **Consortium** | ADHD only from ADHD-200, ASD only from ABIDE | [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]] |
| **Site within consortium** | 27% of HC from sites contributing zero ADHD cases | same paper, Table 1 |
| **Release batch** | HBN's 11 chronological BIDS releases, different collection dates and QC flags | [[Healthy-Brain-Network-HBN]] |
| **Scanner / hardware** | Amplifier, head coil, EEG cap model, impedance target | implicit in every multi-site dataset |
| **Protocol version** | fMRIPrep/FreeSurfer/PCP pipeline generation | [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]] |
| **Atlas / parcellation** | AAL vs Craddock vs FreeSurfer-native | same |
| **Sampling frame** | Completeness criteria that select sites, not subjects | same |
| **Age composition** | Groups differ by age band, and age is also an input feature | HBN, ABIDE |

## 4. The Decisive Controls
1. **Source prediction.** Train the same features to predict *dataset of origin* or *site*. If accuracy is far above chance — and it usually is — then every disease claim must be re-read net of that. Report it in the same table as the main result. This is cheap, decisive, and almost never done.
2. **Site-stratified or leave-one-site-out CV.** The honest generalisation estimate for a multi-site cohort. If performance collapses when a site is held out, the model learned the site.
3. **Within-site analysis, then meta-analysis.** The statistically correct answer for inherently confounded pooling: estimate inside each site, combine effects. Slower, defensible.
4. **Match the classes on site.** If every site contributes to every class, the confound is at least balanced. Report the per-site × per-class table — the paper's own Tables 1–2 contain the evidence and never comment on it.
5. **State the physical units of every feature.** A window defined in samples across different TRs, or a band defined canonically across children with different peak frequencies, is not one feature ([[Aperiodic-1f-Activity-and-Band-Ratios]]).

## 5. Why Harmonisation Is Not the Fix
The reflex is ComBat (or a similar site-effect model). It does not solve this, and can worsen it:

- ComBat estimates site effects **conditional on the protected variables**. When site is nearly collinear with class, it has almost no information with which to separate them.
- The result is either under-correction (site remains) or over-correction (real class signal is removed as "site"), and which one you get is not knowable from the data.
- If site is *perfectly* nested in class, the correction is formally unidentifiable.

Harmonisation addresses **nuisance variance in features**. This is a **confound in the sampling frame**. Design beats correction.

## 6. Diagnostic Signatures
Patterns that should trigger suspicion, several of which appear in the source paper at once:
- The **control group is the hardest class** — often the only class drawn from more than one source.
- The **most heavily weighted modality is demographic** (age/sex), which is often a site/cohort proxy rather than a biological signal.
- Performance **collapses when global feature selection is removed** — the globally selected features were source features.
- Accuracy and AUC **diverge** in the multiclass task while pairwise tasks look healthy.
- A large **drop from the best-reported protocol to the strictest**, with the authors framing the residual as "genuine capability."

## 7. Consequences for Us
- **HBN is structurally protected.** One consortium, one lab, one protocol across releases. Class is not collinear with institution. This is a real reason to prefer it over the ADHD-200 + ABIDE default, and it should be said explicitly in any write-up ([[Healthy-Brain-Network-HBN]]).
- **Any pooled multi-dataset replication is not.** If we ever add ADHD-200 for cross-site validity, treat site as a *stratification variable with its own reported results*, never as extra sample size ([[ADHD-200]]).
- **The transdiagnostic contrast on HBN is the clean alternative** to cross-cohort comparison: vary the *label* inside one cohort rather than vary the *cohort* inside one label.
- **The analogue in time is already a vault commitment:** declare aperiodic handling and IAF policy ([[Decision-Log]] 18). The general rule is one level up — **declare the units in which every feature is defined, in physical terms, and report it per source.**

## 8. Connections
- [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]] — the worked case
- [[Class-Correlated-Artifact-Control]] — the participant-level analogue
- [[Subject-Level-Evaluation-Hygiene]] — why splitting by subject is necessary but not sufficient
- [[Nested-CV-and-Hyperparameter-Leakage]] — selection leakage, the confound this one is often mistaken for
- [[Aperiodic-1f-Activity-and-Band-Ratios]] — the time-unit analogue
- [[Problem-Space-Map]] — data axis: "public/large" is not the same as "comparably acquired"
- [[Decision-Log]] — commitment 22
