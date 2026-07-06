# question

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

Estimand-first causal question DSL (``sp.causal_question``).

The article emphasizes "causal question precedes statistical model" as
the common foundation of all three causal-inference schools:
econometrics' *identification*, epidemiology's *target trial protocol*,
and ML's *estimand-aware learning*.

This module lets a user declare a causal question in one place, then
automatically:

  1. Identify the appropriate research design (IV / DiD / RD / backdoor).
  2. Suggest the right StatsPAI estimator.
  3. Run the analysis and attach diagnostics + sensitivity.
  4. Produce a reproducible Methods paragraph.

>>> import statspai as sp
>>> q = sp.causal_question(
...     treatment="minimum_wage_hike",
...     outcome="employment",
...     estimand="ATT",
...     design="policy_shock",
...     data=df,
...     time_structure="panel",
...     covariates=["industry", "skill"],
... )
>>> q.identify()
>>> r = q.estimate()
>>> q.report()

**6 个公共函数**

### `sp.CausalQuestion()`

**Pre-registered causal question declaration.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `_plan` | `string` |  |  | _plan parameter (Optional[IdentificationPlan]). |
| `_result` | `string` |  |  | _result parameter (Optional[EstimationResult]). |
| `cohort` | `string` |  |  | Treatment cohort or group identifier. |
| `covariates` | `array[string]` |  | `None` | Covariate matrix, DataFrame, or column names. |
| `cutoff` | `number` |  |  | cutoff parameter (Optional[float]). |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `design` | `string` |  | `'auto'` | design parameter (str). |
| `engine` | `string` |  | `'ols'` | engine parameter (str). |
| `estimand` | `string` |  | `'ATE'` | estimand parameter (str). |
| `id` | `string` |  |  | Unit, subject, or panel identifier column. |
| `instruments` | `array[string]` |  | `None` | instruments parameter (List[str]). |
| `notes` | `string` |  | `''` | notes parameter (str). |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `population` | `string` |  | `''` | population parameter (str). |
| `running_variable` | `string` |  |  | running_variable parameter (Optional[str]). |
| `time` | `string` |  |  | Time period column. |
| `time_structure` | `string` |  | `'cross_section'` | time_structure parameter (str). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CausalQuestion(data=df, treatment="value", outcome="value")
print(result.summary())
```

---
### `sp.EstimationResult()`

**Unified view of a causal-question estimate.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple[float, float]). |
> 📝 *ci 参数（浮点数二元组）。*
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `estimator` | `string` | ✓ |  | estimator parameter (str). |
| `n` | `integer` | ✓ |  | n parameter (int). |
| `plan` | `string` | ✓ |  | plan parameter (IdentificationPlan). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `underlying` | `string` | ✓ |  | underlying parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.EstimationResult(estimand="value", estimator="value", estimate=1.0, se=1.0, ci=["a", "b"], n=1.0, underlying="value", plan="value")
print(result.summary())
```

---
### `sp.IdentificationPlan()`

**Output of :meth:`CausalQuestion.identify`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assumptions` | `array[string]` | ✓ |  | assumptions parameter (List[str]). |
| `estimand` | `string` | ✓ |  | estimand parameter (str). |
| `estimator` | `string` | ✓ |  | estimator parameter (str). |
| `fallback_estimators` | `array[string]` |  | `None` | fallback_estimators parameter (List[str]). |
| `identification_story` | `string` | ✓ |  | identification_story parameter (str). |
| `warnings` | `array[string]` |  | `None` | warnings parameter (List[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.IdentificationPlan(estimator="value", estimand="value", identification_story="value", assumptions=["a", "b"])
print(result.summary())
```

---
### `sp.causal_question()`

**Declare a causal question up front (estimand-first). .identify() picks an estimator and lists identifying assumptions; .estimate() runs the analysis; .report() produces a Markdown Methods + Results paragraph. Auto-routes to IV / RD / DiD / longitudinal / selection-on-observables based on supplied fields.**
> 📝 *事先声明因果问题（以估计目标为先）。.identify() 选择估计器并列出识别假设；.estimate() 运行分析；.report() 生成 Markdown 方法+结果段落。根据提供的字段自动路由到 IV / RD（断点回归）/ DiD / 纵向 / 基于可观测变量的选择方案。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `cutoff` | `number` |  |  | cutoff parameter (float). |
| `data` | `string` |  |  | pandas DataFrame containing the variables used by the estimator. |
| `design` | `string (enum)` |  | `'auto'` | design parameter (str). |
| `estimand` | `string (enum)` |  | `'ATE'` | estimand parameter (str). |
| `id` | `string` |  |  | Unit, subject, or panel identifier column. |
| `instruments` | `array[string]` |  |  | instruments parameter (list[str]). |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `population` | `string` |  |  | population parameter (str). |
| `running_variable` | `string` |  |  | running_variable parameter (str). |
| `time` | `string` |  |  | Time period column. |
| `time_structure` | `string (enum)` |  | `'cross_section'` | time_structure parameter (str). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |

> **design** options: `'auto'`, `'rct'`, `'selection_on_observables'`, `'iv'`, `'natural_experiment'`, `'policy_shock'`, `'regression_discontinuity'`, `'synthetic_control'`, `'did'`, `'event_study'`, `'longitudinal_observational'`

> **estimand** options: `'ATE'`, `'ATT'`, `'ATU'`, `'LATE'`, `'CATE'`, `'ITT'`

> **time_structure** options: `'cross_section'`, `'panel'`, `'repeated_cross_section'`, `'longitudinal'`, `'time_series'`, `'pre_post'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.causal_question(data=df, treatment="value", outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_ml_causal_estimator.md`, `docs/guides/replication_workflow.md`

---
### `sp.load_preregister()`

**Load a pre-registration file back into a CausalQuestion.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filename` | `string` | ✓ |  | filename parameter (str \| Path). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.load_preregister(filename="value")
print(result.summary())
```

---
### `sp.preregister()`

**Write a pre-analysis plan (CausalQuestion) to YAML / JSON for OSF, AEA RCT Registry, or a repo-local PAP. Includes a metadata block with timestamp and statspai version.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filename` | `string` | ✓ |  | filename parameter (str \| Path). |
| `fmt` | `string (enum)` |  | `'auto'` | fmt parameter (str). |
| `note` | `string` |  |  | note parameter (str). |
| `question` | `object` | ✓ |  | question parameter (CausalQuestion \| dict). |
| `registry_url` | `string` |  |  | registry_url parameter (str). |

> **fmt** options: `'auto'`, `'yaml'`, `'json'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.preregister(filename="value")
print(result.summary())
```

---
