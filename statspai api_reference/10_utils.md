# utils

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

Utility functions for StatsPAI.

Provides Stata-style data manipulation tools:
- Variable labels (label_var, get_label)
- Pairwise correlation with stars (pwcorr)
- Winsorization (winsor)

**32 个公共函数**

### `sp.describe()`

**Stata-style ``describe`` -- variable names, types, labels, and**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `columns` | `array[string]` |  |  | Subset of columns. Default: all. |
| `df` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.describe(df="value")
print(result.summary())
```

---
### `sp.dgp_bartik()`

**Generate shift-share (Bartik) instrument data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `effect` | `number` |  | `1.0` | True effect of the Bartik instrument on the outcome. |
| `n_industries` | `integer` |  | `10` | Number of industries. |
| `n_regions` | `integer` |  | `50` | Number of regions. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_bartik()
print(result.summary())
```

---
### `sp.dgp_bunching()`

**Generate bunching data around a kink point.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `elasticity` | `number` |  | `0.3` | Behavioral elasticity governing bunching intensity. |
| `kink_point` | `number` |  | `50000.0` | Location of the kink (e.g., tax threshold). |
| `n` | `integer` |  | `10000` | Sample size. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_bunching()
print(result.summary())
```

---
### `sp.dgp_cluster_rct()`

**Generate cluster-randomised trial data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_size` | `integer` |  | `20` | Number of individuals per cluster. |
| `effect` | `number` |  | `0.3` | Treatment effect. |
| `icc` | `number` |  | `0.1` | Intra-cluster correlation coefficient (0-1). |
| `n_clusters` | `integer` |  | `50` | Number of clusters. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_cluster_rct()
print(result.summary())
```

---
### `sp.dgp_did()`

**Generate Difference-in-Differences panel data. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `effect` | `number` |  | `0.5` | Average treatment effect on the treated. |
| `heterogeneous` | `boolean` |  | `False` | If True, the treatment effect varies by unit. |
| `n_groups` | `integer` |  | `4` | Number of treatment-timing groups (used when ``staggered=True``). |
| `n_periods` | `integer` |  | `10` | Number of time periods. |
| `n_units` | `integer` |  | `100` | Number of cross-sectional units. |
| `seed` | `integer` |  |  | Random seed for reproducibility. |
| `staggered` | `boolean` |  | `False` | If True, treatment adoption is staggered across groups. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_did()
print(result.summary())
```

> 📁 See also: `docs/guides/mixtape_ch09_did.md`

---
### `sp.dgp_iv()`

**Generate Instrumental Variables data with endogeneity.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `effect` | `number` |  | `0.5` | True causal effect of treatment on outcome. |
| `first_stage` | `number` |  | `0.4` | Strength of the instrument in the first stage. |
| `n` | `integer` |  | `500` | Sample size. |
| `n_instruments` | `integer` |  | `1` | Number of instruments. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_iv()
print(result.summary())
```

---
### `sp.dgp_observational()`

**Generate observational data with selection on observables.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `confounding` | `number` |  | `0.3` | Strength of confounding (higher = more selection bias). |
| `effect` | `number` |  | `0.5` | True treatment effect. |
| `n` | `integer` |  | `1000` | Sample size. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_observational()
print(result.summary())
```

---
### `sp.dgp_panel()`

**Generate panel data with unit/time fixed effects and AR(1) covariate.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ar1_coef` | `number` |  | `0.5` | AR(1) coefficient for the covariate process. |
| `fe_sd` | `number` |  | `1.0` | Standard deviation of unit fixed effects. |
| `n_periods` | `integer` |  | `20` | Number of time periods. |
| `n_units` | `integer` |  | `100` | Number of units. |
| `seed` | `integer` |  |  | Random seed. |
| `te_sd` | `number` |  | `0.5` | Standard deviation of time fixed effects. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_panel()
print(result.summary())
```

---
### `sp.dgp_rct()`

**Generate Randomised Controlled Trial data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `effect` | `number` |  | `0.3` | Average treatment effect. |
| `heterogeneous` | `boolean` |  | `False` | If True, the treatment effect varies with the first covariate. |
| `n` | `integer` |  | `500` | Sample size. |
| `n_covariates` | `integer` |  | `3` | Number of pre-treatment covariates. |
| `p_treat` | `number` |  | `0.5` | Probability of assignment to treatment. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_rct()
print(result.summary())
```

---
### `sp.dgp_rd()`

**Generate Regression Discontinuity data (sharp or fuzzy).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth_relevant` | `number` |  | `0.5` | Standard deviation of the running variable (controls spread). |
| `cutoff` | `number` |  | `0.0` | RD cutoff value. |
| `effect` | `number` |  | `0.3` | Treatment effect at the cutoff. |
| `fuzzy` | `boolean` |  | `False` | If True, generate a fuzzy RD design. |
| `n` | `integer` |  | `1000` | Sample size. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_rd()
print(result.summary())
```

---
### `sp.dgp_rd_2d()`

**Generate 2D boundary RD data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `effect` | `number` |  | `2.0` | Treatment effect at boundary. |
| `n` | `integer` |  | `2000` | Sample size. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_rd_2d()
print(result.summary())
```

---
### `sp.dgp_rd_hte()`

**Generate RD data with heterogeneous treatment effects.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ate` | `number` |  | `2.0` | Average treatment effect at cutoff. |
| `cutoff` | `number` |  | `0.0` | RD cutoff. |
| `hte_coef` | `number` |  | `1.5` | Slope of heterogeneity w.r.t. covariate z. |
| `n` | `integer` |  | `3000` | Sample size. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_rd_hte()
print(result.summary())
```

---
### `sp.dgp_rd_kink()`

**Generate Regression Kink Design data (Card et al. 2015).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cutoff` | `number` |  | `0.0` | Kink point location. |
| `kink` | `number` |  | `0.8` | True kink in slope at cutoff. |
| `n` | `integer` |  | `2000` | Sample size. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_rd_kink()
print(result.summary())
```

---
### `sp.dgp_rd_multi()`

**Generate multi-cutoff RD data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cutoffs` | `array[string]` |  |  | Cutoff values. Default [0.0, 1.0]. |
| `effects` | `array[string]` |  |  | Treatment effects at each cutoff. Default [2.0, 3.0]. |
| `n` | `integer` |  | `3000` | Sample size. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_rd_multi()
print(result.summary())
```

---
### `sp.dgp_rdit()`

**Generate Regression Discontinuity in Time data (Hausman-Rapson 2018).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cutoff_period` | `integer` |  | `100` | Period of the policy change. |
| `effect` | `number` |  | `2.0` | Treatment effect at the policy change date. |
| `n_periods` | `integer` |  | `200` | Number of time periods. |
| `seasonality` | `boolean` |  | `True` | Include monthly seasonality. |
| `seed` | `integer` |  |  | Random seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_rdit()
print(result.summary())
```

---
### `sp.dgp_synth()`

**Generate synthetic control data with a factor model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `effect` | `number` |  | `0.5` | Treatment effect (additive, constant post-treatment). |
| `n_periods` | `integer` |  | `30` | Number of time periods. |
| `n_units` | `integer` |  | `20` | Number of units (including the treated unit). |
| `seed` | `integer` |  |  | Random seed. |
| `treated_unit` | `integer` |  | `0` | Index of the treated unit. |
| `treatment_time` | `integer` |  | `20` | Period when treatment begins. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dgp_synth()
print(result.summary())
```

---
### `sp.get_label()`

**Get the label for a variable, falling back to the column name.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `df` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `var` | `string` | ✓ |  | var parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.get_label(df="value", var="value")
print(result.summary())
```

---
### `sp.get_labels()`

**Get all variable labels as a dictionary.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `df` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.get_labels(df="value")
print(result.summary())
```

---
### `sp.label_var()`

**Attach a human-readable label to a variable.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `df` | `string` | ✓ |  | DataFrame to label (modified in place). |
| `label` | `string` | ✓ |  | Human-readable label. |
| `var` | `string` | ✓ |  | Column name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.label_var(df="value", var="value", label="value")
print(result.summary())
```

---
### `sp.label_vars()`

**Attach labels to multiple variables at once.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `df` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `labels` | `object` | ✓ |  | {column_name: label_string} mapping. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.label_vars(df="value")
print(result.summary())
```

---
### `sp.outlier_indicator()`

**Flag outlier observations by percentile cutoffs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `combined` | `boolean` |  | `False` | If True, also add a column ``_outlier_any`` marking rows that are outliers on *any* variable. |
| `cuts` | `array[string]` |  | `[1, 99]` | Lower and upper percentile cutoffs. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `vars` | `array[string]` | ✓ |  | Columns to check. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.outlier_indicator(data=df, vars=["a", "b"])
print(result.summary())
```

---
### `sp.pwcorr()`

**Pairwise correlation matrix with significance stars.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `decimals` | `integer` |  | `3` | Decimal places. |
| `method` | `string` |  | `'pearson'` | ``'pearson'``, ``'spearman'``, or ``'kendall'``. |
| `output` | `string` |  | `'text'` | ``'text'``, ``'dataframe'``, ``'latex'``, ``'html'``. |
| `stars` | `boolean` |  | `True` | Show significance stars (* p<0.1, ** p<0.05, *** p<0.01). |
| `vars` | `array[string]` |  |  | Variables to correlate. Default: all numeric columns. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pwcorr(data=df)
print(result.summary())
```

---
### `sp.rank()`

**Rank a variable, optionally within groups.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ascending` | `boolean` |  | `True` | ascending parameter (bool). |
| `by` | `array[string]` |  |  | Group variables. If given, ranks are computed within each group. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string (enum)` |  | `'average'` | Estimator or algorithm variant to use. |
| `var` | `string` | ✓ |  | Column to rank. |

> **method** options: `'average'`, `'min'`, `'max'`, `'dense'`, `'first'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rank(data=df, var="value")
print(result.summary())
```

> 📁 See also: `docs/guides/power_epi.md`

---
### `sp.read_data()`

**Read data from any common format, preserving variable labels.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `encoding` | `string` |  |  | Character encoding (for CSV). |
| `path` | `string` | ✓ |  | File path. Supported: .dta, .csv, .xlsx, .xls, .parquet, .sas7bdat, .sav, .feather, .json. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.read_data(path="value")
print(result.summary())
```

---
### `sp.rowcount()`

**Row-wise count of non-missing values (Stata ``egen rownonmiss``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `vars` | `array[string]` | ✓ |  | vars parameter (Sequence[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rowcount(data=df, vars=["a", "b"])
print(result.summary())
```

---
### `sp.rowmax()`

**Row-wise max across ``vars``, ignoring NaN.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `vars` | `array[string]` | ✓ |  | vars parameter (Sequence[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rowmax(data=df, vars=["a", "b"])
print(result.summary())
```

---
### `sp.rowmean()`

**Row-wise mean across ``vars``, ignoring NaN (Stata ``egen rowmean``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `vars` | `array[string]` | ✓ |  | vars parameter (Sequence[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rowmean(data=df, vars=["a", "b"])
print(result.summary())
```

---
### `sp.rowmin()`

**Row-wise min across ``vars``, ignoring NaN.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `vars` | `array[string]` | ✓ |  | vars parameter (Sequence[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rowmin(data=df, vars=["a", "b"])
print(result.summary())
```

---
### `sp.rowsd()`

**Row-wise standard deviation across ``vars`` (Stata ``egen rowsd``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `vars` | `array[string]` | ✓ |  | vars parameter (Sequence[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rowsd(data=df, vars=["a", "b"])
print(result.summary())
```

---
### `sp.rowtotal()`

**Row-wise sum across ``vars``, treating NaN as 0 (Stata ``egen rowtotal``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `vars` | `array[string]` | ✓ |  | vars parameter (Sequence[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rowtotal(data=df, vars=["a", "b"])
print(result.summary())
```

---
### `sp.scalar_iv_projection()`

**Project a vector of instruments onto a scalar first-stage index.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Exogenous controls to include in the first stage. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `instruments` | `array[string]` | ✓ |  | Excluded-instrument column names. Must have length >= 1. |
| `new_col` | `string` |  |  | Name of the column for the scalar index. Defaults to ``f'{treat}_iv_hat'``. |
| `return_column` | `boolean` |  | `False` | If True, return just the fitted pandas Series. If False, return a copy of ``data`` with the new column appended. |
| `treat` | `string` | ✓ |  | Endogenous treatment variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.scalar_iv_projection(data=df, treat="value", instruments=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.winsor()`

**Winsorize variables at specified percentiles.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cuts` | `array[string]` |  | `[1, 99]` | Lower and upper percentile cutoffs. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `replace` | `boolean` |  | `False` | If True, overwrite original columns. If False, create new columns with ``suffix``. |
| `suffix` | `string` |  | `'_w'` | Suffix for new winsorized columns (when ``replace=False``). |
| `vars` | `array[string]` |  |  | Variables to winsorize. Default: all numeric columns. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.winsor(data=df)
print(result.summary())
```

---
