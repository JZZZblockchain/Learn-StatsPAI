# fairness

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Counterfactual fairness & algorithmic-bias diagnostics (``sp.fairness``).

Treats fairness as a causal-inference problem rather than a pure
statistics one: an algorithm is counterfactually fair if the prediction
would be the same had the protected attribute been different, holding
the non-protected causal ancestors fixed.

Core tools
----------
- :func:`counterfactual_fairness` — Kusner, Loftus, Russell, Silva (2018)
  Level-2/3 predictor evaluation on a user-supplied SCM.
- :func:`orthogonal_to_bias` — Chen & Zhu (arXiv:2403.17852v3, 2024)
  Data pre-processing that removes the part of non-protected features
  correlated with the protected attribute, via residualization.
- :func:`demographic_parity` — P(Y_hat=1 | A=a) — A.
- :func:`equalized_odds` — P(Y_hat=1 | Y=y, A=a) — A.
- :func:`fairness_audit` — one-shot dashboard combining the metrics above.

References
----------
Kusner, M. J., Loftus, J., Russell, C., & Silva, R. (2018).
Counterfactual fairness. NeurIPS.

Hardt, M., Price, E., & Srebro, N. (2016).
Equality of opportunity in supervised learning. NeurIPS.

Chen, S., & Zhu, S. (2024).
Counterfactual Fairness Through Orthogonal to Bias. arXiv:2403.17852v3.

**6 个公共函数**

### `sp.counterfactual_fairness()`

**Kusner-Loftus-Russell-Silva (2018) counterfactual-fairness test: compares factual vs. SCM-intervened predictions to measure path-specific dependence of a classifier on the protected attribute.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `predictor` | `string` | ✓ |  | Callable(DataFrame) -> predictions |
| `protected` | `string` | ✓ |  | protected parameter (str). |
| `scm_intervention` | `string` | ✓ |  | scm_intervention parameter (callable). |
| `threshold` | `number` |  | `0.05` | threshold parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.counterfactual_fairness(data=df, predictor="value", protected="value", scm_intervention="value")
print(result.summary())
```

---
### `sp.demographic_parity()`

**Demographic-parity gap between groups defined by the protected attribute.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `predictions` | `string` | ✓ |  | predictions parameter (str). |
| `protected` | `string` | ✓ |  | protected parameter (str). |
| `threshold` | `number` |  | `0.1` | threshold parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.demographic_parity(data=df, predictions="value", protected="value")
print(result.summary())
```

---
### `sp.equalized_odds()`

**Hardt-Price-Srebro equalized-odds gap -- max of TPR and FPR group differences.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `labels` | `string` | ✓ |  | labels parameter (str). |
| `predictions` | `string` | ✓ |  | predictions parameter (str). |
| `protected` | `string` | ✓ |  | protected parameter (str). |
| `threshold` | `number` |  | `0.1` | threshold parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.equalized_odds(data=df, predictions="value", labels="value", protected="value")
print(result.summary())
```

---
### `sp.evidence_without_injustice()`

**Kwak-Pleasants (2025) evidence-without-injustice counterfactual fairness test. Freezes admissible-evidence features at their factual values and tests whether predictions still change under do(A=a').**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `admissible_features` | `array[string]` | ✓ |  | admissible_features parameter (list). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `alternative_values` | `array[string]` |  |  | alternative_values parameter (list). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. |
| `predictor` | `string` | ✓ |  | predictor parameter (callable). |
| `protected` | `string` | ✓ |  | protected parameter (str). |
| `scm_intervention` | `string` | ✓ |  | scm_intervention parameter (callable). |
| `threshold` | `number` |  | `0.05` | threshold parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.evidence_without_injustice(data=df, predictor="value", protected="value", admissible_features=["a", "b"], scm_intervention="value")
print(result.summary())
```

---
### `sp.fairness_audit()`

**One-shot dashboard combining demographic parity, equalized odds, and (optionally) counterfactual fairness.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `labels` | `string` |  |  | labels parameter (str). |
| `predictions` | `string` | ✓ |  | predictions parameter (str). |
| `predictor` | `string` |  |  | predictor parameter (callable). |
| `protected` | `string` | ✓ |  | protected parameter (str). |
| `scm_intervention` | `string` |  |  | scm_intervention parameter (callable). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.fairness_audit(data=df, predictions="value", protected="value")
print(result.summary())
```

---
### `sp.orthogonal_to_bias()`

**Residualize features against the protected attribute as a pre-processing step toward counterfactual fairness.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `features` | `array[string]` | ✓ |  | Feature matrix or feature column names. |
| `protected` | `string` | ✓ |  | protected parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.orthogonal_to_bias(data=df, features=["a", "b"], protected="value")
print(result.summary())
```

---
