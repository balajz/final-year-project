# 10 — Algorithmic Design

> Status legend: **Implemented** = present in the working prototype; **Designed** = specified but not yet
> implemented/trained; **Proposed** = a formalised extension not yet finalised.

## Algorithm 1 — Global Joint Löwdin Orthogonalised Envelope Connectivity (oAEC)

**Status.** Implemented.

**Purpose.** Compute a positive semi-definite, volume-conduction-suppressed connectivity matrix.

**Inputs.** Windowed signal **X** ∈ ℝ^{C×W} (C channels, W samples).

**Outputs.** Connectivity matrix **C** ∈ 𝒮_{+}^{C}.

**Logic.**

1. Form the orthogonalised matrix **X**⊥ = **X**(**X**ᵀ**X**)⁻¹ᐟ².
2. Extract the Hilbert envelope of each row of **X**⊥.
3. Compute the Pearson correlation matrix of the envelopes.
4. Pass through the SPD guard (Algorithm 2).

**Pseudocode.**

    function oAEC(X):
        G = XᵀX
        inv_sqrt = symmetric_pow(G, -0.5)      # via eigendecomposition
        X_perp = X @ inv_sqrt
        env = abs(hilbert(X_perp))
        C = corrcoef(env)                       # Gram, PSD by construction
        return spd_guard(C)

**Computational considerations.** The dominant cost is the eigendecomposition of the C×C Gram matrix
(C = 19, negligible) and the Hilbert transform over W samples. Per-window cost is low; the pipeline
parallelises over windows.

## Algorithm 2 — SPD Guard

**Status.** Implemented.

**Purpose.** Enforce positive definiteness and quantify any violation.

**Inputs.** Symmetric matrix **C**; floor ε = 1e-6.

**Outputs.** PSD matrix; integrity statistics (n_not_psd, min raw eigenvalue, L1 correction).

**Logic.**

1. Eigendecompose **C** = U Λ Uᵀ.
2. If min(Λ) < ε, clip: Λ' = max(Λ, ε).
3. Reconstruct **C**' = U Λ' Uᵀ.
4. Record whether a correction was applied and its magnitude.

**Pseudocode.**

    function spd_guard(C, eps=1e-6):
        U, lam = eig(C)
        n_bad = count(lam < 0)
        correction = sum(max(eps-lam, 0))
        lam_c = max(lam, eps)
        C_p = U @ diag(lam_c) @ Uᵀ
        return C_p, {n_not_psd: n_bad, min_eig_raw: min(lam), correction: correction}

## Algorithm 3 — Fréchet Mean and Tangent Projection

**Status.** Implemented.

**Purpose.** Move connectivity matrices into a linear tangent space at a geometrically valid reference.

**Inputs.** Set {**C**₁,…,**C**ₘ} of connectivity matrices.

**Outputs.** Reference mean **S**; tangent vectors.

**Logic.**

1. Compute the Fréchet (geometric) mean **S** by iterative fixed-point: **S** ← **S**^{1/2}
   (1/m Σ **S**^{-1/2} **C**ᵢ **S**^{-1/2}) **S**^{1/2}, until convergence.
2. Project each matrix to the tangent space:
   **T**ᵢ = **S**^{1/2} log(**S**^{-1/2} **C**ᵢ **S**^{-1/2}) **S**^{1/2}.

**Pseudocode.**

    function frechet_mean(C_list):
        S = eye(C)
        repeat:
            S_next = S^{1/2} @ mean(S^{-1/2} @ C_i @ S^{-1/2}) @ S^{1/2}
            until ||S_next - S|| < tol
        return S

    function tangent_project(C, S):
        M = S^{-1/2} @ C @ S^{-1/2}
        return S^{1/2} @ logm(M) @ S^{1/2}

**Computational considerations.** 19×19 matrices make the matrix exponential/log and square roots
cheap. The Fréchet mean converges in few iterations. All operations must be preceded by the SPD guard.

## Algorithm 4 — Alignment Arms

**Status.** Implemented (ablation harness).

**Purpose.** Compare alignment strategies to quantify the alignment–signal trade-off.

**Inputs.** Windowed signals; per-subject grouping.

**Outputs.** Aligned representations per arm.

**Logic.**

- **None:** no alignment.
- **Euclidean (EA):** subtract each subject's signal-space mean.
- **Riemannian:** rotate each subject's covariance to identity by **S**^{-1/2} (re-centering).
- **Band-limited Riemannian:** Riemannian re-centering per band.

**Computational considerations.** Alignment is the suspected cause of trait-signal deletion; the arms
are the ablation that measures it (hypothesis H1).

## Algorithm 5 — SpecParam Aperiodic Fit

**Status.** Implemented (fit); acceptance criterion applied.

**Purpose.** Estimate the aperiodic exponent and offset.

**Inputs.** Power spectral density per channel-window over 1–40 Hz.

**Outputs.** Exponent χ, offset b, fit R².

**Logic.**

1. Identify and remove oscillatory peaks from the PSD.
2. Fit the aperiodic model in log-log space: log PSD(f) = b − χ·log(f).
3. Compute R²; accept if R² ≥ 0.85.

**Pseudocode.**

    function specparam(psd, freqs):
        model = linear_regression(log(freqs), log(psd))
        chi = -model.slope; b = model.intercept
        r2 = model.r2
        return chi, b, r2

## Algorithm 6 — Spatial Graph Attention (GATv2)

**Status.** Designed.

**Purpose.** Encode cortical topology.

**Inputs.** Node features **h**ᵢ ∈ ℝ^{d}; adjacency from the 10–20 montage.

**Outputs.** Updated node features.

**Logic.**

1. For each edge (i,j): e_ij = aᵀ LeakyReLU(W [h_i ‖ h_j]).
2. Normalise over neighbours: α_ij = softmax_j(e_ij).
3. Aggregate: h'_i = σ(Σ_j α_ij W h_j).
4. Apply a learnable sparse edge gate over the adjacency.

## Algorithm 7 — Evidence Gate

**Status.** Designed (proposed policy not finalised).

**Purpose.** Decide accept/abstain.

**Inputs.** AQI; coverage target κ; calibration reliability.

**Outputs.** τ ∈ {accept, abstain}.

**Proposed logic.**

    function evidence_gate(AQI, kappa, calib):
        threshold = f(kappa)                    # coverage-linked threshold
        if AQI < threshold or calib.unreliable: return abstain
        return accept

The exact functional form of f(kappa) is **not yet specified**.

## Algorithm 8 — Artifact-Paired Evaluation

**Status.** Implemented (artifact-only arm); artifact-controlled arm designed.

**Purpose.** Quantify the artifact confound.

**Inputs.** Cohort; folds.

**Outputs.** Artifact-only AUROC; artifact-controlled AUROC; neural AUROC.

**Logic.**

1. Define artifact proxies: duration, blink-band amplitude, muscle-band ratio, global amplitude.
2. Fit an artifact-only model on identical folds → artifact-only AUROC.
3. Regress proxies out of the neural feature space (or stratify by proxy) → artifact-controlled AUROC.
4. Report all three together.

## Unspecified / Proposed Algorithms

- The exact calibration method (isotonic vs temperature scaling) is **not yet specified**.
- The exact evidence-gate threshold function is **not yet specified**.
- The split-half stability metric for Panel 3 is **not yet finalised** (candidate: split-half ICC).
