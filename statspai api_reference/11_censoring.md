# censoring

> 📂 所属分类:11 · 其他杂项 (Other)

Inverse probability of censoring / treatment weighting primitives.

**2 个公共函数**

### `sp.IPCWResult()`

**Result of an IPCW fit.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `fitted_hazards` | `string` |  | `None` | fitted_hazards parameter (np.ndarray). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `stabilized` | `boolean` | ✓ |  | stabilized parameter (bool). |
| `summary_stats` | `object` | ✓ |  | summary_stats parameter (dict). |
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.IPCWResult(weights="value", stabilized=True, method="value")
print(result.summary())
```

---
### `sp.ipcw()`

**Inverse Probability of Censoring Weights -- corrects for informative censoring under conditional independent censoring given covariates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `censor_covariates` | `array[string]` | ✓ |  | censor_covariates parameter (list). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `event` | `string` | ✓ |  | event parameter (str). |
| `method` | `string (enum)` |  | `'pooled_logistic'` | Estimator or algorithm variant to use. |
| `stabilize` | `boolean` |  | `True` | stabilize parameter (bool). |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treatment_covariates` | `array[string]` |  |  | treatment_covariates parameter (list). |
| `truncate` | `array[string]` |  | `[0.01, 0.99]` | truncate parameter (tuple). |

> **method** options: `'pooled_logistic'`, `'cox_ph'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ipcw(data=df, time="value", event="value", censor_covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/survival_ph.md`

---
