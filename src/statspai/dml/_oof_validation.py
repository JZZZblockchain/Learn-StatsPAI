"""Stateless validation and canonical serialization for DML OOF records."""

from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Any

import numpy as np

PREDICTION_SCHEMA = "statspai.dml.predictions/1"
BUNDLE_SCHEMA = "statspai.dml.oof/1"
AGGREGATION_RULE = "median_theta_median_variance_plus_split_deviation"
NUMERICAL_TOLERANCE = 1e-12

PREDICTION_KEYS = set(
    "schema_version ids covariate_names arrays training_records source hashes".split()
)
PREDICTION_ARRAY_KEYS = {"y", "d", "x", "g0", "g1", "ps_raw", "fold_ids"}
BUNDLE_KEYS = set(
    "schema_version predictions arrays input_mapping aggregation metadata hash".split()
)
BUNDLE_ARRAY_KEYS = {"ps_used", "psi_b", "psi", "theta", "se"}
INPUT_MAPPING_KEYS = {"input_positions", "dropped_positions"}

_HASH_KEYS = {"data", "predictions_and_folds", "training_source"}
_RECORD_KEYS = set(
    "rep fold_id train_ids test_ids nuisance_train_ids "
    "preprocessing_train_ids origin".split()
)
_LEARNERS = {"g0", "g1", "ps"}
_SOURCE_KEYS = {"engine", "recipe", "seed", "software_versions"}
_META_REQUIRED = set(
    "scoring_engine score psi_a variance_policy trimming_threshold normalize_ipw "
    "clipping_counts".split()
)
_META_OPTIONAL = {"fit_records"}
_FIT_KEYS = {"rep", "fold_id", "fit_seed", "subgroup_fallback_counts"}


def plain(value: Any) -> Any:
    """Convert public frozen views and NumPy values to ordinary JSON values."""
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("JSON object keys must be strings")
        return {key: plain(item) for key, item in value.items()}
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [plain(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def canonical_bytes(value: Any) -> bytes:
    """Encode canonical JSON using the schema's frozen stdlib options."""
    try:
        return json.dumps(
            plain(value),
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
            ensure_ascii=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"value is not finite canonical JSON: {exc}") from exc


def copy_json(value: Any, name: str) -> Any:
    try:
        return json.loads(canonical_bytes(value).decode("utf-8"))
    except ValueError as exc:
        raise ValueError(f"{name} must be finite JSON data: {exc}") from exc


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def read_json(path: Any, label: str) -> Any:
    try:
        return json.loads(
            Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"could not read {label} JSON: {exc}") from exc


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def require_keys(value: Any, expected: set[str], name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    actual = set(value)
    if actual != expected:
        missing = sorted(expected.difference(actual))
        extra = sorted(actual.difference(expected))
        raise ValueError(f"{name} keys invalid; missing={missing}, extra={extra}")
    return value


def freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: freeze_json(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(freeze_json(item) for item in value)
    return value


def _integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _close(actual, expected) -> bool:
    return bool(
        np.allclose(
            actual,
            expected,
            rtol=NUMERICAL_TOLERANCE,
            atol=NUMERICAL_TOLERANCE,
        )
    )


def immutable_array(
    value: Any, name: str, ndim: int, *, integer: bool = False
) -> np.ndarray:
    raw = np.asarray(value)
    if raw.ndim != ndim:
        raise ValueError(f"{name} must be {ndim}-dimensional")
    if integer and raw.size and raw.dtype.kind not in "iu":
        raise ValueError(f"{name} must contain integer values")
    try:
        result = np.asarray(raw, dtype=np.int64 if integer else float)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be numeric") from exc
    if not integer and not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    result = np.ascontiguousarray(result)
    return np.frombuffer(result.tobytes(), dtype=result.dtype).reshape(result.shape)


def validated_names(value: Any, name: str, length: int) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)):
        raise TypeError(f"{name} must be a sequence")
    try:
        result = tuple(value)
    except TypeError as exc:
        raise TypeError(f"{name} must be a sequence") from exc
    if len(result) != length:
        raise ValueError(f"{name} must have length {length}")
    if any(not isinstance(item, str) or not item for item in result):
        raise ValueError(f"{name} must contain non-empty strings")
    if len(set(result)) != len(result):
        raise ValueError(f"{name} must be unique")
    return result


def _id_list(value: Any, known: set[str], name: str) -> list[str]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{name} must contain non-empty string IDs")
    if len(value) != len(set(value)):
        raise ValueError(f"{name} must contain unique IDs")
    if set(value) - known:
        raise ValueError(f"{name} contains unknown IDs")
    return value


def validated_source(value: Any) -> dict[str, Any]:
    result = require_keys(copy_json(value, "source"), _SOURCE_KEYS, "source")
    for name in ("engine", "recipe"):
        if not isinstance(result[name], str) or not result[name].strip():
            raise ValueError(f"source.{name} must be a non-empty string")
    seed = result["seed"]
    if seed is not None and not _integer(seed):
        raise ValueError("source.seed must be an integer or None")
    versions = result["software_versions"]
    if not isinstance(versions, Mapping) or any(
        not isinstance(key, str) or not key or not isinstance(item, str) or not item
        for key, item in versions.items()
    ):
        raise ValueError("source.software_versions must map non-empty strings")
    return dict(result)


def validated_training_records(value: Any, ids, d, folds) -> list[dict[str, Any]]:
    records = copy_json(value, "training_records")
    if not isinstance(records, list):
        raise TypeError("training_records must be a list")
    known, treatment = set(ids), dict(zip(ids, d.tolist()))
    labels_by_rep = []
    for rep, labels in enumerate(folds):
        unique = np.unique(labels)
        if len(unique) < 2 or not np.array_equal(unique, np.arange(len(unique))):
            raise ValueError(f"fold_ids repeat {rep} must be contiguous 0..K-1")
        labels_by_rep.append(unique)
    if len({len(labels) for labels in labels_by_rep}) != 1:
        raise ValueError("all repeats must use the same number of folds")
    expected_pairs = [
        (rep, int(fold)) for rep, labels in enumerate(labels_by_rep) for fold in labels
    ]
    if len(records) != len(expected_pairs):
        raise ValueError("training_records must cover every repeat/fold once")

    actual_pairs = []
    for index, record in enumerate(records):
        record = require_keys(record, _RECORD_KEYS, f"training_records[{index}]")
        rep, fold = record["rep"], record["fold_id"]
        if not all(_integer(item) for item in (rep, fold)):
            raise ValueError("record rep and fold_id must be integers")
        actual_pairs.append((rep, fold))
        if (rep, fold) not in expected_pairs:
            raise ValueError("record repeat/fold is outside fold_ids")
        if record["origin"] not in {"statspai_internal", "caller_declared"}:
            raise ValueError("training record origin is invalid")

        train = _id_list(record["train_ids"], known, "train_ids")
        test = _id_list(record["test_ids"], known, "test_ids")
        expected_test = [row for row, label in zip(ids, folds[rep]) if label == fold]
        expected_train = [row for row in ids if row not in set(expected_test)]
        if test != expected_test or train != expected_train:
            raise ValueError("train/test IDs must be ordered strict fold complements")
        if {treatment[row] for row in train} != {0, 1}:
            raise ValueError("each training fold must contain both treatment arms")

        nuisance = require_keys(record["nuisance_train_ids"], _LEARNERS, "nuisance IDs")
        expected_nuisance = {
            "g0": [row for row in train if treatment[row] == 0],
            "g1": [row for row in train if treatment[row] == 1],
            "ps": train,
        }
        for learner, expected in expected_nuisance.items():
            if _id_list(nuisance[learner], known, f"nuisance.{learner}") != expected:
                raise ValueError(f"nuisance.{learner} has wrong arm/training scope")

        preprocessing = require_keys(
            record["preprocessing_train_ids"], _LEARNERS, "preprocessing IDs"
        )
        for learner in _LEARNERS:
            declared = _id_list(
                preprocessing[learner], known, f"preprocessing.{learner}"
            )
            canonical = [row for row in train if row in set(declared)]
            if declared != canonical:
                raise ValueError(
                    f"preprocessing.{learner} must be an ordered training subset"
                )
    if actual_pairs != expected_pairs:
        raise ValueError("training_records must be sorted by repeat and fold")
    return records


def prediction_hashes(payload: Mapping[str, Any]) -> dict[str, str]:
    arrays = payload["arrays"]
    return {
        "data": digest(
            {
                "ids": payload["ids"],
                "covariate_names": payload["covariate_names"],
                "arrays": {key: arrays[key] for key in ("y", "d", "x")},
            }
        ),
        "predictions_and_folds": digest(
            {"arrays": {key: arrays[key] for key in ("g0", "g1", "ps_raw", "fold_ids")}}
        ),
        "training_source": digest(
            {
                "training_records": payload["training_records"],
                "source": payload["source"],
            }
        ),
    }


def verify_hashes(stored: Any, expected: Mapping[str, str], label: str) -> None:
    stored = require_keys(stored, _HASH_KEYS, f"{label} hashes")
    for name, value in expected.items():
        if not isinstance(stored[name], str) or not hmac.compare_digest(
            stored[name], value
        ):
            raise ValueError(f"{label} hash mismatch for {name}")


def validated_score_arrays(values: Mapping[str, Any], n_rep: int, n_obs: int):
    shape = (n_rep, n_obs)
    scores = {
        name: immutable_array(values[name], name, 2)
        for name in ("ps_used", "psi_b", "psi")
    }
    if any(value.shape != shape for value in scores.values()):
        raise ValueError(f"ps_used, psi_b, and psi must have shape {shape}")
    theta = immutable_array(values["theta"], "theta", 1)
    se = immutable_array(values["se"], "se", 1)
    if theta.shape != (n_rep,) or se.shape != (n_rep,) or np.any(se < 0):
        raise ValueError("theta/se must be one finite value per repeat; se >= 0")
    expected_theta = np.mean(scores["psi_b"], axis=1)
    expected_psi = scores["psi_b"] - theta[:, None]
    expected_se = np.std(scores["psi_b"], axis=1, ddof=0) / np.sqrt(n_obs)
    if not _close(theta, expected_theta):
        raise ValueError("theta must equal mean(psi_b) by repeat")
    if not _close(scores["psi"], expected_psi):
        raise ValueError("psi must equal psi_b - theta by repeat")
    if not _close(se, expected_se):
        raise ValueError("se must use std(psi_b, ddof=0) / sqrt(n)")
    return {**scores, "theta": theta, "se": se}


def validated_input_mapping(kept: Any, dropped: Any, n_obs: int):
    kept = immutable_array(kept, "input_positions", 1, integer=True)
    dropped = immutable_array(dropped, "dropped_positions", 1, integer=True)
    if len(kept) != n_obs or np.any(kept < 0) or np.any(dropped < 0):
        raise ValueError("input mapping has invalid length or negative ordinals")
    if len(set(kept)) != len(kept) or len(set(dropped)) != len(dropped):
        raise ValueError("input mapping ordinals must be unique")
    if set(kept) & set(dropped):
        raise ValueError("kept and dropped input positions must be disjoint")
    combined = sorted(kept.tolist() + dropped.tolist())
    if combined != list(range(len(combined))):
        raise ValueError("input mapping must cover contiguous original ordinals")
    if np.any(np.diff(kept) <= 0) or np.any(np.diff(dropped) <= 0):
        raise ValueError("input positions must be strictly increasing")
    return kept, dropped


def validated_metadata(value: Any, info: Mapping[str, Any], ps_used) -> dict:
    result = copy_json(value, "metadata")
    if not isinstance(result, Mapping):
        raise TypeError("metadata must be a mapping")
    actual, allowed = set(result), _META_REQUIRED | _META_OPTIONAL
    if not _META_REQUIRED <= actual or not actual <= allowed:
        missing = sorted(_META_REQUIRED.difference(actual))
        extra = sorted(actual.difference(allowed))
        raise ValueError(f"metadata keys invalid; missing={missing}, extra={extra}")
    engine = result["scoring_engine"]
    engines = {
        "statspai_irm_internal": "statspai_internal",
        "statspai_irm_external_predictions": "caller_declared",
    }
    if engine not in engines:
        raise ValueError("metadata.scoring_engine is invalid")
    if {row["origin"] for row in info["training_records"]} != {engines[engine]}:
        raise ValueError("metadata scoring engine disagrees with training origin")
    if result["score"] != "ATE" or result["psi_a"] != -1:
        raise ValueError("metadata must declare score='ATE' and psi_a=-1")
    if result["variance_policy"] != "ddof0":
        raise ValueError("metadata.variance_policy must be 'ddof0'")
    if result["normalize_ipw"] is not False:
        raise ValueError("metadata.normalize_ipw must be false in schema version 1")
    threshold = result["trimming_threshold"]
    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, (int, float))
        or not 0 < threshold < 0.5
    ):
        raise ValueError("metadata.trimming_threshold must be between 0 and 0.5")
    ps_raw = info["ps_raw"]
    if not np.allclose(
        ps_used, np.clip(ps_raw, threshold, 1 - threshold), rtol=0, atol=0
    ):
        raise ValueError("ps_used does not match raw propensity clipping")

    counts = result["clipping_counts"]
    if not isinstance(counts, list) or len(counts) != info["n_rep"]:
        raise ValueError("metadata.clipping_counts must have one row per repeat")
    for rep, record in enumerate(counts):
        record = require_keys(
            record, {"rep", "n_clipped_low", "n_clipped_high"}, "clipping count"
        )
        if not all(_integer(record[name]) for name in record):
            raise ValueError("metadata clipping counts must be integers")
        expected = {
            "rep": rep,
            "n_clipped_low": int(np.sum(ps_raw[rep] < threshold)),
            "n_clipped_high": int(np.sum(ps_raw[rep] > 1 - threshold)),
        }
        if dict(record) != expected:
            raise ValueError("metadata clipping count disagrees with ps_raw")

    if engine == "statspai_irm_internal" and "fit_records" not in result:
        raise ValueError("internal metadata requires concrete fit_records")
    if "fit_records" in result:
        pairs = [(row["rep"], row["fold_id"]) for row in info["training_records"]]
        fits = result["fit_records"]
        if not isinstance(fits, list) or len(fits) != len(pairs):
            raise ValueError("metadata.fit_records must cover every repeat/fold")
        for fit, pair in zip(fits, pairs):
            fit = require_keys(fit, _FIT_KEYS, "fit record")
            if not all(_integer(fit[name]) for name in ("rep", "fold_id")):
                raise ValueError("metadata.fit_records repeat/fold must be integers")
            if (fit["rep"], fit["fold_id"]) != pair:
                raise ValueError("metadata.fit_records must be sorted by repeat/fold")
            seed, fallback = fit["fit_seed"], fit["subgroup_fallback_counts"]
            if engine.endswith("external_predictions"):
                if seed is not None or fallback is not None:
                    raise ValueError(
                        "external fit_seed and subgroup_fallback_counts must be None"
                    )
            else:
                if not _integer(seed):
                    raise ValueError("internal fit_seed must be an integer")
                fallback = require_keys(fallback, {"g0", "g1"}, "fallback counts")
                if any(not _integer(item) or item < 0 for item in fallback.values()):
                    raise ValueError("subgroup fallback counts must be non-negative")
    return dict(result)


def validated_aggregation(value: Any, theta, se) -> dict:
    result = require_keys(
        copy_json(value, "aggregation"), {"rule", "theta", "se"}, "aggregation"
    )
    median = float(np.median(theta))
    combined_se = float(np.sqrt(np.median(se**2 + (theta - median) ** 2)))
    if result["rule"] != AGGREGATION_RULE:
        raise ValueError(f"aggregation.rule must be {AGGREGATION_RULE!r}")
    for name in ("theta", "se"):
        if isinstance(result[name], bool) or not isinstance(result[name], (int, float)):
            raise ValueError(f"aggregation.{name} must be numeric")
    if not _close(result["theta"], median):
        raise ValueError("aggregation.theta disagrees with repeat estimates")
    if not _close(result["se"], combined_se):
        raise ValueError("aggregation.se disagrees with repeat estimates")
    return dict(result)
