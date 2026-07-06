# synth

> 📂 所属分类:01 · 核心因果推断方法 (Core Causal Methods)

Synthetic Control module for StatsPAI.

Unified entry point: ``synth(method=...)`` dispatches to all variants.

Variants (20 methods)
---------------------
- **classic** — Abadie, Diamond & Hainmueller (2010)
- **penalized / ridge** — Ridge-penalised SCM
- **demeaned / detrended** — Ferman & Pinto (2021)
- **unconstrained / elastic_net** — Doudchenko & Imbens (2016)
- **augmented / ascm** — Ben-Michael, Feller & Rothstein (2021)
- **sdid** — Arkhangelsky, Athey, Hirshberg, Imbens & Wager (2021)
- **factor / gsynth** — Xu (2017)
- **staggered** — Ben-Michael, Feller & Rothstein (2022)
- **mc / matrix_completion** — Athey, Bayati et al. (2021)
- **discos / distributional** — Gunsilius (2023)
- **multi_outcome** — Sun (2023)
- **scpi / prediction_interval** — Cattaneo, Feng & Titiunik (2021)
- **bayesian** — Bayesian SCM with MCMC posterior (Vives & Martinez 2024)
- **bsts / causal_impact** — Bayesian Structural Time Series (Brodersen et al. 2015)
- **penscm / abadie_lhour** — Penalized SCM with pairwise discrepancy (Abadie & L'Hour 2021)
- **fdid / forward_did** — Forward DID with optimal donor selection (Li 2024)
- **cluster** — Cluster SCM with donor grouping (Rho et al. 2025, arXiv:2503.21629) [@rho2025clustersc]
- **sparse / lasso** — Sparse SCM with L1 penalties (Amjad, Shah & Shen 2018)
- **kernel / kernel_ridge** — Kernel-based nonlinear SCM

Inference
---------
- **placebo** — in-space permutation (default)
- **conformal** — Chernozhukov, Wüthrich & Zhu (2021)
- **bootstrap / jackknife** — for SDID
- **prediction intervals** — Cattaneo et al. (2021)
- **bayesian posterior** — full posterior credible intervals (Bayesian SCM)
- **bsts posterior** — Bayesian structural time series uncertainty

Diagnostics
-----------
- **synth_sensitivity()** — comprehensive robustness suite
- **synth_loo()** — leave-one-out donor analysis
- **synth_time_placebo()** — backdating tests
- **synth_donor_sensitivity()** — donor pool variation
- **synth_rmspe_filter()** — pre-RMSPE robustness

**55 个公共函数**

### `sp.SequentialSDIDResult()`

**Per-cohort and aggregated output of :func:`sequential_sdid`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `aggregate_att` | `number` | ✓ |  | aggregate_att parameter (float). |
| `aggregate_ci` | `array[string]` | ✓ |  | aggregate_ci parameter (tuple). |
| `aggregate_se` | `number` | ✓ |  | aggregate_se parameter (float). |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `per_cohort` | `string` | ✓ |  | per_cohort parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SequentialSDIDResult(aggregate_att=1.0, aggregate_se=1.0, aggregate_ci=["a", "b"], per_cohort="value")
print(result.summary())
```

---
### `sp.SynthComparison()`

**Structured container for multi-method SCM comparison results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `comparison_table` | `string` | ✓ |  | comparison_table parameter (pd.DataFrame). |
| `recommendation_reason` | `string` | ✓ |  | recommendation_reason parameter (str). |
| `recommended` | `string` | ✓ |  | recommended parameter (str). |
| `results` | `object` | ✓ |  | results parameter (Dict[str, CausalResult]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SynthComparison(comparison_table="value", recommended="value", recommendation_reason="value")
print(result.summary())
```

---
### `sp.SynthExperimentalDesignResult()`

**Structured output of :func:`synth_experimental_design`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `baseline_variance` | `number` | ✓ |  | baseline_variance parameter (float). |
| `diagnostics` | `object` |  | `None` | diagnostics parameter (Dict[str, Any]). |
| `donor_units` | `array[string]` | ✓ |  | donor_units parameter (List[Any]). |
| `expected_variance` | `number` | ✓ |  | expected_variance parameter (float). |
| `method` | `string` |  | `'abadie_zhao_2025'` | Estimator or algorithm variant to use. |
| `ranking` | `string` | ✓ |  | ranking parameter (pd.DataFrame). |
| `selected` | `array[string]` | ✓ |  | selected parameter (List[Any]). |
| `weights` | `object` | ✓ |  | Observation weights. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SynthExperimentalDesignResult(selected=["a", "b"], ranking="value", donor_units=["a", "b"], expected_variance=1.0, baseline_variance=1.0)
print(result.summary())
```

---
### `sp.SyntheticControl()`

**Canonical Synthetic Control estimator (Abadie, Diamond & Hainmueller**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `covariates` | `array[string]` |  |  | Column names whose pre-treatment means are used as predictors for the V-weighted matching problem. |
| `data` | `string` | ✓ |  | Long-format panel ``(unit, time, outcome, ...)``. |
| `n_random_starts` | `integer` |  | `4` | Additional random Dirichlet starts for the outer V optimiser. |
| `outcome` | `string` | ✓ |  | Column names. |
| `penalization` | `number` |  | `0.0` | Ridge penalty on donor weights. |
| `special_predictors` | `array[string]` |  |  | R/Stata ``Synth``-style predictor specifications. Each entry is ``(column, period_spec, op)`` where ``period_spec`` is a scalar year, a list of years, or a ``slice(start, stop)`` (inclusive), and ``op`` is ``'mean'`` or ``'sum'``. When omitted together with ``covariates``, the pre-treatment outcome vector itself is used as the predictor (V has no identifying power and is fixed to the identity, following Kaul et al. 2015). |
| `standardize_predictors` | `boolean` |  | `True` | Rescale predictors to unit range before the V optimization. |
| `time` | `string` | ✓ |  | Column names. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Column names. |
| `v_method` | `string (enum)` |  | `'auto'` | ``'auto'`` -> nested V-W when covariates / special predictors are supplied, equal V otherwise. ``'nested'`` forces the outer V optimisation even when only Y lags are used (note: the outer problem is then under-identified, per Kaul et al. 2015). Equal V reduces to the outcome-only simplex LS estimator. |

> **v_method** options: `'auto'`, `'nested'`, `'equal'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SyntheticControl(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.SyntheticSurvivalResult()`

**Output of :func:`synth_survival`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `ci_high` | `string` |  |  | ci_high parameter (Optional[np.ndarray]). |
| `ci_low` | `string` |  |  | ci_low parameter (Optional[np.ndarray]). |
| `gap` | `string` | ✓ |  | gap parameter (np.ndarray). |
| `placebo_gaps` | `string` |  |  | placebo_gaps parameter (Optional[np.ndarray]). |
| `pre_rmse` | `number` |  |  | pre_rmse parameter (Optional[float]). |
| `s_synth` | `string` | ✓ |  | s_synth parameter (np.ndarray). |
| `s_treated` | `string` | ✓ |  | s_treated parameter (np.ndarray). |
| `time_grid` | `string` | ✓ |  | Grid of time values to evaluate. |
| `treat_time` | `number` | ✓ |  | treat_time parameter (float). |
| `treated_unit` | `string` | ✓ |  | treated_unit parameter (str). |
| `weights` | `object` | ✓ |  | Observation weights. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SyntheticSurvivalResult(treated_unit="value", time_grid="value", s_treated="value", s_synth="value", gap="value", treat_time=1.0, alpha=1.0)
print(result.summary())
```

---
### `sp.augsynth()`

**Augmented Synthetic Control with ridge bias correction (Ben-Michael et al. 2021). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `backend` | `string` |  | `'native'` | Computation backend: native or augsynth/R bridge backend |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | treated_unit parameter (str). |
| `treatment_time` | `integer` | ✓ |  | treatment_time parameter (int). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.augsynth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.basque_terrorism()`

**Basque Country terrorism dataset (simulated).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.basque_terrorism()
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.california_prop99()`

**California Proposition 99 tobacco control dataset. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.california_prop99()
print(result.summary())
```

> 📁 See also: `synth_prop99.py`

---
### `sp.california_tobacco()`

**California Proposition 99 tobacco dataset (simulated, extended).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.california_tobacco()
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.causal_impact()`

**Bayesian structural time series for causal impact analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `intervention_time` | `string` | ✓ |  | Date/index of intervention |
| `time` | `string` | ✓ |  | Time / date column |
| `y` | `string` | ✓ |  | Outcome time-series column |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.causal_impact(y="outcome", data=df, time="value", intervention_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`

---
### `sp.conformal_synth()`

**Conformal inference for synthetic control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `grid_range` | `array[string]` |  |  | (min, max) of the hypothesis grid. If None, auto-determined from pre-treatment residual scale. |
| `grid_size` | `integer` |  | `101` | Number of points in the hypothesis grid for CI inversion. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `penalization` | `number` |  | `0.0` | Ridge penalty (used when scm_method='ridge'). |
| `scm_method` | `string` |  | `'classic'` | Which SCM variant to use for weight estimation. Currently supports 'classic' (constrained) and 'ridge'. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_synth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.demeaned_synth()`

**De-meaned / De-trended Synthetic Control Method.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `covariates` | `array[string]` |  |  | Additional covariates to match on. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `penalization` | `number` |  | `0.0` | Ridge penalty on weights. |
| `placebo` | `boolean` |  | `True` | Run in-space placebo inference. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*
| `variant` | `string (enum)` |  | `'demeaned'` | * ``'demeaned'`` -- subtract unit-level pre-treatment means. * ``'detrended'`` -- subtract unit-level linear time trends. |

> **variant** options: `'demeaned'`, `'detrended'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.demeaned_synth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.did_estimate()`

**R-style alias: ``synthdid::did_estimate``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat_time` | `string` | ✓ |  | treat_time parameter. |
| `treat_unit` | `string` | ✓ |  | treat_unit parameter. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.did_estimate(y="outcome", data=df, unit="value", time="value", treat_unit="value", treat_time="value")
print(result.summary())
```

---
### `sp.discos()`

**Distributional Synthetic Controls (Gunsilius 2023). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `data` | `string` | ✓ |  | Panel data in long format with columns for unit, time, and outcome. |
| `method` | `string (enum)` |  | `'mixture'` | ``'mixture'``: constrained (omega >= 0, Sigmaomega = 1) -- minimises the L2-Wasserstein distance between quantile functions. ``'quantile'``: unconstrained quantile-on-quantile regression. |
| `n_quantiles` | `integer` |  | `100` | Number of quantile grid points on (0, 1). |
| `outcome` | `string` | ✓ |  | Outcome variable column name. |
| `placebo` | `boolean` |  | `True` | Run in-space placebo permutation tests for inference. |
| `seed` | `integer` |  |  | Random seed (currently unused; reserved for bootstrap extensions). |
| `time` | `string` | ✓ |  | Time period column name. |
| `treated_unit` | `string` | ✓ |  | Value in *unit* that identifies the treated unit. |
| `treatment_time` | `string` | ✓ |  | First period of treatment (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column name. |

> **method** options: `'mixture'`, `'quantile'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.discos(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.discos_plot()`

**Visualise distributional synthetic control results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | Pre-existing axes for the plot. |
| `ci_alpha` | `number` |  | `0.2` | Transparency for CI band. |
| `color` | `string` |  | `'#2C3E50'` | Primary plot colour. |
| `figsize` | `array[string]` |  | `[10, 6]` | Figure size. |
| `result` | `string` | ✓ |  | Output from ``discos()`` or ``qqsynth()``. |
| `title` | `string` |  |  | Plot title override. |
| `type` | `string (enum)` |  | `'quantile_effect'` | default 'quantile_effect' ``'quantile_effect'``: treatment effect Delta(tau) across quantiles with CIs. ``'quantile_comparison'``: overlay treated vs. counterfactual quantile functions. ``'gap'``: gap plot (treated - synthetic) over time. ``'weights'``: horizontal bar chart of donor weights. |

> **type** options: `'quantile_effect'`, `'quantile_comparison'`, `'gap'`, `'weights'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.discos_plot(result="value")
print(result.summary())
```

---
### `sp.discos_test()`

**Test for distributional treatment effects.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | Output from ``discos()`` or ``qqsynth()``. |
| `test` | `string (enum)` |  | `'ks'` | ``'ks'``: two-sample Kolmogorov-Smirnov test comparing treated and counterfactual quantile functions. ``'cvm'``: Cramer-von Mises test statistic (permutation-based). ``'stochastic_dominance'``: first-order stochastic dominance test. |

> **test** options: `'ks'`, `'cvm'`, `'stochastic_dominance'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.discos_test(result="value")
print(result.summary())
```

---
### `sp.german_reunification()`

**German reunification dataset (simulated).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.german_reunification()
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.gsynth()`

**Generalized Synthetic Control via interactive fixed effects. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `backend` | `string (enum)` |  | `'native'` | ``'native'`` uses StatsPAI's Python interactive fixed-effects implementation. ``'gsynth'``/``'r'`` delegates to the R ``gsynth`` package through ``Rscript`` using the Track-A reference specification ``force='two-way'``, ``CV=TRUE``, ``r=c(0, max_factors)``, and ``se=FALSE``. The R backend is intended for exact reference-package parity; the native path remains the dependency-light default. |
| `covariates` | `array[string]` |  |  | Additional time-varying covariates. |
| `cv_folds` | `integer` |  | `5` | Cross-validation folds for factor selection. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `max_factors` | `integer` |  | `5` | Maximum factors to try during CV. |
| `n_factors` | `integer` |  |  | Number of latent factors. If None, selected by cross-validation. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `placebo` | `boolean` |  | `True` | Run placebo inference. |
| `seed` | `integer` |  |  | Random seed. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

> **backend** options: `'native'`, `'gsynth'`, `'r'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.gsynth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.mc_synth()`

**Matrix Completion Synthetic Control Method.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `covariates` | `array[string]` |  |  | Time-varying covariates to partial out before matrix completion. |
| `cv_folds` | `integer` |  | `5` | Number of CV folds for automatic lambda selection. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `lambda_reg` | `number` |  |  | Nuclear norm penalty. If ``None`` (default), selected automatically via cross-validation on observed entries. |
| `max_iter` | `integer` |  | `500` | Maximum Soft-Impute iterations. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `placebo` | `boolean` |  | `True` | Run placebo (permutation) inference by treating each control unit as if it were treated. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `tol` | `number` |  | `1e-06` | Convergence tolerance (relative change in Frobenius norm). |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mc_synth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.multi_outcome_synth()`

**Multiple Outcomes Synthetic Control Method (Sun 2023).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and joint test. |
| `data` | `string` | ✓ |  | Long-format panel data containing all outcome columns. |
| `method` | `string (enum)` |  | `'concatenated'` | Weight-estimation strategy. * ``'concatenated'`` -- stack all K standardised outcome panels vertically and solve one quadratic programme. * ``'averaged'`` -- standardise each outcome, average across K, then solve SCM on the mean series. |
| `outcomes` | `array[string]` | ✓ |  | Column names for the K outcome variables. |
| `penalization` | `number` |  | `0.0` | Ridge-type penalty added to the diagonal of the donor cross-product matrix (``penalization * I``). Helps when donors are collinear. |
| `placebo` | `boolean` |  | `True` | Run in-space placebo permutations for inference (each donor is pretended to be treated in turn). |
| `standardize` | `boolean` |  | `True` | Standardise each outcome to zero mean / unit variance before stacking or averaging (strongly recommended when outcome scales differ). |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Value identifying the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

> **method** options: `'concatenated'`, `'averaged'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.multi_outcome_synth(data=df, outcomes=["a", "b"], unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.qqsynth()`

**Quantile Synthetic Control (alias for DiSCo with ``method='quantile'``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Panel data in long format. |
| `n_quantiles` | `integer` |  | `100` | Number of quantile grid points. |
| `outcome` | `string` | ✓ |  | Outcome variable column. |
| `placebo` | `boolean` |  | `True` | Run placebo permutation inference. |
| `seed` | `integer` |  |  | Random seed. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.qqsynth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.robust_synth()`

**Robust / unconstrained Synthetic Control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `covariates` | `array[string]` |  |  | Additional covariates to match on. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `intercept` | `boolean` |  | `True` | Fit an intercept (level shift). Only for unconstrained / elastic_net. |
| `l1_penalty` | `number` |  | `0.0` | Lasso (L1) penalty strength. |
| `l2_penalty` | `number` |  | `0.01` | Ridge (L2) penalty strength. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `placebo` | `boolean` |  | `True` | Run in-space placebo inference. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*
| `variant` | `string (enum)` |  | `'unconstrained'` | * ``'unconstrained'`` -- no sign / sum constraints; optional intercept. * ``'elastic_net'`` -- L1 + L2 penalty, no sign constraints. * ``'penalized'`` -- classic SCM constraints + elastic-net penalty. |

> **variant** options: `'unconstrained'`, `'elastic_net'`, `'penalized'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.robust_synth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.sc_estimate()`

**R-style alias: ``synthdid::sc_estimate``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat_time` | `string` | ✓ |  | treat_time parameter. |
| `treat_unit` | `string` | ✓ |  | treat_unit parameter. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sc_estimate(y="outcome", data=df, unit="value", time="value", treat_unit="value", treat_time="value")
print(result.summary())
```

---
### `sp.scdata()`

**Prepare data matrices for synthetic control estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Long-format panel data. |
| `outcome` | `string` | ✓ |  | Outcome variable column name. |
| `time` | `string` | ✓ |  | Time period column name. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.scdata(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.scest()`

**Estimate synthetic control weights.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Long-format panel data. |
| `lasso_lambda` | `number` |  | `1.0` | L1 penalty (used when ``w_constr='lasso'``). |
| `outcome` | `string` | ✓ |  | Outcome variable column name. |
| `ridge_lambda` | `number` |  | `1.0` | L2 penalty (used when ``w_constr='ridge'``). |
| `time` | `string` | ✓ |  | Time period column name. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column name. |
| `w_constr` | `string` |  | `'simplex'` | Weight constraint: - ``'simplex'`` : w >= 0, sum(w) = 1 - ``'lasso'`` : L1-penalised (allows negative, non-summing) - ``'ridge'`` : L2-penalised - ``'ols'`` : ordinary least squares (unconstrained) - ``'ls'`` : least squares (same as 'ols') |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.scest(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

---
### `sp.scpi()`

**Prediction intervals for synthetic control methods.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for prediction intervals. |
| `cores` | `integer` |  | `1` | Number of cores (reserved for future parallel subsampling). |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `e_method` | `string` |  | `'gaussian'` | Method for estimating out-of-sample uncertainty: - ``'gaussian'`` : sub-Gaussian bound using residual variance - ``'ls'`` : location-scale model (allows heteroskedasticity) - ``'qreg'`` : quantile regression (nonparametric) |
| `lasso_lambda` | `number` |  | `1.0` | L1 penalty (used when ``w_constr='lasso'``). |
| `outcome` | `string` | ✓ |  | Outcome variable column name. |
| `pi_type` | `string` |  | `'both'` | Which prediction interval components to include: - ``'in_sample'`` : only in-sample (weight estimation) uncertainty - ``'out_of_sample'``: only out-of-sample (prediction) uncertainty - ``'both'`` : simultaneous interval combining both sources |
| `ridge_lambda` | `number` |  | `1.0` | L2 penalty (used when ``w_constr='ridge'``). |
| `seed` | `integer` |  |  | Random seed for reproducibility in subsampling. |
| `time` | `string` | ✓ |  | Time period column name. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column name. |
| `w_constr` | `string` |  | `'simplex'` | Weight constraint for SCM estimation: - ``'simplex'`` : w >= 0, sum(w) = 1 - ``'lasso'`` : L1-penalised - ``'ridge'`` : L2-penalised - ``'ols'`` : ordinary least squares (unconstrained) - ``'ls'`` : least squares (same as 'ols') |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.scpi(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.sdid()`

**Synthetic Difference-in-Differences estimator (and SC / DID variants). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `backend` | `string (enum)` |  | `'native'` | ``'native'`` uses StatsPAI's Python implementation. ``'synthdid'``/``'r'`` delegates to the R ``synthdid`` package through ``Rscript`` and returns the reference package's point estimate and ``synthdid_se`` standard error. The R backend is mainly for exact cross-language parity claims; the dependency- light native implementation remains the default. |
| `covariates` | `array[string]` |  |  | Reserved for future covariate-adjusted extensions. |
| `data` | `string` | ✓ |  | Balanced panel data in long format. |
| `method` | `string (enum)` |  | `'sdid'` | * ``'sdid'`` -- Synthetic DID (unit + time weights) * ``'sc'`` -- Synthetic Control (unit weights only) * ``'did'`` -- DID (uniform weights) |
| `n_reps` | `integer` |  | `200` | Replications for placebo / bootstrap SE. |
| `outcome` | `string` |  |  | Outcome variable column. Alias ``y=`` accepted for R-style calls. |
| `se_method` | `string (enum)` |  | `'placebo'` | Standard-error method (see Notes). |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `time` | `string` |  |  | Time period column. |
| `treat_time` | `string` |  |  | treat_time parameter. |
| `treat_unit` | `string` |  |  | treat_unit parameter. |
| `treated_unit` | `array[string]` |  |  | Treated unit(s). Alias ``treat_unit=`` accepted. |
| `treatment_time` | `string` |  |  | First treatment period (inclusive). Alias ``treat_time=`` accepted. |
| `unit` | `string` |  |  | Unit identifier column. |
| `y` | `string` |  |  | Outcome variable column name or outcome array. |

> **backend** options: `'native'`, `'synthdid'`, `'r'`

> **method** options: `'sdid'`, `'sc'`, `'did'`

> **se_method** options: `'placebo'`, `'bootstrap'`, `'jackknife'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sdid(y="outcome", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.sequential_sdid()`

**Sequential Synthetic DID for staggered-adoption panels (Arkhangelsky & Samkov 2024): processes cohorts in adoption order using not-yet-treated donors, avoiding TWFE negative weights and SDID overlap failures.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cohort` | `string` | ✓ |  | First-treated period column; never-treated = 0 |
| `cohort_weights` | `string (enum)` |  | `'size'` | cohort_weights parameter (str). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_reps` | `integer` |  | `200` | Number of reps. |
| `never_treated_value` | `string` |  | `0` | never_treated_value parameter. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `se_method` | `string (enum)` |  | `'placebo'` | se_method parameter (str). |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

> **cohort_weights** options: `'size'`, `'equal'`

> **se_method** options: `'placebo'`, `'bootstrap'`, `'jackknife'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sequential_sdid(data=df, outcome="value", unit="value", time="value", cohort="value")
print(result.summary())
```

---
### `sp.staggered_synth()`

**Staggered Adoption Synthetic Control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `method` | `string (enum)` |  | `'separate'` | * ``'separate'`` -- fit a separate SCM for each treated unit. * ``'pooled'`` -- partially pool weights across cohorts with the same adoption time. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `penalization` | `number` |  | `0.0` | Ridge penalty on donor weights. |
| `placebo` | `boolean` |  | `True` | Run placebo inference. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treatment` | `string` | ✓ |  | Binary treatment indicator (0/1). Units transition from 0 to 1 at their respective adoption times. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

> **method** options: `'separate'`, `'pooled'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.staggered_synth(data=df, outcome="value", unit="value", time="value", treatment="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.stochastic_dominance()`

**Test for stochastic dominance of the treated distribution over the Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `order` | `integer (enum)` |  | `1` | Order of stochastic dominance. 1 = first-order (CDF dominance). 2 = second-order (integrated CDF dominance). |
| `result` | `string` | ✓ |  | Output from ``discos()`` or ``qqsynth()``. |

> **order** options: `'1'`, `'2'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.stochastic_dominance(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
### `sp.synth()`

**Unified synthetic control estimator. method= selects variant: 'classic', 'demeaned', 'detrended', 'unconstrained', 'elastic_net', 'augmented', 'sdid', 'gsynth', 'staggered'. inference= selects: 'placebo', 'conformal', 'bootstrap', 'jackknife'. Validation: certified evidence with scoped limitations. Known limitations: Classical SCM certification is specification-specific: ADH/Synth parity requires passing the same special_predictors recipe; the default outcome-only V=I path is a documented Kaul-style convention; Default native classical SCM can differ from Synth on Basque-style panels by a documented local-optimum convention (the outer V optimisation has multiple near-equivalent minima); use backend='synth' or canonical special_predictors when exact R parity is required.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `backend` | `string` |  | `'native'` | Optional reference backend for exact R parity: synth for classic SCM |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `inference` | `string` |  |  | Inference method: placebo/conformal/bootstrap/jackknife |
| `method` | `string` |  | `'classic'` | SCM variant: classic/demeaned/detrended/unconstrained/elastic_net/augmented/sdid/gsynth/staggered |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` |  |  | Treated unit (not needed for staggered) |
| `treatment` | `string` |  |  | Binary treatment column (staggered only) |
| `treatment_time` | `integer` |  |  | First treatment period |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth(data=df, outcome="value", unit="value", time="value")
print(result.summary())
```

> 📁 See also: `synth_prop99.py`, `docs/guides/migration-from-r.md`, `docs/guides/replication_workflow.md`

---
### `sp.synth_compare()`

**Run multiple SCM variants and compare them side by side.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `methods` | `array[string]` |  |  | SCM variants to compare. If ``None`` (default), all 20 registered methods are attempted, in ascending complexity order: ``classic, penalized, demeaned, detrended, unconstrained, elastic_net, augmented, sdid, gsynth, mc, discos, scpi, penscm, fdid, sparse, cluster, kernel, kernel_ridge, bayesian, bsts``. Pass an explicit subset to reduce runtime. |
| `outcome` | `string` | ✓ |  | Outcome variable column name. |
| `placebo` | `boolean` |  | `True` | Whether to run placebo inference for each method. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` |  |  | Identifier of the treated unit. |
| `treatment_time` | `string` |  |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_compare(data=df, outcome="value", unit="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_donor_sensitivity()`

**Donor-pool bootstrap sensitivity for Synthetic Control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Long-format panel. |
| `k` | `integer` |  |  | Donor subset size. Default is ``floor(J * 0.75)`` where *J* is the total number of donors. |
| `n_samples` | `integer` |  | `100` | Number of random donor subsets to draw. |
| `outcome` | `string` | ✓ |  | Outcome variable. |
| `penalization` | `number` |  | `0.0` | Ridge penalty forwarded to SCM. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `time` | `string` | ✓ |  | Time column. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_donor_sensitivity(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_experimental_design()`

**Abadie-Zhao (2025/2026) experimental-design synthetic controls: picks the best k candidate units to treat by minimising the sum of per-unit pre-period synthetic-control MSPEs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `candidates` | `array[string]` |  |  | candidates parameter (list). |
| `concentration_weight` | `number` |  | `0.0` | concentration_weight parameter (float). |
| `data` | `string` | ✓ |  | Long-format panel |
| `donors` | `array[string]` |  |  | donors parameter (list). |
| `k` | `integer` | ✓ |  | Number of units to treat |
| `n_random` | `integer` |  | `500` | Number of random. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `penalization` | `number` |  | `0.0` | penalization parameter (float). |
| `risk` | `string (enum)` |  | `'mspe'` | risk parameter (str). |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

> **risk** options: `'mspe'`, `'rmse'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_experimental_design(data=df, unit="value", time="value", outcome="value", k=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/synth_experimental.md`

---
### `sp.synth_loo()`

**Leave-one-out donor sensitivity for Synthetic Control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for z-based p-values. |
| `data` | `string` | ✓ |  | Long-format panel. |
| `outcome` | `string` | ✓ |  | Outcome variable. |
| `penalization` | `number` |  | `0.0` | Ridge penalty forwarded to SCM. |
| `time` | `string` | ✓ |  | Time column. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_loo(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_mde()`

**Minimum Detectable Effect for a Synthetic Control design.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the placebo test. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `n_simulations` | `integer` |  | `200` | Number of simulations per effect size. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `power_target` | `number` |  | `0.8` | Desired power level. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_mde(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_power()`

**Power analysis for Synthetic Control designs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the placebo test. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `effect_sizes` | `array[string]` |  |  | Grid of hypothetical additive effect sizes to evaluate. If ``None``, auto-generates 10 steps from 0 to 3 * pre-treatment SD of the outcome. |
| `n_simulations` | `integer` |  | `200` | Number of Monte-Carlo simulations per effect size. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_power(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_power_plot()`

**Plot the power curve from :func:`synth_power`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | Axes to plot on. If ``None``, a new figure is created. |
| `figsize` | `array[string]` |  | `[9, 6]` | Figure size (width, height) in inches. |
| `power_result` | `string` | ✓ |  | Output of :func:`synth_power`. Must contain columns ``effect_size``, ``power``, and ``mde_flag``. |
| `title` | `string` |  |  | Custom plot title. Defaults to ``"SCM Power Curve -- Minimum Detectable Effect"``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_power_plot(power_result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_recommend()`

**Quickly recommend the best SCM method for the given data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Long-format panel data. |
| `outcome` | `string` | ✓ |  | Outcome variable column name. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` |  |  | Identifier of the treated unit. |
| `treatment_time` | `string` |  |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_recommend(data=df, outcome="value", unit="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_report()`

**Generate a comprehensive Synthetic Control analysis report.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for CIs and hypothesis tests. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `method` | `string` |  | `'classic'` | SCM variant passed to ``synth()``. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `output` | `string` |  | `'text'` | Output format: ``'text'``, ``'markdown'``, or ``'latex'``. |
| `sensitivity` | `boolean` |  | `True` | Whether to include the sensitivity analysis section. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` |  |  | Identifier of the treated unit. |
| `treatment_time` | `string` |  |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_report(data=df, outcome="value", unit="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_report_to_file()`

**Generate an SCM report and write it directly to a file.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Long-format panel data. |
| `filename` | `string` |  | `'report.md'` | Output file path. |
| `method` | `string` |  | `'classic'` | SCM variant passed to ``synth()``. |
| `outcome` | `string` | ✓ |  | Outcome variable name. |
| `output` | `string` |  | `'markdown'` | Output format: ``'text'``, ``'markdown'``, or ``'latex'``. |
| `sensitivity` | `boolean` |  | `True` | Whether to include the sensitivity analysis section. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treated_unit` | `string` |  |  | Identifier of the treated unit. |
| `treatment_time` | `string` |  |  | First treatment period (inclusive). |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_report_to_file(data=df, outcome="value", unit="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_rmspe_filter()`

**Pre-RMSPE-filtered p-value robustness (Abadie et al. 2010).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Long-format panel. |
| `outcome` | `string` | ✓ |  | Outcome variable. |
| `penalization` | `number` |  | `0.0` | Ridge penalty. |
| `thresholds` | `array[string]` |  |  | Multiples of treated-unit pre-RMSPE used as cut-offs. Default ``[1, 2, 5, 10, 20, np.inf]``. |
| `time` | `string` | ✓ |  | Time column. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_rmspe_filter(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_sensitivity()`

**Run all SCM sensitivity diagnostics in a single call.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Long-format panel. |
| `n_donor_samples` | `integer` |  | `100` | Number of random donor subsets for donor sensitivity. |
| `outcome` | `string` | ✓ |  | Outcome variable. |
| `penalization` | `number` |  | `0.0` | Ridge penalty. |
| `seed` | `integer` |  |  | Random seed. |
| `time` | `string` | ✓ |  | Time column. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | First treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_sensitivity(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_sensitivity_plot()`

**Multi-panel sensitivity diagnostic plot.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `figsize` | `array[string]` |  | `[14, 10]` | Figure size in inches. |
| `sensitivity_result` | `object` | ✓ |  | Output from :func:`synth_sensitivity`. |
| `title` | `string` |  |  | Super-title for the figure. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_sensitivity_plot()
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_survival()`

**Synthetic Survival Control (Han & Shah 2025, arXiv:2511.14133). Fits a convex combination of donor Kaplan-Meier curves on the complementary log-log scale to match the treated arm's pre-treatment survival, then reports the post-treatment survival gap with placebo UCBs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | Long panel with one row per (unit, time) and a precomputed KM survival |
| `n_placebos` | `integer` |  | `100` | Number of placebos. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `survival` | `string` | ✓ |  | Column with survival probability S_i(t) |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat_time` | `number` | ✓ |  | treat_time parameter (float). |
| `treated` | `string` | ✓ |  | Boolean column or name of the single treated unit |
| `unit` | `string` | ✓ |  | Unit/panel-id column |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_survival(data=df, unit="value", time="value", survival="value", treated="value", treat_time=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/v1_2_frontier.md`

---
### `sp.synth_time_placebo()`

**Time-placebo ("backdating") test for Synthetic Control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Long-format panel. |
| `n_placebo_times` | `integer` |  |  | Max number of placebo treatment times to try. Default is all feasible pre-treatment times (leaving >= 2 pre-periods for each placebo fit). |
| `outcome` | `string` | ✓ |  | Outcome variable. |
| `penalization` | `number` |  | `0.0` | Ridge penalty forwarded to SCM. |
| `time` | `string` | ✓ |  | Time column. |
| `treated_unit` | `string` | ✓ |  | Identifier of the treated unit. |
| `treatment_time` | `string` | ✓ |  | Real first treatment period. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_time_placebo(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.synth_to_excel()`

**Multi-sheet Excel workbook for synthetic-control results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `digits` | `integer` |  | `6` | Rounding for floating-point values. |
| `method_names` | `array[string]` |  |  | Override sheet / column labels. |
| `obj` | `array[string]` | ✓ |  | Object to export. |
| `path` | `string` | ✓ |  | Destination ``.xlsx`` file path. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_to_excel(obj=["a", "b"], path="value")
print(result.summary())
```

---
### `sp.synth_to_latex()`

**Formatted LaTeX table for synthetic-control results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `booktabs` | `boolean` |  | `True` | If True, use ``\toprule`` / ``\midrule`` / ``\bottomrule`` (requires ``\usepackage{booktabs}``). Falls back to ``\hline`` if False. |
| `caption` | `string` |  |  | Table caption. Defaults to a sensible auto-generated string. |
| `digits` | `integer` |  | `4` | Number of decimal places. |
| `label` | `string` |  |  | LaTeX label for cross-referencing. Defaults to ``"tab:synth"`` (single) or ``"tab:synth_compare"`` (multi). |
| `method_names` | `array[string]` |  |  | Override column labels in comparison mode. |
| `obj` | `array[string]` | ✓ |  | Object to render. ``SynthComparison`` and lists trigger the side-by-side multi-method layout. |
| `show_ci` | `boolean` |  | `True` | Include the confidence-interval row. |
| `show_weights` | `boolean` |  | `False` | Append a panel listing the top-N donor weights. |
| `top_n_weights` | `integer` |  | `5` | How many donors to show per method when ``show_weights=True``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_to_latex(obj=["a", "b"])
print(result.summary())
```

---
### `sp.synth_to_markdown()`

**GitHub-flavoured Markdown table for synthetic-control results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `digits` | `integer` |  | `4` | digits parameter (int). |
| `method_names` | `array[string]` |  |  | method_names parameter (Optional[Sequence[str]]). |
| `obj` | `array[string]` | ✓ |  | obj parameter (Union[CausalResult, 'SynthComparison', List[CausalResult]]). |
| `show_ci` | `boolean` |  | `True` | show_ci parameter (bool). |
| `show_weights` | `boolean` |  | `False` | show_weights parameter (bool). |
| `title` | `string` |  |  | title parameter (Optional[str]). |
| `top_n_weights` | `integer` |  | `5` | top_n_weights parameter (int). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synth_to_markdown(obj=["a", "b"])
print(result.summary())
```

---
### `sp.synthdid_estimate()`

**R-style alias: ``synthdid::synthdid_estimate``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat_time` | `string` | ✓ |  | treat_time parameter. |
| `treat_unit` | `string` | ✓ |  | treat_unit parameter. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synthdid_estimate(y="outcome", data=df, unit="value", time="value", treat_unit="value", treat_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.synthdid_placebo()`

**Run placebo estimates assigning treatment to each control unit.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string` |  | `'sdid'` | Estimator or algorithm variant to use. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat_time` | `string` | ✓ |  | treat_time parameter. |
| `treat_unit` | `string` | ✓ |  | treat_unit parameter. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synthdid_placebo(y="outcome", data=df, unit="value", time="value", treat_unit="value", treat_time="value")
print(result.summary())
```

---
### `sp.synthdid_plot()`

**Plot observed vs synthetic trajectory.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `ci_alpha` | `number` |  | `0.15` | ci_alpha parameter (float). |
| `figsize` | `array[string]` |  | `[10, 6]` | figsize parameter (Tuple[float, float]). |
| `result` | `string` | ✓ |  | Output of :func:`sdid`. |
| `synth_color` | `string` |  | `'#E74C3C'` | synth_color parameter (str). |
| `title` | `string` |  |  | title parameter (Optional[str]). |
| `treated_color` | `string` |  | `'#2C3E50'` | treated_color parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synthdid_plot(result="value")
print(result.summary())
```

---
### `sp.synthdid_rmse_plot()`

**Pre-treatment RMSE of treated vs synthetic trajectory.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `figsize` | `array[string]` |  | `[8, 5]` | figsize parameter (Tuple[float, float]). |
| `result` | `string` | ✓ |  | result parameter (CausalResult). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synthdid_rmse_plot(result="value")
print(result.summary())
```

---
### `sp.synthdid_units_plot()`

**Horizontal bar chart of unit weight contributions.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `figsize` | `array[string]` |  | `[8, 5]` | figsize parameter (Tuple[float, float]). |
| `result` | `string` | ✓ |  | result parameter (CausalResult). |
| `top_n` | `integer` |  | `10` | Show the top-N donors by weight. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synthdid_units_plot(result="value")
print(result.summary())
```

---
### `sp.synthplot()`

**Unified plot function for all Synthetic Control variants.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | Pre-existing axes for single-panel plots. |
| `figsize` | `array[string]` |  |  | Figure size. Auto-selected if None. |
| `labels` | `array[string]` |  |  | Labels for ``type='compare'``. |
| `result` | `array[string]` | ✓ |  | Output of any ``synth()`` variant. Pass a list for ``type='compare'``. |
| `title` | `string` |  |  | Override the auto-generated title. |
| `top_n` | `integer` |  | `15` | Number of donors to show in weight plots. |
| `type` | `string` |  | `'trajectory'` | Plot type: * ``'trajectory'`` -- treated vs synthetic over time. * ``'gap'`` -- effect (gap) over time. * ``'both'`` -- two-panel: trajectory + gap. * ``'weights'`` -- donor weight bar chart. * ``'placebo'`` -- placebo ATT distribution. * ``'placebo_gap'`` -- placebo gap spaghetti plot (Abadie et al. 2010). * ``'rmspe'`` -- post/pre RMSPE ratio histogram (Abadie et al. 2010). * ``'conformal'`` -- period-level effects + conformal CIs. * ``'staggered'`` -- cohort-level ATT comparison. * ``'factors'`` -- latent factor loadings (gsynth only). * ``'compare'`` -- overlay multiple results. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synthplot(result=["a", "b"])
print(result.summary())
```

---
