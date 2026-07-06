# dml

> 📂 所属分类:01 · 核心因果推断方法 (Core Causal Methods)

Double/Debiased Machine Learning module for StatsPAI.

Implements the Chernozhukov et al. (2018) framework with separate
per-model estimator classes (PLR / IRM / PLIV / IIVM) sharing a common
cross-fitting infrastructure.

Public entry points:

* :func:`dml` — dispatcher, selects the model via ``model=`` string.
* :class:`DoubleML` — legacy façade, delegates to a per-model class.
* :class:`DoubleMLPLR`, :class:`DoubleMLIRM`, :class:`DoubleMLPLIV`,
  :class:`DoubleMLIIVM` — direct per-model entry points.

References
----------
Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C.,
Newey, W., and Robins, J. (2018). "Double/Debiased Machine Learning for
Treatment and Structural Parameters." *Econometrics Journal*, 21(1), C1-C68. [@chernozhukov2018double]

**15 个公共函数**

### `sp.DMLAveragingResult()`

**CausalResult extended with per-candidate and weight details.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_citation_key` | `string` |  |  | _citation_key parameter (Optional[str]). |
| `_influence_funcs` | `string` |  |  | _influence_funcs parameter (Optional[numpy.ndarray]). |
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `detail` | `string` |  |  | Amount of result detail to return. |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  |  | model_info parameter (Optional[Dict[str, Any]]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
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

result = sp.DMLAveragingResult(method="value", estimand="value", estimate=1.0, se=1.0, pvalue=1.0, ci=["a", "b"], alpha=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.DMLDiagnostics()`

**Bundled DML diagnostics returned by :func:`dml_diagnostics`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_overlap_label` | `string` |  | `''` | _overlap_label parameter (str). |
| `_overlap_values` | `string` |  | `None` | _overlap_values parameter (np.ndarray). |
| `_score` | `string` |  |  | _score parameter (Optional[np.ndarray]). |
| `balance_table` | `string` |  | `None` | balance_table parameter (pd.DataFrame). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_clipped_high` | `integer` |  | `0` | Number of clipped high. |
| `n_clipped_low` | `integer` |  | `0` | Number of clipped low. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `orth_pvalue` | `number` |  | `1.0` | orth_pvalue parameter (float). |
| `orth_stat` | `number` |  | `0.0` | orth_stat parameter (float). |
| `orth_warning` | `string` |  |  | orth_warning parameter (Optional[str]). |
| `overlap_table` | `string` | ✓ |  | overlap_table parameter (pd.DataFrame). |
| `overlap_warning` | `string` |  |  | overlap_warning parameter (Optional[str]). |
| `score_kurtosis` | `number` |  | `0.0` | score_kurtosis parameter (float). |
| `score_mean` | `number` |  | `0.0` | score_mean parameter (float). |
| `score_sd` | `number` |  | `0.0` | score_sd parameter (float). |
| `score_skew` | `number` |  | `0.0` | score_skew parameter (float). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DMLDiagnostics(n_obs=1.0, method="value", estimate=1.0, se=1.0, overlap_table="value")
print(result.summary())
```

---
### `sp.DMLPanelResult()`

**Output of :func:`dml_panel`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_lower` | `number` | ✓ |  | ci_lower parameter (float). |
| `ci_upper` | `number` | ✓ |  | ci_upper parameter (float). |
| `diagnostics` | `object` |  | `None` | diagnostics parameter (dict). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `include_time_fe` | `boolean` | ✓ |  | Whether to include time fe. |
| `method` | `string` |  | `'dml_panel'` | Estimator or algorithm variant to use. |
| `ml_g_name` | `string` | ✓ |  | ml_g_name parameter (str). |
| `ml_m_name` | `string` | ✓ |  | ml_m_name parameter (str). |
| `n_folds` | `integer` | ✓ |  | Number of cross-fitting or cross-validation folds. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `n_units` | `integer` | ✓ |  | Number of units. |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `t_stat` | `number` | ✓ |  | t_stat parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DMLPanelResult(estimate=1.0, se=1.0, ci_lower=1.0, ci_upper=1.0, p_value=1.0, t_stat=1.0, n_units=1.0, n_obs=1.0, n_folds=1.0, include_time_fe=True, ml_g_name="value", ml_m_name="value")
print(result.summary())
```

---
### `sp.DMLSensitivityResult()`

**Output of :func:`dml_sensitivity`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adjusted_estimate_high` | `number` | ✓ |  | adjusted_estimate_high parameter (float). |
| `adjusted_estimate_low` | `number` | ✓ |  | adjusted_estimate_low parameter (float). |
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `benchmarks` | `string` | ✓ |  | benchmarks parameter (pd.DataFrame). |
| `bias_bound` | `number` | ✓ |  | bias_bound parameter (float). |
| `cf_d` | `number` |  |  | cf_d parameter (Optional[float]). |
| `cf_y` | `number` |  |  | cf_y parameter (Optional[float]). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` |  | `'DML-OVB (Chernozhukov-Cinelli-Newey 2022)'` | Estimator or algorithm variant to use. |
| `q` | `number` | ✓ |  | Quantile level. |
| `rv_q` | `number` | ✓ |  | rv_q parameter (float). |
| `rv_qa` | `number` | ✓ |  | rv_qa parameter (float). |
| `s` | `number` | ✓ |  | s parameter (float). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DMLSensitivityResult(estimate=1.0, se=1.0, rv_q=1.0, rv_qa=1.0, bias_bound=1.0, adjusted_estimate_low=1.0, adjusted_estimate_high=1.0, benchmarks="value", s=1.0, q=1.0, alpha=1.0)
print(result.summary())
```

---
### `sp.DoubleML()`

**Legacy facade. Prefer the per-model classes directly for new code:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `fold_indices` | `string` |  |  | fold_indices parameter (Optional[Any]). |
| `instrument` | `array[string]` |  |  | instrument parameter (Union[str, List[str], NoneType]). |
| `ml_g` | `string` |  |  | ml_g parameter (Optional[Any]). |
| `ml_m` | `string` |  |  | ml_m parameter (Optional[Any]). |
| `ml_r` | `string` |  |  | ml_r parameter (Optional[Any]). |
| `model` | `string` |  | `'plr'` | Model variant or parameterisation to fit. |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_rep` | `integer` |  | `1` | Number of rep. |
| `normalize_ipw` | `boolean` |  | `False` | normalize_ipw parameter (bool). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `sample_weight` | `string` |  |  | sample_weight parameter (Optional[Any]). |
| `score` | `string` |  |  | score parameter (Optional[str]). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `trimming_threshold` | `number` |  | `0.01` | trimming_threshold parameter (float). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DoubleML(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.DoubleMLIIVM()`

**Interactive IV DML -- binary D, binary Z, LATE via Wald.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `fold_indices` | `string` |  |  | fold_indices parameter (Optional[Any]). |
| `instrument` | `array[string]` |  |  | instrument parameter (Union[str, List[str], NoneType]). |
| `ml_g` | `string` |  |  | ml_g parameter (Optional[Any]). |
| `ml_m` | `string` |  |  | ml_m parameter (Optional[Any]). |
| `ml_r` | `string` |  |  | ml_r parameter (Optional[Any]). |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_rep` | `integer` |  | `1` | Number of rep. |
| `normalize_ipw` | `boolean` |  | `False` | normalize_ipw parameter (bool). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `sample_weight` | `string` |  |  | sample_weight parameter (Optional[Any]). |
| `score` | `string` |  |  | score parameter (Optional[str]). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `trimming_threshold` | `number` |  | `0.01` | trimming_threshold parameter (float). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DoubleMLIIVM(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.DoubleMLIRM()`

**Interactive regression DML -- binary D, ATE via AIPW.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `fold_indices` | `string` |  |  | fold_indices parameter (Optional[Any]). |
| `instrument` | `array[string]` |  |  | instrument parameter (Union[str, List[str], NoneType]). |
| `ml_g` | `string` |  |  | ml_g parameter (Optional[Any]). |
| `ml_m` | `string` |  |  | ml_m parameter (Optional[Any]). |
| `ml_r` | `string` |  |  | ml_r parameter (Optional[Any]). |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_rep` | `integer` |  | `1` | Number of rep. |
| `normalize_ipw` | `boolean` |  | `False` | normalize_ipw parameter (bool). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `sample_weight` | `string` |  |  | sample_weight parameter (Optional[Any]). |
| `score` | `string` |  |  | score parameter (Optional[str]). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `trimming_threshold` | `number` |  | `0.01` | trimming_threshold parameter (float). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DoubleMLIRM(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/case_study_401k.md`, `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.DoubleMLPLIV()`

**Partially linear IV DML -- endogenous D with continuous/binary Z.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `fold_indices` | `string` |  |  | fold_indices parameter (Optional[Any]). |
| `instrument` | `array[string]` |  |  | instrument parameter (Union[str, List[str], NoneType]). |
| `ml_g` | `string` |  |  | ml_g parameter (Optional[Any]). |
| `ml_m` | `string` |  |  | ml_m parameter (Optional[Any]). |
| `ml_r` | `string` |  |  | ml_r parameter (Optional[Any]). |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_rep` | `integer` |  | `1` | Number of rep. |
| `normalize_ipw` | `boolean` |  | `False` | normalize_ipw parameter (bool). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `sample_weight` | `string` |  |  | sample_weight parameter (Optional[Any]). |
| `score` | `string` |  |  | score parameter (Optional[str]). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `trimming_threshold` | `number` |  | `0.01` | trimming_threshold parameter (float). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DoubleMLPLIV(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.DoubleMLPLR()`

**Partially linear regression DML (continuous or binary D, no IV).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `fold_indices` | `string` |  |  | fold_indices parameter (Optional[Any]). |
| `instrument` | `array[string]` |  |  | instrument parameter (Union[str, List[str], NoneType]). |
| `ml_g` | `string` |  |  | ml_g parameter (Optional[Any]). |
| `ml_m` | `string` |  |  | ml_m parameter (Optional[Any]). |
| `ml_r` | `string` |  |  | ml_r parameter (Optional[Any]). |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_rep` | `integer` |  | `1` | Number of rep. |
| `normalize_ipw` | `boolean` |  | `False` | normalize_ipw parameter (bool). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `sample_weight` | `string` |  |  | sample_weight parameter (Optional[Any]). |
| `score` | `string` |  |  | score parameter (Optional[str]). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `trimming_threshold` | `number` |  | `0.01` | trimming_threshold parameter (float). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DoubleMLPLR(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/case_study_401k.md`, `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.dml()`

**Double/Debiased Machine Learning for treatment effect estimation. Supports partially linear (PLR), interactive regression (IRM, binary D), partially linear IV (PLIV), and interactive IV (IIVM, binary D/binary Z -> LATE). Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | List of control variable names |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `instrument` | `string` |  |  | Instrument (required for pliv/iivm) |
| `model` | `string (enum)` |  | `'plr'` | DML model family |
| `n_folds` | `integer` |  | `5` | Cross-fitting folds |
| `n_rep` | `integer` |  | `1` | Repeated cross-fitting splits (median aggregation) |
| `normalize_ipw` | `boolean` |  | `False` | Self-normalize the inverse-propensity weights for the IPW models (irm/iivm); matches DoubleML's normalize_ipw. Rejected for plr/pliv. |
| `score` | `string (enum)` |  |  | Orthogonal score variant (DoubleML-compatible). PLR: 'partialling out' (default) or 'IV-type'. IRM: 'ATE' (default) or 'ATTE'. None selects the model default; defaults reproduce historical output exactly. |
| `treat` | `string` | ✓ |  | Treatment variable |
| `trimming_threshold` | `number` |  | `0.01` | Symmetric propensity clip [t, 1-t] for irm/iivm (DoubleML trimming_rule='truncate'). Default 0.01 = historical clip. |
| `y` | `string` | ✓ |  | Outcome |

> **model** options: `'plr'`, `'irm'`, `'pliv'`, `'iivm'`

> **score** options: `'partialling out'`, `'IV-type'`, `'ATE'`, `'ATTE'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dml(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `dml_card.py`, `docs/guides/case_study_401k.md`, `docs/guides/choosing_matching_estimator.md`

---
### `sp.dml_diagnostics()`

**Build a :class:`DMLDiagnostics` report from a DML CausalResult.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `clip` | `number` |  | `0.02` | For IRM-style overlap: count units with propensity within ``[0, clip] [1-clip, 1]`` as overlap-violating. |
| `result` | `string` | ✓ |  | Result returned by :func:`statspai.dml.dml`. Must include the post-fit residuals (``model_info['_y_resid']``, ``model_info['_d_resid']``); for IRM, additionally the propensity ``model_info['diagnostics']['pscore_min']`` etc. are surfaced. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dml_diagnostics(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.dml_model_averaging()`

**Model-averaging DML (PLR) per Ahrens et al. (2025, JAE). Fits DML-PLR under multiple candidate nuisance learners and reports a risk-weighted (or equal/single-best) average of their theta estimates with a covariance-adjusted SE.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `candidates` | `array[string]` |  |  | List of (ml_g, ml_m, label) sklearn triples; defaults to Lasso/Ridge/RF/GBM |
| `covariates` | `array[string]` | ✓ |  | Covariate columns X |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Treatment column |
| `weight_rule` | `string (enum)` |  | `'short_stacking'` | Weighting of candidate estimators |
| `y` | `string` | ✓ |  | Outcome column |

> **weight_rule** options: `'short_stacking'`, `'single_best'`, `'inverse_risk'`, `'equal'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dml_model_averaging(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/sp_dml_vs_doubleml.md`, `docs/guides/v1_2_frontier.md`

---
### `sp.dml_panel()`

**Long-panel Double/Debiased ML for static panel models with fixed effects (Clarke & Polselli 2025, simplified). Absorbs unit (and optional time) fixed effects via within-transform, cross-fits ML nuisance learners with folds that split units, and reports cluster-robust SE at the unit level. PLR moment (continuous or binary treatment).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `binary_treatment` | `boolean` |  | `False` | binary_treatment parameter (bool). |
| `covariates` | `array[string]` | ✓ |  | Covariate columns X_it |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `include_time_fe` | `boolean` |  | `False` | Whether to include time fe. |
| `ml_g` | `string` |  |  | Outcome nuisance learner |
| `ml_m` | `string` |  |  | Treatment nuisance learner |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `time` | `string` |  |  | Time column (required if include_time_fe) |
| `treat` | `string` | ✓ |  | Treatment column |
| `unit` | `string` | ✓ |  | Unit ID column (FE + clustering) |
| `y` | `string` | ✓ |  | Outcome column |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dml_panel(y="outcome", data=df, treat="value", covariates=["a", "b"], unit="value")
print(result.summary())
```

> 📁 See also: `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.dml_sensitivity()`

**Compute DML-OVB sensitivity for a fitted DML CausalResult.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `benchmark_covariates` | `array[string]` |  |  | Subset of the original covariates to benchmark against. For each ``X_k``, the benchmark sets ``cf_y_bench, cf_d_bench`` to the partial R2 that ``X_k`` itself contributes (multiplied by ``k_y, k_d`` to express "what if a confounder were kx as strong as ``X_k``?"). |
| `cf_d` | `number` |  |  | Hypothesized partial-R2 of an unobserved confounder with the residualised outcome and treatment. If both are given, the report includes a bias bound and adjusted-estimate range. |
| `cf_y` | `number` |  |  | Hypothesized partial-R2 of an unobserved confounder with the residualised outcome and treatment. If both are given, the report includes a bias bound and adjusted-estimate range. |
| `k_d` | `number` |  | `1.0` | Multipliers for the benchmark strengths. |
| `k_y` | `number` |  | `1.0` | Multipliers for the benchmark strengths. |
| `q` | `number` |  | `1.0` | Bias threshold as a fraction of \|theta\|. ``q=1`` => confounder needed to shrink estimate to zero; ``q=0.5`` => half the estimate. |
| `result` | `string` | ✓ |  | result parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dml_sensitivity(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/sensitivity_analysis.md`, `docs/guides/sp_dml_vs_doubleml.md`

---
### `sp.model_averaging_dml()`

**Model-averaging / stacking DML-PLR estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Two-sided CI level. |
| `candidates` | `array[string]` |  |  | Candidate nuisance learners. ``ml_g`` regresses ``y`` on ``X``; ``ml_m`` regresses ``treat`` on ``X``. Defaults to a Lasso/Ridge/ RandomForest/GradientBoosting roster. |
| `covariates` | `array[string]` | ✓ |  | Covariate columns ``X``. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_folds` | `integer` |  | `5` | Cross-fitting folds per candidate. |
| `sample_weight` | `string` |  |  | Per-observation weights. If supplied, every nuisance fit uses ``sample_weight=`` (with a graceful fallback warning if the learner does not accept it), the CLS stacking objective becomes weighted least squares, and the PLR moment + sandwich variance use weighted sums. The MSE used for ``inverse_risk`` / ``single_best`` weighting is also the weighted MSE. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Continuous-or-binary treatment column. |
| `weight_rule` | `string (enum)` |  | `'short_stacking'` | How to combine candidate nuisance predictions or estimates. * ``"short_stacking"`` *(default; Ahrens et al. 2025 eq. 7)* -- solve constrained least squares on cross-fitted predictions for each nuisance separately (``y`` and ``D``), produce stacked nuisances, plug into the PLR moment equation. * ``"single_best"`` -- Ahrens et al. (2025, fn. 8): pick the candidate with lowest joint nuisance MSE. * ``"inverse_risk"`` -- :math:`w_k \propto 1/(\text{MSE}_g + \text{MSE}_m)`. Convenience baseline; **not** in the paper. * ``"equal"`` -- :math:`w_k = 1/K`. Convenience baseline; **not** in the paper. For the non-stacking rules (``inverse_risk`` / ``equal`` / ``single_best``) the function computes per-candidate :math:`\hat\theta_k` and reports the weighted average with a between-candidate-covariance-corrected SE; for ``"short_stacking"`` it reports the standard PLR sandwich SE on the stacked-nuisance score (Neyman orthogonality is preserved). |
| `y` | `string` | ✓ |  | Outcome column. |

> **weight_rule** options: `'short_stacking'`, `'single_best'`, `'inverse_risk'`, `'equal'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.model_averaging_dml(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
