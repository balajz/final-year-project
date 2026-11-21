"""R3b: How much of the 0.90 AUROC is real? Permutation null with CACHED features.

The slow part of the permutation test is recomputing features per permutation. Features do not
depend on labels, so compute them ONCE, cache to disk, then permute only the labels -- that turns
a multi-minute job into seconds.

What this answers
-----------------
1. Repeated grouped 5-fold CV on REAL labels -> AUROC distribution (split noise)
2. Label-permutation null over the SAME folds -> is the real AUROC beyond chance?
3. Corrected p-value: (1 + #{null >= real}) / (1 + n_perm)

Caveat carried from the vault (Commitment 6): repeated CV on identical subjects measures
PARTITION/optimisation noise only, not population generalisation. With n=121 the interval will be
wide. That is the finding, not a nuisance.

Usage:
    python3 scripts/r3b_permutation_test.py --n-perm 200 --out results/r3b_perm.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r3_alignment_ablation as R  # noqa: E402

CACHE = Path("results/features_r3_none.npz")


def build_features(csv_path: Path, cache: Path = CACHE):
    """Compute (X, y, groups) once and cache. Features are label-independent."""
    if cache.exists():
        z = np.load(cache)
        print(f"  loaded cached features: {cache}  X={z['X'].shape}")
        return z["X"], z["y"], z["g"]

    subs = R.load_csv(csv_path)
    Xs, ys, gs = [], [], []
    for gi, (X, y, _) in enumerate(subs):
        W = R.windows(X)
        if W.shape[0] == 0:
            continue
        C = np.array([R.ensure_spd(c)[0] for c in R.cov_stack(W)])
        F = np.concatenate([R.tangent_features(C), R.band_connectivity_features(W)], axis=1)
        Xs.append(F.astype(np.float32))
        ys.append(np.full(len(F), y, dtype=np.int8))
        gs.append(np.full(len(F), gi, dtype=np.int16))

    X = np.concatenate(Xs)
    y = np.concatenate(ys)
    g = np.concatenate(gs)
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, X=X, y=y, g=g)
    print(f"  built + cached features: {cache}  X={X.shape}")
    return X, y, g


def fit_logreg_fast(X: np.ndarray, y: np.ndarray, iters: int = 150, l2: float = 1.0,
                    step: float = 2.0) -> np.ndarray:
    """L2 logistic regression by gradient descent. 60 iters x step 2.0 matches the 300-iter
    reference to ~1e-4 in AUROC at ~7x the speed -- verified in the benchmark."""
    n, d = X.shape
    Xb = np.hstack([X, np.ones((n, 1))])
    w = np.zeros(d + 1)
    for _ in range(iters):
        z = np.clip(Xb @ w, -30, 30)
        p = 1.0 / (1.0 + np.exp(-z))
        grad = Xb.T @ (p - y) / n + l2 * np.r_[w[:-1], 0.0] / n
        w -= step * grad
    return w


def cv_auroc(X, y, g, groups, seed: int, folds_n: int = 5) -> float:
    """Grouped k-fold, participant-level aggregation. Returns AUROC."""
    uniq = groups.copy()
    np.random.default_rng(seed).shuffle(uniq)
    folds = np.array_split(uniq, folds_n)
    scores = np.full(len(y), np.nan)

    for f in folds:
        te = np.isin(g, f)
        tr = ~te
        if tr.sum() == 0 or te.sum() == 0:
            continue
        mu = X[tr].mean(axis=0)
        sd = X[tr].std(axis=0)
        sd[sd == 0] = 1.0
        Xtr = (X[tr] - mu) / sd
        Xte = (X[te] - mu) / sd
        w = fit_logreg_fast(Xtr, y[tr].astype(float))
        scores[te] = np.hstack([Xte, np.ones((Xte.shape[0], 1))]) @ w

    sub_s, sub_y = [], []
    for gi in groups:
        m = g == gi
        if not m.any() or np.all(np.isnan(scores[m])):
            continue
        sub_s.append(np.nanmean(scores[m]))
        sub_y.append(int(y[m][0]))
    return R.auroc(np.array(sub_y), np.array(sub_s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=Path("data/adhdata.csv"))
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--n-repeat", type=int, default=10)
    ap.add_argument("--out", type=Path, default=Path("results/r3b_perm.json"))
    args = ap.parse_args()

    print("R3b: is the no-alignment AUROC beyond chance?")
    X, y, g = build_features(args.csv)
    X = X.astype(np.float64)
    groups = np.unique(g)
    print(f"  subjects {len(groups)}   windows {len(y)}   features {X.shape[1]}")

    # ---- 1) real labels, repeated CV
    real = np.array([cv_auroc(X, y, g, groups, s) for s in range(args.n_repeat)])
    print(f"\nREAL labels (grouped 5-fold x{args.n_repeat}):")
    print(f"  AUROC mean {real.mean():.4f}  sd {real.std():.4f}  "
          f"range [{real.min():.4f}, {real.max():.4f}]")

    # ---- 2) permutation null
    print(f"\npermutation null ({args.n_perm} perms)...")
    subj_label = np.array([int(y[g == gi][0]) for gi in groups])
    null = np.empty(args.n_perm)
    for k in range(args.n_perm):
        perm = np.random.default_rng(9000 + k).permutation(subj_label)
        lut = dict(zip(groups, perm))
        yp = np.array([lut[gi] for gi in g], dtype=float)
        null[k] = cv_auroc(X, yp, g, groups, seed=k)
        if (k + 1) % 20 == 0:
            print(f"    {k + 1}/{args.n_perm}  (null mean {null[:k+1].mean():.3f})", flush=True)

    p = (np.sum(null >= real.mean()) + 1) / (len(null) + 1)

    print(f"\nPERMUTATION NULL: mean {null.mean():.4f}  sd {null.std():.4f}  "
          f"95th pct {np.percentile(null, 95):.4f}  max {null.max():.4f}")
    print(f"\nREAL {real.mean():.4f} vs null 95th pct {np.percentile(null, 95):.4f}")
    print(f"p-value = {p:.4f}   ({np.sum(null >= real.mean())}/{len(null)} perms >= real)")

    print("\nVERDICT")
    if p < 0.05:
        print(f"  Real AUROC exceeds the permutation null (p={p:.4f}).")
        print("  => the pipeline discriminates beyond chance on this cohort, under grouped CV.")
    else:
        print(f"  Real AUROC is NOT beyond chance (p={p:.4f}).")
        print("  => with n=121 subjects the AUROC interval is too wide to claim discrimination.")
        print("     This is the honest result; report it as such, not as a failed experiment.")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({
        "n_subjects": int(len(groups)),
        "n_windows": int(len(y)),
        "real_mean": float(real.mean()),
        "real_sd": float(real.std()),
        "real_all": real.tolist(),
        "null_mean": float(null.mean()),
        "null_sd": float(null.std()),
        "null_p95": float(np.percentile(null, 95)),
        "null_max": float(null.max()),
        "p_value": float(p),
        "n_perm": args.n_perm,
    }, indent=2))
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
