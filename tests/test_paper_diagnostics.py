"""sp.paper() folds the fitted result's automatic diagnostics into Robustness.

The auto-paper's Robustness section must state plainly what the estimator's
self-audit (``result.violations()``) found — a flagged assumption becomes a
line in the paper, with the ``sp.*`` a reviewer would ask the authors to try.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import statspai as sp


def _obs_design(confounding: float, n: int = 800, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    ps = 1 / (1 + np.exp(-(confounding * x1 + 0.6 * confounding * x2)))
    d = (rng.uniform(size=n) < ps).astype(int)
    y = 1 + 2 * d + x1 + x2 + rng.normal(size=n)
    return pd.DataFrame({"y": y, "d": d, "x1": x1, "x2": x2})


def _paper(df: pd.DataFrame):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return sp.paper(df, y="y", treatment="d", covariates=["x1", "x2"])


def test_robustness_section_surfaces_a_flagged_diagnostic():
    draft = _paper(_obs_design(confounding=1.5))  # strong → poor post-match balance
    rob = draft.sections.get("Robustness", "")
    assert "Automatic diagnostic checks" in rob
    # the flagged imbalance and its recommended remedy both make the paper
    assert "imbalance" in rob.lower()
    assert "sp.ebalance" in rob


def test_robustness_section_reports_a_clean_self_audit():
    draft = _paper(_obs_design(confounding=0.15))  # weak → matching balances well
    rob = draft.sections.get("Robustness", "")
    assert "Automatic diagnostic checks" in rob
    # a well-behaved fit must not manufacture a balance violation
    assert "notable residual" not in rob.lower()
