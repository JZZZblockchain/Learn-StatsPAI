# bridge

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Bridging theorems for causal inference (StatsPAI v0.10).
> 📝 *因果推断的桥接定理（StatsPAI v0.10）。*

Each "bridging theorem" pairs two seemingly different estimators on the
same target parameter and proves that — under appropriate conditions —
they identify the same quantity. Reporting both estimates side-by-side
gives doubly-robust identification: if either path's assumption holds,
the estimate is consistent.
> 📝 *每个"桥接定理"将两个看似不同的估计器配对在同一目标参数上，并证明——在适当条件下——它们识别出相同的量。同时报告两个估计值提供了双重稳健识别：只要任一途径的假设成立，估计就是一致的。*

Six bridges shipped (per arXiv 2503.11375 / 2510.26723 / 2310.18563 v6 /
2404.09117 / 2411.02771 / 2202.07234, 2022-2025):
> 📝 *已发布六个桥接定理（基于 arXiv 2503.11375 / 2510.26723 / 2310.18563 v6 / 2404.09117 / 2411.02771 / 2202.07234，2022-2025）：*

* ``did_sc``        — DiD ≡ Synthetic Control (Sun-Xie-Zhang 2025)
> 📝 *``did_sc`` — DiD（双重差分）≡ 合成控制（Sun-Xie-Zhang 2025）*
* ``ewm_cate``      — EWM ≡ CATE → policy (Kato 2025)
> 📝 *``ewm_cate`` — EWM ≡ CATE → 策略（Kato 2025）*
* ``cb_ipw``        — Covariate Balancing ≡ IPW × DR (Słoczyński-Uysal-Wooldridge 2023)
> 📝 *``cb_ipw`` — 协变量平衡 ≡ IPW × DR（Słoczyński-Uysal-Wooldridge 2023）*
* ``kink_rdd``      — Kink-Bunching ≡ RDD (Lu-Wang-Xie 2025)
> 📝 *``kink_rdd`` — 拐点-聚束 ≡ RDD（断点回归）（Lu-Wang-Xie 2025）*
* ``dr_calib``      — Doubly Robust via Calibration (van der Laan-Luedtke-Carone 2024)
> 📝 *``dr_calib`` — 通过校准实现双重稳健（van der Laan-Luedtke-Carone 2024）*
* ``surrogate_pci`` — Long-term Surrogate ≡ PCI (Imbens-Kallus-Mao-Wang 2025, JRSS-B)
> 📝 *``surrogate_pci`` — 长期替代指标 ≡ PCI（Imbens-Kallus-Mao-Wang 2025, JRSS-B）*

The unified entry point is ``sp.bridge(data, kind=..., **kwargs)``,
returning a :class:`BridgeResult` reporting the two path estimates,
their agreement test, and the recommended doubly-robust point estimate.
> 📝 *统一入口点是 ``sp.bridge(data, kind=..., **kwargs)``，返回 :class:`BridgeResult`，报告两个途径的估计值、它们的一致性检验以及推荐的双重稳健点估计。*

**2 个公共函数**

### `sp.BridgeResult()`

**Result of a bridging-theorem comparison.**
> 📝 *桥接定理比较的结果。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `detail` | `object` |  | `None` | 返回的结果详细程度。 |
> 📝 *返回的结果详细程度。*
| `diff` | `number` | ✓ |  | 差异值（float）。 |
| `diff_p` | `number` | ✓ |  | 差异 p 值（float）。 |
| `diff_se` | `number` | ✓ |  | 差异标准误（float）。 |
| `estimate_a` | `number` | ✓ |  | 途径 A 估计值（float）。 |
| `estimate_b` | `number` | ✓ |  | 途径 B 估计值（float）。 |
| `estimate_dr` | `number` | ✓ |  | 双重稳健估计值（float）。 |
| `kind` | `string` | ✓ |  | 桥接类型（str）。 |
| `n_obs` | `integer` | ✓ |  | 观测数量。 |
| `path_a_name` | `string` | ✓ |  | 途径 A 名称（str）。 |
| `path_b_name` | `string` | ✓ |  | 途径 B 名称（str）。 |
| `reference` | `string` |  | `''` | 参考文献（str）。 |
| `se_a` | `number` | ✓ |  | 途径 A 标准误（float）。 |
| `se_b` | `number` | ✓ |  | 途径 B 标准误（float）。 |
| `se_dr` | `number` | ✓ |  | 双重稳健标准误（float）。 |

**Example:**
> 📝 *示例：*

```python
# 创建桥接定理比较结果对象
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.BridgeResult(kind="value", path_a_name="value", path_b_name="value", estimate_a=1.0, estimate_b=1.0, se_a=1.0, se_b=1.0, diff=1.0, diff_se=1.0, diff_p=1.0, estimate_dr=1.0, se_dr=1.0, n_obs=1.0)
print(result.summary())
```

---
### `sp.bridge()`

**Unified dispatcher for six causal-inference bridging theorems (2025-2026): DiD==SC (Shi-Athey), EWM==CATE (Ferman), IPW==DR==CB (Zhao-Percival), Bunching==RDD (Lu-Wang-Xie), DR-via-Calibration (Zhang), Long-term-surrogate==PCI (Imbens-Kallus-Mao-Wang). Reports both path estimates + doubly-robust recommendation.**
> 📝 *六个因果推断桥接定理的统一调度器（2025-2026）：DiD==SC（Shi-Athey）、EWM==CATE（Ferman）、IPW==DR==CB（Zhao-Percival）、Bunching==RDD（Lu-Wang-Xie）、DR-via-Calibration（Zhang）、Long-term-surrogate==PCI（Imbens-Kallus-Mao-Wang）。报告两个途径的估计值 + 双重稳健推荐。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | 包含估计器所需变量的 pandas DataFrame。 |
| `kind` | `string (enum)` | ✓ |  | 要调用哪个桥接定理。 |

> **kind** options: `'did_sc'`, `'ewm_cate'`, `'cb_ipw'`, `'kink_rdd'`, `'dr_calib'`, `'surrogate_pci'`
> 📝 *中文翻译：* **kind** 选项：`'did_sc'`（DiD≡合成控制）、`'ewm_cate'`（EWM≡CATE）、`'cb_ipw'`（协变量平衡≡IPW×DR）、`'kink_rdd'`（拐点≡RDD）、`'dr_calib'`（校准双重稳健）、`'surrogate_pci'`（替代指标≡PCI）

**Example:**
> 📝 *示例：*

```python
# 使用桥接定理统一调度器进行双重稳健因果推断
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.bridge(data=df, kind="value")
print(result.summary())
```

> 📁 See also: `docs/guides/bridging_theorems.md`, `docs/guides/proximal_family.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/bridging_theorems.md`, `docs/guides/proximal_family.md`

---
