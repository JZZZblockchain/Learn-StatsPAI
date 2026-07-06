# tmle

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Targeted Maximum Likelihood Estimation (TMLE) with Super Learner.

TMLE is a doubly robust, semiparametrically efficient estimator for
causal effects that combines initial outcome regression with a targeted
bias-correction step using the propensity score.

Components
----------
- **TMLE** : Full TMLE estimator for ATE/ATT with targeting step
- **SuperLearner** : Ensemble learner for nuisance parameter estimation

References
----------
van der Laan, M. J. & Rose, S. (2011).
Targeted Learning: Causal Inference for Observational and Experimental Data.
Springer Series in Statistics. [@vanderlaan2011targeted]

van der Laan, M. J., Polley, E. C., & Hubbard, A. E. (2007).
Super Learner. Statistical Applications in Genetics and Molecular Biology, 6(1). [@vanderlaan2007super]

**11 个公共函数**

### `sp.HALClassifier()`

**L1-penalised HAL logistic classifier (sklearn-compatible duck-typed API).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `C` | `number` |  | `1.0` | Inverse L1 penalty (larger = less shrinkage), as in scikit-learn. |
| `max_anchors_per_col` | `integer` |  | `40` | Cap on step-function anchor points per feature. |
| `random_state` | `integer` |  | `0` | Random seed or RandomState for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.HALClassifier()
print(result.summary())
```

---
### `sp.HALRegressor()`

**L1-penalised HAL regressor (sklearn-compatible duck-typed API).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cv` | `integer` |  | `5` | Folds for the CV penalty search (used only when ``lambda_`` is None). |
| `lambda_` | `number` |  |  | L1 penalty. ``None`` selects it via cross-validation. |
| `max_anchors_per_col` | `integer` |  | `40` | Cap on step-function anchor points per feature. |
| `random_state` | `integer` |  | `0` | Random seed or RandomState for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.HALRegressor()
print(result.summary())
```

---
### `sp.LTMLEResult()`

**Structured output of :func:`ltmle`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K` | `integer` | ✓ |  | K parameter (int). |
> 📝 *K 参数（整数）。*
| `ate` | `number` | ✓ |  | ate parameter (float). |
> 📝 *ate 参数（浮点数）。*
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple[float, float]). |
> 📝 *ci 参数（浮点数二元组）。*
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `psi_control` | `number` | ✓ |  | psi_control parameter (float). |
> 📝 *psi_control 参数（浮点数）。*
| `psi_treated` | `number` | ✓ |  | psi_treated parameter (float). |
> 📝 *psi_treated 参数（浮点数）。*
| `pvalue` | `number` | ✓ |  | pvalue parameter (float). |
> 📝 *pvalue 参数（浮点数）。*
| `regime_control` | `array[string]` | ✓ |  | regime_control parameter (Sequence[int]). |
> 📝 *regime_control 参数（整数序列）。*
| `regime_treated` | `array[string]` | ✓ |  | regime_treated parameter (Sequence[int]). |
> 📝 *regime_treated 参数（整数序列）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LTMLEResult(psi_treated=1.0, psi_control=1.0, ate=1.0, se=1.0, ci=["a", "b"], pvalue=1.0, K=1.0, n_obs=1.0, regime_treated=["a", "b"], regime_control=["a", "b"])
print(result.summary())
```

---
### `sp.LTMLESurvivalResult()`

**Counterfactual survival curves and contrasts.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `K` | `integer` | ✓ |  | K parameter (int). |
> 📝 *K 参数（整数）。*
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `risk_difference_final` | `number` | ✓ |  | risk_difference_final parameter (float). |
> 📝 *risk_difference_final 参数（浮点数）。*
| `risk_difference_final_se` | `number` | ✓ |  | risk_difference_final_se parameter (float). |
> 📝 *risk_difference_final_se 参数（浮点数）。*
| `rmst_ci` | `array[string]` | ✓ |  | rmst_ci parameter (tuple). |
> 📝 *rmst_ci 参数（元组）。*
| `rmst_control` | `number` | ✓ |  | rmst_control parameter (float). |
> 📝 *rmst_control 参数（浮点数）。*
| `rmst_difference` | `number` | ✓ |  | rmst_difference parameter (float). |
> 📝 *rmst_difference 参数（浮点数）。*
| `rmst_pvalue` | `number` | ✓ |  | rmst_pvalue parameter (float). |
> 📝 *rmst_pvalue 参数（浮点数）。*
| `rmst_se` | `number` | ✓ |  | rmst_se parameter (float). |
> 📝 *rmst_se 参数（浮点数）。*
| `rmst_treated` | `number` | ✓ |  | rmst_treated parameter (float). |
> 📝 *rmst_treated 参数（浮点数）。*
| `survival_control` | `string` | ✓ |  | survival_control parameter (np.ndarray). |
> 📝 *survival_control 参数（np.ndarray）。*
| `survival_treated` | `string` | ✓ |  | survival_treated parameter (np.ndarray). |
> 📝 *survival_treated 参数（np.ndarray）。*
| `times` | `string` | ✓ |  | times parameter (np.ndarray). |
> 📝 *times 参数（np.ndarray）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LTMLESurvivalResult(times="value", survival_treated="value", survival_control="value", rmst_treated=1.0, rmst_control=1.0, rmst_difference=1.0, rmst_se=1.0, rmst_ci=["a", "b"], rmst_pvalue=1.0, risk_difference_final=1.0, risk_difference_final_se=1.0, K=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.SuperLearner()`

**Super Learner ensemble (van der Laan et al. 2007).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `library` | `array[string]` |  |  | Candidate learners. If None, uses a default diverse library. |
| `n_folds` | `integer` |  | `5` | Number of cross-validation folds. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `task` | `string` |  | `'regression'` | 'regression' or 'classification'. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SuperLearner()
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.TMLE()`

**Targeted Maximum Likelihood Estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string` |  | `'ATE'` | estimand parameter (str). |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `outcome_library` | `array[string]` |  |  | outcome_library parameter (Optional[List[BaseEstimator]]). |
| `propensity_bounds` | `array[string]` |  | `[0.025, 0.975]` | propensity_bounds parameter (Tuple[float, float]). |
| `propensity_library` | `array[string]` |  |  | propensity_library parameter (Optional[List[BaseEstimator]]). |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.TMLE(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/g_methods_ph.md`, `docs/guides/public_health.md`

---
### `sp.hal_tmle()`

**TMLE with Highly Adaptive Lasso (HAL) nuisance learners (Qian & van der Laan 2025). The stable 'delta' variant plugs HAL into standard TMLE. The reserved 'projection' variant raises NotImplementedError until the Riesz-projection targeting step has reference parity. Known limitations: variant='projection' raises NotImplementedError -- the Riesz-projection targeting step from Li-Qiu-Wang-vdL (2025) Section 3.2 is not yet ported (the v1.11.x code path was a no-op on the point estimate; see CHANGELOG). The implementation roadmap and parity-test gates are in docs/rfc/hal_tmle_projection.md.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `C_propensity` | `number` |  | `1.0` | Inverse L1 penalty for HAL propensity classifier |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string (enum)` |  | `'ATE'` | Estimand |
| `lambda_outcome` | `number` |  |  | Outcome L1 penalty; None -> 5-fold CV |
| `max_anchors_per_col` | `integer` |  | `40` | Column name for max anchors per. |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `treat` | `string` | ✓ |  | Binary treatment |
| `variant` | `string (enum)` |  | `'delta'` | HAL-TMLE variant |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **estimand** options: `'ATE'`, `'ATT'`

> **variant** options: `'delta'`, `'projection'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.hal_tmle(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/v1_2_frontier.md`

---
### `sp.ltmle()`

**Longitudinal TMLE for static regime contrasts.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `baseline` | `array[string]` |  |  | Baseline time-invariant covariates. |
| `censoring` | `array[string]` |  |  | Censoring indicator column per time point (``1=observed``, ``0=censored``). If None, no censoring is modeled. |
| `covariates_time` | `array[string]` | ✓ |  | ``covariates_time[k]`` lists time-k covariate columns (may be empty). Length ``K``. |
| `data` | `string` | ✓ |  | Wide-format panel: one row per unit. |
| `outcome_type` | `string (enum)` |  | `'auto'` | ``auto`` detects from unique values of ``y``. |
| `propensity_bounds` | `array[string]` |  | `[0.01, 0.99]` | Clip propensity to this range for stability. |
| `regime_control` | `string (enum)` |  |  | Regimes to contrast. Default: all-1 vs all-0. A regime may also be a **callable** ``regime(k, history)`` for *dynamic regimes* that depend on the simulated / observed history of baseline and time-varying covariates. The callable receives ``k`` (int 0..K-1) and ``history`` -- a dict mapping column name to the length-``n`` numpy array observed up to that timepoint -- and must return a length-``n`` numpy array of 0/1 treatment assignments. |
| `regime_treated` | `string (enum)` |  |  | Regimes to contrast. Default: all-1 vs all-0. A regime may also be a **callable** ``regime(k, history)`` for *dynamic regimes* that depend on the simulated / observed history of baseline and time-varying covariates. The callable receives ``k`` (int 0..K-1) and ``history`` -- a dict mapping column name to the length-``n`` numpy array observed up to that timepoint -- and must return a length-``n`` numpy array of 0/1 treatment assignments. |
| `treatments` | `array[string]` | ✓ |  | Treatment column per time point, length ``K``. |
| `y` | `string` | ✓ |  | Final outcome column. |

> **outcome_type** options: `'auto'`, `'binary'`, `'continuous'`

> **regime_control** options: `'0'`, `'1'`

> **regime_treated** options: `'0'`, `'1'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ltmle(y="outcome", data=df, treatments=["a", "b"], covariates_time=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/g_methods_ph.md`

---
### `sp.ltmle_survival()`

**LTMLE for a discrete-time survival outcome under dynamic regimes.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `baseline` | `array[string]` |  |  | Time-invariant baseline covariates. |
| `censoring` | `array[string]` |  |  | ``1`` if the subject is observed *through* interval k, ``0`` if right-censored at or before k. If omitted, no censoring. |
| `covariates_time` | `array[string]` | ✓ |  | Time-varying covariates at each interval. |
| `data` | `string` | ✓ |  | Wide-format, one row per subject. |
| `event_indicators` | `array[string]` | ✓ |  | Column names for the per-interval event indicator ``T_k`` (``1`` if the event occurs *in* interval k, ``0`` otherwise). |
| `propensity_bounds` | `array[string]` |  | `[0.01, 0.99]` | propensity_bounds parameter (Tuple[float, float]). |
| `regime_control` | `string` |  |  | Treatment regimes, same semantics as :func:`ltmle`. |
| `regime_treated` | `string` |  |  | Treatment regimes, same semantics as :func:`ltmle`. |
| `treatments` | `array[string]` | ✓ |  | Treatment column per interval. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ltmle_survival(data=df, event_indicators=["a", "b"], treatments=["a", "b"], covariates_time=["a", "b"])
print(result.summary())
```

---
### `sp.super_learner()`

**Fit a Super Learner ensemble.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `library` | `array[string]` |  |  | Candidate learners. If None, uses a default library. |
| `n_folds` | `integer` |  | `5` | Cross-validation folds. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `task` | `string` |  | `'regression'` | 'regression' or 'classification'. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.super_learner(y="outcome", X="value")
print(result.summary())
```

---
### `sp.tmle()`

**Targeted Maximum Likelihood Estimation for ATE/ATT with double-robustness. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `estimand` | `string` |  | `'ATE'` | Target estimand |
| `treat` | `string` | ✓ |  | Binary treatment column (0/1) |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.tmle(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
