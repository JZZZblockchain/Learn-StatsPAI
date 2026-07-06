# diagnostics

> 📂 所属分类:04 · 诊断、稳健性与推断 (Diagnostics, Robustness & Inference)

Diagnostics and sensitivity analysis for StatsPAI.

Provides:
- Oster (2019) coefficient stability bounds
- McCrary (2008) density discontinuity test for RD manipulation

**25 个公共函数**

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
### `sp.RosenbaumResult()`

**Result container for :func:`rosenbaum_bounds`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `alternative` | `string` | ✓ |  | alternative parameter (str). |
| `detail` | `string` |  | `None` | Amount of result detail to return. |
| `gamma_critical` | `number` | ✓ |  | gamma_critical parameter (float). |
| `gamma_grid` | `string` | ✓ |  | Grid of gamma values to evaluate. |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_pairs` | `integer` | ✓ |  | Number of pairs. |
> 📝 *配对数。*
| `pvalue_lower` | `string` | ✓ |  | pvalue_lower parameter (np.ndarray). |
| `pvalue_upper` | `string` | ✓ |  | pvalue_upper parameter (np.ndarray). |
| `statistic` | `number` | ✓ |  | statistic parameter (float). |
> 📝 *statistic 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RosenbaumResult(gamma_grid="value", pvalue_lower="value", pvalue_upper="value", gamma_critical=1.0, method="value", alpha=1.0, n_pairs=1.0, statistic=1.0, alternative="value")
print(result.summary())
```

---
### `sp.WeakRobustResult()`

**Container holding the unified weak-IV-robust panel.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `data` | `object` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | endog parameter (str). |
| `h0` | `number` | ✓ |  | h0 parameter (float). |
| `instruments` | `array[string]` | ✓ |  | instruments parameter (List[str]). |
| `n` | `integer` | ✓ |  | n parameter (int). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.WeakRobustResult(data=df, endog="value", instruments=["a", "b"], n=1.0, h0=1.0, alpha=1.0)
print(result.summary())
```

---
### `sp.anderson_rubin_test()`

**Anderson-Rubin (1949) test -- size-correct under weak instruments. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | Endogenous regressor (single). |
| `exog` | `array[string]` |  |  | Included exogenous controls. |
| `h0` | `number` |  | `0` | Null hypothesis value for the endogenous coefficient. |
| `instruments` | `array[string]` | ✓ |  | Excluded instruments. |
| `vcov` | `string (enum)` |  | `'HC1'` | Variance estimator used for the Olea-Pflueger effective F reported alongside AR. |
| `y` | `string` | ✓ |  | Outcome variable. |

> **vcov** options: `'HC0'`, `'HC1'`, `'classic'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.anderson_rubin_test(y="outcome", data=df, endog="value", instruments=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_iv_estimator.md`, `docs/guides/migration-from-r.md`, `docs/guides/sensitivity_analysis.md`

---
### `sp.bias_factor()`

**Confounding bias factor ``B`` (Ding & VanderWeele 2016).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `rr_eu` | `number` | ✓ |  | rr_eu parameter (float). |
| `rr_ud` | `number` | ✓ |  | rr_ud parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bias_factor(rr_eu=1.0, rr_ud=1.0)
print(result.summary())
```

---
### `sp.diagnose()`

**Comprehensive regression diagnostics in one call.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Data used in the regression. |
| `print_results` | `boolean` |  | `True` | Print formatted output. |
| `x` | `array[string]` | ✓ |  | Independent variable names (excluding constant). |
| `y` | `string` | ✓ |  | Dependent variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.diagnose(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.diagnose_result()`

**Method-aware diagnostic battery: auto-selects tests by model type (OLS/DID/RDD/IV/SCM).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | Fitted result from any StatsPAI estimator |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.diagnose_result(result="value")
print(result.summary())
```

---
### `sp.effective_f_test()`

**Olea-Pflueger (2013) robust effective F statistic for weak instruments. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | Endogenous regressor (single endogenous variable). |
| `exog` | `array[string]` |  |  | Included exogenous controls (a constant is added automatically). |
| `instruments` | `array[string]` | ✓ |  | Excluded instruments. |
| `vcov` | `string (enum)` |  | `'HC1'` | Variance estimator for the first-stage residuals: - ``'classic'`` -- homoskedastic; F_eff equals first-stage F. - ``'HC0'`` -- White heteroskedasticity-robust. - ``'HC1'`` -- HC0 with small-sample correction ``n/(n-k)``. |

> **vcov** options: `'HC0'`, `'HC1'`, `'classic'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.effective_f_test(data=df, endog="value", instruments=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_iv_estimator.md`, `docs/guides/migration-from-r.md`

---
### `sp.estat()`

**Unified post-estimation diagnostics dispatcher.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for interpretation strings. |
| `lags` | `integer` |  | `1` | Number of lags for the Breusch-Godfrey test. |
| `powers` | `integer` |  | `3` | Highest power of y-hat for the RESET test. |
| `print_results` | `boolean` |  | `True` | If True, print a formatted table to stdout. |
| `result` | `string` | ✓ |  | A fitted result object with ``params``, ``data_info``, etc. |
| `test` | `string` |  | `'all'` | Name of the diagnostic test. One of ``'hettest'``, ``'white'``, ``'reset'``, ``'ovtest'``, ``'bgodfrey'``, ``'dwatson'``, ``'vif'``, ``'ic'``, ``'linktest'``, ``'normality'``, ``'leverage'``, ``'endogenous'``, ``'overid'``, ``'firststage'``, ``'all'``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.estat(result="value")
print(result.summary())
```

---
### `sp.evalue()`

**Compute the E-value for sensitivity to unmeasured confounding. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level used to build a CI from ``se`` when ``ci`` is not supplied (ratio measures). |
| `ci` | `array[string]` |  |  | Confidence interval on the ``measure`` scale. Takes precedence over ``se`` for ratio measures. |
| `delta` | `number` |  | `1.0` | Contrast size for ``OLS`` (E-value for a ``delta``-unit change in the exposure). |
| `estimate` | `number` | ✓ |  | Point estimate on the scale given by ``measure``: - ``'RR'`` risk ratio, ``'OR'`` odds ratio, ``'HR'`` hazard ratio (all must be > 0); - ``'MD'`` / ``'SMD'`` standardised mean difference; - ``'OLS'`` raw linear-regression coefficient (supply ``sd``); - ``'DIFF'`` / ``'RD'`` risk difference (approximate scalar path; |
| `measure` | `string` |  | `'RR'` | One of ``'RR'``, ``'OR'``, ``'HR'``, ``'MD'``, ``'SMD'``, ``'OLS'``, ``'DIFF'``, ``'RD'``. |
| `rare` | `boolean` |  |  | For ``OR`` / ``HR`` only: whether the rare-outcome approximation applies. ``rare=True`` treats OR/HR ~ RR; ``rare=False`` (the default) uses the exact common-outcome conversion to the RR scale (``sqrt(OR)`` for OR; the Ding-VanderWeele formula for HR). |
| `rare_outcome` | `boolean` |  |  | Deprecated alias for ``rare`` (kept for backwards compatibility). |
| `sd` | `number` |  |  | Outcome standard deviation, required for ``measure='OLS'`` to standardise the coefficient. |
| `se` | `number` |  |  | Standard error of ``estimate``. Required for ``MD`` / ``OLS`` to obtain a confidence-interval E-value; for ratio measures it is used (with ``alpha``) to build a CI when ``ci`` is not given. |
| `true` | `number` |  |  | Reference value the confounding would have to move the estimate to. Defaults to the null: 1 for ratio measures, 0 for difference measures. A non-null ``true`` gives a "non-null" E-value. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.evalue(formula="lwage ~ x1 + x2", estimate=1.0)
print(result.summary())
```

> 📁 See also: `nhefs_whatif.py`, `docs/guides/choosing_matching_estimator.md`, `docs/guides/g_methods_ph.md`

---
### `sp.evalue_from_result()`

**Compute an E-value from a StatsPAI CausalResult object.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `measure` | `string` |  | `'SMD'` | How to interpret ``result.estimate`` (for ATE/ATT on continuous outcomes ``'SMD'`` is appropriate; pass ``'RR'`` / ``'OR'`` / ``'HR'`` for ratio estimates). Passed through to :func:`evalue`. |
| `rare` | `boolean` |  |  | rare parameter (Optional[bool]). |
| `rare_outcome` | `boolean` |  |  | rare_outcome parameter (Optional[bool]). |
| `result` | `string` | ✓ |  | Result from any StatsPAI causal estimator exposing a scalar ``estimate`` (and ideally ``se`` / ``ci``). |
| `true` | `number` |  |  | true parameter (Optional[float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.evalue_from_result(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/robustness_workflow.md`, `docs/guides/sensitivity_analysis.md`

---
### `sp.evalue_rd()`

**Exact E-value for a risk difference from a 2x2 table.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the confidence-limit E-value. |
| `grid` | `number` |  | `0.0001` | Step size of the bias-factor grid search for the CI E-value. |
| `n00` | `number` | ✓ |  | Unexposed cases and unexposed non-cases. |
| `n01` | `number` | ✓ |  | Unexposed cases and unexposed non-cases. |
| `n10` | `number` | ✓ |  | Exposed cases and exposed non-cases. |
| `n11` | `number` | ✓ |  | Exposed cases and exposed non-cases. |
| `true` | `number` |  | `0.0` | Reference risk difference (must be <= the observed RD). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.evalue_rd(n11=1.0, n10=1.0, n01=1.0, n00=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/robustness_workflow.md`

---
### `sp.hausman_test()`

**Hausman test for FE vs RE in panel data. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | Panel data in long format. |
| `id` | `string` | ✓ |  | Unit identifier. |
| `time` | `string` | ✓ |  | Time period identifier. |
| `x` | `array[string]` | ✓ |  | Independent variables (time-varying). |
| `y` | `string` | ✓ |  | Dependent variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.hausman_test(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, id="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`

---
### `sp.het_test()`

**Breusch-Pagan test for heteroskedasticity. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.het_test(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.kitagawa_test()`

**Kitagawa (2015) specification test for the validity of LATE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `instrument` | `string` | ✓ |  | Binary instrument variable (Z). |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications for the p-value. |
| `n_grid` | `integer` |  | `100` | Number of grid points for evaluating the CDF conditions. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `treatment` | `string` | ✓ |  | Endogenous binary treatment variable (D). |
| `y` | `string` | ✓ |  | Outcome variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.kitagawa_test(y="outcome", data=df, treatment="value", instrument="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_iv_estimator.md`, `docs/guides/robustness_workflow.md`

---
### `sp.mccrary_test()`

**McCrary (2008) density test for manipulation of the running variable at the cutoff in regression-discontinuity designs. A significant discontinuity in the density of x at c is direct evidence that units are sorting around the cutoff (e.g. test-taking strategy, income manipulation), invalidating local randomisation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bw` | `number` |  |  | Bandwidth; auto if None |
| `c` | `number` |  | `0.0` | Cutoff value |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_bins` | `integer` |  |  | Histogram bins; auto if None |
| `x` | `string` | ✓ |  | Running variable |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mccrary_test(x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_rd_estimator.md`, `docs/guides/robustness_workflow.md`

---
### `sp.oster_bounds()`

**Oster (2019) sensitivity to selection on unobservables -- computes the bounding coefficient under the assumption that selection on unobservables (proportional to delta x selection on observables) brings the explained variance to r_max. The breakdown delta tells you how strong unobserved selection has to be to overturn your result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_long` | `number` |  |  | beta_long parameter (float). |
| `beta_short` | `number` |  |  | Short-regression coefficient; if None, fit from data |
| `controls` | `array[string]` |  |  | Control-variable column names. |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `delta` | `number` |  | `1.0` | Ratio of unobserved-to-observed selection (1.0 = equally strong) |
| `r2_long` | `number` |  |  | r2_long parameter (float). |
| `r2_short` | `number` |  |  | r2_short parameter (float). |
| `r_max` | `number` |  |  | Hypothetical R^2 from a regression that includes all unobserved confounders; default 1.3*R^2_long |
| `treat` | `string` |  |  | Treatment indicator or first-treatment-period column. |
| `y` | `string` |  |  | Outcome (alternative to passing beta_short/long directly) |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.oster_bounds(y="outcome", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/robustness_workflow.md`, `docs/guides/sensitivity_analysis.md`

---
### `sp.rddensity()`

**CJM (2020) density discontinuity test for RD manipulation. Validation: certified evidence with scoped limitations. Known limitations: Certified native reference-parity evidence covers the default rddensity::rddensity unrestricted triangular-kernel selector and test path on the JSS Lee/RD Senate fixture. Manual side-specific bandwidths follow an explicit user-control convention, not a reference-parity guarantee; backend='r' remains available when direct R package execution is required.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `backend` | `string (enum)` |  | `'native'` | ``"native"`` uses StatsPAI's Python port of the default ``rddensity`` unrestricted triangular-kernel selector/test path. ``"r"`` delegates to ``rddensity::rddensity`` through ``Rscript`` when the R package is installed, matching the reference package's selector and test statistic. |
| `c` | `number` |  | `0` | RD cutoff. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `h` | `array[string]` |  |  | Bandwidth. A scalar applies the same bandwidth on both sides; a length-2 sequence is interpreted as ``(h_left, h_right)``. |
| `p` | `integer` |  | `2` | Polynomial order for density estimation. |
| `x` | `string` | ✓ |  | Running variable. |

> **backend** options: `'native'`, `'r'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rddensity(x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_rd_estimator.md`, `docs/guides/migration-from-r.md`, `docs/guides/robustness_workflow.md`

---
### `sp.reset_test()`

**Ramsey RESET test for functional form misspecification. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `powers` | `integer` |  | `3` | Include y2, y3, ..., y^powers in the auxiliary regression. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.reset_test(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.rosenbaum_bounds()`

**Compute Rosenbaum bounds on a paired observational study.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level used to report ``gamma_critical``. |
| `alternative` | `string (enum)` |  | `'greater'` | Direction of the alternative hypothesis for the treatment effect. |
| `control` | `array[string]` |  |  | Outcome in the treated / control unit of each matched pair (same length). Ignored if ``data`` is provided. |
| `data` | `string` |  |  | Long-format data. Must contain exactly two rows per ``pair_id``, one with ``treat=1`` and one with ``treat=0``. |
| `gamma_grid` | `array[string]` |  |  | Gamma values (>= 1) over which to compute bounding p-values. |
| `method` | `string (enum)` |  | `'wilcoxon'` | Wilcoxon signed-rank bound (continuous) or binomial sign test (robust / binary). |
| `pair_id` | `string` |  |  | pair_id parameter (Optional[str]). |
| `treat` | `string` |  |  | Treatment indicator or first-treatment-period column. |
| `treated` | `array[string]` |  |  | Outcome in the treated / control unit of each matched pair (same length). Ignored if ``data`` is provided. |
| `y` | `string` |  |  | Outcome variable column name or outcome array. |

> **alternative** options: `'greater'`, `'less'`, `'two-sided'`

> **method** options: `'wilcoxon'`, `'sign'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rosenbaum_bounds(y="outcome", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/sensitivity_analysis.md`

---
### `sp.rosenbaum_gamma()`

**Compute Rosenbaum bounds on a paired observational study.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level used to report ``gamma_critical``. |
| `alternative` | `string (enum)` |  | `'greater'` | Direction of the alternative hypothesis for the treatment effect. |
| `control` | `array[string]` |  |  | Outcome in the treated / control unit of each matched pair (same length). Ignored if ``data`` is provided. |
| `data` | `string` |  |  | Long-format data. Must contain exactly two rows per ``pair_id``, one with ``treat=1`` and one with ``treat=0``. |
| `gamma_grid` | `array[string]` |  |  | Gamma values (>= 1) over which to compute bounding p-values. |
| `method` | `string (enum)` |  | `'wilcoxon'` | Wilcoxon signed-rank bound (continuous) or binomial sign test (robust / binary). |
| `pair_id` | `string` |  |  | pair_id parameter (Optional[str]). |
| `treat` | `string` |  |  | Treatment indicator or first-treatment-period column. |
| `treated` | `array[string]` |  |  | Outcome in the treated / control unit of each matched pair (same length). Ignored if ``data`` is provided. |
| `y` | `string` |  |  | Outcome variable column name or outcome array. |

> **alternative** options: `'greater'`, `'less'`, `'two-sided'`

> **method** options: `'wilcoxon'`, `'sign'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rosenbaum_gamma(y="outcome", data=df)
print(result.summary())
```

---
### `sp.sensemakr()`

**Sensitivity analysis for omitted variable bias (Cinelli & Hazlett 2020). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `benchmark` | `array[string]` |  |  | Covariates to benchmark confounding strength against |
| `controls` | `array[string]` | ✓ |  | Observed control variables |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `treat` | `string` | ✓ |  | Treatment column of interest |
| `y` | `string` | ✓ |  | Outcome column |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sensemakr(y="outcome", data=df, treat="value", controls=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/robustness_workflow.md`, `docs/guides/sensitivity_analysis.md`

---
### `sp.tF_critical_value()`

**Lee-McCrary-Moreira-Porter (2022, AER) tF adjusted critical value. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. Only ``0.05`` is implemented (the only level for which LMMP publish a complete table). |
| `first_stage_F` | `number` | ✓ |  | Observed first-stage F statistic (or Olea-Pflueger F_eff). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.tF_critical_value(first_stage_F=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_iv_estimator.md`, `docs/guides/migration-from-r.md`

---
### `sp.vif()`

**Variance Inflation Factors for multicollinearity detection.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `x` | `array[string]` | ✓ |  | Independent variables. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.vif(x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.weakrobust()`

**Stata-style unified weak-instrument-robust diagnostic panel.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the robust confidence sets. |
| `clr_simulations` | `integer` |  | `20000` | Monte-Carlo draws for the CLR null distribution. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `string` | ✓ |  | Outcome and single endogenous regressor (column names in ``data``). |
| `exog` | `array[string]` |  |  | Included exogenous controls. An intercept is always added. |
| `grid_size` | `integer` |  | `401` | Grid resolution used by AR/CLR/K confidence-set inversion. |
| `h0` | `number` |  | `0.0` | Null value for the endogenous coefficient. All under-H0 tests (AR, CLR, K) are evaluated at ``beta = h0``. |
| `include_clr` | `boolean` |  | `True` | Also run the CLR test and invert it for a CLR confidence set. |
| `include_k` | `boolean` |  | `True` | Also run the Kleibergen K score test and K confidence set. |
| `instruments` | `array[string]` | ✓ |  | Excluded instruments. |
| `random_state` | `integer` |  |  | Random seed or RandomState for reproducible stochastic steps. |
| `vcov` | `string (enum)` |  | `'HC1'` | Used by the Olea-Pflueger effective F. |
| `y` | `string` | ✓ |  | Outcome and single endogenous regressor (column names in ``data``). |

> **vcov** options: `'HC0'`, `'HC1'`, `'classic'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.weakrobust(y="outcome", data=df, endog="value", instruments=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/sensitivity_analysis.md`

---
