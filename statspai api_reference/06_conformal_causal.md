# conformal_causal

> 📂 所属分类:06 · 贝叶斯方法 (Bayesian Methods)

Conformal Causal Inference: Distribution-free prediction intervals for ITE.

Provides prediction intervals for individual treatment effects (ITE)
without distributional assumptions, using conformal inference.

References
----------
Lei, L. & Candes, E. J. (2021).
Conformal Inference of Counterfactuals and Individual Treatment Effects.
JRSS-B, 83(5), 911-938. [@lei2021conformal]

Chernozhukov, V., Wuthrich, K., & Zhu, Y. (2021).
An Exact and Robust Conformal Inference Method for Counterfactual and
Synthetic Controls. JASA, 116(536), 1849-1864. [@chernozhukov2021exact]

**19 个公共函数**

### `sp.ConformalCATE()`

**Conformal prediction intervals for individual treatment effects.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `calib_fraction` | `number` |  | `0.25` | calib_fraction parameter (float). |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `model` | `string` |  |  | Model variant or parameterisation to fit. |
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

result = sp.ConformalCATE(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.ConformalCounterfactualResult()`

**Counterfactual prediction intervals under each potential outcome.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `lower_Y0` | `string` | ✓ |  | lower_Y0 parameter (np.ndarray). |
| `lower_Y1` | `string` | ✓ |  | lower_Y1 parameter (np.ndarray). |
| `marginal_coverage_estimate` | `number` | ✓ |  | marginal_coverage_estimate parameter (float). |
| `method` | `string` |  | `'Lei-Candes-2021-split-CQR'` | Estimator or algorithm variant to use. |
| `upper_Y0` | `string` | ✓ |  | upper_Y0 parameter (np.ndarray). |
| `upper_Y1` | `string` | ✓ |  | upper_Y1 parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ConformalCounterfactualResult(X="value", lower_Y1="value", upper_Y1="value", lower_Y0="value", upper_Y0="value", alpha=1.0, marginal_coverage_estimate=1.0)
print(result.summary())
```

---
### `sp.ConformalDensityResult()`

**Conditional-density conformal ITE intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coverage_target` | `number` | ✓ |  | coverage_target parameter (float). |
| `intervals` | `string` | ✓ |  | intervals parameter (np.ndarray). |
| `n_calibration` | `integer` | ✓ |  | Number of calibration. |
| `n_test` | `integer` | ✓ |  | Number of test. |
| `point_estimate` | `string` | ✓ |  | point_estimate parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ConformalDensityResult(intervals="value", point_estimate="value", coverage_target=1.0, n_calibration=1.0, n_test=1.0)
print(result.summary())
```

---
### `sp.ConformalITEResult()`

**Prediction intervals for the individual treatment effect tau(x).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `lower` | `string` | ✓ |  | lower parameter (np.ndarray). |
| `method` | `string` |  | `'nested-counterfactual-bound (Lei-Candes 2021 Eq. 3.4)'` | Estimator or algorithm variant to use. |
| `point` | `string` | ✓ |  | point parameter (np.ndarray). |
| `upper` | `string` | ✓ |  | upper parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ConformalITEResult(X="value", lower="value", upper="value", point="value", alpha=1.0)
print(result.summary())
```

---
### `sp.DebiasedConformalResult()`

**Debiased ML conformal counterfactual intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coverage_target` | `number` | ✓ |  | coverage_target parameter (float). |
| `intervals` | `string` | ✓ |  | intervals parameter (np.ndarray). |
| `n_calibration` | `integer` | ✓ |  | Number of calibration. |
| `n_test` | `integer` | ✓ |  | Number of test. |
| `point_estimate` | `string` | ✓ |  | point_estimate parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DebiasedConformalResult(intervals="value", point_estimate="value", coverage_target=1.0, n_calibration=1.0, n_test=1.0)
print(result.summary())
```

---
### `sp.FairConformalResult()`

**Fairness-aware conformal ITE intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coverage_target` | `number` | ✓ |  | coverage_target parameter (float). |
| `group_assignment` | `string` | ✓ |  | group_assignment parameter (np.ndarray). |
| `group_coverage_targets` | `object` | ✓ |  | group_coverage_targets parameter (Dict[str, float]). |
| `group_widths` | `object` | ✓ |  | group_widths parameter (Dict[str, float]). |
| `intervals` | `string` | ✓ |  | intervals parameter (np.ndarray). |
| `point_estimate` | `string` | ✓ |  | point_estimate parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FairConformalResult(intervals="value", point_estimate="value", group_assignment="value", coverage_target=1.0)
print(result.summary())
```

---
### `sp.MultiDPConformalResult()`

**Multi-decision-point conformal ITE intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coverage_target` | `number` | ✓ |  | coverage_target parameter (float). |
| `cumulative_interval` | `string` | ✓ |  | cumulative_interval parameter (np.ndarray). |
| `intervals_per_stage` | `array[string]` | ✓ |  | intervals_per_stage parameter (List[np.ndarray]). |
| `n_stages` | `integer` | ✓ |  | Number of stages. |
| `n_test` | `integer` | ✓ |  | Number of test. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MultiDPConformalResult(intervals_per_stage=["a", "b"], cumulative_interval="value", coverage_target=1.0, n_stages=1.0, n_test=1.0)
print(result.summary())
```

---
### `sp.conformal()`

**Unified conformal causal inference dispatcher. kind= selects the estimator: 'cate' / 'counterfactual' / 'ite' (Lei-Candes 2021 base) / 'weighted' (TBCR 2019 primitive) / 'density' / 'multidp' / 'debiased' / 'fair' (2025-2026 frontier) / 'continuous' (dose-response) / 'interference' (cluster-exchangeable). Kwargs pass through to the target function; see sp.conformal_family guide.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `kind` | `string` |  | `'cate'` | Conformal estimator -- call sp.conformal_available_kinds() for the full list. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal()
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_available_kinds()`

**Return the full list of registered conformal ``kind`` names.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_available_kinds()
print(result.summary())
```

---
### `sp.conformal_cate()`

**Compute conformal prediction intervals for CATE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Miscoverage level. Intervals have (1-alpha) coverage. |
| `calib_fraction` | `number` |  | `0.25` | Fraction of data used for calibration. |
| `covariates` | `array[string]` | ✓ |  | Covariate names. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `model` | `string` |  |  | Outcome model for mu_d(X). If None, uses GBM. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Binary treatment variable (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_cate(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`, `docs/guides/migration-from-r.md`

---
### `sp.conformal_continuous()`

**Split-conformal prediction bands for continuous-treatment dose-response curves (Schroder, Frauen, Schweisthal, He, Melnychuk, Feuerriegel 2024, arXiv:2407.03094).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.1` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `test_data` | `string` | ✓ |  | test_data parameter (DataFrame). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_continuous(y="outcome", data=df, treatment="value", covariates=["a", "b"], test_data="value")
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_counterfactual()`

**Prediction intervals for the counterfactual potential outcomes**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X_test` | `string` |  |  | Points at which to return intervals. Defaults to ``data[covariates]``. |
| `alpha` | `number` |  | `0.1` | Miscoverage level. |
| `calib_frac` | `number` |  | `0.3` | Fraction of each arm used for calibration. |
| `covariates` | `array[string]` | ✓ |  | Columns used as features for both the outcome and propensity models. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `model` | `string` |  |  | Model variant or parameterisation to fit. |
| `propensity_model` | `string` |  |  | propensity_model parameter (Optional[BaseEstimator]). |
| `random_state` | `integer` |  |  | Random seed or RandomState for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Outcome and 0/1 treatment column names. |
| `y` | `string` | ✓ |  | Outcome and 0/1 treatment column names. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_counterfactual(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_debiased_ml()`

**Debiased ML conformal counterfactual intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.1` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_folds` | `integer` |  | `5` | Cross-fitting folds (debiased step). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `test_data` | `string` |  |  | test_data parameter (Optional[pd.DataFrame]). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_debiased_ml(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_density_ite()`

**Conditional-density conformal ITE intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.1` | Miscoverage; intervals target 1 - alpha coverage. |
| `bandwidth` | `number` |  |  | KDE bandwidth; defaults to Silverman's rule on calibration Y. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | Training data with both treated and control units. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `test_data` | `string` |  |  | Test set; defaults to ``data`` (in-sample intervals). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_density_ite(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_fair_ite()`

**Counterfactual-fair conformal prediction for ITE (2025). Wraps standard conformal ITE intervals with a demographic-parity adjustment, giving distribution-free coverage under protected-attribute shifts. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.1` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `protected` | `string` | ✓ |  | Protected-attribute column |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_fair_ite(y="outcome", data=df, treat="value", covariates=["a", "b"], protected="value")
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_interference()`

**Cluster-exchangeable split-conformal prediction under network interference (2509.21660 systematic review).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.1` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Cluster identifier column for clustered standard errors. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `test_clusters` | `array[string]` | ✓ |  | test_clusters parameter (list). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_interference(y="outcome", data=df, treatment="value", cluster="value", covariates=["a", "b"], test_clusters=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_ite_interval()`

**Conformal prediction intervals for the individual treatment**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X_test` | `string` |  |  | X_test parameter (Optional[np.ndarray]). |
| `alpha` | `number` |  | `0.1` | Significance level for confidence intervals and tests. |
| `calib_frac` | `number` |  | `0.3` | calib_frac parameter (float). |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `model` | `string` |  |  | Model variant or parameterisation to fit. |
| `propensity_model` | `string` |  |  | propensity_model parameter (Optional[BaseEstimator]). |
| `random_state` | `integer` |  |  | Random seed or RandomState for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_ite_interval(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.conformal_ite_multidp()`

**Multi-decision-point conformal ITE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.1` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | Long-format wide data: each row = subject; columns include stage-specific outcomes / treatments / histories. |
| `history_per_stage` | `array[string]` | ✓ |  | History (covariates available at decision time k). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `test_data` | `string` |  |  | test_data parameter (Optional[pd.DataFrame]). |
| `treat_per_stage` | `array[string]` | ✓ |  | Binary treatment at each stage. |
| `y_per_stage` | `array[string]` | ✓ |  | Outcome column at each stage k = 1, ..., K. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conformal_ite_multidp(data=df, y_per_stage=["a", "b"], treat_per_stage=["a", "b"], history_per_stage=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
### `sp.weighted_conformal_prediction()`

**Split conformal prediction with per-calibration-point weights.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X_calib` | `string` | ✓ |  | Calibration fold used to compute non-conformity scores. |
| `X_test` | `string` | ✓ |  | Points at which to produce prediction intervals. |
| `X_train` | `string` | ✓ |  | Training fold used to fit the base regression model. |
| `alpha` | `number` |  | `0.1` | Miscoverage level (interval targets ``1-alpha`` coverage). |
| `model` | `string` |  |  | Defaults to ``RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=0)``. |
| `weights_calib` | `string` |  |  | Per-calibration-point likelihood-ratio weights ``w_i = f_test(X_i) / f_train(X_i)`` for covariate-shift correction. If None, uniform weights. |
| `y_calib` | `string` | ✓ |  | Calibration fold used to compute non-conformity scores. |
| `y_train` | `string` | ✓ |  | Training fold used to fit the base regression model. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.weighted_conformal_prediction(X_train="value", y_train="value", X_calib="value", y_calib="value", X_test="value")
print(result.summary())
```

> 📁 See also: `docs/guides/conformal_family.md`

---
