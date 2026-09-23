"""`sp.ddd` covariates: what the additive term does, and the DR route.

Ortiz-Villavicencio and Sant'Anna (2025) show that adding covariates to the
triple-interaction regression does not identify the covariate-adjusted DDD
ATT. The evidence here is T1 -- a design whose true effect is planted, whose
covariate is distributed differently across the four (treat, subgroup) cells,
and whose untreated trend loads on that covariate, so the unadjusted DDD is
biased by a known mechanism. `method='dr'` routes to `sp.ddd_heterogeneous`,
which carries its own R `triplediff` parity (Track A 77).
"""

import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp

TRUTH = 2.0


def _panel(rng, *, n=800, shift=0.8, trend=0.9, time_varying=False):
    """Two-period DDD panel with a cell-dependent covariate.

    ``shift`` moves the covariate's mean in the treated-eligible cell, and
    ``trend`` is how much the *untreated* path loads on it, so the DDD of
    outcome means inherits a bias of roughly ``shift * trend``.
    """
    rows = []
    for i in range(n):
        tr = int(rng.integers(0, 2))
        sub = int(rng.integers(0, 2))
        x = rng.normal(shift * tr * sub, 1.0)
        a = rng.normal()
        for t in (0, 1):
            rows.append(
                {
                    "i": i,
                    "t": t,
                    "tr": tr,
                    "sub": sub,
                    "x": x * (1 + 0.5 * t) if time_varying else x,
                    "y": (
                        a
                        + 0.5 * t
                        + 0.4 * x
                        + trend * x * t
                        + TRUTH * (tr * sub * t)
                        + rng.normal(0, 0.5)
                    ),
                }
            )
    return pd.DataFrame(rows)


def _ddd(df, **kw):
    return sp.ddd(df, y="y", treat="tr", time="t", subgroup="sub", **kw)


def test_additive_covariates_leave_the_coefficient_untouched():
    """A time-invariant covariate has no triple difference to contribute.

    This is the sharpest form of the critique: the adjustment users reach for
    is not merely insufficient, it is arithmetically a no-op, while the bias
    it is meant to remove lives in the covariate's effect on the *trend*.
    """
    rng = np.random.default_rng(0)
    df = _panel(rng)
    plain = _ddd(df)
    with pytest.warns(sp.AssumptionWarning, match="triple-interaction"):
        added = _ddd(df, covariates=["x"])
    assert added.estimate == pytest.approx(plain.estimate, rel=1e-12)
    # ... and both are biased by the planted mechanism: the observed
    # estimate is 2.968 for a true 2.0, 3.4 standard errors away.
    assert plain.estimate - TRUTH > 3 * plain.se


def test_dr_and_reg_routes_recover_the_planted_effect():
    rng = np.random.default_rng(1)
    df = _panel(rng)
    for method in ("dr", "reg", "ipw"):
        r = _ddd(df, covariates=["x"], id="i", method=method)
        assert abs(r.estimate - TRUTH) < 3 * r.se, method
        assert r.model_info["ddd_method"] == method
        assert r.model_info["ddd_delegated_from"] == "sp.ddd"


def test_a_time_varying_covariate_moves_the_regression_but_not_far_enough():
    rng = np.random.default_rng(2)
    df = _panel(rng, time_varying=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        added = _ddd(df, covariates=["x"])
    dr = _ddd(df, covariates=["x"], id="i", method="dr")
    assert abs(added.estimate - TRUTH) > abs(dr.estimate - TRUTH)
    assert abs(dr.estimate - TRUTH) < 3 * dr.se


def test_the_translation_is_exact_without_covariates():
    """Same cell means, so the same point estimate -- and a different SE."""
    rng = np.random.default_rng(3)
    df = _panel(rng)
    pooled = _ddd(df)
    panel = _ddd(df, id="i", method="dr")
    assert panel.estimate == pytest.approx(pooled.estimate, rel=1e-9)
    # The panel route differences within unit, so it is more precise; that is
    # a real difference between the two designs, not a discrepancy.
    assert panel.se < pooled.se


def test_dr_matches_ddd_heterogeneous_called_directly():
    rng = np.random.default_rng(4)
    df = _panel(rng)
    via_ddd = _ddd(df, covariates=["x"], id="i", method="dr")
    direct = sp.ddd_heterogeneous(
        df.assign(g=np.where(df["tr"] == 1, 1.0, -1.0)),
        y="y",
        unit="i",
        time="t",
        cohort="g",
        subgroup="sub",
        never_value=-1.0,
        x=["x"],
        est_method="dr",
    )
    assert via_ddd.estimate == pytest.approx(direct.estimate, rel=1e-12)
    assert via_ddd.se == pytest.approx(direct.se, rel=1e-12)


@pytest.mark.parametrize(
    "kwargs, exc, match",
    [
        ({"method": "magic"}, sp.MethodIncompatibility, "method must be"),
        ({"method": "dr"}, sp.MethodIncompatibility, "needs"),
        (
            {"method": "dr", "id": "i", "weights": "w"},
            sp.MethodIncompatibility,
            "weights",
        ),
        (
            {"method": "dr", "id": "i", "cluster": "sub"},
            sp.MethodIncompatibility,
            "clusters on id",
        ),
    ],
)
def test_argument_errors(kwargs, exc, match):
    rng = np.random.default_rng(5)
    df = _panel(rng, n=100).assign(w=1.0)
    with pytest.raises(exc, match=match):
        _ddd(df, **kwargs)


def test_more_than_two_periods_is_routed_to_the_staggered_estimator():
    rng = np.random.default_rng(6)
    df = _panel(rng, n=200)
    three = pd.concat([df, df.assign(t=2)], ignore_index=True)
    with pytest.raises(sp.MethodIncompatibility, match="two-period"):
        _ddd(three, id="i", method="dr")


def test_all_treated_leaves_no_comparison_group():
    rng = np.random.default_rng(7)
    df = _panel(rng, n=100)
    df = df.assign(tr=1)
    with pytest.raises(sp.MethodIncompatibility, match="two-valued"):
        _ddd(df, id="i", method="dr")
