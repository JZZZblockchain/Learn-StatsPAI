# gmm

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Dynamic panel GMM (Generalized Method of Moments, 广义矩估计) estimators for StatsPAI.
> 📝 *StatsPAI 的动态面板 GMM（Generalized Method of Moments，广义矩估计）估计器。*

Provides:
> 📝 *提供：*
- Arellano-Bond (1991) first-differenced GMM
> 📝 *Arellano-Bond (1991) 一阶差分 GMM*
- Blundell-Bond (1998) system GMM
> 📝 *Blundell-Bond (1998) 系统 GMM*
- Arellano-Bond test for serial correlation (AR(1)/AR(2))
> 📝 *Arellano-Bond 序列相关性检验（AR(1)/AR(2)）*
- Hansen/Sargan test for overidentifying restrictions
> 📝 *Hansen/Sargan 过度识别约束检验*

**2 个公共函数**

### `sp.gmm()`

**General GMM estimator for arbitrary moment conditions. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 *适用于任意矩条件的通用 GMM 估计器。验证：已验证的证据等级（已知真相、参考实现、外部对比或蒙特卡洛结果）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` |  |  | 权重矩阵（q × q）。若为 None，则先使用单位矩阵（一步法），再使用最优矩阵（两步法）。 |
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `data` | `string` |  |  | 传递给 moment_fn 的数据。 |
| `maxiter` | `integer` |  | `200` | 最大迭代次数（int）。 |
| `method` | `string` |  | `'twostep'` | 估计方法：'onestep'（一步法）、'twostep'（两步法）、'iterative'（迭代法）、'cue'（连续更新估计）。 |
| `moment_fn` | `string` | ✓ |  | 函数 g(theta, data) -> np.ndarray，形状为 (n, q)，返回每个观测的矩条件。 |
| `param_names` | `array[string]` |  |  | 参数名称。 |
| `se` | `string` |  | `'robust'` | 标准误类型：'robust'（HAC 类型）、'unadjusted'（未调整）。 |
| `theta0` | `string` | ✓ |  | 初始参数向量。 |
| `tol` | `number` |  | `1e-08` | 数值收敛容差。 |

**Example:**
> 📝 *示例：*

```python
# 使用广义矩估计（GMM）估计任意矩条件模型
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.gmm(data=df, moment_fn="value", theta0="value")
print(result.summary())
```

---
### `sp.xtabond()`

**Arellano-Bond / Blundell-Bond GMM for dynamic panels (standalone). Validation: certified parity evidence.**
> 📝 *适用于动态面板的 Arellano-Bond / Blundell-Bond GMM（独立版本）。验证：已认证的一致性证据。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | 包含估计器所需变量的 pandas DataFrame。 |
| `id` | `string` |  | `'id'` | 个体标识列。 |
| `lags` | `integer` |  | `1` | 滞后阶数（int）。 |
| `method` | `string (enum)` |  | `'difference'` | 估计方法：差分 GMM 或系统 GMM。 |
| `time` | `string` |  | `'time'` | 时间列。 |
| `twostep` | `boolean` |  | `False` | 是否使用两步法估计（bool）。 |
| `x` | `array[string]` |  |  | 外生回归变量。 |
| `y` | `string` | ✓ |  | 因变量。 |

> **method** options: `'difference'`, `'system'`
> 📝 *中文翻译：* **method** 选项：`'difference'`（差分 GMM）、`'system'`（系统 GMM）

**Example:**
> 📝 *示例：*

```python
# 使用 Arellano-Bond / Blundell-Bond GMM 估计动态面板模型
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.xtabond(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

> 📁 See also: `docs/guides/panel_data.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/panel_data.md`

---
