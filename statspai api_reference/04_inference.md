# inference

> 📂 所属分类:04 · 诊断、稳健性与推断 (Diagnostics, Robustness & Inference)

Inference module for StatsPAI.

Provides robust inference methods for supported estimator results:
- Wild Cluster Bootstrap (Cameron, Gelbach & Miller 2008)
- Randomization Inference (Fisher 1935; Young 2019)

**24 个公共函数**

### `sp.BootstrapResult()`

**Container for bootstrap inference results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `boot_distribution` | `string` | ✓ |  | boot_distribution parameter (np.ndarray). |
| `ci_lower` | `number` | ✓ |  | ci_lower parameter (float). |
| `ci_method` | `string` | ✓ |  | ci_method parameter (str). |
| `ci_upper` | `number` | ✓ |  | ci_upper parameter (float). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `n_boot` | `integer` | ✓ |  | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `pvalue` | `number` | ✓ |  | pvalue parameter (float). |
> 📝 *pvalue 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BootstrapResult(estimate=1.0, se=1.0, ci_lower=1.0, ci_upper=1.0, pvalue=1.0, alpha=1.0, n_boot=1.0, boot_distribution="value", ci_method="value")
print(result.summary())
```

---
### `sp.FisherResult()`

**Result container for Fisher's exact permutation test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (Tuple[float, float]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `n_perm` | `integer` | ✓ |  | Number of permutation replications. |
| `n_treated` | `integer` | ✓ |  | Number of treated. |
| `p_one_sided` | `number` | ✓ |  | p_one_sided parameter (float). |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `perm_dist` | `string` | ✓ |  | perm_dist parameter (ndarray). |
| `statistic` | `number` | ✓ |  | statistic parameter (float). |
> 📝 *statistic 参数（浮点数）。*
| `statistic_type` | `string` | ✓ |  | statistic_type parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FisherResult(statistic=1.0, p_value=1.0, p_one_sided=1.0, ci=["a", "b"], perm_dist="value", statistic_type="value", n_perm=1.0, n_obs=1.0, n_treated=1.0)
print(result.summary())
```

---
### `sp.MetaAnalysisResult()`

**Result of a summary-data meta-analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `effects` | `string` | ✓ |  | effects parameter (np.ndarray). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `fixed_estimate` | `number` | ✓ |  | fixed_estimate parameter (float). |
| `fixed_se` | `number` | ✓ |  | fixed_se parameter (float). |
| `h2` | `number` | ✓ |  | h2 parameter (float). |
| `i2` | `number` | ✓ |  | i2 parameter (float). |
| `labels` | `array[string]` | ✓ |  | labels parameter (List[str]). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `prediction_interval` | `array[string]` | ✓ |  | prediction_interval parameter (Optional[tuple]). |
| `q` | `number` | ✓ |  | Quantile level. |
| `q_df` | `integer` | ✓ |  | q_df parameter (int). |
| `q_pvalue` | `number` | ✓ |  | q_pvalue parameter (float). |
| `random_estimate` | `number` | ✓ |  | random_estimate parameter (float). |
| `random_se` | `number` | ✓ |  | random_se parameter (float). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `se_studies` | `string` | ✓ |  | se_studies parameter (np.ndarray). |
| `tau2` | `number` | ✓ |  | tau2 parameter (float). |
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MetaAnalysisResult(estimate=1.0, se=1.0, ci=["a", "b"], p_value=1.0, method="value", fixed_estimate=1.0, fixed_se=1.0, random_estimate=1.0, random_se=1.0, tau2=1.0, q=1.0, q_df=1.0, q_pvalue=1.0, i2=1.0, h2=1.0, prediction_interval=["a", "b"], weights="value", effects="value", se_studies="value", labels=["a", "b"])
print(result.summary())
```

---
### `sp.PATEEstimator()`

**Population Average Treatment Effect estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data_experiment` | `string` | ✓ |  | data_experiment parameter (DataFrame). |
| `data_target` | `string` | ✓ |  | data_target parameter (DataFrame). |
| `method` | `string` |  | `'ipw'` | Estimator or algorithm variant to use. |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `trim` | `number` |  | `0.01` | trim parameter (float). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PATEEstimator(y="outcome", data_experiment="value", data_target="value", treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.aipw()`

**Augmented inverse-probability weighting (AIPW) -- the canonical doubly-robust ATE estimator. Cross-fits an outcome regression and a propensity model and combines them via the efficient-influence-function formula, so the estimate is consistent if either nuisance is correctly specified (Robins, Rotnitzky & Zhao 1994). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Confounders to adjust for |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string (enum)` |  | `'ATE'` | Target estimand |
| `n_folds` | `integer` |  | `5` | Cross-fitting folds (>= 2) |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Binary treatment (0/1) |
| `y` | `string` | ✓ |  | Outcome variable |

> **estimand** options: `'ATE'`, `'ATT'`, `'ATC'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.aipw(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/g_methods_ph.md`

---
### `sp.bootstrap()`

**General bootstrap inference: nonparametric, cluster, block. Percentile/BCa/normal CIs. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_method` | `string (enum)` |  | `'percentile'` | CI method |
| `cluster` | `string` |  |  | Cluster variable for cluster bootstrap |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications. |
| `statistic` | `string` | ✓ |  | Function f(df) -> float |

> **ci_method** options: `'percentile'`, `'bca'`, `'normal'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bootstrap(data=df, statistic="value")
print(result.summary())
```

> 📁 See also: `docs/guides/callaway_santanna.md`, `docs/guides/choosing_did_estimator.md`, `docs/guides/cs_report.md`

---
### `sp.cluster_robust_se()`

**Return cluster-robust standard errors (diagonal sqrt of vcov).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `clusters` | `array[string]` | ✓ |  | Cluster labels for clustered inference. |
| `resid` | `string` | ✓ |  | resid parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cluster_robust_se(X="value", resid="value", clusters=["a", "b"])
print(result.summary())
```

---
### `sp.conley()`

**Compute Conley (1999) spatial HAC standard errors.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `data` | `string` | ✓ |  | Data with latitude and longitude columns (in **degrees**). |
| `dist_cutoff` | `number` | ✓ |  | Distance cutoff *h* in kilometres. Pairs farther apart than this receive zero weight. |
| `kernel` | `string` |  | `'uniform'` | Kernel function: ``"uniform"`` (indicator) or ``"bartlett"`` (linearly declining weight). |
| `lat` | `string` | ✓ |  | Column name for latitude. |
| `lon` | `string` | ✓ |  | Column name for longitude. |
| `result` | `string` | ✓ |  | Fitted OLS result. Must have ``data_info`` containing ``'X'`` (design matrix), ``'y'`` (response), and ``'residuals'``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.conley(data=df, result="value", lat="value", lon="value", dist_cutoff=1.0)
print(result.summary())
```

---
### `sp.cr2_se()`

**CR2 bias-corrected cluster-robust standard errors (Bell & McCaffrey 2002). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` | ✓ |  | Name of the cluster variable in ``data``. |
| `data` | `string` | ✓ |  | The original data used for estimation. |
| `result` | `string` | ✓ |  | A fitted regression result from ``sp.regress()``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cr2_se(data=df, result="value", cluster="value")
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`

---
### `sp.cr3_jackknife_vcov()`

**CR3 cluster-jackknife variance (delete-one-cluster). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `cluster` | `string` | ✓ |  | Cluster identifier column for clustered standard errors. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cr3_jackknife_vcov(y="outcome", X="value", cluster="value")
print(result.summary())
```

---
### `sp.fisher_exact()`

**Fisher's exact randomization test with enhanced features. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the Hodges-Lehmann confidence interval. |
| `cluster` | `string` |  |  | Variable for cluster-level randomization (permute by cluster). |
| `controls` | `array[string]` |  |  | Control variables for covariate-adjusted inference. When provided, the test statistic is computed on residuals from regressing Y on controls. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `n_perm` | `integer` |  | `10000` | Number of random permutations. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `statistic` | `string` |  | `'ate'` | Test statistic to use: - ``'ate'``: Average treatment effect (difference in means). - ``'ks'``: Kolmogorov-Smirnov statistic. - ``'rank_sum'``: Wilcoxon rank-sum statistic. |
| `stratify` | `string` |  |  | Variable for stratified permutation (permute within strata). |
| `treatment` | `string` | ✓ |  | Binary treatment variable name (0/1). |
| `y` | `string` | ✓ |  | Outcome variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.fisher_exact(y="outcome", data=df, treatment="value")
print(result.summary())
```

---
### `sp.front_door()`

**Pearl's front-door adjustment: identifies ATE with unmeasured confounding when a mediator fully transmits the effect of D on Y. Supports binary or continuous mediator; integrate_by controls Pearl (marginal) vs Fulcher et al. (conditional) aggregation. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Pre-treatment covariates |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `integrate_by` | `string (enum)` |  | `'marginal'` | MC integration formulation (continuous M only) |
| `mediator` | `string` | ✓ |  | Fully-transmitting mediator |
| `mediator_type` | `string (enum)` |  | `'auto'` | Mediator model |
| `treat` | `string` | ✓ |  | Binary treatment (0/1) |
| `y` | `string` | ✓ |  | Outcome |

> **integrate_by** options: `'marginal'`, `'conditional'`

> **mediator_type** options: `'auto'`, `'binary'`, `'continuous'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.front_door(formula="y ~ x1 + x2", data=df, treat="value", mediator="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
### `sp.g_computation()`

**Parametric g-formula (standardization) estimator. ATE/ATT for binary D, or dose-response curve for continuous D. Consistent under correctly-specified outcome model; not doubly robust. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Baseline covariates |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string (enum)` |  | `'ATE'` | Target estimand |
| `n_boot` | `integer` |  | `500` | Bootstrap replications for SE |
| `treat` | `string` | ✓ |  | Treatment variable |
| `treat_values` | `array[string]` |  |  | Dose grid (required for dose_response) |
| `y` | `string` | ✓ |  | Outcome |

> **estimand** options: `'ATE'`, `'ATT'`, `'dose_response'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.g_computation(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `nhefs_whatif.py`, `docs/guides/g_methods_ph.md`, `docs/guides/whatif_nhefs.md`

---
### `sp.ipw()`

**Inverse Probability Weighting for ATE/ATT/ATC with propensity score trimming. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string (enum)` |  | `'ATE'` | Target estimand |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `trim` | `number` |  | `0.0` | Propensity score trimming threshold |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **estimand** options: `'ATE'`, `'ATT'`, `'ATC'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ipw(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `nhefs_whatif.py`, `docs/guides/g_methods_ph.md`, `docs/guides/whatif_nhefs.md`

---
### `sp.jackknife_se()`

**Leave-one-cluster-out jackknife standard errors. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` | ✓ |  | Name of the cluster variable in ``data``. |
| `data` | `string` | ✓ |  | The original data used for estimation. |
| `result` | `string` | ✓ |  | A fitted regression result from ``sp.regress()``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.jackknife_se(data=df, result="value", cluster="value")
print(result.summary())
```

---
### `sp.meta_analysis()`

**Summary-data meta-analysis with fixed- and random-effects pooling.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence/prediction intervals. |
| `effects` | `array[string]` | ✓ |  | Per-study effect sizes (e.g. log odds ratios, mean differences). |
| `labels` | `array[string]` |  |  | Study labels for the forest plot. |
| `method` | `string (enum)` |  | `'DL'` | Which model the headline ``estimate`` reports: DerSimonian-Laird random effects (default) or fixed-effect inverse-variance. Both are always computed and available on the result. |
| `se` | `array[string]` | ✓ |  | Per-study standard errors (must be positive). |

> **method** options: `'DL'`, `'fixed'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.meta_analysis(effects=["a", "b"], se=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/meta_analysis.md`

---
### `sp.multiway_cluster_vcov()`

**Compute N-way cluster-robust variance of an OLS coefficient vector. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Design matrix used in the regression. |
| `clusters` | `array[string]` | ✓ |  | One or more cluster variables, one per dimension. Non-numeric labels are supported. |
| `df_adjust` | `boolean` |  | `True` | If True, apply the G/(G-1) * (n-1)/(n-k) CR1 finite-sample correction per component variance. If False, uses raw sandwich (useful when the caller has already degreed-freedom adjusted). |
| `n_params` | `integer` |  |  | Override for the ``k`` used in DOF adjustment; useful when FEs have been absorbed (pass total absorbed DOF here). |
| `psd_correct` | `boolean` |  | `True` | Project V onto PSD cone by zeroing negative eigenvalues. |
| `resid` | `string` | ✓ |  | OLS residuals. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.multiway_cluster_vcov(X="value", resid="value", clusters=["a", "b"])
print(result.summary())
```

---
### `sp.pate()`

**Estimate the Population Average Treatment Effect (PATE). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the confidence interval. |
| `covariates` | `array[string]` | ✓ |  | Shared covariates present in both datasets. |
| `data_experiment` | `string` | ✓ |  | Experimental/study sample. Must contain *y*, *treatment*, and all *covariates*. |
| `data_target` | `string` | ✓ |  | Target population sample. Must contain all *covariates*. Need not contain *y* or *treatment*. |
| `method` | `string (enum)` |  | `'ipw'` | Estimation strategy: * ``'ipw'`` -- Inverse probability of sampling weights. * ``'aipw'`` -- Augmented IPW (doubly robust). * ``'calibration'`` -- Entropy balancing on covariate moments. |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications for standard-error estimation. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `treatment` | `string` | ✓ |  | Binary treatment indicator (only in data_experiment). |
| `trim` | `number` |  | `0.01` | Trimming threshold for participation propensities (values below *trim* or above 1 - *trim* are clipped). |
| `y` | `string` | ✓ |  | Outcome variable (only used from data_experiment). |

> **method** options: `'ipw'`, `'aipw'`, `'calibration'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pate(y="outcome", data_experiment="value", data_target="value", treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.ri_test()`

**Randomization inference p-value. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster-level permutation (permute treatment at cluster level). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_perms` | `integer` |  | `1000` | Number of random permutations. Use 10000+ for publications. |
| `seed` | `integer` |  |  | Random seed. |
| `stat` | `string` |  | `'diff_means'` | Test statistic: - ``'diff_means'``: difference in means (Y_bar_1 - Y_bar_0) - ``'ks'``: Kolmogorov-Smirnov statistic - ``'t'``: t-statistic - A callable ``f(Y, D) -> float`` for custom statistics. |
| `treat` | `string` | ✓ |  | Binary treatment indicator (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ri_test(y="outcome", data=df, treat="value")
print(result.summary())
```

---
### `sp.subcluster_wild_bootstrap()`

**Subcluster wild cluster bootstrap for few-treated-clusters. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Primary cluster column (for SE computation). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `h0` | `number` |  | `0.0` | Null value. |
| `n_boot` | `integer` |  | `999` | Bootstrap replications. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `subcluster` | `string` |  |  | Finer grouping at which sign-flips occur. If ``None``, every observation is its own subcluster (pure Rademacher at obs level). |
| `test_var` | `string` |  |  | Parameter to test; default last element of ``x``. |
| `weight_type` | `string (enum)` |  | `'webb'` | Distribution of sign flips. ``'webb'`` (6-point) recommended when treatment has <= 5 treated clusters. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **weight_type** options: `'rademacher'`, `'webb'`, `'mammen'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.subcluster_wild_bootstrap(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, cluster="value")
print(result.summary())
```

---
### `sp.twoway_cluster()`

**Compute two-way cluster-robust standard errors. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster1` | `string` | ✓ |  | Column name for the first clustering dimension. |
| `cluster2` | `string` | ✓ |  | Column name for the second clustering dimension. |
| `data` | `string` | ✓ |  | Original data containing the cluster variables. |
| `result` | `string` | ✓ |  | Fitted OLS result. Must have ``data_info`` containing ``'X'`` (design matrix), ``'y'`` (response), and ``'residuals'``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.twoway_cluster(data=df, result="value", cluster1="value", cluster2="value")
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`

---
### `sp.wild_cluster_boot()`

**Wild cluster bootstrap t-test for a single coefficient.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence interval. |
| `cluster` | `string` | ✓ |  | Name of the cluster variable. |
| `data` | `string` | ✓ |  | The original data used for estimation. |
| `n_boot` | `integer` |  | `999` | Number of bootstrap replications (use odd number). |
| `result` | `string` | ✓ |  | A fitted regression result from ``sp.regress()``. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `variable` | `string` | ✓ |  | Name of the coefficient to test (H0: beta = 0). |
| `weight_type` | `string` |  | `'rademacher'` | Bootstrap weight distribution: - ``'rademacher'``: +/-1 with equal probability. - ``'webb'``: Webb (2014) 6-point distribution for G < 12. - ``'mammen'``: Mammen (1993) 2-point distribution. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.wild_cluster_boot(data=df, result="value", cluster="value", variable="value")
print(result.summary())
```

---
### `sp.wild_cluster_bootstrap()`

**Cameron-Gelbach-Miller (2008) wild cluster bootstrap -- the canonical fix for cluster-robust inference with few clusters (G < 30). Re-samples cluster-level Rademacher weights to construct a percentile-t reference distribution that has correct size when the standard cluster-robust z-test rejects too often. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Cluster identifier |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `h0` | `number` |  | `0.0` | Null value of the coefficient |
| `n_boot` | `integer` |  | `999` | Number of bootstrap replications. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `test_var` | `string` |  |  | Variable being tested; defaults to first in x |
| `weight_type` | `string (enum)` |  | `'rademacher'` | Bootstrap weight distribution |
| `x` | `array[string]` | ✓ |  | Right-hand-side variables |
| `y` | `string` | ✓ |  | Outcome variable |

> **weight_type** options: `'rademacher'`, `'mammen'`, `'webb'`, `'normal'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.wild_cluster_bootstrap(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, cluster="value")
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`

---
### `sp.wild_cluster_ci_inv()`

**Confidence interval via bootstrap p-value inversion.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Cluster identifier column for clustered standard errors. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `grid_size` | `integer` |  | `41` | Number of null-value grid points to evaluate (odd preferred). |
| `grid_span` | `number` |  | `6.0` | Half-width of the search grid in units of cluster-robust SE. |
| `n_boot` | `integer` |  | `999` | Number of bootstrap replications. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `test_var` | `string` |  |  | test_var parameter (Optional[str]). |
| `weight_type` | `string` |  | `'webb'` | weight_type parameter (str). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.wild_cluster_ci_inv(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, cluster="value")
print(result.summary())
```

---
