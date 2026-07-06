# mediation

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Causal Mediation Analysis module for StatsPAI.

Implements modern causal mediation analysis following Imai, Keele, and
Tingley (2010), decomposing total treatment effects into:
- Average Causal Mediation Effect (ACME): indirect effect through mediator
- Average Direct Effect (ADE): direct effect not through mediator

Also supports the classical Baron-Kenny approach for comparison.

References
----------
Imai, K., Keele, L., and Tingley, D. (2010).
"A General Approach to Causal Mediation Analysis."
*Psychological Methods*, 15(4), 309-334. [@imai2010general]

Baron, R.M. and Kenny, D.A. (1986).
"The Moderator-Mediator Variable Distinction in Social Psychological Research."
*Journal of Personality and Social Psychology*, 51(6), 1173-1182. [@baron1986moderator]

**6 个公共函数**

### `sp.FourWayResult()`

**Result container for :func:`four_way_decomposition`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cde` | `number` | ✓ |  | cde parameter (float). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `int_med` | `number` | ✓ |  | int_med parameter (float). |
| `int_ref` | `number` | ✓ |  | int_ref parameter (float). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `pie` | `number` | ✓ |  | pie parameter (float). |
| `proportions` | `object` | ✓ |  | proportions parameter (Dict[str, float]). |
| `total_effect` | `number` | ✓ |  | total_effect parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FourWayResult(cde=1.0, int_ref=1.0, int_med=1.0, pie=1.0, total_effect=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.MediationAnalysis()`

**Causal Mediation Analysis estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `inference` | `string` |  | `'bootstrap'` | inference parameter (str). |
| `mediator` | `string` | ✓ |  | mediator parameter (str). |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications. |
| `pvalue_method` | `string` |  | `'bootstrap_sign'` | pvalue_method parameter (str). |
| `seed` | `integer` |  | `42` | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MediationAnalysis(y="outcome", data=df, treat="value", mediator="value")
print(result.summary())
```

---
### `sp.four_way_decomposition()`

**Parametric four-way decomposition of TE = CDE + INT_ref + INT_med + PIE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `a0` | `number` |  | `0.0` | Reference and comparison levels of the treatment (default 0, 1). |
| `a1` | `number` |  | `1.0` | Reference and comparison levels of the treatment (default 0, 1). |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `m0` | `number` |  | `0.0` | Mediator reference level at which CDE is evaluated. |
| `mediator` | `string` | ✓ |  | mediator parameter (str). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.four_way_decomposition(y="outcome", data=df, treat="value", mediator="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
### `sp.mediate()`

**Mediation analysis (Imai-Keele-Tingley 2010). Decomposes the total effect into natural direct effect (NDE) and natural indirect effect (NIE) via an interventional or sequential-ignorability identification strategy. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Pre-treatment confounders |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `mediator` | `string` | ✓ |  | Mediator variable |
| `n_boot` | `integer` |  | `1000` | Bootstrap reps for NDE/NIE CIs |
| `treat` | `string` | ✓ |  | Binary treatment |
| `y` | `string` | ✓ |  | Outcome |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mediate(y="outcome", data=df, treat="value", mediator="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
### `sp.mediate_interventional()`

**Interventional (in)direct effects (VanderWeele, Vansteelandt, Robins 2014). Identifies mediation effects in the presence of treatment-induced mediator-outcome confounders where natural (in)direct effects are not identified. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Baseline covariates |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `mediator` | `string` | ✓ |  | Mediator variable |
| `treat` | `string` | ✓ |  | Binary treatment |
| `tv_confounders` | `array[string]` |  |  | Treatment-induced M-Y confounders |
| `y` | `string` | ✓ |  | Outcome |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mediate_interventional(y="outcome", data=df, treat="value", mediator="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
### `sp.mediate_sensitivity()`

**Sensitivity analysis for causal mediation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `mediator` | `string` | ✓ |  | mediator parameter (str). |
| `n_grid` | `integer` |  | `41` | Number of grid. |
| `rho_range` | `array[string]` |  | `[-0.9, 0.9]` | rho_range parameter (tuple). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mediate_sensitivity(y="outcome", data=df, treat="value", mediator="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
