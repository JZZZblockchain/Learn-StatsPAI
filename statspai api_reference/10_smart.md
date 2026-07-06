# smart

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

Smart Workflow Engine.

Registered workflow helpers for planning, diagnostics, sensitivity, and
replication support:

- recommend()           — DAG + data → estimator selection
- compare_estimators()  — run multiple methods, compare, diagnose
- assumption_audit()    — comprehensive assumption testing by method
- sensitivity_dashboard() — multi-dimensional sensitivity analysis
- pub_ready()           — journal-specific publication readiness checklist
- replicate()           — famous paper replication with built-in data

**27 个公共函数**

### `sp.AssumptionResult()`

**Results from comprehensive assumption audit.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `checks` | `array[string]` | ✓ |  | checks parameter (List[statspai.smart.assumptions.AssumptionCheck]). |
| `critical_failures` | `array[string]` | ✓ |  | critical_failures parameter (List[str]). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_fail` | `integer` | ✓ |  | Number of fail. |
| `n_inconclusive` | `integer` | ✓ |  | Number of inconclusive. |
| `n_pass` | `integer` | ✓ |  | Number of pass. |
| `overall_grade` | `string` | ✓ |  | overall_grade parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.AssumptionResult(method="value", checks=["a", "b"], overall_grade="value", n_pass=1.0, n_fail=1.0, n_inconclusive=1.0, critical_failures=["a", "b"])
print(result.summary())
```

---
### `sp.ComparisonResult()`

**Results from multi-estimator comparison.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `agreement` | `object` | ✓ |  | agreement parameter (Dict[str, float]). |
| `estimates_table` | `string` | ✓ |  | estimates_table parameter (pd.DataFrame). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `results` | `object` | ✓ |  | results parameter (Dict[str, Any]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ComparisonResult(estimates_table="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.DiagnosticFinding()`

**A single design-level finding.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `category` | `string` | ✓ |  | category parameter (str). |
| `evidence` | `object` |  | `None` | evidence parameter (Dict[str, Any]). |
| `message` | `string` | ✓ |  | message parameter (str). |
| `severity` | `string` | ✓ |  | severity parameter (str). |
| `suggestion` | `string` |  |  | suggestion parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DiagnosticFinding(severity="value", category="value", message="value")
print(result.summary())
```

---
### `sp.IdentificationError()`

**Raised by ``check_identification(strict=True)`` when a blocker is found.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `report` | `string` | ✓ |  | report parameter ('IdentificationReport'). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.IdentificationError(report="value")
print(result.summary())
```

---
### `sp.IdentificationReport()`

**Report from ``check_identification``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `design` | `string` |  | `''` | design parameter (str). |
| `findings` | `array[string]` |  | `None` | findings parameter (List[DiagnosticFinding]). |
| `n_obs` | `integer` |  | `0` | Number of obs. |
| `n_units` | `integer` |  |  | Number of units. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.IdentificationReport()
print(result.summary())
```

---
### `sp.IntakeResult()`

**Structured routing outcome before estimator selection.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assumptions` | `array[string]` |  | `None` | assumptions parameter (List[str]). |
| `candidate_designs` | `array[string]` |  | `None` | candidate_designs parameter (List[str]). |
| `deciding_question` | `string` |  |  | deciding_question parameter (Optional[str]). |
| `next_step` | `string` |  | `''` | next_step parameter (str). |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. |
| `recommended_design` | `string` |  |  | recommended_design parameter (Optional[str]). |
| `required_data` | `array[string]` |  | `None` | required_data parameter (List[str]). |
| `risks` | `array[string]` |  | `None` | risks parameter (List[str]). |
| `why` | `string` |  | `''` | why parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.IntakeResult(outcome="value")
print(result.summary())
```

---
### `sp.PubReadyResult()`

**Publication readiness checklist results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `checks` | `array[string]` | ✓ |  | checks parameter (List[Dict[str, Any]]). |
| `missing` | `array[string]` | ✓ |  | missing parameter (List[str]). |
| `present` | `array[string]` | ✓ |  | present parameter (List[str]). |
| `score` | `integer` | ✓ |  | score parameter (int). |
| `venue` | `string` | ✓ |  | venue parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PubReadyResult(venue="value", checks=["a", "b"], score=1.0, missing=["a", "b"], present=["a", "b"])
print(result.summary())
```

---
### `sp.RecommendationResult()`

**Result from the estimator recommendation engine.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `data_profile` | `object` | ✓ |  | data_profile parameter (Dict[str, Any]). |
| `design` | `string` | ✓ |  | design parameter (str). |
| `recommendations` | `array[string]` | ✓ |  | recommendations parameter (List[Dict[str, Any]]). |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. |
| `warnings` | `array[string]` | ✓ |  | warnings parameter (List[str]). |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RecommendationResult(y="outcome", data=df, recommendations=["a", "b"], design="value", warnings=["a", "b"], treatment="value")
print(result.summary())
```

---
### `sp.SensitivityDashboard()`

**Multi-dimensional sensitivity analysis results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `baseline` | `object` | ✓ |  | baseline parameter (Dict[str, Any]). |
| `dimensions` | `array[string]` | ✓ |  | dimensions parameter (List[Dict[str, Any]]). |
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `overall_stability` | `string` | ✓ |  | overall_stability parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SensitivityDashboard(dimensions=["a", "b"], overall_stability="value", method="value")
print(result.summary())
```

---
### `sp.assumption_audit()`

**Comprehensive assumption audit for any estimated model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for tests. |
| `data` | `string` |  |  | Original data (needed for some tests). Auto-extracted if available. |
| `result` | `string` | ✓ |  | Estimated model result. |
| `verbose` | `boolean` |  | `True` | Print summary automatically. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.assumption_audit(data=df, result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`

---
### `sp.audit()`

**Reviewer-checklist audit of a fitted StatsPAI result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | Any fitted StatsPAI result with ``model_info`` attached. |
| `treatment` | `string` |  |  | Name of the treatment variable when ``result`` is a plain regression used for causal adjustment on a selection-on-observables design. When supplied, the audit additionally asks for overlap / common-support, post-adjustment balance, and omitted-variable sensitivity -- the checks a referee demands on an observational design but that a bare OLS would otherwise escape. Has no effect on designs whose family already carries these checks (matching / DML / IV / ...). Descriptive regressions (no treatment declared) are never flagged. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.audit(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`, `docs/guides/diagnostics.md`, `docs/guides/paper_pipeline.md`

---
### `sp.bib_for()`

**Top-level structured citation for a fitted result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | Any fitted result object exposing a ``.cite()`` method. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bib_for(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`

---
### `sp.bibtex()`

**Resolve verified BibTeX entries from ``paper.bib`` by citation key.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keys` | `array[string]` | ✓ |  | One or more BibTeX keys, e.g. ``"chernozhukov2016hdm"`` or ``["callaway2021difference", "rambachan2023more"]``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.bibtex(keys=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/agent_native_workflow.md`

---
### `sp.brief()`

**Render a one-line status summary of a fitted result.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | exposing ``method`` / ``estimate`` / ``se`` / ``pvalue`` / ``ci`` / ``n_obs`` attributes). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.brief(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`

---
### `sp.check_identification()`

**Run design-level identification diagnostics before fitting an estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Clustering column for inference. |
| `cohort` | `string` |  |  | First-treatment-period column (for staggered DID). |
| `covariates` | `array[string]` |  |  | Candidate control variables. |
| `cutoff` | `number` |  |  | RD cutoff value. |
| `dag` | `string` |  |  | Causal DAG. If supplied, runs Cinelli-Forney-Pearl (2022) bad-control detection (mediator, descendant, collider, M-bias) and verifies the covariate set satisfies a valid adjustment criterion. Upgrades correlation heuristic to a principled check. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `design` | `string` |  |  | Override auto-detected design: one of 'rct', 'did', 'rd', 'iv', 'observational', 'panel'. |
| `id` | `string` |  |  | Panel identifiers. |
| `instrument` | `string` |  |  | IV instrument. |
| `running_var` | `string` |  |  | RD running variable. |
| `strict` | `boolean` |  | `False` | If True, raise :class:`IdentificationError` when the report's verdict is ``'BLOCKERS'``. Use in CI / automated pipelines where you want a hard failure when the design is broken. The exception carries ``.report`` for post-mortem inspection. |
| `time` | `string` |  |  | Panel identifiers. |
| `treatment` | `string` |  |  | Binary or continuous treatment column. |
| `y` | `string` | ✓ |  | Outcome column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.check_identification(y="outcome", data=df)
print(result.summary())
```

---
### `sp.compare_estimators()`

**Run multiple estimators on the same data and compare.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `id` | `string` |  |  | Panel unit ID. |
| `instrument` | `string` |  |  | instrument parameter (Optional[str]). |
| `method_hints` | `object` |  |  | Per-method keyword overrides, merged with the shared kwargs when dispatching each estimator. Structure:: {'proximal': {'proxy_z': ['z'], 'proxy_w': ['w']}, 'msm': {'time_varying': ['L_lag']}, 'principal_strat': {'strata': 's'}} **Collision rule** (docs/ROADMAP.md Section 6): per-method hints take precedence over the shared kwargs for the method they name. If the top-level ``covariates=['age']`` disagrees with ``method_hints={'proximal': {'covariates': ['age', 'educ']}}``, proximal uses the hint and every other method uses the shared arg. A ``UserWarning`` fires on conflict so the override is visible in the log. |
| `methods` | `array[string]` |  |  | Estimators to compare. Default auto-selects based on data. Classical options: ``'ols'``, ``'matching'``, ``'ipw'``, ``'aipw'``, ``'dml'``, ``'g_computation'``, ``'causal_forest'``, ``'did'``, ``'panel_fe'``. Hint-driven Sprint-B options (require ``method_hints``): ``'proximal'``, ``'msm'``, ``'principal_strat'``, ``'mediate'``, ``'mediate_interventional'``, ``'front_door'``. Each needs method-specific kwargs the shared signature does not expose (proxy_z/proxy_w, time_varying, strata, mediator, etc.) -- pass them through ``method_hints``. |
| `time` | `string` |  |  | Time variable. |
| `treatment` | `string` | ✓ |  | Treatment variable (binary). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.compare_estimators(y="outcome", data=df, treatment="value")
print(result.summary())
```

---
### `sp.design_intake()`

**Route design facts to a method-selection status.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assignment` | `string` |  |  | assignment parameter (Optional[str]). |
| `controls` | `string` |  |  | Control-variable column names. |
| `data_topology` | `string` |  |  | data_topology parameter (Optional[str]). |
| `estimand` | `string` |  |  | estimand parameter (Optional[str]). |
| `identification_support` | `string` |  |  | identification_support parameter (Optional[str]). |
| `needs` | `string` |  |  | needs parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.design_intake()
print(result.summary())
```

---
### `sp.detect_design()`

**Detect the most plausible study design from a DataFrame.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cutoff` | `number` |  |  | RD cutoff value (the heuristic does NOT auto-discover this). |
| `data` | `string` | ✓ |  | The dataset to inspect. Must have >= 1 row. |
| `running_var` | `string` |  |  | Force this numeric column to be evaluated as an RD running variable. |
| `time` | `string` |  |  | Column the caller has already identified as the time dimension. |
| `unit` | `string` |  |  | Column the caller has already identified as the unit ID. Skips unit-detection and pins this column. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.detect_design(data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`, `docs/guides/agent_native_workflow.md`, `docs/guides/data_mcp_ingestion.md`

---
### `sp.examples()`

**Return runnable code examples + registry metadata for a function.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | ✓ |  | Canonical StatsPAI function name (e.g. ``"did"``, ``"regress"``, ``"callaway_santanna"``). Lower-cased and stripped before lookup. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.examples(name="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`

---
### `sp.list_replications()`

**List all available replication datasets and guides.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.list_replications()
print(result.summary())
```

---
### `sp.methods_appendix()`

**Generate a referee-grade *Methods and Formulas* appendix for results.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `format` | `string (enum)` |  | `'latex'` | Output format. ``"latex"`` emits ``\subsection*`` blocks with display math; ``"markdown"`` emits ``###`` headings with ``$$`` math; ``"text"`` emits a plain-text rendering. |
| `include_assumptions` | `boolean` |  | `True` | Include the identifying-assumptions list. |
| `include_citation` | `boolean` |  | `True` | Append the APA-style reference from ``result.cite()``. |
| `include_diagnostics` | `boolean` |  | `True` | Include the inference block (SE method, clustering, bandwidth, F, CI). |
| `include_provenance` | `boolean` |  | `True` | Append a one-line provenance trace (StatsPAI version + estimator identity + methods-spec key) -- the "exact code path" leg of the formula / citation / code-path traceability triple. |
| `results` | `array[string]` | ✓ |  | One or more fitted result objects exposing ``method`` / ``model_info`` / ``cite``. |

> **format** options: `'latex'`, `'markdown'`, `'text'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.methods_appendix(formula="lwage ~ x1 + x2", results=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/methods_appendix.md`

---
### `sp.preflight()`

**Method-specific pre-estimation diagnostics.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | Same DataFrame the agent plans to pass to ``sp.{method}(...)``. |
| `method` | `string` | ✓ |  | Name of the StatsPAI estimator to pre-flight (e.g. ``"did"``, ``"rdrobust"``, ``"ivreg"``, ``"callaway_santanna"``, ``"ebalance"``). Unknown methods get only the universal DataFrame-shape sanity checks. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.preflight(data=df, method="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`, `docs/guides/agent_native_workflow.md`

---
### `sp.pub_ready()`

**Publication readiness checklist.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `design` | `string` |  |  | Research design: 'rct', 'did', 'rd', 'iv', 'observational'. |
| `has_balance` | `boolean` |  | `False` | Already have balance table. |
| `has_heterogeneity` | `boolean` |  | `False` | Already have subgroup analysis. |
| `has_mht` | `boolean` |  | `False` | Already have MHT correction. |
| `has_placebo` | `boolean` |  | `False` | Already have placebo tests. |
| `has_pretrends` | `boolean` |  | `False` | Already have pre-trend tests. |
| `has_robustness` | `boolean` |  | `False` | Already have robustness checks. |
| `has_sensitivity` | `boolean` |  | `False` | Already have sensitivity analysis. |
| `results` | `array[string]` |  |  | List of estimated result objects. |
| `venue` | `string` |  | `'top5_econ'` | Target venue: 'top5_econ', 'aej_applied', 'rct'. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.pub_ready()
print(result.summary())
```

---
### `sp.recommend()`

**Recommend the appropriate estimator(s) for your research question.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `allow_experimental` | `boolean` |  | `False` | Whether to include estimators registered as ``stability='experimental'`` (or ``'deprecated'``) in the ranked output. The default ``False`` is the agent-safe choice -- an LLM agent or pipeline that asks for an estimator recommendation should not silently land on a frontier MVP. Set ``True`` when you are explicitly exploring frontier methods (e.g. ``causal_text``, ``did_multiplegt_dyn``); dropped names are listed in ``RecommendationResult.warnings`` either way. See ``docs/guides/stability.md`` for the full contract. |
| `covariates` | `array[string]` |  |  | Control variables. |
| `cutoff` | `number` |  |  | RD cutoff value. |
| `dag` | `string` |  |  | Causal DAG for identification analysis. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `design` | `string` |  |  | Override design detection: 'rct', 'did', 'rd', 'iv', 'observational', 'panel', 'cross-section'. |
| `id` | `string` |  |  | Unit identifier (for panel data). |
| `instrument` | `string` |  |  | Instrumental variable. |
| `mediator` | `string` |  |  | Mediator variable name. Triggers mediation / front-door recommendations (Imai-Keele-Tingley 2010, VanderWeele et al. 2014, Pearl 1995). |
| `post_treat_strata` | `string` |  |  | Binary post-treatment variable defining principal strata (take-up, survival, employment, ...). Triggers `sp.principal_strat` (Frangakis & Rubin 2002). |
| `proxy_w` | `array[string]` |  |  | Outcome-side proxy variables (see `proxy_z`). |
| `proxy_z` | `array[string]` |  |  | Treatment-side proxy variables. Triggers `sp.proximal` when `proxy_w` is also supplied (Tchetgen Tchetgen et al. 2020). |
| `running_var` | `string` |  |  | Running variable (for RD designs). |
| `time` | `string` |  |  | Time variable (for panel/DID). |
| `treatment` | `string` |  |  | Treatment/exposure variable. |
| `tv_confounders` | `array[string]` |  |  | Time-varying confounders (must be pre-treatment at each period). Triggers `sp.msm` -- Marginal Structural Model via IPTW (Robins, Hernan & Brumback 2000). |
| `verify` | `boolean` |  | `False` | If True, run *resampling-stability* checks on the top-k recommendations (bootstrap CV, permutation placebo, 50%-subsample sign agreement) and attach a composite ``score`` to each recommendation's ``verify`` dict. The score is used to re-rank the top-k. Opt-in because it costs extra compute. |
| `verify_B` | `integer` |  | `50` | Bootstrap replications per recommendation (auto-capped by budget). |
| `verify_budget_s` | `number` |  | `30.0` | Wall-clock budget (seconds) per verified recommendation. |
| `verify_top_k` | `integer` |  | `3` | Number of top recommendations to verify. |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.recommend(y="outcome", data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`, `docs/guides/agent_native_workflow.md`, `docs/guides/data_mcp_ingestion.md`

---
### `sp.replicate()`

**Load a famous dataset and a step-by-step replication guide.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `key` | `string` | ✓ |  | Replication key (see ``sp.list_replications()``). |
| `simulated` | `boolean` |  |  | Override the entry's default data source. ``True`` forces a simulated replica; ``False`` forces the bundled real CSV (only valid for entries where ``has_real_data`` is True). Default ``None`` uses whatever the entry declares (currently real for ``card_1995`` and ``abadie_2010``). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.replicate(key="value")
print(result.summary())
```

---
### `sp.sensitivity_dashboard()`

**Comprehensive multi-dimensional sensitivity analysis.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` |  |  | Original data (auto-extracted if possible). |
| `dimensions` | `array[string]` |  |  | Which dimensions to test. Default: all applicable. |
| `result` | `string` | ✓ |  | Baseline estimated result. |
| `verbose` | `boolean` |  | `True` | verbose parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sensitivity_dashboard(data=df, result="value")
print(result.summary())
```

---
### `sp.session()`

**Set every reachable RNG to a known seed for the duration of the**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `jax` | `boolean` |  | `True` | Yield a fresh JAX ``PRNGKey(seed)`` to the caller via the ``jax_key`` attribute on the yielded session object, when JAX is already imported. Never imports jax on its own. (JAX has no global state so we can't seed it -- agents must thread the key explicitly.) |
| `pythonhashseed` | `boolean` |  | `False` | Set ``PYTHONHASHSEED`` for the duration of the block. Most causal-inference numerics don't depend on dict iteration order, but spec-curve enumerators and graph-based DAG search sometimes do. Off by default to avoid surprising downstream callers. |
| `seed` | `integer` |  |  | Seed value. ``None`` (the default) means "snapshot current state but don't reseed" -- useful for opportunistic save / restore around code that you don't want to leak RNG drift. |
| `torch` | `boolean` |  | `True` | Seed PyTorch (CPU + CUDA) when the library is already imported. Never imports torch on its own. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.session()
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`

---
