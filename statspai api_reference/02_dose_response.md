# dose_response

> 📂 所属分类:02 · 元学习器与机器学习因果推断 (Meta-Learners & ML Causal)

Continuous Treatment Effects: Dose-Response Estimation.

Estimates the dose-response function E[Y(t)] for continuous treatments
using the generalized propensity score (GPS) approach and kernel-based
methods.

References
----------
Hirano, K. & Imbens, G. W. (2004).
The Propensity Score with Continuous Treatments.
Applied Bayesian Modeling and Causal Inference from Incomplete-Data
Perspectives, 226164, 73-84. [@hirano2004propensity]

Kennedy, E. H., Ma, Z., McHugh, M. D., & Small, D. S. (2017).
Non-parametric methods for doubly robust estimation of continuous
treatment effects. JRSS-B, 79(4), 1229-1245. [@kennedy2017parametric]

**5 个公共函数**

### `sp.DoseResponse()`

**Generalized Propensity Score dose-response estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dose_range` | `array[string]` |  |  | dose_range parameter (Optional[Tuple[float, float]]). |
| `n_bootstrap` | `integer` |  | `200` | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `n_dose_points` | `integer` |  | `20` | Number of dose points. |
| `outcome_model` | `string` |  |  | outcome_model parameter (Optional[BaseEstimator]). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `treatment_model` | `string` |  |  | treatment_model parameter (Optional[BaseEstimator]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DoseResponse(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.VCNetResult()`

**Dose-response curve returned by :func:`vcnet` / :func:`scigan`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_hi` | `string` | ✓ |  | ci_hi parameter (np.ndarray). |
| `ci_lo` | `string` | ✓ |  | ci_lo parameter (np.ndarray). |
| `coef_matrix` | `string` | ✓ |  | coef_matrix parameter (np.ndarray). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `mu_hat` | `string` | ✓ |  | mu_hat parameter (np.ndarray). |
| `n_basis` | `integer` | ✓ |  | Number of basis. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `se` | `string` | ✓ |  | se parameter (np.ndarray). |
| `t_grid` | `string` | ✓ |  | Grid of t values to evaluate. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.VCNetResult(t_grid="value", mu_hat="value", se="value", ci_lo="value", ci_hi="value", coef_matrix="value", n_obs=1.0, n_basis=1.0)
print(result.summary())
```

---
### `sp.dose_response()`

**Dose-response function for a continuous treatment under unconfoundedness. Uses generalised propensity-score weighting or double ML for the conditional expectation E[Y(d)]. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dose_range` | `array[string]` |  |  | (lo, hi) over which to evaluate dose-response |
| `n_bootstrap` | `integer` |  | `200` | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `n_dose_points` | `integer` |  | `20` | Number of dose points. |
| `treat` | `string` | ✓ |  | Continuous treatment / dose |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dose_response(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/g_methods_ph.md`

---
### `sp.scigan()`

**Adversarial dose-response estimator (Bica et al. 2020).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `propensity_weights` | `string` |  |  | propensity_weights parameter (Optional[np.ndarray]). |
| `t_grid` | `array[string]` |  |  | Grid of t values to evaluate. |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.scigan(y="outcome", data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.vcnet()`

**Varying-coefficient dose-response estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_basis` | `integer` |  | `6` | Number of B-spline basis functions for the t-axis. |
| `n_bootstrap` | `integer` |  | `200` | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `ridge` | `number` |  | `0.01` | Tikhonov regularisation on the coefficient matrix. |
| `spline_degree` | `integer` |  | `3` | spline_degree parameter (int). |
| `t_grid` | `array[string]` |  |  | Treatment values at which to evaluate the dose-response curve. Defaults to 40 equally-spaced points between the observed min/max. |
| `treatment` | `string` | ✓ |  | Continuous treatment / dose column. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.vcnet(y="outcome", data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
