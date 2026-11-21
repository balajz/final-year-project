---
tags:
  - research-log
  - adhd
---

# Session Log: 2026-11-15 — Analysis of Baibulova et al. (2026)

## New Literature Added
- [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] (*Computers*, May 2026).

## Key Insights & Takeaways
1. **Leak-Free Reality Check:** Realistic subject-level EEG classification for ADHD on the 121-child IEEE DataPort dataset is ~0.74–0.78 AUC-ROC (63%–72% accuracy), *not* the 93%–99% reported by window-split papers.
2. **Theta Dominance:** Band-limited Hilbert envelope connectivity in the theta band (4–8 Hz, AUC 0.7333) carries almost all the discriminative signal compared to beta (13–30 Hz, AUC 0.5667).
3. **Architectural Misnomer:** The paper's "Graph Transformer" actually operates on flattened 171-D upper-triangular edge vectors rather than explicit graph message passing.
4. **Screening vs. Diagnosis:** High sensitivity (80%) + low specificity (44.4%) means EEG connectivity alone behaves as a high-NPV screening/exclusion signal, not a standalone diagnostic tool.

## Concepts & Opportunities Created
- [[Dynamic-Functional-Connectivity]]
- [[Subject-Level-Evaluation-Hygiene]]
- [[Network-Index-Modeling]]
- [[ADHD-Event-Locked-Connectivity-and-Leakage]]

## Questions to Investigate Next
- How do recent EEG Foundation Models (e.g., LaBraM, BIOT, CBraMod) or true spatio-temporal GNNs perform under strict LOSO on this or larger cohorts?
- What multimodal or event-locked datasets exist where behavioral/physiological signals complement EEG's low specificity?
