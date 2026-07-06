# frontier

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Stochastic frontier analysis (SFA).

Cross-sectional estimators: :func:`frontier` (half-normal / exponential /
truncated-normal; supports heteroskedastic ``sigma_u`` & ``sigma_v`` plus
inefficiency determinants ``emean``).

Panel estimators: :func:`xtfrontier` with ``model`` in
``{'ti', 'tvd', 'bc95'}`` (Pitt-Lee 1981, Battese-Coelli 1992,
Battese-Coelli 1995).

Helpers: :func:`te_summary`.

**12 个公共函数**

### `sp.FrontierResult()`

**Result object returned by :func:`frontier` and :func:`xtfrontier`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
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

result = sp.FrontierResult(params="value", std_errors="value")
print(result.summary())
```

---
### `sp.MalmquistResult()`

**Container for Malmquist productivity index decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data_info` | `object` | ✓ |  | data_info parameter (Dict[str, Any]). |
> 📝 *data_info 参数（字典）。*
| `index_table` | `string` | ✓ |  | index_table parameter (pd.DataFrame). |
> 📝 *index_table 参数（pd.DataFrame）。*
| `period_frontiers` | `object` | ✓ |  | period_frontiers parameter (Dict[Any, FrontierResult]). |
> 📝 *period_frontiers 参数（字典，值为 FrontierResult）。*
| `summary_by_period` | `string` | ✓ |  | summary_by_period parameter (pd.DataFrame). |
> 📝 *summary_by_period 参数（pd.DataFrame）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MalmquistResult(index_table="value", summary_by_period="value")
print(result.summary())
```

---
### `sp.MetafrontierResult()`

**Container for a metafrontier fit.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_groups` | `object` | ✓ |  | beta_groups parameter (Dict[Any, pd.Series]). |
| `beta_meta` | `string` | ✓ |  | beta_meta parameter (pd.Series). |
| `data_info` | `object` | ✓ |  | data_info parameter (Dict[str, Any]). |
> 📝 *data_info 参数（字典）。*
| `group_frontiers` | `object` | ✓ |  | group_frontiers parameter (Dict[Any, FrontierResult]). |
| `lp_status` | `string` | ✓ |  | lp_status parameter (str). |
| `te_group` | `string` | ✓ |  | te_group parameter (pd.Series). |
| `te_meta` | `string` | ✓ |  | te_meta parameter (pd.Series). |
| `tgr` | `string` | ✓ |  | tgr parameter (pd.Series). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MetafrontierResult(beta_meta="value", tgr="value", te_meta="value", te_group="value", lp_status="value")
print(result.summary())
```

---
### `sp.frontier()`

**Estimate a cross-sectional stochastic frontier model by ML. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `B` | `integer` |  | `400` | B parameter (int). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster variable for cluster-robust SE (Liang-Zeger 1986). When specified, implies ``vce='robust'`` aggregated over clusters. |
| `cost` | `boolean` |  | `False` | If True, estimate a cost frontier (composed error ``v + u``). |
| `data` | `string` | ✓ |  | Cross-sectional data. Rows with missing values in any referenced column are dropped. |
| `dist` | `string (enum)` |  | `'half-normal'` | Distribution of the inefficiency term ``u``. |
| `emean` | `array[string]` |  |  | Columns parameterizing ``mu_i = delta' [1, z_i]`` for the truncated normal (Battese-Coelli 1995; Kumbhakar-Ghosh-McGuckin 1991). Requires ``dist='truncated-normal'``. |
| `maxiter` | `integer` |  | `2000` | maxiter parameter (int). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `start` | `string` |  |  | User-supplied starting values for the full parameter vector. |
| `te_method` | `string (enum)` |  | `'bc'` | Default technical-efficiency formula accessed via ``.efficiency()``. |
| `tol` | `number` |  | `1e-10` | Numerical convergence tolerance. |
| `usigma` | `array[string]` |  |  | Columns parameterizing ``ln sigma_u_i = gamma_u' [1, w_i]`` (Caudill-Ford-Gropper 1995). |
| `vce` | `string (enum)` |  | `'oim'` | Variance-covariance estimator: ``'oim'`` -- observed information matrix (inverse numerical Hessian). ``'opg'`` -- outer product of gradients (Berndt-Hall-Hall-Hausman). ``'robust'`` -- sandwich ``H^{-1} (S' S) H^{-1}`` (White 1982). |
| `vsigma` | `array[string]` |  |  | Columns parameterizing ``ln sigma_v_i = gamma_v' [1, r_i]`` (Wang 2002). |
| `x` | `array[string]` | ✓ |  | Frontier regressors (a constant is added automatically). |
| `y` | `string` | ✓ |  | Dependent variable (output for production, cost for cost frontier). |

> **dist** options: `'half-normal'`, `'exponential'`, `'truncated-normal'`

> **te_method** options: `'bc'`, `'jlms'`

> **vce** options: `'oim'`, `'opg'`, `'robust'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.frontier(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.lcsf()`

**Two-class Latent-Class SFA (Orea-Kumbhakar 2004; Greene 2005).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `cost` | `boolean` |  | `False` | cost parameter (bool). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dist` | `string` |  | `'half-normal'` | dist parameter (str). |
| `maxiter` | `integer` |  | `500` | maxiter parameter (int). |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `vce` | `string` |  | `'oim'` | vce parameter (str). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `z_class` | `array[string]` |  |  | Covariates shifting the class-1 logit probability. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lcsf(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.malmquist()`

**Compute the Malmquist productivity index via period-by-period SFA.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cost` | `boolean` |  | `False` | cost parameter (bool). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dist` | `string` |  | `'half-normal'` | dist parameter (str). |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. |
| `overflow_threshold` | `number` |  | `1000000.0` | Any firm-level ``m_index`` / ``ec`` / ``tc`` whose absolute value exceeds this is replaced with NaN and a UserWarning is emitted. Protects summary statistics from contamination by degenerate per-period frontier fits. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.malmquist(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, id="value", time="value")
print(result.summary())
```

---
### `sp.metafrontier()`

**Estimate a metafrontier across ``K`` groups.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cost` | `boolean` |  | `False` | cost parameter (bool). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dist` | `string` |  | `'half-normal'` | dist parameter (str). |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `lp_tol` | `number` |  | `1e-07` | Primal / dual feasibility tolerance forwarded to HiGHS. With thousands of constraints and floating-point group betas, HiGHS can declare numerical infeasibility on mathematically feasible problems; loosening ``lp_tol`` (e.g., ``1e-6``) typically recovers these cases. |
| `te_method` | `string (enum)` |  | `'bc'` | te_method parameter (str). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **te_method** options: `'bc'`, `'jlms'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.metafrontier(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.te_rank()`

**Return efficiency scores sorted descending, with rank column.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `B` | `integer` |  | `500` | B parameter (int). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `method` | `string` |  |  | Estimator or algorithm variant to use. |
| `result` | `string` | ✓ |  | result parameter. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `with_ci` | `boolean` |  | `False` | with_ci parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.te_rank(result="value")
print(result.summary())
```

---
### `sp.te_summary()`

**Return a small descriptive DataFrame of TE scores (summary stats only).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | `string` |  |  | Estimator or algorithm variant to use. |
| `result` | `string` | ✓ |  | result parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.te_summary(result="value")
print(result.summary())
```

---
### `sp.translog_design()`

**Build a translog design matrix from Cobb-Douglas inputs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `include_interactions` | `boolean` |  | `True` | If True, adds ``x_k * x_l`` for k < l. |
| `include_squares` | `boolean` |  | `True` | If True, adds ``0.5 * x_k^2`` terms (translog convention). |
| `inputs` | `array[string]` | ✓ |  | Columns containing ``log x_k`` terms (already log-transformed). |
| `interaction_prefix` | `string` |  | `''` | Optional prefix for the generated columns (e.g., ``"tl_"``). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.translog_design(data=df, inputs=["a", "b"])
print(result.summary())
```

---
### `sp.xtfrontier()`

**Panel stochastic frontier estimator. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bias_correct` | `boolean` |  | `False` | TFE-only. If True, applies Dhaene-Jochmans (2015) split-panel jackknife to reduce the O(1/T) incidental-parameters bias on ``beta`` and ``sigma_u``. |
| `cluster` | `string` |  |  | Column name for cluster-robust SEs. Defaults to ``id`` whenever ``vce != 'oim'`` (the natural grouping for panels). |
| `cost` | `boolean` |  | `False` | cost parameter (bool). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dist` | `string (enum)` |  | `'half-normal'` | For ``ti``, ``tvd``, ``tfe``, ``tre``. BC95 always uses TN. |
| `emean` | `array[string]` |  |  | Required for ``model='bc95'``; inefficiency determinants ``z_it``. |
| `id` | `string` | ✓ |  | Panel unit identifier. |
| `maxiter` | `integer` |  | `500` | maxiter parameter (int). |
| `model` | `string (enum)` |  | `'ti'` | ``'ti'`` Pitt-Lee (1981) time-invariant inefficiency. ``'tvd'`` Battese-Coelli (1992) time-varying decay. ``'bc95'`` Battese-Coelli (1995) inefficiency effects model (requires ``emean``). ``'tfe'`` Greene (2005) True Fixed Effects: unit dummies + cross-sectional composed error. Recommended for T >= ~10. ``'tre'`` Greene (2005) True Random Effects: ``alpha_i ~ N(0, sigma_alpha^2)`` integrated out by Gauss-Hermite quadrature. |
| `n_quad` | `integer` |  | `24` | TRE-only. Number of Gauss-Hermite nodes used to integrate out ``alpha_i``. Increase to 48 or 64 when ``sigma_alpha`` is large relative to ``sigma_v`` (large between-firm heterogeneity) so that the quadrature tails are not truncated. A warning is emitted when the fitted ``sigma_alpha`` suggests insufficient tail coverage at the chosen ``n_quad``. |
| `time` | `string` |  |  | Time variable (required for ``model='tvd'`` and recommended for all panel models; falls back to observation order otherwise). |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `vce` | `string (enum)` |  | `'oim'` | Variance-covariance estimator. ``'oim'`` uses the inverse observed information. ``'opg'`` is the outer product of gradients (BHHH). ``'robust'`` is the sandwich ``H^-1 (S'S) H^-1``. Passing ``cluster=`` implies cluster-robust SEs (Liang-Zeger 1986). Note: ``vce='bootstrap'`` is only available on the cross-sectional :func:`frontier`; for panel models use ``'robust'`` with ``cluster=id`` instead. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **dist** options: `'half-normal'`, `'truncated-normal'`

> **model** options: `'ti'`, `'tvd'`, `'bc95'`, `'tfe'`, `'tre'`

> **vce** options: `'oim'`, `'opg'`, `'robust'`, `'cluster'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.xtfrontier(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, id="value")
print(result.summary())
```

---
### `sp.zisf()`

**Zero-Inefficiency Stochastic Frontier (Kumbhakar-Parmeter-Tsionas 2013).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `cost` | `boolean` |  | `False` | cost parameter (bool). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dist` | `string` |  | `'half-normal'` | Distribution of ``u`` in the inefficient regime. Currently only half-normal is supported (KPT 2013 baseline). |
| `maxiter` | `integer` |  | `500` | maxiter parameter (int). |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `vce` | `string` |  | `'oim'` | vce parameter (str). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `zprob` | `array[string]` |  |  | Covariates for the mixing probability; a constant is added. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.zisf(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
