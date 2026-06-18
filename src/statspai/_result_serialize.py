"""Shared agent-native serialization for domain result dataclasses.

Design principle 3 ("统一结果对象") asks every result object to be
serialisable so a human *and* an agent use the same entry point. The
flagship `CausalResult` / `EconometricResults` already expose `.to_dict()`;
the lighter domain result dataclasses (negative controls, proximal, four-way
mediation, network spillover, ITS, Rosenbaum bounds, longitudinal TMLE, BCF
extensions, …) historically only had `.summary()`.

`result_to_dict` gives them a one-line, JSON-safe `.to_dict()` that reuses the
same `core.results._to_jsonable` converter (numpy / pandas / NaN-aware), so the
serialisation logic lives in exactly one place rather than being re-implemented
per estimator (CLAUDE.md §4).
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any, Dict

from .core.results import _to_jsonable


def result_to_dict(obj: Any) -> Dict[str, Any]:
    """Return a JSON-safe ``{field: value}`` mapping for a result dataclass.

    Every field is passed through ``core.results._to_jsonable`` so numpy
    scalars/arrays, pandas Series/DataFrames and NaN/Inf are converted to
    JSON-friendly values (``json.dumps`` never raises on the result).
    """
    if not is_dataclass(obj):
        raise TypeError(
            f"result_to_dict expects a result dataclass, got " f"{type(obj).__name__}."
        )
    return {f.name: _to_jsonable(getattr(obj, f.name)) for f in fields(obj)}
