"""Contracts for validated, serialized DML OOF score bundles."""

from __future__ import annotations

import json

import numpy as np
import pytest

from statspai import OOFBundle, OOFPredictions

from .dml_oof_helpers import (
    bundle_metadata,
    tiny_bundle,
    tiny_inputs,
    tiny_scored_bundle,
)


def test_bundle_roundtrip_copy_hash_and_frame(tmp_path):
    """A scored bundle is immutable, auditable, and exports long-form rows."""
    _, predictions = tiny_bundle(n_rep=2)
    scorer_arrays = {
        "ps_used": np.full((2, 4), 0.5),
        "psi_b": np.tile([2.0, 4.0, -2.0, 8.0], (2, 1)),
        "psi": np.tile([-1.0, 1.0, -5.0, 5.0], (2, 1)),
        "theta": np.array([3.0, 3.0]),
        "se": np.full(2, np.sqrt(3.25)),
        "input_positions": np.arange(4),
        "dropped_positions": np.array([], dtype=int),
    }
    aggregation = {
        "rule": "median_theta_median_variance_plus_split_deviation",
        "theta": 3.0,
        "se": float(np.sqrt(3.25)),
    }
    metadata = bundle_metadata(predictions)
    bundle = OOFBundle.from_arrays(
        predictions=predictions,
        aggregation=aggregation,
        metadata=metadata,
        **scorer_arrays,
    )
    scorer_arrays["psi"][0, 0] = 999.0
    aggregation["theta"] = 999.0
    metadata["scoring_engine"] = "changed"
    assert bundle.psi[0, 0] == -1.0
    assert bundle.aggregation["theta"] == 3.0
    assert bundle.metadata["scoring_engine"] == "statspai_irm_external_predictions"
    for array in (
        bundle.ps_used,
        bundle.psi_b,
        bundle.psi,
        bundle.theta,
        bundle.se,
        bundle.input_positions,
        bundle.dropped_positions,
    ):
        assert not array.flags.writeable

    frame = bundle.to_frame()
    assert frame.shape[0] == 8
    assert list(frame.columns) == [
        "rep",
        "row_id",
        "input_position",
        "fold_id",
        "training_origin",
        "y",
        "d",
        "g0",
        "g1",
        "ps_raw",
        "ps_used",
        "psi_b",
        "psi",
    ]
    assert "x" not in frame
    assert frame.groupby(["rep", "row_id"]).size().eq(1).all()
    frame.loc[0, "psi"] = 999.0
    assert bundle.psi[0, 0] == -1.0

    path = tmp_path / "bundle.json"
    bundle.to_json(path)
    assert set(json.loads(path.read_text(encoding="utf-8"))) == {
        "schema_version",
        "predictions",
        "arrays",
        "input_mapping",
        "aggregation",
        "metadata",
        "hash",
    }
    restored = OOFBundle.from_json(path)
    np.testing.assert_array_equal(restored.psi, bundle.psi)
    np.testing.assert_array_equal(restored.input_positions, bundle.input_positions)
    assert restored.hash == bundle.hash


@pytest.mark.parametrize(
    "target",
    [
        "ps_used",
        "psi_b",
        "psi",
        "theta",
        "se",
        "input_positions",
        "dropped_positions",
        "predictions",
        "aggregation",
        "metadata",
    ],
)
def test_bundle_reader_rejects_tampering(tmp_path, target):
    """The bundle digest covers every score, mapping, and metadata member."""
    _, bundle = tiny_scored_bundle()
    path = tmp_path / "bundle.json"
    bundle.to_json(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    if target in {"ps_used", "psi_b", "psi"}:
        raw["arrays"][target][0][0] += 0.1
    elif target in {"theta", "se"}:
        raw["arrays"][target][0] += 0.1
    elif target == "predictions":
        raw["predictions"]["arrays"]["g0"][0][0] += 1.0
    elif target == "input_positions":
        raw["input_mapping"]["input_positions"][0] = 3
    elif target == "dropped_positions":
        raw["input_mapping"]["dropped_positions"].append(4)
    elif target == "aggregation":
        raw["aggregation"]["theta"] += 1.0
    else:
        raw["metadata"]["score"] = "ATTE"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="hash"):
        OOFBundle.from_json(path)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("ps_used", np.full((1, 3), 0.5)),
        ("psi_b", np.full((1, 4), np.nan)),
        ("theta", np.array([1.0, 2.0])),
        ("se", np.array([-1.0])),
        ("input_positions", np.array([0, 1, 1, 3])),
        ("dropped_positions", np.array([3])),
    ],
)
def test_bundle_rejects_invalid_arrays_and_input_mapping(field, value):
    """Scores and original-row ordinals must match the prediction snapshot."""
    _, predictions = tiny_bundle()
    _, bundle = tiny_scored_bundle()
    kwargs = {
        "predictions": predictions,
        "ps_used": bundle.ps_used,
        "psi_b": bundle.psi_b,
        "psi": bundle.psi,
        "theta": bundle.theta,
        "se": bundle.se,
        "input_positions": bundle.input_positions,
        "dropped_positions": bundle.dropped_positions,
        "aggregation": bundle.aggregation,
        "metadata": bundle.metadata,
    }
    kwargs[field] = value
    with pytest.raises((TypeError, ValueError), match=".+"):
        OOFBundle.from_arrays(**kwargs)


@pytest.mark.parametrize(
    ("case", "change"),
    [
        ("uncentered_psi", lambda kw: kw["psi"].__setitem__((0, 0), 0.0)),
        ("wrong_theta", lambda kw: kw["theta"].__setitem__(0, 4.0)),
        ("wrong_se", lambda kw: kw["se"].__setitem__(0, 0.0)),
        ("wrong_ps_used", lambda kw: kw["ps_used"].__setitem__((0, 0), 0.4)),
        ("wrong_rule", lambda kw: kw["aggregation"].__setitem__("rule", "median")),
        ("wrong_aggregate", lambda kw: kw["aggregation"].__setitem__("theta", 4.0)),
        (
            "nonnumeric_aggregate",
            lambda kw: kw["aggregation"].__setitem__("theta", "three"),
        ),
        (
            "wrong_clipping_count",
            lambda kw: kw["metadata"]["clipping_counts"][0].__setitem__(
                "n_clipped_low", 1
            ),
        ),
        (
            "wrong_engine",
            lambda kw: kw["metadata"].__setitem__("scoring_engine", "fixture"),
        ),
        (
            "origin_engine_mismatch",
            lambda kw: kw["metadata"].__setitem__(
                "scoring_engine", "statspai_irm_internal"
            ),
        ),
    ],
)
def test_bundle_rejects_inconsistent_score_and_provenance(case, change):
    """A version-1 bundle represents canonical binary-ATE scorer output."""
    _, predictions = tiny_bundle()
    _, template = tiny_scored_bundle()
    kwargs = {
        "predictions": predictions,
        "ps_used": template.ps_used.copy(),
        "psi_b": template.psi_b.copy(),
        "psi": template.psi.copy(),
        "theta": template.theta.copy(),
        "se": template.se.copy(),
        "input_positions": template.input_positions.copy(),
        "dropped_positions": template.dropped_positions.copy(),
        "aggregation": dict(template.aggregation),
        "metadata": bundle_metadata(predictions),
    }
    change(kwargs)
    with pytest.raises(ValueError, match=".+"):
        OOFBundle.from_arrays(**kwargs)


def test_bundle_accepts_gapped_mapping_and_public_frozen_fields():
    """Frozen public fields compose into a clone with interleaved dropped rows."""
    _, predictions = tiny_bundle()
    _, bundle = tiny_scored_bundle()
    mapped = OOFBundle.from_arrays(
        predictions=predictions,
        ps_used=bundle.ps_used,
        psi_b=bundle.psi_b,
        psi=bundle.psi,
        theta=bundle.theta,
        se=bundle.se,
        input_positions=[0, 2, 3, 5],
        dropped_positions=[1, 4],
        aggregation=bundle.aggregation,
        metadata=bundle.metadata,
    )
    np.testing.assert_array_equal(mapped.input_positions, [0, 2, 3, 5])
    np.testing.assert_array_equal(mapped.dropped_positions, [1, 4])


def test_bundle_requires_core_metadata_and_validates_optional_fit_records():
    """Core scorer metadata is fixed; optional per-fold details are validated."""
    _, predictions = tiny_bundle()
    _, bundle = tiny_scored_bundle()
    missing = bundle_metadata(predictions)
    missing.pop("variance_policy")
    malformed = bundle_metadata(predictions)
    malformed["fit_records"][0]["fit_seed"] = "unknown"
    boolean_count = bundle_metadata(predictions)
    boolean_count["clipping_counts"][0]["n_clipped_low"] = False
    boolean_rep = bundle_metadata(predictions)
    boolean_rep["fit_records"][0]["rep"] = False
    invalid = (
        (missing, "metadata"),
        (malformed, "fit_seed"),
        (boolean_count, "clipping"),
        (boolean_rep, "fit_records"),
    )
    for metadata, message in invalid:
        with pytest.raises(ValueError, match=message):
            OOFBundle.from_arrays(
                predictions=predictions,
                ps_used=bundle.ps_used,
                psi_b=bundle.psi_b,
                psi=bundle.psi,
                theta=bundle.theta,
                se=bundle.se,
                input_positions=bundle.input_positions,
                dropped_positions=bundle.dropped_positions,
                aggregation=bundle.aggregation,
                metadata=metadata,
            )


def test_bundle_external_metadata_may_omit_unavailable_fit_records():
    """External callers need not invent seeds or fallback audit details."""
    _, predictions = tiny_bundle()
    _, template = tiny_scored_bundle()
    metadata = bundle_metadata(predictions)
    metadata.pop("fit_records")
    bundle = OOFBundle.from_arrays(
        predictions=predictions,
        ps_used=template.ps_used,
        psi_b=template.psi_b,
        psi=template.psi,
        theta=template.theta,
        se=template.se,
        input_positions=template.input_positions,
        dropped_positions=template.dropped_positions,
        aggregation=template.aggregation,
        metadata=metadata,
    )
    assert "fit_records" not in bundle.metadata


def test_bundle_rejects_internal_engine_without_internal_prediction_audit():
    """The score engine must agree with training origin and fit provenance."""
    _, kwargs = tiny_inputs()
    for record in kwargs["training_records"]:
        record["origin"] = "statspai_internal"
    predictions = OOFPredictions.from_arrays(**kwargs)
    _, template = tiny_scored_bundle()
    metadata = bundle_metadata(predictions, scoring_engine="statspai_irm_internal")
    metadata.pop("fit_records")
    with pytest.raises(ValueError, match="fit_records"):
        OOFBundle.from_arrays(
            predictions=predictions,
            ps_used=template.ps_used,
            psi_b=template.psi_b,
            psi=template.psi,
            theta=template.theta,
            se=template.se,
            input_positions=template.input_positions,
            dropped_positions=template.dropped_positions,
            aggregation=template.aggregation,
            metadata=metadata,
        )


def test_bundle_accepts_observed_internal_fit_audit_records():
    """Internal bundles record concrete fold seeds and fallback counts."""
    _, kwargs = tiny_inputs()
    for record in kwargs["training_records"]:
        record["origin"] = "statspai_internal"
    predictions = OOFPredictions.from_arrays(**kwargs)
    _, template = tiny_scored_bundle()
    bundle = OOFBundle.from_arrays(
        predictions=predictions,
        ps_used=template.ps_used,
        psi_b=template.psi_b,
        psi=template.psi,
        theta=template.theta,
        se=template.se,
        input_positions=template.input_positions,
        dropped_positions=template.dropped_positions,
        aggregation=template.aggregation,
        metadata=bundle_metadata(predictions, scoring_engine="statspai_irm_internal"),
    )
    assert bundle.metadata["fit_records"][0]["fit_seed"] == 42
    assert bundle.metadata["fit_records"][0]["subgroup_fallback_counts"] == {
        "g0": 0,
        "g1": 0,
    }


def test_bundle_records_exact_raw_propensity_clipping_counts():
    """Boundary raw probabilities stay visible and their clipping is audited."""
    _, kwargs = tiny_inputs()
    kwargs["ps_raw"][0] = [0.0, 1.0, 0.5, 0.5]
    predictions = OOFPredictions.from_arrays(**kwargs)
    _, template = tiny_scored_bundle()
    metadata = bundle_metadata(predictions)
    metadata["clipping_counts"][0].update(n_clipped_low=1, n_clipped_high=1)
    ps_used = np.array([[0.01, 0.99, 0.5, 0.5]])
    psi_b = (
        predictions.g1
        - predictions.g0
        + predictions.d[None, :] * (predictions.y[None, :] - predictions.g1) / ps_used
        - (1 - predictions.d[None, :])
        * (predictions.y[None, :] - predictions.g0)
        / (1 - ps_used)
    )
    theta = psi_b.mean(axis=1)
    se = np.std(psi_b, axis=1, ddof=0) / np.sqrt(psi_b.shape[1])
    bundle = OOFBundle.from_arrays(
        predictions=predictions,
        ps_used=ps_used,
        psi_b=psi_b,
        psi=psi_b - theta[:, None],
        theta=theta,
        se=se,
        input_positions=template.input_positions,
        dropped_positions=template.dropped_positions,
        aggregation={
            "rule": "median_theta_median_variance_plus_split_deviation",
            "theta": float(np.median(theta)),
            "se": float(np.sqrt(np.median(se**2))),
        },
        metadata=metadata,
    )
    assert bundle.metadata["clipping_counts"][0]["n_clipped_low"] == 1
    np.testing.assert_array_equal(bundle.predictions.ps_raw[0, :2], [0.0, 1.0])


def test_bundle_reader_rejects_unknown_schema(tmp_path):
    """Bundle schema versions are explicit rather than inferred."""
    _, bundle = tiny_scored_bundle()
    path = tmp_path / "bundle.json"
    bundle.to_json(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["schema_version"] = "statspai.dml.oof/999"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="schema"):
        OOFBundle.from_json(path)
