# dtr

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Dynamic Treatment Regimes (DTR).

Estimates optimal sequential treatment rules when treatments are
assigned over multiple time periods.

Methods
-------
- **G-estimation** : Structural nested mean model for optimal DTR
    (Robins 1986, 2004).

References
----------
Robins, J. M. (2004).
Optimal Structural Nested Models for Optimal Sequential Decisions.
In Proceedings of the Second Seattle Symposium in Biostatistics, 189-326. [@robins2004optimal]

Murphy, S. A. (2003).
Optimal Dynamic Treatment Regimes.
JRSS-B, 65(2), 331-355. [@murphy2003optimal]

**2 个公共函数**

### `sp.GEstimation()`

**G-estimation for dynamic treatment regimes via SNMM.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates_by_stage` | `array[string]` | ✓ |  | covariates_by_stage parameter (List[List[str]]). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
| `propensity_covariates` | `array[string]` |  |  | propensity_covariates parameter (Optional[List[List[str]]]). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treatments` | `array[string]` | ✓ |  | treatments parameter (List[str]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GEstimation(y="outcome", data=df, treatments=["a", "b"], covariates_by_stage=["a", "b"])
print(result.summary())
```

---
### `sp.g_estimation()`

**G-estimation for a multi-stage dynamic treatment regime. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates_by_stage` | `array[string]` | ✓ |  | Covariates (tailoring variables) available at each stage. covariates_by_stage[k] are the variables available when deciding treatment k. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
| `propensity_covariates` | `array[string]` |  |  | Covariates for propensity model at each stage. If None, uses covariates_by_stage. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treatments` | `array[string]` | ✓ |  | Treatment variables at each stage, in temporal order. E.g., ['A1', 'A2'] for a two-stage DTR. |
| `y` | `string` | ✓ |  | Final outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.g_estimation(y="outcome", data=df, treatments=["a", "b"], covariates_by_stage=["a", "b"])
print(result.summary())
```

> 📁 See also: `nhefs_whatif.py`, `docs/guides/whatif_nhefs.md`

---
