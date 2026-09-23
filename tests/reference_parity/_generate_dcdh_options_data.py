"""Panel for the dCDH intertemporal event study's options.

Built for the ``controls``, ``trends_lin``, ``trends_nonparam``,
``normalized`` and ``predict_het`` options of
``sp.did_multiplegt_dyn`` against R ``DIDmultiplegtDYN`` 2.3.4.

The design gives the options something to do: the covariates drive a
differential trend (so ``controls`` moves the estimate), the two regions
trend apart (so ``trends_nonparam`` does too), half the groups start
treated (so the baseline-treatment split is exercised in both
directions), and the group-level effect varies with a time-invariant
covariate (so ``predict_het`` has a signal to find).
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
NAME = "dcdh_options_panel"


def build() -> pd.DataFrame:
    rng = np.random.default_rng(20260923)
    n_groups, T = 60, 8
    rows = []
    for g in range(1, n_groups + 1):
        region = "A" if g % 2 == 0 else "B"
        base = int(g % 4 in (2, 3))  # half the groups start treated
        switch = int(rng.integers(3, T))  # first change of treatment
        z = float(rng.normal())  # time-invariant, drives effect size
        x1 = float(rng.normal())
        alpha = float(rng.normal())
        d_prev = base
        for t in range(1, T + 1):
            x1 = 0.6 * x1 + float(rng.normal(0, 0.8))
            x2 = 0.3 * t + float(rng.normal(0, 0.5))
            d = base if t < switch else 1 - base
            # differential trend explained by the covariates, a region trend,
            # and an effect that grows with the horizon and with z
            eff = (0.8 + 0.4 * z) * max(0, t - switch + 1) if t >= switch else 0.0
            y = (
                alpha
                + 0.25 * t
                + 0.9 * x1
                + 0.5 * x2
                + (0.15 * t if region == "A" else -0.05 * t)
                + (eff if base == 0 else -eff)
                + float(rng.normal(0, 0.4))
            )
            rows.append(
                {
                    "id": g,
                    "t": t,
                    "d": d,
                    "y": round(y, 10),
                    "x1": round(x1, 10),
                    "x2": round(x2, 10),
                    "reg": region,
                    "z": round(z, 10),
                }
            )
            d_prev = d
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = build()
    out = HERE / "_fixtures" / f"{NAME}.csv"
    df.to_csv(out, index=False)
    print(f"wrote {out} ({len(df)} rows, {df['id'].nunique()} groups)")
