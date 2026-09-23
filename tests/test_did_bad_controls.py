"""Bad controls: DR / IPW cells, not-yet-treated comparisons, analytic SE.

Evidence tiers. The regression cell with never-treated comparisons is the
estimator this module already shipped, pinned against R ``ptetools`` /
``did`` in ``tests/reference_parity/test_did_synth_didvar_parity.py``; the
tests here hold that path numerically fixed (T2 preserved) and check the new
paths on a DGP where the truth is known (T1): a bad control that the
treatment moves, an outcome whose untreated path depends on the covariate,
and selection into treatment on the pre-treatment covariate.
"""

import numpy as np
import pandas as pd
import pytest

import statspai as sp


def _bad_control_panel(rng, *, n=400, T=6, tau=1.0, selection=1.0, gamma=0.8):
    """Panel where X is a genuine bad control and the design is exact.

    The latent covariate ``X(0)`` is an AR(1); the observed covariate is
    ``X(0) + 1.5 * D``, so the treatment moves it -- that is what makes it a
    bad control.  The untreated outcome loads on the *contemporaneous*
    ``X(0)``, so X is also a genuine control, and because ``X(0)`` is Markov,
    ``E[Y_t(0) - Y_{g-1}(0) | X_{g-1}]`` is linear in the frozen covariate
    and the same for every cohort: conditional parallel trends given
    ``X_{g-1}`` holds exactly, which is what makes the planted ``tau``
    recoverable and a departure from it a real error.

    Adoption probability rises in ``X`` at period 1, so the cohorts are
    selected on the covariate and an unadjusted comparison is biased --
    early enough that every cell's frozen baseline sits at or after the
    selection period, which is what keeps the Markov argument (and the
    covariate placebo) exact.
    """
    rows = []
    for i in range(n):
        x = np.empty(T)
        x[0] = rng.normal()
        for k in range(1, T):
            x[k] = 0.7 * x[k - 1] + rng.normal(0, 0.7)
        p = 1.0 / (1.0 + np.exp(-selection * x[0]))
        g = int(
            rng.choice([3, 4, 5, 0], p=[0.25 * p, 0.25 * p, 0.25 * p, 1 - 0.75 * p])
        )
        a = rng.normal()
        for k in range(T):
            t = k + 1
            d = 1.0 if (g > 0 and t >= g) else 0.0
            rows.append(
                {
                    "i": i,
                    "t": t,
                    "g": g,
                    "x": x[k] + 1.5 * d,  # the treatment moves the covariate
                    "y": (a + 0.3 * t + gamma * x[k] + tau * d + rng.normal(0, 0.5)),
                }
            )
    return pd.DataFrame(rows)


def _fit(df, **kw):
    return sp.did_timevarying_covariates(
        df, y="y", unit="i", time="t", cohort="g", covariates=["x"], **kw
    )


def test_reg_nevertreated_bootstrap_is_unchanged():
    """The shipped default must keep its number to the last bit."""
    rng = np.random.default_rng(0)
    df = _bad_control_panel(rng, n=120)
    a = _fit(df, n_boot=25, seed=3)
    b = _fit(
        df,
        n_boot=25,
        seed=3,
        est_method="reg",
        control_group="nevertreated",
        vce="bootstrap",
    )
    assert a.estimate == pytest.approx(b.estimate, rel=0, abs=0)
    assert a.se == pytest.approx(b.se, rel=0, abs=0)


def test_every_est_method_recovers_the_planted_effect():
    rng = np.random.default_rng(1)
    df = _bad_control_panel(rng, n=600, tau=1.0)
    for method in ("reg", "ipw", "dr"):
        r = _fit(df, est_method=method, vce="analytic")
        assert abs(r.estimate - 1.0) < 3 * r.se, method


def test_analytic_se_agrees_with_the_bootstrap():
    rng = np.random.default_rng(2)
    df = _bad_control_panel(rng, n=400)
    an = _fit(df, vce="analytic")
    bs = _fit(df, n_boot=200, seed=5)
    assert an.estimate == pytest.approx(bs.estimate, rel=1e-12)
    assert an.se == pytest.approx(bs.se, rel=0.25)


def test_notyettreated_uses_more_comparison_units():
    rng = np.random.default_rng(3)
    df = _bad_control_panel(rng, n=300)
    never = _fit(df, vce="analytic")
    notyet = _fit(df, vce="analytic", control_group="notyettreated")
    n_never = pd.DataFrame(never.detail)["n_control"].sum()
    n_notyet = pd.DataFrame(notyet.detail)["n_control"].sum()
    assert n_notyet > n_never
    assert abs(notyet.estimate - never.estimate) < 3 * never.se


def test_covariate_pretest_recovers_the_planted_shift_and_clears_the_placebo():
    """The treatment moves X by exactly 1.5; nothing moves it before."""
    rng = np.random.default_rng(4)
    df = _bad_control_panel(rng, n=600)
    r = _fit(df, vce="analytic", covariate_pretest=True)
    pre = r.model_info["covariate_pretest"]["x"]
    # X is a genuine bad control, and the statistic reads off how bad.
    assert pre["post"] == pytest.approx(1.5, abs=3 * pre["post_se"])
    assert pre["post_pvalue"] < 1e-6
    # The placebo, one period earlier and entirely pre-treatment, is zero.
    assert abs(pre["pre"]) < 3 * pre["pre_se"]
    assert pre["pre_pvalue"] > 0.05


def test_contemporaneous_adjustment_is_the_thing_this_avoids():
    """Controlling for X_t -- the practice the paper argues against.

    The treatment raises X by 1.5 and the outcome loads on X with
    coefficient gamma, so a two-way fixed-effects regression that conditions
    on the *contemporaneous* covariate absorbs part of the effect it is
    trying to measure.  The frozen-baseline estimator does not.
    """
    rng = np.random.default_rng(5)
    df = _bad_control_panel(rng, n=600, tau=1.0, gamma=0.8)
    df = df.assign(d=((df["g"] > 0) & (df["t"] >= df["g"])).astype(float))
    good = _fit(df, est_method="dr", vce="analytic")
    bad = sp.feols("y ~ d + x | i + t", data=df, vcov={"CRV1": "i"})
    bad_att = float(np.asarray(bad.params["d"]))

    assert abs(good.estimate - 1.0) < 3 * good.se
    # 1.5 * 0.8 = 1.2 of the effect is routed through the covariate.
    assert bad_att < 0.5
    assert abs(bad_att - 1.0) > abs(good.estimate - 1.0)


@pytest.mark.parametrize(
    "kwargs, match",
    [
        ({"est_method": "ml"}, "est_method"),
        ({"control_group": "everyone"}, "control_group"),
        ({"vce": "jackknife"}, "vce"),
    ],
)
def test_argument_errors(kwargs, match):
    rng = np.random.default_rng(6)
    df = _bad_control_panel(rng, n=80)
    with pytest.raises(sp.MethodIncompatibility, match=match):
        _fit(df, n_boot=5, **kwargs)
