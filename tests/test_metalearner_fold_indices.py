"""``sp.metalearner(fold_indices=...)``: caller-controlled cross-fitting."""

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold

import statspai as sp
from statspai.exceptions import DataInsufficient, MethodIncompatibility

COV = ["x1", "x2", "x3"]
LEARNERS = ["s", "t", "x", "r", "dr"]


def _data(n=300, seed=20260922):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 3))
    p = 1 / (1 + np.exp(-(0.6 * X[:, 0] - 0.4 * X[:, 1])))
    D = rng.binomial(1, p)
    Y = 1.5 * D + X @ np.array([1.0, -0.5, 0.3]) + 0.5 * D * X[:, 2]
    Y = Y + rng.normal(size=n)
    df = pd.DataFrame(X, columns=COV)
    df["y"], df["d"] = Y, D
    return df


def _fit(df, learner, **kw):
    kw.setdefault("n_folds", 3)
    return sp.metalearner(
        df,
        y="y",
        treat="d",
        covariates=COV,
        learner=learner,
        outcome_model=LinearRegression(),
        propensity_model=LogisticRegression(),
        cate_model=LinearRegression(),
        **kw,
    )


def _kfold_labels(n, k, seed=42):
    f = np.empty(n, dtype=int)
    for j, (_, te) in enumerate(
        KFold(k, shuffle=True, random_state=seed).split(np.zeros(n))
    ):
        f[te] = j
    return f


# Produced by the pre-change code (origin/main 4bf29552) on _data() with
# n_folds=3; verified bit-identical locally. rtol=1e-9 absorbs only BLAS /
# lbfgs round-off across CI platforms. (estimate, se, cate_mean)
_AIPW = (1.3040246261930448, 0.1308618001289441)
_CATE_MEAN = {
    "s": 1.3051128786305295,
    "t": 1.305793946664261,
    "x": 1.305793946664261,
    "r": 1.2865942283097922,
    "dr": 1.3040246261930448,
}


@pytest.mark.parametrize("learner", LEARNERS)
def test_default_path_unchanged(learner):
    r = _fit(_data(), learner)
    np.testing.assert_allclose(r.estimate, _AIPW[0], rtol=1e-9)
    np.testing.assert_allclose(r.se, _AIPW[1], rtol=1e-9)
    np.testing.assert_allclose(
        r.model_info["cate_mean"], _CATE_MEAN[learner], rtol=1e-9
    )
    assert r.model_info["cross_fit_partition"].startswith("KFold(n_splits=3")


@pytest.mark.parametrize("learner", LEARNERS)
def test_kfold_labels_reproduce_default_exactly(learner):
    df = _data()
    a = _fit(df, learner)
    b = _fit(df, learner, fold_indices=_kfold_labels(len(df), 3))
    assert a.estimate == b.estimate
    assert a.se == b.se
    np.testing.assert_array_equal(a.model_info["cate"], b.model_info["cate"])
    assert b.model_info["cross_fit_partition"] == "fold_indices"


@pytest.mark.parametrize("learner", ["r", "dr", "s"])
def test_other_partition_changes_result(learner):
    df = _data()
    a = _fit(df, learner)
    b = _fit(df, learner, fold_indices=_kfold_labels(len(df), 3, seed=0))
    assert a.estimate != b.estimate
    if learner in ("r", "dr"):  # CATE nuisances are cross-fitted too
        assert not np.array_equal(a.model_info["cate"], b.model_info["cate"])


def test_default_gbm_models_reproduced_by_kfold_labels():
    df = _data()
    a = sp.metalearner(df, y="y", treat="d", covariates=COV, learner="dr", n_folds=3)
    b = sp.metalearner(
        df,
        y="y",
        treat="d",
        covariates=COV,
        learner="dr",
        n_folds=3,
        fold_indices=_kfold_labels(len(df), 3),
    )
    assert a.estimate == b.estimate and a.se == b.se


def test_folds_align_with_input_rows_when_rows_are_dropped():
    df = _data()
    f = _kfold_labels(len(df), 3, seed=5)
    dirty = df.copy()
    dirty.loc[[4, 77], "x1"] = np.nan
    keep = dirty[COV].notna().all(axis=1).to_numpy()
    a = _fit(dirty, "dr", fold_indices=f)
    b = _fit(df[keep].reset_index(drop=True), "dr", fold_indices=f[keep])
    assert a.estimate == b.estimate and a.se == b.se


def test_learner_classes_accept_fold_indices():
    df = _data()
    X, Y, D = df[COV].to_numpy(), df["y"].to_numpy(), df["d"].to_numpy()
    f = _kfold_labels(len(df), 3)
    a = sp.DRLearner(n_folds=3).fit(X, Y, D).effect(X)
    b = sp.DRLearner(n_folds=3, fold_indices=f).fit(X, Y, D).effect(X)
    np.testing.assert_array_equal(a, b)
    a = sp.RLearner(n_folds=3).fit(X, Y, D).effect(X)
    b = sp.RLearner(n_folds=3, fold_indices=f).fit(X, Y, D).effect(X)
    np.testing.assert_array_equal(a, b)


@pytest.mark.parametrize(
    "bad",
    [
        lambda n: np.arange(n - 1) % 3,  # wrong length
        lambda n: np.arange(n) % 2,  # 2 folds but n_folds=3
        lambda n: (np.arange(n) % 3) + 1,  # labels 1..3
        lambda n: (np.arange(n) % 3) + 0.25,  # non-integer
        lambda n: np.where(np.arange(n) == 0, np.nan, np.arange(n) % 3),
        lambda n: np.array(["a", "b", "c"] * (n // 3)),  # strings
    ],
)
def test_invalid_fold_vectors_raise(bad):
    df = _data()
    with pytest.raises(MethodIncompatibility):
        _fit(df, "dr", fold_indices=bad(len(df)))


def test_one_arm_training_complement_raises():
    df = _data()
    d = df["d"].to_numpy()
    # Fold 0 = all controls -> training complement of fold 1 and 2 still
    # mixed, but fold 0's complement is treated-only.
    f = np.where(d == 0, 0, 1 + (np.arange(len(d)) % 2))
    with pytest.raises(DataInsufficient):
        _fit(df, "dr", fold_indices=f)
