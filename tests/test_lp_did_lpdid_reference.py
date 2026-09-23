"""LP-DiD leads, lags and pooled windows against Stata ``lpdid`` 1.0.2.

Reference values are the Stata rows of the DiD reconciliation study
(Paper-DiD-JAE, ``replication/applications/castle/results/castle_Stata.json``):
``lpdid l_homicide, unit(sid) time(year) treat(treat) pre_window(5) post_window(4)``
on the castle-doctrine panel with cohort-consistent treatment timing. The
clean-control window at lead h is ``[t+h, t-1]`` (lpdid's ``CCS_m<h> = CCS_0``);
the first-pass StatsPAI rule ``[t+h-1, t-1]`` dropped the earliest observable
calendar year at every lead and moved the deepest lead by 6 percent.

Estimates agree to reghdfe's solver tolerance (1e-7) and standard errors to
1e-8; sample sizes are identical at every horizon.
"""

from __future__ import annotations

import numpy as np
import pytest

import statspai as sp

# statistic -> (estimate, se, n)
STATA = {
    "dyn_e-5": (0.04351527081180941, 0.05712824774469297, 226),
    "dyn_e-4": (0.007605666144508175, 0.05674689138534626, 276),
    "dyn_e-3": (0.06239964168114284, 0.04366401650392433, 326),
    "dyn_e-2": (0.06297572736317507, 0.05078860848719879, 376),
    "dyn_e0": (0.09982924346896227, 0.04436895024170778, 426),
    "dyn_e1": (0.1062628778514961, 0.0513105138104987, 376),
    "dyn_e2": (0.1080677877323661, 0.05794395921686282, 325),
    "dyn_e3": (0.1382595266978718, 0.0567634393442956, 273),
    "dyn_e4": (0.09393880725113447, 0.05402792723173371, 219),
}
POOLED = {
    "post": (0.107937421205443, 0.04935736346942109),
    "pre": (0.04412407406261416, 0.04245987251610112),
}


@pytest.fixture(scope="module")
def castle():
    if not hasattr(sp.datasets, "castle_doctrine"):
        pytest.skip("castle-doctrine panel not shipped")
    df = sp.datasets.castle_doctrine(event_time=True)
    need = {"sid", "year", "l_homicide", "gvar"}
    if not need <= set(df.columns):
        pytest.skip("castle-doctrine panel lacks the cohort column")
    df = df.copy()
    df["treat"] = ((df["gvar"] > 0) & (df["year"] >= df["gvar"])).astype(int)
    return df


@pytest.fixture(scope="module")
def fit(castle):
    return sp.lp_did(
        castle,
        y="l_homicide",
        unit="sid",
        time="year",
        treatment="treat",
        horizons=(-5, 4),
        clean_controls="not_yet_treated",
        cluster="sid",
    )


def test_every_horizon_matches_lpdid(fit):
    es = fit.model_info["event_study"].set_index("relative_time")
    for stat, (est, se, n) in STATA.items():
        k = int(stat.replace("dyn_e", ""))
        row = es.loc[k]
        assert row["att"] == pytest.approx(est, rel=2e-7, abs=1e-9), stat
        assert row["se"] == pytest.approx(se, rel=1e-7), stat
        assert int(row["n_obs"]) == n, f"{stat}: n {int(row['n_obs'])} vs lpdid {n}"


def test_pooled_windows_match_lpdid(fit):
    pooled = fit.model_info["pooled"]
    for key, (est, se) in POOLED.items():
        assert pooled[key]["estimate"] == pytest.approx(est, rel=2e-7)
        assert pooled[key]["se"] == pytest.approx(se, rel=1e-7)


def test_lead_window_is_lpdids(castle):
    """Lead -2 keeps the earliest year with y_{t-2} observed (376 rows)."""
    r = sp.lp_did(
        castle,
        y="l_homicide",
        unit="sid",
        time="year",
        treatment="treat",
        horizons=(-2, 0),
        cluster="sid",
    )
    es = r.model_info["event_study"].set_index("relative_time")
    assert int(es.loc[-2, "n_obs"]) == 376
    assert np.isfinite(es.loc[-2, "se"])
