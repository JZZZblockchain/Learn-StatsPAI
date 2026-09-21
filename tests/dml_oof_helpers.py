"""Small hand-checked fixtures for the DML OOF contract tests."""

from __future__ import annotations

import numpy as np
import pandas as pd

from statspai import OOFBundle, OOFPredictions


def _training_records(ids, d, fold_ids, *, origin="caller_declared"):
    """Describe exact outer-fold training scopes for a small fixture."""
    records = []
    ids = list(ids)
    d_by_id = dict(zip(ids, np.asarray(d).tolist()))
    for rep, labels in enumerate(np.asarray(fold_ids)):
        for fold_id in sorted(set(labels.tolist())):
            test = [row_id for row_id, label in zip(ids, labels) if label == fold_id]
            train = [row_id for row_id, label in zip(ids, labels) if label != fold_id]
            nuisance = {
                "g0": [row_id for row_id in train if d_by_id[row_id] == 0],
                "g1": [row_id for row_id in train if d_by_id[row_id] == 1],
                "ps": list(train),
            }
            records.append(
                {
                    "rep": rep,
                    "fold_id": int(fold_id),
                    "train_ids": train,
                    "test_ids": test,
                    "nuisance_train_ids": nuisance,
                    "preprocessing_train_ids": {
                        name: list(rows) for name, rows in nuisance.items()
                    },
                    "origin": origin,
                }
            )
    return records


def tiny_inputs(n_rep=1):
    """Return a four-row binary-treatment fixture and constructor kwargs."""
    ids = ["a", "b", "c", "d"]
    df = pd.DataFrame({"y": [1.0, 4.0, 3.0, 6.0], "d": [0, 1, 0, 1], "x": [0, 1, 2, 3]})
    fold_ids = np.tile([0, 0, 1, 1], (n_rep, 1))
    kwargs = {
        "ids": ids,
        "y": df.y.to_numpy(copy=True),
        "d": df.d.to_numpy(copy=True),
        "x": df[["x"]].to_numpy(copy=True),
        "covariate_names": ["x"],
        "g0": np.ones((n_rep, 4)),
        "g1": np.full((n_rep, 4), 3.0),
        "ps_raw": np.full((n_rep, 4), 0.5),
        "fold_ids": fold_ids,
        "training_records": _training_records(ids, df.d.to_numpy(), fold_ids),
        "source": {
            "engine": "hand_fixture",
            "recipe": "fixed arrays",
            "seed": None,
            "software_versions": {"fixture": "1"},
        },
    }
    return df, kwargs


def tiny_bundle(n_rep=1):
    """Return the fixture data and its validated OOF predictions."""
    df, kwargs = tiny_inputs(n_rep)
    return df, OOFPredictions.from_arrays(**kwargs)


def bundle_metadata(predictions, *, scoring_engine="statspai_irm_external_predictions"):
    """Build the complete audit metadata required by schema version 1."""
    is_internal = scoring_engine == "statspai_irm_internal"
    fit_records = []
    for record in predictions.training_records:
        fit_records.append(
            {
                "rep": record["rep"],
                "fold_id": record["fold_id"],
                "fit_seed": 42 + record["rep"] if is_internal else None,
                "subgroup_fallback_counts": {"g0": 0, "g1": 0} if is_internal else None,
            }
        )
    return {
        "scoring_engine": scoring_engine,
        "score": "ATE",
        "psi_a": -1.0,
        "variance_policy": "ddof0",
        "trimming_threshold": 0.01,
        "normalize_ipw": False,
        "clipping_counts": [
            {"rep": rep, "n_clipped_low": 0, "n_clipped_high": 0}
            for rep in range(predictions.n_rep)
        ],
        "fit_records": fit_records,
    }


def tiny_scored_bundle(n_rep=1):
    """Return a complete scored bundle for serialization tests."""
    df, predictions = tiny_bundle(n_rep)
    shape = (n_rep, len(df))
    psi_b = np.tile([2.0, 4.0, -2.0, 8.0], (n_rep, 1))
    psi = psi_b - psi_b.mean(axis=1, keepdims=True)
    bundle = OOFBundle.from_arrays(
        predictions=predictions,
        ps_used=np.full(shape, 0.5),
        psi_b=psi_b,
        psi=psi,
        theta=np.full(n_rep, 3.0),
        se=np.full(n_rep, np.sqrt(3.25)),
        input_positions=np.arange(len(df)),
        dropped_positions=np.array([], dtype=int),
        aggregation={
            "rule": "median_theta_median_variance_plus_split_deviation",
            "theta": 3.0,
            "se": float(np.sqrt(3.25)),
        },
        metadata=bundle_metadata(predictions),
    )
    return df, bundle


def permuted_inputs(kwargs, order):
    """Return a coherently row-permuted constructor payload."""
    order = np.asarray(order, dtype=int)
    result = {
        "ids": [kwargs["ids"][i] for i in order],
        "y": np.asarray(kwargs["y"])[order],
        "d": np.asarray(kwargs["d"])[order],
        "x": np.asarray(kwargs["x"])[order],
        "covariate_names": list(kwargs["covariate_names"]),
        "g0": np.asarray(kwargs["g0"])[:, order],
        "g1": np.asarray(kwargs["g1"])[:, order],
        "ps_raw": np.asarray(kwargs["ps_raw"])[:, order],
        "fold_ids": np.asarray(kwargs["fold_ids"])[:, order],
        "source": dict(kwargs["source"]),
    }
    result["training_records"] = _training_records(
        result["ids"], result["d"], result["fold_ids"]
    )
    return result
