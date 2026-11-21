---
tags:
  - project-idea
  - product-definition
  - c5
  - workbench
  - screening
  - audit
  - adhd
status: selected-product-layer
---

# C5 — The EEG Reliability & Calibrated Screening Workbench (Product Layer around C0)

> **Status: SELECTED as the product/framing layer (2026-11-16).** This does **not** replace the locked
> project. It defines *what the deliverable is* and *how it is demoed and graded*. The AI engine remains
> `C0 — Riemann-ST-GraphFormer + Evidence Gate`
> ([[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]). C5 is the shell, the workflow and the report
> layer wrapped around it.
>
> Recorded as Commitment 27 in [[Decision-Log]].

---

## 1. Why This Note Exists

Two failure modes threatened the locked project, and both are documented in the vault:

1. **The accuracy trap.** Presented as a classifier, the project invites the question *"why is AUROC only
   ~0.78 and not 95%?"* — a question the field's own literature cannot answer, and one that our
   [[IEEE-DataPort-ADHD-Child-121]] card now answers definitively: no method — specialist or foundation — has
   materially exceeded **~0.79 AUROC** under subject-disjoint evaluation on this cohort (Commitment 28). The
   93–99% figures in the 2021–2023 literature come from window-level splits. The contribution is
   **calibration, artifact-awareness, and abstention**, not discrimination.
2. **The "audit is not an AI system" trap.** Presented as pure measurement science, the project risks the
   opposite reading ([[00-Candidate-Synthesis-and-Head-to-Head]] §3, C1 row): a statistical audit rather
   than an engineering artefact, which is a weak story for an engineering jury.

C5 resolves both at once. The **model** supplies the engineering artefact; the **workbench** supplies the
measurement claim; and the interface makes the second visible to a non-specialist reviewer in one screen.

---

## 2. What the Product Actually Is (one paragraph)

A locally runnable **web workbench** that accepts one paediatric EEG recording, runs the C0 pipeline, and
returns **three separated outputs**: (a) a calibrated risk index with a prevalence-aware operating point,
(b) an explicit **signal-quality verdict** that can be *"Insufficient evidence — abstain"*, and (c) a
**Reliability Report** that shows *where in the recording* the decision came from and *how much of it
survives* artifact and preprocessing changes. It never outputs a diagnosis. It outputs a triage opinion
with its own error bars.

---

## 3. Non-Negotiable Product Constraints

| # | Constraint | Why | Source |
|---|---|---|---|
| P1 | **No diagnosis output.** Language is "screening index", "triage", "insufficient evidence". | Regulatory category (research/decision-support, not SaMD) and honesty | [[Clinical-Deployment-and-Workflow]] §3, spec §4 |
| P2 | **Abstention is a first-class output**, not an error state. | A tool that cannot say "I don't know" is unusable at the point of care | [[Decision-Log]] 8 |
| P3 | **Every number carries its prevalence assumption.** PPV is always reported at 5% and 10%. | The base paper's 13.79% PPV is only interpretable with its assumed prevalence | [[Decision-Log]] 8, 13 |
| P4 | **The audit panel is read-only evidence, never a live per-patient gate** (except AQI/blink, which is live). | 1/f identity leakage is a *validation-time* finding, not a per-recording test | see §5.4 |
| P5 | **No new training runs.** C5 packages experiments C0 already runs. | Scope guardrail | [[Decision-Log]] 24, 25 |
| P6 | **Accepts `.csv`, `.set`, `.bdf`, `.edf`, `.fif`.** | Native parser for IEEE-121 `.csv`; MNE for `.set`/`.bdf`/`.edf` with auto-canonicalization | [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]], [[Decision-Log]] 32 |
| P7 | **Works on a laptop, offline.** No cloud dependency for the demo. | Jury demo reliability | [[Clinical-Deployment-and-Workflow]] §3 |

---

## 4. The Three Panels

### Panel 1 — Screening Result (the model output)
- Dual calibrated gauges co-designed from Day 1: `s_ADHD` and `s_ASD` (running on `HBN-EEG` clinical `K-SADS` labels via the NITRC DUA, with immediate no-DUA `CBCL` transdiagnostic dimensions as schedule insurance; `IEEE-121` evaluates `s_ADHD` only).
- Each gauge shows: calibrated index, matched operating point (sensitivity/specificity at a stated
  threshold), **PPV at 5% and 10% prevalence**, and the abstention state.
- A single sentence summary in plain language, e.g. *"Index 0.71 (above the 0.62 triage threshold, PPV
  0.30 at 10% prevalence). 18% of windows abstained due to poor signal quality — confidence reduced."*

### Panel 2 — Reliability / Abstention Report (the differentiator)
- **Risk–coverage curve (Dual-Cohort Mandatory)**: for a sweep of AQI thresholds, plot retained-coverage vs specificity (and vs
  PPV at 10% prevalence) on **both cohorts (`IEEE-121` and `HBN-EEG`)** so the workbench abstention claim generalizes rather than being cohort-specific. This is the panel that makes *"Abstain"* auditable.
- **Per-group attrition table** ([[Decision-Log]] 16): how many windows/participants were excluded, split
  by group. The vault's repeated finding is that exclusions disproportionately remove the most
  movement-prone children.
- **Which windows drove the score**: a timeline strip with abstained windows greyed out.
- **Reproducibility badge**: pipeline version, preprocessing config hash, model checkpoint hash, seed.
- **Connectivity-integrity line**: `n_not_psd / n_windows`, minimum raw eigenvalue, and mean/max SPD
  correction actually applied. This is not decoration — pairwise-symmetrised oAEC fails PSD in up to
  78% of band-limited windows, so the count is a direct measure of how trustworthy the graph is
  ([[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]]). Large correction ⇒ the graph panel must
  display a low-reliability warning rather than a confident picture.

### Panel 3 — Topology & Connectivity View (the interpretability hook)
- The 19-node, 5-lobe graph rendered on a schematic scalp; edges weighted by oAEC, pruned by the learned
  sparse gate.
- Node colouring by a scale-invariant attribute (**aperiodic exponent χ**, which is invariant to vertical
  gain offset — this is why χ is preferred over offset A for display; see
  [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] §6 Trap 2).
- **Stability note**: the panel must show *how stable* this graph is across windows and across the
  subject's own resamples, otherwise it is decoration ([[Explanation-Stability-and-Faithfulness]],
  [[Decision-Log]] 10).

---

## 5. What Is Deliberately *Not* In the Product

### 5.1 No multimodal fusion
Its own best evidence says adding a modality contributed nothing
([[Hidayah-2026-Multimodal-GNN-ADHD-ASD]] — and that paper is itself confounded). Adding a second
modality for its own sake is an explicitly rejected pattern ([[Problem-Space-Map]] §4).

### 5.2 No foundation-model zoo
Benchmarking many FMs is closed ([[Decision-Log]] 24, 25) and unaffordable. The workbench compares **C0 vs
the Baibulova baseline** only. A single optional frozen-encoder probe is allowed as an appendix if it
needs no additional training.

### 5.3 No cross-dataset pooling
`IEEE-121` is never pooled with any external ASD cohort. The workbench runs **one cohort at a time** and
says so on screen ([[Decision-Log]] 22, spec §4).

### 5.4 No live "1/f fingerprint" alarm
Tempting to add, but the fingerprint test ([[Assumptions-Register]] A4) is a **cohort-level validation
experiment**: does participant ID decode from `(χ, A)` alone? It has no meaningful per-recording output.
It belongs in Panel 2 as a one-line audit finding (*"subject-identity decodable from (χ,A) at XX% vs
chance 0.5% — spectral identity leak confirmed/rejected"*), never as a red/green light on a patient.

### 5.5 No caregiver-facing mode in Phase 1
Named as an open gap in [[Problem-Space-Map]] §4. It is a **Phase 3 aspiration** at most, and it needs
evaluation machinery the vault does not yet have.

---

## 6. The Headline Claim (what is graded)

The workbench is **not** the contribution. It is the delivery vehicle for one sentence:

> On the 121-child IEEE DataPort cohort, under strict subject-disjoint Nested 5-Fold and Leave-One-Subject-Out
> evaluation, the base paper's 44.44% specificity and 13.79% PPV-at-10%-prevalence are improved to
> **X% and Y%** by artifact-aware abstention plus unsupervised per-subject Riemannian alignment, while
> participant-level AUROC moves by **≤ Z** — demonstrating that no method (specialist or foundation model)
> has materially exceeded the current published frontier of ~0.79 AUROC under subject-disjoint evaluation,
> and that the remaining gains are in **calibration, artifact-awareness, and abstention** rather than
> discrimination. (Commitment 28: "frontier", not "ceiling".)

**The demo exists to make X, Y and Z trustworthy**, not to be impressive on its own. If a reviewer
remembers the dashboard but not the numbers, the project has failed. This is the direct application of
[[Decision-Log]] 9 ("complexity must be earned").

---

## 7. Frame: what C5 is *not* claiming

- Not a diagnostic device, not clinically validated, not a replacement for a clinician.
- Not a benchmark harness for other people's models.
- Not a general EEG platform — it is scoped to paediatric neurodevelopmental screening with one engine.
- Not evidence that the ADHD construct is measurable from 19-channel EEG. It may well show the opposite,
  and that remains a publishable result ([[Problem-Space-Map]] §5).

---

## 8. Delivery Tracks Tied to the Product (Co-Designed Core Scope)

| Track / Stage | Product state | Gate |
|---|---|---|
| **Track 1a (Core)** | CLI + HTML report (static) on IEEE-121 | Base-paper reproduction reproduces 63.16% / 0.7444 + R4 artifact control |
| **Track 1b (Core)** | Same, plus the 5-step ablation ladder and risk–coverage curve | Ablation runs under Nested Group 5-Fold |
| **Track 2a (Core)** | Local web UI (upload → 3 panels) with dual-head architecture (`s_ADHD`, `s_ASD` on HBN `CBCL` no-DUA + `IEEE-121`) | Works on both `.set` and converted IEEE files; no-DUA schedule insurance |
| **Track 2b (Core)** | Plug clinical `K-SADS` `Control / ADHD / ASD / Comorbid` labels into the pre-built `s_ASD` & `s_ADHD` heads | NITRC DUA approved **and** usable ASD `n ≥ ~100` verified |
| **P3 (aspirational)** | Caregiver summary mode | Out of scope for this project's grading |

**Schedule insurance:** Because Track 2a builds the dual-head architecture immediately on no-DUA HBN `CBCL` dimensions (`Attention` vs. `Internalizing`/`Externalizing`), Track 2b requires only plugging in `K-SADS` labels once the NITRC DUA clears—keeping the entire `ADHD + ASD` workbench deliverable without blocking on third-party turnaround. See [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]] R4.

---

## 9. Risks Specific to the Product Layer

| # | Risk | Kill test |
|---|---|---|
| PR1 | **The dashboard becomes the project.** Weeks spent on UI, ablation unfinished. | Hard rule: no UI work until P1b (ablation + risk–coverage curve) is complete. |
| PR2 | **The graph panel is decoration.** Pretty picture, no stability evidence. | Ship the panel only with a stability metric attached (split-half ICC or equivalent). |
| PR3 | **Abstention looks like a bug to a jury.** They ask "why did it refuse?" | Put the risk–coverage curve on the same screen and a one-line explanation of *why* abstention raises PPV. |
| PR4 | ~~**The 19-node graph renders wrong.** `T3/T4/T5/T6` do not exist in HBN's montage.~~ | **RESOLVED:** `scripts/data_loader.py` canonicalizes legacy names and EGI 128 nets to modern `STANDARD_1020_19` on load; see [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]]. |
| PR5 | ~~**`.set` loading fails on HBN.**~~ | **RESOLVED:** Isolated PEP 668 virtual environment standard documented; informative errors for `mne[hdf5]` + `pymatreader`. |

---

## 10. Connections

- **Engine:** [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]] (C0, the locked AI core)
- **Comparison:** [[00-Candidate-Synthesis-and-Head-to-Head]] (C0 + C5 elsewhere in the scorecard)
- **Ingredient modules:** [[Candidate-Evidence-Aware-ADHD-Screening]] (C3 abstention/calibration),
  [[Candidate-Decoding-Multiverse-Aperiodic-Audit]] (C1 audit backbone, audit-only use)
- **Workflow framing:** [[Clinical-Deployment-and-Workflow]] (§5 "what a strong final-year version looks like")
- **Guardrails:** [[Decision-Log]] 8, 9, 16, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32
- **Verification:** [[09-Verification-Pending/V-01-Risk-Register-2026-11-16]], [[09-Verification-Pending/V-04-R5-RESOLVED-Runtime-Traps]]
- **Datasets:** [[IEEE-DataPort-ADHD-Child-121]], [[Healthy-Brain-Network-HBN]]
