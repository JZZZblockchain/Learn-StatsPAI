# multilevel

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Multilevel / mixed-effects models.

Exports
-------
mixed, MixedResult                 Linear mixed effects (Gaussian response)
meglm, melogit, mepoisson,
menbreg, megamma, meologit,
MEGLMResult                        Generalised linear mixed models via
                                   Laplace approximation or adaptive
                                   Gauss-Hermite quadrature (``nAGQ``).
icc                                Intra-class correlation with 95% CI
lrtest                             Likelihood-ratio test between two fitted
                                   mixed models (with chi-bar² boundary
                                   correction when variance components are
                                   being tested)

**11 个公共函数**

### `sp.MEGLMResult()`

**Container for GLMM fits (``meglm``, ``melogit``, ``mepoisson``,**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_G` | `string` |  |  | _G parameter (Optional[np.ndarray]). |
| `_alpha` | `number` |  | `0.05` | _alpha parameter (float). |
| `_converged` | `boolean` |  | `True` | _converged parameter (bool). |
| `_cov_fixed` | `string` |  |  | _cov_fixed parameter (Optional[np.ndarray]). |
| `_cov_type` | `string` |  | `'unstructured'` | _cov_type parameter (str). |
| `_dispersion` | `number` |  |  | _dispersion parameter (Optional[float]). |
| `_fixed_names` | `array[string]` |  | `None` | _fixed_names parameter (List[str]). |
| `_group_col` | `string` |  | `''` | Column name for group. |
| `_method` | `string` |  | `'laplace'` | _method parameter (str). |
| `_n_cov_params` | `integer` |  | `0` | _n_cov_params parameter (int). |
| `_offset_name` | `string` |  |  | _offset_name parameter (Optional[str]). |
| `_random_names` | `array[string]` |  | `None` | _random_names parameter (List[str]). |
| `_se_fixed` | `string` |  |  | _se_fixed parameter (pd.Series). |
| `_x_fixed` | `array[string]` |  | `None` | _x_fixed parameter (List[str]). |
| `_x_random` | `array[string]` |  | `None` | _x_random parameter (List[str]). |
| `_y_name` | `string` |  | `''` | _y_name parameter (str). |
| `blups` | `object` | ✓ |  | blups parameter (Dict[Any, np.ndarray]). |
| `family` | `string` |  | `'gaussian'` | family parameter (str). |
| `fixed_effects` | `string` | ✓ |  | fixed_effects parameter (pd.Series). |
| `link` | `string` |  | `'identity'` | link parameter (str). |
| `log_likelihood` | `number` | ✓ |  | log_likelihood parameter (float). |
| `n_groups` | `integer` | ✓ |  | Number of groups. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `random_effects` | `string` | ✓ |  | random_effects parameter (pd.DataFrame). |
| `thresholds` | `string` |  |  | thresholds parameter (Optional[pd.Series]). |
| `variance_components` | `object` | ✓ |  | variance_components parameter (Dict[str, float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MEGLMResult(fixed_effects="value", random_effects="value", n_obs=1.0, n_groups=1.0, log_likelihood=1.0)
print(result.summary())
```

---
### `sp.MixedResult()`

**Container for ``sp.mixed()`` estimation results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_G` | `string` |  | `None` | _G parameter (np.ndarray). |
| `_alpha` | `number` |  | `0.05` | _alpha parameter (float). |
| `_blocks` | `array[string]` |  | `None` | _blocks parameter (List[_GroupBlock]). |
| `_converged` | `boolean` |  | `True` | _converged parameter (bool). |
| `_cov_fixed` | `string` |  | `None` | _cov_fixed parameter (np.ndarray). |
| `_cov_type` | `string` |  | `'unstructured'` | _cov_type parameter (str). |
| `_fixed_names` | `array[string]` |  | `None` | _fixed_names parameter (List[str]). |
| `_group_cols` | `array[string]` |  | `None` | _group_cols parameter (List[str]). |
| `_lr_test` | `object` |  |  | _lr_test parameter (Optional[Dict[str, float]]). |
| `_method` | `string` |  | `'reml'` | _method parameter (str). |
| `_n_cov_params` | `integer` |  | `0` | _n_cov_params parameter (int). |
| `_nakagawa` | `object` |  |  | _nakagawa parameter (Optional[Dict[str, float]]). |
| `_random_names` | `array[string]` |  | `None` | _random_names parameter (List[str]). |
| `_ranef_se` | `string` |  |  | _ranef_se parameter (Optional[pd.DataFrame]). |
| `_se_fixed` | `string` |  |  | _se_fixed parameter (pd.Series). |
| `_sigma2` | `number` |  | `nan` | _sigma2 parameter (float). |
| `_x_fixed` | `array[string]` |  | `None` | _x_fixed parameter (List[str]). |
| `_x_random` | `array[string]` |  | `None` | _x_random parameter (List[str]). |
| `_y_name` | `string` |  | `''` | _y_name parameter (str). |
| `blups` | `object` | ✓ |  | blups parameter (Dict[Any, np.ndarray]). |
| `fixed_effects` | `string` | ✓ |  | fixed_effects parameter (pd.Series). |
| `icc` | `number` | ✓ |  | icc parameter (float). |
| `log_likelihood` | `number` | ✓ |  | log_likelihood parameter (float). |
| `n_groups` | `integer` | ✓ |  | Number of groups. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `random_effects` | `string` | ✓ |  | random_effects parameter (pd.DataFrame). |
| `variance_components` | `object` | ✓ |  | variance_components parameter (Dict[str, float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MixedResult(fixed_effects="value", random_effects="value", n_obs=1.0, n_groups=1.0, icc=1.0, log_likelihood=1.0)
print(result.summary())
```

---
### `sp.icc()`

**Intra-class correlation for a fitted mixed model. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the confidence interval. Default 0.05. |
| `component` | `string` |  | `'_cons'` | Name of the random-effect variance to put in the numerator. Defaults to the random intercept (``"_cons"``). |
| `n_boot` | `integer` |  | `0` | Number of parametric bootstrap replicates used to compute the CI. ``0`` (default) uses the delta-method approximation on the log-variance scale, which is faster and usually within a few decimals of the parametric-bootstrap answer for moderate N. |
| `result` | `string` | ✓ |  | A ``MixedResult`` returned by :func:`statspai.mixed`. |
| `seed` | `integer` |  |  | RNG seed forwarded to :func:`numpy.random.default_rng`. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.icc(result="value")
print(result.summary())
```

---
### `sp.lrtest()`

**Likelihood-ratio test comparing a *restricted* and a *full* model. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `boundary` | `boolean` |  |  | Whether to apply the chi2 boundary correction. When ``None`` (default) we infer it from whether the restriction touches a variance component -- the only parameters that live on the boundary of their support. |
| `full` | `string` | ✓ |  | Two fitted mixed models. ``full`` should strictly nest ``restricted`` -- i.e. the parameter space of the restricted model is a subset of the full model's. |
| `restricted` | `string` | ✓ |  | Two fitted mixed models. ``full`` should strictly nest ``restricted`` -- i.e. the parameter space of the restricted model is a subset of the full model's. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lrtest(restricted="value", full="value")
print(result.summary())
```

---
### `sp.megamma()`

**Random-effects Gamma GLMM with log link (Stata ``meglm`` ``family(gamma)``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `nAGQ` | `integer` |  | `1` | nAGQ parameter (int). |
| `offset` | `string` |  |  | Offset term or offset column. |
| `x_fixed` | `array[string]` | ✓ |  | x_fixed parameter (Sequence[str]). |
| `x_random` | `array[string]` |  |  | x_random parameter (Optional[Sequence[str]]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.megamma(y="outcome", data=df, x_fixed=["a", "b"], group="value")
print(result.summary())
```

---
### `sp.meglm()`

**Fit a generalised linear mixed model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Optimisation controls / CI width. The default ``tol=1e-8`` keeps the Laplace fixed-effect solution aligned with lme4/Stata reference likelihood optima on the parity fixtures. For AGHQ (``nAGQ > 1``), the default optimiser budget is internally tightened to ``maxiter=5000`` and ``tol=1e-12``; explicit user-supplied controls are respected. |
| `cov_type` | `string` |  | `'unstructured'` | Random-effect covariance: ``'unstructured'`` (default), ``'diagonal'``, ``'identity'``. |
| `data` | `string` | ✓ |  | Long-format dataframe. |
| `family` | `string` |  | `'gaussian'` | ``'gaussian'``, ``'binomial'``, ``'poisson'``, ``'gamma'``, or ``'nbinomial'`` (alias ``'negbin'``). |
| `group` | `string` | ✓ |  | Grouping variable for random effects. |
| `maxiter` | `integer` |  | `300` | Optimisation controls / CI width. The default ``tol=1e-8`` keeps the Laplace fixed-effect solution aligned with lme4/Stata reference likelihood optima on the parity fixtures. For AGHQ (``nAGQ > 1``), the default optimiser budget is internally tightened to ``maxiter=5000`` and ``tol=1e-12``; explicit user-supplied controls are respected. |
| `nAGQ` | `integer` |  | `1` | Number of adaptive Gauss-Hermite quadrature points per scalar random effect. ``1`` (default) == Laplace approximation. Use ``nAGQ=7`` to match Stata ``meglm intpoints(7)``; values ``> 1`` require a single scalar random effect (no random slopes). |
| `offset` | `string` |  |  | Column of fixed offsets added to the linear predictor (e.g. ``log(exposure)`` for Poisson rate models). |
| `tol` | `number` |  | `1e-08` | Optimisation controls / CI width. The default ``tol=1e-8`` keeps the Laplace fixed-effect solution aligned with lme4/Stata reference likelihood optima on the parity fixtures. For AGHQ (``nAGQ > 1``), the default optimiser budget is internally tightened to ``maxiter=5000`` and ``tol=1e-12``; explicit user-supplied controls are respected. |
| `trials` | `string` |  |  | Column of trial counts for binomial responses. Defaults to 1 (Bernoulli). |
| `x_fixed` | `array[string]` | ✓ |  | Fixed-effect regressors (intercept added automatically). |
| `x_random` | `array[string]` |  |  | Random-slope variables; defaults to random intercept only. |
| `y` | `string` | ✓ |  | Outcome column. For binomial models this is the number of successes; pair it with ``trials=`` to model proportions. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.meglm(y="outcome", data=df, x_fixed=["a", "b"], group="value")
print(result.summary())
```

---
### `sp.melogit()`

**Random-effects logistic regression (Stata ``melogit``). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `nAGQ` | `integer` |  | `1` | nAGQ parameter (int). |
| `trials` | `string` |  |  | trials parameter (Optional[str]). |
| `x_fixed` | `array[string]` | ✓ |  | x_fixed parameter (Sequence[str]). |
| `x_random` | `array[string]` |  |  | x_random parameter (Optional[Sequence[str]]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.melogit(y="outcome", data=df, x_fixed=["a", "b"], group="value")
print(result.summary())
```

---
### `sp.menbreg()`

**Random-effects negative-binomial regression (Stata ``menbreg``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `nAGQ` | `integer` |  | `1` | nAGQ parameter (int). |
| `offset` | `string` |  |  | Offset term or offset column. |
| `x_fixed` | `array[string]` | ✓ |  | x_fixed parameter (Sequence[str]). |
| `x_random` | `array[string]` |  |  | x_random parameter (Optional[Sequence[str]]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.menbreg(y="outcome", data=df, x_fixed=["a", "b"], group="value")
print(result.summary())
```

---
### `sp.meologit()`

**Random-effects ordinal logit (Stata ``meologit``, R ``ordinal::clmm``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cov_type` | `string` |  | `'unstructured'` | Covariance estimator type. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `maxiter` | `integer` |  | `300` | maxiter parameter (int). |
| `nAGQ` | `integer` |  | `1` | nAGQ parameter (int). |
| `offset` | `string` |  |  | Offset term or offset column. |
| `tol` | `number` |  | `1e-06` | Numerical convergence tolerance. |
| `x_fixed` | `array[string]` | ✓ |  | x_fixed parameter (Sequence[str]). |
| `x_random` | `array[string]` |  |  | x_random parameter (Optional[Sequence[str]]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.meologit(y="outcome", data=df, x_fixed=["a", "b"], group="value")
print(result.summary())
```

---
### `sp.mepoisson()`

**Random-effects Poisson regression (Stata ``mepoisson``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `nAGQ` | `integer` |  | `1` | nAGQ parameter (int). |
| `offset` | `string` |  |  | Offset term or offset column. |
| `x_fixed` | `array[string]` | ✓ |  | x_fixed parameter (Sequence[str]). |
| `x_random` | `array[string]` |  |  | x_random parameter (Optional[Sequence[str]]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mepoisson(y="outcome", data=df, x_fixed=["a", "b"], group="value")
print(result.summary())
```

---
### `sp.mixed()`

**Fit a linear mixed-effects model. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Optimiser controls and inference significance level. The defaults use a tight likelihood tolerance so REML variance components and ICC agree with R ``lme4`` / Stata ``mixed`` on parity fixtures. |
| `cov_type` | `string` |  | `'unstructured'` | Parameterisation of the random-effect covariance matrix *G*: ``'unstructured'`` (default), ``'diagonal'``, or ``'identity'``. |
| `data` | `string` | ✓ |  | Long-format panel / grouped data. |
| `group` | `array[string]` | ✓ |  | Grouping variable. Pass a list like ``["school", "class"]`` to estimate a three-level nested model -- the innermost level is used as the cluster for the random slopes/intercept; the outer levels enter as additional random-intercept blocks. |
| `maxiter` | `integer` |  | `1000` | Optimiser controls and inference significance level. The defaults use a tight likelihood tolerance so REML variance components and ICC agree with R ``lme4`` / Stata ``mixed`` on parity fixtures. |
| `method` | `string` |  | `'reml'` | ``'reml'`` (default) or ``'ml'``. |
| `tol` | `number` |  | `1e-09` | Optimiser controls and inference significance level. The defaults use a tight likelihood tolerance so REML variance components and ICC agree with R ``lme4`` / Stata ``mixed`` on parity fixtures. |
| `x_fixed` | `array[string]` | ✓ |  | Fixed-effect regressors (intercept is added automatically). |
| `x_random` | `array[string]` |  |  | Random-slope variables. ``None`` => random intercept only. |
| `y` | `string` | ✓ |  | Dependent variable column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mixed(y="outcome", data=df, x_fixed=["a", "b"], group=["a", "b"])
print(result.summary())
```

---
