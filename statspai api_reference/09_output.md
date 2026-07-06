# output

> 📂 所属分类:09 · 结果导出与可视化 (Output & Visualization)

Output utilities for regression and causal-inference results.

The package is organised by purpose:

**Regression-table renderers** (4 entry points historically — see PR-B
design doc; ``regtable`` is the canonical one):

- :func:`regtable` — canonical multi-model regression table renderer.
  Supports text / HTML / LaTeX / Markdown / Quarto / Excel / Word /
  DataFrame, journal templates, multi-row SE, repro provenance.
- :func:`esttab` — Stata ``estout`` / ``esttab`` clone (use ``eststo``
  to register, then ``esttab`` to print). Thin Stata-flavoured surface.
- :func:`modelsummary` — R ``modelsummary`` clone (functional API).
- :func:`outreg2` / :class:`OutReg2` — Stata ``outreg2`` clone
  (Excel-first surface).

**Single-table helpers**:

- :func:`tab` — Stata-style ``tabulate``.
- :func:`sumstats` — descriptive summary statistics.
- :func:`balance_table` — covariate-balance table.
- :func:`mean_comparison` — two-group mean comparison with t-test /
  ranksum / chi2 (lives in ``mean_comparison.py`` since v1.6.x —
  re-exported from ``regression_table`` for back-compat).

**Multi-table / paper bundles**:

- :func:`paper_tables` — Main / Heterogeneity / Robustness panels.
- :class:`Collection` / :func:`collect` — narrative document builder.

**Plotting**:

- :func:`coefplot` — coefficient plot.

**Provenance / replication / citations**:

- :class:`Provenance`, :func:`attach_provenance`, :func:`get_provenance`,
  :func:`compute_data_hash`, :func:`format_provenance`,
  :func:`lineage_summary`.
- :class:`ReplicationPack`, :func:`replication_pack`.
- :func:`cite`, :data:`CSL_REGISTRY`, :func:`csl_url`, ...

**Adapters**:

- :func:`to_gt`, :func:`is_great_tables_available` — ``great_tables``
  adapter (lazy).

**39 个公共函数**

### `sp.Collection()`

**A named, ordered bundle of tables and prose for a single document.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `template` | `string (enum)` |  | `'aer'` | Forwarded to ``paper_tables`` style; also drives the default star levels used by ``add_regression``. |
| `title` | `string` |  |  | Displayed at the top of the rendered document. |

> **template** options: `'aer'`, `'qje'`, `'econometrica'`, `'restat'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.Collection()
print(result.summary())
```

---
### `sp.CollectionItem()`

**One entry in a :class:`Collection`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `kind` | `string` | ✓ |  | kind parameter (ItemKind). |
| `name` | `string` | ✓ |  | name parameter (str). |
| `options` | `object` |  | `None` | options parameter (Dict[str, Any]). |
| `payload` | `string` | ✓ |  | payload parameter. |
| `title` | `string` | ✓ |  | title parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CollectionItem(name="value", kind="value", title="value", payload="value")
print(result.summary())
```

---
### `sp.MeanComparisonResult()`

**Rich result object for balance / mean comparison tables.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `fmt` | `string` | ✓ |  | fmt parameter (str). |
> 📝 *fmt 参数（字符串）。*
| `group` | `string` | ✓ |  | Group or cohort identifier. |
> 📝 *组或队列标识符。*
| `group_labels` | `array[string]` | ✓ |  | group_labels parameter (Tuple[str, str]). |
> 📝 *group_labels 参数（字符串二元组）。*
| `output` | `string` |  | `'text'` | output parameter (str). |
> 📝 *output 参数（字符串）。*
| `test` | `string` | ✓ |  | test parameter (str). |
> 📝 *test 参数（字符串）。*
| `title` | `string` | ✓ |  | title parameter (str). |
> 📝 *title 参数（字符串）。*
| `variables` | `array[string]` | ✓ |  | variables parameter (List[str]). |
> 📝 *variables 参数（字符串列表）。*
> 📝 *variables 参数（字符串列表）。*
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.MeanComparisonResult(data=df, variables=["a", "b"], group="value", group_labels=["a", "b"], test="value", fmt="value", title="value", weights="value")
print(result.summary())
```

---
### `sp.OutReg2()`

**Stata-style stateful regression-table builder.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.OutReg2()
print(result.summary())
```

---
### `sp.PaperTables()`

**Container for the multi-panel paper-table bundle.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `heterogeneity` | `string` |  |  | heterogeneity parameter (Optional[RegtableResult]). |
| `main` | `string` |  |  | main parameter (Optional[RegtableResult]). |
| `placebo` | `string` |  |  | placebo parameter (Optional[RegtableResult]). |
| `robustness` | `string` |  |  | robustness parameter (Optional[RegtableResult]). |
| `template` | `string` |  | `'aer'` | template parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.PaperTables()
print(result.summary())
```

---
### `sp.Provenance()`

**A traceable record of how a single estimate was produced.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data_hash` | `string` |  |  | data_hash parameter (Optional[str]). |
| `data_shape` | `array[string]` |  |  | data_shape parameter (Optional[list]). |
| `function` | `string` | ✓ |  | function parameter (str). |
| `params` | `object` |  | `None` | params parameter (Dict[str, Any]). |
| `python_version` | `string` |  | `None` | python_version parameter (str). |
| `run_id` | `string` |  | `None` | run_id parameter (str). |
| `statspai_version` | `string` |  | `None` | statspai_version parameter (str). |
| `timestamp` | `string` |  | `None` | timestamp parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.Provenance(function="value")
print(result.summary())
```

> 📁 See also: `docs/guides/replication_workflow.md`

---
### `sp.RegtableResult()`

**Rich result object for regression tables with multi-format export.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `add_rows` | `array[string]` | ✓ |  | add_rows parameter (Optional[Dict[str, List[str]]]). |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `apply_coef` | `string` |  |  | apply_coef parameter (Optional[Any]). |
| `apply_coef_deriv` | `string` |  |  | apply_coef_deriv parameter (Optional[Any]). |
| `coef_labels` | `object` | ✓ |  | coef_labels parameter (Optional[Dict[str, str]]). |
| `column_spanners` | `array[string]` |  |  | column_spanners parameter (Optional[List[Tuple[str, int]]]). |
| `dep_var_labels` | `array[string]` | ✓ |  | dep_var_labels parameter (Optional[List[str]]). |
| `drop` | `array[string]` | ✓ |  | drop parameter (Optional[List[str]]). |
| `eform_flags` | `array[string]` |  |  | eform_flags parameter (Optional[List[bool]]). |
| `escape` | `boolean` |  | `True` | escape parameter (bool). |
| `estimate_template` | `string` |  |  | estimate_template parameter (Optional[str]). |
| `fmt` | `string` | ✓ |  | fmt parameter (str). |
> 📝 *fmt 参数（字符串）。*
| `keep` | `array[string]` | ✓ |  | keep parameter (Optional[List[str]]). |
| `model_labels` | `array[string]` | ✓ |  | model_labels parameter (List[str]). |
| `multi_se` | `array[string]` |  |  | multi_se parameter (Optional[List[Tuple[str, List[Dict[str, float]]]]]). |
| `notation` | `array[string]` |  | `'stars'` | notation parameter (Union[str, Tuple[str, ...]]). |
| `notes` | `array[string]` | ✓ |  | notes parameter (Optional[List[str]]). |
| `order` | `array[string]` | ✓ |  | order parameter (Optional[List[str]]). |
| `output` | `string` |  | `'text'` | output parameter (str). |
> 📝 *output 参数（字符串）。*
| `panel_labels` | `array[string]` | ✓ |  | panel_labels parameter (Optional[List[str]]). |
| `panels` | `array[string]` | ✓ |  | panels parameter (List['_PanelData']). |
| `quarto_caption` | `string` |  |  | quarto_caption parameter (Optional[str]). |
| `quarto_label` | `string` |  |  | quarto_label parameter (Optional[str]). |
| `se_label` | `string` |  |  | se_label parameter (Optional[str]). |
| `se_type` | `string` | ✓ |  | se_type parameter (str). |
| `star_levels` | `array[string]` | ✓ |  | star_levels parameter (Tuple[float, ...]). |
| `stars` | `boolean` | ✓ |  | stars parameter (bool). |
| `statistic_template` | `string` |  |  | statistic_template parameter (Optional[str]). |
| `stats` | `array[string]` | ✓ |  | stats parameter (Optional[List[str]]). |
| `template` | `string` |  |  | template parameter (Optional[str]). |
| `tests_rows` | `array[string]` |  |  | tests_rows parameter (Optional[List[Tuple[str, List[str]]]]). |
| `title` | `string` | ✓ |  | title parameter (Optional[str]). |
| `transpose` | `boolean` |  | `False` | transpose parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.RegtableResult(panels=["a", "b"], panel_labels=["a", "b"], model_labels=["a", "b"], dep_var_labels=["a", "b"], keep=["a", "b"], drop=["a", "b"], order=["a", "b"], se_type="value", stars=True, star_levels=["a", "b"], fmt="value", title="value", notes=["a", "b"], add_rows=["a", "b"], stats=["a", "b"])
print(result.summary())
```

---
### `sp.ReplicationPack()`

**Lightweight summary returned by :func:`replication_pack`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `manifest` | `object` | ✓ |  | manifest parameter (Dict[str, Any]). |
| `output_path` | `string` | ✓ |  | Filesystem path for output. |
| `warnings` | `array[string]` | ✓ |  | warnings parameter (List[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.ReplicationPack(output_path="value", warnings=["a", "b"])
print(result.summary())
```

---
### `sp.attach_provenance()`

**Attach a :class:`Provenance` record as ``result._provenance``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` |  |  | The estimator's input data. Used to compute a 12-char SHA-256 fingerprint. |
| `enabled` | `boolean` |  | `True` | Set to False to skip provenance entirely (zero-overhead path). |
| `function` | `string` | ✓ |  | Logical name of the producing call, e.g. ``"statspai.did.callaway_santanna"``. |
| `overwrite` | `boolean` |  | `False` | If False (default) and ``result._provenance`` already exists, do nothing -- preserves the *first* (most-specific) record set by an inner estimator. |
| `params` | `object` |  |  | Call arguments. Will be summarised (frames hashed; long sequences truncated; non-serialisable values reduced to repr). |
| `result` | `string` | ✓ |  | The estimator result. Must accept attribute assignment; ``CausalResult`` / ``ResultBase`` / dataclasses / SimpleNamespace all work. Tuples / dicts / immutable types do not -- for those the call is a silent no-op. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.attach_provenance(data=df, result="value", function="value")
print(result.summary())
```

> 📁 See also: `docs/guides/replication_workflow.md`

---
### `sp.balance_table()`

**Generate a balance table comparing treated and control groups.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` | ✓ |  | Variables to check balance on. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `fmt` | `string` |  | `'%.3f'` | Number format. |
| `labels` | `object` |  |  | Variable labels. |
| `output` | `string` |  | `'text'` | 'text', 'latex', 'html', 'dataframe', or filepath. |
| `test` | `string` |  | `'ttest'` | Test for difference: 'ttest' or 'ranksum'. |
| `title` | `string` |  | `'Balance Table'` | Table title. |
| `treat` | `string` | ✓ |  | Binary treatment variable (0/1). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.balance_table(data=df, treat="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.citations_to_bib_entries()`

**Parse a sequence of citation strings into BibTeX-entry dicts.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `citations` | `array[string]` | ✓ |  | citations parameter (Iterable[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.citations_to_bib_entries(citations=["a", "b"])
print(result.summary())
```

---
### `sp.cite()`

**Inline coefficient citation -- formats one term as e.g. '0.234*** (0.041)' for embedding directly in manuscript prose, Jupyter Markdown cells, or Quarto inline expressions. Mirrors regtable's formatting conventions (stars, SE/CI brackets) for cross-table consistency.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | CI level when second_row='ci' |
| `fmt` | `string` |  | `'%.3f'` | printf-style format string |
| `output` | `string (enum)` |  | `'text'` | Markup |
| `result` | `string` | ✓ |  | EconometricResults or CausalResult |
| `second_row` | `string (enum)` |  | `'se'` | What to put in parens |
| `term` | `string` |  |  | Coefficient name (default: estimand or first param) |

> **output** options: `'text'`, `'latex'`, `'markdown'`, `'html'`

> **second_row** options: `'se'`, `'t'`, `'p'`, `'ci'`, `'none'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.cite(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`, `docs/guides/choosing_did_estimator.md`, `docs/guides/decomposition_family.md`

---
### `sp.coefplot()`

**Forest plot comparing coefficients across models.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for CIs. |
| `ax` | `string` |  |  | ax parameter. |
| `colors` | `array[string]` |  |  | colors parameter (Optional[List[str]]). |
| `figsize` | `array[string]` |  | `[8, 6]` | figsize parameter (tuple). |
| `model_names` | `array[string]` |  |  | model_names parameter (Optional[List[str]]). |
| `title` | `string` |  |  | title parameter (Optional[str]). |
| `variables` | `array[string]` |  |  | Which variables to plot. Default: all shared variables. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.coefplot()
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`

---
### `sp.coefplot_tikz()`

**Return ``pgfplots`` / TikZ source for a coefficient forest plot.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coef_labels` | `object` |  |  | Rename variables on the y-axis, e.g. ``{"x": "Treatment"}``. |
| `level` | `number` |  | `0.95` | Confidence level for the error bars (normal approximation ``b +/- z*se``, matching :func:`coefplot`). |
| `model_names` | `array[string]` |  |  | Legend labels. Default ``Model 1``, ``Model 2``, ... |
| `standalone` | `boolean` |  | `False` | When ``True``, wrap the ``tikzpicture`` in a compilable ``standalone`` document (with the required ``\usepackage{pgfplots}``). Otherwise return just the ``tikzpicture`` to ``\input`` into a paper (needs ``\usepackage{pgfplots}`` in the preamble). |
| `title` | `string` |  |  | Plot title. Default ``"Coefficient plot"``. |
| `variables` | `array[string]` |  |  | Which coefficients to plot. Default: every shared variable, sorted. |
| `xlabel` | `string` |  | `'Coefficient estimate'` | x-axis label. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.coefplot_tikz()
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`

---
### `sp.collect()`

**Session-level multi-table container (Stata 15 collect / R gt::gtsave style). Gather regressions, summary stats, balance tables, and free-form text in one Collection, then export the whole bundle to a single .docx / .xlsx / .tex / .md / .html file.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `template` | `string (enum)` |  | `'aer'` | Journal style template |
| `title` | `string` |  |  | Document title shown at the top |

> **template** options: `'aer'`, `'qje'`, `'econometrica'`, `'restat'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.collect()
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`

---
### `sp.compute_data_hash()`

**Return a short SHA-256 fingerprint of *data*, or ``None``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `length` | `integer` |  | `12` | length parameter (int). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.compute_data_hash(data=df)
print(result.summary())
```

---
### `sp.csl_filename()`

**Return the canonical ``.csl`` *filename* (no path) for a preset.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | ✓ |  | name parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.csl_filename(name="value")
print(result.summary())
```

---
### `sp.csl_url()`

**Return the canonical Zotero/styles URL for a CSL preset.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | ✓ |  | name parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.csl_url(name="value")
print(result.summary())
```

> 📁 See also: `docs/guides/replication_workflow.md`

---
### `sp.estclear()`

**Clear all stored model results.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.estclear()
print(result.summary())
```

---
### `sp.eststo()`

**Store a model result (like Stata's ``estimates store``).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` |  |  | name parameter (Optional[str]). |
| `result` | `string` | ✓ |  | result parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.eststo(result="value")
print(result.summary())
```

---
### `sp.esttab()`

**Stata-style esttab clone -- tabulate one or more model results (or models stored via sp.eststo) into text/LaTeX/HTML/Markdown/CSV.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | CI level when ci=True |
| `ci` | `boolean` |  | `False` | Show confidence intervals instead of SE |
| `results` | `array[string]` |  |  | Models; falls back to global eststo store |
| `se` | `boolean` |  | `True` | Show standard errors |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.esttab()
print(result.summary())
```

---
### `sp.format_provenance()`

**Pretty multi-line rendering of a :class:`Provenance` record.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `indent` | `integer` |  | `2` | indent parameter (int). |
| `prov` | `string` | ✓ |  | prov parameter (Provenance). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.format_provenance(prov="value")
print(result.summary())
```

---
### `sp.get_journal_template()`

**Look up a journal preset by name (case-insensitive).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `string` | ✓ |  | Template identifier (e.g. ``"aer"`` / ``"AER"`` / ``"jf"``). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.get_journal_template(name="value")
print(result.summary())
```

---
### `sp.get_provenance()`

**Return ``result._provenance`` if present, else ``None``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | result parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.get_provenance(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/replication_workflow.md`

---
### `sp.is_great_tables_available()`

**Return True iff ``great_tables`` can be imported in this env.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.is_great_tables_available()
print(result.summary())
```

---
### `sp.lineage_summary()`

**Aggregate a lineage report across multiple results.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lineage_summary()
print(result.summary())
```

---
### `sp.list_csl_styles()`

**List ``(short_name, full_label)`` pairs for every registered style.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.list_csl_styles()
print(result.summary())
```

> 📁 See also: `docs/guides/replication_workflow.md`

---
### `sp.list_journal_templates()`

**Return the canonical names of every registered journal preset.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.list_journal_templates()
print(result.summary())
```

---
### `sp.make_bib_key()`

**Compute a stable BibTeX key from a free-form citation string.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `citation` | `string` | ✓ |  | citation parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.make_bib_key(citation="value")
print(result.summary())
```

---
### `sp.mean_comparison()`

**Balance / mean-comparison table -- Mean (SD) per group, difference, and t-test/ranksum/chi2 p-value. Renders to text/LaTeX/HTML/Markdown/Excel/Word.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `group` | `string` | ✓ |  | Binary grouping variable |
| `test` | `string (enum)` |  | `'ttest'` | Statistical test |
| `variables` | `array[string]` | ✓ |  | Columns to compare |

> **test** options: `'ttest'`, `'ranksum'`, `'chi2'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mean_comparison(data=df, variables=["a", "b"], group="value")
print(result.summary())
```

---
### `sp.modelsummary()`

**Summary table comparing multiple models side by side.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `results` | `array[string]` | ✓ |  | List of EconometricResults |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.modelsummary(results=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`, `docs/guides/migration-from-r.md`

---
### `sp.outreg2()`

**Export regression results to publication-quality tables (Excel, LaTeX, Word).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filename` | `string` | ✓ |  | Output file path (.xlsx, .tex, .docx) |
| `results` | `array[string]` | ✓ |  | One or more EconometricResults objects |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.outreg2(results=["a", "b"], filename="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.paper_tables()`

**Multi-panel paper-facing table bundle (Main / Heterogeneity / Robustness / Placebo) with one-shot export to LaTeX/Markdown/Word/Excel.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `heterogeneity` | `array[string]` |  |  | Subsample / interaction results |
| `main` | `array[string]` | ✓ |  | Main-spec results |
| `placebo` | `array[string]` |  |  | Placebo-outcome results |
| `robustness` | `array[string]` |  |  | Alt-estimator results |
| `template` | `string (enum)` |  | `'aer'` | Journal preset |

> **template** options: `'aer'`, `'qje'`, `'econometrica'`, `'restat'`, `'jf'`, `'aeja'`, `'jpe'`, `'restud'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.paper_tables(main=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`

---
### `sp.parse_citation_to_bib()`

**Parse a citation string into a BibTeX-shaped dict.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `citation` | `string` | ✓ |  | citation parameter (str). |
| `key` | `string` |  |  | key parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.parse_citation_to_bib(citation="value")
print(result.summary())
```

---
### `sp.regtable()`

**Publication-quality multi-model regression table with auto-extracted diagnostic rows (FE/Cluster indicators, IV first-stage F, DiD pre-trend p, RD bandwidth/kernel/poly), journal presets (AER/QJE/Econometrica/JF/AEJA/etc.), multi-SE side-by-side display, eform odds-ratio / IRR / HR transformation with delta-method SE, column spanners (\multicolumn / colspan / cmidrule), unified coef_map (rename + order + drop), depvar_mean / depvar_sd auto rows, and N-mismatch consistency warnings. Returns a RegtableResult exporting to text/LaTeX/HTML/Markdown/Quarto/Word/Excel plus an agent-native to_dict()/to_json() payload (metadata + rendered cell grid + numeric truth per model); save(filename) and filename= infer the format from the extension, including .json.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `apply_coef` | `string` |  |  | Arbitrary coefficient transform (generalises eform); mutually exclusive with eform |
| `apply_coef_deriv` | `string` |  |  | Derivative of apply_coef for delta-method SE rescaling |
| `coef_map` | `object` |  |  | Single-shot rename + reorder + drop (mutually exclusive with coef_labels/keep/drop/order) |
| `column_spanners` | `array[string]` |  |  | Multi-row header: list of (label, span) tuples whose spans partition the model columns (e.g. [('OLS', 2), ('IV', 2)]) |
| `consistency_check` | `boolean` |  | `True` | Warn when sample sizes differ across columns |
| `diagnostics` | `boolean` |  | `'auto'` | Auto-extract FE/Cluster/IV/DiD/RD rows |
| `eform` | `boolean` |  | `False` | Report exp(b) (OR/IRR/HR) with delta-method SE; pass per-model list to mix transformed/untransformed columns |
| `escape` | `boolean` |  | `True` | Auto-escape user-supplied label strings; pass False to preserve raw LaTeX/HTML markup verbatim |
| `estimate` | `string` |  |  | Top-line cell template -- placeholders {estimate} {stars} {std_error} {t_value} {p_value} {conf_low} {conf_high} |
| `filename` | `string` |  |  | File path; format inferred from extension |
| `fixef_sizes` | `boolean` |  | `False` | Auto-emit '# Firm: N' rows from model_info['n_fe_levels'] |
| `multi_se` | `object` |  |  | Stack alternative SE specs under primary SE |
| `notation` | `array (enum)[string]` |  | `'stars'` | Significance marker family |
| `output` | `string (enum)` |  | `'text'` | Render format |
| `repro` | `boolean` |  |  | Append reproducibility footer (version+seed+data hash) |
| `results` | `array[string]` | ✓ |  | Model result objects (positional) |
| `se_type` | `string (enum)` |  | `'se'` | Bottom-row content |
| `statistic` | `string` |  |  | Bottom-line cell template (same placeholders as estimate) |
| `template` | `string (enum)` |  |  | Journal preset |
| `tests` | `object` |  |  | Hypothesis-test rows: {label: [(stat,p) \| p \| None per model]} (stars honour notation) |
| `transpose` | `boolean` |  | `False` | Pivot rows<->columns (single-panel; rejects multi_se) |
| `vcov` | `string (enum)` |  |  | Recompute SE/t/p/CI at print time (OLS-only) |

> **notation** options: `'stars'`, `'symbols'`

> **output** options: `'text'`, `'latex'`, `'html'`, `'markdown'`, `'word'`, `'excel'`

> **se_type** options: `'se'`, `'t'`, `'p'`, `'ci'`

> **template** options: `'aer'`, `'qje'`, `'econometrica'`, `'restat'`, `'jf'`, `'aeja'`, `'jpe'`, `'restud'`

> **vcov** options: `'HC0'`, `'HC1'`, `'HC2'`, `'HC3'`, `'robust'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.regtable(results=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`, `docs/guides/migration-from-r.md`, `docs/guides/replication_workflow.md`

---
### `sp.replication_pack()`

**Package an analysis (PaperDraft / fitted result / list of results) into a replication zip: data CSV + schema manifest, caller code, frozen environment, rendered paper (md/qmd/tex/docx), citations, and an aggregated lineage.json from any results carrying Provenance. The archive's MANIFEST.json records SHA-256 for every file plus the git SHA when available.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bib` | `boolean` |  | `True` | Write paper/paper.bib from citations |
| `code` | `string` |  |  | Inline script or path to .py file |
| `data` | `string` |  |  | Explicit data; falls back to target.data / target.workflow.data |
| `env` | `boolean` |  | `True` | Capture pip freeze of the runtime |
| `extra_files` | `object` |  |  | extra_files parameter (dict). |
| `include_git_sha` | `boolean` |  | `True` | Whether to include git sha. |
| `output_path` | `string` | ✓ |  | Destination .zip path |
| `overwrite` | `boolean` |  | `True` | overwrite parameter (bool). |
| `paper_format` | `string (enum)` |  | `'auto'` | paper_format parameter (str). |
| `target` | `string` | ✓ |  | PaperDraft, fitted result, list of results, or None for a data-only pack |
| `title` | `string` |  | `'Replication Pack'` | title parameter (str). |

> **paper_format** options: `'auto'`, `'md'`, `'qmd'`, `'tex'`, `'docx'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.replication_pack(data=df, target="value", output_path="value")
print(result.summary())
```

> 📁 See also: `docs/guides/replication_workflow.md`

---
### `sp.sumstats()`

**Generate descriptive statistics table.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `by` | `string` |  |  | Group-by variable for stratified summaries. |
| `by_labels` | `object` |  |  | Group labels for ``by=`` panel headers, e.g. ``{0: 'Control', 1: 'Treated'}``. When ``by`` is binary 0/1 and no ``by_labels`` is supplied, ``Control``/``Treated`` is auto-applied so academic Table 1 reads correctly out of the box. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `fmt` | `string` |  | `'%.3f'` | Number format. |
| `labels` | `object` |  |  | Variable labels: ``{'x1': 'Education (years)'}``. |
| `output` | `string` |  | `'text'` | 'text', 'latex', 'html', 'dataframe', or filepath (.xlsx/.docx). |
| `stats` | `array[string]` |  |  | Statistics to compute. Default: ['n', 'mean', 'sd', 'min', 'p25', 'median', 'p75', 'max']. |
| `title` | `string` |  | `'Summary Statistics'` | Table title. |
| `vars` | `array[string]` |  |  | Variables to summarize. Defaults to all numeric columns. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sumstats(data=df)
print(result.summary())
```

---
### `sp.tab()`

**Cross-tabulation with chi-squared / Fisher's exact test.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `col` | `string` |  |  | Column variable. If None, produces a one-way frequency table. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `margins` | `boolean` |  | `True` | Show row/column totals. |
| `normalize` | `string` |  |  | 'row', 'col', 'all', or None. Normalize to proportions. |
| `output` | `string` |  | `'text'` | 'text', 'dataframe', 'latex', or filepath (.xlsx/.docx). |
| `row` | `string` | ✓ |  | Row variable. |
| `test` | `boolean` |  | `True` | Include chi-squared test (and Fisher's exact for 2x2). |
| `title` | `string` |  |  | Table title. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.tab(data=df, row="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.write_bib()`

**Write a clean BibTeX file from citation strings or entry dicts.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `append` | `boolean` |  | `False` | Append to an existing file rather than overwriting. |
| `citations` | `array[string]` | ✓ |  | Either free-form citation strings (parsed via :func:`parse_citation_to_bib`) or pre-built entry dicts ``{"key": ..., "type": ..., "fields": {...}}``. |
| `header` | `boolean` |  | `True` | Prepend a one-line ``% Auto-generated by StatsPAI ...`` comment at the top of fresh files (skipped on append). |
| `path` | `string` | ✓ |  | Destination ``.bib`` file. Parent dirs are created. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.write_bib(citations=["a", "b"], path="value")
print(result.summary())
```

> 📁 See also: `docs/guides/replication_workflow.md`

---
