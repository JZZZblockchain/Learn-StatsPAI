"""Plain-text ``regtable`` columns widen to fit their widest cell.

The text renderer used a fixed 14-character column, so a longer model label
or estimate ran straight into its neighbour: ``model_labels=["Naive",
"+ Full controls"]`` rendered as ``"Naive+ Full controls"`` with no gutter.
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
import pytest

import statspai as sp


@pytest.fixture(scope="module")
def models():
    rng = np.random.default_rng(3)
    n = 300
    df = pd.DataFrame({"x": rng.normal(size=n), "w": rng.normal(size=n)})
    df["y"] = 2.0 + 1.5 * df["x"] - 0.4 * df["w"] + rng.normal(size=n)
    return sp.regress("y ~ x", data=df), sp.regress("y ~ x + w", data=df)


def _cells(line: str) -> list:
    return [c for c in re.split(r"\s{2,}", line.strip()) if c]


@pytest.mark.parametrize("transpose", [False, True])
def test_long_labels_keep_a_gutter(models, transpose):
    labels = ["A rather long first label", "+ Full controls and more"]
    text = sp.regtable(*models, model_labels=labels, transpose=transpose).to_text()
    if transpose:
        rows = [ln for ln in text.splitlines() if ln.startswith(tuple(labels))]
        assert [r[: len(lbl)] for r, lbl in zip(rows, labels)] == labels
        assert all(len(_cells(r)) >= 2 for r in rows)
    else:
        header = next(ln for ln in text.splitlines() if labels[0] in ln)
        assert _cells(header) == labels


def test_default_width_unchanged_for_short_cells(models):
    text = sp.regtable(*models, model_labels=["(1)", "(2)"]).to_text()
    header = next(ln for ln in text.splitlines() if "(1)" in ln)
    # label column (18) + two 14-wide columns
    assert len(header) == 18 + 14 * 2
