import json

import matplotlib
import numpy as np
import pytest

from statspai.core.results import CausalResult
from statspai.dml._diagnostics import dml_diagnostics

matplotlib.use("Agg")


@pytest.mark.parametrize("values", [[-1.0, 1.0, -5.0, 5.0], [9.0, 11.0, 5.0, 15.0]])
def test_centered_moment_is_not_an_orthogonality_test(values):
    res = CausalResult(
        method="Double ML (IRM)",
        estimand="ATE",
        estimate=3.0,
        se=1.0,
        pvalue=0.01,
        ci=(1.0, 5.0),
        alpha=0.05,
        n_obs=4,
        model_info={
            "dml_model": "IRM",
            "_y_resid": np.array(values),
            "_d_resid": np.array([-0.5, 0.5, -0.5, 0.5]),
            "_pscore": np.full(4, 0.5),
        },
    )
    diag = dml_diagnostics(res)
    assert diag.orth_pvalue is None
    assert diag.orth_stat is None
    assert diag.orthogonality_status == "not_tested"
    assert diag.orthogonality_reason == (
        "A solved estimating equation is not a test of Neyman "
        "orthogonality or identification."
    )
    summary = diag.summary()
    assert "Orthogonality: not tested" in summary
    assert "p-value                : 1.0000" not in summary


def test_unavailable_orthogonality_is_plot_and_json_safe():
    res = CausalResult(
        method="Double ML (PLR)",
        estimand="ATE",
        estimate=2.0,
        se=0.5,
        pvalue=0.01,
        ci=(1.0, 3.0),
        alpha=0.05,
        n_obs=4,
        model_info={
            "dml_model": "PLR",
            "_y_resid": np.array([-2.0, -1.0, 1.0, 2.0]),
            "_d_resid": np.array([-0.5, 0.5, -0.5, 0.5]),
        },
    )

    diag = dml_diagnostics(res)
    fig, _ = diag.plot()
    payload = json.loads(json.dumps(diag.to_dict()))

    assert fig is not None
    assert payload["orth_stat"] is None
    assert payload["orth_pvalue"] is None
    assert payload["orthogonality_status"] == "not_tested"
    assert "Centered PLR outcome residual" in diag.summary()
    fig.clear()
