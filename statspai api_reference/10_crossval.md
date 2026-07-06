# crossval

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

Cross-engine validation for StatsPAI.
> 📝 *StatsPAI 的跨引擎验证。*

``sp.cross_validate`` runs one estimand through several *independent* engines
(StatsPAI native, pyfixest, linearmodels, DoubleML, R's fixest via Rscript,
Stata via batch ``do``) and reports whether they agree — turning the
cross-package-reproducibility discipline of Scott Cunningham's "estimate it two
ways and check they match" into a single callable for humans and agents.
> 📝 *``sp.cross_validate`` 将一个估计目标通过多个*独立*引擎（StatsPAI 原生、pyfixest、linearmodels、DoubleML、通过 Rscript 调用的 R fixest、通过批处理 ``do`` 调用的 Stata）运行，并报告它们是否一致——将 Scott Cunningham"用两种方法估计并比对"的跨包可重复性原则转化为面向人类和智能体的单一可调用接口。*

Public surface
--------------
> 📝 *公开接口*
- :func:`cross_validate` — the dispatcher.
> 📝 *:func:`cross_validate` — 调度器。*
- :class:`CrossValidationResult` — the verdict + per-engine table.
> 📝 *:class:`CrossValidationResult` — 判定结果 + 各引擎对比表。*
- :class:`EstimandSpec`, :class:`EngineEstimate`, :class:`TolerancePolicy` —
  building blocks, exposed for advanced use and testing.
> 📝 *:class:`EstimandSpec`、:class:`EngineEstimate`、:class:`TolerancePolicy` — 构建模块，开放给高级用法和测试。*

**2 个公共函数**

### `sp.CrossValidationResult()`

**Outcome of cross-validating one estimand across several engines.**
> 📝 *跨多个引擎交叉验证一个估计目标的结果。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `agreement` | `string` | ✓ |  | 一致性报告（AgreementReport）。 |
| `degradations` | `array[string]` |  |  | 退化信息（可选，List[Dict[str, Any]]）。 |
| `estimand` | `string` | ✓ |  | 估计目标（str）。 |
| `estimates` | `array[string]` | ✓ |  | 各引擎估计结果（List[EngineEstimate]）。 |
| `provenance` | `object` |  |  | 来源信息（可选，Dict[str, Any]）。 |
| `spec` | `object` | ✓ |  | 设定参数（Dict[str, Any]）。 |
| `term` | `string` | ✓ |  | 项名称（str）。 |

**Example:**
> 📝 *示例：*

```python
# 创建跨引擎交叉验证结果对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.CrossValidationResult(estimand="value", term="value", estimates=["a", "b"], agreement="value")
print(result.summary())
```

---
### `sp.cross_validate()`

**Estimate ONE model with several INDEPENDENT engines (StatsPAI, pyfixest, linearmodels, DoubleML, R's fixest, Stata) and report whether they agree (AGREE / PARTIAL / DISAGREE / INSUFFICIENT). Operationalises the cross-package reproducibility check: trust a number only when >=2 independent implementations reproduce it.**
> 📝 *使用多个独立引擎（StatsPAI、pyfixest、linearmodels、DoubleML、R fixest、Stata）估计同一个模型，并报告它们是否一致（AGREE / PARTIAL / DISAGREE / INSUFFICIENT）。将跨包可重复性检验付诸实践：仅当 >=2 个独立实现得出相同结果时才信任某个数值。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `covariates` | `array[string]` |  |  | 协变量矩阵、DataFrame 或列名。 |
| `data_or_result` | `string` | ✓ |  | 数据集（包含 `estimand` 和设定）或已拟合的 StatsPAI 结果对象，用于在其他引擎中重新运行。 |
| `endog` | `array[string]` |  |  | IV 内生变量。 |
| `engines` | `array[string]` |  | `'auto'` | 引擎列表：'auto'（所有已安装且适用的引擎）或指定列表如 ['statspai','R::fixest','pyfixest','Stata']。 |
| `estimand` | `string (enum)` |  |  | 估计目标：ols / feols / iv / poisson / dml / did（Callaway-Sant'Anna；及其别名）。 |
| `fixed_effects` | `array[string]` |  |  | 固定效应（list[str]）。 |
| `formula` | `string` |  |  | fixest 风格公式：'y ~ x \| fe \| endog ~ z'。 |
| `g` | `string` |  |  | DiD 队列/首次处理期列（0 = 从未处理）。 |
| `i` | `string` |  |  | DiD 个体标识列。 |
| `instruments` | `array[string]` |  |  | 工具变量（list[str]）。 |
| `t` | `string` |  |  | DiD 时间列。 |
| `tol` | `object` |  |  | 覆盖容差设置，如 {'coef_rtol':1e-4}。 |
| `treatment` | `string` |  |  | 关注回归变量（默认为协调后的项）。 |
| `vcov` | `string` |  |  | 方差估计量。 |
| `y` | `string` |  |  | 结果列。 |

> **estimand** options: `'ols'`, `'feols'`, `'iv'`, `'poisson'`, `'dml'`, `'did'`
> 📝 *中文翻译：* **estimand** 选项：`'ols'`（普通最小二乘）、`'feols'`（固定效应 OLS）、`'iv'`（工具变量）、`'poisson'`（泊松）、`'dml'`（双重机器学习）、`'did'`（双重差分）

**Example:**
> 📝 *示例：*

```python
# 使用多个独立引擎交叉验证同一模型的估计结果
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.cross_validate(y="outcome", data_or_result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/cross_engine_validation.md`, `docs/guides/data_mcp_ingestion.md`

---
