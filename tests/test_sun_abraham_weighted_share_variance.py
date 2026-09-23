"""``sp.sun_abraham(weights=)`` standard errors against Stata
``eventstudyinteract ... [aw=]`` on the bundled castle-doctrine panel.

Reference values were produced on this machine with Stata 18 MP,
``eventstudyinteract`` version 0.1 (Liyang Sun), on the byte-identical CSV the
DiD reconciliation study locks (``replication/applications/castle``)::

    import delimited castle.csv, clear
    gen cohort = gvar if gvar > 0
    gen never  = (gvar == 0)
    gen rel    = year - gvar if gvar > 0
    forvalues k = 9(-1)2 { gen g_m`k' = (rel == -`k'); replace g_m`k' = 0 if never }
    forvalues k = 0/5    { gen g_p`k' = (rel ==  `k'); replace g_p`k' = 0 if never }
    eventstudyinteract l_homicide g_m9-g_m2 g_p0-g_p5 [aw=popwt], cohort(cohort) ///
        control_cohort(never) absorb(i.sid i.year) vce(cluster sid)
    // sqrt of diag(e(V_iw))

The point estimates already agreed. The standard errors did not at
multi-cohort relative times (0.8 to 2.9 percent), because the cohort-share
covariance term of Sun and Abraham (2021, Prop. 3) was built from the
unweighted multinomial form; eventstudyinteract builds it from the weighted
share regression's robust sandwich, ``sum omega_i^2 u_i u_i' / (sum omega_i)^2``
with omega rescaled to mean one. Single-cohort relative times (where the
share term vanishes) were unaffected, which is why the gap hid.
"""

from __future__ import annotations

import pytest

import statspai as sp

STATA_WT_SE = {
    -9: 0.0379246670,
    -8: 0.0535122815,
    -7: 0.0757572750,
    -6: 0.0470302926,
    -5: 0.0348140056,
    -4: 0.0371974275,
    -3: 0.0294842783,
    -2: 0.0267502981,
    0: 0.0313481411,
    1: 0.0294424348,
    2: 0.0361382194,
    3: 0.0424150404,
    4: 0.0506993563,
    5: 0.0472425459,
}
# reghdfe's iterative solver converges to ~1e-7 relative on the IW covariance
RTOL = 1e-6


@pytest.fixture(scope="module")
def castle():
    df = sp.datasets.castle_doctrine(event_time=True)
    df["gvar"] = df["gvar"].fillna(0).astype(int)
    return df.sort_values(["sid", "year"]).reset_index(drop=True)


def test_weighted_event_study_se_matches_eventstudyinteract(castle):
    r = sp.sun_abraham(
        castle,
        y="l_homicide",
        g="gvar",
        t="year",
        i="sid",
        control_group="nevertreated",
        weights="popwt",
        share_variance=True,
    )
    es = r.model_info["event_study"].set_index("relative_time")
    for k, se in STATA_WT_SE.items():
        assert es.loc[k, "se"] == pytest.approx(se, rel=RTOL), k


def test_weighted_share_term_is_positive_only_where_cohorts_pool(castle):
    on = sp.sun_abraham(
        castle,
        y="l_homicide",
        g="gvar",
        t="year",
        i="sid",
        control_group="nevertreated",
        weights="popwt",
        share_variance=True,
    )
    off = sp.sun_abraham(
        castle,
        y="l_homicide",
        g="gvar",
        t="year",
        i="sid",
        control_group="nevertreated",
        weights="popwt",
        share_variance=False,
    )
    a = on.model_info["event_study"].set_index("relative_time")
    b = off.model_info["event_study"].set_index("relative_time")
    # k = -9 is served by the 2009 cohort alone: no share term
    assert a.loc[-9, "se"] == pytest.approx(b.loc[-9, "se"], rel=1e-12)
    # k = 0 pools five cohorts: the term is positive semi-definite
    assert a.loc[0, "se"] >= b.loc[0, "se"]
