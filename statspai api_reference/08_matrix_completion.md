# matrix_completion

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Matrix Completion for Causal Panel Data.

Estimates treatment effects in panel settings by completing the
counterfactual matrix of untreated potential outcomes using
nuclear-norm regularisation (low-rank matrix completion).

References
----------
Athey, S., Bayati, M., Doudchenko, N., Imbens, G., & Khosravi, K. (2021).
Matrix Completion Methods for Causal Panel Data Models.
JASA, 116(536), 1716-1730. [@athey2021matrix]

**2 个公共函数**

### `sp.MCPanel()`

**Matrix Completion for Causal Panels.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `lambda_reg` | `number` |  |  | lambda_reg parameter (Optional[float]). |
> 📝 *lambda_reg 参数（可选浮点数）。*
| `max_iter` | `integer` |  | `1000` | Maximum number of optimisation iterations. |
> 📝 *优化最大迭代次数。*
| `max_rank` | `integer` |  |  | max_rank parameter (Optional[int]). |
> 📝 *max_rank 参数（可选整数）。*
| `n_bootstrap` | `integer` |  | `200` | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `tol` | `number` |  | `1e-05` | Numerical convergence tolerance. |
> 📝 *数值收敛容差。*
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

result = sp.MCPanel(y="outcome", data=df, unit="value", time="value", treat="value")
print(result.summary())
```

---
### `sp.mc_panel()`

**Estimate treatment effects using matrix completion. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Panel data in long format. |
| `lambda_reg` | `number` |  |  | Nuclear norm regularisation parameter. If None, estimated via the universal threshold: lambda = sigma * sqrt(n). |
| `max_iter` | `integer` |  | `1000` | Maximum iterations for the proximal gradient algorithm. |
| `max_rank` | `integer` |  |  | Maximum rank for the completed matrix. If None, no constraint. |
| `n_bootstrap` | `integer` |  | `200` | Bootstrap iterations for standard errors. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `time` | `string` | ✓ |  | Time period variable. |
| `tol` | `number` |  | `1e-05` | Convergence tolerance. |
| `treat` | `string` | ✓ |  | Binary treatment indicator (0/1). Can be staggered. |
| `unit` | `string` | ✓ |  | Unit identifier variable. |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mc_panel(y="outcome", data=df, unit="value", time="value", treat="value")
print(result.summary())
```

---
