# bounds

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Bounds and Partial Identification for causal effects.

When point identification is not possible (e.g., due to sample selection,
non-compliance, or missing data), bounds provide informative intervals
for the treatment effect.

Methods
-------
- **Lee Bounds** : Bounds on ATE under sample selection (Lee 2009)
- **Manski Bounds** : Worst-case bounds with minimal assumptions (Manski 1990)
- **Horowitz-Manski Bounds** : Tighter bounds conditioning on covariates (2000)
- **IV Bounds** : Bounds under imperfect instruments (Nevo & Rosen 2012)
- **Oster Delta** : Coefficient stability / identified set (Oster 2019)
- **Selection Bounds** : Lee bounds with covariates (Lee 2009, conditional)
- **Breakdown Frontier** : Assumption robustness frontier (Masten & Poirier 2021)

References
----------
Lee, D. S. (2009).
Training, Wages, and Sample Selection: Estimating Sharp Bounds on
Treatment Effects. RES, 76(3), 1071-1102. [@lee2009training]

Manski, C. F. (1990).
Nonparametric Bounds on Treatment Effects.
AER P&P, 80(2), 319-323. [@manski1990nonparametric]

Horowitz, J. L. & Manski, C. F. (2000).
Nonparametric Analysis of Randomized Experiments with Missing
Covariate and Outcome Data. JASA, 95(449), 77-84. [@horowitz2000nonparametric]

Nevo, A. & Rosen, A. M. (2012).
Identification with Imperfect Instruments. RES, 79(3), 1104-1127. [@nevo2012identification]

Oster, E. (2019).
Unobservable Selection and Coefficient Stability.
JBES, 37(2), 187-204. [@oster2019unobservable]

Masten, M. A. & Poirier, A. (2021).
Salvaging Falsified Instrumental Variable Models.
Econometrica, 89(3), 1449-1469. [@masten2021salvaging]

**9 个公共函数**

### `sp.BoundsResult()`

**Result container for partial identification / bounds estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci_lower` | `array[string]` | ✓ |  | ci_lower parameter (Tuple[float, float]). |
| `ci_upper` | `array[string]` | ✓ |  | ci_upper parameter (Tuple[float, float]). |
| `lower` | `number` | ✓ |  | lower parameter (float). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `n_obs` | `integer` |  | `0` | Number of obs. |
| `se_lower` | `number` | ✓ |  | se_lower parameter (float). |
| `se_upper` | `number` | ✓ |  | se_upper parameter (float). |
| `upper` | `number` | ✓ |  | upper parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BoundsResult(lower=1.0, upper=1.0, se_lower=1.0, se_upper=1.0, ci_lower=["a", "b"], ci_upper=["a", "b"], method="value")
print(result.summary())
```

---
### `sp.breakdown_frontier()`

**Masten-Poirier (2021) breakdown frontier for qualitative conclusions. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `assumption` | `string` |  | `'parallel_trends'` | Label for the identifying assumption being relaxed. Currently supports a generic linear violation model applicable to ``'parallel_trends'``, ``'exclusion_restriction'``, or ``'selection_on_observables'``. |
| `estimate` | `number` | ✓ |  | Point estimate of the treatment effect. |
| `max_violation` | `number` |  | `0.1` | Maximum magnitude of the assumption violation to explore. |
| `n_grid` | `integer` |  | `100` | Grid resolution for the frontier. |
| `se` | `number` | ✓ |  | Standard error of the estimate. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.breakdown_frontier(estimate=1.0, se=1.0)
print(result.summary())
```

---
### `sp.horowitz_manski()`

**Horowitz-Manski (2000) bounds conditioning on covariates. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariates to condition on (discretised via quartiles for continuous variables). |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `n_boot` | `integer` |  | `500` | Bootstrap replications. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treatment` | `string` | ✓ |  | Binary treatment variable (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |
| `y_lower` | `number` |  |  | Known lower bound of Y. Defaults to observed min. |
| `y_upper` | `number` |  |  | Known upper bound of Y. Defaults to observed max. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.horowitz_manski(y="outcome", data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/sensitivity_analysis.md`

---
### `sp.iv_bounds()`

**Nevo-Rosen (2012) bounds for LATE under imperfect instruments.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `assumption` | `string` |  | `'monotone_iv'` | - ``'monotone_iv'``: instrument has same-sign direct effect as through the treatment (Nevo-Rosen Proposition 2). - ``'less_than_late'``: direct effect of Z on Y is weakly less than the indirect effect (tighter). |
| `controls` | `array[string]` |  |  | Control variables (residualized out via OLS). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `instrument` | `string` | ✓ |  | Instrument variable (binary). |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treatment` | `string` | ✓ |  | Endogenous treatment (binary). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.iv_bounds(y="outcome", data=df, treatment="value", instrument="value")
print(result.summary())
```

---
### `sp.lee_bounds()`

**Compute Lee (2009) bounds for ATE under sample selection. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `covariates` | `array[string]` |  |  | Not used in basic Lee bounds, reserved for conditional bounds. |
| `data` | `string` | ✓ |  | Input data (including units with missing outcomes). |
| `n_bootstrap` | `integer` |  | `500` | Bootstrap iterations for inference. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `selection` | `string` | ✓ |  | Binary selection/retention indicator (1 = observed, 0 = missing). |
| `treat` | `string` | ✓ |  | Binary treatment variable (0/1). |
| `y` | `string` | ✓ |  | Outcome variable (may have NaN for selected-out units). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lee_bounds(y="outcome", data=df, treat="value", selection="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`, `docs/guides/sensitivity_analysis.md`

---
### `sp.manski_bounds()`

**Compute Manski (1990) worst-case bounds on ATE. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `assumption` | `string` |  | `'none'` | Additional assumption: - 'none': no assumptions (widest bounds) - 'mtr': Monotone Treatment Response (Y(1) >= Y(0) for all) - 'mts': Monotone Treatment Selection (selection on levels) |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Binary treatment variable (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |
| `y_lower` | `number` |  |  | Known lower bound of the outcome. If None, uses observed min. |
| `y_upper` | `number` |  |  | Known upper bound of the outcome. If None, uses observed max. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.manski_bounds(y="outcome", data=df, treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`, `docs/guides/sensitivity_analysis.md`

---
### `sp.ml_bounds()`

**ML-enhanced partial-identification bounds on the ATE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level of the band. |
| `covariates` | `array[string]` | ✓ |  | Covariates X used for the outcome / propensity regressions. |
| `custom_learner` | `string` |  |  | Any ``.fit()`` / ``.predict()``-compatible regressor. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `learner` | `string (enum)` |  | `'random_forest'` | "random_forest" Outcome-regression learner. Ignored if ``custom_learner`` is set. |
| `n_bootstrap` | `integer` |  | `200` | Non-parametric bootstrap replicates for the 2-sided frequentist band. Set to 0 to return the raw plug-in bounds only. |
| `n_splits` | `integer` |  | `5` | Number of cross-fitting folds. |
| `random_state` | `integer` |  |  | Random seed or RandomState for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Outcome and 0/1 treatment column names. |
| `y` | `string` | ✓ |  | Outcome and 0/1 treatment column names. |
| `y_max` | `number` |  |  | A priori bounds on Y. Defaults to the empirical min/max. **Tighter** external bounds (e.g. if Y is a probability, use ``[0, 1]``) give tighter ML bounds. |
| `y_min` | `number` |  |  | A priori bounds on Y. Defaults to the empirical min/max. **Tighter** external bounds (e.g. if Y is a probability, use ``[0, 1]``) give tighter ML bounds. |

> **learner** options: `'random_forest'`, `'gradient_boosting'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ml_bounds(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.oster_delta()`

**Oster (2019) coefficient stability bounds and delta* computation. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `delta_range` | `array[string]` |  | `[-2.0, 2.0]` | Range of proportional selection parameter delta. |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `n_grid` | `integer` |  | `200` | Grid points for delta in the identified set computation. |
| `r_max` | `number` |  | `1.3` | Maximum R-squared assumption. Oster recommends 1.3 * R-squared from the fully controlled regression. If <= 0, it is set to 1.3 * R_full automatically. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `x_base` | `array[string]` | ✓ |  | Key treatment/variable(s) of interest. |
| `x_controls` | `array[string]` | ✓ |  | Additional controls whose inclusion tightens identification. |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.oster_delta(y="outcome", data=df, x_base=["a", "b"], x_controls=["a", "b"])
print(result.summary())
```

---
### `sp.selection_bounds()`

**Lee (2009) bounds for ATE under sample selection, optionally Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariates to condition on for tighter (conditional) bounds. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string` |  | `'conditional'` | - ``'conditional'``: compute Lee bounds within covariate strata and average (tighter). - ``'unconditional'``: standard Lee bounds ignoring covariates. |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `selection` | `string` | ✓ |  | Binary indicator: 1 = outcome observed, 0 = missing. |
| `treatment` | `string` | ✓ |  | Binary treatment (0/1). |
| `y` | `string` | ✓ |  | Outcome variable (may have NaN when selection=0). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.selection_bounds(y="outcome", data=df, treatment="value", selection="value")
print(result.summary())
```

---
