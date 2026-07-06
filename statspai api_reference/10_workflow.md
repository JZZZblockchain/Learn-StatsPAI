# workflow

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

End-to-end causal-inference workflow orchestrator.

``sp.causal(df, y=, treatment=, ...)`` stitches the full analysis
pipeline into one call: diagnose identification -> recommend an
estimator -> fit it -> run the standard robustness suite -> produce
an HTML / Markdown / LaTeX report.

This module materialises the ``agent-native`` workflow as an API while
keeping each stage's statistical assumptions explicit.

**3 个公共函数**

### `sp.CausalWorkflow()`

**Holds state across the diagnose -> estimate -> report pipeline.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `allow_experimental` | `boolean` |  | `False` | allow_experimental parameter (bool). |
| `cate_summary_table` | `string` |  |  | cate_summary_table parameter (Optional[pd.DataFrame]). |
| `cluster` | `string` | ✓ |  | Cluster identifier column for clustered standard errors. |
| `cohort` | `string` | ✓ |  | Treatment cohort or group identifier. |
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. |
| `cutoff` | `number` | ✓ |  | cutoff parameter (Optional[float]). |
| `dag` | `string` | ✓ |  | dag parameter (Optional[Any]). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `degradations` | `array[string]` |  | `None` | degradations parameter (List[Dict[str, Any]]). |
| `design` | `string` | ✓ |  | design parameter (Optional[str]). |
| `diagnostics` | `string` |  |  | diagnostics parameter (Optional[Any]). |
| `estimator_comparison` | `string` |  |  | estimator_comparison parameter (Optional[pd.DataFrame]). |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. |
| `instrument` | `string` | ✓ |  | instrument parameter (Optional[str]). |
| `mediator` | `string` |  |  | mediator parameter (Optional[str]). |
| `pipeline_notes` | `array[string]` |  | `None` | pipeline_notes parameter (List[str]). |
| `post_treat_strata` | `string` |  |  | post_treat_strata parameter (Optional[str]). |
| `proxy_w` | `array[string]` |  |  | proxy_w parameter (Optional[List[str]]). |
| `proxy_z` | `array[string]` |  |  | proxy_z parameter (Optional[List[str]]). |
| `recommendation` | `string` |  |  | recommendation parameter (Optional[Any]). |
| `result` | `string` |  |  | result parameter (Optional[Any]). |
| `robustness_findings` | `object` |  | `None` | robustness_findings parameter (Dict[str, Any]). |
| `running_var` | `string` | ✓ |  | running_var parameter (Optional[str]). |
| `sensitivity_panel_result` | `string` |  |  | sensitivity_panel_result parameter (Optional[pd.DataFrame]). |
| `stages_completed` | `array[string]` |  | `None` | stages_completed parameter (List[str]). |
| `strict` | `boolean` | ✓ |  | strict parameter (bool). |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `tv_confounders` | `array[string]` |  |  | tv_confounders parameter (Optional[List[str]]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CausalWorkflow(y="outcome", data=df, treatment="value", covariates=["a", "b"], id="value", time="value", running_var="value", instrument="value", cutoff=1.0, cohort="value", cluster="value", design="value", dag="value", strict=True)
print(result.summary())
```

---
### `sp.PaperDraft()`

**Draft causal-analysis report assembled by :func:`sp.paper`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `citations` | `array[string]` |  | `None` | citations parameter (List[str]). |
| `dag` | `string` |  |  | dag parameter. |
| `dag_outcome` | `string` |  |  | dag_outcome parameter (Optional[str]). |
| `dag_treatment` | `string` |  |  | dag_treatment parameter (Optional[str]). |
| `degradations` | `array[string]` |  | `None` | degradations parameter (List[Dict[str, Any]]). |
| `fmt` | `string` | ✓ |  | fmt parameter (str). |
> 📝 *fmt 参数（字符串）。*
| `parsed_hints` | `object` |  | `None` | parsed_hints parameter (Dict[str, Any]). |
| `question` | `string` | ✓ |  | question parameter (str). |
| `sections` | `object` | ✓ |  | sections parameter (Dict[str, str]). |
| `workflow` | `string` | ✓ |  | workflow parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PaperDraft(question="value", workflow="value", fmt="value")
print(result.summary())
```

---
### `sp.paper()`

**End-to-end 'data + question -> publication draft' pipeline. Parses a natural-language question, runs sp.causal() (diagnose + recommend + estimate + robustness), and assembles a Markdown / LaTeX / Word draft with EDA, identification verdict, estimator rationale, results, and robustness sections.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cite` | `boolean` |  | `True` | cite parameter (bool). |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `cohort` | `string` |  |  | Treatment cohort or group identifier. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `cutoff` | `number` |  |  | cutoff parameter (float). |
| `dag` | `string` |  |  | dag parameter (DAG). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `design` | `string (enum)` |  |  | design parameter (str). |
| `fmt` | `string (enum)` |  | `'markdown'` | fmt parameter (str). |
| `id` | `string` |  |  | Unit, subject, or panel identifier column. |
| `include_eda` | `boolean` |  | `True` | Whether to include eda. |
| `include_robustness` | `boolean` |  | `True` | Whether to include robustness. |
| `instrument` | `string` |  |  | instrument parameter (str). |
| `output_path` | `string` |  |  | Filesystem path for output. |
| `question` | `string` | ✓ |  | Natural-language causal question |
| `running_var` | `string` |  |  | running_var parameter (str). |
| `strict` | `boolean` |  | `False` | strict parameter (bool). |
| `time` | `string` |  |  | Time period column. |
| `treatment` | `string` |  |  | Treatment indicator, treatment variable, or treatment array. |
| `y` | `string` |  |  | Outcome column (overrides parser) |

> **design** options: `'did'`, `'rd'`, `'iv'`, `'rct'`, `'observational'`, `'synth'`

> **fmt** options: `'markdown'`, `'tex'`, `'docx'`, `'qmd'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.paper(y="outcome", data=df, question="value")
print(result.summary())
```

> 📁 See also: `docs/guides/llm_dag_setup.md`, `docs/guides/methods_appendix.md`, `docs/guides/paper_pipeline.md`

---
