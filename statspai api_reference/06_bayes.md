# bayes

> 📂 所属分类:06 · 贝叶斯方法 (Bayesian Methods)

Bayesian causal inference (``statspai.bayes``).

PyMC-backed Bayesian estimators for the canonical causal designs.
PyMC and ArviZ are **optional** dependencies — importing this
sub-package never imports them. Each estimator resolves PyMC at call
time and raises :class:`ImportError` with the install recipe if the
extras are missing.

Install with:

    pip install "statspai[bayes]"

Available estimators:

- :func:`bayes_did` — 2×2 and panel difference-in-differences with
  optional hierarchical random effects on unit / time.
- :func:`bayes_rd` — sharp regression discontinuity with local
  polynomial + Normal prior on the jump.

**19 个公共函数**

### `sp.BayesianCausalResult()`

**Summary of a Bayesian causal fit.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ess` | `number` | ✓ |  | ess parameter (float). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `hdi_lower` | `number` | ✓ |  | hdi_lower parameter (float). |
| `hdi_prob` | `number` |  | `0.95` | hdi_prob parameter (float). |
| `hdi_upper` | `number` | ✓ |  | hdi_upper parameter (float). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `posterior_mean` | `number` | ✓ |  | posterior_mean parameter (float). |
| `posterior_median` | `number` | ✓ |  | posterior_median parameter (float). |
| `posterior_sd` | `number` | ✓ |  | posterior_sd parameter (float). |
| `prob_positive` | `number` | ✓ |  | prob_positive parameter (float). |
| `prob_rope` | `number` |  |  | prob_rope parameter (Optional[float]). |
| `rhat` | `number` | ✓ |  | rhat parameter (float). |
| `trace` | `string` |  |  | trace parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BayesianCausalResult(method="value", estimand="value", posterior_mean=1.0, posterior_median=1.0, posterior_sd=1.0, hdi_lower=1.0, hdi_upper=1.0, prob_positive=1.0, rhat=1.0, ess=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.BayesianDIDResult()`

**Bayesian DID result with optional per-cohort ATT posteriors.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cohort_labels` | `array[string]` |  | `None` | cohort_labels parameter (List[Any]). |
| `cohort_summaries` | `object` |  | `None` | cohort_summaries parameter (Dict[str, Dict[str, float]]). |
| `ess` | `number` | ✓ |  | ess parameter (float). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `hdi_lower` | `number` | ✓ |  | hdi_lower parameter (float). |
| `hdi_prob` | `number` |  | `0.95` | hdi_prob parameter (float). |
| `hdi_upper` | `number` | ✓ |  | hdi_upper parameter (float). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `posterior_mean` | `number` | ✓ |  | posterior_mean parameter (float). |
| `posterior_median` | `number` | ✓ |  | posterior_median parameter (float). |
| `posterior_sd` | `number` | ✓ |  | posterior_sd parameter (float). |
| `prob_positive` | `number` | ✓ |  | prob_positive parameter (float). |
| `prob_rope` | `number` |  |  | prob_rope parameter (Optional[float]). |
| `rhat` | `number` | ✓ |  | rhat parameter (float). |
| `trace` | `string` |  |  | trace parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BayesianDIDResult(method="value", estimand="value", posterior_mean=1.0, posterior_median=1.0, posterior_sd=1.0, hdi_lower=1.0, hdi_upper=1.0, prob_positive=1.0, rhat=1.0, ess=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.BayesianHTEIVResult()`

**Extension of :class:`BayesianCausalResult` for heterogeneous-effect IV.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_modifier_means` | `string` |  |  | _modifier_means parameter (Optional[np.ndarray]). |
| `cate_slopes` | `string` |  | `None` | cate_slopes parameter (pd.DataFrame). |
| `effect_modifiers` | `array[string]` |  | `None` | effect_modifiers parameter (List[str]). |
| `ess` | `number` | ✓ |  | ess parameter (float). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `hdi_lower` | `number` | ✓ |  | hdi_lower parameter (float). |
| `hdi_prob` | `number` |  | `0.95` | hdi_prob parameter (float). |
| `hdi_upper` | `number` | ✓ |  | hdi_upper parameter (float). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `posterior_mean` | `number` | ✓ |  | posterior_mean parameter (float). |
| `posterior_median` | `number` | ✓ |  | posterior_median parameter (float). |
| `posterior_sd` | `number` | ✓ |  | posterior_sd parameter (float). |
| `prob_positive` | `number` | ✓ |  | prob_positive parameter (float). |
| `prob_rope` | `number` |  |  | prob_rope parameter (Optional[float]). |
| `rhat` | `number` | ✓ |  | rhat parameter (float). |
| `trace` | `string` |  |  | trace parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BayesianHTEIVResult(method="value", estimand="value", posterior_mean=1.0, posterior_median=1.0, posterior_sd=1.0, hdi_lower=1.0, hdi_upper=1.0, prob_positive=1.0, rhat=1.0, ess=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.BayesianIVResult()`

**Bayesian IV result with optional per-instrument LATE posteriors.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ess` | `number` | ✓ |  | ess parameter (float). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `hdi_lower` | `number` | ✓ |  | hdi_lower parameter (float). |
| `hdi_prob` | `number` |  | `0.95` | hdi_prob parameter (float). |
| `hdi_upper` | `number` | ✓ |  | hdi_upper parameter (float). |
| `instrument_labels` | `array[string]` |  | `None` | instrument_labels parameter (List[str]). |
| `instrument_summaries` | `object` |  | `None` | instrument_summaries parameter (Dict[str, Dict[str, float]]). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `posterior_mean` | `number` | ✓ |  | posterior_mean parameter (float). |
| `posterior_median` | `number` | ✓ |  | posterior_median parameter (float). |
| `posterior_sd` | `number` | ✓ |  | posterior_sd parameter (float). |
| `prob_positive` | `number` | ✓ |  | prob_positive parameter (float). |
| `prob_rope` | `number` |  |  | prob_rope parameter (Optional[float]). |
| `rhat` | `number` | ✓ |  | rhat parameter (float). |
| `trace` | `string` |  |  | trace parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BayesianIVResult(method="value", estimand="value", posterior_mean=1.0, posterior_median=1.0, posterior_sd=1.0, hdi_lower=1.0, hdi_upper=1.0, prob_positive=1.0, rhat=1.0, ess=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.BayesianMTEResult()`

**Bayesian Marginal Treatment Effect result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ate` | `number` |  | `nan` | ate parameter (float). |
| `att` | `number` |  | `nan` | att parameter (float). |
| `att_hdi_lower` | `number` |  | `nan` | att_hdi_lower parameter (float). |
| `att_hdi_upper` | `number` |  | `nan` | att_hdi_upper parameter (float). |
| `att_prob_positive` | `number` |  | `nan` | att_prob_positive parameter (float). |
| `att_sd` | `number` |  | `nan` | att_sd parameter (float). |
| `atu` | `number` |  | `nan` | atu parameter (float). |
| `atu_hdi_lower` | `number` |  | `nan` | atu_hdi_lower parameter (float). |
| `atu_hdi_upper` | `number` |  | `nan` | atu_hdi_upper parameter (float). |
| `atu_prob_positive` | `number` |  | `nan` | atu_prob_positive parameter (float). |
| `atu_sd` | `number` |  | `nan` | atu_sd parameter (float). |
| `ess` | `number` | ✓ |  | ess parameter (float). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `hdi_lower` | `number` | ✓ |  | hdi_lower parameter (float). |
| `hdi_prob` | `number` |  | `0.95` | hdi_prob parameter (float). |
| `hdi_upper` | `number` | ✓ |  | hdi_upper parameter (float). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `mte_curve` | `string` |  | `None` | mte_curve parameter (pd.DataFrame). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `posterior_mean` | `number` | ✓ |  | posterior_mean parameter (float). |
| `posterior_median` | `number` | ✓ |  | posterior_median parameter (float). |
| `posterior_sd` | `number` | ✓ |  | posterior_sd parameter (float). |
| `prob_positive` | `number` | ✓ |  | prob_positive parameter (float). |
| `prob_rope` | `number` |  |  | prob_rope parameter (Optional[float]). |
| `rhat` | `number` | ✓ |  | rhat parameter (float). |
| `selection` | `string` |  | `'uniform'` | selection parameter (str). |
| `trace` | `string` |  |  | trace parameter. |
| `u_grid` | `string` |  |  | Grid of u values to evaluate. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BayesianMTEResult(method="value", estimand="value", posterior_mean=1.0, posterior_median=1.0, posterior_sd=1.0, hdi_lower=1.0, hdi_upper=1.0, prob_positive=1.0, rhat=1.0, ess=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.bayes_did()`

**Bayesian Difference-in-Differences with staggered adoption -- hierarchical ATT(g,t) posterior with optional cohort / unit random effects. Full MCMC with PyMC; reports R-hat, ESS, divergences, and 94% HDI.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chains` | `integer` |  | `4` | Number of parallel chains |
| `cohort` | `string` |  |  | First-treatment-period column for staggered adoption |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `draws` | `integer` |  | `2000` | Post-warmup draws per chain |
| `post` | `string` | ✓ |  | Post-treatment indicator (1 = post-period) |
| `target_accept` | `number` |  | `0.9` | HMC target acceptance rate |
| `time` | `string` |  |  | Time period column |
| `treat` | `string` | ✓ |  | Treatment-group indicator (1 = ever-treated) |
| `tune` | `integer` |  | `1000` | Warmup draws per chain |
| `unit` | `string` |  |  | Unit identifier (enables unit random effects) |
| `y` | `string` | ✓ |  | Outcome |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_did(y="outcome", data=df, treat="value", post="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`

---
### `sp.bayes_dml()`

**Bayesian Double Machine Learning (DiTraglia & Liu 2025): Normal-Normal conjugate update on a DML point estimate, with optional full PyMC MCMC over the orthogonal moment equation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `mode` | `string (enum)` |  | `'conjugate'` | mode parameter (str). |
| `model` | `string (enum)` |  | `'plr'` | Model variant or parameterisation to fit. |
| `prior_mean` | `number` |  | `0.0` | prior_mean parameter (float). |
| `prior_sd` | `number` |  | `10.0` | prior_sd parameter (float). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **mode** options: `'conjugate'`, `'full'`

> **model** options: `'plr'`, `'irm'`, `'pliv'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_dml(y="outcome", data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.bayes_fuzzy_rd()`

**Bayesian fuzzy RD: joint model of first-stage jump in treatment probability and outcome jump, yielding posterior over the LATE at the cutoff (Wald ratio).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chains` | `integer` |  | `4` | chains parameter (int). |
| `cutoff` | `number` |  | `0.0` | Cutoff |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `draws` | `integer` |  | `2000` | draws parameter (int). |
| `poly` | `integer` |  | `1` | Polynomial order |
| `running` | `string` | ✓ |  | Running variable |
| `treat` | `string` | ✓ |  | Take-up / treatment received |
| `tune` | `integer` |  | `1000` | tune parameter (int). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_fuzzy_rd(y="outcome", data=df, treat="value", running="value")
print(result.summary())
```

---
### `sp.bayes_hte_iv()`

**Bayesian IV with linear CATE-by-covariate heterogeneity.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `advi_iterations` | `integer` |  | `20000` | ADVI iterations (ignored for NUTS). |
| `chains` | `integer` |  | `4` | :func:`bayes_did`. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `draws` | `integer` |  | `2000` | draws parameter (int). |
| `effect_modifiers` | `array[string]` | ✓ |  | Covariates whose linear interaction with ``treat`` is the heterogeneity signal. The model centres these at their sample mean so ``tau_0`` is interpretable as the average LATE at ``modifiers = mean``. |
| `hdi_prob` | `number` |  | `0.95` | hdi_prob parameter (float). |
| `inference` | `string (enum)` |  | `'nuts'` | Sampler. ADVI is a fast mean-field approximation; see the module-level caveat. |
| `instrument` | `array[string]` | ✓ |  | instrument parameter (Union[str, Sequence[str]]). |
| `prior_coef_sigma` | `number` |  | `10.0` | prior_coef_sigma parameter (float). |
| `prior_hte_sigma` | `number` |  | `5.0` | Prior SD on each element of ``tau_hte`` (the slope of LATE on the corresponding modifier). |
| `prior_late` | `array[string]` |  | `[0.0, 10.0]` | prior_late parameter (Tuple[float, float]). |
| `prior_noise` | `number` |  | `5.0` | prior_noise parameter (float). |
| `progressbar` | `boolean` |  | `False` | :func:`bayes_did`. |
| `random_state` | `integer` |  | `42` | :func:`bayes_did`. |
| `rope` | `array[string]` |  |  | rope parameter (Optional[Tuple[float, float]]). |
| `target_accept` | `number` |  | `0.9` | :func:`bayes_did`. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `tune` | `integer` |  | `1000` | :func:`bayes_did`. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **inference** options: `'nuts'`, `'advi'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_hte_iv(y="outcome", data=df, treat="value", instrument=["a", "b"], effect_modifiers=["a", "b"])
print(result.summary())
```

---
### `sp.bayes_its()`

**Bayesian interrupted time series (segmented regression).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `advi_iterations` | `integer` |  | `20000` | advi_iterations parameter (int). |
| `chains` | `integer` |  | `4` | chains parameter (int). |
| `data` | `string` | ✓ |  | Observed series, sorted in time. |
| `draws` | `integer` |  | `2000` | draws parameter (int). |
| `hdi_prob` | `number` |  | `0.95` | Sampler controls; see :func:`sp.bayes_did`. |
| `inference` | `string` |  | `'nuts'` | inference parameter (str). |
| `intervention` | `integer` |  |  | Integer row position where the intervention begins (``0 < intervention < n``). |
| `prior_level` | `array[string]` |  | `[0.0, 10.0]` | Mean / SD of the Normal prior on the level change (the estimand). |
| `prior_noise` | `number` |  | `5.0` | Prior scales for the slope change, the pre-trend, and the residual SD. |
| `prior_slope_sigma` | `number` |  | `10.0` | Prior scales for the slope change, the pre-trend, and the residual SD. |
| `prior_trend_sigma` | `number` |  | `10.0` | Prior scales for the slope change, the pre-trend, and the residual SD. |
| `progressbar` | `boolean` |  | `False` | progressbar parameter (bool). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `rope` | `array[string]` |  |  | Region of practical equivalence for the level change. |
| `target_accept` | `number` |  | `0.9` | target_accept parameter (float). |
| `time` | `string` |  |  | Time column (used for the trend term and the x-axis). Defaults to the row index. |
| `tune` | `integer` |  | `1000` | tune parameter (int). |
| `y` | `string` | ✓ |  | Outcome column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_its(y="outcome", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`

---
### `sp.bayes_iv()`

**Bayesian instrumental variables with full posterior over structural parameters. Handles weak instruments via shrinkage priors and reports posterior mass near zero on the first-stage coefficient.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chains` | `integer` |  | `4` | chains parameter (int). |
| `covariates` | `array[string]` |  |  | Exogenous controls |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `draws` | `integer` |  | `2000` | draws parameter (int). |
| `instrument` | `string` | ✓ |  | Instrument(s) -- str or list |
| `treat` | `string` | ✓ |  | Endogenous treatment |
| `tune` | `integer` |  | `1000` | tune parameter (int). |
| `y` | `string` | ✓ |  | Outcome |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_iv(y="outcome", data=df, treat="value", instrument="value")
print(result.summary())
```

---
### `sp.bayes_mte()`

**Bayesian Marginal Treatment Effect (Heckman-Vytlacil 2005). Full posterior over the MTE curve under essential heterogeneity, with bivariate-normal latent errors. Derives ATE / ATT / LATE / PRTE as posterior linear functionals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chains` | `integer` |  | `4` | chains parameter (int). |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `draws` | `integer` |  | `2000` | draws parameter (int). |
| `instrument` | `string` | ✓ |  | Instrument(s) |
| `treat` | `string` | ✓ |  | Binary treatment |
| `tune` | `integer` |  | `1000` | tune parameter (int). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_mte(y="outcome", data=df, treat="value", instrument="value")
print(result.summary())
```

---
### `sp.bayes_rd()`

**Bayesian sharp Regression Discontinuity -- full posterior over the RD jump via local polynomial with prior regularisation on bandwidth and bias-correction slopes. Reports HDI, rhat, ESS, divergences.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chains` | `integer` |  | `4` | chains parameter (int). |
| `cutoff` | `number` |  | `0.0` | Cutoff value |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `draws` | `integer` |  | `2000` | draws parameter (int). |
| `poly` | `integer` |  | `1` | Polynomial order |
| `running` | `string` | ✓ |  | Running variable |
| `tune` | `integer` |  | `1000` | tune parameter (int). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_rd(y="outcome", data=df, running="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`

---
### `sp.bayes_synth()`

**Bayesian synthetic control.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `advi_iterations` | `integer` |  | `20000` | advi_iterations parameter (int). |
| `chains` | `integer` |  | `4` | chains parameter (int). |
| `data` | `string` | ✓ |  | Long panel (one row per unit-time). |
| `donors` | `array[string]` |  |  | Donor pool. Defaults to every unit except the treated one. |
| `draws` | `integer` |  | `2000` | draws parameter (int). |
| `hdi_prob` | `number` |  | `0.95` | Sampler controls; see :func:`sp.bayes_did`. |
| `inference` | `string` |  | `'nuts'` | inference parameter (str). |
| `outcome` | `string` | ✓ |  | Outcome, unit-id and time column names. |
| `prior_noise` | `number` |  | `5.0` | Half-Normal scale for the pre-period fit residual SD. |
| `prior_weights_alpha` | `number` |  | `1.0` | Dirichlet concentration. ``1.0`` is uniform over the simplex; ``<1`` favours sparse weights. |
| `progressbar` | `boolean` |  | `False` | progressbar parameter (bool). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `rope` | `array[string]` |  |  | Region of practical equivalence for the ATT. |
| `target_accept` | `number` |  | `0.9` | target_accept parameter (float). |
| `time` | `string` | ✓ |  | Outcome, unit-id and time column names. |
| `treated_unit` | `string` | ✓ |  | The treated unit's id. |
| `treatment_time` | `string` | ✓ |  | First treated period (inclusive); periods ``< treatment_time`` are the pre-treatment fitting window. |
| `tune` | `integer` |  | `1000` | tune parameter (int). |
| `unit` | `string` | ✓ |  | Outcome, unit-id and time column names. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bayes_synth(data=df, outcome="value", unit="value", time="value", treated_unit="value", treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`

---
### `sp.policy_weight_ate()`

**Uniform weight = 1 on every grid point.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.policy_weight_ate()
print(result.summary())
```

---
### `sp.policy_weight_marginal()`

**Marginal PRTE at a specific propensity level ``u_star``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth` | `number` |  | `0.05` | Half-width of the averaging window. |
| `u_star` | `number` | ✓ |  | Target propensity level, in ``[0, 1]``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.policy_weight_marginal(u_star=1.0)
print(result.summary())
```

---
### `sp.policy_weight_observed_prte()`

**True **CHV-2011 PRTE** weights from the observed propensity**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bw_method` | `number` |  |  | Passed to :class:`scipy.stats.gaussian_kde`. ``None`` uses Scott's rule, which is a good default for smooth propensity densities. |
| `propensity_sample` | `string` | ✓ |  | 1-D array of observed propensity scores in ``[0, 1]``. Typical source: ``sp.bayes_mte(...).model_info['propensity']`` or a direct logit fit on your sample. |
| `shift` | `number` | ✓ |  | Policy-scale propensity shift. Must be non-zero and in ``(-1, 1)``. Positive = expand treatment uptake by ``shift`` at every propensity level; negative = contraction. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.policy_weight_observed_prte(propensity_sample="value", shift=1.0)
print(result.summary())
```

---
### `sp.policy_weight_prte()`

****Stylised** PRTE weights -- convenience builder, NOT the**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `shift` | `number` | ✓ |  | Size of the propensity-scale shift. Must be in ``(-1, 1)`` and non-zero. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.policy_weight_prte(shift=1.0)
print(result.summary())
```

---
### `sp.policy_weight_subsidy()`

**Weight = 1 on ``[u_lo, u_hi]``; 0 elsewhere.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `u_hi` | `number` | ✓ |  | Band endpoints on the propensity (``U_D``) scale. Both must lie in ``[0, 1]`` and ``u_lo < u_hi``. |
| `u_lo` | `number` | ✓ |  | Band endpoints on the propensity (``U_D``) scale. Both must lie in ``[0, 1]`` and ``u_lo < u_hi``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.policy_weight_subsidy(u_lo=1.0, u_hi=1.0)
print(result.summary())
```

---
