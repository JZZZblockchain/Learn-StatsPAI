# bcf

> 📂 所属分类:02 · 元学习器与机器学习因果推断 (Meta-Learners & ML Causal)

Bayesian Causal Forest (BCF) for heterogeneous treatment effects.

Decomposes the outcome into a prognostic function mu(X) and a
treatment effect function tau(X), each modeled by BART:

    Y_i = mu(X_i) + tau(X_i) * D_i + epsilon_i

This separation allows regularization-induced confounding (RIC) to be
mitigated, producing better CATE estimates than standard BART.

References
----------
Hahn, P. R., Murray, J. S., & Carvalho, C. M. (2020).
Bayesian Regression Tree Models for Causal Inference: Regularization,
Confounding, and Heterogeneous Effects.
Bayesian Analysis, 15(3), 965-1056. [@hahn2020bayesian]

**8 个公共函数**

### `sp.BCFFactorExposureResult()`

**Output of :func:`bcf_factor_exposure`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `diagnostics` | `object` |  | `None` | diagnostics parameter (Dict[str, Any]). |
| `factor_loadings` | `string` | ✓ |  | factor_loadings parameter (pd.DataFrame). |
| `factor_scores` | `string` | ✓ |  | factor_scores parameter (pd.DataFrame). |
| `method` | `string` |  | `'bcf_factor_exposure'` | Estimator or algorithm variant to use. |
| `per_factor_ate` | `string` | ✓ |  | per_factor_ate parameter (pd.DataFrame). |
| `total_mixture_ate` | `number` | ✓ |  | total_mixture_ate parameter (float). |
| `total_mixture_ci` | `array[string]` | ✓ |  | total_mixture_ci parameter (tuple). |
| `total_mixture_se` | `number` | ✓ |  | total_mixture_se parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BCFFactorExposureResult(factor_loadings="value", factor_scores="value", per_factor_ate="value", total_mixture_ate=1.0, total_mixture_se=1.0, total_mixture_ci=["a", "b"])
print(result.summary())
```

---
### `sp.BCFLongResult()`

**Longitudinal BCF output container.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `average_ate` | `number` | ✓ |  | average_ate parameter (float). |
| `average_ci` | `array[string]` | ✓ |  | average_ci parameter (tuple). |
| `average_se` | `number` | ✓ |  | average_se parameter (float). |
| `individual_cate` | `string` | ✓ |  | individual_cate parameter (pd.DataFrame). |
| `model_info` | `object` |  | `None` | model_info parameter (Dict). |
| `per_time_ate` | `string` | ✓ |  | per_time_ate parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BCFLongResult(per_time_ate="value", average_ate=1.0, average_se=1.0, average_ci=["a", "b"], individual_cate="value")
print(result.summary())
```

---
### `sp.BCFOrdinalResult()`

**Output of :func:`bcf_ordinal`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ate` | `string` | ✓ |  | ate parameter (pd.Series). |
| `ate_ci` | `string` | ✓ |  | ate_ci parameter (pd.DataFrame). |
| `ate_se` | `string` | ✓ |  | ate_se parameter (pd.Series). |
| `cate` | `string` | ✓ |  | cate parameter (pd.DataFrame). |
| `cate_se` | `string` | ✓ |  | cate_se parameter (pd.DataFrame). |
| `diagnostics` | `object` |  | `None` | diagnostics parameter (Dict[str, Any]). |
| `levels` | `array[string]` | ✓ |  | levels parameter (List[Any]). |
| `method` | `string` |  | `'bcf_ordinal'` | Estimator or algorithm variant to use. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BCFOrdinalResult(cate="value", cate_se="value", ate="value", ate_se="value", ate_ci="value", levels=["a", "b"])
print(result.summary())
```

---
### `sp.BayesianCausalForest()`

**Bayesian Causal Forest estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_bootstrap` | `integer` |  | `200` | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_trees_mu` | `integer` |  | `200` | Number of trees mu. |
| `n_trees_tau` | `integer` |  | `50` | Number of trees tau. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BayesianCausalForest(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.bcf()`

**Estimate heterogeneous treatment effects using Bayesian Causal Forest. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `covariates` | `array[string]` | ✓ |  | Covariate names. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `n_bootstrap` | `integer` |  | `200` | Bootstrap iterations for uncertainty quantification. |
| `n_folds` | `integer` |  | `5` | Cross-fitting folds for propensity estimation. |
| `n_trees_mu` | `integer` |  | `200` | Number of trees for the prognostic function mu(X). |
| `n_trees_tau` | `integer` |  | `50` | Number of trees for the treatment effect function tau(X). Fewer trees = stronger shrinkage toward homogeneous effects. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Binary treatment variable (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bcf(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.bcf_factor_exposure()`

**BCF on PCA-factor scores of a high-dimensional exposure vector (arXiv:2601.16595, 2026). Compresses exposures via SVD or user-supplied loadings, then fits one BCF per factor.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `binarize` | `string (enum)` |  | `'median'` | binarize parameter (str). |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `exposures` | `array[string]` | ✓ |  | exposures parameter (list). |
| `loadings` | `string` |  |  | loadings parameter (DataFrame). |
| `n_bootstrap` | `integer` |  | `100` | Number of bootstrap replications. |
| `n_factors` | `integer` |  | `3` | Number of factors. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **binarize** options: `'median'`, `'zero'`, `'none'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bcf_factor_exposure(y="outcome", data=df, exposures=["a", "b"], covariates=["a", "b"])
print(result.summary())
```

---
### `sp.bcf_longitudinal()`

**Hierarchical Bayesian Causal Forest for longitudinal data (BCFLong) -- allows mu_t(X), tau_t(X) to evolve across time with unit-level random intercepts.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_bootstrap` | `integer` |  | `100` | Number of bootstrap replications. |
| `n_trees_mu` | `integer` |  | `200` | Number of trees mu. |
| `n_trees_tau` | `integer` |  | `50` | Number of trees tau. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `unit` | `string` | ✓ |  | Unit identifier column. |
> 📝 *单元标识符列。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bcf_longitudinal(data=df, outcome="value", treatment="value", unit="value", time="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.bcf_ordinal()`

**Bayesian Causal Forest for ordered / dose-level treatment (Zorzetto et al. 2026). Estimates cumulative dose-response curves via chained BCF between consecutive levels.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `baseline` | `string` |  |  | baseline parameter (str). |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_bootstrap` | `integer` |  | `100` | Number of bootstrap replications. |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_trees_mu` | `integer` |  | `200` | Number of trees mu. |
| `n_trees_tau` | `integer` |  | `50` | Number of trees tau. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bcf_ordinal(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
