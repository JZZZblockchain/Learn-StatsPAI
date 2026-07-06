# nonparametric

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

Nonparametric estimation methods.
> 📝 *非参数估计方法。*

Provides local polynomial regression (lpoly), kernel density estimation (kdensity),
and nonparametric regression (npregress).
> 📝 *提供局部多项式回归（lpoly）、核密度估计（kdensity）和非参数回归（npregress）。*

**4 个公共函数**

### `sp.KDensityResult()`

**Results from kernel density estimation.**
> 📝 *核密度估计的结果。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth` | `number` | ✓ |  | 用于局部平滑或核加权的带宽。 |
| `data` | `string` | ✓ |  | 包含估计器所需变量的 pandas DataFrame。 |
| `density` | `string` | ✓ |  | 密度值（ndarray）。 |
| `grid` | `string` | ✓ |  | 网格点（ndarray）。 |
| `kernel` | `string` | ✓ |  | 用于加权或平滑的核函数。 |
| `n` | `integer` | ✓ |  | 样本量（int）。 |

**Example:**
> 📝 *示例：*

```python
# 创建核密度估计结果对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.KDensityResult(data=df, grid="value", density="value", bandwidth=1.0, kernel="value", n=1.0)
print(result.summary())
```

---
### `sp.LPolyResult()`

**Results from local polynomial regression.**
> 📝 *局部多项式回归的结果。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth` | `number` | ✓ |  | 用于局部平滑或核加权的带宽。 |
| `ci_lower` | `string` | ✓ |  | 置信区间下界（ndarray）。 |
| `ci_upper` | `string` | ✓ |  | 置信区间上界（ndarray）。 |
| `data_x` | `string` | ✓ |  | 自变量数据（ndarray）。 |
| `data_y` | `string` | ✓ |  | 因变量数据（ndarray）。 |
| `degree` | `integer` | ✓ |  | 多项式阶数（int）。 |
| `fitted` | `string` | ✓ |  | 拟合值（ndarray）。 |
| `grid` | `string` | ✓ |  | 网格点（ndarray）。 |
| `kernel` | `string` | ✓ |  | 用于加权或平滑的核函数。 |
| `n` | `integer` | ✓ |  | 样本量（int）。 |
| `se` | `string` | ✓ |  | 标准误（ndarray）。 |

**Example:**
> 📝 *示例：*

```python
# 创建局部多项式回归结果对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.LPolyResult(grid="value", fitted="value", se="value", ci_lower="value", ci_upper="value", bandwidth=1.0, degree=1.0, kernel="value", n=1.0, data_x="value", data_y="value")
print(result.summary())
```

---
### `sp.kdensity()`

**Kernel density estimation. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 *核密度估计。验证：已验证的证据等级（已知真相、参考实现、外部对比或蒙特卡洛结果）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth` | `number` |  |  | 核带宽。若为 None，则自动选择。 |
| `bw_method` | `string` |  | `'silverman'` | 带宽选择方法：'silverman' 或 'sheather-jones'。 |
| `data` | `string` |  |  | 输入数据。 |
| `grid` | `string` |  |  | 自定义评估网格。 |
| `kernel` | `string` |  | `'gaussian'` | 核函数：'gaussian'（高斯）、'epanechnikov'、'uniform'（均匀）、'triangular'（三角）、'biweight'（双权）、'cosine'（余弦）。 |
| `n_grid` | `integer` |  | `512` | 评估网格点数。 |
| `weights` | `string` |  |  | 观测权重的列名。 |
| `x` | `string` |  |  | 密度估计的变量名。 |

**Example:**
> 📝 *示例：*

```python
# 使用核密度估计（KDE）估计变量分布
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.kdensity(x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.lpoly()`

**Local polynomial regression.**
> 📝 *局部多项式回归。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | 置信区间的显著性水平。 |
| `bandwidth` | `number` |  |  | 核带宽。若为 None，则使用 Silverman 经验法则。 |
| `ci` | `boolean` |  | `True` | 是否计算置信区间。 |
| `data` | `string` |  |  | 输入数据。 |
| `degree` | `integer` |  | `1` | 多项式阶数（0=Nadaraya-Watson，1=局部线性，2=局部二次）。 |
| `grid` | `string` |  |  | 自定义评估网格。覆盖 n_grid。 |
| `kernel` | `string` |  | `'epanechnikov'` | 核函数：'epanechnikov'、'gaussian'（高斯）、'uniform'（均匀）、'triangular'（三角）、'biweight'（双权）。 |
| `n_grid` | `integer` |  | `100` | 评估网格点数。 |
| `x` | `string` |  |  | 自变量名称。 |
| `y` | `string` |  |  | 因变量名称。 |

**Example:**
> 📝 *示例：*

```python
# 使用局部多项式回归进行非参数估计
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.lpoly(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
