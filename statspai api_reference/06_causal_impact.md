# causal_impact

> 📂 所属分类:06 · 贝叶斯方法 (Bayesian Methods)

Causal Impact module for StatsPAI.
> 📝 *StatsPAI 的因果影响模块。*

Estimates the causal effect of an intervention on a time series by
constructing a synthetic counterfactual from control series using
a structural time-series model.
> 📝 *通过使用结构性时间序列模型从控制序列构建合成反事实，估计干预对时间序列的因果效应。*

Equivalent to Google's R CausalImpact package.
> 📝 *等价于 Google 的 R CausalImpact 包。*

References
----------
> 📝 *参考文献*
Brodersen, K.H., Gallusser, F., Koehler, J., Remy, N., and Scott, S.L. (2015).
"Inferring Causal Impact Using Bayesian Structural Time-Series Models."
*Annals of Applied Statistics*, 9(1), 247-274. [@brodersen2015inferring]
> 📝 *Brodersen, K.H., Gallusser, F., Koehler, J., Remy, N., and Scott, S.L. (2015). "使用贝叶斯结构时间序列模型推断因果影响."《应用统计学年鉴》, 9(1), 247-274.*

**3 个公共函数**

### `sp.CausalImpactEstimator()`

**Causal Impact estimator using a structural time-series model.**
> 📝 *使用结构时间序列模型的因果影响估计器。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | 可信区间的显著性水平。 |
| `covariates` | `array[string]` |  |  | 不受干预影响的控制序列。 |
| `data` | `string` | ✓ |  | 时间序列数据，每行一个时期。 |
| `intervention_time` | `string` | ✓ |  | 首个干预后时期（含）。 |
| `n_seasons` | `integer` |  |  | 季节性周期（如有）。 |
| `time` | `string` | ✓ |  | 用于排序的时间列。 |
| `y` | `string` | ✓ |  | 结果（被干预）序列。 |

**Example:**
> 📝 *示例：*

```python
# 使用结构时间序列模型估计因果影响
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.CausalImpactEstimator(y="outcome", data=df, time="value", intervention_time="value")
print(result.summary())
```

---
### `sp.causal_impact()`

**Bayesian structural time series for causal impact analysis.**
> 📝 *用于因果影响分析的贝叶斯结构时间序列。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | 包含估计器所需变量的 pandas DataFrame。 |
| `intervention_time` | `string` | ✓ |  | 干预日期/索引。 |
| `time` | `string` | ✓ |  | 时间/日期列。 |
| `y` | `string` | ✓ |  | 结果时间序列列。 |

**Example:**
> 📝 *示例：*

```python
# 使用贝叶斯结构时间序列进行因果影响分析
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.causal_impact(y="outcome", data=df, time="value", intervention_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/unified_quasi_experiments.md`

---
### `sp.impactplot()`

**Causal Impact visualization (Google-style 3-panel plot).**
> 📝 *因果影响可视化（Google 风格的三面板图）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | 仅用于单面板类型。 |
| `figsize` | `array[string]` |  | `[12, 9]` | 图形尺寸（tuple[float, float]）。 |
| `result` | `string` | ✓ |  | ``causal_impact()`` 的结果。 |
| `title` | `string` |  |  | 图表标题（可选，str）。 |
| `type` | `string` |  | `'all'` | 图表类型：'all'（三面板：原始 + 逐点 + 累积）、'original'（实际 vs 反事实）、'pointwise'（逐点因果效应）、'cumulative'（累积效应）。 |

**Example:**
> 📝 *示例：*

```python
# 绘制因果影响可视化的三面板图
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.impactplot(result="value")
print(result.summary())
```

---
