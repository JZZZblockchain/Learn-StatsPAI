# power

> 📂 所属分类:04 · 诊断、稳健性与推断 (Diagnostics, Robustness & Inference)

Power and sample size calculations for causal inference and epidemiological
designs.

Supports RCT, DID, RD, IV, cluster RCT, and OLS — plus epidemiological study
designs (two-proportion, log-rank/survival, case-control) — with power
curves, minimum detectable effect (MDE), and sample-size solving.

**12 个公共函数**

### `sp.PowerResult()`

**Container for power analysis results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `design` | `string` | ✓ |  | design parameter (str). |
| `effect_size` | `string` | ✓ |  | effect_size parameter. |
| `n` | `string` | ✓ |  | n parameter. |
| `params` | `object` | ✓ |  | params parameter (Dict[str, Any]). |
| `power_val` | `string` | ✓ |  | power_val parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PowerResult(power_val="value", n="value", effect_size="value", design="value")
print(result.summary())
```

---
### `sp.mde()`

**Compute the Minimum Detectable Effect (MDE) for a given design. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `design` | `string` | ✓ |  | Research design (see :func:`power`). |
| `n` | `integer` |  |  | Sample size. For ``'cluster_rct'`` this is *n_clusters*. |
| `power_target` | `number` |  | `0.8` | Desired power (default 0.80). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mde(design="value")
print(result.summary())
```

---
### `sp.power()`

**Compute statistical power (or solve for sample size) for a causal**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `design` | `string` | ✓ |  | One of ``'rct'``, ``'did'``, ``'rd'``, ``'iv'``, ``'cluster_rct'``, ``'ols'``. |
| `effect_size` | `string` |  |  | Standardised effect size. Pass *None* to solve for MDE (use :func:`mde` for a cleaner interface). |
| `n` | `string` |  |  | Sample size. For cluster_rct this is *n_clusters*. Pass *None* to solve for the minimum n that achieves *power_target*. |
| `power_target` | `number` |  |  | Target power (e.g. 0.80). When *n* is None, the function performs a binary search for the minimum n that achieves this power. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power(design="value")
print(result.summary())
```

---
### `sp.power_case_control()`

**Power (or number of cases) for an unmatched case-control study. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `alternative` | `string (enum)` |  | `'two-sided'` | alternative parameter (str). |
| `exposure_prevalence` | `number` |  | `0.3` | Exposure prevalence among controls (the source-population exposure probability), in (0, 1). |
| `n_cases` | `string` |  |  | Number of cases. ``None`` + ``power_target`` solves for the number of cases. |
| `odds_ratio` | `number` |  | `2.0` | Exposure odds ratio to detect (must be > 0, != 1). |
| `power_target` | `number` |  |  | Desired power; solve for the number of cases when ``n_cases=None``. |
| `ratio` | `number` |  | `1.0` | Number of controls per case. |

> **alternative** options: `'two-sided'`, `'one-sided'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_case_control()
print(result.summary())
```

> 📁 See also: `docs/guides/power_epi.md`

---
### `sp.power_cluster_rct()`

**Power for a Cluster-Randomised Controlled Trial. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `cluster_size` | `number` | ✓ |  | Average number of individuals per cluster. |
| `effect_size` | `string` | ✓ |  | Standardised effect size. |
| `icc` | `number` | ✓ |  | Intra-cluster correlation coefficient. |
| `n_clusters` | `string` | ✓ |  | Total number of clusters (treatment + control). |
| `sigma` | `number` |  | `1.0` | Individual-level outcome standard deviation. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_cluster_rct(n_clusters="value", cluster_size=1.0, effect_size="value", icc=1.0)
print(result.summary())
```

---
### `sp.power_did()`

**Power for Difference-in-Differences.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level (two-sided). |
| `effect_size` | `string` | ✓ |  | Standardised effect size. |
| `n` | `string` | ✓ |  | Total number of units (treated + control). |
| `n_periods` | `integer` | ✓ |  | Total number of time periods. |
| `n_treated_periods` | `integer` | ✓ |  | Number of post-treatment periods. |
| `rho` | `number` |  | `0.5` | First-order autocorrelation of errors (0-1). |
| `sigma` | `number` |  | `1.0` | Error standard deviation. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_did(n="value", effect_size="value", n_periods=1.0, n_treated_periods=1.0)
print(result.summary())
```

---
### `sp.power_iv()`

**Power for Instrumental Variables / 2SLS estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `effect_size` | `string` | ✓ |  | Standardised effect size of the endogenous variable. |
| `first_stage_f` | `number` |  |  | First-stage F-statistic. If provided, power is adjusted for instrument weakness: effective_power ~ power_ols * F / (F + 1). |
| `n` | `string` | ✓ |  | Sample size. |
| `r2_z` | `number` |  |  | R-squared of the first-stage regression. Alternative to *first_stage_f*; if both are given, *first_stage_f* takes precedence. |
| `sigma` | `number` |  | `1.0` | Error standard deviation. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_iv(n="value", effect_size="value")
print(result.summary())
```

---
### `sp.power_logrank()`

**Power (or sample size) for a two-arm log-rank / survival comparison. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `alternative` | `string (enum)` |  | `'two-sided'` | alternative parameter (str). |
| `hazard_ratio` | `number` |  | `0.5` | Hazard ratio between the two arms (must be > 0, != 1). |
| `n` | `string` |  |  | Total sample size. ``None`` + ``power_target`` solves for ``n``. |
| `power_target` | `number` |  |  | Desired power; solve for ``n`` when supplied with ``n=None``. |
| `prob_event` | `number` |  | `1.0` | Probability that a randomly chosen subject is observed to have the event during follow-up (the overall event rate). ``D = n*prob_event``. |
| `ratio` | `number` |  | `1.0` | Allocation ratio ``n2 / n1``. |

> **alternative** options: `'two-sided'`, `'one-sided'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_logrank()
print(result.summary())
```

> 📁 See also: `docs/guides/power_epi.md`

---
### `sp.power_ols()`

**Power for OLS regression (single coefficient of interest). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `effect_size` | `string` | ✓ |  | Standardised effect of the variable of interest. |
| `n` | `string` | ✓ |  | Sample size. |
| `n_covariates` | `integer` |  | `0` | Number of other covariates in the model. |
| `r2_other` | `number` |  | `0.0` | R-squared attributable to other covariates (reduces residual variance and thus improves power). |
| `sigma` | `number` |  | `1.0` | Outcome standard deviation. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_ols(n="value", effect_size="value")
print(result.summary())
```

---
### `sp.power_rct()`

**Power for a two-arm Randomised Controlled Trial. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level (two-sided). |
| `effect_size` | `string` | ✓ |  | Standardised effect size (delta / sigma). |
| `n` | `string` | ✓ |  | Total sample size (treatment + control). |
| `ratio` | `number` |  | `1.0` | Treatment / control allocation ratio (1 = equal allocation). |
| `sigma` | `number` |  | `1.0` | Outcome standard deviation (default 1 for standardised effect). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_rct(n="value", effect_size="value")
print(result.summary())
```

---
### `sp.power_rd()`

**Power for Regression Discontinuity designs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `bandwidth` | `number` |  |  | Bandwidth around the cutoff. If *None*, defaults to 0.5 (half the running-variable range on each side). |
| `density_at_cutoff` | `number` |  | `1.0` | Estimated density of the running variable at the cutoff (default 1.0 for a uniform running variable on [0,1]). |
| `effect_size` | `string` | ✓ |  | Standardised effect size at the cutoff. |
| `kernel` | `string (enum)` |  | `'triangular'` | Kernel used for local weighting. |
| `n` | `string` | ✓ |  | Total sample size in the data. |
| `sigma` | `number` |  | `1.0` | Conditional outcome std dev near the cutoff. |

> **kernel** options: `'triangular'`, `'uniform'`, `'epanechnikov'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_rd(n="value", effect_size="value")
print(result.summary())
```

---
### `sp.power_two_proportions()`

**Power (or sample size) to detect a difference between two proportions. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `alternative` | `string (enum)` |  | `'two-sided'` | Test sidedness. |
| `n` | `string` |  |  | Total sample size (both groups). Pass ``None`` together with ``power_target`` to solve for the smallest ``n`` achieving that power. |
| `p1` | `number` |  | `0.5` | Outcome probabilities in group 1 (reference) and group 2. |
| `p2` | `number` |  | `0.5` | Outcome probabilities in group 1 (reference) and group 2. |
| `power_target` | `number` |  |  | Desired power; when supplied with ``n=None`` the function returns the required total sample size. |
| `ratio` | `number` |  | `1.0` | Allocation ratio ``n2 / n1`` (1.0 = equal allocation). |

> **alternative** options: `'two-sided'`, `'one-sided'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.power_two_proportions()
print(result.summary())
```

> 📁 See also: `docs/guides/power_epi.md`

---
