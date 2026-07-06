# transport

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Transportability (``sp.transport``): generalize causal effects across
populations. Combines Pearl-Bareinboim identification (selection
diagrams) with Dahabreh-Stuart-style density-ratio weighting.

Quick start
-----------
>>> import statspai as sp
>>> g = sp.dag("S -> X; X -> Y; S -> Y")
>>> sp.transport.identify_transport(g, treatment="X", outcome="Y",
...                                 selection_nodes={"S"})
>>> sp.transport.weights(source=rct, target=target_df,
...                      features=["age", "sex"],
...                      treatment="treat", outcome="y")

**7 个公共函数**

### `sp.HeterogeneityResult()`

**Container for Cochran's Q / Rucker's Q' heterogeneity diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `I2` | `number` | ✓ |  | I2 parameter (float). |
| `Q` | `number` | ✓ |  | Q parameter (float). |
| `Q_df` | `integer` | ✓ |  | Q_df parameter (int). |
| `Q_p` | `number` | ✓ |  | Q_p parameter (float). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.HeterogeneityResult(Q=1.0, Q_df=1.0, Q_p=1.0, I2=1.0, method="value")
print(result.summary())
```

---
### `sp.TransportIdentificationResult()`

**Result of a Pearl-Bareinboim transportability identification check.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `admissible_set` | `array[string]` | ✓ |  | admissible_set parameter (frozenset). |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `reason` | `string` | ✓ |  | reason parameter (str). |
| `transportable` | `boolean` | ✓ |  | transportable parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.TransportIdentificationResult(formula="lwage ~ x1 + x2", transportable=True, admissible_set=["a", "b"], reason="value")
print(result.summary())
```

---
### `sp.TransportWeightResult()`

**Result of density-ratio (inverse-odds-of-sampling) transport weighting.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `effect_source` | `number` | ✓ |  | effect_source parameter (float). |
| `effect_transported` | `number` | ✓ |  | effect_transported parameter (float). |
| `ess` | `number` | ✓ |  | ess parameter (float). |
| `max_weight` | `number` | ✓ |  | max_weight parameter (float). |
| `se_transported` | `number` | ✓ |  | se_transported parameter (float). |
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.TransportWeightResult(weights="value", ess=1.0, max_weight=1.0, effect_source=1.0, effect_transported=1.0, se_transported=1.0)
print(result.summary())
```

---
### `sp.heterogeneity_of_effect()`

**DerSimonian-Laird tau2 / Q / I2 heterogeneity statistics for multi-study evidence synthesis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `estimates` | `array[string]` | ✓ |  | estimates parameter (list). |
| `ses` | `array[string]` | ✓ |  | ses parameter (list). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.heterogeneity_of_effect(estimates=["a", "b"], ses=["a", "b"])
print(result.summary())
```

---
### `sp.identify_transport()`

**Pearl-Bareinboim transportability: enumerate s-admissible adjustment sets on a selection diagram; returns the transport formula or NOT identifiable.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `dag` | `string` | ✓ |  | dag parameter (DAG). |
| `outcome` | `array[string]` | ✓ |  | Outcome variable column name or outcome array. |
| `selection_nodes` | `array[string]` | ✓ |  | selection_nodes parameter (set). |
| `treatment` | `array[string]` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.identify_transport(dag="value", treatment=["a", "b"], outcome=["a", "b"], selection_nodes=["a", "b"])
print(result.summary())
```

---
### `sp.rwd_rct_concordance()`

**Report-card: does the RWD estimate fall inside the RCT's 95% CI?**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `rct_estimate` | `number` | ✓ |  | rct_estimate parameter (float). |
| `rct_se` | `number` | ✓ |  | rct_se parameter (float). |
| `rwd_estimate` | `number` | ✓ |  | rwd_estimate parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rwd_rct_concordance(rct_estimate=1.0, rct_se=1.0, rwd_estimate=1.0)
print(result.summary())
```

---
### `sp.synthesise_evidence()`

**Inverse-variance pooling of an RCT and RWD estimate with optional transport shift (Dahabreh et al. 2020; arXiv:2511.19735 2025).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `rct_estimate` | `number` | ✓ |  | rct_estimate parameter (float). |
| `rct_se` | `number` | ✓ |  | rct_se parameter (float). |
| `rwd_estimate` | `number` | ✓ |  | rwd_estimate parameter (float). |
| `rwd_se` | `number` | ✓ |  | rwd_se parameter (float). |
| `transport_shift` | `number` |  | `0.0` | transport_shift parameter (float). |
| `transport_shift_se` | `number` |  | `0.0` | transport_shift_se parameter (float). |
| `weight_mode` | `string (enum)` |  | `'inverse_variance'` | weight_mode parameter (str). |

> **weight_mode** options: `'inverse_variance'`, `'rct_heavy'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.synthesise_evidence(rct_estimate=1.0, rct_se=1.0, rwd_estimate=1.0, rwd_se=1.0)
print(result.summary())
```

---
