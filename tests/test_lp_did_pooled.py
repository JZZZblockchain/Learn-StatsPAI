"""``sp.lp_did`` reports the pooled post- and pre-window estimates that Stata
``lpdid`` calls ``pooled_results``.

The pooled regression puts the *average* long difference over the window on
the left-hand side and runs it on the clean-control sample of the window's
end. On a design where every horizon shares one sample -- a single adoption
date, never-treated controls, a balanced panel -- the pooled coefficient is
exactly the mean of the per-horizon coefficients, because the regressors are
identical across horizons and OLS is linear in the outcome. That identity
pins the construction without a reference run; the castle-doctrine parity
module pins it against ``lpdid`` itself.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

import statspai as sp


def _single_cohort_panel(seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(40):
        g = 6 if i % 2 == 0 else 10**9
        fe = rng.normal()
        for t in range(12):
            d = 1 if t >= g else 0
            te = 2.0 * (t - g + 1) if d else 0.0
            rows.append(
                {"i": i, "t": t, "y": fe + 0.3 * t + te + rng.normal(0, 0.5), "d": d}
            )
    return pd.DataFrame(rows)


def test_pooled_equals_mean_of_horizons_when_samples_coincide():
    r = sp.lp_did(
        _single_cohort_panel(),
        y="y",
        unit="i",
        time="t",
        treatment="d",
        horizons=(-3, 5),
    )
    es = r.model_info["event_study"]
    pooled = r.model_info["pooled"]
    post = es[es["relative_time"] >= 0]["att"].values
    pre = es[es["relative_time"] <= -2]["att"].values
    assert pooled["post"]["horizons"] == [0, 1, 2, 3, 4, 5]
    assert pooled["pre"]["horizons"] == [-3, -2]
    np.testing.assert_allclose(pooled["post"]["estimate"], post.mean(), rtol=1e-10)
    np.testing.assert_allclose(pooled["pre"]["estimate"], pre.mean(), rtol=1e-10)
    assert pooled["post"]["se"] > 0 and pooled["post"]["n_obs"] > 0
    assert 0.0 <= pooled["post"]["pvalue"] <= 1.0


def test_pooled_windows_follow_horizons_argument():
    r = sp.lp_did(
        _single_cohort_panel(),
        y="y",
        unit="i",
        time="t",
        treatment="d",
        horizons=(-1, 3),
    )
    pooled = r.model_info["pooled"]
    assert pooled["post"]["horizons"] == [0, 1, 2, 3]
    assert "pre" not in pooled  # h_min = -1 leaves no pre window beyond the reference
