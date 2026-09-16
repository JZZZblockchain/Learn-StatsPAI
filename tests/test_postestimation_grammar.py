"""Stata-style post-estimation grammar: ``sp.etable`` and ``r.test`` / ``r.lincom``.

Two defects this file guards against were silent:

* ``sp.etable([r1, r2])`` (a list) and ``sp.etable("oops")`` returned an empty
  DataFrame, which reads as "no coefficients" rather than a caller error;
  a mixed call with one pyfixest fit dropped every other column.
* Stata users type ``test`` / ``lincom`` straight after estimation; the
  result object had no such methods, only the free functions.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp


@pytest.fixture(scope="module")
def data() -> pd.DataFrame:
    rng = np.random.default_rng(11)
    n = 300
    df = pd.DataFrame({"x1": rng.normal(size=n), "x2": rng.normal(size=n)})
    df["y"] = 1.0 + 0.5 * df.x1 - 0.3 * df.x2 + rng.normal(size=n)
    return df


@pytest.fixture(scope="module")
def fits(data):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return (
            sp.regress("y ~ x1", data=data, vce="robust"),
            sp.regress("y ~ x1 + x2", data=data, vce="robust"),
        )


class TestEtableInputs:
    def test_list_equals_varargs(self, fits):
        pd.testing.assert_frame_equal(sp.etable(list(fits)), sp.etable(*fits))
        pd.testing.assert_frame_equal(sp.etable(tuple(fits)), sp.etable(*fits))

    def test_table_has_one_column_per_model_and_every_term(self, fits):
        tab = sp.etable(*fits)
        assert list(tab.columns) == ["(1)", "(2)"]
        assert {"Intercept", "x1", "x2"} <= set(tab.index)
        assert tab.loc["x2", "(1)"] == ""

    @pytest.mark.parametrize("bad", ["oops", 3.0, None, pd.DataFrame()])
    def test_non_result_raises(self, fits, bad):
        with pytest.raises(TypeError, match="fitted results"):
            sp.etable(fits[0], bad)

    def test_empty_call_raises(self):
        with pytest.raises(TypeError, match="at least one"):
            sp.etable()
        with pytest.raises(TypeError, match="at least one"):
            sp.etable([])

    def test_mixed_pyfixest_and_native_keeps_every_column(self, fits):
        class _FakePyfixest:
            params = fits[0].params
            std_errors = fits[0].std_errors
            pvalues = fits[0].pvalues
            _pyfixest_fit = object()

        tab = sp.etable(_FakePyfixest(), fits[1])
        assert list(tab.columns) == ["(1)", "(2)"]


class TestResultMethods:
    def test_test_method_matches_free_function(self, fits):
        r = fits[1]
        assert r.test("x1 = x2") == sp.test(r, "x1 = x2")
        joint = r.test("x1 = x2 = 0")
        assert joint["df"][0] == 2

    def test_lincom_method_matches_free_function(self, fits):
        r = fits[1]
        assert r.lincom("x1 + x2") == sp.lincom(r, "x1 + x2")
        assert r.lincom("x1 - x2", alpha=0.1) == sp.lincom(r, "x1 - x2", alpha=0.1)

    def test_lincom_single_term_reproduces_coefficient(self, fits):
        r = fits[1]
        out = r.lincom("x1")
        assert out["estimate"] == pytest.approx(float(r.params["x1"]), rel=1e-12)
        assert out["se"] == pytest.approx(float(r.std_errors["x1"]), rel=1e-12)

    def test_unknown_term_fails_loudly(self, fits):
        with pytest.raises(Exception):
            fits[1].test("nope = 0")


class TestSummaryText:
    def test_counts_print_as_integers(self, data):
        df = data.assign(z=data.x2 + np.random.default_rng(1).normal(size=len(data)))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            text = str(sp.ivreg("y ~ x1 + (x2 ~ z)", data=df).summary())
        assert "N instruments" in text
        assert "1.0000" not in text.split("N instruments", 1)[1].splitlines()[0]

    def test_statistic_label_follows_reference_distribution(self, data, fits):
        assert "P>|t|" in str(fits[1].summary())
        yb = data.assign(yb=(data.y > 1).astype(int))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            text = str(sp.logit("yb ~ x1", data=yb).summary())
        assert "P>|z|" in text and "P>|t|" not in text

    def test_causal_footer_hides_none_and_rounds_floats(self):
        rng = np.random.default_rng(4)
        r = rng.uniform(-1, 1, 500)
        df = pd.DataFrame({"r": r, "y": 0.8 * (r >= 0) + rng.normal(0, 0.3, 500)})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = sp.rdrobust(df, y="y", x="r")
        text = str(res.summary())
        assert ": None" not in text and ":    None" not in text
        h = float(res.model_info["bandwidth_h"])
        assert repr(h) not in text
        assert f"{h:.6g}" in text
