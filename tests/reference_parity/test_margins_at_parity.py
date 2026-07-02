"""Analytical parity: sp.margins_at exact predictive-margin identity.

Predictive margins at fixed covariate values are an exact linear form of the
OLS coefficients: setting x to v and averaging the other regressors over the
sample gives

    margin(x=v) == b0 + b_x * v + b_z * mean(z)

which matches a hand computation to machine precision (observed diff 0). The
symmetric grid x in {-1, 0, 1} also produces symmetric standard errors.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import statspai as sp

GRID = [-1.0, 0.0, 1.0]


@pytest.fixture(scope="module")
def fitted():
    rng = np.random.default_rng(0)
    n = 1500
    x = rng.normal(0, 1, n)
    z = rng.normal(0, 1, n)
    y = 1 + 0.8 * x + 0.5 * z + rng.normal(0, 0.5, n)
    df = pd.DataFrame({"y": y, "x": x, "z": z})
    res = sp.regress("y ~ x + z", data=df)
    return df, res, sp.margins_at(res, data=df, at={"x": GRID})


def test_margins_match_linear_prediction(fitted):
    df, res, tab = fitted
    b = res.params
    zbar = df["z"].mean()
    got = {float(row["x"]): float(row["margin"]) for _, row in tab.iterrows()}
    for v in GRID:
        expected = b["Intercept"] + b["x"] * v + b["z"] * zbar
        assert got[v] == pytest.approx(expected, abs=1e-10)


def test_symmetric_grid_symmetric_se(fitted):
    _, _, tab = fitted
    se = {float(row["x"]): float(row["se"]) for _, row in tab.iterrows()}
    # se at x=-1 and x=+1 are equal (symmetry about the mean); center is smallest
    assert se[-1.0] == pytest.approx(se[1.0], abs=1e-10)
    assert se[0.0] < se[1.0]
