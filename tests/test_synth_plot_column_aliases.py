"""``sp.synth(method=...)`` variants disagree on their trajectory column names.

The ~20 estimators behind the dispatcher spell the two series differently:
``treated`` + ``synthetic`` (gsynth, cluster), ``observed`` +
``counterfactual`` (bsts), ``treated`` + ``counterfactual`` (fdid, kernel,
kernel_ridge, bayesian).  The plotting layer used to hard-code one spelling
per branch, so ``sp.synth_compare(...).plot()`` raised
``KeyError: 'counterfactual'`` as soon as a method using the other spelling
entered the pool -- which the default method list always does.

These tests pin the resolution at the extraction helper (fast and
deterministic) and on one end-to-end dispatcher call.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import statspai as sp
from statspai.core.results import CausalResult
from statspai.synth.plots import _extract_trajectories


def _result(treated_col: str, synth_col: str) -> CausalResult:
    frame = pd.DataFrame(
        {
            "time": [1, 2, 3, 4],
            treated_col: [1.0, 1.1, 2.0, 2.2],
            synth_col: [1.0, 1.05, 1.1, 1.15],
        }
    )
    return CausalResult(
        method="synth",
        estimand="ATT",
        estimate=0.5,
        se=0.1,
        pvalue=0.5,
        ci=(0.3, 0.7),
        alpha=0.05,
        n_obs=len(frame),
        model_info={"trajectory": frame, "treatment_time": 3, "treated_unit": "A"},
    )


@pytest.mark.parametrize(
    "treated_col,synth_col",
    [
        ("treated", "synthetic"),
        ("observed", "counterfactual"),
        ("treated", "counterfactual"),
    ],
)
def test_extract_trajectories_accepts_every_spelling(treated_col, synth_col):
    times, y_treated, y_synth, t_time, _ = _extract_trajectories(
        _result(treated_col, synth_col)
    )
    np.testing.assert_allclose(times, [1, 2, 3, 4])
    np.testing.assert_allclose(y_treated, [1.0, 1.1, 2.0, 2.2])
    np.testing.assert_allclose(y_synth, [1.0, 1.05, 1.1, 1.15])
    assert t_time == 3


def test_unknown_spelling_names_what_it_looked_for():
    with pytest.raises(KeyError) as excinfo:
        _extract_trajectories(_result("actual", "predicted"))
    message = str(excinfo.value)
    assert "treated" in message and "observed" in message


def test_synth_compare_plot_runs_on_the_default_method_pool():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    rng = np.random.default_rng(0)
    units = [f"u{i}" for i in range(8)]
    rows = []
    for u in units:
        level = rng.normal(10, 1)
        for t in range(1, 13):
            effect = 3.0 if (u == "u0" and t >= 9) else 0.0
            rows.append((u, t, level + 0.2 * t + effect + rng.normal(0, 0.1)))
    panel = pd.DataFrame(rows, columns=["unit", "time", "y"])
    comparison = sp.synth_compare(
        data=panel,
        unit="unit",
        time="time",
        outcome="y",
        treated_unit="u0",
        treatment_time=9,
    )
    # Before the fix this raised KeyError('counterfactual').
    assert comparison.plot() is not None
