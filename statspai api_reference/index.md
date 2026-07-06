# StatsPAI 完整 API 参考手册

> 📘 覆盖全部 **1,139** 个公共函数 | 版本:v1.20.0
>
> 使用方式:`import statspai as sp`,所有函数通过 `sp.xxx()` 调用。
>
> 本参考手册按方法论领域拆分为多个小文件,每个文件聚焦一个子包或一个字母范围。

## 📂 分文件目录

| 编号 | 文件 | 内容 | 函数数 | 大小 |
|------|------|------|--------|------|
| 01 | [01_did.md](01_did.md) | did | 59 | 101 KB |
| 01 | [01_dml.md](01_dml.md) | dml | 15 | 28 KB |
| 01 | [01_iv.md](01_iv.md) | iv | 20 | 36 KB |
| 01 | [01_matching.md](01_matching.md) | matching | 25 | 34 KB |
| 01 | [01_rd.md](01_rd.md) | rd | 54 | 68 KB |
| 01 | [01_synth.md](01_synth.md) | synth | 55 | 69 KB |
| 02 | [02_bcf.md](02_bcf.md) | bcf | 8 | 11 KB |
| 02 | [02_causal_discovery.md](02_causal_discovery.md) | causal_discovery | 21 | 23 KB |
| 02 | [02_causal_llm.md](02_causal_llm.md) | causal_llm | 14 | 15 KB |
| 02 | [02_deepiv.md](02_deepiv.md) | deepiv | 2 | 5 KB |
| 02 | [02_dose_response.md](02_dose_response.md) | dose_response | 5 | 7 KB |
| 02 | [02_forest.md](02_forest.md) | forest | 8 | 9 KB |
| 02 | [02_metalearners.md](02_metalearners.md) | metalearners | 23 | 24 KB |
| 03 | [03_fixest.md](03_fixest.md) | fixest | 4 | 10 KB |
| 03 | [03_gmm.md](03_gmm.md) | gmm | 2 | 4 KB |
| 03 | [03_imputation.md](03_imputation.md) | imputation | 3 | 4 KB |
| 03 | [03_multilevel.md](03_multilevel.md) | multilevel | 11 | 18 KB |
| 03 | [03_nonparametric.md](03_nonparametric.md) | nonparametric | 4 | 5 KB |
| 03 | [03_panel.md](03_panel.md) | panel | 13 | 18 KB |
| 03 | [03_regression.md](03_regression.md) | regression | 25 | 31 KB |
| 03 | [03_rlasso.md](03_rlasso.md) | rlasso | 10 | 13 KB |
| 03 | [03_selection.md](03_selection.md) | selection | 3 | 5 KB |
| 04 | [04_diagnostics.md](04_diagnostics.md) | diagnostics | 25 | 31 KB |
| 04 | [04_inference.md](04_inference.md) | inference | 24 | 32 KB |
| 04 | [04_mht.md](04_mht.md) | mht | 6 | 6 KB |
| 04 | [04_postestimation.md](04_postestimation.md) | postestimation | 12 | 12 KB |
| 04 | [04_power.md](04_power.md) | power | 12 | 13 KB |
| 04 | [04_robustness.md](04_robustness.md) | robustness | 12 | 13 KB |
| 05 | [05_bunching.md](05_bunching.md) | bunching | 8 | 12 KB |
| 05 | [05_decomposition.md](05_decomposition.md) | decomposition | 32 | 39 KB |
| 05 | [05_frontier.md](05_frontier.md) | frontier | 12 | 17 KB |
| 05 | [05_network.md](05_network.md) | network | 32 | 28 KB |
| 05 | [05_quasi.md](05_quasi.md) | quasi | 2 | 4 KB |
| 05 | [05_spatial.md](05_spatial.md) | spatial | 35 | 35 KB |
| 05 | [05_structural.md](05_structural.md) | structural | 12 | 19 KB |
| 05 | [05_timeseries.md](05_timeseries.md) | timeseries | 20 | 24 KB |
| 06 | [06_bartik.md](06_bartik.md) | bartik | 8 | 12 KB |
| 06 | [06_bayes.md](06_bayes.md) | bayes | 19 | 27 KB |
| 06 | [06_causal_impact.md](06_causal_impact.md) | causal_impact | 3 | 4 KB |
| 06 | [06_conformal_causal.md](06_conformal_causal.md) | conformal_causal | 19 | 22 KB |
| 07 | [07_epi.md](07_epi.md) | epi | 20 | 20 KB |
| 07 | [07_gformula.md](07_gformula.md) | gformula | 3 | 5 KB |
| 07 | [07_mediation.md](07_mediation.md) | mediation | 6 | 8 KB |
| 07 | [07_mendelian.md](07_mendelian.md) | mendelian | 38 | 40 KB |
| 07 | [07_msm.md](07_msm.md) | msm | 3 | 5 KB |
| 07 | [07_principal_strat.md](07_principal_strat.md) | principal_strat | 3 | 5 KB |
| 07 | [07_survival.md](07_survival.md) | survival | 12 | 12 KB |
| 07 | [07_target_trial.md](07_target_trial.md) | target_trial | 5 | 7 KB |
| 08 | [08_assimilation.md](08_assimilation.md) | assimilation | 3 | 8 KB |
| 08 | [08_bounds.md](08_bounds.md) | bounds | 9 | 15 KB |
| 08 | [08_bridge.md](08_bridge.md) | bridge | 2 | 6 KB |
| 08 | [08_causal.md](08_causal.md) | causal | 8 | 9 KB |
| 08 | [08_causal_rl.md](08_causal_rl.md) | causal_rl | 9 | 9 KB |
| 08 | [08_causal_text.md](08_causal_text.md) | causal_text | 4 | 9 KB |
| 08 | [08_dtr.md](08_dtr.md) | dtr | 2 | 4 KB |
| 08 | [08_experimental.md](08_experimental.md) | experimental | 9 | 10 KB |
| 08 | [08_fairness.md](08_fairness.md) | fairness | 6 | 7 KB |
| 08 | [08_interference.md](08_interference.md) | interference | 20 | 23 KB |
| 08 | [08_longitudinal.md](08_longitudinal.md) | longitudinal | 6 | 6 KB |
| 08 | [08_matrix_completion.md](08_matrix_completion.md) | matrix_completion | 2 | 4 KB |
| 08 | [08_multi_treatment.md](08_multi_treatment.md) | multi_treatment | 2 | 3 KB |
| 08 | [08_ope.md](08_ope.md) | ope | 5 | 6 KB |
| 08 | [08_policy_learning.md](08_policy_learning.md) | policy_learning | 9 | 10 KB |
| 08 | [08_proximal.md](08_proximal.md) | proximal | 13 | 14 KB |
| 08 | [08_qte.md](08_qte.md) | qte | 12 | 16 KB |
| 08 | [08_surrogate.md](08_surrogate.md) | surrogate | 3 | 6 KB |
| 08 | [08_tmle.md](08_tmle.md) | tmle | 11 | 17 KB |
| 08 | [08_transport.md](08_transport.md) | transport | 7 | 7 KB |
| 09 | [09_output.md](09_output.md) | output | 39 | 38 KB |
| 09 | [09_plots.md](09_plots.md) | plots | 8 | 8 KB |
| 10 | [10_crossval.md](10_crossval.md) | crossval | 2 | 5 KB |
| 10 | [10_dag.md](10_dag.md) | dag | 18 | 14 KB |
| 10 | [10_datasets.md](10_datasets.md) | datasets | 5 | 8 KB |
| 10 | [10_question.md](10_question.md) | question | 6 | 9 KB |
| 10 | [10_smart.md](10_smart.md) | smart | 27 | 29 KB |
| 10 | [10_survey.md](10_survey.md) | survey | 7 | 7 KB |
| 10 | [10_utils.md](10_utils.md) | utils | 32 | 23 KB |
| 10 | [10_workflow.md](10_workflow.md) | workflow | 3 | 7 KB |
| 11 | [11_censoring.md](11_censoring.md) | censoring | 2 | 2 KB |
| 11 | [11_core.md](11_core.md) | core | 1 | 1 KB |
| 11 | [11_fast.md](11_fast.md) | fast | 5 | 9 KB |
| 11 | [11_geolift.md](11_geolift.md) | geolift | 1 | 2 KB |
| 12 | [12_A-H.md](12_A-H.md) | 顶层公共函数 (Top-Level API) — A-H | 87 | 100 KB |
| 12 | [12_I-b.md](12_I-b.md) | 顶层公共函数 (Top-Level API) — I-b | 88 | 108 KB |
| 12 | [12_N-n.md](12_N-n.md) | 顶层公共函数 (Top-Level API) — N-n | 93 | 99 KB |
| 12 | [12_c.md](12_c.md) | 顶层公共函数 (Top-Level API) — c | 57 | 69 KB |
| 12 | [12_d.md](12_d.md) | 顶层公共函数 (Top-Level API) — d | 79 | 89 KB |
| 12 | [12_e-j.md](12_e-j.md) | 顶层公共函数 (Top-Level API) — e-j | 95 | 111 KB |
| 12 | [12_k-m.md](12_k-m.md) | 顶层公共函数 (Top-Level API) — k-m | 67 | 76 KB |
| 12 | [12_o-q.md](12_o-q.md) | 顶层公共函数 (Top-Level API) — o-q | 72 | 83 KB |
| 12 | [12_r.md](12_r.md) | 顶层公共函数 (Top-Level API) — r | 76 | 99 KB |
| 12 | [12_s-z.md](12_s-z.md) | 顶层公共函数 (Top-Level API) — s-z | 102 | 122 KB |
| 13 | [13_C-l.md](13_C-l.md) | 未分类函数 (Uncategorized) — C-l | 14 | 19 KB |
| 13 | [13_n-v.md](13_n-v.md) | 未分类函数 (Uncategorized) — n-v | 20 | 18 KB |

> 总计:**1915** 个函数文档,分布在 **94** 个文件中

---

## 🔍 按子包名称查找

| 子包 | 所属文件 |
|------|----------|
| `assimilation` | [08_assimilation.md](08_assimilation.md) |
| `bartik` | [06_bartik.md](06_bartik.md) |
| `bayes` | [06_bayes.md](06_bayes.md) |
| `bcf` | [02_bcf.md](02_bcf.md) |
| `bounds` | [08_bounds.md](08_bounds.md) |
| `bridge` | [08_bridge.md](08_bridge.md) |
| `bunching` | [05_bunching.md](05_bunching.md) |
| `causal` | [08_causal.md](08_causal.md) |
| `causal_discovery` | [02_causal_discovery.md](02_causal_discovery.md) |
| `causal_impact` | [06_causal_impact.md](06_causal_impact.md) |
| `causal_llm` | [02_causal_llm.md](02_causal_llm.md) |
| `causal_rl` | [08_causal_rl.md](08_causal_rl.md) |
| `causal_text` | [08_causal_text.md](08_causal_text.md) |
| `censoring` | [11_censoring.md](11_censoring.md) |
| `conformal_causal` | [06_conformal_causal.md](06_conformal_causal.md) |
| `core` | [11_core.md](11_core.md) |
| `crossval` | [10_crossval.md](10_crossval.md) |
| `dag` | [10_dag.md](10_dag.md) |
| `datasets` | [10_datasets.md](10_datasets.md) |
| `decomposition` | [05_decomposition.md](05_decomposition.md) |
| `deepiv` | [02_deepiv.md](02_deepiv.md) |
| `diagnostics` | [04_diagnostics.md](04_diagnostics.md) |
| `did` | [01_did.md](01_did.md) |
| `dml` | [01_dml.md](01_dml.md) |
| `dose_response` | [02_dose_response.md](02_dose_response.md) |
| `dtr` | [08_dtr.md](08_dtr.md) |
| `epi` | [07_epi.md](07_epi.md) |
| `experimental` | [08_experimental.md](08_experimental.md) |
| `fairness` | [08_fairness.md](08_fairness.md) |
| `fast` | [11_fast.md](11_fast.md) |
| `fixest` | [03_fixest.md](03_fixest.md) |
| `forest` | [02_forest.md](02_forest.md) |
| `frontier` | [05_frontier.md](05_frontier.md) |
| `geolift` | [11_geolift.md](11_geolift.md) |
| `gformula` | [07_gformula.md](07_gformula.md) |
| `gmm` | [03_gmm.md](03_gmm.md) |
| `imputation` | [03_imputation.md](03_imputation.md) |
| `inference` | [04_inference.md](04_inference.md) |
| `interference` | [08_interference.md](08_interference.md) |
| `iv` | [01_iv.md](01_iv.md) |
| `longitudinal` | [08_longitudinal.md](08_longitudinal.md) |
| `matching` | [01_matching.md](01_matching.md) |
| `matrix_completion` | [08_matrix_completion.md](08_matrix_completion.md) |
| `mediation` | [07_mediation.md](07_mediation.md) |
| `mendelian` | [07_mendelian.md](07_mendelian.md) |
| `metalearners` | [02_metalearners.md](02_metalearners.md) |
| `mht` | [04_mht.md](04_mht.md) |
| `msm` | [07_msm.md](07_msm.md) |
| `multi_treatment` | [08_multi_treatment.md](08_multi_treatment.md) |
| `multilevel` | [03_multilevel.md](03_multilevel.md) |
| `network` | [05_network.md](05_network.md) |
| `nonparametric` | [03_nonparametric.md](03_nonparametric.md) |
| `ope` | [08_ope.md](08_ope.md) |
| `output` | [09_output.md](09_output.md) |
| `panel` | [03_panel.md](03_panel.md) |
| `plots` | [09_plots.md](09_plots.md) |
| `policy_learning` | [08_policy_learning.md](08_policy_learning.md) |
| `postestimation` | [04_postestimation.md](04_postestimation.md) |
| `power` | [04_power.md](04_power.md) |
| `principal_strat` | [07_principal_strat.md](07_principal_strat.md) |
| `proximal` | [08_proximal.md](08_proximal.md) |
| `qte` | [08_qte.md](08_qte.md) |
| `quasi` | [05_quasi.md](05_quasi.md) |
| `question` | [10_question.md](10_question.md) |
| `rd` | [01_rd.md](01_rd.md) |
| `regression` | [03_regression.md](03_regression.md) |
| `rlasso` | [03_rlasso.md](03_rlasso.md) |
| `robustness` | [04_robustness.md](04_robustness.md) |
| `selection` | [03_selection.md](03_selection.md) |
| `smart` | [10_smart.md](10_smart.md) |
| `spatial` | [05_spatial.md](05_spatial.md) |
| `structural` | [05_structural.md](05_structural.md) |
| `surrogate` | [08_surrogate.md](08_surrogate.md) |
| `survey` | [10_survey.md](10_survey.md) |
| `survival` | [07_survival.md](07_survival.md) |
| `synth` | [01_synth.md](01_synth.md) |
| `target_trial` | [07_target_trial.md](07_target_trial.md) |
| `timeseries` | [05_timeseries.md](05_timeseries.md) |
| `tmle` | [08_tmle.md](08_tmle.md) |
| `transport` | [08_transport.md](08_transport.md) |
| `utils` | [10_utils.md](10_utils.md) |
| `workflow` | [10_workflow.md](10_workflow.md) |

> 顶层公共函数(A–Z)按首字母范围分块,见 `12_*.md`;未分类函数见 `13_*.md`。
