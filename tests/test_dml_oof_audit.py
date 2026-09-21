"""Focused audit, compatibility, and parity evidence for retained IRM OOF data."""

from __future__ import annotations

import importlib
import math

import numpy as np
import pytest
from sklearn.pipeline import Pipeline

from statspai import OOFPredictions
from statspai.dml.double_ml import DoubleML
from statspai.dml.double_ml import dml as library_dml
from statspai.dml.irm import DoubleMLIRM

from .dml_oof_export_helpers import (
    AuditScaler,
    NoFitClassifier,
    NoFitRegressor,
    TrainingMeanRegressor,
    TrainingRateClassifier,
    corrupt_prediction_snapshot,
    external_estimator,
    external_literal_fixture,
    internal_literal_frame,
    internal_partitions,
)
from .dml_oof_helpers import tiny_inputs, tiny_scored_bundle

AUDIT_FIELDS = (
    "rep",
    "status",
    "failure_reason",
    "n_obs",
    "top_fraction",
    "top_count",
    "cmax",
    "z_c",
    "top_share",
    "h",
    "effective_score_count",
)


def test_bundle_score_concentration_has_hand_checked_values_and_stable_fields():
    """Changing any concentration formula or output name breaks this literal fixture."""
    _, bundle = tiny_scored_bundle(n_rep=2)

    records = bundle.score_concentration(top_fraction=0.5)

    assert len(records) == 2
    row = records[0]
    assert tuple(row) == AUDIT_FIELDS
    assert row["rep"] == 0
    assert row["status"] == "ok"
    assert row["failure_reason"] is None
    assert row["n_obs"] == 4
    assert row["top_fraction"] == 0.5
    assert row["top_count"] == 2
    assert row["cmax"] == pytest.approx(25.0 / 52.0)
    assert row["z_c"] == pytest.approx(4.0 * (25.0 / 52.0) / (2.0 * math.log(4.0)))
    assert row["top_share"] == pytest.approx(25.0 / 26.0)
    assert row["h"] == pytest.approx(313.0 / 676.0)
    assert row["effective_score_count"] == pytest.approx(676.0 / 313.0)
    assert records[1] == {**row, "rep": 1}


def test_score_concentration_is_scale_and_permutation_invariant():
    """Row order and nonzero score units cannot alter squared-share diagnostics."""
    from statspai.dml._score_concentration import score_concentration

    psi = np.array([[-1.0, 1.0, -5.0, 5.0]])
    baseline = score_concentration(psi, top_fraction=0.5)[0]
    transformed = score_concentration(-7.0 * psi[:, [2, 0, 3, 1]], top_fraction=0.5)[0]

    for name in ("cmax", "z_c", "top_share", "h", "effective_score_count"):
        assert transformed[name] == pytest.approx(baseline[name])


@pytest.mark.parametrize(
    ("psi", "reason"),
    [
        (np.array([[0.0, 0.0, 0.0, 0.0]]), "zero_score_mass"),
        (np.array([[0.0, np.nan, 1.0, -1.0]]), "nonfinite_score"),
        (
            np.array([[np.finfo(float).max, -np.finfo(float).max, 1.0, -1.0]]),
            "nonfinite_score_mass",
        ),
    ],
)
def test_score_concentration_returns_explicit_unavailable_states(psi, reason):
    """Undefined diagnostics remain failures instead of becoming silent no-alarms."""
    from statspai.dml._score_concentration import score_concentration

    row = score_concentration(psi)[0]

    assert tuple(row) == AUDIT_FIELDS
    assert row["status"] == "diagnostic_unavailable"
    assert row["failure_reason"] == reason
    for name in ("cmax", "z_c", "top_share", "h", "effective_score_count"):
        assert row[name] is None


def test_legacy_internal_oof_bundle_preserves_rows_folds_training_scope_and_hash(
    tmp_path,
):
    """The legacy façade retains the observed internal fit and its exact partition."""
    frame = internal_literal_frame()
    ids = [f"unit:{position}" for position in range(len(frame))]
    folds = internal_partitions()[101]
    estimator = DoubleML(
        frame,
        "y",
        "d",
        ["x1", "x2"],
        "irm",
        ml_g=Pipeline([("audit", AuditScaler()), ("mean", TrainingMeanRegressor())]),
        ml_m=Pipeline([("audit", AuditScaler()), ("rate", TrainingRateClassifier())]),
        n_folds=2,
        fold_indices=folds,
    )

    bundle = estimator.fit(store_oof=True, observation_ids=ids).get_oof()

    assert bundle.predictions.n_obs == len(frame)
    assert len(bundle.to_frame()) == len(frame)
    np.testing.assert_array_equal(bundle.predictions.fold_ids[0], folds)
    for record in bundle.predictions.training_records:
        expected_test = tuple(
            ids[position] for position in np.flatnonzero(folds == record["fold_id"])
        )
        expected_train = tuple(row_id for row_id in ids if row_id not in expected_test)
        assert record["origin"] == "statspai_internal"
        assert record["test_ids"] == expected_test
        assert record["train_ids"] == expected_train
        assert set(record["nuisance_train_ids"]["ps"]) == set(expected_train)
        assert not set(record["test_ids"]) & set(record["train_ids"])
    path = tmp_path / "internal-oof.json"
    bundle.to_json(path)
    restored = type(bundle).from_json(path)
    assert restored.hash == bundle.hash
    assert dict(restored.predictions.hashes) == dict(bundle.predictions.hashes)


def test_external_oof_bundle_preserves_contract_and_never_falls_back(monkeypatch):
    """External scoring keeps caller provenance and cannot enter internal fitting."""
    frame, predictions = external_literal_fixture()

    def forbidden(*_args, **_kwargs):
        raise AssertionError("external OOF scoring reached an internal fallback")

    base_module = importlib.import_module("statspai.dml._base")
    monkeypatch.setattr(base_module._DoubleMLBase, "_make_splits", forbidden)
    monkeypatch.setattr(DoubleMLIRM, "_fit_one_rep", forbidden)

    bundle = (
        external_estimator(frame)
        .fit(
            external_predictions=predictions,
            store_oof=True,
            observation_ids=predictions.ids,
        )
        .get_oof()
    )

    assert bundle.predictions.n_obs == len(frame)
    assert len(bundle.to_frame()) == predictions.n_rep * len(frame)
    np.testing.assert_array_equal(bundle.predictions.fold_ids, predictions.fold_ids)
    assert bundle.predictions.training_records == predictions.training_records
    assert dict(bundle.predictions.hashes) == dict(predictions.hashes)
    assert bundle.metadata["scoring_engine"] == "statspai_irm_external_predictions"
    assert {record["origin"] for record in bundle.predictions.training_records} == {
        "caller_declared"
    }
    assert all(
        record["subgroup_fallback_counts"] is None
        for record in bundle.metadata["fit_records"]
    )


def test_unretained_external_scoring_rejects_live_mutation_under_stale_hashes(
    monkeypatch,
):
    """Every external path verifies current arrays before scoring or fallback work."""
    frame, predictions = external_literal_fixture()
    corrupt_prediction_snapshot(predictions, "array")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("invalid external OOF input reached scoring or fallback")

    base_module = importlib.import_module("statspai.dml._base")
    irm_module = importlib.import_module("statspai.dml.irm")
    monkeypatch.setattr(base_module._DoubleMLBase, "_make_splits", forbidden)
    monkeypatch.setattr(DoubleMLIRM, "_fit_one_rep", forbidden)
    monkeypatch.setattr(irm_module, "score_binary_ate", forbidden)

    with pytest.raises(ValueError, match="OOF prediction hash mismatch"):
        external_estimator(frame).fit(
            external_predictions=predictions,
            store_oof=False,
            observation_ids=predictions.ids,
        )


def test_functional_external_scoring_rejects_invalid_prediction_type_stably():
    """Functional provenance handling must not mask the public input TypeError."""
    frame, _ = external_literal_fixture()

    with pytest.raises(
        TypeError,
        match="^external_predictions must be an in-memory OOFPredictions instance$",
    ):
        library_dml(
            frame,
            "y",
            "d",
            ["x"],
            model="irm",
            n_folds=2,
            external_predictions={},
        )


def _parity_fixture():
    frame, kwargs = tiny_inputs()
    kwargs["g0"] = np.array([[0.5, 1.0, 2.0, 1.0]])
    kwargs["g1"] = np.array([[2.0, 3.0, 4.0, 5.0]])
    kwargs["ps_raw"] = np.array([[0.0, 1.0, 0.25, 0.75]])
    return frame, OOFPredictions.from_arrays(**kwargs)


def test_external_bundle_matches_transparent_aipw_formula_row_by_row():
    """A hand-written AIPW expression anchors psi_b, theta, and ddof-0 SE."""
    frame, predictions = _parity_fixture()

    bundle = (
        external_estimator(frame, n_rep=1, trimming_threshold=0.1)
        .fit(
            external_predictions=predictions,
            store_oof=True,
            observation_ids=predictions.ids,
        )
        .get_oof()
    )

    y = frame["y"].to_numpy()
    d = frame["d"].to_numpy()
    g0, g1 = predictions.g0[0], predictions.g1[0]
    ps = np.array([0.1, 0.9, 0.25, 0.75])
    expected_psi_b = g1 - g0 + d * (y - g1) / ps - (1.0 - d) * (y - g0) / (1.0 - ps)
    expected_theta = float(sum(expected_psi_b) / 4.0)
    centered = expected_psi_b - expected_theta
    expected_se = math.sqrt(float(sum(centered**2)) / 4.0) / 2.0

    np.testing.assert_allclose(bundle.psi_b[0], expected_psi_b, rtol=0, atol=1e-14)
    np.testing.assert_allclose(bundle.psi[0], centered, rtol=0, atol=1e-14)
    assert bundle.theta[0] == pytest.approx(expected_theta, abs=1e-14)
    assert bundle.se[0] == pytest.approx(expected_se, abs=1e-14)


def test_external_bundle_matches_independent_doubleml_style_moment_calculation():
    """The DoubleML linear-score convention independently reproduces theta and SE."""
    doubleml = pytest.importorskip("doubleml")
    from doubleml.utils import DMLDummyClassifier, DMLDummyRegressor, PSProcessorConfig

    frame, predictions = _parity_fixture()
    bundle = (
        external_estimator(frame, n_rep=1, trimming_threshold=0.1)
        .fit(
            external_predictions=predictions,
            store_oof=True,
            observation_ids=predictions.ids,
        )
        .get_oof()
    )

    y = frame["y"].to_numpy()
    d = frame["d"].to_numpy()
    ps = np.maximum(0.1, np.minimum(0.9, predictions.ps_raw[0]))
    ml_g0, ml_g1 = predictions.g0[0], predictions.g1[0]
    psi_b_reference = (
        ml_g1 - ml_g0 + d * (y - ml_g1) / ps - (1.0 - d) * (y - ml_g0) / (1.0 - ps)
    )
    psi_a_reference = -np.ones(len(frame))
    theta_reference = -float(np.mean(psi_b_reference)) / float(np.mean(psi_a_reference))
    moment = psi_a_reference * theta_reference + psi_b_reference
    se_reference = math.sqrt(
        float(np.mean(moment**2)) / (float(np.mean(psi_a_reference)) ** 2 * len(frame))
    )

    reference_data = doubleml.DoubleMLData.from_arrays(
        x=frame[["x"]].to_numpy(),
        y=y,
        d=d,
    )
    reference = doubleml.DoubleMLIRM(
        reference_data,
        ml_g=DMLDummyRegressor(),
        ml_m=DMLDummyClassifier(),
        n_folds=2,
        n_rep=1,
        ps_processor_config=PSProcessorConfig(clipping_threshold=0.1),
    )
    external = {
        "d": {
            "ml_g0": ml_g0[:, None],
            "ml_g1": ml_g1[:, None],
            "ml_m": predictions.ps_raw[0][:, None],
        }
    }
    with pytest.warns(UserWarning, match="close to zero or one"):
        reference.fit(external_predictions=external)

    np.testing.assert_allclose(bundle.psi_b[0], psi_b_reference, rtol=0, atol=1e-14)
    np.testing.assert_allclose(bundle.psi[0], moment, rtol=0, atol=1e-14)
    assert bundle.theta[0] == pytest.approx(theta_reference, abs=1e-14)
    assert bundle.se[0] == pytest.approx(se_reference, abs=1e-14)
    np.testing.assert_allclose(
        bundle.psi_b[0], reference.psi_elements["psi_b"][:, 0, 0], rtol=0, atol=1e-14
    )
    np.testing.assert_allclose(
        bundle.psi[0], reference.psi[:, 0, 0], rtol=0, atol=1e-14
    )
    assert bundle.theta[0] == pytest.approx(float(reference.coef[0]), abs=1e-14)
    assert bundle.se[0] == pytest.approx(float(reference.se[0]), abs=1e-14)
