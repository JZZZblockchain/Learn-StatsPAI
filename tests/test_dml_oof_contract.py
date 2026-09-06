"""Contracts for immutable, versioned DML out-of-fold predictions."""

from __future__ import annotations

import json
from copy import deepcopy

import numpy as np
import pytest

from statspai import OOFBundle, OOFPredictions
from statspai.dml import OOFBundle as DMLOOFBundle
from statspai.dml import OOFPredictions as DMLOOFPredictions

from .dml_oof_helpers import (
    _training_records,
    permuted_inputs,
    tiny_bundle,
    tiny_inputs,
    tiny_scored_bundle,
)


def test_public_exports_and_schema_versions():
    """Public import locations and artifact versions are stable."""
    assert OOFPredictions is DMLOOFPredictions
    assert OOFBundle is DMLOOFBundle
    _, predictions = tiny_bundle()
    _, bundle = tiny_scored_bundle()
    assert predictions.schema_version == "statspai.dml.predictions/1"
    assert bundle.schema_version == "statspai.dml.oof/1"


def test_prediction_roundtrip_copies_callers_and_partitions_hashes(tmp_path):
    """Caller mutation and persisted corruption cannot alter a snapshot."""
    _, kwargs = tiny_inputs()
    predictions = OOFPredictions.from_arrays(**kwargs)
    kwargs["g0"][0, 0] = 99.0
    kwargs["ids"][0] = "changed"
    kwargs["training_records"][0]["train_ids"][0] = "changed"
    kwargs["source"]["software_versions"]["fixture"] = "changed"
    assert predictions.ids[0] == "a" and predictions.g0[0, 0] == 1.0
    assert predictions.training_records[0]["train_ids"][0] == "c"
    assert predictions.source["software_versions"]["fixture"] == "1"
    for array in (
        predictions.y,
        predictions.d,
        predictions.x,
        predictions.g0,
        predictions.g1,
        predictions.ps_raw,
        predictions.fold_ids,
    ):
        assert not array.flags.writeable
        with pytest.raises(ValueError):
            array.flat[0] = array.flat[0]

    path = tmp_path / "predictions.json"
    predictions.to_json(path)
    first = path.read_bytes()
    predictions.to_json(path)
    assert path.read_bytes() == first
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert set(raw) == {
        "schema_version",
        "ids",
        "covariate_names",
        "arrays",
        "training_records",
        "source",
        "hashes",
    }
    assert set(raw["arrays"]) == {"y", "d", "x", "g0", "g1", "ps_raw", "fold_ids"}
    assert set(raw["hashes"]) == {"data", "predictions_and_folds", "training_source"}
    restored = OOFPredictions.from_json(path)
    np.testing.assert_array_equal(restored.fold_ids, predictions.fold_ids)
    assert dict(restored.hashes) == dict(predictions.hashes)


@pytest.mark.parametrize(
    ("partition", "target"),
    [
        ("data", "ids"),
        ("data", "covariate_names"),
        ("data", "y"),
        ("data", "d"),
        ("data", "x"),
        ("predictions_and_folds", "g0"),
        ("predictions_and_folds", "g1"),
        ("predictions_and_folds", "ps_raw"),
        ("predictions_and_folds", "fold_ids"),
        ("training_source", "training_records"),
        ("training_source", "source"),
    ],
)
def test_prediction_reader_rejects_tampering(tmp_path, partition, target):
    """Every persisted member belongs to an independently checked partition."""
    _, predictions = tiny_bundle()
    path = tmp_path / "predictions.json"
    predictions.to_json(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    if target in {"ids", "covariate_names"}:
        raw[target][0] = "changed"
    elif target == "x":
        raw["arrays"][target][0][0] += 1.0
    elif target in {"y", "d"}:
        raw["arrays"][target][0] += 1
    elif target in {"g0", "g1", "ps_raw", "fold_ids"}:
        raw["arrays"][target][0][0] += 0.1
    elif target == "training_records":
        raw[target][0]["origin"] = "statspai_internal"
    else:
        raw[target]["recipe"] = "changed"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match=rf"hash.*{partition}|{partition}.*hash"):
        OOFPredictions.from_json(path)


@pytest.mark.parametrize(
    "change",
    [
        lambda kw: kw["ids"].__setitem__(1, "a"),
        lambda kw: kw["ids"].__setitem__(1, ""),
        lambda kw: kw["y"].__setitem__(0, np.nan),
        lambda kw: kw.__setitem__("x", [[np.inf], [1.0], [2.0], [3.0]]),
        lambda kw: kw["g0"].__setitem__((0, 0), np.nan),
        lambda kw: kw["ps_raw"].__setitem__((0, 0), -0.1),
        lambda kw: kw["ps_raw"].__setitem__((0, 0), 1.1),
        lambda kw: kw.__setitem__("d", np.zeros(4)),
        lambda kw: kw["d"].__setitem__(0, 2),
        lambda kw: kw.__setitem__("y", kw["y"][:, None]),
        lambda kw: kw.__setitem__("x", kw["x"][:, 0]),
        lambda kw: kw.__setitem__("g0", kw["g0"][:, :3]),
        lambda kw: kw.__setitem__("fold_ids", kw["fold_ids"][:, :3]),
        lambda kw: kw.__setitem__("covariate_names", ["x", "z"]),
        lambda kw: (
            kw.__setitem__("x", np.c_[kw["x"], kw["x"]]),
            kw.__setitem__("covariate_names", ["x", "x"]),
        ),
        lambda kw: kw.__setitem__("fold_ids", [[0.0, 0.0, 1.0, 1.5]]),
        lambda kw: kw.__setitem__("fold_ids", [[0, 0, 2, 2]]),
        lambda kw: kw["training_records"][0]["train_ids"].append("a"),
        lambda kw: kw["source"].pop("recipe"),
        lambda kw: kw["source"].__setitem__("software_versions", {1: "invalid"}),
    ],
)
def test_prediction_rejects_invalid_arrays_and_identity(change):
    """Malformed rows, values, folds, and provenance cannot enter the contract."""
    _, kwargs = tiny_inputs()
    change(kwargs)
    with pytest.raises((TypeError, ValueError), match=".+"):
        OOFPredictions.from_arrays(**kwargs)


def test_prediction_rejects_empty_sample_and_missing_repeat_records():
    """Zero-row artifacts and incomplete repeat metadata are ambiguous."""
    _, empty = tiny_inputs()
    empty.update(
        ids=[],
        y=[],
        d=[],
        x=np.empty((0, 1)),
        g0=np.empty((1, 0)),
        g1=np.empty((1, 0)),
        ps_raw=np.empty((1, 0)),
        fold_ids=np.empty((1, 0), dtype=int),
        training_records=[],
    )
    with pytest.raises(ValueError, match="observation"):
        OOFPredictions.from_arrays(**empty)
    _, missing = tiny_inputs(n_rep=2)
    missing["training_records"] = missing["training_records"][:2]
    with pytest.raises(ValueError, match="record|repeat"):
        OOFPredictions.from_arrays(**missing)


def test_prediction_rejects_duplicate_record_single_arm_and_variable_k():
    """Fold metadata is unique, common-K, and trains on both treatment arms."""
    _, duplicate = tiny_inputs()
    duplicate["training_records"][1] = deepcopy(duplicate["training_records"][0])
    with pytest.raises(ValueError, match="record|fold"):
        OOFPredictions.from_arrays(**duplicate)

    _, single_arm = tiny_inputs()
    single_arm["fold_ids"] = np.array([[0, 1, 0, 1]])
    single_arm["training_records"] = _training_records(
        single_arm["ids"], single_arm["d"], single_arm["fold_ids"]
    )
    with pytest.raises(ValueError, match="treatment|arm"):
        OOFPredictions.from_arrays(**single_arm)

    _, variable_k = tiny_inputs(n_rep=2)
    variable_k["fold_ids"][1] = [0, 1, 2, 2]
    variable_k["training_records"] = _training_records(
        variable_k["ids"], variable_k["d"], variable_k["fold_ids"]
    )
    with pytest.raises(ValueError, match="same.*fold|fold.*same"):
        OOFPredictions.from_arrays(**variable_k)


def test_distinct_repeats_internal_origin_and_shared_preprocessing_are_valid():
    """Different assignments and full-train shared scalers remain representable."""
    _, kwargs = tiny_inputs(n_rep=2)
    kwargs["fold_ids"][1] = [0, 1, 1, 0]
    kwargs["training_records"] = _training_records(
        kwargs["ids"], kwargs["d"], kwargs["fold_ids"], origin="statspai_internal"
    )
    for record in kwargs["training_records"]:
        for learner in ("g0", "g1", "ps"):
            record["preprocessing_train_ids"][learner] = list(record["train_ids"])
    predictions = OOFPredictions.from_arrays(**kwargs)
    assert predictions.n_folds == 2
    assert predictions.training_records[0]["preprocessing_train_ids"]["g0"] == (
        "c",
        "d",
    )


@pytest.mark.parametrize("scope", ["nuisance", "preprocessing", "order"])
def test_prediction_rejects_invalid_training_scope(scope):
    """Nuisance and preprocessing rows stay within canonical outer-train scopes."""
    _, kwargs = tiny_inputs()
    record = kwargs["training_records"][0]
    if scope == "nuisance":
        record["nuisance_train_ids"]["g0"] = ["d"]
    elif scope == "preprocessing":
        record["preprocessing_train_ids"]["g0"].append("a")
    else:
        record["preprocessing_train_ids"]["ps"].reverse()
    with pytest.raises(ValueError, match="nuisance|preprocessing|train|arm"):
        OOFPredictions.from_arrays(**kwargs)


def test_prediction_rejects_bad_origin_and_unsorted_records():
    """Trust labels are enumerated and records have one canonical order."""
    _, kwargs = tiny_inputs()
    kwargs["training_records"][0]["origin"] = "verified_by_statspai"
    with pytest.raises(ValueError, match="origin"):
        OOFPredictions.from_arrays(**kwargs)
    _, kwargs = tiny_inputs()
    kwargs["training_records"].reverse()
    with pytest.raises(ValueError, match="order|sorted"):
        OOFPredictions.from_arrays(**kwargs)


def test_raw_propensity_boundaries_are_legal():
    """Raw classifier probabilities may be zero or one before scoring."""
    _, kwargs = tiny_inputs()
    kwargs["ps_raw"][0, :2] = [0.0, 1.0]
    predictions = OOFPredictions.from_arrays(**kwargs)
    np.testing.assert_array_equal(predictions.ps_raw[0, :2], [0.0, 1.0])


def test_non_ascii_values_use_fixed_canonical_digest(tmp_path):
    """Default ASCII escaping has an independently computed SHA256 fixture."""
    _, kwargs = tiny_inputs()
    kwargs["ids"] = ["甲", "乙", "丙", "丁"]
    kwargs["covariate_names"] = ["协变量"]
    kwargs["source"]["recipe"] = "固定数组"
    kwargs["training_records"] = _training_records(
        kwargs["ids"], kwargs["d"], kwargs["fold_ids"]
    )
    predictions = OOFPredictions.from_arrays(**kwargs)
    path = tmp_path / "unicode.json"
    predictions.to_json(path)
    assert b"\\u7532" in path.read_bytes()
    assert (
        predictions.hashes["data"]
        == "6e2d9e6a77b6c452890688dcbae9175692993e8e2ecee738bac3469895346a12"
    )
    assert OOFPredictions.from_json(path).ids == tuple(kwargs["ids"])


def test_public_frozen_fields_rebuild_and_alignment_checks_order():
    """Frozen views compose, while stale row order fails observable alignment."""
    _, predictions = tiny_bundle()
    rebuilt = OOFPredictions.from_arrays(
        ids=predictions.ids,
        y=predictions.y,
        d=predictions.d,
        x=predictions.x,
        covariate_names=predictions.covariate_names,
        g0=predictions.g0,
        g1=predictions.g1,
        ps_raw=predictions.ps_raw,
        fold_ids=predictions.fold_ids,
        training_records=predictions.training_records,
        source=predictions.source,
    )
    assert dict(rebuilt.hashes) == dict(predictions.hashes)
    _, kwargs = tiny_inputs()
    reordered = permuted_inputs(kwargs, [1, 0, 3, 2])
    reordered_predictions = OOFPredictions.from_arrays(**reordered)
    reordered_predictions.validate_alignment(
        ids=reordered["ids"],
        y=reordered["y"],
        d=reordered["d"],
        x=reordered["x"],
        covariate_names=reordered["covariate_names"],
    )
    with pytest.raises(ValueError, match="alignment"):
        reordered_predictions.validate_alignment(
            ids=kwargs["ids"],
            y=kwargs["y"],
            d=kwargs["d"],
            x=kwargs["x"],
            covariate_names=kwargs["covariate_names"],
        )


def test_prediction_reader_rejects_unknown_schema_and_duplicate_keys(tmp_path):
    """Readers neither infer unknown versions nor accept ambiguous JSON objects."""
    _, predictions = tiny_bundle()
    path = tmp_path / "predictions.json"
    predictions.to_json(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["schema_version"] = "statspai.dml.predictions/999"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="schema"):
        OOFPredictions.from_json(path)

    predictions.to_json(path)
    marker = '"schema_version":"statspai.dml.predictions/1"'
    text = path.read_text(encoding="utf-8").replace(marker, marker + "," + marker, 1)
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate.*schema_version"):
        OOFPredictions.from_json(path)
