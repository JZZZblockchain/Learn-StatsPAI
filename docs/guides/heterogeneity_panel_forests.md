# Heterogeneous effects with panel data: causal forests with clusters, fixed effects and DiD

A causal forest estimates the conditional average treatment effect
`tau(x)`. On panel or grouped data three things can go wrong, and StatsPAI
has one tool for each:

| Your data | Risk | Use |
| --- | --- | --- |
| Cross-section, independent units | — | `sp.causal_forest(...)` |
| Several rows per unit / firm / school | honesty and SEs assume independent rows | `sp.causal_forest(..., clusters="unit")` |
| Panel, treatment switches within units, selection on unit characteristics, effects stable over exposure | unit and period effects masquerade as heterogeneity | `sp.causal_forest(..., fe="twoway", id=..., time=...)` |
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

What is **not** available for FE forests, and why:

* `average_treatment_effect`, `best_linear_projection` and `rate` raise:
  their doubly-robust scores need a propensity `E[D | X]`, which a within-unit
  design does not define. Use `sp.did_forest` for averages with valid
  standard errors.
* `sp.calibrate_cate` runs but warns. FE-forest predictions are shrunk
  toward the mean (slope 0.65 to 0.91 on the true effect above). The
  out-of-bag best-linear-predictor slope proposed as a correction
  [aytug2026attenuated] comes from a *globally* within-transformed
  regression; in the design above it stayed at 0.88 to 1.07 and calibrated
  predictions did not reduce RMSE. The heterogeneity test built on the same
  regression is valid under a constant effect, so `calibration_test` remains
  a sound test; do not read the slope as a de-attenuation factor.

## 4. DiD causal forests for staggered adoption

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

## 5. Evidence and parity

| What | Grade | Where |
| --- | --- | --- |
| Calibration test, AIPW ATE/ATT/ATC/overlap, BLP, `vcovCL` HC0-HC3, given a forest | exact vs grf 2.6.1 / sandwich (<= 8.5e-15) | `tests/reference_parity/test_grf_cluster_operator_parity.py` |
| Forest: CATE RMSE, pointwise variances, coverage, ATE vs grf (i.i.d. and clustered) | T3 (Monte Carlo) | `tests/reference_parity/test_grf_engine_statistical_parity.py` |
| Engine identities (forest weights, OOB, clusters, FE within transform) | exact | `tests/test_grf_engine.py` |
| FE forest and DiD forest recovery | T1 (known truth) | `tests/test_panel_causal_forest.py`, `tests/test_did_forest.py` |

The forest is not bit-identical to grf (independent random streams), so it is
never described as "aligned with R". Track A module 13 (AIPW ATE/ATT vs grf)
is inside its registered budget: estimates within 0.4%, standard errors
within 0.7%.

## 6. Mapping from R `grf`

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

## References

[athey2019generalized; wager2018estimation; kattenberg2023causal;
gavrilova2025difference; callaway2021difference; chernozhukov2025generic;
aytug2026attenuated; aytug2026fixed]
