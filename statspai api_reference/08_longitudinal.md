# longitudinal

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Longitudinal causal inference (``sp.longitudinal``).

Unified entry for What If Layer-4 methods (time-varying treatments with
time-varying confounders).  Wraps MSM / g-formula ICE / IPW under a
single dispatcher with a dynamic-regime DSL.

>>> import statspai as sp
>>> r = sp.longitudinal.analyze(
...     data=panel,
...     id="pid",
...     time="visit",
...     treatment="drug",
...     outcome="cd4",
...     time_varying=["cd4_lag", "viral_load_lag"],
...     baseline=["age", "sex"],
...     regime="if cd4_lag < 200 then 1 else 0",
... )
>>> r.summary()

>>> diff = sp.longitudinal.contrast(
...     data=panel, id="pid", time="visit",
...     treatment="drug", outcome="cd4",
...     regime_a="always_treat",
...     regime_b="never_treat",
...     time_varying=["cd4_lag"],
... )

**6 个公共函数**

### `sp.LongitudinalResult()`

**Result of a unified longitudinal analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple[float, float]). |
> 📝 *ci 参数（浮点数二元组）。*
| `diagnostics` | `object` |  | `None` | diagnostics parameter (dict). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n` | `integer` | ✓ |  | n parameter (int). |
| `n_periods` | `integer` | ✓ |  | Number of periods. |
| `regime_name` | `string` | ✓ |  | regime_name parameter (str). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `underlying_result` | `string` |  |  | underlying_result parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LongitudinalResult(method="value", regime_name="value", estimate=1.0, se=1.0, ci=["a", "b"], n=1.0, n_periods=1.0)
print(result.summary())
```

---
### `sp.Regime()`

**A dynamic treatment regime.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `kind` | `string` | ✓ |  | kind parameter (str). |
| `name` | `string` | ✓ |  | name parameter (str). |
| `rule` | `array[string]` | ✓ |  | rule parameter (Union[list, Callable]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.Regime(kind="value", name="value", rule=["a", "b"])
print(result.summary())
```

---
### `sp.always_treat()`

**Convenience: the always-treat regime over K periods.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K` | `integer` |  | `1` | K parameter (int). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.always_treat()
print(result.summary())
```

---
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
### `sp.never_treat()`

**Convenience: the never-treat regime over K periods.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K` | `integer` |  | `1` | K parameter (int). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.never_treat()
print(result.summary())
```

---
### `sp.regime()`

**Build a dynamic or static treatment regime from a string DSL, list, callable, or scalar. Supports 'if <cond> then <a> else <b>', 'always_treat', 'never_treat', and arbitrary safe expressions. Parsed via a whitelisted AST walker -- no dynamic code execution.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K` | `integer` |  | `1` | K parameter (int). |
| `name` | `string` |  |  | name parameter (str). |
| `rule` | `array[string]` | ✓ |  | rule parameter (str \| list \| callable \| scalar). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.regime(rule=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/grammar.md`

---
