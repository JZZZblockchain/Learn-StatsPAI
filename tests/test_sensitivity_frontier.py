"""
Tests for frontier sensitivity analyses (sp.robustness.sensitivity_frontier).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import statspai as sp


def test_copula_sensitivity_breakpoint_monotone():
    """A larger observed effect should need a larger |rho| to overturn."""
    res_small = sp.copula_sensitivity(estimate=0.2, se=0.05)
    res_large = sp.copula_sensitivity(estimate=0.8, se=0.05)
    if res_small.breakpoint is None or res_large.breakpoint is None:
        pytest.skip("Grid did not cover a breakpoint for one of the cases.")
    assert abs(res_large.breakpoint) >= abs(res_small.breakpoint)


def test_copula_sensitivity_returns_curve():
    res = sp.copula_sensitivity(estimate=0.3, se=0.1)
    z = 1.959963984540054
    first = res.curve.iloc[0]
    np.testing.assert_allclose(first["rho"], -0.5)
    np.testing.assert_allclose(first["bias"], -0.5)
    np.testing.assert_allclose(first["adjusted_estimate"], 0.8)
    np.testing.assert_allclose(first["ci_low"], 0.8 - z * 0.1)
    np.testing.assert_allclose(first["ci_high"], 0.8 + z * 0.1)
    np.testing.assert_allclose(res.breakpoint, 0.15000000000000002)
    assert isinstance(res.curve, pd.DataFrame)
    assert set(res.curve.columns) == {
        "rho",
        "bias",
        "adjusted_estimate",
        "ci_low",
        "ci_high",
        "significant",
    }
    assert res.method == "copula_gaussian"
    assert "Sensitivity" in res.summary()


def test_survival_sensitivity_bounds_monotone():
    res = sp.survival_sensitivity(log_hr=-0.5, se_log_hr=0.2)
    c = res.curve
    first = c.iloc[0]
    np.testing.assert_allclose(first["gamma"], 1.0)
    np.testing.assert_allclose(first["log_hr_worst"], -0.5)
    np.testing.assert_allclose(first["log_hr_best"], -0.5)
    np.testing.assert_allclose(
        first["delta_survival_worst"],
        0.5 ** np.exp(-0.5) - 0.5,
    )
    # Protective effect: the worst case moves toward the null (increases),
    # the best case away from it. Before 1.30 the worst case decreased, so a
    # protective hazard ratio could never be explained away.
    assert (c["log_hr_worst"].diff().dropna() >= -1e-10).all()
    assert (c["log_hr_best"].diff().dropna() <= 1e-10).all()


def test_survival_sensitivity_is_symmetric_in_the_sign_of_the_effect():
    pos = sp.survival_sensitivity(log_hr=0.4, se_log_hr=0.15)
    neg = sp.survival_sensitivity(log_hr=-0.4, se_log_hr=0.15)
    assert pos.breakpoint is not None
    assert neg.breakpoint == pos.breakpoint
    np.testing.assert_allclose(
        neg.curve["log_hr_worst"], -pos.curve["log_hr_worst"], rtol=0, atol=1e-15
    )


def test_survival_sensitivity_rejects_bad_baseline():
    with pytest.raises(ValueError, match="baseline_survival_t"):
        sp.survival_sensitivity(log_hr=-0.5, se_log_hr=0.1, baseline_survival_t=1.5)


def test_survival_sensitivity_rejects_negative_se():
    with pytest.raises(ValueError, match="se_log_hr"):
        sp.survival_sensitivity(log_hr=-0.3, se_log_hr=-0.1)


def test_calibrate_confounding_strength_flags_robust_effect():
    """Large effect, small observed R² → breakpoint should be large (robust)."""
    res = sp.calibrate_confounding_strength(
        estimate=0.6,
        se=0.05,
        observed_r2_outcome=0.01,
        observed_r2_treatment=0.01,
        dof=400,
    )
    # Either no breakpoint (robust) or a large multiplier
    assert (res.breakpoint is None) or (res.breakpoint >= 2.0)


def test_calibrate_confounding_strength_small_effect_fragile():
    """Small effect, modest R² → breakpoint should be small (fragile)."""
    res = sp.calibrate_confounding_strength(
        estimate=0.05,
        se=0.05,
        observed_r2_outcome=0.2,
        observed_r2_treatment=0.1,
        dof=400,
    )
    assert res.breakpoint is not None
    assert res.breakpoint < 4.0  # small effect should be overturn-able within 4x


def test_calibrate_refuses_equal_target():
    with pytest.raises(ValueError, match="already equals"):
        sp.calibrate_confounding_strength(
            estimate=0.0,
            se=0.1,
            observed_r2_outcome=0.1,
            observed_r2_treatment=0.1,
            target_estimate=0.0,
            dof=100,
        )


def test_calibrate_requires_dof():
    with pytest.raises(ValueError, match="dof"):
        sp.calibrate_confounding_strength(
            estimate=0.3, se=0.1, observed_r2_outcome=0.1, observed_r2_treatment=0.1
        )


def test_calibrate_flags_impossible_multipliers():
    # k * R2_D~Xj >= 1 is impossible (sensemakr stops); the row is NaN.
    res = sp.calibrate_confounding_strength(
        estimate=0.3,
        se=0.1,
        observed_r2_outcome=0.1,
        observed_r2_treatment=0.3,
        dof=200,
    )
    bad = res.curve.loc[~res.curve["feasible"]]
    assert len(bad) > 0 and bad["adjusted_estimate"].isna().all()
    assert (bad["multiplier"] * 0.3 / 0.7 >= 1 - 1e-12).all() | (
        bad["multiplier"] * 0.3 >= 1
    ).all()
