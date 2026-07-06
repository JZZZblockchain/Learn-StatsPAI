# bartik

> 📂 所属分类:06 · 贝叶斯方法 (Bayesian Methods)

Shift-Share (Bartik) Instrumental Variables for StatsPAI.

Constructs Bartik instruments from industry shares and national shocks,
with diagnostics for instrument validity following Goldsmith-Pinkham,
Sorkin, and Swift (2020) and Borusyak, Hull, and Jaravel (2022).

References
----------
Goldsmith-Pinkham, P., Sorkin, I., and Swift, H. (2020).
"Bartik Instruments: What, When, Why, and How."
*American Economic Review*, 110(8), 2586-2624. [@goldsmithpinkham2020bartik]

Borusyak, K., Hull, P., and Jaravel, X. (2022).
"Quasi-Experimental Shift-Share Research Designs."
*Review of Economic Studies*, 89(1), 181-213. [@borusyak2022quasi]

**8 个公共函数**

### `sp.BartikIV()`

**Bartik Shift-Share IV estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | endog parameter (str). |
| `leave_one_out` | `boolean` |  | `True` | leave_one_out parameter (bool). |
| `regional_shocks` | `string` |  |  | regional_shocks parameter (Optional[pandas.DataFrame]). |
| `robust` | `string` |  | `'hc1'` | Robust standard-error or covariance estimator option. |
| `shares` | `string` | ✓ |  | shares parameter (DataFrame). |
| `shocks` | `string` | ✓ |  | shocks parameter (Series). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BartikIV(y="outcome", data=df, endog="value", shares="value", shocks="value")
print(result.summary())
```

---
### `sp.ShiftSharePoliticalPanelResult()`

**Structured output of :func:`shift_share_political_panel`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `diagnostics` | `object` |  | `None` | diagnostics parameter (Dict[str, Any]). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` |  | `'shift_share_political_panel'` | Estimator or algorithm variant to use. |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `n_industries` | `integer` | ✓ |  | Number of industries. |
| `n_periods` | `integer` | ✓ |  | Number of periods. |
| `n_units` | `integer` | ✓ |  | Number of units. |
| `per_period` | `string` | ✓ |  | per_period parameter (pd.DataFrame). |
| `rotemberg_panel` | `string` | ✓ |  | rotemberg_panel parameter (pd.DataFrame). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `share_balance` | `string` | ✓ |  | share_balance parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ShiftSharePoliticalPanelResult(estimate=1.0, se=1.0, ci=["a", "b"], per_period="value", rotemberg_panel="value", share_balance="value", n_units=1.0, n_periods=1.0, n_industries=1.0)
print(result.summary())
```

---
### `sp.ShiftSharePoliticalResult()`

**Structured output of :func:`shift_share_political`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `diagnostics` | `object` |  | `None` | diagnostics parameter (Dict[str, Any]). |
| `iv_result` | `string` | ✓ |  | iv_result parameter (CausalResult). |
| `method` | `string` |  | `'shift_share_political'` | Estimator or algorithm variant to use. |
| `n_industries` | `integer` | ✓ |  | Number of industries. |
| `n_periods` | `integer` | ✓ |  | Number of periods. |
| `n_units` | `integer` | ✓ |  | Number of units. |
| `rotemberg_top` | `string` | ✓ |  | rotemberg_top parameter (pd.DataFrame). |
| `share_balance` | `string` | ✓ |  | share_balance parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ShiftSharePoliticalResult(iv_result="value", rotemberg_top="value", share_balance="value", n_units=1.0, n_periods=1.0, n_industries=1.0)
print(result.summary())
```

---
### `sp.bartik()`

**Bartik / shift-share IV estimator (Adao-Kolesar-Morales 2019; Borusyak-Hull-Jaravel 2022). Uses pre-period industry / group shares x exogenous shocks as an instrument for local outcome exposure.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | Endogenous local exposure being instrumented (e.g. employment growth) |
| `shares` | `string` | ✓ |  | Pre-period share column (e.g. industry share) |
| `shocks` | `string` | ✓ |  | Shock column (e.g. industry-level change) |
| `y` | `string` | ✓ |  | Outcome (e.g. local wage growth) |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bartik(y="outcome", data=df, endog="value", shares="value", shocks="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_iv_estimator.md`

---
### `sp.shift_share_political()`

**Park-Xu (2026) political-science shift-share IV: long-difference Bartik IV with AKM shock-cluster SE, Rotemberg top-K, and share-balance diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | endog parameter (str). |
| `leave_one_out` | `boolean` |  | `True` | leave_one_out parameter (bool). |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `shares` | `string` | ✓ |  | shares parameter (DataFrame). |
| `shocks` | `string` | ✓ |  | shocks parameter (Series). |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.shift_share_political(data=df, unit="value", time="value", outcome="value", endog="value", shares="value", shocks="value")
print(result.summary())
```

---
### `sp.shift_share_political_panel()`

**Multi-period panel shift-share IV (Park-Xu 2026 Section 4.2): pooled 2SLS with unit/time/two-way FEs over a time-varying Bartik instrument. Reports per-period event-study, aggregate Rotemberg top-K, and share-balance F-tests.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string (enum)` |  | `'unit'` | Cluster identifier column for clustered standard errors. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | endog parameter (str). |
| `fe` | `string (enum)` |  | `'two-way'` | fe parameter (str). |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `shares` | `string` | ✓ |  | shares parameter (DataFrame). |
| `shocks` | `string` | ✓ |  | shocks parameter (DataFrame). |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

> **cluster** options: `'unit'`, `'time'`, `'twoway'`

> **fe** options: `'two-way'`, `'unit'`, `'time'`, `'none'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.shift_share_political_panel(data=df, unit="value", time="value", outcome="value", endog="value", shares="value", shocks="value")
print(result.summary())
```

> 📁 See also: `docs/guides/shift_share_political_panel.md`

---
### `sp.shift_share_se()`

**Correct standard errors of an existing IV result for shift-share structure.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `iv_result` | `string` | ✓ |  | An IV estimation result that contains ``residuals`` and a ``fitted_values`` in its ``data_info``, plus the instrument residualised values (stored by Bartik estimator). |
| `shares` | `string` | ✓ |  | Exposure-share matrix. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.shift_share_se(iv_result="value", shares="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_iv_estimator.md`

---
### `sp.ssaggregate()`

**Shift-share IV estimation with AKM (2019) corrected standard errors.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `cluster` | `string` |  |  | Observation-level cluster variable (not used in the AKM variance; retained for compatibility and diagnostics). |
| `controls` | `array[string]` |  |  | Exogenous control variables. |
| `data` | `string` | ✓ |  | Observation-level data (n rows). |
| `shares` | `string` | ✓ |  | Exposure-share matrix. ``shares[i, k]`` is unit *i*'s exposure to shock *k*. |
| `shock_data` | `string` |  |  | Shock-level DataFrame (K rows) when *shocks* is a column name. |
| `shocks` | `string` |  |  | Shock vector. Either a 1-D array/Series of length K, or a column name in *shock_data*. If ``None``, the Bartik variable in *x* is used directly (reduced-form mode). |
| `x` | `string` | ✓ |  | Endogenous regressor / constructed Bartik IV column in *data*. If the column is the constructed Bartik instrument itself (i.e. the reduced-form specification), the estimator runs OLS and corrects SEs. If it is an endogenous regressor, a Bartik IV is constructed from *shares* and *shocks* for the first stage. |
| `y` | `string` | ✓ |  | Outcome variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ssaggregate(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, shares="value")
print(result.summary())
```

---
