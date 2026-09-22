# Round 2 — `decomp_qte`: distributional decompositions and IV / distributional QTE

Worktree `r2-decomp-qte`. All numbers below are produced by
`tests/reference_parity/_fixtures/_generate_decomp_qte_stata.do` (Stata 18 MP)
from the CSVs of `_fixtures/_generate_decomp_qte_data.py`, and asserted by
`tests/reference_parity/test_decomp_qte_parity.py` (20 tests, all green).

References installed into the private ado tree `_fixtures/_ado_decomp_qte/`
(covered by the existing `.gitignore` rule `tests/reference_parity/_fixtures/_ado_*/`):

| package | source | version |
| --- | --- | --- |
| `cdeco` / `counterfactual` (Chernozhukov, Fernández-Val & Melly) | `net install counterfactual, from("https://raw.githubusercontent.com/bmelly/Stata/main/")` | cdeco 1.0.2 01mar2023, Distribution-Date 20220803 |
| `qrprocess`, `drprocess` | same repo | (Distribution-Date of repo, 2022) |
| `ivqte` (Frölich & Melly) | same repo | 2.1.15 17feb2010 |
| `fairlie` (Jann) | SSC | 1.0.7 16jun2008 |
| `shapley2` (Chávez Juárez), `ineqdeco` (Jenkins), `moremata` | SSC | shapley2 1.5 10jun15 |
| `paramed` (Liu & Emsley) | SSC | current SSC |

Also checked: `ssc install cdeco / counterfactual / ivqte / nldecompose / rqdeco` → rc 601
(not on SSC; the first four are on Melly's GitHub, `nldecompose` is SJ st0152_1);
`ssc install med4way` → rc 601. R `Counterfactual` 1.1 installed from the CRAN archive
(1.2 does not exist in the archive; only 1.0 / 1.1) and its source read; not used as the
fixture reference because `cdeco` is the same authors' maintained implementation and
`Counterfactual::QteDistEst` hard-codes a `trimming` shift (`trimming + X %*% beta`) and a
`(1:nreg-0.5)/nreg` grid restricted by `trimming`, i.e. a different default quantity.

## 1. Per-function table

| function | reference | class | max rel err est / SE | test |
| --- | --- | --- | --- | --- |
| `melly_decompose` | Stata `cdeco, method(qr) nreg(100) est_opts(method(qreg))` 1.0.2 | **2 → 1** (defects D1–D3 fixed) | q_A, q_B, q_CF: 6.2e-16 (both reference directions); QR process coefficients vs `qrprocess`: 7.5e-15 abs | `test_decomp_qte_parity.py::test_melly_matches_cdeco_qr`, `test_qr_process_matches_qrprocess` |
| `cfm_decompose` | Stata `cdeco, method(logit)` with `drprocess thresholds(1.5(0.05)3.4)` | **2 → 1 (aligned)** via new `thresholds=`, `inversion='step'` | CDFs at thresholds 2.4e-10 abs (Stata `logit` default tolerance); quantiles exact (0) | `test_cfm_matches_cdeco_logit` |
| `machado_mata` | none deterministic (Stata `mmsel` draws random τ and rows) | **5 (T3)**; shares D1/D2 fix | converges to `melly_decompose` (same pool): |Δq_CF| < 0.01 at n_sim = 2e5 | `test_machado_mata_converges_to_melly` |
| `fairlie` | Stata `fairlie` 1.0.7 (Jann), 500/500 groups ⇒ deterministic matching | **2 → 1** (defect D4) | tight-converged logit/probit: contributions 4.5e-15, SE 5.4e-14; Stata default tolerance: 1.6e-10 / 1.6e-6 | `test_fairlie_matches_stata` |
| `yun_nonlinear` | alias of `bauer_sinning`, graded in round 1 against `mvdcmp` | not redone (per brief) | — | `test_decomp_R_parity.py` |
| `shapley_inequality` | `shapley2` 1.5 over `regress` + `ineqdeco` | **1 (aligned)** for GE(0/1/2); Gini = **3** | value function v(S): 1.4e-13; Shapley values vs `shapley2` 2.7e-7 (shapley2 stores v(S) in float); totals 1e-15 | `test_shapley_matches_shapley2`, `test_shapley_gini_value_function_is_plugin_gini` |
| `mediation_decompose` | Stata `paramed` (linear/linear, interaction, covariates at means) | **2 → 1** (defects D5, D6) | effects 8.1e-15, delta SEs 9.5e-15; no-covariate NIE SE: **4 (reference defect)** | `test_mediation_matches_paramed`, `test_mediation_nocov_paramed_nie_se_is_reference_defect` |
| `dist_iv` | Stata `ivqte` 2.1.15 (Frölich & Melly), unconditional endogenous | **3** (inversion convention) + propensity fix (D7) | same complier CDFs; `ivqte` numbers reproduced exactly (1e-12) by applying its inversion rule; propensity vs Stata logit 1.7e-13 | `test_dist_iv_vs_ivqte_is_inversion_convention` |
| `kan_dlate` | deprecated pure alias of `dist_iv` | follows `dist_iv` | — | — |
| `beyond_average_late` | same estimand as `dist_iv` (no covariates) | follows `dist_iv`; duplicated code removed (D8) | identical to `dist_iv` (exact) | `test_beyond_average_late_equals_dist_iv` |
| `distributional_te` | candidate `qte::ci.qtet` 2.0.0 (deprecated in favour of `unc_qte`) | **open** | on `dq_iv.csv` QTT at τ = .1….9: ours 0.457/0.685/0.953/1.088/1.352 vs R 0.478/0.690/0.946/1.100/1.324 — gap not yet bisected (candidates: 100-point y grid + linear interpolation inversion vs R's step ECDF; propensity trimming) | — |
| `disparity_decompose` | none found | **open / 6 (not checked)** | Jackson–VanderWeele; R `causal.decomp` not installed (`packageVersion` NA), not yet tried | existing identity test only |
| `qte_hd_panel` | none | **6** | Canay (2011) two-step with LASSO double selection; no R/Stata package implements this combination (R `quantreg` has no Canay estimator; Stata `ivqte`/`qrprocess` not panel) — not further searched this round | existing `test_hd_panel_qte.py` (known truth) |

Counts: bit-exact/aligned after fix 5 (`melly_decompose`, `cfm_decompose`, `fairlie`,
`mediation_decompose`, `shapley_inequality` GE); convention 2 (`dist_iv`/`beyond_average_late`
inversion, `shapley_inequality` Gini); T4 1 (paramed no-cov NIE SE); T3 1 (`machado_mata`);
open 2 (`distributional_te`, `disparity_decompose`); no reference 1 (`qte_hd_panel`);
aliases 2 (`kan_dlate`, `yun_nonlinear`).

## 2. Defects

**D1 — Melly / Machado–Mata quantile regressions were not quantile regressions** (`decomposition/machado_mata.py::_qreg_irls`).
First divergence: the QR coefficient grid. A 50-iteration IRLS with a 1e-6 step stop left the
coefficients 2–5% off the LP optimum at the median and up to 379% off on a small tail slope
(τ = .9 tenure: 0.00227 vs 0.00047); check-loss 88.9399 vs 88.9359. Fix: `_qreg_grid` now calls
`regression/quantile._qreg_fit` (HiGHS LP, the `sp.qreg` solver); matches Stata `qrprocess` /
`_qreg` to 7.5e-15. `_qreg_fit` now builds its equality matrix sparse (it allocated two dense n×n
identities; unchanged LP).

**D2 — QR-process grid trimmed the tails** (`melly.py`, `machado_mata.py`). `linspace(0.01, 0.99, 99)`
integrates u over (0.005, 0.995) with unequal end masses; CFM's `cdeco` / R `Counterfactual` use the
midpoint grid (j−0.5)/J. New `_tau_process_grid`; default `n_tau_qr` 99 → 100.

**D3 — Melly quantile inversion** used `np.quantile` type 7 (interpolation) instead of the
averaged inverse CDF (type 2, `mm_quantile` default used by `cdeco`). New
`decomposition/_common.averaged_inverse_cdf` (numpy ≥ 1.20 safe).
Before → after (D1–D3 together), `dq_wage.csv`, reference 0, counterfactual quantile:
τ≈.1 1.49961 → 1.48117 (cdeco 1.48117), τ≈.5 2.30641 → 2.30639, τ≈.9 3.11162 → 3.12503 (cdeco 3.12503).
Default output changes. ⚠️ correctness.

**D4 — `fairlie` was not Fairlie's decomposition** (`nonlinear.py`). It drew independent random
subsamples of both groups (no ranking by predicted probability, so no matching), then *rescaled*
the contributions to sum to the explained gap, and reported no SEs. Rewritten to Jann's algorithm:
rank both groups by predicted probability, subsample only the larger group (in rank order), pair
rank to rank, switch covariates in order; delta-method SEs (`fairlie`'s `e(V)`) added as
`detailed['se']`; `model`/`reference`/`n_sim` validated. Before → after (logit, ref 0):
educ 0.010457 → 0.009463 (Stata 0.009463), exper 0.015056 → 0.015866, tenure 0.000835 → 0.001020.
Default output changes (and becomes seed-free with equal group sizes). ⚠️ correctness.

**D5 — `mediation_decompose` NDE evaluated at the wrong covariate profile** (`causal.py`). NDE used
`θ3·mean(M | A=0)`, i.e. covariates at the *unexposed* mean, while NIE / `paramed` / `CMAverse` /
`sp.four_way_decomposition` hold covariates at the overall mean. With confounded exposure:
NDE 0.717658 → 0.770783 (paramed 0.770783); now `cde+int_ref == nde` against `four_way_decomposition`
to 4e-16. `cde` unchanged. Identical without covariates. ⚠️ correctness.

**D6 — `mediation_decompose(inference='analytical')` (the default) computed nothing**: `se`/`ci`
were `None`. Delta-method SEs (OLS s² on n−p, block-diagonal) now populated; match `paramed`
to 9.5e-15. Invalid `inference` now raises. Bootstrap path: bare `except Exception` narrowed to
`LinAlgError`, failures counted and warned; ≤10 usable reps raises.

**D7 — QTE-family propensity scores were penalised / under-converged** (`qte/dist_iv.py`,
`qte/distributional.py` (both the propensity and the DR distribution-regression logits),
`qte/_firpo.py`). `sklearn LogisticRegression(C=1e6, lbfgs)` stops at gradient tol 1e-4: fitted
probabilities 2.5e-5 from the MLE. New `qte/_core.logit_propensity` (Newton to 1e-10) equals Stata
`logit` to 1.7e-13. Output changes in the 5th–6th digit on covariate paths only. ⚠️ minor correctness.

**D8 — `beyond_average_late` carried its own copy of the complier-CDF code and a bare
`except Exception: pass` in the bootstrap.** Now delegates to `qte/_core` (identical numbers,
verified exactly); degenerate resamples surface as NaN and are counted by the existing warning.

**Also changed (not defects in numbers):** `cfm_decompose` monotonisation switched from running
max to sorting (rearrangement, as `cdeco`) — identical whenever the raw DR CDF is monotone (it was
on every fixture); its logit-failure fallback was a silent `except Exception` and now catches
`LinAlgError`/`ConvergenceFailure` and warns. `machado_mata` bootstrap `except Exception: continue`
replaced by counted, warned failures and a hard error below 11 reps; `reference` / `inference`
validated in `melly`, `machado_mata`, `cfm`.

**Reference defect (T4) — `paramed`, no covariates, interaction:** its NIE gradient is
`(θ3·a1, 0, 0, β1, β1·a1, 0)` where ∂NIE/∂β1 needs `θ2 + θ3·a1` (the covariate branch has it right:
`x1 = theta2 + theta3*a0`). Reconstructed exactly: paramed SE 0.055580 = our quadratic form with
the wrong gradient; correct 0.096576 = our SE. Every other paramed number matches to 1e-14.

## 3. Proposed promotion records (for `scripts/build_parity_index.py`)

```python
    "melly_decompose": {
        "status": "bit-exact",
        "reference": "Stata cdeco, method(qr) 1.0.2 (Chernozhukov, Fernandez-Val & Melly; bmelly/Stata counterfactual)",
        "reference_versions": {"Stata": "18.0 MP", "cdeco": "1.0.2 01mar2023 (bmelly/Stata counterfactual, Distribution-Date 20220803)"},
        "tolerance": "fitted and counterfactual quantiles 1e-10 rel (observed 6.2e-16); QR process coefficients 1e-12 abs (observed 7.5e-15)",
        "sides": ["py", "Stata"],
        "test": ["tests/reference_parity/test_decomp_qte_parity.py", "tests/reference_parity/_fixtures/decomp_qte_Stata.json"],
        "note": "100 exact quantile regressions at (j-0.5)/100 (Stata simplex), pooled predictions inverted with mm_quantile definition 2, both reference directions. Evaluated at offset quantiles (0.10003, ...) so that tau*N is never an integer. Regenerate via _fixtures/_generate_decomp_qte_stata.do.",
    },
    "cfm_decompose": {
        "status": "aligned",
        "reference": "Stata cdeco, method(logit) 1.0.2 with drprocess (Chernozhukov, Fernandez-Val & Melly)",
        "reference_versions": {"Stata": "18.0 MP", "cdeco": "1.0.2 01mar2023 (bmelly/Stata counterfactual, Distribution-Date 20220803)"},
        "tolerance": "CDFs at the thresholds 1e-8 abs (observed 2.4e-10: Stata's logit stops at its default tolerance); quantiles 1e-12 abs (observed 0)",
        "sides": ["py", "Stata"],
        "test": ["tests/reference_parity/test_decomp_qte_parity.py", "tests/reference_parity/_fixtures/decomp_qte_Stata.json"],
        "note": "Requires thresholds= (39 shared thresholds 1.5(0.05)3.4) and inversion='step' (cdeco's getquantile). The default inversion='interpolate' is a smoothed quantile, not cdeco's.",
    },
    "fairlie": {
        "status": "bit-exact",
        "reference": "Stata fairlie 1.0.7 (Jann, SSC)",
        "reference_versions": {"Stata": "18.0 MP", "fairlie": "1.0.7 16jun2008 (SSC)"},
        "tolerance": "tightly converged logit/probit: contributions and SEs 1e-12 rel (observed 4.5e-15 / 5.4e-14); at Stata's default logit tolerance contributions 1e-8 and SEs 1e-5 (observed 1.6e-10 / 1.6e-6)",
        "sides": ["py", "Stata"],
        "test": ["tests/reference_parity/test_decomp_qte_parity.py", "tests/reference_parity/_fixtures/decomp_qte_Stata.json"],
        "note": "Equal group sizes (500/500), so fairlie draws no subsample and its rank-to-rank matching is deterministic. Logit ref 0/1 and probit.",
    },
    "mediation_decompose": {
        "status": "bit-exact",
        "reference": "Stata paramed (Liu & Emsley, SSC), yreg(linear) mreg(linear) with interaction",
        "reference_versions": {"Stata": "18.0 MP", "paramed": "SSC"},
        "tolerance": "CDE/NDE/NIE/total and delta-method SEs 1e-12 rel (observed 9.5e-15)",
        "sides": ["py", "Stata"],
        "test": ["tests/reference_parity/test_decomp_qte_parity.py", "tests/reference_parity/_fixtures/decomp_qte_Stata.json"],
        "note": "With covariates, all numbers match. Without covariates paramed's NIE standard error uses theta3 where theta2 + theta3 belongs; the test reconstructs paramed's number from that gradient exactly and StatsPAI's from the correct one (T4 on that single SE).",
    },
    "shapley_inequality": {
        "status": "aligned",
        "reference": "Stata shapley2 1.5 (Chavez Juarez) over regress + ineqdeco (Jenkins)",
        "reference_versions": {"Stata": "18.0 MP", "shapley2": "1.5 10jun15 (SSC)"},
        "tolerance": "value function v(S) 1e-11 rel (observed 1.4e-13); Shapley values 1e-6 rel (observed 2.7e-7, shapley2 routes v(S) through float variables); totals 1e-12",
        "sides": ["py", "Stata"],
        "test": ["tests/reference_parity/test_decomp_qte_parity.py", "tests/reference_parity/_fixtures/decomp_qte_Stata.json"],
        "note": "GE(0), GE(1), GE(2). For index='gini' StatsPAI reports the bias-corrected Gini; ineqdeco's plug-in Gini value function is matched to 2e-12 by gini_population.",
    },
```

`dist_iv` / `beyond_average_late`: do **not** promote to aligned (convention difference on the
quantile inverse; the evidence is a reconstruction, not agreement). If the index has a
"convention" status, the note would be: *"Same Abadie/Frölich–Melly complier CDFs as Stata
ivqte 2.1.15; ivqte inverts with ys[max(1, #{F <= tau})], StatsPAI with inf{y: F(y) >= tau}; ivqte's
numbers are reproduced to 1e-12 by applying its rule (no covariates and with ivqte's own phat)."*

## 4. CHANGELOG / MIGRATION

**⚠️ Correctness**
- `sp.melly_decompose`, `sp.machado_mata`: quantile regressions are now exact (LP) instead of an
  IRLS approximation that stopped 2–5% (median) to several hundred percent (small tail slopes) off
  the optimum; the QR process uses the midpoint grid (j−0.5)/J with default `n_tau_qr=100` (was 99
  points on [0.01, 0.99]); Melly's quantiles use the averaged inverse CDF. `melly_decompose` now
  reproduces Stata `cdeco, method(qr)` to 1e-15. Recompute any Melly / Machado–Mata decomposition.
- `sp.fairlie`: now Fairlie's rank-matched sequential decomposition (Jann's `fairlie`); previously
  unmatched random subsamples with contributions rescaled to the explained gap. Adds per-variable
  delta-method SEs (`detailed['se']`). Contributions change (10% on the test fixture).
- `sp.mediation_decompose`: NDE now holds covariates at their overall mean (as NIE, `paramed`,
  `CMAverse`, `sp.four_way_decomposition`); previously at the unexposed group's mean. Unchanged
  without covariates. The default `inference='analytical'` now actually returns delta-method SEs/CIs.
- `sp.dist_iv`, `sp.distributional_te`, `sp.qte(method='firpo_*')` with covariates: propensity /
  distribution-regression logits are the unpenalised MLE (were sklearn L2-penalised, lbfgs tol 1e-4);
  changes in the 5th–6th digit.

**Added**
- `sp.cfm_decompose(thresholds=..., inversion='interpolate'|'step')`; `inversion='step'` with the same
  thresholds reproduces Stata `cdeco, method(logit)`.

**Changed**
- `sp.cfm_decompose` monotonises the DR CDF by rearrangement (sorting) instead of running max
  (identical when the raw CDF is monotone).
- Bootstrap failures in `machado_mata` / `mediation_decompose` / `beyond_average_late` are warned
  and counted instead of silently dropped.

**MIGRATION rows**

| function | what moves | how to get the old number |
| --- | --- | --- |
| `melly_decompose`, `machado_mata` | all quantiles / components (≈1% in the tails on the fixture) | not reachable (old QR was not a minimiser) |
| `melly_decompose`, `machado_mata` | default `n_tau_qr` 99 → 100, grid now (j−0.5)/J | — |
| `fairlie` | `detailed['contribution']`; new `detailed['se']` | not reachable (old algorithm was not Fairlie's) |
| `mediation_decompose` (with covariates) | `nde`, `total`, `propn_mediated` | `nde_old = cde + theta3*(mean(M|A=0) - E[M|A=0,c̄])` — not exposed |
| `dist_iv`, `distributional_te`, `qte` (covariates) | 5th–6th digit | — |

## 5. Not closed

- `distributional_te`: gap vs `qte::ci.qtet` (up to 2% at τ = .9) not bisected. Next step: pass
  `n_grid` = unique y and a step inverse, then compare IPW weights (R `qte` trims propensity?).
- `disparity_decompose`: no reference tried (R `causal.decomp` not installed; its `smiRD`/`smi`
  estimand should be checked against Jackson–VanderWeele's linear formula before use).
- `qte_hd_panel`: no canonical reference (class 6; see table).
- `dist_iv` analytic SE vs `ivqte, variance`: ivqte's variance formula evaluated with StatsPAI's
  densities reproduces StatsPAI's SE to ~1e-3 rel, so the remaining 0.3–8% gap vs ivqte is the
  density estimate (ivqte `kdens` bandwidth on a resampled quantile process vs StatsPAI Silverman on
  κ-weights) plus the inversion convention. Not pinned; kept as convention, not parity.
- `machado_mata`: T3 by construction (random draws); only convergence-to-Melly asserted.
- Test status: new parity file 20/20; module suites `tests/test_decomposition_*.py`,
  `test_mediation.py`, `test_qte.py`, `test_quantile.py`, `test_yun_nonlinear_decomp.py`,
  tierD decomposition/QTE files, the QTE-family reference-parity files (65) and doctests of
  every touched module all pass. Three existing tests were edited because they pinned removed
  or defective behaviour: `test_decomposition_tier_c.py::test_qreg_irls_recovers_true_beta` and
  `test_decomposition_cov_misc2.py::test_qreg_irls_singular_fallback` (renamed
  `test_qreg_grid_collinear_design_is_finite`) tested the deleted IRLS helper and now test the
  exact solver; `test_decomposition_cov_causal2.py::test_mediation_decompose_total_identity`
  asserted `cde == nde` with covariates (D5) and now asserts `nde == CDE + INT_ref` from
  `four_way_decomposition`, keeping `cde == nde` without covariates.
  `mediation_decompose(inference='none')` remains accepted; `machado_mata` with ≤10 bootstrap
  replications warns and returns `se=None` (it used to do so silently).

## 6. `.gitignore`

None needed: `_fixtures/_ado_decomp_qte/` is covered by `tests/reference_parity/_fixtures/_ado_*/`.
Stata writes `_fixtures/_generate_decomp_qte_stata.log` when run; delete it or ignore `*.log` there.

## Files

New: `tests/reference_parity/_fixtures/_generate_decomp_qte_data.py`, `..._stata.do`,
`decomp_qte_Stata.json`, `dq_wage.csv`, `dq_med.csv`, `dq_iv.csv`,
`tests/reference_parity/test_decomp_qte_parity.py`.
Modified: `decomposition/{_common,causal,cfm,machado_mata,melly,nonlinear}.py`,
`qte/{_core,_firpo,beyond_average,dist_iv,distributional}.py`, `regression/quantile.py`.
