# principal_strat

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Principal Stratification (Frangakis & Rubin 2002).

Principal strata classify units by the joint potential values of a
post-treatment variable (e.g. compliance type or survival status).
Methods provided:

* ``principal_strat(..., method='monotonicity')`` — sharp bounds on
  complier/always-taker/never-taker ATEs under monotonicity (Angrist,
  Imbens & Rubin 1996; Abadie 2002) + point-identified LATE.
* ``principal_strat(..., method='principal_score')`` — covariate-
  based weighting estimator (Jo & Stuart 2009; Ding & Lu 2017) that
  point-identifies stratum-specific effects when principal ignorability
  holds.

Also ships :func:`survivor_average_causal_effect` (SACE bounds —
Zhang & Rubin 2003) as a specialized entry point for the classical
truncation-by-death problem.

**3 个公共函数**

### `sp.PrincipalStratResult()`

**Principal stratification result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `bounds` | `string` | ✓ |  | bounds parameter (Optional[pandas.DataFrame]). |
| `effects` | `string` | ✓ |  | effects parameter (DataFrame). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` | ✓ |  | model_info parameter (Dict[str, Any]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `strata_proportions` | `object` | ✓ |  | strata_proportions parameter (Dict[str, float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PrincipalStratResult(method="value", effects="value", bounds="value", n_obs=1.0, alpha=1.0)
print(result.summary())
```

---
### `sp.principal_strat()`

**Principal Stratification (Frangakis & Rubin 2002). 'monotonicity' method identifies the complier PCE (= LATE) and reports Zhang-Rubin sharp bounds on the always-survivor SACE. 'principal_score' uses Ding-Lu covariate weighting to point-identify stratum-specific effects under principal ignorability. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact). Known limitations: Always-survivor SACE under encouragement design (Mealli & Pacini 2013, partial identification) is not yet implemented; only AIR / Wald LATE point estimates (tau_Y on outcome, tau_S on the post-treatment stratum) are reported when an instrument is supplied.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | CI level (e.g. 0.05 for 95% CIs) |
| `covariates` | `array[string]` |  |  | Baseline covariates (required for principal_score) |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `instrument` | `string` |  |  | Binary instrument column. When supplied, switches to the AIR / Wald LATE estimator: under random Z, monotonicity, and exclusion, reports two LATEs among Z-compliers -- tau_Y for the effect of the treatment on the outcome, and tau_S for the effect on the post-treatment stratum variable. method= is ignored on this path. |
| `method` | `string (enum)` |  | `'monotonicity'` | Identification strategy |
| `n_boot` | `integer` |  | `500` | Bootstrap replications |
| `seed` | `integer` |  |  | Random seed for reproducible bootstrap draws |
| `strata` | `string` | ✓ |  | Binary post-treatment variable |
| `treat` | `string` | ✓ |  | Binary treatment |
| `y` | `string` | ✓ |  | Outcome |

> **method** options: `'monotonicity'`, `'principal_score'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.principal_strat(y="outcome", data=df, treat="value", strata="value")
print(result.summary())
```

---
### `sp.survivor_average_causal_effect()`

**Zhang-Rubin (2003) sharp bounds on the Survivor Average Causal Effect. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `survival` | `string` | ✓ |  | survival parameter (str). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.survivor_average_causal_effect(y="outcome", data=df, treat="value", survival="value")
print(result.summary())
```

---
