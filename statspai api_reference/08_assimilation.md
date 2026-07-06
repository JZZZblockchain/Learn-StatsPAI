# assimilation

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Assimilative Causal Inference (``sp.assimilation``).
> 📝 *同化因果推断（Assimilative Causal Inference，``sp.assimilation``）。*

Bridges Bayesian data assimilation — the workhorse of numerical
weather prediction, climate reanalysis, and oceanography — with
causal inference.  Proposed in
> 📝 *将贝叶斯数据同化——数值天气预报、气候再分析和海洋学的主力方法——与因果推断连接起来。提出于：*

    *Assimilative Causal Inference*,
    Nature Communications, 2026.
> 📝 *《同化因果推断》，Nature Communications，2026。*

The core idea is to treat the *causal effect* as a latent time-varying
state, and update its posterior belief as new randomised or
observational data batches arrive.  Each update fuses:
> 📝 *核心思想是将*因果效应*视为一个潜在时变状态，并随着新的随机实验或观察数据批次的到来更新其后验信念。每次更新融合：*

1. A **forecast** step propagating the prior through a user-supplied
   dynamics model (default: random-walk).
> 📝 *1. **预测**步骤：通过用户提供的动力学模型（默认：随机游走）传播先验。*
2. An **analysis** step that incorporates the fresh observational or
   experimental batch via a Kalman-style innovation.
> 📝 *2. **分析**步骤：通过卡尔曼式的新息将新的观察或实验批次纳入。*

The result is a running posterior over the causal effect, with an
effective-sample-size diagnostic that flags when new evidence should
trigger a re-design of the experiment.
> 📝 *结果是对因果效应的运行后验，并带有有效样本量诊断，当新证据应触发实验重新设计时会发出信号。*

Why this module exists in StatsPAI
----------------------------------
> 📝 *本模块在 StatsPAI 中的存在理由*
* Streaming A/B tests: the treatment effect may drift over seasons;
  assimilation lets you pool evidence without pretending the effect is
  static.
> 📝 *流式 A/B 测试：处理效应可能随季节漂移；同化让您能够汇总证据而不必假设效应是静态的。*
* Adaptive monitoring: public-health or policy evaluation that wants to
  update the target estimate monthly instead of waiting for a single
  large study.
> 📝 *自适应监测：公共卫生或政策评估希望每月更新目标估计，而不是等待单一大型研究。*
* Multi-source evidence synthesis: combine an RCT prior with streaming
  RWE (real-world-evidence) updates under a transport-compatible
  framework (pairs naturally with :mod:`sp.transport`).
> 📝 *多源证据综合：在可传输兼容框架下将 RCT 先验与流式 RWE（Real-World Evidence，真实世界证据）更新结合（与 :mod:`sp.transport` 自然配对）。*

**3 个公共函数**

### `sp.assimilative_causal()`

**End-to-end Assimilative Causal Inference pipeline (Nature Communications 2026): for each data batch, apply `estimator` to get (theta, SE), then fuse via Kalman filtering or particle filter. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 *端到端同化因果推断流水线（Nature Communications 2026）：对每个数据批次，应用 `estimator` 获取 (theta, SE)，然后通过卡尔曼滤波或粒子滤波进行融合。验证：已验证的证据等级（已知真相、参考实现、外部对比或蒙特卡洛结果）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `backend` | `string (enum)` |  | `'kalman'` | 后端方法（str）。 |
| `batches` | `array[string]` | ✓ |  | 数据批次（list）。 |
| `estimator` | `string` | ✓ |  | 将批次映射为 (theta_hat, se) 的函数。 |
| `prior_mean` | `number` |  | `0.0` | 先验均值（float）。 |
| `prior_var` | `number` |  | `1.0` | 先验方差（float）。 |
| `process_var` | `number` |  | `0.0` | 过程方差（float）。 |

> **backend** options: `'kalman'`, `'particle'`
> 📝 *中文翻译：* **backend** 选项：`'kalman'`（卡尔曼滤波）、`'particle'`（粒子滤波）

**Example:**
> 📝 *示例：*

```python
# 使用同化因果推断流水线融合多批次因果效应估计
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.assimilative_causal(batches=["a", "b"], estimator="value")
print(result.summary())
```

> 📁 See also: `docs/guides/assimilative_ci.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/assimilative_ci.md`

---
### `sp.causal_kalman()`

**Closed-form Kalman filter over a stream of causal-effect estimates + SEs. Produces a running posterior over the time-varying (or static) causal effect. Validation: validated evidence tier (known-truth, reference, external-parity, or Monte Carlo artifact).**
> 📝 *对因果效应估计 + 标准误流的闭式卡尔曼滤波。产生对时变（或静态）因果效应的运行后验。验证：已验证的证据等级（已知真相、参考实现、外部对比或蒙特卡洛结果）。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `estimates` | `array[string]` | ✓ |  | 估计值（list）。 |
| `prior_mean` | `number` |  | `0.0` | 先验均值（float）。 |
| `prior_var` | `number` |  | `1.0` | 先验方差（float）。 |
| `process_var` | `number` |  | `0.0` | 过程方差（float）。 |
| `standard_errors` | `array[string]` | ✓ |  | 标准误（list）。 |

**Example:**
> 📝 *示例：*

```python
# 使用卡尔曼滤波融合因果效应估计流
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.causal_kalman(estimates=["a", "b"], standard_errors=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/assimilative_ci.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/assimilative_ci.md`

---
### `sp.particle_filter()`

**Bootstrap SIR particle filter for non-Gaussian assimilative causal inference. Supports arbitrary prior sampler, transition sampler, and observation log-pdf, with systematic resampling triggered by an ESS threshold.**
> 📝 *用于非高斯同化因果推断的 Bootstrap SIR 粒子滤波。支持任意先验采样器、转移采样器和观测对数概率密度函数，并在 ESS 阈值触发系统重采样。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | 置信区间和检验的显著性水平。 |
| `ess_resample_threshold` | `number` |  | `0.5` | ESS 重采样阈值（float）。 |
| `estimates` | `array[string]` | ✓ |  | 估计值（list）。 |
| `n_particles` | `integer` |  | `2000` | 粒子数量。 |
| `prior_mean` | `number` |  | `0.0` | 先验均值（float）。 |
| `prior_var` | `number` |  | `1.0` | 先验方差（float）。 |
| `process_sd` | `number` |  | `0.0` | 过程标准差（float）。 |
| `standard_errors` | `array[string]` | ✓ |  | 标准误（list）。 |

**Example:**
> 📝 *示例：*

```python
# 使用粒子滤波进行非高斯同化因果推断
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.particle_filter(estimates=["a", "b"], standard_errors=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/assimilative_ci.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/assimilative_ci.md`

---
