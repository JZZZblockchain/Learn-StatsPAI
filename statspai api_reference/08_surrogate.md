# surrogate

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Long-term effects via surrogate indices (``sp.surrogate``).

Industrial A/B tests can only run for weeks, but the quantities of interest
(LTV, retention, clinical outcomes) are months or years downstream. The
surrogate-index framework lets you extrapolate short-term surrogates to
long-term outcomes by combining an experimental sample (with the surrogate)
and an observational sample (with both surrogate and long-term outcome).

Estimators
----------
- :func:`surrogate_index` — Athey, Chetty, Imbens & Kang (2019).
  Classical single-wave surrogate index.
- :func:`long_term_from_short` — Tran, Bibaut & Kallus (arXiv:2311.08527,
  2023). Long-term effect of long-term treatments from short-term
  experiments.
- :func:`proximal_surrogate_index` — Imbens, Kallus, Mao & Wang (2025, JRSS-B
  87(2); arXiv:2202.07234). Proximal identification when unobserved
  confounders link surrogate and long-term outcome.

References
----------
Athey, S., Chetty, R., Imbens, G. W., & Kang, H. (2019).
"The Surrogate Index: Combining Short-Term Proxies to Estimate Long-Term
Treatment Effects More Rapidly and Precisely." NBER Working Paper 26463. [@athey2019surrogate]

Imbens, G., Kallus, N., Mao, X., & Wang, Y. (2025).
"Long-term Causal Inference Under Persistent Confounding via Data
Combination." Journal of the Royal Statistical Society Series B,
87(2), 362-388. arXiv:2202.07234. [@imbens2025long]

**3 个公共函数**

### `sp.long_term_from_short()`

**Long-term ATE under multi-wave short-term surrogates; extends the classical surrogate index to sustained treatments via iterated conditional expectations (Ghassami et al. 2024).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `experimental` | `string` | ✓ |  | experimental parameter (DataFrame). |
| `long_term_outcome` | `string` | ✓ |  | long_term_outcome parameter (str). |
| `n_boot` | `integer` |  | `200` | Number of bootstrap replications. |
| `observational` | `string` | ✓ |  | observational parameter (DataFrame). |
| `surrogates_waves` | `array[string]` | ✓ |  | List of wave column lists |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.long_term_from_short(experimental="value", observational="value", treatment="value", surrogates_waves=["a", "b"], long_term_outcome="value")
print(result.summary())
```

---
### `sp.proximal_surrogate_index()`

**Proximal surrogate-index estimator: long-term ATE when an unobserved U confounds S->Y, using a proxy W and 2SLS-style bridge-function identification (Imbens-Kallus-Mao-Wang 2025, JRSS-B).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `experimental` | `string` | ✓ |  | experimental parameter (DataFrame). |
| `long_term_outcome` | `string` | ✓ |  | long_term_outcome parameter (str). |
| `n_boot` | `integer` |  | `200` | Number of bootstrap replications. |
| `observational` | `string` | ✓ |  | observational parameter (DataFrame). |
| `proxies` | `array[string]` | ✓ |  | proxies parameter (list). |
| `surrogates` | `array[string]` | ✓ |  | surrogates parameter (list). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.proximal_surrogate_index(experimental="value", observational="value", treatment="value", surrogates=["a", "b"], proxies=["a", "b"], long_term_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/proximal_family.md`

---
### `sp.surrogate_index()`

**Athey-Chetty-Imbens-Kang surrogate-index estimator for the long-term ATE: combines an experimental sample (treatment + short-term surrogate) with an observational sample (surrogate + long-term outcome) to extrapolate the effect on the long-term outcome.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `experimental` | `string` | ✓ |  | experimental parameter (DataFrame). |
| `long_term_outcome` | `string` | ✓ |  | long_term_outcome parameter (str). |
| `model` | `string` |  | `'ols'` | Model variant or parameterisation to fit. |
| `n_boot` | `integer` |  | `0` | Bootstrap replicates (0 = analytic delta-method SE) |
| `observational` | `string` | ✓ |  | observational parameter (DataFrame). |
| `surrogates` | `array[string]` | ✓ |  | surrogates parameter (list). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.surrogate_index(experimental="value", observational="value", treatment="value", surrogates=["a", "b"], long_term_outcome="value")
print(result.summary())
```

---
