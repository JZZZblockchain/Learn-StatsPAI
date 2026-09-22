"""Tests for Gardner (2021) two-stage DID estimator."""

import json
import pathlib
import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp


def _synthetic_staggered_panel(seed=0, N=200, T=10, tau=2.0):
    rng = np.random.default_rng(seed)
    unit = np.repeat(np.arange(N), T)
    time = np.tile(np.arange(T), N)
    cohort = rng.choice([3, 5, 7, np.inf], size=N, p=[0.25, 0.25, 0.25, 0.25])
    first_treat = np.repeat(cohort, T)
    ue = rng.normal(0, 0.3, N)
    te = rng.normal(0, 0.3, T)
    unit_fe = np.repeat(ue, T)
    time_fe = np.tile(te, N)
    treated_now = (time >= first_treat) & np.isfinite(first_treat)
    y = 1.0 + unit_fe + time_fe + tau * treated_now + rng.normal(0, 0.3, N * T)
    return pd.DataFrame(
        {
            "id": unit,
            "t": time,
            "y": y,
            "first_treat": np.where(np.isfinite(first_treat), first_treat, 0.0),
        }
    )


def test_gardner_att_recovers_truth():
    df = _synthetic_staggered_panel(seed=0, N=300)
    r = sp.gardner_did(df, y="y", group="id", time="t", first_treat="first_treat")
    assert abs(r.estimate - 2.0) < 0.15, f"ATT {r.estimate} off from true 2.0"
    assert r.se > 0
    assert r.ci[0] < r.estimate < r.ci[1]
    assert r.estimand == "ATT"
    assert r.n_obs > 0


def test_gardner_agrees_with_bjs_imputation():
    df = _synthetic_staggered_panel(seed=1, N=300)
    r_g = sp.gardner_did(df, y="y", group="id", time="t", first_treat="first_treat")
    r_b = sp.did_imputation(df, y="y", group="id", time="t", first_treat="first_treat")
    # Gardner and BJS target the same estimand → should be close
    assert abs(r_g.estimate - r_b.estimate) / max(abs(r_b.estimate), 1e-6) < 0.10


def test_gardner_event_study_support():
    df = _synthetic_staggered_panel(seed=2, N=250)
    r = sp.gardner_did(
        df,
        y="y",
        group="id",
        time="t",
        first_treat="first_treat",
        event_study=True,
        horizon=[-2, -1, 0, 1, 2],
    )
    es = r.model_info["event_study"]
    assert set(es["horizon"]) == {"D_k-2", "D_k-1", "D_k+0", "D_k+1", "D_k+2"}
    # Post-treatment coefs should be ≈ 2.0, pre-treatment ≈ 0
    post = [es["coef"][k] for k in ("D_k+0", "D_k+1", "D_k+2")]
    # After the v1.5.1 reference-category fix, pre-trend should be ~0 and
    # post-treatment should closely track the truth.
    assert np.mean(post) > 1.6
    for k in ("D_k-2", "D_k-1"):
        assert abs(es["coef"][k]) < 0.3  # pre-trend tight relative to ATT


def test_gardner_alias_did_2stage():
    df = _synthetic_staggered_panel(seed=3, N=150)
    r1 = sp.gardner_did(df, y="y", group="id", time="t", first_treat="first_treat")
    r2 = sp.did_2stage(df, y="y", group="id", time="t", first_treat="first_treat")
    assert r1.estimate == pytest.approx(r2.estimate, abs=1e-10)


def test_gardner_in_registry():
    fns = sp.list_functions()
    assert "gardner_did" in fns
    assert "did_2stage" in fns


def test_gardner_raises_on_missing_column():
    df = _synthetic_staggered_panel(seed=4, N=100)
    with pytest.raises(ValueError):
        sp.gardner_did(
            df, y="nonexistent", group="id", time="t", first_treat="first_treat"
        )


def test_gardner_cluster_parameter():
    df = _synthetic_staggered_panel(seed=5, N=200)
    # Explicit cluster=group should match default behaviour
    r_default = sp.gardner_did(
        df, y="y", group="id", time="t", first_treat="first_treat"
    )
    r_cluster = sp.gardner_did(
        df, y="y", group="id", time="t", first_treat="first_treat", cluster="id"
    )
    assert r_default.estimate == pytest.approx(r_cluster.estimate)
    assert r_default.se == pytest.approx(r_cluster.se)


# ---------------------------------------------------------------------------
# Two-stage corrected variance (did2s parity)
# ---------------------------------------------------------------------------

_PARITY = pathlib.Path(__file__).resolve().parent / "r_parity"

# The pre-correction default: stage-2-only cluster sandwich on the committed
# mpdta fixture (tests/r_parity/results/73_did2s_py.json as committed before
# the correction, statistic static_ATT). Kept so vce='stage2' is pinned to the
# number users saw before the default changed.
_LEGACY_STAGE2_SE_MPDTA = 0.005117728129401425


def _mpdta_fixture():
    return pd.read_csv(_PARITY / "data" / "73_did2s.csv")


def _r_golden():
    with open(_PARITY / "results" / "73_did2s_R.json", encoding="utf-8") as fh:
        rows = json.load(fh)["rows"]
    (row,) = [r for r in rows if r["statistic"] == "static_ATT"]
    return float(row["estimate"]), float(row["se"])


def test_gardner_default_se_matches_r_did2s_golden():
    """vce='analytic' reproduces did2s::did2s's corrected clustered SE.

    Tolerance rel 1e-6 is the Track A budget (compare.py::TOLERANCES);
    observed 2.7e-10 (the residual is fixest's first-stage demeaning
    tolerance, which also produces the 4.8e-8 point-estimate gap).
    """
    est_r, se_r = _r_golden()
    df = _mpdta_fixture()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        r = sp.gardner_did(
            df, y="lemp", group="countyreal", time="year", first_treat="first_treat"
        )
    assert not [w for w in caught if "gardner_did" in str(w.message)]
    assert r.estimate == pytest.approx(est_r, rel=1e-6)
    assert r.se == pytest.approx(se_r, rel=1e-6)
    assert r.model_info["vce"] == "analytic"
    assert "did2s" in r.model_info["se_convention"]


def test_gardner_stage2_reproduces_legacy_se():
    """vce='stage2' returns the pre-correction number, unchanged, and warns."""
    df = _mpdta_fixture()
    with pytest.warns(UserWarning, match="understates"):
        r = sp.gardner_did(
            df,
            y="lemp",
            group="countyreal",
            time="year",
            first_treat="first_treat",
            vce="stage2",
        )
    assert r.se == pytest.approx(_LEGACY_STAGE2_SE_MPDTA, rel=1e-12)
    # Same point estimate as the default; only the variance convention moved.
    default = sp.gardner_did(
        df, y="lemp", group="countyreal", time="year", first_treat="first_treat"
    )
    assert r.estimate == pytest.approx(default.estimate, rel=1e-12)
    assert r.se < default.se


def test_gardner_event_study_overall_se_uses_cross_horizon_covariance():
    """In event-study mode the overall ATT SE is w'Vw over the post horizons."""
    df = _synthetic_staggered_panel(seed=6, N=120, T=8)
    r = sp.gardner_did(
        df,
        y="y",
        group="id",
        time="t",
        first_treat="first_treat",
        event_study=True,
        horizon=[-2, -1, 0, 1, 2],
    )
    es = r.model_info["event_study"]
    vcov = es["vcov"]
    post = ["D_k+0", "D_k+1", "D_k+2"]
    counts = np.array(
        [
            ((df["t"] - df["first_treat"]) == k)[df["first_treat"] > 0].sum()
            for k in (0, 1, 2)
        ],
        dtype=float,
    )
    w = counts / counts.sum()
    V = vcov.loc[post, post].to_numpy()
    assert r.se == pytest.approx(float(np.sqrt(w @ V @ w)), rel=1e-12)
    for k in post:
        assert es["se"][k] == pytest.approx(float(np.sqrt(vcov.loc[k, k])), rel=1e-12)


def test_gardner_rejects_unknown_vce():
    df = _synthetic_staggered_panel(seed=7, N=60, T=6)
    with pytest.raises(ValueError, match="vce must be"):
        sp.gardner_did(
            df, y="y", group="id", time="t", first_treat="first_treat", vce="robust"
        )
