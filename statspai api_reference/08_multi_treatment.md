# multi_treatment

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Multi-valued Treatment Effects.

Estimates causal effects when the treatment takes more than two
values (e.g., different drug dosages, multiple policy options).

Uses inverse probability weighting with multinomial propensity scores.

References
----------
Cattaneo, M. D. (2010).
Efficient semiparametric estimation of multi-valued treatment effects.
Journal of Econometrics, 155(2), 138-154. [@cattaneo2010efficient]

Lechner, M. (2001).
Identification and estimation of causal effects of multiple treatments
under the conditional independence assumption.
Econometric Evaluation of Labour Market Policies, 43-58. [@lechner2001identification]

**2 个公共函数**

### `sp.MultiTreatment()`

**Multi-valued treatment effects estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `reference` | `integer` |  |  | reference parameter (Optional[int]). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MultiTreatment(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.multi_treatment()`

**Effects of multi-valued (3+ level) treatments via AIPW. Returns pairwise contrasts versus a reference level.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
| `reference` | `integer` |  |  | Reference treatment level (defaults to 0 / smallest) |
| `treat` | `string` | ✓ |  | Multi-valued treatment (int) |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.multi_treatment(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
