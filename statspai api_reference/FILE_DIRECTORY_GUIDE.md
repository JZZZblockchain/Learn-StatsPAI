# StatsPAI 目录文件说明 (File Directory Guide)

> StatsPAI v1.20.0 — Python 因果推断与应用计量经济学开源库
> 作者：Biaoyue Wang & Scott Rozelle (Stanford REAP)
> 许可证：MIT | DOI: [10.5281/zenodo.19933900](https://doi.org/10.5281/zenodo.19933900)

---

## 顶层文件 (Top-Level Files)

### 项目文档 (Project Documentation)

| 文件 | 说明 |
|---|---|
| [README.md](README.md) | **英文主文档**：项目介绍、安装说明、功能概览、文档/PyPI 链接 |
| [README_CN.md](README_CN.md) | **中文主文档**：与英文版对应的中文介绍 |
| [CHANGELOG.md](CHANGELOG.md) (579KB) | **完整更新日志**：涵盖所有版本的详细变更记录 |
| [CHANGELOG_GITHUB.md](CHANGELOG_GITHUB.md) | **旧版更新日志**：前身项目 "pyEconometrics" 的变更记录 |
| [MIGRATION.md](MIGRATION.md) (87KB) | **迁移指南**：版本间迁移 + 从 Stata/R 迁移到 StatsPAI 的完整说明 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | **贡献指南**：贡献类型、开发环境搭建、代码规范、PR 流程、署名政策 |
| [CONTRIBUTORS.md](CONTRIBUTORS.md) | **贡献者名单**：核心维护者和社区贡献者 |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | **行为准则**：Contributor Covenant 开源社区行为规范 |
| [SECURITY.md](SECURITY.md) | **安全策略**：支持的版本、私有漏洞报告方式 |
| [SUPPORT.md](SUPPORT.md) | **支持方式**：通过 GitHub Discussions、Issues 或邮件获取帮助 |
| [CITATION.cff](CITATION.cff) | **引用元数据**：CFF 格式，方便学术引用 |
| [LICENSE](LICENSE) | **MIT 开源许可证** |
| [paper.md](paper.md) | **JOSS 论文**：提交给 Journal of Open Source Software 的项目论文 |
| [paper.bib](paper.bib) (188KB) | **论文参考文献**：BibTeX 格式的参考文献库 |

### 构建与配置 (Build & Configuration)

| 文件 | 说明 |
|---|---|
| [pyproject.toml](pyproject.toml) | **Python 构建配置**：setuptools 后端，定义依赖（numpy, pandas, scipy, statsmodels, numba 等）、CLI 入口点、可选依赖组 |
| [mkdocs.yml](mkdocs.yml) | **文档站点配置**：MkDocs Material 主题的完整配置 |
| [MANIFEST.in](MANIFEST.in) | **PyPI 分发包控制**：指定源码分发包中包含/排除的文件 |
| [.gitignore](.gitignore) | **Git 忽略规则**：标准 Python + 项目特定的忽略规则 |
| [.pre-commit-config.yaml](.pre-commit-config.yaml) | **Pre-commit 钩子**：black/isort 格式化、flake8 检查、导入守卫、schema 检查 |
| [.codespellrc](.codespellrc) | **拼写检查配置**：带领域特有忽略列表（计量经济学缩写词） |
| [.flake8](.flake8) | **Flake8 配置**：max-line-length=88，与 black 保持一致的排除规则 |
| [.zenodo.json](.zenodo.json) | **Zenodo 存档元数据**：DOI 注册信息 |
| [test_results_full_suite.md](test_results_full_suite.md) | **完整测试结果报告**：约 5200+ 测试通过、98 跳过、各批次耗时 |

---

## 顶层目录 (Top-Level Directories)

### `src/` — 主包源代码 (Main Package Source)

包含唯一的 Python 包 `src/statspai/`，所有功能通过 `import statspai as sp` 统一调用。

#### 核心入口与基础设施

| 文件 | 说明 |
|---|---|
| [src/statspai/\_\_init\_\_.py](src/statspai/__init__.py) (78KB) | **主入口**：通过延迟加载 + 冲突名提前导入导出所有公共 API。所有 `sp.xxx()` 调用都经过此文件 |
| [src/statspai/\_\_init\_\_.pyi](src/statspai/__init__.pyi) (63KB) | **类型存根**：IDE 自动补全和类型检查支持 |
| [src/statspai/registry.py](src/statspai/registry.py) (613KB) | **函数注册表**：为每个公共函数提供机器可读的 JSON Schema 兼容元数据，支撑 `sp.list_functions()` / `sp.describe_function()` / `sp.search_functions()` / `sp.function_schema()`，专为 AI Agent 消费设计 |
| [src/statspai/validation.py](src/statspai/validation.py) | **验证报告**：生成结构化 `ValidationReport` 对象，包含证据、注册表统计、外部基准（Stata/R）交叉检验 |
| [src/statspai/cli.py](src/statspai/cli.py) | **命令行界面**：`statspai list` / `statspai describe` / `statspai search` / `statspai help` / `statspai version` |
| [src/statspai/help.py](src/statspai/help.py) | **帮助系统**：API 帮助文档的底层实现 |
| [src/statspai/exceptions.py](src/statspai/exceptions.py) | **自定义异常体系**：为 Agent 消费设计的语义化错误处理 |
| [src/statspai/parity.py](src/statspai/parity.py) | **一致性验证基础设施**：与外部软件（Stata/R）结果比对 |
| [src/statspai/\_parity_index.json](src/statspai/_parity_index.json) (202KB) | **一致性索引数据**：函数到验证状态的映射 |
| [src/statspai/\_baseline_cards.py](src/statspai/_baseline_cards.py) | **基线 Agent 卡片定义** |
| [src/statspai/\_agent_cards_extra.py](src/statspai/_agent_cards_extra.py) (183KB) | **扩展 Agent 卡片数据**：基线之外的额外卡片 |
| [src/statspai/\_causal_family_seeds.py](src/statspai/_causal_family_seeds.py) | **因果族模板种子数据**：注册表中因果族的模板定义 |
| [src/statspai/\_auto_estimators.py](src/statspai/_auto_estimators.py) | **自动估计器调度**：根据数据特征自动选择合适的估计方法 |
| [src/statspai/\_article_aliases.py](src/statspai/_article_aliases.py) | **期刊文章别名**：AER 等期刊风格的列命名约定映射 |
| `_citation.py`, `_house_style.py`, `_input_validation.py`, `_result_serialize.py`, `_schema_export.py` | **支撑基础设施**：引用、风格、输入验证、结果序列化、Schema 导出 |
| `_agent_docs.py`, `_aliases.py`, `_canonical_aliases.py` | **更多支撑模块**：Agent 文档、别名系统、规范别名 |
| [src/statspai/py.typed](src/statspai/py.typed) | **PEP 561 标记**：标明该包附带类型存根 |

#### 方法子包 (Method Subpackages)

StatsPAI 拥有 **80+ 个子包**，涵盖现代因果推断的完整领域：

| 子包 | 功能领域 | 包含方法举例 |
|---|---|---|
| `agent/` | Agent 原生接口 & MCP 集成 | LLM Agent 调用协议、模型上下文协议 |
| `assimilation/` | 同化因果推断 | 同化方法 |
| `bartik/` | Bartik / Shift-Share 工具变量 | Bartik 工具变量构造与估计 |
| `bayes/` | 贝叶斯计量 | Bayesian IV, fuzzy RD, HTE, MTE 采样器 |
| `bcf/` | 贝叶斯因果森林 | BCF 模型 |
| `bounds/` | 部分识别边界 | Manski 边界等 |
| `bridge/` | 估计量桥接定理 | 不同因果估计量之间的桥接 |
| `bunching/` | 聚束估计 | Bunching / Kink 设计 |
| `causal/` | **核心因果推断** | `causal_question`, `identify()`, 估计量框架 |
| `causal_discovery/` | 因果发现算法 | PC, GES, FCI, NOTEARS, LLM 辅助 DAG |
| `causal_impact/` | 因果影响 / 中断时间序列 | 贝叶斯结构时间序列 |
| `causal_llm/` | LLM 驱动的因果推理 | 自然语言构建 DAG |
| `causal_rl/` | 因果强化学习 / 策略学习 | 最优策略学习 |
| `causal_text/` | 文本因果推断 | 文本作为处理/结果/混杂因子 |
| `censoring/` | 删失数据 & 竞争风险 | 删失回归、竞争风险模型 |
| `checks/` | 数据验证 & 诊断检查 | 输入数据校验 |
| `compat/` | Stata/R 兼容层 | Stata/R 语法映射 |
| `conformal_causal/` | 处理效应 conformal 推断 | Conformal 预测区间 |
| `core/` | **核心结果对象** | `CausalResult`, `EconometricResults`, `EffectSummary` |
| `crossval/` | 交叉验证 | 交叉引擎验证 |
| `dag/` | DAG 工具 | 有向无环图工具集 |
| `datasets/` | 内置示例数据集 | 练习用数据集 |
| `decomposition/` | 方差/不平等分解 | Oaxaca-Blinder, Shapley 等 |
| `deepiv/` | 深度工具变量 | 神经网络 IV |
| `diagnostics/` | **诊断工具** | Kitagawa, Rosenbaum bounds, E-value, 弱 IV 检验, Hausman, McCrary |
| `did/` | **双重差分** | 经典 2x2, staggered (CSDID, Sun-Abraham), 连续 DiD, honest DiD |
| `dml/` | **双重/去偏机器学习** | DoubleML |
| `dose_response/` | 剂量-反应 / 连续处理效应 | 连续处理效应估计 |
| `dtr/` | 动态治疗方案 | DTR 方法 |
| `epi/` | 流行病学方法 | 关联度量、目标试验模拟 |
| `experimental/` | 实验设计 & A/B 测试 | 随机化推断、样本量计算 |
| `fairness/` | 因果模型公平性 | 算法公平性评估 |
| `fast/` | 高性能实现 | 加速计算 |
| `fixest/` | 固定效应估计 | 受 R fixest 启发 |
| `forest/` | 因果森林 / 广义随机森林 | GRF |
| `frontier/` | 随机前沿分析 | SFA |
| `geolift/` | GeoLift / 地理实验 | 地理随机化实验 |
| `gformula/` | G-formula / G-computation | G 公式 |
| `gmm/` | 广义矩估计 | GMM |
| `imputation/` | 缺失数据插补 | 多种插补方法 |
| `inference/` | 推断方法 | 标准误、置信区间 |
| `interference/` | 干扰下的因果推断 | SUTVA 违背处理 |
| `iv/` | **工具变量** | 2SLS, JIVE, 弱 IV, MTE, 贝叶斯 IV, 非参数 IV, 近似外生性 |
| `longitudinal/` | 纵向/面板方法 | 纵向数据分析 |
| `matching/` | **匹配方法** | PSM, CEM, 遗传匹配, 倾向得分 |
| `matrix_completion/` | 矩阵补全因果推断 | 矩阵补全方法 |
| `mediation/` | 因果中介分析 | 中介效应 |
| `mendelian/` | 孟德尔随机化 | 遗传工具变量 |
| `metalearners/` | 元学习器 | S/T/X/R/DR learners |
| `mht/` | 多重假设检验校正 | 多重比较校正 |
| `msm/` | 边际结构模型 | MSM |
| `multi_treatment/` | 多值处理效应 | 多处理水平 |
| `multilevel/` | 多层/分层/混合效应模型 | 混合效应模型 |
| `network/` | 网络计量 | 特征向量中心性等 |
| `neural_causal/` | 神经因果模型 | Dragonnet, TARNet, CEVAE |
| `nonparametric/` | 非参数估计 | 核回归等 |
| `ope/` | 离线策略评估 | OPE |
| `output/` | **结果导出** | LaTeX, Word, Excel, Markdown 表格 (`outreg2`, `modelsummary` 等价物) |
| `panel/` | 面板数据模型 | FE, RE 等 |
| `plots/` | **可视化** | 事件研究图, RD 图, love plot, SCM 轨迹图 |
| `policy_learning/` | 策略学习 | 最优策略树 |
| `postestimation/` | 估计后处理 | margins, predictions, contrasts |
| `power/` | 功效分析 & 样本量计算 | 统计功效 |
| `principal_strat/` | 主分层 | 主分层方法 |
| `proximal/` | 近端因果推断 | 近端方法 |
| `qte/` | 分位数处理效应 | QTE |
| `quasi/` | 准实验方法 | 准实验设计 |
| `question/` | 研究问题规范 | 因果问题 DSL |
| `rd/` | **断点回归** | Sharp, Fuzzy, RDD, RKD, 空间 RD |
| `regression/` | **回归** | OLS, WLS, logit, probit (`regress()` 函数) |
| `rlasso/` | 严谨 Lasso | Post-double-selection, partialling-out |
| `robustness/` | **稳健性检验** | 安慰剂检验, Oster bounds, Conley SE, 规范曲线, 敏感性分析 |
| `schemas/` | JSON Schema | 结果对象和函数元数据的 JSON Schema |
| `selection/` | 样本选择模型 | Heckman 两步法等 |
| `smart/` | SMART 设计 | 序贯多分配随机试验 |
| `spatial/` | **空间计量** | SAR, SEM, SDM, SLX |
| `structural/` | 结构估计 | 结构方程模型 |
| `surrogate/` | 替代指标方法 | 替代指标 |
| `survey/` | 调查数据分析 | 复杂抽样设计 |
| `survival/` | **生存分析** | KM, Cox, AFT, 竞争风险 |
| `synth/` | **合成控制 & 合成 DiD** | SCM, SDID |
| `target_trial/` | 目标试验模拟 | 观察数据模拟 RCT |
| `timeseries/` | 时间序列计量 | 时间序列方法 |
| `tmle/` | 目标最大似然估计 | TMLE |
| `transport/` | 可迁移性 / 可推广性 | 效应外推 |
| `utils/` | 工具函数 | 内部辅助工具 |
| `workflow/` | 可复现研究工作流 | 论文流水线、复现包 |

---

### `tests/` — 测试套件 (Test Suite)

**约 5200+ 测试**，是项目质量保证的核心。

#### 顶层测试文件

超过 50 个独立测试文件，覆盖所有方法领域的单元测试和集成测试。

#### 测试子目录

| 子目录 | 说明 |
|---|---|
| `agent_bench/` | **Agent 基准测试**：提示词、标准答案、运行器、结果评估 |
| `agent_eval/` | **Agent 评估**：DID 工作流对话记录、MCP 协议对话记录 |
| `coverage_monte_carlo/` | **蒙特卡洛覆盖度/检验水平/功效研究**：统计性质的 MC 模拟验证 |
| `external_parity/` | **外部发布值验证**：与 CausalML 书籍、DoubleML、honest DID 论文、NHEFS 等对比 |
| `fixtures/` | **测试数据**：NIST StRD (统计参考数据集)、HTZ 面板数据等 |
| `golden_master/` | **Golden Master / 快照测试**：回归输出的一致性快照验证 |
| `integration/` | **集成测试**：因果 MAS (带模拟 LLM) |
| `iv/` | **IV 专项测试**：贝叶斯 IV、弱工具变量、MTE、非参数 IV 等 |
| `numerical_accuracy/` | **数值精度测试**：精度边界验证 |
| `orig_parity/` | **原始一致性测试**：初版一致性验证 |
| `output_snapshots/` | **输出快照测试**：HTML、LaTeX、Markdown、纯文本表格渲染验证 |
| `panel/` | **面板数据测试**：面板模型专项 |
| `perf/` | **性能回归测试**：性能退化检测 |
| `r_parity/` | **R 语言交叉验证**：与 R 输出对比 |
| `reference_parity/` | **参考一致性测试**：参照值验证 |
| `spatial/` | **空间计量测试**：空间模型专项 |
| `stata_parity/` | **Stata 交叉验证**：与 Stata 输出对比 |

---

### `docs/` — 文档站点 (Documentation Site)

基于 MkDocs Material 主题构建。

| 文件 | 说明 |
|---|---|
| `index.md` | **文档首页** |
| `getting-started.md` | **入门指南** |
| `cookbook.md` | **实用手册**：常见分析任务的代码配方 |
| `faq.md` | **常见问题** |
| `stats.md` | **统计方法论**：底层统计学原理 |
| `parity.md` | **一致性文档**：与 Stata/R 的比对方法及结果 |
| `agent_cards_spec.md` | **Agent 卡片规范** |
| `ROADMAP.md` | **项目路线图** |
| `changelog.md` | **文档版更新日志** |
| `joss_reviewer_guide.md` | **JOSS 审稿人指南** |
| `joss_reviewer_qa.md` | **JOSS 审稿 Q&A** |
| `joss_validation_dossier.md` | **JOSS 验证档案** |
| `jss_source_audit_dossier.md` | **JSS 源码审计档案** |
| `guides/` (~60 个文件) | **方法指南**：agent API, DID, IV, RD, DML, matching, synth, survival, mediation, Mendelian, panel, causal RL, causal text, conformal, spatial, G-methods, target trials, 复现工作流, 表格导出等 |
| `reference/` (20+ 个文件) | **API 参考**：按方法族的完整 API 文档 |
| `rfc/` (10 个文件) | **设计 RFC & 交接文档**：连续 DiD, DID 路线图, 输出整合, vcov, multiplegt_dyn, HAL-TMLE, 导入优化等 |
| `dev/` | **开发者文档**：agent 基础设施、grammar/SE 菜单路线图、一致性差距清单、R 一致性容差 |
| `superpowers/plans/` | **详细计划**：HTZ clubsandwich 一致性、Rust 加权 demeaning (Phase A)、Rust IRLS (Phase B) |
| `superpowers/specs/` (20 个文件) | **全栈设计规范**：decomposition, MTE 变体, auto-CATE, 贝叶斯方法, spatial, agent-native 设计, Rust IRLS/FEPois 等 |

---

### `examples/` — 示例代码 (Examples)

| 文件 | 说明 |
|---|---|
| `README.md` | 示例概览 |
| `card_iv.py` | Card (1995) IV 分析示例 |
| `did_mpdta.py` | Callaway & Sant'Anna DiD 示例 |
| `dml_card.py` | DoubleML 示例 |
| `gmethods_timevarying.py` | 时变处理 G-methods 示例 |
| `nhefs_whatif.py` | NHEFS 数据集 What-If 分析 |
| `rd_lee.py` | Lee (2008) RD 分析示例 |
| `synth_prop99.py` | 加州 Prop 99 合成控制示例 |
| `notebooks/reproduce_401k_doubleml.ipynb` | 401(k) DoubleML 复现 Jupyter 笔记本 |

---

### `scripts/` — 开发与质量控制脚本 (Development & QA Scripts)

共 20+ 个脚本，用于自动化开发流程。

| 脚本 | 说明 |
|---|---|
| `build_parity_index.py` (79KB) | **构建一致性索引**：从所有估计器模块生成 parity index JSON |
| `build_replication_notebooks.py` | **生成复现笔记本**：自动生成复现 Jupyter 笔记本 |
| `agent_card_coverage.py` | **Agent 卡片覆盖率检查**：检查哪些函数有对应 agent card |
| `agent_workflow_spec_audit.py` | **Agent 工作流规范审计** |
| `benchmark_ratchet.py` | **性能基准棘轮**：性能回归检测 |
| `check_contract_inventory.py` | **合同清单验证** |
| `check_example_execution.py` | **示例可执行性验证** |
| `coverage_campaign.py` | **覆盖率提升活动** |
| `dump_schemas.py` | **导出 JSON Schemas**：导出到 schemas/ 目录 |
| `error_taxonomy_audit.py` | **错误分类审计**：错误分类体系完整性 |
| `examples_coverage.py` | **示例覆盖率度量** |
| `failure_mode_audit.py` | **失败模式审计**：各估计器的失败模式 |
| `gen_api_ref.py` | **生成 API 参考文档** |
| `gen_baseline_cards.py` | **生成基线 Agent 卡片** |
| `generate_stub.py` | **生成 .pyi 类型存根** |
| `help_coverage.py` | **帮助覆盖率度量** |
| `quality_gate.py` | **CI 质量门**：flake8/mypy 计数棘轮机制 |
| `registry_stats.py` | **注册表统计** |
| `result_protocol_audit.py` | **结果对象协议审计** |
| `schema_quality.py` | **Schema 质量检查** |
| `se_menu_matrix.py` | **标准误选择矩阵** |
| `section3_contract_audit.py` | **Section 3 合同审计** |
| `signature_house_style.py` | **函数签名风格一致性** |
| `stability_audit.py` | **跨版本稳定性审计** |
| `sync_agent_blocks.py` | **同步 Agent 块定义** |
| `tier_a_fixture_lock.py` | **锁定 Tier A 测试数据** |
| `tierd_classify.py` | **Tier-D 函数分类** |
| `api_surface_diff.py` | **API 表面差异比较** |
| `_resolve.py` | **共享路径解析工具** |

---

### `tools/` — 引用与文献审计工具 (Citation & Bibliography Audit)

| 脚本 | 说明 |
|---|---|
| `audit_citations.py` (55KB) | **综合引用审计**：检查代码中引用的完整性 |
| `audit_bib_coverage.py` | **文献覆盖率检查** |
| `audit_bib_duplicates.py` | **重复 BibTeX 条目检测** |
| `audit_retractions.py` | **撤稿论文检查**：检测已被撤稿的引用文献 |
| `suggest_bibkey_backfills.py` | **缺失 BibTeX 键补充建议** |

---

### `benchmarks/` — 性能基准测试 (Performance Benchmarks)

| 文件/目录 | 说明 |
|---|---|
| `README.md`, `RESULTS.md` | 基准测试文档 |
| `_utils.py`, `baseline.json`, `results.json` | 基准测试基础设施与基线数据 |
| `bench_did.py`, `bench_hdfe.py`, `bench_hdfe_scaled.py`, `bench_regression.py` | **微基准测试**：DiD, HDFE, 回归性能 |
| `run_all.py` | **运行全部基准**的编排脚本 |
| `cross_library/` | **跨库 HDFE 基准**：Python vs. R vs. Stata 性能对比 |
| `hdfe/` (20+ 个文件) | **详尽 HDFE 基准**：数据集、分阶段验证、R 和 Stata 参考运行器 |
| `recommend_hit_rate/` | **推荐命中率评估**：语料库与记分卡 |

---

### `rust/` — Rust 原生扩展 (Rust Native Extensions)

高性能 HDFE 固定效应操作的 Rust 实现。

| 文件 | 说明 |
|---|---|
| `README.md` | Rust crate 概述 |
| `statspai_hdfe/Cargo.toml` | Rust crate 定义 |
| `statspai_hdfe/Cargo.lock` | 依赖锁定文件 |
| `statspai_hdfe/src/lib.rs` (29KB) | **主 Rust 库**：Python 绑定层 (`#[pyfunction]`) |
| `statspai_hdfe/src/demean.rs` (32KB) | **加权组内变换 (demeaning)**：高性能固定效应消去 |
| `statspai_hdfe/src/irls.rs` (23KB) | **迭代重加权最小二乘 (IRLS)** |
| `statspai_hdfe/src/separation.rs` | 分离检测 |
| `statspai_hdfe/src/singletons.rs` | 单例组处理 |
| `statspai_hdfe/src/cluster.rs` | 聚类标准误 |
| `statspai_hdfe/src/cholesky.rs` | Cholesky 分解 |
| `statspai_hdfe/src/sort_perm.rs` | 排序置换 |

---

### `schemas/` — JSON Schemas (供 AI Agent 消费)

| 文件 | 说明 |
|---|---|
| `agent_cards.json` (1.4MB) | **全部 Agent 卡片** JSON 格式 |
| `functions.json` (1.7MB) | **全部函数元数据/Schema** JSON 格式 |
| `tools.json` (926KB) | **工具定义** 供 Agent 使用 |
| `index.json` | **Schema 索引** |
| `result.schema.json` | **`CausalResult` 的 JSON Schema** |

---

### `papers/` — 论文复现数据与脚本 (Paper Replication)

| 文件 | 说明 |
|---|---|
| `StasPAI-paper-axiv.md` | **论文草稿** (arXiv 格式) |
| `data_card1995.csv` | Card (1995) 复现数据 |
| `data_lalonde.csv` | LaLonde 复现数据 |
| `data_nsw_dw.csv`, `data_nsw_experimental.csv` | NSW 实验数据 |
| `paper.bib` | **论文参考文献** |
| `run_experiments.py` | **实验运行脚本** |
| `run_real_data_replication.py` | **真实数据复现脚本** |
| `run_replication.py` | **复现执行脚本** |

---

### `StatsPAI_full_data_analysis_skill/` — Claude Code 技能 (Claude Code Skill)

教 AI 助手如何端到端驱动 StatsPAI 完成完整实证分析。

| 文件 | 说明 |
|---|---|
| `SKILL.md` (146KB) | **技能主体定义**：操作策略、模式路由、产出关卡、AER/经济/流行病学/ML-因果模式的完整工作流 |
| `README.md` | **技能概览与使用文档** |
| `EVALS.md` | **技能评估标准** |
| `validate_api_claims.py` | **API 声明验证**：验证技能中的 API 声明与实际代码库一致 |

---

### `plans/` — 开发计划文档 (Development Planning)

包含带日期的计划文件和方法子目录：

- 顶层计划：spatial 核心设计 (2026年4月)、综合改进路线图、R/Stata 一致性路线图、一致性/性能工作日志、输出硬化、经济学者 MCP 工作流硬化、JOSS 安全经济学者 MCP 硬化
- 子目录：agent 实证分析提升、agent 运行时编排器、因果推断正确性遍历、CausalPy 设计遍历、CausalPy 启发合约、StatsPAI 硬化月

---

### `specs/` — 技术规范文档 (Technical Specifications)

| 文件 | 说明 |
|---|---|
| `2026-04-15-sp-01-spatial-full-stack-design.md` | **空间计量全栈设计规范** |
| `2026-04-15-statspai-ecosystem-gap-analysis.md` | **生态系统差距分析**：与同类工具的对比分析 |

---

### `test-notebooks/` — 测试 Notebook

| 文件 | 说明 |
|---|---|
| `demo_causal_inference.ipynb` (155KB) | **因果推断完整演示**：涵盖整个因果推断工作流的综合性 Jupyter 笔记本 |

---

### `.github/` — GitHub 配置

| 文件/目录 | 说明 |
|---|---|
| `ISSUE_TEMPLATE/bug_report.md` | Bug 报告模板 |
| `ISSUE_TEMPLATE/feature_request.md` | 功能请求模板 |
| `ISSUE_TEMPLATE/config.yml` | Issue 模板配置 |
| `dependabot.yml` | Dependabot 自动依赖更新配置 |
| `workflows/ci-cd.yml` (19.7KB) | **主 CI/CD 流水线** |
| `workflows/build-wheels.yml` | Wheel 构建发布工作流 |
| `workflows/parity-guards.yml` | 一致性守卫检查 |
| `workflows/r-parity.yml` | R 一致性测试 |
| `workflows/benchmarks.yml` | 性能基准运行器 |
| `workflows/citation-audit.yml` | 引用审计自动化 |
| `workflows/docs.yml` | 文档构建与部署 |
| `workflows/recommend-benchmark.yml` | 推荐系统基准 |
| `workflows/retraction-sweep.yml` | 撤稿扫描 |

---

### Campaign 目录 (内部开发跟踪)

这些是隐藏目录（以 `.` 开头），用于内部开发进度跟踪：

| 目录 | 说明 |
|---|---|
| `.cov_decomp/DECOMP_CAMPAIGN.md` | 分解覆盖率提升活动 |
| `.coverage_campaign/CAMPAIGN.md` | 通用覆盖率提升活动 |
| `.examples_campaign/CAMPAIGN.md + worklist.md` | 示例硬化活动 |
| `.tier_eg_campaign/CAMPAIGN.md` | Tier 示例生成活动 |
| `.tierd_campaign/CAMPAIGN.md + worklist.md` | Tier-D 分类活动 |

---

## 总结

StatsPAI 是一个成熟的大型 Python 项目，拥有：

- **80+ 方法子包**，覆盖现代因果推断的全领域
- **约 5200+ 测试**，包含与 Stata、R 和已发表文献的广泛一致性验证
- **Rust 原生扩展**，用于性能关键的 HDFE 操作（加权 demeaning、IRLS）
- **全面文档**：60+ 用户指南 + 20+ API 参考
- **AI Agent 支持**：函数注册表、JSON Schema、Agent 卡片、完整 Claude Code 技能
- **可复现研究工具链**：Word/Excel/LaTeX 导出、复现包

访问 [https://pypi.org/project/statspai/](https://pypi.org/project/statspai/) 安装使用。
