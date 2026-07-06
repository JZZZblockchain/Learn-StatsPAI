# rlasso

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Rigorous (data-driven) Lasso — a faithful port of R's ``hdm`` package.

Public surface
--------------
- :func:`rlasso` — rigorous (post-)Lasso with a data-driven, theory-
  justified penalty (``hdm::rlasso``).
- :func:`rlasso_effect` / :func:`rlasso_effects` — treatment-effect
  inference after Lasso-selecting controls (``hdm::rlassoEffect(s)``).
- :func:`rlasso_iv` — instrumental-variables estimation with Lasso
  selection of instruments and/or controls (``hdm::rlassoIV``).
- :class:`RlassoRegressor` / :class:`RlassoClassifier` — scikit-learn
  adapters so the rigorous Lasso can serve as a Double-ML nuisance
  learner (``sp.dml(..., ml_g='rlasso')``).

Every estimator is validated to agree numerically with ``hdm`` (see
``tests/reference_parity/test_rlasso_parity.py``): the core ``rlasso``
matches to machine precision; the IV/effect estimators to ~1e-6.

References
----------
Chernozhukov, V., Hansen, C. and Spindler, M. (2016). "hdm:
    High-Dimensional Metrics." *The R Journal*, 8(2), 185-199.
    [@chernozhukov2016hdm]

**10 个公共函数**

### `sp.RlassoClassifier()`

**Linear-probability classifier backed by the rigorous Lasso.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `c` | `number` |  | `1.1` | c parameter (float). |
| `clip` | `number` |  | `0.001` | clip parameter (float). |
| `gamma` | `number` |  |  | gamma parameter (Optional[float]). |
| `homoscedastic` | `boolean` |  | `False` | homoscedastic parameter (bool). |
| `intercept` | `boolean` |  | `True` | intercept parameter (bool). |
| `lambda_start` | `number` |  |  | lambda_start parameter (Optional[float]). |
| `num_iter` | `integer` |  | `15` | num_iter parameter (int). |
| `post` | `boolean` |  | `True` | post parameter (bool). |
| `tol` | `number` |  | `1e-05` | Numerical convergence tolerance. |
> 📝 *数值收敛容差。*
| `x_dependent` | `boolean` |  | `False` | x_dependent parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RlassoClassifier()
print(result.summary())
```

---
### `sp.RlassoRegressor()`

**Rigorous (post-)Lasso as a scikit-learn regressor.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `c` | `number` |  | `1.1` | c parameter (float). |
| `gamma` | `number` |  |  | gamma parameter (Optional[float]). |
| `homoscedastic` | `boolean` |  | `False` | homoscedastic parameter (bool). |
| `intercept` | `boolean` |  | `True` | intercept parameter (bool). |
| `lambda_start` | `number` |  |  | lambda_start parameter (Optional[float]). |
| `num_iter` | `integer` |  | `15` | num_iter parameter (int). |
| `post` | `boolean` |  | `True` | post parameter (bool). |
| `tol` | `number` |  | `1e-05` | Numerical convergence tolerance. |
> 📝 *数值收敛容差。*
| `x_dependent` | `boolean` |  | `False` | x_dependent parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RlassoRegressor()
print(result.summary())
```

---
### `sp.RlassologitClassifier()`

**Logistic rigorous-Lasso classifier -- a genuine (calibrated) propensity.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `c` | `number` |  |  | c parameter (Optional[float]). |
| `clip` | `number` |  | `1e-05` | clip parameter (float). |
| `gamma` | `number` |  |  | gamma parameter (Optional[float]). |
| `intercept` | `boolean` |  | `True` | intercept parameter (bool). |
| `lambda_` | `number` |  |  | lambda_ parameter (Optional[float]). |
| `post` | `boolean` |  | `True` | post parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RlassologitClassifier()
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`

---
### `sp.rlasso()`

**Rigorous Lasso / post-Lasso -- a faithful port of ``hdm::rlasso``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Design matrix of candidate covariates (``p`` may exceed ``n``). |
| `colnames` | `array[string]` |  |  | Names for the columns of ``X`` (default ``V1..Vp``). |
| `control` | `object` |  |  | Overrides for ``numIter`` (default 15), ``tol`` (default 1e-5) and ``threshold`` (default ``None``). |
| `intercept` | `boolean` |  | `True` | Center ``X`` and ``y`` and report an intercept on the original scale. |
| `penalty` | `object` |  |  | Overrides for ``homoscedastic`` (``True`` / ``False`` / ``"none"``), ``X.dependent.lambda`` (bool), ``c`` (slack, default 1.1), ``gamma`` (default ``0.1/log(n)``), ``lambda.start`` and ``numSim``. Defaults reproduce hdm exactly. |
| `post` | `boolean` |  | `True` | If ``True``, re-estimate the selected support by OLS (post-Lasso). |
| `rng` | `string` |  |  | Only used when ``X.dependent.lambda`` simulation is requested. |
| `y` | `string` | ✓ |  | Response. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rlasso(y="outcome", X="value")
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`, `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.rlasso_effect()`

**Effect of ``d`` on ``y`` after Lasso-selecting controls ``x``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `I3` | `string` |  |  | Amelioration set forced into the control set (double-selection only) -- hdm's ``I3`` argument. |
| `control` | `object` |  |  | Forwarded to :func:`statspai.rlasso.rlasso`. |
| `d` | `string` | ✓ |  | d parameter (Union[np.ndarray, pd.Series, str]). |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `method` | `string` |  | `'partialling out'` | See the module docstring. |
| `penalty` | `object` |  |  | Forwarded to :func:`statspai.rlasso.rlasso`. |
| `post` | `boolean` |  | `True` | Post-Lasso inside the selection steps. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rlasso_effect(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, d="value")
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`

---
### `sp.rlasso_effects()`

**Estimate the effect of each targeted column of ``X`` on ``y``. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `control` | `object` |  |  | control parameter (Optional[Dict[str, Any]]). |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `index` | `array[string]` |  |  | index parameter (Optional[Sequence[int]]). |
| `method` | `string` |  | `'partialling out'` | Estimator or algorithm variant to use. |
| `penalty` | `object` |  |  | penalty parameter (Optional[Dict[str, Any]]). |
| `post` | `boolean` |  | `True` | post parameter (bool). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rlasso_effects(y="outcome", data=df, X="value")
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`

---
### `sp.rlasso_iv()`

**Instrumental-variables estimation with rigorous-Lasso selection.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `control` | `object` |  |  | Forwarded to :func:`statspai.rlasso.rlasso` (penalty level, loadings, iteration controls). |
| `d` | `string` | ✓ |  | name). |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `intercept` | `boolean` |  | `True` | Passed to the underlying ``rlasso`` first stages. |
| `penalty` | `object` |  |  | Forwarded to :func:`statspai.rlasso.rlasso` (penalty level, loadings, iteration controls). |
| `post` | `boolean` |  | `True` | Post-Lasso (OLS refit) inside every selection step. |
| `select_X` | `boolean` |  | `True` | Lasso-select among the controls (partialling-out). |
| `select_Z` | `boolean` |  | `True` | Lasso-select among the instruments. |
| `x` | `array[string]` |  |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | name). |
| `z` | `array[string]` | ✓ |  | Instrument, proxy, or auxiliary variable used by this estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rlasso_iv(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, d="value", z=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`, `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.rlassologit()`

**Logistic rigorous (post-)Lasso -- a faithful port of ``hdm::rlassologit``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `colnames` | `array[string]` |  |  | Column names (default ``V1..Vp``). |
| `control` | `object` |  |  | ``threshold`` -- coefficients below it are zeroed (default None). |
| `intercept` | `boolean` |  | `True` | Include an intercept. |
| `penalty` | `object` |  |  | Overrides for ``c`` (slack; default 1.1 for ``post=True``, else 0.5), ``gamma`` (default ``0.1/log n``) and ``lambda`` (raw penalty; bypasses the data-driven level). |
| `post` | `boolean` |  | `True` | If ``True``, refit the selected support by *unpenalized* logistic regression (post-Lasso); else keep the glmnet-penalized fit. |
| `y` | `string (enum)` | ✓ |  | Outcome variable column name or outcome array. |

> **y** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rlassologit(y="outcome", X="value")
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`

---
### `sp.rlassologit_effect()`

**Effect of ``d`` on a binary ``y`` after Lasso-selecting controls ``x``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `I3` | `string` |  |  | Amelioration set forced into the control set (hdm's ``I3``). |
| `d` | `string` | ✓ |  | d parameter (Union[np.ndarray, pd.Series, str]). |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `post` | `boolean` |  | `True` | Post-Lasso inside the two selection steps. |
| `x` | `array[string]` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rlassologit_effect(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, d="value")
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`

---
### `sp.rlassologit_effects()`

**Logistic high-dimensional effect of each targeted column of ``X``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `I3` | `string` |  |  | I3 parameter (Optional[np.ndarray]). |
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `index` | `array[string]` |  |  | index parameter (Optional[Sequence[int]]). |
| `post` | `boolean` |  | `True` | post parameter (bool). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rlassologit_effects(y="outcome", data=df, X="value")
print(result.summary())
```

> 📁 See also: `docs/guides/rigorous_lasso_hdm.md`

---
