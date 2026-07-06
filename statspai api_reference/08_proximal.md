# proximal

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Proximal Causal Inference (Tchetgen Tchetgen et al. 2020).

Identifies the ATE in the presence of an *unmeasured* confounder :math:`U`,
using two proxies of :math:`U`:

* :math:`Z` — "treatment-inducing confounding proxy" (independent of Y | D, U)
* :math:`W` — "outcome-inducing confounding proxy" (independent of D | U)

plus measured covariates :math:`X`.

**13 个公共函数**

### `sp.NegativeControlResult()`

**Unified result for negative-control procedures.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `interpretation` | `string` |  | `''` | interpretation parameter (str). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_obs` | `integer` |  | `0` | Number of obs. |
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

result = sp.NegativeControlResult(method="value", estimate=1.0, se=1.0, pvalue=1.0, ci=["a", "b"])
print(result.summary())
```

---
### `sp.ProximalCausalInference()`

**Class wrapper for :func:`proximal`.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ProximalCausalInference()
print(result.summary())
```

---
### `sp.ProximalRegResult()`

**Result of the regression-based proximal causal inference estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ate` | `number` | ✓ |  | ate parameter (float). |
> 📝 *ate 参数（浮点数）。*
| `bridge_coefs` | `object` | ✓ |  | bridge_coefs parameter (Dict[str, float]). |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `propensity_coefs` | `object` | ✓ |  | propensity_coefs parameter (Dict[str, float]). |
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

result = sp.ProximalRegResult(ate=1.0, se=1.0, ci=["a", "b"], pvalue=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.ProxyScoreResult()`

**Per-candidate proxy score for PCI.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `recommended_w` | `array[string]` | ✓ |  | recommended_w parameter (List[str]). |
| `recommended_z` | `array[string]` | ✓ |  | recommended_z parameter (List[str]). |
| `w_candidates` | `string` | ✓ |  | w_candidates parameter (pd.DataFrame). |
| `z_candidates` | `string` | ✓ |  | z_candidates parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ProxyScoreResult(z_candidates="value", w_candidates="value", recommended_z=["a", "b"], recommended_w=["a", "b"])
print(result.summary())
```

---
### `sp.bidirectional_pci()`

**Bidirectional proximal causal inference (Min, Zhang & Luo 2025). Solves for both outcome and treatment bridges simultaneously in a single two-way regression system. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `proxy_w` | `array[string]` | ✓ |  | proxy_w parameter (list). |
| `proxy_z` | `array[string]` | ✓ |  | proxy_z parameter (list). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bidirectional_pci(y="outcome", data=df, treat="value", proxy_z=["a", "b"], proxy_w=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/proximal_family.md`

---
### `sp.double_negative_control()`

**Double negative control estimator (Miao et al. 2018; Shi et al. 2020).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `nce` | `string` | ✓ |  | nce parameter (str). |
| `nco` | `string` | ✓ |  | nco parameter (str). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.double_negative_control(y="outcome", data=df, treat="value", nce="value", nco="value")
print(result.summary())
```

> 📁 See also: `docs/guides/proximal_family.md`

---
### `sp.fortified_pci()`

**Fortified proximal causal inference (Yu, Shi & Tchetgen Tchetgen 2025). Adds a bridge-function stability constraint that gives robust ATT under mild misspecification of the outcome/treatment bridge. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `proxy_w` | `array[string]` | ✓ |  | Outcome-side proxies |
| `proxy_z` | `array[string]` | ✓ |  | Treatment-side proxies |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.fortified_pci(y="outcome", data=df, treat="value", proxy_z=["a", "b"], proxy_w=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/proximal_family.md`

---
### `sp.negative_control_exposure()`

**Regress outcome on a *negative-control exposure*.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `nce` | `string` | ✓ |  | nce parameter (str). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.negative_control_exposure(y="outcome", data=df, nce="value")
print(result.summary())
```

---
### `sp.negative_control_outcome()`

**Lipsitch-style NCO calibration.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Measured confounders to condition on. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `nco` | `string` | ✓ |  | Negative-control outcome -- a variable plausibly unaffected by the true treatment but sharing confounders with the real Y. |
| `treat` | `string` | ✓ |  | Treatment indicator or exposure variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.negative_control_outcome(data=df, nco="value", treat="value")
print(result.summary())
```

---
### `sp.pci_mtp()`

**Proximal causal inference for modified treatment policies (Park & Ying 2025). Estimates the effect of a policy that shifts the treatment distribution (e.g., raises the dose by 10%) under unobserved confounding identified by PCI.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `delta` | `number` | ✓ |  | Additive shift applied to the treatment under the modified policy |
| `proxy_w` | `array[string]` | ✓ |  | proxy_w parameter (list). |
| `proxy_z` | `array[string]` | ✓ |  | proxy_z parameter (list). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pci_mtp(y="outcome", data=df, treat="value", proxy_z=["a", "b"], proxy_w=["a", "b"], delta=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/proximal_family.md`

---
### `sp.proximal()`

**Proximal Causal Inference via linear 2SLS on the outcome bridge. Identifies ATE with unmeasured confounding using two proxy variables: a treatment-side Z (instrument for W) and an outcome-side W (endogenous bridge regressor). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bridge` | `string (enum)` |  | `'linear'` | Bridge function family |
| `covariates` | `array[string]` |  |  | Baseline covariates |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_boot` | `integer` |  | `0` | Bootstrap SE replications |
| `proxy_w` | `array[string]` | ✓ |  | Outcome-side proxies (endogenous) |
| `proxy_z` | `array[string]` | ✓ |  | Treatment-side proxies (instruments for W) |
| `treat` | `string` | ✓ |  | Treatment |
| `y` | `string` | ✓ |  | Outcome |

> **bridge** options: `'linear'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.proximal(y="outcome", data=df, treat="value", proxy_z=["a", "b"], proxy_w=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/proximal_family.md`

---
### `sp.proximal_regression()`

**Doubly-robust regression-based PCI estimator for the ATE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Measured covariates X. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `propensity_bounds` | `array[string]` |  | `[0.02, 0.98]` | propensity_bounds parameter (tuple). |
| `treat` | `string` | ✓ |  | Binary treatment column. |
| `w_proxy` | `string` | ✓ |  | Outcome-inducing confounding proxy W. |
| `y` | `string` | ✓ |  | Outcome column. |
| `z_proxy` | `string` | ✓ |  | Treatment-inducing confounding proxy Z. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.proximal_regression(y="outcome", data=df, treat="value", z_proxy="value", w_proxy="value")
print(result.summary())
```

---
### `sp.select_pci_proxies()`

**Score and rank candidate proxies for PCI.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `candidates` | `array[string]` | ✓ |  | All variables that could plausibly serve as proxies. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `top_k` | `integer` |  | `2` | Number of top candidates to recommend per side. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.select_pci_proxies(y="outcome", data=df, treat="value", candidates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/proximal_family.md`

---
