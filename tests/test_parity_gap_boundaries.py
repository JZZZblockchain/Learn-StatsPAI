"""Executable bounds for documented parity/convention gaps.

These tests intentionally read committed parity artifacts only. They make the
"known gap" language auditable without requiring R or Stata at test time.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import statspai as sp


ROOT = Path(__file__).resolve().parents[1]
R_RESULTS = ROOT / "tests" / "r_parity" / "results"
STATA_RESULTS = ROOT / "tests" / "stata_parity" / "results"


def _payload(module: str, side: str) -> dict[str, Any]:
    if side == "Stata":
        path = STATA_RESULTS / f"{module}_Stata.json"
    else:
        path = R_RESULTS / f"{module}_{side}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _row(module: str, side: str, statistic: str) -> dict[str, Any]:
    for row in _payload(module, side)["rows"]:
        if row["statistic"] == statistic:
            return row
    raise AssertionError(f"{module}_{side}.json has no statistic {statistic!r}")


def _estimate(module: str, side: str, statistic: str) -> float:
    value = _row(module, side, statistic)["estimate"]
    assert isinstance(value, (int, float)) and math.isfinite(value)
    return float(value)


def _rel_gap(a: float, b: float) -> float:
    denom = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / denom


def _extra(module: str, side: str = "py") -> dict[str, Any]:
    extra = _payload(module, side).get("extra", {})
    assert isinstance(extra, dict)
    return extra


def _gap_description(module: str, gap: str) -> str:
    for row in sp.parity_gap_report(repo_root=ROOT, fmt="records"):
        if row["module_id"] == module and row["gap"] == gap:
            return row["description"]
    raise AssertionError(f"parity_gap_report has no {module}/{gap} row")


def test_parity_gap_report_has_actionable_stable_rows():
    rows = sp.parity_gap_report(repo_root=ROOT, fmt="records")
    assert len(rows) >= 30

    expected = {
        ("06_rd", "bandwidth_selector_gap"),
        ("08_dml", "fold_split_note"),
        ("16_bjs", "stata_gap_note"),
        ("17_etwfe", "aggregation_note"),
        ("52_scm_unique", "note"),
    }
    observed = {(row["module_id"], row["gap"]) for row in rows}
    assert expected <= observed

    for row in rows:
        assert row["module_id"]
        assert row["description"].strip()
        assert row["priority"] in {"high", "medium", "low"}
        assert row["next_action"].strip()


def test_rd_bandwidth_gap_is_documented_and_common_bandwidth_passes():
    extra = _extra("06_rd")
    assert "bandwidth_selector_gap" in extra
    assert "forced to the same bandwidth" in extra["bandwidth_selector_gap"]

    py_h = _estimate("06_rd", "py", "default_bandwidth_h")
    r_h = _estimate("06_rd", "R", "default_bandwidth_h")
    assert 0.70 <= _rel_gap(py_h, r_h) <= 0.80

    for stat in (
        "forced_h0.042287_conventional_est",
        "forced_h0.042287_robust_est",
    ):
        assert _rel_gap(_estimate("06_rd", "py", stat), _estimate("06_rd", "R", stat)) < 1e-10

    se_rel = _rel_gap(
        _row("06_rd", "py", "forced_h0.042287_conventional_est")["se"],
        _row("06_rd", "R", "forced_h0.042287_conventional_est")["se"],
    )
    assert se_rel <= 0.07


def test_dml_fold_split_gap_stays_small_and_explained():
    note = _extra("08_dml")["fold_split_note"]
    assert "fold-split" in note
    assert "machine precision" in note

    py_theta = _estimate("08_dml", "py", "theta_DML_PLR")
    r_theta = _estimate("08_dml", "R", "theta_DML_PLR")
    assert abs(py_theta - r_theta) <= 3e-4
    assert _rel_gap(py_theta, r_theta) <= 0.003


def test_scm_nonunique_row_is_bounded_by_unique_solution_counterpart():
    nonunique = _extra("07_scm")
    assert nonunique["validation_tier"] == "identification_dependent_native"
    assert nonunique["tier"] == "T4"
    assert "not unique" in nonunique["native_note"]

    py_gap = _estimate("07_scm", "py", "avg_post_gap")
    r_gap = _estimate("07_scm", "R", "avg_post_gap")
    stata_gap = _estimate("07_scm", "Stata", "avg_post_gap")
    assert _rel_gap(py_gap, r_gap) <= 0.025
    assert _rel_gap(py_gap, stata_gap) <= 0.001

    unique = _extra("52_scm_unique")
    assert unique["true_gap"] == 2.0
    assert "Unique-solution counterpart" in unique["note"]
    assert abs(_estimate("52_scm_unique", "py", "avg_post_gap") - 2.0) <= 1e-5
    assert _estimate("52_scm_unique", "py", "pre_treatment_rmse") == 0.0
    assert _rel_gap(
        _estimate("52_scm_unique", "py", "avg_post_gap"),
        _estimate("52_scm_unique", "R", "avg_post_gap"),
    ) <= 0.01


def test_did_aggregation_convention_rows_keep_point_parity():
    bjs_note = _extra("16_bjs")
    assert "parity_note" in bjs_note
    assert (
        "different autosample/aggregation convention"
        in _gap_description("16_bjs", "stata_gap_note")
    )
    assert _rel_gap(
        _estimate("16_bjs", "py", "att_bjs"),
        _estimate("16_bjs", "R", "att_bjs"),
    ) < 1e-7

    etwfe_note = _extra("17_etwfe")["aggregation_note"]
    assert "weighting='treated'" in etwfe_note
    assert "Point estimates match to machine precision" in etwfe_note
    assert _rel_gap(
        _estimate("17_etwfe", "py", "att_etwfe"),
        _estimate("17_etwfe", "R", "att_etwfe"),
    ) < 1e-12


def test_causal_forest_gap_is_within_combined_monte_carlo_error():
    extra = _extra("13_causal_forest")
    assert "clean overlap" in extra["dgp"]
    assert "AIPW doubly-robust" in extra["note"]

    for stat in ("ate_causal_forest", "att_causal_forest"):
        py = _row("13_causal_forest", "py", stat)
        r = _row("13_causal_forest", "R", stat)
        combined_se = math.sqrt(float(py["se"]) ** 2 + float(r["se"]) ** 2)
        assert abs(float(py["estimate"]) - float(r["estimate"])) / combined_se <= 1.25
        assert _rel_gap(float(py["estimate"]), float(r["estimate"])) <= 0.07
