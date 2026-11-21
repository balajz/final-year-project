# 12 — Mathematical and Theoretical Foundations

## Notation

| Symbol | Meaning |
|---|---|
| **X** ∈ ℝ^{C×N} | Multichannel signal matrix: C channels, N samples |
| **X**⊥ | Orthogonalised channel matrix |
| **G** = **X**ᵀ**X** | Gram (channel second-moment) matrix |
| **C** ∈ 𝒮_{++}^{C} | Symmetric positive definite covariance/correlation matrix |
| **S** | Fréchet (geometric) reference mean |
| **T** | Tangent-space vector representation |
| χ | Aperiodic exponent (1/f slope magnitude) |
| b | Aperiodic offset (intercept in log-log space) |
| π | Screening prevalence |
| Se, Sp | Sensitivity, specificity |
| p̂ | Calibrated predicted probability |
| τ | Evidential state ∈ {accept, abstain} |
| κ | Coverage target |
| α_ij | Graph attention coefficient |

## 1. Global Joint Löwdin Orthogonalisation

The orthogonalised channel matrix is

    **X**⊥ = **X** (**X**ᵀ**X**)^{−1/2} = **X** **G**^{−1/2},

where **G**^{−1/2} is the inverse symmetric square root obtained from the eigendecomposition
**G** = **U** **Λ** **U**ᵀ as **G**^{−1/2} = **U** **Λ**^{−1/2} **U**ᵀ.

**Property (whiteness).**

    **X**⊥ **X**⊥ᵀ = **X** **G**^{−1/2} **G**^{−1/2} **X**ᵀ = **X** **G**^{−1} **X**ᵀ = **I**_C.

So the orthogonalised channels are mutually uncorrelated at zero lag. Any remaining correlation in
their Hilbert envelopes is therefore attributable to lagged amplitude interaction rather than
instantaneous volume conduction.

**Property (positive semi-definiteness).** The envelope correlation matrix

    **C** = Corr(**E**),  where **E** = |Hilbert(**X**⊥)|

is the correlation matrix of real vectors and is therefore a Gram matrix with non-negative eigenvalues
by construction. This is the formal justification for the design choice: a correlation matrix of a
genuine vector set cannot be indefinite.

**Contrast with pairwise symmetricalisation.** Pairwise orthogonalised envelope correlation
orthogonalises each channel pair independently and then averages scalar correlations. The resulting
matrix is not the Gram matrix of any common vector set and carries no definiteness guarantee. On
band-limited data the effective rank of the Gram matrix collapses, and the averaged matrix can exhibit
negative eigenvalues.

## 2. SPD Guard

Given **C** with eigendecomposition **C** = **U** **Λ** **U**ᵀ and floor ε:

    **C**' = **U** · diag(max(λ_j, ε)) · **U**ᵀ,  Λ = diag(λ_j).

Correction magnitude recorded as

    Δ = Σ_j max(ε − λ_j, 0),  and  n_not_psd = |{j : λ_j < 0}|.

## 3. Riemannian Geometry of 𝒮_{++}^{C}

The manifold 𝒮_{++}^{C} with the affine-invariant metric

    d(**A**, **B**) = ‖log(**A**^{−1/2} **B** **A**^{−1/2})‖_F

supports the following operations.

**Exponential map** from the tangent space at **S**:

    Exp_**S**(**T**) = **S**^{1/2} exp(**S**^{−1/2} **T** **S**^{−1/2}) **S**^{1/2}.

**Logarithmic map** to the tangent space at **S**:

    Log_**S**(**C**) = **S**^{1/2} log(**S**^{−1/2} **C** **S**^{−1/2}) **S**^{1/2}.

**Fréchet mean.** The geometric mean of {**C**₁,…,**C**ₘ} is

    **S** = argmin_{**S**∈𝒮_{++}} Σᵢ d²(**S**, **C**ᵢ),

computed by the fixed-point iteration

    **S**_{k+1} = **S**_k^{1/2} · (1/m Σᵢ **S**_k^{−1/2} **C**ᵢ **S**_k^{−1/2}) · **S**_k^{1/2}.

**Tangent feature vectorisation.** The tangent vectors are vectorised (upper triangle) to form the
feature vector used by linear models.

## 4. Alignment Operators

**Euclidean alignment.** For subject s with mean covariance over its windows,

    **R**_s = (1/M) Σ_{m=1}^{M} **C**_s^{(m)},

each matrix is whitened as

    **C**̃_s^{(m)} = **R**_s^{−1/2} **C**_s^{(m)} **R**_s^{−1/2}.

**Riemannian re-centering.** Identical in form but applied in the manifold using the Fréchet mean as
**R**_s.

**Formal note on information loss.** Whitening by **R**_s^{−1/2} removes all subject-specific
first-/second-order structure. Any diagnostic signal carried in **R**_s itself — rather than in
within-subject variation about it — is annihilated by construction. This is the formal statement of
the trait-deletion risk that motivates the dual-path design (Section 5).

## 5. Spectral Model (Aperiodic/Periodic Separation)

The power spectral density is modelled as

    PSD(f) = L(f) + Σₙ Gₙ(f),

with the aperiodic component in log-power space

    L(f) = b − χ · log(f),

and periodic components modelled as Gaussian bumps in log-power space. The exponent χ is the quantity
extracted for the trait path.

**Gain invariance.** Under a multiplicative gain g on the signal, the PSD scales by g², so

    log PSD'(f) = log PSD(f) + 2 log g.

The additive constant affects only b; the slope −χ is unchanged. Hence χ is invariant to vertical gain
offset — the property motivating its use as a trait feature.

## 6. Dual-Path Fusion

Let **z**_i^{trait} ∈ ℝ^{d_t} be node i's trait features (derived from χ) and **z**_i^{state} ∈ ℝ^{d_s}
its state features (derived from aligned connectivity). The fused node feature is

    **h**_i = φ( [ **z**_i^{trait} ‖ **z**_i^{state} ] ),

where φ is a learned linear or non-linear projection. This is a **proposed** formulation; the exact
combination operator is not yet finalised.

## 7. Graph Attention (GATv2)

For node i and neighbour j:

    e_ij = **a**ᵀ · LeakyReLU( **W** [**h**_i ‖ **h**_j] ),
    α_ij = softmax_{j∈𝒩(i)} (e_ij),
    **h**'_i = σ( Σ_{j∈𝒩(i)} α_ij **W** **h**_j ).

A learnable sparse gate g_ij ∈ [0,1] modulates the adjacency:

    α_ij ← α_ij · g_ij.

The five-lobe partition defines a structured prior over 𝒩(i).

## 8. Calibration and Predictive Value

**Positive predictive value.** For prevalence π, sensitivity Se, specificity Sp:

    PPV(π) = (Se · π) / ( Se · π + (1 − Sp)(1 − π) ).

**Expected calibration error.** With B bins of predicted probability and bin frequencies n_b:

    ECE = Σ_{b=1}^{B} (n_b / n) · | acc(b) − conf(b) |.

**Brier score.**

    Brier = (1/n) Σ_i ( p̂_i − y_i )².

**Risk–coverage.** For a coverage level c (fraction of recordings retained after gating), define
selective risk

    Risk(c) = E[ ℓ(p̂, y) | recording retained ],

and report Risk(c) jointly with specificity(c) and PPV(c) to make abstention auditable.

## 9. Permutation Null

For B permutations π_b of the participant-level labels, the null distribution of the statistic Â is

    { Â(π_b) },  and the corrected p-value is

    p = ( 1 + #{ b : Â(π_b) ≥ Â_obs } ) / ( 1 + B ).

## 10. Formal Statement of the Optimization Objective

The project's objective is not to maximise AUROC but to maximise specificity subject to a bounded
change in discrimination:

    maximise  Sp(θ; τ_fixed)
    subject to | AUROC(θ) − AUROC_baseline | ≤ δ,
               τ = 0.80 (fixed sensitivity),
               θ ∈ Θ (model and gate parameters).

The constraint is what makes the result interpretable: any specificity gain must come from calibration
and abstention rather than from a differently-capable classifier.

## 11. Not Yet Formalised

- The functional form of the AQI scalar aggregation.
- The gate threshold function f(κ).
- The stability metric for Panel 3 (candidate: split-half intraclass correlation).
