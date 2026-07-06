# gformula

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Parametric g-formula via Iterative Conditional Expectation (ICE).

Sequential g-computation for longitudinal data with time-varying
treatments and time-varying confounding -- the estimator pioneered
by Robins (1986) and made tractable in its ICE form by Bang &
Robins (2005).

Public API
----------
>>> import statspai as sp
>>> result = sp.gformula.ice(
...     data=df,
...     id_col="id", time_col="t",
...     treatment_cols=["A0", "A1", "A2"],
...     confounder_cols=["L0", "L1", "L2"],
...     outcome_col="Y",
...     treatment_strategy=[1, 1, 1],  # always-treat
... )
>>> result.summary()

**3 个公共函数**

### `sp.ICEResult()`

**Result of the iterative conditional expectation (ICE) g-formula.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple[float, float]). |
> 📝 *ci 参数（浮点数二元组）。*
| `method` | `string` |  | `'parametric-g-formula-ICE'` | Estimator or algorithm variant to use. |
| `per_timepoint_means` | `array[string]` |  |  | per_timepoint_means parameter (list[float] \| None). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `strategy` | `array[string]` | ✓ |  | strategy parameter (list). |
| `value` | `number` | ✓ |  | value parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ICEResult(strategy=["a", "b"], value=1.0, se=1.0, ci=["a", "b"])
print(result.summary())
```

---
### `sp.MCGFormulaResult()`

**Result of one or two Monte-Carlo g-formula arms.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `contrast_ci` | `array[string]` |  |  | contrast_ci parameter (Optional[tuple]). |
| `contrast_se` | `number` |  |  | contrast_se parameter (Optional[float]). |
| `contrast_value` | `number` |  |  | contrast_value parameter (Optional[float]). |
| `method` | `string` |  | `'MC-parametric-g-formula'` | Estimator or algorithm variant to use. |
| `n_simulations` | `integer` | ✓ |  | Number of simulations. |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `strategies` | `object` |  |  | strategies parameter (Optional[dict]). |
| `trajectories` | `string` |  |  | trajectories parameter (Optional[pd.DataFrame]). |
| `value` | `number` | ✓ |  | value parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MCGFormulaResult(value=1.0, se=1.0, ci=["a", "b"], n_simulations=1.0)
print(result.summary())
```

---
### `sp.gformula_mc()`

**Monte-Carlo parametric g-formula estimate of :math:`E[Y(g)]`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bootstrap` | `integer` |  | `200` | Non-parametric bootstrap replicates for SE / CI. Set to 0 to skip inference (point estimate only). |
| `confounder_cols` | `array[string]` | ✓ |  | Either a flat list (same confounders at every timepoint) or a list-of-lists with per-timepoint confounder sets. A confounder whose name ends in an index / time tag can be supplied as a flat list; for true time-varying confounders supply the nested form so the g-formula respects the correct temporal ordering. |
| `control_strategy` | `array[string]` |  |  | If provided, a second arm is simulated under the control strategy and a contrast (treat - control) is reported. |
| `data` | `string` | ✓ |  | One row per subject. Must contain all treatment, confounder and outcome columns. |
| `id_col` | `string` |  |  | Unused when ``data`` is already wide; kept for API symmetry |
| `n_simulations` | `integer` |  | `10000` | Monte-Carlo trajectories per arm. |
| `outcome_col` | `string` | ✓ |  | Terminal outcome column. |
| `return_trajectories` | `boolean` |  | `False` | Attach the simulated trajectories DataFrame to the result. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `strategy` | `array[string]` |  | `[1, 1, 1]` | Either a static sequence of treatment values (e.g. ``[1]*K`` = always-treat), or a callable with signature ``strategy(t: int, history: dict) -> np.ndarray of length n_sim`` for dynamic regimes that depend on simulated state. |
| `time_col` | `string` |  |  | Unused when ``data`` is already wide; kept for API symmetry |
| `treatment_cols` | `array[string]` | ✓ |  | Treatment column names, chronologically ordered. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.gformula_mc(formula="lwage ~ x1 + x2", data=df, treatment_cols=["a", "b"], confounder_cols=["a", "b"], outcome_col="value")
print(result.summary())
```

---
