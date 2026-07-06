# geolift

> 📂 所属分类:11 · 其他杂项 (Other)

Geo-experiment ("geo-lift") causal measurement.
> 📝 *地理实验（"geo-lift"）因果测量。*

Estimates the incremental lift of an intervention switched on in a set of
treated geographies, against a synthetic counterfactual built from the untreated
geographies. See :func:`geolift`.
> 📝 *估计在一组处理地理区域中开启的干预措施的增量提升，基于从未处理地理区域构建的合成反事实。参见 :func:`geolift`。*

**1 个公共函数**

### `sp.geolift()`

**Estimate geo-experiment lift via synthetic control.**
> 📝 *通过合成控制法估计地理实验的提升效果。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `agg` | `string (enum)` |  | `'mean'` | 如何将多个处理地理区域聚合为一个处理序列。 |
| `alpha` | `number` |  | `0.05` | 传递给 :func:`sp.synth` 的显著性水平。 |
| `data` | `string` | ✓ |  | 长面板数据：每行一个（地理区域, 时间）观测。 |
| `geo` | `string` | ✓ |  | 地理区域（市场）标识列。 |
| `method` | `string` |  | `'classic'` | 传递给 :func:`sp.synth` 的合成控制方法（如 ``'classic'``、``'augmented'``、``'sdid'``）。 |
| `outcome` | `string` | ✓ |  | 结果/KPI 列（如销售额、转化率）。 |
| `time` | `string` | ✓ |  | 时间列。 |
| `treated_geos` | `array[string]` | ✓ |  | 干预措施开启的地理区域。 |
| `treatment_time` | `string` | ✓ |  | 首个处理期（含）。更早的时期用于训练合成控制。 |

> **agg** options: `'mean'`, `'sum'`
> 📝 *中文翻译：* **agg** 选项：`'mean'`（均值）、`'sum'`（求和）

**Example:**
> 📝 *示例：*

```python
# 通过合成控制法估计地理实验的因果提升效果
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.geolift(data=df, outcome="value", geo="value", time="value", treated_geos=["a", "b"], treatment_time="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/unified_quasi_experiments.md`

---
