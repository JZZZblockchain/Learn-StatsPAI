"""Exact structural identities of the GRF engine (``statspai.forest._grf_engine``).

These do not depend on any reference implementation: each is a property the
algorithm must satisfy by construction, checked to floating-point precision.
"""

from __future__ import annotations

import numpy as np
import pytest

from statspai.forest import _grf_engine as E


def _design(n=400, p=3, seed=0, clusters=None):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, p))
    W = rng.integers(0, 2, n).astype(float)
    Y = X[:, 0] + (1 + X[:, 1]) * W + rng.normal(size=n)
    return X, Y - Y.mean(), W - W.mean()


def _weighted_slope(alpha, Y, W):
    a = alpha / alpha.sum()
    wb = np.sum(a * W)
    yb = np.sum(a * Y)
    return np.sum(a * (W - wb) * (Y - yb)) / np.sum(a * (W - wb) ** 2)


def test_causal_prediction_equals_forest_weighted_regression():
    X, Y, W = _design()
    forest = E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, num_trees=100, seed=3)
    Xnew = np.random.default_rng(9).normal(size=(15, 3))
    tau, _ = forest.predict(Xnew)
    alpha = forest.forest_weights(Xnew)
    np.testing.assert_allclose(alpha.sum(axis=1), 1.0, atol=1e-12)
    expected = np.array([_weighted_slope(alpha[i], Y, W) for i in range(15)])
    np.testing.assert_allclose(tau, expected, rtol=1e-10, atol=1e-12)


def test_regression_prediction_equals_forest_weighted_mean():
    X, Y, _ = _design()
    forest = E.train_forest(
        X, Y, kind=E.KIND_REGRESSION, num_trees=60, ci_group_size=1, seed=1
    )
    pred, _ = forest.predict(X[:20])
    alpha = forest.forest_weights(X[:20])
    np.testing.assert_allclose(pred, alpha @ Y, rtol=1e-10, atol=1e-12)


def test_oob_weights_exclude_the_row_itself():
    X, Y, W = _design(n=300)
    forest = E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, num_trees=80, seed=2)
    alpha = forest.forest_weights(X, oob=True)
    np.testing.assert_array_equal(np.diag(alpha), 0.0)
    tau_oob, _ = forest.predict_oob(X)
    expected = np.array([_weighted_slope(alpha[i], Y, W) for i in range(len(Y))])
    np.testing.assert_allclose(tau_oob, expected, rtol=1e-9, atol=1e-11)


def test_oob_weights_exclude_the_whole_cluster():
    X, Y, W = _design(n=300)
    clusters = np.repeat(np.arange(60), 5)
    forest = E.train_forest(
        X, Y, W, kind=E.KIND_CAUSAL, num_trees=80, seed=4, clusters=clusters
    )
    alpha = forest.forest_weights(X, oob=True)
    same_cluster = clusters[:, None] == clusters[None, :]
    assert np.all(alpha[same_cluster] == 0.0)


def test_training_rows_never_estimate_and_grow_in_the_same_tree():
    """Honest leaves hold only estimation rows: a row's own leaf mass in a
    tree that drew it comes from the other half, so non-OOB predictions at a
    training row still give it weight only through estimation-sample trees."""
    X, Y, W = _design(n=200)
    forest = E.train_forest(
        X, Y, W, kind=E.KIND_CAUSAL, num_trees=20, seed=5, ci_group_size=1
    )
    n_nodes = np.diff(np.concatenate([forest.node_offsets, [forest.left.size]]))
    for t in range(forest.num_trees):
        base = forest.leaf_offset_base[t]
        offsets = forest.leaf_offsets[base : base + n_nodes[t] + 1]
        members = forest.leaf_members[
            forest.member_base[t] : forest.member_base[t] + offsets[-1]
        ]
        drawn = np.flatnonzero(
            np.unpackbits(forest.drawn_bitmap[t], bitorder="little")[: len(Y)]
        )
        # Estimation rows are a subset of the drawn rows and hold roughly
        # half of them (honesty_fraction = 0.5).
        assert np.isin(members, drawn).all()
        assert 0.3 * drawn.size <= members.size <= 0.7 * drawn.size


def test_seed_determinism_and_thread_independence():
    X, Y, W = _design(n=300)
    a = E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, num_trees=40, seed=7, n_jobs=1)
    b = E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, num_trees=40, seed=7, n_jobs=4)
    c = E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, num_trees=40, seed=8, n_jobs=1)
    np.testing.assert_array_equal(a.predict(X)[0], b.predict(X)[0])
    assert not np.array_equal(a.predict(X)[0], c.predict(X)[0])


def test_num_trees_rounds_to_little_bag_multiple():
    X, Y, W = _design(n=200)
    forest = E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, num_trees=21, seed=0)
    assert forest.num_trees == 22


def test_variance_requires_little_bags_and_is_positive():
    X, Y, W = _design(n=500)
    forest = E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, num_trees=200, seed=0)
    _, var = forest.predict(X[:30], estimate_variance=True)
    assert np.all(np.isfinite(var)) and np.all(var >= 0)
    single = E.train_forest(
        X, Y, W, kind=E.KIND_CAUSAL, num_trees=50, seed=0, ci_group_size=1
    )
    _, var1 = single.predict(X[:5], estimate_variance=True)
    assert np.all(np.isnan(var1))


def test_invalid_sampling_options_raise():
    X, Y, W = _design(n=100)
    with pytest.raises(ValueError, match="sample_fraction"):
        E.train_forest(X, Y, W, kind=E.KIND_CAUSAL, sample_fraction=0.8)
    with pytest.raises(ValueError, match="no clusters"):
        E.train_forest(
            X, Y, W, kind=E.KIND_CAUSAL, sample_fraction=0.001, ci_group_size=1
        )


def _dummy_residuals(V, unit, time):
    D = np.column_stack(
        [np.eye(unit.max() + 1)[unit], np.eye(time.max() + 1)[time][:, 1:]]
    )
    beta = np.linalg.lstsq(D, V, rcond=None)[0]
    return V - D @ beta


@pytest.mark.parametrize("balanced", [True, False])
def test_fe_residualize_equals_two_way_dummy_regression(balanced):
    rng = np.random.default_rng(11)
    N, T = 40, 6
    unit = np.repeat(np.arange(N), T)
    time = np.tile(np.arange(T), N)
    if not balanced:
        keep = rng.uniform(size=N * T) > 0.25
        unit, time = unit[keep], time[keep]
        _, unit = np.unique(unit, return_inverse=True)
    V = rng.normal(size=unit.size) + unit * 0.3 + time * 0.7
    idx = np.arange(unit.size, dtype=np.int64)
    out = np.zeros(unit.size)
    sweeps = E._fe_residualize(
        idx,
        V,
        np.ones(unit.size),
        unit.astype(np.int64),
        time.astype(np.int64),
        np.zeros(N),
        np.zeros(N),
        np.zeros(T),
        np.zeros(T),
        out,
        10000,
        1e-13,
    )
    assert sweeps > 0
    if balanced:
        assert sweeps <= 2
    np.testing.assert_allclose(out, _dummy_residuals(V, unit, time), atol=1e-9)


def test_fe_forest_recovers_a_constant_effect_under_fixed_effect_confounding():
    rng = np.random.default_rng(2)
    N, T = 300, 5
    unit = np.repeat(np.arange(N), T)
    time = np.tile(np.arange(T), N)
    alpha = rng.normal(scale=3.0, size=N)
    adopt = np.where(alpha > 0.5, 2, np.where(alpha > -0.5, 3, 99))
    D = (time >= adopt[unit]).astype(float)
    X = rng.normal(size=(N, 2))[unit]
    Y = alpha[unit] + 2.0 * time + 1.5 * D + rng.normal(size=N * T)
    Yc, Dc = Y - Y.mean(), D - D.mean()
    fe = E.train_forest(
        X,
        Yc,
        Dc,
        kind=E.KIND_CAUSAL_FE,
        num_trees=400,
        seed=0,
        clusters=unit,
        unit=unit,
        time=time,
    )
    tau, _ = fe.predict_oob(X)
    assert abs(np.nanmean(tau) - 1.5) < 0.15
    pooled = E.train_forest(
        X, Yc, Dc, kind=E.KIND_CAUSAL, num_trees=400, seed=0, clusters=unit
    )
    tau_pooled, _ = pooled.predict_oob(X)
    assert abs(np.nanmean(tau_pooled) - 1.5) > 0.5
