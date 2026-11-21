# 08 — Detailed Module Descriptions

## Module 1 — Ingest

**Purpose.** Convert any supported input into a canonical in-memory recording.

**Responsibilities.** Schema validation; channel-name resolution; missing-channel handling; sampling-rate
check; provenance recording.

**Inputs.** File path to `.csv`, `.set`, `.bdf`, `.edf`, or `.fif`; channel-label table.

**Processing logic.**

1. Detect format from extension/magic.
2. Read time series and channel labels.
3. Resolve labels through the bidirectional mapping to canonical 19-channel order.
4. Apply median imputation for missing channels; record which were imputed.
5. Emit provenance: format, original labels, resampling applied, imputed channels.

**Outputs.** Matrix **X** ∈ ℝ^{19×N}; provenance record.

**Dependencies.** Canonical montage definition.

**Interactions.** Supplies L2 (quality) and L3 (preprocessing).

---

## Module 2 — Artifact Quality Index (AQI)

**Purpose.** Quantify the recording's contamination and identify per-window quality.

**Responsibilities.** Muscle-burden estimate; blink-burden estimate; global amplitude dispersion;
flatline/clipping detection; per-window quality vector; scalar AQI.

**Inputs.** Canonical matrix; band definitions.

**Processing logic.**

- Muscle ratio: log(EMG-band power / low-band power), EMG band 30–60 Hz.
- Blink amplitude: log of blink-band (≈1–4 Hz) envelope amplitude, frontal channels weighted.
- Amplitude: log global standard deviation.
- Flatline: channel variance below 1e-10.
- Clipping: fraction of samples at the ADC rails.
- Combine into a scalar AQI (defined functional form: *not yet finalised*).

**Outputs.** AQI scalar; per-window quality vector.

**Dependencies.** Band definitions.

**Interactions.** Consumed by the decision component (abstention) and by Panel 2 (timeline, risk–coverage).

---

## Module 3 — Preprocessing

**Purpose.** Clean, segment, and decompose the signal.

**Responsibilities.** Trend removal; bad-channel rule; band separation; segmentation; SpecParam fit.

**Inputs.** Canonical matrix; reference bad-channel thresholds; band edges; SpecParam acceptance.

**Processing logic.**

1. Detrend / high-pass.
2. Apply reference bad-channel rule:
   - robust deviation: MAD-based z > 5.0;
   - neighbour correlation: max |r| < 0.40;
   - predictability: R² < 0.75;
   - flatline: variance < 1e-10.
3. Segment into 4-second windows; group into 10-window sequences.
4. Band-pass each window into contiguous bands: delta 0.5–4, theta 4–8, alpha 8–13, beta 13–30,
   gamma 30–45 Hz.
5. Fit the spectral model over 1–40 Hz; accept fits with R² ≥ 0.85; emit exponent χ and offset A per
   channel per window.

**Outputs.** Band-limited window signals; exponent/offset arrays; per-window acceptance flags.

**Dependencies.** Band definitions; SpecParam implementation.

**Interactions.** Supplies connectivity and representation modules.

---

## Module 4 — Connectivity (Joint Löwdin oAEC)

**Purpose.** Compute echo-suppressed connectivity that is positive semi-definite by construction.

**Responsibilities.** Joint orthogonalisation; envelope extraction; correlation; SPD guard.

**Inputs.** Band-limited window signals.

**Processing logic.**

1. For a window, form the channel matrix and compute the orthogonalised version
   **X**⊥ = **X**(**X**ᵀ**X**)⁻¹ᐟ².
2. Extract the Hilbert envelope of each orthogonalised channel.
3. Compute the Pearson correlation of envelopes → connectivity matrix.
4. Pass through the SPD guard: eigendecompose, clip eigenvalues below ε = 1e-6, record the L1
   correction magnitude, `n_not_psd`.

**Outputs.** Connectivity matrix; SPD integrity statistics.

**Dependencies.** Band signals.

**Interactions.** Supplies geometry and the integrity line in Panel 2.

---

## Module 5 — Geometry

**Purpose.** Move connectivity matrices into a linear working space.

**Responsibilities.** Fréchet mean; tangent projection; alignment arms.

**Inputs.** Connectivity matrices.

**Processing logic.**

- Compute the Fréchet (geometric) mean **S** of the reference set.
- Tangent projection: **T** = **S**^{1/2} log(**S**^{−1/2} **C** **S**^{−1/2}) **S**^{1/2}.
- Alignment arms (ablation): none; Euclidean alignment (remove per-subject mean in signal space);
  Riemannian re-centering (rotate to identity by **S**^{−1/2}); band-limited Riemannian.

**Outputs.** Tangent vectors; aligned matrices.

**Dependencies.** Connectivity output; SPD guard.

**Interactions.** Supplies state path of the representation module.

---

## Module 6 — Representation (Dual-Path)

**Purpose.** Assemble node features carrying both gain-invariant and state information.

**Responsibilities.** Trait-path construction; state-path construction; fusion.

**Inputs.** Exponent array (trait); tangent vectors / aligned matrices (state).

**Processing logic.**

- Trait: the per-channel aperiodic exponent χ, appended as node features (gain-invariant).
- State: the aligned dynamic connectivity, vectorised per node.
- Fusion: learned linear combination or concatenation.

**Outputs.** Node feature tensors; edge-weight matrix.

**Dependencies.** Geometry output; SpecParam output.

**Interactions.** Supplies the encoder.

---

## Module 7 — Spatio-Temporal Encoder

**Purpose.** Learn cortical-topology-aware spatial and temporal structure.

**Responsibilities.** Graph attention over the montage; sequence encoding; participant pooling.

**Inputs.** Node features; adjacency from the 10–20 montage; 10-window sequences.

**Processing logic.**

- **Spatial (GATv2).** For edges (i,j), attention coefficient
  e_ij = aᵀ LeakyReLU(W[h_i ‖ h_j]); normalise with softmax; aggregate neighbours; apply a learnable
  sparse edge gate.
- **Temporal.** Parallel Transformer encoder and bidirectional GRU over window sequences.
- **Pooling.** Combine spatial and temporal outputs to a participant-level embedding.

**Outputs.** Participant-level embedding.

**Dependencies.** Graph construction; fused node features.

**Interactions.** Supplies the decision component and Panel 3.

---

## Module 8 — Decision (Calibration + Evidence Gate)

**Purpose.** Map the embedding to a calibrated probability and decide whether to release a prediction.

**Responsibilities.** Probability calibration; operating-point selection; abstention.

**Inputs.** Participant embedding; AQI.

**Processing logic.**

1. Linear head → logit.
2. Calibrate the probability (e.g. isotonic or temperature scaling) using training-fold statistics.
3. Select the threshold for a target sensitivity (e.g. 80%).
4. Evidence gate: if AQI below a coverage-linked threshold, or if calibration is unreliable, abstain.
5. Compute PPV at π ∈ {5%, 10%} from calibrated sensitivity and specificity.

**Outputs.** Calibrated probability p̂; evidential state τ ∈ {accept, abstain}; operating point; PPVs.

**Dependencies.** Calibration statistics; AQI.

**Interactions.** Supplies all three panels.

---

## Module 9 — Presentation

**Purpose.** Render the decision with an audit trail.

**Responsibilities.** Three-panel rendering; integrity and attrition reporting; reproducibility badge.

**Inputs.** Result record.

**Processing logic.** Read-only; no inference. Computes derived views (risk–coverage curve, attrition
table, graph with split-half stability).

**Outputs.** Three rendered panels (HTML for offline viewing).

**Dependencies.** Result record.

**Interactions.** None downstream.

---

## Cross-Cutting — Reproducibility Ledger

Records pipeline version, preprocessing config hash, model checkpoint hash, and seed. Attached to every
output record and displayed in Panel 2.
