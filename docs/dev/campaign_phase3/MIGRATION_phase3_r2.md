<!-- Round 2 rows. Families that already have a round-1 table (Time series,
Treatment effects, DiD and synthetic control, RD and IV, Spatial, survey and
structural): append the rows to that table. The other three families are new
tables. The section title's defect count moves from 125 to 174 (125 + 49). -->

### Time series

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| `sp.structural_break(method="bai-perron")` (default) | Bai-Perron sequential procedure (`mbreaks::dosequa`): global minimum segment, sup F(l+1\|l) critical values; `p_values` is `None`, new `critical_values` / `sequential_tests`; `min_segment` and `alpha` must be tabulated values | fixture dates unchanged; statistics on the Wald scale, p-values → critical values; other data can select different dates | — (the old procedure was not Bai-Perron) |
| `sp.structural_break` sup-F p-value | Hansen (1997) approximation (strucchange, Stata `estat sbsingle`) instead of a fixed-seed Monte Carlo | `r2_wn`: default p 0.2297329322069956 (= R); the Monte-Carlo value was within 0.03 | `pvalue_method="simulate"` |

### Treatment effects

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| `sp.policy_value` | (n, 1) `scores` or unequal lengths raise `ValueError` | mean(scores)·mean(policy) → `ValueError` | — (wrong number); pass `scores.ravel()` |

### RD and IV

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| `sp.rd2d` / `sp.boundary_rd` | port of R `rd2d`: pointwise effects, `rdbw2d` bandwidths, robust bias-corrected inference, WBATE headline; default `approach` `"distance"` → `"location"` | one pooled effect → five pointwise effects (0.446 … 1.357), WBATE 0.891 (SE 0.0903) on `rd_open_bd.csv` | none exactly; `approach="pooled"` gives one one-score effect (now via `sp.rdrobust`) |
| `sp.rd2d_bw` | returns a DataFrame of per-point bandwidths (= `rdbw2d`) instead of a float | float → DataFrame | — |
| `sp.rd_discrete` | `'bsd'` = `RDHonest`, `'bme'` / `'bm'` = `RDHonestBME`; `K=` ignored (`DeprecationWarning`); `model_info['discrete']` drops `n_left`, `bin_means`, `honest_ci`, adds `maximum_bias`, `bandwidth`, `eff_obs` | bsd M = .05, h = 5: SE 0.0113 → 0.1121; default CI [−34.5, 35.8] → [0.464, 1.216]; bm h = 4: 0.7271 → 1.4953 | — (old SEs understated by ~√(bin size)) |

### Spatial, survey and structural

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| `sp.malmquist` | EC = TE_{t+1}/TE_t (`efficiency="bc"`); M changes with it; TC unchanged | mean EC t→2 1.0653 → 1.0389; mean M t→2 1.0997 → 1.0730 | `efficiency="residual"` |
| `sp.zisf` JLMS efficiency | `efficiency(method="jlms")` and `model_info["mean_efficiency_jlms"]` are exp(−E[u\|ε]) | 0.81702 → 0.81279 | — (the old value was the BC number under the JLMS label) |
| `sp.mgwr` | PySAL mgwr search, kernel, SOC stop and bandwidth freeze; `tol` is the SOC threshold | Georgia bandwidths [93, 101, 156, 158] → [101, 101, 117, 157] | — (the old search matched no reference); `kernel_eps=1.0` with a small `tol` for GWmodel's kernel |

### Decomposition and QTE

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| `sp.melly_decompose`, `sp.machado_mata` | exact LP quantile regressions; midpoint grid (j − 0.5)/J, default `n_tau_qr` 99 → 100; averaged inverse CDF | counterfactual τ ≈ .1 1.49961 → 1.48117; τ ≈ .9 3.11162 → 3.12503 | — (the old QR was not a minimiser) |
| `sp.fairlie` | Jann's rank-matched sequential decomposition; new `detailed['se']` | educ 0.010457 → 0.009463 | — (the old algorithm was not Fairlie's) |
| `sp.mediation_decompose` (with covariates) | `nde`, `total`, `propn_mediated`: covariates at the overall mean | NDE 0.717658 → 0.770783 | `nde_old = cde + theta3*(mean(M\|A=0) - E[M\|A=0, c̄])` (not exposed) |
| `sp.mediation_decompose(inference="analytical")` (default) | delta-method `se` / `ci` returned | `None` → SEs (= `paramed` 9.5e-15) | — |
| `sp.dist_iv`, `sp.distributional_te`, `sp.qte(method="firpo_*")` with covariates | unpenalised Newton logit propensities | 5th–6th digit | — |

### ML causal inference

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| `sp.calibration_test` / `sp.test_calibration` | `grf::test_calibration` regression, HC3, grf's t against 0 with one-sided p; no `null` column; non-training rows raise; covariance chosen by `vce=` (result key `vcov_type`) | differential 0.180 → 1.187; mean 0.985 → 1.00297 | — (the old differential coefficient estimated b2 − b1) |
| `sp.rate` | grf AIPW scores, tie averaging, QINI `k/n` weights, rank-corrected SE; non-training `X` raises | AUTOC SE 0.0949 → 0.0725 (grf bootstrap 0.0744) | — |
| `sp.cate_eval` | same RATE operator as `sp.rate` | as `sp.rate` | — |
| `sp.average_treatment_effect(target_sample="overlap")` | grf R-learner OLS with intercept and HC3 | 1.12386 / 0.07687 → 1.12514 / 0.07968 | — |
| `sp.honest_variance` | `se` is the half-sample spread, not divided by √`n_splits` | 0.0038 (25 splits) → ≈ sd(tau)/√n | — (Monte-Carlo error of the average, not an SE) |
| `sp.blp_test` | CDDF weighted regression on an out-of-fold proxy; default `vce="HC1"` (result key `vcov_type`) | constant-effect DGP β2 ≈ 1.43, p ≈ 3e-52 → null DGP β2 0.137, p 0.29 | `proxy="in_sample"` for the in-sample proxy (the regression stays weighted); `vce="const"` for GenericML's default |
| `sp.gate_test` | GATES weighted regression when `y` / `treat` / `covariates` are given | ANOVA on predictions → GATES γ_k (= GenericML) | call without outcomes for the descriptive path (warns) |
| `sp.forest_diagnostics` on non-training rows | overlap reported as NaN with a warning | perfect overlap → NaN | — |
| `sp.ips` / `sp.snips` / `sp.doubly_robust` with `clip` | `clip` caps the weight only; `pi_b <= 0` raises | `clip=2` IPS 0.8496 → 1.1904 (obp) | — |
| `sp.snips` | delta-method SE (= `sp.ope.snips`) | 0.00039, against a bootstrap SE of 0.0174 (n = 2000) → delta-method SE | — |
| `sp.doubly_robust` with a 1-D policy | action vector read as actions, not probabilities | always action 2: 1.3054 → 0.8555 | — |
| `sp.dml_panel(include_time_fe=True)`, unbalanced or weighted | exact two-way within transform | 0.82050 → 0.81951 (DoubleML) | — |
| `sp.dml_model_averaging` / `sp.model_averaging_dml` | exact QP for K ≤ 12 learners | weights move ~1e-8 | — |

### Sensitivity, Mendelian randomization, transport and trial design

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| `sp.mi_estimate` / `MICEResult.combine` | Barnard–Rubin df with `dfcom`, full within covariance, t-based p / CI | x2 df 31.25 → 24.99 | pass estimates without `df_resid` to `combine` (large-sample df) |
| `sp.mediate_sensitivity` | Imai–Keele–Yamamoto / `medsens` | crossing ρ 0.558 → 0.487; ACME(−0.9) 0.852 → 1.533 | — (wrong formula) |
| `sp.calibrate_confounding_strength` | `sensemakr::ovb_bounds`; `dof=` required | k = 5 bias bound 0.0199 → 0.4640 | — |
| `sp.survival_sensitivity` | worst case moves toward the null for HR < 1 | log HR −0.4, SE 0.15: breakpoint None → 1.2 | — |
| `sp.unified_sensitivity` | `rho_max` honoured on both paths; default None = Oster's min(1, 1.3 R²); RR CI is EValue's interval | summary-path default 1.0 → 1.3 rule | `rho_max=1.0` |
| `sp.attrition_bounds(method="lee")` | Lee's quantile rule (= `sp.lee_bounds`) | (0.70358, 1.61981) → (0.71883, 1.60455) | — ; `trimming="exact"` for `leebounds` with exact thresholds |
| `sp.mr_bma` | Zuber et al. Bayes factor (IVW scaling, prior σ 0.5); `model_averaged_estimate` added | BIC weights → Bayes-factor posterior probabilities | `method="bic"` |
| `sp.mr_multivariable` | SE × max(1, RSE) | changes only when RSE < 1 | — |
| `sp.mr_mediation` | total effect SE from random-effects IVW (`sp.mr_ivw`) | fixed-effect SE → random-effects SE | — |
| `sp.grapple` | GRAPPLE robust profile score (Tukey) with its sandwich; `RuntimeWarning` on non-convergence | β 2.694 → 2.7197; SE 0.510 → 0.5520 | — (different estimator) |
| `sp.transport_weights_fn` / `sp.transport_generalize` | SE with w² (HC0) | 0.0864 → 0.1556 | — |
| `sp.identify_transport` | descendants of X no longer admissible | X→Z→Y, S→Z: formula → "not transportable" | — |
| `sp.randomize` | `randomizr` `complete_ra` rule within strata / over clusters; re-randomization keeps the design | old: odd-stratum misfits to a fixed arm (5 → 2 treated, 7 → 4) | — (draws differ for the same seed) |

### DiD and synthetic control

| Function | What changes | Old → new (example) | Old number, if you need it |
| --- | --- | --- | --- |
| no-covariate SCM fits (`solve_simplex_weights`: `sp.synth` equal-V, sensitivity tools, `conformal_synth`, `multi_outcome_synth`, `synth_experimental_design`) | exact active-set weights for identified problems | pre-RMSPE 0.17714 → 0.1771399093 (moves ~1e-7) | — |
| `sp.synth_loo` / `sp.synth_time_placebo` | `se` / `pvalue` NaN when T1 < 2 or SE ≤ 0 | last time placebo p 0.0 → NaN | — |
| `sp.conformal_synth` | Chernozhukov–Wüthrich–Zhu / `scinference` procedure | p 0.0556 → 0.444; CI (−inf, inf) at α 0.05 when T = 18 | — (the old procedure had no reference) |
| `sp.synth_power` / `sp.synth_mde` | rank-p rejection rule; centred null baseline | Prop. 99 power at δ = 0 1.0 → 0.0; MDE 0 → 10.9 | — (anti-conservative) |
| `sp.synth_survival` | exact solver; band [gap − q_hi, gap − q_lo], pointwise | weights off by 0.03 → exact | — |
| `sp.shift_share_political*` Rotemberg weights | GPSS weights (signed, sum to 1), = `bartik.weight::bw` | max \|α_k\| 0.447 → 0.702 | `abs_weight` column retained |
| `sp.shift_share_political` share-balance F | df1 = rank([1, S]) − 1 | F 0.924 → 1.143; p 0.490 → 0.357 | — |
| `sp.shift_share_political_panel` | exact two-way within transform (unbalanced panels); `cluster="twoway"` is Cameron–Gelbach–Miller; `cluster="shock"` is AKM; `first_stage_F` is a partial F | balanced-panel β and unit / time SEs unchanged | — (`"twoway"` was HC0 on unit × time cells) |
| `sp.synth_experimental_design().method` | `"abadie_zhao_2025"` → `"loo_sc_fit_ranking"` (label only) | — | — |
