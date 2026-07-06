# imputation

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Missing data handling and multiple imputation.
> 📝 *缺失数据处理与多重插补。*

Provides MICE (Multiple Imputation by Chained Equations),
EM imputation, and analysis tools for multiply-imputed data.
> 📝 *提供 MICE（Multiple Imputation by Chained Equations，链式方程多重插补）、EM 插补以及多重插补数据的分析工具。*

**3 个公共函数**

### `sp.MICEResult()`

**Results from MICE imputation.**
> 📝 *MICE 插补的结果。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `convergence` | `string` | ✓ |  | 收敛信息。 |
| `imputed_datasets` | `string` | ✓ |  | 插补后的数据集。 |
| `methods` | `string` | ✓ |  | 插补方法。 |
| `n_imputations` | `string` | ✓ |  | 插补次数。 |
| `n_missing` | `string` | ✓ |  | 缺失值数量。 |
| `n_obs` | `string` | ✓ |  | 观测数量。 |
| `variables_imputed` | `string` | ✓ |  | 被插补的变量。 |

**Example:**
> 📝 *示例：*

```python
# 创建 MICE 多重插补结果对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.MICEResult(imputed_datasets="value", n_imputations="value", n_obs="value", n_missing="value", variables_imputed="value", methods="value", convergence="value")
print(result.summary())
```

---
### `sp.mi_estimate()`

**Run an estimator on each imputed dataset and combine using Rubin's rules.**
> 📝 *在每个插补数据集上运行估计器，并使用 Rubin 规则合并结果。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `estimator` | `string` | ✓ |  | 返回 EconometricResults 对象的估计函数。 |
| `mice_result` | `string` | ✓ |  | mice() 的结果。 |

**Example:**
> 📝 *示例：*

```python
# 在每个插补数据集上运行估计器并用 Rubin 规则合并
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.mi_estimate(mice_result="value", estimator="value")
print(result.summary())
```

---
### `sp.mice()`

**Multiple Imputation by Chained Equations (MICE).**
> 📝 *链式方程多重插补（MICE，Multiple Imputation by Chained Equations）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | 含有缺失值（NaN）的数据。 |
| `m` | `integer` |  | `5` | 插补次数。 |
| `max_iter` | `integer` |  | `10` | 每次插补的 MICE 迭代次数。 |
| `method` | `object` |  | `'pmm'` | 每变量的插补方法：'pmm'（预测均值匹配）、'norm'（贝叶斯线性）、'logreg'（二元逻辑回归）、'sample'（随机抽样）。字典映射变量名到方法。 |
| `predictors` | `array[string]` |  |  | 字典映射变量 -> 预测变量列表。若为 None，则使用所有其他变量。 |
| `print_progress` | `boolean` |  | `False` | 是否打印进度（bool）。 |
| `seed` | `integer` |  |  | 随机种子。 |

**Example:**
> 📝 *示例：*

```python
# 使用链式方程多重插补（MICE）处理缺失数据
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.mice(data=df)
print(result.summary())
```

---
