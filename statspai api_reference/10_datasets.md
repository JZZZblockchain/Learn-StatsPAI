# datasets

> 📂 所属分类:10 · 工作流、工具与数据 (Workflow, Utils & Data)

Canonical econometrics datasets with documented expected estimates.
> 📝 *具有文档化预期估计值的规范计量经济学数据集。*

This subpackage provides deterministic, reproducible datasets used
throughout the causal-inference literature, consolidated under a
single import path ``sp.datasets``:
> 📝 *本子包提供因果推断文献中使用的确定性、可重复数据集，统一通过 ``sp.datasets`` 导入路径访问：*

>>> import statspai as sp
>>> df = sp.datasets.nsw_lalonde()
>>> df.attrs['expected_experimental_att']
1794

Each function returns a ``pd.DataFrame`` with:
> 📝 *每个函数返回一个 ``pd.DataFrame``，具有：*

- A fully-deterministic DGP (fixed seed, BSD/MIT redistributable).
> 📝 *完全确定性的 DGP（Data Generating Process，数据生成过程）（固定种子，BSD/MIT 可再分发）。*
- ``df.attrs`` containing:
> 📝 *``df.attrs`` 包含：*
  - ``'paper'`` — original paper citation
> 📝 *``'paper'`` — 原始论文引用*
  - ``'expected_*'`` — theoretically-anchored estimates (from the
    published paper on the ORIGINAL data, not necessarily the
    simulated replica)
> 📝 *``'expected_*'`` — 理论锚定的估计值（来自原始数据上发表的论文，不一定是模拟副本）*
  - ``'notes'`` — what to be careful about when using this replica
> 📝 *``'notes'`` — 使用此副本时需要注意的事项*

The simulated replicas are designed to match the *structure* and
*summary statistics* of the original datasets.  For numerical R /
Stata parity against the original data, see
``tests/external_parity/PUBLISHED_REFERENCE_VALUES.md``.
> 📝 *模拟副本旨在匹配原始数据集的*结构*和*汇总统计量*。关于与原始数据的数值 R/Stata 一致性，请参见 ``tests/external_parity/PUBLISHED_REFERENCE_VALUES.md``。*

Available datasets
------------------
> 📝 *可用数据集*

DID / panel
> 📝 *DID（双重差分）/ 面板*
    ``mpdta()``                 — Callaway-Sant'Anna teen employment
> 📝 *``mpdta()`` — Callaway-Sant'Anna 青少年就业*
    ``teen_employment()``       — alias of ``mpdta()``
> 📝 *``teen_employment()`` — ``mpdta()`` 的别名*

RD
> 📝 *RD（断点回归）*
    ``lee_2008_senate()``       — US Senate RD (Lee 2008)
> 📝 *``lee_2008_senate()`` — 美国参议院 RD（Lee 2008）*

IV
> 📝 *IV（工具变量）*
    ``card_1995()``             — IV returns-to-schooling
> 📝 *``card_1995()`` — IV 教育回报率*
    ``angrist_krueger_1991()``  — quarter-of-birth IV
> 📝 *``angrist_krueger_1991()`` — 出生季度 IV*

Matching / SOO
> 📝 *匹配 / SOO（Selection on Observables）*
    ``nsw_lalonde()``           — LaLonde NSW job training (experimental subset)
> 📝 *``nsw_lalonde()`` — LaLonde NSW 就业培训（实验子集）*
    ``nsw_dw()``                — Dehejia-Wahba NSW + PSID comparison
> 📝 *``nsw_dw()`` — Dehejia-Wahba NSW + PSID 对比*

Synthetic control
> 📝 *合成控制*
    ``california_prop99()``     — ADH tobacco (re-exported from synth)
> 📝 *``california_prop99()`` — ADH 烟草（从 synth 重新导出）*
    ``basque_terrorism()``      — Abadie-Gardeazabal (re-exported)
> 📝 *``basque_terrorism()`` — Abadie-Gardeazabal（重新导出）*
    ``german_reunification()``  — ADH 2015 (re-exported)
> 📝 *``german_reunification()`` — ADH 2015（重新导出）*

Public health / epidemiology (REAL data)
> 📝 *公共卫生 / 流行病学（真实数据）*
    ``nhefs()``                 — Hernán-Robins *What If* NHEFS (g-methods
                                  canon: quit-smoking → weight / mortality)
> 📝 *``nhefs()`` — Hernán-Robins《What If》NHEFS（g-methods 经典案例：戒烟 → 体重/死亡率）*
    ``load_nhefs()``            — alias of ``nhefs()``
> 📝 *``load_nhefs()`` — ``nhefs()`` 的别名*

**5 个公共函数**

### `sp.basque_terrorism()`

**Basque Country terrorism dataset (simulated).**
> 📝 *巴斯克地区恐怖主义数据集（模拟）。*

**Example:**
> 📝 *示例：*

```python
# 加载巴斯克地区恐怖主义模拟数据集
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.basque_terrorism()
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/synth.md`

---
### `sp.from_fred()`

**Normalise FRED series observations (one or many series) into a tidy time series with parsed dates and NaN for '.' missings. No network call.**
> 📝 *将 FRED 序列观测值（一个或多个序列）规范化为整洁的时间序列，包含解析后的日期，并将 '.' 缺失值转为 NaN。不涉及网络调用。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `payload` | `array[string]` | ✓ |  | FRED 序列观测值响应数据，需已预先获取。 |

**Example:**
> 📝 *示例：*

```python
# 将 FRED 序列数据规范化为整洁时间序列
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.from_fred(payload=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/data_mcp_ingestion.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/data_mcp_ingestion.md`

---
### `sp.from_sdmx()`

**Expand an SDMX-JSON payload (OECD / Eurostat / IMF) into a long frame with one column per dimension plus a value column. No network call.**
> 📝 *将 SDMX-JSON 数据（OECD/Eurostat/IMF）展开为长格式数据框，每个维度一列加上一个值列。不涉及网络调用。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `payload` | `array[string]` | ✓ |  | SDMX-JSON（OECD/Eurostat/IMF）响应数据，需已预先获取。 |

**Example:**
> 📝 *示例：*

```python
# 将 SDMX-JSON 数据展开为长格式数据框
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.from_sdmx(payload=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/data_mcp_ingestion.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/data_mcp_ingestion.md`

---
### `sp.from_worldbank()`

**Normalise a World Bank Indicators payload (already fetched via a data MCP / REST) into a tidy long or wide panel ready for sp.feols / sp.cross_validate. No network call.**
> 📝 *将世界银行指标数据（已通过数据 MCP/REST 获取）规范化为整洁的长格式或宽格式面板，可直接用于 sp.feols/sp.cross_validate。不涉及网络调用。*

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `payload` | `array[string]` | ✓ |  | 世界银行指标 API v2/Data360 响应数据，需已预先获取。 |

**Example:**
> 📝 *示例：*

```python
# 将世界银行指标数据规范化为整洁面板格式
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.from_worldbank(payload=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/data_mcp_ingestion.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/data_mcp_ingestion.md`

---
### `sp.german_reunification()`

**German reunification dataset (simulated).**
> 📝 *德国统一数据集（模拟）。*

**Example:**
> 📝 *示例：*

```python
# 加载德国统一模拟数据集
import statspai as sp
import pandas as pd

# 加载或准备数据
df = sp.datasets.card_1995()  # 示例数据集

result = sp.german_reunification()
print(result.summary())
```

> 📁 See also: `docs/guides/synth.md`
> 📝 *中文翻译：* 📁 另见：`docs/guides/synth.md`

---
