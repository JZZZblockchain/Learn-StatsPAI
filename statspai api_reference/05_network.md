# network

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Social network analysis for StatsPAI (``sp.network``).

A numpy/scipy-native SNA toolkit aligned with R's ``igraph`` / ``sna`` /
``statnet`` and Stata's ``nwcommands``, covering the layers an applied
network analyst needs:

Construction
    :func:`network_graph` (factory) and the :class:`Graph` object — build
    from a dense/sparse adjacency, an edge list, or a tidy ``DataFrame``.

Descriptives
    :func:`network_summary`, :func:`transitivity`, :func:`clustering`,
    :func:`reciprocity`, :func:`assortativity`, :func:`network_components`.

Centrality
    :func:`centrality` dispatcher plus :func:`degree_centrality`,
    :func:`closeness_centrality`, :func:`betweenness_centrality`,
    :func:`eigenvector_centrality`, :func:`katz_centrality`, :func:`pagerank`,
    :func:`bonacich_power`, :func:`hits`.

Community detection
    :func:`community_detection` (Louvain / greedy / label propagation) and
    :func:`network_modularity`.

Network regression
    :func:`netlm` / :func:`netlogit` (QAP / MRQAP) and
    :func:`dyadic_regression` (dyadic-cluster-robust SEs).

Network formation
    :func:`ergm` (exponential random graph models via MPLE).

Data & plots
    :func:`karate_club`, :func:`florentine_families`, :func:`network_plot`.

Roadmap
-------
Sparse-CSR storage for very large graphs; full **MCMC-MLE** ERGM estimation
(the current :func:`ergm` uses maximum pseudo-likelihood); **SAOM / RSiena**
stochastic actor-oriented models for network *dynamics*; temporal/multiplex
networks.  These are tracked rather than silently stubbed.

**32 个公共函数**

### `sp.CentralityResult()`

**Per-node centrality table (the ``sp.centrality`` output).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `measures` | `array[string]` | ✓ |  | measures parameter (List[str]). |
| `most_central` | `object` |  | `None` | most_central parameter (Dict[str, Any]). |
| `scores` | `string` | ✓ |  | scores parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CentralityResult(scores="value", measures=["a", "b"])
print(result.summary())
```

---
### `sp.CommunityResult()`

**Community-detection partition (the ``sp.community_detection`` output).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `membership` | `string` | ✓ |  | membership parameter (pd.Series). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `modularity` | `number` | ✓ |  | modularity parameter (float). |
| `n_communities` | `integer` | ✓ |  | Number of communities. |
| `sizes` | `array[string]` |  | `None` | sizes parameter (List[int]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CommunityResult(membership="value", n_communities=1.0, modularity=1.0, method="value")
print(result.summary())
```

---
### `sp.ComponentsResult()`

**Connected-component decomposition of a graph.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `connection` | `string` |  | `'weak'` | connection parameter (str). |
| `largest_size` | `integer` | ✓ |  | largest_size parameter (int). |
| `membership` | `string` | ✓ |  | membership parameter (pd.Series). |
| `n_components` | `integer` | ✓ |  | Number of generated components or embedding dimensions. |
| `sizes` | `array[string]` | ✓ |  | sizes parameter (List[int]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ComponentsResult(n_components=1.0, membership="value", sizes=["a", "b"], largest_size=1.0)
print(result.summary())
```

---
### `sp.DyadicRegressionResult()`

**Dyadic OLS with dyadic-cluster-robust standard errors.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coefficients` | `string` | ✓ |  | coefficients parameter (pd.DataFrame). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `n_dyads` | `integer` | ✓ |  | Number of dyads. |
| `n_nodes` | `integer` | ✓ |  | Number of nodes. |
| `r_squared` | `number` | ✓ |  | r_squared parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DyadicRegressionResult(coefficients="value", n_dyads=1.0, n_nodes=1.0, r_squared=1.0)
print(result.summary())
```

---
### `sp.ERGMResult()`

**ERGM fit by maximum pseudo-likelihood (the ``sp.ergm`` output).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coefficients` | `string` | ✓ |  | coefficients parameter (pd.DataFrame). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `directed` | `boolean` | ✓ |  | directed parameter (bool). |
| `dyad_independent` | `boolean` | ✓ |  | dyad_independent parameter (bool). |
| `log_pseudolikelihood` | `number` | ✓ |  | log_pseudolikelihood parameter (float). |
| `method` | `string` |  | `'MPLE'` | Estimator or algorithm variant to use. |
| `n_dyads` | `integer` | ✓ |  | Number of dyads. |
| `terms` | `array[string]` | ✓ |  | terms parameter (List[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ERGMResult(coefficients="value", terms=["a", "b"], log_pseudolikelihood=1.0, n_dyads=1.0, directed=True, dyad_independent=True)
print(result.summary())
```

---
### `sp.Graph()`

**A social network as a dense adjacency matrix.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adjacency` | `string` | ✓ |  | Square ``(n, n)`` adjacency. Entry ``A[i, j]`` is the weight of the tie from ``i`` to ``j`` (``1`` for an unweighted tie). |
| `allow_self_loops` | `boolean` |  | `False` | Keep the diagonal of ``adjacency``. Off by default (SNA convention). |
| `directed` | `boolean` |  | `False` | If ``False`` the graph is treated as undirected and stored symmetrically. |
| `node_labels` | `array[string]` |  |  | Human-readable node names (defaults to ``"0".."n-1"``). |
| `weighted` | `boolean` |  |  | Whether to treat off-diagonal entries as weights. If ``None`` (default) it is inferred: the graph is *weighted* when any entry is not in ``{0, 1}``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.Graph(adjacency="value")
print(result.summary())
```

---
### `sp.NetworkSummaryResult()`

**Structural summary of a network (the ``sp.network_summary`` output).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assortativity` | `number` | ✓ |  | assortativity parameter (float). |
| `average_clustering` | `number` | ✓ |  | average_clustering parameter (float). |
| `average_path_length` | `number` | ✓ |  | average_path_length parameter (float). |
| `density` | `number` | ✓ |  | density parameter (float). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `diameter` | `number` | ✓ |  | diameter parameter (float). |
| `directed` | `boolean` | ✓ |  | directed parameter (bool). |
| `is_connected` | `boolean` | ✓ |  | is_connected parameter (bool). |
| `largest_component_frac` | `number` | ✓ |  | largest_component_frac parameter (float). |
| `mean_degree` | `number` | ✓ |  | mean_degree parameter (float). |
| `n_components` | `integer` | ✓ |  | Number of generated components or embedding dimensions. |
| `n_edges` | `integer` | ✓ |  | Number of edges. |
| `n_nodes` | `integer` | ✓ |  | Number of nodes. |
| `reciprocity` | `number` | ✓ |  | reciprocity parameter (float). |
| `transitivity` | `number` | ✓ |  | transitivity parameter (float). |
| `weighted` | `boolean` | ✓ |  | weighted parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.NetworkSummaryResult(n_nodes=1.0, n_edges=1.0, directed=True, weighted=True, density=1.0, n_components=1.0, largest_component_frac=1.0, is_connected=True, diameter=1.0, average_path_length=1.0, mean_degree=1.0, transitivity=1.0, average_clustering=1.0, reciprocity=1.0, assortativity=1.0)
print(result.summary())
```

---
### `sp.QAPResult()`

**QAP / MRQAP network-regression result (``sp.netlm`` / ``sp.netlogit``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coefficients` | `string` | ✓ |  | coefficients parameter (pd.DataFrame). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_dyads` | `integer` | ✓ |  | Number of dyads. |
| `nperm` | `integer` | ✓ |  | nperm parameter (int). |
| `p_qap` | `object` | ✓ |  | p_qap parameter (Dict[str, float]). |
| `permutation` | `string` |  | `'dsp'` | permutation parameter (str). |
| `r_squared` | `number` | ✓ |  | r_squared parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.QAPResult(coefficients="value", r_squared=1.0, n_dyads=1.0, nperm=1.0, method="value")
print(result.summary())
```

---
### `sp.assortativity()`

**Newman degree-assortativity coefficient.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | Network whose endpoint-degree correlation should be computed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.assortativity(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.betweenness_centrality()`

**Shortest-path betweenness centrality (Brandes 2001). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | graph parameter. |
| `normalized` | `boolean` |  | `True` | Scale by ``1/((n-1)(n-2))`` (directed) or ``2/((n-1)(n-2))`` (undirected), so scores lie in ``[0, 1]``. |
| `weighted` | `boolean` |  |  | Use tie weights as path lengths (Dijkstra). Defaults to the graph's own weighted flag. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.betweenness_centrality(graph="value")
print(result.summary())
```

---
### `sp.bonacich_power()`

**Bonacich (1987) power centrality.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `beta` | `number` |  | `0.1` | Bonacich attenuation parameter. Positive values reward ties to powerful nodes; negative values reward ties to weak nodes. |
| `graph` | `string` | ✓ |  | Network to score. |
| `weighted` | `boolean` |  |  | Use tie weights; defaults to the graph's weighted flag. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bonacich_power(graph="value")
print(result.summary())
```

---
### `sp.centrality()`

**Centrality dispatcher: degree, closeness, betweenness (Brandes), eigenvector, Katz, PageRank, Bonacich power. Returns a per-node score table.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | graph parameter (Graph). |
| `kind` | `string (enum)` |  | `'all'` | Measure(s) to compute |
| `normalized` | `boolean` |  | `True` | normalized parameter (bool). |

> **kind** options: `'all'`, `'degree'`, `'closeness'`, `'betweenness'`, `'eigenvector'`, `'katz'`, `'pagerank'`, `'bonacich'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.centrality(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.closeness_centrality()`

**Closeness centrality with the Wasserman-Faust disconnected correction.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | Network to score. |
| `weighted` | `boolean` |  |  | Use tie weights as distances. Defaults to the graph's weighted flag. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.closeness_centrality(graph="value")
print(result.summary())
```

---
### `sp.clustering()`

**Per-node local clustering coefficient (Watts-Strogatz). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | Network whose local clustering coefficients should be computed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.clustering(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.community_detection()`

**Partition a network into communities by modularity optimisation: Louvain (Blondel 2008), greedy/CNM (Clauset-Newman-Moore 2004), or label propagation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | graph parameter (Graph). |
| `method` | `string (enum)` |  | `'louvain'` | Detection algorithm |
| `resolution` | `number` |  | `1.0` | resolution parameter (float). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |

> **method** options: `'louvain'`, `'greedy'`, `'label_prop'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.community_detection(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.degree_centrality()`

**Degree centrality. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | graph parameter. |
| `mode` | `string (enum)` |  | `'all'` | mode parameter (str). |
| `normalized` | `boolean` |  | `True` | Divide by ``n - 1`` (the maximum possible degree). |

> **mode** options: `'all'`, `'in'`, `'out'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.degree_centrality(graph="value")
print(result.summary())
```

---
### `sp.dyadic_regression()`

**OLS on dyadic data with Aronow-Samii-Assenova dyadic-cluster-robust standard errors that allow arbitrary dependence between dyads sharing a node (Fafchamps-Gubert).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `i` | `string` | ✓ |  | First-node id column |
| `j` | `string` | ✓ |  | Second-node id column |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dyadic_regression(y="outcome", data=df, covariates=["a", "b"], i="value", j="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.eigenvector_centrality()`

**Eigenvector centrality (leading eigenvector of the adjacency matrix). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | Network to score. |
| `max_iter` | `integer` |  | `1000` | Maximum power-iteration steps. |
| `tol` | `number` |  | `1e-09` | Convergence tolerance on the score vector. |
| `weighted` | `boolean` |  |  | Use tie weights; defaults to the graph's weighted flag. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.eigenvector_centrality(graph="value")
print(result.summary())
```

---
### `sp.ergm()`

**Exponential random graph model (ERGM) fit by maximum pseudo-likelihood (MPLE). Terms: edges, mutual, triangles, nodematch/nodecov/absdiff. MPLE=MLE for dyad-independent models; MCMC-MLE is the roadmap.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `directed` | `boolean` |  |  | directed parameter (bool). |
| `graph` | `string` | ✓ |  | graph parameter (Graph). |
| `node_attrs` | `string` |  |  | node_attrs parameter (DataFrame). |
| `terms` | `array[string]` |  | `['edges']` | ERGM terms, e.g. ['edges','nodematch:gender'] |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ergm(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.florentine_families()`

**Padgett's Florentine marriage network (undirected, 15 families).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.florentine_families()
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.hits()`

**Kleinberg HITS hub and authority scores.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | Directed or undirected network to score. |
| `max_iter` | `integer` |  | `1000` | Maximum power-iteration steps. |
| `tol` | `number` |  | `1e-12` | L1 convergence tolerance for hub and authority vectors. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.hits(graph="value")
print(result.summary())
```

---
### `sp.karate_club()`

**Zachary's karate club friendship network (undirected, 34 nodes).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.karate_club()
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.katz_centrality()`

**Katz centrality.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.1` | Attenuation parameter. Must be below ``1 / lambda_max(A)``. |
| `beta` | `number` |  | `1.0` | Baseline score for each node. |
| `graph` | `string` | ✓ |  | Network to score. |
| `normalized` | `boolean` |  | `True` | L2-normalise the returned vector. |
| `weighted` | `boolean` |  |  | Use tie weights; defaults to the graph's weighted flag. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.katz_centrality(graph="value")
print(result.summary())
```

---
### `sp.netlm()`

**MRQAP linear network regression of one relational matrix on others, with permutation inference (Dekker double-semi-partialling) robust to network autocorrelation. sna::netlm.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `directed` | `boolean` |  |  | directed parameter (bool). |
| `method` | `string (enum)` |  | `'dsp'` | Permutation scheme |
| `nperm` | `integer` |  | `1000` | nperm parameter (int). |
| `predictors` | `string` | ✓ |  | Predictor matrix / list / {name: matrix} |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `y` | `string` | ✓ |  | Dependent network matrix |

> **method** options: `'dsp'`, `'y'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.netlm(y="outcome", predictors="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.netlogit()`

**QAP logistic network regression for a binary dependent network, with dependent-matrix-permutation inference. sna::netlogit analogue.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `directed` | `boolean` |  |  | directed parameter (bool). |
| `nperm` | `integer` |  | `1000` | nperm parameter (int). |
| `predictors` | `string` | ✓ |  | predictors parameter (ndarray). |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. |
| `y` | `string` | ✓ |  | Binary dependent network |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.netlogit(y="outcome", predictors="value")
print(result.summary())
```

---
### `sp.network_components()`

**Connected-component decomposition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `connection` | `string (enum)` |  | `'weak'` | For directed graphs, whether to use weak or strong connectivity. Ignored for undirected graphs. |
| `graph` | `string` | ✓ |  | graph parameter. |

> **connection** options: `'weak'`, `'strong'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.network_components(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.network_modularity()`

**Newman-Girvan modularity ``Q`` of a partition.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | graph parameter. |
| `membership` | `string` | ✓ |  | Community label per node (any hashable labels). |
| `resolution` | `number` |  | `1.0` | resolution parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.network_modularity(graph="value", membership="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.network_plot()`

**Draw a network as a node-link diagram.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter. |
| `cmap` | `string` |  | `'tab10'` | cmap parameter (str). |
| `edge_alpha` | `number` |  | `0.35` | edge_alpha parameter (float). |
| `graph` | `string` | ✓ |  | graph parameter. |
| `labels` | `boolean` |  | `False` | Annotate nodes with their labels. |
| `layout` | `string (enum)` |  | `'spring'` | layout parameter (str). |
| `node_color` | `array[string]` |  |  | Per-node values (e.g. a community membership :class:`pandas.Series`) mapped through ``cmap``. |
| `node_size` | `array[string]` |  |  | Per-node sizes (e.g. a centrality score); rescaled to a sensible point range. |
| `seed` | `integer` |  | `0` | Layout seed (spring layout). |
| `title` | `string` |  |  | title parameter (Optional[str]). |

> **layout** options: `'spring'`, `'circular'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.network_plot(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.network_summary()`

**Structural summary of a network: density, components, diameter, average path length, transitivity (global clustering), reciprocity, and Newman degree assortativity.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | graph parameter (Graph). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.network_summary(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.pagerank()`

**Google PageRank (Brin & Page 1998).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.85` | Probability of following a tie rather than teleporting. |
| `graph` | `string` | ✓ |  | Directed or undirected network to score. |
| `max_iter` | `integer` |  | `1000` | Maximum power-iteration steps. |
| `tol` | `number` |  | `1e-12` | L1 convergence tolerance. |
| `weighted` | `boolean` |  |  | Use tie weights; defaults to the graph's weighted flag. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pagerank(graph="value")
print(result.summary())
```

---
### `sp.reciprocity()`

**Directed reciprocity: share of arcs that are reciprocated.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | Directed network. Undirected inputs return ``1.0`` by construction. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.reciprocity(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
### `sp.transitivity()`

**Global clustering coefficient (transitivity).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `graph` | `string` | ✓ |  | graph parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.transitivity(graph="value")
print(result.summary())
```

> 📁 See also: `docs/guides/social_network_analysis.md`

---
