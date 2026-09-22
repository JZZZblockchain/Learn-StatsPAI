Cross-language parity campaign, phase 3, round 2. Estimator callables with a
cross-language (R / Stata) grade went from 362 to 415 of 773 (46.8% → 53.7%).
The round fixed 49 defects: time series 1, spatial / structural (frontier,
MGWR) 4, treatment effects 1, RD 2, decomposition and QTE 8, ML causal
inference (grf operators, CDDF, off-policy evaluation, DML) 13, sensitivity /
Mendelian randomization / transport / trial design 13, synthetic-control
tools and shift-share 7 (counted as in round 1: each numbered item once;
convention changes and docstring-, label- and citation-only corrections not
counted). Each was found by running the named R, Stata or Python reference
on the same data, or while building that comparison. None was caught by the
existing unit tests. See [MIGRATION.md](MIGRATION.md#parity-campaign-phase3).

### ⚠️ Correctness

**Time series**

- **`sp.structural_break(method="bai-perron")`, the default, was not the
  Bai-Perron sequential procedure.** It was a binary segmentation: each
  segment used its own relative trimming `int(seg_len·min_segment)` instead
  of the global h = floor(ε·T), the candidate range dropped the last
  admissible date, and every step was referred to the full-sample sup-F(1|0)
  law (the Monte-Carlo p-value at `alpha`) instead of Bai-Perron's
  sup F(l+1|l) critical values, which grow with l. It is now a transcription
  of `mbreaks::dosequa` (`prewhit=0, robust=0, hetdat=1, hetvar=0`), with
  the critical-value tables asserted equal to `mbreaks::supF_next_cv1..5`.
  Break dates are identical to `dosequa` in 6 series × 4 levels, and every
  step statistic equals the traced `mbreaks:::pftest` value (observed
  ~1e-14). On the fixtures the dates did not move; only the reported
  statistics change (F scale → Wald scale, p-values → critical values). On
  other data the old per-segment trimming and full-sample null can select
  different dates. `p_values` is now `None`; results carry `f_stats`,
  `critical_values` and `sequential_tests`. The old procedure is not
  reachable.
- **`sp.structural_break` sup-F p-value: Hansen (1997) by default.** The
  default was a fixed-seed Monte-Carlo approximation of the Andrews law
  (1/5001 resolution, grid-dependent). It is now Hansen's (1997)
  approximation, the one strucchange, Stata `estat sbsingle` and the
  method's author use: p against `strucchange::sctest(type="supF")` 3.7e-13
  on a 54-point grid, against Stata `pvalsup()` ≤ 2.7e-11. On `r2_wn` the
  default p is 0.2297329322069956 (R 0.22973293220700686).
  `pvalue_method="simulate"` returns the old Monte-Carlo value. This is a
  convention change, not counted as a defect.

**Spatial, survey and structural**

- **`sp.malmquist`: the efficiency change included noise.** EC was
  exp(ε_{t+1} − ε_t) with ε = y − x'β, so it contained v_{t+1} − v_t, and M
  inherited it; the docstring claimed D = 1 on the frontier, but 6–19% of
  firm-periods on the fixture have D > 1. EC is now the ratio of predicted
  technical efficiencies, TE_{t+1}/TE_t (`efficiency="bc"`, the default;
  `"jlms"` also available); TC is unchanged. Components match R `sfaR`
  1.0.1 (`sfacross` per period plus `efficiencies()`) to 2.7e-7. Fixture:
  mean EC t→2 / t→3 1.0653 / 0.9759 → 1.0389 / 0.9456; mean M 1.0997 /
  1.1170 → 1.0730 / 1.0824; row 1 (M, EC, TC) (1.26878, 1.15400, 1.09947)
  → (1.11709, 1.01603, 1.09947). `efficiency="residual"` returns the old
  index.
- **`sp.zisf`: the JLMS efficiency was the Battese–Coelli mixture.**
  `efficiency(method="jlms")` and `model_info["mean_efficiency_jlms"]` now
  return exp(−E[u|ε]) with E[u|ε] = (1 − P(eff|ε))·E[u|ε, ineff]. Fixture
  mean 0.81702 → 0.81279. The default (BC) efficiency is unchanged. `zisf`
  now has references: Stata `chks` 1.1 (8.6e-8 / 9.4e-8, estimate / SE) and
  R `sfa::zsfm` 1.2.0 (production, cost and `zprob=`).
- **`sp.mgwr`: the bandwidth search was not MGWR's algorithm.** Every stage
  differed from the authors' PySAL `mgwr`: GWmodel's `gold()` instead of
  mgwr's golden section (δ = 0.38197, rounded probes, memo, stop at
  |Δcriterion| ≤ 1e-6, 2-decimal result); bounds [20, n] instead of
  [40 + 2p, n] (adaptive) / [min d / 2, 2·max d] (fixed); no 1.0000001
  factor on the adaptive kernel; CV not divided by n; a max|Δf| stop instead
  of the score of change (SOC); no bandwidth freeze after 5 unchanged
  sweeps; no SE / ENP_j / AICc. Rewritten as a transcription of mgwr 2.2.1:
  bandwidths, initial bandwidth, bandwidth history and iteration count are
  identical in 4 configurations, betas 3.0e-12, SE / ENP_j / AICc ≤ 1e-15.
  Georgia: bandwidths [93, 101, 156, 158] → [101, 101, 117, 157]; RSS
  51.2691 → 50.803541834793; AICc 297.0704149757866 (new, = mgwr); runtime
  6.2 s → 0.42 s. `tol` is now the SOC threshold. The old search matched no
  reference and is not kept; `kernel_eps=1.0` gives GWmodel's kernel.

**RD and IV**

- **`sp.rd2d` / `sp.rd2d_bw` / `sp.boundary_rd` computed a different
  estimator.** Through 1.28.0 the default `approach="distance"` was a local
  linear fit on the signed distance to the boundary line, with a Silverman /
  curvature rule-of-thumb bandwidth, conventional (not bias-corrected)
  inference, one pooled number and `model_info['bandwidth']` rounded to 6
  decimals; `approach="location"` pooled pointwise fits by inverse-variance
  weights. R `rd2d` estimates pointwise effects τ(b) with the `rdbw2d`
  MSE / CER bandwidths and robust bias-corrected inference. Rebuilt as a
  port of R `rd2d` 1.0.0 (sharp and fuzzy, product / radial kernels, HC0–3,
  clusters, all 8 `bwselect` rules, mass points, kinks, WBATE headline with
  the cross-point covariance): 1.6e-11 / 3.8e-12 (estimate / SE) against
  `rd2d::rd2d`, 1.5e-12 / 1.1e-12 against `rd2d.distance`. **Breaking:**
  the default `approach` is now `"location"` (R's `rd2d`), and
  `sp.rd2d_bw` returns a DataFrame of per-point bandwidths instead of a
  float. No like-for-like old number exists: on `rd_open_bd.csv` R reports
  five pointwise effects (0.446 / 0.929 / 1.020 / 0.704 / 1.357,
  bias-corrected) and WBATE 0.891 (SE 0.0903). A single one-score effect is
  `approach="pooled"`, now `sp.rdrobust` on the signed distance to the
  boundary curve, not the old fit. Not ported: `covs.eff` and the simulated
  uniform bands / LBATE.
- **`sp.rd_discrete` was not the Kolesár–Rothe procedure.** The
  local-linear-on-bin-means variance used `var(bin)/n_bin` inside a sandwich
  already weighted by `n_bin`, so SEs were understated by ~√(bin size);
  `M` came from maximum second differences; the `'bm'` bound `K·Σ|w|` is not
  the BME interval. `'bsd'` now runs the RDHonest engine behind
  `sp.rd_honest`, and `'bme'` (alias `'bm'`) ports `RDHonestBME`; both match
  R `RDHonest` 1.0.1.9000 to 1e-9 at fixed h (1e-6 when RDHonest selects h
  and M). Fixture (estimate / SE / CI): bsd M = .05, h = 5 0.7208 / 0.0113 /
  [0.105, 1.337] → 0.7619 / 0.1121 / [0.445, 1.079]; bsd default 0.6636 /
  0.0083 / [−34.5, 35.8] → 0.8401 / 0.1466 / [0.464, 1.216]; bm h = 4
  0.7271 / 0.0130 → 1.4953 / 0.0549 / [0.640, 2.355].
  `model_info['discrete']` loses `n_left`, `bin_means`, `honest_ci` and gains
  `maximum_bias`, `bandwidth`, `eff_obs`. The headline p-value uses bias/SE;
  R's own BME p-value is kept as `p_value_rdhonest` (see
  Reference-implementation findings).

**Decomposition and QTE**

- **`sp.melly_decompose` / `sp.machado_mata`: the quantile regressions were
  not quantile regressions, and the process grid and inversion were not
  cdeco's.** A 50-iteration IRLS with a 1e-6 step stop left coefficients
  2–5% off the LP optimum at the median and up to 379% off on a small tail
  slope (τ = .9 tenure 0.00227 against 0.00047). The QR process now uses the
  `sp.qreg` LP solver (= Stata `qrprocess` to 7.5e-15), the midpoint grid
  (j − 0.5)/J with default `n_tau_qr` 99 → 100 (was 99 points on
  [0.01, 0.99]), and Melly's quantiles use the averaged inverse CDF
  (`mm_quantile` definition 2) instead of `np.quantile` type 7.
  `melly_decompose` now matches Stata `cdeco, method(qr)` 1.0.2 to 6.2e-16.
  `dq_wage.csv`, counterfactual quantile: τ ≈ .1 1.49961 → 1.48117,
  τ ≈ .5 2.30641 → 2.30639, τ ≈ .9 3.11162 → 3.12503 (cdeco 1.48117 /
  3.12503). `machado_mata` shares the fix; it stays Monte Carlo and
  converges to `melly_decompose`. The old numbers are not reachable.
- **`sp.fairlie` was not Fairlie's decomposition.** It drew independent
  random subsamples of both groups (no ranking by predicted probability, so
  no matching), rescaled the contributions to sum to the explained gap and
  reported no SEs. It is now Jann's algorithm (rank both groups, subsample
  the larger in rank order, pair rank to rank, switch covariates in order)
  with delta-method SEs in `detailed['se']`; with equal group sizes it is
  seed-free. Matches Stata `fairlie` 1.0.7 to 4.5e-15 (contributions) and
  5.4e-14 (SE) with a tightly converged logit. Logit, reference 0: educ
  0.010457 → 0.009463 (Stata 0.009463), exper 0.015056 → 0.015866, tenure
  0.000835 → 0.001020.
- **`sp.mediation_decompose`: NDE at the wrong covariate profile, and no
  SEs by default.** NDE used θ3·mean(M | A = 0), covariates at the
  unexposed mean, while NIE, Stata `paramed`, `CMAverse` and
  `sp.four_way_decomposition` hold covariates at the overall mean. With
  confounded exposure NDE 0.717658 → 0.770783 (`paramed` 0.770783);
  `cde + int_ref == nde` against `four_way_decomposition` to 4e-16; `cde` is
  unchanged, and nothing changes without covariates. The default
  `inference='analytical'` returned `se` / `ci` = `None`; delta-method SEs
  now match `paramed` to 9.5e-15.
- **QTE-family propensity scores were penalised and under-converged**
  (`sp.dist_iv`, `sp.distributional_te` propensity and DR
  distribution-regression logits, `sp.qte(method="firpo_*")` with
  covariates). sklearn `LogisticRegression(C=1e6, lbfgs)` stops at gradient
  tolerance 1e-4, 2.5e-5 from the MLE. A Newton fit to 1e-10 now equals
  Stata `logit` to 1.7e-13. Estimates move in the 5th–6th digit on
  covariate paths only.

**ML causal inference (grf operators, CDDF, off-policy evaluation, DML)**

- **`sp.calibration_test` / `sp.test_calibration` were not grf's test.**
  The old version regressed a Horvitz–Thompson pseudo-outcome on
  `[tau, tau - mean(tau)]` (HC1, two-sided normal p); because the columns
  share `tau`, the "differential" coefficient estimated b2 − b1, so its test
  of 0 was a test of equal calibration. It now regresses `Y - Y.hat` on
  `(W - W.hat)·mean(tau)` and `(W - W.hat)(tau - mean(tau))` with HC3 and
  reports grf's t against 0 with a one-sided p from t(n − 2), matching
  `grf::test_calibration` 2.6.1 to 1.1e-15 (coefficient, SE) and 1.6e-13
  (p). Fixture: differential 0.180 → 1.187 (grf 1.18726); mean 0.985 →
  1.00297. The output no longer has a `null` column. Rows that are not the
  training sample used mean-of-Y / mean-of-T stand-ins for the nuisances;
  they now raise. New `vce=` (HC0–HC3, default HC3); the result dict keeps
  the key `vcov_type`. HC0 carries the n/(n − 1) factor of the
  `sandwich::vcovCL` call grf makes; `t_vs_zero` / `p_one_sided` are kept
  as synonyms of `t` / `p`. (The `dml_diagnostics` fix of the same
  campaign is superseded by the upstream redesign already on main.)
- **`sp.rate` was not grf's RATE.** Scores were a Horvitz–Thompson signal,
  not grf's AIPW scores; tied priorities were not averaged; QINI used
  weights `1 - u` instead of grf's `k/n`, off by exactly mean(score)/(2n)
  on the fixture (0.25814 vs 0.25869); the influence-function SE omitted the
  rank-estimation term (0.0949 against grf's half-sample bootstrap 0.0744,
  +28%). The point estimate and TOC curve now equal
  `grf::rank_average_treatment_effect` / `.fit` to 4.6e-15, including tied
  priorities; the analytic rank-corrected SE is 0.0725, within grf's Monte
  Carlo error (the SE stays T3). Non-training `X` now raises.
- **`sp.cate_eval`** had its own copy of the old RATE with the same tie,
  QINI-weight and SE defects; it now shares `sp.rate`'s operator.
- **`sp.average_treatment_effect(target_sample="overlap")`** used an
  e(1 − e)-weighted AIPW mean; grf uses the R-learner OLS with intercept and
  HC3. Fixture: 1.12386 / 0.07687 → 1.12514 / 0.07968 (grf exact). Other
  target samples were already exact. Out-of-sample rows that fall back to
  the plug-in now warn (only a `method` field recorded it).
- **`sp.honest_variance`: the SE was the Monte-Carlo error of the average**,
  `sd(half-means)/sqrt(n_splits)`, which shrinks to 0 with more splits
  (0.0038 at 25 splits against a sampling SE of 0.024). It is now the
  half-sample spread (≈ sd(tau)/sqrt(n)); the docstring calls it
  descriptive.
- **`sp.blp_test` ran unweighted OLS on in-sample CATE predictions**, while
  its docstring claimed equivalence to `grf::test_calibration`. On a
  constant-effect DGP (n = 400, T-learner) it reported β2 ≈ 1.43,
  p ≈ 3e-52. It is now the CDDF weighted regression (weights 1/(p(1 − p)))
  on an out-of-fold proxy by default (`proxy="cross_fit"`), equal to
  `GenericML::BLP` 0.2.3 to 2.3e-15 / 1.2e-15 given the same proxy,
  propensity and baseline. Null DGP: β2 0.137, p 0.29. New `vce=` (default
  HC1; `"const"` is GenericML's default); the result dict keeps the key
  `vcov_type`. `proxy="in_sample"` restores the in-sample proxy (the
  regression stays weighted).
- **`sp.gate_test` had no outcome regression.** It ran ANOVA / t-tests on
  the model's own predictions grouped by the same predictions, so its
  p-values had no meaning. With `y` / `treat` / `covariates` it now runs the
  GATES weighted regression, equal to `GenericML::GATES`
  (`monotonize=FALSE`) with `quantile_group` membership to 1.9e-15. `vce=`
  as in `blp_test`; `vce="const"` on the weighted regression reproduces
  `sandwich::vcovHC(type="const")`, which is not `vcov(lm)`. Without
  outcomes the descriptive path remains and warns.
- **`sp.forest_diagnostics`** filled propensities with `mean(T)` on
  non-training rows and so reported perfect overlap; it now reports NaN
  with a warning.
- **`sp.ips` / `sp.snips` / `sp.doubly_robust`: `clip` also floored the
  behaviour propensity at `1/clip`.** With `clip=2` IPS gave 0.8496 against
  Open Bandit Pipeline (`obp`) 0.5.7 `lambda_=2` 1.1904. `clip` now caps the
  weight only, as `obp`'s `lambda_`; `pi_b <= 0` raises. The default
  `clip=50` is inert whenever `pi_b >= 0.02`.
- **`sp.snips` SE divided by `sum(w)` instead of `mean(w)`**: 0.00039
  against a bootstrap SE of 0.0174 (n = 2000). It is now the delta-method
  SE, equal to `sp.ope.snips`.
- **`sp.doubly_robust` with a 1-D (deterministic-action) policy** read the
  action vector as target probabilities in the correction term. Fixture,
  always action 2: 1.3054 → 0.8555 (arm-2 sample mean 0.896). Values now
  equal `obp` `DoublyRobust` to 1.8e-16 with the same reward model
  (`q_hat=`).
- **`sp.dml_panel(include_time_fe=True)`: the two-way within transform
  stopped after one sweep**, exact only for balanced unweighted panels.
  Unbalanced fixture: max abs error 0.19 in y; estimate 0.82050 → 0.81951
  (Python `DoubleML` 0.11.3 0.81951). Now alternating projections to 1e-13,
  equal to `fixest::demean` (2.6e-14). Balanced unweighted panels are
  unchanged.
- **`sp.dml_model_averaging` / `sp.model_averaging_dml`**: the CLS weights
  came from SLSQP (ftol 1e-10); for K ≤ 12 learners they now come from an
  exact support-enumeration QP (short-stacking weights equal
  `ddml::ddml_plm(ensemble_type="nnls1")` to 4.4e-14). Output moves by about
  1e-8. The SLSQP fallback for K > 12 now warns.

**Sensitivity, Mendelian randomization, transport and trial design**

- **`sp.mi_estimate`: degrees of freedom and covariance.** It used Rubin's
  large-sample df `(m-1)(1+1/r)^2` everywhere (the comment said
  Barnard–Rubin) and pooled only the diagonal of the within covariance. It
  now uses Barnard–Rubin df with `dfcom = data_info['df_resid']`, the full
  `var_cov`, and p / CI from t(df), matching R `mice::pool` 3.19.0 (df
  1.4e-14, p 3e-13) and Stata `mi estimate: regress`. Example x2: df
  31.25 → 24.99; p now equals mice's 1.5656e-06. Results add `ubar`, `b`,
  `t`, `riv`, `lambda`, `fmi`, `fmi_barnard_rubin`, `df`, `dfcom`,
  `ci_lower`, `ci_upper`. Passing estimates without `df_resid` to
  `MICEResult.combine` gives the large-sample df.
- **`sp.mediate_sensitivity` used a heuristic bias, not Imai–Keele–
  Yamamoto.** It subtracted `α_T ρ σ_Y/σ_M`. It now fixes ρ in the `medsens`
  SUR / FGLS, with delta-method SE / CI and the exact crossing
  ρ̃ = corr(resid M ~ T + X, resid Y ~ T + X); matches R
  `mediation::medsens` 4.5.1 (ACME 8e-14). Crossing 0.558 → 0.487;
  ACME(−0.9) 0.852 → 1.533. `eps=sqrt(machine eps)` reproduces medsens'
  stopping rule.
- **`sp.calibrate_confounding_strength`: the bias bound was off by √dof.**
  It used `√(k r_y · k r_d/(1 − k r_d)) · se`, with no √dof and linear
  scaling of both R². It now computes the Cinelli–Hazlett benchmark bounds
  exactly as `sensemakr::ovb_bounds` 0.1.6 (1.3e-15). `dof=` is now
  required. At k = 5 the bias bound 0.0199 → 0.4640; an estimate of 0.10
  went from "robust" to a breakpoint at k = 1.5.
- **`sp.survival_sensitivity` never overturned protective effects**: the
  worst case was `log_hr − log Γ` regardless of sign. It now moves toward
  the null. log HR = −0.4, SE 0.15: breakpoint None → 1.2 (the same as the
  positive case).
- **`sp.unified_sensitivity`**: `rho_max` was ignored on the data path
  (always the 1.3 rule), while the documented default 1.0 was used on the
  summary path, so the two paths disagreed. The default is now Oster's
  min(1, 1.3 R²) on both and an explicit value is honoured (registry default
  1.0 → None). The RR CI was the rescaled t CI, not the interval the E-value
  used; it is now `EValue`'s `exp(0.91 d ± 1.78 se/sd)` (1e-12).
- **`sp.attrition_bounds(method="lee")`** kept `n − ceil(qn)` observations,
  one fewer than Lee's rule, and disagreed with `sp.lee_bounds`. It now
  shares that helper: (0.70358, 1.61981) → (0.71883, 1.60455), equal to
  `sp.lee_bounds`; `trimming="exact"` gives (0.70557, 1.61782), equal to
  Stata `leebounds` with exact thresholds.
- **`sp.mr_bma` was BIC model averaging under the MR-BMA name.** It is now
  Zuber et al.'s Bayes factor (IVW scaling, normal prior σ = 0.5), equal to
  their `summary_mvMR_BF` (posterior probabilities 7e-15), with
  `model_averaged_estimate` added. `method="bic"` returns the old quantity.
- **`sp.mr_multivariable` shrank the SE under under-dispersion** (RSE < 1
  multiplied the SE down); `MendelianRandomization::mr_mvivw` floors the
  factor at 1, and so does StatsPAI now (9e-16 / 2e-16). Only data with
  RSE < 1 change.
- **`sp.mr_mediation` total effect used the fixed-effect IVW SE** (the
  defect round 1 fixed in `sp.mr_ivw`); it now calls `sp.mr_ivw`.
- **`sp.grapple` was a different estimator**: a joint Gaussian MLE with a
  numerical-Hessian SE, not GRAPPLE's robust profile score. It now solves
  GRAPPLE's estimating equations (Tukey by default; `loss="huber"` /
  `"l2"`) with its sandwich. LDL data: β 2.694 → 2.7197 (GRAPPLE 2.7196),
  SE 0.510 → 0.5520. It warns (`RuntimeWarning`) when the (τ², β)
  alternation does not converge.
- **`sp.transport_weights_fn` / `sp.transport_generalize` SE** used
  Σw(y − m)² instead of Σw²(y − m)², so it was not invariant to rescaling
  w: 0.0864 → 0.1556 (= `sandwich::vcovHC(HC0)`).
- **`sp.identify_transport` admitted descendants of X** in the adjustment
  set and weighted by the target margin P(Z)_T; for X→Z→Y, S→Z it returned
  a wrong formula; for that graph it now reports "not transportable" under
  the covariates-only design.
- **`sp.randomize`**: `method="complete"` silently ran simple
  randomization; stratum counts used round-half-to-even and gave odd-stratum
  misfits to a fixed arm (5 → 2 treated, 7 → 4); cluster assignment was
  Bernoulli; re-randomization redrew by simple randomization, discarding
  strata and clusters. It now follows `randomizr` 2.0.1's `complete_ra`
  rule within strata and over clusters, and re-randomization redraws from
  the same design. Draws differ for the same seed.

**DiD and synthetic control**

- **The shared simplex solver stopped at SLSQP tolerance.**
  `solve_simplex_weights` (every no-covariate SCM fit, including `sp.synth`
  equal-V fits, `conformal_synth`, `multi_outcome_synth`,
  `synth_experimental_design` and the sensitivity tools) returned weights
  about 1e-7 off the optimum. Identified problems (full column rank, or
  ridge > 0) now use the exact active-set solver; rank-deficient problems
  keep SLSQP. Treated fit: weights 9e-8 → 2e-14 abs, ATT 3e-8 → 5e-15 rel
  from `Synth::synth` / quadprog. Outputs move by about 1e-7 (a pinned
  pre-RMSPE 0.17714 → 0.1771399093). `synth_loo`, `synth_time_placebo`,
  `synth_donor_sensitivity` and `synth_rmspe_filter` now match per-fit
  `Synth::synth` 1.1.10 to ≤ 1e-13 (3e-14 for `synth_loo`).
- **`sp.synth_loo` / `sp.synth_time_placebo`: degenerate naive p-values.**
  With one placebo post-period `np.std` = 0 gave se = 0, z = inf and p = 0,
  so the last time placebo was always "significant" (fixture: att −0.041,
  p 0.0). SE and p are now NaN when T1 < 2 or SE ≤ 0; the docstrings call
  them descriptive i.i.d.-gap quantities (`alpha` is unused).
- **`sp.conformal_synth` computed a different procedure from
  Chernozhukov–Wüthrich–Zhu.** Weights were fit on the pre-period only and
  never re-estimated under the null, pointwise p used (1 + #)/(T0 + 1) on
  pre-fit residuals, and the joint test used |mean| of the residuals. It is
  now `scinference`'s procedure: the SC refit on all T0 + T1 periods with
  the post outcomes shifted by θ0, moving-block S = Σ|u| over length-T1
  cyclic blocks, pointwise p from T0 plus one post-period, CIs by grid
  inversion. Joint p-values equal `scinference` on every grid point where
  its solver succeeds (see Reference-implementation findings). On the
  `test_cov95_synth_variants` panel p 0.0556 → 0.444, and at α = 0.05 the
  CI is (−inf, inf) because T = 18 < 20; the estimate is unchanged. When α
  is below the smallest attainable p the set is (−inf, inf); grid
  truncation warns and sets `model_info['ci_truncated']`; the default grid
  is ±max(5·sd(pre-residuals), 3·max|post gap|); `se` is documented as a
  CI-implied scale.
- **`sp.synth_survival`**: the exponentiated-gradient loop stopped short
  (weights off by 0.03 and SSR 7% too large on a 12-period, 8-donor
  example) and now uses the exact solver; the placebo band had the wrong
  sign (`gap + q`, now [gap − q_hi, gap − q_lo]); the band was documented
  as uniform but is pointwise; a bare `except Exception: continue` is
  removed. No package computes this estimator (identity tests only).
- **`sp.synth_power` / `sp.synth_mde`**: rejection used `ratio >=` the
  interpolated (1 − α) quantile of the placebo ratios, which is not the rank
  test `sp.synth` reports and is anti-conservative; it now rejects when
  `placebo_rank_pvalue <= α`. The null baseline kept the real effect (the
  observed post gaps were used uncentred); they are now centred before δ is
  injected. Prop. 99 (`n_sim` 50): power at δ = 0 1.0 → 0.0; MDE 0 → 10.9.
  With J = 8 placebos and α = 0.05 (1/9 > α) `synth_mde` now returns inf.
- **`sp.shift_share_political`**: the Rotemberg weights were normalised by
  Σ|·|, so they did not sum to one, and had no `beta_k`; they are now
  `sp.bartik`'s GPSS weights, equal to `bartik.weight::bw` (max |α_k| 0.447
  before, 0.702 after). The share-balance F used df1 = K; with shares
  summing to one it is rank([1, S]) − 1: F 0.924 → 1.143, p 0.490 → 0.357
  (= `anova(lm)`). The summary labelled the HC1 SE "AKM shock-cluster"; HC1
  stays as `se` (= `AER::ivreg` + HC1) and AKM, AKM0 and EHW are added to
  `diagnostics` (= `ShiftShareSE::ivreg_ss`).
- **`sp.shift_share_political_panel`**: the two-way within transform was
  one pass of unit-then-time demeaning, inexact on unbalanced panels (now
  alternating projections, equal to `fixest` at 1e-14 on a 7-row-deleted
  panel); `cluster="twoway"` was HC0 on unit × time cells (now
  Cameron–Gelbach–Miller unit + time − cell, = `fixest ~unit+time`);
  `cluster="shock"` used the wrong AKM formula (now `ivreg_ss` with FE
  dummies, 1.2e-15); the Rotemberg weights demeaned x by period only and
  were Σ|·|-normalised (now GPSS on the FE-residualised x, = `bw` with FE
  dummies); `first_stage_F` was var(D̂)/var(resid) (now the homoskedastic
  partial F with FE df). Balanced-panel β and the unit / time SEs were
  already right.

### Fixed

**Spatial, survey and structural**

- `sp.malmquist` forwards `usigma` / `vsigma` / `emean` / `cluster`; these
  columns were dropped before the call, so every documented use of
  `**frontier_kwargs` raised `MethodIncompatibility`.
- The `sp.malmquist` docstring no longer attributes the definition to Coelli
  & Rao (a DEA paper); the FGLR citation key is `fare1992productivity`.

**Treatment effects**

- `sp.policy_value` raises `ValueError` unless `scores` and `policy` are
  1-D and of equal length (a scalar policy is still accepted). An (n, 1)
  score column broadcast to an n × n outer product and silently returned
  mean(scores)·mean(policy). Valid inputs are unchanged; results equal
  `grf::average_treatment_effect(subset = pi == 1)` × mean(pi) to 6.7e-16.

**Decomposition and QTE**

- `sp.beyond_average_late` carried its own copy of the complier-CDF code
  and a bare `except Exception: pass` in the bootstrap; it now delegates to
  the shared QTE core (numbers identical) and degenerate resamples are
  counted by the existing warning.

**ML causal inference**

- The forest-inference module header cited `athey2019surrogate` for GRF; it
  is `athey2019generalized`. A misused `chernozhukov2020generic` citation
  (a different paper) is removed.

**Sensitivity, Mendelian randomization, transport and trial design**

- The MR-BMA reference in the `sp.mr_bma` docs and registry named the
  co-authors as "Zuber, Colijn, Staley & Burgess"; the paper (Nature
  Communications 11:29, 2020, doi:10.1038/s41467-019-13870-3) is by Zuber,
  Colijn, Klaver & Burgess. Corrected everywhere (`paper.bib` was already
  right).

**DiD and synthetic control**

- `sp.shift_share_political` / `sp.shift_share_political_panel`: "Park &
  Xu" and the "§4.2" attributions were unverified; the paper is Park (2026),
  single-authored, arXiv:2603.00135 (`paper.bib::park2026shift`).
- `sp.sequential_sdid` is cohort-by-cohort SDID (`sp.sdid` on truncated
  cohort sub-panels; per-cohort ATT(g) equals `synthdid::synthdid_estimate`
  0.0.9 to 1e-8), not the Arkhangelsky–Samkov sequential estimator
  (arXiv:2404.00164), which aggregates by cohort, loops over horizons,
  imputes τ̂ back and uses a Bayesian bootstrap. Module, summary and
  `model_info` are relabelled ("cohort_by_cohort_sdid") and
  `model_info['estimator']` is added. The `cohort_weights="size"` docstring
  said units × post-periods; it weights by units. Dropped cohorts now warn.
- `sp.synth_experimental_design` is a leave-one-out SC-fit ranking
  heuristic, not the Abadie–Zhao design (arXiv:2108.02196), which is a joint
  w / v MIQP targeting population predictor means. `method` is now
  `"loo_sc_fit_ranking"` (was `"abadie_zhao_2025"`).
  `docs/guides/synth_experimental.md` is rewritten: it presented a variance
  formula that does not appear in that paper and an unsourced
  `concentration_weight ≈ 0.5` recommendation. `expected_variance` is
  documented as a sum of pre-period MSPEs, not an ATT variance.
- `sp.synth_survival` no longer claims to be Han & Shah's SSC
  (arXiv:2511.14133), a different estimator (survival scale, unconstrained
  PCR weights); its citation key is `abadie2010synthetic`.
- `sp.multi_outcome_synth`'s citation lists all three authors;
  `sp.qqsynth`'s docstring is corrected.

### Added

**Time series**

- `sp.structural_break(pvalue_method="hansen" | "simulate")`; module-level
  `hansen_supf_pvalue`; Bai-Perron critical-value tables in
  `timeseries/_break_tables.py`.
- Parity file `tests/reference_parity/test_r2_ts_parity.py` against
  strucchange, mbreaks, Stata `estat sbsingle` / `pvalsup()` and `xtbreak`.

**Spatial, survey and structural**

- `sp.malmquist(efficiency="bc" | "jlms" | "residual")`.
- `sp.mgwr(criterion=, bw_min=, bw_max=, bws_same_times=, rss_score=,
  search_tol=, search_max_iter=, kernel_eps=)`; results carry `bse`,
  `tvalues`, `ENP_j`, `tr_S`, `sigma2`, `aicc` / `aic` / `bic` / `llf`,
  `bw_init`, `bws_history`, `scores`, `converged`.
- `sp.spatial_panel(twoways_lag="splm" | "within")`: `"within"` is the
  Lee–Yu (2010) eq. 21 dummy-model profile likelihood (`vce="oim"` only);
  the default is unchanged.
- Parity files `test_r2_frontier_parity.py` (sfaR, metafrontier, sfa,
  Stata `chks`) and `test_r2_spatial_parity.py` (PySAL mgwr, Stata
  `xsmle`).

**Treatment effects**

- Parity file `test_r2_teffects_parity.py`: `gformula_ice_fn` point
  estimate against `ltmle(gcomp=TRUE)` (2.1e-11), `policy_value` against
  grf / policytree, TMLE ATT against `tmle::tmle`.

**RD and IV**

- `sp.rd2d(..., weights=)` (WBATE), `q`, `deriv`, `tangvec`, `kernel_type`,
  `vce`, `cluster`, `fuzzy`, `fitmethod`, `bwparam`, `method`,
  `masspoints`, `bwcheck`, `scaleregul`, `scalebiascrct`, `stdvars`,
  `kink_unknown`, `kink_position`, `cqt`, `distance`, `side`, mirroring R
  `rd2d`.
- `sp.rd_discrete(order=, kernel=, opt_criterion=)`; `p_value_rdhonest`.
- Parity file `tests/reference_parity/test_rd_open_R_parity.py` against R
  `rd2d` and `RDHonest`.

**Decomposition and QTE**

- `sp.cfm_decompose(thresholds=, inversion="interpolate" | "step")`;
  `inversion="step"` with the same thresholds reproduces Stata `cdeco,
  method(logit)` (CDFs 2.4e-10, quantiles exact).
- `sp.fairlie` per-variable delta-method SEs in `detailed['se']`.
- Parity file `tests/reference_parity/test_decomp_qte_parity.py` against
  Stata `cdeco`, `qrprocess`, `fairlie`, `shapley2` / `ineqdeco`, `paramed`
  and `ivqte`.

**ML causal inference**

- `vce=` on `sp.calibration_test` / `sp.test_calibration`, `sp.blp_test`
  and `sp.gate_test`; `priorities=`, `se_method="half_sample"`,
  `n_bootstrap=` on `sp.rate`; `propensity=`, `baseline=`, `proxy=`,
  `seed=` on `sp.blp_test` and `sp.gate_test`.
- `fold_indices=` on `sp.dml_panel` and `sp.dml_model_averaging`; stacked
  residuals in `dml_model_averaging().model_info`.
- `q_hat=` on `sp.direct_method` and `sp.doubly_robust`.
- Parity files `test_ml_causal_R_parity.py` (grf, GenericML),
  `test_ml_causal_obp_parity.py` (Open Bandit Pipeline) and
  `test_ml_causal_dml_parity.py` (fixest, ddml, DoubleML).

**Sensitivity, Mendelian randomization, transport and trial design**

- `sp.subgroup_analysis` heterogeneity test also reports `F`, `pvalue_F`
  and `df_resid` (Stata `testparm`).
- `sp.attrition_test(correction=)` (`False` = Stata `tabulate, chi2`);
  `sp.balance_check(equal_var=)` (`True` = `iebaltab`);
  `sp.attrition_bounds(trimming=)`.
- `sp.mediate_sensitivity(conf_level=, eps=, max_iter=)`;
  `sp.calibrate_confounding_strength(multipliers=)`;
  `sp.mr_bma(prior_sd=, method=)`; `sp.grapple(loss=, k=, tol=,
  max_iter=)`.
- Parity files `test_misc_sens_R_parity.py` (mice, mediation, sensemakr,
  EValue, MendelianRandomization, metafor, causaleffect, Zuber et al.'s
  `summary_mvMR_BF`, GRAPPLE) and `test_misc_sens_stata_parity.py` (Stata
  `regress`, `mi estimate`, `leebounds`, `iebaltab`).

**DiD and synthetic control**

- `sp.synth_rmspe_filter(metric="rmspe" | "mspe", placebo_pool=
  "include_treated" | "exclude_treated")`: the SCtools / ADH MSPE cut-offs
  and placebo pools without the treated unit (defaults unchanged); the
  placebo table and treated ratio in `df.attrs`. Both conventions match
  `SCtools::mspe.test` 0.3.3.1.
- `sp.conformal_synth`: `model_info['joint_pvalue_grid']`,
  `['ci_truncated']`, `*_ci_unbounded`.
- `sp.shift_share_political`: AKM / AKM0 SE, CI and p in `diagnostics`;
  `beta_k` in `rotemberg_top`. `sp.shift_share_political_panel`:
  `diagnostics['akm0_ci']`, `['balanced']`.
- `sp.multi_outcome_synth`: `model_info['placebo_failures']`; shared
  weights and per-outcome ATTs match `augsynth::augsynth_multiout` 0.2.0.
- Parity file `tests/reference_parity/test_synth_rest_R_parity.py` against
  Synth, SCtools, scinference, augsynth, synthdid, AER, ShiftShareSE,
  bartik.weight and fixest.

**Citations**

- `paper.bib` gains verified entries `chernozhukov2025generic`
  (Econometrica 93(4), 1121–1164), `hansen1997approximate`, `choi2001unit`
  and `fuentes2001parametric`.

### Changed

- `sp.structural_break(method="bai-perron")`: `min_segment` must be one of
  .05, .10, .15, .20, .25 and `alpha` one of .10, .05, .025, .01; other
  values raise. `p_values` is `None`.
- `sp.mgwr`: `tol` is the SOC threshold.
- `sp.rd2d` / `sp.boundary_rd`: default `approach` `"distance"` →
  `"location"`; `approach="pooled"` delegates to `sp.rdrobust`.
  `sp.rd2d_bw` returns a per-point DataFrame (breaking).
- `sp.rd_discrete(K=)` is ignored with a `DeprecationWarning`.
- `sp.melly_decompose` / `sp.machado_mata`: default `n_tau_qr` 99 → 100.
- `sp.cfm_decompose` monotonises the DR CDF by rearrangement (sorting)
  instead of a running maximum; identical when the raw CDF is monotone. Its
  logit-failure fallback catches `LinAlgError` / `ConvergenceFailure` and
  warns instead of a silent `except Exception`.
- Bootstrap failures in `sp.machado_mata`, `sp.mediation_decompose` and
  `sp.beyond_average_late` are counted and warned; ≤ 10 usable replications
  raise in `mediation_decompose`, and `machado_mata` warns and returns
  `se=None`. An invalid `inference=` raises in `mediation_decompose`, and
  `reference` / `inference` are validated in `melly_decompose`,
  `machado_mata` and `cfm_decompose`.
- `sp.calibration_test` / `sp.test_calibration`: the output has no `null`
  column; rows that are not the training sample raise. `sp.rate` raises on
  non-training `X`.
- `sp.calibrate_confounding_strength`: `dof=` is required.
- `sp.unified_sensitivity(rho_max=None)`: one default (Oster's
  min(1, 1.3 R²)) on both paths.
- `sp.grapple` issues a `RuntimeWarning` when the (τ², β) alternation does
  not converge.
- `sp.synth_loo` / `sp.synth_time_placebo`: silently dropped fits raise a
  `RuntimeWarning`; the summary line is relabelled.
- `sp.conformal_synth`: `pre_treatment_rmse` is no longer rounded to 6
  decimals.
- `sp.synth_experimental_design().method` is `"loo_sc_fit_ranking"`.

**Not fixed in this release.** `sp.rd_extrapolate(method="ols")` evaluates
every point at the unconditional mean of Z, so `detail.cate` is flat in x
(1.89778 at all 3 points on `rd_open_extrap.csv`) and equals the global
regression-adjustment ATE (Stata `teffects ra` 1.897784556341). It does not
extrapolate the Angrist–Rokkanen CATE(x) = E[Y1 − Y0 | X = x]. The
`sp.margins_at` / `sp.contrast` / `sp.pwcompare` p-values and intervals use
N(0, 1) instead of Stata's t(df_r) (G − 1 under clustering), `pwcompare`'s
Sidak adjustment underflows to 0 below p ≈ 1e-17, `sp.margins(method="mem")`
evaluates factor dummies at the base level, an `at=` variable not in the
model is ignored, and the margins family averages over all of `data=`
rather than the estimation sample; strict xfails pin Stata's numbers.
Estimates and SEs of those three functions are already bit-exact with
Stata. [CHECK: whether the postestimation line lands D1–D5 in this release]

### Reference-implementation findings

- **Stata `sbcusum.ado`** hard-codes CUSUM boundary constants whose
  crossing probabilities are 0.0100000791, 0.0499991147 and 0.0999993370
  (relative errors −7.7e-7, +2.5e-6, +1.2e-6). StatsPAI uses the exact root
  of strucchange's closed form, which an independent density-propagation
  computation confirms to about 1e-12.
- **Stata `_xturfisher.ado`** codes the Fisher L* scale as `3*(5N+3)` while
  its df is 5N+4; Stata's own `[XT] xtunitroot` manual prints 5N+4, as do
  plm and the logistic-moment identity (asserted for N ∈ {1, 2, 5, 12, 50}).
- **Stata `estat sbsingle`** uses a different trimmed range from strucchange
  when 0.15·n is not an integer (n = 250: first regimes 38..212 against
  37..213); the p-values agree on the fixtures.
- **Stata `chks`** drops rows with y ≤ 0 even in the linear model (it runs
  `gen ln(depvar)` and then `drop if rowmiss`): 90 of 500 rows on the
  fixture. The comparison runs on y + 10.
- **R `metafrontier` 0.3.1** (SFA branch): `EC_group` is Shephard-oriented
  while `TC_group` is Farrell-oriented, so `MPI_group` mixes the two.
- **R `sfa::zsfm` 1.2.0**: L-BFGS-B stops with a score of 3e-4 to 7e-4;
  the T2 comparison is on its own log-likelihood polished to its optimum.
- **Stata `xsmle` 1.4.5**, two-way SAR / SDM: its reported maximum is
  below StatsPAI's by 4.85e-5 (SAR) and 5.15e-4 (SDM) on its own objective;
  `type(both, leeyu)` returns the `type(ind, leeyu)` fit (N = 768 = 48·16),
  so the time effects are dropped.
- **R `rd2d` 1.0.0**, `kernel_type="rad"`: it fits at radius
  sqrt(hx² + hy²) but rescales the variance with hx·hy, inflating every
  radial SE by sqrt((hx² + hy²)/(hx·hy)) (√2 when hx = hy). Weighted `lm()`
  plus `sandwich::vcovHC(HC0)` at that radius equals StatsPAI's SE to 1e-10.
- **R `RDHonest::RDHonestBME`** adds `maximum.bias` (outcome units) to a z
  statistic in its p-value; StatsPAI reports the p-value with bias/SE and
  keeps R's as `p_value_rdhonest`.
- **Stata `paramed`**, no covariates, with interaction: the NIE gradient
  uses θ3·a1 where θ2 + θ3·a1 belongs (the covariate branch is right). Its
  SE 0.055580 is reproduced exactly from that gradient; the correct SE is
  0.096576.
- **R `mediation::medsens`** stops its default iteration about 1e-4 short
  of the fixed point at |ρ| = 0.9; `eps=sqrt(machine eps)` reproduces it.
- **GRAPPLE** (GitHub 317e837) stops its `optim` / `uniroot` early (score
  O(1e-3) at its estimate): fitted β agrees to 8e-4, τ² to 6e-5, SE to
  3e-5; its sandwich at its own point matches to 8e-16 (l2).
- **R `scinference`** calls `limSolve::lsei(type=1)` without checking
  `IsError`. At θ0 ∈ {8.75, 9} lsei fails and returns infeasible weights
  (SSR 310.4 against 86.6 at the simplex optimum), and scinference reports
  joint p 0.55 / 0.65 where the value is 0.2 / 0.2. StatsPAI equals
  scinference's code with quadprog as the solver on every grid point.
- **Stata `synth.ado`** rounds the unit weights to 3 decimals
  (`roundmat`), so no Stata SCM tool can reach T2; not run as a reference.
