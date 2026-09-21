"""Ordinary IRM propensity regressors retain upstream clipping semantics."""

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import StratifiedKFold

import statspai as sp


def _inputs(weighted):
    rng = np.random.default_rng(42)
    x = np.linspace(-3, 3, 200)
    d = (rng.uniform(size=200) < 1 / (1 + np.exp(-2 * x))).astype(int)
    frame = pd.DataFrame({"x": x, "d": d, "y": 2 * d + x + rng.normal(size=200)})
    weights = np.linspace(0.5, 2.0, len(frame)) if weighted else None
    return frame, weights


def _clipped_reference(frame, weights):
    """Independent cross-fit regressions and pre-OOF AIPW/sandwich formula."""
    x = frame[["x"]].to_numpy()
    y, d = frame.y.to_numpy(), frame.d.to_numpy()
    g0, g1, raw = (np.zeros(len(frame)) for _ in range(3))
    splits = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
    for train, test in splits.split(x, d):
        for arm, predictions in ((0, g0), (1, g1)):
            rows = train[d[train] == arm]
            model = LinearRegression().fit(
                x[rows],
                y[rows],
                sample_weight=None if weights is None else weights[rows],
            )
            predictions[test] = model.predict(x[test])
        model = LinearRegression().fit(
            x[train],
            d[train],
            sample_weight=None if weights is None else weights[train],
        )
        raw[test] = model.predict(x[test])
    propensity = np.clip(raw, 0.01, 0.99)
    pseudo = g1 - g0 + d * (y - g1) / propensity
    pseudo -= (1 - d) * (y - g0) / (1 - propensity)
    if weights is None:
        theta = np.mean(pseudo)
        se = np.std(pseudo, ddof=0) / np.sqrt(len(frame))
    else:
        theta = np.sum(weights * pseudo) / np.sum(weights)
        se = np.sqrt(np.sum(weights**2 * (pseudo - theta) ** 2)) / np.sum(weights)
    return theta, se, raw, pseudo


@pytest.mark.parametrize("weighted", [False, True])
def test_ordinary_ate_clips_propensity_regression_predictions(weighted):
    frame, weights = _inputs(weighted)
    theta, se, raw, pseudo = _clipped_reference(frame, weights)
    assert raw.min() < 0 and raw.max() > 1

    result = sp.DoubleMLIRM(
        frame,
        y="y",
        treat="d",
        covariates=["x"],
        ml_g=LinearRegression(),
        ml_m=LinearRegression(),
        n_folds=2,
        sample_weight=weights,
    ).fit()

    # Same folds/learners/formula: allow only floating-point reduction noise.
    np.testing.assert_allclose(
        [result.estimate, result.se], [theta, se], rtol=1e-14, atol=1e-14
    )
    np.testing.assert_array_equal(result.model_info["_pscore"], raw)
    np.testing.assert_allclose(
        result.model_info["_y_resid"], pseudo - theta, rtol=1e-14, atol=1e-14
    )
    diagnostics = result.model_info["diagnostics"]
    assert diagnostics["pscore_min"] == raw.min()
    assert diagnostics["pscore_max"] == raw.max()
    assert diagnostics["n_clipped_below"] == np.sum(raw < 0.01)
    assert diagnostics["n_clipped_above"] == np.sum(raw > 0.99)
    if not weighted:
        # Independently reviewed upstream 42147197 reproduction.
        np.testing.assert_allclose(
            [result.estimate, result.se],
            [1.7222670559572055, 0.25276749479811816],
            rtol=1e-14,
            atol=1e-14,
        )


def test_retained_ate_rejects_out_of_range_propensity_regression_predictions():
    frame, _ = _inputs(False)
    estimator = sp.DoubleMLIRM(
        frame,
        y="y",
        treat="d",
        covariates=["x"],
        ml_g=LinearRegression(),
        ml_m=LinearRegression(),
        n_folds=2,
    )
    with pytest.raises(ValueError, match="ps_raw must lie"):
        estimator.fit(store_oof=True)

    # A failed retained fit must not leave capture state affecting later fits.
    result = estimator.fit()
    assert np.isfinite(result.estimate) and np.isfinite(result.se)
