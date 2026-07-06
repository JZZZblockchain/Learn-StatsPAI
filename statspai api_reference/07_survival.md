# survival

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Survival and duration analysis models.

**12 个公共函数**

### `sp.CoxResult()`

**Result from Cox proportional hazards estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_X` | `string` |  |  | _X parameter. |
| `_baseline_hazard_df` | `string` |  |  | _baseline_hazard_df parameter (Optional[pandas.DataFrame]). |
| `_concordance` | `number` |  |  | _concordance parameter (Optional[float]). |
| `_durations` | `string` |  |  | _durations parameter. |
| `_events` | `string` |  |  | _events parameter. |
| `_hazard_ratios` | `string` |  |  | _hazard_ratios parameter. |
| `_hr_ci` | `string` |  |  | _hr_ci parameter. |
| `_schoenfeld_resid` | `string` |  |  | _schoenfeld_resid parameter. |
| `_strata` | `string` |  |  | _strata parameter. |
| `data_info` | `object` |  |  | data_info parameter (Optional[Dict[str, Any]]). |
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). |
| `model_info` | `string` | ✓ |  | model_info parameter. |
| `params` | `string` | ✓ |  | params parameter. |
| `std_errors` | `string` | ✓ |  | std_errors parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CoxResult(params="value", std_errors="value", model_info="value")
print(result.summary())
```

---
### `sp.CumIncResult()`

**Cumulative incidence functions for competing risks.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `causes` | `array[string]` | ✓ |  | causes parameter (List[int]). |
| `cif_table` | `string` | ✓ |  | cif_table parameter (pd.DataFrame). |
| `gray_test` | `object` |  |  | gray_test parameter (Optional[Dict[int, Dict[str, float]]]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CumIncResult(cif_table="value", causes=["a", "b"])
print(result.summary())
```

---
### `sp.FineGrayResult()`

**Fine-Gray proportional subdistribution hazards model result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bse` | `string` | ✓ |  | bse parameter (np.ndarray). |
| `cause` | `integer` | ✓ |  | cause parameter (int). |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `loglik` | `number` | ✓ |  | loglik parameter (float). |
| `n_events` | `integer` | ✓ |  | Number of events. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `params` | `string` | ✓ |  | params parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FineGrayResult(params="value", bse="value", covariates=["a", "b"], cause=1.0, n_obs=1.0, n_events=1.0, loglik=1.0)
print(result.summary())
```

---
### `sp.KMResult()`

**Kaplan-Meier survival analysis result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `tables` | `object` | ✓ |  | tables parameter (Dict[str, pandas.DataFrame]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.KMResult()
print(result.summary())
```

---
### `sp.aft()`

**Fit an Accelerated Failure Time model by MLE. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `family` | `string (enum)` |  | `'weibull'` | family parameter (AFTFamily). |
| `formula` | `string` | ✓ |  | ``"duration + event ~ x1 + x2"``. |

> **family** options: `'exponential'`, `'weibull'`, `'lognormal'`, `'loglogistic'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.aft(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/survival_ph.md`

---
### `sp.cox()`

**Cox Proportional Hazards model via partial likelihood. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` |  |  | Column name for cluster-robust SE. |
| `data` | `string` |  |  | Input data. |
| `duration` | `string` |  |  | Column name for follow-up time (overrides formula LHS). |
| `event` | `string` |  |  | Column name for event indicator (1 = event, 0 = censored). |
| `formula` | `string` |  |  | Formula of the form ``'duration ~ x1 + x2'``. If given, ``duration`` is inferred from the LHS. |
| `hazard_ratio` | `boolean` |  | `True` | If True, report hazard ratios in the summary alongside coefficients. |
| `robust` | `string` |  | `'nonrobust'` | ``'hc0'`` for sandwich SE. |
| `strata` | `string` |  |  | Column name for stratification variable. |
| `ties` | `string` |  | `'efron'` | Tie-handling method: ``'efron'`` or ``'breslow'``. |
| `x` | `array[string]` |  |  | Covariate column names (overrides formula RHS). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cox(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/survival_ph.md`

---
### `sp.cox_frailty()`

**Cox proportional hazards with shared gamma frailty.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Column identifying clusters (e.g. hospital, site). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | ``"duration + event ~ x1 + x2"`` (like R's ``Surv(time, event) ~ x``). |
| `maxiter` | `integer` |  | `50` | maxiter parameter (int). |
| `tol` | `number` |  | `1e-06` | Numerical convergence tolerance. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cox_frailty(data=df, cluster="value")
print(result.summary())
```

---
### `sp.cuminc()`

**Cumulative incidence functions for competing risks (Aalen-Johansen).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the confidence bands. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `duration` | `string` | ✓ |  | Column name for the follow-up time. |
| `event` | `string` | ✓ |  | Column name for the event indicator. ``0`` = censored; ``1, 2, ...`` = competing causes. |
| `group` | `string` |  |  | Column name for a grouping variable. When supplied, CIFs are estimated per group and Gray's K-sample test is reported per cause. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cuminc(data=df, duration="value", event="value")
print(result.summary())
```

> 📁 See also: `docs/guides/competing_risks.md`

---
### `sp.finegray()`

**Fine & Gray (1999) proportional subdistribution hazards model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cause` | `integer` |  | `1` | Cause of interest (default ``1``). |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `duration` | `string` | ✓ |  | Follow-up-time column. |
| `event` | `string` | ✓ |  | Event indicator: ``0`` = censored, ``1, 2, ...`` = causes. |
| `max_iter` | `integer` |  | `50` | Newton-Raphson controls. |
| `tol` | `number` |  | `1e-07` | Newton-Raphson controls. |
| `x` | `array[string]` | ✓ |  | Covariate column names. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.finegray(x=["treatment", "covariate1", "covariate2"], data=df, duration="value", event="value")
print(result.summary())
```

> 📁 See also: `docs/guides/competing_risks.md`

---
### `sp.kaplan_meier()`

**Kaplan-Meier non-parametric survival function estimator. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals (Greenwood formula). |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `duration` | `string` | ✓ |  | Column name for duration / follow-up time. |
| `event` | `string` | ✓ |  | Column name for event indicator (1 = event, 0 = censored). |
| `group` | `string` |  |  | Column name for group variable (stratification). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.kaplan_meier(formula="lwage ~ x1 + x2", data=df, duration="value", event="value")
print(result.summary())
```

> 📁 See also: `docs/guides/survival_ph.md`

---
### `sp.logrank_test()`

**Log-rank test for equality of survival distributions across groups. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `duration` | `string` | ✓ |  | Column names. |
| `event` | `string` | ✓ |  | Column names. |
| `group` | `string` | ✓ |  | Column names. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.logrank_test(data=df, duration="value", event="value", group="value")
print(result.summary())
```

---
### `sp.survreg()`

**Parametric survival model (AFT parameterization). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `dist` | `string` |  | `'weibull'` | dist parameter (str). |
| `duration` | `string` |  |  | Follow-up time column (or formula LHS). |
| `event` | `string` |  |  | Event indicator column. |
| `formula` | `string` |  |  | Formula ``'duration ~ x1 + x2'``. |
| `robust` | `string` |  | `'nonrobust'` | Robust standard-error or covariance estimator option. |
| `x` | `array[string]` |  |  | Covariate columns (or formula RHS). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.survreg(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/survival_ph.md`

---
