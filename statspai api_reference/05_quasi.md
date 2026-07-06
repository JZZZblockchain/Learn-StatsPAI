# quasi

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Lightweight pre/post quasi-experimental designs.
> 📝 *轻量级前/后准实验设计。*

These wrap StatsPAI's OLS (Ordinary Least Squares, 普通最小二乘法) machinery into named, assumption-surfacing designs so
non-experts reach for the right estimator:
> 📝 *这些将 StatsPAI 的 OLS（Ordinary Least Squares，普通最小二乘法）机制封装为有名称、明确假设的设计，使非专家用户也能选择正确的估计器：*

- :func:`ancova` — covariate-adjusted comparison of group means.
> 📝 *:func:`ancova` — 协变量调整的组均值比较。*
- :func:`negd` — pre/post non-equivalent group design (ANCOVA or change-score).
> 📝 *:func:`negd` — 前/后非对等组设计（ANCOVA 或变化分数）。*

Both return the unified :class:`~statspai.core.results.CausalResult`.
> 📝 *两者都返回统一的 :class:`~statspai.core.results.CausalResult`。*

**2 个公共函数**

### `sp.ancova()`

**Covariate-adjusted comparison of group means (ANCOVA).**
> 📝 *协变量调整的组均值比较（ANCOVA）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | 报告的置信区间的显著性水平。 |
| `cluster` | `string` |  |  | 聚类稳健标准误列。 |
| `covariates` | `array[string]` |  |  | 调整协变量。非数值协变量作为分类变量（``C(col)``）处理。 |
| `data` | `string` | ✓ |  | 每行一个观测个体。 |
| `group` | `string` | ✓ |  | 处理组列。0/1 数值列直接使用；其他两水平列会被编码（通过 ``group_value`` 显式指定处理水平）。 |
| `group_value` | `string` |  |  | ``group`` 中表示处理的水平。 |
| `outcome` | `string` | ✓ |  | 结果列。 |
| `robust` | `string` |  | `'hc1'` | 异方差稳健标准误类型，传递给 :func:`sp.regress`。 |

**Example:**
> 📝 *示例：*

```python
# 使用 ANCOVA（协方差分析）进行协变量调整的组均值比较
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.ancova(data=df, outcome="value", group="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/unified_quasi_experiments.md`

---
### `sp.negd()`

**Pre/post non-equivalent group design (NEGD).**
> 📝 *前/后非对等组设计（NEGD）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | 同 :func:`ancova`。 |
| `cluster` | `string` |  |  | 同 :func:`ancova`。 |
| `covariates` | `array[string]` |  |  | 额外的调整协变量。 |
| `data` | `string` | ✓ |  | 每行一个观测个体（宽格式：包含 ``pre`` 和 ``post`` 列）。 |
| `group` | `string` | ✓ |  | 处理组列（编码方式见 :func:`ancova`）。 |
| `group_value` | `string` |  |  | 同 :func:`ancova`。 |
| `method` | `string (enum)` |  | `'ancova'` | 估计方法（见上文）。 |
| `post` | `string` | ✓ |  | 基线和后续结果列。 |
| `pre` | `string` | ✓ |  | 基线和后续结果列。 |
| `robust` | `string` |  | `'hc1'` | 同 :func:`ancova`。 |

> **method** options: `'ancova'`, `'change_score'`
> 📝 *中文翻译：* **method** 选项：`'ancova'`（协方差分析）、`'change_score'`（变化分数）

**Example:**
> 📝 *示例：*

```python
# 使用前/后非对等组设计（NEGD）估计处理效应
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.negd(data=df, group="value", pre="value", post="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/unified_quasi_experiments.md`

---
