"""``sp.stata`` runs Stata command lines; ``list_functions(core=True)``;
real signatures on the callable ``sp.iv`` / ``sp.rd`` modules.

``sp.stata`` must give exactly what the equivalent ``sp.*`` call gives, and
must refuse -- not approximate -- a line whose translation is incomplete
(``xtreg, fe`` without the ``xtset`` panel id would otherwise run pooled OLS).
"""

from __future__ import annotations

import inspect
import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp
from statspai.exceptions import MethodIncompatibility


@pytest.fixture(scope="module")
def df() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    n = 300
    out = pd.DataFrame(
        {
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
            "firm": rng.integers(0, 30, n),
            "id": np.repeat(np.arange(60), 5),
        }
    )
    out["y"] = 1 + 0.5 * out.x1 - 0.2 * out.x2 + rng.normal(size=n)
    out["yb"] = (out.y > 1).astype(int)
    return out


def _quiet(fn, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return fn(*args, **kwargs)


class TestStataRunner:
    def test_regress_matches_direct_call(self, df):
        a = _quiet(sp.stata, "regress y x1 x2, vce(robust)", data=df)
        b = _quiet(sp.regress, "y ~ x1 + x2", data=df, vce="robust")
        pd.testing.assert_series_equal(a.params, b.params)
        pd.testing.assert_series_equal(a.std_errors, b.std_errors)

    def test_cluster_logit_matches_direct_call(self, df):
        a = _quiet(sp.stata, "logit yb x1 x2, vce(cluster firm)", data=df)
        b = _quiet(sp.logit, "yb ~ x1 + x2", data=df, vce="cluster firm")
        pd.testing.assert_series_equal(a.std_errors, b.std_errors)

    def test_postestimation_chain_uses_latest_result(self, df):
        fit = _quiet(sp.regress, "y ~ x1 + x2", data=df)
        script = "* a comment\nregress y x1 x2  // fit\nlincom x1 + x2"
        assert _quiet(sp.stata, script, data=df) == sp.lincom(fit, "x1 + x2")
        assert _quiet(sp.stata, "regress y x1 x2; test x1 = x2", data=df) == sp.test(
            fit, "x1 = x2"
        )

    def test_margins_dydx(self, df):
        fit = _quiet(sp.logit, "yb ~ x1 + x2", data=df)
        got = _quiet(sp.stata, "logit yb x1 x2\nmargins, dydx(*)", data=df)
        pd.testing.assert_frame_equal(got, _quiet(sp.margins, fit, data=df))

    def test_chained_postestimation_does_not_warn_about_piping(self, df):
        # The "pipe the previous result_id" notes are for sp.from_stata
        # callers; sp.stata pipes the result itself, so they are noise here.
        script = (
            "logit yb x1 x2, vce(cluster firm)\n"
            "margins, dydx(x1)\ntest x1 = x2\nlincom x1 + x2"
        )
        with warnings.catch_warnings():
            warnings.simplefilter("error", UserWarning)
            sp.stata(script, data=df)

    def test_result_argument_for_postestimation_only_script(self, df):
        fit = _quiet(sp.regress, "y ~ x1 + x2", data=df)
        assert sp.stata("lincom x1 - x2", result=fit) == sp.lincom(fit, "x1 - x2")

    @pytest.mark.parametrize(
        "line, match",
        [
            ("xtreg y x1, fe vce(cluster id)", "cannot be run as written"),
            ("use auto", "cannot run"),
        ],
    )
    def test_incomplete_or_unknown_commands_raise(self, df, line, match):
        with pytest.raises(MethodIncompatibility, match=match):
            _quiet(sp.stata, line, data=df)

    def test_missing_data_or_result_raises(self):
        with pytest.raises(TypeError, match="needs data"):
            sp.stata("regress y x1")
        with pytest.raises(TypeError, match="post-estimation"):
            sp.stata("lincom x1")
        with pytest.raises(ValueError, match="no command"):
            sp.stata("  // nothing\n")


class TestCoreFunctions:
    def test_core_list_is_curated_and_registered(self):
        core = sp.list_functions(core=True)
        assert core[:3] == ["regress", "ivreg", "feols"]
        assert len(core) == len(set(core)) <= 40
        assert set(core) <= set(sp.list_functions())

    def test_filters_compose_with_core(self):
        causal = sp.list_functions(core=True, category="causal")
        assert causal and set(causal) <= set(sp.list_functions(core=True))
        assert all(sp.describe_function(n)["category"] == "causal" for n in causal)


class TestPostestimationTranslationsDispatch:
    """``sp.from_stata`` post-estimation payloads must run on a fitted result.

    The structural translation sweep exempts post-estimation tools (they need
    a prior fit), which is how ``margins(dydx=)`` and ``test(terms=)`` --
    keywords neither function accepts -- shipped. This runs them for real.
    """

    @pytest.fixture(scope="class")
    def fitted(self, df):
        data = df.assign(grp=df["firm"] % 3)
        return data, _quiet(sp.regress, "y ~ x1 + x2 + C(grp)", data=data)

    @pytest.mark.parametrize(
        "line",
        [
            "margins, dydx(*)",
            "margins, dydx(x1) atmeans",
            "margins, dydx(x1) at(x2=0)",
            "test x1 x2",
            "test x1 = x2",
            "lincom x1 - 2*x2",
            "lincom x1 + x2, level(90)",
        ],
    )
    def test_payload_runs(self, fitted, line):
        data, fit = fitted
        out = sp.from_stata(line)
        assert out["ok"], out
        fn = getattr(sp, out["tool"])
        kwargs = dict(out["arguments"])
        if "data" in inspect.signature(fn).parameters:
            kwargs["data"] = data
        _quiet(fn, fit, **kwargs)

    def test_translations_match_direct_calls(self, fitted):
        data, fit = fitted
        lin = sp.from_stata("lincom x1 + x2, level(90)")["arguments"]
        assert sp.lincom(fit, **lin) == sp.lincom(fit, "x1 + x2", alpha=0.1)
        tst = sp.from_stata("test x1 = x2")["arguments"]
        assert sp.test(fit, **tst) == sp.test(fit, "x1 = x2")
        mem = sp.from_stata("margins, dydx(x1) atmeans")["arguments"]
        pd.testing.assert_frame_equal(
            _quiet(sp.margins, fit, data=data, **mem),
            _quiet(sp.margins, fit, data=data, variables=["x1"], method="mem"),
        )

    @pytest.mark.parametrize(
        "line", ["margins", "margins grp", "margins, eyex(x1)", "contrast x1 x2"]
    )
    def test_quantities_sp_does_not_compute_are_refused(self, line):
        assert not sp.from_stata(line)["ok"]

    def test_xtreg_without_panel_id_keeps_the_fixed_effect_placeholder(self):
        out = sp.from_stata("xtreg y x, fe")
        assert out["arguments"]["fml"] == "y ~ x | <panel_id>"

    def test_margins_then_marginsplot_chain(self, df):
        import matplotlib

        matplotlib.use("Agg")
        fig_ax = _quiet(
            sp.stata, "logit yb x1 x2\nmargins, dydx(*)\nmarginsplot", data=df
        )
        assert len(fig_ax) == 2


def test_callable_modules_expose_real_signatures():
    iv_params = inspect.signature(sp.iv).parameters
    assert {"formula", "data", "method"} <= set(iv_params)
    rd_params = inspect.signature(sp.rd).parameters
    assert list(rd_params)[:4] == ["data", "y", "x", "c"]
    assert "method" in rd_params
