---
tags:
  - technical-concept
  - eeg
  - connectivity
---

# Dynamic Functional Connectivity (dFC)

## Definition
Dynamic Functional Connectivity models brain functional coupling as a **time-varying sequence of graphs** $\{A_t\}_{t=1}^T$ over sliding windows, rather than collapsing an entire EEG recording into a single static correlation matrix $\bar{A}$.

## Why It Matters in Neuro-AI
- **Non-stationarity:** EEG signals are inherently non-stationary; cognitive states, attention lapses, and seizure transitions evolve over seconds.
- **Network Flexibility Hypothesis:** Conditions like ADHD are hypothesized to involve reduced network flexibility and restricted transitions across functional brain states (e.g., concentrating occupancy in a single dominant state, as observed in [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]).

## Common Estimation Methods
1. **Raw Amplitude Pearson Correlation:** Fast, but heavily vulnerable to volume conduction, spatial proximity, and high-amplitude artifacts.
2. **Hilbert Amplitude-Envelope Correlation (AEC):** Bandpass filters EEG into specific rhythms (e.g., theta 4–8 Hz, beta 13–30 Hz), extracts analytic amplitude envelopes via Hilbert transform, and correlates envelopes. More robust to phase jitter and raw spikes, though still affected by volume conduction unless orthogonalized.
3. **Phase-Locking Value (PLV) / Directed Transfer Entropy (DTE):** Captures phase synchronization or directional information flow.

## Open Limitations
- Window length ($L$) and overlap ($\Delta$) are typically chosen heuristically (e.g., 4 s windows, 50% overlap) without aligning to cognitive events or physiological state transitions.
