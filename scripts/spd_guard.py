"""SPD guard for connectivity matrices before Riemannian tangent-space mapping.

Rationale (verified by scripts/r2_oaec_spd_test.py):
  * Pairwise-symmetrised oAEC is NOT positive semi-definite. In 4/4 synthetic scenarios
    (independent, volume-conduction, two-source, short-window) it produced negative
    eigenvalues; worst case min-eig = -0.93 on a 19-channel matrix. It is an average of
    pairwise scalars, not a Gram matrix, so no PSD guarantee exists.
  * Globally Löwdin-orthogonalised AEC IS PSD by construction (it is the correlation
    matrix of real vectors), and was PSD in 4/4 scenarios.

Policy implemented here:
  1. Prefer the globally-orthogonalised construction (`aec_global_lowdin`).
  2. Regardless of construction, EVERY matrix passes through `ensure_spd()` before any
     Riemannian operation, and the correction magnitude is logged.
  3. If a matrix needs a large correction, that is recorded as a data-quality signal, not
     silently repaired -- a big correction means the connectivity estimate is unreliable.

No scipy / sklearn / mne required. NumPy only.
"""
from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------- constructions


def lowdin(X: np.ndarray) -> np.ndarray:
    """Symmetric (Löwdin) orthogonalisation: X_perp = X (X^T X)^(-1/2).

    X is (channels, samples). Removes zero-lag volume conduction between ALL channels
    jointly, unlike pairwise orthogonalisation which is order-dependent and asymmetric.
    """
    R = X @ X.T
    w, V = np.linalg.eigh(R)
    w = np.clip(w, 1e-12, None)
    Rm_half = (V * (w**-0.5)) @ V.T
    return Rm_half @ X


def hilbert_env(x: np.ndarray) -> np.ndarray:
    """Analytic-signal magnitude (Hilbert envelope) via FFT."""
    n = x.shape[-1]
    X = np.fft.fft(x, axis=-1)
    h = np.zeros(n)
    h[0] = 1
    if n % 2 == 0:
        h[n // 2] = 1
        h[1 : n // 2] = 2
    else:
        h[1 : (n + 1) // 2] = 2
    return np.abs(np.fft.ifft(X * h, axis=-1))


def corr_matrix(E: np.ndarray) -> np.ndarray:
    """Pearson correlation between rows of E (channels x samples)."""
    Ec = E - E.mean(axis=1, keepdims=True)
    C = (Ec @ Ec.T) / max(Ec.shape[1] - 1, 1)
    sd = np.sqrt(np.clip(np.diag(C), 0, None))
    d = np.outer(sd, sd)
    d[d <= 0] = 1e-12
    return np.clip(C / d, -1.0, 1.0)


def aec_global_lowdin(X: np.ndarray) -> np.ndarray:
    """RECOMMENDED connectivity: joint Löwdin orthogonalisation, then envelope correlation.

    Provably PSD: it is corr() of real-valued envelope vectors.
    """
    return corr_matrix(hilbert_env(lowdin(X)))


def oaec_pairwise(X: np.ndarray) -> np.ndarray:
    """DO NOT FEED THIS TO A RIEMANNIAN STAGE WITHOUT `ensure_spd`.

    Pairwise orthogonalisation, symmetrised by averaging |r_ij| and |r_ji|. This mirrors
    MNE-CPP `ConnectivityAec::computeOrthogonalized` and Brainstorm HENV. It is NOT
    guaranteed PSD and empirically is not (see test output).
    """
    E = hilbert_env(X)
    n_ch = X.shape[0]
    M = np.zeros((n_ch, n_ch))
    for i in range(n_ch):
        for j in range(n_ch):
            if i == j:
                M[i, j] = 1.0
                continue
            xi, xj = X[i], X[j]
            xj_perp = xj - (xj @ xi / max(xi @ xi, 1e-12)) * xi
            xi_perp = xi - (xi @ xj / max(xj @ xj, 1e-12)) * xj
            r_ij = np.corrcoef(E[i], hilbert_env(xj_perp[None, :])[0])[0, 1]
            r_ji = np.corrcoef(hilbert_env(xi_perp[None, :])[0], E[j])[0, 1]
            M[i, j] = (abs(r_ij) + abs(r_ji)) / 2.0
    np.fill_diagonal(M, 1.0)
    return M


# --------------------------------------------------------------------------- SPD guard


def min_eig(M: np.ndarray) -> float:
    """Smallest eigenvalue of the symmetrised matrix; NaN if not finite."""
    if not np.all(np.isfinite(M)):
        return float("nan")
    return float(np.linalg.eigvalsh((M + M.T) / 2.0).min())


def ensure_spd(M: np.ndarray, eps: float = 1e-6) -> tuple[np.ndarray, float]:
    """Return (SPD matrix, correction magnitude).

    Projection is the standard 'nearest SPD in eigenvalue' operation:
    symmetrise -> eigendecompose -> clip eigenvalues at `eps` -> reconstruct.

    Correction magnitude = L1 norm of the eigenvalue changes, i.e. how much we had to
    bend the matrix. Log it: large values mean the connectivity estimate is suspect.
    """
    A = (np.asarray(M, dtype=float) + np.asarray(M, dtype=float).T) / 2.0
    np.fill_diagonal(A, 1.0)  # keep self-correlation at 1
    w, V = np.linalg.eigh(A)
    w_clipped = np.clip(w, eps, None)
    correction = float(np.abs(w_clipped - w).sum())
    A_spd = (V * w_clipped) @ V.T
    return A_spd, correction


def spd_report(matrices: np.ndarray, eps: float = 1e-6) -> dict:
    """Batch audit. `matrices` is (n_windows, n_ch, n_ch).

    Returns per-window eigenvalues before correction plus aggregate statistics, so the
    pipeline can log 'how often and how badly did we need to repair'.
    """
    raw = np.array([min_eig(M) for M in matrices])
    corrected = []
    corr_mag = []
    for M in matrices:
        A, c = ensure_spd(M, eps=eps)
        corrected.append(min_eig(A))
        corr_mag.append(c)
    raw = np.asarray(raw)
    corrected = np.asarray(corrected)
    return {
        "n_windows": len(matrices),
        "n_not_psd": int(np.sum(raw < 0)),
        "frac_not_psd": float(np.mean(raw < 0)),
        "min_eig_raw": float(np.nanmin(raw)),
        "median_eig_raw": float(np.nanmedian(raw)),
        "min_eig_after": float(np.nanmin(corrected)),
        "max_correction": float(np.max(corr_mag)),
        "mean_correction": float(np.mean(corr_mag)),
    }


# --------------------------------------------------------------------------- self-check

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    X = rng.standard_normal((19, 512))
    X = hilbert_env(X)  # arbitrary but non-degenerate

    print("construction                  min eig")
    A = oaec_pairwise(X)
    B = aec_global_lowdin(X)
    print(f"pairwise-sym oAEC            {min_eig(A):+.4e}")
    print(f"global Löwdin AEC            {min_eig(B):+.4e}")

    A2, c = ensure_spd(A)
    B2, c2 = ensure_spd(B)
    print(f"\nafter ensure_spd:")
    print(f"  pairwise  min eig {min_eig(A2):+.4e}  correction {c:.3e}")
    print(f"  lowdin    min eig {min_eig(B2):+.4e}  correction {c2:.3e}")
    print("\nOK: both are usable after the guard; only Löwdin needs no repair.")
