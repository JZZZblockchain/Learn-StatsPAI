"""Fit-local OOF collector state-machine and split-preflight contracts."""

from __future__ import annotations

import importlib

import numpy as np
import pytest

from statspai import dml
from statspai.dml._irm_score import score_binary_ate
from statspai.dml._oof_retention import (
    AnalysisIdentity,
    OOFRetention,
    external_analysis_identity,
)
from statspai.dml.irm import DoubleMLIRM
from statspai.exceptions import DataInsufficient, MethodIncompatibility

from .dml_oof_export_helpers import (
    NoFitClassifier,
    NoFitRegressor,
    TrainingMeanRegressor,
    external_estimator,
    external_literal_fixture,
    internal_estimator,
    internal_literal_frame,
    internal_partitions,
    partition_splits,
    reset_internal_audits,
)
from .dml_oof_helpers import tiny_bundle


def _score():
    return score_binary_ate(
        y=[1.0, 4.0, 3.0, 6.0],
        d=[0, 1, 0, 1],
        g0=[1.0] * 4,
        g1=[3.0] * 4,
        ps_raw=[0.5] * 4,
        trimming_threshold=0.01,
    )


def _identity():
    return AnalysisIdentity(
        ids=("a", "b", "c", "d"),
        input_positions=(0, 1, 2, 3),
        dropped_positions=(),
        observation_ids_source="caller_provided",
    )


def _external_collector(n_rep=1):
    _, predictions = tiny_bundle(n_rep)
    identity = external_analysis_identity(
        predictions=predictions,
        n_input=4,
        observation_ids_source="caller_provided",
    )
    return OOFRetention.external(
        predictions=predictions,
        identity=identity,
        n_rep=n_rep,
        n_folds=2,
        trimming_threshold=0.01,
    )


def _internal_collector(n_rep=1):
    return OOFRetention.internal(
        y=np.array([1.0, 4.0, 3.0, 6.0]),
        d=np.array([0, 1, 0, 1]),
        x=np.arange(4, dtype=float)[:, None],
        covariate_names=["x"],
        identity=_identity(),
        n_rep=n_rep,
        n_folds=2,
        random_state=42,
        trimming_threshold=0.01,
    )


def _valid_splits():
    return [
        (np.array([2, 3]), np.array([0, 1])),
        (np.array([0, 1]), np.array([2, 3])),
    ]


def _record_internal(capture):
    score = _score()
    capture.record_internal_splits(_valid_splits(), min_subgroup_fit=1)
    capture.record_internal_score(
        g0=np.ones(4),
        g1=np.full(4, 3.0),
        ps_raw=np.full(4, 0.5),
        score=score,
        fallback_g0=0,
        fallback_g1=0,
    )
    return score


@pytest.mark.parametrize("mode", ["internal", "external"])
def test_collector_valid_control_builds_one_complete_bundle(mode):
    collector = _internal_collector() if mode == "internal" else _external_collector()
    capture = collector.start_rep(0, 42)
    score = _record_internal(capture) if mode == "internal" else _score()
    if mode == "external":
        capture.record_external_score(score)
    collector.finish_rep(capture, score.theta, score.se)
    bundle = collector.build(score.theta, score.se)
    assert bundle.predictions.n_rep == 1
    assert bundle.metadata["scoring_engine"].endswith(
        "internal" if mode == "internal" else "external_predictions"
    )


def test_collector_rejects_out_of_order_duplicate_and_out_of_range_start():
    with pytest.raises(RuntimeError):
        _external_collector(2).start_rep(1, 43)
    collector = _external_collector(2)
    collector.start_rep(0, 42)
    with pytest.raises(RuntimeError):
        collector.start_rep(0, 42)
    with pytest.raises(RuntimeError):
        _external_collector(2).start_rep(-1, 41)
    with pytest.raises(RuntimeError):
        _external_collector(2).start_rep(2, 44)


def test_collector_rejects_incomplete_foreign_and_duplicate_finish():
    collector = _external_collector()
    capture = collector.start_rep(0, 42)
    with pytest.raises(RuntimeError):
        collector.finish_rep(capture, _score().theta, _score().se)

    left, right = _external_collector(), _external_collector()
    foreign = left.start_rep(0, 42)
    right.start_rep(0, 42)
    with pytest.raises(RuntimeError):
        right.finish_rep(foreign, _score().theta, _score().se)

    collector = _external_collector()
    capture = collector.start_rep(0, 42)
    score = _score()
    capture.record_external_score(score)
    collector.finish_rep(capture, score.theta, score.se)
    with pytest.raises(RuntimeError):
        collector.finish_rep(capture, score.theta, score.se)


def test_collector_rejects_early_and_duplicate_build():
    with pytest.raises(RuntimeError):
        _external_collector().build(3.0, 1.0)
    collector = _external_collector()
    capture = collector.start_rep(0, 42)
    score = _score()
    capture.record_external_score(score)
    collector.finish_rep(capture, score.theta, score.se)
    collector.build(score.theta, score.se)
    with pytest.raises(RuntimeError):
        collector.build(score.theta, score.se)


def test_capture_rejects_mixed_mode_out_of_order_and_duplicate_records():
    internal = _internal_collector().start_rep(0, 42)
    external = _external_collector().start_rep(0, 42)
    with pytest.raises(RuntimeError):
        internal.record_external_score(_score())
    with pytest.raises(RuntimeError):
        external.record_internal_splits(_valid_splits(), min_subgroup_fit=1)
    with pytest.raises(RuntimeError):
        external.record_internal_score(
            g0=np.ones(4),
            g1=np.ones(4),
            ps_raw=np.full(4, 0.5),
            score=_score(),
            fallback_g0=0,
            fallback_g1=0,
        )
    with pytest.raises(RuntimeError):
        internal.record_internal_score(
            g0=np.ones(4),
            g1=np.ones(4),
            ps_raw=np.full(4, 0.5),
            score=_score(),
            fallback_g0=0,
            fallback_g1=0,
        )

    internal.record_internal_splits(_valid_splits(), min_subgroup_fit=1)
    with pytest.raises(RuntimeError):
        internal.record_internal_splits(_valid_splits(), min_subgroup_fit=1)
    duplicate_internal = _internal_collector().start_rep(0, 42)
    duplicate_internal.record_internal_splits(_valid_splits(), min_subgroup_fit=1)
    score = _score()
    duplicate_internal.record_internal_score(
        g0=np.ones(4),
        g1=np.full(4, 3.0),
        ps_raw=np.full(4, 0.5),
        score=score,
        fallback_g0=0,
        fallback_g1=0,
    )
    with pytest.raises(RuntimeError):
        duplicate_internal.record_internal_score(
            g0=np.ones(4),
            g1=np.full(4, 3.0),
            ps_raw=np.full(4, 0.5),
            score=score,
            fallback_g0=0,
            fallback_g1=0,
        )
    external.record_external_score(_score())
    with pytest.raises(RuntimeError):
        external.record_external_score(_score())


@pytest.mark.parametrize("changed", ["theta", "se"])
def test_finish_requires_exact_captured_score_scalars(changed):
    collector = _external_collector()
    capture = collector.start_rep(0, 42)
    score = _score()
    capture.record_external_score(score)
    theta = np.nextafter(score.theta, np.inf) if changed == "theta" else score.theta
    se = np.nextafter(score.se, np.inf) if changed == "se" else score.se
    with pytest.raises(RuntimeError):
        collector.finish_rep(capture, theta, se)


def _bad_splits(case):
    splits = _valid_splits()
    if case == "count":
        return splits[:1]
    replacements = {
        "float": np.array([2.0, 3.0]),
        "two_dim": np.array([[2, 3]]),
        "negative": np.array([-1, 3]),
        "out_of_range": np.array([2, 4]),
        "duplicate": np.array([2, 2]),
        "unsorted": np.array([3, 2]),
    }
    if case in replacements:
        splits[0] = (replacements[case], splits[0][1])
    elif case == "overlap":
        splits[0] = (np.array([1, 2, 3]), splits[0][1])
    elif case == "incomplete":
        splits[0] = (np.array([2]), splits[0][1])
    elif case == "test_duplicate":
        splits[1] = (splits[1][0], np.array([1, 2, 3]))
    elif case == "test_unsorted":
        splits[0] = (splits[0][0], np.array([1, 0]))
    return splits


@pytest.mark.parametrize(
    "case",
    [
        "count",
        "float",
        "two_dim",
        "negative",
        "out_of_range",
        "duplicate",
        "unsorted",
        "overlap",
        "incomplete",
        "test_duplicate",
        "test_unsorted",
    ],
)
def test_internal_split_preflight_rejects_malformed_indices(case):
    capture = _internal_collector().start_rep(0, 42)
    with pytest.raises(ValueError):
        capture.record_internal_splits(_bad_splits(case), min_subgroup_fit=1)


def test_second_fold_index_error_is_found_before_any_learner_fit(monkeypatch):
    frame = internal_literal_frame()
    splits = partition_splits(internal_partitions()[101])
    train, test = splits[1]
    splits[1] = (train, np.r_[test[:-1], len(frame)])
    estimator = internal_estimator(frame, forbid_fit=True)
    monkeypatch.setattr(estimator, "_make_splits", lambda *_a, **_k: splits)
    with pytest.raises(ValueError, match="out-of-range"):
        estimator.fit(store_oof=True)


@pytest.mark.parametrize("one_shot", [True, False], ids=["generator", "list"])
def test_internal_split_source_requires_reiterable_sequence(monkeypatch, one_shot):
    splits = partition_splits(internal_partitions()[101])
    estimator = internal_estimator(internal_literal_frame())
    source = iter(splits) if one_shot else splits
    monkeypatch.setattr(estimator, "_make_splits", lambda *_a, **_k: source)
    reset_internal_audits()
    if one_shot:
        with pytest.raises(ValueError, match="splits must be a sequence"):
            estimator.fit(store_oof=True)
        assert TrainingMeanRegressor.fit_rows == []
    else:
        bundle = estimator.fit(store_oof=True).get_oof()
        np.testing.assert_array_equal(bundle.predictions.fold_ids[0], [0, 0, 1, 1] * 12)
        assert TrainingMeanRegressor.fit_rows


@pytest.mark.parametrize("side", ["train", "test"])
@pytest.mark.parametrize("boolean", [False, np.bool_(False)], ids=["bool", "np_bool"])
def test_mixed_boolean_split_index_fails_before_learner(monkeypatch, side, boolean):
    splits = partition_splits(internal_partitions()[101])
    fold, part = (1, 0) if side == "train" else (0, 1)
    pair = list(splits[fold])
    pair[part] = pair[part].tolist()
    pair[part][0] = boolean
    splits[fold] = tuple(pair)
    estimator = internal_estimator(internal_literal_frame(), forbid_fit=True)
    monkeypatch.setattr(estimator, "_make_splits", lambda *_a, **_k: splits)
    with pytest.raises(ValueError, match=f"{side} indices.*integer"):
        estimator.fit(store_oof=True)


@pytest.mark.parametrize("dispatcher", [False, True])
def test_internal_explicit_folds_with_repeats_fail_before_retention_work(
    monkeypatch, dispatcher
):
    frame = internal_literal_frame()
    folds = np.tile([0, 0, 1, 1], 12)
    message = (
        "dml.irm: explicit fold_indices require n_rep=1; pass one fold "
        "assignment for the single cross-fit repetition."
    )
    retention_module = importlib.import_module("statspai.dml._oof_retention")
    irm_module = importlib.import_module("statspai.dml.irm")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("explicit-fold gate reached retention or fitting work")

    monkeypatch.setattr(retention_module, "internal_analysis_identity", forbidden)
    monkeypatch.setattr(retention_module.OOFRetention, "internal", forbidden)
    monkeypatch.setattr(DoubleMLIRM, "_make_splits", forbidden)
    monkeypatch.setattr(irm_module, "score_binary_ate", forbidden)
    with pytest.raises(MethodIncompatibility) as error:
        if dispatcher:
            dml(
                frame,
                y="y",
                treat="d",
                covariates=["x1", "x2"],
                model="irm",
                ml_g=NoFitRegressor(),
                ml_m=NoFitClassifier(),
                n_folds=2,
                n_rep=2,
                fold_indices=folds,
                store_oof=True,
            )
        else:
            internal_estimator(frame, n_rep=2, fold_indices=folds, forbid_fit=True).fit(
                store_oof=True
            )
    assert str(error.value) == message


def test_retained_internal_rejects_nine_rows_per_arm_before_any_fit(monkeypatch):
    frame = internal_literal_frame(36)
    folds = np.tile([0, 0, 1, 1], 9)
    fit_calls = []

    def forbidden_fit(*_args, **_kwargs):
        fit_calls.append(True)
        raise AssertionError("learner fit ran before retained fallback preflight")

    monkeypatch.setattr(DoubleMLIRM, "_fit_weighted", forbidden_fit)
    with pytest.raises(
        DataInsufficient, match="subgroup-mean fallback.*fold 0.*count=9"
    ):
        internal_estimator(frame, fold_indices=folds, forbid_fit=True).fit(
            store_oof=True
        )
    assert fit_calls == []


def test_second_fold_fallback_error_is_found_before_any_fit(monkeypatch):
    frame = internal_literal_frame(39)
    d = frame["d"].to_numpy()
    d0, d1 = np.flatnonzero(d == 0), np.flatnonzero(d == 1)
    first_test = np.sort(np.r_[d0[:10], d1[:9]])
    second_test = np.setdiff1d(np.arange(len(frame)), first_test)
    splits = [(second_test, first_test), (first_test, second_test)]
    fit_calls = []

    def forbidden_fit(*_args, **_kwargs):
        fit_calls.append(True)
        raise AssertionError("learner fit ran before second-fold fallback preflight")

    estimator = internal_estimator(frame, forbid_fit=True)
    monkeypatch.setattr(estimator, "_make_splits", lambda *_a, **_k: splits)
    monkeypatch.setattr(DoubleMLIRM, "_fit_weighted", forbidden_fit)
    with pytest.raises(
        DataInsufficient, match="subgroup-mean fallback.*fold 1.*count=9"
    ):
        estimator.fit(store_oof=True)
    assert fit_calls == []


def test_legacy_unstored_fit_keeps_nine_row_subgroup_fallback():
    frame = internal_literal_frame(36)
    folds = np.tile([0, 0, 1, 1], 9)
    reset_internal_audits()
    result = internal_estimator(frame, fold_indices=folds).fit()
    diagnostics = result.model_info["diagnostics"]
    assert diagnostics["n_subgroup_fallback_g0"] == 2
    assert diagnostics["n_subgroup_fallback_g1"] == 2


def test_retained_internal_accepts_ten_rows_per_arm_without_fallback():
    frame = internal_literal_frame(40)
    folds = np.tile([0, 0, 1, 1], 10)
    result = internal_estimator(frame, fold_indices=folds).fit(store_oof=True)
    assert all(
        record["subgroup_fallback_counts"] == {"g0": 0, "g1": 0}
        for record in result.get_oof().metadata["fit_records"]
    )


@pytest.mark.parametrize("mode", ["internal", "external"])
def test_store_false_forbids_all_retention_construction_and_attachment(
    monkeypatch, mode
):
    retention_module = importlib.import_module("statspai.dml._oof_retention")
    base_module = importlib.import_module("statspai.dml._base")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("store_oof=False reached retention work")

    monkeypatch.setattr(retention_module.OOFRetention, "internal", forbidden)
    monkeypatch.setattr(retention_module.OOFRetention, "external", forbidden)
    monkeypatch.setattr(retention_module, "_internal_software_versions", forbidden)
    monkeypatch.setattr(base_module, "_attach_result_oof", forbidden)
    if mode == "internal":
        frame = internal_literal_frame()
        estimator = internal_estimator(frame, fold_indices=internal_partitions()[101])
        result = estimator.fit()
    else:
        frame, predictions = external_literal_fixture()
        estimator = external_estimator(frame)
        result = estimator.fit(
            external_predictions=predictions, observation_ids=predictions.ids
        )
        assert result.model_info["external_predictions_hashes"] == dict(
            predictions.hashes
        )
    with pytest.raises(ValueError, match="^OOF records are unavailable;"):
        result.get_oof()
    assert "_dml_oof_bundle" not in result.__dict__
    assert "_oof_rep_capture" not in estimator.__dict__
