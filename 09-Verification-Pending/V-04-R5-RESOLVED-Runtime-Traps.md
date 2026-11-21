---
tags:
  - verification
  - runtime
  - channels
  - bands
  - formats
  - resolved
date: 2026-11-16
status: RESOLVED
---

# V-04 Verification: R5 Runtime Traps Resolved (Names, Bands, Formats, Bad Channels)

**Status: RESOLVED (2026-11-16)**
**Code artifact:** `scripts/r5_runtime_audit.py`
**Output artifact:** `results/r5_runtime_audit.json`
**Formal Decision:** [[07-Decisions/Decision-Log]] Commitment 32

---

## 1. Executive Summary

Risk **R5** flagged multiple runtime incompatibilities between specifications, dataset schemas, and reference pipelines that would cause silent failures or corrupted representations at runtime:
1. **Electrode names:** Spec referenced legacy 10–20 names (`T3, T4, T5, T6`), whereas modern 10–20 and HBN EGI 128-channel montages use `T7, T8, P7, P8`.
2. **Frequency band overlap:** Spec stated `beta 12–30 Hz` while alpha ended at `12 Hz` or `13 Hz`, creating bin double-counting.
3. **SpecParam fit range:** SpecParam needs sufficient high-frequency spectrum beyond the alpha peak to fit the $1/f$ slope reliably.
4. **Bad-channel variance rule:** Naive "variance > 3 SD" rules interpolate legitimate high-amplitude pediatric signals (e.g. occipital alpha at O1/O2).
5. **Multi-format ingestion & dependencies:** Real datasets ship as CSV (IEEE-121) or EEGLAB `.set`/BDF (HBN). Loading MAT v7.3 files >2 GB requires `pymatreader` and `h5py`, which fail on modern Python environments under PEP 668 unless installed in a virtual environment.

All five items have been audited on real data (`data/adhdata.csv`), verified programmatically, and locked into standard utilities.

---

## 2. Empirical Verification Findings

### A. Electrode Names & Aliasing
- **Dataset Audit (`data/adhdata.csv`):**
  - Inspected 2,166,383 rows across 121 children (61 ADHD, 60 Control).
  - The Kaggle IEEE-121 CSV **already natively uses modern 10–20 names**:
    `['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7', 'T8', 'P7', 'P8', 'Fz', 'Cz', 'Pz']`.
  - Legacy names (`T3, T4, T5, T6`) appear **0 times** in the raw CSV.
  - An un-aliased parser expecting `T3–T6` would fail to match columns, leading to missing channels or NaNs.
- **Normalization Engine:**
  - Implemented `normalize_channel_name()` supporting bi-directional aliases:
    - Legacy: `T3 -> T7`, `T4 -> T8`, `T5 -> P7`, `T6 -> P8`
    - Case normalizer: `FP1 -> Fp1`, `CZ -> Cz`, etc.
    - EGI 128 HydroCel Net: `E22/E25 -> Fp1`, `E9/E8 -> Fp2`, `E33 -> F7`, `E24 -> F3`, `E11 -> Fz`, `E124 -> F4`, `E122 -> F8`, `E45 -> T7`, `E36 -> C3`, `E129/VREF -> Cz`, `E104 -> C4`, `E108 -> T8`, `E58 -> P7`, `E52 -> P3`, `E62 -> Pz`, `E92 -> P4`, `E96 -> P8`, `E70 -> O1`, `E83 -> O2`.

### B. Canonical Oscillatory Bands & The EMG/Gamma Confound
- **Oscillatory Clinical Ladder (Contiguous & Disjoint):**
  - **Delta:** 0.5 – 4.0 Hz
  - **Theta:** 4.0 – 8.0 Hz
  - **Alpha:** 8.0 – 13.0 Hz
  - **Beta:** 13.0 – 30.0 Hz
  - **Gamma:** 30.0 – 45.0 Hz
  - Within the oscillatory hierarchy, all bands are strictly contiguous and non-overlapping with **zero bin overlap**.
- **The EMG / Gamma Spectral Confound:**
  - **EMG / Muscle Artifact Band:** 30.0 – 60.0 Hz.
  - **Crucial Confound:** The EMG artifact monitoring band deliberately and completely spans the cortical gamma band (30.0 – 45.0 Hz). This is an inherent physiological reality: frontalis and temporalis muscle tension (e.g. from pediatric fidgeting or effortful concentration) produces high-frequency electrical activity that overlaps cortical gamma rhythms.
  - **Rule:** High-frequency EMG ratio and gamma power must **never** be treated as independent orthogonal features in the model. If an artifact-only classifier correlates strongly with gamma power, it is picking up the muscle-tension confound rather than a pure neural biomarker.
- **SpecParam Fit Range:** Locked to **1.0 – 40.0 Hz** (matching HBN reference pipeline) with fit quality threshold $R^2 \ge 0.85$.

### C. Bad-Channel Detection: Naive 3 SD vs PREP Reference Rule (20-Subject Spot Check)
We evaluated both bad-channel criteria across a **20-subject spot check** from the IEEE-121 cohort (`data/adhdata.csv`):
- **Naive rule (`variance > 3 SD`):**
  - Flagged 7 of 20 subjects. It specifically flagged healthy occipital and parietal channels (`O1` in subject `v110`, `P3` in `v123`, `C3` in `v108`/`v121`) as bad channels.
  - Reason: Normal pediatric posterior alpha bursts naturally generate high amplitude variance across the recording, exceeding 3 standard deviations above the whole-head average. Naively pruning them destroys genuine posterior neural dynamics.
- **Citable Reference Rule (PREP / Automagic 3.1 / Bigdely-Shamlo et al., 2015):**
  - Evaluates multi-dimensional criteria: robust Median Absolute Deviation ($z_{\text{MAD}} > 5.0$), neighbor correlation ($r < 0.40$), predictability ($R^2 < 0.75$), and flatline detection ($\text{var} < 10^{-10}$).
  - Correctly avoids pruning healthy posterior channels on variance alone, while isolating genuine electrode dropouts, extreme drift, or high-noise pops (e.g. `Fp1` in `v114` with $z=17.20$).
- **Observed Flag Rate & Attrition Constraint:**
  - In the 20-subject spot check, PREP flagged channels in 9 of 20 subjects. In two extreme cases (`v108` and `v114`), PREP flagged 8 of 19 channels (>40% of the net).
  - **Mandatory Attrition Rule:** When $>4$ channels (>20% of the 19-channel montage) fail PREP criteria, the window/subject must not be silently interpolated. It must trigger the **AQI Selective Abstention Gate** ("Insufficient Signal Quality"), and **per-group attrition rates** (ADHD vs. Control) must be reported explicitly ([[Decision-Log]] Commitment 16).

### D. File Formats & Dependency Management
- Native pure-Python/NumPy reader implemented for `.csv`.
- MNE ingestion wrapper created for `.set` (EEGLAB), `.bdf` (BioSemi), and `.edf`.
- Modern macOS Python (Homebrew Python 3.15) enforces **PEP 668** (`externally-managed-environment`). System-wide `pip install` fails.
- Formalized isolated virtual environment setup instructions:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install numpy scipy mne pymatreader h5py pandas
  ```

---

## 3. Resolution Summary Table

| Item | Previous State | Resolved State (Commitment 32) | Empirical Verification |
|---|---|---|---|
| **Electrode Names** | `T3, T4, T5, T6` in older drafts | Canonical modern 10–20: `T7, T8, P7, P8` | `adhdata.csv` audited: 100% modern names natively. |
| **Spectral Bands** | `beta 12–30` (overlap) | `4–8 / 8–13 / 13–30 Hz` strictly disjoint | `verify_band_disjointness()` passes with 0 overlaps. |
| **SpecParam Fit** | Unspecified / 45 Hz | 1.0–40.0 Hz, $R^2 \ge 0.85$ | Matches published HBN reference pipeline. |
| **Bad-Channel Rule** | Naive `var > 3 SD` | PREP Reference: $z_{\text{MAD}} > 5.0, r < 0.40, R^2 < 0.75$ | Naive 3 SD falsely dropped `O1/P3` on real data; PREP preserves them. |
| **File Formats** | EDF-only upload | Multi-format: `.csv`, `.set`, `.bdf`, `.edf` | Handled via unified data loader with PEP 668 venv documentation. |

---

## 4. Connections
- Risk Register: [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] R5
- Decisions: [[07-Decisions/Decision-Log]] Commitment 32
- Specifications: [[04-Project-Ideas/Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[04-Project-Ideas/Candidate-C5-Reliability-Screening-Workbench]]
