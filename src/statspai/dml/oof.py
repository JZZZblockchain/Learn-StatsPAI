"""Immutable, versioned records for DML out-of-fold predictions.

Hashes detect corruption of serialized artifacts; they do not authenticate a
producer or prove that caller-declared learners avoided held-out data.  The
alignment check compares observable row identity and values only.
"""

from __future__ import annotations

import hmac
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, Tuple

import numpy as np
import pandas as pd

from . import _oof_validation as _v


def _make(cls, values):
    instance = object.__new__(cls)
    for name, value in values.items():
        object.__setattr__(instance, name, value)
    return instance


@dataclass(frozen=True, init=False, eq=False)
class OOFPredictions:
    """Validated predictions and declared cross-fitting provenance.

    Records marked ``caller_declared`` describe claims StatsPAI can check for
    structural consistency, not training behavior StatsPAI observed.
    """

    schema_version: str
    ids: Tuple[str, ...]
    covariate_names: Tuple[str, ...]
    y: np.ndarray = field(repr=False)
    d: np.ndarray = field(repr=False)
    x: np.ndarray = field(repr=False)
    g0: np.ndarray = field(repr=False)
    g1: np.ndarray = field(repr=False)
    ps_raw: np.ndarray = field(repr=False)
    fold_ids: np.ndarray = field(repr=False)
    training_records: Tuple[Mapping[str, Any], ...]
    source: Mapping[str, Any]
    hashes: Mapping[str, str]

    @classmethod
    def from_arrays(
        cls,
        *,
        ids,
        y,
        d,
        x,
        covariate_names,
        g0,
        g1,
        ps_raw,
        fold_ids,
        training_records,
        source,
    ) -> "OOFPredictions":
        """Validate and defensively copy a complete analysis-sample snapshot."""
        y = _v.immutable_array(y, "y", 1)
        d = _v.immutable_array(d, "d", 1)
        x = _v.immutable_array(x, "x", 2)
        if not len(y):
            raise ValueError("OOFPredictions requires at least one observation")
        ids = _v.validated_names(ids, "ids", len(y))
        covariates = _v.validated_names(covariate_names, "covariate_names", x.shape[1])
        if d.shape != y.shape or x.shape[0] != len(y):
            raise ValueError("d and x observation counts must match y")
        if not np.all((d == 0) | (d == 1)) or set(d.tolist()) != {0.0, 1.0}:
            raise ValueError("d must contain both binary treatment groups")
        d = _v.immutable_array(d.astype(np.int64), "d", 1, integer=True)

        predictions = {
            name: _v.immutable_array(value, name, 2, integer=name == "fold_ids")
            for name, value in {
                "g0": g0,
                "g1": g1,
                "ps_raw": ps_raw,
                "fold_ids": fold_ids,
            }.items()
        }
        shape = predictions["g0"].shape
        if shape[0] < 1 or shape[1] != len(y):
            raise ValueError("prediction shape must be (at least one repeat, n_obs)")
        if any(value.shape != shape for value in predictions.values()):
            raise ValueError("g0, g1, ps_raw, and fold_ids must share shape (R, n)")
        if not np.all((predictions["ps_raw"] >= 0) & (predictions["ps_raw"] <= 1)):
            raise ValueError("ps_raw must lie in inclusive [0, 1]")

        records = _v.validated_training_records(
            training_records, ids, d, predictions["fold_ids"]
        )
        source = _v.validated_source(source)
        arrays = {"y": y.tolist(), "d": d.tolist(), "x": x.tolist()}
        arrays.update({name: value.tolist() for name, value in predictions.items()})
        payload = {
            "schema_version": _v.PREDICTION_SCHEMA,
            "ids": list(ids),
            "covariate_names": list(covariates),
            "arrays": arrays,
            "training_records": records,
            "source": source,
        }
        return _make(
            cls,
            {
                "schema_version": _v.PREDICTION_SCHEMA,
                "ids": ids,
                "covariate_names": covariates,
                "y": y,
                "d": d,
                "x": x,
                **predictions,
                "training_records": _v.freeze_json(records),
                "source": _v.freeze_json(source),
                "hashes": MappingProxyType(_v.prediction_hashes(payload)),
            },
        )

    @property
    def n_obs(self) -> int:
        return len(self.ids)

    @property
    def n_rep(self) -> int:
        return self.g0.shape[0]

    @property
    def n_folds(self) -> int:
        return len(np.unique(self.fold_ids[0]))

    def validate_alignment(self, *, ids, y, d, x, covariate_names) -> None:
        """Raise unless current analysis inputs exactly match this row order."""
        try:
            checks = {
                "ids": tuple(ids) == self.ids,
                "covariate_names": tuple(covariate_names) == self.covariate_names,
                "y": np.array_equal(np.asarray(y, dtype=float), self.y),
                "d": np.array_equal(np.asarray(d), self.d),
                "x": np.array_equal(np.asarray(x, dtype=float), self.x),
            }
        except (TypeError, ValueError):
            checks = {"input": False}
        failed = [name for name, matches in checks.items() if not matches]
        if failed:
            raise ValueError(
                "OOFPredictions alignment failed for: " + ", ".join(failed)
            )

    def _payload(self):
        arrays = {
            name: getattr(self, name).tolist()
            for name in ("y", "d", "x", "g0", "g1", "ps_raw", "fold_ids")
        }
        return {
            "schema_version": self.schema_version,
            "ids": list(self.ids),
            "covariate_names": list(self.covariate_names),
            "arrays": arrays,
            "training_records": _v.plain(self.training_records),
            "source": _v.plain(self.source),
            "hashes": dict(self.hashes),
        }

    def to_json(self, path) -> None:
        """Write deterministic UTF-8 JSON with three partition hashes."""
        Path(path).write_bytes(_v.canonical_bytes(self._payload()))

    @classmethod
    def _from_payload(cls, payload):
        payload = _v.require_keys(payload, _v.PREDICTION_KEYS, "prediction")
        if payload["schema_version"] != _v.PREDICTION_SCHEMA:
            raise ValueError(
                f"unknown OOFPredictions schema: {payload['schema_version']!r}"
            )
        arrays = _v.require_keys(
            payload["arrays"], _v.PREDICTION_ARRAY_KEYS, "prediction arrays"
        )
        _v.verify_hashes(payload["hashes"], _v.prediction_hashes(payload), "prediction")
        result = cls.from_arrays(
            ids=payload["ids"],
            covariate_names=payload["covariate_names"],
            training_records=payload["training_records"],
            source=payload["source"],
            **arrays,
        )
        _v.verify_hashes(payload["hashes"], result.hashes, "prediction")
        return result

    @classmethod
    def from_json(cls, path):
        """Read only after checking schema, duplicate keys, and stored hashes."""
        return cls._from_payload(_v.read_json(path, "OOFPredictions"))

    def _clone(self):
        arrays = {
            name: getattr(self, name)
            for name in ("y", "d", "x", "g0", "g1", "ps_raw", "fold_ids")
        }
        return type(self).from_arrays(
            ids=self.ids,
            covariate_names=self.covariate_names,
            training_records=self.training_records,
            source=self.source,
            **arrays,
        )


@dataclass(frozen=True, init=False, eq=False)
class OOFBundle:
    """Validated StatsPAI binary-ATE score output (tolerance ``1e-12``)."""

    schema_version: str
    predictions: OOFPredictions
    ps_used: np.ndarray = field(repr=False)
    psi_b: np.ndarray = field(repr=False)
    psi: np.ndarray = field(repr=False)
    theta: np.ndarray = field(repr=False)
    se: np.ndarray = field(repr=False)
    input_positions: np.ndarray = field(repr=False)
    dropped_positions: np.ndarray = field(repr=False)
    aggregation: Mapping[str, Any]
    metadata: Mapping[str, Any]
    hash: str

    @classmethod
    def from_arrays(
        cls,
        *,
        predictions,
        ps_used,
        psi_b,
        psi,
        theta,
        se,
        input_positions,
        dropped_positions,
        aggregation,
        metadata,
    ) -> "OOFBundle":
        """Validate and copy canonical binary-ATE scoring output."""
        if not isinstance(predictions, OOFPredictions):
            raise TypeError("predictions must be OOFPredictions")
        scores = _v.validated_score_arrays(
            {"ps_used": ps_used, "psi_b": psi_b, "psi": psi, "theta": theta, "se": se},
            predictions.n_rep,
            predictions.n_obs,
        )
        kept, dropped = _v.validated_input_mapping(
            input_positions, dropped_positions, predictions.n_obs
        )
        info = {
            "n_rep": predictions.n_rep,
            "ps_raw": predictions.ps_raw,
            "training_records": predictions.training_records,
        }
        metadata = _v.validated_metadata(metadata, info, scores["ps_used"])
        aggregation = _v.validated_aggregation(
            aggregation, scores["theta"], scores["se"]
        )
        instance = _make(
            cls,
            {
                "schema_version": _v.BUNDLE_SCHEMA,
                "predictions": predictions._clone(),
                **scores,
                "input_positions": kept,
                "dropped_positions": dropped,
                "aggregation": _v.freeze_json(aggregation),
                "metadata": _v.freeze_json(metadata),
            },
        )
        object.__setattr__(instance, "hash", _v.digest(instance._unsigned_payload()))
        return instance

    def _unsigned_payload(self):
        return {
            "schema_version": self.schema_version,
            "predictions": self.predictions._payload(),
            "arrays": {
                name: getattr(self, name).tolist()
                for name in ("ps_used", "psi_b", "psi", "theta", "se")
            },
            "input_mapping": {
                "input_positions": self.input_positions.tolist(),
                "dropped_positions": self.dropped_positions.tolist(),
            },
            "aggregation": _v.plain(self.aggregation),
            "metadata": _v.plain(self.metadata),
        }

    def _payload(self):
        result = self._unsigned_payload()
        result["hash"] = self.hash
        return result

    def to_frame(self) -> pd.DataFrame:
        """Return repeat-major score rows without individual covariate values."""
        repeats, n_obs = self.ps_used.shape
        rep = np.repeat(np.arange(repeats), n_obs)
        folds = self.predictions.fold_ids.reshape(-1)
        origins = {
            (row["rep"], row["fold_id"]): row["origin"]
            for row in self.predictions.training_records
        }
        return pd.DataFrame(
            {
                "rep": rep,
                "row_id": np.tile(self.predictions.ids, repeats),
                "input_position": np.tile(self.input_positions, repeats),
                "fold_id": folds,
                "training_origin": [
                    origins[(int(r), int(f))] for r, f in zip(rep, folds)
                ],
                "y": np.tile(self.predictions.y, repeats),
                "d": np.tile(self.predictions.d, repeats),
                **{
                    name: getattr(self.predictions, name).reshape(-1)
                    for name in ("g0", "g1", "ps_raw")
                },
                **{
                    name: getattr(self, name).reshape(-1)
                    for name in ("ps_used", "psi_b", "psi")
                },
            }
        )

    def to_json(self, path) -> None:
        """Write deterministic UTF-8 JSON with one whole-bundle hash."""
        Path(path).write_bytes(_v.canonical_bytes(self._payload()))

    @classmethod
    def from_json(cls, path):
        """Read only after checking schema, duplicate keys, and stored hash."""
        payload = _v.require_keys(
            _v.read_json(path, "OOFBundle"), _v.BUNDLE_KEYS, "bundle"
        )
        if payload["schema_version"] != _v.BUNDLE_SCHEMA:
            raise ValueError(f"unknown OOFBundle schema: {payload['schema_version']!r}")
        arrays = _v.require_keys(
            payload["arrays"], _v.BUNDLE_ARRAY_KEYS, "bundle arrays"
        )
        positions = _v.require_keys(
            payload["input_mapping"], _v.INPUT_MAPPING_KEYS, "input mapping"
        )
        stored = payload["hash"]
        unsigned = {name: value for name, value in payload.items() if name != "hash"}
        if not isinstance(stored, str) or not hmac.compare_digest(
            stored, _v.digest(unsigned)
        ):
            raise ValueError("bundle hash mismatch")
        result = cls.from_arrays(
            predictions=OOFPredictions._from_payload(payload["predictions"]),
            aggregation=payload["aggregation"],
            metadata=payload["metadata"],
            **arrays,
            **positions,
        )
        if not hmac.compare_digest(stored, result.hash):
            raise ValueError("bundle hash changed during reconstruction")
        return result


__all__ = ["OOFBundle", "OOFPredictions"]
