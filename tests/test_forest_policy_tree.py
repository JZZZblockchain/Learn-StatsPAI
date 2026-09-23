"""Policy learning on a fixed-effects forest's imputation scores.

``sp.policy_tree`` maximises a doubly-robust objective and so needs a
propensity. A within-unit design has none; the imputation scores that give
the ATT serve instead, which fixes the population to the treated cells and
makes the rule *retrospective*. These tests pin that estimand, the exact
variance of the three functionals the result reports, and the reason the
rule is fitted and priced on disjoint units.
"""

import warnings

import numpy as np
import pandas as pd
import pytest

import statspai as sp
from statspai.exceptions import (
    AssumptionWarning,
    DataInsufficient,
    MethodIncompatibility,
)
from statspai.forest import _fe_imputation as fi

TAU0, SLOPE = 0.3, 0.8


def panel(seed=0, n_units=220, n_periods=8, slope=SLOPE):
    """tau = TAU0 + slope * z, with z independent of adoption."""
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_units):
        a, z, w = rng.normal(), rng.normal(), rng.normal()
        never = i % 5 == 0
        g = 10**6 if never else int(np.clip(4 + round(a), 3, n_periods))
        for t in range(1, n_periods + 1):
            d = 1.0 * (t >= g)
            y = a + 0.25 * t + (TAU0 + slope * z) * d + rng.normal(0, 0.6)
            rows.append((i, t, y, d, z, w))
    return pd.DataFrame(rows, columns=["id", "t", "y", "d", "z", "w"])


def _forest(df, **kw):
    kw.setdefault("n_estimators", 250)
    kw.setdefault("random_state", 0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return sp.causal_forest(
            "y ~ d | z + w",
            data=df,
            fe="twoway",
            unit="id",
            time="t",
            clusters=df["id"].to_numpy(),
            **kw,
        )


@pytest.fixture(scope="module")
def fe_forest():
    df = panel()
    return _forest(df), df


# --------------------------------------------------------------------------- #
#  The rule
# --------------------------------------------------------------------------- #


def test_finds_the_threshold_the_cost_implies(fe_forest):
    # tau = 0.3 + 0.8 z exceeds a cost c exactly when z > (c - 0.3) / 0.8,
    # so the depth-1 split has a known place to be.
    cf, _ = fe_forest
    for cost, want in ((0.3, 0.0), (0.9, 0.75)):
        res = sp.forest_policy_tree(cf, depth=1, cost=cost, random_state=0)
        tree = res["tree"]
        assert tree["type"] == "split"
        assert res["policy_covariates"][tree["feature"]] == "z"
        assert abs(tree["threshold"] - want) < 0.25, (cost, tree)


def test_a_higher_cost_treats_fewer_cells(fe_forest):
    cf, _ = fe_forest
    shares = [
        sp.forest_policy_tree(cf, depth=1, cost=c, n_splits=3, random_state=0)[
            "share_treated"
        ]
        for c in (0.0, 0.3, 0.9)
    ]
    assert shares[0] > shares[1] > shares[2]
    assert all(0.0 <= s <= 1.0 for s in shares)


def test_depth_two_is_searched_exactly_and_deeper_is_greedy(fe_forest):
    cf, _ = fe_forest
    assert "exact" in sp.forest_policy_tree(cf, depth=2, cost=0.3, n_splits=3)["method"]
    assert (
        "greedy" in sp.forest_policy_tree(cf, depth=3, cost=0.3, n_splits=3)["method"]
    )


def test_policy_covariates_can_be_restricted(fe_forest):
    cf, _ = fe_forest
    res = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3, x=["z"])
    assert res["policy_covariates"] == ["z"]
    assert res["tree"]["feature"] == 0


def test_unknown_policy_covariate_names_the_column(fe_forest):
    cf, _ = fe_forest
    with pytest.raises(MethodIncompatibility, match="nope"):
        sp.forest_policy_tree(cf, x=["nope"])


# --------------------------------------------------------------------------- #
#  What the rule was worth
# --------------------------------------------------------------------------- #


def test_the_gain_is_exactly_the_difference_within_one_split(fe_forest):
    # The three values are functionals of one y, computed from one design,
    # so the gain's *estimate* is exactly the difference. Its *variance* is
    # not the difference of theirs: the BJS centring weights the cohort x
    # event-time mean by each functional's own v^2, and the gain's weights
    # vanish on every cell the rule treats, so it is centred on the withheld
    # cells alone. Coverage of both readings is measured in
    # tests/reference_parity/test_fe_forest_policy_recovery.py.
    cf, _ = fe_forest
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", AssumptionWarning)
        res = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=1, random_state=0)
    v, allv, gain = res["value"], res["value_treat_all"], res["gain_over_treat_all"]
    np.testing.assert_allclose(
        gain["estimate"], v["estimate"] - allv["estimate"], rtol=0, atol=1e-10
    )
    vcov = res["diagnostics"]["vcov"]
    assert vcov.shape == (3, 3)
    np.testing.assert_allclose(vcov, vcov.T, rtol=0, atol=1e-18)
    np.testing.assert_allclose(gain["se"], np.sqrt(vcov[2, 2]), rtol=1e-10)
    assert gain["se"] > 0
    # Not the naive sum of variances either, which ignores the covariance.
    assert gain["se"] < np.sqrt(v["se"] ** 2 + allv["se"] ** 2)
    # The contrast reading is reported alongside so a caller who rebuilds it
    # from vcov sees a labelled alternative rather than a discrepancy.
    contrast = float(np.sqrt(np.array([1.0, -1.0, 0.0]) @ vcov @ [1.0, -1.0, 0.0]))
    np.testing.assert_allclose(
        res["diagnostics"]["gain_se_contrast"], contrast, rtol=1e-12
    )
    assert res["diagnostics"]["gain_se_contrast"] != gain["se"]


def test_treat_all_value_is_the_att_minus_the_cost(fe_forest):
    cf, _ = fe_forest
    cost = 0.3
    res = sp.forest_policy_tree(cf, depth=1, cost=cost, random_state=0)
    # The evaluation half's own ATT: the same functional with pi == 1.
    eval_att = res["value_treat_all"]["estimate"] + cost
    assert 0.0 < eval_att < 1.0
    # Positive effects on average, so treating everyone is worth something.
    assert res["value_treat_all"]["estimate"] > -cost


def test_a_rule_that_treats_everyone_has_exactly_zero_gain(fe_forest):
    # Structurally zero, not "could not be estimated": reporting NaN here
    # would be wrong, and did happen before the degenerate case was handled.
    cf, _ = fe_forest
    res = sp.forest_policy_tree(cf, depth=1, cost=-5.0, n_splits=3, random_state=0)
    assert res["share_treated"] == 1.0
    gain = res["gain_over_treat_all"]
    assert gain["estimate"] == 0.0
    assert gain["se"] == 0.0
    assert gain["p"] == 1.0
    assert not np.isnan(gain["ci_low"]) and not np.isnan(gain["ci_high"])


def test_gain_is_detected_when_the_heterogeneity_is_real(fe_forest):
    cf, _ = fe_forest
    gain = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3, random_state=0)[
        "gain_over_treat_all"
    ]
    assert gain["estimate"] > 0 and gain["ci_low"] > 0


def test_no_heterogeneity_leaves_nothing_for_the_rule_to_find():
    # tau constant and cost equal to it: every rule is worth exactly 0.
    cf = _forest(panel(seed=7, slope=0.0))
    res = sp.forest_policy_tree(cf, depth=1, cost=TAU0, random_state=3)
    gain = res["gain_over_treat_all"]
    assert abs(gain["estimate"]) < 4 * max(gain["se"], 1e-12) or gain["se"] == 0.0


# --------------------------------------------------------------------------- #
#  Splitting, and the contracts
# --------------------------------------------------------------------------- #


def test_fitting_and_pricing_use_disjoint_units(fe_forest):
    cf, df = fe_forest
    res = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3, random_state=0)
    assert res["split_by"] == "units"
    assert res["n_train_units"] + res["n_eval_units"] == df["id"].nunique()
    assert res["n_cells_fitted"] > 0 and res["n_cells_priced"] > 0
    assert len(res["policy"]) == res["n_cells_priced"]
    assert set(np.unique(res["policy"])) <= {0, 1}


def test_the_result_is_reproducible_given_random_state(fe_forest):
    cf, _ = fe_forest
    a = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3, random_state=11)
    b = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3, random_state=11)
    assert a["value"]["estimate"] == b["value"]["estimate"]


def test_medians_over_splits_do_not_satisfy_the_arithmetic_identity(fe_forest):
    # Documented, not a bug: each feature is VEIN-aggregated on its own, and
    # a median of differences is not a difference of medians. Anyone who
    # subtracts the two values and compares with the gain should find this
    # stated rather than discover it.
    cf, _ = fe_forest
    res = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=5, random_state=0)
    diff = res["value"]["estimate"] - res["value_treat_all"]["estimate"]
    assert res["gain_over_treat_all"]["estimate"] != diff


def test_split_stability_is_reported(fe_forest):
    # A tight interval on the value of a rule that changes from split to
    # split is not evidence for that rule.
    cf, _ = fe_forest
    res = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=5, random_state=0)
    stab = res["diagnostics"]["split_stability"]
    assert sum(stab["root_covariate_counts"].values()) == 5
    assert 0.0 < stab["root_covariate_modal_share"] <= 1.0
    assert stab["threshold_min"] <= stab["threshold_max"]
    assert stab["share_treated_min"] <= stab["share_treated_max"]
    assert res["representative_split"] in range(5)


def test_one_split_warns_that_it_is_a_draw(fe_forest):
    cf, _ = fe_forest
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        res = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=1)
    hits = [w for w in rec if "one draw" in str(w.message)]
    assert len(hits) == 1 and issubclass(hits[0].category, AssumptionWarning)
    assert res["value"]["n_splits"] == 1


@pytest.mark.parametrize("bad", [0, -1, 2.5, True])
def test_bad_n_splits_is_refused(fe_forest, bad):
    cf, _ = fe_forest
    with pytest.raises(MethodIncompatibility, match="n_splits"):
        sp.forest_policy_tree(cf, n_splits=bad)


def test_train_frac_moves_the_halves(fe_forest):
    cf, _ = fe_forest
    small = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3, train_frac=0.3)
    large = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3, train_frac=0.7)
    assert small["n_train_units"] < large["n_train_units"]
    assert small["n_cells_fitted"] < large["n_cells_fitted"]


@pytest.mark.parametrize("bad", [0.0, 1.0, -0.2])
def test_degenerate_train_frac_is_refused(fe_forest, bad):
    cf, _ = fe_forest
    with pytest.raises(MethodIncompatibility, match="train_frac"):
        sp.forest_policy_tree(cf, train_frac=bad)


@pytest.mark.parametrize("bad", [0, -1, 2.5, True])
def test_bad_depth_is_refused(fe_forest, bad):
    cf, _ = fe_forest
    with pytest.raises(MethodIncompatibility, match="depth"):
        sp.forest_policy_tree(cf, depth=bad)


def test_pooled_forests_are_sent_to_the_doubly_robust_version():
    rng = np.random.default_rng(2)
    n = 400
    X = rng.normal(size=(n, 2))
    T = rng.binomial(1, 0.5, size=n)
    Y = X[:, 0] + (1 + X[:, 0]) * T + rng.normal(scale=0.5, size=n)
    df = pd.DataFrame({"y": Y, "d": T, "x0": X[:, 0], "x1": X[:, 1]})
    cf = sp.causal_forest("y ~ d | x0 + x1", data=df, n_estimators=100, random_state=0)
    with pytest.raises(MethodIncompatibility, match="sp.policy_tree"):
        sp.forest_policy_tree(cf)


def test_a_panel_too_small_to_split_says_so():
    cf = _forest(panel(seed=4, n_units=14, n_periods=5), n_estimators=80)
    with pytest.raises((DataInsufficient, MethodIncompatibility)) as exc:
        sp.forest_policy_tree(cf, depth=1, min_leaf_size=200)
    assert "forest_policy_tree()" in str(exc.value)


def test_thin_halves_warn():
    cf = _forest(panel(seed=5, n_units=40), n_estimators=120)
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3)
    hits = [w for w in rec if "close to noise" in str(w.message)]
    assert len(hits) == 1 and issubclass(hits[0].category, AssumptionWarning)


def test_rules_are_printable_and_name_the_covariates(fe_forest):
    cf, _ = fe_forest
    res = sp.forest_policy_tree(cf, depth=1, cost=0.3, n_splits=3)
    assert "z" in res["rules"]
    assert "TREAT" in res["rules"]
    assert "treated cells" in res["estimand"]


def test_imputation_covariates_reach_the_scores():
    # covariates="auto" only picks up what varies *within* units; z and w
    # above are fixed per unit and absorbed by the unit effect, so the panel
    # needs a time-varying column for this to be visible.
    df = panel(seed=9, n_units=160)
    rng = np.random.default_rng(1)
    df["gdp"] = rng.normal(size=len(df)) + 0.1 * df["t"]
    df["y"] = df["y"] + 0.4 * df["gdp"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cf = sp.causal_forest(
            "y ~ d | z + w + gdp",
            data=df,
            fe="twoway",
            unit="id",
            time="t",
            clusters=df["id"].to_numpy(),
            n_estimators=150,
            random_state=0,
        )
        res = sp.forest_policy_tree(
            cf, depth=1, cost=0.3, n_splits=2, covariates="auto"
        )
    assert "gdp" in res["diagnostics"]["imputation_covariates"]


def test_policy_must_match_the_priced_cells(fe_forest):
    from statspai.forest.forest_heterogeneity import _policy_functional

    cf, _ = fe_forest
    with pytest.raises(MethodIncompatibility, match="one action per treated cell"):
        _policy_functional(
            cf,
            np.ones(3),
            cost=0.0,
            variance="bjs",
            cluster=None,
            members=None,
            covariates="none",
            alpha=0.05,
            context="test",
        )
    design = fi.imputation_design(cf, "test", "none")
    m = int(design.target.sum())
    with pytest.raises(MethodIncompatibility, match="must be 0/1"):
        _policy_functional(
            cf,
            np.full(m, 0.5),
            cost=0.0,
            variance="bjs",
            cluster=None,
            members=None,
            covariates="none",
            alpha=0.05,
            context="test",
        )


def test_is_registered():
    assert sp.describe_function("forest_policy_tree") is not None
