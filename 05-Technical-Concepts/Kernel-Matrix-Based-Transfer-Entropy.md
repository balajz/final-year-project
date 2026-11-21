---
tags:
  - technical-concept
  - connectivity
  - information-theory
  - kernel-methods
  - differentiable
---

# Kernel / Matrix-Based Transfer Entropy (Differentiable TE)

Synthesized from [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]] and its lineage (De La Pava Panche et al.; kernelized Phase Transfer Entropy; TEKTE-Net).

## 1. Why Matrix-Based Entropy
Classical TE needs conditional probability density estimation, which is brittle at the sample sizes available per EEG window. The kernel trick replaces densities with **Gram matrices**: for samples $\{z_i\}_{i=1}^{n}$, build $K_{ij} = \kappa(z_i, z_j)$, trace-normalize, and read entropy off the eigenspectrum.

For $\mathcal{N}(A) = A / \mathrm{tr}(A)$ and PSD $A$:

$$H_{\alpha_R}(A) = \frac{1}{1-\alpha_R}\,\log \mathrm{tr}\!\left(\mathcal{N}(A)^{\alpha_R}\right)$$

Joint entropy of several variables uses the Hadamard product, $H(K_1,\dots,K_M) = H(K_1 \odot \cdots \odot K_M)$, which is valid because products of PSD kernels are PSD.

**Kernel used in CTE-Net:** rational quadratic, $\kappa(z_i,z_j) = a^2\left(1 + \frac{\lVert z_i-z_j\rVert^2}{2\alpha_{RQ}\ell^2}\right)^{-\alpha_{RQ}}$ — a scale mixture of RBF kernels, i.e. a continuum of length scales rather than one bandwidth.

## 2. The TE Decomposition
With source past $x^-$, target past $y^-$, target present $y$:

$$TE_{c\to c'} = H(y^-,x^-) - H(y,y^-,x^-) + H(y,y^-) - H(y^-)$$

All four terms are differentiable → gradients flow back into the signal representation, so "connectivity" is *learned jointly* with the classifier. Plausible causal reading requires additional assumptions; the estimator measures **directed predictive information** only.

## 3. Where This Breaks (earned from the critique)
1. **Direction confounding under channel mixing.** If the "source" and "target" signals are outputs of a block where every channel already contains all other channels (self-attention projected back to channel space), $c\to c'$ asymmetry is partly manufactured by the mixing. *Mitigation:* estimate TE on non-mixed signals, add a channel-shuffled null, or mask attention per-channel and check stability.
2. **Lag units.** Always report $\tau,\mu$ in **milliseconds** together with the effective sampling rate of the embedded signal. A pooled representation may run at 16–32 Hz, changing the meaning of "$\mu=2$" by an order of magnitude. State the physiological band the lag range can even represent (theta cycle = 125–250 ms).
3. **Single-lag TE is not TE.** $D_y=1$, $D_x$ small, one $\mu$ → a nonlinear lag-specific predictive test. Fine as a feature, misleading if described as full transfer entropy.
4. **Sampling variability.** $n \approx$ number of Takens anchors inside one 4 s window ($\sim10^2$), strongly autocorrelated → effective $n$ much smaller; entropy estimators are biased at these sizes. Negative TE values (10% in CTE-Net) are the visible symptom. Never interpret a negative coefficient as "negative information flow".
5. **Non-negativity is not enforced.** Do not clip silently; report the fraction and the range (CTE-Net: −0.0801 to 0.5156).
6. **PSD bookkeeping.** Positivity constraints on $a,\ell,\alpha_{RQ}$ and an $\varepsilon$ floor are required for stable log/trace operations; claim PSD preservation only for positive parameters and Hadamard products.
7. **Everything passes through the bottleneck.** When the classifier head consumes *only* the TE vector, high accuracy proves "this statistic is discriminative", **not** "directed connectivity is the mechanism". Always pair with a raw/static-TE and a surrogate control.

## 4. Minimal Validation Checklist
- [ ] TE computed on raw vs contextualized signals (does learning the representation matter?)
- [ ] Fixed/random-projection TE control (does *learning* the kernel projections matter?)
- [ ] Phase-randomized / time-shuffled surrogate null (does *direction* matter?)
- [ ] Channel-permutation null (does *topology* matter?)
- [ ] Convergence: TE vs number of anchors; report mean ± SD across repeated subsampling
- [ ] Lag sweep reported in ms, including at least one theta-scale lag
- [ ] Stability: per-window vs participant-mean Spearman + top-$k$% Jaccard
- [ ] Reference sensitivity (linked mastoid vs CAR) — edge agreement, not just accuracy

## 5. Connections
- Papers: [[GomezRivera-2026-CTE-Net-Directed-TE-ADHD]]
- Concepts: [[Dynamic-Functional-Connectivity]], [[Representation-Dispersion-and-Stability]]
- Opportunities: [[ADHD-Child-Audit-and-Temporal-Scale-Gaps]]
