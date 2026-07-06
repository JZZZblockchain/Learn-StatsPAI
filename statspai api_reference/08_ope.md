# ope

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Off-Policy Evaluation (``sp.ope``): estimate the value of a target
policy from data collected under a different behaviour policy. Covers
contextual bandits and off-policy reinforcement learning evaluation.
> 📝 *离线策略评估（OPE，Off-Policy Evaluation，``sp.ope``）：从不同行为策略下收集的数据中估计目标策略的价值。涵盖上下文赌博机和离线策略强化学习评估。*

Implemented: DM, IPS, SNIPS, DR, Switch-DR, sharp OPE under
unobserved confounding (Hess, Frauen, Melnychuk & Feuerriegel 2025,
arXiv:2502.13022), causal-policy forest (Kato 2025, arXiv:2512.22846).
> 📝 *已实现：DM（直接法）、IPS（逆倾向得分）、SNIPS（自归一化 IPS）、DR（双重稳健）、Switch-DR、未观测混杂下的锐利 OPE（Hess, Frauen, Melnychuk & Feuerriegel 2025, arXiv:2502.13022）、因果策略森林（Kato 2025, arXiv:2512.22846）。*

**5 个公共函数**

### `sp.OPEResult()`

**Container returned by sp.ope.* estimators (IPS, SNIPS, DR, Switch-DR, DM). Reports value, SE, CI, importance-ratio diagnostics.**
> 📝 *sp.ope.* 估计器（IPS、SNIPS、DR、Switch-DR、DM）返回的容器。报告策略价值、标准误、置信区间、重要性比率诊断。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | 置信区间（下界, 上界）。 |
| `diagnostics` | `object` | ✓ |  | 重要性比率诊断。 |
| `method` | `string` | ✓ |  | OPE 估计器名称（ips、snips、dr、switch_dr、dm）。 |
| `se` | `number` | ✓ |  | 策略价值估计的标准误。 |
| `value` | `number` | ✓ |  | 估计的策略价值。 |

**Example:**
> 📝 *示例：*

```python
# 创建离线策略评估（OPE）结果对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.OPEResult(method="value", value=1.0, se=1.0, ci=["a", "b"])
print(result.summary())
```

---
### `sp.direct_method()`

**Direct outcome regression (plug-in Q-model) OPE.**
> 📝 *直接结果回归（插件 Q 模型）OPE。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | 动作（np.ndarray）。 |
| `R` | `string` | ✓ |  | 奖励（np.ndarray）。 |
| `X` | `string` | ✓ |  | 特征矩阵或协变量 DataFrame。 |
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `n_actions` | `integer` |  |  | 动作数量。 |
| `pi_target` | `string` | ✓ |  | 目标策略。 |

**Example:**
> 📝 *示例：*

```python
# 使用直接法（DM）进行离线策略评估
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.direct_method(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
### `sp.doubly_robust()`

**Doubly-robust OPE (Dudik et al. 2011).**
> 📝 *双重稳健 OPE（Dudik et al. 2011）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | 动作（np.ndarray）。 |
| `R` | `string` | ✓ |  | 奖励（np.ndarray）。 |
| `X` | `string` | ✓ |  | 特征矩阵或协变量 DataFrame。 |
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `clip` | `number` |  | `50.0` | 重要性权重截断值（float）。 |
| `n_actions` | `integer` |  |  | 动作数量。 |
| `pi_behavior` | `string` |  |  | 行为策略（可选，np.ndarray）。 |
| `pi_target` | `string` | ✓ |  | 目标策略。 |

**Example:**
> 📝 *示例：*

```python
# 使用双重稳健法（DR）进行离线策略评估
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.doubly_robust(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
### `sp.ips()`

**Inverse propensity score OPE.**
> 📝 *逆倾向得分 OPE。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | 动作（np.ndarray）。 |
| `R` | `string` | ✓ |  | 奖励（np.ndarray）。 |
| `X` | `string` | ✓ |  | 特征矩阵或协变量 DataFrame。 |
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `clip` | `number` |  | `50.0` | 重要性权重截断值（float）。 |
| `pi_behavior` | `string` |  |  | 行为策略（可选，np.ndarray）。 |
| `pi_target` | `string` | ✓ |  | 目标策略。 |

**Example:**
> 📝 *示例：*

```python
# 使用逆倾向得分法（IPS）进行离线策略评估
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.ips(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
### `sp.snips()`

**Self-normalised IPS (bias-reduction for large IS weights).**
> 📝 *自归一化 IPS（针对大重要性权重的偏差减少）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `A` | `string` | ✓ |  | 动作（np.ndarray）。 |
| `R` | `string` | ✓ |  | 奖励（np.ndarray）。 |
| `X` | `string` | ✓ |  | 特征矩阵或协变量 DataFrame。 |
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `clip` | `number` |  | `50.0` | 重要性权重截断值（float）。 |
| `pi_behavior` | `string` |  |  | 行为策略（可选，np.ndarray）。 |
| `pi_target` | `string` | ✓ |  | 目标策略。 |

**Example:**
> 📝 *示例：*

```python
# 使用自归一化逆倾向得分法（SNIPS）进行离线策略评估
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.snips(X="value", A="value", R="value", pi_target="value")
print(result.summary())
```

---
