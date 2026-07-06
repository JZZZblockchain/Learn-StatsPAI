# causal_llm

> 📂 所属分类:02 · 元学习器与机器学习因果推断 (Meta-Learners & ML Causal)

LLM × Causal Inference (StatsPAI v0.10).

Three integration points where large language models help causal
analysis without replacing the formal estimator:

* :func:`llm_dag_propose` — propose candidate DAGs from variable
  names + domain description (Kiciman-Sharma 2025, arXiv 2402.11068).
* :func:`llm_unobserved_confounders` — generate plausible unobserved
  confounder candidates for E-value sensitivity analysis
  (arXiv 2603.14273).
* :func:`llm_sensitivity_priors` — propose Cornfield-style sensitivity
  parameter priors based on the substantive context.

All three are **offline** by default — they ship with deterministic
heuristic backends so they work without an API key. If a real LLM
client (OpenAI / Anthropic / local) is available via the optional
``[llm]`` extra, set the ``client`` keyword argument.

The deterministic backends are designed to be **transparent**: they
return reproducible candidates derived from variable-name pattern
matching and domain heuristics, not silent fabrications.

**14 个公共函数**

### `sp.DAGValidationResult()`

**Output of :func:`llm_dag_validate`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `edge_evidence` | `string` | ✓ |  | edge_evidence parameter (pd.DataFrame). |
| `n_supported` | `integer` | ✓ |  | Number of supported. |
| `n_unsupported` | `integer` | ✓ |  | Number of unsupported. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DAGValidationResult(edge_evidence="value", n_supported=1.0, n_unsupported=1.0, alpha=1.0)
print(result.summary())
```

---
### `sp.LLMConstrainedDAGResult()`

**Output of :func:`llm_dag_constrained`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `converged` | `boolean` | ✓ |  | converged parameter (bool). |
| `cpdag` | `string` | ✓ |  | cpdag parameter (pd.DataFrame). |
| `edge_confidence` | `string` | ✓ |  | edge_confidence parameter (pd.DataFrame). |
| `final_edges` | `array[string]` | ✓ |  | final_edges parameter (List[Tuple[str, str]]). |
| `iteration_log` | `array[string]` | ✓ |  | iteration_log parameter (List[Dict[str, Any]]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `provenance` | `object` |  | `None` | provenance parameter (Dict[str, Any]). |
> 📝 *provenance 参数（字典）。*
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

result = sp.LLMConstrainedDAGResult(final_edges=["a", "b"], edge_confidence="value", iteration_log=["a", "b"], skeleton="value", cpdag="value", variables=["a", "b"], n_obs=1.0, alpha=1.0, converged=True)
print(result.summary())
```

---
### `sp.LLMDAGProposal()`

**Result of an LLM (or heuristic) DAG proposal.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `backend` | `string` |  | `'heuristic'` | backend parameter (str). |
| `confidence` | `number` |  | `0.5` | confidence parameter (float). |
| `edges` | `array[string]` | ✓ |  | edges parameter (List[tuple]). |
| `rationale` | `array[string]` | ✓ |  | rationale parameter (List[str]). |
| `roles` | `object` | ✓ |  | roles parameter (dict). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.LLMDAGProposal(edges=["a", "b"], rationale=["a", "b"])
print(result.summary())
```

---
### `sp.SensitivityPriorProposal()`

**Suggested sensitivity parameter priors for sensemakr-style analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `backend` | `string` |  | `'heuristic'` | backend parameter (str). |
| `domain` | `string` | ✓ |  | domain parameter (str). |
| `r2` | `number` | ✓ |  | r2 parameter (float). |
| `rationale` | `string` | ✓ |  | rationale parameter (str). |
| `rho_max` | `number` | ✓ |  | rho_max parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SensitivityPriorProposal(rho_max=1.0, r2=1.0, rationale="value", domain="value")
print(result.summary())
```

---
### `sp.UnobservedConfounderProposal()`

**List of plausible unobserved confounders + suggested E-values.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `backend` | `string` |  | `'heuristic'` | backend parameter (str). |
| `candidates` | `array[string]` | ✓ |  | candidates parameter (List[str]). |
| `domain` | `string` | ✓ |  | domain parameter (str). |
| `suggested_evalue_thresholds` | `array[string]` | ✓ |  | suggested_evalue_thresholds parameter (List[float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.UnobservedConfounderProposal(candidates=["a", "b"], suggested_evalue_thresholds=["a", "b"], domain="value")
print(result.summary())
```

---
### `sp.anthropic_client()`

**Construct an Anthropic-compatible LLM client for use with sp.causal_llm.causal_mas. Requires the optional anthropic>=0.30 extra. Defaults to Claude Opus 4.7.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | `string` |  |  | api_key parameter (str). |
| `base_url` | `string` |  |  | base_url parameter (str). |
| `max_retries` | `integer` |  | `3` | max_retries parameter (int). |
| `max_tokens` | `integer` |  | `1024` | max_tokens parameter (int). |
| `model` | `string` |  | `'claude-opus-4-7'` | Model variant or parameterisation to fit. |
| `temperature` | `number` |  | `0.0` | temperature parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.anthropic_client()
print(result.summary())
```

> 📁 See also: `docs/guides/causal_mas.md`, `docs/guides/llm_dag_setup.md`

---
### `sp.causal_mas()`

**Multi-agent LLM causal discovery (arXiv:2509.00987, 2025). Runs proposer / critic / domain-expert / synthesiser agents over several rounds, returns per-edge confidence + audit log.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `client` | `string` |  |  | LLM chat client |
| `confounders` | `array[string]` |  |  | confounders parameter (list). |
| `domain` | `string` |  | `''` | domain parameter (str). |
| `final_threshold` | `number` |  | `0.5` | final_threshold parameter (float). |
| `instruments` | `array[string]` |  |  | instruments parameter (list). |
| `outcome` | `string` |  |  | Outcome variable column name or outcome array. |
| `rounds` | `integer` |  | `3` | rounds parameter (int). |
| `treatment` | `string` |  |  | Treatment indicator, treatment variable, or treatment array. |
| `variables` | `array[string]` | ✓ |  | variables parameter (list). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.causal_mas(variables=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/causal_mas.md`

---
### `sp.echo_client()`

**Deterministic scripted-response LLM client for testing sp.causal_llm.causal_mas without network access.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `response_fn` | `string` | ✓ |  | Maps (role, prompt) -> str |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.echo_client(response_fn="value")
print(result.summary())
```

---
### `sp.llm_dag_constrained()`

**Closed-loop LLM-assisted DAG discovery: iterate LLM-propose -> constrained PC -> CI-test validate -> demote, until edge set converges or max_iter is hit. Returns a final DAG with per-edge LLM confidence and CI-test p-value.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci_test` | `string (enum)` |  | `'fisherz'` | ci_test parameter (str). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `descriptions` | `object` |  |  | Variable -> human description |
| `forbid_low_conf` | `boolean` |  | `False` | forbid_low_conf parameter (bool). |
| `high_conf_threshold` | `number` |  | `0.7` | high_conf_threshold parameter (float). |
| `low_conf_threshold` | `number` |  | `0.3` | low_conf_threshold parameter (float). |
| `max_iter` | `integer` |  | `3` | Maximum number of optimisation iterations. |
| `oracle` | `string` |  |  | LLM oracle f(vars, desc)->[(a,b[,conf])] |
| `variables` | `array[string]` |  |  | Subset of columns to include |

> **ci_test** options: `'fisherz'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_dag_constrained(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/llm_dag_family.md`, `docs/guides/paper_pipeline.md`

---
### `sp.llm_dag_propose()`

**Propose a candidate DAG from variable names + domain description.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `client` | `string` |  |  | An LLM client implementing ``.complete(prompt: str) -> str``. If ``None``, use the deterministic heuristic backend. |
| `domain` | `string` |  | `''` | Free-text domain description (e.g. "labor economics, education and earnings"). Helps the LLM but ignored by the heuristic backend. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `variables` | `array[string]` | ✓ |  | Names of variables in the dataset. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_dag_propose(variables=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/agent_native_workflow.md`, `docs/guides/llm_dag_family.md`, `docs/guides/llm_dag_setup.md`

---
### `sp.llm_dag_validate()`

**Per-edge CI-test validation of a declared DAG. For each directed edge a->b, run partial-correlation independence test conditioning on parents(b)\{a}. Edges with p>alpha are flagged unsupported.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci_test` | `string (enum)` |  | `'fisherz'` | ci_test parameter (str). |
| `dag` | `string` | ✓ |  | dag parameter (DAG). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |

> **ci_test** options: `'fisherz'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_dag_validate(data=df, dag="value")
print(result.summary())
```

> 📁 See also: `docs/guides/llm_dag_family.md`

---
### `sp.llm_sensitivity_priors()`

**Propose sensitivity-analysis priors for the substantive setting.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `client` | `string` |  |  | LLM client with ``.complete(prompt: str) -> str``. |
| `domain` | `string (enum)` |  | `'health'` | domain parameter (str). |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

> **domain** options: `'health'`, `'education'`, `'labor'`, `'policy'`, `'marketing'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_sensitivity_priors(treatment="value", outcome="value")
print(result.summary())
```

---
### `sp.llm_unobserved_confounders()`

**Enumerate plausible unobserved confounders for a study.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `client` | `string` |  |  | LLM client with ``.complete(prompt: str) -> str``. |
| `domain` | `string (enum)` |  | `'health'` | domain parameter (str). |
| `outcome` | `string` | ✓ |  | Free-text descriptions (used by LLM, ignored by heuristic). |
| `point_estimate_rr` | `number` |  | `1.5` | Observed risk ratio; suggested E-values are scaled relative to this so the user can read "to nullify a RR of X you'd need an unobserved RR of Y". |
| `treatment` | `string` | ✓ |  | Free-text descriptions (used by LLM, ignored by heuristic). |

> **domain** options: `'health'`, `'education'`, `'labor'`, `'policy'`, `'marketing'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_unobserved_confounders(treatment="value", outcome="value")
print(result.summary())
```

---
### `sp.openai_client()`

**Construct an OpenAI-compatible LLM client for use with sp.causal_llm.causal_mas. Requires the optional openai>=1.0 extra. Supports custom base_url for Azure / vLLM / Ollama.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `api_key` | `string` |  |  | api_key parameter (str). |
| `base_url` | `string` |  |  | base_url parameter (str). |
| `max_retries` | `integer` |  | `3` | max_retries parameter (int). |
| `max_tokens` | `integer` |  | `1024` | max_tokens parameter (int). |
| `model` | `string` |  | `'gpt-4o-mini'` | Model variant or parameterisation to fit. |
| `organization` | `string` |  |  | organization parameter (str). |
| `temperature` | `number` |  | `0.0` | temperature parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.openai_client()
print(result.summary())
```

> 📁 See also: `docs/guides/causal_mas.md`

---
