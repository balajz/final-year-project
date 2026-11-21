# scripts/ — runnable verification checks

These are the **cheap decisive tests** named in the vault. Each runs in seconds on a laptop with
only NumPy. They exist so that a claim in the knowledge base can be *checked* rather than trusted.

| Script | Checks | Vault note | Runtime |
|---|---|---|---|
| `r2_oaec_spd_test.py` | Is orthogonalised envelope correlation PSD? Compares pairwise-symmetrised oAEC vs global Löwdin AEC across 4 signal regimes, 200 trials each | `09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD.md` | ~12 s |
| `spd_guard.py` | Production helper + self-check: `aec_global_lowdin()`, `ensure_spd()`, `spd_report()` | same | <1 s |
| `r3_alignment_ablation.py` | **Alignment-signal ablation**: does Riemannian per-subject alignment raise specificity without destroying AUROC? 4 arms, participant-level CV | `09-Verification-Pending/V-03-R3-Alignment-Harness.md` | ~5 s synthetic; ~47 s on real IEEE-121 |
| `r3_harness_selftest.py` | Structural self-test for the R3 harness | same | ~3 s |
| `r3b_permutation_test.py` | Permutation null over cached features (200 permutations) to assess split noise and significance | same | ~10–15 min |
| `r4_artifact_only.py` | Standalone evaluation of non-neural artifact classifier (EMG, blinks, duration, variance) and EMG/gamma correlation | `09-Verification-Pending/V-03-R3-Alignment-Harness.md` | ~7 s |
| `r5_runtime_audit.py` | **R5 Runtime Traps Verification**: Audits CSV schema, modern channel aliases, band disjointness, bad-channel rules (naive vs PREP), format dependencies | `09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps.md` | ~4 s |
| `data_loader.py` | Unified multi-format EEG loader (`.csv`, `.set`, `.bdf`, `.edf`, `.fif`) with automatic 10-20 canonicalization and PEP 668 venv diagnostics | same | <1 s |

## Requirements

Python 3.10+ and NumPy only. No scipy, MNE, sklearn required.

```bash
brew install python3      # or use your existing python3
python3 -m pip install numpy
```

## Run

```bash
python3 scripts/r2_oaec_spd_test.py    # full verification, prints the PSD table + verdict
python3 scripts/spd_guard.py           # smoke test of the guard module
python3 scripts/r3_harness_selftest.py # structural check of the R3 harness
python3 scripts/r3_alignment_ablation.py --synthetic          # logic check, no data needed
python3 scripts/r3_alignment_ablation.py --csv data/adhdata.csv --out results/r3_ieee121.json # REAL IEEE-121 run
python3 scripts/r5_runtime_audit.py            # R5 runtime traps audit and verification
python3 scripts/data_loader.py                 # Smoke test multi-format loader on IEEE-121
```

## Result recorded (2026-11-16)

- **R2 (oAEC PSD):** Pairwise-symmetrised oAEC (MNE-CPP / Brainstorm default) produced negative eigenvalues in up to 156/200 band-limited windows (worst min-eig = −0.93). Global Löwdin AEC produced 0 failures in 1,200 windows. Decision: use global Löwdin + `ensure_spd()`.
- **R3 (Riemannian Alignment Ablation on Real Data):** Tested on `data/adhdata.csv` (121 children, 8,279 windows). `none` = 0.9055 AUROC, `euclid` = 0.8109, `riemann` = 0.7995, `riemann_band` = 0.7667. Every alignment arm degrades performance (Trap 2 confirmed). Decision: Lock Dual-Path Trait + State Decomposition (Commitment 31).
- **R3b (Permutation Significance Null):** 200 label permutations on unaligned features yielded null mean AUROC = 0.4877 ± 0.0669 (95th pct = 0.5963, max = 0.6658) vs. real 0.9081 ± 0.0089 ($p = 0.0050$, 0/200 null runs reached real). The classification signal is genuine and statistically significant.
- **R5 (Runtime Traps Resolved):**
  - Confirmed `data/adhdata.csv` natively uses modern names (`T7, T8, P7, P8`). Built canonical aliasing normalizer for legacy 10-20 and EGI 128 nets.
  - Confirmed 100% disjoint frequency bands (`4–8, 8–13, 13–30 Hz`) and SpecParam 1–40 Hz fit standard ($R^2 \ge 0.85$).
  - Tested bad-channel rules on real EEG: naive 3 SD falsely drops occipital alpha (`O1`, `O2`), whereas PREP reference rule (`z > 5 MAD, r < 0.40, R^2 < 0.75`) correctly preserves physiological dynamics.
  - Delivered unified multi-format ingestion engine `scripts/data_loader.py` with PEP 668 venv compliance. (Commitment 32).
