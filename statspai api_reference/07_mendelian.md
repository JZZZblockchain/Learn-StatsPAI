# mendelian

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Mendelian Randomization methods.

Uses genetic variants as instrumental variables to estimate causal effects
in epidemiological/health economics studies.

Core estimators (``mr``):
  - IVW (inverse-variance weighted)
  - MR-Egger regression
  - Weighted / penalized median

Diagnostics (``diagnostics``):
  - Cochran's Q / Rucker's Q' (heterogeneity)
  - MR-Egger intercept test (directional pleiotropy)
  - Leave-one-out sensitivity
  - Steiger directionality test
  - MR-PRESSO global test + outlier correction
  - Radial MR

Frontier (``frontier``, v1.6):
  - MR-Lap (Burgess-Davies-Thompson 2016 sample-overlap correction)
  - MR-Clust (Foley et al. 2021 clustered pleiotropy)
  - GRAPPLE (Wang et al. 2021 profile-likelihood MR)
  - MR-cML-BIC (Xue-Shen-Pan 2021 constrained maximum likelihood)

**38 个公共函数**

### `sp.FStatisticResult()`

**Result container returned by :func:`mr_f_statistic`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `f_max` | `number` | ✓ |  | f_max parameter (float). |
| `f_mean` | `number` | ✓ |  | f_mean parameter (float). |
| `f_min` | `number` | ✓ |  | f_min parameter (float). |
| `per_snp_F` | `string` | ✓ |  | per_snp_F parameter (np.ndarray). |
| `r2_mean` | `number` | ✓ |  | r2_mean parameter (float). |
| `weak_instrument_risk` | `boolean` | ✓ |  | weak_instrument_risk parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FStatisticResult(f_mean=1.0, f_min=1.0, f_max=1.0, weak_instrument_risk=True, r2_mean=1.0, per_snp_F="value")
print(result.summary())
```

---
### `sp.GrappleResult()`

**Output of :func:`grapple`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_lower` | `number` | ✓ |  | ci_lower parameter (float). |
| `ci_upper` | `number` | ✓ |  | ci_upper parameter (float). |
| `converged` | `boolean` | ✓ |  | converged parameter (bool). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `loglik` | `number` | ✓ |  | loglik parameter (float). |
| `n_snps` | `integer` | ✓ |  | Number of snps. |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `tau2` | `number` | ✓ |  | tau2 parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GrappleResult(estimate=1.0, se=1.0, ci_lower=1.0, ci_upper=1.0, p_value=1.0, tau2=1.0, loglik=1.0, converged=True, n_snps=1.0)
print(result.summary())
```

---
### `sp.HeterogeneityResult()`

**Container for Cochran's Q / Rucker's Q' heterogeneity diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `I2` | `number` | ✓ |  | I2 parameter (float). |
| `Q` | `number` | ✓ |  | Q parameter (float). |
| `Q_df` | `integer` | ✓ |  | Q_df parameter (int). |
| `Q_p` | `number` | ✓ |  | Q_p parameter (float). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.HeterogeneityResult(Q=1.0, Q_df=1.0, Q_p=1.0, I2=1.0, method="value")
print(result.summary())
```

---
### `sp.LeaveOneOutResult()`

**Container for leave-one-out IVW estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `table` | `string` | ✓ |  | table parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LeaveOneOutResult(table="value")
print(result.summary())
```

---
### `sp.MRClustResult()`

**Output of :func:`mr_clust`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K` | `integer` | ✓ |  | K parameter (int). |
> 📝 *K 参数（整数）。*
| `assignments` | `string` | ✓ |  | assignments parameter (np.ndarray). |
| `bic` | `object` | ✓ |  | bic parameter (dict). |
| `cluster_estimates` | `string` | ✓ |  | cluster_estimates parameter (pd.DataFrame). |
| `loglik` | `number` | ✓ |  | loglik parameter (float). |
| `n_snps` | `integer` | ✓ |  | Number of snps. |
| `responsibilities` | `string` | ✓ |  | responsibilities parameter (np.ndarray). |
| `wald_ratios` | `string` | ✓ |  | wald_ratios parameter (np.ndarray). |
| `wald_se` | `string` | ✓ |  | wald_se parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MRClustResult(cluster_estimates="value", assignments="value", responsibilities="value", K=1.0, loglik=1.0, wald_ratios="value", wald_se="value", n_snps=1.0)
print(result.summary())
```

---
### `sp.MRLapResult()`

**Output of :func:`mr_lap`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bias_correction` | `number` | ✓ |  | bias_correction parameter (float). |
| `ci_lower` | `number` | ✓ |  | ci_lower parameter (float). |
| `ci_upper` | `number` | ✓ |  | ci_upper parameter (float). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `estimate_ivw` | `number` | ✓ |  | estimate_ivw parameter (float). |
| `f_mean` | `number` | ✓ |  | f_mean parameter (float). |
| `n_snps` | `integer` | ✓ |  | Number of snps. |
| `overlap_fraction` | `number` | ✓ |  | overlap_fraction parameter (float). |
| `overlap_rho` | `number` | ✓ |  | overlap_rho parameter (float). |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MRLapResult(estimate=1.0, se=1.0, ci_lower=1.0, ci_upper=1.0, p_value=1.0, estimate_ivw=1.0, bias_correction=1.0, overlap_fraction=1.0, overlap_rho=1.0, f_mean=1.0, n_snps=1.0)
print(result.summary())
```

---
### `sp.MRPressoResult()`

**Container for MR-PRESSO global test and outlier-corrected estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `distortion_p` | `number` |  |  | distortion_p parameter (Optional[float]). |
| `global_test_pvalue` | `number` |  | `1.0` | global_test_pvalue parameter (float). |
| `global_test_rss_obs` | `number` |  | `0.0` | global_test_rss_obs parameter (float). |
| `outlier_corrected_estimate` | `number` | ✓ |  | outlier_corrected_estimate parameter (Optional[float]). |
| `outlier_corrected_p` | `number` | ✓ |  | outlier_corrected_p parameter (Optional[float]). |
| `outlier_corrected_se` | `number` | ✓ |  | outlier_corrected_se parameter (Optional[float]). |
| `outliers` | `array[string]` |  | `None` | outliers parameter (List[int]). |
| `raw_estimate` | `number` | ✓ |  | raw_estimate parameter (float). |
| `raw_p` | `number` | ✓ |  | raw_p parameter (float). |
| `raw_se` | `number` | ✓ |  | raw_se parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MRPressoResult(raw_estimate=1.0, raw_se=1.0, raw_p=1.0, outlier_corrected_estimate=1.0, outlier_corrected_se=1.0, outlier_corrected_p=1.0)
print(result.summary())
```

---
### `sp.MRRapsResult()`

**Output of :func:`mr_raps`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_lower` | `number` | ✓ |  | ci_lower parameter (float). |
| `ci_upper` | `number` | ✓ |  | ci_upper parameter (float). |
| `converged` | `boolean` | ✓ |  | converged parameter (bool). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `loglik_robust` | `number` | ✓ |  | loglik_robust parameter (float). |
| `n_snps` | `integer` | ✓ |  | Number of snps. |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `tau2` | `number` | ✓ |  | tau2 parameter (float). |
| `tuning_c` | `number` | ✓ |  | tuning_c parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MRRapsResult(estimate=1.0, se=1.0, ci_lower=1.0, ci_upper=1.0, p_value=1.0, tau2=1.0, loglik_robust=1.0, converged=True, tuning_c=1.0, n_snps=1.0)
print(result.summary())
```

---
### `sp.MRResult()`

**Results from Mendelian Randomization analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `estimates` | `string` | ✓ |  | estimates parameter (DataFrame). |
| `exposure` | `string` | ✓ |  | Exposure term or exposure column. |
| `heterogeneity` | `object` | ✓ |  | heterogeneity parameter (Dict[str, Any]). |
| `n_snps` | `integer` | ✓ |  | Number of snps. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `pleiotropy` | `object` | ✓ |  | pleiotropy parameter (Optional[Dict[str, float]]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MRResult(estimates="value", n_snps=1.0, exposure="value", outcome="value")
print(result.summary())
```

---
### `sp.MRcMLResult()`

**Output of :func:`mr_cml`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K_selected` | `integer` | ✓ |  | K_selected parameter (int). |
| `ci_lower` | `number` | ✓ |  | ci_lower parameter (float). |
| `ci_upper` | `number` | ✓ |  | ci_upper parameter (float). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `invalid_snps` | `string` | ✓ |  | invalid_snps parameter (np.ndarray). |
| `loglik` | `number` | ✓ |  | loglik parameter (float). |
| `n_snps` | `integer` | ✓ |  | Number of snps. |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `path` | `string` | ✓ |  | path parameter (pd.DataFrame). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MRcMLResult(estimate=1.0, se=1.0, ci_lower=1.0, ci_upper=1.0, p_value=1.0, K_selected=1.0, invalid_snps="value", path="value", loglik=1.0, n_snps=1.0)
print(result.summary())
```

---
### `sp.ModeBasedResult()`

**Result container returned by :func:`mr_mode`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth` | `number` | ✓ |  | Bandwidth used for local smoothing or kernel weighting. |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple[float, float]). |
> 📝 *ci 参数（浮点数二元组）。*
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` |  | `'weighted-mode'` | Estimator or algorithm variant to use. |
| `n_snps` | `integer` | ✓ |  | Number of snps. |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ModeBasedResult(estimate=1.0, se=1.0, ci=["a", "b"], p_value=1.0, n_snps=1.0, bandwidth=1.0)
print(result.summary())
```

---
### `sp.PleiotropyResult()`

**Container for the MR-Egger intercept (directional-pleiotropy) test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `intercept` | `number` | ✓ |  | intercept parameter (float). |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PleiotropyResult(intercept=1.0, se=1.0, p_value=1.0)
print(result.summary())
```

---
### `sp.RadialResult()`

**Container for radial-MR diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `Q_pvalue` | `number` | ✓ |  | Q_pvalue parameter (float). |
| `outliers` | `array[string]` | ✓ |  | outliers parameter (list[int]). |
| `table` | `string` | ✓ |  | table parameter (pd.DataFrame). |
| `total_Q` | `number` | ✓ |  | total_Q parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RadialResult(table="value", total_Q=1.0, Q_pvalue=1.0, outliers=["a", "b"])
print(result.summary())
```

---
### `sp.SteigerResult()`

**Container for the Steiger directionality test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `correct_direction` | `boolean` | ✓ |  | correct_direction parameter (bool). |
| `r2_exposure` | `number` | ✓ |  | r2_exposure parameter (float). |
| `r2_outcome` | `number` | ✓ |  | r2_outcome parameter (float). |
| `sample_size_exposure` | `integer` | ✓ |  | sample_size_exposure parameter (int). |
| `sample_size_outcome` | `integer` | ✓ |  | sample_size_outcome parameter (int). |
| `steiger_pvalue` | `number` | ✓ |  | steiger_pvalue parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SteigerResult(correct_direction=True, steiger_pvalue=1.0, r2_exposure=1.0, r2_outcome=1.0, sample_size_exposure=1.0, sample_size_outcome=1.0)
print(result.summary())
```

---
### `sp.grapple()`

**GRAPPLE: profile-likelihood MR with joint weak-instrument and balanced-pleiotropy robustness (Wang et al. 2021). Model: beta_y = beta*beta_x + u, Var(u) = se_y^2 + beta^2*se_x^2 + tau^2; jointly MLE over (beta, tau^2) via L-BFGS-B; SE from observed Fisher info.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_init` | `number` |  |  | beta_init parameter (float). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `tau2_init` | `number` |  | `0.0001` | tau2_init parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.grapple(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

---
### `sp.mendelian_randomization()`

**Mendelian Randomization analysis using summary statistics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` |  |  | Column name for SNP-exposure association beta. |
| `beta_outcome` | `string` |  |  | Column name for SNP-outcome association beta. |
| `data` | `string` |  |  | Summary statistics with one row per SNP/instrument. |
| `exposure_name` | `string` |  | `'Exposure'` | exposure_name parameter (str). |
| `methods` | `array[string]` |  |  | MR methods to use. Default: ['ivw', 'egger', 'weighted_median']. |
| `outcome_name` | `string` |  | `'Outcome'` | outcome_name parameter (str). |
| `se_exposure` | `string` |  |  | Column name for SNP-exposure SE. |
| `se_outcome` | `string` |  |  | Column name for SNP-outcome SE. |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mendelian_randomization(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr()`

**Unified Mendelian Randomization dispatcher. method= selects the estimator: 'ivw' / 'egger' / 'median' / 'penalized_median' / 'mode' / 'all' (runs IVW+Egger+Median together) / 'mvmr' / 'mediation' / 'bma' (multi-exposure) / 'presso' / 'radial' / 'leave_one_out' / 'steiger' / 'heterogeneity' / 'pleiotropy_egger' / 'f_statistic' (diagnostics). Kwargs are passed through to the target function unchanged; see sp.mendelian_family guide. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | `string` |  | `'ivw'` | MR estimator / diagnostic -- call sp.mr_available_methods() for the full list. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr()
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_available_methods()`

**Return the full list of registered MR method names (incl. aliases).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_available_methods()
print(result.summary())
```

---
### `sp.mr_bma()`

**MR Bayesian model averaging over exposure subsets (Zuber et al. 2020). Outputs marginal inclusion probabilities and top posterior models.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `exposures` | `array[string]` |  |  | exposures parameter (list). |
| `max_model_size` | `integer` |  |  | max_model_size parameter (int). |
| `outcome` | `string` |  | `'beta_y'` | Outcome variable column name or outcome array. |
| `outcome_se` | `string` |  | `'se_y'` | outcome_se parameter (str). |
| `snp_associations` | `string` | ✓ |  | snp_associations parameter (DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_bma(snp_associations="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_clust()`

**Clustered Mendelian randomization via finite Gaussian mixture on Wald ratios (Foley et al. 2021). EM with SNP-specific measurement SE; optional 'null' cluster at theta=0; K selected by BIC. Returns per-cluster estimate, SNP-to-cluster responsibilities, and the K-path.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K_range` | `array[string]` |  | `[1, 5]` | K_range parameter (tuple). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `include_null` | `boolean` |  | `True` | Whether to include null. |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_clust(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

---
### `sp.mr_cml()`

**MR-cML-BIC: constrained maximum-likelihood MR with L0-sparse pleiotropy (Xue, Shen & Pan 2021). Block-coordinate descent jointly updates causal beta, true exposure effects, and a K-sparse pleiotropy vector; K selected by BIC. Robust to correlated + uncorrelated pleiotropy simultaneously.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K_max` | `integer` |  |  | K_max parameter (int). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_cml(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

---
### `sp.mr_egger()`

**MR-Egger regression. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_egger(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`, `docs/guides/migration-from-r.md`

---
### `sp.mr_f_statistic()`

**Per-SNP F-statistic summary for instrument strength. Flags weak-instrument risk when any F < 10 (Staiger-Stock).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `n_samples` | `integer` |  |  | Number of samples. |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_f_statistic(beta_exposure="value", se_exposure="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_funnel_plot()`

**Funnel plot of SNP-specific Wald ratios vs. precision.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (np.ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (np.ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (np.ndarray). |
| `snp_ids` | `array[string]` |  |  | snp_ids parameter (Optional[List[str]]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_funnel_plot(beta_exposure="value", beta_outcome="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_heterogeneity()`

**Cochran's Q (IVW) or Ruecker's Q' (Egger) heterogeneity statistic with I^2, used to detect horizontal pleiotropy.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `method` | `string (enum)` |  | `'ivw'` | Estimator or algorithm variant to use. |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |

> **method** options: `'ivw'`, `'egger'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_heterogeneity(beta_exposure="value", beta_outcome="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_ivw()`

**Inverse-Variance Weighted (IVW) MR estimator. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_ivw(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`, `docs/guides/migration-from-r.md`

---
### `sp.mr_lap()`

**Sample-overlap-corrected IVW MR (Burgess-Davies-Thompson 2016 closed-form correction). Removes first-order bias when exposure and outcome GWAS share participants; requires overlap_fraction and overlap_rho (e.g. from LD-score regression).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `overlap_fraction` | `number` |  | `1.0` | overlap_fraction parameter (float). |
| `overlap_rho` | `number` |  | `0.0` | overlap_rho parameter (float). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_lap(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

---
### `sp.mr_leave_one_out()`

**Drop-one IVW sensitivity -- per-SNP table of estimates when each SNP is removed in turn. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `snp_ids` | `array[string]` |  |  | snp_ids parameter (list). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_leave_one_out(beta_exposure="value", beta_outcome="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_median()`

**Weighted median MR estimator. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications. |
| `penalized` | `boolean` |  | `False` | penalized parameter (bool). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_median(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_mediation()`

**Two-step (network) MR: decompose the total causal effect of an exposure on an outcome into direct + indirect (mediated) components.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_exposure` | `string` |  | `'beta_x'` | beta_exposure parameter (str). |
| `beta_mediator` | `string` |  | `'beta_m'` | beta_mediator parameter (str). |
| `beta_outcome` | `string` |  | `'beta_y'` | beta_outcome parameter (str). |
| `snp_associations` | `string` | ✓ |  | snp_associations parameter (DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_mediation(snp_associations="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_mode()`

**Weighted or simple mode-based MR estimator (Hartwig 2017). Consistent under the ZEMPA (zero-mode pleiotropy) assumption -- more permissive than the median's 50% rule.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `method` | `string (enum)` |  | `'weighted'` | Estimator or algorithm variant to use. |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications. |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |

> **method** options: `'weighted'`, `'simple'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_mode(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_multivariable()`

**Multivariable Mendelian randomization (Sanderson-Windmeijer 2019): direct causal effects of multiple correlated exposures via weighted least-squares on SNP-summary data, with conditional F-statistics for instrument strength.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `exposures` | `array[string]` |  |  | exposures parameter (list). |
| `outcome` | `string` |  | `'beta_y'` | Outcome variable column name or outcome array. |
| `outcome_se` | `string` |  | `'se_y'` | outcome_se parameter (str). |
| `snp_associations` | `string` | ✓ |  | snp_associations parameter (DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_multivariable(snp_associations="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_pleiotropy_egger()`

**Formal MR-Egger intercept test for directional (unbalanced) horizontal pleiotropy.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_pleiotropy_egger(beta_exposure="value", beta_outcome="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_presso()`

**MR-PRESSO global test + per-SNP outlier detection + outlier-corrected IVW estimate + distortion test. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications. |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `sig_threshold` | `number` |  | `0.05` | sig_threshold parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_presso(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_radial()`

**Radial IVW MR (Bowden 2018) with per-SNP Bonferroni-thresholded outlier flagging. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `snp_ids` | `array[string]` |  |  | snp_ids parameter (list). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_radial(beta_exposure="value", beta_outcome="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_raps()`

**MR-RAPS: Robust Adjusted Profile Score for two-sample summary-data MR (Zhao et al. 2020, Annals of Statistics). Profile-likelihood MR with Tukey biweight loss + weak-instrument correction; resistant to a small fraction of gross pleiotropy outliers. Complements GRAPPLE (Gaussian) with a robust-loss variant of the same structural model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_init` | `number` |  |  | beta_init parameter (float). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |
| `tau2_init` | `number` |  | `0.0001` | tau2_init parameter (float). |
| `tuning_c` | `number` |  | `4.685` | tuning_c parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_raps(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

---
### `sp.mr_scatter_plot()`

**Classic MR scatter plot with IVW and MR-Egger lines.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (np.ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (np.ndarray). |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (np.ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_scatter_plot(beta_exposure="value", beta_outcome="value", se_exposure="value", se_outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
### `sp.mr_steiger()`

**Steiger directionality test -- verifies that the SNPs explain more variance in the exposure than the outcome, supporting the assumed causal direction.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta_exposure` | `string` | ✓ |  | beta_exposure parameter (ndarray). |
| `beta_outcome` | `string` | ✓ |  | beta_outcome parameter (ndarray). |
| `eaf` | `string` |  |  | Effect-allele frequencies |
| `n_exposure` | `integer` | ✓ |  | Number of exposure. |
| `n_outcome` | `integer` | ✓ |  | Number of outcome. |
| `se_exposure` | `string` | ✓ |  | se_exposure parameter (ndarray). |
| `se_outcome` | `string` | ✓ |  | se_outcome parameter (ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mr_steiger(beta_exposure="value", se_exposure="value", n_exposure=1.0, beta_outcome="value", se_outcome="value", n_outcome=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/mendelian_family.md`

---
