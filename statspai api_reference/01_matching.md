# matching

> 📂 所属分类:01 · 核心因果推断方法 (Core Causal Methods)

Matching module for StatsPAI.
> 📝 *StatsPAI 匹配（Matching）模块。*

Unified interface for matching estimators:
> 📝 *匹配估计器的统一接口：*

- Nearest-neighbor matching (propensity score, Mahalanobis, Euclidean)
> 📝 *最近邻匹配（倾向得分 Propensity Score, PS、马氏距离 Mahalanobis、欧氏距离 Euclidean）*
- Exact matching
> 📝 *精确匹配*
- Coarsened Exact Matching (CEM, 粗化精确匹配)
- Propensity score stratification / subclassification
> 📝 *倾向得分分层 / 子分类*
- Abadie-Imbens (2011) bias correction
> 📝 *Abadie-Imbens（2011）偏差校正*
- Entropy balancing (Hainmueller 2012)
> 📝 *熵平衡（Hainmueller 2012）*
- Covariate Balancing Propensity Score (CBPS, 协变量平衡倾向得分) (Imai-Ratkovic 2014)
- Genetic Matching (Diamond-Sekhon 2013)
> 📝 *遗传匹配（Diamond-Sekhon 2013）*
- Stable Balancing Weights (SBW, 稳定平衡权重) (Zubizarreta 2015)
- Optimal pair / full / cardinality matching (Rosenbaum 1989, 2012)
> 📝 *最优配对 / 全匹配 / 基数匹配（Rosenbaum 1989, 2012）*
- Overlap weights (Li-Morgan-Zaslavsky 2018)
> 📝 *重叠权重（Li-Morgan-Zaslavsky 2018）*

The single entry point is :func:`match` — a method-aware dispatcher
that routes ``method=`` to the correct estimator.  Standalone
functions (``ebalance``, ``cbps``, ``genmatch``, ``sbw``,
``optimal_match``, ``cardinality_match``, ``overlap_weights``) remain
fully accessible for power users who need their estimator-specific
parameters.
> 📝 *单一入口点是 :func:`match`——一个方法感知的分发器，将 ``method=`` 路由到正确的估计器。独立函数（``ebalance``、``cbps``、``genmatch``、``sbw``、``optimal_match``、``cardinality_match``、``overlap_weights``）对于需要特定估计器参数的高级用户仍然完全可用。*

References
----------
> 📝 *参考文献*
Rosenbaum, P.R. and Rubin, D.B. (1983). Biometrika, 70(1), 41-55.
Abadie, A. and Imbens, G.W. (2006). Econometrica, 74(1), 235-267.
Abadie, A. and Imbens, G.W. (2011). JBES, 29(1), 1-11.
Iacus, S.M., King, G., and Porro, G. (2012). Political Analysis, 20(1), 1-24.
Hainmueller, J. (2012). Political Analysis, 20(1), 25-46.
Imai, K. and Ratkovic, M. (2014). JRSS-B, 76(1), 243-263.
Diamond, A. and Sekhon, J.S. (2013). REStat, 95(3), 932-945.
Zubizarreta, J.R. (2015). JASA, 110(511), 910-922.
Li, F., Morgan, K.L., and Zaslavsky, A.M. (2018). JASA, 113(521), 390-400.
Rosenbaum, P.R. (2012). JASA, 107(498), 691-700.
Cunningham, S. (2021). *Causal Inference: The Mixtape*. Yale University
Press. [@rosenbaum1983central]

**25 个公共函数**

### `sp.BalanceDiagnosticsResult()`

**Container for raw/weighted matching balance diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ps` | `string` |  |  | ps parameter (Optional[pandas.Series]). |
| `summary` | `object` | ✓ |  | summary parameter (Dict[str, Any]). |
| `table` | `string` | ✓ |  | table parameter (DataFrame). |
| `weights` | `string` |  |  | Observation weights. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BalanceDiagnosticsResult(table="value")
print(result.summary())
```

---
### `sp.CardinalityMatchResult()`

**Result of :func:`cardinality_match` (Zubizarreta cardinality matching).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ate` | `number` | ✓ |  | ate parameter (float). |
> 📝 *ate 参数（浮点数）。*
| `balance` | `string` | ✓ |  | balance parameter (pd.DataFrame). |
| `control_matched` | `string` | ✓ |  | control_matched parameter (np.ndarray). |
| `n_matched_pairs` | `integer` | ✓ |  | Number of matched pairs. |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `treated_matched` | `string` | ✓ |  | treated_matched parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CardinalityMatchResult(treated_matched="value", control_matched="value", ate=1.0, se=1.0, n_matched_pairs=1.0, balance="value")
print(result.summary())
```

---
### `sp.GenMatchResult()`

**Output of :func:`sp.genmatch` (Diamond-Sekhon genetic matching).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `att` | `number` | ✓ |  | att parameter (float). |
| `att_se` | `number` | ✓ |  | att_se parameter (float). |
| `balance` | `string` | ✓ |  | balance parameter (pd.DataFrame). |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `matches` | `string` | ✓ |  | matches parameter (np.ndarray). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `n_treated` | `integer` | ✓ |  | Number of treated. |
| `pvalue` | `number` | ✓ |  | pvalue parameter (float). |
> 📝 *pvalue 参数（浮点数）。*
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GenMatchResult(att=1.0, att_se=1.0, ci=["a", "b"], pvalue=1.0, weights="value", balance="value", matches="value", n_treated=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.MatchEstimator()`

**Unified matching estimator supporting multiple distance x method combinations.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ai_matches` | `integer` |  | `1` | ai_matches parameter (int). |
> 📝 *ai_matches 参数（整数）。*
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bias_correction` | `boolean` |  | `False` | bias_correction parameter (bool). |
> 📝 *bias_correction 参数（布尔值）。*
| `bwidth` | `number` |  | `0.06` | bwidth parameter (float). |
> 📝 *bwidth 参数（浮点数）。*
| `caliper` | `number` |  |  | caliper parameter (Optional[float]). |
> 📝 *caliper 参数（可选浮点数）。*
| `common_support` | `string` |  | `'none'` | common_support parameter (str). |
> 📝 *common_support 参数（字符串）。*
| `covariates` | `array[string]` | ✓ |  | Variables to match on. |
> 📝 *用于匹配的变量。*
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `distance` | `string` |  |  | ``'propensity'``, ``'mahalanobis'``, ``'euclidean'`` or ``'exact'``. |
| `estimand` | `string` |  | `'ATT'` | ``'ATT'`` or ``'ATE'``. |
| `kernel` | `string` |  | `'epan'` | Kernel function used for weighting or smoothing. |
| `method` | `string` |  | `'nearest'` | ``'nearest'``, ``'stratify'`` or ``'cem'`` (legacy ``'psm'`` / ``'mahalanobis'`` are also accepted). |
| `n_bins` | `integer` |  |  | Number of bins. |
| `n_matches` | `integer` |  | `1` | Number of matches. |
| `n_strata` | `integer` |  | `5` | Number of strata. |
| `ps_poly` | `integer` |  | `1` | ps_poly parameter (int). |
| `replace` | `boolean` |  | `True` | replace parameter (bool). |
| `se_method` | `string` |  | `'auto'` | se_method parameter (str). |
| `treat` | `string` | ✓ |  | Binary (0/1) treatment column. |
| `y` | `string` | ✓ |  | Outcome column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MatchEstimator(y="outcome", data=df, treat="value", covariates=["a", "b"])
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
### `sp.OptimalMatchResult()`

**Result of :func:`optimal_match` (optimal 1:1 Hungarian matching).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ate` | `number` | ✓ |  | ate parameter (float). |
> 📝 *ate 参数（浮点数）。*
| `distances` | `string` | ✓ |  | distances parameter (np.ndarray). |
| `n_matched` | `integer` | ✓ |  | Number of matched. |
| `n_treated` | `integer` | ✓ |  | Number of treated. |
| `pairs` | `string` | ✓ |  | pairs parameter (pd.DataFrame). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.OptimalMatchResult(pairs="value", distances="value", ate=1.0, se=1.0, n_treated=1.0, n_matched=1.0)
print(result.summary())
```

---
### `sp.PSBalanceResult()`

**Container for propensity score balance diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ps` | `string` | ✓ |  | ps parameter (Series). |
| `table` | `string` | ✓ |  | table parameter (DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PSBalanceResult(table="value", ps="value")
print(result.summary())
```

---
### `sp.PSMatch2Result()`

**Container for a ``sp.psmatch2`` run.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `common_support` | `string` | ✓ |  | common_support parameter (str). |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `matched_data` | `string` | ✓ |  | matched_data parameter (pd.DataFrame). |
| `method` | `string` |  | `'neighbor'` | Estimator or algorithm variant to use. |
| `n_matches` | `integer` | ✓ |  | Number of matches. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `result` | `string` | ✓ |  | result parameter (CausalResult). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PSMatch2Result(result="value", matched_data="value", treat="value", covariates=["a", "b"], outcome="value", n_matches=1.0, common_support="value")
print(result.summary())
```

---
### `sp.SBWResult()`

**Stable balancing weights with a diagnostic panel.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `balance` | `string` | ✓ |  | balance parameter (pd.DataFrame). |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `effective_sample_size` | `number` | ✓ |  | effective_sample_size parameter (float). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `pvalue` | `number` | ✓ |  | pvalue parameter (float). |
> 📝 *pvalue 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `solver_status` | `string` | ✓ |  | solver_status parameter (str). |
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SBWResult(method="value", estimand="value", estimate=1.0, se=1.0, pvalue=1.0, ci=["a", "b"], alpha=1.0, n_obs=1.0, weights="value", effective_sample_size=1.0, balance="value", solver_status="value")
print(result.summary())
```

---
### `sp.balance_diagnostics()`

**Unified balance diagnostics for matching and weighting estimators.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariates to audit. |
| `data` | `string` | ✓ |  | Analysis frame. |
| `method` | `string (enum)` |  | `'logit'` | Propensity-score model when ``ps`` is not supplied. |
| `ps` | `string` |  |  | Propensity scores. If omitted, estimated with ``method``. |
| `threshold` | `number` |  | `0.1` | Balance threshold for absolute standardized mean differences. |
| `treatment` | `string` | ✓ |  | Binary treatment indicator. |
| `weights` | `string` |  |  | Observation weights after matching/weighting. If omitted, ATE inverse-propensity weights are computed from ``ps``. |

> **method** options: `'logit'`, `'probit'`, `'gbm'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.balance_diagnostics(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.balanceplot()`

**Love plot: covariate balance visualization (SMD dot plot).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `figsize` | `array[string]` |  | `[8, None]` | Height auto-scales with number of covariates if None. |
| `result` | `string` | ✓ |  | Result from ``match()`` or ``ebalance()``. |
| `threshold` | `number` |  | `0.1` | SMD threshold lines. |
| `title` | `string` |  |  | title parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.balanceplot(result="value")
print(result.summary())
```

---
### `sp.cardinality_match()`

**Cardinality matching -- maximise the number of matched pairs subject**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `smd_tolerance` | `number` |  | `0.1` | smd_tolerance parameter (float). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cardinality_match(data=df, treatment="value", outcome="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.cbps()`

**Covariate-Balancing Propensity Score estimator (Imai-Ratkovic 2014). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `add_intercept` | `boolean` |  | `True` | Prepend a constant to the covariate matrix. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariates entering the logit score. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string (enum)` |  | `'ATE'` | estimand parameter (Literal['ATE', 'ATT']). |
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Binary 0/1 treatment column. |
| `trim` | `number` |  | `0.0` | Optional pscore clip for stability. |
| `variant` | `string (enum)` |  | `'over'` | 'exact': just-identified CBPS (only balance moments). 'over': over-identified CBPS (MLE + balance, solved via two-step GMM). |
| `y` | `string` | ✓ |  | Outcome column. |

> **estimand** options: `'ATE'`, `'ATT'`

> **variant** options: `'exact'`, `'over'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cbps(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`

---
### `sp.ebalance()`

**Entropy Balancing treatment effect estimator. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariates to balance on. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `moments` | `integer` |  | `1` | Number of moments to balance: - 1: means only - 2: means and variances - 3: means, variances, and skewness |
| `treat` | `string` | ✓ |  | Binary treatment indicator (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ebalance(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/migration-from-r.md`

---
### `sp.genmatch()`

**Genetic Matching for ATT estimation. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `generations` | `integer` |  | `20` | generations parameter (int). |
| `k` | `integer` |  | `1` | Number of matches per treated unit. |
| `mutation_rate` | `number` |  | `0.2` | mutation_rate parameter (float). |
| `population_size` | `integer` |  | `40` | population_size parameter (int). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Binary treatment indicator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.genmatch(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.love_plot()`

**Love plot: dot plot of standardized mean differences before/after.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `covariates` | `array[string]` | ✓ |  | Covariate columns. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `figsize` | `array[string]` |  | `[7, None]` | (width, height). Height defaults to 0.4 * n_covariates + 1. |
| `ps_method` | `string` |  | `'logit'` | PS estimation method for balance computation. |
| `threshold` | `number` |  | `0.1` | SMD threshold for the vertical dashed line (default 0.1). |
| `title` | `string` |  | `'Covariate Balance (Love Plot)'` | Plot title. |
| `treatment` | `string` | ✓ |  | Binary treatment column. |
| `weights` | `string` |  |  | IPW or matching weights. If None, inverse-PS weights are computed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.love_plot(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/robustness_workflow.md`

---
### `sp.optimal_match()`

**Optimal 1:1 matching via the Hungarian algorithm.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `caliper` | `number` |  |  | Drop any pair with distance greater than ``caliper``. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `metric` | `string` |  | `'mahalanobis'` | metric parameter (str). |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.optimal_match(data=df, treatment="value", outcome="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.overlap_plot()`

**Mirrored density plot of propensity scores by treatment group.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | Axes to plot on. If None, a new figure is created. |
| `covariates` | `array[string]` | ✓ |  | Covariates for PS estimation (ignored if *ps* supplied). |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `figsize` | `array[string]` |  | `[8, 4]` | Figure size (width, height). |
| `method` | `string` |  | `'logit'` | PS estimation method if *ps* is None. |
| `ps` | `string` |  |  | Pre-estimated propensity scores. |
| `title` | `string` |  | `'Propensity Score Overlap'` | Plot title. |
| `treatment` | `string` | ✓ |  | Binary treatment column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.overlap_plot(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/robustness_workflow.md`

---
### `sp.overlap_weights()`

**Overlap-weight (ATO) treatment effect estimator. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariates for the logistic propensity-score model. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string (enum)` |  | `'ATO'` | Which generalized-weight scheme to use. All follow Li-Li-Li (2019) Table 1; 'ATO' uses the overlap weights; 'matching' uses the ``min(e, 1-e)`` weight; 'entropy' uses ``-e*log(e) - (1-e)*log(1-e)``; 'ATE/ATT/ATC' reduce to standard IPW for comparison. |
| `n_bootstrap` | `integer` |  | `500` | Paired-sample bootstrap replications for SE. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Binary 0/1 treatment column. |
| `trim` | `number` |  | `0.0` | Optional clip of pscore to ``[trim, 1-trim]``. For overlap weights this is rarely needed -- set to 0 by default. |
| `y` | `string` | ✓ |  | Outcome column. |

> **estimand** options: `'ATO'`, `'ATE'`, `'ATT'`, `'ATC'`, `'matching'`, `'entropy'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.overlap_weights(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`

---
### `sp.propensity_score()`

**Estimate propensity scores P(D=1|X).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate column names. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `method` | `string (enum)` |  | `'logit'` | Estimation method. ``'logit'`` uses IRLS (no sklearn needed). ``'probit'`` uses scipy.optimize. ``'gbm'`` tries sklearn GradientBoostingClassifier, falling back to logit with interactions. |
| `treatment` | `string` | ✓ |  | Name of binary treatment column (0/1). |
| `trimming` | `string` |  |  | If ``'crump'``, apply Crump et al. (2009) trimming after estimation. Trimmed observations receive ``NaN`` scores. |

> **method** options: `'logit'`, `'probit'`, `'gbm'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.propensity_score(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.ps_balance()`

**Compute comprehensive propensity score balance table.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate columns to assess balance for. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `method` | `string` |  | `'logit'` | PS estimation method ('logit', 'probit', 'gbm'). |
| `treatment` | `string` | ✓ |  | Binary treatment column. |
| `weights` | `string` |  |  | IPW or matching weights. If None, inverse-PS weights are computed automatically from estimated propensity scores. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ps_balance(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/robustness_workflow.md`

---
### `sp.psmatch2()`

**Stata psmatch2-faithful supported propensity-score matching paths (nearest-neighbour, kernel, radius): returns matched-sample variables (_pscore _treated _support _weight _y; plus _n1 through _nn _pdif for nearest-neighbour), the psmatch2 analytic ATT standard error, plus post-matching balance, common-support plotting, and frequency-weighted PSM-DID. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ai` | `integer` |  | `0` | Abadie-Imbens (2006) robust SE with J within-arm matches (Stata ai(J)) |
| `bwidth` | `number` |  | `0.06` | Kernel bandwidth (method='kernel') |
| `caliper` | `number` |  |  | Max PS distance / radius bandwidth |
| `common_support` | `string (enum)` |  | `'none'` | Common-support trimming |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `kernel` | `string (enum)` |  | `'epan'` | Kernel type (method='kernel') |
| `method` | `string (enum)` |  | `'neighbor'` | Matching algorithm |
| `neighbor` | `integer` |  | `1` | Number of nearest neighbours k |
| `outcome` | `string` |  |  | Outcome variable (Stata outcome(); optional) |
| `se` | `string (enum)` |  | `'psmatch2'` | Standard-error estimator |
| `treat` | `string` | ✓ |  | Binary treatment column (0/1) |

> **common_support** options: `'none'`, `'minmax'`

> **kernel** options: `'epan'`, `'normal'`, `'biweight'`, `'uniform'`, `'tricube'`

> **method** options: `'neighbor'`, `'kernel'`, `'radius'`

> **se** options: `'psmatch2'`, `'ai'`, `'abadie_imbens'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.psmatch2(data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/psm_did.md`

---
### `sp.psplot()`

**Propensity score distribution plot (common support diagnostic).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `colors` | `array[string]` |  | `['#3498DB', '#E74C3C']` | Colors for (control, treated). |
| `covariates` | `array[string]` | ✓ |  | Covariates used to estimate the propensity score. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `figsize` | `array[string]` |  | `[8, 5]` | figsize parameter (tuple). |
| `labels` | `array[string]` |  | `['Control', 'Treated']` | Labels for (control, treated). |
| `n_bins` | `integer` |  | `40` | Number of histogram bins. |
| `title` | `string` |  |  | title parameter (Optional[str]). |
| `treat` | `string` | ✓ |  | Binary treatment column. |
| `trim` | `number` |  |  | If set, draw vertical lines at (trim, 1-trim) to show the recommended trimming region. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.psplot(data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/psm_did.md`

---
### `sp.sbw()`

**Stable Balancing Weights (Zubizarreta 2015) with optional ATT/ATE Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for inference on the outcome. |
| `covariates` | `array[string]` | ✓ |  | Columns whose means must be balanced. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `delta` | `array[string]` |  | `0.02` | Balance tolerance. With ``tolerance_scale='sd'`` the constraint is ``\|mean_T(X_j) - weighted mean_C(X_j)\| <= delta_j * sd(X_j)``. |
| `estimand` | `string (enum)` |  | `'att'` | ``'att'`` reweights controls to match treated means (standard); ``'atc'`` reweights treated to match control means; ``'ate'`` reweights each group to match the pooled means. |
| `include_squares` | `boolean` |  | `False` | Also balance second-moments (w_j2 columns). |
| `objective` | `string (enum)` |  | `'variance'` | Dispersion objective. ``'variance'`` minimises Sigma w_i2; ``'entropy'`` minimises Sigma w_i log(n * w_i) (KL from uniform). |
| `solver_options` | `object` |  |  | Passed to ``scipy.optimize.minimize``. |
| `tolerance_scale` | `string (enum)` |  | `'sd'` | Whether ``delta`` is in SD units (standard) or raw units. |
| `treat` | `string` | ✓ |  | Binary 0/1 treatment indicator column. |
| `y` | `string` |  |  | Outcome column. If provided, a weighted ATT/ATE estimate with HC-robust SE is attached to the returned :class:`SBWResult`. |

> **estimand** options: `'att'`, `'ate'`, `'atc'`

> **objective** options: `'variance'`, `'entropy'`

> **tolerance_scale** options: `'sd'`, `'raw'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sbw(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.trimming()`

**Trim sample to optimal overlap region.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariates for PS estimation (if *ps* not supplied). |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `method` | `string (enum)` |  | `'crump'` | ``'crump'`` uses Crump et al. (2009) optimal rule. ``'sturmer'`` trims at the fixed [0.1, 0.9] interval. |
| `ps` | `string` |  |  | Pre-estimated propensity scores. If None, estimated via *ps_method*. |
| `ps_method` | `string` |  | `'logit'` | Method for PS estimation if *ps* is None. |
| `treatment` | `string` | ✓ |  | Binary treatment column. |

> **method** options: `'crump'`, `'sturmer'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.trimming(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/sp_dml_vs_doubleml.md`

---
