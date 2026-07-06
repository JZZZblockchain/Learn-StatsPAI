# fixest

> 📂 所属分类:03 · 回归、面板与多层模型 (Regression, Panel & Multilevel)

High-dimensional fixed effects estimation via pyfixest.
> 📝 *通过 pyfixest 进行高维固定效应估计。*

This module provides thin wrappers around pyfixest's estimation functions,
converting results into StatsPAI's ``EconometricResults`` for seamless
integration with ``outreg2`` and the rest of the ecosystem.
> 📝 *本模块提供了围绕 pyfixest 估计函数的薄封装，将结果转换为 StatsPAI 的 ``EconometricResults``，以便与 ``outreg2`` 及生态系统的其余部分无缝集成。*

Requires: ``pip install pyfixest``
> 📝 *需要：``pip install pyfixest``*

Examples
--------
> 📝 *示例*
>>> from statspai.fixest import feols, fepois
>>>
>>> # Two-way fixed effects with clustered SEs
>>> result = feols("wage ~ experience | firm + year",
...               data=df, vcov={"CRV1": "firm"})
>>> print(result.summary())
>>>
>>> # Poisson regression
>>> result = fepois("patents ~ rd_spending | firm", data=df)
>>>
>>> # Works with outreg2
>>> from statspai import outreg2
>>> outreg2(result, filename="table.xlsx")

**4 个公共函数**

### `sp.etable()`

**Display a pyfixest-style regression table for StatsPAI results.**
> 📝 *为 StatsPAI 结果显示 pyfixest 风格的回归表。*

**Example:**
> 📝 *示例：*

```python
# 显示 pyfixest 风格的回归表
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.etable()
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`, `docs/guides/migration-from-r.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/exporting-regression-tables.md`, `docs/guides/migration-from-r.md`

---
### `sp.feglm()`

**Estimate GLM (logit, probit, Gaussian) with high-dimensional fixed effects. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 *估计具有高维固定效应的 GLM（广义线性模型，Generalized Linear Model）（logit、probit、高斯）。验证：已验证的证据等级（已知真相、参考实现、外部对比或蒙特卡洛结果）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | 扩展 ``vce=`` 菜单的聚类标识列（也是一维 ``{"CRV1": cluster}`` 的简写）。 |
| `conley_cutoff` | `number` |  |  | Conley 距离截断值（可选，float）。 |
| `conley_lat` | `string` |  |  | Conley 纬度坐标列（可选，str）。 |
| `conley_lon` | `string` |  |  | Conley 经度坐标列（可选，str）。 |
| `data` | `string` | ✓ |  | 输入数据集。 |
| `family` | `string` |  | `'gaussian'` | GLM 分布族：``"gaussian"``（高斯）、``"logit"``、``"probit"``。 |
| `fml` | `string` | ✓ |  | pyfixest 公式。 |
| `seed` | `integer` |  |  | 抽样（非枚举）``vce="wild"`` 的随机种子。 |
| `vcov` | `object` |  |  | 方差-协方差估计器（``vce=`` 是规范别名）。还支持 ``vce="CR2"``/``"CR3"``/``"jackknife"``（配合 ``cluster=``）使用 clubSandwich 偏差减小的聚类稳健标准误，以及 ``vce="wild"``（配合 ``cluster=``）使用限制得分 Wild 聚类 Bootstrap（Kline-Santos 2012；在枚举情况下与 Stata ``boottest`` 比特一致）。 |
| `wild_reps` | `integer` |  | `9999` | ``vce="wild"`` 的重复次数。当 ``2**G <= wild_reps`` 时，完整 Rademacher 网格被枚举（确定性）。 |
| `wild_weight_type` | `string` |  | `'rademacher'` | Wild 权重分布（``"rademacher"`` 或 ``"webb"``）。 |

**Example:**
> 📝 *示例：*

```python
# 使用 pyfixest 估计高维固定效应 GLM 模型
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.feglm(formula="lwage ~ x1 + x2", data=df, fml="value")
print(result.summary())
```

> 📁 See also: `docs/guides/grammar.md`, `docs/guides/migration-from-r.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/grammar.md`, `docs/guides/migration-from-r.md`

---
### `sp.feols()`

**Estimate OLS / IV with high-dimensional fixed effects via pyfixest. Validation: certified parity evidence.**
> 📝 *通过 pyfixest 估计具有高维固定效应的 OLS/IV。验证：已认证的一致性证据。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | 扩展 ``vce=`` 菜单的聚类标识列；也是一维 ``{"CRV1": cluster}`` 的简写。 |
| `collin_tol` | `number` |  | `1e-06` | 共线性容差。 |
| `conley_cutoff` | `number` |  |  | ``vce="conley"`` 的 Conley 距离截断值（km）。 |
| `conley_lat` | `string` |  |  | ``vce="conley"`` 的坐标列（十进制度数）。 |
| `conley_lon` | `string` |  |  | ``vce="conley"`` 的坐标列（十进制度数）。 |
| `data` | `string` | ✓ |  | 输入数据集。 |
| `fixef_rm` | `string` |  | `'none'` | 如何处理单一固定效应：``"none"``（保留）或 ``"singleton"``（删除）。 |
| `fml` | `string` | ✓ |  | pyfixest 风格公式。示例：- ``"Y ~ X1 + X2"`` — 普通 OLS - ``"Y ~ X1 \| firm + year"`` — 双向固定效应 - ``"Y ~ 1 \| firm \| X1 ~ Z1"`` — 带固定效应的 IV - ``"Y ~ X1 \| csw0(firm, year)"`` — 多重估计 |
| `lean` | `boolean` |  | `False` | 若为 True，则删除大型中间数组以节省内存。 |
| `seed` | `integer` |  |  | ``vce="wild"`` 的随机种子。 |
| `ssc` | `string` |  |  | 通过 ``pyfixest.ssc()`` 的小样本校正。 |
| `vcov` | `object` |  |  | 方差-协方差估计器（``vce=`` 是规范别名）。- ``"iid"`` — 经典 - ``"HC1"``、``"HC2"``、``"HC3"`` — 异方差稳健 - ``{"CRV1": "firm"}`` — 聚类稳健 - ``{"CRV1": "firm + year"}`` — 双向聚类 - ``vce="CR2"``/``"CR3"``/``"jackknife"``（配合 ``cluster=``）— Pustejovsky-Tipton 偏差减小的聚类稳健，在 FE 吸收的组内设计上；与 R ``clubSandwich::vcovCR(plm)`` 一致。- ``vce="wild"``（配合 ``cluster=``）— WCR Wild 聚类 Bootstrap（Cameron-Gelbach-Miller 2008）；已对 Stata ``boottest`` 验证。- ``vce="conley"``（配合 ``conley_lat=/conley_lon=/conley_cutoff=``）— Conley 空间 HAC（Stata ``acreg`` 平面距离约定）。 |
| `weights` | `string` |  |  | 回归权重的列名。 |
| `wild_reps` | `integer` |  | `999` | ``vce="wild"`` 的 Bootstrap 重复次数。 |
| `wild_weight_type` | `string` |  | `'rademacher'` | Wild 权重分布（``"rademacher"``、``"webb"``、``"mammen"``）。 |

**Example:**
> 📝 *示例：*

```python
# 使用 pyfixest 估计高维固定效应 OLS/IV 模型
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.feols(formula="lwage ~ x1 + x2", data=df, fml="value")
print(result.summary())
```

> 📁 See also: `docs/guides/economist_mcp_workflow.md`, `docs/guides/economist_mcp_workflow_zh.md`, `docs/guides/gpu_acceleration.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/economist_mcp_workflow.md`, `docs/guides/economist_mcp_workflow_zh.md`, `docs/guides/gpu_acceleration.md`

---
### `sp.fepois()`

**Estimate Poisson regression with high-dimensional fixed effects via pyfixest. Validation: certified parity evidence.**
> 📝 *通过 pyfixest 估计具有高维固定效应的泊松回归。验证：已认证的一致性证据。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | 扩展 ``vce=`` 菜单的聚类标识列；也是一维 ``{"CRV1": cluster}`` 的简写。 |
| `collin_tol` | `number` |  | `1e-06` | 共线性容差。 |
| `conley_cutoff` | `number` |  |  | Conley 距离截断值（可选，float）。 |
| `conley_lat` | `string` |  |  | Conley 纬度坐标列（可选，str）。 |
| `conley_lon` | `string` |  |  | Conley 经度坐标列（可选，str）。 |
| `data` | `string` | ✓ |  | 输入数据集。 |
| `fixef_rm` | `string` |  | `'none'` | 单一固定效应处理方式。 |
| `fml` | `string` | ✓ |  | pyfixest 公式。例如 ``"Y ~ X1 \| firm"``。 |
| `iwls_maxiter` | `integer` |  | `25` | 最大 IWLS 迭代次数。 |
| `iwls_tol` | `number` |  | `1e-08` | IWLS 收敛容差。 |
| `seed` | `integer` |  |  | 抽样（非枚举）``vce="wild"`` 的随机种子。 |
| `ssc` | `string` |  |  | 小样本校正。 |
| `vcov` | `object` |  |  | 方差-协方差估计器（``vce=`` 是规范别名）。除了 pyfixest 的值（``"iid"``、``"HC1"``、``{"CRV1": "firm"}`` 等），还支持扩展菜单：- ``vce="CR2"``/``"CR3"``/``"jackknife"``（配合 ``cluster=``）— clubSandwich GLM 偏差减小的聚类稳健标准误，在 FE-as-dummies 设计上；与 R ``clubSandwich::vcovCR(glm)`` 一致。- ``vce="wild"``（配合 ``cluster=``）— 限制得分 Wild 聚类 Bootstrap（Kline-Santos 2012），使用 Stata ``boottest`` 的精确学生化；在枚举情况下与 ``boottest`` 比特一致。 |
| `weights` | `string` |  |  | 回归权重的列名（扩展 ``vce=`` 菜单不支持）。 |
| `wild_reps` | `integer` |  | `9999` | ``vce="wild"`` 的重复次数。当 ``2**G <= wild_reps`` 时，完整 Rademacher 网格被枚举（确定性）。 |
| `wild_weight_type` | `string` |  | `'rademacher'` | Wild 权重分布（``"rademacher"`` 或 ``"webb"``）。 |

**Example:**
> 📝 *示例：*

```python
# 使用 pyfixest 估计高维固定效应泊松回归
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.fepois(formula="lwage ~ x1 + x2", data=df, fml="value")
print(result.summary())
```

> 📁 See also: `docs/guides/grammar.md`, `docs/guides/migration-from-r.md`, `docs/guides/panel_data.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/grammar.md`, `docs/guides/migration-from-r.md`, `docs/guides/panel_data.md`

---
