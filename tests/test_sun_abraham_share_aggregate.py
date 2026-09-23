"""The Sun-Abraham aggregate ATT under both variance conventions.

Stata ``eventstudyinteract`` stores the joint covariance of the interaction-
weighted event-time coefficients with the cohort-share estimation term
(``e(V_iw)``); a ``lincom`` on it with the fixest ``agg='att'`` weights is the
aggregate's standard error under that convention. R ``fixest::sunab``'s
``agg='att'`` treats the shares as fixed. ``sp.sun_abraham`` exposes both:
``model_info['se_fixest_att_share']`` and ``model_info['se_fixest_att']``.

Reference values are the Stata and R rows of the DiD reconciliation study
(Paper-DiD-JAE, ``replication/applications/<app>/results``), captured with
eventstudyinteract 0.1 / avar and fixest 0.14.0 on the locked castle-doctrine
and no-fault-divorce panels.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import statspai as sp

FIX = Path(__file__).parent / "fixtures"

# (panel, weights) -> (Stata e(V_iw) lincom SE, R fixest agg='att' SE)
REFERENCE = {
    ("castle", None): (0.0419209965, 0.0413168895),
    ("castle", "popwt"): (0.0271543866, 0.0257587248),
    ("divorce", None): (3.4745723570, 3.4614005897),
    ("divorce", "weight"): (2.8450017306, 2.6898223423),
}


def _panel(name: str) -> tuple[pd.DataFrame, dict]:
    if name == "castle":
        df = (
            sp.datasets.castle_doctrine()
            if hasattr(sp.datasets, "castle_doctrine")
            else None
        )
        if df is None or "gvar" not in df.columns:
            pytest.skip("castle-doctrine panel with cohort column not shipped")
        return df, dict(y="l_homicide", g="gvar", t="year", i="sid")
    df = pd.read_csv(FIX / "divorce_no_fault_panel.csv")
    df = df[df["always_treated"] == 0]
    return df, dict(y="asmrs", g="nfd", t="year", i="stfips")


@pytest.mark.parametrize("panel,weights", sorted(REFERENCE, key=str))
def test_share_and_fixed_share_aggregates_reproduce_both_references(panel, weights):
    df, cfg = _panel(panel)
    fit = sp.sun_abraham(df, **cfg, control_group="nevertreated", weights=weights)
    se_share, se_fixed = REFERENCE[(panel, weights)]
    mi = fit.model_info
    assert mi["se_fixest_att_share"] == pytest.approx(se_share, rel=5e-9)
    assert mi["se_fixest_att"] == pytest.approx(se_fixed, rel=5e-9)
    assert mi["se_fixest_att_share"] > mi["se_fixest_att"]


def test_joint_event_time_vcov_diagonal_matches_reported_se():
    df, cfg = _panel("divorce")
    fit = sp.sun_abraham(df, **cfg, control_group="nevertreated")
    V = np.asarray(fit.model_info["vcov_event_time"])
    es = fit.model_info["event_times"]
    detail = fit.detail.set_index("relative_time")
    for j, e in enumerate(es):
        assert np.sqrt(V[j, j]) == pytest.approx(float(detail.loc[e, "se"]), rel=1e-12)
    assert np.allclose(V, V.T)


def test_without_share_term_both_aggregates_coincide():
    df, cfg = _panel("divorce")
    fit = sp.sun_abraham(df, **cfg, control_group="nevertreated", share_variance=False)
    assert fit.model_info["se_fixest_att_share"] == pytest.approx(
        fit.model_info["se_fixest_att"], rel=1e-14
    )
