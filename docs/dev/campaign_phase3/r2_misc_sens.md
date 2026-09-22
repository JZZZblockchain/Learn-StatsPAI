# Phase 3, round 2 — `misc_sens` family

Worktree `r2-misc-sens` (round-1 baseline staged; this work = unstaged diff +
untracked files). Nothing committed. **Status: done; open items in §5.**

Counts (27 listed functions): class 1: 6 (`ancova`, `negd`,
`subgroup_analysis`, `mendelian_randomization`, `heterogeneity_of_effect`,
`synthesise_evidence`); class 2 (defect fixed, then aligned/bit-exact): 13
(`mi_estimate`, `mediate_sensitivity`, `calibrate_confounding_strength`,
`unified_sensitivity`, `survival_sensitivity`, `attrition_bounds`, `mr_bma`,
`mr_mediation`, `grapple`, `transport_weights_fn`, `transport_generalize`,
`identify_transport`, `randomize`) plus `mr_multivariable` (outside the list);
class 3: 2 (`attrition_test`, `balance_check`); class 5: 1 (`mice`);
class 6: 4 (`copula_sensitivity`, `rwd_rct_concordance`, `mr_clust`,
`mr_lap`); not examined: 1 (`optimal_design`, release-line file).
Defects fixed: 13 (§2).

Generators (run in this order):

1. `python tests/reference_parity/_fixtures/_generate_misc_sens_data.py` (CSVs)
2. `Rscript tests/reference_parity/_generate_misc_sens_R.R` (writes
   `misc_sens_mi_imputed.csv` + `misc_sens_R.json`; needs mice, mediation,
   sensemakr, EValue, MendelianRandomization, mrclust, combinat; downloads
   Zuber et al.'s `summary_mvMR_BF.R` @ demo_AMD 4981b5a and GRAPPLE's
   `R/mr_fun_general.R` @ 317e837 — GRAPPLE cannot be installed, its haploR
   import is archived)
3. `cd tests/reference_parity/_fixtures && stata-mp -b do _generate_misc_sens_stata.do`

Tests: `tests/reference_parity/test_misc_sens_R_parity.py`,
`tests/reference_parity/test_misc_sens_stata_parity.py`.

## 1. Per-function table

| function | reference | class | max rel err est / SE | test |
| --- | --- | --- | --- | --- |
| `mi_estimate` (Rubin pooling) | R `mice::pool` 3.19.0; Stata 18 `mi estimate: regress` | 2 | est 4e-16, SE 1e-15, df 1.4e-14, p 3e-13 (R); FMI vs Stata via `fmi_barnard_rubin` 1e-12 | R + Stata |
| `mice` (imputation) | — | 5 (stochastic; not compared) | — | — |
| `mediate_sensitivity` | R `mediation::medsens` 4.5.1 (lm/lm) | 2 | ACME 8e-14, CI 7e-13 (medsens eps); fixed point vs `eps=1e-26`: 3e-13 | R |
| `calibrate_confounding_strength` | R `sensemakr::ovb_bounds` 0.1.6 | 2 | 1.3e-15 est, 2e-16 SE, CI 1e-12 | R |
| `unified_sensitivity` | `EValue::evalues.OLS` 4.1.4, `sensemakr` (rv_q, rv_qa), `sp.oster_delta` (psacalc-graded in round 1) | 2 | 1e-12 | R |
| `survival_sensitivity` | `EValue::evalues.HR` (bias factor at CI limit) | 2 (identity-level) | grid 1e-5 abs | R |
| `copula_sensitivity` | none (arXiv method, no package) | 6 | — | — |
| `subgroup_analysis` | Stata `regress, vce(robust)` / OLS + `testparm` | 1 (+F form added) | ≤1e-9 | Stata |
| `ancova` | Stata `regress, vce(robust|cluster)` | 1 | ≤1e-9 | Stata |
| `negd` | Stata `regress` (ancova & change score) | 1 | ≤1e-9 | Stata |
| `attrition_test` | Stata `tabulate, chi2`; `regress` | 3 (Yates default; `correction=False` = Stata) | 1e-15 | Stata |
| `attrition_bounds` | Stata `leebounds` 1.5 (shipped and exact-threshold copy) | 2 | 1e-12 | Stata |
| `balance_check` | Stata `iebaltab` 7.5 | 3 (Welch default; `equal_var=True` = iebaltab) | t 1e-10, F 1e-9 | Stata |
| `mr_bma` | Zuber et al. `summary_mvMR_BF` (demo_AMD @ 4981b5a, MIT) | 2 | pp 7e-15, marginal 6e-15, BMA est 8e-15 | R |
| `mr_mediation` | `MendelianRandomization::mr_ivw` + `mr_mvivw` 0.10.0 | 2 | ≤3e-16 | R |
| `mr_multivariable` (RSE<1) | `mr_mvivw` default model | 2 | est 9e-16, SE 2e-16 | R |
| `mendelian_randomization` | `mr_allmethods(method="main")` | 1 (IVW, Egger, intercept, WM estimate); WM SE bootstrap = 5 | 1e-15 | R |
| `grapple` | GRAPPLE 0.2.2 `grappleRobustEst` (GitHub 317e837; sourced, not installable) | 2 → aligned | sandwich at GRAPPLE's point: l2 8e-16, tukey/huber 4e-7 (R `integrate` moments); fitted β ≤ 8e-4, τ² ≤ 6e-5, SE ≤ 3e-5 (GRAPPLE stops early: its score at its β is O(1e-3); ours 1e-15) | R |
| `transport_weights_fn` / `transport_generalize` | R `glm` + `quantile(type=7)` + `sandwich::vcovHC(HC0)` 3.1.1 (no canonical transport package, see round-1 `pate`) | 2 | 7e-16 | R |
| `heterogeneity_of_effect` | `metafor::rma(method="DL")` 5.0.1 | 1 | 4e-16 | R |
| `synthesise_evidence` (inverse_variance) | `metafor::rma(method="FE")` | 1 | 4e-16 | R |
| `identify_transport` | `causaleffect::transport` 1.3.15 | 2 (descendant bug) + 6 (different identification problem: causaleffect uses target observational data) | structural | R |
| `rwd_rct_concordance` | — (three lines of arithmetic) | 6 | — | — |
| `randomize` | randomizr 2.0.1 `complete_ra` rule (source transcribed; draws cannot match across RNGs) | 2 | rule-level tests | `tests/test_randomize_design.py` |
| `copula_sensitivity` | none (arXiv method, no package) | 6 | — | — |
| `optimal_design` | not examined (experimental/optimal.py owned by another line) | — | — | — |

## 2. Defects (all found against the reference on identical bytes)

1. **`mi_estimate` df and covariance** (default output changes). Used Rubin's
   large-sample df `(m-1)(1+1/r)^2` everywhere while its comment said
   Barnard-Rubin; pooled only the diagonal of the within covariance and called
   the estimator a second time for names. Now: Barnard-Rubin df with
   `dfcom = data_info['df_resid']` (mice / Stata), full `var_cov`, p/CI from
   t(df), returns `ubar, b, t, riv, lambda, fmi, fmi_barnard_rubin, df, dfcom,
   ci_lower, ci_upper`. Example x2: df 31.25 → 24.99, p 1.5656e-06 (mice) now
   exact. First divergence: `df`.
2. **`mediate_sensitivity` wrong sensitivity function** (default output
   changes). Subtracted a heuristic bias `α_T ρ σ_Y/σ_M`; not Imai-Keele-
   Yamamoto. Now the medsens SUR/FGLS with ρ fixed, delta-method SE/CI,
   exact crossing ρ̃ = corr(resid M~T+X, resid Y~T+X). Reference data:
   crossing 0.558 → 0.487; ACME(−0.9) 0.852 → 1.533. medsens' default stopping
   rule stops ~1e-4 short at |ρ|=0.9; `eps=sqrt(machine eps)` reproduces it.
3. **`calibrate_confounding_strength` bias bound off by √dof** (API: `dof=`
   now required). Bound was `√(k r_y · k r_d/(1−k r_d)) · se` — no √dof and
   linear scaling of both R². Now Cinelli-Hazlett benchmark bounds exactly as
   `ovb_bounds`. Reference data, k=5: bias 0.0199 → 0.4640; an estimate of
   0.10 went from "robust" to breakpoint k=1.5.
4. **`survival_sensitivity` never overturned protective effects**. Worst case
   was `log_hr − log Γ` regardless of sign. Now moves toward the null.
   log_hr=−0.4, se 0.15: breakpoint None → 1.2 (= positive case).
5. **`unified_sensitivity`**: `rho_max` ignored on the data path (always
   1.3 rule) while documented default 1.0 was used on the summary path —
   the two paths disagreed; default is now Oster's min(1, 1.3 R²) on both and
   an explicit value is honoured. RR CI reported the rescaled t CI, not the
   interval the E-value used (now EValue's `exp(0.91 d ± 1.78 se/sd)`, 1e-12).
6. **`attrition_bounds(method='lee')`** kept `n − ceil(qn)` obs (one fewer
   than Lee's rule) and disagreed with `sp.lee_bounds`; now delegates to the
   shared helper, adds `trimming=`. Old (0.70358, 1.61981) → quantile rule
   (0.71883, 1.60455) = `sp.lee_bounds`; `trimming='exact'` (0.70557,
   1.61782) = `leebounds` with exact thresholds (shipped `leebounds`:
   0.70358, 1.61782 — its rounded-threshold artefact, round-1 finding).
7. **`mr_bma` was BIC-BMA under the MR-BMA name** (default output changes).
   Now Zuber et al.'s Bayes factor (IVW scaling, normal prior σ=0.5),
   `model_averaged_estimate` added; `method='bic'` keeps the old quantity.
8. **`mr_multivariable` SE shrank under under-dispersion** (RSE<1 multiplied
   the SE down); `mr_mvivw` floors at 1. Only affects RSE<1 data.
9. **`mr_mediation` total effect used the fixed-effect IVW SE** (the defect
   round 1 fixed in `sp.mr_ivw`); now calls `sp.mr_ivw`.

10. **`grapple` was a different estimator** (default output changes): a
   joint Gaussian MLE with a numerical Hessian SE, not GRAPPLE's robust
   profile score. Now solves GRAPPLE's estimating equations (Tukey default,
   `loss=` huber / l2) with its sandwich. LDL data: β 2.694 → 2.7197
   (GRAPPLE 2.7196), SE 0.510 → 0.5520.
11. **`transport_weights_fn` SE** used Σw(y−m)² instead of Σw²(y−m)² (not
    invariant to rescaling w). Reference data: 0.0864 → 0.1556 (= HC0).
12. **`identify_transport` admitted descendants of X** as the adjustment set
    and weighted by the target margin P(Z)_T: X→Z→Y, S→Z returned a wrong
    formula; now "not transportable" under the covariates-only design.
13. **`randomize`**: `method='complete'` silently did simple randomization;
    strata counts used round-half-to-even and gave odd-stratum misfits to a
    fixed arm (5 → 2 treated, 7 → 4); cluster assignment was Bernoulli;
    re-randomization redrew by simple randomization, discarding strata and
    clusters. Now randomizr's `complete_ra` rule within strata / over
    clusters, and re-randomization redraws from the same design.

Additions without numeric change: `subgroup_analysis` het test also reports
`F`, `pvalue_F`, `df_resid` (Stata `testparm`); `attrition_test(correction=)`;
`balance_check(equal_var=)`.

## 3. Proposed promotion records

```python
"mr_bma": {"status": "bit-exact", "reference": "Zuber et al. summary_mvMR_BF (GitHub verena-zuber/demo_AMD 4981b5a)",
           "reference_versions": {"summary_mvMR_BF.R": "demo_AMD@4981b5a"}, "tolerance": "1e-12 rel",
           "sides": ["py", "R"], "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
           "note": "IVW-scaled Bayes factor, prior sd 0.5, prior_prob 0.5 and 0.1; method='bic' keeps the pre-1.30 quantity."},
"mr_mediation": {"status": "bit-exact", "reference": "R MendelianRandomization::mr_ivw + mr_mvivw",
                 "reference_versions": {"MendelianRandomization": "0.10.0"}, "tolerance": "1e-12 rel",
                 "sides": ["py", "R"], "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
                 "note": "Total and direct effects; the indirect SE has no reference."},
"mendelian_randomization": {"status": "bit-exact", "reference": "R MendelianRandomization::mr_allmethods(method = 'main')",
                            "reference_versions": {"MendelianRandomization": "0.10.0"}, "tolerance": "1e-12 rel",
                            "sides": ["py", "R"], "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
                            "note": "IVW, Egger (+intercept), weighted-median estimate; WM bootstrap SE is Monte Carlo."},
"grapple": {"status": "aligned", "reference": "GRAPPLE::grappleRobustEst (GitHub jingshuw/GRAPPLE 317e837)",
            "reference_versions": {"GRAPPLE": "0.2.2"}, "tolerance": "sandwich at GRAPPLE's estimates 1e-6 (l2 1e-12); fitted beta 1e-3, tau2 / SE 1e-4",
            "sides": ["py", "R"], "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
            "note": "GRAPPLE stops its optim / uniroot early (score O(1e-3) at its estimate); StatsPAI solves the equations to machine precision."},
"transport_weights_fn": {"status": "bit-exact", "reference": "R glm + quantile(type = 7) + sandwich::vcovHC(HC0)",
                         "reference_versions": {"sandwich": "3.1.1"}, "tolerance": "1e-12 rel",
                         "sides": ["py", "R"], "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
                         "note": "Composition of base-R pieces; no canonical transport package exists."},
"heterogeneity_of_effect": {"status": "bit-exact", "reference": "R metafor::rma(method = 'DL')",
                            "reference_versions": {"metafor": "5.0.1"}, "tolerance": "1e-12 rel",
                            "sides": ["py", "R"], "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
                            "note": "tau2, Q, Q p-value, I2."},
"synthesise_evidence": {"status": "bit-exact", "reference": "R metafor::rma(method = 'FE')",
                        "reference_versions": {"metafor": "5.0.1"}, "tolerance": "1e-12 rel",
                        "sides": ["py", "R"], "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
                        "note": "weight_mode='inverse_variance' only."},
"mi_estimate": {
    "status": "bit-exact",
    "reference": "R mice::pool; Stata mi estimate: regress",
    "reference_versions": {"mice": "3.19.0", "Stata": "18"},
    "tolerance": "1e-9 rel (p, CI via t quantiles at fractional df); 1e-12 est/SE/df",
    "sides": ["py", "R", "Stata"],
    "test": ["tests/reference_parity/test_misc_sens_R_parity.py",
             "tests/reference_parity/test_misc_sens_stata_parity.py"],
    "note": "Pooling only, on R's five mice imputations; Barnard-Rubin df with dfcom = residual df. Stata's FMI is the Barnard-Rubin small-sample FMI (fmi_barnard_rubin).",
},
"mediate_sensitivity": {
    "status": "bit-exact",
    "reference": "R mediation::medsens (lm/lm, rho.by = 0.1)",
    "reference_versions": {"mediation": "4.5.1"},
    "tolerance": "1e-10 rel",
    "sides": ["py", "R"],
    "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
    "note": "eps=sqrt(machine eps) reproduces medsens' stopping rule; default iterates to the fixed point (= medsens(eps=1e-26)).",
},
"calibrate_confounding_strength": {
    "status": "bit-exact",
    "reference": "R sensemakr::ovb_bounds (kd = ky = k)",
    "reference_versions": {"sensemakr": "0.1.6"},
    "tolerance": "1e-12 rel (CI 1e-10)",
    "sides": ["py", "R"],
    "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
    "note": "Benchmark covariate x2; dof required.",
},
"unified_sensitivity": {
    "status": "bit-exact",
    "reference": "R EValue::evalues.OLS; sensemakr::sensemakr (rv_q, rv_qa)",
    "reference_versions": {"EValue": "4.1.4", "sensemakr": "0.1.6"},
    "tolerance": "1e-10 rel",
    "sides": ["py", "R"],
    "test": ["tests/reference_parity/test_misc_sens_R_parity.py"],
    "note": "Oster component equals sp.oster_delta (psacalc-graded).",
},
"attrition_bounds": {
    "status": "bit-exact",
    "reference": "Stata leebounds (thresholds held exactly)",
    "reference_versions": {"leebounds": "1.5", "Stata": "18"},
    "tolerance": "1e-12 rel",
    "sides": ["py", "Stata"],
    "test": ["tests/reference_parity/test_misc_sens_stata_parity.py"],
    "note": "trimming='exact'; default quantile rule equals sp.lee_bounds.",
},
"ancova": {"status": "bit-exact", "reference": "Stata regress, vce(robust) / vce(cluster)",
           "reference_versions": {"Stata": "18"}, "tolerance": "1e-9 rel",
           "sides": ["py", "Stata"], "test": ["tests/reference_parity/test_misc_sens_stata_parity.py"],
           "note": "HC1 and CR1 with t(N-k) / t(G-1)."},
"negd": {"status": "bit-exact", "reference": "Stata regress, vce(robust)",
         "reference_versions": {"Stata": "18"}, "tolerance": "1e-9 rel",
         "sides": ["py", "Stata"], "test": ["tests/reference_parity/test_misc_sens_stata_parity.py"],
         "note": "ANCOVA and change-score forms."},
"subgroup_analysis": {"status": "bit-exact", "reference": "Stata regress + testparm",
                      "reference_versions": {"Stata": "18"}, "tolerance": "1e-9 rel",
                      "sides": ["py", "Stata"], "test": ["tests/reference_parity/test_misc_sens_stata_parity.py"],
                      "note": "HC1 and classical; interaction test as F (testparm) and chi2 = qF."},
"attrition_test": {"status": "bit-exact", "reference": "Stata tabulate, chi2; regress",
                   "reference_versions": {"Stata": "18"}, "tolerance": "1e-10 rel",
                   "sides": ["py", "Stata"], "test": ["tests/reference_parity/test_misc_sens_stata_parity.py"],
                   "note": "correction=False (Pearson); default keeps Yates."},
"balance_check": {"status": "bit-exact", "reference": "Stata iebaltab (ietoolkit)",
                  "reference_versions": {"ietoolkit": "7.5", "Stata": "18"}, "tolerance": "1e-9 rel",
                  "sides": ["py", "Stata"], "test": ["tests/reference_parity/test_misc_sens_stata_parity.py"],
                  "note": "equal_var=True; iebaltab's difference is control minus treatment."},
```

## 4. CHANGELOG / MIGRATION (draft)

⚠️ Correctness: items 1–9 of §2. MIGRATION rows:

| function | old | new | reproduce old |
| --- | --- | --- | --- |
| `mi_estimate` / `MICEResult.combine` | Rubin large-sample df, diagonal U | Barnard-Rubin df, full U | pass estimates without `df_resid` to `combine` (large-sample df) |
| `mediate_sensitivity` | heuristic linear bias | IKY / medsens | not kept (wrong formula) |
| `calibrate_confounding_strength` | no √dof, linear R² scaling | sensemakr bounds, `dof=` required | not kept |
| `survival_sensitivity` | worst case away from null for HR<1 | toward null | not kept |
| `unified_sensitivity` | `rho_max` ignored on data path | honoured; default 1.3 rule | pass `rho_max=1.0` |
| `attrition_bounds` | n − ceil(qn) kept | Lee quantile rule | not kept |
| `mr_bma` | BIC weights | Zuber Bayes factor | `method='bic'` |
| `mr_multivariable` | SE × RSE when RSE<1 | SE × max(1,RSE) | not kept |
| `mr_mediation` | fixed-effect total SE | random-effects (sp.mr_ivw) | not kept |
| `grapple` | Gaussian MLE | GRAPPLE robust profile score (Tukey) | not kept (different estimator) |
| `transport_weights_fn` / `transport_generalize` | SE with w | SE with w² (HC0) | not kept |
| `identify_transport` | mediators admissible | non-descendants of X only | not kept |
| `randomize` | see §2.13 | randomizr rule | not kept (draws differ for the same seed) |

## 5. Open / not closed

- `mr_clust` (class 6): `mrclust::mr_clust_em` fits a different mixture (null
  + junk + K Gaussian components with its own initialisation, output rounded
  to 3 dp); sp's EM on Wald ratios with BIC over K is not that model.
  Reference output is in the fixture (`mrclust`) but not asserted.
- `mr_lap` (class 6): R `MRlap` (GitHub) not installed; it is an LDSC-based
  pipeline on full GWAS, sp implements the Burgess-Davies-Thompson closed
  form. Not comparable.
- `copula_sensitivity`, `rwd_rct_concordance` (class 6): no package.
- `synthesise_evidence(weight_mode='rct_heavy')`, `mr_mediation` indirect SE:
  no reference quantity.
- `identify_transport`: sufficient-condition search only (documented); a
  complete Bareinboim-Pearl implementation would be a feature.
- `optimal_design`: not examined (release-line file).
- `mice` imputation step: stochastic, not compared.

## Integrator items (registry / schemas)

- `registry.py` ParamSpec drift: `unified_sensitivity.rho_max` default
  1.0 → None (intentional: one default on both paths; `tests/test_registry_default_contract.py`
  fails until the spec is updated).
- New parameters needing ParamSpecs + schema regeneration:
  `mediate_sensitivity(conf_level, eps, max_iter)`,
  `calibrate_confounding_strength(dof [required], multipliers)`,
  `mr_bma(prior_sd, method)`, `grapple(loss, k, tol, max_iter)`,
  `attrition_bounds(trimming)`, `attrition_test(correction)`,
  `balance_check(equal_var)`.
- Pre-existing doctest failures (not caused here):
  `robustness/subgroup.py` and `transport/__init__.py` module docstrings use
  undefined `df` / `rct`.

## 6. .gitignore

`tests/reference_parity/_fixtures/_ado_misc_sens/` and
`tests/reference_parity/_fixtures/_ado_misc_sens_patched/` (covered by the
round-1 `_ado_*/` pattern). R packages installed in the user library:
causaleffect 1.3.15, combinat 0.0-8.
