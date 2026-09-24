"""``CausalForest.get_nuisances()`` and the fit-time propensity-overlap check."""

import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp
from statspai.exceptions import AssumptionWarning, MethodIncompatibility


def _data(n=300, seed=20260922, strength=None):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 3))
    if strength is None:
        p = 1 / (1 + np.exp(-(0.6 * X[:, 0] - 0.4 * X[:, 1])))
    else:
        p = 1 / (1 + np.exp(-strength * X[:, 0]))
    D = rng.binomial(1, p)
    Y = 1.5 * D + X @ np.array([1.0, -0.5, 0.3]) + 0.5 * D * X[:, 2]
    Y = Y + rng.normal(size=n)
    df = pd.DataFrame(X, columns=["x1", "x2", "x3"])
    df["y"], df["d"] = Y, D
    return df


def _overlap_warnings(record):
    return [
        w
        for w in record
        if issubclass(w.category, AssumptionWarning)
        and "internal propensities" in str(w.message)
    ]


def _fit(df, **kw):
    kw.setdefault("n_estimators", 200)
    kw.setdefault("random_state", 1)
    return sp.causal_forest("y ~ d | x1 + x2 + x3", data=df, **kw)


# Re-pinned for the engine seeding fix (independent per-group seeds and
# per-nuisance random streams; see CHANGELOG): the forest for random_state=1
# is a different draw, the ATE moving 1.322 -> 1.394 on this n = 300 design
# (SE ~ 0.15, truth ~ 1.5). Originally pinned from origin/main 4bf29552 on
# macOS/arm64.
# These are coarse regression canaries, NOT a cross-platform contract: the
# engine is bit-deterministic for a given random_state on a given machine
# (verified for 1, 2, 4 and 8 numba threads), but a split is an argmax over
# criteria, so a difference in summation order -- which is what a different
# SIMD width gives you -- flips a split and the whole subtree below it.
# Measured on this DGP: jittering X and y by a *relative 1e-15*, i.e. pure
# round-off, moves the ATE by up to 4.7e-3 relative while leaving
# ``W_hat.sum()`` bit-identical. The original rtol=1e-9 duly passed on
# macOS/arm64 and failed on the Linux/x86-64 pandas-3 leg by 2.9e-4 with
# every library version identical. Do not re-tighten these; a real engine
# regression moves them by far more than a percent.
_ATE_PIN_RTOL = 2e-2
_W_PIN_RTOL = 1e-3


def test_estimate_unchanged_and_nuisances_exposed():
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        cf = _fit(_data())
    assert not _overlap_warnings(rec)
    np.testing.assert_allclose(
        cf.diagnostics["average_treatment_effect"],
        1.394246631218219,
        rtol=_ATE_PIN_RTOL,
    )
    np.testing.assert_allclose(float(cf.ate()), 1.3552878639464825, rtol=_ATE_PIN_RTOL)
    nu = cf.get_nuisances()
    np.testing.assert_array_equal(nu["W_hat"], cf._e_insample)
    np.testing.assert_array_equal(nu["Y_hat"], cf._m_insample)
    np.testing.assert_allclose(nu["W_hat"].sum(), 158.89617422293276, rtol=_W_PIN_RTOL)
    assert not nu["W_hat"].flags.writeable and not nu["Y_hat"].flags.writeable
    assert nu["W_hat"] is not cf._e_insample  # a copy, internals untouched
    assert nu["source"] == {
        "Y_hat": "grf regression forest (OOB)",
        "W_hat": "grf regression forest (OOB)",
    }
    ov = cf.diagnostics["nuisance_overlap"]
    assert ov["applicable"] is True and ov["warning"] is False
    assert nu["overlap"] == ov


def test_weak_overlap_warns_and_records():
    df = _data(n=600, strength=8.0)
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        cf = _fit(df)
    hits = _overlap_warnings(rec)
    assert len(hits) == 1
    ov = cf.diagnostics["nuisance_overlap"]
    e = cf.get_nuisances()["W_hat"]
    share = np.mean((e < 0.01) | (e > 0.99))
    assert ov["warning"] is True
    assert ov["share_outside"] == pytest.approx(share)
    assert share > cf.NUISANCE_OVERLAP_MAX_SHARE
    assert ov["n_below"] + ov["n_above"] == int(np.sum((e < 0.01) | (e > 0.99)))


def test_warning_is_attributed_to_the_caller():
    df = _data(n=600, strength=8.0)
    for fit in (
        lambda: _fit(df),
        lambda: sp.CausalForest(n_estimators=200, random_state=1).fit(
            "y ~ d | x1 + x2 + x3", data=df
        ),
    ):
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always")
            fit()
        hits = _overlap_warnings(rec)
        assert len(hits) == 1
        assert hits[0].filename == __file__


def test_fit_is_bit_deterministic_given_random_state():
    # What the absolute pins above were really guarding, stated so that it
    # holds on every platform rather than on the one they were taken from.
    df = _data()
    a, b = _fit(df), _fit(df)
    assert float(a.ate()) == float(b.ate())
    assert (
        a.diagnostics["average_treatment_effect"]
        == b.diagnostics["average_treatment_effect"]
    )
    np.testing.assert_array_equal(
        a.get_nuisances()["W_hat"], b.get_nuisances()["W_hat"]
    )
    np.testing.assert_array_equal(
        a.effect(df[["x1", "x2", "x3"]]), b.effect(df[["x1", "x2", "x3"]])
    )


def test_warning_does_not_change_estimate():
    df = _data(n=600, strength=8.0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        a = _fit(df)
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        b = _fit(df)
    assert float(a.ate()) == float(b.ate())


def test_supplied_w_hat_is_checked_and_reported():
    df = _data(n=400)
    w_hat = np.where(np.arange(len(df)) % 4 == 0, 0.001, 0.5)
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        cf = _fit(df, W_hat=w_hat)
    assert _overlap_warnings(rec)
    nu = cf.get_nuisances()
    np.testing.assert_array_equal(nu["W_hat"], w_hat)
    assert nu["source"]["W_hat"] == "user-supplied"
    assert cf.diagnostics["nuisance_overlap"]["share_outside"] == pytest.approx(0.25)


def test_continuous_treatment_is_not_checked():
    rng = np.random.default_rng(3)
    n = 300
    X = rng.normal(size=(n, 2))
    T = X[:, 0] + rng.normal(size=n)
    Y = T * X[:, 1] + rng.normal(size=n)
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        cf = sp.causal_forest(
            Y=Y, T=T, X=X, discrete_treatment=False, n_estimators=100, random_state=0
        )
    assert not _overlap_warnings(rec)
    assert cf.diagnostics["nuisance_overlap"]["applicable"] is False


def test_get_nuisances_requires_fit():
    with pytest.raises(MethodIncompatibility):
        sp.CausalForest().get_nuisances()
