"""
r4_artifact_control.py -- Decisive Artifact-Control Test on IEEE-121 Neural Features.

THE QUESTION
------------
In R3b, the unaligned neural/connectivity feature set (tangent + band connectivity) reaches
AUROC = 0.9081 ± 0.0089 (p = 0.005). Meanwhile, an artifact-only classifier using 5 recording-
quality proxies (duration, blink variance, blink-band power, 30-60 Hz EMG, total variance)
reaches ~0.7784 on the exact same 121 subjects.

Does the 0.9081 discrimination survive when artifact proxies are controlled?

THREE CONTROL ARMS (all strict subject-disjoint grouped 5-fold CV, 10 repeats)
------------------------------------------------------------------------------
1. baseline          : Uncontrolled R3 feature set (reproduces 0.9081)
2. residualized      : Fold-safe OLS residualization — inside EACH training fold, regress the
                       684 neural features onto the 5 subject-level artifact proxies and
                       subtract the predicted artifact component from both train and test.
3. duration_matched  : Truncate every subject's window stream to the minimum window count
                       across subjects (equal duration for all 121 children), removing duration
                       as a cue entirely.
4. emg_stratified    : Evaluate the neural feature set separately on the clean half vs. noisy
                       half of subjects (median split on 30-60 Hz EMG power).

Usage:
    python3 scripts/r4_artifact_control.py --csv data/adhdata.csv --out results/r4_artifact_control.json

Dependencies: NumPy only (uses cached R3 features when available).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r3_alignment_ablation as R  # noqa: E402
import r3b_permutation_test as R3B  # noqa: E402
from r4_artifact_only import extract_subject_artifact_features  # noqa: E402


def compute_subject_artifacts(csv_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load subjects in the exact sorted order of R.load_csv and extract (N_subj, 5) proxies."""
    subs = R.load_csv(csv_path)
    art_feats = []
    emg_vals = []
    for X, _, _ in subs:
        d = extract_subject_artifact_features(X, sfreq=R.FS)
        art_feats.append(d["features"])
        emg_vals.append(d["emg_power"])
    return np.stack(art_feats, axis=0), np.array(emg_vals, dtype=float)


def eval_neural_cv(
    X: np.ndarray,
    y: np.ndarray,
    g: np.ndarray,
    groups: np.ndarray,
    A_subj: np.ndarray | None = None,
    residualize: bool = False,
    n_repeats: int = 10,
    folds_n: int = 5,
) -> dict:
    """Run repeated grouped 5-fold CV, optionally with fold-safe OLS artifact residualization."""
    aucs, specs, ppv10s = [], [], []

    for seed in range(n_repeats):
        uniq = groups.copy()
        np.random.default_rng(seed).shuffle(uniq)
        folds = np.array_split(uniq, folds_n)
        scores = np.full(len(y), np.nan)

        for f in folds:
            te = np.isin(g, f)
            tr = ~te
            if tr.sum() == 0 or te.sum() == 0:
                continue

            Xtr = X[tr].copy()
            Xte = X[te].copy()

            if residualize and A_subj is not None:
                # Map subject-level artifact proxies to window rows (zero leakage: fit on train only)
                Atr = np.hstack([A_subj[g[tr]], np.ones((tr.sum(), 1))])
                Ate = np.hstack([A_subj[g[te]], np.ones((te.sum(), 1))])
                # Ridge-stabilized OLS: (Atr^T Atr + 1e-4 I)^-1 Atr^T Xtr
                reg = 1e-4 * np.eye(Atr.shape[1])
                reg[-1, -1] = 0.0
                beta = np.linalg.solve(Atr.T @ Atr + reg, Atr.T @ Xtr)
                Xtr = Xtr - Atr @ beta
                Xte = Xte - Ate @ beta

            mu = Xtr.mean(axis=0)
            sd = Xtr.std(axis=0)
            sd[sd == 0] = 1.0
            Xtr = (Xtr - mu) / sd
            Xte = (Xte - mu) / sd

            w = R3B.fit_logreg_fast(Xtr, y[tr].astype(float))
            scores[te] = np.hstack([Xte, np.ones((Xte.shape[0], 1))]) @ w

        sub_s, sub_y = [], []
        for gi in groups:
            m = g == gi
            if not m.any() or np.all(np.isnan(scores[m])):
                continue
            sub_s.append(np.nanmean(scores[m]))
            sub_y.append(int(y[m][0]))

        sub_s = np.array(sub_s)
        sub_y = np.array(sub_y)
        aucs.append(R.auroc(sub_y, sub_s))
        spec, _, sens = R.specificity_at_sensitivity(sub_y, sub_s, 0.80)
        specs.append(spec)
        ppv10s.append(R.ppv(sens, spec, 0.10))

    return {
        "n_subjects": int(len(groups)),
        "n_windows": int(np.sum(np.isin(g, groups))),
        "auroc_mean": round(float(np.mean(aucs)), 4),
        "auroc_sd": round(float(np.std(aucs)), 4),
        "spec_at_80sens_mean": round(float(np.nanmean(specs)), 4),
        "ppv_at_10pct_mean": round(float(np.nanmean(ppv10s)), 4),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=Path("data/adhdata.csv"))
    ap.add_argument("--n-repeats", type=int, default=10)
    ap.add_argument("--out", type=Path, default=Path("results/r4_artifact_control.json"))
    args = ap.parse_args()

    if not args.csv.exists():
        print(f"Error: {args.csv} not found.")
        sys.exit(1)

    print("=" * 70)
    print("R4 ARTIFACT-CONTROL TEST: BRAIN SIGNAL OR RECORDING PROTOCOL?")
    print("=" * 70)

    X, y, g = R3B.build_features(args.csv)
    X = X.astype(np.float64)
    groups = np.unique(g)
    A_subj, emg_vals = compute_subject_artifacts(args.csv)
    assert len(A_subj) >= len(groups), "Subject count mismatch between CSV and cached features."

    # 1. Baseline (uncontrolled)
    res_base = eval_neural_cv(X, y, g, groups, n_repeats=args.n_repeats)

    # 2. Fold-safe OLS artifact residualization
    res_resid = eval_neural_cv(X, y, g, groups, A_subj=A_subj, residualize=True, n_repeats=args.n_repeats)

    # 3. Duration-matched subsampling (equal window count per subject)
    win_counts = [int(np.sum(g == gi)) for gi in groups]
    min_win = min(win_counts)
    keep_idx = np.concatenate([np.where(g == gi)[0][:min_win] for gi in groups])
    res_dur = eval_neural_cv(X[keep_idx], y[keep_idx], g[keep_idx], groups, n_repeats=args.n_repeats)

    # 4. EMG median stratification (clean half vs. noisy half)
    emg_med = float(np.median(emg_vals[groups]))
    clean_groups = groups[emg_vals[groups] < emg_med]
    noisy_groups = groups[emg_vals[groups] >= emg_med]
    res_clean = eval_neural_cv(X, y, g, clean_groups, n_repeats=args.n_repeats)
    res_noisy = eval_neural_cv(X, y, g, noisy_groups, n_repeats=args.n_repeats)

    delta_resid = res_resid["auroc_mean"] - res_base["auroc_mean"]
    delta_dur = res_dur["auroc_mean"] - res_base["auroc_mean"]

    print(f"\n  1. Baseline (uncontrolled):       AUROC {res_base['auroc_mean']:.4f} ± {res_base['auroc_sd']:.4f}  | spec@80 {res_base['spec_at_80sens_mean']:.4f}")
    print(f"  2. Artifact-residualized (OLS):   AUROC {res_resid['auroc_mean']:.4f} ± {res_resid['auroc_sd']:.4f} ({delta_resid:+.4f}) | spec@80 {res_resid['spec_at_80sens_mean']:.4f}")
    print(f"  3. Duration-matched ({min_win} win/subj): AUROC {res_dur['auroc_mean']:.4f} ± {res_dur['auroc_sd']:.4f} ({delta_dur:+.4f}) | spec@80 {res_dur['spec_at_80sens_mean']:.4f}")
    print(f"  4a. Clean EMG half (n={res_clean['n_subjects']}):        AUROC {res_clean['auroc_mean']:.4f} ± {res_clean['auroc_sd']:.4f}")
    print(f"  4b. Noisy EMG half (n={res_noisy['n_subjects']}):        AUROC {res_noisy['auroc_mean']:.4f} ± {res_noisy['auroc_sd']:.4f}")

    out_payload = {
        "dataset": str(args.csv),
        "n_subjects": int(len(groups)),
        "n_windows": int(len(y)),
        "min_windows_per_subject": int(min_win),
        "baseline": res_base,
        "artifact_residualized": res_resid,
        "duration_matched": res_dur,
        "emg_clean_half": res_clean,
        "emg_noisy_half": res_noisy,
        "delta_auroc_residualized": round(float(delta_resid), 4),
        "delta_auroc_duration_matched": round(float(delta_dur), 4),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"\nSaved reproducible results to {args.out}")
    print("=" * 70)


if __name__ == "__main__":
    main()
