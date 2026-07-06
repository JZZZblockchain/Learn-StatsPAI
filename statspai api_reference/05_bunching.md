# bunching

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Bunching Estimator for kink/notch analysis.

Estimates behavioural responses to policy thresholds (tax kinks,
regulatory notches) by comparing the observed distribution of a
running variable to a counterfactual polynomial distribution.

References
----------
Kleven, H. J. & Waseem, M. (2013).
Using Notches to Uncover Optimization Frictions and Structural Elasticities.
QJE, 128(2), 669-723. [@kleven2013using]

Chetty, R., Friedman, J. N., Olsen, T., & Pistaferri, L. (2011).
Adjustment Costs, Firm Responses, and Micro vs. Macro Labor Supply
Elasticities. QJE, 126(2), 749-804. [@chetty2011adjustment]

**8 个公共函数**

### `sp.BunchingEstimator()`

**Bunching estimator for kink/notch designs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bin_width` | `number` |  |  | bin_width parameter (Optional[float]). |
| `bunch_region` | `array[string]` |  |  | bunch_region parameter (Optional[Tuple[float, float]]). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `design` | `string` |  | `'kink'` | design parameter (str). |
| `dt` | `number` |  |  | dt parameter (Optional[float]). |
| `exclude_region` | `array[string]` |  |  | exclude_region parameter (Optional[Tuple[float, float]]). |
| `n_bins` | `integer` |  | `50` | Number of bins. |
| `n_bootstrap` | `integer` |  | `200` | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `poly_order` | `integer` |  | `7` | poly_order parameter (int). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `running_var` | `string` | ✓ |  | running_var parameter (str). |
| `threshold` | `number` | ✓ |  | threshold parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BunchingEstimator(data=df, running_var="value", threshold=1.0)
print(result.summary())
```

---
### `sp.GeneralBunchingResult()`

**Output of high-order bunching design.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bias_corrected_elasticity` | `number` | ✓ |  | bias_corrected_elasticity parameter (float). |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `naive_elasticity` | `number` | ✓ |  | naive_elasticity parameter (float). |
| `polynomial_order` | `integer` | ✓ |  | polynomial_order parameter (int). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GeneralBunchingResult(naive_elasticity=1.0, bias_corrected_elasticity=1.0, se=1.0, ci=["a", "b"], polynomial_order=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.KinkUnifiedResult()`

**Joint RDD + RKD + Bunching estimate at a common cutoff.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth` | `number` | ✓ |  | Bandwidth used for local smoothing or kernel weighting. |
| `bunching_elasticity` | `number` | ✓ |  | bunching_elasticity parameter (float). |
| `bunching_se` | `number` | ✓ |  | bunching_se parameter (float). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `rdd_effect` | `number` | ✓ |  | rdd_effect parameter (float). |
| `rdd_se` | `number` | ✓ |  | rdd_se parameter (float). |
| `rkd_effect` | `number` | ✓ |  | rkd_effect parameter (float). |
| `rkd_se` | `number` | ✓ |  | rkd_se parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.KinkUnifiedResult(rdd_effect=1.0, rdd_se=1.0, rkd_effect=1.0, rkd_se=1.0, bunching_elasticity=1.0, bunching_se=1.0, bandwidth=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.NotchResult()`

**Result container for notch bunching analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `bin_centers` | `string` | ✓ |  | bin_centers parameter (ndarray). |
| `causal_result` | `string` | ✓ |  | causal_result parameter (CausalResult). |
| `ci` | `array[string]` | ✓ |  | ci parameter (Tuple[float, float]). |
| `counterfactual` | `string` | ✓ |  | counterfactual parameter (ndarray). |
| `elasticity` | `number` | ✓ |  | elasticity parameter (Optional[float]). |
| `excess_bunching` | `number` | ✓ |  | excess_bunching parameter (float). |
| `marginal_buncher` | `number` | ✓ |  | marginal_buncher parameter (float). |
| `missing_mass` | `number` | ✓ |  | missing_mass parameter (float). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `notch_point` | `number` | ✓ |  | notch_point parameter (float). |
| `notch_size` | `number` |  |  | notch_size parameter (Optional[float]). |
| `observed` | `string` | ✓ |  | observed parameter (ndarray). |
| `pvalue` | `number` | ✓ |  | pvalue parameter (float). |
> 📝 *pvalue 参数（浮点数）。*
| `se_bunching` | `number` | ✓ |  | se_bunching parameter (float). |
| `se_elasticity` | `number` | ✓ |  | se_elasticity parameter (Optional[float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.NotchResult(excess_bunching=1.0, missing_mass=1.0, marginal_buncher=1.0, elasticity=1.0, se_bunching=1.0, se_elasticity=1.0, pvalue=1.0, ci=["a", "b"], alpha=1.0, notch_point=1.0, bin_centers="value", observed="value", counterfactual="value", n_obs=1.0, causal_result="value")
print(result.summary())
```

---
### `sp.bunching()`

**Estimate bunching at a policy threshold. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `bin_width` | `number` |  |  | Width of bins. If None, computed from data range / n_bins. |
| `bunch_region` | `array[string]` |  |  | (lower, upper) bounds of the bunching region. If None, uses [threshold - 2*bin_width, threshold + 2*bin_width]. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `design` | `string` |  | `'kink'` | 'kink' or 'notch'. |
| `dt` | `number` |  |  | Change in marginal tax rate at the kink (for elasticity). E.g., 0.10 for a 10pp increase. |
| `exclude_region` | `array[string]` |  |  | Same as bunch_region unless otherwise specified. |
| `n_bins` | `integer` |  | `50` | Number of bins on each side of the threshold. |
| `n_bootstrap` | `integer` |  | `200` | Bootstrap iterations for standard errors. |
| `poly_order` | `integer` |  | `7` | Order of the counterfactual polynomial. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `running_var` | `string` | ✓ |  | Name of the running variable (e.g., income). |
| `threshold` | `number` | ✓ |  | Policy threshold (kink/notch point). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bunching(data=df, running_var="value", threshold=1.0)
print(result.summary())
```

---
### `sp.general_bunching()`

**High-order bunching design with bias correction. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bandwidth` | `number` |  | `1.0` | Bandwidth used for local smoothing or kernel weighting. |
| `bin_width` | `number` |  |  | Defaults to bandwidth / 25. |
| `cutoff` | `number` |  | `0.0` | cutoff parameter (float). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_boot` | `integer` |  | `200` | Number of bootstrap replications. |
| `polynomial_order` | `integer` |  | `4` | Order of the counterfactual polynomial fit. |
| `running` | `string` | ✓ |  | Running variable (e.g. earnings). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.general_bunching(data=df, running="value")
print(result.summary())
```

---
### `sp.kink_unified()`

**Run RDD + RKD + Bunching on the same data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `bandwidth` | `number` |  |  | Bandwidth used for local smoothing or kernel weighting. |
| `bin_width` | `number` |  |  | bin_width parameter (Optional[float]). |
| `cutoff` | `number` |  | `0.0` | cutoff parameter (float). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `polynomial_order` | `integer` |  | `2` | polynomial_order parameter (int). |
| `running` | `string` | ✓ |  | Running variable (also forms density for Bunching). |
| `y` | `string` | ✓ |  | Outcome variable (used by RDD/RKD). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.kink_unified(y="outcome", data=df, running="value")
print(result.summary())
```

---
### `sp.notch()`

**Bunching at Notches estimator (Kleven & Waseem 2013). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `bin_width` | `number` |  | `500` | Bin width for the histogram. |
| `data` | `string` | ✓ |  | Input dataset. |
| `exclude_range` | `array[string]` |  |  | Range around the notch to exclude from the counterfactual fit. If None, defaults to (notch_point - 3*bin_width, notch_point + 5*bin_width). |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications for standard errors. |
| `notch_point` | `number` | ✓ |  | Location of the notch in the running variable. |
| `notch_size` | `number` |  |  | Size of the discontinuous jump (delta-tau). If provided, a structural elasticity is estimated. |
| `poly_order` | `integer` |  | `7` | Polynomial order for the counterfactual distribution. |
| `seed` | `integer` |  | `42` | Random seed for reproducibility. |
| `x` | `string` | ✓ |  | Running variable name (e.g., 'income'). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.notch(x=["treatment", "covariate1", "covariate2"], data=df, notch_point=1.0)
print(result.summary())
```

---
