"""Analytical parity: sp.sqreg known-truth recovery (4-decimal display).

sp.sqreg currently rounds its reported coefficients to 4 decimal places
(src/statspai/regression/quantile.py:209-210). The values still recover
R's quantreg::rq at the 4-decimal level (observed diff 0), and the ranking
of predictors at each quantile correctly reflects the planted DGP. A
bit-exact headline target would require lifting the internal rounding
without user consent; kept at the analytical-only tier that reflects the
estimator's true behaviour. Regenerate:
    Rscript tests/reference_parity/_generate_sqreg_R.R
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import pandas as pd
import pytest

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import statspai as sp

_FIX = Path(__file__).parent / "_fixtures"


@pytest.fixture(scope="module")
def ref():
    return json.loads((_FIX / "sqreg_R.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def fitted():
    df = pd.read_csv(_FIX / "sqreg_data.csv")
    return sp.sqreg(df, "y", ["x1", "x2", "x3"], quantiles=[0.25, 0.5, 0.75])


@pytest.mark.parametrize(
    "tau_str,tau_val",
    [("tau_025", 0.25), ("tau_050", 0.5), ("tau_075", 0.75)],
)
def test_coefficients_match_at_four_decimals(fitted, ref, tau_str, tau_val):
    col = f"Q({tau_val})"
    got = {row["variable"]: float(row[col]) for _, row in fitted.iterrows()}
    ref_coefs = ref[tau_str]
    for name in ("(Intercept)", "x1", "x2", "x3"):
        sp_name = "const" if name == "(Intercept)" else name
        assert got[sp_name] == pytest.approx(ref_coefs[name], abs=1e-4)  # noqa: E501
