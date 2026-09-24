"""Every lazily exported public callable must be in ``statspai.__all__``.

``_register_lazy`` makes ``sp.<name>`` work, but the registry's
auto-registration pass walks ``__all__``.  A name that is reachable yet
absent from ``__all__`` is therefore invisible to ``sp.list_functions()``,
``sp.describe_function()`` and ``sp.function_schema()`` -- it works for a
Python user and does not exist for an agent.  That is how
``sp.iv_forest``, ``sp.multi_arm_forest`` and ``sp.causal_survival_forest``
went unregistered for several releases.

Ratchet, like the other drift gates: the offenders outside the GRF family
at the time this gate was added are frozen in
``scripts/lazy_export_all_baseline.json``; entries may be removed (add the
name to ``__all__``), never added.
"""

from __future__ import annotations

import inspect
import json
import pathlib

import statspai as sp

_BASELINE = (
    pathlib.Path(__file__).resolve().parents[1]
    / "scripts"
    / "lazy_export_all_baseline.json"
)


def _missing() -> set:
    lazy = getattr(sp, "_LAZY_ATTRS", {})
    exported = set(sp.__all__)
    out = set()
    for name in lazy:
        if name.startswith("_") or name in exported:
            continue
        obj = getattr(sp, name, None)
        if obj is None or inspect.ismodule(obj) or not callable(obj):
            continue
        out.add(name)
    return out


def _baseline() -> set:
    return set(json.loads(_BASELINE.read_text(encoding="utf-8"))["missing"])


def test_no_new_lazy_export_is_missing_from_all() -> None:
    new = sorted(_missing() - _baseline())
    assert not new, (
        "Reachable as sp.<name> but missing from statspai.__all__ (and so "
        f"from sp.list_functions()): {new}. Add them to __all__."
    )


def test_baseline_has_no_stale_entries() -> None:
    stale = sorted(_baseline() - _missing())
    assert not stale, (
        f"Fixed since the baseline was frozen: {stale}. Delete them from "
        "scripts/lazy_export_all_baseline.json."
    )


def test_grf_family_is_registered() -> None:
    names = set(sp.list_functions())
    for name in (
        "causal_forest",
        "iv_forest",
        "instrumental_forest",
        "multi_arm_forest",
        "lm_forest",
        "causal_survival_forest",
        "regression_forest",
        "multi_regression_forest",
        "probability_forest",
        "quantile_forest",
        "survival_forest",
        "variable_importance",
        "best_linear_projection",
        "get_scores",
    ):
        assert name in names, name
