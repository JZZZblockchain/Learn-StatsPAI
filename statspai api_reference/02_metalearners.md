# metalearners

> 📂 所属分类:02 · 元学习器与机器学习因果推断 (Meta-Learners & ML Causal)

Meta-Learners for heterogeneous treatment effect estimation.

Provides S/T/X/R/DR-Learner implementations that decompose CATE
estimation into standard supervised-learning sub-problems. All learners
accept any scikit-learn compatible estimator.

References
----------
Kunzel et al. (2019). Metalearners for estimating heterogeneous treatment
effects using machine learning. PNAS, 116(10), 4156-4165. [@kunzel2019metalearners]

Nie & Wager (2021). Quasi-oracle estimation of heterogeneous treatment
effects. Biometrika, 108(2), 299-319. [@nie2021quasi]

Kennedy (2023). Towards optimal doubly robust estimation of heterogeneous
causal effects. Electronic Journal of Statistics, 17(2), 3008-3049. [@kennedy2023towards]

**23 个公共函数**

### `sp.AutoCATEResult()`

**Leaderboard + winner from ``sp.auto_cate``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `agreement` | `string` | ✓ |  | agreement parameter (pd.DataFrame). |
| `best_learner` | `string` | ✓ |  | best_learner parameter (str). |
| `best_result` | `string` | ✓ |  | best_result parameter (CausalResult). |
| `leaderboard` | `string` | ✓ |  | leaderboard parameter (pd.DataFrame). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `results` | `object` | ✓ |  | results parameter (Dict[str, CausalResult]). |
| `selection_rule` | `string` | ✓ |  | selection_rule parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.AutoCATEResult(leaderboard="value", best_learner="value", best_result="value", agreement="value", selection_rule="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.CATEEvalResult()`

**Output of :func:`cate_eval`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `autoc` | `number` | ✓ |  | autoc parameter (float). |
| `autoc_ci` | `array[string]` | ✓ |  | autoc_ci parameter (Tuple[float, float]). |
| `autoc_se` | `number` | ✓ |  | autoc_se parameter (float). |
| `method` | `string` |  | `'Yadlowsky et al. 2025 (DR-RATE, IF-SE)'` | Estimator or algorithm variant to use. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `qini` | `number` | ✓ |  | qini parameter (float). |
| `qini_ci` | `array[string]` | ✓ |  | qini_ci parameter (Tuple[float, float]). |
| `qini_se` | `number` | ✓ |  | qini_se parameter (float). |
| `target` | `string` |  | `'AUTOC'` | target parameter (str). |
| `toc_curve` | `string` | ✓ |  | toc_curve parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CATEEvalResult(autoc=1.0, autoc_se=1.0, autoc_ci=["a", "b"], qini=1.0, qini_se=1.0, qini_ci=["a", "b"], toc_curve="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.ClusterCATEResult()`

**Per-cluster CATE table.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_table` | `string` | ✓ |  | cluster_table parameter (pd.DataFrame). |
| `n_clusters` | `integer` | ✓ |  | Number of clusters. |
> 📝 *聚类数量。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ClusterCATEResult(cluster_table="value", n_clusters=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.DRLearner()`

**DR-Learner (Kennedy 2023): doubly robust CATE estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cate_model` | `string` |  |  | Final-stage model for tau(X). |
| `n_folds` | `integer` |  | `5` | Cross-fitting folds for nuisance estimation. |
| `outcome_model` | `string` |  |  | Model for mu_d(X) = E[Y\|X, D=d]. |
| `propensity_model` | `string` |  |  | Model for e(X) = P(D=1\|X). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DRLearner()
print(result.summary())
```

---
### `sp.FunctionalCATEResult()`

**Output of FOCaL functional CATE estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cate_grid` | `string` | ✓ |  | Grid of cate values to evaluate. |
| `function_grid` | `string` | ✓ |  | Grid of function values to evaluate. |
| `n_test` | `integer` | ✓ |  | Number of test. |
| `n_train` | `integer` | ✓ |  | Number of train. |
| `se_grid` | `string` | ✓ |  | Grid of se values to evaluate. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FunctionalCATEResult(cate_grid="value", function_grid="value", se_grid="value", n_train=1.0, n_test=1.0)
print(result.summary())
```

---
### `sp.RLearner()`

**R-Learner (Nie & Wager 2021).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cate_model` | `string` |  |  | Model for tau(X). Fit on pseudo-outcome. |
| `n_folds` | `integer` |  | `5` | Cross-fitting folds for nuisance estimation. |
| `outcome_model` | `string` |  |  | Model for m(X) = E[Y\|X]. |
| `propensity_model` | `string` |  |  | Model for e(X) = P(D=1\|X). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RLearner()
print(result.summary())
```

---
### `sp.SLearner()`

**S-Learner: single model, treatment as a feature.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | `string` |  |  | Outcome model mu(X, D). Default: GradientBoostingRegressor. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SLearner()
print(result.summary())
```

---
### `sp.TLearner()`

**T-Learner: separate models for each treatment arm.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_0` | `string` |  |  | Control outcome model. Default: GradientBoostingRegressor. |
| `model_1` | `string` |  |  | Treated outcome model. Default: same type as model_0. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.TLearner()
print(result.summary())
```

---
### `sp.XLearner()`

**X-Learner (Kunzel et al. 2019).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cate_model_0` | `string` |  |  | CATE model for control-side imputed effects. |
| `cate_model_1` | `string` |  |  | CATE model for treated-side imputed effects. |
| `model_0` | `string` |  |  | Control outcome model. |
| `model_1` | `string` |  |  | Treated outcome model. |
| `propensity_model` | `string` |  |  | Model for e(x) = P(D=1\|X). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.XLearner()
print(result.summary())
```

---
### `sp.auto_cate()`

**Race several meta-learners and return a scored leaderboard + winner.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for both learner confidence intervals and the BLP-beta1 acceptance region used by the selection rule. |
| `cate_model` | `string` |  |  | Override the default gradient-boosting models used for nuisance and final CATE fitting. |
| `covariates` | `array[string]` | ✓ |  | Effect-modifier columns used as features for every nuisance and CATE model. |
| `data` | `string` | ✓ |  | Input data. Must contain ``y``, ``treat`` and all ``covariates``. |
| `learners` | `array[string]` |  | `['s', 't', 'x', 'r', 'dr']` | Short codes of the meta-learners to race. Duplicates are ignored. |
| `n_bootstrap` | `integer` |  | `200` | Bootstrap iterations for ATE standard error on non-DR learners (passed through to ``metalearner``). |
| `n_folds` | `integer` |  | `5` | Number of folds used for both the shared nuisance cross-fit and each learner's honest CATE prediction. |
| `outcome_model` | `string` |  |  | Override the default gradient-boosting models used for nuisance and final CATE fitting. |
| `propensity_model` | `string` |  |  | Override the default gradient-boosting models used for nuisance and final CATE fitting. |
| `random_state` | `integer` |  | `42` | Seed for all K-fold splits. |
| `score` | `string` |  | `'r_loss'` | Currently only ``'r_loss'`` is implemented. Reserved for future expansion. |
| `treat` | `string` | ✓ |  | Binary treatment column name (values in {0, 1}). |
| `y` | `string` | ✓ |  | Outcome column name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.auto_cate(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.auto_cate_tuned()`

**Optuna-tuned CATE learner race -- nuisance, per-learner, or both.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `string` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `learners` | `string` |  | `['s', 't', 'x', 'r', 'dr']` | learners parameter (LearnersArg). |
| `n_bootstrap` | `integer` |  | `200` | Number of bootstrap replications. |
> 📝 *bootstrap 重复次数。*
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `n_trials` | `integer` |  | `25` | Budget for the nuisance-tuning study (ignored when ``tune == 'per_learner'``). |
| `n_trials_per_learner` | `integer` |  |  | Budget for each per-learner study. Defaults to ``max(5, n_trials // 3)``. |
| `per_learner_search_space` | `array[string]` |  |  | Override default spaces. See :data:`DEFAULT_SEARCH_SPACE` and :data:`DEFAULT_PER_LEARNER_SEARCH_SPACE`. Passed through / see :func:`auto_cate`. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `sampler` | `string` |  |  | sampler parameter (Optional[Any]). |
| `search_space` | `array[string]` |  |  | Override default spaces. See :data:`DEFAULT_SEARCH_SPACE` and :data:`DEFAULT_PER_LEARNER_SEARCH_SPACE`. Passed through / see :func:`auto_cate`. |
| `timeout` | `number` |  |  | Wall-clock limit per study (seconds). |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `tune` | `string (enum)` |  | `'nuisance'` | Tuning regime: - ``'nuisance'`` -- tune the shared outcome / propensity GBMs against held-out R-loss, then hand them to ``auto_cate``. (v0.9.5 behaviour.) - ``'per_learner'`` -- keep default nuisance models; for each learner, tune its final-stage CATE model against held-out R-loss. - ``'both'`` -- run ``'nuisance'`` first, then ``'per_learner'`` using the tuned nuisance. Most expensive; most thorough. |
| `verbose` | `boolean` |  | `False` | verbose parameter (bool). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **tune** options: `'nuisance'`, `'per_learner'`, `'both'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.auto_cate_tuned(y="outcome", data=df, treat="value", covariates="value")
print(result.summary())
```

---
### `sp.blp_test()`

**Best Linear Predictor (BLP) test for CATE heterogeneity.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `covariates` | `array[string]` | ✓ |  | Covariate column names. |
| `data` | `string` | ✓ |  | Original data. |
| `n_folds` | `integer` |  | `5` | Folds for propensity cross-fitting. |
| `result` | `string` | ✓ |  | Result from ``metalearner()``. |
| `treat` | `string` | ✓ |  | Outcome and treatment column names. |
| `y` | `string` | ✓ |  | Outcome and treatment column names. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.blp_test(y="outcome", data=df, result="value", treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.cate_by_group()`

**Group-level average treatment effects.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for CIs. |
| `by` | `string` | ✓ |  | Column name to group by, or 'cate' to group by CATE quartiles. |
| `data` | `string` | ✓ |  | Original data (same rows as the estimation sample). |
| `n_groups` | `integer` |  | `4` | Number of quantile groups when ``by='cate'`` or when the grouping variable is continuous. |
| `result` | `string` | ✓ |  | Result from ``metalearner()``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cate_by_group(data=df, result="value", by="value")
print(result.summary())
```

---
### `sp.cate_eval()`

**Evaluate any CATE estimator via RATE / AUTOC / Qini (Yadlowsky 2025).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `T` | `string` | ✓ |  | Observed outcome and binary treatment. |
| `X` | `string` |  |  | Required if any of ``e_hat / m_hat / mu1_hat / mu0_hat`` is None; cross-fit nuisances are estimated with GBM defaults. |
| `Y` | `string` | ✓ |  | Observed outcome and binary treatment. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cate` | `string` | ✓ |  | Estimated CATE :math:`\hat\tau(X_i)` from any estimator. |
| `clip` | `number` |  | `0.02` | Propensity clip. |
| `e_hat` | `string` |  |  | Pre-computed nuisance predictions (e.g., from the same estimator that produced ``cate``). If provided, no internal cross-fitting runs. |
| `m_hat` | `string` |  |  | Pre-computed nuisance predictions (e.g., from the same estimator that produced ``cate``). If provided, no internal cross-fitting runs. |
| `mu0_hat` | `string` |  |  | Pre-computed nuisance predictions (e.g., from the same estimator that produced ``cate``). If provided, no internal cross-fitting runs. |
| `mu1_hat` | `string` |  |  | Pre-computed nuisance predictions (e.g., from the same estimator that produced ``cate``). If provided, no internal cross-fitting runs. |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `q_grid` | `integer` |  | `100` | Grid of q values to evaluate. |
| `random_state` | `integer` |  | `0` | Random seed or RandomState for reproducible stochastic steps. |
| `target` | `string (enum)` |  | `'AUTOC'` | Which scalar headline to emit; both are computed and returned. |

> **target** options: `'AUTOC'`, `'QINI'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cate_eval(cate="value", Y="value", T="value")
print(result.summary())
```

---
### `sp.cate_group_plot()`

**Plot group-level CATEs with confidence intervals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `color` | `string` |  | `'#2C3E50'` | color parameter (str). |
| `figsize` | `array[string]` |  | `[8, 5]` | figsize parameter (tuple). |
| `group_df` | `string` | ✓ |  | Output from ``cate_by_group()``. |
| `title` | `string` |  |  | title parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cate_group_plot(group_df="value")
print(result.summary())
```

---
### `sp.cate_plot()`

**Plot the CATE distribution.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `color` | `string` |  | `'#2C3E50'` | color parameter (str). |
| `figsize` | `array[string]` |  | `[8, 5]` | figsize parameter (tuple). |
| `kind` | `string` |  | `'hist'` | 'hist' for histogram, 'kde' for kernel density, 'both'. |
| `result` | `string` | ✓ |  | Result from ``metalearner()``. |
| `title` | `string` |  |  | title parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cate_plot(result="value")
print(result.summary())
```

---
### `sp.cate_summary()`

**Descriptive statistics of the CATE distribution.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | Result from ``metalearner()`` containing ``model_info['cate']``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cate_summary(result="value")
print(result.summary())
```

---
### `sp.cluster_cate()`

**Cluster-based CATE estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_clusters` | `integer` |  | `4` | Number of K-means clusters. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cluster_cate(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.compare_metalearners()`

**Fit multiple meta-learners and compare their ATE estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate / effect modifier variables. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `learners` | `array[string]` |  |  | Which learners to compare. Default: all five ('s','t','x','r','dr'). |
| `treat` | `string` | ✓ |  | Binary treatment variable (0/1). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.compare_metalearners(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.focal_cate()`

**Functional doubly-robust CATE estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | Training data with outcome columns y_columns (one per function evaluation point t). |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `test_data` | `string` |  |  | Defaults to ``data``. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y_columns` | `array[string]` | ✓ |  | Outcome columns; len = number of function points. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.focal_cate(data=df, y_columns=["a", "b"], treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.gate_test()`

**Test for significant heterogeneity across GATE (Group ATE) groups.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `by` | `string` | ✓ |  | Column name to group by, or 'cate' for CATE quartiles. |
| `data` | `string` | ✓ |  | Original data (same rows as estimation). |
| `n_groups` | `integer` |  | `4` | Number of groups. |
| `result` | `string` | ✓ |  | Result from ``metalearner()``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.gate_test(data=df, result="value", by="value")
print(result.summary())
```

---
### `sp.metalearner()`

**Meta-learner framework for CATE: S-, T-, X-, R-, DR-Learner. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `learner` | `string (enum)` |  | `'dr'` | Learner type |
| `treat` | `string` | ✓ |  | Binary treatment column (0/1) |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **learner** options: `'s'`, `'t'`, `'x'`, `'r'`, `'dr'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.metalearner(y="outcome", data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.predict_cate()`

**Predict CATE on new (out-of-sample) data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `new_data` | `string` | ✓ |  | New data with the same covariate columns used in estimation. |
| `result` | `string` | ✓ |  | Result from ``metalearner()`` containing a fitted estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.predict_cate(result="value", new_data="value")
print(result.summary())
```

---
