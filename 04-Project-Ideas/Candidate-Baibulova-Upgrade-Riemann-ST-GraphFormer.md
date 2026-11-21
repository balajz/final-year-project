---
tags:
  - project-idea
  - base-paper-upgrade
  - adhd
  - eeg
  - dynamic-connectivity
  - graph-transformer
  - network-index
status: selected-final-project
---

# Final Selected Project: Next-Gen Spatio-Temporal Graph Transformer & Calibrated Dual-Index (Upgrading Baibulova et al., 2026)

> **Status: FINAL SELECTED PROJECT (Locked 2026-11-16).** Directly upgrades our college base paper — [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] ([DOI: 10.3390/computers15060333](https://doi.org/10.3390/computers15060333)) — by solving its 6 architectural, signal-processing, and clinical-screening bottlenecks, and expanding to unified **ADHD + ASD** differential screening on HBN-EEG.

---

## 1. Why Baibulova et al. (2026) Is an Ideal College Base Paper
In engineering capstone culture, picking a recent, reproducible base paper with public code ([GitHub repo](https://github.com/Mukhanovaa/EEG_ADHD_Dynamic_Envelope_Connectivity_Hybrid_ST_Graph_Transformer/tree/main)) and a public dataset ([[IEEE-DataPort-ADHD-Child-121]]) gives the review panel a concrete baseline (**63.16% test accuracy / 0.7444 test AUROC / 0.7770 LOSO AUROC / 44.44% specificity**).

More importantly, our vault's 9-paper investigation has already uncovered **six exact scientific and architectural flaws** in Baibulova et al. that explain *why* their specificity collapsed to 44.44% and *how* to fix it cleanly.

---

## 2. The 6 Drawbacks of the Base Paper & Our Exact Technical Upgrades

| # | Drawback in Baibulova et al. (2026) | Evidence from Our Vault | Our Next-Level Upgrade |
|---|---|---|---|
| **D1** | **"Graph Transformer" Misnomer (Topology Destruction):** Equation (6) flattens the $19 \times 19$ matrix into a 171-D vector $e_t = \text{vec}_{\text{upper}}(A_t)$ before feeding the Transformer+GRU. Node-level spatial graph topology is completely discarded in their main model. | [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]] §4; [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] shows criss-cross spatial-temporal factorized attention + 3D/relative positional priors preserve montage topology. | **True Topological Spatio-Temporal Graph Attention (ST-GATv2 / Criss-Cross Graph Transformer):** Operate on node embeddings $V_t \in \mathbb{R}^{19 \times d}$ weighted by continuous edge attention over 10–20 anatomical coordinates, preserving node hubs (`O1, P7, Fp1, Fz`) before temporal Transformer+GRU pooling. |
| **D2** | **Volume Conduction & Zero-Lag Leakage in Pearson Envelope Correlation:** Equation (3) uses raw zero-lag Pearson correlation on Hilbert envelopes, and Eq. (4) applies a hard heuristic threshold $\theta = 0.40$. Zero-lag correlation is heavily inflated by scalp volume conduction (Figure 7) and reference scheme ([[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] showed CAR rewrites edges to Jaccard 0.067). | [[Dynamic-Functional-Connectivity]], [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]], [[Kernel-Matrix-Based-Transfer-Entropy]] | **Orthogonalized / Phase-Lag Connectivity + Learnable Sparse Graph Gate:** Replace raw Pearson envelope correlation with **orthogonalized Amplitude Envelope Correlation (oAEC)** or **Weighted Phase Lag Index (wPLI)** to eliminate zero-lag volume conduction, and replace the arbitrary $\theta=0.40$ cutoff with a differentiable sparse edge gate ($\alpha$-entmax / L1 topological gate). |
| **D3** | **Aperiodic $1/f$ Contamination of "Theta Dominance":** Table 6 claims theta connectivity (4–8 Hz, AUC 0.7333) dominates beta (13–30 Hz, AUC 0.5667), and Section 4.2 claims delta/theta vs. beta power shifts—without removing the $1/f$ background. | [[Troendle-2026-TBR-Multiverse-HBN]] & [[Aperiodic-1f-Activity-and-Band-Ratios]] prove that $1/f$ exponent ($\chi$) and offset ($A$) shifts masquerade as theta changes and act as a subject identity fingerprint. | **SpecParam-Decomposed Oscillatory Connectivity + Aperiodic Node Features:** Decompose each window's spectrum via `SpecParam` into periodic oscillatory peaks + aperiodic $(\chi_i, A_i)$ per channel, feeding $(\chi_i, A_i)$ as explicit node attributes alongside pure oscillatory coupling. |
| **D4** | **Unaligned Cross-Subject Baseline Shifts (44.44% Specificity & PPV = 13.79%):** Standardizing upper-triangular edges by global training-set $\mu_{\text{train}}, \sigma_{\text{train}}$ (Eq. 7) leaves per-subject skull conductivity and impedance shifts intact—causing high false positives on unseen children. | [[Wang-2025-CBraMod-CrissCross-Brain-Foundation-Model]] & [[Unsupervised-Alignment-Leverage]] show per-subject **Euclidean / Riemannian Alignment** on unlabeled windows buys $+14\text{ pp}$ cross-subject accuracy and fixes threshold shift. | **Unsupervised Riemannian / Tangent-Space Subject Alignment:** Project each child's sequence of SPD connectivity matrices $\{C_t + \epsilon I\}_{t=1}^T$ onto the **Riemannian tangent space** centered at the subject's unlabeled geometric mean covariance before sequence encoding. |
| **D5** | **Unverified Artifact Exploiting ($\pm 6\text{ MAD}$ Clamping Leaves Ocular/EMG Structure):** Figure 5 shows `Fp1/Fp2` have $2.5\times$ the spike rate of central channels, and `Fp1-O1` / `Fp1-P7` appear as top theta edges in Table 7—classic vertical eye-blink propagation! | [[Class-Correlated-Artifact-Control]], [[Kim-2025-NoiseRobust-GCN-ADHD-vs-Tic]] | **Built-In Artifact Audit & Quality-Gated Selective Abstention:** Run the [[Class-Correlated-Artifact-Control]] battery (artifact-only baseline + frontal-dropout check) and add an **Uncertainty & Artifact Abstention Gate** ([[Candidate-Evidence-Aware-ADHD-Screening]]) that outputs `"Insufficient Signal Quality — Abstain"` on blink-corrupted sequences, directly boosting clinical specificity and PPV. |
| **D6** | **Single-Cohort, Task-Blind Limitation ($n=19$ Test Split):** The 19-subject test split has huge confidence intervals (`AUC [0.489, 0.944]`), and the Kaggle CSV stripped all visual-counting stimulus timestamps and severity scores. | [[Healthy-Brain-Network-HBN]], [[Candidate-Event-Locked-NeuroBehavioral-HBN]], [[Decision-Log]] commitments 6–12 | **Dual-Cohort Validation & Continuous Severity Calibration:** Benchmark on **IEEE DataPort ($N=121$, LOSO + Nested Group 5-Fold)** to prove direct improvement over Baibulova's code, *and* scale to **HBN-EEG ($N > 1,000$ public BIDS)** where the scalar Network Index $s^{(i)}$ can be validated against **actual continuous CBCL Attention severity scores** and event-locked **Contrast Change Detection (CCD)** trials! |

---

## 3. Architecture of the Upgraded System ("Riemann-ST-GraphFormer + Evidence Gate")

1. **Stage 1 — Artifact-Audited & Aperiodic-Aware Signal Processing:**
   - Input: 19-channel EEG ($128\text{ Hz}$ on IEEE DataPort; 10–20 subset of HBN-EEG).
   - Extract per-window **Artifact Quality Index (AQI)** (frontal blink energy, 30–60 Hz muscle ratio, outlier fraction) + **SpecParam Aperiodic Node Features** $(\chi_i, A_i) \in \mathbb{R}^{19 \times 2}$.
   - Compute volume-conduction-robust **joint-Löwdin orthogonalised Envelope Connectivity (oAEC)** in theta (4–8 Hz), alpha (8–13 Hz), and beta (13–30 Hz) bands. **The pairwise-symmetrised oAEC that MNE-CPP/Brainstorm default to is NOT PSD** (verified, up to 78% failures in band-limited windows) and is a trap; every matrix passes `ensure_spd()` with the correction logged ([[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]]).
2. **Stage 2 — Riemannian Subject-Centering (Zero-Label Adaptation):**
   - Regularize each window's connectivity matrix into SPD form and map to the **Riemannian tangent space** relative to that subject's unlabeled baseline geometric mean—eliminating cross-subject impedance/gain offsets without using test labels.
3. **Stage 3 — True Topological Spatio-Temporal Graph Transformer:**
   - **Spatial Graph Attention:** Unlike Baibulova's flattened 171-D vector, each time step $t \in \{1..T\}$ updates 19 cortical node embeddings using multi-head **Graph Attention (GATv2)** over the frequency-specific connectivity graph + 3D electrode distance priors.
   - **Dual-Stream Temporal Dynamics:** Aggregated node/community embeddings pass through the parallel **Multi-Head Temporal Transformer** (long-range state occupancy/flexibility) + **BiGRU** (local state transitions).
4. **Stage 4 — Calibrated Network Index & Selective Abstention:**
   - Outputs both the **Calibrated Network Index $s^{(i)}$** (Platt/temperature-scaled for 5%–10% clinical prevalence) and an **Epistemic + Artifact Abstention Gate** (risk–coverage curve showing how specificity and PPV rise from 44.4% / 13.8% when noisy windows are flagged).

---

## 4. Why This Specific Upgrade Satisfies Both Academic Jury Expectations & Vault Rigor
- **Direct Base-Paper Comparison:** You can run Baibulova et al.'s official GitHub code out-of-the-box as Baseline 0, then show a clean, step-by-step ablation table (`+oAEC/wPLI`, `+Riemannian Alignment`, `+True Spatial Graph Attention`, `+Aperiodic 1/f Node Priors`, `+Quality Abstention Gate`).
- **Bulletproof Against Negative or Ceiling Results:** Even if participant-level AUROC on the 121-child dataset stays near the current published frontier (~0.79 — the best subject-disjoint figure in the literature, from REVE under Brain4FMs' fixed-LR protocol), **Riemannian centering + selective abstention on artifact-heavy segments directly fixes their worst metric (44.44% specificity / 13.79% PPV)**, and validating the Network Index against continuous **CBCL Attention scores on HBN-EEG** proves whether their "Network Index" actually tracks clinical severity. The contribution is calibration and specificity, not discrimination. Do not frame AUROC improvement as the headline — see [[Decision-Log]] Commitment 28.

## 9. Connection to the Product Layer
This note specifies the **AI engine**. The **deliverable** that wraps it — panels, abstention UI, audit report, demo script, delivery phases — is [[Candidate-C5-Reliability-Screening-Workbench]] (Commitment 27). Two consequences for this note:
- The engine's headline claim is the **specificity/PPV rescue**, not AUROC, and it is graded through the workbench.
- Two safeguards in §6 must survive into the implementation and must not be dropped from a spec: **Trap 1** (joint Löwdin oAEC SPD validity — resolved in [[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]], Commitment 29) and **Trap 2** (dual-path trait/state: keep scale-invariant aperiodic node features so Riemannian centring cannot delete static group differences — empirically confirmed on IEEE-121 in [[09-Verification-Pending/V-03-R3-Alignment-Harness]], Commitment 31).

## 10. Connections
- Base Paper: [[Baibulova-2026-Hybrid-ST-Graph-Transformer-ADHD]]
- Related Candidates: [[00-Candidate-Synthesis-and-Head-to-Head]], [[Candidate-Evidence-Aware-ADHD-Screening]], [[Candidate-Decoding-Multiverse-Aperiodic-Audit]], [[Candidate-Event-Locked-NeuroBehavioral-HBN]]
- Technical Concepts: [[Dynamic-Functional-Connectivity]], [[Network-Index-Modeling]], [[Aperiodic-1f-Activity-and-Band-Ratios]], [[Subject-Level-Evaluation-Hygiene]], [[Nested-CV-and-Hyperparameter-Leakage]]
- Opportunities: [[Unsupervised-Alignment-Leverage]], [[Class-Correlated-Artifact-Control]]

---

## 6. Deep Brainstorming Stress-Test: 4 Mathematical & Methodological Traps We Must Solve in the Design

When we stress-test the 6 upgrades above against our vault's 31 guardrails in [[Decision-Log]], four subtle traps emerge that would trip up a naive implementation—and solving them on paper right now is what makes this architecture genuinely publication-grade. **Trap 1 is resolved and verified** ([[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]]); **Trap 2 is resolved on real data** (alignment drops AUROC 0.9055 → 0.7995, locking the dual-path architecture, [[09-Verification-Pending/V-03-R3-Alignment-Harness]], Commitment 31); Traps 3–4 remain open design obligations.

### Trap 1: The SPD Manifold vs. Phase-Lag / Orthogonalized Connectivity Conflict (Upgrades D2 × D4)
- **The mathematical conflict:** Riemannian tangent-space alignment (D4) requires Symmetric Positive Definite (SPD) matrices ($\mathcal{S}_{++}^{19}$, all eigenvalues $> 0$). Raw covariance and Pearson correlation matrices are Positive Semi-Definite (so $C_t + \epsilon I \in \mathcal{S}_{++}^{19}$). However, **wPLI** and **pairwise-orthogonalized oAEC** (D2) are **not guaranteed to be Positive Semi-Definite**—they can have negative eigenvalues because phase-lag indices and asymmetric pairwise projections are not Gram matrices.
- **The clean architectural resolution — VERIFIED 2026-11-16, matrix is `ensure_spd`-guarded:**
  1. Perform **Euclidean / Riemannian whitening on the band-filtered 19-channel signals first** ($\tilde{X}_t = \bar{R}_{\text{subj}}^{-1/2} X_t$, where $\bar{R}_{\text{subj}}$ is the geometric mean of the child's unlabeled raw/band covariance matrices), **or** apply **symmetric (Löwdin) orthogonalisation** ($X_{\perp} = X (X^\top X)^{-1/2}$) per window before extracting Hilbert envelopes.
  2. The PSD claim holds **only** for **joint** Löwdin orthogonalisation, then envelope correlation — that matrix **is** a correlation matrix of real vectors, hence PSD by construction. **Pairwise-symmetrised oAEC (the MNE-CPP/Brainstorm default) is NOT PSD**: measured up to 78% negative-eigenvalue windows in band-limited signals, worst-case min eigenvalue −0.93. All connectivity matrices pass `ensure_spd()` (clip eigenvalues at $\epsilon$, log the correction) before any tangent-space mapping. See [[09-Verification-Pending/V-02-R2-RESOLVED-oAEC-SPD]].

### Trap 2: Does Per-Subject Alignment Wash Out Between-Group Trait Differences? (Upgrade D4)
- **The conceptual trap:** If you center every child's connectivity matrices around that child's own mean matrix $\bar{R}_{\text{subj}}$, you remove all **static between-subject offsets** (skull thickness, electrode impedance, global gain)—which is why it rescues specificity—but what if part of the true ADHD signal was a static shift in mean connectivity?
- **The clean architectural resolution (Dual-Path Trait + State Decomposition):**
  - **Dynamic State-Flexibility Stream (Aligned):** The Riemannian-centered sequence $\{\tilde{C}_t\}_{t=1}^{10}$ measures pure **within-subject temporal reconfigurations and state occupancy transitions** (directly testing Baibulova's Figure 10 hypothesis that ADHD brains get "stuck" in a single hyper-occupied state with reduced network flexibility, free of impedance confounds).
  - **Gain-Invariant Static Trait Stream (Node Priors):** To preserve static trait information without re-introducing impedance leakage, feed **scale-invariant node features** into the GATv2 nodes: the `SpecParam` **aperiodic exponent $\chi_i$** (slope is invariant to vertical gain offset $A_i$!) and **periodic peak power relative to the $1/f$ floor**.
  - **Ablation Guard (Commitment 30):** The 4-arm ablation harness `scripts/r3_alignment_ablation.py` is verified and ready. If real IEEE-121 data shows $\Delta\text{AUROC} < -0.05$ under Riemannian centering, this dual-path design is mandatory to prevent signal deletion. See [[09-Verification-Pending/V-03-R3-Alignment-Harness]].

### Trap 3: Overfitting on $N=121$ Subjects (Why Baibulova's Figure 18 Validation Curve Decayed)
- **The empirical warning in the base paper:** Look at Baibulova et al.'s Figure 18 (Bottom): their subject-level validation AUC peaks around epoch 4 at $\approx 0.70$ and **steadily decays to $\approx 0.62$** as training continues. With only 84 training subjects (or 120 in LOSO), a heavy parameter count memorizes subject fingerprints (`21–24 pp` leakage gap in [[Geethapriya-2026-Leakage-Aware-Subjectwise-ADHD]]).
- **The clean architectural resolution (Commitment 9 — Complexity Must Be Earned):**
  - **Community-Factorized Low-Rank Spatial GATv2:** Instead of learning an unconstrained $171 \times d$ projection, constrain the spatial graph attention using the **5 anatomical 10–20 communities** shown in Baibulova's Figure 8 (`Frontal`, `Central`, `Temporal`, `Parietal`, `Occipital`) with parameter sharing across the $T=10$ windows.
  - **Cross-Cohort Pretraining / Transfer from HBN-EEG ($N > 1,000$) to IEEE-121 ($N=121$):** Pretrain or fit the spatial-temporal graph representation on the 19-channel 10–20 subset of public **HBN-EEG**, then evaluate zero-shot and fine-tuned transfer on the 121-child dataset.

### Trap 4: Bridging IEEE-121's Visual Counting Task with HBN-EEG's 6 Tasks (Upgrade D6)
- **The paradigm mismatch:** Many papers mistakenly treat `IEEE-DataPort-ADHD-Child-121` as resting-state, when Section 3.1 explicitly notes it was recorded during a **structured visual counting task**.
- **The clean architectural resolution:** HBN-EEG includes both **passive Resting State** and **active visual attention tasks** (**Contrast Change Detection [CCD]** and **Symbol Search**). By extracting the matching 19 channels (`Fp1, Fp2, F3, F4, C3, C4, P3, P4, O1, O2, F7, F8, T7, T8, P7, P8, Fz, Cz, Pz`) from HBN-EEG, we can test whether active visual-attention connectivity generalizes better to IEEE-121 than resting-state connectivity, *and* test event-locked windows around CCD stimulus/button-press markers (directly fulfilling Baibulova et al.'s Section 6 Conclusions).

---

## 7. Multi-Condition & Specificity Expansion: Transdiagnostic CBCL Contrast & Conditional ASD Extension

To elevate the project into a genuine **multi-application neurodevelopmental platform** without falling into the dataset-pooling confound ([[Cohort-and-Site-Confounding]], [[Decision-Log]] Commitment 22), we evaluate transdiagnostic specificity strictly via **Approach A (Same-Machine Unified HBN-EEG Screening)**:

### 7.1 Why Approach A Is Scientifically Valid (and Why Pooling Is Banned)
- **Banned Pattern:** Never pool `IEEE-DataPort-ADHD-Child-121` (visual counting, 19 ch, Tehran) with a separate public ASD dataset (eyes-closed rest, different amplifier/country). That creates 100% collinearity between disorder and acquisition site ([[Hidayah-2026-Multimodal-GNN-ADHD-ASD]]).
- **Valid Pattern (Approach A):** On **HBN-EEG**, all participants (Control, ADHD, ASD, and Co-occurring ADHD + ASD — ~44% comorbidity) are recorded on the **same 128-channel EGI HydroCel system** under the **same 6 tasks**.
- **Shared Signal Bottlenecks:** Neurodevelopmental resting/task EEG exhibits altered long-range connectivity, aperiodic shifts, and high sensory-motor/blink noise—meaning our `oAEC` echo removal, `SpecParam 1/f` node priors, `Dual-Path Riemannian Alignment`, and `AQI Abstention Gate` solve the exact same bottlenecks across conditions.

### 7.2 Primary Transdiagnostic Contrast vs. Conditional ASD Extension (Commitment 33)
- **Primary / Default Target (Zero DUA Required):**
  - **CBCL Bifactor Specificity Contrast:** Decode continuous `attention` factor scores and demonstrate that the learned attention-network index is invariant to (does not cross-decode) orthogonal `externalizing` or `internalizing` psychiatric factors.
  - Accessible immediately on public BIDS / S3 / NEMAR releases (`ds005505`–`ds005516`) with **zero credentials and 0 days latency**.
- **Conditional Extension (Contingent on NITRC DUA):**
  - **ASD Social/Sensory-Network Index ($s_{\text{ASD}}$):** Discrete clinical classification (`K-SADS` ADHD vs ASD vs Comorbid vs Control) is retained strictly as an exploratory extension, executed **only if** the NITRC DUA is approved within the Phase 2 timeline and yields $n_{\text{ASD}} \ge 100$ usable recordings.
  - Project defense and paper publication do **not** depend on DUA arrival ([[09-Verification-Pending/V-05-R4-RESOLVED-ASD-Scope-and-DUA]]).
- **Unified Evidence Gate:** Single `AQI + Epistemic Uncertainty` abstention module that flags noisy/blink-flooded segments as *"Insufficient Signal Quality — Abstain"* before outputting any clinical score.

---

## 8. Two-Track Core Execution & IEEE/Scopus Publication Roadmap (Updated 2026-11-16)

### Core Track 1 — Base-Paper Upgrade, Artifact Audit & 5-Step Ablation (`IEEE-121`)
1. **Base-Paper Reproduction:** Run [Baibulova et al.'s GitHub pipeline](https://github.com/Mukhanovaa/EEG_ADHD_Dynamic_Envelope_Connectivity_Hybrid_ST_Graph_Transformer/tree/main) on [[IEEE-DataPort-ADHD-Child-121]] under **Nested Group 5-Fold CV** and **LOSO** to establish the exact before-and-after baseline (`63.16%` test acc / `0.7444` test AUROC / `0.7770` LOSO AUROC / `44.44%` specificity / `13.79%` PPV).
2. **R4 Artifact Audit & 5-Step Ablation Ladder:** Run `scripts/r4_artifact_only.py` and `scripts/r4_artifact_control.py`, then quantify the isolated contribution of each upgrade:
   - `+ Symmetric Löwdin oAEC` (removes zero-lag volume conduction while preserving SPD manifold validity)
   - `+ SpecParam 1/f Node Priors (χ_i, A_i)` (separates aperiodic background from oscillatory connectivity)
   - `+ Dual-Path Riemannian Trait/State Alignment` (fixes cross-subject impedance while retaining static ADHD traits)
   - `+ 5-Lobe 19-Node Spatial GATv2` (restores true cortical graph topology before Transformer+GRU)
   - `+ AQI & Epistemic Selective Abstention Gate` (flags blink/EMG-corrupted segments)
3. **Publication Statistical Checklist:** Report participant-level AUROC (secondary), balanced accuracy, specificity at matched sensitivity, **Brier score / ECE**, **PPV at 5%–10% prevalence**, **Risk–Coverage abstention curve**, **DeLong's test** vs. Baibulova baseline, and a **per-group attrition table** ([[Decision-Log]] Commitments 6–16).

### Core Track 2 — Unified `ADHD + ASD` Co-Design on `HBN-EEG` & C5 Workbench
1. **Dual-Head Co-Design from Day 1:** Build the shared `Riemann-ST-GraphFormer` backbone with dual calibrated output heads (`s_ADHD`, `s_ASD`) and the 3-panel **C5 Reliability Workbench** ([[Candidate-C5-Reliability-Screening-Workbench]], Commitment 27; `.csv`/`.set`/`.bdf`/`.edf`/`.fif` upload $\rightarrow$ dual triage gauges + Risk–Coverage report + stable 5-lobe graph), with **no UI work until the Track 1 ablation ladder and risk–coverage curve are complete**.
2. **Immediate No-DUA Transdiagnostic Insurance:** Validate immediately on the 19-channel 10–20 subset of [[Healthy-Brain-Network-HBN]] (`ds005505`–`ds005516` mini-set + selective S3 subset) against orthogonal `CBCL` dimensions (`Attention` vs. `Externalizing` vs. `Internalizing`) and active `Contrast Change Detection (CCD)` vs. passive resting state.
3. **Clinical `K-SADS` `ADHD + ASD` Labels:** Submit the free [NITRC HBN DUA](https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network) at project start to unlock clinical `Control`, `ADHD`, `ASD`, and `Co-occurring ADHD+ASD` labels on the **same 128-channel hardware** (Approach A, zero cross-dataset pooling), verifying usable ASD sample size ($n_{\text{ASD}} \ge 100$).
