# causal_discovery

> 📂 所属分类:02 · 元学习器与机器学习因果推断 (Meta-Learners & ML Causal)

Causal Discovery: Learning causal structure from observational data.

Algorithms
----------
- **NOTEARS** : NO TEARS continuous optimisation for DAG learning
  (Zheng et al. 2018). Formulates structure learning as a smooth
  optimisation problem with an acyclicity constraint.

- **PC Algorithm** : Constraint-based causal discovery using conditional
  independence tests (Spirtes, Glymour, Scheines 2000). Learns a CPDAG
  (completed partially directed acyclic graph).

References
----------
Zheng, X., Aragam, B., Ravikumar, P., & Xing, E. P. (2018).
DAGs with NO TEARS: Continuous Optimization for Structure Learning.
Advances in Neural Information Processing Systems, 31. [@zheng2018dags]

Spirtes, P., Glymour, C., & Scheines, R. (2000).
Causation, Prediction, and Search (2nd ed.). MIT Press. [@spirtes2000causation]

**21 个公共函数**

### `sp.DYNOTEARSResult()`

**Output of :func:`dynotears`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | A parameter (np.ndarray). |
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `lag` | `integer` | ✓ |  | lag parameter (int). |
| `loss` | `number` | ✓ |  | loss parameter (float). |
| `threshold` | `number` | ✓ |  | threshold parameter (float). |
| `variables` | `array[string]` | ✓ |  | variables parameter (List[str]). |
> 📝 *variables 参数（字符串列表）。*
> 📝 *variables 参数（字符串列表）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DYNOTEARSResult(variables=["a", "b"], W="value", A="value", lag=1.0, threshold=1.0, loss=1.0)
print(result.summary())
```

---
### `sp.FCIResult()`

**Partial Ancestral Graph (PAG) learned by :func:`fci`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `ci_test` | `string` | ✓ |  | ci_test parameter (str). |
| `edges` | `array[string]` | ✓ |  | edges parameter (List[Tuple[str, str, str]]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `pag_left` | `string` | ✓ |  | pag_left parameter (pd.DataFrame). |
| `pag_right` | `string` | ✓ |  | pag_right parameter (pd.DataFrame). |
| `separating_sets` | `array[string]` | ✓ |  | separating_sets parameter (Dict[Tuple[str, str], Set[str]]). |
| `skeleton` | `string` | ✓ |  | skeleton parameter (pd.DataFrame). |
| `variables` | `array[string]` | ✓ |  | variables parameter (List[str]). |
> 📝 *variables 参数（字符串列表）。*
> 📝 *variables 参数（字符串列表）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.FCIResult(variables=["a", "b"], skeleton="value", pag_left="value", pag_right="value", edges=["a", "b"], separating_sets=["a", "b"], n_obs=1.0, alpha=1.0, ci_test="value")
print(result.summary())
```

---
### `sp.GESResult()`

**Result of :func:`ges` -- a CPDAG (Markov equivalence class).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adjacency` | `string` | ✓ |  | adjacency parameter (np.ndarray). |
> 📝 *adjacency 参数（np.ndarray）。*
| `bic` | `number` | ✓ |  | bic parameter (float). |
| `names` | `array[string]` | ✓ |  | names parameter (List[str]). |
> 📝 *names 参数（字符串列表）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.GESResult(adjacency="value", names=["a", "b"], bic=1.0)
print(result.summary())
```

---
### `sp.ICPResult()`

**Result of an Invariant Causal Prediction run (:func:`icp`).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `accepted_subsets` | `array[string]` | ✓ |  | accepted_subsets parameter (list[frozenset]). |
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `coefficients` | `array[string]` | ✓ |  | coefficients parameter (dict[str, tuple[float, float]]). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `parents` | `array[string]` | ✓ |  | parents parameter (set[str]). |
| `rejection_reason` | `array[string]` | ✓ |  | rejection_reason parameter (dict[frozenset, str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ICPResult(parents=["a", "b"], accepted_subsets=["a", "b"], rejection_reason=["a", "b"], alpha=1.0, coefficients=["a", "b"], method="value")
print(result.summary())
```

---
### `sp.LPCMCIResult()`

**Output of :func:`lpcmci`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `edge_types` | `string` | ✓ |  | edge_types parameter (np.ndarray). |
> 📝 *edge_types 参数（np.ndarray）。*
| `p_values` | `string` | ✓ |  | p_values parameter (np.ndarray). |
> 📝 *p_values 参数（np.ndarray）。*
| `parents` | `array[string]` | ✓ |  | parents parameter (Dict[str, List[tuple]]). |
> 📝 *parents 参数（字典，值为元组列表）。*
| `tau_max` | `integer` | ✓ |  | tau_max parameter (int). |
> 📝 *tau_max 参数（整数）。*
| `variables` | `array[string]` | ✓ |  | variables parameter (List[str]). |
> 📝 *variables 参数（字符串列表）。*
> 📝 *variables 参数（字符串列表）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LPCMCIResult(variables=["a", "b"], tau_max=1.0, alpha=1.0, edge_types="value", p_values="value", parents=["a", "b"])
print(result.summary())
```

---
### `sp.LiNGAMResult()`

**Result of a :func:`lingam` (DirectLiNGAM) fit.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adjacency` | `string` | ✓ |  | adjacency parameter (np.ndarray). |
> 📝 *adjacency 参数（np.ndarray）。*
| `names` | `array[string]` | ✓ |  | names parameter (List[str]). |
> 📝 *names 参数（字符串列表）。*
| `order` | `array[string]` | ✓ |  | order parameter (List[int]). |
> 📝 *order 参数（整数列表）。*
| `residuals` | `string` | ✓ |  | residuals parameter (np.ndarray). |
> 📝 *residuals 参数（np.ndarray）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LiNGAMResult(order=["a", "b"], adjacency="value", names=["a", "b"], residuals="value")
print(result.summary())
```

---
### `sp.NOTEARS()`

**NOTEARS: Continuous optimization for DAG structure learning.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `h_tol` | `number` |  | `1e-08` | h_tol parameter (float). |
| `lambda1` | `number` |  | `0.1` | lambda1 parameter (float). |
| `max_iter` | `integer` |  | `100` | Maximum number of optimisation iterations. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `rho_max` | `number` |  | `1e+16` | rho_max parameter (float). |
| `variables` | `array[string]` |  |  | variables parameter (Optional[List[str]]). |
| `w_threshold` | `number` |  | `0.3` | w_threshold parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.NOTEARS(data=df)
print(result.summary())
```

---
### `sp.PCAlgorithm()`

**PC Algorithm for causal discovery.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci_test` | `string` |  | `'fisherz'` | ci_test parameter (str). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `forbidden` | `array[string]` |  |  | forbidden parameter (Optional[List[Tuple[str, str]]]). |
| `max_cond_size` | `integer` |  |  | max_cond_size parameter (Optional[int]). |
| `required` | `array[string]` |  |  | required parameter (Optional[List[Tuple[str, str]]]). |
| `variables` | `array[string]` |  |  | variables parameter (Optional[List[str]]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PCAlgorithm(data=df)
print(result.summary())
```

---
### `sp.PCMCIResult()`

**PCMCI output -- lag-specific adjacency + discovered links.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adjacency` | `string` | ✓ |  | adjacency parameter (np.ndarray). |
> 📝 *adjacency 参数（np.ndarray）。*
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `method` | `string` |  | `'PCMCI (Runge et al. 2019)'` | Estimator or algorithm variant to use. |
| `n_effective` | `integer` | ✓ |  | Number of effective. |
| `p_matrix` | `string` | ✓ |  | p_matrix parameter (np.ndarray). |
| `tau_max` | `integer` | ✓ |  | tau_max parameter (int). |
> 📝 *tau_max 参数（整数）。*
| `val_matrix` | `string` | ✓ |  | val_matrix parameter (np.ndarray). |
| `variables` | `array[string]` | ✓ |  | variables parameter (List[str]). |
> 📝 *variables 参数（字符串列表）。*
> 📝 *variables 参数（字符串列表）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PCMCIResult(variables=["a", "b"], tau_max=1.0, alpha=1.0, p_matrix="value", val_matrix="value", adjacency="value", n_effective=1.0)
print(result.summary())
```

---
### `sp.W()`

**Spatial weights matrix with CSR-sparse backing.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `id_order` | `array[string]` |  |  | Explicit ordering of observation ids. Defaults to ``sorted(neighbors)``. |
| `neighbors` | `array[string]` | ✓ |  | Mapping observation id -> list of neighbour ids. |
| `weights` | `array[string]` |  |  | Matching weight values. If ``None``, binary (1.0) weights are used. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.W(neighbors=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/gpu_acceleration.md`, `docs/guides/proximal_family.md`

---
### `sp.dynotears()`

**DYNOTEARS: continuous-optimisation structure learning for structural VARs. Returns contemporaneous (W) and lagged (A) adjacency matrices with the contemporaneous part enforced to be acyclic via the NOTEARS h(W) penalty.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `lag` | `integer` |  | `1` | lag parameter (int). |
| `lambda_a` | `number` |  | `0.05` | lambda_a parameter (float). |
| `lambda_w` | `number` |  | `0.05` | lambda_w parameter (float). |
| `threshold` | `number` |  | `0.1` | threshold parameter (float). |
| `variables` | `array[string]` |  |  | variables parameter (list). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dynotears(data=df)
print(result.summary())
```

---
### `sp.fci()`

**Run FCI. Returns a :class:`FCIResult` with the learned PAG. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for CI tests. |
| `ci_test` | `string` |  | `'fisherz'` | Only Fisher-Z partial-correlation test is supported; extensions (kernel / chi-square) can be added later. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `max_cond_size` | `integer` |  |  | Max size of conditioning set. |
| `variables` | `array[string]` |  |  | Columns to use; defaults to all numeric columns. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.fci(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.ges()`

**Greedy Equivalence Search. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `max_iter` | `integer` |  | `500` | Maximum total edge additions + removals. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ges(data=df)
print(result.summary())
```

---
### `sp.icp()`

**Invariant Causal Prediction: infer direct parents of Y by testing invariance of P(Y | X_S) across environments.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `environment` | `string` | ✓ |  | environment parameter (ndarray). |
| `max_subset_size` | `integer` |  |  | max_subset_size parameter (int). |
| `method` | `string (enum)` |  | `'linear'` | Estimator or algorithm variant to use. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **method** options: `'linear'`, `'nonlinear'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.icp(y="outcome", X="value", environment="value")
print(result.summary())
```

---
### `sp.lingam()`

**Fit DirectLiNGAM (Shimizu 2011). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `standardize` | `boolean` |  | `True` | Zero-mean / unit-variance each variable before the algorithm. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lingam(data=df)
print(result.summary())
```

---
### `sp.lpcmci()`

**Latent-PCMCI: time-series causal discovery allowing hidden common causes. Outputs a lag-specific adjacency tensor with typed edges (directed, bidirected, uncertain).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `tau_max` | `integer` |  | `3` | tau_max parameter (int). |
| `variables` | `array[string]` |  |  | variables parameter (list). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lpcmci(data=df)
print(result.summary())
```

---
### `sp.nonlinear_icp()`

**Alias for ``icp(..., method='nonlinear')`` -- Heinze-Deml et al. 2018.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `environment` | `string` | ✓ |  | environment parameter (np.ndarray). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.nonlinear_icp(y="outcome", X="value", environment="value")
print(result.summary())
```

---
### `sp.notears()`

**Learn a DAG from data using NOTEARS (Zheng et al. 2018). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Observational data (n_samples x d_variables). |
| `h_tol` | `number` |  | `1e-08` | Convergence threshold for acyclicity constraint h(W). |
| `lambda1` | `number` |  | `0.1` | L1 penalty weight for sparsity. Higher = sparser graph. |
| `max_iter` | `integer` |  | `100` | Maximum augmented Lagrangian iterations. |
| `random_state` | `integer` |  | `42` | Random seed. |
| `rho_max` | `number` |  | `1e+16` | Maximum penalty parameter rho. |
| `variables` | `array[string]` |  |  | Column names to use. If None, uses all numeric columns. |
| `w_threshold` | `number` |  | `0.3` | Threshold for pruning small edge weights. Edges with \|W_ij\| < w_threshold are removed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.notears(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.partial_corr_pvalue()`

**Partial-correlation p-value for H0: ``X Y | Z``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `Z` | `string` |  |  | Instrument matrix or auxiliary covariate matrix. |
| `x` | `string` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.partial_corr_pvalue(y="outcome", x=["treatment", "covariate1", "covariate2"])
print(result.summary())
```

---
### `sp.pc_algorithm()`

**Learn causal structure using the PC algorithm. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for conditional independence tests. Lower alpha = sparser graph (fewer edges). |
| `ci_test` | `string` |  | `'fisherz'` | Conditional independence test: 'fisherz' (partial correlation) or 'hsic' (kernel-based, non-linear). |
| `data` | `string` | ✓ |  | Observational data (n_samples x d_variables). |
| `forbidden` | `array[string]` |  |  | Background knowledge: edges that must NOT appear in the final graph (treated as undirected -- both ``(a, b)`` and ``(b, a)`` are forbidden when either is given). The skeleton phase keeps these absent regardless of CI test outcomes. |
| `max_cond_size` | `integer` |  |  | Maximum conditioning set size. If None, goes up to d-2. |
| `required` | `array[string]` |  |  | Background knowledge: directed edges ``a -> b`` that must appear in the CPDAG. The skeleton phase preserves them regardless of CI rejection, and the orientation phase pins their direction. |
| `variables` | `array[string]` |  |  | Column names to use. If None, uses all numeric columns. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pc_algorithm(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/llm_dag_family.md`, `docs/guides/migration-from-r.md`

---
### `sp.pcmci()`

**PCMCI causal discovery for stationary time-series.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_test` | `number` |  |  | Custom CI test ``(x, y, Z) -> p_value``. Defaults to :func:`partial_corr_pvalue`. |
| `data` | `string` | ✓ |  | Time-series DataFrame with one row per time step. Must be strictly ordered (rows are consecutive time points). |
| `max_conds_dim` | `integer` |  |  | Hard cap on the conditioning-set size during PC1. ``None`` means no cap (the algorithm stops automatically when no predictors remain). |
| `mci_alpha` | `number` |  |  | Significance threshold for the final MCI adjacency. Defaults to ``pc_alpha``. |
| `pc_alpha` | `number` |  | `0.05` | Significance threshold used during the PC1 selection stage. |
| `tau_max` | `integer` |  | `3` | Maximum lag to consider for parent candidates. |
| `variables` | `array[string]` |  |  | Columns to use. Defaults to all columns. |
| `verbose` | `boolean` |  | `False` | verbose parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pcmci(data=df)
print(result.summary())
```

---
