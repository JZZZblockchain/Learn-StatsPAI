"""Smoke tests for shared Excel table styling helpers."""

from __future__ import annotations

import pandas as pd
import pytest

from statspai.output._excel_style import TIMES, render_dataframe_to_xlsx


def test_render_dataframe_to_xlsx_applies_shared_booktab_style(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    df = pd.DataFrame(
        {"Mean": ["1.23"], "SD": ["0.45"]},
        index=["x"],
    )
    path = tmp_path / "table.xlsx"

    render_dataframe_to_xlsx(
        df,
        str(path),
        title="Table A",
        notes=["Note text."],
        index_label="Variable",
    )

    wb = openpyxl.load_workbook(path)
    ws = wb["Table"]

    assert ws["A1"].value == "Table A"
    assert ws["A1"].font.name == TIMES
    assert ws["A2"].value == "Variable"
    assert ws["A3"].value == "x"
    assert ws["A4"].value == "Note text."
    assert ws["A2"].border.top.style == "medium"
    assert ws["A2"].border.bottom.style == "thin"
    assert ws["A3"].border.bottom.style == "medium"
