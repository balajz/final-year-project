---
tags:
  - technical-concept
  - biomarker
  - decision-support
---

# Network Index Modeling

## Concept
Instead of outputting only a discrete class label $\hat{y} \in \{0, 1\}$, **Network Index Modeling** learns a continuous scalar score $s = f_\theta(\{A_t\}_{t=1}^T) \in \mathbb{R}$ (typically the pre-sigmoid logit under binary cross-entropy) that quantifies the degree of deviation in brain network organization.

## Potential Value
- Enables continuous severity/risk stratification, statistical effect-size analysis (Cohen's $d$, distribution overlap), and threshold tuning for screening (high sensitivity / high NPV) vs. confirmatory use.
- Bridges complex spatio-temporal deep models with interpretable clinical decision-support indicators.

## Limitations Observed in [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]
- Without clinical symptom scores (e.g., Conners or ADHD-RS severity ratings) as regression targets, a logit trained solely on binary labels is only a **proxy** for deviation—it does not guarantee monotonic alignment with clinical severity.
- Significant distribution overlap (0.45–0.72) limits standalone diagnostic utility.
