# structural

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Structural estimation methods.

**12 个公共函数**

### `sp.BLPResult()`

**Results from BLP demand estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_data_index` | `string` | ✓ |  | _data_index parameter (pd.Index). |
| `_elasticity_matrices` | `object` | ✓ |  | _elasticity_matrices parameter (dict). |
| `_market_ids` | `string` | ✓ |  | _market_ids parameter (np.ndarray). |
| `_product_ids` | `string` | ✓ |  | _product_ids parameter (np.ndarray). |
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `converged` | `boolean` | ✓ |  | converged parameter (bool). |
| `gmm_objective` | `number` | ✓ |  | gmm_objective parameter (float). |
| `linear_params` | `string` | ✓ |  | linear_params parameter (pd.Series). |
| `mean_utility` | `string` | ✓ |  | mean_utility parameter (pd.Series). |
| `n_markets` | `integer` | ✓ |  | Number of markets. |
| `n_products` | `integer` | ✓ |  | Number of products. |
| `nonlinear_params` | `string` | ✓ |  | nonlinear_params parameter (pd.Series). |
| `own_elasticities` | `string` | ✓ |  | own_elasticities parameter (pd.Series). |
| `se_linear` | `string` | ✓ |  | se_linear parameter (pd.Series). |
| `se_nonlinear` | `string` | ✓ |  | se_nonlinear parameter (pd.Series). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BLPResult(linear_params="value", nonlinear_params="value", se_linear="value", se_nonlinear="value", mean_utility="value", own_elasticities="value", n_markets=1.0, n_products=1.0, gmm_objective=1.0, converged=True, _market_ids="value", _product_ids="value", _data_index="value", alpha=1.0)
print(result.summary())
```

---
### `sp.ProductionResult()`

**Result object for production function estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coef` | `object` | ✓ |  | coef parameter (Dict[str, float]). |
| `cov` | `string` |  |  | cov parameter (Optional[np.ndarray]). |
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  |  | model_info parameter (Optional[Dict[str, Any]]). |
| `params` | `string` | ✓ |  | params parameter (pd.Series). |
| `productivity_process` | `object` | ✓ |  | productivity_process parameter (Dict[str, float]). |
| `residuals` | `string` | ✓ |  | residuals parameter (np.ndarray). |
> 📝 *residuals 参数（np.ndarray）。*
| `sample` | `string` | ✓ |  | sample parameter (pd.DataFrame). |
| `std_errors` | `string` | ✓ |  | std_errors parameter (pd.Series). |
| `tfp` | `string` | ✓ |  | tfp parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ProductionResult(method="value", params="value", std_errors="value", tfp="value", residuals="value", sample="value")
print(result.summary())
```

---
### `sp.acf()`

**Alias for sp.ackerberg_caves_frazer. Ackerberg-Caves-Frazer (2015) production function estimator. Modern default. Corrects the OP/LP identification problem: all coefficient identification moves to stage 2, with free inputs instrumented by their lagged values and state inputs at the contemporaneous level. Aliased as sp.acf.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | boot_reps parameter (int). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `free` | `array[string]` |  |  | Default ['l']. Instrumented with lag in stage 2. |
| `functional_form` | `string (enum)` |  | `'cobb-douglas'` | Production function form |
| `output` | `string` |  | `'y'` | output parameter (str). |
| `panel_id` | `string` |  | `'id'` | panel_id parameter (str). |
| `polynomial_degree` | `integer` |  | `3` | polynomial_degree parameter (int). |
| `productivity_degree` | `integer` |  | `1` | productivity_degree parameter (int). |
| `proxy` | `string` |  | `'m'` | proxy parameter (str). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | Default ['k']. |
| `time` | `string` |  | `'year'` | Time period column. |

> **functional_form** options: `'cobb-douglas'`, `'translog'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.acf(data=df)
print(result.summary())
```

---
### `sp.ackerberg_caves_frazer()`

**Ackerberg-Caves-Frazer (2015) production function estimator. Modern default. Corrects the OP/LP identification problem: all coefficient identification moves to stage 2, with free inputs instrumented by their lagged values and state inputs at the contemporaneous level. Aliased as sp.acf.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | boot_reps parameter (int). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `free` | `array[string]` |  |  | Default ['l']. Instrumented with lag in stage 2. |
| `functional_form` | `string (enum)` |  | `'cobb-douglas'` | Production function form |
| `output` | `string` |  | `'y'` | output parameter (str). |
| `panel_id` | `string` |  | `'id'` | panel_id parameter (str). |
| `polynomial_degree` | `integer` |  | `3` | polynomial_degree parameter (int). |
| `productivity_degree` | `integer` |  | `1` | productivity_degree parameter (int). |
| `proxy` | `string` |  | `'m'` | proxy parameter (str). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | Default ['k']. |
| `time` | `string` |  | `'year'` | Time period column. |

> **functional_form** options: `'cobb-douglas'`, `'translog'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ackerberg_caves_frazer(data=df)
print(result.summary())
```

---
### `sp.blp()`

**Estimate a BLP random-coefficients logit demand model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level (used in summary output). |
| `data` | `string` | ✓ |  | Panel of product-market observations. |
| `instruments` | `array[string]` |  |  | Excluded instrument columns. If None, standard BLP instruments (functions of own and rival characteristics) are constructed. |
| `market_id` | `string` |  | `'market_id'` | Column identifying markets. |
| `maxiter` | `integer` |  | `200` | Maximum outer-loop iterations. |
| `method` | `string` |  | `'contraction'` | Inner-loop method. Currently only 'contraction' (NFP) is supported. |
| `n_draws` | `integer` |  | `200` | Number of quasi-Monte Carlo draws for integration. |
| `prices` | `string` | ✓ |  | Column name for product prices. |
| `product_id` | `string` |  | `'product_id'` | Column identifying products. |
| `seed` | `integer` |  |  | Random seed for reproducibility of Monte Carlo draws. |
| `shares` | `string` | ✓ |  | Column name for observed market shares (0 < s < 1). |
| `tol_inner` | `number` |  | `1e-12` | Contraction mapping tolerance. |
| `tol_outer` | `number` |  | `1e-06` | Outer-loop GMM tolerance. |
| `x_linear` | `array[string]` | ✓ |  | Product characteristics entering mean utility linearly. These will be included alongside price in the linear part. |
| `x_random` | `array[string]` |  |  | Subset of x_linear that also have random coefficients. If None, defaults to all of x_linear. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.blp(data=df, shares="value", prices="value", x_linear=["a", "b"])
print(result.summary())
```

---
### `sp.levinsohn_petrin()`

**Levinsohn-Petrin (2003) production function estimator. Uses intermediate inputs (materials/energy) as proxy -- avoids the OP zero-investment selection problem. Same ACF caveat applies to beta_l identification: prefer sp.acf for rigorous identification.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | boot_reps parameter (int). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `free` | `array[string]` |  |  | Default ['l']. |
| `functional_form` | `string (enum)` |  | `'cobb-douglas'` | Production function form |
| `output` | `string` |  | `'y'` | output parameter (str). |
| `panel_id` | `string` |  | `'id'` | panel_id parameter (str). |
| `polynomial_degree` | `integer` |  | `3` | polynomial_degree parameter (int). |
| `productivity_degree` | `integer` |  | `1` | productivity_degree parameter (int). |
| `proxy` | `string` |  | `'m'` | Intermediate input. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | Default ['k']. |
| `time` | `string` |  | `'year'` | Time period column. |

> **functional_form** options: `'cobb-douglas'`, `'translog'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.levinsohn_petrin(data=df)
print(result.summary())
```

---
### `sp.levpet()`

**Alias for sp.levinsohn_petrin. Levinsohn-Petrin (2003) production function estimator. Uses intermediate inputs (materials/energy) as proxy -- avoids the OP zero-investment selection problem. Same ACF caveat applies to beta_l identification: prefer sp.acf for rigorous identification.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | boot_reps parameter (int). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `free` | `array[string]` |  |  | Default ['l']. |
| `functional_form` | `string (enum)` |  | `'cobb-douglas'` | Production function form |
| `output` | `string` |  | `'y'` | output parameter (str). |
| `panel_id` | `string` |  | `'id'` | panel_id parameter (str). |
| `polynomial_degree` | `integer` |  | `3` | polynomial_degree parameter (int). |
| `productivity_degree` | `integer` |  | `1` | productivity_degree parameter (int). |
| `proxy` | `string` |  | `'m'` | Intermediate input. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | Default ['k']. |
| `time` | `string` |  | `'year'` | Time period column. |

> **functional_form** options: `'cobb-douglas'`, `'translog'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.levpet(data=df)
print(result.summary())
```

---
### `sp.markup()`

**De Loecker & Warzynski (2012) firm-time markup estimator. Takes a fitted ProductionResult plus revenue and input-cost columns; returns mu_it = theta_v_it * (PQ)/(P_v V) where theta_v is the output elasticity of the flexible input. Cobb-Douglas only for now (translog forthcoming).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `correct_eta` | `boolean` |  | `True` | Subtract stage-1 i.i.d. shock from log revenue. |
| `flexible_input` | `string` |  | `'m'` | flexible_input parameter (str). |
| `input_cost` | `string` | ✓ |  | Log expenditure on flexible input. |
| `result` | `string` | ✓ |  | result parameter (ProductionResult). |
| `revenue` | `string` | ✓ |  | Log revenue column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.markup(result="value", revenue="value", input_cost="value")
print(result.summary())
```

---
### `sp.olley_pakes()`

**Olley-Pakes (1996) production function estimator. Two-stage control function with INVESTMENT as the productivity proxy. Drops zero-investment firms (required for the inversion). Note: beta_l identification can fail if labor responds to current productivity (ACF critique) -- prefer sp.acf for modern work.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | boot_reps parameter (int). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `drop_zero_proxy` | `boolean` |  | `True` | drop_zero_proxy parameter (bool). |
| `free` | `array[string]` |  |  | Default ['l']. |
| `functional_form` | `string (enum)` |  | `'cobb-douglas'` | Production function form |
| `output` | `string` |  | `'y'` | output parameter (str). |
| `panel_id` | `string` |  | `'id'` | panel_id parameter (str). |
| `polynomial_degree` | `integer` |  | `3` | polynomial_degree parameter (int). |
| `productivity_degree` | `integer` |  | `1` | productivity_degree parameter (int). |
| `proxy` | `string` |  | `'i'` | Investment column (must be > 0). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | Default ['k']. |
| `time` | `string` |  | `'year'` | Time period column. |

> **functional_form** options: `'cobb-douglas'`, `'translog'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.olley_pakes(data=df)
print(result.summary())
```

---
### `sp.opreg()`

**Alias for sp.olley_pakes. Olley-Pakes (1996) production function estimator. Two-stage control function with INVESTMENT as the productivity proxy. Drops zero-investment firms (required for the inversion). Note: beta_l identification can fail if labor responds to current productivity (ACF critique) -- prefer sp.acf for modern work.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | boot_reps parameter (int). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `drop_zero_proxy` | `boolean` |  | `True` | drop_zero_proxy parameter (bool). |
| `free` | `array[string]` |  |  | Default ['l']. |
| `functional_form` | `string (enum)` |  | `'cobb-douglas'` | Production function form |
| `output` | `string` |  | `'y'` | output parameter (str). |
| `panel_id` | `string` |  | `'id'` | panel_id parameter (str). |
| `polynomial_degree` | `integer` |  | `3` | polynomial_degree parameter (int). |
| `productivity_degree` | `integer` |  | `1` | productivity_degree parameter (int). |
| `proxy` | `string` |  | `'i'` | Investment column (must be > 0). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | Default ['k']. |
| `time` | `string` |  | `'year'` | Time period column. |

> **functional_form** options: `'cobb-douglas'`, `'translog'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.opreg(data=df)
print(result.summary())
```

---
### `sp.prod_fn()`

**Production function estimator (Cobb-Douglas) -- unified method= dispatcher. Solves the simultaneity between input choices and unobserved productivity by inverting an input policy as a control function. method= selects: 'op' (Olley-Pakes 1996, investment proxy), 'lp' (Levinsohn-Petrin 2003, intermediate-input proxy), 'acf' (Ackerberg-Caves-Frazer 2015, corrected identification -- DEFAULT), 'wrdg' (Wooldridge 2009, one-step joint GMM).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | Firm-cluster bootstrap replications for SE. |
| `data` | `string` | ✓ |  | Long panel: one row per (firm, year). |
| `free` | `array[string]` |  |  | Free inputs, default ['l']. |
| `functional_form` | `string (enum)` |  | `'cobb-douglas'` | Production function form (translog adds quadratic + cross terms). |
| `method` | `string (enum)` |  | `'acf'` | Estimator |
| `output` | `string` |  | `'y'` | Log output column. |
| `panel_id` | `string` |  | `'id'` | Firm identifier column. |
| `polynomial_degree` | `integer` |  | `3` | Stage-1 polynomial degree. |
| `productivity_degree` | `integer` |  | `1` | Productivity AR polynomial degree (1=linear AR(1), recommended). |
| `proxy` | `string` |  |  | Proxy column. Defaults to 'i' for OP, 'm' otherwise. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | State/predetermined inputs, default ['k']. |
| `time` | `string` |  | `'year'` | Time identifier column. |

> **functional_form** options: `'cobb-douglas'`, `'translog'`

> **method** options: `'op'`, `'lp'`, `'acf'`, `'wrdg'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.prod_fn(data=df)
print(result.summary())
```

---
### `sp.wooldridge_prod()`

**Wooldridge (2009) one-step GMM production function estimator. Stacks the level equation and the productivity-substituted equation into a single nonlinear LS problem. More efficient than two-step ACF; covariance matrix available without bootstrap.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boot_reps` | `integer` |  | `0` | boot_reps parameter (int). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `free` | `array[string]` |  |  | Default ['l']. |
| `output` | `string` |  | `'y'` | output parameter (str). |
| `panel_id` | `string` |  | `'id'` | panel_id parameter (str). |
| `polynomial_degree` | `integer` |  | `2` | Lower than ACF default -- joint problem is higher-dimensional. |
| `productivity_degree` | `integer` |  | `2` | productivity_degree parameter (int). |
| `proxy` | `string` |  | `'m'` | proxy parameter (str). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `state` | `array[string]` |  |  | Default ['k']. |
| `time` | `string` |  | `'year'` | Time period column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.wooldridge_prod(data=df)
print(result.summary())
```

---
