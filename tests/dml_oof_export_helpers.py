"""Deterministic fixtures and no-fit learners for retained DML OOF tests."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from statspai import OOFPredictions, dml
from statspai.dml.irm import DoubleMLIRM

from .dml_oof_helpers import tiny_inputs


class NoFitRegressor(BaseEstimator):
    """Fail if the external-prediction path touches an outcome learner."""

    def fit(self, *_args, **_kwargs):
        raise AssertionError("external OOF scoring must not fit ml_g")

    def predict(self, *_args, **_kwargs):
        raise AssertionError("external OOF scoring must not predict with ml_g")


class NoFitClassifier(BaseEstimator):
    """Fail if the external-prediction path touches a propensity learner."""

    def fit(self, *_args, **_kwargs):
        raise AssertionError("external OOF scoring must not fit ml_m")

    def predict(self, *_args, **_kwargs):
        raise AssertionError("external OOF scoring must not predict with ml_m")

    def predict_proba(self, *_args, **_kwargs):
        raise AssertionError("external OOF scoring must not predict_proba with ml_m")


def _row_positions(x):
    return tuple(np.rint(np.asarray(x)[:, 0] + 24.0).astype(int).tolist())


class AuditScaler(TransformerMixin, BaseEstimator):
    """Identity transform that records the rows and means seen by each pipeline."""

    fit_rows = []
    fit_means = []

    def fit(self, x, _y=None):
        type(self).fit_rows.append(_row_positions(x))
        type(self).fit_means.append(np.mean(np.asarray(x), axis=0))
        return self

    def transform(self, x):
        return np.array(x, dtype=float, copy=True)


class TrainingMeanRegressor(BaseEstimator):
    """Deterministic training-mean outcome learner with shared fit audit."""

    fit_rows = []

    def fit(self, x, y):
        type(self).fit_rows.append(_row_positions(x))
        self.mean_ = float(np.mean(y))
        return self

    def predict(self, x):
        return np.full(len(x), self.mean_, dtype=float)


class TrainingRateClassifier(BaseEstimator):
    """Deterministic treatment-rate classifier with shared fit audit."""

    fit_rows = []

    def fit(self, x, y):
        type(self).fit_rows.append(_row_positions(x))
        self.rate_ = float(np.mean(y))
        self.classes_ = np.array([0.0, 1.0])
        return self

    def predict(self, x):
        return np.full(len(x), self.rate_ >= 0.5, dtype=float)

    def predict_proba(self, x):
        treated = np.full(len(x), self.rate_, dtype=float)
        return np.column_stack((1.0 - treated, treated))


def reset_internal_audits():
    AuditScaler.fit_rows = []
    AuditScaler.fit_means = []
    TrainingMeanRegressor.fit_rows = []
    TrainingRateClassifier.fit_rows = []


def internal_literal_frame(n=48):
    """Return the deterministic Task 5 internal data formula."""
    position = np.arange(n)
    d = (position % 2).astype(float)
    x1 = position.astype(float) - 24.0
    x2 = (position % 5).astype(float) - 2.0
    y = 5.0 + 2.0 * d + 0.25 * x2
    return pd.DataFrame({"y": y, "d": d, "x1": x1, "x2": x2})


def internal_mapping_frame():
    """Return the frozen 41-row missing-data and duplicate-index fixture."""
    position = np.arange(41)
    d = (position % 2).astype(float)
    x = position.astype(float)
    x[0] = np.nan
    y = 5.0 + 2.0 * d + 0.25 * position
    fold = np.concatenate(([0], np.repeat([0, 1], 20)))
    frame = pd.DataFrame({"y": y, "d": d, "x": x, "fold": fold})
    frame.index = position // 2
    return frame


def internal_partitions():
    return {
        101: np.tile([0, 0, 1, 1], 12),
        102: np.tile([0, 1, 1, 0], 12),
        103: np.tile([0, 0, 1, 1, 1, 1, 0, 0], 6),
    }


def partition_splits(labels):
    return [
        (np.flatnonzero(labels != fold), np.flatnonzero(labels == fold))
        for fold in range(2)
    ]


def internal_estimator(
    frame, *, n_rep=1, random_state=101, fold_indices=None, forbid_fit=False
):
    """Build a deterministic internal IRM estimator for retention tests."""
    if forbid_fit:
        ml_g, ml_m = NoFitRegressor(), NoFitClassifier()
    else:
        ml_g = Pipeline([("audit", AuditScaler()), ("mean", TrainingMeanRegressor())])
        ml_m = Pipeline([("audit", AuditScaler()), ("rate", TrainingRateClassifier())])
    return DoubleMLIRM(
        frame,
        y="y",
        treat="d",
        covariates=["x1", "x2"] if "x1" in frame else ["x"],
        ml_g=ml_g,
        ml_m=ml_m,
        n_folds=2,
        n_rep=n_rep,
        random_state=random_state,
        fold_indices=fold_indices,
    )


def internal_functional_fit(frame, observation_ids):
    """Run the functional internal retained path with deterministic learners."""
    return dml(
        frame,
        "y",
        "d",
        ["x1", "x2"],
        model="irm",
        ml_g=Pipeline([("audit", AuditScaler()), ("mean", TrainingMeanRegressor())]),
        ml_m=Pipeline([("audit", AuditScaler()), ("rate", TrainingRateClassifier())]),
        n_folds=2,
        fold_indices=internal_partitions()[101],
        store_oof=True,
        observation_ids=observation_ids,
    )


def external_literal_fixture():
    """Return the frozen three-repeat Task 5 external fixture."""
    frame, kwargs = tiny_inputs(3)
    kwargs["g1"][1, 0] = 4.0
    kwargs["g1"][2, 0] = 6.0
    return frame, OOFPredictions.from_arrays(**kwargs)


def external_estimator(frame, **kwargs):
    """Build an IRM estimator whose nuisance learners must remain unused."""
    options = {
        "ml_g": NoFitRegressor(),
        "ml_m": NoFitClassifier(),
        "n_folds": 2,
        "n_rep": 3,
    }
    options.update(kwargs)
    return DoubleMLIRM(frame, y="y", treat="d", covariates=["x"], **options)


def corrupt_prediction_snapshot(predictions, field):
    """Create one stale-hash in-memory corruption using ``object`` access."""
    from statspai.dml import _oof_validation as validation

    if field == "array":
        changed = predictions.g0.copy()
        changed[0, 0] += 1.0
        object.__setattr__(predictions, "_g0", validation.snapshot_array(changed))
    elif field == "header":
        changed = predictions.d.astype(np.float64)
        object.__setattr__(predictions, "_d", validation.snapshot_array(changed))
    elif field == "source":
        changed = dict(predictions.source)
        changed["recipe"] = "corrupted after construction"
        object.__setattr__(predictions, "source", changed)
    else:
        changed = dict(predictions.hashes)
        changed["data"] = "0" * (64 if field == "digest" else 63)
        object.__setattr__(predictions, "hashes", changed)


def corrupt_bundle_snapshot(bundle, field):
    """Corrupt one live bundle field without updating its declared hashes."""
    from statspai.dml import _oof_validation as validation

    if field == "nested":
        changed = bundle.predictions.g0.copy()
        changed[0, 0] += 1.0
        target, name = bundle.predictions, "_g0"
    elif field == "nested_header":
        changed = bundle.predictions.d.astype(np.float64)
        target, name = bundle.predictions, "_d"
    elif field == "whole":
        changed = bundle.psi.copy()
        changed[0, 0] += 1.0
        target, name = bundle, "_psi"
    else:
        object.__setattr__(bundle, "hash", "0" * 64)
        return
    object.__setattr__(target, name, validation.snapshot_array(changed))
