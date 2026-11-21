---
tags:
  - dataset
  - adhd
  - eeg
  - public
  - multi-site
---

# ADHD-200

**Status: not yet investigated. Facts below are from general knowledge, not from a paper in this vault — verify against the official ADHD-200 documentation before use.**

## Identity
- **Source:** ADHD-200 Consortium, distributed via the Neuro Bureau / NITRC (1000 Functional Connectomes Project).
- **Access:** public, registration required. Includes **resting-state fMRI** as the primary modality and **EEG for a subset** — the EEG portion is much smaller than the fMRI portion and is the only part relevant to us.

## Acquisition (to verify)
- **8 sites** (NYU, Peking, Brown, Kennedy Krieger, Oregon, Pittsburgh, Washington University, Duke).
- **19 channels**, 128 Hz for most sites, linked-earlobe reference for most.
- Ages **7–21**.
- Resting state; **EO/EC availability differs by site**.
- Phenotypes: ADHD subtype, age, sex, handedness, IQ, medication status, connectomics measures.

## Why It Would Be Useful
- **Multi-site by construction.** That makes site a hard grouping variable — which is a liability for pooled analysis and an **asset** for our project: cross-site generalization is exactly the test that a single-cohort multiverse cannot run.
- If the specification-curve shape from HBN replicates across ADHD-200 sites with different amplifiers, the "analyst vs brain" decomposition gains external validity.
- It is also the natural second cohort for the aperiodic identity test, since a fingerprint should be consistent within subject across sites **only if it is neural rather than hardware**.

## Risks
- **Site is trivially decodable** from EEG (impedance, amplifier, filter settings). Any multi-site model must group by site, and any reported AUC must be reported per site. This is a bigger version of the confound in [[IEEE-DataPort-ADHD-Child-121]].
- **Diagnostic procedure is not harmonised** across sites (some K-SADS, some custom), so label noise varies by site.
- The EEG subset may be too small for subtype-level analysis.
- Medication status is site-dependent and inconsistently recorded — the same provenance problem as everywhere else in this field.

## Status in Our Project
- **Tier 2.** Not needed for the pilot or the first paper. Needed only if the HBN result is promising and we want a cross-site replication.
- **Warning added 2026-11-15:** [[Hidayah-2026-Multimodal-GNN-ADHD-ASD]] pools 188 ADHD-200 subjects with 188 ABIDE ASD subjects and 188 controls, and its own tables show class–site collinearity (Pittsburgh 0 ADHD / 39 HC; WashU 0 / 11). Pooling sites is not extra sample size; it is a confound factory ([[Cohort-and-Site-Confounding]], [[Decision-Log]] 22). If ADHD-200 is ever used, use **leave-one-site-out CV** and report per site.
- **Next action:** locate the EEG subset size and the per-site channel/rate table before committing any design to it.

## Connections
- Datasets: [[Healthy-Brain-Network-HBN]], [[IEEE-DataPort-ADHD-Child-121]]
- Opportunities: [[Decoding-Multiverse-and-Aperiodic-Identity]]
- Concepts: [[Subject-Level-Evaluation-Hygiene]]
