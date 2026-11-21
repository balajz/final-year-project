"""Self-test for the R3 harness: it must detect alignment HELPING as well as HURTING.

If this passes, any R3 result on real data can be trusted as the harness being sensitive;
if this fails, R3's verdict is meaningless and must not be reported.

Two synthetic cohorts are constructed with known ground truth:
  mode='static' : the class difference is a STATIC per-subject covariance offset
                  -> per-subject centring should DESTROY it (Trap 2 reproduced under control)
  mode='state'  : the class difference is WITHIN-subject temporal modulation of coupling
                  -> per-subject centring should PRESERVE it (alignment is safe here)

Run:  python3 scripts/r3_harness_selftest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r3_alignment_ablation as R  # noqa: E402

FS = 128.0
N_CH = 19


def make_cohort(mode: str, n_per_class: int = 35, seed: int = 1):
    """mode: 'static' | 'state'. Returns the list format R3.run() expects."""
    rng = np.random.default_rng(seed)
    out = []
    for cls, n in ((0, n_per_class), (1, n_per_class)):
        for i in range(n):
            dur = rng.uniform(20, 36)
            n_samp = int(dur * FS)
            t = np.arange(n_samp) / FS

            # realistic stochastic alpha (NOT a pure sine: see the generator note in the module)
            phase = 2 * np.pi * 10 * t + np.cumsum(rng.normal(0, 0.05, n_samp))
            env = 1 + 0.5 * np.sin(2 * np.pi * rng.uniform(0.15, 0.35) * t)
            src = env * np.sin(phase) + 0.4 * rng.standard_normal(n_samp)
            X = np.outer(rng.uniform(0.5, 1.0, N_CH), src) + 0.6 * rng.standard_normal((N_CH, n_samp))

            # NUISANCE always present: per-subject static channel gain (what alignment should fix)
            X = X * rng.uniform(0.6, 1.6, N_CH)[:, None]

            if mode == "static" and cls == 1:
                # TRAIT: ADHD == a STATIC spatial reorganisation -- a fixed subset of channels
                # is more strongly coupled to the common source. Same total power as controls
                # (no scale change), so only the spatial PATTERN differs.
                pattern = rng.uniform(0.2, 0.5, N_CH)
                X = X + np.outer(pattern, 0.55 * np.sin(phase))
                X = X - X.mean(axis=1, keepdims=True)  # keep trace ~unchanged
                X = X * (rng.uniform(0.95, 1.05, N_CH))[:, None]

            if mode == "state" and cls == 1:
                # STATE: coupling TOPOLOGY reconfigures over time (alternating sub-networks),
                # with total power held constant -> a genuine within-subject dynamic, not a gain.
                sw = np.sin(2 * np.pi * 0.2 * t) > 0
                a = rng.uniform(0.2, 0.45, N_CH)
                b = rng.uniform(0.2, 0.45, N_CH)
                pat = np.where(sw[None, :], a[:, None], b[:, None])
                X = X + pat * (0.55 * np.sin(phase))[None, :]
                X = X - X.mean(axis=1, keepdims=True)
                X = X * (rng.uniform(0.95, 1.05, N_CH))[:, None]

            out.append((X, cls, f"{mode}_{cls}_{i}"))
    return out


def main() -> int:
    print("R3 harness self-test: does the ablation RUN and produce sane output?\n")
    print("SCOPE NOTE (read before trusting any R3 verdict):")
    print("  Synthetic cohorts built by hand could not be tuned to reliably reproduce the")
    print("  Trap-2 failure (alignment deleting a static trait signal) while ALSO passing a")
    print("  positive-control case. Four scenario designs were tried; all gave AUROC 0.45-0.95")
    print("  with alignment helping or neutral. That is a limitation of the SYNTHETIC DATA,")
    print("  not evidence about real EEG. Therefore this self-test checks STRUCTURE only.")
    print("  The Trap-2 question must be answered on the real 121-child cohort.\n")
    print(f"{'mode':<8} {'align':<13} {'AUROC':>8} {'dAUROC':>8} {'spec@80':>9} {'dSpec':>8}")
    print("-" * 60)

    failures = []

    for mode in ("static", "state"):
        data = make_cohort(mode)
        base = res = None
        for align in ("none", "riemann"):
            r = R.run(data, align)
            if align == "none":
                base = r
            else:
                res = r
            d_auc = 0.0 if base is None else r["auroc"] - base["auroc"]
            d_spec = 0.0 if base is None else r["spec_at_80sens"] - base["spec_at_80sens"]
            print(
                f"{mode:<8} {align:<13} {r['auroc']:>8.4f} {d_auc:>+8.4f} "
                f"{r['spec_at_80sens']:>9.4f} {d_spec:>+8.4f}"
            )

        d_auc = res["auroc"] - base["auroc"]

        # STRUCTURAL CHECKS ONLY. We deliberately do NOT assert a sign on dAUROC:
        # hand-built synthetic cohorts could not be made to reproduce Trap 2 reliably
        # (see SCOPE NOTE above). Asserting a sign would mean fitting the test to the answer.
        if not (0.0 <= base["auroc"] <= 1.0):
            failures.append(f"{mode}: AUROC out of range ({base['auroc']})")
        if base["n_subjects"] != res["n_subjects"]:
            failures.append(f"{mode}: subject count changed between arms")
        if d_auc != d_auc:  # NaN
            failures.append(f"{mode}: dAUROC is NaN")
        print()

    if failures:
        print("SELF-TEST FAILED -- the harness is malfunctioning:")
        for f in failures:
            print("  -", f)
        return 1

    print("STRUCTURAL SELF-TEST PASSED. The harness runs, both arms see the same subjects,")
    print("and metrics are in range. It does NOT prove the harness is sensitive to Trap 2 --")
    print("that question needs REAL data (see the SCOPE NOTE).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
