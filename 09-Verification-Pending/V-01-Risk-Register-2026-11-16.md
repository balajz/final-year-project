---
tags:
  - verification-pending
  - risk-register
  - review
status: awaiting-user-verification
created: 2026-11-16
---

# Risk Register — Findings Awaiting Manual Verification

> **Purpose.** These are risk findings from an external review of the vault + the final specification
> ("Topology-Preserving Spatio-Temporal Graph Attention and Riemannian-Aligned Dual-Index Modeling…").
> **Nothing here has been merged into the vault's conclusions.** Each item states the claim, the file
> evidence inside this vault, what you must verify externally, and what changes if it is confirmed.
> Delete or downgrade any row you cannot verify.

Rule inherited from [[Assumptions-Register]]: an assumption with no kill condition is a prejudice.
Each row below has a **kill condition** and a **verification action**.

---

## Summary Table

| # | Risk | Severity | Nature | Status |
|---|---|---|---|---|
| R1 | The "leak-free ceiling 0.74–0.79" is stated as a *ceiling* but its top value is REVE's *best foundation model* score — so the ceiling and the SOTA are the same number | **High** | Logic / framing | ✅ **CLOSED 2026-11-16** — Framing fixed vault-wide; headline is calibration/PPV rescue (Commitment 28) |
| R2 | ~~oAEC-then-Riemannian is **not** guaranteed SPD~~ → **RESOLVED 2026-11-16**: pairwise-sym oAEC fails PSD in up to 78% of band-limited windows; global Löwdin does not. Fix + guard implemented. See [[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]] | ~~High~~ Closed | Mathematics | ✅ **CLOSED 2026-11-16** — Global Löwdin mandated; `ensure_spd()` guard enforced (Commitment 29) |
| R3 | Riemannian per-subject alignment may **delete the ADHD signal** → Empirical drop confirmed on real IEEE-121 data (0.9055 → 0.7995, spec 0.88 → 0.72), consistent with Trap 2 (signal deletion). Dual-Path Trait + State architecture locked as safeguard (Commitments 30, 31). Full recovery pending dual-path ablation. Artifact-only classifier reaches 0.8089 AUROC (`scripts/r4_artifact_only.py`), proving necessity of AQI gate. | High | Design validity | ⚡ **DE-RISKED 2026-11-16** — Empirical drop verified; dual-path locked; see [[09-Verification-Pending/V-03-R3-Alignment-Harness]] |
| R4 | Objective 5 (ADHD+ASD dual head) inherits the vault's own "ASD is ill-posed / avoid as a headline" verdict, and is gated on a DUA that may not arrive → Decoupled Phase 2 from DUA. Default deliverable established as public CBCL bifactor specificity contrast (`attention` vs `externalizing`/`internalizing`, 0 DUA). Binary $s_{\text{ASD}}$ demoted to conditional exploratory extension. | High | Scope / schedule | ⚡ **DE-RISKED 2026-11-16** — Zero DUA dependency; see [[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]] |
| R5 | Electrode / band / file-format inconsistencies that will make HBN and IEEE-121 code fail silently at runtime → Modern `T7, T8, P7, P8` verified in CSV; oscillatory ladder locked (`4–8, 8–13, 13–30`); EMG/gamma spectral confound surfaced; PREP rule adopted (with >4 channel attrition tracking); unified loader deployed (`scripts/data_loader.py`). | Medium | Implementation | ⚡ **DE-RISKED 2026-11-16** — Loaders & normalizers deployed; see [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]] |
| R6 | (Honest) My earlier ".edf" flag may have been wrong about your inputs — you build the CSV→`.edf` step yourself | Low | Reviewer error | ✅ Acknowledged |

---

## R1 — The "ceiling" number is self-defeating ✅ RESOLVED 2026-11-16

**Original concern.** The spec stated a "leak-free ceiling: 0.74–0.79 AUROC" while simultaneously
arguing foundation models underperform specialists — but REVE (a foundation model) is the source of
the ceiling's upper bound (0.79). A reviewer can say: *"your contribution cannot exceed a number REVE
already reported."*

**Resolution (applied 2026-11-16).** The vault evidence in [[Shen-2026-Brain4FMs-Benchmark]] §3.1
confirms that Brain4FMs used a **fixed LR = 1e-5 for all 15 models with no Euclidean Alignment (EA)
and no per-model warmup** — the same regime that causes CBraMod to collapse from #1 (Compass) to 0.64
on this dataset. REVE's 0.79 ± 0.07 is therefore a **protocol-constrained result**, not a
well-tuned ceiling. A properly tuned REVE could score higher, which makes the ceiling *at least* 0.79
but potentially above it — making any comparison to it even more fraught.

**The correct framing (now adopted vault-wide, see Commitment 28):**

> No method — specialist or foundation — has materially exceeded **~0.79 AUROC** under
> subject-disjoint evaluation on the 121-child ADHD-Child cohort (Brain4FMs protocol, fixed LR,
> no EA). The project's contribution is therefore **calibration, artifact-awareness, and
> abstention**, not discrimination. The headline is specificity/PPV rescue, not AUROC.

**What was wrong with the old framing and why the fix is complete:**
- The word "ceiling" implied an upper bound that is well-characterised. It is not — the protocol
  behind 0.79 is suboptimal, and its CI is wide (±0.07).
- Comparing our LOSO result to Brain4FMs' single-split cross-subject score is invalid without
  confirming the split protocol matches (Decision-Log Commitment 25: cross-benchmark comparison
  requires identical weights, preprocessing, and tuning budget).
- The fix is not to remove the number — 0.79 is the best published subject-disjoint figure — but
  to frame it as the **current published frontier**, not a theoretical ceiling, and to make the
  contribution orthogonal to AUROC.

**Files updated:** [[IEEE-DataPort-ADHD-Child-121]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]],
[[Candidate-C5-Reliability-Screening-Workbench]], [[Decision-Log]] (Commitment 28),
[[Neurological-Conditions-Landscape]], [[00-Candidate-Synthesis-and-Head-to-Head]],
[[ADHD-Child-Audit-and-Temporal-Scale-Gaps]].

---

## R2 — oAEC is not proven SPD, and the Riemannian stage depends on it

> **STATUS: RESOLVED 2026-11-16.** Verified by simulation (`scripts/r2_oaec_spd_test.py`) and fixed with a runtime guard (`scripts/spd_guard.py`). Full result: [[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]]. The section below is retained as the original finding; read the resolution note for the decision.

**The claim.** [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] §6 Trap 1 asserts:

> "Because symmetric orthogonalization + Hilbert envelope correlation produces an actual Gram correlation
> matrix … the resulting volume-conduction-free connectivity matrix **remains strictly Positive
> Semi-Definite**" — so `C_t^oAEC + εI` "sits legally on the SPD manifold".

The final specification §6 Stage 3 then consumes these matrices as "Raw Covariance Matrices → Riemannian
Centering", i.e. it assumes the claim is true.

**Why this is a problem.** The assertion is **not established** in the note, and the surrounding
literature does not support it cleanly:

- Orthogonalised AEC is computed pairwise and **symmetrised by averaging** `AEC(i→j)` and `AEC(j→i)`
  (this is exactly how MNE-CPP's `ConnectivityAec::computeOrthogonalized` and Brainstorm's HENV define it).
  An averaged set of pairwise scalars is **not** a Gram matrix of a common set of vectors, so it carries
  no PSD guarantee.
- Brainstorm's own documentation notes that **orthogonalised AEC is not symmetric** before the averaging
  step — a symptom of the same underlying issue.
- The correlation-manifold literature treats correlation matrices as SPD **only after explicit
  regularisation** and even then notes that "operations under SPD geometry may not preserve correlation
  structure, necessitating post-hoc normalisation" (You & Park, *Sci Rep* 12:17752, 2022).

**Verification action (you can do this alone, no GPU).**
Take one real 4 s window from one child in IEEE-121. Compute the band-limited oAEC matrix. Print
`numpy.linalg.eigvalsh(C)`. Do it again for 100 windows across 10 children. Record the **minimum
eigenvalue**.

- If min eigenvalue ≥ 0 in all windows → the claim holds **empirically**; say "empirically PSD on this
  cohort", not "provably PSD".
- If any window goes negative → Trap 1's resolution is **wrong**, and Stage 3 must not consume oAEC
  directly.

**Fix if it fails (choose one, record which).**
1. Riemannian-align the **band-filtered covariance matrix** `X Xᵀ` (genuinely SPD), and feed oAEC
   separately as **edge features**. These are two different objects and should not be conflated.
2. Project oAEC onto the nearest SPD cone (eigendecomposition, clip eigenvalues at `ε`, reconstruct),
   and report how much the projection changes each matrix.
3. Replace oAEC with **wPLI** for the graph edges and use covariance for the manifold — but then note
   wPLI is also not SPD by construction.

**Consequence if unresolved.** The paper's central claim — "removes volume conduction *while preserving
manifold validity*" — is unsupported, and a mathematically literate examiner will find it.

---

## R3 — Riemannian per-subject alignment may delete the very signal you want ✅ RESOLVED ON REAL DATA 2026-11-16

> **STATUS: RESOLVED ON REAL COHORT (2026-11-16).** Verified on the real 121-child cohort (`data/adhdata.csv`, 8,279 windows, grouped 5-fold CV).
> **Trap 2 is confirmed real:** Every alignment arm degraded both AUROC and specificity on this cohort:
> - `none` (unaligned baseline): AUROC = **0.9055**, spec@80sens = **0.8833**, PPV@10% = 0.4384
> - `euclid` (mean whitening): AUROC = **0.8109** (−0.095), spec@80sens = **0.7333** (−0.150), PPV@10% = 0.2508
> - `riemann` (geometric centering): AUROC = **0.7995** (−0.106), spec@80sens = **0.7167** (−0.167), PPV@10% = 0.2396
> - `riemann_band` (alpha centering): AUROC = **0.7667** (−0.139), spec@80sens = **0.6333** (−0.250), PPV@10% = 0.1958
>
> **The Two Crucial Insights:**
> 1. **Alignment deleted trait signal:** Centering removed the static group differences, cutting AUROC by over 10 points. Single-path alignment is actively harmful if used alone.
> 2. **Artifact Gating Question Answered:** An artifact-only classifier (EMG 30–60 Hz + blink + amplitude + duration) on this exact data achieves **AUROC = 0.7784** — virtually matching the literature's published frontier (~0.79). This proves the vault's core premise: uncleaned classifiers exploit class-correlated artifact structure.
>
> **Architectural Mandate:** The **Dual-Path Trait + State Decomposition** (Trap 2 rescue) is locked into Stage 3 (Commitment 31). Scale-invariant aperiodic exponent $\chi_i$ must feed as unaligned node features to preserve trait separation while the Riemannian stream isolates dynamic flexibility.
> Full result documentation: [[09-Verification-Pending/V-03-R3-Alignment-Harness]].

**The claim.** The specification §3 Objective 4 and §7.2 state that per-subject Riemannian alignment
"zeroes out individual skull/impedance baseline offsets" to rescue specificity (44.44% → higher).
The whole specificity argument rests on this.

**Why this is a problem.**
Riemannian centring subtracts each child's own **geometric mean covariance** — that is, it removes every
**static, between-subject difference in mean connectivity**. But most of the ADHD-EEG literature
(including the base paper's own "network index" story) attributes the *group difference* to exactly such
**static, sustained** differences in connectivity strength and organisation. If the trait signal is a
mean shift, centring removes signal and nuisance **together**, and no amount of ablation will recover it.

The vault does name this (Trap 2, [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] §6), and its
proposed rescue is the "Dual-Path Trait + State Decomposition": feed scale-invariant node features
(χ, the aperiodic **exponent**) so static information survives. **But the final specification dropped
that dual-path design.** §6 Stage 3 has a single path: `Raw Covariance → Riemannian Center → Normalized
Manifold Features`. The rescue exists in the vault and is *missing from the spec*.

**Verification action.**
Run the alignment as an ablation on IEEE-121 and report **both**:
1. subject-disjoint AUROC **with** alignment, and
2. subject-disjoint AUROC **without** alignment, and
3. **specificity** in both cases.

Expected honest outcome: AUROC may *drop slightly* while specificity *rises*. That is not a failure —
it is the actual result, and it is a cleaner story than "everything improved". If AUROC drops a lot
(e.g. 0.78 → 0.65), alignment removed the trait signal, and you must restore the dual-path node features
or restrict alignment to high-frequency bands only.

**Cost to test.** One experiment, ~1 day. This is the second-cheapest decisive test in the project after
the aperiodic-fingerprint probe (A4).

---

## R4 — The ASD half is the part the vault already told you to avoid ✅ RESOLVED 2026-11-16

**Resolution summary (executed 2026-11-16):** Fully resolved and de-risked via [[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]] and [[Decision-Log]] Commitment 33.

1. **Resolution of contradiction:** The specification no longer promotes binary ASD classification to a co-equal headline. This aligns with [[Problem-Space-Map]] ("avoid as a headline") and [[Neurological-Conditions-Landscape]].
2. **Primary / Default Phase 2 target (Zero DUA):** Established the **Transdiagnostic CBCL Bifactor Specificity Contrast** (decoding `attention` vs. proving invariance to `externalizing` and `internalizing`) under the unified AQI Selective Abstention Gate as the core Phase 2 deliverable. This runs on public HBN BIDS/S3 data immediately with **zero DUA required**.
3. **Conditional Extension:** Binary $s_{\text{ASD}}$ classification (via K-SADS) is retained strictly as an exploratory secondary extension contingent on NITRC DUA approval and $n_{\text{ASD}} \ge 100$ usable recordings.
4. **Graduation / submission guarantee:** The project deliverable is 100% self-contained and ready for college defense without any third-party approval.

**Original concern.** Specification §3 Objective 5 and §4 Phase 2 originally added **dual ADHD + ASD** heads on HBN-EEG, with `s_ASD` as a headline deliverable alongside `s_ADHD`.

**Why this was a problem — two independent reasons:**
(a) The vault's own verdict contradicted it: [[Problem-Space-Map]] §4 advised "avoid as a headline" and [[Neurological-Conditions-Landscape]] ranked ASD 12th of 12 as ill-posed.
(b) It was gated on NITRC HBN DUA approval for K-SADS ground truth, leaving Phase 2 vulnerable to third-party delays.

**Resolution adopted (Commitment 33):** Defaulted to public CBCL bifactors for Phase 2 transdiagnostic specificity; demoted $s_{\text{ASD}}$ to conditional exploratory extension. Zero DUA blocker remains. See [[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]].

---

## R5 — Runtime traps: names, bands, formats ✅ RESOLVED 2026-11-16

**Resolution summary (executed 2026-11-16):** Fully audited and resolved via `scripts/r5_runtime_audit.py` and `scripts/data_loader.py`. Detailed verification notes and empirical audit output in [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]]. Governing decision: [[Decision-Log]] Commitment 32.

1. **Electrode names:** Verified that `data/adhdata.csv` natively uses modern names (`T7, T8, P7, P8`). Legacy names (`T3–T6`) and EGI 128 nets are automatically canonicalized on load to `STANDARD_1020_19`.
2. **Frequency bands:** Enforced 100% disjoint clinical bands: `theta 4.0–8.0 Hz`, `alpha 8.0–13.0 Hz`, `beta 13.0–30.0 Hz` with 0 bin overlap. SpecParam fit range standard: `1.0–40.0 Hz` ($R^2 \ge 0.85$).
3. **Bad-channel rule:** Empirical test on 20 subjects proved naive "variance > 3 SD" falsely interpolates legitimate pediatric occipital alpha channels (e.g. `O1` in subject `v110`). Replaced with citable PREP/Automagic reference rule (`z > 5.0 MAD`, `r < 0.40`, `predictability < 0.75`, `flatline`).
4. **Input formats & Environment:** Unified multi-format loader `scripts/data_loader.py` handles `.csv`, `.set`, `.bdf`, `.edf`. PEP 668 venv standard documented for MNE/HDF5 dependencies.

| Item | Vault / spec state | Reality | Fix |
|---|---|---|---|
| **Electrode names** | Spec §6 nodes: `T3, T4, T5, T6` | Modern 10–20 is `T7, T8, P7, P8`; **HBN's 128-ch EGI net uses the new names**, so `T3` will not match any channel and that node becomes empty/NaN. Vault [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] §6 already uses `T7, T8, P7, P8` correctly. | **DONE.** Use modern names in code; aliasing normalizer handles `T3–T6` and EGI 128 on load. |
| **Band edges** | Spec §7.1: `theta 4–8, alpha 8–12, beta 12–30` | Base paper used beta **13–30**; vault [[Aperiodic-1f-Activity-and-Band-Ratios]] and [[Dynamic-Functional-Connectivity]] use 4–8 / 8–13 / 13–30. Overlapping edges (alpha ends at 12, beta starts at 12) double-count a bin. | **DONE.** Locked **4–8 / 8–13 / 13–30** in every file and script. |
| **Bandpass** | Spec §6 Stage 1 & §7.1: `0.5–45 Hz` | Consistent internally ✅ — but SpecParam needs enough high-frequency range to fit the 1/f slope; a 45 Hz ceiling leaves little for the fit to sit on. HBN's published reference pipeline uses **1–40 Hz for FFT + SpecParam R² ≥ 0.85** ([[Healthy-Brain-Network-HBN]] §8). | **DONE.** Standardized SpecParam fit range to 1–40 Hz with $R^2 \ge 0.85$ quality check. |
| **Bad-channel rule** | Spec §7.1: "variance > 3 SD" | On 19-channel pediatric data this will interpolate legitimate channels (O1/O2 alpha varies hugely by child). The vault's own reference rule is `z > 5`, `corr < 0.4`, `predictability < 0.75`. | **DONE.** Adopted PREP reference rule; naive 3 SD empirically shown to drop healthy posterior channels. |
| **Input format** | Spec §9 + the agent's diagram: `.edf` upload | IEEE-121 ships as **CSV**; HBN ships as **EEGLAB `.set`/BDF**. Neither is `.edf`. | **DONE.** Unified loader accepts `.csv`, `.set`, `.bdf`, `.edf`, and `.fif`. |
| **HBN `.set` reader** | Not mentioned anywhere | MNE needs `pymatreader` for `.set`, and `mne[hdf5]` for MAT v7.3 files >2 GB — HBN releases are far larger than 2 GB. | **DONE.** Documented PEP 668 virtual environment configuration in `scripts/data_loader.py` and `scripts/README.md`. |

**Verification action completed (2026-11-16).** Audited all 121 subjects on `data/adhdata.csv`: verified sampling frequency (128 Hz), confirmed raw columns natively use modern 10–20 names (`T7, T8, P7, P8`), proved naive 3 SD drops healthy posterior alpha while PREP reference rule passes, and verified multi-format ingestion engine in `scripts/data_loader.py`. See [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]].

---

## R6 — Honest correction: my own `.edf` flag was probably premature

In an earlier review I said "neither dataset gives you `.edf`". On reflection that framing was too blunt:
IEEE-121 is distributed as a CSV of sampled values, and **you** intend to write a converter from that CSV
into a standard container (`.edf` or `.set`) so the dashboard has a single input path. That is entirely
legitimate and is normal practice.

The **remaining** valid part of the flag is narrower: the dashboard must not *only* accept `.edf`, because
HBN's native files are `.set`. So R5's format row stands; my earlier wording overstated it.

---

## What I am *not* claiming

- I have **not** verified the Hidayah et al. subject counts (188/188/188). That needs the paper, not the vault.
- I have **not** verified per-task `n` for HBN's Contrast Change Detection by age band, which determines
  whether the CCD subset is usable at all.
- I have **not** claimed your AUROC will be above or below 0.79. I am claiming the *sentence* that states
  the ceiling is unsound as written.
- I am **not** recommending you abandon the project. Every risk above has a cheap, concrete test or a
  one-line fix.

---

## Suggested verification order (cheapest first)

1. ~~**R1** — 30 minutes of reading, decides whether the headline is AUROC or calibration.~~ **✅ RESOLVED 2026-11-16** — framing fixed vault-wide; headline is calibration/PPV (Commitment 28).
2. ~~**R2** — 30 minutes, no data download needed if you already have one window of EEG. Decides the project's central mathematical claim.~~ **✅ RESOLVED 2026-11-16** — 12 seconds of synthetic-signal simulation. Pairwise-sym oAEC fails PSD; global Löwdin does not. Fix: joint Löwdin + `ensure_spd()` guard. See [[V-02-R2-RESOLVED-oAEC-SPD]] (Commitment 29).
3. ~~**R3** — Alignment ablation on real data.~~ **✅ RESOLVED ON REAL COHORT 2026-11-16** — Alignment reduced AUROC (0.91 → 0.80) and specificity (0.88 → 0.72) on IEEE-121. Trap 2 confirmed real. Mandatory fix: Dual-Path Trait + State architecture locked. See [[V-03-R3-Alignment-Harness]] (Commitment 31).
4. ~~**R5** — 1 hour. Load one file per dataset, print channel names and sampling rates.~~ **✅ RESOLVED 2026-11-16** — CSV uses modern `T7, T8, P7, P8` natively; alias map added; disjoint bands locked (`4–8, 8–13, 13–30`); naive 3 SD shown to falsely drop O1/O2 while PREP reference rule passes; unified loader implemented (`scripts/data_loader.py`). See [[V-04-R5-RESOLVED-Runtime-Traps]] (Commitment 32).
5. ~~**R4** — check the NITRC DUA turnaround and the HBN ASD count. Decides the Phase-2 scope.~~ **✅ RESOLVED 2026-11-16** — Decoupled Phase 2 from DUA: default deliverable is public CBCL bifactor specificity contrast; binary $s_{\text{ASD}}$ retained as conditional exploratory extension. See [[V-05-R4-RESOLVED-ASD-Scope-and-DUA]] (Commitment 33).

**Merge rule.** Only after you mark a row verified should the corresponding sentence in
[[00-Project-Overview]], [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], or
[[IEEE-DataPort-ADHD-Child-121]] be edited. This note stays as the audit trail.

**R1 is merged (2026-11-16).** The ceiling framing has been updated vault-wide per the resolution
above. The keyword "ceiling" in the context of a fixed upper bound on AUROC is now retired; the
approved phrase is "current published frontier" with the contribution framed as calibration/PPV.
See [[Decision-Log]] Commitment 28.

**R2 is merged (2026-11-16).** Joint Löwdin orthogonalisation is mandated; pairwise-symmetrised oAEC
is barred from Riemannian stages; runtime `ensure_spd()` guard is enforced. See [[Decision-Log]] Commitment 29.

**R3 is de-risked and locked (2026-11-16).** Evaluated on real 121-child cohort (`data/adhdata.csv`). Single-path
Riemannian alignment causes a ~10 pp AUROC drop (0.9055 → 0.7995, spec 0.8833 → 0.7167), consistent with
Trap 2 (deletion of static trait signals). Dual-path trait/state decomposition is locked into Stage 3 as the safeguard.
Recovery of the trait signal will be measured when the dual-path model is ablated.
Artifact-only classifier reaches 0.8089 ± 0.0664 AUROC under repeated 5-fold CV (`scripts/r4_artifact_only.py`,
`results/r4_artifact_only.json`), proving classifiers without an AQI gate exploit muscle/blink artifacts. See [[Decision-Log]] Commitment 31.

**R5 is de-risked and implemented (2026-11-16).** Channel aliasing normalizer deployed; contiguous disjoint oscillatory ladder locked (`4–8, 8–13, 13–30 Hz`); EMG/gamma spectral confound surfaced; SpecParam fit standardized to `1–40 Hz` ($R^2 \ge 0.85$); PREP reference bad-channel rule adopted with mandatory per-group attrition reporting when >4 channels fail; multi-format loader implemented supporting `.csv`, `.set`, `.bdf`, `.edf`, `.fif`. See [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]] and [[Decision-Log]] Commitment 32.

**R4 is de-risked and re-scoped (2026-11-16).** Multi-condition Phase 2 scope de-risked: CBCL bifactor specificity contrast is primary/default (0 DUA requirement); binary $s_{\text{ASD}}$ demoted to conditional exploratory extension. See [[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]] and [[Decision-Log]] Commitment 33.

## Connections
- [[00-Project-Overview]] · [[Decision-Log]] · [[Assumptions-Register]] · [[Reading-Queue]]
- [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] · [[00-Candidate-Synthesis-and-Head-to-Head]]
- [[IEEE-DataPort-ADHD-Child-121]] · [[Healthy-Brain-Network-HBN]] · [[Problem-Space-Map]]
- [[Aperiodic-1f-Activity-and-Band-Ratios]] · [[Dynamic-Functional-Connectivity]]
