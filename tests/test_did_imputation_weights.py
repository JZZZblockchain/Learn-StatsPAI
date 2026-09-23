"""``sp.did_imputation(weights=)`` against Stata ``did_imputation [aw=]`` on the
bundled castle-doctrine panel.

Reference values were produced on this machine with Stata 18 MP,
``did_imputation`` version 22nov2023 (Borusyak), on the byte-identical CSV
the DiD reconciliation study locks (``replication/applications/castle``)::

    import delimited castle.csv, clear
    gen Ei = gvar if gvar > 0                      // missing = never treated
    did_imputation l_homicide sid year Ei [aw=popwt], autosample
    did_imputation l_homicide sid year Ei [aw=popwt], ///
        horizons(0/5) pretrends(5) autosample minn(0)

Two contracts:

1. The weighted estimator is Stata's: estimate and standard error of the
   headline ATT, the horizons and the leads agree to 1e-6 relative.
2. The weighted estimator is linear in the outcome with the weight vector
   ``save_weights`` exposes: ``w'y`` reproduces the ATT to machine precision.
   This identity is what R ``didimputation`` 0.5.1 fails under weights (its
   variance builds the projection from ``Z * omega`` on both sides of the
   normal equations), and why the reconciliation study follows the Stata
   implementation for the weighted variance.
"""

from __future__ import annotations

import pytest

import statspai as sp

# (estimate, se) from Stata did_imputation [aw=popwt] on castle.csv
STATA_WT_ATT = (0.06593680767036858, 0.02550030676886575)
STATA_WT_DYN = {
    0: (0.01763079549709801, 0.02218932473290589),
    4: (0.0468900036503328, 0.03998505946731346),
}
STATA_WT_PRE = {-1: (-0.04704115923137493, 0.05147889224239272)}
# unweighted headline, same Stata run without [aw=]
STATA_UNW_ATT = (0.07980156409939809, 0.06088398010579676)

RTOL = 1e-6  # the paper's declared cross-software budget


@pytest.fixture(scope="module")
def castle():
    df = sp.datasets.castle_doctrine(event_time=True)
    df["gvar"] = df["gvar"].fillna(0).astype(int)
    return df.sort_values(["sid", "year"]).reset_index(drop=True)


def test_weighted_att_matches_stata(castle):
    r = sp.did_imputation(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        cluster="sid",
        weights="popwt",
    )
    assert r.estimate == pytest.approx(STATA_WT_ATT[0], rel=RTOL)
    assert r.se == pytest.approx(STATA_WT_ATT[1], rel=RTOL)
    assert r.model_info["weights"] == "popwt"


def test_unweighted_is_unchanged(castle):
    r = sp.did_imputation(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        cluster="sid",
    )
    assert r.estimate == pytest.approx(STATA_UNW_ATT[0], rel=RTOL)
    assert r.se == pytest.approx(STATA_UNW_ATT[1], rel=RTOL)


def test_weighted_horizons_and_leads_match_stata(castle):
    r = sp.did_imputation(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        cluster="sid",
        weights="popwt",
        horizon=list(range(0, 6)),
        pretrends=5,
    )
    es = r.model_info["event_study"].set_index("relative_time")
    for k, (est, se) in {**STATA_WT_DYN, **STATA_WT_PRE}.items():
        # estimates: reghdfe converges to ~1e-8 absolute, which is 1e-6 relative on a
        # 0.018 coefficient
        assert es.loc[k, "att"] == pytest.approx(est, rel=1e-5), k
        assert es.loc[k, "se"] == pytest.approx(se, rel=RTOL), k


def test_weighted_estimator_is_linear_with_exposed_weights(castle):
    r = sp.did_imputation(
        castle,
        y="l_homicide",
        group="sid",
        time="year",
        first_treat="gvar",
        cluster="sid",
        weights="popwt",
        save_weights=True,
    )
    w = r.model_info["estimation_weights"].to_numpy()
    assert float(w @ castle["l_homicide"].to_numpy()) == pytest.approx(
        r.estimate, rel=1e-10
    )
    assert abs(w.sum()) < 1e-10  # imputation weights sum to zero


def test_weights_validation(castle):
    bad = castle.copy()
    bad.loc[0, "popwt"] = -1.0
    with pytest.raises(ValueError, match="non-negative"):
        sp.did_imputation(
            bad,
            y="l_homicide",
            group="sid",
            time="year",
            first_treat="gvar",
            weights="popwt",
        )
    with pytest.raises(ValueError, match="not found"):
        sp.did_imputation(
            castle,
            y="l_homicide",
            group="sid",
            time="year",
            first_treat="gvar",
            weights="nope",
        )
    with pytest.raises(sp.MethodIncompatibility, match="project="):
        sp.did_imputation(
            castle,
            y="l_homicide",
            group="sid",
            time="year",
            first_treat="gvar",
            weights="popwt",
            project=["population"],
        )
