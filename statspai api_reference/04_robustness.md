# robustness

> 📂 所属分类:04 · 诊断、稳健性与推断 (Diagnostics, Robustness & Inference)

Robustness analysis tools.

- ``spec_curve``: Specification Curve Analysis (Simonsohn et al. 2020)
- ``robustness_report``: Automated battery of robustness checks
- ``subgroup_analysis``: Subgroup heterogeneity analysis with forest plot

**12 个公共函数**

### `sp.FrontierSensitivityResult()`

**Container for frontier sensitivity analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `breakpoint` | `number` | ✓ |  | breakpoint parameter (Optional[float]). |
| `curve` | `string` | ✓ |  | curve parameter (pd.DataFrame). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `interpretation` | `string` | ✓ |  | interpretation parameter (str). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FrontierSensitivityResult(method="value", estimate=1.0, se=1.0, curve="value", breakpoint=1.0, interpretation="value")
print(result.summary())
```

---
### `sp.RobustnessResult()`

**Container for robustness report results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `baseline_estimate` | `number` | ✓ |  | baseline_estimate parameter (float). |
| `baseline_se` | `number` | ✓ |  | baseline_se parameter (float). |
| `n_checks` | `integer` | ✓ |  | Number of checks. |
| `results_df` | `string` | ✓ |  | results_df parameter (pd.DataFrame). |
| `x` | `string` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RobustnessResult(x=["treatment", "covariate1", "covariate2"], results_df="value", baseline_estimate=1.0, baseline_se=1.0, n_checks=1.0)
print(result.summary())
```

---
### `sp.SensitivityDashboard()`

**Multi-dimensional sensitivity analysis results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `baseline` | `object` | ✓ |  | baseline parameter (Dict[str, Any]). |
| `dimensions` | `array[string]` | ✓ |  | dimensions parameter (List[Dict[str, Any]]). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `overall_stability` | `string` | ✓ |  | overall_stability parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SensitivityDashboard(dimensions=["a", "b"], overall_stability="value", method="value")
print(result.summary())
```

---
### `sp.SpecCurveResult()`

**Holds all specification curve outputs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `choice_dims` | `array[string]` | ✓ |  | choice_dims parameter (List[str]). |
| `median_estimate` | `number` | ✓ |  | median_estimate parameter (float). |
| `n_specs` | `integer` | ✓ |  | Number of specs. |
| `results_df` | `string` | ✓ |  | results_df parameter (pd.DataFrame). |
| `share_positive` | `number` | ✓ |  | share_positive parameter (float). |
| `share_significant` | `number` | ✓ |  | share_significant parameter (float). |
| `x` | `string` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SpecCurveResult(y="outcome", x=["treatment", "covariate1", "covariate2"], results_df="value", n_specs=1.0, median_estimate=1.0, share_significant=1.0, share_positive=1.0, choice_dims=["a", "b"])
print(result.summary())
```

---
### `sp.SubgroupResult()`

**Container for subgroup heterogeneity analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `het_tests` | `object` | ✓ |  | het_tests parameter (Dict[str, Dict[str, float]]). |
| `overall_estimate` | `number` | ✓ |  | overall_estimate parameter (float). |
| `overall_se` | `number` | ✓ |  | overall_se parameter (float). |
| `results_df` | `string` | ✓ |  | results_df parameter (pd.DataFrame). |
| `x` | `string` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SubgroupResult(x=["treatment", "covariate1", "covariate2"], results_df="value", overall_estimate=1.0, overall_se=1.0)
print(result.summary())
```

---
### `sp.calibrate_confounding_strength()`

**Calibrate the strength of an unobserved confounder required to**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `observed_r2_outcome` | `number` | ✓ |  | Partial-R2 of the observed covariate(s) with Y (resp. D). Used to benchmark "1x as confounding as observed" / "2x" etc. |
| `observed_r2_treatment` | `number` | ✓ |  | Partial-R2 of the observed covariate(s) with Y (resp. D). Used to benchmark "1x as confounding as observed" / "2x" etc. |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `target_estimate` | `number` |  | `0.0` | Effect value to explain away. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.calibrate_confounding_strength(estimate=1.0, se=1.0, observed_r2_outcome=1.0, observed_r2_treatment=1.0)
print(result.summary())
```

---
### `sp.copula_sensitivity()`

**Gaussian-copula sensitivity to unobserved confounding.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `rho_grid` | `array[string]` |  |  | Correlation grid. Defaults to ``np.linspace(-0.5, 0.5, 21)``. |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `sigma_u` | `number` |  | `1.0` | Standard deviations of the latent confounder and the outcome. With default values the bias coefficient is numerically equal to ``rho``, matching Chernozhukov-Cinelli-Hazlett's "percentile scaling." |
| `sigma_y` | `number` |  | `1.0` | Standard deviations of the latent confounder and the outcome. With default values the bias coefficient is numerically equal to ``rho``, matching Chernozhukov-Cinelli-Hazlett's "percentile scaling." |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.copula_sensitivity(estimate=1.0, se=1.0)
print(result.summary())
```

---
### `sp.robustness_report()`

**Run an automated battery of robustness checks.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_var` | `string` |  |  | Column for clustered SE check. |
| `data` | `string` | ✓ |  | Analysis dataset. |
| `drop_controls` | `array[string]` |  |  | Baseline controls to drop (one-by-one) for sensitivity. |
| `extra_controls` | `array[string]` |  |  | Additional controls to add (one-by-one) beyond baseline. |
| `formula` | `string` | ✓ |  | Baseline regression formula, e.g. ``"y ~ x1 + x2 + x3"``. |
| `subsets` | `object` |  |  | Named boolean masks for subsample checks. |
| `trim_pct` | `number` |  |  | Drop observations beyond this percentile from both tails. E.g. ``0.01`` trims top and bottom 1 %. |
| `winsor_levels` | `array[string]` |  |  | Winsorization percentiles, e.g. ``[0.01, 0.05]``. |
| `x` | `string` | ✓ |  | Key explanatory variable whose estimate stability is assessed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.robustness_report(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/robustness_workflow.md`

---
### `sp.spec_curve()`

**Specification curve analysis -- run many model specifications and visualise robustness.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `controls` | `array[string]` |  |  | Candidate control sets to sweep |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `x` | `string` | ✓ |  | Treatment / focal regressor |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.spec_curve(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`, `docs/guides/mixtape_ch09_did.md`, `docs/guides/replication_workflow.md`

---
### `sp.subgroup_analysis()`

**Run subgroup heterogeneity analysis with forest plot.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `by` | `object` | ✓ |  | Mapping of *display name* -> *column name* for grouping. |
| `data` | `string` | ✓ |  | Analysis dataset. |
| `formula` | `string` | ✓ |  | Regression formula, e.g. ``"wage ~ education + experience"``. |
| `robust` | `string` |  | `'hc1'` | Standard error type for subgroup regressions. |
| `x` | `string` | ✓ |  | Key explanatory variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.subgroup_analysis(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.survival_sensitivity()`

**Nonparametric sensitivity for survival / hazard-ratio outcomes.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `baseline_survival_t` | `number` |  | `0.5` | Baseline S_0(t) used to report Delta survival at time t. |
| `gamma_grid` | `array[string]` |  |  | Gamma (>= 1) values. Defaults to ``np.linspace(1.0, 3.0, 21)``. |
| `log_hr` | `number` | ✓ |  | log_hr parameter (float). |
| `se_log_hr` | `number` | ✓ |  | se_log_hr parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.survival_sensitivity(log_hr=1.0, se_log_hr=1.0)
print(result.summary())
```

---
### `sp.unified_sensitivity()`

**Run every applicable sensitivity analysis in one shot: E-value, Oster delta (when R^2 inputs given), Rosenbaum Gamma (when matched_pairs outcomes exposed), Sensemakr (when raw data supplied via data/y/treat/controls), and a breakdown-frontier bias estimate. Also available as result.sensitivity().**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_uncontrolled` | `number` |  |  | beta_uncontrolled parameter (float). |
| `controls` | `array[string]` |  |  | Control-variable column names. |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `include_oster` | `boolean` |  | `True` | Whether to include oster. |
| `include_rosenbaum` | `boolean` |  | `True` | Whether to include rosenbaum. |
| `include_sensemakr` | `boolean` |  | `True` | Whether to include sensemakr. |
| `r2_controlled` | `number` |  |  | r2_controlled parameter (float). |
| `r2_treated` | `number` |  |  | r2_treated parameter (float). |
| `result` | `string` | ✓ |  | result parameter (CausalResult \| EconometricResults). |
| `rho_max` | `number` |  | `1.0` | rho_max parameter (float). |
| `treat` | `string` |  |  | Treatment indicator or first-treatment-period column. |
| `y` | `string` |  |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.unified_sensitivity(y="outcome", data=df, result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/sensitivity_analysis.md`

---
