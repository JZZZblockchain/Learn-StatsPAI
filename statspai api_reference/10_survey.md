# survey

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

Survey design and weighted estimation — StatsPAI's answer to R's ``survey``
package and Stata's ``svy:`` prefix.

Supports stratified, clustered, and weighted survey designs with
design-corrected standard errors for means, totals, and regression.

>>> import statspai as sp
>>> design = sp.svydesign(data=df, weights='pw', strata='stratum',
...                       cluster='psu')
>>> design.mean('income')
>>> design.total('income')
>>> design.glm('income ~ education + age')

**7 个公共函数**

### `sp.SurveyDesign()`

**Declare a complex survey design.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Primary sampling unit (PSU) variable (column name). |
| `data` | `string` | ✓ |  | Survey microdata. |
| `fpc` | `string` |  |  | Finite population correction -- column of stratum population sizes or sampling fractions. If values are < 1 they are treated as fractions; otherwise as population counts. |
| `nest` | `boolean` |  | `False` | If True, PSU ids are nested within strata (re-label internally). |
| `strata` | `string` |  |  | Stratification variable (column name). |
| `weights` | `string` | ✓ |  | Sampling weights (inverse probability). If *str*, column name in *data*. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SurveyDesign(data=df, weights="value")
print(result.summary())
```

---
### `sp.linear_calibration()`

**Deville-Sarndal (1992) linear calibration.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `totals` | `object` | ✓ |  | ``{column_name: population_total}`` for continuous auxiliary variables. |
| `weight` | `string` |  |  | Design weight column. If ``None``, uses equal weights. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.linear_calibration(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/survey_ph.md`

---
### `sp.rake()`

**Raking (iterative proportional fitting).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `margins` | `object` | ✓ |  | ``{column_name: {category: target_proportion}}``. E.g. ``{"sex": {"M": 0.49, "F": 0.51}, "age_group": {"18-34": 0.3, ...}}``. |
| `max_iter` | `integer` |  | `100` | Maximum number of optimisation iterations. |
| `tol` | `number` |  | `1e-06` | Numerical convergence tolerance. |
| `weight` | `string` |  |  | Existing design weight column. If ``None``, starts with equal weights. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rake(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/survey_ph.md`

---
### `sp.svydesign()`

**Declare a complex survey design for design-corrected estimation. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | PSU cluster variable |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `fpc` | `string` |  |  | Finite population correction column |
| `strata` | `string` |  |  | Stratification variable |
| `weights` | `string` | ✓ |  | Sampling weights column |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.svydesign(data=df, weights="value")
print(result.summary())
```

> 📁 See also: `docs/guides/survey_ph.md`

---
### `sp.svyglm()`

**Survey-weighted generalised linear model. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `design` | `string` | ✓ |  | design parameter ('SurveyDesign'). |
| `family` | `string` |  | `'gaussian'` | ``"gaussian"``, ``"binomial"`` (logistic), or ``"poisson"``. |
| `formula` | `string` | ✓ |  | ``"y ~ x1 + x2"`` style formula. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.svyglm(formula="lwage ~ x1 + x2", design="value")
print(result.summary())
```

> 📁 See also: `docs/guides/survey_ph.md`

---
### `sp.svymean()`

**Survey-weighted mean with design-corrected standard errors. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `design` | `string` | ✓ |  | design parameter ('SurveyDesign'). |
| `variables` | `array[string]` | ✓ |  | Column name(s) in the design's data. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.svymean(variables=["a", "b"], design="value")
print(result.summary())
```

> 📁 See also: `docs/guides/survey_ph.md`

---
### `sp.svytotal()`

**Survey-weighted total with design-corrected standard errors. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `design` | `string` | ✓ |  | design parameter ('SurveyDesign'). |
| `variables` | `array[string]` | ✓ |  | variables parameter (Union[str, List[str]]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.svytotal(variables=["a", "b"], design="value")
print(result.summary())
```

> 📁 See also: `docs/guides/survey_ph.md`

---
