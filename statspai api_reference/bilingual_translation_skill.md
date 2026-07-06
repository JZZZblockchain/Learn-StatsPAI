# StatsPAI API 参考文档中英双语化规范

只编辑 `COMPLETE_API_REFERENCE.md`。翻译完后再运行 `python scripts/split_api_reference.py` 拆分。

---

## 规则 A：代码块纯中文注释

每个 ` ```python ` 块的第一行必须是纯中文注释，不夹杂任何英文。

```python
# 使用两阶段最小二乘法估计教育回报率，以大学距离作为工具变量
import statspai as sp
result = sp.iv("lwage ~ (educ ~ nearc4) + exper + expersq", data=df)
```

---

## 规则 B：所有英文文本下方放中文翻译

格式：`> 📝 *中文翻译*`

覆盖范围：
- 章节描述段落和 bullet list 每一项
- 每个 `### `sp.xxx()`` 下的 `**英文描述**` 行
- 参数表 Description 列中的英文描述
- 所有英文句子

示例：

```
## did

Difference-in-Differences (DID) module for StatsPAI.
> 📝 *双重差分（DID）模块。*

- Classic 2×2 DID (two groups, two periods)
> 📝 *经典 2×2 DID（两组、两期）*

**Unified IV estimation: 2SLS, LIML, Fuller, GMM, JIVE.**
> 📝 *统一工具变量估计：支持 2SLS、LIML、Fuller、GMM、JIVE 方法。*
```

### 参数表 Description 列翻译

在参数表末尾新增一列 `中文翻译`，将 Description 列的每一行英文翻译填入。不要插入额外行破坏表格结构。

```
| Parameter | Type | Required | Default | Description | 中文翻译 |
|-----------|------|----------|---------|-------------|----------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables. | 包含各变量的 pandas 数据框。 |
| `formula` | `string` | ✓ |  | R-style formula, e.g. 'y ~ x1 + x2'. | R 风格公式，如 'y ~ x1 + x2'。 |
| `robust` | `string (enum)` |  | `'nonrobust'` | Standard error type. | 标准误类型。 |
```

枚举选项的翻译同样放在该行的中文翻译列中：`'nonrobust' — 普通标准误、'hc0' — 异方差稳健…`

---

## 规则 E：保留原始 `sp.xxx()` 函数引用

原文中出现的 `sp.xxx()`、`:func:\`xxx\``、`:class:\`xxx\`` 等函数/类引用，翻译时**必须原样保留**，不得删除或改写。

```
# 原文：
**Structured output of :func:`cs_report`.**

# 错误翻译（删除了 :func:`cs_report`）：
> 📝 *结构化输出。*

# 正确翻译（保留原始引用）：
> 📝 *:func:`cs_report` 的结构化输出。*

# 原文：
**Alias for sp.iv(method='2sls').**

# 正确翻译：
> 📝 *sp.iv(method='2sls') 的别名。*
```

---

## 规则 C：`##` 章节标题采用"英文 — 中文"同行格式

```
## did — 双重差分

## iv — 工具变量

## rd — 断点回归
```

---

## 规则 D：计量术语缩写展开

首次出现时展开为 `缩写 (English Full Name, 中文翻译)`。同一章节内只展开一次。

| 缩写 | 英文全称 | 中文 |
|------|----------|------|
| 2SLS | Two-Stage Least Squares | 两阶段最小二乘法 |
| AFT | Accelerated Failure Time | 加速失效时间模型 |
| AIC | Akaike Information Criterion | 赤池信息准则 |
| AIPW | Augmented Inverse Probability Weighting | 增强逆概率加权 |
| ATE | Average Treatment Effect | 平均处理效应 |
| ATT | Average Treatment Effect on the Treated | 处理组平均处理效应 |
| BCF | Bayesian Causal Forest | 贝叶斯因果森林 |
| BIC | Bayesian Information Criterion | 贝叶斯信息准则 |
| CATE | Conditional Average Treatment Effect | 条件平均处理效应 |
| CEM | Coarsened Exact Matching | 粗化精确匹配 |
| CI | Confidence Interval | 置信区间 |
| DAG | Directed Acyclic Graph | 有向无环图 |
| DDD | Triple Differences | 三重差分 |
| DiD / DID | Difference-in-Differences | 双重差分 |
| DML | Double/Debiased Machine Learning | 双重/去偏机器学习 |
| DTR | Dynamic Treatment Regime | 动态治疗方案 |
| FE | Fixed Effects | 固定效应 |
| GARCH | Generalized Autoregressive Conditional Heteroskedasticity | 广义自回归条件异方差 |
| GMM | Generalized Method of Moments | 广义矩估计 |
| GRF | Generalized Random Forest | 广义随机森林 |
| HDFE | High-Dimensional Fixed Effects | 高维固定效应 |
| HR | Hazard Ratio | 风险比 |
| HTE | Heterogeneous Treatment Effect | 异质性处理效应 |
| IPW | Inverse Probability Weighting | 逆概率加权 |
| IRM | Interactive Regression Model | 交互回归模型 |
| ITE | Individual Treatment Effect | 个体处理效应 |
| IV | Instrumental Variables | 工具变量 |
| JIVE | Jackknife Instrumental Variables Estimator | 刀切法工具变量估计 |
| KM | Kaplan-Meier | Kaplan-Meier 估计 |
| LATE | Local Average Treatment Effect | 局部平均处理效应 |
| LIML | Limited Information Maximum Likelihood | 有限信息极大似然 |
| MCMC | Markov Chain Monte Carlo | 马尔可夫链蒙特卡洛 |
| MCP | Model Context Protocol | 模型上下文协议 |
| MHT | Multiple Hypothesis Testing | 多重假设检验 |
| MR | Mendelian Randomization | 孟德尔随机化 |
| MSM | Marginal Structural Model | 边际结构模型 |
| MTE | Marginal Treatment Effect | 边际处理效应 |
| OLS | Ordinary Least Squares | 普通最小二乘法 |
| OPE | Off-Policy Evaluation | 离线策略评估 |
| OR | Odds Ratio | 比值比 |
| PLR | Partially Linear Regression | 部分线性回归 |
| PSM | Propensity Score Matching | 倾向得分匹配 |
| QTE | Quantile Treatment Effect | 分位数处理效应 |
| RCT | Randomized Controlled Trial | 随机对照试验 |
| RD / RDD | Regression Discontinuity (Design) | 断点回归(设计) |
| RE | Random Effects | 随机效应 |
| RKD | Regression Kink Design | 断点拐点设计 |
| RR | Relative Risk / Risk Ratio | 相对风险 |
| SAR | Spatial Autoregressive Model | 空间自回归模型 |
| SCM | Synthetic Control Method | 合成控制法 |
| SDID | Synthetic Difference-in-Differences | 合成双重差分 |
| SDM | Spatial Durbin Model | 空间杜宾模型 |
| SE | Standard Error | 标准误 |
| SEM | Spatial Error Model | 空间误差模型 |
| SFA | Stochastic Frontier Analysis | 随机前沿分析 |
| SUTVA | Stable Unit Treatment Value Assumption | 稳定单元处理值假设 |
| TMLE | Targeted Maximum Likelihood Estimation | 目标最大似然估计 |
| TWFE | Two-Way Fixed Effects | 双向固定效应 |
| VAR | Vector Autoregression | 向量自回归 |
| WLS | Weighted Least Squares | 加权最小二乘法 |

---

## 禁止

- 不删除任何内容
- 不修改函数名、参数名、代码、表格结构、文件路径
- 不翻译反引号 `` ` `` 内的代码/变量名
