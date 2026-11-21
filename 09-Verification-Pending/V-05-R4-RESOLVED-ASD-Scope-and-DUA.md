---
tags:
  - verification
  - scoping
  - hbn
  - superseded
date: 2026-11-16
status: SUPERSEDED-BY-COMMITMENT-34
---

# V-05 — R4 RESOLVED: ASD Scope Contradiction & NITRC DUA De-Risking

> **⚠️ SUPERSEDED (2026-11-16) by [[Decision-Log]] Commitment 34.**
>
> This note recorded the *first* R4 resolution: demote binary `s_ASD` to an exploratory extension and
> default Phase 2 to the public CBCL bifactor contrast. Commitment 34 **reverses the demotion** — the
> `s_ADHD` + `s_ASD` dual-head is co-designed as **Core Track 2** from Day 1 — while keeping every
> de-risking guarantee from this note (the no-DUA CBCL arm runs in parallel, nothing depends on the DUA
> arriving, kill condition retained).
>
> **The R4 problem is still solved; the solution changed.** Read Commitment 34 as authoritative. The text
> below is retained only as the reasoning trail for *why* the DUA dependency was a risk in the first place.
>
> **What survives:** the DUA is still the bottleneck (hence the parallel no-DUA arm); raw `s_ASD` AUROC is
> still never headlined; the CBCL transdiagnostic contrast remains the strongest part of Track 2.
> **What does not survive:** "demoted to exploratory / conditional only" (§1 item 2, §3 item 1).

**Associated Risk:** [[V-01-Risk-Register-2026-11-16]] § R4 (High → RESOLVED)  
**Verification Date:** 2026-11-16  
**Auditor:** Architecture Review  
**Governing Decision:** [[Decision-Log]] Commitment 33  
**Target Notes Updated:** [[Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]], [[Candidate-C5-Reliability-Screening-Workbench]], [[00-Project-Overview]]  

---

## 1. Executive Summary

Risk R4 identified a critical strategic and schedule contradiction:
1. **Strategic contradiction:** Specification §3 Objective 5 and §4 Phase 2 elevated Autism Spectrum Disorder (ASD) to a co-equal headline deliverable ($s_{\text{ASD}}$ alongside $s_{\text{ADHD}}$), despite [[Problem-Space-Map]] §4 explicitly directing "Avoid as a headline" and [[Neurological-Conditions-Landscape]] ranking ASD 12th of 12 conditions as "Ill-posed — weak, heterogeneous effects".
2. **Schedule & Governance dependency:** Discrete clinical ASD diagnostic labels (`K-SADS`) require the institutional **NITRC HBN Data Usage Agreement (DUA)**, creating a third-party gate that could delay project graduation if review is prolonged.

**Resolution:**
The project's Phase 2 multi-condition deliverable is de-risked by decoupling it entirely from third-party DUA approval:
1. **Primary / Default Phase 2 Deliverable:** The **Transdiagnostic Specificity Contrast** on public HBN BIDS CBCL bifactors (**attention** vs. **externalizing** vs. **internalizing** vs. **p-factor**) under the unified AQI Selective Abstention Gate. This requires **ZERO DUA**, is immediately accessible on public S3/NEMAR releases, and scientifically supersedes binary disease classification.
2. **Conditional Exploratory Extension:** Discrete $s_{\text{ASD}}$ classification is demoted from a headline deliverable to an exploratory secondary extension, executed **only if** the NITRC DUA is approved within Phase 2 and yields $n_{\text{ASD}} \ge 100$ usable recordings.
3. **Core Project Completion Guarantee:** The graduation submission and paper deliverables are 100% complete with Phase 1 (IEEE-121 engine + C5 workbench + calibration/PPV rescue) and Phase 2 Default (HBN CBCL bifactor specificity contrast). No external approval blocks graduation.

---

## 2. Detailed Technical & Clinical Justification

### 2.1 The Clinical Strength of the Dimensional Bifactor Contrast
In pediatric neurodevelopment, binary diagnostic labels ("ADHD" vs "Control", "ASD" vs "Control") are heavily contaminated by shared genetic architecture, high clinical comorbidity (~44% comorbidity between ADHD and ASD), and nonspecific distress/movement.

A model claiming to "classify ASD from EEG" typically picks up generic non-specific distress or motor restlessness rather than autism-specific neurobiology.

In contrast, HBN's public BIDS metadata ships **four CBCL-derived orthogonal factor scores** across thousands of children:
- $F_{\text{attention}}$: Inattention, impulsivity, executive dysfunction
- $F_{\text{externalizing}}$: Conduct, oppositional behavior, aggression
- $F_{\text{internalizing}}$: Anxiety, depressive withdrawal, somatic complaints
- $F_{p}$: General psychopathology bifactor

By testing whether $F_{\text{attention}}$, $F_{\text{internalizing}}$, and $F_{\text{externalizing}}$ (and $s_{\text{ASD}}$ once `K-SADS` labels clear) decode above a stated **equivalence bound (minimum detectable effect)**—paired with an explicit **power calculation** for the usable per-task sample size $n$—we measure the same construct dimensionally, where a null result is interpretable rather than ambiguous.

**HBN Artifact Control (Mandatory):** Multi-task, multi-release HBN-EEG introduces its own recording confounds—release-batch drift, `CCD`-active button-press/ocular motion vs. resting-state movement, and per-child blink/EMG load. Track 2 therefore applies the **exact same artifact-control battery** used on `IEEE-121`: the `AQI` selective abstention gate, an artifact-only baseline on HBN proxies, and release-batch stratification, rather than assuming public BIDS EEG is artifact-free.

### 2.2 Access Route Comparison

| Feature | Primary / Default Route (Public BIDS / S3) | Conditional Extension Route (NITRC DUA) |
|---|---|---|
| **Platform** | NEMAR / Public S3 (`s3://fcp-indi/data/Projects/HBN/BIDS_EEG`) | NITRC / FCON 1000 portal |
| **DUA Requirement** | **NO DUA** (public, anonymous, immediate) | Institutional DUA (PI signature, institutional review) |
| **Latency** | **0 days** (immediate download) | Uncertain (weeks to months) |
| **Available Targets** | CBCL bifactor scores (`attention`, `externalizing`, `internalizing`, `p-factor`) + CCD active task markers | Clinical `K-SADS` diagnoses (ADHD subtypes, ASD, Comorbid, Controls) |
| **Project Role** | **Phase 2 Default Deliverable** | **Phase 2 Exploratory Extension** (reported if approved) |

---

## 3. Specifications Updated Vault-Wide

1. **[[04-Project-Ideas/Candidate-Baibulova-Upgrade-Riemann-ST-GraphFormer]]:**
   - Section 7 renamed to: *Transdiagnostic Specificity Contrast (CBCL Bifactors) & Conditional ASD Extension on HBN-EEG*.
   - Objective 5 explicitly framed: Default is CBCL attention vs externalizing/internalizing specificity contrast. $s_{\text{ASD}}$ marked as an exploratory extension contingent on DUA approval.
2. **[[04-Project-Ideas/Candidate-C5-Reliability-Screening-Workbench]]:**
   - Panel 1 clinical gauge: Phase 1 displays $s_{\text{ADHD}}$ and AQI evidence score. Phase 2 default displays transdiagnostic attention specificity vs externalizing/internalizing index. $s_{\text{ASD}}$ gauge rendered conditionally only when DUA labels are present.
3. **[[07-Decisions/Decision-Log]]:**
   - Added **Commitment 33** locking this hierarchy into project governance.

---

## 4. Final Risk Register Status

With R4 resolved, **R1, R2, R4, and R5 in [[V-01-Risk-Register-2026-11-16]] are closed; R3 remains open pending execution of the Dual-Path Trait + State ablation** (and `scripts/r4_artifact_only.py` / `scripts/r4_artifact_control.py` remain awaiting execution on `IEEE-121`).
