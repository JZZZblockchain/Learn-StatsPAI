# panel

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Unified panel regression module for StatsPAI.

Provides a single entry point ``panel()`` covering all panel estimators:

**Static models** — FE, RE, Between, First Difference, Pooled OLS, Two-way FE
**Correlated RE** — Mundlak (1978), Chamberlain (1982)
**Dynamic panel** — Arellano-Bond, Blundell-Bond (System GMM)
**HDFE absorption** — high-dimensional fixed-effects OLS (Stata's reghdfe /
R's fixest)

All results return ``PanelResults`` with built-in diagnostics:

>>> result = sp.panel(df, "y ~ x1 + x2", entity='id', time='t')
>>> result.hausman_test()        # FE vs RE
>>> result.bp_lm_test()          # Pooled vs RE
>>> result.f_test_effects()      # Joint significance of FE
>>> result.compare('re')         # Side-by-side comparison

References
----------
Wooldridge, J.M. (2010). Econometric Analysis of Cross Section and Panel Data.
Mundlak, Y. (1978). "On the Pooling of Time Series and Cross Section Data."
Chamberlain, G. (1982). "Multivariate Regression Models for Panel Data."
Arellano, M. and Bond, S. (1991). "Some Tests of Specification for Panel Data."
Blundell, R. and Bond, S. (1998). "Initial Conditions and Moment Restrictions."
Hausman, J.A. (1978). "Specification Tests in Econometrics."
Breusch, T.S. and Pagan, A.R. (1980). "The Lagrange Multiplier Test."
Pesaran, M.H. (2004). "General Diagnostic Tests for Cross Section Dependence."
Correia, S. (2017). "Linear Models with High-Dimensional Fixed Effects."

**13 个公共函数**

### `sp.Absorber()`

**Reusable HDFE demean operator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `accelerate` | `boolean` |  | `True` | Enable Irons-Tuck Delta2 acceleration. |
| `drop_singletons` | `boolean` |  | `True` | If True, singleton observations (FE groups of size 1) are pruned before building the absorber. ``keep_mask`` stores the surviving rows. |
| `fe_data` | `string` | ✓ |  | FE columns. Must have no NaN. |
| `maxiter` | `integer` |  | `10000` | Maximum alternating-projection iterations. |
| `solver` | `string (enum)` |  | `'map'` | Within-transformation backend. ``"map"`` uses alternating projections with Irons-Tuck acceleration (default, typically fastest on well-conditioned panels). ``"lsmr"`` / ``"lsqr"`` delegate to ``scipy.sparse.linalg.lsmr`` / ``lsqr`` on the sparse FE design matrix -- more robust for ill-conditioned or highly nested FE structures. See the migration guide for how this maps to ``pyreghdfe``. |
| `tol` | `number` |  | `1e-08` | Convergence threshold on max \|dx\| per iteration. |
| `weights` | `string` |  |  | Observation weights. If given, weighted means are used. |

> **solver** options: `'map'`, `'lsmr'`, `'lsqr'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.Absorber(fe_data="value")
print(result.summary())
```

---
### `sp.FEOLSResult()`

**Result of ``sp.feols()``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `absorber` | `string` | ✓ |  | absorber parameter (Absorber). |
| `cluster_info` | `object` | ✓ |  | cluster_info parameter (Dict[str, Any]). |
| `conf_int_lower` | `string` | ✓ |  | conf_int_lower parameter (pd.Series). |
| `conf_int_upper` | `string` | ✓ |  | conf_int_upper parameter (pd.Series). |
| `converged` | `boolean` | ✓ |  | converged parameter (bool). |
| `df_resid` | `integer` | ✓ |  | df_resid parameter (int). |
| `dof_fe` | `integer` | ✓ |  | dof_fe parameter (int). |
| `fitted_within` | `string` | ✓ |  | fitted_within parameter (np.ndarray). |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `iters` | `integer` | ✓ |  | iters parameter (int). |
| `n_fe` | `array[string]` | ✓ |  | Number of fe. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `n_singletons_dropped` | `integer` | ✓ |  | Number of singletons dropped. |
| `params` | `string` | ✓ |  | params parameter (pd.Series). |
| `pvalues` | `string` | ✓ |  | pvalues parameter (pd.Series). |
| `r2_within` | `number` | ✓ |  | r2_within parameter (float). |
| `residuals` | `string` | ✓ |  | residuals parameter (np.ndarray). |
> 📝 *residuals 参数（np.ndarray）。*
| `se_type` | `string` | ✓ |  | se_type parameter (str). |
| `std_errors` | `string` | ✓ |  | std_errors parameter (pd.Series). |
| `tvalues` | `string` | ✓ |  | tvalues parameter (pd.Series). |
| `vcov` | `string` | ✓ |  | Variance-covariance estimator option. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FEOLSResult(formula="lwage ~ x1 + x2", params="value", std_errors="value", vcov="value", tvalues="value", pvalues="value", conf_int_lower="value", conf_int_upper="value", residuals="value", fitted_within="value", n_obs=1.0, n_singletons_dropped=1.0, n_fe=["a", "b"], dof_fe=1.0, df_resid=1.0, r2_within=1.0, se_type="value", absorber="value", converged=True, iters=1.0)
print(result.summary())
```

---
### `sp.MethodIncompatibility()`

**The requested method is incompatible with the data / options.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alternative_functions` | `array[string]` |  |  | alternative_functions parameter (Optional[List[str]]). |
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). |
| `message` | `string` | ✓ |  | message parameter (str). |
| `recovery_hint` | `string` |  | `''` | recovery_hint parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MethodIncompatibility(message="value")
print(result.summary())
```

---
### `sp.PanelCompareResults()`

**Side-by-side comparison of two panel models.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_a` | `string` | ✓ |  | model_a parameter (PanelResults). |
| `model_b` | `string` | ✓ |  | model_b parameter (PanelResults). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PanelCompareResults(model_a="value", model_b="value")
print(result.summary())
```

---
### `sp.PanelRegression()`

**Deprecated: use ``panel()`` directly. Kept for backward compatibility.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PanelRegression()
print(result.summary())
```

---
### `sp.PanelResults()`

**Panel regression results with built-in diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_dep_var` | `string` |  |  | _dep_var parameter (Optional[str]). |
| `_entity` | `string` |  |  | _entity parameter (Optional[str]). |
| `_formula` | `string` |  |  | Formula for the component. |
| `_indep_vars` | `array[string]` |  |  | _indep_vars parameter (Optional[List[str]]). |
| `_lm_result` | `string` |  |  | _lm_result parameter (Optional[Any]). |
| `_method` | `string` |  |  | _method parameter (Optional[str]). |
| `_panel_data` | `string` |  |  | _panel_data parameter (Optional[pandas.DataFrame]). |
| `_time` | `string` |  |  | _time parameter (Optional[str]). |
| `data_info` | `object` |  |  | data_info parameter (Optional[Dict[str, Any]]). |
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). |
| `model_info` | `object` | ✓ |  | model_info parameter (Dict[str, Any]). |
| `params` | `string` | ✓ |  | params parameter (Series). |
| `std_errors` | `string` | ✓ |  | std_errors parameter (Series). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PanelResults(formula="lwage ~ x1 + x2", params="value", std_errors="value")
print(result.summary())
```

---
### `sp.absorb_ols()`

**OLS with absorbed high-dimensional fixed effects (reghdfe-style).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Regressors *excluding* the absorbed FEs and the constant (the constant is absorbed by any FE dimension). |
| `cluster` | `array[string]` |  |  | One-way or multi-way cluster variables for robust SEs. If provided, returns cluster-robust SEs (one-way: Liang-Zeger sandwich; multi-way: inclusion-exclusion Cameron-Gelbach-Miller). |
| `drop_singletons` | `boolean` |  | `True` | drop_singletons parameter (bool). |
| `fe` | `string` | ✓ |  | Fixed-effect columns. |
| `maxiter` | `integer` |  | `10000` | Demean convergence controls. |
| `return_absorber` | `boolean` |  | `False` | If True, also return the ``Absorber`` object for reuse. |
| `solver` | `string (enum)` |  | `'map'` | Within-transformation backend. See :class:`Absorber`. |
| `tol` | `number` |  | `1e-08` | Demean convergence controls. |
| `weights` | `string` |  |  | Observation weights. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **solver** options: `'map'`, `'lsmr'`, `'lsqr'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.absorb_ols(y="outcome", X="value", fe="value")
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`

---
### `sp.balance_panel()`

**Balance a panel by keeping only units observed in every time period. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Panel data in long format. |
| `entity` | `string` | ✓ |  | Entity (unit) identifier column. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.balance_panel(data=df, entity="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`

---
### `sp.demean()`

**Return the within-transformed ``x`` and the singleton keep mask. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `drop_singletons` | `boolean` |  | `True` | drop_singletons parameter (bool). |
| `fe` | `string` | ✓ |  | fe parameter (Union[pd.DataFrame, np.ndarray]). |
| `maxiter` | `integer` |  | `10000` | maxiter parameter (int). |
| `solver` | `string` |  | `'map'` | solver parameter (str). |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `weights` | `string` |  |  | Observation weights. |
| `x` | `string` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.demean(x=["treatment", "covariate1", "covariate2"], fe="value")
print(result.summary())
```

> 📁 See also: `docs/guides/gpu_acceleration.md`, `docs/guides/panel_data.md`

---
### `sp.hdfe_ols()`

**reghdfe-style OLS with high-dimensional fixed effects. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `array[string]` |  |  | One-way or multi-way cluster column(s). |
| `conley_cutoff` | `number` |  |  | Conley distance cutoff in km for ``vce="conley"``. |
| `conley_lat` | `string` |  |  | Coordinate columns (decimal degrees) for ``vce="conley"``. |
| `conley_lon` | `string` |  |  | Coordinate columns (decimal degrees) for ``vce="conley"``. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `drop_singletons` | `boolean` |  | `True` | drop_singletons parameter (bool). |
| `formula` | `string` | ✓ |  | ``"y ~ x1 + x2 \| fe1 + fe2 + fe3"``. The ``\| fe...`` part is optional. |
| `maxiter` | `integer` |  | `10000` | maxiter parameter (int). |
| `se_type` | `string (enum)` |  |  | Override automatic inference of SE type. Usually inferred from ``cluster`` / ``wild``. |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `vce` | `string` |  |  | Canonical SE-menu keyword (matches ``sp.regress`` / ``sp.feols``): - ``"robust"`` / ``"hc1"`` -- heteroskedasticity-robust on the FE-absorbed design with reghdfe's small-sample factor ``N/(N-k-df_a)``; matches Stata ``reghdfe ..., vce(robust)``. - ``"hc0"`` -- no small-sample factor. - ``"CR2"`` / ``"CR3"`` / ``"jackknife"`` -- Pustejovsky-Tipton (2018) bias-reduced cluster-robust on the within design (requires ``cluster=``, one-way); matches R ``clubSandwich::vcovCR(plm)``. - ``"conley"`` -- Conley spatial HAC on the within design (requires ``conley_lat=/conley_lon=/conley_cutoff=``; Stata ``acreg`` planar distance convention). - ``"wild"`` -- shorthand for ``wild=True`` (requires ``cluster=``). |
| `weights` | `string` |  |  | Observation weights. Column name or raw array. |
| `wild` | `boolean` |  | `False` | If True (and ``cluster`` is given), return wild-cluster-bootstrap p-values / CIs alongside classical cluster SE. Applied variable- by-variable. Only supported with a single cluster column. |
| `wild_n_boot` | `integer` |  | `999` | Bootstrap replications. |
| `wild_seed` | `integer` |  |  | wild_seed parameter (Optional[int]). |
| `wild_weight_type` | `string (enum)` |  | `'webb'` | wild_weight_type parameter (str). |

> **se_type** options: `'iid'`, `'cluster'`, `'multiway_cluster'`, `'wild_cluster'`

> **wild_weight_type** options: `'rademacher'`, `'webb'`, `'mammen'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.hdfe_ols(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/grammar.md`, `docs/guides/panel_data.md`

---
### `sp.panel_compare()`

**Estimate the same model with multiple panel methods and return a side-by-side comparison table.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `entity` | `string` | ✓ |  | Panel entity identifier column. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `methods` | `array[string]` |  |  | List of methods to compare, default: pooled/fe/re/twoway/mundlak |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.panel_compare(formula="lwage ~ x1 + x2", data=df, entity="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`

---
### `sp.panel_logit()`

**Panel logit model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` |  |  | Column for cluster-robust SEs. |
| `data` | `string` | ✓ |  | Panel data in long format. |
| `id` | `string` |  | `'id'` | Unit and time identifier columns. |
| `maxiter` | `integer` |  | `200` | Maximum optimizer iterations. |
| `method` | `string` |  | `'fe'` | 'fe' (conditional FE logit), 're' (random effects), 'cre' (Mundlak). |
| `n_quadrature` | `integer` |  | `12` | Gauss-Hermite quadrature points (RE/CRE only). |
| `robust` | `string` |  | `'nonrobust'` | 'nonrobust' or 'robust'. |
| `time` | `string` |  | `'time'` | Unit and time identifier columns. |
| `tol` | `number` |  | `1e-08` | Gradient tolerance. |
| `x` | `array[string]` | ✓ |  | Regressors. |
| `y` | `string` | ✓ |  | Binary dependent variable (0/1). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.panel_logit(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.panel_probit()`

**Panel probit model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` |  |  | Column for cluster-robust SEs. |
| `data` | `string` | ✓ |  | Panel data in long format. |
| `id` | `string` |  | `'id'` | Unit and time identifier columns. |
| `maxiter` | `integer` |  | `200` | Maximum optimizer iterations. |
| `method` | `string` |  | `'re'` | 're' (random effects) or 'cre' (Mundlak). FE probit not supported (incidental parameters problem). |
| `n_quadrature` | `integer` |  | `12` | Gauss-Hermite quadrature points. |
| `robust` | `string` |  | `'nonrobust'` | 'nonrobust' or 'robust'. |
| `time` | `string` |  | `'time'` | Unit and time identifier columns. |
| `tol` | `number` |  | `1e-08` | Gradient tolerance. |
| `x` | `array[string]` | ✓ |  | Regressors. |
| `y` | `string` | ✓ |  | Binary dependent variable (0/1). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.panel_probit(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
