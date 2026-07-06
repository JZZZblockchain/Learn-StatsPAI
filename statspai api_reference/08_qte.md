# qte

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Quantile Treatment Effects (QTE) module for StatsPAI.

Provides estimators for:
- **Quantile DID** (Athey & Imbens 2006) — DID at each quantile
- **QTE via Quantile Regression** (Firpo 2007) — conditional QTE with controls
- **QTE via Distribution** — propensity-score reweighting approach

References
----------
Athey, S. & Imbens, G. W. (2006).
    Identification and Inference in Nonlinear Difference-in-Differences Models.
    *Econometrica*, 74(2), 431-497. [@athey2006identification]

Firpo, S. (2007).
    Efficient Semiparametric Estimation of Quantile Treatment Effects.
    *Econometrica*, 75(1), 259-276. [@firpo2007efficient]

**12 个公共函数**

### `sp.BeyondAverageResult()`

**Distributional LATE on compliers.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_high` | `string` | ✓ |  | ci_high parameter (np.ndarray). |
| `ci_low` | `string` | ✓ |  | ci_low parameter (np.ndarray). |
| `complier_share` | `number` | ✓ |  | complier_share parameter (float). |
| `late_q` | `string` | ✓ |  | late_q parameter (np.ndarray). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `quantiles` | `string` | ✓ |  | quantiles parameter (np.ndarray). |
| `se_q` | `string` | ✓ |  | se_q parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BeyondAverageResult(quantiles="value", late_q="value", se_q="value", ci_low="value", ci_high="value", complier_share=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.DTEResult()`

**Container for distributional treatment effect estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cdf_counterfactual` | `string` | ✓ |  | cdf_counterfactual parameter. |
| `cdf_treated` | `string` | ✓ |  | cdf_treated parameter. |
| `dte` | `string` | ✓ |  | dte parameter. |
| `dte_se` | `string` | ✓ |  | dte_se parameter. |
| `grid` | `string` | ✓ |  | grid parameter. |
| `ks_pvalue` | `string` | ✓ |  | ks_pvalue parameter. |
| `ks_stat` | `string` | ✓ |  | ks_stat parameter. |
| `method` | `string` |  | `'ipw'` | Estimator or algorithm variant to use. |
| `n_obs` | `string` | ✓ |  | Number of obs. |
| `qte_effects` | `string` | ✓ |  | qte_effects parameter. |
| `qte_se` | `string` | ✓ |  | qte_se parameter. |
| `qte_taus` | `string` | ✓ |  | qte_taus parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DTEResult(grid="value", dte="value", dte_se="value", qte_taus="value", qte_effects="value", qte_se="value", cdf_treated="value", cdf_counterfactual="value", ks_stat="value", ks_pvalue="value", n_obs="value")
print(result.summary())
```

---
### `sp.DistIVResult()`

**Distributional IV LATE per quantile.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_high` | `string` | ✓ |  | ci_high parameter (np.ndarray). |
| `ci_low` | `string` | ✓ |  | ci_low parameter (np.ndarray). |
| `late_q` | `string` | ✓ |  | late_q parameter (np.ndarray). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `quantiles` | `string` | ✓ |  | quantiles parameter (np.ndarray). |
| `se_q` | `string` | ✓ |  | se_q parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DistIVResult(quantiles="value", late_q="value", se_q="value", ci_low="value", ci_high="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.HDPanelQTEResult()`

**QTE at multiple quantiles with high-dim control selection.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_high` | `string` | ✓ |  | ci_high parameter (np.ndarray). |
| `ci_low` | `string` | ✓ |  | ci_low parameter (np.ndarray). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `qte` | `string` | ✓ |  | qte parameter (np.ndarray). |
| `quantiles` | `string` | ✓ |  | quantiles parameter (np.ndarray). |
| `se` | `string` | ✓ |  | se parameter (np.ndarray). |
| `selected_controls` | `array[string]` | ✓ |  | selected_controls parameter (List[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.HDPanelQTEResult(quantiles="value", qte="value", se="value", ci_low="value", ci_high="value", selected_controls=["a", "b"], n_obs=1.0)
print(result.summary())
```

---
### `sp.QTEResult()`

**Container for quantile treatment effect estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ate` | `number` | ✓ |  | ate parameter (float). |
> 📝 *ate 参数（浮点数）。*
| `ci_lower` | `string` | ✓ |  | ci_lower parameter (np.ndarray). |
> 📝 *ci_lower 参数（np.ndarray）。*
| `ci_upper` | `string` | ✓ |  | ci_upper parameter (np.ndarray). |
> 📝 *ci_upper 参数（np.ndarray）。*
| `effects` | `string` | ✓ |  | effects parameter (np.ndarray). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  |  | model_info parameter (Optional[dict]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `quantiles` | `string` | ✓ |  | quantiles parameter (np.ndarray). |
| `se` | `string` | ✓ |  | se parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.QTEResult(quantiles="value", effects="value", se="value", ci_lower="value", ci_upper="value", ate=1.0, method="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.beyond_average_late()`

**Beyond-average LATE (Xie-Wu 2025). Identifies the entire treatment-effect distribution among compliers under incomplete compliance, not just its mean. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `instrument` | `string` | ✓ |  | instrument parameter (str). |
| `quantiles` | `array[string]` |  |  | Quantiles tau at which to evaluate QTE (default 0.1..0.9 step 0.1) |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.beyond_average_late(y="outcome", data=df, treat="value", instrument="value")
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
### `sp.dist_iv()`

**Distributional IV: LATE at each quantile of Y. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `instrument` | `string` | ✓ |  | instrument parameter (str). |
| `n_boot` | `integer` |  | `200` | Number of bootstrap replications. |
| `quantiles` | `string` |  |  | Defaults to (0.1, 0.25, 0.5, 0.75, 0.9). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dist_iv(y="outcome", data=df, treat="value", instrument="value")
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
### `sp.distributional_te()`

**Estimate distributional treatment effects. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string (enum)` |  | `'ipw'` | Estimator or algorithm variant to use. |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `n_grid` | `integer` |  | `100` | Number of grid. |
| `quantiles` | `array[string]` |  |  | quantiles parameter (Optional[List[float]]). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `treatment` | `string` | ✓ |  | 0-3 group encoding for CiC). |
| `x` | `array[string]` |  |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **method** options: `'ipw'`, `'dr'`, `'cic'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.distributional_te(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, treatment="value")
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
### `sp.kan_dlate()`

**KAN-Powered D-IV-LATE (Shaw 2025, arXiv 2506.12765). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `instrument` | `string` | ✓ |  | instrument parameter (str). |
| `n_boot` | `integer` |  | `200` | Number of bootstrap replications. |
| `quantiles` | `string` |  |  | quantiles parameter (Optional[np.ndarray]). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.kan_dlate(y="outcome", data=df, treat="value", instrument="value")
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
### `sp.qdid()`

**Quantile Difference-in-Differences (Athey & Imbens 2006 CIC). Estimates QTE at multiple quantiles via changes-in-changes on a 2x2 design with bootstrap SE. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Binary treated / control group |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `quantiles` | `array[string]` |  |  | Quantiles to estimate, defaults to [0.1, ..., 0.9] |
| `time` | `string` | ✓ |  | Binary pre / post indicator |
| `y` | `string` | ✓ |  | Outcome |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.qdid(y="outcome", data=df, group="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
### `sp.qte()`

**Quantile Treatment Effect via quantile regression or IPW weighting. Returns QTE at supplied quantiles with bootstrap SE. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `controls` | `array[string]` |  |  | Control-variable column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string (enum)` |  | `'quantile_regression'` | Estimation method |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `quantiles` | `array[string]` |  |  | quantiles parameter (list). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **method** options: `'quantile_regression'`, `'ipw'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.qte(y="outcome", data=df, treatment="value")
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
### `sp.qte_hd_panel()`

**High-dimensional panel QTE via LASSO-selected controls.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | High-dim candidate control set. |
| `data` | `string` | ✓ |  | Long-format panel. |
| `lasso_alpha` | `number` |  | `0.01` | lasso_alpha parameter (float). |
| `quantiles` | `string` |  |  | Defaults to (0.1, 0.25, 0.5, 0.75, 0.9). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.qte_hd_panel(y="outcome", data=df, treat="value", unit="value", time="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/qte_family.md`

---
