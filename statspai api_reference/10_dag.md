# dag

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

DAG (Directed Acyclic Graph) module for causal reasoning.

Declare causal graphs, compute adjustment sets, check for collider bias,
enumerate paths, detect bad controls, and visualize causal structures —
the Python equivalent of R's ``dagitty`` and ``ggdag``.

>>> import statspai as sp
>>> g = sp.dag('X -> Y; Z -> X; Z -> Y')
>>> g.adjustment_sets('X', 'Y')
[{'Z'}]
>>> g.backdoor_paths('X', 'Y')
>>> g.bad_controls('X', 'Y')
>>> g.summary('X', 'Y')
>>> g.do('X')  # interventional graph
>>> sp.dag_example('discrimination')  # classic textbook DAG

**18 个公共函数**

### `sp.DAG()`

**A directed acyclic graph for causal reasoning.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `spec` | `string` |  | `''` | Edge specification. Supported formats: - ``"X -> Y; Z -> X; Z -> Y"`` (semicolon-separated) - ``"X -> Y\n Z -> X\n Z -> Y"`` (newline-separated) - ``"X -> Y, Z -> X, Z -> Y"`` (comma-separated) - Bidirected (latent common cause): ``"X <-> Y"`` adds a latent node ``_L_X_Y`` with edges to both X and Y. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DAG()
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_matching_estimator.md`, `docs/guides/paper_pipeline.md`, `docs/guides/replication_workflow.md`

---
### `sp.IdentificationResult()`

**Outcome of an identification query.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `c_components` | `array[string]` | ✓ |  | c_components parameter (list[NodeSet]). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `explanation` | `string` | ✓ |  | explanation parameter (str). |
| `hedge` | `array[string]` | ✓ |  | hedge parameter (tuple[frozenset[str], frozenset[str]] \| None). |
| `identifiable` | `boolean` | ✓ |  | identifiable parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.IdentificationResult(identifiable=True, estimand="value", c_components=["a", "b"], hedge=["a", "b"], explanation="value")
print(result.summary())
```

---
### `sp.LLMCausalAssessResult()`

**Output of :func:`llm_causal_assess`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `level1_accuracy` | `number` | ✓ |  | level1_accuracy parameter (Optional[float]). |
> 📝 *level1_accuracy 参数（可选浮点数）。*
| `level2_accuracy` | `number` | ✓ |  | level2_accuracy parameter (Optional[float]). |
> 📝 *level2_accuracy 参数（可选浮点数）。*
| `llm_identifier` | `string` | ✓ |  | llm_identifier parameter (str). |
> 📝 *llm_identifier 参数（字符串）。*
| `per_item` | `string` | ✓ |  | per_item parameter (pd.DataFrame). |
> 📝 *per_item 参数（pd.DataFrame）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LLMCausalAssessResult(level1_accuracy=1.0, level2_accuracy=1.0, per_item="value", llm_identifier="value")
print(result.summary())
```

---
### `sp.LLMDAGResult()`

**Merged LLM-oracle / CI-test DAG returned by :func:`llm_dag`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci_asserts` | `array[string]` | ✓ |  | ci_asserts parameter (List[Edge]). |
> 📝 *ci_asserts 参数（Edge 列表）。*
| `ci_rejects` | `array[string]` | ✓ |  | ci_rejects parameter (List[Edge]). |
> 📝 *ci_rejects 参数（Edge 列表）。*
| `disagreements` | `array[string]` | ✓ |  | disagreements parameter (List[Tuple[str, str, str]]). |
> 📝 *disagreements 参数（字符串三元组列表）。*
| `edges` | `array[string]` | ✓ |  | edges parameter (List[Edge]). |
> 📝 *edges 参数（Edge 列表）。*
| `oracle_edges` | `array[string]` | ✓ |  | oracle_edges parameter (List[Edge]). |
> 📝 *oracle_edges 参数（Edge 列表）。*
| `provenance` | `object` |  | `None` | provenance parameter (Dict[str, Any]). |
> 📝 *provenance 参数（字典）。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LLMDAGResult(edges=["a", "b"], oracle_edges=["a", "b"], ci_rejects=["a", "b"], ci_asserts=["a", "b"], disagreements=["a", "b"])
print(result.summary())
```

---
### `sp.PairwiseBenchmarkResult()`

**Output of :func:`pairwise_causal_benchmark`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `accuracy` | `number` | ✓ |  | accuracy parameter (float). |
| `per_pair` | `string` | ✓ |  | per_pair parameter (pd.DataFrame). |
| `precision_forward` | `number` | ✓ |  | precision_forward parameter (float). |
| `recall_forward` | `number` | ✓ |  | recall_forward parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PairwiseBenchmarkResult(accuracy=1.0, precision_forward=1.0, recall_forward=1.0, per_pair="value")
print(result.summary())
```

---
### `sp.RuleCheck()`

**Result of checking one do-calculus rule on a DAG.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `applicable` | `boolean` | ✓ |  | applicable parameter (bool). |
| `reason` | `string` | ✓ |  | reason parameter (str). |
| `rule` | `integer` | ✓ |  | rule parameter (int). |
| `transformed` | `string` | ✓ |  | transformed parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RuleCheck(applicable=True, rule=1.0, reason="value", transformed="value")
print(result.summary())
```

---
### `sp.SCM()`

**Structural Causal Model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `equations` | `object` |  | `None` | equations parameter (dict[str, dict[str, Any]]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SCM()
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`

---
### `sp.SWIGGraph()`

**Single World Intervention Graph for a DAG under ``do(X=x)``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `intervention` | `object` | ✓ |  | intervention parameter (Mapping[str, str]). |
| `parent` | `string` | ✓ |  | parent parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SWIGGraph(parent="value")
print(result.summary())
```

---
### `sp.dag()`

**Declare a causal DAG and perform identification analysis: backdoor/frontdoor adjustment sets, d-separation, path enumeration, bad controls detection, variable role classification, do-operator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `spec` | `string` | ✓ |  | Edge spec: "Z -> X; Z -> Y; X -> Y" |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dag(spec="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_mas.md`, `docs/guides/llm_dag_family.md`, `docs/guides/mediation.md`

---
### `sp.dag_example()`

**Load a classic textbook DAG: confounding, collider, mediation, discrimination, movie_star, police, frontdoor, bad_control_earnings, m_bias.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | ✓ |  | Example name, e.g. 'discrimination' |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dag_example(name="value")
print(result.summary())
```

---
### `sp.dag_example_positions()`

**Return hand-tuned node positions for a named example DAG.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | ✓ |  | name parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dag_example_positions(name="value")
print(result.summary())
```

---
### `sp.dag_examples()`

**List available classic DAG examples.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dag_examples()
print(result.summary())
```

---
### `sp.dag_simulate()`

**Run a classic DAG simulation from Cunningham (2021, ch. 3).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n` | `integer` |  | `10000` | Number of observations (default 10000). |
| `name` | `string` | ✓ |  | ``'discrimination'`` or ``'movie_star'``. |
| `seed` | `integer` |  | `42` | Random seed for reproducibility. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.dag_simulate(name="value")
print(result.summary())
```

---
### `sp.identify()`

**Shpitser-Pearl ID algorithm: decide if P(Y | do(X)) is non-parametrically identifiable on a semi-Markovian DAG, return the do-free estimand or a witness hedge.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `dag` | `string` | ✓ |  | dag parameter (DAG). |
| `outcome` | `array[string]` | ✓ |  | Outcome variable column name or outcome array. |
| `treatment` | `array[string]` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.identify(dag="value", treatment=["a", "b"], outcome=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/causal_mas.md`, `docs/guides/choosing_ml_causal_estimator.md`, `docs/guides/replication_workflow.md`

---
### `sp.llm_causal_assess()`

**Level-1 (knowledge) and Level-2 (deductive reasoning) evaluation of an LLM's causal-reasoning ability.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `level1_items` | `string` |  |  | level1_items parameter (DataFrame). |
| `level2_items` | `string` |  |  | level2_items parameter (DataFrame). |
| `llm_client` | `string` | ✓ |  | llm_client parameter (callable). |
| `llm_identifier` | `string` |  | `'llm'` | llm_identifier parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_causal_assess(llm_client="value")
print(result.summary())
```

---
### `sp.llm_dag()`

**Merge an LLM-proposed DAG with a data-driven CI-test skeleton.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci_test` | `string` |  | `'fisherz'` | ci_test parameter (str). |
| `data` | `string` |  |  | Observational data used for CI-test skeleton construction. Required for merge_strategy in {"intersection", "union_with_ci"}. |
| `descriptions` | `object` |  |  | Human-readable description per variable (passed to the oracle). |
| `merge_strategy` | `string (enum)` |  | `'intersection'` | How to combine oracle and CI-test results. |
| `oracle` | `string` |  |  | A callable ``f(variables, descriptions) -> list[(from, to)]``. If ``None``, this function runs a **data-only** pipeline. |
| `variables` | `array[string]` | ✓ |  | Variable names. |

> **merge_strategy** options: `'oracle_only'`, `'intersection'`, `'union_with_ci'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_dag(data=df, variables=["a", "b"])
print(result.summary())
```

---
### `sp.pairwise_causal_benchmark()`

**Pairwise causal-direction discovery benchmark for an LLM.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ground_truth` | `string` | ✓ |  | ground_truth parameter (DataFrame). |
| `llm_client` | `string` | ✓ |  | llm_client parameter (callable). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pairwise_causal_benchmark(ground_truth="value", llm_client="value")
print(result.summary())
```

---
### `sp.swig()`

**Build a Single-World Intervention Graph (SWIG) by node-splitting intervened variables. Bridges Pearl's SCM and Hernan-Robins potential-outcome languages.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `dag` | `string` | ✓ |  | dag parameter (DAG). |
| `intervention` | `array[string]` | ✓ |  | intervention parameter (dict \| list). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.swig(dag="value", intervention=["a", "b"])
print(result.summary())
```

---
