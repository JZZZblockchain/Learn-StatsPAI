# selection

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Variable selection tools.
> 📝 *变量选择工具。*

- ``stepwise``: Stepwise regression with AIC/BIC/p-value criteria
> 📝 *``stepwise``：基于 AIC/BIC/p 值准则的逐步回归*
- ``lasso_select``: LASSO-based variable selection with coordinate descent
> 📝 *``lasso_select``：基于 LASSO 的变量选择，使用坐标下降法*

**3 个公共函数**

### `sp.SelectionResult()`

**Result container for variable selection procedures.**
> 📝 *变量选择过程的结果容器。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coefficients` | `object` |  |  | 系数（可选，Dict[str, float]）。 |
| `dropped` | `array[string]` | ✓ |  | 被剔除的变量（List[str]）。 |
| `final_model` | `object` | ✓ |  | 最终模型（Dict[str, Any]）。 |
| `history` | `string` | ✓ |  | 选择历史（pd.DataFrame）。 |
| `lasso_path` | `object` |  |  | LASSO 路径文件系统路径。 |
| `method` | `string` |  | `''` | 使用的估计器或算法变体。 |
| `selected` | `array[string]` | ✓ |  | 被选中的变量（List[str]）。 |

**Example:**
> 📝 *示例：*

```python
# 创建变量选择结果对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.SelectionResult(selected=["a", "b"], dropped=["a", "b"], history="value")
print(result.summary())
```

---
### `sp.lasso_select()`

**LASSO-based variable selection.**
> 📝 *基于 LASSO 的变量选择。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | 包含估计器所需变量的 pandas DataFrame。 |
| `eps` | `number` |  | `0.001` | lambda_min / lambda_max 的比率。 |
| `max_iter` | `integer` |  | `1000` | 每个 lambda 的最大坐标下降迭代次数。 |
| `method` | `string (enum)` |  | `'cv'` | 选择正则化参数 lambda 的方法。 |
| `n_folds` | `integer` |  | `10` | 交叉验证折数（仅用于 ``method="cv"``）。 |
| `n_lambda` | `integer` |  | `100` | 网格中 lambda 值的数量。 |
| `seed` | `integer` |  | `42` | CV 折分配的随机种子。 |
| `tol` | `number` |  | `1e-06` | 收敛容差。 |
| `verbose` | `boolean` |  | `True` | 是否打印进度。 |
| `x` | `array[string]` | ✓ |  | 候选自变量。 |
| `y` | `string` | ✓ |  | 因变量列。 |

> **method** options: `'cv'`, `'bic'`, `'aic'`
> 📝 *中文翻译：* **method** 选项：`'cv'`（交叉验证）、`'bic'`（BIC 准则）、`'aic'`（AIC 准则）

**Example:**
> 📝 *示例：*

```python
# 使用 LASSO 进行基于正则化的变量选择
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.lasso_select(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.stepwise()`

**Stepwise variable selection for OLS regression.**
> 📝 *OLS 回归的逐步变量选择。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha_in` | `number` |  | `0.05` | 变量进入的 p 值阈值（当 ``criterion="pvalue"`` 时）。 |
| `alpha_out` | `number` |  | `0.1` | 变量剔除的 p 值阈值（当 ``criterion="pvalue"`` 时）。 |
| `criterion` | `string (enum)` |  | `'bic'` | 优化准则。默认为 ``"bic"``。 |
| `data` | `string` | ✓ |  | 包含所有变量的数据集。 |
| `method` | `string (enum)` |  | `'both'` | 选择策略。默认为 ``"both"``（双向）。 |
| `verbose` | `boolean` |  | `True` | 是否打印逐步进度。 |
| `x` | `array[string]` | ✓ |  | 候选自变量列名。 |
| `y` | `string` | ✓ |  | 因变量列名。 |

> **criterion** options: `'aic'`, `'bic'`, `'adjr2'`, `'pvalue'`
> 📝 *中文翻译：* **criterion** 选项：`'aic'`（AIC）、`'bic'`（BIC）、`'adjr2'`（调整 R²）、`'pvalue'`（p 值）

> **method** options: `'forward'`, `'backward'`, `'both'`
> 📝 *中文翻译：* **method** 选项：`'forward'`（前向）、`'backward'`（后向）、`'both'`（双向）

**Example:**
> 📝 *示例：*

```python
# 使用逐步回归进行变量选择
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.stepwise(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
