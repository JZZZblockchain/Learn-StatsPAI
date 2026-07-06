# mht

> 📂 所属分类:04 · 诊断、稳健性与推断 (Diagnostics, Robustness & Inference)

Multiple Hypothesis Testing (MHT) module for StatsPAI.

Provides corrections for simultaneous inference across many outcomes or
subgroups --- the single most common gap when Python users replicate
empirical economics workflows that rely on Stata's ``rwolf`` or ``wyoung``.

Estimators and utilities:

- **Romano-Wolf stepdown** (Romano & Wolf 2005, 2016) --- bootstrap
  FWER control that exploits dependence across test statistics.
- **Westfall-Young maxT** (Westfall & Young 1993) --- single-step
  resampling-based FWER control.
- **Bonferroni**, **Holm** (1979), **Benjamini-Hochberg** (1995) ---
  classical non-resampling adjustments included for comparison.
- ``adjust_pvalues()`` --- convenience dispatcher across all methods.

**6 个公共函数**

### `sp.RomanoWolfResult()`

**Container for Romano-Wolf multiple hypothesis testing results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n_boot` | `integer` | ✓ |  | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `n_outcomes` | `integer` | ✓ |  | Number of outcomes. |
| `table` | `string` | ✓ |  | table parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RomanoWolfResult(table="value", n_outcomes=1.0, n_boot=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.adjust_pvalues()`

**Adjust p-values for multiple comparisons. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `method` | `string` |  | `'holm'` | Adjustment method. One of: - ``'bonferroni'`` -- Bonferroni correction. - ``'holm'`` -- Holm (1979) step-down. - ``'bh'`` or ``'fdr'`` -- Benjamini-Hochberg FDR. For Romano-Wolf or Westfall-Young adjustments (which require the original data and bootstrap), use :func:`romano_wolf` directly. |
| `pvalues` | `string` | ✓ |  | Unadjusted p-values. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.adjust_pvalues(pvalues="value")
print(result.summary())
```

---
### `sp.benjamini_hochberg()`

**Benjamini-Hochberg (1995) FDR correction. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `pvalues` | `string` | ✓ |  | Unadjusted p-values. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.benjamini_hochberg(pvalues="value")
print(result.summary())
```

---
### `sp.bonferroni()`

**Bonferroni correction: ``p_adj = min(p * S, 1)``. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `pvalues` | `string` | ✓ |  | Unadjusted p-values. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bonferroni(pvalues="value")
print(result.summary())
```

---
### `sp.holm()`

**Holm (1979) step-down correction. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `pvalues` | `string` | ✓ |  | Unadjusted p-values. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.holm(pvalues="value")
print(result.summary())
```

---
### `sp.romano_wolf()`

**Romano-Wolf stepdown adjusted p-values for multiple outcomes. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Nominal significance level (used only for display). |
| `cluster` | `string` |  |  | Column name for cluster-robust standard errors and cluster bootstrap resampling. |
| `controls` | `array[string]` |  |  | Additional control variables included in every regression. |
| `data` | `string` | ✓ |  | Analysis data (complete cases used; rows with NaN in any relevant column are dropped). |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications. |
| `seed` | `integer` |  |  | Random seed for reproducibility (uses ``np.random.default_rng``). |
| `x` | `array[string]` | ✓ |  | Treatment / regressor(s) of interest. The adjusted p-value corresponds to the *first* element of ``x``. |
| `y` | `array[string]` | ✓ |  | Outcome variable names (one regression per outcome). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.romano_wolf(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
