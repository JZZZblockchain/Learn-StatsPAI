# interference

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Interference and Spillover Effects.

Estimates direct and spillover treatment effects when SUTVA
(Stable Unit Treatment Value Assumption) is violated, i.e.,
one unit's treatment affects another unit's outcome.

References
----------
Hudgens, M. G. & Halloran, M. E. (2008).
Toward Causal Inference with Interference.
JASA, 103(482), 832-842. [@hudgens2008toward]

Aronow, P. M. & Samii, C. (2017).
Estimating Average Causal Effects Under General Interference.
Annals of Applied Statistics, 11(4), 1912-1947. [@aronow2017estimating]

**20 个公共函数**

### `sp.CrossClusterRCTResult()`

**Output of cross-cluster RCT with interference correction.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `direct_effect` | `number` | ✓ |  | direct_effect parameter (float). |
| `direct_se` | `number` | ✓ |  | direct_se parameter (float). |
| `method` | `string` |  | `'Cluster RCT with Cross-Cluster Interference'` | Estimator or algorithm variant to use. |
| `n_clusters` | `integer` | ✓ |  | Number of clusters. |
> 📝 *聚类数量。*
| `spillover_effect` | `number` | ✓ |  | spillover_effect parameter (float). |
| `spillover_se` | `number` | ✓ |  | spillover_se parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CrossClusterRCTResult(direct_effect=1.0, direct_se=1.0, spillover_effect=1.0, spillover_se=1.0, n_clusters=1.0)
print(result.summary())
```

---
### `sp.DNCGNNDiDResult()`

**Output of DNC + GNN + DiD.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[dict]). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` |  | `'DNC + GNN-aware DiD'` | Estimator or algorithm variant to use. |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DNCGNNDiDResult(estimate=1.0, se=1.0, ci=["a", "b"], n_obs=1.0)
print(result.summary())
```

---
### `sp.InwardOutwardResult()`

**Output of :func:`inward_outward_spillover`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `inward_effect` | `number` | ✓ |  | inward_effect parameter (float). |
| `inward_se` | `number` | ✓ |  | inward_se parameter (float). |
| `outward_effect` | `number` | ✓ |  | outward_effect parameter (float). |
| `outward_se` | `number` | ✓ |  | outward_se parameter (float). |
| `ratio_in_out` | `number` | ✓ |  | ratio_in_out parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.InwardOutwardResult(inward_effect=1.0, outward_effect=1.0, inward_se=1.0, outward_se=1.0, ratio_in_out=1.0)
print(result.summary())
```

---
### `sp.MatchedPairResult()`

**Output of matched-pair cluster RCT estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` |  | `'Matched-Pair Cluster RCT'` | Estimator or algorithm variant to use. |
> 📝 *要使用的估计器或算法变体。*
| `n_clusters` | `integer` | ✓ |  | Number of clusters. |
> 📝 *聚类数量。*
| `n_pairs` | `integer` | ✓ |  | Number of pairs. |
> 📝 *配对数。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MatchedPairResult(estimate=1.0, se=1.0, ci=["a", "b"], n_pairs=1.0, n_clusters=1.0)
print(result.summary())
```

---
### `sp.NetworkExposureResult()`

**Container for :func:`network_exposure` Horvitz-Thompson estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `contrasts` | `string` | ✓ |  | contrasts parameter (pd.DataFrame). |
| `design` | `string` | ✓ |  | design parameter (str). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `estimates` | `string` | ✓ |  | estimates parameter (pd.DataFrame). |
| `exposure_levels` | `array[string]` | ✓ |  | exposure_levels parameter (List[str]). |
| `mapping` | `string` | ✓ |  | mapping parameter (str). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `p_treat` | `number` | ✓ |  | p_treat parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.NetworkExposureResult(estimates="value", contrasts="value", exposure_levels=["a", "b"], n_obs=1.0, p_treat=1.0, design="value", mapping="value")
print(result.summary())
```

---
### `sp.NetworkHTEResult()`

**Output of :func:`network_hte`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_alpha` | `number` | ✓ |  | ci_alpha parameter (float). |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `direct_effect` | `number` | ✓ |  | direct_effect parameter (float). |
| `direct_se` | `number` | ✓ |  | direct_se parameter (float). |
| `individual_direct` | `string` | ✓ |  | individual_direct parameter (np.ndarray). |
| `individual_spillover` | `string` | ✓ |  | individual_spillover parameter (np.ndarray). |
| `spillover_effect` | `number` | ✓ |  | spillover_effect parameter (float). |
| `spillover_se` | `number` | ✓ |  | spillover_se parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.NetworkHTEResult(direct_effect=1.0, direct_se=1.0, spillover_effect=1.0, spillover_se=1.0, individual_direct="value", individual_spillover="value", covariates=["a", "b"], ci_alpha=1.0)
print(result.summary())
```

---
### `sp.PeerEffectsResult()`

**Container for :func:`peer_effects` linear-in-means estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (Dict[str, tuple]). |
| `coefficients` | `string` | ✓ |  | coefficients parameter (pd.DataFrame). |
| `contextual_peer` | `object` | ✓ |  | contextual_peer parameter (Dict[str, float]). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `direct` | `object` | ✓ |  | direct parameter (Dict[str, float]). |
| `endogenous_peer` | `number` | ✓ |  | endogenous_peer parameter (float). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `se` | `object` | ✓ |  | se parameter (Dict[str, float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PeerEffectsResult(endogenous_peer=1.0, ci=["a", "b"], n_obs=1.0, coefficients="value")
print(result.summary())
```

---
### `sp.SpilloverEstimator()`

**Spillover / interference effects estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Cluster identifier column for clustered standard errors. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `exposure_fn` | `string` |  | `'fraction'` | exposure_fn parameter (str). |
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
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

result = sp.SpilloverEstimator(y="outcome", data=df, treat="value", cluster="value")
print(result.summary())
```

---
### `sp.StaggeredClusterRCTResult()`

**Staggered-rollout cluster RCT output.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `event_study` | `string` | ✓ |  | event_study parameter (pd.DataFrame). |
| `method` | `string` |  | `'Staggered-Rollout Cluster RCT'` | Estimator or algorithm variant to use. |
| `n_clusters` | `integer` | ✓ |  | Number of clusters. |
> 📝 *聚类数量。*
| `overall_att` | `number` | ✓ |  | overall_att parameter (float). |
| `overall_se` | `number` | ✓ |  | overall_se parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.StaggeredClusterRCTResult(overall_att=1.0, overall_se=1.0, event_study="value", n_clusters=1.0)
print(result.summary())
```

---
### `sp.cluster_cross_interference()`

**Cluster-randomised trial under cross-cluster interference (Ding et al. 2025). Estimates direct + spillover effects when treatment of one cluster affects outcomes in adjacent clusters. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` | ✓ |  | Cluster identifier column for clustered standard errors. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `neighbour_treat_share` | `string` | ✓ |  | Column with neighbours' treatment share |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cluster_cross_interference(y="outcome", data=df, cluster="value", treat="value", neighbour_treat_share="value")
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.cluster_matched_pair()`

**Matched-pair cluster RCT estimator (weighted DIM + Bai SE).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Cluster identifier. |
| `data` | `string` | ✓ |  | Individual-level data. |
| `pair` | `string` | ✓ |  | Pair identifier (each pair contains exactly two clusters). |
| `treat` | `string` | ✓ |  | Cluster-level binary treatment. |
| `y` | `string` | ✓ |  | Outcome. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cluster_matched_pair(y="outcome", data=df, cluster="value", treat="value", pair="value")
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.cluster_staggered_rollout()`

**Staggered-rollout cluster RCT estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | first_treat = first calendar time the cluster is treated (0 / NaN for never-treated). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `first_treat` | `string` | ✓ |  | first_treat = first calendar time the cluster is treated (0 / NaN for never-treated). |
| `lags` | `integer` |  | `4` | lags parameter (int). |
| `leads` | `integer` |  | `2` | leads parameter (int). |
| `time` | `string` | ✓ |  | first_treat = first calendar time the cluster is treated (0 / NaN for never-treated). |
| `y` | `string` | ✓ |  | first_treat = first calendar time the cluster is treated (0 / NaN for never-treated). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cluster_staggered_rollout(y="outcome", data=df, cluster="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.dnc_gnn_did()`

**DiD with double negative controls + (optional) GNN embedding for**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | Long-format panel. |
| `embedding` | `string` |  |  | Pre-computed (n_units, k) GNN embedding. If None, use simple unit-level lagged outcome as a stand-in network feature. |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. |
| `n_boot` | `integer` |  | `100` | Number of bootstrap replications. |
| `nc_exposure` | `array[string]` | ✓ |  | Negative-control exposures -- pseudo-treatments expected NOT to cause the outcome. |
| `nc_outcome` | `array[string]` | ✓ |  | Negative-control outcomes -- variables expected NOT affected by the treatment but sharing the same confounding structure. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat` | `string` | ✓ |  | First-treatment-period column (0 = never-treated). |
| `y` | `string` | ✓ |  | Outcome. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dnc_gnn_did(y="outcome", data=df, treat="value", time="value", id="value", nc_outcome=["a", "b"], nc_exposure=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.interference()`

**Unified interference / spillover dispatcher. design= selects the estimator: 'partial' (Hudgens-Halloran cluster) / 'network_exposure' (Aronow-Samii HT) / 'peer_effects' (Manski / Bramoulle linear-in-means) / 'network_hte' (Wu & Yuan 2025 orthogonal, arXiv:2509.18484) / 'inward_outward' (directed network; Fang, Airoldi & Forastiere 2025, arXiv:2506.06615) / 'cluster_matched_pair' (Bai 2022) / 'cluster_cross' (Ding et al. 2025) / 'cluster_staggered' (Zhou et al. 2025) / 'dnc_gnn' (Zhao et al. 2026). Kwargs pass through to the target function; see sp.interference_family guide. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `design` | `string` |  | `'partial'` | Interference design -- call sp.interference_available_designs() for the full list. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.interference()
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.interference_available_designs()`

**Return the full list of registered interference ``design`` names.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.interference_available_designs()
print(result.summary())
```

---
### `sp.inward_outward_spillover()`

**Decompose network spillover into inward (incoming edges to unit i) and outward (from i to neighbours) components.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `inward_exposure` | `string` | ✓ |  | inward_exposure parameter (str). |
| `outward_exposure` | `string` | ✓ |  | outward_exposure parameter (str). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.inward_outward_spillover(y="outcome", data=df, treatment="value", inward_exposure="value", outward_exposure="value")
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.network_exposure()`

**Aronow-Samii Horvitz-Thompson estimator for arbitrary interference via a user-supplied exposure mapping. Handles Bernoulli randomisation designs with simulated conservative variance. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact). Known limitations: design='complete' is reserved but not implemented; passing it raises NotImplementedError. Use design='bernoulli' with p_treat=K/N as an approximation only if that matches the assignment mechanism you are willing to assume.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `Y` | `string` | ✓ |  | Outcome vector |
| `Z` | `string` | ✓ |  | Treatment vector (0/1) |
| `adjacency` | `string` | ✓ |  | Adjacency matrix (n x n) or sparse |
| `design` | `string (enum)` |  | `'bernoulli'` | Randomisation design |
| `mapping` | `string (enum)` |  | `'as4'` | Exposure mapping |
| `n_sim` | `integer` |  | `2000` | Number of sim. |
| `p_treat` | `number` |  |  | Marginal treatment probability |

> **design** options: `'bernoulli'`, `'complete'`

> **mapping** options: `'as4'`, `'as3'`, `'as2'`, `'custom'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.network_exposure(Y="value", Z="value", adjacency="value")
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.network_hte()`

**Orthogonal learning of direct + spillover effects under network interference via cross-fitted double-residualisation (Wu & Yuan 2025, arXiv:2509.18484).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_folds` | `integer` |  | `5` | Number of cross-fitting or cross-validation folds. |
| `neighbor_exposure` | `string` | ✓ |  | neighbor_exposure parameter (str). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.network_hte(y="outcome", data=df, treatment="value", neighbor_exposure="value", covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.peer_effects()`

**Fit the linear-in-means peer-effects model via 2SLS.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `include_contextual` | `boolean` |  | `True` | Include the contextual peer effect (W X) as regressors. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.peer_effects(y="outcome", data=df, covariates=["a", "b"], W="value")
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
### `sp.spillover()`

**Direct + spillover treatment effect estimation under partial interference (within-cluster). Uses the Hudgens-Halloran decomposition with chosen exposure function. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` | ✓ |  | Cluster column (interference boundary) |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `exposure_fn` | `string (enum)` |  | `'fraction'` | Exposure function |
| `n_bootstrap` | `integer` |  | `500` | Number of bootstrap replications. |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. |
> 📝 *处理指示变量或首次处理周期列。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **exposure_fn** options: `'fraction'`, `'any'`, `'count'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.spillover(y="outcome", data=df, treat="value", cluster="value")
print(result.summary())
```

> 📁 See also: `docs/guides/interference_family.md`

---
