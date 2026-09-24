# The GRF family: instrumental, multi-arm, survival and prediction forests

`sp.causal_forest` is one member of the generalized random forest (GRF)
family of Athey, Tibshirani and Wager (2019). StatsPAI implements the rest
of the family on the same engine, so every forest here is honest, samples
whole clusters when you pass `clusters=`, reports out-of-bag predictions for
the training rows, and — where grf does — little-bag variance estimates.

| grf (R) | StatsPAI | estimand |
| --- | --- | --- |
| `causal_forest` | `sp.causal_forest` | CATE `E[Y(1) - Y(0) | x]` |
| `instrumental_forest` | `sp.iv_forest` (alias `sp.instrumental_forest`) | conditional LATE `Cov[Y,Z|x] / Cov[W,Z|x]` |
| `multi_arm_causal_forest` | `sp.multi_arm_forest` | `E[Y(k) - Y(0) | x]`, k = 1..K-1 |
| `lm_forest` | `sp.lm_forest` | `h(x)` in `Y = c(x) + W'h(x)` |
| `causal_survival_forest` | `sp.causal_survival_forest` | RMST or survival-probability difference at a horizon |
| `regression_forest` | `sp.regression_forest` | `E[Y | x]` |
| `multi_regression_forest` | `sp.multi_regression_forest` | `E[Y_1..Y_q | x]` |
| `probability_forest` | `sp.probability_forest` | `P[Y = k | x]` |
| `quantile_forest` | `sp.quantile_forest` | conditional quantiles |
| `survival_forest` | `sp.survival_forest` | `S(t | x) = P[T > t | x]` |
| `variable_importance` | `sp.variable_importance` | depth-weighted split shares |
| `best_linear_projection` | `sp.best_linear_projection` | BLP of the CATE on covariates |
| `get_scores` | `sp.get_scores` | doubly-robust scores |

Option names follow `sp.causal_forest` (`n_estimators`, `min_samples_leaf`,
`max_samples`, `honest`, `ci_group_size`, ...). One exception is worth
knowing: grf's `alpha` (the minimum share of a parent each child keeps) is
`split_alpha`, because in StatsPAI `alpha` is always a significance level.

## Instrumental forest

```python
import statspai as sp

iv = sp.iv_forest(df, y="earnings", treat="college", instrument="distance_low",
                  covariates=["age", "female", "parent_educ"], clusters="county")
iv.late, iv.se, iv.ci          # average conditional LATE, doubly robust
iv.cate                        # out-of-bag tau(X_i)
sp.best_linear_projection(iv, A=df[["parent_educ"]])
```

The average is `E[tau(X)]`, estimated from scores whose Riesz representer
divides by the compliance score `Delta(x)` — how much the instrument moves
the treatment at `x`. Where `Delta` is near zero the instrument is locally
weak and those rows dominate the average; `iv_forest` warns when the
estimated compliance falls below 0.05, and `iv.detail["compliance_score_range"]`
reports it. You can pass your own `compliance_score=`.

## Multi-arm causal forest and linear-model forest

```python
ma = sp.multi_arm_forest(df, y="y", treat="arm", covariates=X_cols,
                         reference="control")
ma.average_treatment_effect()        # one row per arm vs the reference
ma.best_linear_projection(A=df[["age"]])
```

One forest serves all contrasts: its trees split on the gradient of every
arm's effect at once and apply the causal-forest balance constraints to
each arm. Propensities come from a probability forest; the AIPW scores
divide by them, so the fit warns when an arm's estimated propensity falls
below 0.01. `sp.lm_forest` is the same machinery for any set of regressors
(continuous doses, several treatments at once, varying coefficients).

## Causal survival forest

```python
csf = sp.causal_survival_forest(df, time="months", event="died", treat="drug",
                                covariates=X_cols, horizon=36,
                                target="RMST")       # or "survival_probability"
csf.ate, csf.se                                      # 36-month RMST difference
```

**Choose `horizon` from the study design**, not from the data: effects past
the point where most people are censored are not identified, and the
estimator divides by the probability of remaining uncensored up to the
horizon. The fit refuses when that probability is estimated as zero and
warns below 0.05. (When `horizon` is omitted the 80th percentile of event
times is used and recorded in `csf.detail["horizon_source"]`.)

The paper leaves the discretisation of the censoring integral open.
StatsPAI follows the implementation maintained by the method's authors
(grf): the integral is a sum over censoring times at or below `min(U, h)`
of the log-hazard increment over `S^C`, and the denominator of the
estimating equation uses its population value `(W - e)^2`. Given the same
nuisance curves, the scores agree with grf's to 1e-15.

## Prediction forests

`sp.regression_forest`, `sp.multi_regression_forest`,
`sp.probability_forest`, `sp.quantile_forest` and `sp.survival_forest`
return `.predictions` (out-of-bag) and `.predict(newdata)`. The quantile
forest splits on the class of `Y` relative to the node's quantiles, so it
follows changes in spread and shape, not only in the mean;
`regression_splitting=True` gives Meinshausen's quantile regression forest.
The survival forest splits on the log-rank statistic, computed exactly for
every candidate split, and returns forest-weighted Kaplan-Meier (or
Nelson-Aalen) curves.

## What is verified, and how

| layer | evidence | where |
| --- | --- | --- |
| everything after the forest (local solves, scores, averages, SEs, BLP, curves, quantiles, importance) | **T2**: fed grf's own forest weights and inputs, matches grf 2.6.1 to <= 7e-14 | `tests/reference_parity/test_grf_family_operator_parity.py` |
| causal-survival score map (nuisance curves -> scores) | **T2**: 1.2e-15, with tied event/censoring times and rows past the horizon | `tests/reference_parity/test_csf_psi_operator_parity.py` |
| the forests themselves | **T3**: against three grf seeds on known-truth designs, CATE RMSE ratio 0.97-1.02, coverage within 0.013, average effects within 0.3 grf SEs | `tests/reference_parity/test_grf_family_statistical_parity.py` |
| causal survival averages | **T1**: 40 replications, RMST bias 0.0007 (MC se 0.0038) with 100% coverage; survival probability -0.0024 (0.0039), 97.5% | CHANGELOG |

Two forests grown from independent random streams never agree tree by tree,
so no forest is claimed to reproduce grf's numbers — only to be the same
estimator, which is what the operator pins plus the statistical comparison
establish.

## Seeds

Each little bag of trees gets its own seed from
`numpy.random.SeedSequence(random_state)`, and each auxiliary forest (the
outcome, treatment, instrument, propensity, censoring and survival
nuisances) its own stream. Different `random_state` values therefore give
independent forests, which is what a seed-robustness check needs. Before
this, consecutive seeds shared nearly every tree.

## References

[@athey2019generalized], [@wager2018estimation], [@cui2023estimating],
[@nie2021quasi], [@aronow2013beyond], [@chernozhukov2022locally],
[@semenova2021debiased], [@ishwaran2008random], [@meinshausen2006quantile]
