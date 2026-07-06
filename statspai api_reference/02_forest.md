# forest

> 📂 所属分类:02 · 元学习器与机器学习因果推断 (Meta-Learners & ML Causal)

Forest-based causal inference estimators for StatsPAI.

Hosts ``CausalForest`` (grf-style honest causal forests) and its
companions:

- :func:`causal_forest` / :class:`CausalForest` — heterogeneous
  treatment-effect estimation via honest random forests
  (Wager-Athey 2018; Athey-Tibshirani-Wager 2019).
- :func:`iv_forest` — instrumental-variable causal forests
  (Athey-Tibshirani-Wager 2019).
- :func:`multi_arm_forest` — multi-arm extension.
- :func:`calibration_test` / :func:`test_calibration` /
  :func:`rate` / :func:`honest_variance` — post-fit honesty &
  calibration diagnostics.

This package was previously named ``statspai.causal`` — the old
name is kept as a deprecation shim for one minor version cycle.
Use ``from statspai.forest import ...`` going forward.

**8 个公共函数**

### `sp.CausalForest()`

**Causal Forest for heterogeneous treatment effect estimation**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bootstrap` | `boolean` |  | `True` | Whether to use bootstrap sampling for trees |
| `discrete_treatment` | `boolean` |  | `True` | Whether treatment is discrete (binary/categorical) or continuous |
| `honest` | `boolean` |  | `True` | Whether to use honest estimation (separate samples for splitting and effects) |
| `max_depth` | `integer` |  |  | Maximum depth of trees |
| `max_samples` | `number` |  | `0.5` | Fraction of samples to use for each tree |
| `min_samples_leaf` | `integer` |  | `5` | Minimum number of samples required to be at a leaf node |
| `model_t` | `string` |  |  | Model for treatment propensity (first stage) |
| `model_y` | `string` |  |  | Model for outcome regression (first stage) |
| `n_estimators` | `integer` |  | `100` | Number of trees in the forest |
| `n_jobs` | `integer` |  | `1` | Number of parallel jobs |
| `random_state` | `integer` |  |  | Random state for reproducibility |
| `verbose` | `integer` |  | `0` | Verbosity level |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CausalForest()
print(result.summary())
```

---
### `sp.average_treatment_effect()`

**Aggregate CATE predictions into ATE/ATT/ATC/ATO targets. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `T` | `string` |  |  | T parameter (Optional[np.ndarray]). |
| `X` | `string` |  |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `clip` | `number` |  | `0.01` | Propensity scores are clipped to ``[clip, 1-clip]`` before the inverse-propensity term to stabilise the score under near-overlap violations. |
| `forest` | `string` | ✓ |  | forest parameter ('CausalForest'). |
| `target_sample` | `string` |  | `'all'` | target_sample parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.average_treatment_effect(forest="value")
print(result.summary())
```

---
### `sp.calibration_test()`

**BLP-of-CATE calibration test (Chernozhukov-Demirer-Duflo-Fernandez-Val 2020).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `T` | `string` |  |  | If not given, the forest's stored training arrays are used. |
| `X` | `string` |  |  | If not given, the forest's stored training arrays are used. |
| `Y` | `string` |  |  | If not given, the forest's stored training arrays are used. |
| `alpha` | `number` |  | `0.05` | Significance level for reported CIs. |
| `forest` | `string` | ✓ |  | forest parameter ('CausalForest'). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.calibration_test(forest="value")
print(result.summary())
```

---
### `sp.causal_forest()`

**Causal Forest for heterogeneous treatment effect estimation (CATE). Validation: certified evidence with scoped limitations. Known limitations: The AIPW ATE/ATT are validated against grf on clean-overlap designs only; under severe propensity-overlap loss the AIPW influence function inflates the standard error (conservative, over-covering inference), so inspect the sp.audit overlap diagnostic before interpreting the ATE on that kind of sample.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | 'y ~ treatment \| x1 + x2' (pipe separates covariates) |
| `n_trees` | `integer` |  | `100` | Number of trees. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.causal_forest(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.forest_diagnostics()`

**Return overlap and CATE-distribution diagnostics for a fitted forest.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `T` | `string` |  |  | T parameter (Optional[np.ndarray]). |
| `X` | `string` |  |  | Feature matrix or covariate DataFrame. |
| `forest` | `string` | ✓ |  | forest parameter ('CausalForest'). |
| `propensity_bounds` | `array[string]` |  | `[0.05, 0.95]` | propensity_bounds parameter (Tuple[float, float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.forest_diagnostics(forest="value")
print(result.summary())
```

---
### `sp.honest_variance()`

**Half-sample bootstrap variance of the ATE/GATE estimate.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` |  |  | Feature matrix or covariate DataFrame. |
| `forest` | `string` | ✓ |  | forest parameter ('CausalForest'). |
| `n_splits` | `integer` |  | `25` | Number of random half-sample draws. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.honest_variance(forest="value")
print(result.summary())
```

---
### `sp.rate()`

**Rank-Average Treatment Effect (Yadlowsky et al. 2023).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `T` | `string` |  |  | If omitted, falls back to the forest's stored training arrays. |
| `X` | `string` |  |  | If omitted, falls back to the forest's stored training arrays. |
| `Y` | `string` |  |  | If omitted, falls back to the forest's stored training arrays. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `forest` | `string` | ✓ |  | forest parameter ('CausalForest'). |
| `q_grid` | `integer` |  | `100` | Number of quantile grid points used to report the TOC curve. Does not affect the point estimate or SE (those are computed from ranks exactly). |
| `seed` | `integer` |  |  | Ignored; kept for API backwards compatibility. |
| `target` | `string (enum)` |  | `'AUTOC'` | target parameter (str). |

> **target** options: `'AUTOC'`, `'QINI'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rate(forest="value")
print(result.summary())
```

---
### `sp.test_calibration()`

**BLP-of-CATE calibration test (Chernozhukov-Demirer-Duflo-Fernandez-Val 2020).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `T` | `string` |  |  | If not given, the forest's stored training arrays are used. |
| `X` | `string` |  |  | If not given, the forest's stored training arrays are used. |
| `Y` | `string` |  |  | If not given, the forest's stored training arrays are used. |
| `alpha` | `number` |  | `0.05` | Significance level for reported CIs. |
| `forest` | `string` | ✓ |  | forest parameter ('CausalForest'). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.test_calibration(forest="value")
print(result.summary())
```

---
