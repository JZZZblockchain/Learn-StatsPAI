# Heterogeneous effects with panel data: causal forests with clusters, fixed effects and DiD

A causal forest estimates the conditional average treatment effect
`tau(x)`. On panel or grouped data three things can go wrong, and StatsPAI
has one tool for each:

| Your data | Risk | Use |
| --- | --- | --- |
| Cross-section, independent units | — | `sp.causal_forest(...)` |
| Several rows per unit / firm / school | honesty and SEs assume independent rows | `sp.causal_forest(..., clusters="unit")` |
| Panel, treatment switches within units, selection on unit characteristics | unit and period effects masquerade as heterogeneity | `sp.causal_forest(..., fe="twoway", id=..., time=...)`, then `sp.forest_group_effects` / `sp.cate_pretrend_test` |
| Staggered adoption, effects that change with exposure | pooled comparisons use already-treated units as controls | `sp.did_forest(...)` |

All three share one engine, an implementation of generalized random forests
[athey2019generalized; wager2018estimation].

## 1. Why a pooled or globally demeaned forest fails

Take `Y_it = alpha_i + gamma_t + tau(X_i) D_it + e_it`.

* **Pooled forest.** If adoption depends on `alpha_i`, the forest splits on
  covariates correlated with `alpha_i` and reports level differences as
  effect differences.
* **Global two-way demeaning, then a forest.** Unit demeaning is harmless,
  but subtracting period means subtracts the cross-sectional mean of
  `tau(X_j) D_jt` over *all* units `j`. The demeaned outcome no longer equals
  `tau(X_i)` times the demeaned treatment unless `tau` is constant, so the
  forest fits a misspecified model exactly when there is heterogeneity to find.
* **Node-level demeaning** [kattenberg2023causal] removes the effects inside
  each node and each leaf. Units in a node have similar `x`, so `tau` is
  nearly constant there and the within regression is correctly specified.

StatsPAI's own simulation (N = 300 units, T = 6, three adoption cohorts plus
never-treated, adoption selected on the unit effect, 4 seeds, estimates on
treated rows):

| | pooled forest (clusters = unit) | `fe="twoway"` |
| --- | --- | --- |
| bias, constant effect | +0.36 to +2.37 | -0.02 to +0.03 |
| bias, `tau = 1 + x1` | +0.34 to +2.36 | -0.06 to +0.02 |
| RMSE, `tau = 1 + x1` | 0.76 to 2.41 | 0.32 to 0.42 |
| heterogeneity test p (constant effect) | 0.00 to 0.91 | 0.06 to 0.86 |

## 2. Clustered forests

```python
import statspai as sp

cf = sp.causal_forest(
    data=df, y="wage", d="training", x=["age", "educ", "tenure"],
    clusters="firm",
)
cf.average_treatment_effect()          # AIPW ATE, cluster-robust SE
cf.average_treatment_effect("treated") # ATT
sp.calibration_test(cf)                # heterogeneity test, cluster-robust
cf.best_linear_projection()            # which covariates drive tau(x)
cf.effect_interval(X_new)              # pointwise CIs
```

With `clusters=` every tree draws whole clusters, honest halves are split by
cluster, user-supplied nuisance models are cross-fitted in folds that never
split a cluster, and every average, calibration test, BLP and RATE uses
cluster-robust variances. `equalize_cluster_weights=True` gives clusters equal
weight.

## 3. Causal forests with fixed effects

```python
cf = sp.causal_forest(
    data=panel, y="y", d="treated", x=["x1", "x2", "x3"],
    id="county", time="year", fe="twoway",
)
tau_hat = cf.predict()                 # out-of-bag CATE per row
cf.effect_variance()                   # little-bag variances
sp.calibration_test(cf)                # heterogeneity test
```

Requirements, all checked at fit time: `(unit, time)` pairs are unique,
the treatment varies within units, and `clusters` (default: the unit) nest
units. Unbalanced panels are fine.

### Which splitting rule

The default `split_rule="grf"` splits on the GRF gradient criterion applied
to the node-residualized data. `split_rule="cffe"` replaces it with the
criterion of [kattenberg2023causal] and the `causalfe` package
[aytug2026causalfe], which scores a candidate split by

```
n_L n_R / n^2 (tau_L - tau_R)^2,   tau = sum(D~ Y~) / sum(D~^2)
```

on the parent node's residualized outcome and treatment. Use it to
reproduce that implementation; everything downstream (honest leaves,
little-bag variances, imputation scores) is unchanged, and the imputation
ATT does not depend on the forest at all.

That criterion compares ratios computed in the candidate children, so it
needs the shallow, large-leaf trees it was designed with. On the causalfe
package's own simulation (15 replications, 400 trees) its CATE RMSE was
0.74 with StatsPAI's defaults (`min_samples_leaf=5`, no depth cap) and 0.53
with `min_samples_leaf=20, max_depth=4`; the GRF criterion gave 0.50 under
both. StatsPAI warns when `cffe` is combined with deep default trees.

```python
cf = sp.causal_forest(
    data=panel, y="y", d="treated", x=["x1", "x2", "x3"],
    id="county", time="year", fe="twoway",
    split_rule="cffe", min_samples_leaf=20, max_depth=4,
)
```

### Averages, groups and tests: imputation scores

A within-unit design has no propensity `E[D | X]`, so the doubly-robust
(AIPW) scores behind a pooled forest's averages do not exist. The FE forest's
own model supplies another unbiased signal. Fit the unit and period effects
on the **untreated** cells only (plus any time-varying covariates, see
`controls` below) and impute each treated cell's untreated outcome
[borusyak2024revisiting]:

```
Gamma_it = Y_it - alpha_hat_i - gamma_hat_t        (treated cells)
```

`Gamma_it` is unbiased for that cell's effect under parallel trends and no
anticipation, whatever the heterogeneity: in `x`, in calendar time, or in
exposure. The forest becomes a *proxy* and `Gamma` the *signal*, the division
of labour of generic machine-learning inference [chernozhukov2025generic]:

```python
cf.average_treatment_effect("treated")    # imputation ATT
cf.best_linear_projection()               # Gamma on (1, X), treated cells
sp.calibration_test(cf)                   # Gamma on the OOB prediction
sp.calibrate_cate(cf)                     # de-attenuated predictions
sp.forest_group_effects(cf, by=...)       # group ATTs (see section 4)
```

* **The ATT is the imputation estimator.** On `mpdta` it equals
  `sp.did_imputation` to 1e-13, and with `variance="bjs"` so does its
  standard error (5e-15 relative), so it inherits that estimator's
  Stata / R parity.
* **Standard errors** come from the exact linear weights of the estimator
  (every quantity here is `v'y`), clustered by the forest's clusters.
  Treated residuals need a model of the heterogeneity. `variance="bjs"` uses
  cohort x event-time means (conservative). The default `variance="forest"`
  first subtracts the out-of-bag forest prediction, which never uses the
  unit's own data because trees draw whole units.
* **`controls`.** The default `controls="none"` is the pure two-way model,
  i.e. exactly `sp.did_imputation` without covariates. `controls="auto"`
  adds the effect modifiers and controls that vary within units to the
  untreated model linearly (time-invariant ones are absorbed by the unit
  effect); a list of names selects some of them. If a time-varying covariate
  such as GDP drives the outcome, leaving it out gives the untreated outcome
  unit-specific trends and biases every average (section 4); a covariate
  that itself responds to the treatment must stay out. The identity with
  `sp.did_imputation` holds for `controls="none"` (or covariates that do not
  vary within units).
* **Two-way only.** Imputation needs period ids, so it requires
  `fe="twoway"`; `fe="unit"` forests keep the within calibration regression
  and raise for the averages.
* **What stays unavailable.** `target_sample="all"`, `"control"` or
  `"overlap"` raise: parallel trends identifies effects on treated cells,
  and effects on untreated cells are extrapolations of `tau(x)` (predict them
  with `cf.effect(X_new)` after `sp.forest_support`, section 4). `sp.rate`
  also raises.

Monte Carlo evidence (200 replications; N = 300 units, T = 8, cohorts 3, 5
and 7 plus never-treated, adoption selected on the unit effect; 500 trees):

| | effect `(1 + x1)(1 + 0.2 e)` | constant effect |
| --- | --- | --- |
| bias of the imputation ATT | -0.003 | -0.003 |
| bias of the mean forest prediction (`forest_plug_in`) | -0.177 | -0.001 |
| ATT coverage, `variance="forest"` / `"bjs"` | 97.5% / 100% | 94.5% / 94.0% |
| mean ATT standard error, `"forest"` / `"bjs"` | 0.093 / 0.140 | 0.085 / 0.082 |
| group ATT coverage (`x1 > 0` vs not), `"forest"` | 97.5% | 96.3% |
| calibration test rejects at 5% | 100% | 4.0% |
| RMSE of treated cells' predictions, raw / calibrated | 0.634 / 0.570 | 0.213 / 0.118 |

The mean forest prediction is shrunk toward zero when effects are
heterogeneous, which is why it is reported only for comparison. The
calibration slope is now a genuine de-attenuation factor. The 1.29.0
regression on globally within-transformed variables [aytug2026attenuated],
available as `method="within"`, tests for heterogeneity with the right size,
but its slope stayed at 0.88 to 1.07 while the predictions' slope on the
truth was 0.65 to 0.91, and rescaling by it did not reduce RMSE.

## 4. Worked example: a currency union on a dyadic trade panel

[aytug2026euro] estimates how the euro's trade effect varies across country
pairs: a pooled causal forest on pair-year data, then a causal forest with
fixed effects [kattenberg2023causal; aytug2026causalfe] to remove pair and
year effects, followed by pair- and country-level effects, counterfactual
effects for the countries that stayed out, and pre-trends by predicted-effect
group. `sp.datasets.currency_union_panel()` has the same layout with
**simulated** numbers and a known effect `tau_true`: 15 countries, 105 pairs,
1995-2015, 11 countries adopting in 1999 and one in 2001, pair effects that
rise with the latent "core" index that also drives adoption, and effects that
rise with pre-adoption trade intensity and size. (Country codes are generic;
nothing here is an estimate of the euro's effect.)

```python
import numpy as np
import statspai as sp

df = sp.datasets.currency_union_panel(seed=0)      # true ATT 0.133
x = ["pre_trade", "log_gdp_prod", "log_gdppc"]

pooled = sp.causal_forest(data=df, y="log_trade", d="euro", x=x,
                          clusters="pair", random_state=0)
pooled.average_treatment_effect("treated")          # 0.482 (se 0.041)

cf = sp.causal_forest(data=df, y="log_trade", d="euro", x=x,
                      id="pair", time="year", fe="twoway", random_state=0)
C = "auto"            # GDP varies within pairs and drives trade
att = cf.average_treatment_effect("treated", controls=C)
# estimate 0.134, se 0.023, 95% CI [0.089, 0.179]; forest_plug_in 0.166;
# imputation_controls ['log_gdp_prod', 'log_gdppc']
cf.average_treatment_effect("treated")["estimate"]   # controls="none": 0.199
```

The pooled forest compares core pairs, which trade more *and* adopted, with
peripheral ones and more than triples the effect. The FE forest's imputation
ATT recovers it once GDP enters the untreated model; without it, pairs
growing faster look more affected and the estimate is 0.199. With the second wave of adopters
(`currency_union_panel(late_adopters=True)`: adoptions in 2007-2015 during a
common downturn, 378 pairs) the imputation ATT is 0.160 (se 0.012) against a
true 0.150; `tests/test_forest_fe_imputation.py` checks both designs.

**Which covariates drive the heterogeneity.**

```python
sp.calibration_test(cf, controls=C)     # differential slope 0.63 (se 0.19), p = 5e-4
cf.best_linear_projection(controls=C)   # pre_trade 0.060 (se 0.021); GDP terms ~0
```

**Pair, country and period effects.** `members` makes each country a group
that contains all of its pairs, the aggregation behind the country tables of
[aytug2026euro]; `scale="percent"` converts log points to `100 (exp(x) - 1)`:

```python
members = df[["country_i", "country_j"]].to_numpy()
by_country = sp.forest_group_effects(cf, members=members, scale="percent",
                                     controls=C)
#        n_rows  estimate_pct  ci_low_pct  ci_high_pct  forest_mean_pct
# C07       185          32.5        20.2         46.0             26.6
# C05       185          21.0        10.7         32.3             25.2
# ...
# C06       185           6.0        -1.5         14.2             17.8
by_country.attrs["tests"]["equality_p"]             # 0.0008

sp.forest_group_effects(cf, by="cate_quantile", controls=C)     # GATES
#       estimate     se  forest_mean
# Q1       0.067  0.031        0.069
# Q4       0.192  0.030        0.267    Q4 - Q1 = 0.125 (se 0.036)

period = np.where(df.year <= 2003, "1999-2003",
                  np.where(df.year <= 2008, "2004-2008", "2009-2015"))
sp.forest_group_effects(cf, by=period, controls=C)  # 0.126, 0.126, 0.145
sp.forest_group_effects(cf, by=df["pair"].to_numpy(), controls=C)  # per pair
```

Group estimates average imputation scores, so each country's interval is a
sampling interval for its average effect, not the spread of fitted values.
Countries appear in many pairs, so rows that share a country may be
correlated; `cluster="dyadic"` allows that [aronow2015cluster]. It is
justified as the number of countries grows: with 15 countries it warns, and
a group that loads on a single country can get a non-positive variance,
which is reported as `NaN` rather than as a zero-width interval.

**Counterfactual effects for countries that did not adopt.** A forest can
predict `tau(x)` for pairs that were never treated, but only as an
extrapolation from pairs that were. `sp.forest_support` says where that
extrapolation leaves the data:

```python
outs = df[(df.ever_euro == 0) & (df.year == 2010)]
sup = sp.forest_support(cf, outs[x])
sup.attrs["summary"]["share_supported"]             # 0.62
# mean predicted effect and share of supported pairs:
# C13  +3.6%  0.14 | C14  +8.2%  0.86 | C15  +10.0%  0.79
```

Only 14% of the pairs involving `C13` lie inside the covariate region of
pairs that switched, so its counterfactual is mostly an extrapolation. The
distance benchmark compares each reference row with rows of *other* units,
as a new unit is, so a pair's own years do not make the data look denser
than it is.

**Were high-effect pairs already on a different path?** A forest can rank
pairs by pre-existing trends rather than by effects. `sp.cate_pretrend_test`
sorts units by their mean OOB prediction and runs the pre-trend regression of
[borusyak2024revisiting] on untreated cells with group x lead indicators:

```python
pt = sp.cate_pretrend_test(cf, n_groups=2, leads=3, controls=C)
pt["equal_across_groups"]      # chi2(3) = 3.13, p = 0.37
pt["joint_zero"]               # chi2(6) = 8.21, p = 0.22
```

In 100 replications of a staggered design like that of section 3
(N = 300, T = 7, cohorts 3, 4 and 6; two groups, two leads) the equality
test rejected 3% of the time without a pre-trend and 71% of the time when
high-`x1` treated units trended by 0.3 per period before adoption (the joint
test: 5% and 95%).

`time_effects="common"` (default) tests the comparison the imputation
scores use; `"by_group"` runs a separate event study per group, as in the
appendix of [aytug2026euro].

## 5. DiD causal forests for staggered adoption

```python
res = sp.did_forest(
    df, y="emp", id="county", time="year", cohort="first_treat",
    x=["pop", "income"], clusters="state",
    control_group="notyettreated",
)
res.event_study            # dynamic effects with influence-function SEs
res.overall                # ATT over post-treatment cells
res.pretrend_test          # joint Wald test of pre-period effects
res.att_gt                 # doubly-robust ATT(g, t) + heterogeneity test per cell
res.unit_cate              # each treated unit's CATE by event time
res.predict_cate(X, event_time=2)
res.forest(2004, 2006)     # the CausalForest behind one cell
```

For each cohort `g` and period `t`, the treated units (cohort `g`) and the
comparison units (never treated, plus not yet treated by `max(t, g - 1)`) form
one cross-section. The outcome is `Y_t - Y_{g-1}`. Under conditional parallel
trends its conditional mean contrast is `tau_{g,t}(x)`, so one honest causal
forest per cell estimates it: the DiD causal forest of
[gavrilova2025difference] applied to every Callaway-Sant'Anna group-time
comparison [callaway2021difference]. On a two-period block, removing unit and
period effects is the same long difference, which is the block construction of
[aytug2026fixed].

`ATT(g, t)` is the forest's doubly-robust ATT: the mean out-of-bag CATE over
cohort `g` plus an inverse-propensity-weighted residual correction. Each cell
has a per-unit influence function; aggregates sum them unit by unit (or
cluster by cluster), so units that appear in several cells are accounted for.
Cohort-size weights are treated as known.

Monte Carlo (200 replications; N = 800, T = 7, cohorts 4 and 6 plus
never-treated; adoption and the untreated trend both depend on `x1`; effect
`(1 + x1)(1 + 0.25 e)`; 300 trees per cell):

| quantity | 95% CI coverage |
| --- | --- |
| overall ATT | 97.5% |
| event study, e = 0 ... 3 | 95.5% to 98.5% |
| event study, e = -5 ... -2 (placebos) | 93.0% to 97.0% |
| pre-trend joint test, rejection at 5% | 8.0% |

A second run of 300 replications (fresh seeds) checked the pre-period
calibration directly: reported standard errors are 0.99 to 1.05 times the
Monte Carlo standard deviation of every placebo cell and event-study
coefficient, and the Wald statistic has mean 4.00 and variance 7.91 against
4 and 8 for its chi-squared(4) reference, rejecting in 3.3% of replications.
Pooled over both runs the pre-trend test rejects in 26 of 500 replications
(5.2%). Post-treatment intervals are slightly conservative.

The simulation design of [gavrilova2025difference] (workers in firms, firm
treatment, CATT 10 for `x1 = 1` and 1 for `x1 = 0`) is a known-truth test in
`tests/reference_parity/test_panel_forest_recovery.py`.

## 6. Evidence and parity

| What | Grade | Where |
| --- | --- | --- |
| Calibration test, AIPW ATE/ATT/ATC/overlap, BLP, `vcovCL` HC0-HC3, given a forest | exact vs grf 2.6.1 / sandwich (<= 8.5e-15) | `tests/reference_parity/test_grf_cluster_operator_parity.py` |
| Forest: CATE RMSE, pointwise variances, coverage, ATE vs grf (i.i.d. and clustered) | T3 (Monte Carlo) | `tests/reference_parity/test_grf_engine_statistical_parity.py` |
| Engine identities (forest weights, OOB, clusters, FE within transform) | exact | `tests/test_grf_engine.py` |
| FE forest and DiD forest recovery | T1 (known truth) | `tests/test_panel_causal_forest.py`, `tests/test_did_forest.py` |
| FE-forest imputation ATT = `sp.did_imputation` (estimate and BJS SE) | exact identity (1e-13 / 5e-15), hence the Stata / R parity of `did_imputation` | `tests/test_forest_fe_imputation.py` |
| Group, BLP and calibration estimates = OLS of imputation scores; dyadic variance = pairwise definition = `sp.dyadic_regression` | exact | `tests/test_forest_fe_imputation.py` |
| Pre-trend regression = dummy-variable OLS with CR1 | exact (1e-8) | `tests/test_forest_fe_imputation.py` |
| Imputation ATT / group coverage, calibration size and power | T1 (Monte Carlo, section 3) | `tests/reference_parity/test_fe_forest_imputation_recovery.py` |

**Comparison with `causalfe`.** `causalfe` 0.3.2 [aytug2026causalfe] is the
Python implementation of [kattenberg2023causal] used in [aytug2026euro]. On
its own simulation design (50 replications) the two forests predict equally
well (CATE RMSE 0.476 vs 0.456, correlation 0.92 for both), but its pointwise
95% intervals cover 46% of treated cells against 93% here. With adoption
selected on the unit effect and effects that grow with exposure, the
two-way fixed-effects coefficient it reports as the ATE is biased by -0.18
(coverage 86%) while the imputation ATT is biased by -0.003 (coverage 96%).
This compares statistical properties of two stochastic estimators; it is not
parity. Scripts and numbers: `benchmarks/cross_library/panel_forest_causalfe/`.

The forest is not bit-identical to grf (independent random streams), so it is
never described as "aligned with R". Track A module 13 (AIPW ATE/ATT vs grf)
is inside its registered budget: estimates within 0.4%, standard errors
within 0.7%.

## 7. Mapping from R `grf`

| R | StatsPAI |
| --- | --- |
| `causal_forest(X, Y, W, clusters = g)` | `sp.causal_forest(Y=Y, T=W, X=X, clusters=g)` |
| `predict(cf)` (out-of-bag) | `cf.predict()` |
| `predict(cf, X.new, estimate.variance = TRUE)` | `cf.effect(X_new)`, `cf.effect_variance(X_new)` |
| `average_treatment_effect(cf, target.sample = "treated")` | `cf.average_treatment_effect("treated")` |
| `test_calibration(cf)` | `sp.calibration_test(cf)` |
| `best_linear_projection(cf, A)` | `cf.best_linear_projection(A)` |
| `rank_average_treatment_effect(cf, priorities)` | `sp.rate(cf)` (OOB priorities; see its docstring) |
| `split_frequencies(cf)` | `cf.split_frequencies()` |

Python `causalfe` (0.3.2):

| `causalfe` | StatsPAI |
| --- | --- |
| `CFFEForest(n_trees=, max_depth=, min_leaf=).fit(X, Y, D, unit, time)` | `sp.causal_forest(Y=Y, T=D, X=X, id=unit, time=time, fe="twoway", split_rule="cffe", n_estimators=, max_depth=, min_samples_leaf=)` |
| `predict(X)` | `cf.effect(X)`; `cf.predict()` for out-of-bag |
| `predict_interval(X)` | `cf.effect(X)`, `cf.effect_variance(X)` |
| `ate()` / `ate_interval()` (within-FE coefficient) | `cf.average_treatment_effect("treated")` (imputation ATT; see section 6) |
| `feature_importances()` | `cf.variable_importance()`, `cf.split_frequencies()` |

## References

[athey2019generalized; wager2018estimation; kattenberg2023causal;
gavrilova2025difference; callaway2021difference; chernozhukov2025generic;
aytug2026attenuated; aytug2026fixed; aytug2026causalfe; aytug2026euro;
borusyak2024revisiting; aronow2015cluster]
