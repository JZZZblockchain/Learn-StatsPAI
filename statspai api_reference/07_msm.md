# msm

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Marginal Structural Models (MSM) for time-varying treatments.
> 📝 *适用于时变处理的边际结构模型（MSM，Marginal Structural Models）。*

Implements Robins' inverse-probability-of-treatment-weighted (IPTW)
estimator for longitudinal data with time-varying confounding.
> 📝 *实现了 Robins 的逆处理概率加权（IPTW，Inverse-Probability-of-Treatment-Weighted）估计器，用于具有时变混杂的纵向数据。*

**3 个公共函数**

### `sp.MarginalStructuralModel()`

**Class wrapper around :func:`msm` for programmatic access.**
> 📝 *围绕 :func:`msm` 的类封装，提供编程式访问。*

**Example:**
> 📝 *示例：*

```python
# 创建边际结构模型类封装对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.MarginalStructuralModel()
print(result.summary())
```

---
### `sp.msm()`

**Marginal Structural Models for time-varying treatments with time-varying confounders. Uses stabilized IPTW and cluster-robust inference. Handles binary or continuous treatment; exposure summary can be current, cumulative, or ever.**
> 📝 *适用于具有时变混杂的时变处理的边际结构模型。使用稳定化 IPTW 和聚类稳健推断。支持二元或连续处理；暴露摘要可以是当前、累积或曾经。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `baseline` | `array[string]` |  |  | 基线协变量。 |
| `data` | `string` | ✓ |  | 长格式面板数据（个体 × 时间）。 |
| `exposure` | `string (enum)` |  | `'cumulative'` | 暴露摘要类型。 |
| `family` | `string (enum)` |  | `'gaussian'` | 结果分布族。 |
| `id` | `string` | ✓ |  | 个体标识列。 |
| `time` | `string` | ✓ |  | 时期标识列。 |
| `time_varying` | `array[string]` | ✓ |  | 时变混杂变量（处理前）。 |
| `treat` | `string` | ✓ |  | 时变处理变量。 |
| `trim` | `number` |  | `0.01` | 权重截断分位数。 |
| `y` | `string` | ✓ |  | 结果变量。 |

> **exposure** options: `'cumulative'`, `'current'`, `'ever'`
> 📝 *中文翻译：* **exposure** 选项：`'cumulative'`（累积）、`'current'`（当前）、`'ever'`（曾经）

> **family** options: `'gaussian'`, `'binomial'`
> 📝 *中文翻译：* **family** 选项：`'gaussian'`（高斯）、`'binomial'`（二项）

**Example:**
> 📝 *示例：*

```python
# 使用边际结构模型（MSM）估计时变处理的因果效应
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.msm(y="outcome", data=df, treat="value", id="value", time="value", time_varying=["a", "b"])
print(result.summary())
```

> 📁 See also: `gmethods_timevarying.py`, `docs/guides/g_methods_ph.md`
> 📝 *中文翻译：* 📁 另见：`gmethods_timevarying.py`, `docs/guides/g_methods_ph.md`

---
### `sp.stabilized_weights()`

**Compute stabilized IPTW weights for time-varying treatments. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 *计算时变处理的稳定化 IPTW 权重。验证：已验证的证据等级（已知真相、参考实现、外部对比或蒙特卡洛结果）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `baseline` | `array[string]` |  |  | 基线协变量。 |
| `data` | `string` | ✓ |  | 排序后的长格式面板数据（每行一个个体-时间观测）。 |
| `id` | `string` | ✓ |  | 个体标识列。 |
| `time` | `string` | ✓ |  | 时间标识列。 |
| `time_varying` | `array[string]` | ✓ |  | 时变混杂变量（已滞后至处理前）。 |
| `treat` | `string` | ✓ |  | 处理列（二元 0/1 或连续）。 |
| `treat_type` | `string (enum)` |  | `'auto'` | 覆盖自动检测的处理类型。 |
| `trim_per_period` | `number` |  | `0.0` | 若 > 0，在计算累积乘积*之前*将每期密度比在对称分位数 ``[trim_per_period, 1 - trim_per_period]`` 处截断。常用值为 0.01。设为 0 则禁用每期截断（默认）。 |

> **treat_type** options: `'auto'`, `'binary'`, `'continuous'`
> 📝 *中文翻译：* **treat_type** 选项：`'auto'`（自动检测）、`'binary'`（二元）、`'continuous'`（连续）

**Example:**
> 📝 *示例：*

```python
# 计算时变处理的稳定化逆概率加权（IPTW）权重
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.stabilized_weights(data=df, treat="value", id="value", time="value", time_varying=["a", "b"])
print(result.summary())
```

---
