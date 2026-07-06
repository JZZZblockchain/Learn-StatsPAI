# did — 双重差分

> 📂 所属分类:01 · 核心因果推断方法 (Core Causal Methods)

Difference-in-Differences (DID) module for StatsPAI.
> 📝 *StatsPAI 的双重差分法（Difference-in-Differences，DID）模块。*

Provides estimators for:
> 📝 *提供以下估计方法：*
- Classic 2×2 DID (two groups, two periods)
> 📝 *经典 2×2 DID（两组、两期）*
- Triple Differences / DDD (two groups, two periods, within-unit subgroup)
> 📝 *三重差分法（Triple Differences / DDD）（两组、两期、组内子群）*
- Callaway & Sant'Anna (2021) — staggered DID with DR/IPW/REG
> 📝 *Callaway & Sant'Anna（2021）— 交错处理时点 DID，支持 DR/IPW/REG 三种估计方法*
- Sun & Abraham (2021) — interaction-weighted event study
> 📝 *Sun & Abraham（2021）— 交互加权事件研究*
- Synthetic DID (Arkhangelsky et al. 2021)
> 📝 *合成双重差分法 / Synthetic DID（Arkhangelsky et al. 2021）*
- Goodman-Bacon (2021) — TWFE decomposition diagnostic
> 📝 *Goodman-Bacon（2021）— 双向固定效应（Two-Way Fixed Effects，TWFE）分解诊断*
- Honest DID (Rambachan & Roth 2023) — parallel trends sensitivity
> 📝 *Honest DID（Rambachan & Roth 2023）— 平行趋势敏感性分析*
- de Chaisemartin & D'Haultfoeuille (2020) — DID with treatment switching
> 📝 *de Chaisemartin & D'Haultfoeuille（2020）— 处理状态可切换的 DID*
- Borusyak, Jaravel & Spiess (2024) — imputation DID estimator
> 📝 *Borusyak, Jaravel & Spiess（2024）— 插补法 DID 估计*
- Stacked DID (Cengiz, Dube, Lindner & Zipperer, 2019)
> 📝 *堆叠 DID / Stacked DID（Cengiz, Dube, Lindner & Zipperer, 2019）*
- did_analysis() — one-call DID workflow
> 📝 *did_analysis() — 一站式 DID 工作流*
- Wooldridge (2021) — extended TWFE with cohort × time interactions
> 📝 *Wooldridge（2021）— 扩展双向固定效应（Extended TWFE，ETWFE），含队列 × 时间交互项*
- Sant'Anna & Zhao (2020) — doubly robust DID
> 📝 *Sant'Anna & Zhao（2020）— 双重稳健 DID*
- TWFE decomposition — Bacon (2021) + de Chaisemartin–D'Haultfoeuille (2020) weights
> 📝 *TWFE 分解 — Bacon（2021）+ de Chaisemartin–D'Haultfoeuille（2020）权重*

**59 个公共函数**

### `sp.CSReport()`

**Structured output of :func:`cs_report`.**
> 📝 ***:func:`cs_report` 的结构化输出。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `breakdown` | `string` | ✓ |  | breakdown parameter (pd.DataFrame). | breakdown 参数（pandas 数据框）。 |
| `calendar` | `string` | ✓ |  | calendar parameter (pd.DataFrame). | calendar 参数（pandas 数据框）。 |
| `dynamic` | `string` | ✓ |  | dynamic parameter (pd.DataFrame). | dynamic 参数（pandas 数据框）。 |
| `group` | `string` | ✓ |  | Group or cohort identifier. | 组或队列标识符。 |
| `meta` | `object` |  | `None` | meta parameter (Dict[str, Any]). | meta 参数（字典，键为字符串，值为任意类型）。 |
| `overall` | `object` | ✓ |  | overall parameter (Dict[str, float]). | overall 参数（字典，键为字符串，值为浮点数）。 |
| `pretrend` | `object` | ✓ |  | pretrend parameter (Dict[str, Any]). | pretrend 参数（字典，键为字符串，值为任意类型）。 |
| `simple` | `string` | ✓ |  | simple parameter (pd.DataFrame). | simple 参数（pandas 数据框）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.CSReport(simple="value", dynamic="value", group="value", calendar="value", breakdown="value")
print(result.summary())
```

---
### `sp.CausalResult()`

**Unified result object for all causal inference methods in StatsPAI.**
> 📝 ***StatsPAI 中所有因果推断方法的统一结果对象。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `_citation_key` | `string` |  |  | Key into the citation registry. | 引用注册表的键。 |
| `_influence_funcs` | `string` |  |  | Influence function matrix (n_units, n_estimates) for joint inference. | 用于联合推断的影响函数矩阵（n_units × n_estimates）。 |
| `alpha` | `number` | ✓ |  | Significance level used for CI. | 置信区间所用的显著性水平。 |
| `ci` | `array[string]` | ✓ |  | Confidence interval (lower, upper). | 置信区间（下限，上限）。 |
| `detail` | `string` |  |  | Detailed estimates (e.g., group-time ATTs). | 详细估计结果（例如，组-时 ATT）。 |
| `estimand` | `string` | ✓ |  | What is being estimated ('ATT', 'ATE', 'LATE'). | 估计对象（'ATT'：处理组平均处理效应，'ATE'：平均处理效应，'LATE'：局部平均处理效应）。 |
| `estimate` | `number` | ✓ |  | Point estimate of the main treatment effect. | 主要处理效应的点估计。 |
| `method` | `string` | ✓ |  | Name of the estimation method (displayed in summary). | 估计方法名称（在摘要中显示）。 |
| `model_info` | `object` |  |  | Model metadata and aggregated results. | 模型元数据和汇总结果。 |
| `n_obs` | `integer` | ✓ |  | Number of observations. | 观测值数量。 |
| `pvalue` | `number` | ✓ |  | Two-sided p-value for H0: effect = 0. | 原假设 H0: 效应 = 0 的双侧 p 值。 |
| `se` | `number` | ✓ |  | Standard error. | 标准误。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.CausalResult(method="value", estimand="value", estimate=1.0, se=1.0, pvalue=1.0, ci=["a", "b"], alpha=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.DIDAnalysis()`

**Bundled results from a full DID analysis workflow.**
> 📝 ***完整 DID 分析工作流的打包结果。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `bacon` | `object` |  |  | bacon parameter (Optional[Dict[str, Any]]). | bacon 参数（可选字典，键为字符串，值为任意类型）。 |
| `design` | `string` | ✓ |  | design parameter (str). | design 参数（字符串）。 |
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). | diagnostics 参数（可选字典，键为字符串，值为任意类型）。 |
| `event_study_result` | `string` |  |  | event_study_result parameter (Optional[CausalResult]). | event_study_result 参数（可选 CausalResult 对象）。 |
| `main_result` | `string` | ✓ |  | main_result parameter (CausalResult). | main_result 参数（CausalResult 对象）。 |
| `method_used` | `string` | ✓ |  | method_used parameter (str). | method_used 参数（字符串）。 |
| `sensitivity` | `string` |  |  | sensitivity parameter (Optional[pd.DataFrame]). | sensitivity 参数（可选 pandas 数据框）。 |
| `steps_log` | `array[string]` |  | `None` | steps_log parameter (List[str]). | steps_log 参数（字符串列表）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.DIDAnalysis(design="value", method_used="value", main_result="value")
print(result.summary())
```

---
### `sp.DataInsufficient()`

**Sample or design is too small / sparse for the chosen method.**
> 📝 ***样本或设计规模过小/过于稀疏，不适用于所选方法。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alternative_functions` | `array[string]` |  |  | alternative_functions parameter (Optional[List[str]]). | alternative_functions 参数（可选字符串列表）。 |
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). | diagnostics 参数（可选字典，键为字符串，值为任意类型）。 |
| `message` | `string` | ✓ |  | message parameter (str). | message 参数（字符串）。 |
| `recovery_hint` | `string` |  | `''` | recovery_hint parameter (str). | recovery_hint 参数（字符串）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.DataInsufficient(message="value")
print(result.summary())
```

---
### `sp.HarvestDIDResult()`

**Full diagnostic output of :func:`harvest_did`.**
> 📝 ***:func:`harvest_did` 的完整诊断输出。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` | ✓ |  | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple). | ci 参数（元组）。 |
| `comparisons` | `string` | ✓ |  | comparisons parameter (pd.DataFrame). | comparisons 参数（pandas 数据框）。 |
| `diagnostics` | `object` |  | `None` | diagnostics parameter (Dict[str, Any]). | diagnostics 参数（字典，键为字符串，值为任意类型）。 |
| `estimate` | `number` | ✓ |  | estimate parameter (float). | estimate 参数（浮点数）。 |
| `event_study` | `string` | ✓ |  | event_study parameter (pd.DataFrame). | event_study 参数（pandas 数据框）。 |
| `method` | `string` |  | `'harvest_did'` | Estimator or algorithm variant to use. | 所使用的估计器或算法变体。 |
| `n_comparisons` | `integer` | ✓ |  | Number of comparisons. | 比较数量。 |
| `pretrend_test` | `object` | ✓ |  | pretrend_test parameter (Dict[str, float]). | pretrend_test 参数（字典，键为字符串，值为浮点数）。 |
| `se` | `number` | ✓ |  | se parameter (float). | se 参数（浮点数，标准误）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.HarvestDIDResult(estimate=1.0, se=1.0, ci=["a", "b"], alpha=1.0, n_comparisons=1.0, comparisons="value", event_study="value")
print(result.summary())
```

---
### `sp.MethodIncompatibility()`

**The requested method is incompatible with the data / options.**
> 📝 ***所请求的方法与数据/选项不兼容。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alternative_functions` | `array[string]` |  |  | alternative_functions parameter (Optional[List[str]]). | alternative_functions 参数（可选字符串列表）。 |
| `diagnostics` | `object` |  |  | diagnostics parameter (Optional[Dict[str, Any]]). | diagnostics 参数（可选字典，键为字符串，值为任意类型）。 |
| `message` | `string` | ✓ |  | message parameter (str). | message 参数（字符串）。 |
| `recovery_hint` | `string` |  | `''` | recovery_hint parameter (str). | recovery_hint 参数（字符串）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.MethodIncompatibility(message="value")
print(result.summary())
```

---
### `sp.SensitivityResult()`

**Result of Rambachan & Roth (2023) sensitivity analysis.**
> 📝 ***Rambachan & Roth（2023）敏感性分析的结果。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `att` | `number` | ✓ |  | att parameter (float). | att 参数（浮点数，处理组平均处理效应）。 |
| `att_se` | `number` | ✓ |  | att_se parameter (float). | att_se 参数（浮点数，处理组平均处理效应的标准误）。 |
| `breakdown_mbar` | `number` | ✓ |  | breakdown_mbar parameter (float). | breakdown_mbar 参数（浮点数）。 |
| `ci_lower` | `string` | ✓ |  | ci_lower parameter (np.ndarray). | ci_lower 参数（numpy 数组）。 |
| `ci_upper` | `string` | ✓ |  | ci_upper parameter (np.ndarray). | ci_upper 参数（numpy 数组）。 |
| `mbar_grid` | `string` | ✓ |  | Grid of mbar values to evaluate. | 待评估的 mbar 值网格。 |
| `method` | `string` |  | `'C-LF'` | Estimator or algorithm variant to use. | 所使用的估计器或算法变体。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.SensitivityResult(mbar_grid="value", ci_lower="value", ci_upper="value", breakdown_mbar=1.0, att=1.0, att_se=1.0)
print(result.summary())
```

---
### `sp.aggte()`

**Aggregate Callaway-Sant'Anna group-time ATTs into interpretable summaries -- overall ATT, event-study by relative time, group-specific ATT(g), or calendar-time ATT(t). Inference uses the multiplier bootstrap on the pre-stored influence functions, so SEs are correct under clustering at the unit level. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 ***将 Callaway-Sant'Anna 组-时 ATT（分组-时间平均处理效应，Average Treatment Effect on the Treated）聚合为可解释的汇总指标 — 总体 ATT、按相对时间的事件研究、分组特定 ATT(g) 或日历时间 ATT(t)。推断使用预存影响函数上的乘数自举法（multiplier bootstrap），因此标准误（Standard Error，SE）在单元级聚类下是正确的。验证状态：已验证证据层（已知真实值、参考实现、外部一致性或蒙特卡洛模拟验证）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `balance_e` | `integer` |  |  | For dynamic: cap event time at +/-balance_e for balanced panel | 用于动态聚合：为平衡面板将事件时间上限设为 +/-balance_e |
| `boot_type` | `string (enum)` |  | `'multiplier'` | Bootstrap variant | 自举方法类型，可选值：`'multiplier'` — 乘数自举法 |
| `bstrap` | `boolean` |  | `True` | bstrap parameter (bool). | bstrap 参数（布尔值）。 |
| `cband` | `boolean` |  | `True` | Uniform confidence band | 一致置信带 |
| `max_e` | `number` |  | `inf` | max_e parameter (float). | max_e 参数（浮点数）。 |
| `min_e` | `number` |  | `-inf` | min_e parameter (float). | min_e 参数（浮点数）。 |
| `n_boot` | `integer` |  | `1000` | Number of bootstrap replications. | 自举重复次数。 |
| `na_rm` | `boolean` |  | `True` | Drop ATT(g,t) cells with missing / infinite SE before aggregating | 聚合前删除标准误缺失/无穷大的 ATT(g,t) 单元格 |
| `random_state` | `integer` |  |  | Random seed or RandomState for reproducible stochastic steps. | 随机种子或 RandomState，用于可复现的随机步骤。 |
| `result` | `string` | ✓ |  | Output of sp.callaway_santanna or sp.did with staggered=True | sp.callaway_santanna 或 staggered=True 时 sp.did 的输出结果 |
| `type` | `string (enum)` |  | `'simple'` | Aggregation type | 聚合类型，可选值：`'simple'` — 简单聚合、`'dynamic'` — 动态（事件研究）聚合、`'group'` — 按组聚合、`'calendar'` — 按日历时间聚合 |

> **boot_type** options: `'multiplier'`
> 📝 ***boot_type** 选项：`'multiplier'`（乘数自举法）*

> **type** options: `'simple'`, `'dynamic'`, `'group'`, `'calendar'`
> 📝 ***type** 选项：`'simple'`（简单聚合）、`'dynamic'`（动态/事件研究聚合）、`'group'`（按组聚合）、`'calendar'`（按日历时间聚合）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.aggte(result="value")
print(result.summary())
```

> 📁 See also: `did_mpdta.py`, `docs/guides/callaway_santanna.md`, `docs/guides/cross_engine_validation.md`
> 📝 *另请参阅：`did_mpdta.py`、`docs/guides/callaway_santanna.md`、`docs/guides/cross_engine_validation.md`*

---
### `sp.bacon_decomposition()`

**Goodman-Bacon (2021) decomposition of the TWFE DiD coefficient into a weighted sum of underlying 2x2 DID comparisons: treated-vs-never, treated-vs-notyet, earlier-vs-later. Diagnoses when TWFE is contaminated by already-treated units acting as controls. Validation: certified parity evidence.**
> 📝 ***Goodman-Bacon（2021）将 TWFE DID 系数分解为底层 2x2 DID 比较的加权和：处理组 vs 从未处理组、处理组 vs 尚未处理组、早期处理组 vs 后期处理组。用于诊断 TWFE 何时被已处理单元充当控制组所污染。验证状态：已认证一致性证据。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. | 单元、受试者或面板标识符列。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | Time-varying binary treatment indicator | 时变二元处理指示变量 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.bacon_decomposition(y="outcome", data=df, treat="value", time="value", id="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/migration-from-r.md`, `docs/guides/mixtape_ch09_did.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/migration-from-r.md`、`docs/guides/mixtape_ch09_did.md`*

---
### `sp.bacon_plot()`

**Scatter plot of Goodman-Bacon decomposition.**
> 📝 ***Goodman-Bacon 分解的散点图。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `bacon_result` | `object` | ✓ |  | Output from ``bacon_decomposition()``. Must contain ``'decomposition'`` DataFrame and ``'beta_twfe'``. | ``bacon_decomposition()`` 的输出结果。必须包含 ``'decomposition'`` 数据框和 ``'beta_twfe'``。 |
| `colors` | `object` |  |  | Map comparison type -> color. Defaults provided. | 比较类型到颜色的映射。提供默认值。 |
| `figsize` | `array[string]` |  | `[10, 6]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，指定图形大小）。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.bacon_plot()
print(result.summary())
```

> 📁 See also: `docs/guides/mixtape_ch09_did.md`
> 📝 *另请参阅：`docs/guides/mixtape_ch09_did.md`*

---
### `sp.bjs()`

**Borusyak, Jaravel & Spiess (2024) imputation DID estimator.**
> 📝 ***Borusyak, Jaravel & Spiess（2024）插补法 DID 估计器。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. | 置信区间的显著性水平。 |
| `boot_seed` | `integer` |  | `0` | Seed for the cluster bootstrap (deterministic results). | 聚类自举的种子（用于可复现结果）。 |
| `cluster` | `string` |  |  | Variable for cluster-robust standard errors. Defaults to ``group`` (unit-level clustering). | 聚类稳健标准误的变量。默认为 ``group``（单元级聚类）。 |
| `controls` | `array[string]` |  |  | Additional control covariates. | 额外的控制协变量。 |
| `data` | `string` | ✓ |  | Panel data in long format. | 长格式面板数据。 |
| `first_treat` | `string` | ✓ |  | Column indicating the period of first treatment. Use ``np.inf``, ``np.nan``, or ``0`` for never-treated units. | 指示首次处理时期的列。对从未处理的单元使用 ``np.inf``、``np.nan`` 或 ``0``。 |
| `group` | `string` | ✓ |  | Unit identifier column. | 单元标识符列。 |
| `horizon` | `array[string]` |  |  | Relative time periods for event study estimates, e.g. ``list(range(-5, 6))``. If ``None``, reports only the overall ATT (no event study disaggregation). | 事件研究估计的相对时期，例如 ``list(range(-5, 6))``。如果为 ``None``，仅报告总体 ATT（不进行事件研究细分）。 |
| `n_boot` | `integer` |  | `199` | Number of cluster-bootstrap replications when ``vce='bootstrap'``. | 当 ``vce='bootstrap'`` 时的聚类自举重复次数。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `vce` | `string (enum)` |  | `'analytic'` | Standard-error mode for the overall ATT. ``'analytic'`` uses the influence-function cluster SE (fast) but under-counts the variance from estimating the unit/time fixed effects and is **anti-conservative** (~0.87 coverage at a nominal 95% level); a ``UserWarning`` recommends ``'bootstrap'``. ``'bootstrap'`` resamples whole clusters and re-runs the full imputation estimator. Point estimates are identical either way; per-horizon event-study SEs are unaffected. | 总体 ATT 的标准误模式。``'analytic'`` 使用影响函数聚类标准误（快速）但低估了估计单元/时间固定效应带来的方差，是**反保守**的（名义 95% 水平下覆盖率约为 0.87）；会发出 ``UserWarning`` 建议使用 ``'bootstrap'``。``'bootstrap'`` 对整个聚类重采样并重新运行完整插补估计器。两种方式的点估计完全相同；各期事件研究标准误不受影响。可选值：`'analytic'` — 解析法、`'bootstrap'` — 自举法 |
| `y` | `string` | ✓ |  | Outcome variable name. | 结果变量名称。 |

> **vce** options: `'analytic'`, `'bootstrap'`
> 📝 ***vce** 选项：`'analytic'`（解析法）、`'bootstrap'`（自举法）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.bjs(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mixtape_ch09_did.md`
> 📝 *另请参阅：`docs/guides/mixtape_ch09_did.md`*

---
### `sp.bjs_pretrend_joint()`

**Cluster-bootstrap joint Wald test for BJS pre-treatment coefficients.**
> 📝 ***对 BJS 处理前系数的聚类自举联合 Wald 检验。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `controls` | `array[string]` |  |  | Control-variable column names. | 控制变量列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `first_treat` | `string` | ✓ |  | first_treat parameter (str). | first_treat 参数（字符串）。 |
| `group` | `string` | ✓ |  | Group or cohort identifier. | 组或队列标识符。 |
| `horizon` | `array[string]` |  |  | If omitted, inferred from ``result.model_info['event_study']``. | 如果省略，从 ``result.model_info['event_study']`` 推断。 |
| `n_boot` | `integer` |  | `300` | Cluster-bootstrap replications. Clusters are sampled with replacement; unit ids are reassigned in the resampled frame so BJS refits cleanly. | 聚类自举重复次数。聚类采用有放回抽样；在重采样样本中重新分配单元 ID，以便 BJS 干净地重新拟合。 |
| `result` | `string` | ✓ |  | Output of :func:`did_imputation` on ``data`` with a non-trivial ``horizon`` that covers negative values. Only its ``model_info['event_study']`` frame is consulted, to look up the observed pre-period point estimates that we re-test with a covariance-aware statistic. Same arguments you passed to the original :func:`did_imputation` call. Needed to re-run BJS on each cluster-bootstrap resample. | :func:`did_imputation` 在 ``data`` 上使用包含负值的非平凡 ``horizon`` 的输出结果。仅查阅其 ``model_info['event_study']`` 数据框，以查找观测到的处理前时期点估计，我们使用协方差感知统计量对其重新检验。需要传递与原始 :func:`did_imputation` 调用相同的参数，以便在每个聚类自举重采样样本上重新运行 BJS。 |
| `seed` | `integer` |  |  | RNG seed for reproducibility. | 随机数生成器种子，用于可复现性。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.bjs_pretrend_joint(y="outcome", data=df, result="value", group="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/robustness_workflow.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/robustness_workflow.md`*

---
### `sp.borusyak_jaravel_spiess()`

**Borusyak, Jaravel & Spiess (2024) imputation DID estimator.**
> 📝 ***Borusyak, Jaravel & Spiess（2024）插补法 DID 估计器。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. | 置信区间的显著性水平。 |
| `boot_seed` | `integer` |  | `0` | Seed for the cluster bootstrap (deterministic results). | 聚类自举的种子（用于可复现结果）。 |
| `cluster` | `string` |  |  | Variable for cluster-robust standard errors. Defaults to ``group`` (unit-level clustering). | 聚类稳健标准误的变量。默认为 ``group``（单元级聚类）。 |
| `controls` | `array[string]` |  |  | Additional control covariates. | 额外的控制协变量。 |
| `data` | `string` | ✓ |  | Panel data in long format. | 长格式面板数据。 |
| `first_treat` | `string` | ✓ |  | Column indicating the period of first treatment. Use ``np.inf``, ``np.nan``, or ``0`` for never-treated units. | 指示首次处理时期的列。对从未处理的单元使用 ``np.inf``、``np.nan`` 或 ``0``。 |
| `group` | `string` | ✓ |  | Unit identifier column. | 单元标识符列。 |
| `horizon` | `array[string]` |  |  | Relative time periods for event study estimates, e.g. ``list(range(-5, 6))``. If ``None``, reports only the overall ATT (no event study disaggregation). | 事件研究估计的相对时期，例如 ``list(range(-5, 6))``。如果为 ``None``，仅报告总体 ATT（不进行事件研究细分）。 |
| `n_boot` | `integer` |  | `199` | Number of cluster-bootstrap replications when ``vce='bootstrap'``. | 当 ``vce='bootstrap'`` 时的聚类自举重复次数。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `vce` | `string (enum)` |  | `'analytic'` | Standard-error mode for the overall ATT. ``'analytic'`` uses the influence-function cluster SE (fast) but under-counts the variance from estimating the unit/time fixed effects and is **anti-conservative** (~0.87 coverage at a nominal 95% level); a ``UserWarning`` recommends ``'bootstrap'``. ``'bootstrap'`` resamples whole clusters and re-runs the full imputation estimator. Point estimates are identical either way; per-horizon event-study SEs are unaffected. | 总体 ATT 的标准误模式。``'analytic'`` 使用影响函数聚类标准误（快速）但低估了估计单元/时间固定效应带来的方差，是**反保守**的（名义 95% 水平下覆盖率约为 0.87）；会发出 ``UserWarning`` 建议使用 ``'bootstrap'``。``'bootstrap'`` 对整个聚类重采样并重新运行完整插补估计器。两种方式的点估计完全相同；各期事件研究标准误不受影响。可选值：`'analytic'` — 解析法、`'bootstrap'` — 自举法 |
| `y` | `string` | ✓ |  | Outcome variable name. | 结果变量名称。 |

> **vce** options: `'analytic'`, `'bootstrap'`
> 📝 ***vce** 选项：`'analytic'`（解析法）、`'bootstrap'`（自举法）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.borusyak_jaravel_spiess(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

---
### `sp.breakdown_m()`

**Compute the breakdown value of M. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 ***计算 M 的崩溃值（breakdown value）。验证状态：已验证证据层（已知真实值、参考实现、外部一致性或蒙特卡洛模拟验证）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `e` | `integer` |  | `0` | Relative time period. | 相对时期。 |
| `method` | `string` |  | `'smoothness'` | Estimator or algorithm variant to use. | 所使用的估计器或算法变体。 |
| `result` | `string` | ✓ |  | DID result with event study. | 包含事件研究的 DID 结果。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.breakdown_m(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/callaway_santanna.md`, `docs/guides/honest_did.md`, `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/callaway_santanna.md`、`docs/guides/honest_did.md`、`docs/guides/migration-from-r.md`*

---
### `sp.callaway_santanna()`

**Callaway-Sant'Anna (2021) staggered DID with group-time ATTs. Robust to heterogeneous treatment effects and staggered adoption. Validation: certified evidence with scoped limitations. Known limitations: panel=False (repeated cross-sections) currently requires estimator='reg' and control_group='nevertreated'; the IPW and DR variants for RCS are planned for a future release.**
> 📝 ***Callaway-Sant'Anna（2021）交错处理时点 DID，含组-时 ATT。对异质性处理效应和交错采纳具有稳健性。验证状态：已认证证据，有限制说明。已知限制：panel=False（重复截面数据 / Repeated Cross-Sections，RCS）当前要求 estimator='reg' 且 control_group='nevertreated'；RCS 的 IPW（逆概率加权）和 DR（双重稳健）变体计划在未来版本中发布。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `anticipation` | `integer` |  | `0` | Number of anticipation periods | 预期效应期数 |
| `base_period` | `string (enum)` |  | `'universal'` | Base period | 基期，可选值：`'universal'` — 通用基期、`'varying'` — 可变基期 |
| `control_group` | `string (enum)` |  | `'nevertreated'` | Control group | 控制组，可选值：`'nevertreated'` — 从未处理组、`'notyettreated'` — 尚未处理组 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `estimator` | `string (enum)` |  | `'dr'` | 2x2 estimator | 2x2 估计器，可选值：`'dr'` — 双重稳健（Doubly Robust）、`'ipw'` — 逆概率加权（Inverse Probability Weighting）、`'reg'` — 回归（Regression） |
| `g` | `string` | ✓ |  | First-treatment-period column (0 = never-treated) | 首次处理时期列（0 = 从未处理） |
| `i` | `string` | ✓ |  | Unit identifier | 单元标识符 |
| `panel` | `boolean` |  | `True` | False means repeated cross-sections | False 表示重复截面数据 |
| `t` | `string` | ✓ |  | Time period column | 时间周期列 |
| `x` | `array[string]` |  |  | Covariates for conditional parallel trends | 条件平行趋势假设的协变量 |
| `y` | `string` | ✓ |  | Outcome variable | 结果变量 |

> **base_period** options: `'universal'`, `'varying'`
> 📝 ***base_period** 选项：`'universal'`（通用基期）、`'varying'`（可变基期）*

> **control_group** options: `'nevertreated'`, `'notyettreated'`
> 📝 ***control_group** 选项：`'nevertreated'`（从未处理组）、`'notyettreated'`（尚未处理组）*

> **estimator** options: `'dr'`, `'ipw'`, `'reg'`
> 📝 ***estimator** 选项：`'dr'`（双重稳健）、`'ipw'`（逆概率加权）、`'reg'`（回归）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.callaway_santanna(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df, g="value", t="value", i="value")
print(result.summary())
```

> 📁 See also: `did_mpdta.py`, `docs/guides/agent_api.md`, `docs/guides/callaway_santanna.md`
> 📝 *另请参阅：`did_mpdta.py`、`docs/guides/agent_api.md`、`docs/guides/callaway_santanna.md`*

---
### `sp.cic()`

**Changes-in-Changes (Athey & Imbens 2006). Nonparametric quantile DiD that identifies the full counterfactual outcome distribution for treated units, not just the mean. Reports quantile treatment effects (QTE) via empirical-CDF transformation; bootstrap SE.**
> 📝 ***变化中的变化法 / Changes-in-Changes（Athey & Imbens 2006）。非参数分位数 DID，识别处理组完整的反事实结果分布，而不仅仅是均值。通过经验累积分布函数（CDF）变换报告分位数处理效应（Quantile Treatment Effect，QTE）；自举标准误。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `group` | `string` | ✓ |  | Treatment-group indicator (0/1) | 处理组指示变量（0/1） |
| `n_boot` | `integer` |  | `500` | Number of bootstrap replications. | 自举重复次数。 |
| `n_grid` | `integer` |  | `200` | Grid size for inverse-CDF mapping | 逆累积分布函数映射的网格大小 |
| `quantiles` | `array[string]` |  |  | Quantile grid (default: deciles) | 分位数网格（默认：十分位数） |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. | 随机种子，用于可复现的随机步骤。 |
| `time` | `string` | ✓ |  | Period indicator (0=pre, 1=post) | 时期指示变量（0=处理前，1=处理后） |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.cic(y="outcome", data=df, group="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/migration-from-r.md`, `docs/guides/qte_family.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/migration-from-r.md`、`docs/guides/qte_family.md`*

---
### `sp.cohort_anchored_event_study()`

**Cohort-anchored event study. Instead of averaging across cohorts at each relative-time bin (which can contaminate leads / lags with other cohorts' dynamics), estimates separate event-study paths per cohort and then aggregates with cohort weights. Successor to the Rambachan-Roth sensitivity-friendly specification.**
> 📝 ***队列锚定事件研究。不在每个相对时间区间内跨队列取平均（这可能使超前/滞后项被其他队列的动态所污染），而是为每个队列估计独立的事件研究路径，然后用队列权重进行聚合。是 Rambachan-Roth 敏感性友好型设定的后继方案。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. | 单元、受试者或面板标识符列。 |
| `lags` | `integer` |  | `4` | lags parameter (int). | lags 参数（整数，滞后项期数）。 |
| `leads` | `integer` |  | `4` | leads parameter (int). | leads 参数（整数，超前项期数）。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. | 处理指示变量或首次处理周期列。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.cohort_anchored_event_study(y="outcome", data=df, treat="value", time="value", id="value")
print(result.summary())
```

---
### `sp.cohort_event_study_plot()`

**Per-cohort event study plot (overlay).**
> 📝 ***逐队列事件研究图（叠加显示）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `aggregate_color` | `string` |  | `'#2C3E50'` | Color for aggregate line. | 聚合线的颜色。 |
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `ci` | `boolean` |  | `True` | Show confidence intervals for each cohort. | 显示每个队列的置信区间。 |
| `ci_alpha` | `number` |  | `0.08` | CI band transparency. | 置信区间带的透明度。 |
| `figsize` | `array[string]` |  | `[12, 7]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，图形大小）。 |
| `palette` | `array[string]` |  |  | Colors for each cohort. Auto-generated if None. | 每个队列的颜色。如果为 None 则自动生成。 |
| `result` | `string` | ✓ |  | Result from ``callaway_santanna()`` or ``did(method='cs')``. Must have ``detail`` with 'group', 'relative_time', 'att' columns, and ``model_info['event_study']`` for aggregate. | ``callaway_santanna()`` 或 ``did(method='cs')`` 的结果。必须包含带有 'group'、'relative_time'、'att' 列的 ``detail``，以及用于聚合的 ``model_info['event_study']``。 |
| `show_aggregate` | `boolean` |  | `True` | Overlay the aggregate event study line. | 叠加显示聚合事件研究线。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.cohort_event_study_plot(result="value")
print(result.summary())
```

---
### `sp.continuous_did()`

**DiD with continuous treatment intensity. Four modes: (i) 'twfe' TWFE with dosexpost interaction; (ii) 'att_gt' dose-quantile group-time ATT versus the untreated (dose=0) arm with bootstrap SE (heuristic); (iii) 'dose_response' local-linear regression of DeltaY=Y_post-Y_pre on baseline dose; (iv) 'cgs' Callaway-Goodman-Bacon-Sant'Anna (2024) ATT(d|g,t) MVP -- 2-period design, OR only, bootstrap SE, [pending verification] markers on paper formulas. Full CGS parity (cohort aggregation, DR/IPW, analytical IF variance) is on the roadmap -- see docs/rfc/continuous_did_cgs.md. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact). Known limitations: method='cgs' is an MVP -- 2-period design, OR only, bootstrap SE; full CGS parity (cohort aggregation, DR/IPW, analytical IF variance) is on the roadmap (see docs/rfc/continuous_did_cgs.md). Other modes (twfe / att_gt / dose_response) are stable.**
> 📝 ***连续处理强度的 DID。四种模式：(i) 'twfe'：带剂量×时期交互项的 TWFE；(ii) 'att_gt'：剂量分位数组-时 ATT，与未处理（剂量=0）组比较，使用自举标准误（启发式）；(iii) 'dose_response'：ΔY=Y_post-Y_pre 对基线剂量的局部线性回归；(iv) 'cgs'：Callaway-Goodman-Bacon-Sant'Anna（2024）ATT(d|g,t) 最小可行产品（MVP）— 两期设计，仅 OR（结果回归），自举标准误，[待验证] 论文公式标记。完整 CGS 一致性（队列聚合、DR/IPW、解析影响函数方差）在路线图中 — 参见 docs/rfc/continuous_did_cgs.md。验证状态：已验证证据层（已知真实值、参考实现、外部一致性或蒙特卡洛模拟验证）。已知限制：method='cgs' 是最小可行产品 — 两期设计，仅 OR，自举标准误；完整 CGS 一致性（队列聚合、DR/IPW、解析 IF 方差）在路线图中（参见 docs/rfc/continuous_did_cgs.md）。其他模式（twfe / att_gt / dose_response）是稳定的。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster variable for SE (TWFE mode) | 标准误的聚类变量（TWFE 模式） |
| `controls` | `array[string]` |  |  | Control variables | 控制变量 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `dose` | `string` | ✓ |  | Continuous treatment / dose variable | 连续处理/剂量变量 |
| `id` | `string` | ✓ |  | Unit identifier | 单元标识符 |
| `method` | `string (enum)` |  | `'att_gt'` | Estimation mode | 估计模式，可选值：`'att_gt'` — 剂量分位数组-时 ATT、`'twfe'` — 双向固定效应、`'dose_response'` — 剂量响应曲线、`'cgs'` — Callaway-Goodman-Bacon-Sant'Anna 方法 |
| `n_boot` | `integer` |  | `500` | Bootstrap replications for SE | 标准误计算的自举重复次数 |
| `n_quantiles` | `integer` |  | `5` | Number of dose quantiles for discretisation | 离散化所用的剂量分位数个数 |
| `post` | `string` |  |  | Binary post-treatment indicator (inferred from t_pre / t_post if omitted) | 二元处理后指示变量（如果省略则从 t_pre / t_post 推断） |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. | 随机种子，用于可复现的随机步骤。 |
| `t_post` | `integer` |  |  | First post-treatment period | 第一个处理后时期 |
| `t_pre` | `integer` |  |  | Last pre-treatment period | 最后一个处理前时期 |
| `time` | `string` | ✓ |  | Time period column | 时间周期列 |
| `y` | `string` | ✓ |  | Outcome variable | 结果变量 |

> **method** options: `'att_gt'`, `'twfe'`, `'dose_response'`, `'cgs'`
> 📝 ***method** 选项：`'att_gt'`（剂量分位数组-时 ATT）、`'twfe'`（双向固定效应）、`'dose_response'`（剂量响应曲线）、`'cgs'`（Callaway-Goodman-Bacon-Sant'Anna 方法）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.continuous_did(y="outcome", data=df, dose="value", time="value", id="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/migration-from-r.md`*

---
### `sp.cs_report()`

**One-call staggered-DID workflow: estimate -> aggregate -> sensitivity.**
> 📝 ***一站式交错 DID 工作流：估计 → 聚合 → 敏感性分析。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `anticipation` | `integer` |  | `0` | anticipation parameter (int). | anticipation 参数（整数，预期效应期数）。 |
| `control_group` | `string (enum)` |  | `'nevertreated'` | control_group parameter (str). | control_group 参数（字符串），可选值：`'nevertreated'` — 从未处理组、`'notyettreated'` — 尚未处理组 |
| `data_or_result` | `string` | ✓ |  | Either a long-format panel (then ``y, g, t, i`` are required and :func:`callaway_santanna` is run first), or an already-fitted :func:`callaway_santanna` result. | 可以是长格式面板数据（此时需要 ``y, g, t, i`` 参数，且会先运行 :func:`callaway_santanna`），或者是已经拟合好的 :func:`callaway_santanna` 结果。 |
| `estimator` | `string (enum)` |  | `'dr'` | estimator parameter (str). | estimator 参数（字符串），可选值：`'dr'` — 双重稳健、`'ipw'` — 逆概率加权、`'reg'` — 回归 |
| `g` | `string` |  |  | Outcome / cohort / time / unit id columns (required when ``data_or_result`` is a DataFrame). | 结果/队列/时间/单元 ID 列（当 ``data_or_result`` 是数据框时必需）。 |
| `i` | `string` |  |  | Outcome / cohort / time / unit id columns (required when ``data_or_result`` is a DataFrame). | 结果/队列/时间/单元 ID 列（当 ``data_or_result`` 是数据框时必需）。 |
| `max_e` | `number` |  | `inf` | Event-time window passed to the dynamic aggregation. | 传递给动态聚合的事件时间窗口上限。 |
| `min_e` | `number` |  | `-inf` | Event-time window passed to the dynamic aggregation. | 传递给动态聚合的事件时间窗口下限。 |
| `n_boot` | `integer` |  | `1000` | Multiplier-bootstrap replications for :func:`aggte`. | :func:`aggte` 的乘数自举重复次数。 |
| `random_state` | `integer` |  | `0` | Seed for the bootstrap (set to ``None`` for non-reproducibility). | 自举种子（设为 ``None`` 则结果不可复现）。 |
| `rr_method` | `string (enum)` |  | `'smoothness'` | Sensitivity restriction handed to :func:`breakdown_m`. | 传递给 :func:`breakdown_m` 的敏感性限制方法，可选值：`'smoothness'` — 平滑性、`'relative_magnitude'` — 相对幅度 |
| `save_to` | `string` |  |  | When set, treats the value as a *path prefix* and writes the report in every supported format in one call: - ``<prefix>.txt`` -- fixed-width plain-text report - ``<prefix>.md`` -- GitHub-flavoured Markdown - ``<prefix>.tex`` -- booktabs LaTeX fragment - ``<prefix>.xlsx`` -- multi-sheet workbook - ``<prefix>.png`` -- 2x2 summary figure (only if matplotlib is installed; silently skipped otherwise) Missing parent directories are created on the fly. | 设置后，将该值视为*路径前缀*，一次调用即可写出所有支持格式的报告：- ``<prefix>.txt`` — 定宽纯文本报告 - ``<prefix>.md`` — GitHub 风格 Markdown - ``<prefix>.tex`` — booktabs LaTeX 片段 - ``<prefix>.xlsx`` — 多工作表工作簿 - ``<prefix>.png`` — 2x2 汇总图（仅当安装了 matplotlib 时；否则静默跳过）缺失的父目录会自动创建。 |
| `t` | `string` |  |  | Outcome / cohort / time / unit id columns (required when ``data_or_result`` is a DataFrame). | 结果/队列/时间/单元 ID 列（当 ``data_or_result`` 是数据框时必需）。 |
| `verbose` | `boolean` |  | `True` | If ``True``, print the report before returning. | 如果为 ``True``，在返回前打印报告。 |
| `x` | `array[string]` |  |  | Covariates for conditional parallel trends. | 条件平行趋势假设的协变量。 |
| `y` | `string` |  |  | Outcome / cohort / time / unit id columns (required when ``data_or_result`` is a DataFrame). | 结果/队列/时间/单元 ID 列（当 ``data_or_result`` 是数据框时必需）。 |

> **control_group** options: `'nevertreated'`, `'notyettreated'`
> 📝 ***control_group** 选项：`'nevertreated'`（从未处理组）、`'notyettreated'`（尚未处理组）*

> **estimator** options: `'dr'`, `'ipw'`, `'reg'`
> 📝 ***estimator** 选项：`'dr'`（双重稳健）、`'ipw'`（逆概率加权）、`'reg'`（回归）*

> **rr_method** options: `'smoothness'`, `'relative_magnitude'`
> 📝 ***rr_method** 选项：`'smoothness'`（平滑性）、`'relative_magnitude'`（相对幅度）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.cs_report(y="outcome", x=["treatment", "covariate1", "covariate2"], data_or_result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/callaway_santanna.md`, `docs/guides/cs_report.md`, `docs/guides/honest_did.md`
> 📝 *另请参阅：`docs/guides/callaway_santanna.md`、`docs/guides/cs_report.md`、`docs/guides/honest_did.md`*

---
### `sp.ddd()`

**Triple Differences (DDD) estimator. Adds a within-treatment-group subgroup that is unaffected by treatment as an additional control dimension, relaxing parallel trends from 'same trend across groups' to 'same differential trend across subgroups within groups'.**
> 📝 ***三重差分法（DDD）估计器。引入处理组内部不受处理影响的子群作为额外的控制维度，将平行趋势假设从「跨组相同趋势」放松到「组内子群间相同差异趋势」。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. | 协变量矩阵、数据框或列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `robust` | `boolean` |  | `True` | Robust standard-error or covariance estimator option. | 稳健标准误或协方差估计器选项。 |
| `subgroup` | `string` | ✓ |  | Within-group subgroup (1=affected, 0=not) | 组内子群指示变量（1=受影响，0=不受影响） |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | Primary treatment indicator | 主要处理指示变量 |
| `weights` | `string` |  |  | Observation weights. | 观测权重。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.ddd(y="outcome", data=df, treat="value", time="value", subgroup="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/migration-from-r.md`*

---
### `sp.design_robust_event_study()`

**Design-robust event study with explicit negative-weight diagnostics per cohort x relative-time cell. Reports which event-study coefficients receive negative weights in TWFE and flags the affected horizons.**
> 📝 ***设计稳健的事件研究，含显式的每个队列×相对时间单元格的负权重诊断。报告哪些事件研究系数在 TWFE 中获得负权重，并标记受影响的时间区间。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. | 单元、受试者或面板标识符列。 |
| `lags` | `integer` |  | `4` | lags parameter (int). | lags 参数（整数，滞后项期数）。 |
| `leads` | `integer` |  | `4` | leads parameter (int). | leads 参数（整数，超前项期数）。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. | 处理指示变量或首次处理周期列。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.design_robust_event_study(y="outcome", data=df, treat="value", time="value", id="value")
print(result.summary())
```

---
### `sp.did_2stage()`

**Gardner (2021) two-stage DID estimator.**
> 📝 ***Gardner（2021）两阶段 DID 估计器。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Two-sided CI level. | 双侧置信区间水平。 |
| `boot_seed` | `integer` |  | `0` | Seed for the cluster bootstrap (deterministic results). | 聚类自举种子（结果可复现）。 |
| `cluster` | `string` |  |  | Cluster variable for Stage-2 SEs. Defaults to ``group``. | 第二阶段标准误的聚类变量。默认为 ``group``。 |
| `controls` | `array[string]` |  |  | Additional covariates included in both stages. | 两个阶段都包含的额外协变量。 |
| `data` | `string` | ✓ |  | Long-format panel. | 长格式面板数据。 |
| `event_study` | `boolean` |  | `False` | If True, Stage 2 reports coefficients by relative time ``k = t - first_treat_i``. | 如果为 True，第二阶段按相对时间 ``k = t - first_treat_i`` 报告系数。 |
| `first_treat` | `string` | ✓ |  | First-treatment-period column. Never-treated units should be encoded as ``0``, ``NaN``, or ``+inf``. | 首次处理时期列。从未处理的单元应编码为 ``0``、``NaN`` 或 ``+inf``。 |
| `group` | `string` | ✓ |  | Unit (panel-id) column. | 单元（面板 ID）列。 |
| `horizon` | `array[string]` |  |  | Relative-time leads/lags to report when ``event_study=True``; defaults to ``range(-5, 6)`` intersected with available support. | 当 ``event_study=True`` 时报告的相对时间超前/滞后项；默认为 ``range(-5, 6)`` 与可用支持集的交集。 |
| `n_boot` | `integer` |  | `199` | Number of cluster-bootstrap replications when ``vce='bootstrap'``. | 当 ``vce='bootstrap'`` 时的聚类自举重复次数。 |
| `time` | `string` | ✓ |  | Time column. | 时间列。 |
| `vce` | `string (enum)` |  | `'analytic'` | Standard-error mode. ``'analytic'`` clusters the Stage-2 residuals (fast) but ignores the variance from estimating the Stage-1 fixed effects and is **anti-conservative** (empirically ~0.78 coverage at a nominal 95% level); a ``UserWarning`` recommends ``'bootstrap'``. ``'bootstrap'`` resamples whole clusters and re-runs the full two-step procedure (Gardner 2021 / ``did2s``), substantially improving coverage (~0.90 vs ~0.78 in simulations; it approaches nominal as the number of clusters grows). Point estimates are identical either way. | 标准误模式。``'analytic'`` 对第二阶段残差进行聚类（快速）但忽略了估计第一阶段固定效应带来的方差，是**反保守**的（名义 95% 水平下经验覆盖率约为 0.78）；会发出 ``UserWarning`` 建议使用 ``'bootstrap'``。``'bootstrap'`` 对整个聚类重采样并重新运行完整两步程序（Gardner 2021 / ``did2s``），显著改善覆盖率（模拟中约 0.90 对比 0.78；随着聚类数量增加趋近名义水平）。两种方式点估计完全相同。可选值：`'analytic'` — 解析法、`'bootstrap'` — 自举法 |
| `y` | `string` | ✓ |  | Outcome column name. | 结果列名。 |

> **vce** options: `'analytic'`, `'bootstrap'`
> 📝 ***vce** 选项：`'analytic'`（解析法）、`'bootstrap'`（自举法）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_2stage(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

---
### `sp.did_2x2()`

**Canonical 2x2 DID: two groups (treated / control) x two periods (pre / post). Point estimate via either group-means differencing or OLS on the treat x post interaction; optional covariates, robust / cluster SE, and sample weights.**
> 📝 ***经典 2x2 DID：两组（处理组/控制组）× 两期（事前/事后）。点估计通过组均值差分或对处理×事后交互项的 OLS 回归得到；可选协变量、稳健/聚类标准误和样本权重。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Column for cluster-robust SE (defaults to treat) | 聚类稳健标准误的列（默认为 treat） |
| `covariates` | `array[string]` |  |  | Covariates included additively; for DR use sp.drdid | 以加法形式包含的协变量；双重稳健估计请使用 sp.drdid |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `robust` | `boolean` |  | `True` | Heteroskedasticity-robust SE when no cluster provided | 当未提供聚类变量时使用异方差稳健标准误 |
| `time` | `string` | ✓ |  | Time / period indicator | 时间/时期指示变量 |
| `treat` | `string` | ✓ |  | Binary treatment-group indicator (0/1) | 二元处理组指示变量（0/1） |
| `weights` | `string` |  |  | Optional column name for sampling weights | 可选的抽样权重列名 |
| `y` | `string` | ✓ |  | Outcome variable | 结果变量 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_2x2(y="outcome", data=df, treat="value", time="value")
print(result.summary())
```

---
### `sp.did_analysis()`

**Workflow wrapper that runs a full DiD pipeline: auto-detects 2x2 vs. staggered, runs the right estimator (CS by default), optionally runs Bacon decomposition, event study, and Rambachan-Roth sensitivity, and aggregates into a DIDAnalysis report object.**
> 📝 ***运行完整 DID 流程的工作流包装器：自动检测 2x2 vs 交错设计，运行合适的估计器（默认 CS），可选运行 Bacon 分解、事件研究和 Rambachan-Roth 敏感性分析，并汇总为 DIDAnalysis 报告对象。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. | 单元、受试者或面板标识符列。 |
| `method` | `string (enum)` |  | `'auto'` | Estimator selection | 估计器选择，可选值：`'auto'` — 自动选择、`'2x2'` — 经典 2x2 DID、`'cs'` — Callaway-Sant'Anna、`'sa'` — Sun-Abraham、`'sdid'` — 合成 DID |
| `run_bacon` | `boolean` |  | `True` | run_bacon parameter (bool). | run_bacon 参数（布尔值，是否运行 Bacon 分解）。 |
| `run_event_study` | `boolean` |  | `True` | run_event_study parameter (bool). | run_event_study 参数（布尔值，是否运行事件研究）。 |
| `run_sensitivity` | `boolean` |  | `True` | run_sensitivity parameter (bool). | run_sensitivity 参数（布尔值，是否运行敏感性分析）。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | Binary treatment or first-treat column | 二元处理变量或首次处理时期列 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

> **method** options: `'auto'`, `'2x2'`, `'cs'`, `'sa'`, `'sdid'`
> 📝 ***method** 选项：`'auto'`（自动选择）、`'2x2'`（经典 2x2 DID）、`'cs'`（Callaway-Sant'Anna）、`'sa'`（Sun-Abraham）、`'sdid'`（合成 DID）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_analysis(y="outcome", data=df, treat="value", time="value", id="value")
print(result.summary())
```

---
### `sp.did_bcf()`

**Bayesian Causal Forests DiD. Fits a BART-style ensemble with treatment and prognostic terms on the DiD residuals, providing heterogeneous treatment-effect posterior draws per unit. Useful for machine-learning DiD with covariates.**
> 📝 ***贝叶斯因果森林（Bayesian Causal Forests，BCF）DID。在 DID 残差上拟合带处理项和预后项的 BART（Bayesian Additive Regression Trees）风格集成模型，为每个单元提供异质性处理效应的后验抽样。适用于带协变量的机器学习 DID。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. | 协变量矩阵、数据框或列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. | 单元、受试者或面板标识符列。 |
| `n_trees` | `integer` |  | `50` | Number of trees. | 树的数量。 |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. | 随机种子，用于可复现的随机步骤。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | Treatment indicator or first-treatment-period column. | 处理指示变量或首次处理周期列。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_bcf(y="outcome", data=df, treat="value", time="value", id="value")
print(result.summary())
```

---
### `sp.did_imputation()`

**Borusyak-Jaravel-Spiess (2024) imputation DiD. Fits a TWFE model on untreated observations only, imputes counterfactual Y(0) for treated obs, and averages the imputation residuals. Efficient under no-anticipation + parallel trends; analytical SE via bjs_inference. Validation: certified evidence with scoped limitations. Known limitations: R/Stata parity is for the documented untreated-only TWFE and simple ATT aggregation convention only; event-study and SE rows are backend-specific diagnostics.**
> 📝 ***Borusyak-Jaravel-Spiess（2024）插补法 DID。仅在未处理观测上拟合 TWFE 模型，为处理观测插补反事实 Y(0)，并对插补残差取平均。在无预期效应+平行趋势下是有效的；通过 bjs_inference 获得解析标准误。验证状态：已认证证据，有限制说明。已知限制：R/Stata 一致性仅针对已文档化的仅未处理 TWFE 和简单 ATT 聚合约定；事件研究和 SE 行是后端特定诊断。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `controls` | `array[string]` |  |  | Control-variable column names. | 控制变量列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `first_treat` | `string` | ✓ |  | First-treatment period; 0 = never-treated | 首次处理时期；0 = 从未处理 |
| `group` | `string` | ✓ |  | Unit identifier | 单元标识符 |
| `horizon` | `array[string]` |  |  | Relative-time leads / lags (default: all available) | 相对时间超前/滞后项（默认：所有可用项） |
| `time` | `string` | ✓ |  | Time period column | 时间周期列 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_imputation(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/migration-from-r.md`*

---
### `sp.did_misclassified()`

**Staggered DiD robust to treatment-timing misclassification and anticipation. Adjusts the CS-style aggregation for a user-supplied misclassification probability pi_misclass and a known anticipation horizon. Use when first-treat dates are noisy (e.g., survey-reported).**
> 📝 ***对处理时点误分类和预期效应具有稳健性的交错 DID。根据用户提供的误分类概率 pi_misclass 和已知预期效应期限调整 CS 风格的聚合。当首次处理日期存在噪声时使用（例如，调查自报数据）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `anticipation_periods` | `integer` |  | `0` | anticipation_periods parameter (int). | anticipation_periods 参数（整数，预期效应期数）。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `id` | `string` | ✓ |  | Unit, subject, or panel identifier column. | 单元、受试者或面板标识符列。 |
| `pi_misclass` | `number` |  | `0.0` | P(observed treat != true treat) -- between 0 and 1 | P(观测处理 != 真实处理) — 介于 0 和 1 之间 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | First-treatment period (possibly noisy) | 首次处理时期（可能存在噪声） |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_misclassified(y="outcome", data=df, treat="value", time="value", id="value")
print(result.summary())
```

---
### `sp.did_multiplegt()`

**de Chaisemartin & D'Haultfuille (2020) DID_M estimator. Weighted average of consecutive-period DID cells where treatment 'switchers' are compared to 'stayers'. Handles treatments that switch on AND off (unlike Callaway-Sant'Anna which assumes staggered adoption). Supports placebo lags, dynamic horizons, cluster bootstrap SE, joint placebo test and average-cumulative-effect summary from dCDH (2024). The heteroskedastic-weights variant and full dCDH (2024) intertemporal event-study (did_multiplegt_dyn Stata) are on the roadmap -- see docs/rfc/multiplegt_dyn.md. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 ***de Chaisemartin & D'Haultfuille（2020）DID_M 估计器。对相邻时期 DID 单元格的加权平均，其中处理「切换者」与「保持者」进行比较。能够处理开启和关闭的处理状态（不同于假设交错采纳的 Callaway-Sant'Anna）。支持安慰剂滞后期、动态区间、聚类自举标准误、联合安慰剂检验以及 dCDH（2024）的平均累积效应汇总。异方差权重变体和完整 dCDH（2024）跨期事件研究（did_multiplegt_dyn Stata）在路线图中 — 参见 docs/rfc/multiplegt_dyn.md。验证状态：已验证证据层（已知真实值、参考实现、外部一致性或蒙特卡洛模拟验证）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster variable for bootstrap (defaults to group) | 自举的聚类变量（默认为 group） |
| `controls` | `array[string]` |  |  | Controls residualised via first differences | 通过一阶差分残差化的控制变量 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `dynamic` | `integer` |  | `0` | Number of post-treatment dynamic horizons | 处理后动态区间数量 |
| `group` | `string` | ✓ |  | Unit identifier | 单元标识符 |
| `n_boot` | `integer` |  | `100` | Cluster-bootstrap replications | 聚类自举重复次数 |
| `placebo` | `integer` |  | `0` | Number of pre-treatment placebo lags | 处理前安慰剂滞后项数量 |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. | 随机种子，用于可复现的随机步骤。 |
| `time` | `string` | ✓ |  | Time period column | 时间周期列 |
| `treatment` | `string` | ✓ |  | Binary current-treatment indicator (may switch on and off) | 二元当期处理指示变量（可开启和关闭） |
| `y` | `string` | ✓ |  | Outcome variable | 结果变量 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_multiplegt(y="outcome", data=df, group="value", time="value", treatment="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/migration-from-r.md`*

---
### `sp.did_plot()`

**Classic DID diagram showing treatment effect with counterfactual.**
> 📝 ***展示处理效应及反事实的经典 DID 图示。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `annotate_effect` | `boolean` |  | `True` | Annotate the treatment effect arrow on the plot. | 在图上标注处理效应箭头。 |
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `colors` | `array[string]` |  |  | (treatment, control, counterfactual) colors. | （处理组、控制组、反事实）颜色。 |
| `data` | `string` | ✓ |  | Input dataset. | 输入数据集。 |
| `figsize` | `array[string]` |  | `[10, 6]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，图形大小）。 |
| `labels` | `object` |  |  | Custom labels: ``{'treat': ..., 'control': ..., 'counterfactual': ...}``. | 自定义标签：``{'treat': ..., 'control': ..., 'counterfactual': ...}``。 |
| `show_counterfactual` | `boolean` |  | `True` | Draw the dashed counterfactual line. | 绘制反事实虚线。 |
| `time` | `string` | ✓ |  | Time period variable. | 时间周期变量。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |
| `treat` | `string` | ✓ |  | Binary treatment group indicator (0/1). | 二元处理组指示变量（0/1）。 |
| `treat_time` | `integer` |  |  | Treatment onset time. If None, inferred as the midpoint. | 处理开始时间。如果为 None，推断为中点。 |
| `y` | `string` | ✓ |  | Outcome variable. | 结果变量。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_plot(y="outcome", data=df, time="value", treat="value")
print(result.summary())
```

---
### `sp.did_report()`

**DID report bundle: fits selected methods and writes report artifacts.**
> 📝 ***DID 报告包：拟合所选方法并写入报告产物。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `cluster` | `string` |  |  | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `controls` | `array[string]` |  |  | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `data` | `string` | ✓ |  | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `first_treat` | `string` | ✓ |  | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `group` | `string` | ✓ |  | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `include_sensitivity` | `boolean` |  | `True` | Whether to run Rambachan-Roth breakdown M*. Defaults to ``True`` in ``did_report`` (vs ``False`` in ``did_summary``) because a report is expected to be comprehensive. | 是否运行 Rambachan-Roth 崩溃值 M* 分析。``did_report`` 中默认为 ``True``（``did_summary`` 中为 ``False``），因为报告预期应当全面。 |
| `methods` | `array[string]` |  | `'auto'` | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `plot_sort_by` | `string` |  | `'estimate'` | Sort the forest plot by estimate ascending. | 森林图按估计值升序排序。 |
| `save_to` | `string` | ✓ |  | Directory path. Created if it does not exist. | 目录路径。如果不存在则创建。 |
| `time` | `string` | ✓ |  | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |
| `verbose` | `boolean` |  | `False` | Print progress lines. | 打印进度信息。 |
| `y` | `string` | ✓ |  | Same as :func:`did_summary`. | 同 :func:`did_summary`。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_report(y="outcome", data=df, time="value", first_treat="value", group="value", save_to="value")
print(result.summary())
```

---
### `sp.did_summary()`

**One-call method-robustness comparison for staggered DID.**
> 📝 ***一站式交错 DID 方法稳健性比较。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. | 置信区间的显著性水平。 |
| `cluster` | `string` |  |  | Cluster variable for SE (defaults to ``group`` in each sub-method). | 标准误的聚类变量（每个子方法中默认为 ``group``）。 |
| `controls` | `array[string]` |  |  | Time-varying covariates passed to methods that support them. | 传递给支持协变量的方法的时变协变量。 |
| `data` | `string` | ✓ |  | Panel dataset (long format). | 面板数据集（长格式）。 |
| `first_treat` | `string` | ✓ |  | First-treatment period per unit; NaN (or 0) for never-treated. | 每个单元的首次处理时期；从未处理单元为 NaN（或 0）。 |
| `group` | `string` | ✓ |  | Unit identifier. | 单元标识符。 |
| `include_sensitivity` | `boolean` |  | `False` | If ``True`` and ``'cs'`` is among the methods fit, compute the Rambachan-Roth (2023) *breakdown M\** -- the largest relative violation of parallel trends under which the treatment effect is still significantly different from zero. The value is added to ``model_info['breakdown_m']`` and to the ``breakdown_m`` column of ``detail`` (CS row only; other methods leave ``NaN``). | 如果为 ``True`` 且拟合方法中包含 ``'cs'``，计算 Rambachan-Roth（2023）*崩溃值 M\** — 平行趋势被违反的最大相对幅度，在此幅度下处理效应仍显著异于零。该值添加到 ``model_info['breakdown_m']`` 和 ``detail`` 的 ``breakdown_m`` 列中（仅 CS 行；其他方法留空为 ``NaN``）。 |
| `methods` | `array[string]` |  | `'auto'` | Methods to run. Valid keys: ``'cs'``, ``'sa'``, ``'bjs'``, ``'etwfe'``, ``'stacked'``, or ``'all'`` / ``'auto'`` for all. | 要运行的方法。有效键：``'cs'``（Callaway-Sant'Anna）、``'sa'``（Sun-Abraham）、``'bjs'``（Borusyak-Jaravel-Spiess）、``'etwfe'`（扩展 TWFE）、``'stacked'`（堆叠 DID），或 ``'all'`` / ``'auto'`` 表示全部。 |
| `time` | `string` | ✓ |  | Time / period variable (integer-valued). | 时间/时期变量（整数值）。 |
| `verbose` | `boolean` |  | `False` | Print progress for each method. | 打印每个方法的进度信息。 |
| `y` | `string` | ✓ |  | Outcome variable. | 结果变量。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_summary(y="outcome", data=df, time="value", first_treat="value", group="value")
print(result.summary())
```

---
### `sp.did_summary_plot()`

**Forest plot of DID method-robustness summary.**
> 📝 ***DID 方法稳健性汇总的森林图。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `ax` | `string` |  |  | Existing axes to draw on. If ``None`` a new figure is created. | 用于绘图的现有坐标轴。如果为 ``None`` 则创建新图形。 |
| `color` | `string` |  | `'#2C3E50'` | Color for point estimates and CIs. | 点估计和置信区间的颜色。 |
| `figsize` | `array[string]` |  | `[9, 5]` | Figure size when creating a new figure. | 创建新图形时的图形大小。 |
| `highlight_color` | `string` |  | `'#C0392B'` | Color for the cross-method mean line. | 跨方法均值线的颜色。 |
| `reference` | `number` |  |  | Horizontal reference value (e.g. 0 for 'no effect'). Defaults to ``0``. | 水平参考值（例如 0 表示「无效应」）。默认为 ``0``。 |
| `result` | `string` | ✓ |  | Output of :func:`did_summary`. Must have a ``detail`` DataFrame with columns ``estimate``, ``ci_low``, ``ci_high``, and either ``method`` or ``estimator``. | :func:`did_summary` 的输出。必须具有包含 ``estimate``、``ci_low``、``ci_high`` 列以及 ``method`` 或 ``estimator`` 列的 ``detail`` 数据框。 |
| `sort_by` | `string` |  |  | If ``'estimate'``, sort methods by point estimate ascending. Otherwise keep the order in ``result.detail``. | 如果为 ``'estimate'``，按点估计升序排列方法。否则保持 ``result.detail`` 中的顺序。 |
| `title` | `string` |  |  | Plot title. Defaults to ``"DID Method-Robustness Summary"``. | 图形标题。默认为 ``"DID Method-Robustness Summary"``（DID 方法稳健性汇总）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_summary_plot(result="value")
print(result.summary())
```

---
### `sp.did_summary_to_latex()`

**Render a :func:`did_summary` result as a LaTeX**
> 📝 ***将 :func:`did_summary` 结果渲染为 LaTeX 表格。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `caption` | `string` |  | `'DID method-robustness summary.'` | LaTeX caption. | LaTeX 标题。 |
| `digits` | `integer` |  | `4` | Decimal precision. | 小数精度。 |
| `include_breakdown` | `boolean` |  | `True` | Include the Rambachan-Roth breakdown M* column when sensitivity was requested. | 请求敏感性分析时包含 Rambachan-Roth 崩溃值 M* 列。 |
| `include_ci` | `boolean` |  | `True` | Include the 95 % CI column. | 包含 95% 置信区间列。 |
| `label` | `string` |  | `'tab:did_summary'` | LaTeX label for the table. | 表格的 LaTeX 标签。 |
| `result` | `string` | ✓ |  | Output of :func:`did_summary`. | :func:`did_summary` 的输出。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_summary_to_latex(result="value")
print(result.summary())
```

---
### `sp.did_summary_to_markdown()`

**Render a :func:`did_summary` result as a GitHub-Flavoured Markdown table.**
> 📝 ***将 :func:`did_summary` 结果渲染为 GitHub-Flavoured Markdown 表格。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `digits` | `integer` |  | `4` | Decimal precision for numeric columns. | 数值列的小数精度。 |
| `include_breakdown` | `boolean` |  | `True` | Include the Rambachan-Roth breakdown M* column (CS row only, blank for others). Ignored if sensitivity was not requested. | 包含 Rambachan-Roth 崩溃值 M* 列（仅 CS 行，其他行为空）。如果未请求敏感性分析则忽略。 |
| `include_ci` | `boolean` |  | `True` | Include the 95 % CI column. | 包含 95% 置信区间列。 |
| `result` | `string` | ✓ |  | Output of :func:`did_summary`. | :func:`did_summary` 的输出。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.did_summary_to_markdown(result="value")
print(result.summary())
```

---
### `sp.dl_propensity_score()`

**Neural-net propensity score estimator (arXiv:2404.04794, 2024).**
> 📝 ***神经网络倾向得分估计器（arXiv:2404.04794，2024）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `covariates` | `array[string]` | ✓ |  | Covariate matrix, DataFrame, or column names. | 协变量矩阵、数据框或列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `hidden_sizes` | `array[string]` |  |  | hidden_sizes parameter (list). | hidden_sizes 参数（列表，隐藏层大小）。 |
| `treatment` | `string` | ✓ |  | Treatment indicator, treatment variable, or treatment array. | 处理指示变量、处理变量或处理数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.dl_propensity_score(data=df, treatment="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.drdid()`

**Doubly-robust DiD (Sant'Anna & Zhao 2020). Combines outcome regression with IPW; consistent if either model is correct. Primary estimator for 2x2 DiD with covariates. Validation: certified parity evidence.**
> 📝 ***双重稳健 DID（Sant'Anna & Zhao 2020）。结合结果回归与 IPW（逆概率加权，Inverse Probability Weighting）；只要其中一个模型正确，估计就是一致的。带协变量的 2x2 DID 的主要估计器。验证状态：已认证一致性证据。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `covariates` | `array[string]` |  |  | Covariates X | 协变量 X |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `group` | `string` | ✓ |  | Unit-level treatment indicator (0/1) | 单元级处理指示变量（0/1） |
| `id` | `string` |  |  | Unit identifier for true two-period panel DR-DID | 真正两期面板 DR-DID 的单元标识符 |
| `method` | `string (enum)` |  | `'imp'` | Estimation method: 'imp' (improved, locally efficient) or 'trad' | 估计方法：'imp'（改进的、局部有效）或 'trad'（传统），可选值：`'imp'` — 改进局部有效法、`'trad'` — 传统法 |
| `n_boot` | `integer` |  |  | Bootstrap replications (None -> analytical SE) | 自举重复次数（None 表示使用解析标准误） |
| `seed` | `integer` |  |  | Random seed for reproducible stochastic steps. | 随机种子，用于可复现的随机步骤。 |
| `time` | `string` | ✓ |  | Time period column | 时间周期列 |
| `y` | `string` | ✓ |  | Outcome variable | 结果变量 |

> **method** options: `'imp'`, `'trad'`
> 📝 ***method** 选项：`'imp'`（改进的局部有效法）、`'trad'`（传统法）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.drdid(y="outcome", data=df, group="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`*

---
### `sp.enhanced_event_study_plot()`

**Enhanced event study plot with pre/post shading and significance coloring.**
> 📝 ***增强型事件研究图，含事前/事后阴影和显著性着色。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha_level` | `number` |  | `0.05` | alpha_level parameter (float). | alpha_level 参数（浮点数，显著性水平）。 |
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `ci_alpha` | `number` |  | `0.15` | Confidence band transparency. | 置信带透明度。 |
| `color` | `string` |  | `'#2C3E50'` | Default color for estimates. | 估计值的默认颜色。 |
| `figsize` | `array[string]` |  | `[10, 6]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，图形大小）。 |
| `marker` | `string` |  | `'o'` | marker parameter (str). | marker 参数（字符串，标记样式）。 |
| `markersize` | `integer` |  | `6` | markersize parameter (int). | markersize 参数（整数，标记大小）。 |
| `post_color` | `string` |  | `'#FDEDEC'` | Post-treatment shading color. | 处理后区域阴影颜色。 |
| `pre_color` | `string` |  | `'#EBF5FB'` | Pre-treatment shading color. | 处理前区域阴影颜色。 |
| `result` | `string` | ✓ |  | DID result with event study in ``model_info['event_study']``. | 在 ``model_info['event_study']`` 中包含事件研究的 DID 结果。 |
| `shade_post` | `boolean` |  | `True` | Shade post-treatment region. | 为处理后区域添加阴影。 |
| `shade_pre` | `boolean` |  | `True` | Shade pre-treatment region. | 为处理前区域添加阴影。 |
| `show_zero` | `boolean` |  | `True` | Show horizontal zero line. | 显示水平零线。 |
| `sig_color` | `string` |  | `'#E74C3C'` | Color for significant estimates. None disables coloring. | 显著估计值的颜色。None 表示不着色。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.enhanced_event_study_plot(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mixtape_ch09_did.md`
> 📝 *另请参阅：`docs/guides/mixtape_ch09_did.md`*

---
### `sp.etwfe()`

**Extended Two-Way Fixed Effects (Wooldridge 2021). Explicit API mirroring the R etwfe package. The headline reports the treated-observation-weighted simple ATT from etwfe::emfx(type='simple') / Stata jwdid, with cgroup selecting not-yet-treated or never-treated controls. Known limitations: cgroup='nevertreated' combined with panel=False (repeated cross-sections) is not yet supported; pass either panel=True with cgroup='nevertreated' or panel=False with cgroup='notyet'; cgroup='nevertreated' combined with panel=False (repeated cross-sections) is not yet supported. Use panel=True with cgroup='nevertreated' or panel=False with cgroup='notyet'.**
> 📝 ***扩展双向固定效应 / Extended Two-Way Fixed Effects（Wooldridge 2021）。显式 API 镜像 R 的 etwfe 包。主要报告 etwfe::emfx(type='simple') / Stata jwdid 中以处理观测加权的简单 ATT，通过 cgroup 选择尚未处理或从未处理的控制组。已知限制：cgroup='nevertreated' 与 panel=False（重复截面数据）的组合尚不支持；请使用 panel=True 配合 cgroup='nevertreated'，或 panel=False 配合 cgroup='notyet'。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cgroup` | `string (enum)` |  | `'notyet'` | Control group: 'notyet' (not-yet-treated) or 'nevertreated'. The latter is only supported when panel=True. | 控制组：'notyet'（尚未处理）或 'nevertreated'（从未处理）。后者仅在 panel=True 时支持，可选值：`'notyet'` — 尚未处理组、`'nevertreated'` — 从未处理组 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `controls` | `array[string]` |  |  | Control-variable column names. | 控制变量列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `first_treat` | `string` | ✓ |  | first_treat parameter (str). | first_treat 参数（字符串，首次处理时期）。 |
| `group` | `string` | ✓ |  | Group or cohort identifier. | 组或队列标识符。 |
| `panel` | `boolean` |  | `True` | If False, treat data as repeated cross-section | 如果为 False，将数据视为重复截面 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `xvar` | `array[string]` |  |  | R-style alias for controls | controls 的 R 风格别名 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

> **cgroup** options: `'notyet'`, `'nevertreated'`
> 📝 ***cgroup** 选项：`'notyet'`（尚未处理组）、`'nevertreated'`（从未处理组）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.etwfe(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/migration-from-r.md`*

---
### `sp.etwfe_emfx()`

**R ``etwfe::emfx``-style aggregated marginal effects for an ETWFE fit. Validation: certified parity evidence.**
> 📝 ***ETWFE 拟合的 R ``etwfe::emfx`` 风格聚合边际效应。验证状态：已认证一致性证据。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. | 置信区间的显著性水平。 |
| `include_leads` | `boolean` |  | `False` | For ``type='event'`` and ``type='calendar'``, whether to include pre-treatment relative times (``rel_time < 0``) in the output. These coefficients identify pre-trends and are informative for parallel-trends inspection. Default ``False`` for backward compatibility with earlier versions; set ``True`` for full event-study output matching the R ``etwfe::emfx(type='event')`` default. ``rel_time = -1`` is always the reference category and is excluded. | 对于 ``type='event'`` 和 ``type='calendar'``，是否在输出中包含处理前相对时期（``rel_time < 0``）。这些系数识别事前趋势，对平行趋势检验很有用。默认 ``False`` 是为了与早期版本向后兼容；设置为 ``True`` 可获得匹配 R ``etwfe::emfx(type='event')`` 默认值的完整事件研究输出。``rel_time = -1`` 始终是参考类别，会被排除。 |
| `result` | `string` | ✓ |  | Output of :func:`etwfe` or :func:`wooldridge_did`. | :func:`etwfe` 或 :func:`wooldridge_did` 的输出。 |
| `type` | `string (enum)` |  | `'simple'` | Aggregation type. | 聚合类型，可选值：`'simple'` — 简单 ATT、`'group'` — 按组聚合、`'event'` — 事件研究、`'calendar'` — 按日历时间聚合 |
| `weighting` | `string (enum)` |  | `'treated'` | Aggregation weights for cohort-level marginal effects. ``'treated'`` uses the number of treated post-period observations, matching R ``etwfe::emfx(type='simple')`` and Stata ``jwdid, estat simple``. ``'cohort'`` preserves the historical StatsPAI cohort-share weighting. | 队列级边际效应的聚合权重。``'treated'`` 使用处理后观测数量，匹配 R ``etwfe::emfx(type='simple')`` 和 Stata ``jwdid, estat simple``。``'cohort'`` 保留 StatsPAI 历史队列份额加权，可选值：`'cohort'` — 队列份额加权、`'treated'` — 处理观测数量加权 |

> **type** options: `'simple'`, `'group'`, `'event'`, `'calendar'`
> 📝 ***type** 选项：`'simple'`（简单 ATT）、`'group'`（按组聚合）、`'event'`（事件研究）、`'calendar'`（按日历时间聚合）*

> **weighting** options: `'cohort'`, `'treated'`
> 📝 ***weighting** 选项：`'cohort'`（队列份额加权）、`'treated'`（处理观测数量加权）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.etwfe_emfx(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/stability.md`
> 📝 *另请参阅：`docs/guides/stability.md`*

---
### `sp.event_study()`

**Traditional OLS event-study with entity and time FEs. Generates relative-time dummies around the treatment date, omits a reference period, and estimates via TWFE + optional clustered SE. Exposed for users who want the classical specification alongside CS / SA / BJS; not robust to staggered-effect heterogeneity -- use sp.sun_abraham for that.**
> 📝 ***传统 OLS 事件研究，含个体和时间固定效应（Fixed Effects，FE）。在事件日期周围生成相对时间虚拟变量，省略参考期，通过 TWFE + 可选聚类标准误进行估计。为想要经典设定（与 CS/SA/BJS 并列）的用户开放；不对交错效应异质性具有稳健性 — 请使用 sp.sun_abraham。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. | 协变量矩阵、数据框或列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `ref_period` | `integer` |  | `-1` | Reference relative-time period to omit | 要省略的参考相对时期 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat_time` | `string` | ✓ |  | First-treatment period column | 首次处理时期列 |
| `unit` | `string` | ✓ |  | Unit identifier | 单元标识符 |
| `window` | `array[string]` |  | `[-4, 4]` | (lead, lag) horizons | （超前、滞后）时间窗口 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.event_study(y="outcome", data=df, treat_time="value", time="value", unit="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`*

---
### `sp.gardner_did()`

**Gardner (2021) two-stage DID. Stage-1 fits two-way FEs on untreated observations; Stage-2 regresses the residualised outcome on treatment dummies (ATT or event study). Numerically close to Borusyak-Jaravel-Spiess imputation with unit-clustered SEs. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 ***Gardner（2021）两阶段 DID。第一阶段在未处理观测上拟合双向固定效应；第二阶段将残差化的结果对处理虚拟变量回归（ATT 或事件研究）。数值上接近 Borusyak-Jaravel-Spiess 插补法配合单元聚类标准误。验证状态：已验证证据层（已知真实值、参考实现、外部一致性或蒙特卡洛模拟验证）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster variable for Stage-2 SEs (defaults to group) | 第二阶段标准误的聚类变量（默认为 group）。 |
| `controls` | `array[string]` |  |  | Additional covariates | 额外协变量。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `event_study` | `boolean` |  | `False` | If True, report coefficients by relative time k = t - first_treat | 如果为 True，按相对时间 k = t - first_treat 报告系数。 |
| `first_treat` | `string` | ✓ |  | First-treatment-period column; 0/NaN/inf = never treated | 首次处理时期列；0/NaN/inf = 从未处理。 |
| `group` | `string` | ✓ |  | Unit/panel-id column | 单元/面板 ID 列。 |
| `horizon` | `array[string]` |  |  | Relative-time leads/lags to report (default range(-5, 6)) | 要报告的相对时间超前/滞后项（默认为 range(-5, 6)）。 |
| `time` | `string` | ✓ |  | Time column | 时间列。 |
| `y` | `string` | ✓ |  | Outcome column | 结果列。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.gardner_did(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/v1_2_frontier.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/v1_2_frontier.md`*

---
### `sp.ggdid()`

**Plot an ``aggte()`` result, mirroring R :func:`did::ggdid`.**
> 📝 ***绘制 ``aggte()`` 结果，镜像 R :func:`did::ggdid`。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `band_color` | `string` |  | `'#F18F01'` | Colours for the pointwise estimate and the uniform band. | 点态估计和一致置信带的颜色。 |
| `figsize` | `array[string]` |  | `[10, 6]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，图形大小）。 |
| `point_color` | `string` |  | `'#2E86AB'` | Colours for the pointwise estimate and the uniform band. | 点态估计和一致置信带的颜色。 |
| `result` | `string` | ✓ |  | Output of :func:`aggte`. | :func:`aggte` 的输出结果。 |
| `show_pointwise` | `boolean` |  | `True` | Draw pointwise CI lines. | 绘制点态置信区间线。 |
| `show_uniform` | `boolean` |  | `True` | Draw uniform band (shaded region). | 绘制一致置信带（阴影区域）。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.ggdid(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/migration-from-r.md`*

---
### `sp.group_time_plot()`

**Plot group-time ATT estimates from Callaway-Sant'Anna.**
> 📝 ***绘制 Callaway-Sant'Anna 的组-时 ATT 估计。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha_level` | `number` |  | `0.05` | Significance threshold. | 显著性阈值。 |
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `color` | `string` |  | `'#2C3E50'` | Default color for dot plot. | 点图的默认颜色。 |
| `figsize` | `array[string]` |  | `[12, 7]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，图形大小）。 |
| `insig_color` | `string` |  | `'#BDC3C7'` | Color for insignificant estimates. | 不显著估计值的颜色。 |
| `plot_type` | `string` |  | `'dot'` | 'dot' or 'heatmap'. | 绘图类型：'dot'（点图）或 'heatmap'（热图）。 |
| `result` | `string` | ✓ |  | Result from ``callaway_santanna()`` or ``did(method='cs')``. Must have ``detail`` DataFrame with 'group', 'time', 'att' columns. | ``callaway_santanna()`` 或 ``did(method='cs')`` 的结果。必须具有包含 'group'、'time'、'att' 列的 ``detail`` 数据框。 |
| `sig_color` | `string` |  | `'#E74C3C'` | Color for significant estimates. | 显著估计值的颜色。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.group_time_plot(result="value")
print(result.summary())
```

---
### `sp.harvest_did()`

**Harvest every valid 2x2 DID comparison from a staggered panel and aggregate them via precision-weighted / simple / cohort-weighted averages. Agnostic to cohort structure; useful for robustness comparisons against CS / SA / BJS.**
> 📝 ***从交错面板中提取所有有效的 2x2 DID 比较，并通过精度加权/简单/队列加权平均进行聚合。与队列结构无关；适用于与 CS/SA/BJS 的稳健性对比。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cohort` | `string` |  |  | First-treat cohort column (for static harvesting) | 首次处理队列列（用于静态提取）。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `horizons` | `array[string]` |  |  | horizons parameter (list). | horizons 参数（列表，时间窗口）。 |
| `never_value` | `string` |  | `0` | never_value parameter. | never_value 参数（表示从未处理的值）。 |
| `outcome` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |
| `reference` | `integer` |  | `-1` | Pre-treatment reference horizon relative to each cohort | 相对于每个队列的处理前参考窗口。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` |  |  | Time-varying treat indicator (for dynamic harvesting) | 时变处理指示变量（用于动态提取）。 |
| `unit` | `string` | ✓ |  | Unit identifier column. | 单元标识符列。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.harvest_did(data=df, unit="value", time="value", outcome="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/harvest_did.md`, `docs/guides/v1_2_frontier.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/harvest_did.md`、`docs/guides/v1_2_frontier.md`*

---
### `sp.honest_did()`

**Rambachan & Roth (2023) sensitivity analysis for parallel trends. Validation: certified parity evidence.**
> 📝 ***Rambachan & Roth（2023）平行趋势敏感性分析。验证状态：已认证一致性证据。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level. | 显著性水平。 |
| `backend` | `string (enum)` |  | `'native'` | ``'native'`` uses StatsPAI's dependency-light analytic intervals. ``'honestdid'``/``'r'`` delegates to the R ``HonestDiD`` package through ``Rscript`` and returns the reference package's finite-sample conditional intervals. The R backend is mainly useful when exact parity with ``HonestDiD::createSensitivityResults_relativeMagnitudes`` is required; the default native path remains available without an R installation. | ``'native'`` 使用 StatsPAI 轻依赖解析区间。``'honestdid'``/``'r'`` 通过 ``Rscript`` 委托给 R ``HonestDiD`` 包，返回参考包的有限样本条件区间。R 后端主要在需要与 ``HonestDiD::createSensitivityResults_relativeMagnitudes`` 精确一致时有用；默认原生路径无需安装 R 即可使用，可选值：`'native'` — 原生实现、`'honestdid'`/`'r'` — R HonestDiD 包 |
| `e` | `integer` |  | `0` | Relative time period for which to compute robust CIs. 0 = on-impact effect, 1 = one period after, etc. | 计算稳健置信区间的相对时期。0 = 即时效应，1 = 之后一期，等等。 |
| `honestdid_method` | `string (enum)` |  |  | Solver method passed to the R ``HonestDiD`` backend. The default preserves HonestDiD defaults: ``'C-LF'`` for ``method='relative_magnitude'`` and ``'FLCI'`` for ``method='smoothness'``. Ignored by ``backend='native'``. | 传递给 R ``HonestDiD`` 后端的求解方法。默认保留 HonestDiD 默认值：``method='relative_magnitude'`` 时为 ``'C-LF'``，``method='smoothness'`` 时为 ``'FLCI'``。``backend='native'`` 时忽略，可选值：`'C-LF'`、`'Conditional'`、`'FLCI'`、`'C-F'` |
| `m_grid` | `array[string]` |  |  | Grid of M values (maximum violation magnitude) to evaluate. | 要评估的 M 值（最大违背幅度）网格。 |
| `method` | `string` |  | `'smoothness'` | Type of restriction on violations: - ``'smoothness'``: \|Deltadelta_t\| <= M (bounded change in violation) - ``'relative_magnitude'``: \|delta_post\| <= M x max\|delta_pre\| | 违背类型限制：- ``'smoothness'``：\|Δδ_t\| ≤ M（违背的变化有界）- ``'relative_magnitude'``：\|δ_post\| ≤ M × max\|δ_pre\|（相对幅度限制） |
| `result` | `string` | ✓ |  | A fitted DID result that contains event study estimates in ``result.model_info['event_study']``. | 在 ``result.model_info['event_study']`` 中包含事件研究估计的已拟合 DID 结果。 |

> **backend** options: `'native'`, `'honestdid'`, `'r'`
> 📝 ***backend** 选项：`'native'`（原生实现）、`'honestdid'`/`'r'`（R HonestDiD 包）*

> **honestdid_method** options: `'C-LF'`, `'Conditional'`, `'FLCI'`, `'C-F'`
> 📝 ***honestdid_method** 选项：`'C-LF'`、`'Conditional'`、`'FLCI'`、`'C-F'`（求解方法）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.honest_did(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`, `docs/guides/callaway_santanna.md`, `docs/guides/choosing_did_estimator.md`
> 📝 *另请参阅：`docs/guides/agent_api.md`、`docs/guides/callaway_santanna.md`、`docs/guides/choosing_did_estimator.md`*

---
### `sp.overlap_weighted_did()`

**Overlap-weighted 2x2 DiD. Weights observations by e(X)(1-e(X)), where e(X) is the estimated propensity score, placing highest weight on units with the most overlap between treated and control covariate distributions. Useful when overlap is poor at the tails.**
> 📝 ***重叠加权的 2x2 DID。以 e(X)(1-e(X)) 为权重对观测进行加权，其中 e(X) 是估计的倾向得分（Propensity Score），对处理组和控制组协变量分布重叠最大的单元赋予最高权重。适用于尾部重叠较差的情况。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `covariates` | `array[string]` | ✓ |  | Covariates X | 协变量 X。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `ps_model` | `string (enum)` |  | `'logit'` | Propensity score model | 倾向得分模型，可选值：`'logit'` — Logit 回归、`'rf'` — 随机森林、`'gbm'` — 梯度提升机、`'dl'` — 深度学习 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `treat` | `string` | ✓ |  | Binary treatment indicator | 二元处理指示变量。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

> **ps_model** options: `'logit'`, `'rf'`, `'gbm'`, `'dl'`
> 📝 ***ps_model** 选项：`'logit'`（Logit 回归）、`'rf'`（随机森林）、`'gbm'`（梯度提升机）、`'dl'`（深度学习）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.overlap_weighted_did(y="outcome", data=df, treat="value", time="value", covariates=["a", "b"])
print(result.summary())
```

---
### `sp.panel()`

**Unified panel regression: FE, RE, between, FD, pooled OLS, two-way FE, Mundlak/Chamberlain CRE, Arellano-Bond, Blundell-Bond system GMM. Results include built-in diagnostics: .hausman_test(), .bp_lm_test(), .f_test_effects(), .pesaran_cd_test(), .compare(method). Validation: certified parity evidence.**
> 📝 ***统一面板回归：固定效应（FE）、随机效应（RE）、组间（between）、一阶差分（FD）、混合 OLS、双向固定效应（two-way FE）、Mundlak/Chamberlain 相关随机效应（CRE）、Arellano-Bond、Blundell-Bond 系统 GMM。结果包含内置诊断：.hausman_test()、.bp_lm_test()、.f_test_effects()、.pesaran_cd_test()、.compare(method)。验证状态：已认证一致性证据。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `cluster` | `string` |  |  | Cluster variable: entity, time, or twoway | 聚类变量：个体、时间或双向聚类。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `entity` | `string` | ✓ |  | Unit identifier column | 单元标识符列。 |
| `formula` | `string` | ✓ |  | Regression formula: 'y ~ x1 + x2' | 回归公式：'y ~ x1 + x2'。 |
| `gmm_lags` | `string` |  | `'(2, 5)'` | GMM instrument lag range | GMM 工具变量滞后范围。 |
| `lags` | `integer` |  | `1` | AR lags for dynamic panel (ab/system) | 动态面板（ab/system）的 AR 滞后阶数。 |
| `method` | `string (enum)` |  | `'fe'` | Estimation method | 估计方法，可选值：`'fe'` — 固定效应、`'re'` — 随机效应、`'be'` — 组间估计、`'fd'` — 一阶差分、`'pooled'` — 混合 OLS、`'twoway'` — 双向固定效应、`'mundlak'` — Mundlak 方法、`'cre'` — 相关随机效应、`'chamberlain'` — Chamberlain 方法、`'ab'` — Arellano-Bond、`'system'` — Blundell-Bond 系统 GMM |
| `robust` | `string` |  | `'nonrobust'` | Standard errors: nonrobust, robust, kernel, driscoll-kraay | 标准误：非稳健、稳健、核、Driscoll-Kraay。 |
| `time` | `string` | ✓ |  | Time column | 时间列。 |
| `twostep` | `boolean` |  | `False` | Two-step GMM | 两步 GMM 估计。 |

> **method** options: `'fe'`, `'re'`, `'be'`, `'fd'`, `'pooled'`, `'twoway'`, `'mundlak'`, `'cre'`, `'chamberlain'`, `'ab'`, `'system'`
> 📝 ***method** 选项：`'fe'`（固定效应）、`'re'`（随机效应）、`'be'`（组间估计）、`'fd'`（一阶差分）、`'pooled'`（混合 OLS）、`'twoway'`（双向固定效应）、`'mundlak'`（Mundlak 方法）、`'cre'`（相关随机效应）、`'chamberlain'`（Chamberlain 方法）、`'ab'`（Arellano-Bond）、`'system'`（Blundell-Bond 系统 GMM）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.panel(formula="lwage ~ x1 + x2", data=df, entity="value", time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/grammar.md`, `docs/guides/mixtape_ch09_did.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/grammar.md`、`docs/guides/mixtape_ch09_did.md`*

---
### `sp.parallel_trends_plot()`

**Plot raw outcome means over time for treatment and control groups.**
> 📝 ***绘制处理组和控制组原始结果均值的时间趋势图。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `agg` | `string` |  | `'mean'` | Aggregation function: 'mean' or 'median'. | 聚合函数：'mean'（均值）或 'median'（中位数）。 |
| `ax` | `string` |  |  | Existing axes to plot on. | 用于绘图的现有坐标轴。 |
| `ci` | `boolean` |  | `True` | Show 95% confidence intervals (+/-1.96 SE of mean). | 显示 95% 置信区间（均值标准误的 ±1.96 倍）。 |
| `colors` | `array[string]` |  |  | Colors for (treatment, control). Default: ('#E74C3C', '#2C3E50'). | （处理组、控制组）颜色。默认：('#E74C3C', '#2C3E50')。 |
| `data` | `string` | ✓ |  | Input dataset. | 输入数据集。 |
| `figsize` | `array[string]` |  | `[10, 6]` | Figure size. | 图形大小。 |
| `id` | `string` |  |  | Unit identifier (for panel data). | 单元标识符（用于面板数据）。 |
| `labels` | `object` |  |  | Custom labels, e.g. ``{'treat': 'New Jersey', 'control': 'Pennsylvania'}``. | 自定义标签，例如 ``{'treat': '新泽西州', 'control': '宾夕法尼亚州'}``。 |
| `time` | `string` | ✓ |  | Time period variable. | 时间周期变量。 |
| `title` | `string` |  |  | Plot title. | 图形标题。 |
| `treat` | `string` | ✓ |  | Treatment group indicator. Binary (0/1) for 2x2, or first-treatment-period for staggered (0 = never treated). | 处理组指示变量。2x2 设计为二元变量（0/1），交错设计为首次处理时期（0 = 从未处理）。 |
| `treat_time` | `integer` |  |  | Treatment onset time. Draws a vertical line if provided. | 处理开始时间。如果提供则绘制垂直线。 |
| `y` | `string` | ✓ |  | Outcome variable. | 结果变量。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.parallel_trends_plot(y="outcome", data=df, time="value", treat="value")
print(result.summary())
```

---
### `sp.pretrends_power()`

**Power of the pre-trend test against a hypothesised violation.**
> 📝 ***针对假设违背的前趋势检验的检验功效（Power）。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level of the pre-trend test. | 前趋势检验的显著性水平。 |
| `delta` | `string` |  |  | Hypothesised trend violation in the pre-period (length = number of pre-periods). Default: linear trend ``delta[k] = (k+1) * min(\|SE\|)`` -- a violation equal to one SE at the furthest lag, declining linearly to near-zero. | 事前时期的假设趋势违背（长度 = 事前时期数量）。默认：线性趋势 ``delta[k] = (k+1) * min(|SE|)`` — 在最远滞后项处等于一个标准误的违背，线性下降至接近零。 |
| `result` | `string` | ✓ |  | Event-study result with pre-treatment estimates and SEs. | 包含处理前估计和标准误的事件研究结果。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.pretrends_power(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`, `docs/guides/sensitivity_analysis.md`
> 📝 *另请参阅：`docs/guides/migration-from-r.md`、`docs/guides/sensitivity_analysis.md`*

---
### `sp.pretrends_summary()`

**Print a combined pre-trends diagnostic report.**
> 📝 ***打印综合前趋势诊断报告。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level. | 显著性水平。 |
| `delta` | `string` |  |  | Passed to ``pretrends_power``. | 传递给 ``pretrends_power``。 |
| `result` | `string` | ✓ |  | Event-study result. | 事件研究结果。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.pretrends_summary(result="value")
print(result.summary())
```

---
### `sp.pretrends_test()`

**Joint Wald test of pre-treatment ATTs (or event-study leads) against zero -- the canonical sanity check for the parallel-trends assumption in DiD designs. Failing to reject is necessary but not sufficient evidence for parallel trends; always pair with sp.honest_did / sp.sensitivity_rr for design-robust inference.**
> 📝 ***对处理前 ATT（或事件研究超前项）为零的联合 Wald 检验 — DID 设计中平行趋势假设的经典稳健性检查。未能拒绝是平行趋势的必要但非充分证据；始终配合 sp.honest_did / sp.sensitivity_rr 进行设计稳健推断。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `result` | `string` | ✓ |  | DiD or event-study result with pre-period coefficients | 包含事前系数的 DID 或事件研究结果。 |
| `type` | `string (enum)` |  | `'wald'` | Test statistic | 检验统计量，可选值：`'wald'` — Wald 检验 |

> **type** options: `'wald'`
> 📝 ***type** 选项：`'wald'`（Wald 检验）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.pretrends_test(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/agent_api.md`, `docs/guides/choosing_did_estimator.md`, `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/agent_api.md`、`docs/guides/choosing_did_estimator.md`、`docs/guides/migration-from-r.md`*

---
### `sp.sensitivity_plot()`

**Plot Rambachan & Roth (2023) sensitivity analysis.**
> 📝 ***绘制 Rambachan & Roth（2023）敏感性分析。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `breakdown_color` | `string` |  | `'#E74C3C'` | Color for the breakdown point marker. | 崩溃点标记的颜色。 |
| `color` | `string` |  | `'#2C3E50'` | CI band color. | 置信区间带颜色。 |
| `figsize` | `array[string]` |  | `[10, 6]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，图形大小）。 |
| `original_ci` | `array[string]` |  |  | Original CI (at M=0) for comparison. | 用于比较的原始置信区间（M=0 时）。 |
| `original_color` | `string` |  | `'#27AE60'` | Color for original estimate marker. | 原始估计值标记的颜色。 |
| `original_estimate` | `number` |  |  | Original point estimate. | 原始点估计。 |
| `sensitivity` | `string` | ✓ |  | Output from ``honest_did()``. | ``honest_did()`` 的输出结果。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.sensitivity_plot(sensitivity="value")
print(result.summary())
```

---
### `sp.sensitivity_rr()`

**Rambachan-Roth (2023) honest-DiD sensitivity analysis: computes the largest violation of parallel trends (parametrised by Mbar -- relative magnitude of the post-period violation versus the worst observed pre-period one) under which the post-treatment ATT is still different from zero at level alpha. Reports both the robust confidence sets and the breakdown Mbar.**
> 📝 ***Rambachan-Roth（2023）honest-DiD 敏感性分析：计算在水平 alpha 下处理后 ATT 仍显著异于零的最大平行趋势违背程度（由 Mbar 参数化 — 事后违背相对于最差观测事前违背的相对幅度）。报告稳健置信集和崩溃 Mbar。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `Mbar` | `string` |  |  | Grid of relative-magnitude bounds; default is np.linspace(0, 2, n_grid) | 相对幅度边界网格；默认为 np.linspace(0, 2, n_grid)。 |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `method` | `string (enum)` |  | `'C-LF'` | Identification method | 识别方法，可选值：`'C-LF'`（条件似然法） |
| `n_grid` | `integer` |  | `20` | Mbar grid size when Mbar=None | 当 Mbar=None 时的 Mbar 网格大小。 |
| `result` | `string` | ✓ |  | Event-study or DiD result with full pre/post coefficients | 包含完整事前/事后系数的事件研究或 DID 结果。 |

> **method** options: `'C-LF'`
> 📝 ***method** 选项：`'C-LF'`（条件似然法）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.sensitivity_rr(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/callaway_santanna.md`, `docs/guides/choosing_did_estimator.md`, `docs/guides/cs_report.md`
> 📝 *另请参阅：`docs/guides/callaway_santanna.md`、`docs/guides/choosing_did_estimator.md`、`docs/guides/cs_report.md`*

---
### `sp.stacked_did()`

**Stacked DiD (Cengiz, Dube, Lindner, Zipperer 2019). For each treatment cohort, constructs a sub-experiment with only that cohort + clean (never-treated or not-yet-treated) controls, then TWFE on the stacked panel. Robust to staggered-adoption contamination at the cost of dropping late-treated units in early sub-experiments.**
> 📝 ***堆叠 DID（Cengiz, Dube, Lindner, Zipperer 2019）。为每个处理队列构建一个仅包含该队列 + 干净（从未处理或尚未处理）控制组的子实验，然后在堆叠面板上进行 TWFE。以在早期子实验中丢弃晚期处理单元为代价，对交错采纳污染具有稳健性。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `controls` | `array[string]` |  |  | Control-variable column names. | 控制变量列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `first_treat` | `string` | ✓ |  | first_treat parameter (str). | first_treat 参数（字符串，首次处理时期）。 |
| `group` | `string` | ✓ |  | Unit identifier | 单元标识符。 |
| `never_treated_only` | `boolean` |  | `True` | Use only never-treated as controls (drops late-treated) | 仅使用从未处理单元作为控制组（丢弃晚期处理单元）。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `window` | `array[string]` |  | `[-5, 5]` | Event-time (lead, lag) window per sub-experiment | 每个子实验的事件时间（超前、滞后）窗口。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.stacked_did(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/migration-from-r.md`*

---
### `sp.sun_abraham()`

**Sun-Abraham (2021) interaction-weighted event-study. Fixes the contamination in dynamic event-study TWFE coefficients from other relative-time bins by using cohort-specific interaction weights. Canonical companion to Callaway-Sant'Anna for event studies. Validation: certified parity evidence.**
> 📝 ***Sun-Abraham（2021）交互加权事件研究。通过使用队列特定的交互权重，修复动态事件研究 TWFE 系数中来自其他相对时间区间的污染。事件研究的经典 Callaway-Sant'Anna 伴侣方法。验证状态：已认证一致性证据。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster variable (defaults to i) | 聚类变量（默认为 i）。 |
| `control_group` | `string (enum)` |  | `'nevertreated'` | Control arm | 控制组，可选值：`'nevertreated'` — 从未处理组、`'notyettreated'` — 尚未处理组 |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. | 协变量矩阵、数据框或列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `event_window` | `array[string]` |  |  | (lead, lag) window for event-study coefficients | 事件研究系数的（超前、滞后）窗口。 |
| `g` | `string` | ✓ |  | First-treatment period (0 = never-treated) | 首次处理时期（0 = 从未处理）。 |
| `i` | `string` | ✓ |  | Unit identifier | 单元标识符。 |
| `t` | `string` | ✓ |  | Time period column | 时间周期列。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

> **control_group** options: `'nevertreated'`, `'notyettreated'`
> 📝 ***control_group** 选项：`'nevertreated'`（从未处理组）、`'notyettreated'`（尚未处理组）*

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.sun_abraham(y="outcome", data=df, g="value", t="value", i="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`, `docs/guides/honest_did.md`, `docs/guides/migration-from-r.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`、`docs/guides/honest_did.md`、`docs/guides/migration-from-r.md`*

---
### `sp.treatment_rollout_plot()`

**Visualise staggered treatment adoption timing.**
> 📝 ***可视化交错处理采纳时间。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `ax` | `string` |  |  | ax parameter. | ax 参数（matplotlib 坐标轴对象）。 |
| `data` | `string` | ✓ |  | Panel data with unit, time, and treatment columns. | 包含单元、时间和处理列的面板数据。 |
| `figsize` | `array[string]` |  | `[12, 7]` | figsize parameter (Tuple[float, float]). | figsize 参数（浮点数元组，图形大小）。 |
| `id` | `string` | ✓ |  | Unit identifier. | 单元标识符。 |
| `never_color` | `string` |  | `'#BDC3C7'` | Color for never-treated units. | 从未处理单元的颜色。 |
| `show_cohort_labels` | `boolean` |  | `True` | Annotate cohort boundaries on the y-axis. | 在 y 轴上标注队列边界。 |
| `sort_by` | `string` |  | `'treat_time'` | Sort units by: 'treat_time' (earliest first), 'id', or 'random'. | 单元排序方式：'treat_time'（最早处理在前）、'id' 或 'random'（随机）。 |
| `time` | `string` | ✓ |  | Time period variable. | 时间周期变量。 |
| `title` | `string` |  |  | title parameter (Optional[str]). | title 参数（可选字符串，图形标题）。 |
| `treat` | `string` | ✓ |  | First-treatment-period column (0 = never treated), or binary treatment indicator. | 首次处理时期列（0 = 从未处理），或二元处理指示变量。 |
| `treated_color` | `string` |  | `'#E74C3C'` | Color for treated unit-periods. | 已处理单元-时期的颜色。 |
| `untreated_color` | `string` |  | `'#ECF0F1'` | Color for untreated unit-periods. | 未处理单元-时期的颜色。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.treatment_rollout_plot(data=df, time="value", treat="value", id="value")
print(result.summary())
```

---
### `sp.twfe_decomposition()`

**TWFE decomposition: Goodman-Bacon (2021) + de Chaisemartin-D'Haultfoeuille weights.**
> 📝 ***TWFE 分解：Goodman-Bacon（2021）+ de Chaisemartin-D'Haultfoeuille 权重。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level. | 显著性水平。 |
| `data` | `string` | ✓ |  | Panel dataset in long format. | 长格式面板数据集。 |
| `first_treat` | `string` | ✓ |  | Treatment timing column (NaN or 0 for never-treated). | 处理时间列（NaN 或 0 表示从未处理）。 |
| `group` | `string` | ✓ |  | Unit identifier. | 单元标识符。 |
| `time` | `string` | ✓ |  | Time period variable. | 时间周期变量。 |
| `y` | `string` | ✓ |  | Outcome variable. | 结果变量。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.twfe_decomposition(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

---
### `sp.wooldridge_did()`

**Wooldridge (2021) extended TWFE (ETWFE). Saturated TWFE regression with cohort x post interactions; recovers cohort-specific ATTs. Numerically equivalent to CS / SA / BJS under the saturated specification. Validation: certified parity evidence.**
> 📝 ***Wooldridge（2021）扩展 TWFE（ETWFE）。含队列×事后交互项的饱和 TWFE 回归；恢复队列特定的 ATT。在饱和设定下数值上等价于 CS/SA/BJS。验证状态：已认证一致性证据。***

| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. | 置信区间和检验的显著性水平。 |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. | 聚类标准误的聚类标识符列。 |
| `controls` | `array[string]` |  |  | Control-variable column names. | 控制变量列名。 |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. | 包含估计器所用变量的 pandas 数据框。 |
| `first_treat` | `string` | ✓ |  | First-treatment period; 0 = never-treated | 首次处理时期；0 = 从未处理。 |
| `group` | `string` | ✓ |  | Unit identifier | 单元标识符。 |
| `time` | `string` | ✓ |  | Time period column. | 时间周期列。 |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. | 结果变量列名或结果数组。 |

**示例：**
> 📝 *示例代码*

```python
# 加载或准备数据
import statspai as sp
import pandas as pd

# 加载示例数据集
df = sp.datasets.card_1995()

result = sp.wooldridge_did(y="outcome", data=df, group="value", time="value", first_treat="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`
> 📝 *另请参阅：`docs/guides/choosing_did_estimator.md`*

---
