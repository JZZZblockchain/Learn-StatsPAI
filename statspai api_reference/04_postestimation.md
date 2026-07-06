# postestimation

> 📂 所属分类:04 · 诊断、稳健性与推断 (Diagnostics, Robustness & Inference)

Post-estimation tools for StatsPAI.

Provides:
- margins(): Average Marginal Effects (AME), Marginal Effects at the Mean (MEM)
- marginsplot(): Visualize marginal effects
- test(): Wald / F test for linear restrictions (beta1 = beta2, joint significance)
- lincom(): Linear combinations of coefficients with inference

Equivalent to Stata's ``margins``, ``test``, ``lincom`` commands.

**12 个公共函数**

### `sp.contrast()`

**Compute contrasts of predictive margins across levels of a variable. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Estimation data. |
| `method` | `string` |  | `'r'` | Contrast type: - ``'r'`` (reference): each level vs *reference* level. - ``'ar'`` (adjacent): each level vs the previous level. - ``'gw'`` (grand-mean weighted): each level vs the weighted grand mean of all levels. |
| `reference` | `string` |  |  | Reference level when ``method='r'``. Defaults to the smallest observed level. |
| `result` | `string` | ✓ |  | Fitted model result. |
| `variable` | `string` | ✓ |  | Categorical variable whose levels are contrasted. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.contrast(data=df, result="value", variable="value")
print(result.summary())
```

---
### `sp.event_study_table()`

**Adapter that turns an event-study fit into a regtable input.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `include_reference` | `boolean` |  | `False` | Whether to render the reference period row (typically ``t=-1``) where the estimate is identically zero. |
| `label_fmt` | `string` |  | `'t={t}'` | Format string for the row label of each event-time bin. The ``{t}`` placeholder receives the integer relative time. |
| `regex` | `string` |  |  | Pattern with one capture group that matches the relative time in coefficient names. Required when the CausalResult fast path is not applicable. Examples: ``r"^tau_(-?\d+)$"``, ``r"^lag(\d+)$"``, ``r"::(-?\d+)$"``. |
| `result` | `string` | ✓ |  | Fitted model. The CausalResult fast path is used automatically when ``model_info['event_study']`` is present. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.event_study_table(result="value")
print(result.summary())
```

---
### `sp.lincom()`

**Estimate a linear combination of coefficients with inference. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `expression` | `string` | ✓ |  | Linear combination. Examples: - ``"x1 + x2"`` -- beta_x1 + beta_x2 - ``"x1 - x2"`` -- beta_x1 - beta_x2 - ``"2*x1 + 3*x2"`` -- 2*beta_x1 + 3*beta_x2 |
| `result` | `string` | ✓ |  | Fitted model. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lincom(result="value", expression="value")
print(result.summary())
```

---
### `sp.margins()`

**Compute marginal effects from a fitted model. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `at` | `object` |  |  | Fix covariates at specific values for conditional margins. E.g., ``{'age': 30, 'female': 1}``. |
| `data` | `string` |  |  | Data to compute margins on. Defaults to the estimation sample. |
| `eps` | `number` |  | `1e-05` | Step size for numerical differentiation. |
| `method` | `string` |  | `'ame'` | - 'ame': Average Marginal Effect (average dy/dx across all obs) - 'mem': Marginal Effect at the Mean (dy/dx at mean of X) |
| `result` | `string` | ✓ |  | Fitted model result (must have ``.params`` and associated data). |
| `variables` | `array[string]` |  |  | Variables to compute dy/dx for. Default: all regressors. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.margins(data=df, result="value")
print(result.summary())
```

---
### `sp.margins_at()`

**Compute predictive margins at specific covariate values. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `at` | `object` | ✓ |  | Mapping of variable names to lists/arrays of values. If multiple variables are given, the Cartesian product of all value lists is used. Example:: at={"experience": [1, 5, 10], "female": [0, 1]} produces 6 grid points. |
| `data` | `string` | ✓ |  | Data to compute margins on. |
| `result` | `string` | ✓ |  | Fitted model result (must have ``.params`` and associated data). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.margins_at(data=df, result="value")
print(result.summary())
```

---
### `sp.margins_at_plot()`

**Plot predictive margins from ``margins_at()`` with confidence bands.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `by` | `string` |  |  | Variable to produce separate lines for (legend grouping). |
| `figsize` | `array[string]` |  | `[8, 5]` | figsize parameter (Tuple[float, float]). |
| `margins_at_df` | `string` | ✓ |  | Output from ``margins_at()``. |
| `palette` | `array[string]` |  |  | Colours for each ``by`` group. |
| `title` | `string` |  |  | title parameter (Optional[str]). |
| `x` | `string` |  |  | Variable to place on the x-axis. If *None*, inferred as the at-variable with the most unique values. |
| `xlabel` | `string` |  |  | xlabel parameter (Optional[str]). |
| `ylabel` | `string` |  | `'Predicted Value'` | ylabel parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.margins_at_plot(x=["treatment", "covariate1", "covariate2"], margins_at_df="value")
print(result.summary())
```

---
### `sp.margins_table()`

**Marginal-effects result that pipes straight into ``sp.regtable``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Forwarded verbatim to :func:`margins`. |
| `at` | `object` |  |  | Forwarded verbatim to :func:`margins`. |
| `data` | `string` |  |  | Forwarded verbatim to :func:`margins`. |
| `eps` | `number` |  | `1e-05` | Forwarded verbatim to :func:`margins`. |
| `method` | `string` |  | `'ame'` | Forwarded verbatim to :func:`margins`. |
| `result` | `string` | ✓ |  | Fitted model -- same input ``sp.margins`` accepts. |
| `variables` | `array[string]` |  |  | Forwarded verbatim to :func:`margins`. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.margins_table(data=df, result="value")
print(result.summary())
```

---
### `sp.marginsplot()`

**Plot marginal effects with confidence intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `color` | `string` |  | `'#2C3E50'` | color parameter (str). |
| `figsize` | `array[string]` |  | `[8, 5]` | figsize parameter (Tuple[float, float]). |
| `margins_df` | `string` | ✓ |  | Output from ``margins()``. |
| `title` | `string` |  |  | title parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.marginsplot(margins_df="value")
print(result.summary())
```

---
### `sp.postestimation_contract()`

**Return the post-estimation actions supported by *result*.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` |  |  | Analysis frame available for data-dependent actions. When supplied, the contract marks ``margins``/``predict`` paths as ready rather than merely method-available. |
| `include_diagnostics` | `boolean` |  | `True` | Include scalar diagnostics from ``model_info`` / ``diagnostics``. |
| `result` | `string` | ✓ |  | Fitted StatsPAI result, estimator, or compatible object. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.postestimation_contract(data=df, result="value")
print(result.summary())
```

---
### `sp.postestimation_report()`

**Return the post-estimation actions supported by *result*.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` |  |  | Analysis frame available for data-dependent actions. When supplied, the contract marks ``margins``/``predict`` paths as ready rather than merely method-available. |
| `include_diagnostics` | `boolean` |  | `True` | Include scalar diagnostics from ``model_info`` / ``diagnostics``. |
| `result` | `string` | ✓ |  | Fitted StatsPAI result, estimator, or compatible object. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.postestimation_report(data=df, result="value")
print(result.summary())
```

---
### `sp.pwcompare()`

**Pairwise comparisons of predictive margins across all levels. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adjust` | `string` |  | `'none'` | P-value adjustment method: - ``'none'``: unadjusted. - ``'bonferroni'``: Bonferroni correction. - ``'sidak'``: Sidak correction. - ``'holm'``: Holm step-down procedure. |
| `alpha` | `number` |  | `0.05` | Significance level for (adjusted) confidence intervals. |
| `data` | `string` | ✓ |  | Estimation data. |
| `result` | `string` | ✓ |  | Fitted model result. |
| `variable` | `string` | ✓ |  | Categorical variable whose levels are compared pairwise. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pwcompare(data=df, result="value", variable="value")
print(result.summary())
```

---
### `sp.test()`

**Wald test for linear restrictions on coefficients. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `hypothesis` | `string` | ✓ |  | Hypothesis specification. Examples: - ``"x1 = 0"`` -- test if beta_x1 = 0 - ``"x1 = x2"`` -- test if beta_x1 = beta_x2 - ``"x1 = x2 = 0"`` -- joint test - ``"x1 + x2 = 1"`` -- linear restriction |
| `result` | `string` | ✓ |  | Fitted model with ``.params`` and ``.std_errors``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.test(result="value", hypothesis="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/choosing_iv_estimator.md`, `docs/guides/migration-from-r.md`

---
