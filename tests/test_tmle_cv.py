"""Opt-in cross-validated TMLE: ``sp.tmle(fold_indices=...)``.

The default path (``fold_indices=None``) must be numerically unchanged;
the CV-TMLE path must equal a hand-rolled targeting step on the same
out-of-fold nuisances, and sit within second-order distance of AIPW on
those nuisances.
"""

import numpy as np
import pandas as pd
import pytest
from scipy.optimize import brentq
from scipy.special import expit, logit
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression

import statspai as sp
from statspai.exceptions import DataInsufficient, MethodIncompatibility
from statspai.tmle import SuperLearner

COV = ["x1", "x2", "x3"]


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


def _fit(df, **kw):
    return sp.tmle(
        df,
        y="y",
        treat="d",
        covariates=COV,
        outcome_library=[LinearRegression()],
        propensity_library=[LogisticRegression()],
        **kw,
    )


def _folds(n, k=5, seed=7):
    return np.random.default_rng(seed).permutation(np.arange(n) % k)


# ---------------------------------------------------------------------------
# (a) default path unchanged
# ---------------------------------------------------------------------------

# Produced by the pre-change code (origin/main 4bf29552) on _data(); the
# change was verified bit-identical locally. rtol=1e-9 leaves room only for
# BLAS / lbfgs round-off across CI platforms, not for any method change.
_PINNED = {
    ("ATE", "single"): (1.2898891351089663, 0.12290952363138945),
    ("ATE", "per_arm"): (1.2885177831186274, 0.12261904582960428),
    ("ATT", "single"): (1.2251790334360984, 0.1297774588063753),
    ("ATT", "per_arm"): (1.219555357652584, 0.12964724262444058),
}


@pytest.mark.parametrize("estimand,fluct", sorted(_PINNED))
def test_default_path_unchanged(estimand, fluct):
    r = _fit(_data(), estimand=estimand, fluctuation=fluct)
    est, se = _PINNED[(estimand, fluct)]
    np.testing.assert_allclose(r.estimate, est, rtol=1e-9)
    np.testing.assert_allclose(r.se, se, rtol=1e-9)
    assert r.model_info["cross_fitted"] is False
    assert r.model_info["n_cv_folds"] is None
    assert r.model_info["nuisance_source"] == {
        "Q": "super_learner",
        "g1W": "super_learner",
    }


# ---------------------------------------------------------------------------
# (b) CV-TMLE equals a hand-rolled targeting step on out-of-fold nuisances
# ---------------------------------------------------------------------------


def _hand_rolled(df, folds, bounds=(0.025, 0.975), q_bound=1e-5):
    Y = df["y"].to_numpy(float)
    A = df["d"].to_numpy(float)
    W = df[COV].to_numpy(float)
    n = len(Y)
    y_min, y_rng = Y.min(), Y.max() - Y.min()
    Ys = (Y - y_min) / (y_rng + 1e-10)
    QA, Q1, Q0, g = (np.empty(n) for _ in range(4))
    for k in range(folds.max() + 1):
        tr, te = folds != k, folds == k
        q = LinearRegression().fit(np.column_stack([A[tr], W[tr]]), Ys[tr])
        QA[te] = q.predict(np.column_stack([A[te], W[te]]))
        Q1[te] = q.predict(np.column_stack([np.ones(te.sum()), W[te]]))
        Q0[te] = q.predict(np.column_stack([np.zeros(te.sum()), W[te]]))
        gm = LogisticRegression().fit(W[tr], A[tr])
        # SuperLearner clips classification output to (1e-6, 1 - 1e-6).
        g[te] = np.clip(gm.predict_proba(W[te])[:, 1], 1e-6, 1 - 1e-6)
    QA, Q1, Q0 = (np.clip(v, q_bound, 1 - q_bound) for v in (QA, Q1, Q0))
    g = np.clip(g, *bounds)
    H = A / g - (1 - A) / (1 - g)

    def score(e):
        return np.sum(H * (Ys - expit(logit(QA) + e * H)))

    eps = brentq(score, -10, 10, xtol=1e-15)
    s = y_rng + 1e-10
    QsA = expit(logit(QA) + eps * H) * s + y_min
    Qs1 = expit(logit(Q1) + eps / g) * s + y_min
    Qs0 = expit(logit(Q0) - eps / (1 - g)) * s + y_min
    psi = np.mean(Qs1 - Qs0)
    eif = Qs1 - Qs0 + A * (Y - QsA) / g - (1 - A) * (Y - QsA) / (1 - g) - psi
    se = np.std(eif, ddof=1) / np.sqrt(n)
    # AIPW on the same (untargeted) out-of-fold nuisances.
    qa, q1, q0 = (v * s + y_min for v in (QA, Q1, Q0))
    aipw = np.mean(q1 - q0 + A * (Y - qa) / g - (1 - A) * (Y - qa) / (1 - g))
    return psi, se, aipw, eps


def test_cv_tmle_matches_hand_rolled_targeting():
    df = _data(n=2000, seed=11)
    folds = _folds(len(df))
    r = _fit(df, fold_indices=folds)
    psi, se, aipw, eps = _hand_rolled(df, folds)
    # Same nuisances, same fluctuation; the package's Newton stops at
    # |step| < 1e-8, and quadratic convergence puts its epsilon within
    # ~1e-15 of the root brentq finds, so the plug-in agrees to round-off.
    np.testing.assert_allclose(r.estimate, psi, rtol=0, atol=1e-10)
    np.testing.assert_allclose(r.se, se, rtol=0, atol=1e-10)
    np.testing.assert_allclose(r.model_info["epsilon"], eps, rtol=0, atol=1e-9)
    # TMLE and AIPW both solve the efficient-influence-function equation
    # on the same nuisances; they differ by a second-order remainder
    # (O_p(1/n) here), far below one standard error. 0.1 SE is a loose,
    # sample-size-aware bound for that remainder; observed ~4e-3 SE.
    assert abs(r.estimate - aipw) < 0.1 * r.se
    assert r.model_info["cross_fitted"] is True
    assert r.model_info["n_cv_folds"] == 5
    assert r.model_info["nuisance_source"]["Q"] == "super_learner_out_of_fold"
    assert r.model_info["sl_outcome_weights"] is None
    assert len(r.model_info["sl_outcome_weights_by_fold"]) == 5
    assert len(r.model_info["sl_propensity_weights_by_fold"]) == 5
    assert r.method.startswith("CV-TMLE")


def _hand_rolled_att(df, folds, bounds=(0.025, 0.975), q_bound=1e-5):
    """ATT targeting as documented: only Q is updated (g held fixed), the
    estimate is the estimating-equation form, p = full-sample treated share."""
    Y = df["y"].to_numpy(float)
    A = df["d"].to_numpy(float)
    W = df[COV].to_numpy(float)
    n = len(Y)
    y_min, y_rng = Y.min(), Y.max() - Y.min()
    Ys = (Y - y_min) / (y_rng + 1e-10)
    QA, Q0, g = (np.empty(n) for _ in range(3))
    for k in range(folds.max() + 1):
        tr, te = folds != k, folds == k
        q = LinearRegression().fit(np.column_stack([A[tr], W[tr]]), Ys[tr])
        QA[te] = q.predict(np.column_stack([A[te], W[te]]))
        Q0[te] = q.predict(np.column_stack([np.zeros(te.sum()), W[te]]))
        gm = LogisticRegression().fit(W[tr], A[tr])
        g[te] = np.clip(gm.predict_proba(W[te])[:, 1], 1e-6, 1 - 1e-6)
    QA, Q0 = (np.clip(v, q_bound, 1 - q_bound) for v in (QA, Q0))
    g = np.clip(g, *bounds)
    H_A = A - (1 - A) * g / (1 - g)
    H_0 = -g / (1 - g)

    def score(e):
        return np.sum(H_A * (Ys - expit(logit(QA) + e * H_A)))

    eps = brentq(score, -10, 10, xtol=1e-15)
    s = y_rng + 1e-10
    Qs0 = expit(logit(Q0) + eps * H_0) * s + y_min
    p = A.mean()
    summand = A * (Y - Qs0) / p - (1 - A) * g * (Y - Qs0) / ((1 - g) * p)
    psi = np.mean(summand)
    eif = summand - psi * A / p
    return psi, np.std(eif, ddof=1) / np.sqrt(n), eps


def test_cv_tmle_att_matches_hand_rolled_targeting():
    df = _data(n=2000, seed=11)
    folds = _folds(len(df))
    r = _fit(df, fold_indices=folds, estimand="ATT")
    psi, se, eps = _hand_rolled_att(df, folds)
    # Same nuisances and fluctuation; agreement to round-off (see ATE test).
    np.testing.assert_allclose(r.estimate, psi, rtol=0, atol=1e-10)
    np.testing.assert_allclose(r.se, se, rtol=0, atol=1e-10)
    np.testing.assert_allclose(r.model_info["epsilon"], eps, rtol=0, atol=1e-9)


def test_inner_super_learner_cv_stays_inside_training_complement():
    df = _data(n=600, seed=3)
    folds = _folds(len(df), k=3)
    q_lib = [LinearRegression(), RandomForestRegressor(n_estimators=30, random_state=0)]
    g_lib = [
        LogisticRegression(),
        RandomForestClassifier(n_estimators=30, random_state=0),
    ]
    r = sp.tmle(
        df,
        y="y",
        treat="d",
        covariates=COV,
        outcome_library=q_lib,
        propensity_library=g_lib,
        fold_indices=folds,
    )
    Y = df["y"].to_numpy(float)
    A = df["d"].to_numpy(float)
    W = df[COV].to_numpy(float)
    Ys = (Y - Y.min()) / (Y.max() - Y.min() + 1e-10)  # full-sample bounds
    AW = np.column_stack([A, W])
    for k in range(3):
        tr = folds != k
        sq = SuperLearner(library=q_lib, n_folds=5, task="regression", random_state=42)
        sq.fit(AW[tr], Ys[tr])
        sg = SuperLearner(
            library=g_lib, n_folds=5, task="classification", random_state=42
        )
        sg.fit(W[tr], A[tr])
        # Identical computation on identical rows: exact equality.
        assert r.model_info["sl_outcome_weights_by_fold"][k] == sq.weights_.tolist()
        assert r.model_info["sl_propensity_weights_by_fold"][k] == sg.weights_.tolist()
    # Two-learner library: the weights are informative, not trivially [1.0].
    assert any(0 < w[0] < 1 for w in r.model_info["sl_outcome_weights_by_fold"]) or any(
        0 < w[0] < 1 for w in r.model_info["sl_propensity_weights_by_fold"]
    )


def test_super_learner_failure_names_the_fold():
    df = _data()
    folds = _folds(len(df))
    # Binary outcome whose only 3 positives sit in fold 0: fold 0's
    # training complement has a single outcome class.
    y = np.zeros(len(df))
    y[np.flatnonzero(folds == 0)[:3]] = 1.0
    df["y"] = y
    with pytest.raises(DataInsufficient, match="fold 0") as info:
        _fit(df, fold_indices=folds)
    assert info.value.diagnostics["cv_fold"] == 0


def test_cv_tmle_differs_from_in_sample_fit():
    df = _data()
    a = _fit(df)
    b = _fit(df, fold_indices=_folds(len(df)))
    assert a.estimate != b.estimate


def test_cv_tmle_aligns_folds_with_input_rows_when_rows_are_dropped():
    df = _data()
    folds = _folds(len(df))
    dirty = df.copy()
    dirty.loc[[3, 50], "x2"] = np.nan
    keep = dirty[COV].notna().all(axis=1).to_numpy()
    r_dirty = _fit(dirty, fold_indices=folds)
    r_clean = _fit(df[keep].reset_index(drop=True), fold_indices=folds[keep])
    assert r_dirty.estimate == r_clean.estimate
    assert r_dirty.se == r_clean.se


def test_cv_tmle_binary_outcome_and_att_run():
    df = _data(n=600)
    df["y"] = (df["y"] > df["y"].median()).astype(float)
    r = _fit(df, fold_indices=_folds(len(df), k=3), estimand="ATT")
    assert np.isfinite(r.estimate) and r.se > 0
    assert r.model_info["n_cv_folds"] == 3


# ---------------------------------------------------------------------------
# (c) invalid fold vectors raise
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        lambda n: np.zeros(n - 1, dtype=int),  # wrong length
        lambda n: np.zeros(n, dtype=int),  # one fold
        lambda n: (np.arange(n) % 3) + 1,  # labels 1..3, not 0..2
        lambda n: np.where(np.arange(n) % 2, 0, 2),  # labels {0, 2}
        lambda n: (np.arange(n) % 2) + 0.5,  # non-integer
        lambda n: np.where(np.arange(n) == 0, np.nan, np.arange(n) % 2),
        lambda n: (np.arange(n) % 2).astype(bool),  # bool, not labels
        lambda n: np.arange(n).reshape(-1, 1) % 2,  # 2-D
    ],
)
def test_invalid_fold_vectors_raise(bad):
    df = _data()
    with pytest.raises(MethodIncompatibility):
        _fit(df, fold_indices=bad(len(df)))


def test_fold_whose_training_complement_has_one_arm_raises():
    df = _data()
    folds = np.where(df["d"].to_numpy() == 1, 0, 1)  # train of fold 1 = treated only
    with pytest.raises(DataInsufficient):
        _fit(df, fold_indices=folds)


def test_fold_indices_with_supplied_nuisances_raise():
    df = _data()
    n = len(df)
    with pytest.raises(MethodIncompatibility):
        sp.tmle(
            df,
            y="y",
            treat="d",
            covariates=COV,
            g1W=np.full(n, 0.5),
            fold_indices=_folds(n),
        )
