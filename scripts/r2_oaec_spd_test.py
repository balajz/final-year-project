"""R2 verification: is orthogonalised Amplitude Envelope Correlation (oAEC) positive semi-definite?

Two constructions are tested side by side, because the vault's Trap 1 and the real-world
implementations (MNE-CPP ConnectivityAec, Brainstorm HENV) describe DIFFERENT objects:

  A. PAIRWISE-SYMMETRISED oAEC  (what the libraries actually implement)
     For each pair (i,j): orthogonalise j w.r.t. i -> envelope corr  r_ij
                         orthogonalise i w.r.t. j -> envelope corr  r_ji
                         store (|r_ij| + |r_ji|)/2
     This is an AVERAGE OF SCALARS, not a Gram matrix. No PSD guarantee.

  B. GLOBALLY-ORTHOGONALISED AEC  (what the vault's Trap 1 claims)
     Orthogonalise ALL channels jointly via symmetric (Löwdin) orthogonalisation
     X_perp = X (X^T X)^{-1/2}, THEN take envelope correlation.
     Envelope correlation of ACTUAL VECTORS is a correlation matrix of real data,
     hence Gram => PSD. This is the only version that can be provably PSD.

Run:  python3 r2_oaec_spd_test.py
"""
import numpy as np

RNG = np.random.default_rng(20261116)

# ----------------------------------------------------------------------------- helpers
def bandpass(x, fs, lo, hi, order=4):
    """Zero-phase Butterworth-equivalent via FFT masking (no scipy needed)."""
    n = x.shape[-1]
    X = np.fft.rfft(x, axis=-1)
    f = np.fft.rfftfreq(n, 1 / fs)
    mask = ((f >= lo) & (f <= hi)).astype(float)
    # soft edges to avoid ringing
    return np.fft.irfft(X * mask, n=n, axis=-1)


def hilbert_env(x):
    """Analytic-signal envelope via FFT (matches scipy.signal.hilbert |.|)."""
    n = x.shape[-1]
    X = np.fft.fft(x, axis=-1)
    h = np.zeros(n)
    h[0] = 1
    if n % 2 == 0:
        h[n // 2] = 1
        h[1:n // 2] = 2
    else:
        h[1:(n + 1) // 2] = 2
    return np.abs(np.fft.ifft(X * h, axis=-1))


def corr_matrix(E):
    """Pearson correlation between rows of E (channels x samples)."""
    Ec = E - E.mean(axis=1, keepdims=True)
    C = (Ec @ Ec.T) / (Ec.shape[1] - 1)
    sd = np.sqrt(np.diag(C))
    d = np.outer(sd, sd)
    d[d == 0] = 1e-12
    return C / d


def lowdin(X):
    """Symmetric (Löwdin) orthogonalisation: X_perp = X (X^T X)^(-1/2)."""
    R = X @ X.T  # channels x channels
    w, V = np.linalg.eigh(R)
    w = np.clip(w, 1e-12, None)
    Rm_half = (V * (w ** -0.5)) @ V.T
    return Rm_half @ X


def oaec_pairwise(X, eps=1e-10):
    """Construction A: pairwise orthogonalisation, symmetrised by averaging |.|."""
    E = hilbert_env(X)
    n_ch = X.shape[0]
    M = np.zeros((n_ch, n_ch))
    for i in range(n_ch):
        for j in range(n_ch):
            if i == j:
                M[i, j] = 1.0
                continue
            # orthogonalise j w.r.t. i:  j_perp = j - (j.i/|i|^2) i
            xi, xj = X[i], X[j]
            xj_perp = xj - (xj @ xi / (xi @ xi)) * xi
            r_ij = np.corrcoef(E[i], hilbert_env(xj_perp[None, :])[0])[0, 1]
            xi_perp = xi - (xi @ xj / (xj @ xj)) * xj
            r_ji = np.corrcoef(hilbert_env(xi_perp[None, :])[0], E[j])[0, 1]
            M[i, j] = (abs(r_ij) + abs(r_ji)) / 2
    np.fill_diagonal(M, 1.0)
    return M


def aec_global_lowdin(X):
    """Construction B: global Löwdin orthogonalisation, then envelope correlation."""
    return corr_matrix(hilbert_env(lowdin(X)))


def plain_aec(X):
    """Naive AEC (the base paper's starting point): envelope correlation, no correction."""
    return corr_matrix(hilbert_env(X))


# ----------------------------------------------------------------------------- scenarios
def make_signals(kind, n_ch=19, n_samp=512, fs=128):
    """Return (X, note). X is channels x samples."""
    t = np.arange(n_samp) / fs
    if kind == "independent":
        X = RNG.standard_normal((n_ch, n_samp))
    elif kind == "volume_conduction":
        # one deep source, mixed into every channel with channel-dependent gain
        src = np.sin(2 * np.pi * 10 * t + RNG.uniform(0, 2 * np.pi))
        src = src + 0.5 * RNG.standard_normal(n_samp)
        gain = RNG.uniform(0.6, 1.0, n_ch)
        mix = RNG.normal(0, 0.15, (n_ch, n_ch))
        X = np.outer(gain, src) + mix @ np.outer(np.ones(n_ch), src) * 0.2
        X = X + 0.4 * RNG.standard_normal((n_ch, n_samp))
    elif kind == "two_sources":
        s1 = np.sin(2 * np.pi * 9 * t) + 0.3 * RNG.standard_normal(n_samp)
        s2 = np.sin(2 * np.pi * 21 * t + 1.1) + 0.3 * RNG.standard_normal(n_samp)
        A = RNG.normal(0, 0.4, (n_ch, 2))
        X = A @ np.vstack([s1, s2]) + 0.5 * RNG.standard_normal((n_ch, n_samp))
    elif kind == "few_samples":
        # short window: FEWER samples than channels -- the pathological case.
        # Use broadband noise (no band-pass) so channels are not all-zero after filtering.
        n_samp = 12
        X = RNG.standard_normal((n_ch, n_samp))
        return X - X.mean(axis=1, keepdims=True)
    else:
        raise ValueError(kind)
    X = bandpass(X, fs, 8, 13)  # alpha band, a realistic connectivity band
    X = X - X.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, keepdims=True)
    sd[sd == 0] = 1
    return X / sd


def evaluate(M, name):
    if not np.all(np.isfinite(M)):
        return dict(name=name, min_eig=np.nan, max_eig=np.nan, n_neg=0,
                    n_ch=M.shape[0], nan=True)
    M = (M + M.T) / 2.0                      # guarantee symmetry before eigvalsh
    try:
        w = np.linalg.eigvalsh(M)
    except np.linalg.LinAlgError:
        return dict(name=name, min_eig=np.nan, max_eig=np.nan, n_neg=0,
                    n_ch=M.shape[0], nan=True)
    return dict(name=name, min_eig=w.min(), max_eig=w.max(),
                n_neg=int((w < -1e-9).sum()), n_ch=M.shape[0], nan=False)


# ----------------------------------------------------------------------------- run
def main():
    trials = 200
    scenarios = ["independent", "volume_conduction", "two_sources", "few_samples"]
    methods = [("plain AEC (baseline)", plain_aec),
               ("A pairwise-sym oAEC", oaec_pairwise),
               ("B global Löwdin AEC", aec_global_lowdin)]

    print("=" * 88)
    print("R2: Is oAEC positive semi-definite?  19 channels, alpha band, 200 trials/scenario")
    print("=" * 88)

    results = {}
    for sc in scenarios:
        print(f"\n--- scenario: {sc} ---")
        print(f"{'method':<26} {'min eig (mean)':>15} {'worst eig':>11} {'trials w/ neg':>14}")
        for mname, fn in methods:
            mins, negs, nans = [], 0, 0
            for _ in range(trials):
                X = make_signals(sc)
                r = evaluate(fn(X), mname)
                if r["nan"]:
                    nans += 1
                    continue
                mins.append(r["min_eig"])
                negs += int(r["n_neg"] > 0)
            if not mins:
                print(f"{mname:<26} {'NaN (degenerate)':>15} {'-':>11} {nans:>10}/{trials}  <-- DEGENERATE")
                results[(sc, mname)] = (np.nan, np.nan, trials)
                continue
            mins = np.array(mins)
            results[(sc, mname)] = (mins.mean(), mins.min(), negs)
            flag = "  <-- NOT PSD" if negs else ""
            if nans:
                flag += f"  (+{nans} degenerate)"
            print(f"{mname:<26} {mins.mean():>15.2e} {mins.min():>11.2e} {negs:>10}/{trials}{flag}")

    # ---------------------------------------------------------------- verdict
    print("\n" + "=" * 88)
    print("VERDICT")
    print("=" * 88)
    pw = [results[(sc, "A pairwise-sym oAEC")] for sc in scenarios]
    gl = [results[(sc, "B global Löwdin AEC")] for sc in scenarios]
    pw_fail = sum(1 for m, w, n in pw if n > 0)
    gl_fail = sum(1 for m, w, n in gl if n > 0)
    print(f"Construction A (pairwise-symmetrised, what libraries implement): "
          f"{pw_fail}/{len(scenarios)} scenarios produced negative eigenvalues")
    print(f"Construction B (global Löwdin, what Trap 1 claims):            "
          f"{gl_fail}/{len(scenarios)} scenarios produced negative eigenvalues")

    if pw_fail > 0:
        print("\n=> Trap 1's claim is FALSE for the oAEC that MNE-CPP / Brainstorm produce.")
        print("   Stage 3 must NOT consume pairwise-symmetrised oAEC as an SPD matrix.")
    if gl_fail == 0:
        print("\n=> Trap 1's claim holds ONLY for the globally-orthogonalised construction.")
        print("   The fix is to orthogonalise all channels jointly (Löwdin), then correlate")
        print("   envelopes -> the matrix is a correlation matrix of real vectors -> PSD by construction.")
    elif gl_fail < len(scenarios):
        print("\n=> Global Löwdin also risks failure in some regimes (short windows);")
        print("   prefers an explicit eigenvalue check + projection before tangent-space mapping.")

    print("\nSmallest eigenvalue observed overall:")
    print(f"  pairwise-sym oAEC worst-case min eig: "
          f"{min(r[1] for r in pw if not np.isnan(r[1])):.3e}")


if __name__ == "__main__":
    main()
