---
tags:
  - research-log
  - foundation-models
  - benchmark
  - bci
  - leakage
  - methodology
---

# Session Log: 2026-11-15 — Liu et al. (2026), EEG-FM-Compass

## What Arrived

A *National Science Review* review + benchmark: 55 EEG foundation models taxonomised, 12 open-source FMs + 8 specialists benchmarked across 13 datasets / 9 BCI paradigms, in LOSO and within-subject few-shot scenarios, with full fine-tuning vs linear probing ([note](Liu-2026-EEG-FM-Compass-Benchmark)).

## The One-Sentence Reading

**The most useful benchmark in the vault, and its headline is weaker than its tables: the paper's own numbers show that the FM-vs-classical verdict flips with the amount of calibration data available, and three of its eight FM wins are on corpora the models were pre-trained on.**

## What Changed in Our Thinking

**1. The BCI quadrant stopped being an argument.** It was a well-reasoned area note with one alignment figure behind it. It now has 13 datasets, 9 paradigms, a protocol ladder, a cost table, and a concrete demonstration that specialists win on 5/13 tasks outright — including every P300 dataset, seizure detection, sleep staging and SSVEP. The area note's claim that BCI is "structurally easier" survives; its claim that BCI is *unexplored* does not. **It is saturated at the decoder level and wide open at the protocol level.** That is a more precise, and more useful, position.

**2. Our central hypothesis acquired a third independent confirmation — and a better form.** We have said "the evaluation frame beats the model." Compass shows a new axis of the frame: **the labelled budget**. On three MI datasets, CBraMod's advantage over CSP+LDA goes +14.8 → −10.3, +2.2 → −1.8, +7.1 → −5.6 when the fine-tuning set shrinks from "all trials of the training subjects" to "30% of one session." Twenty-five accuracy points from a data-quantity change, on the same model, same task, same splits. That is not a model result; it is a boundary condition on every model result in the field.

**3. A new leakage class, and it is the most defence-resistant one we have.** [[Pretraining-Corpus-Overlap]]. Procedural leakage is caught by subject-disjoint CV. Sampling-frame leakage is caught by site-stratified CV. Corpus-provenance leakage is caught by *neither*, because the split is computed inside a dataset that was already in the model's unsupervised pre-training set — and the permutation null cannot see it either, since the null destroys the association it would need. Compass's SEED column is the cleanest example in our reading: 88.31 for EEGPT and 79.18 for LaBraM against 52–54 for every other FM, on the one task the field agrees is unsolved cross-subject. That is not a representation result.

**4. Two benchmarks, opposite conclusions, both defensible.** [[Shen-2026-Brain4FMs-Benchmark]] says objective family matters (AE > contrastive, bidirectional > autoregressive). Compass says objective family is not decisive (ranks 1–15, 7–18, 9–20, all overlapping). The difference in tuning policy explains it: Brain4FMs fixed `lr = 1e-5` across 15 architectures and produced F1 = 0.00 collapses; Compass tunes per model. **Per-model tuning absorbs the objective effect.** So the disagreement is not a contradiction — it is a measurement of how large the tuning effect is relative to the design effect. It also means neither paper's objective ranking is citable, and it is the first time the vault's thesis has been confirmed *inside* the benchmark literature rather than across modalities. → commitment 25.

**5. A fourth candidate, from the empty quadrant.** [[Candidate-Session-Shift-BCI-Calibration]]. Compass covers {across subject, same session} and {same subject, same session}. The deployment cell — **same user, new day, new cap placement** — is neither, and it is what Euclidean alignment was designed for. The exchange-rate framing (how many labelled trials does unsupervised alignment replace?) turns the vault's alignment work into a deployment quantity. Commitment 19 is unblocked.

**6. Commitment 2 got sharper.** We banned "Model X on Dataset Y." Compass makes "Model X on 13 datasets" equally infeasible — 24 A800s + 8 A100s. Any candidate that requires re-benchmarking FMs is dead on criterion 4, and now we can say why with a number.

## What Did Not Change

- **The three existing candidates remain live and unranked.** Compass neither kills nor promotes them; it is a different quadrant and does not bear on the ADHD ceiling.
- **No scaling-law conclusion is adopted.** The paper's Q3 is a cross-sectional correlation across models that differ in corpus, objective, tokenizer, tuning and architecture. It has one within-family comparison. "No evidence in the tested range" is the honest version; "EEG FMs do not scale" is not, and the vault should not repeat it.
- **No revision to the ADHD numbers.** Compass contains no ADHD dataset.
- **The vault is still ideation-only.** Nothing was run. The candidate's decisive quantities (`k*`, session-identification accuracy) are named, not measured.

## The Overlooked Finding

Compass reports the MI inversion in its tables and does not state it in its text. The paper says "current EEG FMs rely on a relatively large amount of fine-tuning data to realize their advantage, and their benefit diminishes when only limited calibration data are available." That is directionally right and quantitatively understated. What the tables show is a **sign reversal on 3/3 datasets**, not a diminishing benefit, and a collapse to near-parity on 2/2 P300 datasets. Five for five monotone.

The reason it matters: "FMs need more data" is a caveat. "Classical pipelines beat FMs under the calibration budget the paper itself calls deployment-realistic, on every motor-imagery dataset tested" is a finding — and it is the finding the abstract does not report.

Caveat that must travel with it: the inversion is *also* a bias–variance effect. A 4M-parameter model fine-tuned on <30 trials per class will lose to a 4-parameter-per-feature linear classifier regardless of representation quality. So it is not evidence that pre-training is worthless; it is evidence that **the crossover point between pre-training and classical pipelines is a function of the labelled budget, and nobody reports the crossover.** That reframing is the candidate's premise.

## Things Not To Do With This Paper

- Do not cite **88.31 on SEED** or **81.92 on TUAB** as generalization. Both are in-corpus or likely in-corpus ([[Pretraining-Corpus-Overlap]]).
- Do not cite **"no scaling laws"** as established. Cite "no monotonic relation observed in a cross-sectional comparison that cannot identify one."
- Do not cite the **Nemenyi non-significant group** as evidence of parity. Absence of evidence of superiority is the finding; equivalence is not.
- Do not cite **"average decoding accuracy"** pooled across 13 datasets whose chances run 20%–50%. It is not a quantity.
- Do not cite **80.18% on CHB-MIT** as a seizure-detection performance. It is segment balanced accuracy with no false-alarm rate, no latency, no patient-level pooling.
- Do not use this paper as a template. We cannot re-run it, and it cost 32 GPUs to produce one ranking table.

## Follow-Ups Worth Keeping (reading/reasoning only)

1. **Is TUAB a subset of TUEG at the recording level?** If yes, every TUEG-pre-trained model's TUAB number — not just LUNA's — is in-corpus. Cheap to settle from corpus documentation.
2. **Which of the 12 evaluated FMs pre-trained on TUEG-family corpora**, and does any report participant identifiers? This determines how much of the clinical benchmark is salvageable.
3. **Is the MI inversion reproduced outside Compass?** Three datasets, one paper, one tuning policy. A second source would make it a fact rather than a table.
4. **Has anyone published a calibration-budget curve for cross-session BCI** (accuracy vs k labelled trials, aligned vs unaligned, held-out session)? This is the candidate's prior-art check and it is the gating question.
5. **What is the published cross-session ceiling on BCI-IV-2a/2b** for CSP+LDA and EEGNet? If it is already near within-session, the candidate's premise weakens before any design work.

## Connections

- [[Liu-2026-EEG-FM-Compass-Benchmark]] · [[Pretraining-Corpus-Overlap]] · [[Candidate-Session-Shift-BCI-Calibration]]
- [[Brain-Foundation-Models-Landscape]] §7 (the two-benchmark disagreement) · [[BCI-Paradigms-and-Applications]] §3b
- [[Decision-Log]] 24–25 · [[Assumptions-Register]] A13 · [[Problem-Space-Map]] §3–§4
- [[Shen-2026-Brain4FMs-Benchmark]] · [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] · [[Unsupervised-Alignment-Leverage]]
