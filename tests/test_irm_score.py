"""Task 4 contracts for the shared IRM scorer and internal reuse."""

from __future__ import annotations

import importlib
import math

import numpy as np
import pandas as pd
import pytest
from sklearn.base import BaseEstimator

from statspai.dml._irm_score import IRMScore, score_binary_ate
from statspai.dml.double_ml import DoubleML
from statspai.dml.irm import DoubleMLIRM
from statspai.exceptions import MethodIncompatibility


def _canonical_inputs():
    return {
        "y": np.array([1.0, 4.0, 3.0, 6.0]),
        "d": np.array([0.0, 1.0, 0.0, 1.0]),
        "g0": np.ones(4),
        "g1": np.full(4, 3.0),
        "ps_raw": np.full(4, 0.5),
    }


class TrainingMeanRegressor(BaseEstimator):
    def fit(self, X, y, sample_weight=None):
        del X, sample_weight
        self.value_ = float(np.mean(y))
        return self

    def predict(self, X):
        return np.full(len(X), self.value_)


class CenteredDoubleMeanRegressor(BaseEstimator):
    def __init__(self, center):
        self.center = center

    def fit(self, X, y, sample_weight=None):
        del X, sample_weight
        self.value_ = float(
            self.center + 2.0 * np.mean(np.asarray(y, dtype=float) - self.center)
        )
        return self

    def predict(self, X):
        return np.full(len(X), self.value_)


class TrainingRateClassifier(BaseEstimator):
    def fit(self, X, y, sample_weight=None):
        del X, sample_weight
        self.rate_ = float(np.mean(y))
        self.classes_ = np.array([0.0, 1.0])
        return self

    def predict_proba(self, X):
        rate = np.full(len(X), self.rate_)
        return np.column_stack((1.0 - rate, rate))


def _internal_fixture(kind="normal"):
    row_id = np.arange(64)
    treatment = np.tile([0.0, 1.0, 0.0, 1.0], 16)
    partition = np.tile([0, 0, 1, 1], 16)
    residual = np.repeat(np.tile([-3.0, -1.0, 1.0, 3.0], 4), 4)
    if kind == "normal":
        outcome = 10.0 + 4.0 * treatment + 2.0 * partition + residual
        learner = TrainingMeanRegressor()
    elif kind == "large_offset":
        outcome = 10.0 + 4.0 * treatment + 2.0 * partition + residual + float(2**50)
        learner = TrainingMeanRegressor()
    else:
        center = float(2**50)
        outcome = 0.5 * center + center * treatment + 0.5 * residual
        learner = CenteredDoubleMeanRegressor(center=center)
    frame = pd.DataFrame(
        {
            "y": outcome,
            "d": treatment,
            "x1": row_id.astype(float) - 32.0,
            "x2": residual,
        }
    )
    return frame, partition, learner


def _internal_estimator(kind="normal", *, n_rep=1, fold_indices=None):
    frame, partition, learner = _internal_fixture(kind)
    if fold_indices is None and n_rep == 1:
        fold_indices = partition
    estimator = DoubleMLIRM(
        frame,
        y="y",
        treat="d",
        covariates=["x1", "x2"],
        ml_g=learner,
        ml_m=TrainingRateClassifier(),
        n_folds=2,
        n_rep=n_rep,
        random_state=101,
        fold_indices=fold_indices,
        score="ATE",
        normalize_ipw=False,
        trimming_threshold=0.01,
    )
    return estimator


def test_score_binary_ate_matches_hand_calculation():
    score = score_binary_ate(**_canonical_inputs(), trimming_threshold=0.01)

    assert isinstance(score, IRMScore)
    np.testing.assert_array_equal(score.ps_used, [0.5, 0.5, 0.5, 0.5])
    np.testing.assert_array_equal(score.psi_b, [2.0, 4.0, -2.0, 8.0])
    assert score.theta == 3.0
    np.testing.assert_array_equal(score.psi, [-1.0, 1.0, -5.0, 5.0])
    assert score.se == math.sqrt(3.25)


def test_score_binary_ate_clips_raw_boundaries_without_mutating_input():
    values = _canonical_inputs()
    values["ps_raw"] = np.array([0.0, 1.0, 0.5, 0.5])
    before = values["ps_raw"].copy()

    score = score_binary_ate(**values, trimming_threshold=0.1)

    np.testing.assert_array_equal(values["ps_raw"], before)
    np.testing.assert_array_equal(score.ps_used, [0.1, 0.9, 0.5, 0.5])
    np.testing.assert_allclose(score.psi_b, [2.0, 28.0 / 9.0, -2.0, 8.0])
    assert score.theta == pytest.approx(25.0 / 9.0)
    assert score.se**2 == pytest.approx(343.0 / 108.0)


@pytest.mark.parametrize("name", ["y", "d", "g0", "g1", "ps_raw"])
def test_score_binary_ate_does_not_mutate_or_share_caller_arrays(name):
    values = _canonical_inputs()
    before = {
        key: (value.copy(), value.shape, value.dtype, value.flags.writeable)
        for key, value in values.items()
    }

    score = score_binary_ate(**values, trimming_threshold=0.01)

    for key, value in values.items():
        expected, shape, dtype, writeable = before[key]
        np.testing.assert_array_equal(value, expected)
        assert value.shape == shape
        assert value.dtype == dtype
        assert value.flags.writeable == writeable
    for output in (score.ps_used, score.psi_b, score.psi):
        assert not np.shares_memory(values[name], output)


@pytest.mark.parametrize("field", ["ps_used", "psi_b", "psi"])
@pytest.mark.parametrize(
    "operation", ["value", "shape", "dtype", "strides", "resize", "setflags"]
)
def test_score_arrays_are_immutable_snapshots(field, operation):
    score = score_binary_ate(**_canonical_inputs(), trimming_threshold=0.01)
    expected = getattr(score, field).copy()
    array = getattr(score, field)

    with pytest.raises((AttributeError, TypeError, ValueError)):
        if operation == "value":
            array[0] = 99.0
        elif operation == "shape":
            array.shape = (2, 2)
        elif operation == "dtype":
            array.dtype = np.uint8
        elif operation == "strides":
            array.strides = (0,)
        elif operation == "resize":
            array.resize((2, 2), refcheck=False)
        else:
            array.setflags(write=True)

    np.testing.assert_array_equal(getattr(score, field), expected)


@pytest.mark.parametrize("field", ["ps_used", "psi_b", "psi"])
@pytest.mark.parametrize("operation", ["shape", "dtype", "strides", "resize"])
def test_unbound_numpy_header_mutation_cannot_change_score_snapshot(field, operation):
    score = score_binary_ate(**_canonical_inputs(), trimming_threshold=0.01)
    expected = getattr(score, field)
    expected_state = (
        expected.shape,
        expected.dtype.str,
        expected.strides,
        expected.tobytes(),
    )
    exposed = getattr(score, field)

    try:
        if operation == "shape":
            np.ndarray.__setattr__(exposed, "shape", (2, 2))
        elif operation == "dtype":
            np.ndarray.__setattr__(exposed, "dtype", np.uint8)
        elif operation == "strides":
            np.ndarray.__setattr__(exposed, "strides", (0,))
        else:
            np.ndarray.resize(exposed, (2, 2), refcheck=False)
    except (AttributeError, TypeError, ValueError):
        pass

    fresh = getattr(score, field)
    assert (
        fresh.shape,
        fresh.dtype.str,
        fresh.strides,
        fresh.tobytes(),
    ) == expected_state


def test_irm_score_cannot_be_constructed_directly():
    with pytest.raises(TypeError, match="score_binary_ate"):
        IRMScore()


@pytest.mark.parametrize(
    "threshold", [True, np.bool_(False), float("nan"), 0.0, 0.5, [0.1], "bad"]
)
def test_score_binary_ate_rejects_invalid_threshold(threshold):
    with pytest.raises(ValueError, match="trimming_threshold"):
        score_binary_ate(**_canonical_inputs(), trimming_threshold=threshold)


@pytest.mark.parametrize("name", ["y", "d", "g0", "g1", "ps_raw"])
@pytest.mark.parametrize(
    "bad",
    [
        np.array(1.0),
        np.ones((2, 2)),
        np.array([1 + 0j] * 4),
        np.array(["1", "2", "3", "4"]),
        np.array([1.0, 2.0, np.nan, 4.0]),
        np.array([1.0, 2.0, np.inf, 4.0]),
    ],
)
def test_score_binary_ate_rejects_invalid_arrays(name, bad):
    values = _canonical_inputs()
    values[name] = bad
    error = TypeError if bad.dtype.kind in "OUS" else ValueError
    with pytest.raises(error, match=name):
        score_binary_ate(**values, trimming_threshold=0.01)


def test_score_binary_ate_rejects_empty_or_different_lengths():
    values = {name: np.array([], dtype=float) for name in _canonical_inputs()}
    with pytest.raises(ValueError, match="non-empty"):
        score_binary_ate(**values, trimming_threshold=0.01)

    values = _canonical_inputs()
    values["g1"] = values["g1"][:-1]
    with pytest.raises(ValueError, match="same length"):
        score_binary_ate(**values, trimming_threshold=0.01)


@pytest.mark.parametrize(
    "d,match",
    [([0.0, 1.0, 2.0, 1.0], "binary"), ([0.0, 0.0, 0.0, 0.0], "both")],
)
def test_score_binary_ate_rejects_invalid_treatment(d, match):
    values = _canonical_inputs()
    values["d"] = np.asarray(d)
    with pytest.raises(ValueError, match=match):
        score_binary_ate(**values, trimming_threshold=0.01)


@pytest.mark.parametrize("ps_raw", [[-0.1, 0.5, 0.5, 0.5], [1.1, 0.5, 0.5, 0.5]])
def test_score_binary_ate_rejects_propensity_outside_closed_unit_interval(ps_raw):
    values = _canonical_inputs()
    values["ps_raw"] = np.asarray(ps_raw)
    with pytest.raises(ValueError, match="inclusive"):
        score_binary_ate(**values, trimming_threshold=0.01)


def test_score_binary_ate_rejects_nonfinite_arithmetic():
    values = _canonical_inputs()
    values["y"] = np.array([np.finfo(float).max] * 4)
    values["g0"] = np.array([-np.finfo(float).max] * 4)
    with pytest.raises(ValueError, match="non-finite"):
        score_binary_ate(**values, trimming_threshold=0.01)


def test_score_binary_ate_calls_the_shared_leaf_once_with_clipped_propensity(
    monkeypatch,
):
    from statspai.dml._oof_score import binary_ate_pseudo_outcome as real_leaf

    scorer_module = importlib.import_module("statspai.dml._irm_score")
    calls = []

    def spy(y, d, g0, g1, ps_used):
        calls.append((y.copy(), d.copy(), g0.copy(), g1.copy(), ps_used.copy()))
        return real_leaf(y, d, g0, g1, ps_used)

    monkeypatch.setattr(scorer_module, "binary_ate_pseudo_outcome", spy)
    values = _canonical_inputs()
    values["ps_raw"] = np.array([0.0, 1.0, 0.5, 0.5])

    score_binary_ate(**values, trimming_threshold=0.1)

    assert len(calls) == 1
    np.testing.assert_array_equal(calls[0][-1], [0.1, 0.9, 0.5, 0.5])


@pytest.mark.parametrize(
    "kind,estimate,se,y_residual_block",
    [
        (
            "normal",
            4.0,
            0.75,
            [
                10.0,
                -10.0,
                2.0,
                -2.0,
                6.0,
                -6.0,
                -2.0,
                2.0,
                2.0,
                -2.0,
                -6.0,
                6.0,
                -2.0,
                2.0,
                -10.0,
                10.0,
            ],
        ),
        (
            "large_offset",
            4.0,
            0.75,
            [
                10.0,
                -10.0,
                2.0,
                -2.0,
                6.0,
                -6.0,
                -2.0,
                2.0,
                2.0,
                -2.0,
                -6.0,
                6.0,
                -2.0,
                2.0,
                -10.0,
                10.0,
            ],
        ),
        (
            "cancellation",
            float.fromhex("0x1.0000000000000p+50"),
            float.fromhex("0x1.1e3779b97f4a8p-2"),
            [
                3.0,
                -3.0,
                3.0,
                -3.0,
                1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                -1.0,
                1.0,
                -3.0,
                3.0,
                -3.0,
                3.0,
            ],
        ),
    ],
)
def test_internal_irm_prechange_literal_goldens(kind, estimate, se, y_residual_block):
    """Literal anchors captured at reviewed base 4e18e20d before IRM refactoring."""
    result = _internal_estimator(kind).fit()
    info = result.model_info

    assert result.estimate == estimate
    assert result.se == se
    if kind == "cancellation":
        assert result.pvalue == 0.0
        assert result.ci == tuple(
            map(float.fromhex, ["0x1.ffffffffffffcp+49", "0x1.0000000000002p+50"])
        )
    else:
        assert result.pvalue == float.fromhex("0x1.9e25951000000p-24")
        assert result.ci == tuple(
            map(float.fromhex, ["0x1.43d7ecd46602ep+1", "0x1.5e140995ccfe9p+2"])
        )
    np.testing.assert_array_equal(info["_y_resid"], np.tile(y_residual_block, 4))
    np.testing.assert_array_equal(info["_d_resid"], np.tile([-0.5, 0.5], 32))
    np.testing.assert_array_equal(info["_pscore"], np.full(64, 0.5))
    np.testing.assert_array_equal(
        info["_y_resid"] + result.estimate,
        np.tile(np.asarray(y_residual_block) + estimate, 4),
    )
    retained = _internal_estimator(kind).fit(store_oof=True)
    bundle = retained.get_oof()
    assert (
        retained.estimate,
        retained.se,
        retained.pvalue,
        retained.ci,
    ) == (result.estimate, result.se, result.pvalue, result.ci)
    np.testing.assert_array_equal(bundle.theta, [estimate])
    np.testing.assert_array_equal(bundle.se, [se])
    np.testing.assert_array_equal(bundle.psi[0], retained.model_info["_y_resid"])


def test_internal_irm_two_repeat_prechange_literal_golden(monkeypatch):
    estimator = _internal_estimator("normal", n_rep=2)
    partitions = iter(
        [
            np.tile([0, 0, 1, 1], 16),
            np.tile([0, 1, 1, 0], 16),
        ]
    )

    def prewritten_splits(X, *, rng_seed, fold_indices=None, stratify=None):
        del X, rng_seed, fold_indices, stratify
        partition = next(partitions)
        return [
            (np.flatnonzero(partition != fold), np.flatnonzero(partition == fold))
            for fold in range(2)
        ]

    monkeypatch.setattr(estimator, "_make_splits", prewritten_splits)
    result = estimator.fit()

    assert result.estimate == 4.0
    assert result.se == float.fromhex("0x1.5e8add236a58fp-1")
    assert result.model_info["theta_all_reps"] == [4.0, 4.0]
    assert result.model_info["se_all_reps"] == [
        0.75,
        float.fromhex("0x1.3988e1409212ep-1"),
    ]
    np.testing.assert_array_equal(
        result.model_info["_y_resid"],
        np.tile(
            [
                8.0,
                -8.0,
                4.0,
                -4.0,
                4.0,
                -4.0,
                0.0,
                0.0,
                0.0,
                0.0,
                -4.0,
                4.0,
                -4.0,
                4.0,
                -8.0,
                8.0,
            ],
            4,
        ),
    )


def test_internal_unweighted_ate_calls_shared_scorer(monkeypatch):
    irm_module = importlib.import_module("statspai.dml.irm")
    real_scorer = score_binary_ate
    calls = []

    def spy(*args, **kwargs):
        calls.append((args, kwargs))
        return real_scorer(*args, **kwargs)

    monkeypatch.setattr(irm_module, "score_binary_ate", spy, raising=False)
    result = _internal_estimator("normal").fit()

    assert result.estimate == 4.0
    assert len(calls) == 1
    assert calls[0][1]["trimming_threshold"] == 0.01


def test_internal_explicit_folds_with_multiple_repeats_still_fail_at_fit():
    frame, partition, learner = _internal_fixture("normal")
    estimator = DoubleMLIRM(
        frame,
        y="y",
        treat="d",
        covariates=["x1", "x2"],
        ml_g=learner,
        ml_m=TrainingRateClassifier(),
        n_folds=2,
        n_rep=2,
        fold_indices=partition,
    )

    with pytest.raises(MethodIncompatibility, match="require n_rep=1"):
        estimator.fit()


def test_weighted_internal_ate_reuses_canonical_scorer(monkeypatch):
    irm_module = importlib.import_module("statspai.dml.irm")
    calls = []

    def spy(*args, **kwargs):
        calls.append((args, kwargs))
        return score_binary_ate(*args, **kwargs)

    monkeypatch.setattr(irm_module, "score_binary_ate", spy)
    frame, partition, learner = _internal_fixture("normal")
    result = DoubleMLIRM(
        frame,
        y="y",
        treat="d",
        covariates=["x1", "x2"],
        ml_g=learner,
        ml_m=TrainingRateClassifier(),
        n_folds=2,
        fold_indices=partition,
        sample_weight=np.linspace(1.0, 2.0, len(frame)),
    ).fit()

    assert np.isfinite(result.estimate)
    assert len(calls) == 1


@pytest.mark.parametrize("score,normalize_ipw", [("ATTE", False), ("ATE", True)])
def test_internal_atte_and_normalized_ipw_do_not_enter_v1_scorer(
    monkeypatch, score, normalize_ipw
):
    irm_module = importlib.import_module("statspai.dml.irm")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("unsupported internal score entered binary ATE scorer")

    monkeypatch.setattr(irm_module, "score_binary_ate", forbidden)
    frame, partition, learner = _internal_fixture("normal")
    result = DoubleMLIRM(
        frame,
        y="y",
        treat="d",
        covariates=["x1", "x2"],
        ml_g=learner,
        ml_m=TrainingRateClassifier(),
        n_folds=2,
        fold_indices=partition,
        score=score,
        normalize_ipw=normalize_ipw,
    ).fit()

    assert np.isfinite(result.estimate)


def test_internal_default_explicit_and_legacy_facade_remain_bit_exact():
    frame, partition, learner = _internal_fixture("normal")
    common = {
        "y": "y",
        "treat": "d",
        "covariates": ["x1", "x2"],
        "ml_g": learner,
        "ml_m": TrainingRateClassifier(),
        "n_folds": 2,
        "fold_indices": partition,
    }
    default = DoubleMLIRM(frame, **common).fit()
    explicit = DoubleMLIRM(
        frame,
        **common,
        score="ATE",
        normalize_ipw=False,
        trimming_threshold=0.01,
    ).fit()
    legacy = DoubleML(frame, model="irm", **common)
    legacy_result = legacy.fit()

    expected = (default.estimate, default.se, default.pvalue, default.ci)
    assert (explicit.estimate, explicit.se, explicit.pvalue, explicit.ci) == expected
    assert (
        legacy_result.estimate,
        legacy_result.se,
        legacy_result.pvalue,
        legacy_result.ci,
    ) == expected
    assert legacy.model == "irm"
    assert legacy.data is frame
    assert legacy.y == "y" and legacy.treat == "d"
    assert legacy.covariates == ["x1", "x2"]
