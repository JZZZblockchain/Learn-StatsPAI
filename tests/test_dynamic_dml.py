"""Contracts for sp.dynamic_dml (sequential treatment, Lewis & Syrgkanis 2021).

The estimand is the effect of *intervening* on each period's treatment on
the final outcome, so on a linear dynamic system it has a closed form: the
direct blip plus every path that runs through the states the treatment
moves. That closed form is what these tests check against, along with the
two things that silently break the estimator in practice -- an incomplete
state, and treating the periods as independent when summing them.
"""

import warnings

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression

import statspai as sp
from statspai.exceptions import (
    AssumptionWarning,
    DataInsufficient,
    MethodIncompatibility,
)

M = 3
A_T, B_T = 0.8, 0.5  # T_t = A_T W_t + B_T T_{t-1} + e
C_W, D_W = 0.6, 0.7  # W_t = C_W W_{t-1} + D_W T_{t-1} + v   (treatment moves state)
THETA = np.array([0.4, 0.6, 1.0])  # structural blips
PHI = np.array([0.5, 0.9, 1.3])  # state -> outcome
GAMMA = np.array([0.3, -0.5, 0.8])  # heterogeneity in the baseline modifier


def truth() -> np.ndarray:
    """Effect of intervening on each period, indirect paths included."""
    total = THETA.astype(float).copy()
    for t in range(M):
        for k in range(t + 1, M):
            total[t] += PHI[k] * D_W * (C_W ** (k - t - 1))
    return total


def dgp(seed: int, n_units: int = 4000, het: bool = False) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n_units)
    W = np.zeros((n_units, M))
    T = np.zeros((n_units, M))
    W[:, 0] = rng.normal(size=n_units)
    for t in range(M):
        if t:
            W[:, t] = C_W * W[:, t - 1] + D_W * T[:, t - 1] + rng.normal(size=n_units)
        T[:, t] = (
            A_T * W[:, t] + (B_T * T[:, t - 1] if t else 0.0) + rng.normal(size=n_units)
        )
    blips = THETA + (np.outer(x, GAMMA) if het else 0.0)
    y = (T * blips).sum(1) + (W * PHI).sum(1) + 0.4 * x + rng.normal(size=n_units)
    return pd.DataFrame(
        {
            "id": np.repeat(np.arange(n_units), M),
            "t": np.tile(np.arange(M), n_units),
            "y": np.repeat(y, M),
            "d": T.ravel(),
            "w": W.ravel(),
            "x": np.repeat(x, M),
        }
    )


def fit(df, **kw):
    kw.setdefault("model_y", LinearRegression())
    kw.setdefault("model_t", LinearRegression())
    kw.setdefault("n_folds", 4)
    return sp.dynamic_dml(df, y="y", treat="d", id="id", time="t", **kw)


@pytest.fixture(scope="module")
def fitted():
    return fit(dgp(0), covariates=["w"])


# --------------------------------------------------------------------------- #
#  Known truth
# --------------------------------------------------------------------------- #


def test_recovers_the_sequence_effect_including_indirect_paths(fitted):
    # The estimand is not the structural blip THETA: intervening on T_t also
    # moves W_{t+1}, ..., and the effect of setting the whole sequence
    # carries those paths. Recovering THETA here would be a bug.
    got = fitted.periods["estimate"].to_numpy()
    np.testing.assert_allclose(got, truth(), rtol=0.08)
    assert np.all(np.abs(got - THETA) > 0.1 * np.abs(truth() - THETA))


def test_every_period_is_within_four_standard_errors_of_the_truth(fitted):
    # Asserting that one draw's 95% interval covers would flake 5% of the
    # time by construction. Four standard errors is a correctness check with
    # a negligible false-failure rate; the coverage claim itself is measured
    # over replications in
    # tests/reference_parity/test_dynamic_dml_econml_parity.py.
    tab = fitted.periods
    z = (tab["estimate"].to_numpy() - truth()) / tab["se"].to_numpy()
    assert np.abs(z).max() < 4.0, tab


def test_total_effect_matches_the_sum_of_the_truth(fitted):
    z = (fitted.estimate - truth().sum()) / fitted.se
    assert abs(z) < 4.0, (fitted.estimate, fitted.se, truth().sum())
    np.testing.assert_allclose(fitted.estimate, truth().sum(), rtol=0.06)


def test_lag_index_counts_periods_before_the_outcome(fitted):
    assert list(fitted.periods["lag"]) == [M - 1, M - 2, 0]
    assert fitted.periods.index.name == "period"


# --------------------------------------------------------------------------- #
#  The two things that silently break it
# --------------------------------------------------------------------------- #


def test_dropping_the_treatment_history_biases_everything_and_warns():
    # Sequential ignorability needs T_{t-1} in the state: T_t depends on it,
    # and it predicts the later state. Without it the estimator is confident
    # and wrong, which is why lags=1 is the default and lags=0 warns.
    df = dgp(1, n_units=3000)
    good = fit(df, covariates=["w"], lags=1)
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        bad = fit(df, covariates=["w"], lags=0)
    hits = [w for w in rec if "treatment history" in str(w.message)]
    assert len(hits) == 1 and issubclass(hits[0].category, AssumptionWarning)

    tr = truth()
    good_err = np.abs(good.periods["estimate"].to_numpy() - tr) / tr
    bad_err = np.abs(bad.periods["estimate"].to_numpy() - tr) / tr
    assert good_err.max() < 0.10
    assert bad_err.max() > 0.25
    bad_z = (bad.periods["estimate"].to_numpy() - tr) / bad.periods["se"].to_numpy()
    assert np.abs(bad_z).min() > 4.0  # confident and wrong, every period
    assert bad.diagnostics["lagged_treatment_included"] is False
    assert good.diagnostics["lagged_treatment_included"] is True


def test_total_effect_uses_the_joint_covariance_not_a_sum_of_variances(fitted):
    # The period effects are negatively correlated here, so adding variances
    # would roughly double the standard error and make the total look far
    # less precise than it is.
    independent = fitted.diagnostics["independent_sum_se"]
    assert fitted.se < 0.75 * independent
    np.testing.assert_allclose(
        independent, np.sqrt(np.sum(fitted.periods["se"].to_numpy() ** 2)), rtol=1e-12
    )
    ones = np.ones(M)
    np.testing.assert_allclose(
        fitted.se, np.sqrt(ones @ fitted.vcov @ ones), rtol=1e-12
    )
    assert fitted.vcov.shape == (M, M)
    np.testing.assert_allclose(fitted.vcov, fitted.vcov.T, rtol=0, atol=1e-18)


# --------------------------------------------------------------------------- #
#  Contrasts
# --------------------------------------------------------------------------- #


def test_contrast_reproduces_the_total_and_single_periods(fitted):
    total = fitted.contrast([1] * M)
    np.testing.assert_allclose(total["estimate"], fitted.estimate, rtol=1e-12)
    np.testing.assert_allclose(total["se"], fitted.se, rtol=1e-12)
    last = fitted.contrast([0, 0, 1])
    np.testing.assert_allclose(
        last["estimate"], fitted.periods["estimate"].iloc[-1], rtol=1e-12
    )
    np.testing.assert_allclose(last["se"], fitted.periods["se"].iloc[-1], rtol=1e-12)


def test_contrast_rejects_the_wrong_number_of_weights(fitted):
    with pytest.raises(MethodIncompatibility, match="one weight per period"):
        fitted.contrast([1, 1])


def test_cumulative_walks_the_treat_from_here_on_profile(fitted):
    cum = fitted.cumulative()
    assert list(cum["n_periods_treated"]) == [3, 2, 1]
    np.testing.assert_allclose(cum["estimate"].iloc[0], fitted.estimate, rtol=1e-12)
    np.testing.assert_allclose(
        cum["estimate"].iloc[-1], fitted.periods["estimate"].iloc[-1], rtol=1e-12
    )
    # Treating for longer must move the estimate by the extra period's effect.
    np.testing.assert_allclose(
        cum["estimate"].iloc[0] - cum["estimate"].iloc[1],
        fitted.periods["estimate"].iloc[0],
        rtol=1e-12,
    )


# --------------------------------------------------------------------------- #
#  Heterogeneity
# --------------------------------------------------------------------------- #


def test_modifiers_recover_the_heterogeneity_slopes():
    res = fit(dgp(2, n_units=8000, het=True), covariates=["w"], modifiers=["x"])
    assert res.coef is not None
    block = res.coef.xs("x", level="term")
    slopes, slope_se = block["estimate"].to_numpy(), block["se"].to_numpy()
    assert np.abs((slopes - GAMMA) / slope_se).max() < 4.0, block
    np.testing.assert_allclose(slopes, GAMMA, atol=0.12)
    # The period effects are still read at the mean modifier value.
    tab = res.periods
    z = (tab["estimate"].to_numpy() - truth()) / tab["se"].to_numpy()
    assert np.abs(z).max() < 4.0, tab
    assert res.diagnostics["modifiers"] == ["x"]
    # Modifiers enter the state as well, or E[Y | state] omits a driver of
    # the outcome (and, with a varying effect, biases the periods).
    assert "x" in res.diagnostics["state_columns"]


def test_without_modifiers_there_is_no_coefficient_table(fitted):
    assert fitted.coef is None
    assert fitted.diagnostics["modifiers"] == []


# --------------------------------------------------------------------------- #
#  Panel handling and contracts
# --------------------------------------------------------------------------- #


def test_unbalanced_units_are_dropped_with_a_warning():
    df = dgp(3, n_units=600)
    df = df.drop(df[(df["id"] < 40) & (df["t"] == 2)].index)
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        res = fit(df, covariates=["w"])
    hits = [w for w in rec if "not observed in all" in str(w.message)]
    assert len(hits) == 1
    assert res.n_units == 560 and res.diagnostics["n_units_dropped"] == 40


def test_missing_values_drop_the_whole_unit():
    df = dgp(4, n_units=400)
    df.loc[df.index[5], "w"] = np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", AssumptionWarning)
        res = fit(df, covariates=["w"])
    assert res.n_units == 399  # the unit, not just the row
    assert res.diagnostics["n_units_dropped"] == 1


def test_duplicated_unit_period_is_refused():
    df = dgp(5, n_units=200)
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    with pytest.raises(MethodIncompatibility, match="duplicated unit-period"):
        fit(df, covariates=["w"])


def test_single_period_is_refused():
    df = dgp(6, n_units=200)
    with pytest.raises(DataInsufficient, match="at least two periods"):
        fit(df, covariates=["w"], periods=[0])


def test_no_complete_unit_is_refused():
    df = dgp(7, n_units=100)
    df = df[~((df["id"] % 2 == 0) & (df["t"] == 2))]
    df = df[~((df["id"] % 2 == 1) & (df["t"] == 1))]
    with pytest.raises(DataInsufficient, match="no unit is observed"):
        fit(df, covariates=["w"])


def test_unknown_column_names_the_column():
    df = dgp(8, n_units=120)
    with pytest.raises(MethodIncompatibility, match="nope"):
        fit(df, covariates=["nope"])


def test_more_folds_than_units_is_refused():
    df = dgp(9, n_units=6)
    with pytest.raises(DataInsufficient, match="cannot fill"):
        fit(df, covariates=["w"], n_folds=10)


@pytest.mark.parametrize("bad", [-1, 3, 1.5, True])
def test_bad_lags_are_refused(bad):
    df = dgp(10, n_units=200)
    with pytest.raises(MethodIncompatibility, match="lags"):
        fit(df, covariates=["w"], lags=bad)


def test_periods_selects_a_window():
    df = dgp(11, n_units=500)
    res = fit(df, covariates=["w"], periods=[1, 2], lags=1)
    assert res.n_periods == 2 and res.period_labels == [1, 2]
    assert res.periods.shape[0] == 2


def test_fold_ids_make_the_fit_reproducible():
    df = dgp(12, n_units=400)
    folds = np.arange(400) % 4
    a = fit(df, covariates=["w"], fold_ids=folds)
    b = fit(df, covariates=["w"], fold_ids=folds)
    np.testing.assert_array_equal(
        a.periods["estimate"].to_numpy(), b.periods["estimate"].to_numpy()
    )
    assert a.n_folds == 4


def test_baseline_controls_enter_every_period():
    df = dgp(13, n_units=500)
    res = fit(df, covariates=["w"], baseline=["x"])
    assert "x" in res.diagnostics["state_columns"]
    assert "d_lag1" in res.diagnostics["state_columns"]


def test_summary_and_registry():
    df = dgp(14, n_units=300)
    res = fit(df, covariates=["w"])
    text = res.summary()
    assert "Dynamic Double/Debiased ML" in text
    assert "Total (treat every period)" in text
    assert sp.describe_function("dynamic_dml") is not None
