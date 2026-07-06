# regression

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Regression module initialization

**25 个公共函数**

### `sp.GLMEstimator()`

**Generalized Linear Model estimator using IRLS**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GLMEstimator()
print(result.summary())
```

---
### `sp.GLMRegression()`

**Generalized Linear Model with IRLS estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` |  |  | Design matrix (alternative to formula). |
| `data` | `string` |  |  | Data frame containing the variables. |
| `family` | `string` |  | `'gaussian'` | Distribution family. |
| `formula` | `string` |  |  | Model formula (e.g. ``"y ~ x1 + x2"``). |
| `link` | `string` |  |  | Link function (``None`` selects canonical link). |
| `var_names` | `array[string]` |  |  | Variable names when using ``y``/``X`` directly. |
| `y` | `string` |  |  | Response array (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GLMRegression(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.IVRegression()`

**Instrumental Variables regression model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X_endog` | `string` |  |  | Alternative to formula interface. |
| `X_exog` | `string` |  |  | Alternative to formula interface. |
| `Z` | `string` |  |  | Alternative to formula interface. |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` |  |  | Formula with IV syntax: ``"y ~ (endog ~ z1 + z2) + exog1 + exog2"`` |
| `fuller_alpha` | `number` |  | `1.0` | Fuller constant (only used when method='fuller'). ``alpha=1`` gives the bias-corrected Fuller estimator; ``alpha=4`` minimises MSE under normal errors. |
| `method` | `string` |  | `'2sls'` | Estimation method. |
| `var_names` | `object` |  |  | Alternative to formula interface. |
| `y` | `string` |  |  | Alternative to formula interface. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.IVRegression(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.clogit()`

**McFadden's conditional (fixed-effect) logit for choice data. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `data` | `string` |  |  | Long-format data with one row per alternative per choice set. |
| `formula` | `string` |  |  | Formula ``"chosen ~ price + quality"``. |
| `group` | `string` |  |  | Variable identifying the choice set / decision-maker. |
| `maxiter` | `integer` |  | `100` | maxiter parameter (int). |
| `robust` | `string` |  | `'nonrobust'` | Robust standard-error or covariance estimator option. |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `x` | `array[string]` |  |  | Alternative-specific (and/or individual-specific interacted with alternative dummies) covariates. |
| `y` | `string` |  |  | Binary indicator: 1 = chosen, 0 = not chosen. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.clogit(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.cloglog()`

**Complementary log-log regression via maximum likelihood. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `at_values` | `object` |  |  | Variable values for ``marginal_effects='at'``. |
| `cluster` | `string` |  |  | Column name for clustered standard errors. |
| `data` | `string` |  |  | Data containing the variables. |
| `formula` | `string` |  |  | Formula like ``"y ~ x1 + x2"``. |
| `marginal_effects` | `string` |  |  | ``'average'`` (AME), ``'mean'`` (MEM), or ``'at'`` (MER). |
| `maxiter` | `integer` |  | `100` | Maximum Newton-Raphson iterations. |
| `robust` | `string` |  | `'nonrobust'` | ``'nonrobust'`` for MLE SE, ``'hc1'`` / ``'robust'`` for sandwich SE. |
| `tol` | `number` |  | `1e-08` | Convergence tolerance on log-likelihood change. |
| `weights` | `string` |  |  | Column name for frequency/analytic weights. |
| `x` | `array[string]` |  |  | Regressor names (alternative to formula). |
| `y` | `string` |  |  | Dependent variable name (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cloglog(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.glm()`

**Fit a Generalized Linear Model. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` |  |  | Variable name for clustered standard errors. |
| `data` | `string` |  |  | Data frame containing the variables. |
| `exposure` | `string` |  |  | Variable name for exposure (``log(exposure)`` is added as offset). |
| `family` | `string` |  | `'gaussian'` | Distribution family. One of ``"gaussian"``, ``"binomial"``, ``"poisson"``, ``"gamma"``, ``"inverse_gaussian"``, ``"negative_binomial"``. |
| `formula` | `string` |  |  | Model formula (e.g. ``"y ~ x1 + x2"``). |
| `link` | `string` |  |  | Link function. If ``None`` the canonical link for the chosen family is used. Options: ``"identity"``, ``"log"``, ``"logit"``, ``"probit"``, ``"inverse"``, ``"cloglog"``, ``"power"``, ``"sqrt"``. |
| `maxiter` | `integer` |  | `100` | Maximum number of IRLS iterations. |
| `offset` | `string` |  |  | Variable name for offset. |
| `robust` | `string` |  | `'nonrobust'` | Standard-error type (``"nonrobust"``, ``"hc0"``-``"hc3"``, ``"hac"``). |
| `tol` | `number` |  | `1e-08` | Convergence tolerance on the relative change in deviance. |
| `weights` | `string` |  |  | Variable name for observation weights. |
| `x` | `array[string]` |  |  | Names of independent variables (alternative to formula). |
| `y` | `string` |  |  | Name of the dependent variable (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.glm(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.heckman()`

**Heckman two-step selection model correcting for sample selection bias. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `select` | `string` | ✓ |  | Binary selection indicator (1 = observed, 0 = not) |
| `x` | `array[string]` | ✓ |  | Regressors in the outcome equation |
| `y` | `string` | ✓ |  | Outcome variable (observed only when select=1) |
| `z` | `array[string]` | ✓ |  | Selection-equation variables (include exclusion restrictions in z but not x) |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.heckman(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, select="value", z=["a", "b"])
print(result.summary())
```

---
### `sp.hurdle()`

**Hurdle (two-part) model for count data. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `count_model` | `string` |  | `'poisson'` | Count distribution: "poisson" or "negbin". |
| `data` | `string` |  |  | Dataset. |
| `formula` | `string` |  |  | Patsy-style formula. |
| `maxiter` | `integer` |  | `200` | maxiter parameter (int). |
| `robust` | `string` |  | `'nonrobust'` | Robust standard-error or covariance estimator option. |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `x` | `array[string]` |  |  | Regressors (used for both hurdle and count parts). |
| `y` | `string` |  |  | Dependent variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.hurdle(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.iv()`

**Unified IV estimation: 2SLS, LIML, Fuller, GMM, JIVE. Includes first-stage F, Sargan/Hansen J, and Hausman diagnostics. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Column name for cluster-robust SEs |
| `data` | `string` | ✓ |  | pandas DataFrame |
| `formula` | `string` | ✓ |  | IV formula: 'y ~ (endog ~ instruments) + exog' |
| `fuller_alpha` | `number` |  | `1.0` | Fuller constant (method='fuller' only) |
| `method` | `string (enum)` |  | `'2sls'` | Estimation method |
| `robust` | `string (enum)` |  | `'nonrobust'` | Standard error type |

> **method** options: `'2sls'`, `'liml'`, `'fuller'`, `'gmm'`, `'jive'`

> **robust** options: `'nonrobust'`, `'hc0'`, `'hc1'`, `'hc2'`, `'hc3'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.iv(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/diagnostics.md`, `docs/guides/exporting-regression-tables.md`

---
### `sp.ivreg()`

**Two-stage least squares (2SLS) IV regression. Alias for sp.iv(method='2sls'). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame |
| `formula` | `string` | ✓ |  | IV formula: 'y ~ (endog ~ instruments) + exog' |
| `robust` | `string` |  | `'nonrobust'` | Standard error type |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ivreg(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `card_iv.py`, `docs/guides/choosing_iv_estimator.md`, `docs/guides/diagnostics.md`

---
### `sp.logit()`

**Logit (logistic) regression via maximum likelihood. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `at_values` | `object` |  |  | Variable values for ``marginal_effects='at'``. |
| `cluster` | `string` |  |  | Column name for clustered standard errors. |
| `data` | `string` |  |  | Data containing the variables. |
| `formula` | `string` |  |  | Formula like ``"y ~ x1 + x2"``. |
| `marginal_effects` | `string` |  |  | ``'average'`` (AME), ``'mean'`` (MEM), or ``'at'`` (MER). |
| `maxiter` | `integer` |  | `100` | Maximum Newton-Raphson iterations. |
| `odds_ratio` | `boolean` |  | `False` | Report odds ratios instead of log-odds coefficients. |
| `robust` | `string` |  | `'nonrobust'` | ``'nonrobust'`` for MLE SE, ``'hc1'`` / ``'robust'`` for sandwich SE. |
| `tol` | `number` |  | `1e-08` | Convergence tolerance on log-likelihood change. |
| `weights` | `string` |  |  | Column name for frequency/analytic weights. |
| `x` | `array[string]` |  |  | Regressor names (alternative to formula). |
| `y` | `string` |  |  | Dependent variable name (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.logit(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.mlogit()`

**Multinomial logit for J > 2 unordered categories via MLE. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `base` | `integer` |  | `0` | Base / reference category (index into sorted unique values). |
| `cluster` | `string` |  |  | Cluster variable for clustered SE. |
| `data` | `string` |  |  | Data. |
| `formula` | `string` |  |  | Formula ``"y ~ x1 + x2"``. |
| `maxiter` | `integer` |  | `100` | maxiter parameter (int). |
| `robust` | `string` |  | `'nonrobust'` | ``"robust"`` / ``"HC1"`` for Huber-White sandwich SE. |
| `rrr` | `boolean` |  | `False` | Report Relative Risk Ratios (exp(beta)) instead of coefficients. |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `x` | `array[string]` |  |  | Regressors. |
| `y` | `string` |  |  | Dependent variable (categorical, integer-coded). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mlogit(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.nbreg()`

**Negative-binomial count regression for overdispersed non-negative outcomes. Formula fixed effects such as 'y ~ x | id' are implemented with explicit dummies for moderate panels. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Column name for cluster-robust SEs |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `dispersion` | `string (enum)` |  | `'mean'` | Negative-binomial parameterisation |
| `exposure` | `string` |  |  | Positive exposure column |
| `formula` | `string` | ✓ |  | Formula such as 'count ~ x1 + x2 \| id' |
| `irr` | `boolean` |  | `False` | Report incidence-rate ratios |
| `offset` | `string` |  |  | Column containing a log offset |
| `robust` | `string (enum)` |  | `'nonrobust'` | Standard error type |

> **dispersion** options: `'mean'`, `'constant'`

> **robust** options: `'nonrobust'`, `'robust'`, `'hc0'`, `'hc1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.nbreg(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.ologit()`

**Ordered logit (proportional odds) model via MLE. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` |  |  | Formula ``"y ~ x1 + x2"``. |
| `maxiter` | `integer` |  | `100` | maxiter parameter (int). |
| `robust` | `string` |  | `'nonrobust'` | Robust standard-error or covariance estimator option. |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `x` | `array[string]` |  |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` |  |  | Ordered categorical dependent variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ologit(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.oprobit()`

**Ordered probit model via MLE. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` |  |  | Formula ``"y ~ x1 + x2"``. |
| `maxiter` | `integer` |  | `100` | maxiter parameter (int). |
| `robust` | `string` |  | `'nonrobust'` | Robust standard-error or covariance estimator option. |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `x` | `array[string]` |  |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` |  |  | Ordered categorical dependent variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.oprobit(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.poisson()`

**Poisson regression via MLE (IRLS). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` |  |  | Variable name for clustered standard errors. |
| `data` | `string` |  |  | Data containing all variables. |
| `exposure` | `string` |  |  | Exposure variable (will be logged and used as offset). |
| `formula` | `string` |  |  | Model formula, e.g. "y ~ x1 + x2". |
| `irr` | `boolean` |  | `False` | If True, report Incidence Rate Ratios (exp(beta)) instead of raw coefficients. |
| `maxiter` | `integer` |  | `100` | Maximum IRLS iterations. |
| `offset` | `string` |  |  | Offset variable (log of exposure already computed). |
| `robust` | `string` |  | `'nonrobust'` | Standard error type: "nonrobust", "robust"/"hc0", "hc1". |
| `tol` | `number` |  | `1e-08` | Convergence tolerance. |
| `weights` | `string` |  |  | Frequency/analytic weight variable. |
| `x` | `array[string]` |  |  | Independent variable names (alternative to formula). |
| `y` | `string` |  |  | Dependent variable name (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.poisson(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.ppmlhdfe()`

**Pseudo-Poisson Maximum Likelihood with high-dimensional fixed effects. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `absorb` | `string` |  |  | Fixed effects to absorb, e.g. ``"origin + destination + year"``. Overrides any FE specification in the formula. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `array[string]` |  |  | Variable name for clustered standard errors (recommended for gravity models, e.g. cluster on country-pair). A pair ``cluster=["a", "b"]`` requests two-way clustering (Cameron-Gelbach-Miller 2011 inclusion-exclusion with the single ``G_min/(G_min-1)`` small-sample factor -- byte-identical to Stata ``ppmlhdfe ..., cluster(a b)``). |
| `conley_cutoff` | `number` |  |  | conley_cutoff parameter (Optional[float]). |
| `conley_lat` | `string` |  |  | conley_lat parameter (Optional[str]). |
| `conley_lon` | `string` |  |  | conley_lon parameter (Optional[str]). |
| `data` | `string` |  |  | Data containing all variables. |
| `formula` | `string` |  |  | Model formula. Fixed effects can be specified via ``\|``: ``"trade ~ dist + contig \| origin + destination + year"`` |
| `maxiter` | `integer` |  | `1000` | Maximum IRLS iterations. |
| `robust` | `string` |  | `'robust'` | Default is robust SE (as in Stata's ppmlhdfe). Options: "robust"/"hc0", "hc1", "nonrobust". |
| `seed` | `integer` |  |  | RNG seed for sampled (non-enumerated) wild draws. |
| `separation` | `boolean` |  | `True` | If True, check for separation (perfect prediction of zeros) and warn. Observations causing separation are not dropped automatically. |
| `tol` | `number` |  | `1e-08` | Convergence tolerance. |
| `vce` | `string` |  |  | Canonical SE-menu keyword. ``"robust"``/``"hc1"``/``"hc0"`` alias the ``robust=`` parameter. ``"wild"`` (with ``cluster=``) runs the boottest-convention score wild cluster bootstrap on the FE-absorbed design -- exact at any FE dimensionality (the weighted-FWL reduction of the score numerator is exact) and byte-identical to ``sp.fepois(vce="wild")`` on low-dimensional FE. ``"CR2"``/``"CR3"``/``"jackknife"`` (with ``cluster=``) compute the clubSandwich glm bias-reduced SEs on the FE-as-dummies design (guarded against high-dimensional FE). |
| `weights` | `string` |  |  | Weight variable name. |
| `wild_reps` | `integer` |  | `9999` | Replications for ``vce="wild"`` (enumerates the 2^G grid when ``2**G <= wild_reps``). |
| `wild_weight_type` | `string` |  | `'rademacher'` | Wild weight distribution. |
| `x` | `array[string]` |  |  | Independent variable names (alternative to formula). |
| `y` | `string` |  |  | Dependent variable name (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ppmlhdfe(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/grammar.md`, `docs/guides/panel_data.md`

---
### `sp.probit()`

**Probit regression via maximum likelihood. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `at_values` | `object` |  |  | Variable values for ``marginal_effects='at'``. |
| `cluster` | `string` |  |  | Column name for clustered standard errors. |
| `data` | `string` |  |  | Data containing the variables. |
| `formula` | `string` |  |  | Formula like ``"y ~ x1 + x2"``. |
| `marginal_effects` | `string` |  |  | ``'average'`` (AME), ``'mean'`` (MEM), or ``'at'`` (MER). |
| `maxiter` | `integer` |  | `100` | Maximum Newton-Raphson iterations. |
| `robust` | `string` |  | `'nonrobust'` | ``'nonrobust'`` for MLE SE, ``'hc1'`` / ``'robust'`` for sandwich SE. |
| `tol` | `number` |  | `1e-08` | Convergence tolerance on log-likelihood change. |
| `weights` | `string` |  |  | Column name for frequency/analytic weights. |
| `x` | `array[string]` |  |  | Regressor names (alternative to formula). |
| `y` | `string` |  |  | Dependent variable name (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.probit(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/decomposition_family.md`

---
### `sp.qreg()`

**Quantile regression at specified quantile(s). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` |  |  | 'y ~ x1 + x2' (alternative to y/x) |
| `quantile` | `number` |  | `0.5` | Quantile (0-1) |
| `x` | `array[string]` |  |  | Regressor columns (alternative to formula) |
| `y` | `string` |  |  | Outcome column (alternative to formula) |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.qreg(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.regress()`

**OLS regression with robust/clustered standard errors. The workhorse of econometric analysis. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Column name for cluster-robust SEs |
| `data` | `string` | ✓ |  | pandas DataFrame with variables |
| `formula` | `string` | ✓ |  | R-style formula, e.g. 'y ~ x1 + x2' |
| `robust` | `string (enum)` |  | `'nonrobust'` | Standard error type |

> **robust** options: `'nonrobust'`, `'hc0'`, `'hc1'`, `'hc2'`, `'hc3'`, `'hac'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.regress(formula="lwage ~ x1 + x2", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/assimilative_ci.md`, `docs/guides/choosing_iv_estimator.md`, `docs/guides/exporting-regression-tables.md`

---
### `sp.sqreg()`

**Simultaneous quantile regression at multiple quantiles.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `quantiles` | `array[string]` |  |  | quantiles parameter (Optional[List[float]]). |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sqreg(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.tobit()`

**Tobit model for censored dependent variables. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `ll` | `number` |  | `0.0` | Lower censoring limit (set -inf for none) |
| `ul` | `number` |  |  | Upper censoring limit (default: none) |
| `x` | `array[string]` | ✓ |  | Regressors |
| `y` | `string` | ✓ |  | Censored outcome variable |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.tobit(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.xtnbreg()`

**Panel negative-binomial regression. model='fe' uses explicit entity fixed effects through nbreg; model='re' dispatches to the random-intercept NB-2 GLMM menbreg.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Cluster variable; defaults to entity for FE |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `entity` | `string` | ✓ |  | Panel/unit identifier |
| `exposure` | `string` |  |  | Exposure term or exposure column. |
| `formula` | `string` | ✓ |  | Formula such as 'count ~ x1 + x2' |
| `irr` | `boolean` |  | `False` | irr parameter (bool). |
| `model` | `string (enum)` |  | `'fe'` | Panel model |
| `offset` | `string` |  |  | Offset term or offset column. |
| `time` | `string` |  |  | Optional time column |
| `time_effects` | `boolean` |  | `False` | Include time dummies for model='fe' |

> **model** options: `'fe'`, `'re'`, `'pooled'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.xtnbreg(formula="lwage ~ x1 + x2", data=df, entity="value")
print(result.summary())
```

---
### `sp.zinb()`

**Zero-Inflated Negative Binomial (ZINB) regression via MLE. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster variable name. |
| `data` | `string` |  |  | Dataset. |
| `formula` | `string` |  |  | Patsy-style formula for the count equation. |
| `inflate` | `array[string]` |  |  | Inflation-equation regressors. Default: same as count regressors. |
| `maxiter` | `integer` |  | `200` | maxiter parameter (int). |
| `robust` | `string` |  | `'nonrobust'` | Standard error type. |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `x` | `array[string]` |  |  | Count-equation regressors. |
| `y` | `string` |  |  | Dependent variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.zinb(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
### `sp.zip_model()`

**Zero-Inflated Poisson (ZIP) regression via MLE. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` |  |  | Cluster variable name for clustered standard errors. |
| `data` | `string` |  |  | Dataset. |
| `formula` | `string` |  |  | Patsy-style formula for the count equation, e.g. "y ~ x1 + x2". |
| `inflate` | `array[string]` |  |  | Inflation-equation regressors. Default: same as count regressors. |
| `maxiter` | `integer` |  | `200` | Maximum iterations for optimizer. |
| `robust` | `string` |  | `'nonrobust'` | "nonrobust", "HC0", "HC1", etc. |
| `tol` | `number` |  | `1e-08` | Convergence tolerance. |
| `x` | `array[string]` |  |  | Count-equation regressors (alternative to formula). |
| `y` | `string` |  |  | Dependent variable name (alternative to formula). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.zip_model(formula="y ~ x1 + x2", data=df)
print(result.summary())
```

---
