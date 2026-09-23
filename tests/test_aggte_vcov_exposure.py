"""``sp.aggte`` exposes the joint covariance of its cells, and the joint tests
that consume it read that object instead of a diagonal approximation.

Three contracts, each pinned to something that can be checked without a
reference implementation:

1. ``model_info['vcov']`` is the covariance the reported standard errors came
   from: ``sqrt(diag(vcov)) == detail['se']`` exactly, for every aggregation.
2. ``honest_did(method='smoothness')`` on a dynamic ``aggte`` result runs the
   FLCI on that covariance (no fallback warning) and gives the same answer
   whether it is handed the ``aggte`` result or the raw Callaway--Sant'Anna
   fit -- the two routes used to disagree because the raw-fit route rebuilt
   the covariance with fixed cohort shares.
3. The Callaway--Sant'Anna joint pre-trend test on ATT(g, t) cells is
   rank-aware.  On a panel whose pre-treatment cells are linearly dependent
   the old ridge-and-invert code returned a statistic of order 1e9; the
   spectral pseudo-inverse returns a finite quadratic form with ``df`` equal
   to the rank, and on a full-rank panel it reproduces the plain inverse.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp


def _panel(n_per_cohort: int = 12, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    unit = 0
    for cohort in (0, 4, 6):
        for _ in range(n_per_cohort):
            fe = rng.normal(0, 0.3)
            for t in range(1, 9):
                treated = cohort > 0 and t >= cohort
                rows.append(
                    (
                        unit,
                        t,
                        cohort,
                        fe + 0.1 * t + rng.normal(0, 0.5) + (0.3 if treated else 0.0),
                    )
                )
            unit += 1
    return pd.DataFrame(rows, columns=["unit", "time", "g", "y"])


@pytest.fixture(scope="module")
def cs():
    return sp.callaway_santanna(
        _panel(),
        y="y",
        g="g",
        t="time",
        i="unit",
        estimator="reg",
        control_group="nevertreated",
        base_period="universal",
    )


@pytest.mark.parametrize("agg", ["simple", "dynamic", "group", "calendar"])
def test_vcov_diagonal_is_the_reported_se(cs, agg):
    r = sp.aggte(cs, type=agg, bstrap=False, cband=False)
    V = r.model_info["vcov"]
    assert V.shape == (len(r.detail), len(r.detail))
    assert r.model_info["vcov_source"] == "influence_functions"
    np.testing.assert_allclose(np.sqrt(np.diag(V)), r.detail["se"].values, rtol=1e-12)
    # symmetric, positive semi-definite
    np.testing.assert_allclose(V, V.T, atol=1e-15)
    assert np.linalg.eigvalsh(V).min() > -1e-12


def test_dynamic_result_carries_pre_block(cs):
    d = sp.aggte(cs, type="dynamic", bstrap=False, cband=False)
    pre = d.detail["relative_time"].values < 0
    assert d.model_info["pre_event_times"] == [
        int(e) for e in d.detail["relative_time"].values[pre]
    ]
    np.testing.assert_allclose(
        d.model_info["vcv_pre"], d.model_info["vcov"][np.ix_(pre, pre)]
    )


def test_honest_did_uses_the_exposed_covariance(cs):
    d = sp.aggte(cs, type="dynamic", bstrap=False, cband=False)
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # any fallback warning fails the test
        via_aggte = sp.honest_did(d, e=0, method="smoothness", m_grid=[0.0, 0.05])
        via_fit = sp.honest_did(cs, e=0, method="smoothness", m_grid=[0.0, 0.05])
    pd.testing.assert_frame_equal(via_aggte, via_fit)
    # at M = 0 the FLCI is at least as tight as the Wald interval on the
    # target coefficient (it may extrapolate from the pre-period)
    row0 = d.detail[d.detail["relative_time"] == 0].iloc[0]
    wald_len = 2 * 1.959963984540054 * row0["se"]
    assert (
        via_aggte.iloc[0]["ci_upper"] - via_aggte.iloc[0]["ci_lower"] <= wald_len + 1e-9
    )


def test_pretrends_power_reads_full_covariance(cs):
    d = sp.aggte(cs, type="dynamic", bstrap=False, cband=False)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        out = sp.pretrends_power(d)
    assert 0.0 <= out["power"] <= 1.0


def test_pretrend_test_is_rank_aware(cs):
    pt = cs.model_info["pretrend_test"]
    assert np.isfinite(pt["statistic"])
    assert pt["df"] == pt["rank"] <= pt["n_cells"]
    assert 0.0 <= pt["pvalue"] <= 1.0
    # reproduce the statistic from the exposed influence functions
    pre = cs.detail["relative_time"].values < 0
    psi = cs._influence_funcs[:, pre]
    V = psi.T @ psi / cs.model_info["n_units"] ** 2
    theta = cs.detail["att"].values[pre]
    w, v = np.linalg.eigh(0.5 * (V + V.T))
    keep = w > w.max() * pre.sum() * np.finfo(float).eps * 1e3
    stat = float(np.sum((v[:, keep].T @ theta) ** 2 / w[keep]))
    assert pt["statistic"] == pytest.approx(stat, rel=1e-10)
    assert pt["rank"] == int(keep.sum())


def test_pretrend_test_rank_deficient_design_does_not_explode():
    # Seven units, three of them single-unit cohorts, ten periods: 17
    # pre-treatment cells but at most six independent influence-function
    # directions, so the pre-period covariance is singular by construction.
    rng = np.random.default_rng(3)
    rows = []
    unit = 0
    for cohort, count in ((0, 4), (6, 1), (8, 1), (9, 1)):
        for _ in range(count):
            fe = rng.normal(0, 0.3)
            for t in range(1, 11):
                treated = cohort > 0 and t >= cohort
                rows.append(
                    (
                        unit,
                        t,
                        cohort,
                        fe + 0.1 * t + rng.normal(0, 0.5) + (0.3 if treated else 0.0),
                    )
                )
            unit += 1
    df = pd.DataFrame(rows, columns=["unit", "time", "g", "y"])
    fit = sp.callaway_santanna(
        df,
        y="y",
        g="g",
        t="time",
        i="unit",
        estimator="reg",
        control_group="nevertreated",
        base_period="universal",
    )
    pt = fit.model_info["pretrend_test"]
    assert pt["n_cells"] == 17
    assert pt["rank_deficient"] is True
    assert pt["rank"] <= 6
    assert (
        np.isfinite(pt["statistic"]) and pt["statistic"] < 1e4
    )  # ridge-and-invert gave ~1e9-scale numbers
    assert 0.0 <= pt["pvalue"] <= 1.0
