"""
Forest-based causal inference estimators for StatsPAI.

Hosts ``CausalForest`` (grf-style honest causal forests) and its
companions:

- :func:`causal_forest` / :class:`CausalForest` — heterogeneous
  treatment-effect estimation via honest random forests
  (Wager-Athey 2018; Athey-Tibshirani-Wager 2019).
- :func:`iv_forest` — instrumental-variable causal forests
  (Athey-Tibshirani-Wager 2019).
- :func:`multi_arm_forest` — multi-arm extension.
- :func:`calibration_test` / :func:`test_calibration` /
  :func:`rate` / :func:`honest_variance` — post-fit honesty &
  calibration diagnostics.

This package was previously named ``statspai.causal`` — the old
name is kept as a deprecation shim for one minor version cycle.
Use ``from statspai.forest import ...`` going forward.
"""

from .causal_forest import CausalForest, causal_forest
from .forest_inference import (
    average_treatment_effect,
    calibrate_cate,
    calibration_test,
    forest_diagnostics,
    honest_variance,
    rate,
    test_calibration,
)
from .iv_forest import IVForestResult, iv_forest
from .multi_arm_forest import MultiArmForestResult, multi_arm_forest

__all__ = [
    "CausalForest",
    "causal_forest",
    "calibrate_cate",
    "calibration_test",
    "test_calibration",
    "rate",
    "honest_variance",
    "average_treatment_effect",
    "forest_diagnostics",
    "multi_arm_forest",
    "MultiArmForestResult",
    "iv_forest",
    "IVForestResult",
]
