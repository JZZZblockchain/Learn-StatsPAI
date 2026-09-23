"""Causal forests on panel data: clusters and fixed effects.

Known-truth (tier T1) checks on a staggered-adoption panel in which units
select into early treatment on their fixed effect, so a pooled forest is
confounded while a forest that removes unit and period effects within nodes
is not; plus the input contracts of ``clusters=`` / ``fe=``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import statspai as sp
from statspai.exceptions import (
    AssumptionWarning,
    DataInsufficient,
    MethodIncompatibility,
)


def _panel(N=300, T=6, seed=0, hetero=True, drop=0.0):
    rng = np.random.default_rng(seed)
    Xu = rng.standard_normal((N, 3))
    nu = rng.standard_normal(N)
    alpha = 2 * Xu[:, 0] + 2 * nu
    score = nu + 0.5 * Xu[:, 0] + 0.5 * rng.standard_normal(N)
    adopt = np.where(
        score > 1.0, 2, np.where(score > 0.0, 3, np.where(score > -0.7, 4, 99))
    )
    gamma = rng.standard_normal(T) * 2
    unit = np.repeat(np.arange(N), T)
    t = np.tile(np.arange(T), N)
    D = (t >= adopt[unit]).astype(float)
    tau = 1 + Xu[unit, 0] if hetero else np.ones(N * T)
    Y = alpha[unit] + gamma[t] + tau * D + rng.standard_normal(N * T)
    df = pd.DataFrame(Xu[unit], columns=["x1", "x2", "x3"])
    df["y"], df["d"], df["id"], df["t"], df["tau"] = Y, D, unit, t, tau
    if drop:
        df = (
            df.sample(frac=1 - drop, random_state=seed)
            .sort_index()
            .reset_index(drop=True)
        )
    return df


def _fe_forest(df, **kw):
    return sp.causal_forest(
        data=df,
        y="y",
        d="d",
        x=["x1", "x2", "x3"],
        id="id",
        time="t",
        fe="twoway",
        n_estimators=kw.pop("n_estimators", 800),
        random_state=kw.pop("random_state", 0),
        **kw,
    )


@pytest.fixture(scope="module")
def homogeneous():
    df = _panel(seed=1, hetero=False)
    return df, _fe_forest(df)


@pytest.fixture(scope="module")
def heterogeneous():
    df = _panel(seed=2, hetero=True)
    return df, _fe_forest(df)


class TestFixedEffectsForest:
    def test_homogeneous_effect_is_recovered_without_spurious_heterogeneity(
        self, homogeneous
    ):
        df, cf = homogeneous
        tau_hat = cf.predict()
        treated = df["d"].to_numpy() == 1
        # T1: true effect is 1 everywhere.
        assert abs(tau_hat[treated].mean() - 1.0) < 0.15
        table = sp.calibration_test(cf)
        assert table.loc["differential_forest_prediction", "p_one_sided"] > 0.05

    def test_pooled_forest_is_confounded_by_the_fixed_effects(self, homogeneous):
        df, _ = homogeneous
        pooled = sp.causal_forest(
            data=df,
            y="y",
            d="d",
            x=["x1", "x2", "x3"],
            clusters="id",
            n_estimators=800,
            random_state=0,
        )
        treated = df["d"].to_numpy() == 1
        assert abs(pooled.predict()[treated].mean() - 1.0) > 0.5

    def test_heterogeneous_effect_is_recovered(self, heterogeneous):
        df, cf = heterogeneous
        tau = df["tau"].to_numpy()
        treated = df["d"].to_numpy() == 1
        tau_hat = cf.predict()
        assert abs(np.mean(tau_hat[treated] - tau[treated])) < 0.15
        assert np.corrcoef(tau_hat[treated], tau[treated])[0, 1] > 0.8
        assert np.sqrt(np.mean((tau_hat[treated] - tau[treated]) ** 2)) < 0.6
        table = sp.calibration_test(cf)
        assert table.loc["differential_forest_prediction", "p_one_sided"] < 0.01

    def test_variance_and_intervals_are_available(self, heterogeneous):
        df, cf = heterogeneous
        var = cf.effect_variance()
        assert var.shape == (len(df),) and np.all(var >= 0)
        lo, hi = cf.effect_interval(df[["x1", "x2", "x3"]].to_numpy()[:10])
        assert np.all(lo <= hi)

    def test_diagnostics_describe_the_panel(self, heterogeneous):
        _, cf = heterogeneous
        diag = cf.diagnostics
        assert diag["fe"] == "twoway"
        assert diag["n_units"] == 300 and diag["n_periods"] == 6
        assert diag["n_clusters"] == 300
        assert 0 < diag["share_units_switching_treatment"] < 1

    def test_doubly_robust_averages_are_refused(self, heterogeneous):
        # No propensity: the ATE over all cells and RATE stay refused; the
        # effect on treated cells and the BLP use imputation scores instead
        # (tests/test_forest_fe_imputation.py).
        df, cf = heterogeneous
        with pytest.raises(MethodIncompatibility, match="fixed effects"):
            cf.average_treatment_effect()
        with pytest.raises(MethodIncompatibility, match="fixed effects"):
            sp.rate(cf)
        effect = cf.ate()  # plug-in value survives, inference error recorded
        assert np.isfinite(float(effect))
        assert effect.inference_error is not None
        att = cf.average_treatment_effect("treated")
        treated = df["d"].to_numpy() == 1
        assert (
            abs(att["estimate"] - df["tau"].to_numpy()[treated].mean()) < 4 * att["se"]
        )
        assert list(cf.best_linear_projection().index)[0] == "Intercept"

    def test_calibrate_cate_warns_that_fe_slope_is_not_deattenuation(
        self, heterogeneous
    ):
        _, cf = heterogeneous
        with pytest.warns(AssumptionWarning, match="does not correct the shrinkage"):
            out = sp.calibrate_cate(cf, method="within")
        assert out["cate"].shape == cf.predict().shape
        assert sp.calibrate_cate(cf)["method"] == "blp_imputation"

    def test_unbalanced_panel(self):
        df = _panel(seed=3, hetero=True, drop=0.2)
        cf = _fe_forest(df, n_estimators=600)
        treated = df["d"].to_numpy() == 1
        tau = df["tau"].to_numpy()
        assert np.corrcoef(cf.predict()[treated], tau[treated])[0, 1] > 0.7

    def test_unit_fe_only(self):
        df = _panel(N=200, seed=4, hetero=False)
        # With only unit effects, the common period shocks confound the effect
        # in a staggered design; the fit must still run and report fe='unit'.
        cf = sp.causal_forest(
            data=df,
            y="y",
            d="d",
            x=["x1", "x2"],
            id="id",
            fe="unit",
            n_estimators=300,
            random_state=0,
        )
        assert cf.diagnostics["fe"] == "unit"
        assert cf.diagnostics["n_periods"] is None


class TestFixedEffectsContracts:
    def test_unit_is_required(self):
        df = _panel(N=50, T=4)
        with pytest.raises(MethodIncompatibility, match="unit="):
            sp.causal_forest(
                data=df, y="y", d="d", x=["x1"], fe="twoway", n_estimators=50
            )

    def test_time_is_required_for_twoway(self):
        df = _panel(N=50, T=4)
        with pytest.raises(MethodIncompatibility, match="time="):
            sp.causal_forest(
                data=df, y="y", d="d", x=["x1"], id="id", fe="twoway", n_estimators=50
            )

    def test_duplicate_unit_periods_are_refused(self):
        df = _panel(N=50, T=4)
        df = pd.concat([df, df.iloc[:5]], ignore_index=True)
        with pytest.raises(MethodIncompatibility, match="unique"):
            _fe_forest(df, n_estimators=50)

    def test_treatment_without_within_unit_variation_is_refused(self):
        df = _panel(N=50, T=4)
        df["d"] = (df["id"] % 2).astype(float)
        with pytest.raises(DataInsufficient, match="does not vary within units"):
            _fe_forest(df, n_estimators=50)

    def test_clusters_must_nest_units(self):
        df = _panel(N=50, T=4)
        with pytest.raises(MethodIncompatibility, match="nest units"):
            _fe_forest(df, n_estimators=50, clusters=df["t"].to_numpy())

    def test_unit_without_fe_is_refused(self):
        df = _panel(N=50, T=4)
        with pytest.raises(MethodIncompatibility, match="only used with fe"):
            sp.causal_forest(data=df, y="y", d="d", x=["x1"], id="id", n_estimators=50)

    def test_fe_requires_the_grf_engine(self):
        df = _panel(N=50, T=4)
        with pytest.warns(DeprecationWarning):
            with pytest.raises(MethodIncompatibility, match="split_rule='grf'"):
                _fe_forest(df, n_estimators=50, split_rule="legacy")

    def test_bad_fe_value(self):
        df = _panel(N=50, T=4)
        with pytest.raises(MethodIncompatibility, match="fe must be"):
            sp.causal_forest(
                data=df, y="y", d="d", x=["x1"], id="id", fe="both", n_estimators=50
            )

    def test_missing_column_names(self):
        df = _panel(N=50, T=4)
        with pytest.raises(MethodIncompatibility, match="not a column"):
            sp.causal_forest(
                data=df, y="y", d="d", x=["x1"], id="firm", fe="unit", n_estimators=50
            )


class TestClusteredForest:
    def _clustered(self, seed=0):
        rng = np.random.default_rng(seed)
        G, m = 100, 10
        g = np.repeat(np.arange(G), m)
        X = rng.normal(size=(G * m, 3))
        shock = rng.normal(scale=1.5, size=G)[g]
        W = (rng.uniform(size=G) < 0.5)[g].astype(float)  # cluster-level assignment
        Y = X[:, 0] + shock + (1 + X[:, 1]) * W + rng.normal(size=G * m)
        return X, W, Y, g

    def test_cluster_robust_se_exceeds_iid_se_under_cluster_assignment(self):
        X, W, Y, g = self._clustered()
        iid = sp.causal_forest(Y=Y, T=W, X=X, n_estimators=600, random_state=0)
        clu = sp.causal_forest(
            Y=Y, T=W, X=X, clusters=g, n_estimators=600, random_state=0
        )
        se_iid = iid.average_treatment_effect()["se"]
        res = clu.average_treatment_effect()
        assert res["n_clusters"] == 100
        # Treatment and outcome shocks are shared within clusters, so the
        # clustered SE must be materially larger.
        assert res["se"] > 1.5 * se_iid

    def test_user_nuisance_models_are_cross_fitted_by_cluster(self):
        from sklearn.linear_model import LinearRegression, LogisticRegression

        X, W, Y, g = self._clustered(seed=1)
        cf = sp.causal_forest(
            Y=Y,
            T=W,
            X=X,
            clusters=g,
            n_estimators=200,
            random_state=0,
            model_y=LinearRegression(),
            model_t=LogisticRegression(),
        )
        assert "cross-fitted" in cf.diagnostics["nuisance_source"]["Y_hat"]
        assert np.all((cf._e_insample >= 0) & (cf._e_insample <= 1))

    def test_precomputed_nuisances(self):
        X, W, Y, g = self._clustered(seed=2)
        cf = sp.causal_forest(
            Y=Y,
            T=W,
            X=X,
            clusters=g,
            n_estimators=200,
            random_state=0,
            Y_hat=np.full(len(Y), Y.mean()),
            W_hat=0.5,
        )
        assert cf.diagnostics["nuisance_source"] == {
            "Y_hat": "user-supplied",
            "W_hat": "user-supplied",
        }
        np.testing.assert_array_equal(cf._e_insample, 0.5)

    def test_cluster_contracts(self):
        X, W, Y, g = self._clustered()
        with pytest.raises(MethodIncompatibility, match="one label per row"):
            sp.causal_forest(Y=Y, T=W, X=X, clusters=g[:-1], n_estimators=50)
        with pytest.raises(DataInsufficient, match="at least two clusters"):
            sp.causal_forest(Y=Y, T=W, X=X, clusters=np.zeros(len(Y)), n_estimators=50)
        with pytest.raises(MethodIncompatibility, match="Y_hat"):
            sp.causal_forest(Y=Y, T=W, X=X, Y_hat=np.ones(3), n_estimators=50)
        with pytest.raises(MethodIncompatibility, match="bootstrap"):
            sp.causal_forest(Y=Y, T=W, X=X, n_estimators=50, bootstrap=True)

    def test_equalize_cluster_weights_changes_observation_weights(self):
        rng = np.random.default_rng(5)
        sizes = rng.integers(2, 20, size=80)
        g = np.repeat(np.arange(80), sizes)
        X = rng.normal(size=(g.size, 2))
        W = rng.integers(0, 2, g.size).astype(float)
        Y = X[:, 0] * W + rng.normal(size=g.size)
        cf = sp.causal_forest(
            Y=Y,
            T=W,
            X=X,
            clusters=g,
            equalize_cluster_weights=True,
            n_estimators=200,
            random_state=0,
        )
        w = cf._observation_weight
        np.testing.assert_allclose(np.bincount(g, weights=w), 1 / 80)

    def test_max_samples_above_half_disables_variance_with_warning(self):
        X, W, Y, _ = self._clustered()
        with pytest.warns(AssumptionWarning, match="little bags"):
            cf = sp.causal_forest(Y=Y, T=W, X=X, n_estimators=50, max_samples=0.7)
        assert cf.ci_group_size == 1
        with pytest.raises(MethodIncompatibility, match="ci_group_size"):
            cf.effect_variance()

    def test_legacy_split_rule_is_deprecated_but_reproducible(self):
        X, W, Y, _ = self._clustered()
        with pytest.warns(DeprecationWarning, match="legacy"):
            a = sp.causal_forest(
                Y=Y, T=W, X=X, n_estimators=10, random_state=0, split_rule="legacy"
            )
        with pytest.warns(DeprecationWarning):
            b = sp.causal_forest(
                Y=Y, T=W, X=X, n_estimators=10, random_state=0, split_rule="legacy"
            )
        np.testing.assert_array_equal(a.effect(X), b.effect(X))
        assert a.diagnostics["engine"] == "legacy"

    def test_compare_estimators_includes_the_forest(self):
        # Regression: compare_estimators passed treatment=/covariates= to
        # sp.causal_forest, which accepts neither, so the forest row was
        # silently dropped from every comparison.
        X, W, Y, g = self._clustered(seed=6)
        df = pd.DataFrame(X, columns=["x1", "x2", "x3"])
        df["d"], df["y"], df["id"] = W.astype(int), Y, g
        cmp = sp.compare_estimators(
            df,
            y="y",
            treatment="d",
            covariates=["x1", "x2", "x3"],
            methods=["ols", "causal_forest"],
            id="id",
        )
        assert "Causal Forest" in cmp.results
        forest = cmp.results["Causal Forest"]
        assert forest.diagnostics["n_clusters"] == 100


def test_causal_forest_accepts_unit_alias_and_calibrate_accepts_x_alias():
    df = _panel(N=60, T=4, seed=9)
    a = sp.causal_forest(
        data=df,
        y="y",
        d="d",
        x=["x1"],
        unit="id",
        time="t",
        fe="twoway",
        n_estimators=100,
        random_state=0,
    )
    b = sp.causal_forest(
        data=df,
        y="y",
        d="d",
        x=["x1"],
        id="id",
        time="t",
        fe="twoway",
        n_estimators=100,
        random_state=0,
    )
    np.testing.assert_array_equal(a.predict(), b.predict())
    rng = np.random.default_rng(0)
    X = rng.normal(size=(400, 2))
    T = rng.integers(0, 2, 400)
    Y = X[:, 0] * T + rng.normal(size=400)
    cf = sp.causal_forest(Y=Y, T=T, X=X, n_estimators=200, random_state=0)
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        by_alias = sp.calibrate_cate(cf, X=X[:5])
        by_name = sp.calibrate_cate(cf, newdata=X[:5])
    np.testing.assert_array_equal(by_alias["cate"], by_name["cate"])
