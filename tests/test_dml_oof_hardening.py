"""Hardening regressions for immutable and auditable DML OOF records."""

from __future__ import annotations

import builtins
import hashlib
import hmac
import json
import warnings
from pathlib import Path

import numpy as np
import pytest

from statspai import OOFBundle, OOFPredictions
from statspai.dml import _oof_validation as _validation

from .dml_oof_helpers import (
    _training_records,
    bundle_metadata,
    tiny_bundle,
    tiny_inputs,
    tiny_scored_bundle,
)


def _bundle_kwargs(bundle, *, predictions=None):
    return {
        "predictions": predictions or bundle.predictions,
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


def _mutate_array_header(array, operation):
    changed_shape = (array.size,) if array.ndim > 1 else (1, array.size)
    if operation == "shape":
        array.shape = changed_shape
    elif operation == "dtype":
        array.dtype = np.uint8
    elif operation == "strides":
        array.strides = tuple(0 for _ in array.shape)
    elif operation == "resize":
        array.resize(changed_shape, refcheck=False)
    else:
        array.setflags(write=True)


@pytest.mark.parametrize("record_type", [OOFPredictions, OOFBundle])
def test_direct_constructors_reject_invalid_empty_records(record_type):
    """Public records can only be created through validated constructors."""
    with pytest.raises(TypeError, match="from_arrays"):
        record_type()


@pytest.mark.parametrize(
    "operation", ["shape", "dtype", "strides", "resize", "setflags"]
)
def test_prediction_array_header_mutation_cannot_change_record(tmp_path, operation):
    """A caller-controlled NumPy header cannot mutate prediction state."""
    _, predictions = tiny_bundle()
    path = tmp_path / "predictions.json"
    predictions.to_json(path)
    expected_bytes = path.read_bytes()
    expected_hashes = dict(predictions.hashes)
    expected_y = predictions.y.copy()

    exposed = predictions.y
    try:
        _mutate_array_header(exposed, operation)
    except (AttributeError, TypeError, ValueError):
        pass

    np.testing.assert_array_equal(predictions.y, expected_y)
    assert dict(predictions.hashes) == expected_hashes
    predictions.to_json(path)
    assert path.read_bytes() == expected_bytes


@pytest.mark.parametrize(
    "operation", ["shape", "dtype", "strides", "resize", "setflags"]
)
def test_bundle_array_header_mutation_cannot_change_record(tmp_path, operation):
    """A caller-controlled NumPy header cannot mutate score-bundle state."""
    _, bundle = tiny_scored_bundle()
    path = tmp_path / "bundle.json"
    bundle.to_json(path)
    expected_bytes = path.read_bytes()
    expected_hash = bundle.hash
    expected_psi_b = bundle.psi_b.copy()

    exposed = bundle.psi_b
    try:
        _mutate_array_header(exposed, operation)
    except (AttributeError, TypeError, ValueError):
        pass

    np.testing.assert_array_equal(bundle.psi_b, expected_psi_b)
    assert bundle.hash == expected_hash
    bundle.to_json(path)
    assert path.read_bytes() == expected_bytes


@pytest.mark.parametrize("field", ["y", "x", "g0", "ps_raw"])
def test_prediction_rejects_complex_analysis_and_nuisance_arrays(field):
    """Complex values are rejected instead of silently losing imaginary parts."""
    _, kwargs = tiny_inputs()
    value = np.asarray(kwargs[field], dtype=complex)
    value.flat[0] += 1j
    kwargs[field] = value
    with pytest.raises(ValueError, match="complex"):
        OOFPredictions.from_arrays(**kwargs)


@pytest.mark.parametrize("field", ["y", "d", "x"])
def test_alignment_rejects_complex_live_arrays_without_warning(field):
    """Live alignment inputs reject imaginary parts without lossy casts."""
    _, predictions = tiny_bundle()
    live = {
        "ids": predictions.ids,
        "y": predictions.y,
        "d": predictions.d,
        "x": predictions.x,
        "covariate_names": predictions.covariate_names,
    }
    complex_value = np.asarray(live[field], dtype=complex)
    complex_value.flat[0] += 7j
    live[field] = complex_value

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with pytest.raises(
            ValueError, match="^OOFPredictions alignment failed for: input$"
        ):
            predictions.validate_alignment(**live)
    assert not any(item.category.__name__ == "ComplexWarning" for item in caught)


@pytest.mark.parametrize("field", ["ps_used", "psi_b", "psi", "theta", "se"])
def test_bundle_rejects_complex_score_arrays(field):
    """Every scorer array preserves real-valued ATE semantics."""
    _, bundle = tiny_scored_bundle()
    kwargs = _bundle_kwargs(bundle)
    value = np.asarray(kwargs[field], dtype=complex)
    value.flat[0] += 1j
    kwargs[field] = value
    with pytest.raises(ValueError, match="complex"):
        OOFBundle.from_arrays(**kwargs)


def test_bundle_rejects_self_consistent_score_not_bound_to_inputs():
    """Centered-score algebra cannot hide a pseudo-outcome unrelated to inputs."""
    _, bundle = tiny_scored_bundle()
    kwargs = _bundle_kwargs(bundle)
    psi_b = bundle.psi_b.copy() + 1.0
    theta = psi_b.mean(axis=1)
    kwargs.update(
        psi_b=psi_b,
        theta=theta,
        psi=psi_b - theta[:, None],
        se=np.std(psi_b, axis=1, ddof=0) / np.sqrt(psi_b.shape[1]),
        aggregation={
            "rule": "median_theta_median_variance_plus_split_deviation",
            "theta": float(np.median(theta)),
            "se": float(np.sqrt(np.median(np.var(psi_b, axis=1) / psi_b.shape[1]))),
        },
    )
    with pytest.raises(ValueError, match="psi_b|pseudo-outcome|ATE"):
        OOFBundle.from_arrays(**kwargs)


def _large_offset_bundle(theta):
    _, kwargs = tiny_inputs()
    offset = 1e12
    kwargs["y"] = np.array([0.0, offset, 0.0, offset])
    kwargs["g0"] = np.zeros((1, 4))
    kwargs["g1"] = np.full((1, 4), offset)
    predictions = OOFPredictions.from_arrays(**kwargs)
    psi_b = np.full((1, 4), offset)
    return OOFBundle.from_arrays(
        predictions=predictions,
        ps_used=np.full((1, 4), 0.5),
        psi_b=psi_b,
        psi=psi_b - theta,
        theta=[theta],
        se=[0.0],
        input_positions=np.arange(4),
        dropped_positions=[],
        aggregation={
            "rule": "median_theta_median_variance_plus_split_deviation",
            "theta": theta,
            "se": 0.0,
        },
        metadata=bundle_metadata(predictions),
    )


def test_large_offset_tolerance_is_ulp_bounded_not_relative():
    """A few ULPs are tolerated, while a material large-offset error is not."""
    offset = 1e12
    near = np.nextafter(offset, np.inf)
    assert _large_offset_bundle(near).theta[0] == near
    with pytest.raises(ValueError, match="theta"):
        _large_offset_bundle(offset + 0.5)


@pytest.mark.parametrize("artifact", ["prediction", "bundle"])
@pytest.mark.parametrize("bad_digest", ["0" * 63, "A" * 64, "g" * 64])
def test_reader_rejects_malformed_digest_before_comparison(
    tmp_path, monkeypatch, artifact, bad_digest
):
    """Stored digests must be exactly lowercase 64-character SHA256 hex."""
    if artifact == "prediction":
        _, value = tiny_bundle()
        path = tmp_path / "prediction.json"
        value.to_json(path)
        raw = json.loads(path.read_text(encoding="utf-8"))
        raw["hashes"]["data"] = bad_digest
        reader = OOFPredictions.from_json
    else:
        _, value = tiny_scored_bundle()
        path = tmp_path / "bundle.json"
        value.to_json(path)
        raw = json.loads(path.read_text(encoding="utf-8"))
        raw["hash"] = bad_digest
        reader = OOFBundle.from_json
    path.write_text(json.dumps(raw), encoding="utf-8")

    def unexpected_compare(*_args, **_kwargs):
        raise AssertionError("malformed digest reached compare_digest")

    monkeypatch.setattr(hmac, "compare_digest", unexpected_compare)
    with pytest.raises(ValueError, match="hash mismatch"):
        reader(path)


def test_tiny_bundle_has_independent_canonical_hash_golden(tmp_path):
    """The whole-bundle hash is pinned independently of the package helper."""
    _, bundle = tiny_scored_bundle()
    path = tmp_path / "bundle.json"
    bundle.to_json(path)
    actual_bytes = path.read_bytes()
    golden_bytes = (
        Path(__file__).parent / "fixtures" / "dml_oof" / "bundle_v1.json"
    ).read_bytes()
    assert actual_bytes == golden_bytes
    assert (
        hashlib.sha256(golden_bytes).hexdigest()
        == "2868d029b14a341d9e7bf3a82a5482450d019272dfaaa806acb3272efd1acfd8"
    )

    payload = json.loads(golden_bytes)
    stored = payload.pop("hash")
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
        ensure_ascii=True,
    ).encode("utf-8")
    expected = "a7ac8a82f6a671cab63b5254a2bc64a38c5ef63926e1afb7709b4047dc4c1840"
    assert stored == hashlib.sha256(encoded).hexdigest() == expected


def test_training_validation_builds_sets_linearly(monkeypatch):
    """Set construction scales with fold records rather than rows times records."""
    n_obs = 40
    ids = [f"row:{index}" for index in range(n_obs)]
    d = np.arange(n_obs) % 2
    folds = np.array([np.arange(n_obs) % 4])
    records = _training_records(ids, d, folds)
    calls = 0

    def counting_set(*args, **kwargs):
        nonlocal calls
        calls += 1
        return builtins.set(*args, **kwargs)

    monkeypatch.setattr(_validation, "set", counting_set, raising=False)
    OOFPredictions.from_arrays(
        ids=ids,
        y=np.arange(n_obs, dtype=float),
        d=d,
        x=np.arange(n_obs, dtype=float)[:, None],
        covariate_names=["x"],
        g0=np.zeros((1, n_obs)),
        g1=np.ones((1, n_obs)),
        ps_raw=np.full((1, n_obs), 0.5),
        fold_ids=folds,
        training_records=records,
        source={
            "engine": "fixture",
            "recipe": "four balanced folds",
            "seed": None,
            "software_versions": {"fixture": "1"},
        },
    )
    assert calls <= 20 * len(records) + 10


def test_top_level_type_stub_exports_oof_contracts():
    """Static tooling sees the same two containers as the runtime namespace."""
    text = Path("src/statspai/__init__.pyi").read_text(encoding="utf-8")
    assert "from .dml.oof import OOFBundle as OOFBundle" in text
    assert "from .dml.oof import OOFPredictions as OOFPredictions" in text


def test_oof_containers_are_importable_but_not_registered_functions():
    """Data containers stay public without posing as statistical callables."""
    import statspai as sp

    assert sp.OOFBundle is OOFBundle
    assert sp.OOFPredictions is OOFPredictions
    registered = set(sp.list_functions())
    assert {"OOFBundle", "OOFPredictions"}.isdisjoint(registered)
    assert "dml" in registered
