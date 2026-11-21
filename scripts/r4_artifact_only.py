"""
r4_artifact_only.py -- Standalone evaluation of artifact-only classification on IEEE-121.

Tests whether a simple classifier using ONLY non-neural artifact metrics:
1. Total recording duration (duration_sec)
2. Frontal blink variance (log_fp_variance on Fp1, Fp2)
3. Frontal blink-band power (0.5-4 Hz on Fp1, Fp2)
4. High-frequency EMG band power (30-60 Hz across peripheral channels)
5. Total recording amplitude variance (log_total_variance)
can discriminate ADHD from Control without any brain connectivity features.

Includes:
- Repeated subject-disjoint 5-fold CV (10 repeats)
- Label-permutation null (default 200 permutations) with exact p-value
- EMG-median stratification (clean half vs. noisy half)
- Empirical correlation between EMG (30-60 Hz) and cortical Gamma (30-45 Hz)

Usage:
    python3 scripts/r4_artifact_only.py --csv data/adhdata.csv --n-perm 200 --out results/r4_artifact_only.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import numpy as np

# Canonical 19-channel modern 10-20 layout
CHANNELS = [
    "Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4",
    "O1", "O2", "F7", "F8", "T7", "T8", "P7", "P8",
    "Fz", "Cz", "Pz"
]


def bandpower_fft(sig: np.ndarray, sfreq: float, band: tuple[float, float]) -> float:
    """Mean log bandpower using rfft."""
    n = sig.shape[-1]
    freqs = np.fft.rfftfreq(n, d=1.0 / sfreq)
    fft_vals = np.abs(np.fft.rfft(sig, axis=-1)) ** 2 / n
    idx = (freqs >= band[0]) & (freqs < band[1])
    if not np.any(idx):
        return 0.0
    power = np.mean(fft_vals[..., idx], axis=-1)
    return float(np.mean(np.log(power + 1e-12)))


def extract_subject_artifact_features(continuous: np.ndarray, sfreq: float = 128.0) -> dict:
    """Extract 5 recording-quality / artifact proxies from continuous (19, n_samples) EEG."""
    _, n_samp = continuous.shape
    duration_sec = n_samp / sfreq

    # 1. Frontal channels (Fp1, Fp2) for eye-blinks (indices 0, 1)
    fp_sig = continuous[[0, 1], :]
    fp_var = float(np.mean(np.var(fp_sig, axis=1)))
    fp_delta_power = bandpower_fft(fp_sig, sfreq, (0.5, 4.0))

    # 2. EMG band (30-60 Hz) across temporal / peripheral channels (F7, F8, T7, T8, P7, P8)
    periph_idx = [10, 11, 12, 13, 14, 15]
    emg_power = bandpower_fft(continuous[periph_idx, :], sfreq, (30.0, 60.0))

    # 3. Cortical Gamma band (30-45 Hz) across all channels
    gamma_power = bandpower_fft(continuous, sfreq, (30.0, 45.0))

    # 4. Total amplitude variance
    total_var = float(np.mean(np.var(continuous, axis=1)))

    return {
        "features": np.array([
            duration_sec,
            np.log(fp_var + 1e-12),
            fp_delta_power,
            emg_power,
            np.log(total_var + 1e-12),
        ], dtype=float),
        "emg_power": emg_power,
        "gamma_power": gamma_power,
    }


def fit_logistic_regression(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    l2: float = 1.0,
    max_iter: int = 500,
    lr: float = 0.05,
) -> np.ndarray:
    """Simple L2 logistic regression via gradient descent."""
    N, D = X_train.shape
    X_tr = np.hstack([X_train, np.ones((N, 1))])
    X_te = np.hstack([X_test, np.ones((X_test.shape[0], 1))])

    mu = np.mean(X_tr[:, :D], axis=0, keepdims=True)
    sigma = np.std(X_tr[:, :D], axis=0, keepdims=True) + 1e-8
    X_tr[:, :D] = (X_tr[:, :D] - mu) / sigma
    X_te[:, :D] = (X_te[:, :D] - mu) / sigma

    w = np.zeros(D + 1)
    for _ in range(max_iter):
        p = 1.0 / (1.0 + np.exp(-np.clip(X_tr @ w, -15, 15)))
        grad = X_tr.T @ (p - y_train) / N
        grad[:D] += (l2 / N) * w[:D]
        w -= lr * grad

    return 1.0 / (1.0 + np.exp(-np.clip(X_te @ w, -15, 15)))


def compute_roc_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Mann-Whitney U statistic formulation for ROC-AUC."""
    pos = y_score[y_true == 1]
    neg = y_score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    diffs = pos[:, None] - neg[None, :]
    return float(np.mean((diffs > 0).astype(float) + 0.5 * (diffs == 0).astype(float)))


def cv_auroc_subject(X: np.ndarray, y: np.ndarray, n_splits: int = 5, seed: int = 42) -> float:
    """Single subject-disjoint K-fold pass returning out-of-fold pooled subject AUROC."""
    rng = np.random.default_rng(seed)
    N = len(y)
    indices = np.arange(N)
    rng.shuffle(indices)
    folds = np.array_split(indices, n_splits)

    oof_probs = np.full(N, np.nan)
    for te in folds:
        tr = np.setdiff1d(indices, te)
        if len(np.unique(y[tr])) < 2:
            continue
        oof_probs[te] = fit_logistic_regression(X[tr], y[tr], X[te])

    valid = np.isfinite(oof_probs)
    return compute_roc_auc(y[valid], oof_probs[valid])


def run_artifact_evaluation(
    csv_path: Path,
    n_splits: int = 5,
    n_repeats: int = 10,
    n_perm: int = 200,
    seed: int = 42,
) -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from data_loader import load_ieee121_csv

    recs = load_ieee121_csv(csv_path)
    print(f"Loaded {len(recs)} subjects from {csv_path}")

    X_list, y_list, emg_powers, gamma_powers = [], [], [], []
    for r in recs:
        feat_dict = extract_subject_artifact_features(r.data, sfreq=r.sfreq)
        X_list.append(feat_dict["features"])
        y_list.append(1 if "adhd" in str(r.label).lower() else 0)
        emg_powers.append(feat_dict["emg_power"])
        gamma_powers.append(feat_dict["gamma_power"])

    X = np.stack(X_list, axis=0)
    y = np.array(y_list, dtype=int)
    emg_arr = np.array(emg_powers, dtype=float)
    N = len(y)

    # 1. Empirical correlation between EMG (30-60 Hz) and Gamma (30-45 Hz)
    corr_emg_gamma = float(np.corrcoef(emg_arr, gamma_powers)[0, 1])

    # 2. Repeated subject-disjoint K-Fold CV (out-of-fold subject AUROC per repeat)
    real_aurocs = [cv_auroc_subject(X, y, n_splits=n_splits, seed=seed + rep) for rep in range(n_repeats)]
    mean_auc = float(np.mean(real_aurocs))
    std_auc = float(np.std(real_aurocs))

    # 3. Label-permutation null over identical folds
    null_aurocs = np.empty(n_perm, dtype=float)
    for k in range(n_perm):
        perm_rng = np.random.default_rng(9000 + k)
        y_perm = perm_rng.permutation(y)
        null_aurocs[k] = cv_auroc_subject(X, y_perm, n_splits=n_splits, seed=seed + (k % n_repeats))
    p_value = float((np.sum(null_aurocs >= mean_auc) + 1) / (n_perm + 1))

    # 4. EMG median stratification (clean half vs. noisy half)
    emg_med = float(np.median(emg_arr))
    clean_mask = emg_arr < emg_med
    noisy_mask = ~clean_mask
    clean_aucs = [cv_auroc_subject(X[clean_mask], y[clean_mask], n_splits=n_splits, seed=seed + rep) for rep in range(n_repeats)]
    noisy_aucs = [cv_auroc_subject(X[noisy_mask], y[noisy_mask], n_splits=n_splits, seed=seed + rep) for rep in range(n_repeats)]

    return {
        "dataset": str(csv_path),
        "n_subjects": N,
        "n_adhd": int(np.sum(y == 1)),
        "n_control": int(np.sum(y == 0)),
        "artifact_features": [
            "duration_sec",
            "log_fp_variance",
            "fp_delta_power",
            "emg_30_60hz_power",
            "log_total_variance",
        ],
        "emg_gamma_correlation": round(corr_emg_gamma, 4),
        "repeated_cv": {
            "n_splits": n_splits,
            "n_repeats": n_repeats,
            "mean_auroc": round(mean_auc, 4),
            "std_auroc": round(std_auc, 4),
            "min_auroc": round(float(np.min(real_aurocs)), 4),
            "max_auroc": round(float(np.max(real_aurocs)), 4),
        },
        "permutation_null": {
            "n_perm": n_perm,
            "null_mean": round(float(np.mean(null_aurocs)), 4),
            "null_sd": round(float(np.std(null_aurocs)), 4),
            "null_p95": round(float(np.percentile(null_aurocs, 95)), 4),
            "null_max": round(float(np.max(null_aurocs)), 4),
            "p_value": round(p_value, 4),
        },
        "emg_stratification": {
            "emg_median": round(emg_med, 4),
            "clean_half_n": int(np.sum(clean_mask)),
            "clean_half_auroc_mean": round(float(np.mean(clean_aucs)), 4),
            "clean_half_auroc_sd": round(float(np.std(clean_aucs)), 4),
            "noisy_half_n": int(np.sum(noisy_mask)),
            "noisy_half_auroc_mean": round(float(np.mean(noisy_aucs)), 4),
            "noisy_half_auroc_sd": round(float(np.std(noisy_aucs)), 4),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=Path("data/adhdata.csv"))
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--n-repeats", type=int, default=10)
    ap.add_argument("--out", type=Path, default=Path("results/r4_artifact_only.json"))
    args = ap.parse_args()

    if not args.csv.exists():
        print(f"Error: {args.csv} not found.")
        sys.exit(1)

    print("=" * 70)
    print("ARTIFACT-ONLY CLASSIFIER EVALUATION (R4 EMPIRICAL AUDIT)")
    print("=" * 70)

    res = run_artifact_evaluation(args.csv, n_repeats=args.n_repeats, n_perm=args.n_perm)

    print("\nRESULTS:")
    print(f"  Subjects: {res['n_subjects']} ({res['n_adhd']} ADHD / {res['n_control']} Control)")
    print(f"  Artifact-only AUROC: {res['repeated_cv']['mean_auroc']:.4f} ± {res['repeated_cv']['std_auroc']:.4f}")
    print(f"  Permutation null ({args.n_perm}): {res['permutation_null']['null_mean']:.4f} ± "
          f"{res['permutation_null']['null_sd']:.4f} (p = {res['permutation_null']['p_value']:.4f})")
    print(f"  EMG clean half (n={res['emg_stratification']['clean_half_n']}): "
          f"{res['emg_stratification']['clean_half_auroc_mean']:.4f} ± {res['emg_stratification']['clean_half_auroc_sd']:.4f}")
    print(f"  EMG noisy half (n={res['emg_stratification']['noisy_half_n']}): "
          f"{res['emg_stratification']['noisy_half_auroc_mean']:.4f} ± {res['emg_stratification']['noisy_half_auroc_sd']:.4f}")
    print(f"  EMG (30-60 Hz) vs Gamma (30-45 Hz) Pearson r: {res['emg_gamma_correlation']:.4f}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"\nSaved reproducible results to {args.out}")
    print("=" * 70)


if __name__ == "__main__":
    main()
