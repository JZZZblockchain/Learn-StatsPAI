"""Duplicate ``model_labels`` must not drop columns from any export.

``model_labels=["OLS", "OLS", "2SLS"]`` is the ordinary way to label an
economics table, and Stata ``esttab`` / R ``modelsummary`` both render it.
``RegtableResult.to_dataframe`` used to key each row by label, so the second
``"OLS"`` overwrote the first: the text / LaTeX renderers showed three columns
while ``to_dataframe``, ``to_excel``, ``to_word``, ``save('.csv')`` and the
JSON payload silently carried two, with the surviving ``OLS`` column holding
the *last* OLS model's numbers under the first model's position.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

import statspai as sp
from statspai.output.regression_table import RegtableResult

LABELS = ["OLS", "OLS", "2SLS"]


@pytest.fixture(scope="module")
def models():
    rng = np.random.default_rng(7)
    n = 400
    df = pd.DataFrame({"z": rng.normal(size=n), "w": rng.normal(size=n)})
    df["d"] = 0.8 * df["z"] + rng.normal(size=n)
    df["y"] = 1.0 + 0.5 * df["d"] + 0.3 * df["w"] + rng.normal(size=n)
    m1 = sp.regress("y ~ d", data=df)
    m2 = sp.regress("y ~ d + w", data=df)
    m3 = sp.ivreg("y ~ (d ~ z) + w", data=df)
    return m1, m2, m3


@pytest.fixture(scope="module")
def table(models):
    return sp.regtable(*models, model_labels=LABELS)


def _coef_row(df: pd.DataFrame) -> list:
    return list(df.loc["d"].iloc[0]) if df.loc["d"].ndim == 2 else list(df.loc["d"])


def test_to_dataframe_keeps_every_model(table):
    df = table.to_dataframe()
    assert list(df.columns) == LABELS
    cells = _coef_row(df)
    # Three distinct estimates, in model order -- not two, not reordered.
    assert len(set(cells)) == 3
    text = table.to_text()
    for cell in cells:
        assert cell in text


def test_excel_keeps_every_model(table, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    path = tmp_path / "dup.xlsx"
    table.to_excel(str(path))
    ws = openpyxl.load_workbook(path).active
    header = next(
        [c.value for c in row]
        for row in ws.iter_rows()
        if [c.value for c in row][1:4] == LABELS
    )
    assert header[1:4] == LABELS
    d_row = next(
        [c.value for c in row] for row in ws.iter_rows() if row[0].value == "d"
    )
    assert d_row[1:4] == _coef_row(table.to_dataframe())


def test_word_keeps_every_model(table, tmp_path):
    docx = pytest.importorskip("docx")
    path = tmp_path / "dup.docx"
    table.to_word(str(path))
    t = docx.Document(str(path)).tables[0]
    assert len(t.columns) == 1 + len(LABELS)
    assert [c.text for c in t.rows[0].cells][1:] == LABELS


def test_csv_keeps_every_model(table, tmp_path):
    path = tmp_path / "dup.csv"
    table.save(str(path))
    header = path.read_text(encoding="utf-8").splitlines()[0].split(",")
    assert header[1:] == LABELS


def test_to_dict_rows_are_lossless_and_round_trip(table):
    payload = table.to_dict()
    assert payload["model_labels"] == LABELS
    keys = payload["columns"][1:]
    assert len(keys) == len(set(keys)) == len(LABELS)
    d_rec = next(r for r in payload["table"] if r["term"] == "d")
    assert [d_rec[k] for k in keys] == _coef_row(table.to_dataframe())
    json.dumps(payload)  # JSON-safe
    rebuilt = RegtableResult.from_dict(payload)
    assert rebuilt.to_text() == table.to_text()
    assert list(rebuilt.to_dataframe().columns) == LABELS


def test_collection_exports_keep_every_model(models, table, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    coll = sp.collect("dup").add_regression(*models, model_labels=LABELS)
    xlsx = tmp_path / "coll.xlsx"
    coll.to_xlsx(str(xlsx))
    wb = openpyxl.load_workbook(xlsx)
    assert any(
        list(row)[1:4] == LABELS
        for ws in wb.worksheets
        for row in ws.iter_rows(values_only=True)
    )
    item = json.loads(coll.to_json())["items"][0]
    assert item["content"]["model_labels"] == LABELS


def test_unique_labels_unchanged(models):
    t2 = sp.regtable(*models, model_labels=["A", "B", "C"])
    assert list(t2.to_dataframe().columns) == ["A", "B", "C"]
    assert t2.to_dict()["columns"] == ["term", "A", "B", "C"]
