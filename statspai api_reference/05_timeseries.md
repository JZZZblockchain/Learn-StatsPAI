# timeseries

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Time series methods for causal inference contexts.

Provides VAR (vector autoregression), structural break tests,
Granger causality, and cointegration analysis.

**20 个公共函数**

### `sp.ARIMAResult()`

**Fitted ARIMA(p,d,q) / SARIMAX model returned by :func:`statspai.arima`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_model` | `string` | ✓ |  | _model parameter. |
| `aic` | `number` | ✓ |  | aic parameter (float). |
| `aicc` | `number` | ✓ |  | aicc parameter (float). |
| `bic` | `number` | ✓ |  | bic parameter (float). |
| `fitted_values` | `string` | ✓ |  | fitted_values parameter (np.ndarray). |
| `log_likelihood` | `number` | ✓ |  | log_likelihood parameter (float). |
| `n` | `integer` | ✓ |  | n parameter (int). |
| `order` | `array[string]` | ✓ |  | order parameter (Tuple[int, int, int]). |
| `params` | `string` | ✓ |  | params parameter (pd.Series). |
| `residuals` | `string` | ✓ |  | residuals parameter (np.ndarray). |
> 📝 *residuals 参数（np.ndarray）。*
| `se` | `string` | ✓ |  | se parameter (pd.Series). |
| `seasonal_order` | `array[string]` | ✓ |  | seasonal_order parameter (Optional[Tuple[int, int, int, int]]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ARIMAResult(order=["a", "b"], seasonal_order=["a", "b"], params="value", se="value", aic=1.0, bic=1.0, aicc=1.0, log_likelihood=1.0, residuals="value", fitted_values="value", n=1.0, _model="value")
print(result.summary())
```

---
### `sp.BVARResult()`

**Posterior summary of a Bayesian VAR with Minnesota prior.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coef` | `string` | ✓ |  | coef parameter (np.ndarray). |
| `coef_sd` | `string` |  |  | coef_sd parameter (Optional[np.ndarray]). |
| `fitted` | `string` | ✓ |  | fitted parameter (np.ndarray). |
| `lags` | `integer` | ✓ |  | lags parameter (int). |
| `lambda1` | `number` | ✓ |  | lambda1 parameter (float). |
| `lambda2` | `number` | ✓ |  | lambda2 parameter (float). |
| `n` | `integer` | ✓ |  | n parameter (int). |
| `residuals` | `string` | ✓ |  | residuals parameter (np.ndarray). |
> 📝 *residuals 参数（np.ndarray）。*
| `sigma` | `string` | ✓ |  | sigma parameter (np.ndarray). |
| `var_names` | `array[string]` | ✓ |  | var_names parameter (list[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BVARResult(coef="value", sigma="value", fitted="value", residuals="value", var_names=["a", "b"], lags=1.0, n=1.0, lambda1=1.0, lambda2=1.0)
print(result.summary())
```

---
### `sp.CointegrationResult()`

**Results from cointegration test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `critical_values` | `array[string]` | ✓ |  | critical_values parameter (list[float]). |
| `eigenvalues` | `string` | ✓ |  | eigenvalues parameter (Optional[numpy.ndarray]). |
| `eigenvectors` | `string` | ✓ |  | eigenvectors parameter (Optional[numpy.ndarray]). |
| `lags` | `integer` | ✓ |  | lags parameter (int). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `n_vars` | `integer` | ✓ |  | Number of vars. |
| `rank` | `integer` | ✓ |  | rank parameter (int). |
| `test_stats` | `string` | ✓ |  | test_stats parameter. |
| `test_type` | `string` | ✓ |  | test_type parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CointegrationResult(test_type="value", test_stats="value", critical_values=["a", "b"], rank=1.0, eigenvalues="value", eigenvectors="value", n_obs=1.0, n_vars=1.0, lags=1.0)
print(result.summary())
```

---
### `sp.GARCHResult()`

**Fitted GARCH(p,q) model returned by :func:`garch`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `aic` | `number` | ✓ |  | aic parameter (float). |
| `alpha` | `string` | ✓ |  | Significance level for confidence intervals and tests. |
| `beta` | `string` | ✓ |  | beta parameter (np.ndarray). |
| `bic` | `number` | ✓ |  | bic parameter (float). |
| `coef` | `string` |  |  | coef parameter (Optional[np.ndarray]). |
| `log_likelihood` | `number` | ✓ |  | log_likelihood parameter (float). |
| `mu` | `number` | ✓ |  | mu parameter (float). |
| `n` | `integer` | ✓ |  | n parameter (int). |
| `omega` | `number` | ✓ |  | omega parameter (float). |
| `p` | `integer` | ✓ |  | p parameter (int). |
| `param_names` | `array[string]` |  |  | param_names parameter (Optional[List[str]]). |
| `q` | `integer` | ✓ |  | Quantile level. |
| `residuals` | `string` | ✓ |  | residuals parameter (np.ndarray). |
> 📝 *residuals 参数（np.ndarray）。*
| `se_vec` | `string` |  |  | se_vec parameter (Optional[np.ndarray]). |
| `sigma2` | `string` | ✓ |  | sigma2 parameter (np.ndarray). |
| `std_residuals` | `string` | ✓ |  | std_residuals parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GARCHResult(omega=1.0, alpha="value", beta="value", mu=1.0, sigma2="value", residuals="value", std_residuals="value", log_likelihood=1.0, aic=1.0, bic=1.0, n=1.0, p=1.0, q=1.0)
print(result.summary())
```

---
### `sp.ITSResult()`

**Result container for :func:`its`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_level` | `array[string]` | ✓ |  | ci_level parameter (tuple). |
| `ci_slope` | `array[string]` | ✓ |  | ci_slope parameter (tuple). |
| `coefficients` | `string` | ✓ |  | coefficients parameter (pd.DataFrame). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `intervention_time` | `integer` | ✓ |  | intervention_time parameter (int). |
| `level_change` | `number` | ✓ |  | level_change parameter (float). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `pvalue_level` | `number` | ✓ |  | pvalue_level parameter (float). |
| `pvalue_slope` | `number` | ✓ |  | pvalue_slope parameter (float). |
| `se_level` | `number` | ✓ |  | se_level parameter (float). |
| `se_slope` | `number` | ✓ |  | se_slope parameter (float). |
| `slope_change` | `number` | ✓ |  | slope_change parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ITSResult(level_change=1.0, slope_change=1.0, se_level=1.0, se_slope=1.0, ci_level=["a", "b"], ci_slope=["a", "b"], pvalue_level=1.0, pvalue_slope=1.0, coefficients="value", n_obs=1.0, intervention_time=1.0)
print(result.summary())
```

---
### `sp.LocalProjectionsResult()`

**Impulse-response container returned by :func:`local_projections`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `ci_lower` | `string` | ✓ |  | ci_lower parameter (np.ndarray). |
> 📝 *ci_lower 参数（np.ndarray）。*
| `ci_upper` | `string` | ✓ |  | ci_upper parameter (np.ndarray). |
> 📝 *ci_upper 参数（np.ndarray）。*
| `horizons` | `string` | ✓ |  | horizons parameter (np.ndarray). |
> 📝 *horizons 参数（np.ndarray）。*
| `irf` | `string` | ✓ |  | irf parameter (np.ndarray). |
> 📝 *irf 参数（np.ndarray）。*
| `n_obs_per_horizon` | `string` | ✓ |  | Number of obs per horizon. |
> 📝 *每个时间范围的观测值数量。*
| `outcome_name` | `string` | ✓ |  | outcome_name parameter (str). |
> 📝 *outcome_name 参数（字符串）。*
| `se` | `string` | ✓ |  | se parameter (np.ndarray). |
| `shock_name` | `string` | ✓ |  | shock_name parameter (str). |
> 📝 *shock_name 参数（字符串）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LocalProjectionsResult(horizons="value", irf="value", se="value", ci_lower="value", ci_upper="value", alpha=1.0, shock_name="value", outcome_name="value", n_obs_per_horizon="value")
print(result.summary())
```

---
### `sp.StructuralBreakResult()`

**Results from structural break tests.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bic` | `number` | ✓ |  | bic parameter (Optional[float]). |
| `break_dates` | `array[string]` | ✓ |  | break_dates parameter (list[int]). |
| `f_stats` | `string` | ✓ |  | f_stats parameter. |
| `n_breaks` | `integer` | ✓ |  | Number of breaks. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `p_values` | `string` | ✓ |  | p_values parameter. |
| `rss_full` | `number` | ✓ |  | rss_full parameter (float). |
| `rss_segments` | `number` | ✓ |  | rss_segments parameter (Optional[float]). |
| `test_type` | `string` | ✓ |  | test_type parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.StructuralBreakResult(test_type="value", break_dates=["a", "b"], f_stats="value", p_values="value", n_breaks=1.0, rss_full=1.0, rss_segments=1.0, bic=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.VARResult()`

**Results from VAR estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `aic` | `number` | ✓ |  | aic parameter (float). |
| `bic` | `number` | ✓ |  | bic parameter (float). |
| `coefs` | `object` | ✓ |  | coefs parameter (Dict[str, pandas.DataFrame]). |
| `det_sigma` | `number` | ✓ |  | det_sigma parameter (float). |
| `hqic` | `number` | ✓ |  | hqic parameter (float). |
| `lags` | `integer` | ✓ |  | lags parameter (int). |
| `log_likelihood` | `number` | ✓ |  | log_likelihood parameter (float). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `residuals` | `string` | ✓ |  | residuals parameter (DataFrame). |
| `se` | `object` | ✓ |  | se parameter (Dict[str, numpy.ndarray]). |
| `se_df` | `string` |  | `'stata'` | se_df parameter (str). |
| `sigma_u` | `string` | ✓ |  | sigma_u parameter (DataFrame). |
| `var_names` | `array[string]` | ✓ |  | var_names parameter (List[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.VARResult(residuals="value", sigma_u="value", var_names=["a", "b"], lags=1.0, n_obs=1.0, aic=1.0, bic=1.0, hqic=1.0, det_sigma=1.0, log_likelihood=1.0)
print(result.summary())
```

---
### `sp.arima()`

**Fit ARIMA(p,d,q) or SARIMAX. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `auto` | `boolean` |  | `False` | If True, select (p, d, q) by AICc grid search (ignores ``order``). |
| `exog` | `string` |  |  | Exogenous regressors (ARIMAX). |
| `max_d` | `integer` |  | `2` | Bounds for the auto search. |
| `max_p` | `integer` |  | `5` | Bounds for the auto search. |
| `max_q` | `integer` |  | `5` | Bounds for the auto search. |
| `method` | `string (enum)` |  | `'statespace'` | Estimation convention. ``'statespace'`` keeps the default exact Kalman/SARIMAX likelihood. ``'css_ml'`` is retained as a compatibility alias for ``'innovations_mle'``. The innovations-MLE path uses statsmodels' stationary/invertible exact-MLE parameterization, matching ``stats::arima(method='ML')`` and tightly converged Stata ``arima`` coefficient conventions for pure ARMA models. |
| `order` | `array[string]` |  | `[1, 0, 0]` | order parameter (Tuple[int, int, int]). |
| `seasonal_order` | `array[string]` |  |  | seasonal_order parameter (Optional[Tuple[int, int, int, int]]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **method** options: `'statespace'`, `'css_ml'`, `'innovations_mle'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.arima(y="outcome")
print(result.summary())
```

---
### `sp.bvar()`

**Bayesian VAR with Minnesota (Litterman) prior.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Columns are the endogenous variables. |
| `lags` | `integer` |  | `4` | lags parameter (int). |
| `lambda1` | `number` |  | `0.1` | Overall tightness (smaller = stronger shrinkage toward RW). |
| `lambda2` | `number` |  | `0.5` | Cross-variable shrinkage relative to own-lag. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bvar(data=df)
print(result.summary())
```

---
### `sp.cusum_test()`

**CUSUM test for parameter stability. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `x` | `array[string]` |  |  | Regressors. |
| `y` | `string` | ✓ |  | Dependent variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cusum_test(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.engle_granger()`

**Engle-Granger (1987) two-step cointegration test. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `lags` | `integer` |  |  | Lags for ADF test. If None, uses AIC selection. |
| `trend` | `string` |  | `'c'` | trend parameter (str). |
| `variables` | `array[string]` |  |  | Variables to test (first is dependent). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.engle_granger(data=df)
print(result.summary())
```

---
### `sp.garch()`

**Fit GARCH(p,q) by conditional Gaussian MLE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `mean` | `boolean` |  | `True` | Estimate a constant mean mu; if False, mu = 0. |
| `p` | `integer` |  | `1` | Number of GARCH (lagged sigma2) terms. |
| `q` | `integer` |  | `1` | Number of ARCH (lagged epsilon2) terms. |
| `y` | `string` | ✓ |  | Return series (or log-return, etc.). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.garch(y="outcome")
print(result.summary())
```

---
### `sp.granger_causality()`

**Granger causality test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `caused` | `string` |  |  | Variable being tested for causation. |
| `causing` | `string` |  |  | Variable hypothesized to cause. |
| `data` | `string` |  |  | Data (if var_result not provided). |
| `lags` | `integer` |  |  | Number of lags (if fitting new VAR). |
| `var_result` | `string` |  |  | Pre-estimated VAR model. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.granger_causality(data=df)
print(result.summary())
```

---
### `sp.irf()`

**Compute impulse response functions from VAR.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `impulse` | `string` |  |  | Impulse variable (if None, all). |
| `orthogonal` | `boolean` |  | `True` | Orthogonalized (Cholesky) IRF. |
| `periods` | `integer` |  | `20` | Number of periods for IRF. |
| `response` | `string` |  |  | Response variable (if None, all). |
| `var_result` | `string` | ✓ |  | Estimated VAR model. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.irf(var_result="value")
print(result.summary())
```

---
### `sp.its()`

**Segmented regression for interrupted time series.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | Observed series, sorted in time. |
| `hac_lag` | `integer` |  | `4` | Newey-West truncation lag. |
| `intervention` | `integer` |  |  | Time index (integer row position) at which the intervention begins. Required. |
| `seasonality_harmonics` | `integer` |  | `2` | seasonality_harmonics parameter (int). |
| `seasonality_period` | `integer` |  |  | Period P of Fourier seasonal terms (e.g. 12 for monthly data with annual cycle). If None, no seasonality is added. |
| `time` | `string` |  |  | Time column. If None, uses row index 0..n-1. |
| `y` | `string` | ✓ |  | Outcome column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.its(y="outcome", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`

---
### `sp.johansen()`

**Johansen (1991) cointegration test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `lags` | `integer` |  | `1` | Number of lags in the VECM. |
| `test` | `string` |  | `'trace'` | 'trace' or 'maxeig' (maximum eigenvalue). |
| `trend` | `string` |  | `'c'` | 'n' (none), 'c' (constant), 'ct' (constant + trend). |
| `variables` | `array[string]` |  |  | Variables to test. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.johansen(data=df)
print(result.summary())
```

---
### `sp.local_projections()`

**Estimate impulse responses via Jorda (2005) local projections. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for the confidence band. |
| `auto_lag` | `boolean` |  | `True` | If ``True`` (the legacy default), also adds ``y_{t-1}`` and ``shock_{t-1}`` as automatic regressors. Set ``False`` for a bare ``y_{t+h} ~ const + shock_t + controls`` specification. These two auto-controls were silent in the pre-1.16 docstring. |
| `controls` | `array[string]` |  |  | Additional regressors taken **verbatim** from ``data``: the column values at time t are used directly, without re-lagging. If you want the lag of a control, lag it yourself before passing it in (e.g. ``df["unemp_lag"] = df["unemp"].shift(1)`` and then ``controls=["unemp_lag"]``). The pre-1.16 behaviour silently re-lagged controls a second time on top of an auto- added ``y_{t-1}``, producing collinear columns and surprising impulse responses; see ``MIGRATION.md`` for context. |
| `cumulative` | `boolean` |  | `False` | If ``True``, return the cumulative response ``y_{t+h} - y_{t-1}``. Default (False) returns ``y_{t+h}`` directly. |
| `data` | `string` | ✓ |  | Time-ordered panel (single series for now -- panel extension TBD). |
| `endog_order` | `array[string]` |  |  | Endogenous variable order used only when ``identification='lpirfs_cholesky'``. Defaults to ``[outcome, shock]``. |
| `horizons` | `integer` |  | `20` | Number of horizons h = 0, 1, ..., H to estimate. |
| `identification` | `string (enum)` |  | `'direct'` | Shock-identification convention. ``'direct'`` uses the coefficient on the observed ``shock`` variable in each horizon regression. ``'lpirfs_cholesky'`` reproduces ``lpirfs::lp_lin`` with ``lags_endog_lin=1`` and ``shock_type=1``: the variables in ``endog_order`` define the Cholesky ordering, and the reported response is the unit structural shock for ``shock``. |
| `nw_lags` | `integer` |  |  | Newey-West truncation lag. Defaults to ``round(1.5 * horizons)`` per Kilian & Kim (2011) recommendation. |
| `outcome` | `string` | ✓ |  | Column name of the outcome variable y. |
| `shock` | `string` | ✓ |  | Column name of the shock / treatment variable. |

> **identification** options: `'direct'`, `'lpirfs_cholesky'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.local_projections(data=df, outcome="value", shock="value")
print(result.summary())
```

---
### `sp.structural_break()`

**Structural break detection. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` |  |  | Time series data (assumed ordered by time). |
| `max_breaks` | `integer` |  | `5` | Maximum number of breaks to test. |
| `method` | `string` |  | `'bai-perron'` | Estimator or algorithm variant to use. |
| `min_segment` | `number` |  | `0.15` | Minimum segment length as fraction of sample. |
| `x` | `array[string]` |  |  | Regressors. If None, uses constant only (mean shift). |
| `y` | `string` |  |  | Dependent variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.structural_break(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.var()`

**Estimate a Vector Autoregression (VAR) model. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `data` | `string` | ✓ |  | Time series data. |
| `lags` | `integer` |  | `1` | Number of lags. |
| `se_df` | `string (enum)` |  | `'stata'` | Residual-variance denominator for coefficient standard errors. ``'stata'``/``'ml'`` uses ``T`` and matches Stata ``var`` default conditional-MLE standard errors. ``'r'``/``'unbiased'`` uses ``T - k_params`` and matches the equation-by-equation ``lm()`` standard errors returned inside R ``vars::VAR()``. |
| `trend` | `string` |  | `'c'` | trend parameter (str). |
| `variables` | `array[string]` |  |  | Variable names. If None, uses all numeric columns. |

> **se_df** options: `'stata'`, `'ml'`, `'r'`, `'unbiased'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.var(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/v1_2_frontier.md`

---
