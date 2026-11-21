---
tags:
  - project-idea
  - candidate
  - adhd
  - eeg
  - multiverse
  - aperiodic
  - alignment
status: candidate-not-selected
---

# Candidate: The ADHD-EEG Decoding Multiverse & Aperiodic Identity Audit

> **Status: candidate, NOT selected.** Synthesized from [[Decoding-Multiverse-and-Aperiodic-Identity]], [[Unsupervised-Alignment-Leverage]], and [[Class-Correlated-Artifact-Control]].

## 1. Real-World Problem
Dozens of papers claim 85%–99% EEG diagnostic accuracy for pediatric ADHD, while rigorous clinical replication ([[Troendle-2026-TBR-Multiverse-HBN]]) finds 0/576 significant specifications for the FDA-cleared theta/beta biomarker, and leak-free benchmarks ([[Shen-2026-Brain4FMs-Benchmark]], [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]], [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]) collapse to 0.72–0.79 AUROC. Clinicians and neuro-AI researchers have no way to separate **genuine neural diagnostic signal** from **analyst degrees of freedom, 1/f subject identity fingerprints, and class-correlated movement artifacts**.

## 2. Core AI & Scientific Contribution
A **measurement-science and representation-auditing framework** on the public **Healthy Brain Network (HBN-EEG, OpenNeuro `ds005505`–`ds005516` / NEMAR, $N > 1,100$)** and replicated on the 121-child IEEE DataPort cohort:
1. **First Specification-Curve Audit of *Decoding* (AUC & PPV), Not Just Regression Coefficients:** Systematically evaluates ~160 defensible pipelines across `{uncorrected PSD, SpecParam periodic, aperiodic-only (χ, A)}` × `{canonical vs. IAF-relative bands}` × `{no alignment vs. Euclidean Alignment (EA)}` × `{clean vs. artifact-filtered strata}` under strict subject-disjoint CV, benchmarked against a **permutation-of-the-multiverse null** and an **age-decoding positive control**.
2. **The Aperiodic Identity Fingerprint Decomposition ($2 \times 2$):** Tests the mechanistic hypothesis that the 21–24 pp segment-to-subject leakage gap in EEG pipelines is driven by a stable personal **1/f spectral fingerprint $(\chi, A)$** + spatial covariance shift, measuring both **participant-ID accuracy** and **ADHD AUROC** across `{raw vs. SpecParam-adjusted} × {unaligned vs. EA}`.
3. **Class-Correlated Artifact Control Battery:** Quantifies how much of any surviving decoding signal is predictable from artifact proxies alone (blink rate, 30–75 Hz EMG power, quality-tier attrition).

## 3. Why It Beats "Model X on Dataset Y"
- Directly explains *why* 15 Brain Foundation Models and complex GNNs/Transformers hit a hard wall at ~0.78 AUROC.
- Produces a reusable, open-source Python benchmark/audit harness (`specparam` + `mne` + `scikit-learn`) and a definitive empirical answer regardless of whether ADHD AUROC is high, moderate, or null.

## 4. Feasibility & Data Access
- **Data:** HBN-EEG is openly hosted on [NEMAR](https://nemar.org/dataexplorer/detail?dataset_id=ds005505), on the public S3 mirror (`s3://fcp-indi/data/Projects/HBN/BIDS_EEG/`, `--no-sign-request`), and mirrored through OpenNeuro, in BIDS format with CBCL psychopathology factors (attention, internalizing, externalizing, p-factor) in the participant metadata — no DUA bottleneck for the BIDS releases.
- **Compute:** CPU/M-series friendly; runs completely locally without cloud GPU clusters.

## 6. Relationship to the Detailed Design Note
This note is the **proposal**. The working design — specification dimensions, controls, metrics, expected outcomes, novelty statement, and the one-week falsifier — lives in [[Decoding-Multiverse-and-Aperiodic-Identity]]. The mechanistic background is in [[Aperiodic-1f-Activity-and-Band-Ratios]] and [[Multiverse-and-Specification-Curve-Analysis]].

**Access verified (2026-11-15).** The NEMAR/S3 route is real and needs no DUA: 11 releases, 2,782 subject-records, ~1.9 TB, 20-subject 100 Hz mini sets per release. See [[Healthy-Brain-Network-HBN]]. The practical constraint is therefore **storage and per-task `n`**, not permission. Outstanding: whether releases overlap in subjects, and the per-task counts by age band.

## 7. Competing Candidates (none selected)
- [[Candidate-Event-Locked-NeuroBehavioral-HBN]] — event-locked active-paradigm contrast, trades breadth for temporal precision.
- [[Candidate-Evidence-Aware-ADHD-Screening]] — calibration/abstention framing.

## 8. Connections
- Opportunities: [[Decoding-Multiverse-and-Aperiodic-Identity]], [[Unsupervised-Alignment-Leverage]], [[Class-Correlated-Artifact-Control]]
- Datasets: [[Healthy-Brain-Network-HBN]], [[IEEE-DataPort-ADHD-Child-121]]
- Concepts: [[Multiverse-and-Specification-Curve-Analysis]], [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Subject-Level-Evaluation-Hygiene]]
- Decisions: [[Decision-Log]]
