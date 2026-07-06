# experimental

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Experimental design and analysis tools.

Provides randomization, balance checking, attrition analysis,
and pre-analysis plan generation for RCTs.

**9 个公共函数**

### `sp.AttritionResult()`

**Results from attrition analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `control_rate` | `string` | ✓ |  | control_rate parameter. |
| `covariate_tests` | `string` | ✓ |  | covariate_tests parameter. |
| `diff_p_value` | `string` | ✓ |  | diff_p_value parameter. |
| `diff_test_stat` | `string` | ✓ |  | diff_test_stat parameter. |
| `n_attrit` | `string` | ✓ |  | Number of attrit. |
| `n_total` | `string` | ✓ |  | Number of total. |
| `overall_rate` | `string` | ✓ |  | overall_rate parameter. |
| `treat_rate` | `string` | ✓ |  | treat_rate parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.AttritionResult(overall_rate="value", treat_rate="value", control_rate="value", diff_test_stat="value", diff_p_value="value", covariate_tests="value", n_total="value", n_attrit="value")
print(result.summary())
```

---
### `sp.BalanceResult()`

**Results from balance check.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n_control` | `integer` | ✓ |  | Number of control. |
| `n_treat` | `integer` | ✓ |  | Number of treat. |
| `normalized_diffs` | `object` | ✓ |  | normalized_diffs parameter (Dict[str, float]). |
| `omnibus_f` | `number` | ✓ |  | omnibus_f parameter (float). |
| `omnibus_p` | `number` | ✓ |  | omnibus_p parameter (float). |
| `table` | `string` | ✓ |  | table parameter (DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BalanceResult(table="value", omnibus_f=1.0, omnibus_p=1.0, n_treat=1.0, n_control=1.0)
print(result.summary())
```

---
### `sp.OptimalDesignResult()`

**Results from optimal design calculation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `cluster_size` | `integer` | ✓ |  | cluster_size parameter (Optional[int]). |
| `design_type` | `string` | ✓ |  | design_type parameter (str). |
| `icc` | `number` | ✓ |  | icc parameter (float). |
| `mde` | `number` | ✓ |  | mde parameter (Optional[float]). |
| `n_clusters` | `integer` | ✓ |  | Number of clusters. |
> 📝 *聚类数量。*
| `n_per_arm` | `integer` | ✓ |  | Number of per arm. |
| `n_total` | `integer` | ✓ |  | Number of total. |
| `power` | `number` | ✓ |  | power parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.OptimalDesignResult(n_total=1.0, n_per_arm=1.0, n_clusters=1.0, cluster_size=1.0, icc=1.0, mde=1.0, power=1.0, alpha=1.0, design_type="value")
print(result.summary())
```

---
### `sp.RandomizationResult()`

**Results from randomization.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `balance` | `object` | ✓ |  | balance parameter (Optional[Dict[str, Any]]). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_control` | `integer` | ✓ |  | Number of control. |
| `n_treated` | `integer` | ✓ |  | Number of treated. |
| `seed` | `integer` | ✓ |  | Random seed for reproducible stochastic steps. |
| `strata_col` | `string` | ✓ |  | Column name for strata. |
| `treatment_col` | `string` | ✓ |  | Treatment variable column name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RandomizationResult(data=df, treatment_col="value", n_treated=1.0, n_control=1.0, strata_col="value", method="value", seed=1.0)
print(result.summary())
```

---
### `sp.attrition_bounds()`

**Compute bounds on treatment effects under attrition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string` |  | `'lee'` | Bounding method: 'lee' (Lee 2009), 'manski' (worst-case). |
| `observed` | `string` |  |  | Indicator for observed outcome. If None, uses non-missing y. |
| `treatment` | `string` | ✓ |  | Treatment indicator (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.attrition_bounds(y="outcome", data=df, treatment="value")
print(result.summary())
```

---
### `sp.attrition_test()`

**Test for differential attrition in an RCT.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Baseline covariates to test as predictors of attrition. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `observed` | `string` | ✓ |  | Indicator for whether outcome is observed (1) or missing (0). |
| `treatment` | `string` | ✓ |  | Treatment indicator (0/1). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.attrition_test(data=df, treatment="value", observed="value")
print(result.summary())
```

---
### `sp.balance_check()`

**Check covariate balance between treatment and control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariates to check balance on. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `treatment` | `string` | ✓ |  | Binary treatment variable (0/1). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.balance_check(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.optimal_design()`

**Compute optimal sample size and design parameters.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `baseline_mean` | `number` |  | `0.0` | baseline_mean parameter (float). |
| `cluster_size` | `integer` |  |  | Average cluster size. |
| `cost_per_cluster` | `number` |  |  | Cost of adding a cluster (for optimal allocation). |
| `cost_per_unit` | `number` |  |  | Cost per individual unit. |
| `design` | `string` |  | `'individual'` | 'individual', 'cluster', 'stratified'. |
| `icc` | `number` |  | `0.0` | Intra-cluster correlation (for cluster designs). |
| `mde` | `number` |  |  | Minimum detectable effect. If None, compute MDE given n. |
| `n_arms` | `integer` |  | `2` | Number of treatment arms. |
| `n_clusters` | `integer` |  |  | Number of clusters (if fixed). |
| `power` | `number` |  | `0.8` | Statistical power (1 - Type II error). |
| `prop_treat` | `number` |  | `0.5` | Proportion assigned to treatment. |
| `r2` | `number` |  | `0.0` | R-squared from baseline covariates (variance reduction). |
| `sigma` | `number` |  | `1.0` | Standard deviation of the outcome. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.optimal_design()
print(result.summary())
```

---
### `sp.randomize()`

**Randomize units to treatment and control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `balance_vars` | `array[string]` |  |  | Variables to check balance on (for re-randomization). |
| `cluster` | `string` |  |  | Cluster variable for cluster randomization. |
| `data` | `string` | ✓ |  | Data with units to randomize. |
| `method` | `string` |  | `'simple'` | 'simple', 'complete', 'stratified', 'cluster'. |
| `n_arms` | `integer` |  | `2` | Number of treatment arms. |
| `n_rerand` | `integer` |  | `0` | Number of re-randomization iterations (0 = no re-randomization). |
| `prob` | `array[string]` |  |  | Probability of each arm. Default: equal. |
| `rerand_threshold` | `number` |  | `0.001` | Mahalanobis distance threshold for re-randomization. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `strata` | `string` |  |  | Stratification variable for block randomization. |
| `treatment_col` | `string` |  | `'treatment'` | Name of treatment column to create. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.randomize(data=df)
print(result.summary())
```

---
