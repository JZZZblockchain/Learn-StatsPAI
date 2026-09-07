"""Public complete repeated-crossfit OOF retention contracts."""

from __future__ import annotations

import importlib
import json
import typing

import numpy as np
import pandas as pd
import pytest
import sklearn
import statspai

from statspai import CausalResult, OOFBundle
from statspai.agent.tools._helpers import _default_serializer
from statspai.dml._oof_result import clone_bundle
from statspai.dml.irm import DoubleMLIRM

from .dml_oof_export_helpers import (
    AuditScaler,
    TrainingMeanRegressor,
    TrainingRateClassifier,
    corrupt_bundle_snapshot,
    corrupt_prediction_snapshot,
    external_estimator,
    external_literal_fixture,
    internal_estimator,
    internal_literal_frame,
    internal_mapping_frame,
    internal_partitions,
    partition_splits,
    reset_internal_audits,
)

EXPECTED_PSI_B = np.array(
    [
        [2.0, 4.0, -2.0, 8.0],
        [3.0, 4.0, -2.0, 8.0],
        [5.0, 4.0, -2.0, 8.0],
    ]
)
EXPECTED_THETA = np.array([3.0, 3.25, 3.75])
EXPECTED_PSI = np.array(
    [
        [-1.0, 1.0, -5.0, 5.0],
        [-0.25, 0.75, -5.25, 4.75],
        [1.25, 0.25, -5.75, 4.25],
    ]
)
EXPECTED_SE = np.array(
    [
        float.fromhex("0x1.cd82b446159f3p+0"),
        float.fromhex("0x1.c7ee08a0e6d4cp+0"),
        float.fromhex("0x1.d0d3ac685eda4p+0"),
    ]
)
EXPECTED_AGGREGATE = (3.25, float.fromhex("0x1.d1ed52076fbe9p+0"))


def _expected_frame():
    return pd.DataFrame(
        {
            "rep": pd.Series([0] * 4 + [1] * 4 + [2] * 4, dtype="int64"),
            "row_id": pd.Series(["a", "b", "c", "d"] * 3, dtype="object"),
            "input_position": pd.Series([0, 1, 2, 3] * 3, dtype="int64"),
            "fold_id": pd.Series([0, 0, 1, 1] * 3, dtype="int64"),
            "training_origin": pd.Series(["caller_declared"] * 12, dtype="object"),
            "y": pd.Series([1.0, 4.0, 3.0, 6.0] * 3, dtype="float64"),
            "d": pd.Series([0, 1, 0, 1] * 3, dtype="int64"),
            "g0": pd.Series([1.0] * 12, dtype="float64"),
            "g1": pd.Series(
                [3.0] * 4 + [4.0, 3.0, 3.0, 3.0] + [6.0, 3.0, 3.0, 3.0],
                dtype="float64",
            ),
            "ps_raw": pd.Series([0.5] * 12, dtype="float64"),
            "ps_used": pd.Series([0.5] * 12, dtype="float64"),
            "psi_b": pd.Series(EXPECTED_PSI_B.reshape(-1), dtype="float64"),
            "psi": pd.Series(EXPECTED_PSI.reshape(-1), dtype="float64"),
        }
    )


def _fit_external_literal():
    frame, predictions = external_literal_fixture()
    result = external_estimator(frame).fit(
        external_predictions=predictions,
        store_oof=True,
        observation_ids=predictions.ids,
    )
    return predictions, result


def test_external_store_retains_all_literal_repeats_and_scorer_outputs(monkeypatch):
    frame, predictions = external_literal_fixture()
    irm_module = importlib.import_module("statspai.dml.irm")
    real_score = irm_module.score_binary_ate
    captures = []

    def score_spy(**kwargs):
        inputs = {name: np.array(value, copy=True) for name, value in kwargs.items()}
        score = real_score(**kwargs)
        captures.append((inputs, score))
        return score

    monkeypatch.setattr(irm_module, "score_binary_ate", score_spy)
    result = external_estimator(frame).fit(
        external_predictions=predictions,
        store_oof=True,
        observation_ids=predictions.ids,
    )
    bundle = result.get_oof()

    assert isinstance(bundle, OOFBundle)
    assert (result.estimate, result.se) == EXPECTED_AGGREGATE
    np.testing.assert_array_equal(bundle.psi_b, EXPECTED_PSI_B)
    np.testing.assert_array_equal(bundle.psi, EXPECTED_PSI)
    np.testing.assert_array_equal(bundle.theta, EXPECTED_THETA)
    np.testing.assert_array_equal(bundle.se, EXPECTED_SE)
    assert len(captures) == 3
    for rep, (inputs, score) in enumerate(captures):
        np.testing.assert_array_equal(bundle.predictions.g0[rep], inputs["g0"])
        np.testing.assert_array_equal(bundle.predictions.g1[rep], inputs["g1"])
        np.testing.assert_array_equal(bundle.predictions.ps_raw[rep], inputs["ps_raw"])
        np.testing.assert_array_equal(bundle.ps_used[rep], score.ps_used)
        np.testing.assert_array_equal(bundle.psi_b[rep], score.psi_b)
        np.testing.assert_array_equal(bundle.psi[rep], score.psi)
        assert bundle.theta[rep] == score.theta
        assert bundle.se[rep] == score.se
    assert bundle.predictions.source == predictions.source
    assert bundle.predictions.training_records == predictions.training_records
    assert dict(bundle.predictions.hashes) == dict(predictions.hashes)
    assert all(
        row["fit_seed"] is None and row["subgroup_fallback_counts"] is None
        for row in bundle.metadata["fit_records"]
    )


def test_external_store_to_frame_matches_complete_literal_golden():
    _, result = _fit_external_literal()
    pd.testing.assert_frame_equal(
        result.get_oof().to_frame(),
        _expected_frame(),
        check_dtype=True,
        check_like=False,
    )


@pytest.mark.parametrize("field", ["array", "header", "source", "digest", "malformed"])
def test_external_store_rejects_stale_hash_before_score_split_or_attach(
    monkeypatch, field
):
    frame, predictions = external_literal_fixture()
    corrupt_prediction_snapshot(predictions, field)
    base_module = importlib.import_module("statspai.dml._base")
    irm_module = importlib.import_module("statspai.dml.irm")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("stale external OOF record reached work")

    monkeypatch.setattr(irm_module, "score_binary_ate", forbidden)
    monkeypatch.setattr(DoubleMLIRM, "_make_splits", forbidden)
    monkeypatch.setattr(base_module, "_attach_result_oof", forbidden, raising=False)
    with pytest.raises(ValueError, match="hash"):
        external_estimator(frame).fit(
            external_predictions=predictions,
            store_oof=True,
            observation_ids=predictions.ids,
        )


def test_causal_result_getter_type_hints_and_unstored_error_contract():
    hints = typing.get_type_hints(CausalResult.get_oof)
    assert hints["return"] is typing.Any
    result = CausalResult("fixture", "ATE", 0.0, 1.0, 1.0, (-1.0, 1.0), 0.05, 1)
    message = (
        "OOF records are unavailable; refit a supported model='irm' ATE "
        "call with store_oof=True"
    )
    with pytest.raises(ValueError, match=f"^{message}$"):
        result.get_oof()
    with pytest.raises(ValueError, match=f"^{message}$"):
        result.get_residuals()


def test_external_unstored_result_getters_raise_same_error():
    frame, predictions = external_literal_fixture()
    result = external_estimator(frame).fit(
        external_predictions=predictions, observation_ids=predictions.ids
    )
    for getter in (result.get_oof, result.get_residuals):
        with pytest.raises(ValueError, match="^OOF records are unavailable;"):
            getter()


class _SecondRepeat:
    def __index__(self):
        return 1


def test_external_getters_clone_and_residual_integer_protocol():
    predictions, result = _fit_external_literal()
    first = result.get_oof()
    second = result.get_oof()
    assert first is not second
    assert first.predictions is not second.predictions
    assert first.hash == second.hash
    assert dict(first.predictions.hashes) == dict(second.predictions.hashes)
    expected = pd.DataFrame(
        {
            "rep": pd.Series([1] * 4, dtype="int64"),
            "row_id": pd.Series(predictions.ids, dtype="object"),
            "input_position": pd.Series([0, 1, 2, 3], dtype="int64"),
            "fold_id": pd.Series([0, 0, 1, 1], dtype="int64"),
            "training_origin": pd.Series(["caller_declared"] * 4, dtype="object"),
            "psi": pd.Series(EXPECTED_PSI[1], dtype="float64"),
            "y_minus_gd": pd.Series([0.0, 1.0, 2.0, 3.0], dtype="float64"),
            "d_minus_ps_raw": pd.Series([-0.5, 0.5, -0.5, 0.5], dtype="float64"),
        }
    )
    for rep in (1, np.int64(1), _SecondRepeat()):
        pd.testing.assert_frame_equal(result.get_residuals(rep), expected)
    all_rows = result.get_residuals()
    assert list(all_rows.columns) == list(expected.columns)
    assert len(all_rows) == 12
    assert list(all_rows["rep"]) == [0] * 4 + [1] * 4 + [2] * 4


@pytest.mark.parametrize("rep", [True, np.bool_(True), 1.0, "1"])
def test_residual_selector_rejects_non_integer_protocol_values(rep):
    _, result = _fit_external_literal()
    with pytest.raises(TypeError, match="^rep must be an integer or None$"):
        result.get_residuals(rep)


@pytest.mark.parametrize("rep", [-1, 3])
def test_residual_selector_rejects_out_of_range_values(rep):
    _, result = _fit_external_literal()
    with pytest.raises(IndexError, match="^rep is outside the stored repeat range$"):
        result.get_residuals(rep)


@pytest.mark.parametrize("caller_ids", [False, True])
def test_internal_mapping_uses_original_ordinals_with_duplicate_index(caller_ids):
    frame = internal_mapping_frame()
    frame["unused"] = 1.0
    frame.iloc[5, frame.columns.get_loc("unused")] = np.nan
    supplied = tuple(f"case:{position}" for position in range(41))
    kwargs = {"observation_ids": supplied} if caller_ids else {}
    result = internal_estimator(frame, fold_indices="fold").fit(
        store_oof=True, **kwargs
    )
    bundle = result.get_oof()
    assert tuple(bundle.input_positions) == tuple(range(1, 41))
    assert tuple(bundle.dropped_positions) == (0,)
    expected_ids = (
        supplied[1:] if caller_ids else tuple(f"row:{i}" for i in range(1, 41))
    )
    assert bundle.predictions.ids == expected_ids
    np.testing.assert_array_equal(bundle.predictions.y, frame["y"].to_numpy()[1:])
    np.testing.assert_array_equal(bundle.predictions.d, frame["d"].to_numpy()[1:])
    np.testing.assert_array_equal(bundle.predictions.x[:, 0], frame["x"].to_numpy()[1:])
    np.testing.assert_array_equal(
        bundle.predictions.fold_ids[0], frame["fold"].to_numpy()[1:]
    )


@pytest.mark.parametrize(
    ("observation_ids", "error"),
    [
        ("case", TypeError),
        ([f"case:{i}" for i in range(40)], ValueError),
        (["duplicate"] * 41, ValueError),
        ([""] + [f"case:{i}" for i in range(1, 41)], ValueError),
        ([0] + [f"case:{i}" for i in range(1, 41)], ValueError),
    ],
)
def test_internal_mapping_rejects_invalid_ids_before_fit(
    monkeypatch, observation_ids, error
):
    def forbidden(*_args, **_kwargs):
        raise AssertionError("invalid observation IDs reached learner fitting")

    monkeypatch.setattr(DoubleMLIRM, "_fit_weighted", forbidden)
    with pytest.raises(error):
        internal_estimator(internal_mapping_frame(), fold_indices="fold").fit(
            store_oof=True, observation_ids=observation_ids
        )


def test_internal_three_repeats_capture_exact_splits_scores_and_fit_scopes(
    monkeypatch, tmp_path
):
    frame = internal_literal_frame()
    ids = tuple(f"unit:{position}" for position in range(len(frame)))
    partitions = internal_partitions()
    calls_by_seed = {}
    scorer_calls = []
    irm_module = importlib.import_module("statspai.dml.irm")
    real_score = irm_module.score_binary_ate

    def split_spy(_x, *, rng_seed, fold_indices=None, stratify=None):
        assert fold_indices is None
        assert stratify is not None
        calls_by_seed[rng_seed] = calls_by_seed.get(rng_seed, 0) + 1
        if calls_by_seed[rng_seed] != 1:
            raise AssertionError("split seed was used more than once")
        return partition_splits(partitions[rng_seed])

    def score_spy(**kwargs):
        inputs = {name: np.array(value, copy=True) for name, value in kwargs.items()}
        score = real_score(**kwargs)
        scorer_calls.append((inputs, score))
        return score

    reset_internal_audits()
    estimator = internal_estimator(frame, n_rep=3)
    monkeypatch.setattr(estimator, "_make_splits", split_spy)
    monkeypatch.setattr(irm_module, "score_binary_ate", score_spy)
    result = estimator.fit(store_oof=True, observation_ids=ids)
    bundle = result.get_oof()

    assert calls_by_seed == {101: 1, 102: 1, 103: 1}
    assert len(scorer_calls) == 3
    np.testing.assert_array_equal(
        bundle.predictions.fold_ids, list(partitions.values())
    )
    assert len({tuple(row) for row in bundle.predictions.fold_ids}) == 3
    expected_g, expected_m, expected_audit = [], [], []
    records = list(bundle.predictions.training_records)
    for rep, (seed, labels) in enumerate(partitions.items()):
        for fold in range(2):
            train = np.flatnonzero(labels != fold)
            test = np.flatnonzero(labels == fold)
            g0 = tuple(train[frame["d"].to_numpy()[train] == 0])
            g1 = tuple(train[frame["d"].to_numpy()[train] == 1])
            record = records[2 * rep + fold]
            assert (record["rep"], record["fold_id"]) == (rep, fold)
            assert record["train_ids"] == tuple(ids[index] for index in train)
            assert record["test_ids"] == tuple(ids[index] for index in test)
            assert record["nuisance_train_ids"] == {
                "g0": tuple(ids[index] for index in g0),
                "g1": tuple(ids[index] for index in g1),
                "ps": tuple(ids[index] for index in train),
            }
            assert record["preprocessing_train_ids"] == record["nuisance_train_ids"]
            expected_g.extend((g1, g0))
            expected_m.append(tuple(train))
            expected_audit.extend((g1, g0, tuple(train)))
            fit = bundle.metadata["fit_records"][2 * rep + fold]
            assert fit == {
                "rep": rep,
                "fold_id": fold,
                "fit_seed": seed,
                "subgroup_fallback_counts": {"g0": 0, "g1": 0},
            }
    assert TrainingMeanRegressor.fit_rows == expected_g
    assert TrainingRateClassifier.fit_rows == expected_m
    assert AuditScaler.fit_rows == expected_audit

    for rep, (inputs, score) in enumerate(scorer_calls):
        for name in ("g0", "g1", "ps_raw"):
            np.testing.assert_array_equal(
                getattr(bundle.predictions, name)[rep], inputs[name]
            )
        for name in ("ps_used", "psi_b", "psi"):
            np.testing.assert_array_equal(
                getattr(bundle, name)[rep], getattr(score, name)
            )
        assert bundle.theta[rep] == score.theta
        assert bundle.se[rep] == score.se
    np.testing.assert_array_equal(bundle.theta, result.model_info["theta_all_reps"])
    np.testing.assert_array_equal(bundle.se, result.model_info["se_all_reps"])
    assert (result.estimate, result.se) == (
        bundle.aggregation["theta"],
        bundle.aggregation["se"],
    )
    np.testing.assert_array_equal(result.model_info["_y_resid"], bundle.psi[-1])
    np.testing.assert_array_equal(
        result.model_info["_pscore"], bundle.predictions.ps_raw[-1]
    )
    assert bundle.predictions.source == {
        "engine": "statspai_irm_internal",
        "recipe": (
            "StatsPAI-observed outer-fold scopes; observation_ids_source="
            "caller_provided; fit_seed is random_state + rep for split/call "
            "provenance and does not override learner randomness"
        ),
        "seed": 101,
        "software_versions": {
            "statspai": str(statspai.__version__),
            "numpy": str(np.__version__),
            "scikit-learn": str(sklearn.__version__),
        },
    }
    assert bundle.metadata["clipping_counts"] == tuple(
        {"rep": rep, "n_clipped_low": 0, "n_clipped_high": 0} for rep in range(3)
    )
    path = tmp_path / "internal-oof.json"
    bundle.to_json(path)
    restored = OOFBundle.from_json(path)
    assert restored.hash == bundle.hash
    pd.testing.assert_frame_equal(restored.to_frame(), bundle.to_frame())


def _fit_fixed_internal(frame):
    reset_internal_audits()
    labels = internal_partitions()[101]
    result = internal_estimator(frame, fold_indices=labels).fit(store_oof=True)
    return result.get_oof(), [value.copy() for value in AuditScaler.fit_means]


def test_internal_held_out_outcome_does_not_enter_nuisance_training():
    frame = internal_literal_frame()
    baseline, _ = _fit_fixed_internal(frame)
    changed = frame.copy()
    changed.loc[0, "y"] += 100.0
    perturbed, _ = _fit_fixed_internal(changed)
    labels = internal_partitions()[101]
    held_out = labels == 0
    for name in ("g0", "g1", "ps_raw"):
        np.testing.assert_array_equal(
            getattr(baseline.predictions, name)[0, held_out],
            getattr(perturbed.predictions, name)[0, held_out],
        )
    assert not np.array_equal(
        baseline.predictions.g0[0, ~held_out], perturbed.predictions.g0[0, ~held_out]
    )


def test_internal_held_out_covariate_does_not_enter_fold_preprocessing():
    frame = internal_literal_frame()
    _, baseline_means = _fit_fixed_internal(frame)
    changed = frame.copy()
    changed.loc[0, "x1"] += 1000.0
    _, perturbed_means = _fit_fixed_internal(changed)
    for before, after in zip(baseline_means[:3], perturbed_means[:3]):
        np.testing.assert_array_equal(before, after)
    assert any(
        not np.array_equal(before, after)
        for before, after in zip(baseline_means[3:], perturbed_means[3:])
    )


@pytest.mark.parametrize("field", ["nested", "nested_header", "whole", "declared"])
def test_clone_and_stored_getters_fail_closed_on_live_corruption(field):
    _, result = _fit_external_literal()
    healthy = result.get_oof()
    control = clone_bundle(healthy)
    assert control.hash == healthy.hash
    assert dict(control.predictions.hashes) == dict(healthy.predictions.hashes)
    corrupt_bundle_snapshot(healthy, field)
    with pytest.raises(ValueError):
        clone_bundle(healthy)

    _, stored_result = _fit_external_literal()
    corrupt_bundle_snapshot(stored_result.__dict__["_dml_oof_bundle"], field)
    for getter in (stored_result.get_oof, stored_result.get_residuals):
        with pytest.raises(ValueError):
            getter()


def test_snapshots_resist_caller_object_header_and_frame_mutation():
    caller, result = _fit_external_literal()
    stored = result.__dict__["_dml_oof_bundle"]
    returned = result.get_oof()
    baseline = returned.to_frame()
    declared = returned.hash, dict(returned.predictions.hashes)
    assert stored is not caller
    assert stored.predictions is not caller
    assert returned is not stored
    assert returned.predictions is not stored.predictions
    assert returned.predictions is not caller

    with pytest.raises(ValueError):
        caller.g0[0, 0] = -99.0
    corrupt_prediction_snapshot(caller, "array")
    header = returned.psi
    with pytest.raises(ValueError):
        header[0, 0] = -99.0
    header.shape = (header.size,)
    header.dtype = np.uint8
    header.strides = (0,)
    with pytest.raises(ValueError):
        header.resize((1,))
    with pytest.raises(ValueError):
        header.setflags(write=True)
    object.__setattr__(returned, "hash", "0" * 64)
    changed_frame = returned.to_frame()
    changed_frame.iloc[0, 0] = 99
    changed_frame.columns = [f"changed_{i}" for i in range(len(changed_frame.columns))]
    changed_frame.index = np.arange(len(changed_frame)) + 10

    fresh = result.get_oof()
    assert (fresh.hash, dict(fresh.predictions.hashes)) == declared
    pd.testing.assert_frame_equal(fresh.to_frame(), baseline)


def test_reused_estimator_cleans_failed_and_successful_capture_state(monkeypatch):
    frame = internal_literal_frame()
    labels = internal_partitions()[101]
    estimator = internal_estimator(frame, fold_indices=labels)
    irm_module = importlib.import_module("statspai.dml.irm")
    real_score = irm_module.score_binary_ate

    def injected_failure(**_kwargs):
        raise RuntimeError("injected scorer failure")

    monkeypatch.setattr(irm_module, "score_binary_ate", injected_failure)
    with pytest.raises(RuntimeError, match="injected scorer failure"):
        estimator.fit(store_oof=True)
    assert "_oof_rep_capture" not in estimator.__dict__

    monkeypatch.setattr(irm_module, "score_binary_ate", real_score)
    stored = estimator.fit(store_oof=True)
    expected_hash = stored.get_oof().hash
    unstored = estimator.fit()
    assert stored.get_oof().hash == expected_hash
    with pytest.raises(ValueError, match="^OOF records are unavailable;"):
        unstored.get_oof()
    assert "_oof_rep_capture" not in estimator.__dict__


def test_real_agent_serializer_and_public_summaries_omit_retained_rows():
    frame = internal_literal_frame()
    secret_ids = tuple(f"private-subject-{i}" for i in range(len(frame)))
    result = internal_estimator(frame, fold_indices=internal_partitions()[101]).fit(
        store_oof=True, observation_ids=secret_ids
    )
    payloads = (result.to_dict(), _default_serializer(result))
    rendered = [json.dumps(payload, sort_keys=True) for payload in payloads]
    rendered.append(result.summary())
    for text in rendered:
        assert not any(identifier in text for identifier in secret_ids)
        assert "_dml_oof_bundle" not in text
        assert '"g0"' not in text and '"g1"' not in text
