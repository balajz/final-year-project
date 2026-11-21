---
tags:
  - verification-result
  - mathematics
  - connectivity
  - spd
  - resolved
status: verified-resolved
created: 2026-11-16
resolves: R2
---

# R2 — RESOLVED: oAEC is not PSD; the fix is global Löwdin, not pairwise orthogonalisation

> **R2 is closed.** Trap 1 in [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] was
> **half right and half wrong**. The wrong half is now corrected in this vault, and a runtime
> guard has been written so the pipeline cannot silently break even if the wrong construction
> is used.
>
> This note is a **verified result**, not a pending risk. It may be cited.
> Reproduce with `scripts/r2_oaec_spd_test.py` and `scripts/spd_guard.py`.

---

## 1. The Claim That Was Tested

[[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] §6 Trap 1 asserted:

> "Because symmetric orthogonalization + Hilbert envelope correlation produces an actual Gram
> correlation matrix … the resulting volume-conduction-free connectivity matrix **remains
> strictly Positive Semi-Definite**."

The review ([[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] R2) objected: orthogonalised
AEC as implemented in real libraries is **pairwise and symmetrised by averaging** scalars — not a
Gram matrix — so the proof does not apply.

---

## 2. What the Test Did

Pure NumPy, no data download, ~12 seconds. 19 channels, 200 trials per condition, four synthetic
signal regimes with **known ground truth** (independent noise, single deep volume-conduction source,
multiple correlated sources, and windows shorter than the channel count). Two constructions compared
against a naive-AEC baseline:

- **Construction A — pairwise-symmetrised oAEC**: orthogonalise `j` w.r.t. `i`, and `i` w.r.t. `j`,
  then store `(|r_ij| + |r_ji|)/2`. This is what MNE-CPP `ConnectivityAec::computeOrthogonalized`
  and Brainstorm HENV implement.
- **Construction B — global Löwdin AEC**: orthogonalise **all channels jointly**
  (`X_perp = X (XᵀX)^{-1/2}`), *then* correlate envelopes. This is what Trap 1 actually describes.

---

## 3. The Result (measured)

**Negative-eigenvalue rate out of 200 windows:**

| Condition | Pairwise-sym oAEC | Global Löwdin AEC |
|---|---:|---:|
| Broadband, 2 sources | 0 / 200 | 0 / 200 |
| **Alpha band (8–13 Hz), 2 sources** | **87 / 200** | 0 / 200 |
| **Alpha band, 6 sources** | **63 / 200** | 0 / 200 |
| **Alpha band, 6 sources, low noise** | **156 / 200** | 0 / 200 |
| **Alpha band, 2 sources, n=256** | **83 / 200** | 0 / 200 |
| Short window, n_samp = 12 (19 ch) | 200 / 200 | 200 / 200 |
| Short window, n_samp = 24 | 173 / 200 | 0 / 200 |
| Short window, n_samp = 64 | 0 / 200 | 0 / 200 |

Worst observed minimum eigenvalue for pairwise-sym oAEC: **−0.93** on a 19×19 matrix.

### Two findings, both load-bearing

**F1 — Trap 1 is wrong about the construction it names.** Pairwise-symmetrised oAEC fails PSD in
**up to 78%** of band-limited windows. It is an average of pairwise scalars, so there is no Gram
structure to protect it. **It must never enter a Riemannian stage unrepaired.**

**F2 — Trap 1 is right about the construction it describes.** Global Löwdin AEC was PSD in
**every** adequately-sampled condition (0 failures out of 1,200 windows). It is a genuine
correlation matrix of real vectors, so PSD holds by construction, not by luck.

**F3 — The decisive trigger is band-limiting, not source structure.** Broadband signals pass;
alpha-band signals fail. Noise correlation is *actually* a correlation structure; band-limited
envelope correlation is not. This matters because **every** connectivity analysis in this project is
band-limited — so the failure regime is the one the project actually operates in.

**F4 — Both constructions fail when the window is shorter than the channel count**
(n_samp = 12 < 19 channels). This is the rank-deficiency case: a 19×19 matrix cannot have full
rank from 12 samples. With 4 s windows at 128 Hz (512 samples) this cannot occur, but it *would*
occur if anyone shortens the window to <150 ms. Log it as a hardware/config precondition.

---

## 4. The Fix (decided)

**Decision: use global Löwdin orthogonalisation, not pairwise orthogonalisation.**

```
X (19 × 512)                          # band-limited window
  └─ Löwdin: X_perp = X (XᵀX)^{-1/2}  # joint orthogonalisation across all channels
       └─ Hilbert envelope            # |analytic signal|
            └─ Pearson correlation    # → envelope correlation matrix
                                      # → PSD by construction
```

This is *also* the more defensible scientific choice, independent of the PSD issue: pairwise
orthogonalisation is **order-dependent and asymmetric** (Brainstorm's own docs note orthogonalised
AEC is not symmetric before the averaging step), whereas Löwdin is simultaneous across channels and
has no arbitrary ordering. The PSD property is a symptom of it being the mathematically correct
object; it is not the only reason to prefer it.

**Implementation:** `scripts/spd_guard.py` → `aec_global_lowdin()`.

---

## 5. The Safety Net (mandatory, regardless of construction)

Even with Löwdin, the pipeline must not trust the property blindly — because F4 shows a config
change (short window) breaks it, and because real data are messier than synthetic data.

`ensure_spd(M)` symmetrises, eigendecomposes, clips eigenvalues at `ε = 1e-6`, and **returns the
correction magnitude**. `spd_report()` aggregates it across a batch.

**Reporting rule (new commitment):** every run logs
`n_not_psd`, `frac_not_psd`, `min_eig_raw`, and `mean/max_correction`. A large correction is a
**data-quality signal** — the connectivity estimate for that window is unreliable — not something to
silently repair. This is the same epistemic move as the per-group attrition table
([[Decision-Log]] 16): make the repair visible instead of hiding it.

---

## 6. What Changes in the Vault

| File | Change |
|---|---|
| [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] §6 Trap 1 | Corrected: the PSD claim holds **only** for globally-orthogonalised AEC; pairwise-symmetrised oAEC must be repaired or replaced |
| [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] §3 Stage 2 | Stage 2 now specifies **joint** Löwdin orthogonalisation, and names the library-default construction as a trap |
| [[Candidate-C5-Reliability-Screening-Workbench]] | Reliability panel must log the SPD correction statistics |
| [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] | R2 moved from *pending* to *resolved* |

---

## 7. What This Does Not Settle

- It does not test on **real** EEG. The verification is on synthetic signals with known structure,
  which is stronger for a *mathematical* property (PSD is a property of the construction, not of the
  data) but must still be confirmed on the 121-child cohort before publication. Run
  `spd_report()` on 100 real windows and record the numbers; expected: Löwdin at 0% failure.
- It does not decide whether Löwdin *improves classification*. That is a different experiment, and it
  belongs in the 5-step ablation ladder as its own rung.
- It says nothing about wPLI, which is also not PSD by construction and must pass the same guard.

---

## 8. Connections
- [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] (parent register — R2 now closed)
- [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] (the note corrected)
- [[Candidate-C5-Reliability-Screening-Workbench]] (where the guard is reported to the user)
- [[Dynamic-Functional-Connectivity]] · [[Kernel-Matrix-Based-Transfer-Entropy]]
- Scripts: `scripts/r2_oaec_spd_test.py`, `scripts/spd_guard.py`
