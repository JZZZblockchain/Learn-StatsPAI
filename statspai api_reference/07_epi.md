# epi

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Epidemiology domain primitives (``sp.epi``).

Fills the gap the article calls out — statspai already has the heavy
epidemiological causal machinery (IPW, G-formula, MSM, target trial),
but lacked the entry-level statistical primitives that clinicians,
epidemiologists, and public-health researchers reach for first.

Modelled after R's ``epiR``, ``epitools``, and ``fmsb``.

>>> import statspai as sp
>>> sp.epi.odds_ratio(50, 20, 30, 40)
>>> sp.epi.relative_risk(50, 950, 10, 990)
>>> sp.epi.mantel_haenszel(tables_2x2xK)
>>> sp.epi.direct_standardize(events, pop, standard_weights)
>>> sp.epi.bradford_hill(strength=1.0, temporality=1.0, consistency=0.5, ...)

**20 个公共函数**

### `sp.DiagnosticTestResult()`

**Container for binary diagnostic-test performance metrics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `fn` | `integer` | ✓ |  | fn parameter (int). |
| `fp` | `integer` | ✓ |  | fp parameter (int). |
| `lr_neg` | `number` | ✓ |  | lr_neg parameter (float). |
| `lr_pos` | `number` | ✓ |  | lr_pos parameter (float). |
| `npv` | `number` | ✓ |  | npv parameter (float). |
| `ppv` | `number` | ✓ |  | ppv parameter (float). |
| `prevalence` | `number` | ✓ |  | prevalence parameter (float). |
| `sensitivity` | `number` | ✓ |  | sensitivity parameter (float). |
| `sensitivity_ci` | `array[string]` | ✓ |  | sensitivity_ci parameter (tuple[float, float]). |
| `specificity` | `number` | ✓ |  | specificity parameter (float). |
| `specificity_ci` | `array[string]` | ✓ |  | specificity_ci parameter (tuple[float, float]). |
| `tn` | `integer` | ✓ |  | tn parameter (int). |
| `tp` | `integer` | ✓ |  | tp parameter (int). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DiagnosticTestResult(sensitivity=1.0, sensitivity_ci=["a", "b"], specificity=1.0, specificity_ci=["a", "b"], ppv=1.0, npv=1.0, lr_pos=1.0, lr_neg=1.0, prevalence=1.0, tp=1.0, fp=1.0, fn=1.0, tn=1.0)
print(result.summary())
```

---
### `sp.KappaResult()`

**Container for Cohen's kappa inter-rater agreement.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple[float, float]). |
> 📝 *ci 参数（浮点数二元组）。*
| `expected_agreement` | `number` | ✓ |  | expected_agreement parameter (float). |
| `kappa` | `number` | ✓ |  | kappa parameter (float). |
| `n_categories` | `integer` | ✓ |  | Number of categories. |
| `observed_agreement` | `number` | ✓ |  | observed_agreement parameter (float). |
| `p_value` | `number` | ✓ |  | p_value parameter (float). |
> 📝 *p_value 参数（浮点数）。*
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*
| `z` | `number` | ✓ |  | Instrument, proxy, or auxiliary variable used by this estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.KappaResult(kappa=1.0, se=1.0, ci=["a", "b"], observed_agreement=1.0, expected_agreement=1.0, n_categories=1.0, weights="value", z=1.0, p_value=1.0)
print(result.summary())
```

---
### `sp.ROCResult()`

**Container for ROC-curve coordinates and AUC inference.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `auc` | `number` | ✓ |  | auc parameter (float). |
| `auc_ci` | `array[string]` | ✓ |  | auc_ci parameter (tuple[float, float]). |
| `auc_se` | `number` | ✓ |  | auc_se parameter (float). |
| `fpr` | `string` | ✓ |  | fpr parameter (np.ndarray). |
| `thresholds` | `string` | ✓ |  | thresholds parameter (np.ndarray). |
| `tpr` | `string` | ✓ |  | tpr parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ROCResult(thresholds="value", tpr="value", fpr="value", auc=1.0, auc_se=1.0, auc_ci=["a", "b"])
print(result.summary())
```

---
### `sp.attributable_risk()`

**Attributable fractions in the exposed (AF) and in the population (Levin PAF) with delta-method CI. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `a` | `number` | ✓ |  | a parameter (float \| 2x2 array). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `b` | `number` |  |  | b parameter (float). |
| `c` | `number` |  |  | c parameter (float). |
| `d` | `number` |  |  | d parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.attributable_risk(a=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.auc()`

**Shortcut: just return the AUC. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `scores` | `string` | ✓ |  | scores parameter. |
| `y_true` | `string` | ✓ |  | y_true parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.auc(y_true="value", scores="value")
print(result.summary())
```

---
### `sp.bradford_hill()`

**Structured 9-viewpoint Bradford-Hill causal-assessment rubric with prerequisite check (temporality required) and narrative verdict.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `analogy` | `number` |  |  | analogy parameter (float). |
| `biological_gradient` | `number` |  |  | biological_gradient parameter (float). |
| `coherence` | `number` |  |  | coherence parameter (float). |
| `consistency` | `number` |  |  | consistency parameter (float). |
| `evidence` | `object` |  |  | Optional dict mapping viewpoint -> [0,1] score |
| `experiment` | `number` |  |  | experiment parameter (float). |
| `notes` | `object` |  |  | notes parameter (dict). |
| `plausibility` | `number` |  |  | plausibility parameter (float). |
| `specificity` | `number` |  |  | specificity parameter (float). |
| `strength` | `number` |  |  | strength parameter (float). |
| `temporality` | `number` |  |  | temporality parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bradford_hill()
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.breslow_day_test()`

**Breslow-Day test for homogeneity of the odds ratio across strata, with Tarone correction.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tables` | `string` | ✓ |  | tables parameter (array (K, 2, 2)). |
| `tarone_correction` | `boolean` |  | `True` | tarone_correction parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.breslow_day_test(tables="value")
print(result.summary())
```

---
### `sp.cohen_kappa()`

**Cohen's kappa for inter-rater agreement on nominal or ordinal scales. Supports linear / quadratic weighting. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `rater_a` | `string` | ✓ |  | rater_a parameter (array). |
| `rater_b` | `string` | ✓ |  | rater_b parameter (array). |
| `weights` | `string (enum)` |  | `'unweighted'` | Observation weights. |

> **weights** options: `'unweighted'`, `'linear'`, `'quadratic'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cohen_kappa(rater_a="value", rater_b="value")
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.diagnostic_test()`

**Alias for :func:`sensitivity_specificity`.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.diagnostic_test()
print(result.summary())
```

---
### `sp.direct_standardize()`

**Direct age/covariate standardization of a rate using external standard-population weights. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `events` | `array[string]` | ✓ |  | events parameter (list \| ndarray). |
| `population` | `array[string]` | ✓ |  | population parameter (list \| ndarray). |
| `standard_weights` | `array[string]` | ✓ |  | standard_weights parameter (list \| ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.direct_standardize(events=["a", "b"], population=["a", "b"], standard_weights=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`, `docs/guides/public_health.md`

---
### `sp.incidence_rate_ratio()`

**Person-time incidence rate ratio with exact Poisson CI (Clopper-Pearson on conditional binomial). Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `events_exposed` | `number` | ✓ |  | events_exposed parameter (float). |
| `events_unexposed` | `number` | ✓ |  | events_unexposed parameter (float). |
| `method` | `string (enum)` |  | `'exact'` | Estimator or algorithm variant to use. |
| `pt_exposed` | `number` | ✓ |  | Person-time at risk (exposed) |
| `pt_unexposed` | `number` | ✓ |  | pt_unexposed parameter (float). |

> **method** options: `'exact'`, `'wald'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.incidence_rate_ratio(events_exposed=1.0, pt_exposed=1.0, events_unexposed=1.0, pt_unexposed=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.indirect_standardize()`

**Indirect standardization -> SMR (standardized morbidity / mortality ratio) with Garwood exact Poisson CI. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `events_reference` | `array[string]` | ✓ |  | events_reference parameter (list \| ndarray). |
| `observed` | `number` | ✓ |  | observed parameter (float). |
| `population_reference` | `array[string]` | ✓ |  | population_reference parameter (list \| ndarray). |
| `population_study` | `array[string]` | ✓ |  | population_study parameter (list \| ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.indirect_standardize(observed=1.0, events_reference=["a", "b"], population_reference=["a", "b"], population_study=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.mantel_haenszel()`

**Mantel-Haenszel pooled OR or RR across K strata, with Robins-Breslow-Greenland variance and Cochran's Q homogeneity check. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `measure` | `string (enum)` |  | `'OR'` | measure parameter (str). |
| `tables` | `string` | ✓ |  | Stack of K per-stratum 2x2 tables |

> **measure** options: `'OR'`, `'RR'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mantel_haenszel(tables="value")
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`, `docs/guides/public_health.md`

---
### `sp.number_needed_to_treat()`

**Number needed to treat (or harm), defined as |1 / RD|. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `a` | `string` | ✓ |  | a parameter. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `b` | `number` |  |  | b parameter (Optional[float]). |
| `c` | `number` |  |  | c parameter (Optional[float]). |
| `d` | `number` |  |  | d parameter (Optional[float]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.number_needed_to_treat(a="value")
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.odds_ratio()`

**Odds ratio from a 2x2 table with Woolf (asymptotic) or Fisher-exact CI. Haldane-Anscombe correction for zero cells. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `a` | `number` | ✓ |  | a (exposed, outcome+) count or 2x2 array |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `b` | `number` |  |  | b (exposed, outcome-) count |
| `c` | `number` |  |  | c (unexposed, outcome+) count |
| `d` | `number` |  |  | d (unexposed, outcome-) count |
| `method` | `string (enum)` |  | `'woolf'` | CI method |

> **method** options: `'woolf'`, `'exact'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.odds_ratio(a=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`, `docs/guides/public_health.md`

---
### `sp.prevalence_ratio()`

**Prevalence ratio (cross-sectional RR); mathematically identical Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.prevalence_ratio()
print(result.summary())
```

---
### `sp.relative_risk()`

**Relative risk (risk ratio) from a 2x2 table with Katz log-RR CI. Haldane correction for zero cells. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `a` | `number` | ✓ |  | a parameter (float \| 2x2 array). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `b` | `number` |  |  | b parameter (float). |
| `c` | `number` |  |  | c parameter (float). |
| `d` | `number` |  |  | d parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.relative_risk(a=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`, `docs/guides/public_health.md`

---
### `sp.risk_difference()`

**Risk difference (absolute risk reduction) with Wald or Newcombe hybrid-score CI. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `a` | `number` | ✓ |  | a parameter (float \| 2x2 array). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `b` | `number` |  |  | b parameter (float). |
| `c` | `number` |  |  | c parameter (float). |
| `d` | `number` |  |  | d parameter (float). |
| `method` | `string (enum)` |  | `'wald'` | Estimator or algorithm variant to use. |

> **method** options: `'wald'`, `'newcombe'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.risk_difference(a=1.0)
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.roc_curve()`

**ROC curve with AUC (trapezoidal) and Hanley-McNeil (1982) standard error. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `scores` | `string` | ✓ |  | scores parameter (array). |
| `y_true` | `string` | ✓ |  | y_true parameter (array). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.roc_curve(y_true="value", scores="value")
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
### `sp.sensitivity_specificity()`

**Sensitivity, specificity, PPV, NPV, LR+ / LR- with Wilson score CIs. Accepts either raw binary labels or pre-computed confusion counts. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `fn` | `integer` |  |  | fn parameter (int). |
| `fp` | `integer` |  |  | fp parameter (int). |
| `tn` | `integer` |  |  | tn parameter (int). |
| `tp` | `integer` |  |  | tp parameter (int). |
| `y_pred` | `string` |  |  | y_pred parameter (array). |
| `y_true` | `string` |  |  | y_true parameter (array). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sensitivity_specificity()
print(result.summary())
```

> 📁 See also: `docs/guides/epi_measures.md`

---
