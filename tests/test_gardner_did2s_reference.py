"""Reference parity: ``sp.gardner_did`` standard errors vs R/Stata ``did2s``.

Pins the Butts--Gardner (2022) two-stage corrected clustered variance on the
Cheng--Hoekstra castle-doctrine panel (``sp.datasets.castle_doctrine``), for
the static ATT and for every relative-time coefficient of the saturated event
study, unweighted and population-weighted.

Provenance of the constants
---------------------------
R side (the canonical reference, ``did2s`` is Butts & Gardner's own
implementation): ``did2s`` 1.2.1, ``fixest`` 0.14.0,
R version 4.5.2 (2025-10-31), aarch64-apple-darwin20, executed 2026-09-07 by
``Paper-DiD-JAE/replication/applications/_common/run_R.R`` on
``castle/data/castle.csv`` (SHA-256
``a1cf71b325c7cffabdfe2c1bf9755f4d5cb100ec71c27723a47b59a394c32ced``), a panel
that is column-for-column identical to ``sp.datasets.castle_doctrine(
event_time=True)`` (``sid``, ``year``, ``l_homicide``, ``gvar`` with 0 = never
treated, ``popwt``; verified with ``numpy.array_equal`` before pinning).
The calls were::

    did2s(d, yname = "l_homicide", first_stage = ~ 0 | sid + year,
          second_stage = ~ treat,                     # "att"
          treatment = "treat", cluster_var = "sid"[, weights = "popwt"])
    did2s(d, yname = "l_homicide", first_stage = ~ 0 | sid + year,
          second_stage = ~ i(rel, ref = c(-1, -1000)),  # "dyn_e{k}"
          treatment = "treat", cluster_var = "sid"[, weights = "popwt"])

with ``treat = 1{year >= gvar}`` for adopters, ``rel = year - gvar`` and the
never-treated coded ``-1000``. Stata ``did2s`` v0.5 (Stata 18) on the same
CSV agrees with R on every row to 1.2e-07 relative on the estimate
and 1.2e-08 on the SE, so the R numbers below stand for both references.

Tolerance: ``rel=1e-6`` on estimate and SE (CLAUDE.md §5.1 T2). Observed on
2026-09-07: unweighted worst 2.8e-9, weighted worst 1.2e-7 (the weighted
point estimates carry fixest's iterative demeaning tolerance; the SEs are
at 1e-8).

References
----------
Butts, K. and Gardner, J. (2022). did2s: Two-Stage Difference-in-Differences.
*R Journal*, 14(3), 162-173. [@butts2022stage]
Gardner, J. (2022). Two-stage differences in differences. arXiv:2207.05943.
[@gardner2022twostage]
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp

REL = 1e-6

# (estimate, se) from castle_R.json, estimator == "did2s", spec == "unw".
R_UNW_ATT = (0.079801547713374, 0.0609789882894638)
R_UNW_DYN = {
    -9: (-0.171286064950389, 0.0307272522117777),
    -8: (-0.0259978828055484, 0.146964375308744),
    -7: (-0.19178299914089, 0.0858483276238106),
    -6: (0.0394654349100029, 0.0295682323104704),
    -5: (0.0138838286655264, 0.0295428129221351),
    -4: (-0.016116266460033, 0.0271471264659165),
    -3: (0.0289119413000516, 0.0197398174954507),
    -2: (0.0329448489309216, 0.0312180997342677),
    0: (0.0710705994708897, 0.0577589180282935),
    1: (0.0928844567463144, 0.0633702867537619),
    2: (0.0767730116461888, 0.0786996513487697),
    3: (0.100185177897873, 0.0795975872308234),
    4: (0.0502468940830696, 0.0739403468433287),
    5: (0.0958408999607778, 0.0458734039149931),
}

# spec == "wt": weights = "popwt" (Stata ``[aw=popwt]``).
R_WT_ATT = (0.0659367931285578, 0.0282004391800215)
R_WT_DYN = {
    -9: (-0.200803447598062, 0.0193615821496832),
    -8: (-0.153001287624103, 0.0387287332881592),
    -7: (-0.049649233734802, 0.0339428073317867),
    -6: (0.0478512712506468, 0.0167356659411754),
    -5: (0.0232006472708082, 0.0145817670690438),
    -4: (-0.0103615695829782, 0.0161063912406936),
    -3: (0.0134015054563927, 0.0145095476998044),
    -2: (0.00310130908268144, 0.0149282717098072),
    0: (0.0176307737962924, 0.0301161623719765),
    1: (0.0967059143911821, 0.0323585345093071),
    2: (0.079444110001191, 0.0378100750442217),
    3: (0.0747030759945081, 0.0456100913532877),
    4: (0.0468900124540102, 0.0485946060330947),
    5: (0.12303686946441, 0.0419613210639413),
}

HORIZON = list(range(-9, 6))  # full support of rel on castle; -1 is R's ref


@pytest.fixture(scope="module")
def castle() -> pd.DataFrame:
    d = sp.datasets.castle_doctrine(event_time=True).copy()
    d["gvar"] = d["gvar"].fillna(0)
    assert len(d) == 550 and d["sid"].nunique() == 50
    return d


def _label(k: int) -> str:
    return f"D_k{k:+d}"


@pytest.mark.parametrize(
    "weights, expected",
    [(None, R_UNW_ATT), ("popwt", R_WT_ATT)],
    ids=["unweighted", "popwt"],
)
def test_static_att_matches_did2s(castle, weights, expected):
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # the anti-conservatism warning is gone
        res = sp.gardner_did(
            castle,
            y="l_homicide",
            group="sid",
            time="year",
            first_treat="gvar",
            weights=weights,
        )
    att_r, se_r = expected
    assert res.estimate == pytest.approx(att_r, rel=REL)
    assert res.se == pytest.approx(se_r, rel=REL)
    assert res.model_info["vce"] == "analytic"
    assert res.model_info["n_clusters"] == 50


@pytest.mark.parametrize(
    "weights, expected",
    [(None, R_UNW_DYN), ("popwt", R_WT_DYN)],
    ids=["unweighted", "popwt"],
)
def test_event_study_matches_did2s_at_every_horizon(castle, weights, expected):
    res = sp.gardner_did(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        event_study=True,
        horizon=HORIZON,
        weights=weights,
    )
    es = res.model_info["event_study"]
    assert set(expected) == {k for k in HORIZON if k != -1}
    for k, (att_r, se_r) in expected.items():
        assert es["coef"][_label(k)] == pytest.approx(att_r, rel=REL), k
        assert es["se"][_label(k)] == pytest.approx(se_r, rel=REL), k
    # The full covariance is exposed with its labels, and the reported SEs
    # are its square-root diagonal.
    V = res.model_info["vcov"]
    labels = res.model_info["cell_labels"]
    assert V.shape == (len(labels), len(labels))
    assert np.allclose(np.sqrt(np.diag(V)), [es["se"][lab] for lab in labels])


@pytest.mark.parametrize("weights", [None, "popwt"], ids=["unweighted", "popwt"])
def test_event_study_aggregate_equals_static_att(castle, weights):
    """The weight-share average of the post coefficients is the static ATT.

    Every post-treatment horizon (0..5) is in HORIZON, so the aggregate
    must reproduce the ``~ treat`` coefficient exactly. Its SE is the
    delta-method SE on the saturated covariance and is documented to
    differ from the static-ATT SE (different Stage-2 residuals).
    """
    static = sp.gardner_did(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        weights=weights,
    )
    dyn = sp.gardner_did(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        event_study=True,
        horizon=HORIZON,
        weights=weights,
    )
    assert dyn.estimate == pytest.approx(static.estimate, rel=1e-10)
    assert np.isfinite(dyn.se) and dyn.se > 0
    assert dyn.se == pytest.approx(static.se, rel=0.05)  # same order, not equal


def test_vce_none_skips_inference(castle):
    res = sp.gardner_did(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        vce="none",
    )
    assert res.estimate == pytest.approx(R_UNW_ATT[0], rel=REL)
    assert np.isnan(res.se) and np.isnan(res.pvalue)
    assert res.model_info["vcov"] is None


def test_single_cluster_raises(castle):
    """One cluster makes the cluster sum identically zero; say so."""
    d = castle.assign(one=1)
    with pytest.raises(ValueError, match="at least two clusters"):
        sp.gardner_did(
            d,
            y="l_homicide",
            group="sid",
            time="year",
            first_treat="gvar",
            cluster="one",
        )


def test_nonpositive_weights_raise(castle):
    d = castle.copy()
    d.loc[d.index[0], "popwt"] = 0.0
    with pytest.raises(ValueError, match="strictly positive"):
        sp.gardner_did(
            d,
            y="l_homicide",
            group="sid",
            time="year",
            first_treat="gvar",
            weights="popwt",
        )
