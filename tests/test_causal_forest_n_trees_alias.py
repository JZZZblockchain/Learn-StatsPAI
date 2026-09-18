"""``sp.causal_forest`` accepts grf's ``n_trees`` spelling for ``n_estimators``.

The registry advertised ``n_trees`` while the callable only took
``n_estimators``, so a call built from ``sp.describe_function`` failed with a
``TypeError``.  The alias now resolves to the same fit, passing both is
rejected, and the alias is advertised.
"""

import numpy as np
import pandas as pd
import pytest

import statspai as sp


@pytest.fixture(scope="module")
def data():
    rng = np.random.default_rng(7)
    n = 400
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    d = rng.binomial(1, 1 / (1 + np.exp(-0.5 * x1)))
    y = (1.0 + 0.5 * x1) * d + x2 + rng.normal(size=n)
    return pd.DataFrame({"y": y, "d": d, "x1": x1, "x2": x2})


def _fit(df, **kw):
    return sp.causal_forest("y ~ d | x1 + x2", data=df, random_state=0, **kw)


def test_n_trees_alias_is_the_same_fit(data):
    a = _fit(data, n_estimators=40)
    b = _fit(data, n_trees=40)
    np.testing.assert_array_equal(
        a.effect(data[["x1", "x2"]].to_numpy()),
        b.effect(data[["x1", "x2"]].to_numpy()),
    )
    assert float(a.ate()) == float(b.ate())


def test_passing_both_spellings_is_rejected(data):
    with pytest.raises(TypeError):
        _fit(data, n_estimators=40, n_trees=40)


def test_registry_names_the_real_parameter_and_the_alias():
    spec = sp.describe_function("causal_forest")
    names = [p["name"] for p in spec["params"]]
    assert "n_estimators" in names and "n_trees" not in names
    assert spec.get("aliases", {}).get("n_trees") == "n_estimators"
