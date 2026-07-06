# decomposition

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Decomposition Analysis module for StatsPAI.

Decomposition toolkit covering mean, distributional, inequality,
demographic, and causal decomposition methods under a
unified API: ``sp.decompose(method=...)``.

Methods (19 in total — Yu-Elwert added in v1.15)
-----------------------------------------------

**Mean decomposition**
- ``oaxaca`` — Blinder-Oaxaca (Blinder 1973; Oaxaca 1973) with 5
  reference-coefficient choices (A, B, pooled/Neumark, Cotton, Reimers)
- ``gelbach`` — Gelbach (2016) sequential orthogonal decomposition of
  omitted-variable bias
- ``fairlie`` — Fairlie (2005) nonlinear decomposition for logit/probit
- ``bauer_sinning`` / ``yun_nonlinear`` — Bauer-Sinning (2008) + Yun
  (2005) detailed nonlinear decomposition

**Distributional decomposition**
- ``rif`` — Recentered Influence Function regression + OB decomposition
  (Firpo-Fortin-Lemieux 2009)
- ``ffl`` — Firpo-Fortin-Lemieux (2018) two-step detailed decomposition
- ``dfl`` — DiNardo-Fortin-Lemieux (1996) reweighting
- ``machado_mata`` — Machado-Mata (2005) quantile decomposition
- ``melly`` — Melly (2005) analytical quantile decomposition
- ``cfm`` — Chernozhukov-Fernández-Val-Melly (2013) counterfactual
  distributions via distribution regression

**Inequality decomposition**
- ``subgroup`` — between/within decomposition (Theil T/L, GE, Gini,
  Atkinson, CV²)
- ``shapley_inequality`` — Shorrocks-Shapley (2013) allocation of
  inequality to covariates
- ``gini_source`` — Lerman-Yitzhaki (1985) Gini source decomposition

**Demographic / standardisation**
- ``kitagawa`` — Kitagawa (1955) two-factor rate decomposition
- ``das_gupta`` — Das Gupta (1993) multi-factor decomposition

**Causal decomposition**
- ``gap_closing`` — Lundberg (2022) gap-closing estimator
  (regression / IPW / AIPW)
- ``mediation`` — VanderWeele (2014) natural direct/indirect effects
- ``disparity`` / ``causal_jvw`` — Jackson-VanderWeele (2018) causal
  disparity decomposition
- ``yu_elwert`` — Yu & Elwert (2025) nonparametric causal decomposition
  of group disparities into baseline, prevalence, effect, and selection
  components (efficient-influence-function-based; ML-friendly)

Unified Entry
-------------
``sp.decompose(method=..., **kwargs)`` dispatches to any of the above.

Polish (v1.15)
--------------
Every result class now inherits ``DecompResultMixin``, exposing a
common ``.confint()``, ``.cite()``, ``.to_dict()``, ``.to_json()``,
``.to_excel()``, and ``.to_word()`` surface in addition to each
method's bespoke ``.summary()`` / ``.plot()`` / ``.to_latex()``.
Plots share a common palette and minimalist style via
:mod:`statspai.decomposition.plots` (forest plots, mediation forest,
Yu-Elwert mechanism plot, RIF heatmap, …).

**32 个公共函数**

### `sp.GelbachResult()`

**Result container for Gelbach (2016) decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `base_coef` | `number` | ✓ |  | base_coef parameter (float). |
| `base_var` | `string` | ✓ |  | base_var parameter (str). |
| `decomposition` | `string` | ✓ |  | decomposition parameter (pd.DataFrame). |
| `full_coef` | `number` | ✓ |  | full_coef parameter (float). |
| `total_change` | `number` | ✓ |  | total_change parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GelbachResult(total_change=1.0, decomposition="value", base_coef=1.0, full_coef=1.0, base_var="value")
print(result.summary())
```

---
### `sp.KitagawaResult()`

**Result of the Kitagawa (2015) LATE validity test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `first_stage` | `number` | ✓ |  | first_stage parameter (float). |
> 📝 *first_stage 参数（浮点数）。*
| `max_violation_treated` | `number` | ✓ |  | max_violation_treated parameter (float). |
> 📝 *max_violation_treated 参数（浮点数）。*
| `max_violation_untreated` | `number` | ✓ |  | max_violation_untreated parameter (float). |
> 📝 *max_violation_untreated 参数（浮点数）。*
| `n_boot` | `integer` | ✓ |  | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `statistic` | `number` | ✓ |  | statistic parameter (float). |
> 📝 *statistic 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.KitagawaResult(statistic=1.0, p_value=1.0, first_stage=1.0, n_boot=1.0, n_obs=1.0, max_violation_treated=1.0, max_violation_untreated=1.0)
print(result.summary())
```

---
### `sp.OaxacaResult()`

**Result container for Oaxaca-Blinder decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `detailed` | `string` | ✓ |  | detailed parameter (pd.DataFrame). |
| `group_stats` | `object` | ✓ |  | group_stats parameter (Dict[str, Any]). |
| `overall` | `object` | ✓ |  | overall parameter (Dict[str, float]). |
| `reference` | `integer` | ✓ |  | reference parameter (Union[str, int]). |
| `var_names` | `array[string]` | ✓ |  | var_names parameter (List[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.OaxacaResult(detailed="value", reference=1.0, var_names=["a", "b"])
print(result.summary())
```

---
### `sp.YuElwertResult()`

**Yu-Elwert (2025) causal decomposition of a group disparity.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `baseline` | `number` |  | `0.0` | baseline parameter (float). |
| `ci` | `array[string]` |  |  | ci parameter (Optional[Dict[str, Tuple[float, float]]]). |
| `detailed` | `string` |  | `None` | detailed parameter (pd.DataFrame). |
| `disparity` | `number` |  | `0.0` | disparity parameter (float). |
| `effect` | `number` |  | `0.0` | effect parameter (float). |
| `method` | `string` |  | `'plugin'` | Estimator or algorithm variant to use. |
| `nuisance` | `object` |  | `None` | nuisance parameter (Dict[str, Any]). |
| `prevalence` | `number` |  | `0.0` | prevalence parameter (float). |
| `se` | `object` |  |  | se parameter (Optional[Dict[str, float]]). |
| `selection` | `number` |  | `0.0` | selection parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.YuElwertResult()
print(result.summary())
```

---
### `sp.available_methods()`

**Return list of all registered decomposition method names.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.available_methods()
print(result.summary())
```

---
### `sp.bauer_sinning()`

**Bauer-Sinning (2008) nonlinear Oaxaca-Blinder decomposition with**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `model` | `string (enum)` |  | `'logit'` | Model variant or parameterisation to fit. |
| `reference` | `integer (enum)` |  | `0` | reference parameter (int). |
| `variant` | `string` |  | `'yun'` | variant parameter (str). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **model** options: `'logit'`, `'probit'`

> **reference** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bauer_sinning(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.cfm_decompose()`

**Chernozhukov-Fernandez-Val-Melly (2013) counterfactual decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `ks_test` | `boolean` |  | `True` | ks_test parameter (bool). |
| `n_thresh` | `integer` |  | `40` | Number of thresh. |
| `reference` | `integer (enum)` |  | `0` | Same convention as ``machado_mata`` / ``melly_decompose``: ``reference=0`` builds the counterfactual from A's distribution regression coefficients applied to B's X (F_{Y<0\|1>}), opposite to the reweighting convention in ``dfl_decompose``. |
| `tau_grid` | `array[string]` |  |  | Grid of tau values to evaluate. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **reference** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cfm_decompose(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.chilean_households()`

**Chilean-style household income with urban/rural gap.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n` | `integer` |  | `2500` | n parameter (int). |
| `seed` | `integer` |  | `42` | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.chilean_households()
print(result.summary())
```

---
### `sp.cps_wage()`

**CPS-style wage data with a gender gap.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n` | `integer` |  | `3000` | n parameter (int). |
| `seed` | `integer` |  | `42` | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cps_wage()
print(result.summary())
```

> 📁 See also: `docs/guides/psm_did.md`

---
### `sp.das_gupta()`

**Das Gupta (1993) multi-factor decomposition. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data_a` | `string` | ✓ |  | Each row contributes the factor value. The aggregate for each group is computed as Sigma_i _f factor_{f,i}. For single-row DataFrames (one population, no stratification) the aggregate is simply _f factor_f. |
| `data_b` | `string` | ✓ |  | Each row contributes the factor value. The aggregate for each group is computed as Sigma_i _f factor_{f,i}. For single-row DataFrames (one population, no stratification) the aggregate is simply _f factor_f. |
| `factor_names` | `array[string]` | ✓ |  | factor_names parameter (Sequence[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.das_gupta(data_a="value", data_b="value", factor_names=["a", "b"])
print(result.summary())
```

---
### `sp.decompose()`

**Unified entry point for all decomposition methods. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | `string` | ✓ |  | One of the methods listed in ``available_methods()``. Aliases are supported (e.g. 'mm' -> 'machado_mata'). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.decompose(method="value")
print(result.summary())
```

> 📁 See also: `docs/guides/decomposition_family.md`

---
### `sp.dfl_decompose()`

**DFL (1996) reweighting decomposition at a chosen distributional statistic. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `inference` | `string (enum)` |  | `'analytical'` | inference parameter (str). |
| `n_boot` | `integer` |  | `299` | Number of bootstrap replications. |
| `quantile_grid` | `array[string]` |  |  | If provided, also compute quantile-process decomposition on this grid. |
| `reference` | `integer (enum)` |  | `0` | - 0: reweight Group B to look like A's X (default). The counterfactual is F_{Y<1\|0>} -- A's X distribution with B's outcome structure. - 1: reweight Group A to look like B's X. The counterfactual is F_{Y<0\|1>} -- B's X distribution with A's outcome structure. .. warning:: ``reference`` has different economic semantics across method families. In DFL, ``reference=0`` yields cf = *A's X, B's beta* (reweighting approach). In ``machado_mata`` / ``melly`` / ``cfm``, ``reference=0`` yields cf = *A's beta, B's X* (coefficient-substitution approach). These are **opposite** counterfactual constructions. Within each method labels are internally consistent (DFL structure = A - cf; MM composition = A - cf). When comparing estimates across methods, read the per-method docstrings carefully. |
| `seed` | `integer` |  | `12345` | Random seed for reproducible stochastic steps. |
| `stat` | `string (enum)` |  | `'mean'` | stat parameter (str). |
| `tau` | `number` |  | `0.5` | Quantile level or target treatment-effect index. |
| `trim` | `number` |  | `0.001` | trim parameter (float). |
| `weights` | `string` |  |  | Observation weights. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **inference** options: `'bootstrap'`, `'analytical'`

> **reference** options: `'0'`, `'1'`

> **stat** options: `'mean'`, `'variance'`, `'std'`, `'quantile'`, `'iqr'`, `'gini'`, `'log_var'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dfl_decompose(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.disparity_decompose()`

**Jackson & VanderWeele (2018) causal disparity decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `mediator` | `string` | ✓ |  | mediator parameter (str). |
| `target_level` | `number` |  |  | Value at which to fix mediator for the "initial" counterfactual. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.disparity_decompose(y="outcome", data=df, group="value", mediator="value")
print(result.summary())
```

---
### `sp.disparity_panel()`

**Synthetic disparity panel with treatment, mediator, outcome.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n` | `integer` |  | `3000` | n parameter (int). |
| `seed` | `integer` |  | `42` | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.disparity_panel()
print(result.summary())
```

---
### `sp.fairlie()`

**Fairlie (2005) nonlinear decomposition for binary outcomes.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `model` | `string (enum)` |  | `'logit'` | Model variant or parameterisation to fit. |
| `n_sim` | `integer` |  | `500` | Number of sim. |
| `reference` | `integer (enum)` |  | `0` | reference parameter (int). |
| `seed` | `integer` |  | `12345` | Random seed for reproducible stochastic steps. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string (enum)` | ✓ |  | Outcome variable column name or outcome array. |

> **model** options: `'logit'`, `'probit'`

> **reference** options: `'0'`, `'1'`

> **y** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.fairlie(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.ffl_decompose()`

**Firpo-Fortin-Lemieux two-step detailed distributional decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string (enum)` | ✓ |  | Group or cohort identifier. |
| `inference` | `string (enum)` |  | `'analytical'` | inference parameter (str). |
| `n_boot` | `integer` |  | `299` | Number of bootstrap replications. |
| `reference` | `integer (enum)` |  | `0` | 0: B reweighted to look like A's X (composition = effect of A's X on B's outcomes relative to observed B) |
| `seed` | `integer` |  | `12345` | Random seed for reproducible stochastic steps. |
| `stat` | `string` |  | `'quantile'` | 'log_var', 'theil_t', 'theil_l', 'atkinson'} |
| `tau` | `number` |  | `0.5` | Quantile level or target treatment-effect index. |
| `trim` | `number` |  | `0.001` | trim parameter (float). |
| `weights` | `string` |  |  | Observation weights. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **group** options: `'0'`, `'1'`

> **inference** options: `'analytical'`, `'bootstrap'`

> **reference** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ffl_decompose(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.gap_closing()`

**Lundberg (2021) gap-closing estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `inference` | `string (enum)` |  | `'analytical'` | inference parameter (str). |
| `method` | `string (enum)` |  | `'aipw'` | AIPW is doubly robust (recommended). |
| `n_boot` | `integer` |  | `299` | Number of bootstrap replications. |
| `seed` | `integer` |  | `12345` | Random seed for reproducible stochastic steps. |
| `target_dist` | `integer (enum)` |  | `1` | - 1: shift Group A's covariate distribution to match Group B's - 0: shift Group B's to match Group A's |
| `trim` | `number` |  | `0.001` | trim parameter (float). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **inference** options: `'analytical'`, `'bootstrap'`

> **method** options: `'regression'`, `'ipw'`, `'aipw'`

> **target_dist** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.gap_closing(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.gelbach()`

**Gelbach (2016) decomposition of omitted variable bias. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `added_x` | `array[string]` | ✓ |  | Variables added to obtain the full (long) specification. |
| `alpha` | `number` |  | `0.05` | Significance level. |
| `base_x` | `array[string]` | ✓ |  | Variables in the base (short) specification. |
| `data` | `string` | ✓ |  | Input dataset. |
| `var_of_interest` | `string` |  |  | Which base variable's coefficient change to decompose. Defaults to the first element of ``base_x``. |
| `y` | `string` | ✓ |  | Outcome variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.gelbach(y="outcome", data=df, base_x=["a", "b"], added_x=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
### `sp.inequality_index()`

**Compute a single inequality index. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  |  | Significance level for confidence intervals and tests. |
| `eps` | `number` |  | `1.0` | eps parameter (float). |
| `index` | `string` |  | `'theil_t'` | atkinson, gini, cv2 |
| `weights` | `string` |  |  | Observation weights. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.inequality_index(y="outcome")
print(result.summary())
```

---
### `sp.kitagawa_decompose()`

**Kitagawa (1955) two-factor rate decomposition. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `by` | `array[string]` | ✓ |  | Category variable(s) defining cells. |
| `data` | `string` | ✓ |  | Tidy data. Either individual-level (aggregated internally) or pre-aggregated cell-level with columns: `group`, `by`, `rate`, optional `weights` (population size in each cell). |
| `group` | `string` | ✓ |  | Binary group indicator. |
| `normalize` | `string (enum)` |  | `'symmetric'` | - 'a': rate effect evaluated at A's composition - 'b': rate effect evaluated at B's composition - 'symmetric': average (default) |
| `rate` | `string` | ✓ |  | Column holding the category-specific rate (or 0/1 outcome at the individual level). |
| `weights` | `string` |  |  | Cell population weights. If None, each row treated as individual-level data (weight = 1). |

> **normalize** options: `'symmetric'`, `'a'`, `'b'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.kitagawa_decompose(data=df, rate="value", group="value", by=["a", "b"])
print(result.summary())
```

---
### `sp.machado_mata()`

**Machado-Mata (2005) quantile decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `inference` | `string` |  | `'none'` | inference parameter (str). |
| `n_boot` | `integer` |  | `199` | Number of bootstrap replications. |
| `n_sim` | `integer` |  | `500` | Number of sim. |
| `n_tau_qr` | `integer` |  | `99` | Number of tau qr. |
| `reference` | `integer (enum)` |  | `0` | 0: use Group A's coefficients with Group B's X. The counterfactual is F_{Y<0\|1>} -- A's beta on B's X. 1: use Group B's coefficients with Group A's X. .. warning:: Opposite convention to ``dfl_decompose``. In DFL, ``reference=0`` means *A's X, B's beta* (reweighting). Here, ``reference=0`` means *A's beta, B's X* (coefficient swap). See ``dfl_decompose`` docstring for the full convention map. |
| `seed` | `integer` |  | `12345` | Random seed for reproducible stochastic steps. |
| `tau_grid` | `array[string]` |  |  | tau grid for reporting (default: deciles 0.1..0.9) |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **reference** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.machado_mata(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.mediation_decompose()`

**Linear nested-models mediation decomposition (VanderWeele 2014 Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `inference` | `string (enum)` |  | `'analytical'` | inference parameter (str). |
| `mediator` | `string` | ✓ |  | mediator parameter (str). |
| `n_boot` | `integer` |  | `299` | Number of bootstrap replications. |
| `seed` | `integer` |  | `12345` | Random seed for reproducible stochastic steps. |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **inference** options: `'analytical'`, `'bootstrap'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mediation_decompose(y="outcome", data=df, treatment="value", mediator="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
### `sp.melly_decompose()`

**Melly (2005) quantile decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `n_tau_qr` | `integer` |  | `99` | Number of tau qr. |
| `reference` | `integer (enum)` |  | `0` | Same convention as ``machado_mata``: ``reference=0`` uses A's beta on B's X (coefficient-swap counterfactual F_{Y<0\|1>}), opposite to ``dfl_decompose`` whose ``reference=0`` uses A's X with B's beta. |
| `tau_grid` | `array[string]` |  |  | Grid of tau values to evaluate. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **reference** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.melly_decompose(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.mincer_wage_panel()`

**Two-period Mincer wage distribution with a structural shift.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n` | `integer` |  | `5000` | n parameter (int). |
| `seed` | `integer` |  | `42` | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mincer_wage_panel()
print(result.summary())
```

---
### `sp.oaxaca()`

**Oaxaca-Blinder decomposition of mean outcome gaps. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for p-values. |
| `data` | `string` | ✓ |  | Input dataset. |
| `detail` | `boolean` |  | `True` | If True, compute variable-level contributions to the explained component. |
| `group` | `string` | ✓ |  | Binary group indicator (0 = Group A, 1 = Group B). |
| `reference` | `integer (enum)` |  | `0` | Reference coefficient vector beta*: - ``0`` -- Group A coefficients (beta_A). The "explained" part uses Group A's returns as the benchmark. - ``1`` -- Group B coefficients (beta_B). - ``'pooled'`` -- Pooled OLS (Neumark 1988). - ``'cotton'`` -- Sample-size weighted average (Cotton 1988). - ``'reimers'`` -- Equal-weighted average (Reimers 1983). |
| `x` | `array[string]` | ✓ |  | Covariate names. |
| `y` | `string` | ✓ |  | Outcome variable name. |

> **reference** options: `'pooled'`, `'cotton'`, `'reimers'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.oaxaca(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
### `sp.rif_decomposition()`

**RIF Oaxaca-Blinder decomposition (FFL 2009, Section 5). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `group` | `string` | ✓ |  | Binary (0/1) group indicator column. |
| `quantile_convention` | `string (enum)` |  | `'statspai'` | Quantile RIF convention for ``statistic="quantile"``. Use ``"dineq"`` for R ``dineq::rif`` parity. |
| `reference` | `integer` |  | `0` | Which group's coefficients to use as the reference (0 or 1). |
| `statistic` | `string` |  | `'quantile'` | statistic parameter (StatisticKind). |
| `tau` | `number` |  | `0.5` | Quantile level or target treatment-effect index. |

> **quantile_convention** options: `'statspai'`, `'dineq'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rif_decomposition(formula="lwage ~ x1 + x2", data=df, group="value")
print(result.summary())
```

---
### `sp.rifreg()`

**RIF regression (Firpo, Fortin & Lemieux 2009).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | ``"y ~ x1 + x2"`` style. |
| `quantile_convention` | `string (enum)` |  | `'statspai'` | Quantile RIF convention for ``statistic="quantile"``. |
| `statistic` | `string (enum)` |  | `'quantile'` | statistic parameter (StatisticKind). |
| `tau` | `number` |  | `0.5` | Quantile level (default 0.5 = median UQPE). |

> **quantile_convention** options: `'statspai'`, `'dineq'`

> **statistic** options: `'quantile'`, `'variance'`, `'gini'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rifreg(data=df)
print(result.summary())
```

---
### `sp.shapley_inequality()`

**Shorrocks-Shapley decomposition of an inequality index across**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `index` | `string` |  | `'theil_t'` | index parameter (str). |
| `weights` | `string` |  |  | Observation weights. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.shapley_inequality(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.source_decompose()`

**Lerman-Yitzhaki (1985) Gini source decomposition. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `sources` | `array[string]` | ✓ |  | sources parameter (Sequence[str]). |
| `weights` | `string` |  |  | Observation weights. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.source_decompose(data=df, sources=["a", "b"])
print(result.summary())
```

---
### `sp.subgroup_decompose()`

**Subgroup decomposition (between / within) of an inequality index. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  |  | Significance level for confidence intervals and tests. |
| `by` | `string` | ✓ |  | by parameter (str). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `eps` | `number` |  | `1.0` | eps parameter (float). |
| `index` | `string` |  | `'theil_t'` | index parameter (str). |
| `weights` | `string` |  |  | Observation weights. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.subgroup_decompose(y="outcome", data=df, by="value")
print(result.summary())
```

---
### `sp.yu_elwert_decompose()`

**Nonparametric causal decomposition of a group disparity.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Two-sided coverage level. |
| `cluster` | `string` |  |  | Column name to use for cluster bootstrap. |
| `data` | `string` | ✓ |  | Long-format panel with one row per observation. |
| `group` | `string` | ✓ |  | Binary group indicator (0/1) -- ``1`` = advantaged / index group. |
| `inference` | `string` |  | `'bootstrap'` | ``"bootstrap"`` returns SEs and percentile CIs from the non-parametric (cluster-aware) bootstrap. ``"none"`` skips inference. |
| `method` | `string (enum)` |  | `'plugin'` | ``"plugin"`` uses within-cell OLS for outcomes and within-group logit for the propensity and computes plug-in expectations (Yu-Elwert 2025, Section 4.1). ``"efficient"`` augments each moment with the doubly-robust correction term -- recommended when nuisance functions might be misspecified. |
| `n_boot` | `integer` |  | `499` | Number of bootstrap replications. |
| `seed` | `integer` |  | `12345` | Random seed for reproducible stochastic steps. |
| `treatment` | `string` | ✓ |  | Binary treatment indicator (0/1). |
| `trim` | `number` |  | `0.005` | Lower/upper clip for fitted propensities (only used in ``method="efficient"``). |
| `x` | `array[string]` | ✓ |  | Adjustment covariates (used to identify within-group CATEs). |
| `y` | `string` | ✓ |  | Name of the (continuous) outcome column. |

> **method** options: `'plugin'`, `'efficient'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.yu_elwert_decompose(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, treatment="value", group="value")
print(result.summary())
```

> 📁 See also: `docs/guides/decomposition_family.md`

---
### `sp.yun_nonlinear()`

**Bauer-Sinning (2008) nonlinear Oaxaca-Blinder decomposition with**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `model` | `string (enum)` |  | `'logit'` | Model variant or parameterisation to fit. |
| `reference` | `integer (enum)` |  | `0` | reference parameter (int). |
| `variant` | `string` |  | `'yun'` | variant parameter (str). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **model** options: `'logit'`, `'probit'`

> **reference** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.yun_nonlinear(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, group="value")
print(result.summary())
```

---
