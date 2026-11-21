---
tags:
  - technical-concept
  - leakage
  - foundation-models
  - benchmark
  - methodology
  - evaluation
---

# Pretraining–Corpus Overlap (Corpus-Provenance Leakage)

> **One line:** when the evaluation corpus is a subset or derivative of the pre-training corpus, the model may have already seen the test recordings — and every standard leakage defence passes anyway.

Derived from [[Liu-2026-EEG-FM-Compass-Benchmark]] §4.3 and [[Shen-2026-Brain4FMs-Benchmark]]. Related but distinct from [[Cohort-and-Site-Confounding]] and [[Nested-CV-and-Hyperparameter-Leakage]].

---

## 1. Why This Is a Separate Bug

The vault now has three leakage classes, and they require three different defences. They are easy to confuse because all three produce "a number that is too high."

| Class | What is shared | Defence | Can standard CV catch it? |
|---|---|---|---|
| **Procedural** ([[Nested-CV-and-Hyperparameter-Leakage]], [[Subject-Level-Evaluation-Hygiene]]) | epochs from the same subject across train/test; model selection on the reporting folds | subject-disjoint splits, nested selection | **Yes** — this is what CV is for |
| **Sampling-frame** ([[Cohort-and-Site-Confounding]]) | class membership correlates with source/site | per-site × per-class table, source-prediction accuracy, leave-one-site-out | **No** — the split is clean *within* the confound |
| **Corpus-provenance** (this note) | the exact recordings, possibly the exact participants, used as test data were in the model's unsupervised pre-training set | per-model pretraining manifest + recording-level overlap audit | **No** — the downstream split is computed inside a dataset that was already in pretraining |

The third one is new to the field because self-supervised pre-training needs **no labels**. Nobody audits a corpus for label leakage, so the corpus is never checked against anybody's test set. The default practice is to scrape the same public repositories everyone benchmarks on — TUEG, TUH, Sleep-EDF, SEED, BCIC-IV — and those repositories are frequently *supersets* of the benchmarks.

## 2. The Structural Mechanism

1. Pre-training corpora are assembled from aggregators (TUEG, TUH, OpenNeuro, NEMAR).
2. Benchmarks are assembled from *the same aggregators*, because they are the data that exists.
3. TUAB is derived from TUEG; the TUH Seizure Corpus is derived from TUEG; several "independent" MI datasets share subjects; Sleep-EDFx is in many sleep pre-training mixes.
4. Therefore "pre-trained on 27,000 hours of EEG" very often means "pre-trained on the test set plus 26,900 other hours."
5. The overlap is invisible in the downstream paper because the pre-training paper reports corpus *names and hours*, not participant identifiers.

The failure is not dishonesty. It is that **the unit of disclosure (dataset name) is coarser than the unit of contamination (recording/participant)**.

## 3. Why It Survives Every Defence in the Decision Log

- **Subject-disjoint splitting** — passes. The test subject is disjoint from the *fine-tuning* subjects. Nothing in the split knows about pre-training.
- **Nested CV** — passes. Nested selection is orthogonal.
- **Inductive / held-out evaluation** — passes. The test labels were never seen.
- **Permutation null** — passes, and this is the subtle part. A label permutation destroys the label↔input association, so a model that memorized recordings gains *nothing* under the null and the null looks clean. The advantage is real only when the true labels are used — which is exactly the condition the null is designed to destroy.
- **Leakage-aware ranking** — is a *repair*, not a defence. Dropping a whole dataset from an average restores the ordering of the aggregate; it does not make the dropped number interpretable, and it discards the evidence rather than correcting it.

This makes corpus-provenance leakage the most defence-resistant of the three, because it operates on the model's weights rather than on the experimental protocol.

## 4. How to Detect It (paper-level, no execution)

1. **Manifest, at recording level.** For each model: the list of corpora, and for each corpus, whether participant/recording identifiers are published. If a model reports only hours, the overlap is unknown, not zero.
2. **Provenance chains.** Check whether the benchmark corpus is a *subset* of a pre-training corpus. Repositories document this: TUAB/TUSZ are subsets of TUEG; several "independent" corpora are re-releases.
3. **Corpus-identity probe (the diagnostic).** Train a classifier to predict *which corpus* a window came from, using the model's frozen embeddings. If corpus identity is highly decodable, the encoder carries provenance information — and provenance is confounded with label whenever a corpus is single-class or single-site.
4. **Read the gap, not the score.** Models with an in-corpus task should look *qualitatively* different on it — 20–35 point jumps with no plausible neural explanation, or the only model above chance on an otherwise-solved-hard task. Both patterns appear in Compass (SEED, TUAB).

## 5. Worked Example: Compass

| Cell | In-corpus? | Score | Peer FMs on the same task |
|---|---|---|---|
| EEGPT on SEED | **yes** (3-class emotion) | 88.31 | 52.5, 53.6, 49.7 … |
| LaBraM on SEED | **yes** | 79.18 | — |
| LUNA on TUAB | **likely** (TUEG ⊃ TUAB) | 81.92 | 80.49, 77.03, 76.23 |
| Every FM on SEED-IV (Brain4FMs) | no | AUROC ≈ 0.53 | cross-subject emotion is unsolved |

The SEED column is the cleanest single illustration in the literature we have read: a task the field considers *unsolved cross-subject* reaches 88% for exactly the two models whose pre-training corpus contains it. No amount of subject-disjoint CV, nested selection or permutation testing would flag that. Only the manifest does.

**Confidence:** TUAB ⊂ TUEG is asserted from the corpora's documented derivation and should be verified at the recording level before being cited as fact. The SEED pattern is inferred from the magnitude gap and the paper's own in-pretraining marker convention; the marker itself should be confirmed in Tables 2–3.

## 6. What It Invalidates, and What It Does Not

**Invalidates:**
- any individual in-corpus number presented as generalization;
- any claim of the form "model X is the best EEG model" that rests on an in-corpus task;
- any comparison between a model that saw the corpus and one that did not (this is not a model comparison at all — it is a memorization-vs-learning comparison).

**Does not invalidate:**
- the benchmark's *within-corpus* comparison, **if all compared models are equally in-corpus** — but then the comparison measures fitting speed, not transfer, and must be labelled as such;
- the benchmark's other datasets, provided in-corpus cells are reported separately rather than footnoted;
- a model's usefulness as a *backbone to fine-tune* — a model that memorized TUEG is still a legitimate initialization for TUEG-like data. That is a deployment claim, and it should be stated as one.

## 7. The Rule (commitment 24)

Never compare models whose pre-training corpus contains the evaluation corpus, and never report a within-corpus result as generalization. Required for any FM claim:

- (a) a per-model pre-training → downstream mapping at **recording/participant** level, not dataset-name level;
- (b) exclusion of any downstream dataset whose source corpus appears in pre-training, from every headline average and every headline sentence — not only from a supplementary ranking;
- (c) if the cell must be kept, label it **in-corpus** in the main table;
- (d) acknowledgement that harmonisation does not help (there is nothing to harmonise — it is the same recordings) and that permutation nulls cannot detect it.

## 8. Connections
- **Papers:** [[Liu-2026-EEG-FM-Compass-Benchmark]] · [[Shen-2026-Brain4FMs-Benchmark]] · [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]]
- **Sibling leakage classes:** [[Cohort-and-Site-Confounding]] · [[Nested-CV-and-Hyperparameter-Leakage]] · [[Subject-Level-Evaluation-Hygiene]]
- **Areas:** [[Brain-Foundation-Models-Landscape]] · [[BCI-Paradigms-and-Applications]]
- **Decisions:** [[Decision-Log]] 24 · [[Assumptions-Register]] A13
