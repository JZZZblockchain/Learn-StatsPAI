"""Canonical ``id`` / ``time`` / ``covariates`` spellings on causal entry points.

The DiD, RD, synthetic-control and matching families grew up spelling the
same idea differently (``i`` / ``group`` / ``unit`` / ``id`` for the panel
identifier, ``x`` / ``controls`` / ``covs`` / ``X`` for covariates), because
each mirrors its reference package.  Signatures are kept as they are -- they
are what Stata / R users recognise -- and ``@accepts_aliases`` additionally
accepts the house-style spellings.

Contract checked here:

* alias and native spelling give identical numbers;
* both spellings in one call is a ``TypeError``;
* a misspelt keyword names the closest real parameter (did-you-mean);
* introspected signatures, and therefore the published schemas, are unchanged.
"""

from __future__ import annotations

import inspect
import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp


@pytest.fixture(scope="module")
def staggered() -> pd.DataFrame:
    rng = np.random.default_rng(3)
    rows = []
    for unit in range(60):
        cohort = [0, 4, 6][unit % 3]
        fe = rng.normal()
        z = rng.normal()
        for t in range(1, 9):
            treated = cohort > 0 and t >= cohort
            rows.append(
                {
                    "unit": unit,
                    "year": t,
                    "first": cohort,
                    "d": int(treated),
                    "z": z,
                    "y": fe + 0.2 * t + 0.3 * z + 1.5 * treated + rng.normal(0, 0.5),
                }
            )
    return pd.DataFrame(rows)


@pytest.fixture(scope="module")
def cross_section() -> pd.DataFrame:
    rng = np.random.default_rng(5)
    n = 600
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    d = (rng.random(n) < 1 / (1 + np.exp(-0.5 * x1))).astype(int)
    r = rng.uniform(-1, 1, n)
    return pd.DataFrame(
        {
            "x1": x1,
            "x2": x2,
            "d": d,
            "r": r,
            "y": 1 + 2 * d + x1 - 0.5 * x2 + rng.normal(size=n),
            "yr": 0.5 * r + 0.8 * (r >= 0.1) + 0.2 * x1 + rng.normal(0, 0.3, n),
        }
    )


def _quiet(fn, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return fn(*args, **kwargs)


STAGGERED_CASES = [
    (
        "callaway_santanna",
        dict(id="unit", time="year", first_treat="first", covariates=["z"]),
        dict(i="unit", t="year", g="first", x=["z"]),
        dict(bstrap=False),
    ),
    (
        "sun_abraham",
        dict(unit="unit", time="year", cohort="first", controls=["z"]),
        dict(i="unit", t="year", g="first", covariates=["z"]),
        {},
    ),
    (
        "bjs",
        dict(id="unit", time="year", first_treat="first", covariates=["z"]),
        dict(group="unit", time="year", first_treat="first", controls=["z"]),
        {},
    ),
    (
        "gardner_did",
        dict(unit="unit", time="year", first_treat="first", covariates=["z"]),
        dict(group="unit", time="year", first_treat="first", controls=["z"]),
        {},
    ),
    (
        "wooldridge_did",
        dict(id="unit", time="year", first_treat="first"),
        dict(group="unit", time="year", first_treat="first"),
        {},
    ),
    (
        "stacked_did",
        dict(id="unit", time="year", first_treat="first"),
        dict(group="unit", time="year", first_treat="first"),
        {},
    ),
    (
        "did_multiplegt",
        dict(id="unit", time="year", treat="d"),
        dict(group="unit", time="year", treatment="d"),
        dict(n_boot=0),
    ),
]


@pytest.mark.parametrize(
    "name, canonical, native, extra", STAGGERED_CASES, ids=lambda c: str(c)[:24]
)
def test_staggered_alias_equivalence(staggered, name, canonical, native, extra):
    fn = getattr(sp, name)
    a = _quiet(fn, staggered, y="y", **canonical, **extra)
    b = _quiet(fn, staggered, y="y", **native, **extra)
    assert a.estimate == pytest.approx(b.estimate, rel=1e-12, abs=1e-12)
    assert a.se == pytest.approx(b.se, rel=1e-12, abs=1e-12, nan_ok=True)


def test_event_study_id_alias(staggered):
    df = staggered.assign(tt=staggered["first"].replace(0, np.nan))
    a = _quiet(sp.event_study, df, y="y", treat_time="tt", time="year", id="unit")
    b = _quiet(sp.event_study, df, y="y", treat_time="tt", time="year", unit="unit")
    assert a.estimate == pytest.approx(b.estimate, rel=1e-12)


def test_rd_running_cutoff_aliases(cross_section):
    native = _quiet(sp.rdrobust, cross_section, y="yr", x="r", c=0.1, covs=["x1"])
    alias = _quiet(
        sp.rdrobust,
        cross_section,
        y="yr",
        running="r",
        cutoff=0.1,
        covariates=["x1"],
    )
    assert alias.estimate == pytest.approx(native.estimate, rel=1e-12)
    assert alias.se == pytest.approx(native.se, rel=1e-12)
    via_rdd = _quiet(sp.rdd, cross_section, y="yr", x="r", c=0.1, covs=["x1"])
    assert via_rdd.estimate == pytest.approx(native.estimate, rel=1e-12)


def test_psm_treat_covariates_aliases(cross_section):
    native = _quiet(sp.psm, cross_section, y="y", d="d", X=["x1", "x2"])
    alias = _quiet(sp.psm, cross_section, y="y", treat="d", covariates=["x1", "x2"])
    assert alias.estimate == pytest.approx(native.estimate, rel=1e-12)


@pytest.mark.parametrize("name", ["ipw", "ebalance"])
def test_controls_alias_on_weighting_estimators(cross_section, name):
    fn = getattr(sp, name)
    native = _quiet(fn, cross_section, y="y", treat="d", covariates=["x1", "x2"])
    alias = _quiet(fn, cross_section, y="y", treat="d", controls=["x1", "x2"])
    assert alias.estimate == pytest.approx(native.estimate, rel=1e-12)


def test_synth_id_alias():
    rng = np.random.default_rng(1)
    rows = [
        {
            "st": f"u{u}",
            "yr": 2000 + t,
            "sales": u * 0.1 - 0.1 * t + rng.normal(0, 0.2) - 3 * (u == 0 and t >= 6),
        }
        for u in range(8)
        for t in range(10)
    ]
    df = pd.DataFrame(rows)
    common = dict(outcome="sales", time="yr", treated_unit="u0", treatment_time=2006)
    a = _quiet(sp.synth, df, id="st", placebo=False, **common)
    b = _quiet(sp.synth, df, unit="st", placebo=False, **common)
    assert a.estimate == pytest.approx(b.estimate, rel=1e-12)


class TestRefusals:
    def test_alias_and_native_together_raise(self, cross_section):
        with pytest.raises(TypeError, match="pass only one"):
            sp.rdrobust(cross_section, y="yr", x="r", running="r")
        with pytest.raises(TypeError, match="pass only one"):
            sp.psm(cross_section, y="y", d="d", treat="d", X=["x1"])

    def test_misspelt_keyword_suggests_the_real_parameter(self, cross_section):
        with pytest.raises(TypeError, match="did you mean.*'running'"):
            sp.rdrobust(cross_section, y="yr", runing="r")
        with pytest.raises(TypeError, match="did you mean.*'covariates'"):
            sp.ipw(cross_section, y="y", treat="d", covariate=["x1"])

    def test_first_treat_is_not_a_treatment_indicator_alias(self):
        # g/first_treat is the adoption period; treat= would silently mean a
        # 0/1 indicator in sp.did, so callaway_santanna must not accept it.
        assert "treat" not in sp.callaway_santanna.__statspai_aliases__

    def test_rd_family_keeps_x_as_the_running_variable(self):
        for name in ("rdrobust", "rdplot", "rdbwselect", "rddensity", "rkd"):
            assert "x" in inspect.signature(getattr(sp, name)).parameters
            assert getattr(sp, name).__statspai_aliases__.get("x") is None


def test_describe_function_lists_aliases():
    spec = sp.describe_function("rdrobust")
    assert spec["aliases"]["running"] == "x"
    assert spec["aliases"]["cutoff"] == "c"
    assert "aliases" not in sp.describe_function("kaplan_meier")


def test_signatures_are_unchanged():
    """Aliases are call-time only: introspection (and the schemas) is untouched."""
    params = inspect.signature(sp.callaway_santanna).parameters
    assert {"i", "t", "g", "x"} <= set(params)
    assert not {"id", "time", "first_treat", "covariates"} & set(params)
    assert sp.bjs is sp.did_imputation
