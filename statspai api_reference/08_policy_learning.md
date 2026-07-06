# policy_learning

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Policy Learning: Optimal treatment assignment from heterogeneous effects.

Learns an interpretable treatment assignment policy that maximises
the expected welfare (value) of the population. Given estimated CATE,
finds the optimal tree-based policy: "who should be treated?"

Components
----------
- **PolicyTree** : Optimal depth-limited decision tree for treatment
  assignment (Athey & Wager 2021).
- **policy_value** : Evaluate the expected value of a treatment policy
  using doubly robust scores.

References
----------
Athey, S. & Wager, S. (2021).
Policy Learning with Observational Data.
Econometrica, 89(1), 133-161. [@athey2021matrix]

Zhou, Z., Athey, S., & Wager, S. (2023).
Offline Multi-Action Policy Learning: Generalization and Optimization.
Operations Research, 71(1), 148-183. [@zhou2023offline]

**9 个公共函数**

### `sp.OPEResult()`

**Container returned by sp.ope.* estimators (IPS, SNIPS, DR, Switch-DR, DM). Reports value, SE, CI, importance-ratio diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | Confidence interval (lo, hi) |
| `diagnostics` | `object` | ✓ |  | Importance-ratio diagnostics |
| `method` | `string` | ✓ |  | OPE estimator name (ips, snips, dr, switch_dr, dm) |
| `se` | `number` | ✓ |  | Standard error of the value estimate |
| `value` | `number` | ✓ |  | Estimated policy value |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.OPEResult(method="value", value=1.0, se=1.0, ci=["a", "b"])
print(result.summary())
```

---
### `sp.PolicyTree()`

**Optimal depth-limited policy tree.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `max_depth` | `integer` |  | `2` | max_depth parameter (int). |
| `min_leaf_size` | `integer` |  | `25` | min_leaf_size parameter (int). |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `policy_covariates` | `array[string]` |  |  | policy_covariates parameter (Optional[List[str]]). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PolicyTree(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.PolicyTreeResult()`

**Result of :func:`policy_tree`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `fraction_treated` | `number` | ✓ |  | fraction_treated parameter (float). |
| `max_depth` | `integer` |  | `0` | max_depth parameter (int). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `policy` | `string` | ✓ |  | policy parameter (ndarray). |
| `policy_covariates` | `array[string]` |  | `[]` | policy_covariates parameter (Tuple[str, ...]). |
| `rules` | `string` | ✓ |  | rules parameter (str). |
| `scores` | `string` |  |  | scores parameter (Optional[numpy.ndarray]). |
| `tree` | `string` | ✓ |  | tree parameter (PolicyTree). |
| `value_gain` | `number` | ✓ |  | value_gain parameter (float). |
| `value_gain_se` | `number` |  | `nan` | value_gain_se parameter (float). |
| `value_policy` | `number` | ✓ |  | value_policy parameter (float). |
| `value_policy_ci` | `array[string]` |  | `[nan, nan]` | value_policy_ci parameter (Tuple[float, float]). |
| `value_policy_se` | `number` |  | `nan` | value_policy_se parameter (float). |
| `value_treat_all` | `number` | ✓ |  | value_treat_all parameter (float). |
| `value_treat_none` | `number` | ✓ |  | value_treat_none parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PolicyTreeResult(tree="value", policy="value", value_treat_all=1.0, value_treat_none=1.0, value_policy=1.0, value_gain=1.0, fraction_treated=1.0, rules="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.direct_method()`

**Direct outcome regression (plug-in Q-model) OPE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | A parameter (np.ndarray). |
| `R` | `string` | ✓ |  | R parameter (np.ndarray). |
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `n_actions` | `integer` |  |  | Number of actions. |
| `pi_target` | `string` | ✓ |  | pi_target parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.direct_method(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
### `sp.doubly_robust()`

**Doubly-robust OPE (Dudik et al. 2011).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | A parameter (np.ndarray). |
| `R` | `string` | ✓ |  | R parameter (np.ndarray). |
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `clip` | `number` |  | `50.0` | clip parameter (float). |
| `n_actions` | `integer` |  |  | Number of actions. |
| `pi_behavior` | `string` |  |  | pi_behavior parameter (Optional[np.ndarray]). |
| `pi_target` | `string` | ✓ |  | pi_target parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.doubly_robust(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
### `sp.ips()`

**Inverse propensity score OPE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | A parameter (np.ndarray). |
| `R` | `string` | ✓ |  | R parameter (np.ndarray). |
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `clip` | `number` |  | `50.0` | clip parameter (float). |
| `pi_behavior` | `string` |  |  | pi_behavior parameter (Optional[np.ndarray]). |
| `pi_target` | `string` | ✓ |  | pi_target parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ips(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
### `sp.policy_tree()`

**Doubly-robust policy-tree -- article-facing alias. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `array[string]` |  |  | Feature matrix or covariate DataFrame. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `d` | `string` |  |  | d parameter (Optional[str]). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `depth` | `integer` |  |  | depth parameter (Optional[int]). |
| `max_depth` | `integer` |  |  | max_depth parameter (Optional[int]). |
| `treat` | `string` |  |  | Treatment indicator or first-treatment-period column. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.policy_tree(y="outcome", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.policy_value()`

**Evaluate the expected value of a treatment policy. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `policy` | `string` | ✓ |  | Binary policy recommendations (0 or 1). |
| `scores` | `string` | ✓ |  | Doubly robust scores (AIPW pseudo-outcomes for treatment). Positive scores indicate the individual benefits from treatment. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.policy_value(scores="value", policy="value")
print(result.summary())
```

---
### `sp.snips()`

**Self-normalised IPS (bias-reduction for large IS weights).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | A parameter (np.ndarray). |
| `R` | `string` | ✓ |  | R parameter (np.ndarray). |
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `clip` | `number` |  | `50.0` | clip parameter (float). |
| `pi_behavior` | `string` |  |  | pi_behavior parameter (Optional[np.ndarray]). |
| `pi_target` | `string` | ✓ |  | pi_target parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.snips(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
