# Causal forests with fixed effects: StatsPAI vs `causalfe`

Monte Carlo comparison of `sp.causal_forest(fe="twoway")` with
[`causalfe`](https://github.com/haytug/causalfe) 0.3.2 (tag `v0.3.2`), the
Python implementation described in [aytug2026causalfe] of the method of
[kattenberg2023causal]. Both forests are stochastic and use different
splitting rules, so this compares statistical properties (T3-style); it is
**not** a parity claim.

## Designs (`dgps.py`)

* **A**: the causalfe paper's `dgp_did_heterogeneous(N=200, T=6)`, with
  covariates drawn per row, `tau = x0`, random adoption periods, and unit and
  period effects independent of `x`.
* **B**: N = 200, T = 8, unit effect `2 x1 + noise`, adoption probability
  increasing in the unit effect (cohorts 3, 5, 7, never), effect
  `(1 + x1)(1 + 0.25 e)` growing with exposure `e`.

Settings: causalfe `CFFEForest(n_trees=100, max_depth=4, min_leaf=20)` with
`predict_interval` and `ate()` / `ate_interval()` (the pair-clustered
within-FE coefficient it recentres its predictions on). StatsPAI uses 2,000
trees, little-bag pointwise intervals, `average_treatment_effect("treated")`
(imputation ATT) and `calibrate_cate`. Metrics are computed on treated cells;
the average-effect target is the mean true effect over treated cells. 50
replications per design (seeds 0-49).

## Results (`results.json`)

| | A: causalfe | A: StatsPAI | B: causalfe | B: StatsPAI |
| --- | --- | --- | --- | --- |
| CATE RMSE | 0.476 | 0.456 (calibrated 0.417) | 0.853 | 0.822 (calibrated 0.707) |
| CATE correlation with truth | 0.916 | 0.917 | 0.858 | 0.854 |
| pointwise 95% CI coverage | 46.2% | 93.4% | 12.2% | 62.0% |
| average effect: bias | -0.011 | -0.012 | -0.178 | -0.003 |
| average effect: 95% CI coverage | 98% | 98% | 86% | 96% |
| average effect: mean CI width | 0.496 | 0.526 | 0.608 | 0.484 |

In B the true effect varies with exposure, which no function of `x` alone
captures, so neither forest's pointwise intervals reach nominal coverage
there (`sp.did_forest` models exposure explicitly). The two-way fixed-effects
coefficient that causalfe reports as its ATE weights cells by adoption timing
and is biased under dynamic effects; the imputation ATT is not.

## Reproduce

```bash
python -m venv cfvenv
cfvenv/bin/pip install "git+https://github.com/haytug/causalfe@v0.3.2"
for n in A B; do cfvenv/bin/python run_causalfe.py $n 0 50 > cf_$n.log; done
for n in A B; do PYTHONPATH=../../../src python run_statspai.py $n 0 50 > sp_$n.log; done
python summarize.py
```

Each script prints one JSON line per replication; `summarize.py` averages the
`*.log` files. causalfe takes about 20 s per replication.
