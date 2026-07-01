"""Analytical parity: sp.pate transportability recovery.

The Population Average Treatment Effect reweights an experimental sample to a
target population's covariate distribution, so it estimates
``E_target[tau(X)]`` rather than the study SATE. On a known DGP with a
covariate-modified effect tau(x) = 1 + 0.5 x, an experiment drawn from
X ~ N(0, 1) has SATE = 1.0, while a target population with X ~ N(1, 1) has
PATE = E[1 + 0.5 X] = 1.5. The estimator tracks the *target* value, not the
sample SATE. Analytical evidence tier (known-truth recovery on a deterministic
DGP; no cross-package reference).
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import statspai as sp

TARGET_PATE = 1.5
SAMPLE_SATE = 1.0


def _simulate(seed, n=4000):
    rng = np.random.default_rng(seed)
    xe = rng.normal(0, 1, n)
    de = rng.integers(0, 2, n)
    ye = (1 + 0.5 * xe) * de + 0.7 * xe + rng.normal(0, 0.5, n)
    exp = pd.DataFrame({"y": ye, "d": de, "x": xe})
    tgt = pd.DataFrame({"x": rng.normal(1, 1, n)})  # shifted target
    return exp, tgt


def _fit(exp, tgt, seed):
    return sp.pate(
        exp, tgt, y="y", treatment="d", covariates=["x"], method="ipw", seed=seed
    )


def test_recovers_target_pate_across_seeds():
    ests = []
    for seed in range(6):
        exp, tgt = _simulate(seed)
        ests.append(float(_fit(exp, tgt, seed).estimate))
    assert float(np.mean(ests)) == pytest.approx(TARGET_PATE, abs=0.1)


def test_reweighting_moves_estimate_toward_target():
    # PATE should sit clearly above the sample SATE (1.0) since the target
    # population is shifted to higher X where tau(x) is larger.
    exp, tgt = _simulate(0)
    est = float(_fit(exp, tgt, 0).estimate)
    assert est > (SAMPLE_SATE + TARGET_PATE) / 2  # past the midpoint toward target
