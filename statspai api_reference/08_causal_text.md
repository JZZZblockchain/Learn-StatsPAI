# causal_text

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Causal inference with text data — MVP (P1-B, v1.6 experimental).

Two methods to start the family:

* :func:`text_treatment_effect` — Veitch-Wang-Blei (2020) text-as-
  treatment via embedding adjustment.  Estimates the ATE of a
  user-supplied treatment indicator while controlling for the
  confounding variation captured in the text embedding.

* :func:`llm_annotator_correct` — Egami-Hinck-Stewart-Wei (2024)
  measurement-error correction for LLM-derived treatment labels.
  Given a small validation subset where both LLM and human labels
  exist, debias the downstream regression coefficient via Hausman-
  style correction.

Status
------
**Experimental.**  Both estimators ship with conservative defaults and
validation-set-estimated noise parameters; consume them as a starting
point, not a final answer.  Future versions will add text-as-confounder
(Roberts-Stewart-Nielsen) and text-as-outcome (Egami et al. 2018)
methods alongside topic-model integration.

References
----------
- Veitch, V., Sridhar, D., & Blei, D. M. (2019). "Adapting text embeddings
  for causal inference."  *UAI*.  arXiv:1905.12741.
- Egami, N., Hinck, M., Stewart, B., & Wei, H. (2024). "Using
  imperfect surrogates for downstream inference: Design-based
  supervised learning for social science applications of large
  language models."  *NeurIPS*.  arXiv:2306.04746.

**4 个公共函数**

### `sp.LLMAnnotatorResult()`

**Output of :func:`llm_annotator_correct`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `annotator_diagnostics` | `object` | ✓ |  | annotator_diagnostics parameter (Dict[str, Any]). |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `correction_factor` | `number` | ✓ |  | correction_factor parameter (float). |
| `detail` | `string` |  |  | Amount of result detail to return. |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `model_info` | `object` |  |  | model_info parameter (Optional[Dict[str, Any]]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `naive_estimate` | `number` | ✓ |  | naive_estimate parameter (float). |
| `naive_se` | `number` | ✓ |  | naive_se parameter (float). |
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

result = sp.LLMAnnotatorResult(method="value", estimand="value", estimate=1.0, se=1.0, pvalue=1.0, ci=["a", "b"], alpha=1.0, n_obs=1.0, naive_estimate=1.0, naive_se=1.0, correction_factor=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/causal_text_family.md`

---
### `sp.TextTreatmentResult()`

**ATE result for text-as-treatment estimation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. |
> 📝 *置信区间和检验的显著性水平。*
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). |
> 📝 *ci 参数（元组）。*
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). |
| `embedder_name` | `string` | ✓ |  | embedder_name parameter (str). |
| `embedding_dim` | `integer` | ✓ |  | embedding_dim parameter (int). |
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

result = sp.TextTreatmentResult(method="value", estimand="value", estimate=1.0, se=1.0, pvalue=1.0, ci=["a", "b"], alpha=1.0, n_obs=1.0, embedding_dim=1.0, embedder_name="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_text_family.md`

---
### `sp.llm_annotator_correct()`

**[experimental] Egami et al. (2024) measurement-error correction for downstream OLS coefficients when the treatment indicator was produced by an LLM (or any imperfect classifier). Binary T uses Hausman (1998) 1/(1 - p_01 - p_10) inflation; multi-class T (K>=3) uses the inverse-confusion-matrix transform built from the validation-set Bayes posterior. Optional bias-corrected bootstrap jointly resamples the validation set and the unlabeled corpus for honest CIs. SE inflation factor (delta-method) always reported in diagnostics. Validation status: experimental. Known limitations: method='hausman' is the only supported correction; the logistic and Bayesian variants from Egami et al. (2024) are not yet implemented.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `annotations_human` | `string` | ✓ |  | NaN where unavailable; >=30 valid rows |
| `annotations_llm` | `string` | ✓ |  | Binary or K-class numeric labels |
| `bootstrap` | `boolean` |  | `False` | Joint resample full sample (validation rows + unlabeled rows) for bias-corrected percentile CIs reflecting validation-set noise |
| `bootstrap_seed` | `integer` |  |  | NumPy default_rng seed |
| `covariates` | `string` |  |  | Covariate matrix, DataFrame, or column names. |
| `method` | `string (enum)` |  | `'hausman'` | Estimator or algorithm variant to use. |
| `n_bootstrap` | `integer` |  | `500` | Bootstrap replicates (>=50) |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **method** options: `'hausman'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.llm_annotator_correct(annotations_llm="value", outcome="value", annotations_human="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_text_family.md`

---
### `sp.text_treatment_effect()`

**[experimental] Veitch-Wang-Blei (2020) text-as-treatment ATE estimation. Embeds a text column into n_components features (default hash embedder, deterministic) and uses them as confounder adjustment in OLS with HC1 SEs. Validation status: experimental. Known limitations: embedder='sbert' requires the optional sentence-transformers extra; the bundled 'hash' embedder is a deterministic fallback, not a published parity reference; Veitch et al. (2020) full BERT/topic-model recipe is not yet implemented -- see module docstring.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `embedder` | `string (enum)` |  | `'hash'` | Text embedding backend or custom embedding callable. |
| `n_components` | `integer` |  | `20` | Number of generated components or embedding dimensions. |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `text_col` | `string` | ✓ |  | Text column used by causal-text estimators. |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

> **embedder** options: `'hash'`, `'sbert'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.text_treatment_effect(data=df, text_col="value", outcome="value", treatment="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_text_family.md`

---
