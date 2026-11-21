"""R3: Does per-subject Riemannian alignment delete the ADHD signal along with the nuisance?

THE QUESTION
------------
Riemannian per-subject alignment subtracts each child's own geometric-mean covariance. That removes
every STATIC between-subject difference in mean connectivity. But most of the ADHD-EEG literature
(including the base paper's "network index") attributes the group difference to exactly such static,
sustained connectivity differences. So alignment may remove signal and nuisance together.

This script answers it empirically, on whatever data are available:

    Does alignment help SPECIFICITY without destroying AUROC?

WHY THIS IS THE DECISIVE TEST
-----------------------------
The locked project's headline claim is "specificity 44.44% -> X%". That claim only holds if alignment
buys specificity without eating the discriminative signal. If AUROC collapses under alignment, the
whole D4 upgrade is net-negative and must be redesigned (see Trap 2: dual-path trait/state).

WHAT IT REPORTS (per alignment variant, participant-level)
----------------------------------------------------------
    AUROC, AUROC delta vs no-alignment, specificity @80% sensitivity,
    balanced accuracy, sensitivity, PPV at 5% and 10% prevalence

ALIGNMENT VARIANTS
------------------
    none            : global z-score only (what Baibulova et al. do)
    euclid          : per-subject Euclidean alignment  R^-1/2 X  (R = mean of subject covariances)
    riemann         : per-subject Riemannian (tangent-space) centering of covariances
    riemann_band    : Riemannian centering restricted to alpha band only (a partial-alignment probe)

READINESS
---------
Runs TODAY on synthetic data (--synthetic) to prove the logic end to end.
Runs UNCHANGED on the real cohort the moment the CSV is on disk (--csv path).

The real CSV is the Kaggle redistribution of IEEE DataPort 10.21227/rzfh-zn36:
    columns: Fz, Cz, Pz, C3, T3, C4, T4, Fp1, Fp2, F3, F4, F7, F8, P3, P4, T5, T6, O1, O2, Class, ID
    Class in {ADHD, Control}, ID = participant id. 128 Hz, 19 channels.

Usage
-----
    python3 scripts/r3_alignment_ablation.py --synthetic
    python3 scripts/r3_alignment_ablation.py --csv data/adhd2.csv --max-subjects 121
    python3 scripts/r3_alignment_ablation.py --csv data/adhd2.csv --out results/r3.json

Dependencies: NumPy only (no scipy / sklearn / MNE).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spd_guard import ensure_spd, min_eig  # noqa: E402

FS = 128.0
WIN_SEC = 4.0
WIN_SAMPLES = int(FS * WIN_SEC)  # 512
STEP = WIN_SAMPLES // 2  # 50% overlap, matches base paper
# Canonical (modern 10-20) channel order. The Kaggle/IEEE-121 file ships these exact names.
CHANNELS = [
    "Fz", "Cz", "Pz", "C3", "T7", "C4", "T8", "Fp1", "Fp2",
    "F3", "F4", "F7", "F8", "P3", "P4", "P7", "P8", "O1", "O2",
]
# Old 10-20 aliases still seen in papers and some redistributions (R5: never hardcode one set).
ALIASES = {"T3": "T7", "T4": "T8", "T5": "P7", "T6": "P8"}
BANDS = {"theta": (4.0, 8.0), "alpha": (8.0, 13.0), "beta": (13.0, 30.0)}


# --------------------------------------------------------------------------- signal utils
def bandpass(x: np.ndarray, lo: float, hi: float, fs: float = FS) -> np.ndarray:
    """FFT-masked zero-phase band-pass (no scipy)."""
    n = x.shape[-1]
    X = np.fft.rfft(x, axis=-1)
    f = np.fft.rfftfreq(n, 1.0 / fs)
    return np.fft.irfft(X * ((f >= lo) & (f <= hi)), n=n, axis=-1)


def windows(x: np.ndarray, win: int = WIN_SAMPLES, step: int = STEP) -> np.ndarray:
    """(channels, samples) -> (n_windows, channels, win_samples). Drops a short tail."""
    n = x.shape[1]
    if n < win:
        return np.empty((0, x.shape[0], win))
    idx = range(0, n - win + 1, step)
    return np.stack([x[:, i : i + win] for i in idx], axis=0)


def cov_stack(W: np.ndarray) -> np.ndarray:
    """Per-window covariance matrices, (n_win, ch, ch). W: (n_win, ch, samples)."""
    Wc = W - W.mean(axis=2, keepdims=True)
    C = np.einsum("nct,ndt->ncd", Wc, Wc) / max(Wc.shape[2] - 1, 1)
    return C


# --------------------------------------------------------------------------- alignment
def riemann_mean(C: np.ndarray, max_iter: int = 50, tol: float = 1e-6) -> np.ndarray:
    """True Karcher (Fréchet) geometric mean on the SPD manifold under AIRM.

    Iterative gradient ascent in the tangent space:
        S_mean = (1/N) * sum_i log(M^-1/2 * C_i * M^-1/2)
        M_new = M^1/2 * exp(S_mean) * M^1/2
    """
    M = C.mean(axis=0)
    M = (M + M.T) / 2
    for _ in range(max_iter):
        w, V = np.linalg.eigh(M)
        w = np.clip(w, 1e-12, None)
        M_half = (V * np.sqrt(w)) @ V.T
        M_inv_half = (V * (1.0 / np.sqrt(w))) @ V.T

        logs = []
        for c in C:
            T = M_inv_half @ c @ M_inv_half
            T = (T + T.T) / 2
            wT, VT = np.linalg.eigh(T)
            wT = np.clip(wT, 1e-12, None)
            logT = (VT * np.log(wT)) @ VT.T
            logs.append(logT)

        S_mean = np.mean(logs, axis=0)
        step_norm = float(np.linalg.norm(S_mean))

        wS, VS = np.linalg.eigh((S_mean + S_mean.T) / 2)
        expS = (VS * np.exp(wS)) @ VS.T
        M_new = M_half @ expS @ M_half
        M_new = (M_new + M_new.T) / 2
        M = M_new
        if step_norm < tol:
            break
    return M


def align_euclid(C: np.ndarray) -> np.ndarray:
    """Euclidean alignment: whiten by the subject's arithmetic mean covariance.

    Yields SPD matrices centered around Identity in the Euclidean sense:
        (1/N) * sum_i C_tilde_i = I.
    """
    R = C.mean(axis=0)
    w, V = np.linalg.eigh((R + R.T) / 2)
    w = np.clip(w, 1e-12, None)
    Rm_half = (V * (w**-0.5)) @ V.T
    return np.array([Rm_half @ c @ Rm_half for c in C])


def align_riemann(C: np.ndarray) -> np.ndarray:
    """Riemannian alignment: whiten by the subject's Riemannian geometric mean.

    Yields SPD matrices centered around Identity in the Riemannian sense:
        GeometricMean(C_tilde_1, ..., C_tilde_N) = I.
    """
    R = riemann_mean(C)
    w, V = np.linalg.eigh((R + R.T) / 2)
    w = np.clip(w, 1e-12, None)
    Rm_half = (V * (w**-0.5)) @ V.T
    return np.array([Rm_half @ c @ Rm_half for c in C])


# --------------------------------------------------------------------------- features
def tangent_features(C: np.ndarray) -> np.ndarray:
    """Upper-triangular tangent-space vector per window (171 dims for 19 channels)."""
    n_ch = C.shape[1]
    iu = np.triu_indices(n_ch, k=1)
    feats = []
    for c in C:
        Cs, _ = ensure_spd(c)                     # R2 guard: never log-map a non-PSD matrix
        w, V = np.linalg.eigh(Cs)
        logC = (V * np.log(np.clip(w, 1e-12, None))) @ V.T
        feats.append(logC[iu])
    return np.array(feats)


def band_connectivity_features(W: np.ndarray) -> np.ndarray:
    """Mean inter-channel correlation per band, as a flat vector (n_win, 3*171).

    This is a proxy for the oAEC connectivity input; correlation is used here because R3 is about
    ALIGNMENT (D4), not about volume conduction (D2, resolved separately in R2).
    """
    n_ch = W.shape[1]
    iu = np.triu_indices(n_ch, k=1)
    out = []
    for band, (lo, hi) in BANDS.items():
        Xb = bandpass(W, lo, hi)
        Xc = Xb - Xb.mean(axis=2, keepdims=True)
        sd = Xc.std(axis=2, keepdims=True)
        sd[sd == 0] = 1.0
        Xc = Xc / sd
        r = np.einsum("nct,ndt->ncd", Xc, Xc) / max(W.shape[2] - 1, 1)
        out.append(r[:, iu[0], iu[1]])
    return np.concatenate(out, axis=1)


# --------------------------------------------------------------------------- metrics
def auroc(y: np.ndarray, s: np.ndarray) -> float:
    y = np.asarray(y, bool)
    s = np.asarray(s, float)
    n1, n0 = y.sum(), (~y).sum()
    if n1 == 0 or n0 == 0:
        return float("nan")
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), float)
    ranks[order] = np.arange(1, len(s) + 1)
    # average ties
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    sums = np.zeros(len(cnt))
    np.add.at(sums, inv, ranks)
    ranks = (sums / cnt)[inv]
    return float((ranks[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def specificity_at_sensitivity(y, s, target_sens=0.80):
    """Threshold that reaches >= target_sens, report specificity and threshold."""
    y = np.asarray(y, bool)
    s = np.asarray(s, float)
    best = None
    for thr in np.unique(s):
        pred = s >= thr
        sens = pred[y].mean() if y.any() else 0.0
        spec = (~pred[~y]).mean() if (~y).any() else 0.0
        if sens >= target_sens:
            if best is None or spec > best[0]:
                best = (spec, thr, sens)
    if best is None:
        return float("nan"), float("nan"), float("nan")
    return best


def ppv(sens: float, spec: float, prevalence: float) -> float:
    num = sens * prevalence
    den = num + (1 - spec) * (1 - prevalence)
    return float(num / den) if den > 0 else float("nan")


# --------------------------------------------------------------------------- data loading
def load_csv(path: Path, max_subjects: int | None = None):
    """Load the Kaggle/IEEE-121 CSV. Returns (list_of_(X, y, pid), names)."""
    rows = list(csv.DictReader(path.open(newline="")))
    if not rows:
        raise SystemExit(f"empty csv: {path}")
    have = set(rows[0].keys())
    # Accept both modern (T7/T8/P7/P8) and legacy (T3/T4/T5/T6) names.
    rename = {}
    for old_name, new_name in ALIASES.items():
        if old_name in have and new_name not in have:
            rename[old_name] = new_name
    available = {rename.get(c, c) for c in have}

    need = set(CHANNELS) | {"Class", "ID"}
    if not need.issubset(available):
        missing = sorted(need - available)
        raise SystemExit(
            f"csv missing columns: {missing}\n"
            f"  found: {sorted(have)}\n"
            f"  expected either modern 10-20 (T7/T8/P7/P8) or legacy (T3/T4/T5/T6) names."
        )
    if rename:
        print(f"  (mapping legacy channel names: {rename})")

    subjects: dict[str, dict] = {}
    for r in rows:
        for old_name, new_name in rename.items():
            r[new_name] = r[old_name]
        pid = r["ID"]
        rec = subjects.setdefault(pid, {"label": r["Class"], "ch": [[] for _ in CHANNELS]})
        for i, ch in enumerate(CHANNELS):
            v = r[ch]
            rec["ch"][i].append(float(v) if v not in ("", None) else np.nan)

    data = []
    for k, (pid, rec) in enumerate(sorted(subjects.items())):
        if max_subjects is not None and k >= max_subjects:
            break
        X = np.array(rec["ch"], dtype=float)
        # median-impute per channel (the Kaggle CSV carries missing values)
        for i in range(X.shape[0]):
            col = X[i]
            bad = ~np.isfinite(col)
            if bad.all():
                X[i] = 0.0
            elif bad.any():
                col[bad] = np.nanmedian(col)
        y = 1 if str(rec["label"]).strip().lower().startswith("adhd") else 0
        data.append((X, y, pid))
    return data


def synth_subjects(n_per_class=60, seed=0):
    """Synthetic cohort WITH a known static between-subject signal.

    Ground truth is deliberately adversarial to alignment: the class difference lives in a
    STATIC per-subject covariance offset, which is exactly what per-subject centering removes.
    If alignment helps here, it is genuinely helping; if it destroys AUROC, that is the real
    Trap-2 failure mode, reproduced under control.
    """
    rng = np.random.default_rng(seed)
    n_ch = len(CHANNELS)
    data = []
    for cls, n in ((0, n_per_class), (1, n_per_class)):
        for i in range(n):
            pid = f"{'ADHD' if cls else 'CTRL'}_{i:03d}"
            dur = rng.uniform(20, 40)  # seconds; recording length varies per child
            n_samp = int(dur * FS)
            t = np.arange(n_samp) / FS

            # --- shared source structure.
            # NOTE: a PURE deterministic sine makes every window identical (zero across-window
            # variance), which silently breaks any alignment test. Use a stochastic narrowband
            # source with phase drift + slow amplitude modulation -- what real alpha looks like.
            alpha_amp = rng.uniform(0.6, 1.0)
            phase = 2 * np.pi * 10 * t + np.cumsum(rng.normal(0, 0.05, n_samp))
            env = 1 + 0.5 * np.sin(2 * np.pi * rng.uniform(0.15, 0.35) * t)
            src = alpha_amp * env * np.sin(phase) + 0.4 * rng.standard_normal(n_samp)
            X = np.outer(rng.uniform(0.5, 1.0, n_ch), src)
            X += 0.7 * rng.standard_normal((n_ch, n_samp))

            # --- STATIC per-subject nuisance: skull/impedance gain (this is what we WANT removed)
            gain = rng.uniform(0.6, 1.6, n_ch)
            X *= gain[:, None]

            # --- STATIC class signal: ADHD children have globally stronger alpha coherence
            #     across channels. This is the trait effect we must NOT remove.
            if cls == 1:
                shared = rng.uniform(0.3, 0.45) * np.sin(2 * np.pi * 10 * t)
                X += shared[None, :] * 1.4

            data.append((X, cls, pid))
    return data


# --------------------------------------------------------------------------- main experiment
def run(subjects, align: str, use_connectivity: bool = True, seed: int = 0) -> dict:
    """Participant-level CV: leave-one-subject-out is expensive, so grouped 5-fold is used."""
    rng = np.random.default_rng(seed)
    Xs, ys, groups = [], [], []

    for gi, (X, y, pid) in enumerate(subjects):
        W = windows(X)
        if W.shape[0] == 0:
            continue
        C = cov_stack(W)
        # R2 guard on every matrix before any manifold operation
        C = np.array([ensure_spd(c)[0] for c in C])

        if align == "none":
            Cn = C
        elif align == "euclid":
            Cn = align_euclid(C)
        elif align == "riemann":
            Cn = align_riemann(C)
        elif align == "riemann_band":
            # partial alignment: only the alpha-band covariance is centred
            Wb = bandpass(W.reshape(-1, W.shape[2]), *BANDS["alpha"]).reshape(W.shape)
            Cb = np.array([ensure_spd(c)[0] for c in cov_stack(Wb)])
            Cn = align_riemann(Cb)
        else:
            raise ValueError(align)

        F = tangent_features(Cn)
        if use_connectivity:
            F = np.concatenate([F, band_connectivity_features(W)], axis=1)

        Xs.append(F)
        ys.append(np.full(len(F), y))
        groups.append(np.full(len(F), gi))

    X = np.concatenate(Xs)
    y = np.concatenate(ys)
    g = np.concatenate(groups)

    # global z-score on training folds only (as in the base paper)
    uniq = np.unique(g)
    rng.shuffle(uniq)
    folds = np.array_split(uniq, 5)

    scores = np.full(len(y), np.nan)
    for f in folds:
        te = np.isin(g, f)
        tr = ~te
        mu = X[tr].mean(axis=0)
        sd = X[tr].std(axis=0)
        sd[sd == 0] = 1.0
        Xtr, Xte = (X[tr] - mu) / sd, (X[te] - mu) / sd
        w = _fit_logreg(Xtr, y[tr])
        scores[te] = np.hstack([Xte, np.ones((Xte.shape[0], 1))]) @ w

    # participant-level aggregation: mean of window scores per subject
    sub_scores, sub_y = [], []
    for gi in np.unique(g):
        m = g == gi
        if np.all(np.isnan(scores[m])):
            continue
        sub_scores.append(np.nanmean(scores[m]))
        sub_y.append(y[m][0])
    sub_scores = np.array(sub_scores)
    sub_y = np.array(sub_y)

    a = auroc(sub_y, sub_scores)
    spec, thr, sens = specificity_at_sensitivity(sub_y, sub_scores, 0.80)
    return {
        "align": align,
        "n_subjects": int(len(sub_y)),
        "n_windows": int(len(y)),
        "auroc": a,
        "sens_at_op": sens,
        "spec_at_80sens": spec,
        "bal_acc": (sens + spec) / 2 if np.isfinite(sens) and np.isfinite(spec) else float("nan"),
        "ppv_at_5pct": ppv(sens, spec, 0.05),
        "ppv_at_10pct": ppv(sens, spec, 0.10),
    }


def _fit_logreg(X: np.ndarray, y: np.ndarray, l2: float = 1.0, iters: int = 300):
    """Minimal L2 logistic regression (gradient descent). Returns weight vector."""
    n, d = X.shape
    Xb = np.hstack([X, np.ones((n, 1))])
    w = np.zeros(d + 1)
    for _ in range(iters):
        z = np.clip(Xb @ w, -30, 30)
        p = 1 / (1 + np.exp(-z))
        grad = Xb.T @ (p - y) / n + l2 * np.r_[w[:-1], 0.0] / n
        w -= 0.5 * grad
    return w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, help="path to the Kaggle/IEEE-121 adhd2.csv")
    ap.add_argument("--synthetic", action="store_true", help="run the logic on synthetic data")
    ap.add_argument("--max-subjects", type=int, default=None)
    ap.add_argument("--out", type=Path, default=None, help="write JSON results here")
    args = ap.parse_args()

    if args.csv:
        subjects = load_csv(args.csv, args.max_subjects)
        source = f"csv:{args.csv}"
    elif args.synthetic:
        subjects = synth_subjects()
        source = "synthetic"
    else:
        ap.error("choose --csv PATH or --synthetic")

    print(f"source: {source}   subjects: {len(subjects)}")

    rows = []
    base = None
    for align in ("none", "euclid", "riemann", "riemann_band"):
        r = run(subjects, align)
        rows.append(r)
        if align == "none":
            base = r
        d_auc = r["auroc"] - base["auroc"]
        d_spec = r["spec_at_80sens"] - base["spec_at_80sens"]
        print(
            f"  {align:<13} AUROC {r['auroc']:.4f} ({d_auc:+.4f})   "
            f"spec@80sens {r['spec_at_80sens']:.4f} ({d_spec:+.4f})   "
            f"PPV@10% {r['ppv_at_10pct']:.4f}"
        )

    print("\nVERDICT")
    r_r = next(r for r in rows if r["align"] == "riemann")
    d_auc = r_r["auroc"] - base["auroc"]
    d_spec = r_r["spec_at_80sens"] - base["spec_at_80sens"]
    if d_auc < -0.05:
        print(f"  ALIGNMENT DELETED SIGNAL: AUROC {d_auc:+.4f} (>5pp loss) (specificity change: {d_spec:+.4f}).")
        print("  -> Trap 2 is REAL on this data. Restore the dual-path node features (aperiodic")
        print("     exponent chi is scale-invariant) or restrict alignment to partial/band-limited.")
    elif d_spec <= 0:
        print(f"  Alignment did NOT improve specificity ({d_spec:+.4f}) -> D4 upgrade has no justification on this data.")
    else:
        print(f"  Alignment buys specificity ({d_spec:+.4f}) at acceptable AUROC cost ({d_auc:+.4f}).")
        print("  -> D4 upgrade justified. Record this table as the ablation rung.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({"source": source, "rows": rows}, indent=2))
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
