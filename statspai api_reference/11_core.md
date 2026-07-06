# core

> 📂 所属分类:11 · 其他杂项 (Other)

Core package initialization
> 📝 *核心包初始化*

**1 个公共函数**

### `sp.EconometricResults()`

**Unified results class for econometric models**
> 📝 *计量经济学模型的统一结果类*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data_info` | `object` |  |  | 数据信息参数（可选，Dict[str, Any]）。 |
| `diagnostics` | `object` |  |  | 诊断信息参数（可选，Dict[str, Any]）。 |
| `model_info` | `object` | ✓ |  | 模型信息参数（Dict[str, Any]）。 |
| `params` | `string` | ✓ |  | 参数（Series）。 |
| `std_errors` | `string` | ✓ |  | 标准误（Series）。 |

**Example:**
> 📝 *示例：*

```python
# 创建计量经济学模型结果对象并输出摘要
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.EconometricResults(params="value", std_errors="value")
print(result.summary())
```

---
