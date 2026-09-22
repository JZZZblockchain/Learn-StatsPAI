# Phase 3, round 2: `open_items`

Worktree: `.claude/worktrees/r2-open-items`. The round-1 baseline is staged, and this round's work is the unstaged diff plus the untracked files. Nothing is committed.

Five threads ran in parallel: time series (the lead), frontier, spatial, treatment effects, and postestimation. The rd_iv sub-agent was stopped by the API limit before it reported, so its items are listed as open in §R below.

## Summary by outcome class

| item | class | note |
|---|---|---|
| `structural_break(method='bai-perron')`, the default | 2 → 1 | Defect: it ran a binary segmentation, not the Bai-Perron procedure. Now matches `mbreaks::dosequa` |
| sup-F p-value | 1 (default changed) | Hansen (1997), the same as strucchange and Stata `sbsingle` |
| CUSUM boundary vs Stata | 4 | Stata's hard-coded constants are imprecise. Independent numerical proof |
| Fisher L* 5N+3 vs 5N+4 | 4 (Stata side) | Stata's ado disagrees with Stata's own manual and with the t-moment identity |
| xtbreak F(l+1\|l) | 3 | Different convention (the BP test, not the procedure). Rebuilt from our numbers |
| `malmquist` | 2 → 1 (aligned) | Defect: EC included noise |
| `zisf` | 1 (aligned) | New references `chks` (Stata) and `sfa::zsfm` (R). JLMS label defect fixed |
| `mgwr` bandwidth search | 2 → 1 (bit-exact) | Now matches PySAL mgwr |
| `spatial_panel` two-way vs xsmle | 4 | xsmle stops short of its own maximum; its `leeyu` option drops the time effects. MC plus analytic argument. New opt-in `twoways_lag="within"` |
| `gformula_ice_fn` point | 1 | `ltmle(gcomp=TRUE)` |
| `tmle` ATT | 3 | Shown to be a genuine TMLE. R's `oneStepATT` reproduced exactly in Python |
| `policy_value` | 2 → 1 | Silent-broadcast defect |
| `margins_at` / `contrast` / `pwcompare` | est/SE 1; 5 defects (D1–D5) pinned as strict xfail | `postestimation/` belongs to another line and was not edited |
| rd_iv leftovers (`ivqreg` over-identified, Stata `weakiv` residual, `effective_f_test` labels, rdlocrand T3, class-6 re-search) | **open** | See §R |

**Default-output changes, each needing a CHANGELOG ⚠️ entry and a MIGRATION row:**
- `structural_break` (the default method and the sup-F p-value)
- `malmquist`
- `mgwr`
- `zisf` JLMS efficiency (not the default efficiency)
- **Pending, for the postestimation line:** margins D1, D3 and D5

**Files owned by other lines that were touched (flagged):**
- `tests/reference_parity/test_frontier_struct_R_parity.py`: Malmquist now passes `efficiency="residual"`
- `tests/reference_parity/test_spatial_survey_R_parity.py`: mgwr now passes `kernel_eps=1.0, tol=1e-15`
- `tests/test_structural_break_size.py` and `tests/reference_parity/test_structural_break_parity.py`: Bai-Perron results now carry `critical_values` in place of `p_values`
- `tests/spatial/test_gwr.py`: an assertion that is not a property of MGWR was dropped

**Integrator items:**
- Rerun `scripts/dump_schemas.py` for the new parameters:
  - `structural_break(pvalue_method=)`
  - `malmquist(efficiency=)`
  - the new `mgwr` arguments
  - `spatial_panel(twoways_lag=)`
- Add the matching registry ParamSpecs.
- Add a `.gitignore` line for `_fixtures/_ado_r2_*`; the existing `_ado_*/` pattern already covers it.
- Candidates for `paper.bib`, with DOIs verified on Crossref:
  - Hansen (1997), 10.2307/1392074
  - Choi (2001), 10.1016/S0261-5606(00)00048-6
  - Fuentes, Grifell-Tatjé & Perelman (2001), 10.1023/A:1007852020847
- Decide on a side token for Python references (`"Python-ref"`) in the `mgwr` record.

## Time series: sup-F p-value, sequential Bai-Perron, CUSUM boundary, Fisher L*

Done by the lead (tag `r2_ts`).

Files:
- Data: `_fixtures/_generate_r2_ts_data.py` writes `r2_ts_break.csv`: n = 300; three mean shifts; one and two slope/intercept breaks; white noise. The round-1 `ts_break.csv` is reused.
- R: `_generate_r2_ts_R.R` writes `r2_ts_R.json` (strucchange 1.5.4, mbreaks 1.0.1).
- Stata: `_fixtures/_generate_r2_ts_stata.do` writes `r2_ts_Stata.json`. It uses Stata 18 `estat sbsingle` and Mata `pvalsup()`, plus SSC xtbreak 2.2 and moremata installed in `_ado_r2_ts/`.
- Test: `tests/reference_parity/test_r2_ts_parity.py`, 45 tests.

### (a) Per-item results

| item | reference | class | max rel err | test |
|---|---|---|---|---|
| sup-F p-value (`structural_break(method='sup-f'/'chow')`) | `strucchange::sctest(Fstats, type="supF")` 1.5.4. Stata 18 `estat sbsingle` `r(p_swald)` and Mata `pvalsup()` on a 54-point grid (k ∈ {1,2,3,5,10,40} × π0 from .005 to .5). Hansen's own `pv_sup.R` | 1, via a new default `pvalue_method="hansen"`. The old Monte-Carlo p-value remains available as `"simulate"` | p vs R 3.7e-13 on the grid (abs ≤ 3.6e-15), 6 data cases ≤ 1e-15 rel; vs Stata ≤ 2.7e-11 (Stata stores p to about 12 digits). Wald statistic ≤ 1e-14 | `test_supf_pvalue_*`, `test_hansen_pvalue_*` |
| `structural_break(method='bai-perron')`, the default | `mbreaks::dosequa` 1.0.1 (Nguyen, Yamamoto and Perron; MIT) with `prewhit=0, robust=0, hetdat=1, hetvar=0` | **2 → 1** | break dates identical in 6 cases × 4 levels. Every step statistic equals the traced `mbreaks:::pftest` value, 1e-10 asserted (observed ~1e-14). CV tables equal exactly | `test_bai_perron_sequential_matches_dosequa` |
| xtbreak `F(l+1|l)` | SSC xtbreak 2.2 (Ditzen, Karavias and Westerlund), `hypothesis(3) sequential breakconstant` | 3: xtbreak computes the Bai-Perron *test* (breaks estimated globally, one pooled σ² with T−(l+2)q df), not the per-segment statistic of the sequential *procedure*. Rebuilt from our SSRs | F(1|0) 1e-15; F(2|1) rebuilt 1e-15 | `test_xtbreak_f_next_is_the_bp_test_convention` |
| CUSUM boundary vs Stata constants (round-1 grade B) | Stata 18 `sbcusum.ado` hard-coded constants; strucchange closed form | 4: Stata's constants are imprecise. Independent evidence below | ours equals the exact root; Stata off by −7.7e-7 / +2.5e-6 / +1.2e-6 | `test_cusum_boundary_is_exact_root_and_stata_constant_is_not` |
| Fisher L* constant (Stata 5N+3 vs plm 5N+4) | plm 2.6.7 (T2 from round 1); Stata `_xturfisher.ado` line 145 | 4 on the Stata side, with an analytic proof below. Choi (2001) itself could not be read | analytic identity to 1e-14 | `test_fisher_logit_constant_matches_t_moments`, `test_panel_unitroot_uses_5n_plus_4` |

**Fisher L\*: which constant is right.** Choi's paper (JIMF 20(2):249–272, DOI 10.1016/S0261-5606(00)00048-6, confirmed on Crossref) is paywalled; Unpaywall lists no open-access copy. The formula therefore has not been read from the paper. Four pieces of evidence point the same way:

1. **Stata's own manual contradicts Stata's code.** The *Methods and formulas* section of `[XT] xtunitroot` (stata.com/manuals/xtxtunitroot.pdf, read here) prints `k = 3(5N+4)/(π²N(5N+2))` and `L* ~ t(5N+4)`. `_xturfisher.ado` line 145 codes `3*(5*r(N)+3)` and line 147 codes df `5*r(N)+4`.
2. **plm** codes 5N+4 in both places.
3. **Analytic identity.** Under H0 each ln(p/(1−p)) is standard logistic, with variance π²/3 and excess kurtosis 6/5. So L = Σ has variance Nπ²/3 and excess kurtosis 1.2/N.
   - Matching the kurtosis to t_ν's 6/(ν−4) gives ν = 5N+4.
   - Matching the variance, k·Nπ²/3 = ν/(ν−2), then gives k = 3(5N+4)/(π²N(5N+2)).
   - Stata's 5N+3 is inconsistent with its own df.
4. The test asserts this identity for N ∈ {1, 2, 5, 12, 50}.

Conclusion: StatsPAI, like plm, is right, and Stata's ado has a typo. Class 4, to be recorded in `STATA_HEADLINE_GAP_EXCEPTIONS` if the module is ever promoted to Track A. Worth reporting to StataCorp.

**CUSUM: which boundary is right.** strucchange's `pvalue.efp` evaluates
2[1 − Φ(3x) + e^{−4x²}(Φ(x)+Φ(5x)−1) − e^{−16x²}(1−Φ(x))].

An independent computation was used as a check. It propagates the Gaussian transition density on the moving interval [−a(1+2t), a(1+2t)] with Gauss–Legendre quadrature, multiplying by the exact Brownian-bridge non-crossing factor for each linear boundary between time steps.

Findings:
- At M = 50–200 steps and 400–800 nodes, the numerical crossing probability agrees with the closed form to about 1e-12. So the closed form is exact to that accuracy, not a truncation.
- StatsPAI's `boundary_coef` is its root, found with brentq at 1e-14.
- Stata's constants have crossing probabilities of 0.0100000791, 0.0499991147 and 0.0999993370. Their errors are relative −7.7e-7, +2.5e-6 and +1.2e-6, with mixed signs.
- They are not roots of the two-term Brown-Durbin-Evans approximation either, nor of the three-term series without the e^{−16x²} term; both were tried.

Conclusion: Stata's constants are imprecise at the 1e-6 level. StatsPAI is right. The round-1 test's `rtol=3e-6` against Stata stays as the documented class-4 gap.

**sup-F p-value.** Hansen (1997), *Approximate Asymptotic P Values for Structural-Change Tests*, JBES 15(1):60–67, DOI 10.2307/1392074 / 10.1080/07350015.1997.10524687. It was checked on Crossref, and Hansen's program page users.ssc.wisc.edu/~bhansen/progs/jbes_97.html was read.

His R code `pv_sup.R` was downloaded from that page and parsed:
- Its 40 × 25 × 3 coefficient table equals `strucchange:::sc.beta.sup` exactly (max abs difference 0).
- Stata's `pvalsup()` reproduces it on the grid.

`hansen_supf_pvalue` transcribes `pv_sup`. It is evaluated at strucchange's λ = ((n−from)·to)/(from·(n−to)) over the integer candidate range; a single candidate date gives an F(k, n−2k) Chow test, as in `sctest`.

Stata's `sbsingle` uses a different trimmed range when 0.15·n is not an integer (n = 250: Stata's first regimes 38..212, strucchange's 37..213). On these fixtures the supremum lies inside both ranges and the p-values agree, but for other data Stata's p can differ through π0.

### (b) Defects

**T1 — `structural_break(method='bai-perron')` (the default) was not the Bai-Perron sequential procedure. ⚠️ correctness, default output changes.**

It was a binary segmentation with three differences from Bai-Perron:
- Each segment used its own relative trimming, `int(seg_len·min_segment)`, instead of the global h = floor(ε·T).
- Its candidate range dropped the last admissible date.
- Every step was referred to the full-sample sup-F(1|0) law, via the MC p-value at `alpha`, instead of Bai-Perron's sup F(l+1|l) critical values, which grow with l.

How it was found: reading `mbreaks:::sequa`. Round 1 had class-6'd this path as "no package computes this".

Fix: new `_bai_perron_sequential`, a transcription of `sequa`. It uses the tables in the new `timeseries/_break_tables.py`, which the test asserts are equal to `mbreaks::supF_next_cv1..5`.

Result fields:
- `f_stats`: the accepted sup F(l+1|l) statistics, on mbreaks' scale.
- `critical_values`: the new critical-value field.
- `sequential_tests`: every step, including the final non-rejection.
- `p_values` is now `None`, since there is no p-value approximation for F(l+1|l).
- `min_segment` must be one of .05, .10, .15, .20, .25, and `alpha` one of .10, .05, .025, .01. Other values raise.

Before → after:
- The fixture cases give identical dates after the fix. Only the reported statistics change: F scale → Wald scale, and p-values → critical values.
- The old per-segment trimming and full-sample null can select different dates on other data, so the default output is not guaranteed unchanged.
- Two existing tests that pinned `p_values` were updated: `tests/test_structural_break_size.py::test_bai_perron_exposes_aligned_stats` and `tests/reference_parity/test_structural_break_parity.py::test_break_improves_fit_and_is_significant`.

**T2 — sup-F p-value default changed from a fixed-seed MC to Hansen (1997). ⚠️ default output.**

This is a convention move rather than a bug. Both are approximations of the Andrews law, but the MC had 1/5001 resolution and grid dependence, while Hansen's approximation is the one R, Stata and the method's author use.

Before → after on `r2_wn`: `pvalue_method="simulate"` still returns the old MC value (within 0.03 of Hansen's, asserted); the default now returns 0.2297329322069956, which equals R's value (0.22973293220700686) to 1e-15 rel.

The old number stays reachable through `pvalue_method="simulate"`.

### (c) Proposed `_FROZEN_PROMOTIONS`

```python
"structural_break": {
    "status": "bit-exact",
    "reference": "strucchange::Fstats + sctest(type = 'supF') / breakpoints; mbreaks::dosequa (Bai-Perron sequential); Stata estat sbsingle",
    "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "strucchange": "1.5.4", "mbreaks": "1.0.1", "Stata": "18"},
    "tolerance": "statistics 1e-10 rel (observed <= 1e-14); sup-F p-values 1e-10 rel for p > 1e-6, 1e-13 abs below (R uses 1 - pchisq); break dates exact",
    "sides": ["py", "R", "Stata"],
    "test": ["tests/reference_parity/test_r2_ts_parity.py", "tests/reference_parity/_fixtures/r2_ts_R.json", "tests/reference_parity/_fixtures/r2_ts_Stata.json", "tests/reference_parity/test_timeseries_R_parity.py"],
    "note": "sup-F p-value = Hansen (1997) pv_sup (table equal to strucchange sc.beta.sup and Stata pvalsup) at strucchange's lambda; method='bai-perron' = mbreaks::dosequa(prewhit=0, robust=0, hetdat=1, hetvar=0), 6 series x 4 levels, every step statistic matched to the traced pftest; 'global' = breakpoints (round 1). xtbreak's F(l+1|l) is the BP test with global breaks and a pooled sigma (convention, rebuilt). The default bai-perron path was a binary segmentation with a full-sample null before this round.",
},
```

If a record for `cusum_test` already exists (round 1), add to its note: "Boundary = exact root (checked against an independent density-propagation computation); Stata sbcusum's hard-coded constants miss it by up to 2.5e-6 (class 4)". Add the matching note to `panel_unitroot`: "Stata L* uses 5N+3 in k against its own manual and the t(5N+4) moment match (class 4)".

### (d) CHANGELOG / MIGRATION

- **⚠️ Correctness:** `sp.structural_break(method="bai-perron")`, the default, now runs the Bai-Perron sequential procedure (as in `mbreaks::dosequa`):
  - It uses a global minimum segment `h = floor(min_segment·n)` and the Bai-Perron sup F(l+1|l) critical values.
  - The earlier binary segmentation used per-segment trimming and the full-sample sup-F null.
  - `p_values` is `None`; the new fields are `critical_values` and `sequential_tests`.
  - `min_segment` and `alpha` must be tabulated values.
- **Changed:** the sup-F p-value defaults to Hansen's (1997) approximation, as in strucchange and Stata `estat sbsingle`. New `pvalue_method="hansen"|"simulate"`.
- **Added:** `hansen_supf_pvalue` (module-level), `timeseries/_break_tables.py`, and round-2 parity fixtures (strucchange, mbreaks, Stata sbsingle / pvalsup, xtbreak).
- **MIGRATION rows:**

  | call | old | new | how to get the old output |
  |---|---|---|---|
  | `structural_break()` default | binary segmentation, `p_values` list | BP sequential, `p_values=None` | not reachable: the old procedure was not Bai-Perron |
  | sup-F p-value | MC | Hansen (1997) | `pvalue_method="simulate"` |

- **Integrator:**
  - The signature changed, so `dump_schemas.py` must be rerun.
  - The registry needs `ParamSpec("pvalue_method", "str", False, "hansen", "sup-F p-value: 'hansen' (Hansen 1997, strucchange/Stata) or 'simulate' (Monte-Carlo Andrews limit)", ["hansen", "simulate"])`.
  - The `paper.bib` entries `hansen1997approximate`, `choi2001unit` and `nguyen_mbreaks` are not added (the brief forbids editing paper.bib). Both DOIs above were verified on Crossref.
  - Licence note: the Hansen table comes from the author's research code (no licence file) and matches GPL strucchange. The BP tables come from MIT mbreaks. These are published numerical tables; the maintainer should confirm attribution is enough.

### (e) Still open

- **Choi (2001) not read.** It is paywalled with no OA copy. The 5N+4 conclusion rests on the analytic moment match, Stata's own manual and plm, not on the paper text.
- **mbreaks' other options are not implemented.** These include `hetvar=1`, `robust=1`, `prewhit=1`, partial structural change (`x_name`), and the `dorepart` repartition estimates.
- **Stata's sbsingle trimmed range.** Uses ceil(0.15·n) (n = 250: first regimes 38..212), while strucchange uses floor (37..213). This is not an option in sp. It does not matter on the fixtures.

### (f) Housekeeping

- `.gitignore`: `tests/reference_parity/_fixtures/_ado_r2_ts/` (xtbreak and moremata).
- R package installed into the user library: mbreaks 1.0.1.
- The Stata do-file sets `python_exec` to the repository venv (Python 3.10) for the session only, because xtbreak's Python block fails to load under Python 3.13.
- New files:
  - `src/statspai/timeseries/_break_tables.py`
  - `tests/reference_parity/test_r2_ts_parity.py`
  - `tests/reference_parity/_generate_r2_ts_R.R`
  - `tests/reference_parity/_fixtures/_generate_r2_ts_data.py`
  - `tests/reference_parity/_fixtures/_generate_r2_ts_stata.do`
  - `tests/reference_parity/_fixtures/r2_ts_break.csv`
  - `tests/reference_parity/_fixtures/r2_ts_R.json`
  - `tests/reference_parity/_fixtures/r2_ts_Stata.json`
- Modified files: `src/statspai/timeseries/structural_break.py`, `tests/test_structural_break_size.py`, `tests/reference_parity/test_structural_break_parity.py`.
- Tests:
  - 182 passed across `test_r2_ts_parity.py`, `test_timeseries_R_parity.py`, `test_cusum_test_parity.py`, `test_structural_break_parity.py`, `test_structural_break_size.py`, `test_new_v06_modules.py` and `test_correctness_inference_fixes.py`.
  - The `structural_break.py` doctests pass.


## Frontier: `sp.malmquist` and `sp.zisf`

Sub-agent tag `r2_frontier`. Test: `tests/reference_parity/test_r2_frontier_parity.py`.

### (a) Per-function table

| function | reference (version) | class | max rel err est / SE |
|---|---|---|---|
| `sp.malmquist`, default `efficiency="bc"` and `"jlms"` | R sfaR 1.0.1: `sfacross` fitted once per period, plus `efficiencies()$teBC` / `$teJLMS`. EC is taken from the package; TC is computed from sfaR's betas | **2** → T2 on the components | EC 2.7e-7, TC 1.9e-7, M 1.7e-7 (tolerance 1e-6); betas ≤ 1e-6 |
| `sp.malmquist`, corroboration only | R metafrontier 0.3.1 `malmquist_meta(method="sfa")`, two groups `id %% 2`: `EC_group` and `1/TC_group` (its TC is Farrell-oriented) | matches to the reference's optimiser limit. **Not counted as parity.** | 1.8e-5 (tolerance 1e-4). optim's `ndeps` of 1e-3 gives 2.8e-3; 1e-6 gives 1.8e-5. sfaR on the same group-period agrees with us to about 1e-7 |
| `sp.malmquist(efficiency="residual")`, the old default | round-1 R recomputation | 6 (no package computes the composed-residual index) | unchanged |
| `sp.zisf`, production, constant p | Stata 18 `chks` 1.1, `estimation(zsf) eoption(ml)` (`net install` into a private ado dir) | **1 (T2)** | 8.6e-8 / 9.4e-8 (tolerance 1e-6) |
| `sp.zisf`: production, cost, and `zprob=["z"]` | R sfa 1.2.0 `zsfm` (`"ZISF"`, `"ZISF_Z"`, `inefdec=FALSE`). Compared on sfa's own log-likelihood, transcribed from `zsfm`, Newton-polished from sfa's reported point to its optimum (numDeriv score ≤ 3.5e-8) | **1 (T2)**, labelled "sfa likelihood at its optimum" | ≤ 1.3e-8 / ≤ 5.4e-8; logL within 1e-9 |
| `sp.zisf` vs sfa's reported point as returned | the same fits | limited by the reference's optimiser: sfa's L-BFGS-B stops at REL_REDUCTION_OF_F with a score of 3e-4 to 7e-4; logL(sp) ≥ logL(sfa) in all three cases | 1.6e-5 / 1.8e-4 (tolerances 5e-5 / 5e-4) |
| `zisf` P(efficient \| ε) and E[u \| ε, inefficient] | `zsfm` `post.prob` / `jlms` | same optimiser limit | 2.4e-5 / 4.3e-7 (tolerance 1e-4) |

Identity and known-truth tests:
- **`malmquist`:**
  - M = EC·TC.
  - EC equals the ratio of each period's `efficiency("bc")`.
  - TC does not depend on the `efficiency` setting.
  - Simulation: TC recovery has mean log TC within 0.03 and correlation > 0.95.
  - Simulation: the MSE of the TE-ratio EC is less than half that of the residual EC.
- **`zisf`:**
  - Recovery from simulated `zprob` data is within 3.5 SE.
  - The cost model is the exact mirror of the production model.
  - JLMS = exp(−E[u|ε]), and BC ≥ JLMS (Jensen).

### (b) Defects

**M1 ⚠️ correctness (`frontier/malmquist.py`). The efficiency change included noise.**
- *What was wrong:* EC was computed as exp(ε₂ − ε₁), with ε = y − x'β. That includes v₂ − v₁, and M inherited it.
- *Docstring:* it claimed D = 1 on the frontier, but 6–19% of firm-periods on the fixture have D > 1. It also attributed the definition to Coelli & Rao, which is a DEA paper.
- *Source for the correct definition:* Pantzios, Karagiannis & Tzouvelekas (JPA 36:21–31, doi:10.1007/s11123-010-0202-2; author PDF, eq. 21 and endnote 1). Under SFA the cross-period distance has no conditional-expectation predictor, so the index is built from its components: TEC is the ratio of predicted efficiencies (Fuentes, Grifell-Tatjé & Perelman 2001), and TC is the frontier shift.
- *Fix:* new argument `efficiency={'bc','jlms','residual'}`, default `'bc'`.
  - EC = TE_{t+1}/TE_t.
  - TC is unchanged.
  - The old quantity remains available as `'residual'`.
- *Before → after on the fixture:*

  | quantity | before | after |
  |---|---|---|
  | mean EC, t→2 / t→3 | 1.0653 / 0.9759 | 1.0389 / 0.9456 |
  | mean M, t→2 / t→3 | 1.0997 / 1.1170 | 1.0730 / 1.0824 |
  | mean TC | 1.0343 / 1.1460 | unchanged |
  | row 1 (M, EC, TC) | (1.26878, 1.15400, 1.09947) | (1.11709, 1.01603, 1.09947) |

- *Default output changes:* yes.

**M2 (`malmquist.py`). The documented `**frontier_kwargs` could not be used.** `usigma` / `vsigma` / `emean` / `cluster` columns were dropped before the call, so every use of these options raised `MethodIncompatibility`. The columns are now kept, with a regression test.

**Z1 (`frontier/mixture.py`, `zisf`). `efficiency(method="jlms")` and `model_info["mean_efficiency_jlms"]` returned the Battese-Coelli mixture.**
- They now return exp(−E[u|ε]), with E[u|ε] = (1 − P(eff|ε))·E[u|ε, ineff].
- Fixture mean 0.81702 → 0.81279.
- The default BC efficiency is unchanged.

**Reference defect (Stata `chks`).** `chks` silently drops rows with y ≤ 0 even in the linear model, because it runs `gen ln(depvar)` and then `drop if rowmiss`. On the fixture that removed 90 of 500 rows (x1 0.562 vs 0.591).
- The generator passes y + 10 and compares `_cons − 10`; the linear likelihood is invariant to that shift.
- Worth reporting upstream.

**Reference inconsistency (metafrontier 0.3.1, SFA branch).** `EC_group` is Shephard-oriented while `TC_group` is 1/TC (Farrell), so its `MPI_group` mixes the two orientations.

### (c) Proposed `_FROZEN_PROMOTIONS`

```python
"malmquist": {
    "status": "aligned",
    "reference": "sfaR::sfacross 1.0.1 per period + sfaR::efficiencies (teBC / teJLMS); TC from sfaR betas",
    "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "sfaR": "1.0.1", "metafrontier": "0.3.1"},
    "tolerance": "EC / TC / M 1e-6 rel (observed 2.7e-7); metafrontier::malmquist_meta(method='sfa') EC_group and 1/TC_group 1e-4 (observed 1.8e-5, reference optim BFGS with finite-difference gradients)",
    "sides": ["py", "R"],
    "test": ["tests/reference_parity/test_r2_frontier_parity.py", "tests/reference_parity/_fixtures/r2_frontier_R.json"],
    "note": "Default efficiency='bc': EC = TE_{t+1}/TE_t (Battese-Coelli, each period's own frontier), TC = exp(0.5 (x_t + x_{t+1})'(b_{t+1} - b_t)), M = EC * TC. metafrontier's TC_group uses Farrell distances and equals 1 / TC. efficiency='residual' (pre-1.29.0 default, composed-residual EC) has no package reference. Regenerate via _generate_r2_frontier_R.R.",
},
"zisf": {
    "status": "aligned",
    "reference": "Stata chks 1.1 (estimation(zsf) eoption(ml)); R sfa::zsfm 1.2.0 (ZISF / ZISF_Z, likelihood at its optimum)",
    "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "sfa": "1.2.0", "numDeriv": "2016.8.1.1", "stata": "18", "chks": "1.1 (chks.pkg dated 20190320)"},
    "tolerance": "estimates and OIM SEs 1e-6 rel (observed chks 8.6e-8 / 9.4e-8; sfa likelihood at its optimum 1.3e-8 / 5.4e-8); sfa's reported L-BFGS-B point 5e-5 / 5e-4 (observed 1.6e-5 / 1.8e-4)",
    "sides": ["py", "R", "Stata"],
    "test": ["tests/reference_parity/test_r2_frontier_parity.py", "tests/reference_parity/_fixtures/r2_frontier_R.json", "tests/reference_parity/_fixtures/r2_frontier_stata.json"],
    "note": "chks drops rows with y <= 0 (ln(depvar) check), so it is run on y + 10 and _cons - 10 is compared. sfa ZISF parameterises P = exp(-|gamma|) and sigma as SDs (mapped by the delta method); ZISF_Z uses the same logit link; cost via inefdec=FALSE. sfa's reported point stops at score ~3e-4; the T2 comparison is its own log-likelihood Newton-polished to score <= 3.5e-8. Regenerate via _generate_r2_frontier_R.R and _fixtures/_generate_r2_frontier_stata.do.",
},
```

### (d) CHANGELOG / MIGRATION

- **⚠️ Correctness.** `sp.malmquist`: EC is now the ratio of predicted technical efficiencies (`efficiency="bc"`, the default; `"jlms"` is also available). Before, it was exp(ε_{t+1} − ε_t), which includes the change in noise, and M inherited it. TC is unchanged. The old index is available as `efficiency="residual"`.
- **Fixed.** `sp.malmquist` now forwards `usigma` / `vsigma` / `emean` / `cluster`; before, these always raised.
- **Fixed.** `sp.zisf(...).efficiency(method="jlms")` and `model_info["mean_efficiency_jlms"]` now return exp(−E[u|ε]).
- **Added.** `sp.malmquist(efficiency=)`.
- **MIGRATION rows:**
  - `malmquist`: EC / M change (numbers as in §b M1). The old values are reproduced with `efficiency="residual"`.
  - `zisf` JLMS: 0.81702 → 0.81279. The old value was the BC number under the wrong label, so it cannot be reproduced.
- **Citation.** Fuentes, Grifell-Tatjé & Perelman (2001), JPA 15(2):79–94, doi:10.1023/A:1007852020847. Verified on Crossref and in Pantzios et al.'s reference list. It appears as a verified string in the `malmquist.py` docstring. **The integrator should add it to `paper.bib`.** The docstring's FGLR citation was corrected to `fare1992productivity`, and the Coelli–Rao attribution was removed.

### (e) Open items and what was checked

- **The ZISF paper itself.** Kumbhakar, Parmeter & Tsionas (2013) is paywalled and was not read. It is replaced by two independent implementations that agree with each other and with sp: `sfa` (by Parmeter, a KPT co-author) and `chks`.
- **`chks` coverage.** It has no z-covariates in P and no cost option, so those cases have R evidence only.
- **`zsfm`'s own Hessian SEs.** They agree only to 1.8e-4. The T2 SE claim therefore rests on the polished likelihood and on `chks`.
- **Not fixed, flagged: `lcsf`** (round-1 T2) has the same JLMS labelling problem in `mixture.py`. `efficiency_jlms` is the BC mixture, and `inefficiency_jlms` = −log TE_BC. These accessors are unpinned. Easy follow-up.
- **Also checked, no ZISF found:** the sfaR CRAN archive and the `hdakpo/sfaR` GitHub repository. A CRAN scan found `sfa::zsfm`; a GitHub search found `chks`.

### (f) Housekeeping

- **`.gitignore`:** nothing new. The round-1 `_fixtures/_ado_*/` pattern covers `_ado_r2_frontier/`.
- **R packages installed:** sfa 1.2.0 and pso.
- **Stata:** `chks` in the private ado dir.
- **New files:**
  - `tests/reference_parity/test_r2_frontier_parity.py`
  - `tests/reference_parity/_generate_r2_frontier_R.R`
  - `tests/reference_parity/_generate_r2_frontier_data.py`
  - `tests/reference_parity/_fixtures/_generate_r2_frontier_stata.do`
  - `tests/reference_parity/_fixtures/r2_frontier_R.json`
  - `tests/reference_parity/_fixtures/r2_frontier_stata.json`
  - `tests/reference_parity/_fixtures/r2_frontier_zisf_z.csv`
- **Modified:**
  - `src/statspai/frontier/malmquist.py`
  - `src/statspai/frontier/mixture.py` (`zisf` only)
  - `tests/reference_parity/test_frontier_struct_R_parity.py`, a round-1 file. Minimal edit: the Malmquist test now passes `efficiency="residual"`, and the docstring no longer says `zisf` has no reference.
- **Tests, all passing:**
  - 39 in the frontier parity files
  - 100 in `tests/test_frontier.py`
  - 5 doctests
  - 42 harness-contract tests
- **Signature change:** `malmquist(efficiency=)`. Needs `dump_schemas` and a registry ParamSpec.


## Spatial: `sp.mgwr` bandwidth search; `sp.spatial_panel` two-way effects vs xsmle

Sub-agent tag `r2_spatial`. Test: `tests/reference_parity/test_r2_spatial_parity.py` (18 tests).

### (a) Per-function table

| function | reference | class | max rel err est / SE (observed) |
|---|---|---|---|
| `sp.mgwr` (default search) | PySAL `mgwr` 2.2.1 `Sel_BW(multi=True).search()` + `MGWR.fit()` (the authors' code; Python 3.13.9, numpy 2.2.6) | **2 → 1 (bit-exact)** | Bandwidths, initial bandwidth, bandwidth history and iteration count are identical in all 4 configurations. Betas 3.0e-12 (≤ 3.6e-14 except the 200-sweep CV case). SE 9.4e-16, ENP_j 1.0e-15, AICc 0, SOC path 8e-13 |
| `sp.mgwr` vs GWmodel `gwr.multiscale` 2.4.1 search | GWmodel | 6 / open: a different algorithm | GWmodel selects bws [105, 101, 107, 157] (AICc 297.3085); mgwr selects [101, 101, 117, 157] |
| `sp.spatial_panel(effects="twoways")` SAR/SDM vs xsmle 1.4.5 `type(both)` | Stata 18 xsmle | **4**: the reference stops short of its own maximum | xsmle's e(ll) equals the splm/StatsPAI objective evaluated at xsmle's coefficients (1e-12 asserted, about 1e-15 observed). StatsPAI's maximum is higher by 4.85e-5 (SAR) and 5.15e-4 (SDM) |
| xsmle `type(both, leeyu)` | Stata 18 xsmle | **4**: reference defect | Output is identical to `type(ind, leeyu)`: same ρ, same ll, N = 768 = 48·16, so the time effects are dropped. That ρ equals StatsPAI's entity-effects ρ to 3.6e-11 (SAR) and 1e-14 (SDM) |
| `sp.spatial_panel(twoways_lag="within")` (new) | Lee & Yu (2010) eq. 21, direct approach | T1 identities | SSE equals least squares with unit and time dummies (1e-10); score root < 1e-7; SSE_splm = SSE_within + ρ²N Σ_t c_t² (1e-11) |

The four mgwr configurations are:
- adaptive bisquare with AICc (mgwr's default);
- fixed Gaussian with AICc;
- adaptive bisquare with CV (runs 200 sweeps on both sides without converging);
- adaptive exponential with BIC and `multi_bw_min=20`.

Data: Georgia, standardised with ddof 0; y = PctBach, X = (PctFB, PctBlack, PctRural). This is mgwr's own test configuration.

### (b) Defects

**SP1 — the `sp.mgwr` bandwidth search was not MGWR's algorithm (⚠️ default output).** Bisected against the mgwr source (`search.golden_section`, `search.multi_bw`, `sel_bw.Sel_BW._init_section`, `kernels.Kernel`, `gwr.MGWR._chunk_compute_R`). Every stage differed:

| stage | StatsPAI before | mgwr |
|---|---|---|
| search | GWmodel `gold()` | golden section with δ = 0.38197, `np.round` probes, memo of evaluated bandwidths, stop when \|Δcriterion\| ≤ 1e-6, result rounded to 2 decimals |
| bounds | [20, n] | [40 + 2p, n] adaptive; [min d / 2, 2·max d] fixed |
| adaptive kernel | k-th neighbour distance | k-th neighbour distance × 1.0000001 |
| CV criterion | not divided by n | divided by n |
| stopping rule | max\|Δf\| < tol | score of change (SOC) < tol |
| bandwidth freeze | none | freeze after 5 unchanged sweeps |
| SE / ENP_j / AICc | absent | from replaying the recorded bandwidth history |

- *Fix:* `spatial/gwr/mgwr.py` rewritten as a transcription of mgwr. `bandwidth.py` is untouched, so the round-1 `gold()` pins still pass.
- *New outputs:* `bse`, `tvalues`, `ENP_j`, `tr_S`, `sigma2`, `aicc`/`aic`/`bic`/`llf`, `bw_init`, `bws_history`, `scores`, `converged`.
- *New arguments:* `criterion`, `bw_min`/`bw_max`, `bws_same_times`, `rss_score`, `search_tol`, `search_max_iter`, `kernel_eps`.
- *Before → after (Georgia):*
  - bandwidths [93, 101, 156, 158] → [101, 101, 117, 157];
  - RSS 51.2691 → 50.803541834793;
  - AICc 297.0704149757866 and ENP_j [3.3971, 3.5119, 2.7782, 1.7864], both new and both equal to mgwr;
  - runtime 6.2 s → 0.42 s.
- *Default output changed:* yes. `tol` now means the SOC threshold.
- *Kernel convention:* `kernel_eps=1.0` reproduces GWmodel's kernel. mgwr's ε moves the fixed-bandwidth GWmodel betas by 7e-6.

**No source defect in `spatial_panel`.** The analysis:

- *Analytic.* With W row-standardised, J_N W = J_N W J_N. Applying Q gives the direct-approach residual J_N(Ỹ − ρWỸ − X̃β), whose lag is Q(Wy); this is Lee–Yu (2010) eq. 21, the dummy-model profile likelihood. splm instead uses W(Qy) = Q(Wy) + 1·c_t, where c_t ≠ 0 unless W is also column-stochastic (usaww column sums range from 0.33 to 1.70). β(ρ) is identical under the two lags, so SSE_splm = SSE_within + ρ²N Σ_t c_t². Read in Lee & Yu, J. Econometrics 154:165–185 (author PDF), §3.1 eq. 21, §3.2 eq. 24, §3.3.
- *Known-truth Monte Carlo* (`tests/reference_parity/_r2_spatial_twoways_mc.py`). DGP: ρ = 0.4, large trending time effects, 1000 replications. Columns: splm's lag W(Qy); the within lag Q(Wy); the Lee–Yu transformation approach.

  | design | splm W(Qy) bias | within Q(Wy) bias | Lee–Yu transform bias | MC s.e. |
  |---|---:|---:|---:|---:|
  | usaww N = 48, T = 5 | −0.0387 | −0.0373 | −0.0065 | 0.0022 |
  | usaww N = 48, T = 17 | −0.0361 | −0.0346 | −0.0043 | 0.0012 |
  | usaww N = 48, T = 50 | −0.0314 | −0.0300 | +0.0003 | 0.0007 |
  | 5-NN N = 200, T = 5 | −0.0112 | −0.0104 | −0.0023 | 0.0012 |
  | 5-NN N = 800, T = 5 (250 reps) | −0.0044 | −0.0042 | −0.0022 | 0.0011 |

  Both direct-approach lags carry the same O(1/N) bias, which does not fall with T; only the transformation approach is consistent at fixed N. Neither lag is "the correct one". The default therefore stays splm (the canonical R reference), with the exact dummy-model likelihood available as the opt-in `twoways_lag="within"` (`vce="oim"` only).
- *What splm does* (`splm:::spfeml` / `splaglm` / `conclikpan`): `lag.listw` applied to the two-way-demeaned y, i.e. W(Qy). Its `LeeYu=TRUE` option is a bias correction applied to the direct estimates, not a transformation.
- *What xsmle does.* Its default, `technique(nr) difficult` and `technique(bfgs)` fits all "converge" near ρ ≈ 0.19691. Started at our point with `iterate(0)`, it reports ll 1659.4476945, which is above its own reported maximum. Its point is a stationary point of neither objective. The Mata engine is compiled, so the gradient could not be read. `technique(bfgs)` errors for SDM.

### (c) Proposed `_FROZEN_PROMOTIONS`

```python
"mgwr": {
    "status": "bit-exact",
    "reference": "PySAL mgwr 2.2.1 Sel_BW(multi=True).search() + MGWR.fit() (authors' implementation); fixed-bandwidth back-fitting also GWmodel::gwr.multiscale 2.4.1",
    "reference_versions": {"python": "3.13.9", "mgwr": "2.2.1", "numpy": "2.2.6", "R": "R version 4.5.2 (2025-10-31)", "GWmodel": "2.4.1"},
    "tolerance": "bandwidths, initial bandwidth, bandwidth history and iteration count exact; betas 1e-9 rel (observed 3.0e-12); SEs, ENP_j, tr(S), sigma2, AICc/AIC/BIC 1e-10 rel (observed <= 1e-15); SOC path 1e-9 (observed 8e-13)",
    "sides": ["py", "Python-ref", "R"],
    "test": ["tests/reference_parity/test_r2_spatial_parity.py", "tests/reference_parity/_fixtures/r2_spatial_mgwr.json", "tests/reference_parity/test_spatial_survey_R_parity.py", "tests/reference_parity/_fixtures/spatial_survey_R.json"],
    "note": "Georgia, y = PctBach, X = (PctFB, PctBlack, PctRural) standardised (ddof 0) as in mgwr's docs; adaptive bisquare AICc, fixed Gaussian AICc, adaptive bisquare CV (200 sweeps, not converged on either side), adaptive exponential BIC with multi_bw_min 20. The search is mgwr's golden_section (delta 0.38197, integer probes, memo, 2-decimal rounding), kernel eps 1.0000001, SOC stop and 5-sweep bandwidth freeze; SEs from replaying the bandwidth history. kernel_eps = 1 reproduces GWmodel's fixed-bandwidth fixed point. GWmodel's own bandwidth search is a different algorithm and is not reproduced. Regenerate via _generate_r2_spatial_mgwr.py (mgwr on PYTHONPATH) and _generate_spatial_survey_R.R.",
},
```

- `"Python-ref"` is a new side token. The integrator should map it the same way as `blp`'s pyblp, via `_parity_taxonomy.PYTHON_REFERENCE_ROWS`.
- `spatial_panel` keeps its round-1 record, with a new note: "for two-way SAR/SDM xsmle's e(ll) is the splm objective (1e-12) but its reported maximum is below StatsPAI's (class 4); type(both, leeyu) returns the type(ind, leeyu) fit, so the time effects are dropped. twoways_lag = 'within' gives the Lee-Yu (2010) eq. 21 dummy-model profile likelihood; see test_r2_spatial_parity.py and r2_spatial_stata.json."

### (d) CHANGELOG / MIGRATION

- **⚠️ Correctness:** `sp.mgwr` now runs PySAL mgwr's MGWR (search, kernel, SOC stop, bandwidth freeze) and reports mgwr's SE / ENP_j / tr(S) / σ² / AICc / AIC / BIC. On Georgia the bandwidths change from [93, 101, 156, 158] to [101, 101, 117, 157]. `tol` is now the SOC threshold.
- **Added:** `sp.mgwr(criterion=, bw_min=, bw_max=, bws_same_times=, rss_score=, search_tol=, search_max_iter=, kernel_eps=)` and the new result fields.
- **Added:** `sp.spatial_panel(twoways_lag="splm"|"within")`. The default is unchanged.
- **MIGRATION:** `mgwr` default bandwidths and the meaning of `tol` have changed. The old search matched no reference, so it is not available. For GWmodel's kernel use `kernel_eps=1.0` with a small `tol`.

### (e) Open

- GWmodel's `gwr.multiscale` bandwidth search, which is a different algorithm.
- The Lee–Yu transformation estimator is not implemented in sp; it exists only in the MC script. It is the consistent estimator for two-way effects, but no package reproduces it. Candidate follow-up.
- xsmle `technique(bfgs)` errors for SDM two-way.

### (f) Housekeeping

- **.gitignore:** `_fixtures/_ado_r2_spatial/` is already covered by `_ado_*/`.
- **Installs:** PySAL mgwr 2.2.1 into a scratch `--target` directory, not the venv. It is needed only on PYTHONPATH when regenerating.
- **Created:**
  - `test_r2_spatial_parity.py`
  - `_generate_r2_spatial_mgwr.py`
  - `_r2_spatial_twoways_mc.py`
  - `_fixtures/_generate_r2_spatial_stata.do`
  - `_fixtures/r2_spatial_{georgia.csv, mgwr.json, stata.json}`
- **Modified:**
  - `src/statspai/spatial/gwr/mgwr.py` (rewritten).
  - `src/statspai/spatial/panel/estimator.py` (`twoways_lag`).
  - `tests/spatial/test_gwr.py`: dropped the assertion "MGWR RSS ≤ 1.05 × GWR RSS", which is not a property of MGWR (PySAL mgwr itself gives 2271.0 vs GWR's 2107.0 there).
  - Round-1 `test_spatial_survey_R_parity.py`: the fixed-bandwidth pin now passes `kernel_eps=1.0, tol=1e-15` and holds at 1.6e-10. **Flagged: round-1 file.**
- **Tests:**
  - 18 new tests;
  - 176 in `test_spatial_survey_R_parity.py` plus `tests/spatial/`;
  - 40 in `test_tierD_*spatial*`;
  - doctests.


## Treatment effects: ICE point estimate, TMLE ATT, policy value

Sub-agent tag `r2_teffects`.

Inputs and versions:
- Data: the round-1 files `teffects_{cs,wide,long}.csv`. The long file is reshaped to four-period wide form inside both the generator and the test.
- Generator: `tests/reference_parity/_generate_r2_teffects_R.R`, which writes `_fixtures/r2_teffects_R.json`. Re-running it reproduces the fixture byte for byte.
- Test: `tests/reference_parity/test_r2_teffects_parity.py`.
- R 4.5.2 with ltmle 1.3.0, SuperLearner 2.0.40, tmle 2.1.1, grf 2.6.1 and policytree 1.2.4.

### (a) Per-function results

| function | reference | class | max rel err est / SE | test |
| --- | --- | --- | --- | --- |
| `gformula_ice_fn` (point estimate) | `ltmle::ltmle(gcomp=TRUE, SL.library=list(Q="SL.lm"))` 1.3.0, pooled; 2 periods (3 regimes × Y and Yb) and 4 periods (3 regimes) | 1 (T2). The SE stays pinned by round 1's `geex`, because ltmle reports no gcomp variance | 2.1e-11 vs ltmle; 2.4e-15 vs a hand-coded `lm()` ICE / – | `test_ice_point_matches_ltmle_gcomp`, `test_ice_observed_past_equals_regime_past_identity` |
| `gformula_ice_fn`, binary Yb, always-treat | same | 3 (convention) | 2.7e-4. `SL.lm` clips predictions to [0,1] and sp's linear ICE does not. The test asserts that the two differ | same |
| `tmle(estimand='ATT')` | `tmle::tmle` 2.1.1 (`oneStepATT`) | 3. A different but equally valid TMLE; the mechanism is reproduced exactly | sp vs R 1.4e-3 (`single`), 3.7e-3 (`per_arm`). A Python port of `oneStepATT`, run on R's exported inputs, matches R to 3.3e-16 | `test_tmle_att_*` |
| `policy_value` | `grf::average_treatment_effect(subset = pi == 1)` × mean(pi) on grf's `get_scores`; reward contrast from `policytree::double_robust_scores` | 2 → 1 (identity: the scores are an input) | 6.7e-16 / – (the function returns no SE) | `test_policy_value_*` |

**ICE.** ltmle sets every earlier treatment node to the regime value; sp keeps the observed values. Under OLS on nested histories the two give the same estimate, which the four-period regimes (1111, 0000, 1010) confirm, and a reference-free test asserts the identity. The 2.1e-11 residual is inside ltmle: R's own hand-coded `lm()` ICE differs from ltmle by the same amount.

**TMLE ATT.** Round 1 described sp's estimator as "an ATE-style fluctuation followed by a DR-ATT estimating equation". That was wrong. sp fluctuates along the ATT clever covariate `A − (1−A)g/(1−g)`. With R's initial Q and g as inputs, and for both fluctuations and both outcomes:
- sp's estimate equals the substitution estimator Σ A(Q1* − Q0*)/n1;
- the ATT efficient-influence-function equation has mean zero, to within 1e-10 of the SD of the EIF.

So sp's ATT is a genuine TMLE. R's version differs in four ways, and the Python port reproduces all four exactly:
- It takes small steps (0.001) that update both Q and g, and stops when the loss stops decreasing.
- It keeps only rows with g ≥ min(g | A = 1) (989 of 1000).
- It recalibrates g on those rows.
- Its plug-in weights Q1 − Q0 by g.

Because R stops on the loss, it solves its own EIF equation only approximately: the mean IC is −2.6e-4 against an SE of 0.0876.

With identical nuisances, all variants agree to within 0.1 SE. Continuous Y:

| variant | ATT |
| --- | --- |
| sp `single` | 1.58551 |
| sp `per_arm` | 1.58179 |
| R's path, all rows | 1.58674 |
| R as shipped | 1.58767 |

A T3 simulation checked bias and coverage. Its scripts are in the session scratchpad and are not committed. Setup: 400 replications, n = 1000, round 1's DGP, Q misspecified and g correct. True ATT is 1.66636, from 4e7 draws.

| estimator | bias | coverage |
| --- | --- | --- |
| R | −0.0047 | 0.915 |
| sp `single` | −0.0061 | 0.920 |
| sp `per_arm` | −0.0059 | 0.922 |

The Monte Carlo SE of the bias is 0.0041. All three estimators have an SD of about 0.081 and a mean SE of about 0.0765, so all three under-cover by the same amount.

### (b) Defects

1. **`policy_value`: silent misuse** (`src/statspai/policy_learning/policy_tree.py`).
   - What was wrong: `scores` passed as an (n,1) column against an (n,) policy broadcast to an n×n outer product, and the function silently returned mean(scores)·mean(policy).
   - Fix: raise `ValueError` unless both inputs are 1-D and the same length. A scalar policy is still accepted.
   - The docstring now states what is returned: the gain over treating no one, E[Y(pi)] − E[Y(0)], with no SE.
   - Default output for valid inputs is unchanged. Regression test: `test_policy_value_rejects_column_vector_scores`.

No defect was found in `gformula_ice_fn` or in the TMLE ATT.

### (c) Proposed `_FROZEN_PROMOTIONS`

```python
"gformula_ice_fn": {
    "status": "bit-exact",
    "reference": "ltmle::ltmle 1.3.0 (gcomp = TRUE, SL.library = list(Q = 'SL.lm')) point estimate; base-R lm() ICE with geex::m_estimate 1.1.1 sandwich SE",
    "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "ltmle": "1.3.0", "SuperLearner": "2.0.40", "geex": "1.1.1"},
    "tolerance": "point 1e-10 rel vs ltmle (observed 2.1e-11), 1e-12 vs hand lm (observed 2.4e-15); sandwich SE 1e-9 rel (observed 7.1e-12)",
    "sides": ["py", "R"],
    "test": [
        "tests/reference_parity/test_r2_teffects_parity.py",
        "tests/reference_parity/_fixtures/r2_teffects_R.json",
        "tests/reference_parity/test_teffects_R_parity.py",
        "tests/reference_parity/_fixtures/teffects_R.json",
    ],
    "note": "Pooled sequential regression, 2- and 4-period regimes; ltmle sets past A to the regime, sp keeps them observed (identical under OLS on nested histories). SL.lm clips to [0, 1]: the binary-Yb always-treat block, where the clip binds, is a documented convention gap.",
},
"policy_value": {
    "status": "bit-exact",
    "reference": "grf::average_treatment_effect(subset = policy == 1) x mean(policy) on grf get_scores; policytree::double_robust_scores reward contrast",
    "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "grf": "2.6.1", "policytree": "1.2.4"},
    "tolerance": "1e-12 rel (observed 6.7e-16)",
    "sides": ["py", "R"],
    "test": [
        "tests/reference_parity/test_r2_teffects_parity.py",
        "tests/reference_parity/_fixtures/r2_teffects_R.json",
    ],
    "note": "Value gain over treat-none, mean(Gamma * pi), on grf's own AIPW scores (causal_forest seed 7); the scores are an input, so forest randomness does not enter. No SE.",
},
```

There is no promotion for the TMLE ATT, because it is class 3.

### (d) CHANGELOG / MIGRATION

- **Fixed:** `sp.policy_value` raises `ValueError` when `scores` / `policy` are not 1-D or have different lengths. An (n,1) score column used to return mean(scores)·mean(policy) silently.
- **MIGRATION row:** `policy_value` | (n,1) scores | wrong number → `ValueError` | pass `scores.ravel()`.

### (e) Still open, and what was checked

- **Reproducing R's ATT in sp.** This would need a `one_step` fluctuation, common-support trimming and g recalibration. It was not added, because `tmle/tmle.py` is on the uncommitted release line; that line's owner can add it.
- **ICE: other packages checked.**
  - `lmtp` 1.5.4: `lmtp_sub()` is `deprecate_stop` since 1.5.0, and its predictions are bounded.
  - `gfoRmula` 1.1.1: Monte Carlo only.
  - `gfoRmulaICE` 1.1.1: binomial / quasibinomial models only.
  - ltmle's default glm path: a quasibinomial model on the rescaled Y, which is a different model.
- **Policy value: other packages checked.**
  - `policytree` 1.2.4 has no value function.
  - `evalITR` 1.1.0 computes Horvitz–Thompson PAV / PAPE, a value level rather than a DR gain.
  - `DynTxRegime` and `DTRreg` were not checked.

### (f) Housekeeping

- **Installed, used only to read source:** R packages lmtp 1.5.4 and evalITR 1.1.0.
- **Created:**
  - `tests/reference_parity/_generate_r2_teffects_R.R`
  - `tests/reference_parity/_fixtures/r2_teffects_R.json`
  - `tests/reference_parity/test_r2_teffects_parity.py`
- **Modified:** `src/statspai/policy_learning/policy_tree.py` (`policy_value` only).
- **Tests run (all pass):**
  - `test_r2_teffects_parity.py` (23 tests)
  - the related suites (111 tests): `test_teffects_R_parity`, `test_policy_value_parity`, `test_policy_tree_parity`, `test_gformula_ice`, `test_policy_learning`, `test_policy_targeting`, `test_policy_tree_exact_search`, `test_policy_weights_contract`, `test_tmle`, `test_tmle_shared_nuisance`
  - the `policy_tree.py` doctests (4)


## Postestimation: `margins_at` / `contrast` / `pwcompare` (plus `margins(at=, method="mem")`) vs Stata 18

Sub-agent tag `r2_postest`. `src/statspai/postestimation/` belongs to another line, so it was **not edited**. Each defect is pinned by an `xfail(strict=True)` test that asserts Stata's number.

The fixes were checked on a scratch copy of `src`:
- With them applied, the D1, D2, D3 and D5 xfails pass.
- The 84 existing postestimation tests still pass.
- D4 was not patched in the scratch copy; its fix is a single raise.

### (a) Per-function table

| function | reference | class | max rel err, est / SE | test |
|---|---|---|---|---|
| `sp.margins_at` (single and multiple at-variables, at() on a factor, g##c.x, g##i.h; OLS / HC1 / CR1) | Stata 18 `margins, at(...)` | est and SE: 1 (bit-exact). p and CI: **defects D1 and D5, open** | 3.3e-15 / 3.5e-15 | `tests/reference_parity/test_r2_postest_parity.py` |
| `sp.contrast` r / rb# (`reference=`) / ar / gw | Stata 18 `margins r.g` / `rb3.g` / `ar.g` / `gw.g` | est and SE: 1. p and CI: **D1**. Against the `contrast` *command*: 3 (asbalanced, and an interacting c.x is held at 0; both mechanisms are asserted as identities) | 7.9e-15 / 4.9e-15 | same |
| `sp.pwcompare` none / bonferroni / sidak / holm | Stata 18 `margins g, pwcompare(effects) mcompare(...)`; R emmeans 2.0.3 `pairs(adjust=)` | est and SE: 1. Adjusted p and CI: **D1, D2**. For holm, emmeans uses Bonferroni intervals, and sp does the same | 7.9e-15 / 4.9e-15 (emmeans 1e-10) | same |
| `sp.margins(variables=, at=)`, dydx at given values | Stata `margins, dydx(x) at(z=..)` and `at(g=..)` after regress / regress g##c.x / logit / probit / poisson | 1 | linear 3e-15; probit 1.1e-11 / 3.8e-12; poisson 4.2e-9 / 4.8e-10; logit at Stata defaults 2.4e-7 / 5.2e-8, which is Stata's optimiser gap (against Stata at tol 1e-14: 1.4e-12 / 3.0e-13) | same |
| `sp.margins(method="mem")` | Stata `margins, dydx() atmeans` | 1 without a factor (≤ 9.4e-9 / 1.8e-9). **Defect D3** with a factor in the model | — | same |
| `sp.test` as the joint contrast | Joint row of `contrast r.g`: F with df_r (G−1 under cluster), chi2 after logit / probit | 1 | F 3.3e-15, p 7.8e-14; probit 1.6e-11; logit 5.2e-7 (optimiser) | same |
| `margins_at` SE against R | `marginaleffects::avg_predictions` 0.32.0 | 1. The reference SE uses a numerical Jacobian (Richardson), good to 1.8e-10 | 1e-15 / 1.8e-10 | same |

ML tolerance: Stata's default `logit` stops 1.1e-6 (relative) from the optimum on the coefficients themselves. Refitted with nrtolerance / tolerance / ltolerance 1e-14, it matches sp to 4.6e-12. `test_logit_gap_is_the_optimiser` asserts this.

### (b) Defects

All five are in `src/statspai/postestimation/margins.py`, which another line owns. None was fixed here.

- **D1: wrong reference distribution.**
  - What: `margins_at` / `contrast` / `pwcompare` hard-code `stats.norm` for their critical values and p-values. Stata uses t(e(df_r)): 594 on this fixture, or G−1 = 39 under clustering. `sp.margins`, in the same file, already calls `inference_df(result)`.
  - First divergence: the critical value. The estimates and SEs are identical.
  - Before → after: the cluster `pwcompare(sidak)` "2 vs 1" p-value goes from 7.5e-14 to 1.39e-8. Before the fix, the cluster `margins_at` CI bound was off by 9.6e-3 (relative) and the OLS contrast CI by 9.7e-4.
  - Fix: `df = inference_df(result)`, then `stats.t(df)` when df is finite and the normal otherwise.
  - Convention note: `marginaleffects` defaults to N(0,1) even after `lm()` (asserted in the test). With `df = df.residual` its CI equals Stata's.
- **D2: Sidak underflow.**
  - What: `1-(1-p)**m` returns exactly 0 for p below about 1e-17.
  - Before → after: "4 vs 3" goes from 0 to 7.04e-26, Stata's value. emmeans uses the same formula and also returns 0.
  - Fix: `-np.expm1(m*np.log1p(-p))`.
- **D3: `method="mem"` with a factor in the model.**
  - What: `frame.mean(numeric_only=True)` averages the raw `g` codes (2.19), so every `C(g)[T.k]` dummy evaluates to 0, which is the base level. Stata `atmeans` sets each dummy to its share (.323 / .303 / .235 / .138).
  - Before → after: logit dydx(x) at(z=1) atmeans goes from 0.1409 to 0.1480, and probit from 0.1170 to 0.1322. The old values were off by 1.0% and 2.1%.
  - Fix: average each design part and build each term from those means. The same change applies in `_design_derivative`.
- **D4: an at-variable that is not in the model is silently ignored.**
  - What: `margins_at` and `margins(at=)` return identical rows for every at-value. Stata raises r(322).
  - Fix: raise `MethodIncompatibility`.
- **D5: margins average over all of `data=`, not the estimation sample.**
  - What: with 25 missing outcomes the margin is off by 3.4e-3 (relative) and the gw contrast by 5.0e-3. Restricting to the estimation sample brings both to 1e-15. A missing covariate gives a NaN margin.
  - Fix: store the estimation-sample mask at fit time, or drop incomplete rows.

Every fix except D4 changes default output. D4 turns calls that used to succeed into errors.

### (c) Proposed `_FROZEN_PROMOTIONS`

**Add these only after D1–D5 land and the xfails are removed.** Promoting them before that would certify p-values and intervals that are wrong.

```python
"margins_at": {
    "status": "bit-exact",
    "reference": "Stata 18 margins, at(...); R marginaleffects::avg_predictions",
    "reference_versions": {"Stata": "18", "R": "R version 4.5.2 (2025-10-31)", "marginaleffects": "0.32.0"},
    "tolerance": "1e-10 rel (observed <= 3.5e-15 est / SE; marginaleffects SE 1.8e-10, numerical Jacobian)",
    "sides": ["py", "R", "Stata"],
    "test": ["tests/reference_parity/test_r2_postest_parity.py",
             "tests/reference_parity/_fixtures/r2_postest_stata.json",
             "tests/reference_parity/_fixtures/r2_postest_R.json"],
    "note": "Single and multiple at-variables, at() on a factor, g##c.x and g##i.h, OLS / vce(robust) / vce(cluster). Predictive margins average over the observed covariates (asobserved).",
},
"contrast": {
    "status": "bit-exact",
    "reference": "Stata 18 margins r.g / rb3.g / ar.g / gw.g",
    "reference_versions": {"Stata": "18"},
    "tolerance": "1e-10 rel (observed <= 7.9e-15 est / 4.9e-15 SE)",
    "sides": ["py", "Stata"],
    "test": ["tests/reference_parity/test_r2_postest_parity.py",
             "tests/reference_parity/_fixtures/r2_postest_stata.json"],
    "note": "Contrasts of predictive margins (asobserved). Stata's contrast command is asbalanced and holds interacting continuous covariates at 0; both mechanisms asserted as identities.",
},
"pwcompare": {
    "status": "bit-exact",
    "reference": "Stata 18 margins g, pwcompare(effects) mcompare(noadjust|bonferroni|sidak); R emmeans pairs(adjust=)",
    "reference_versions": {"Stata": "18", "R": "R version 4.5.2 (2025-10-31)", "emmeans": "2.0.3"},
    "tolerance": "1e-10 rel (observed <= 7.9e-15 diff / 4.9e-15 SE)",
    "sides": ["py", "R", "Stata"],
    "test": ["tests/reference_parity/test_r2_postest_parity.py",
             "tests/reference_parity/_fixtures/r2_postest_stata.json",
             "tests/reference_parity/_fixtures/r2_postest_R.json"],
    "note": "Six pairwise comparisons, OLS / robust / cluster, additive, g##c.x and g##i.h. Holm intervals follow the emmeans convention (Bonferroni).",
},
```

After D3 is fixed, the existing `"margins"` record can add this note: "dydx() at() after regress / logit / probit / poisson and atmeans also held in test_r2_postest_parity.py".

### (d) CHANGELOG / MIGRATION

For the owning line, once its fixes land.

⚠️ Correctness:
- `sp.margins_at` / `sp.contrast` / `sp.pwcompare`: p-values and intervals use t(df_r), or G−1 under clustering, instead of N(0,1).
- `pwcompare(adjust="sidak")`: no longer underflows to 0 for very small p.
- `sp.margins(method="mem")`: factor dummies are held at their sample shares, as Stata's `atmeans` does.
- The margins family averages over the estimation sample.
- An `at=` variable that is not in the model raises.

MIGRATION: D1, D3 and D5 change default output. To reproduce the old D5 numbers, pass the rows explicitly. D4 now raises.

### (e) Open items and what was checked

Refused loudly by sp (asserted in the test):
- `margins_at` / `contrast` / `pwcompare` after logit or probit. Stata's pr-scale and xb-scale values are already in the fixture, ready for when support lands.
- `sp.poisson` with `C()` in the formula.

Features sp does not have, so there is nothing to compare:
- `atmeans` in `margins_at`.
- The `a.` / `g.` operators and the joint test in `contrast`. The joint test is covered through `sp.test`.
- `scheffe` / `tukey` / `cimargins` in `pwcompare`.

### (f) Housekeeping

- No `.gitignore` entries needed: only built-in Stata commands are used.
- No R packages were installed: emmeans 2.0.3 and marginaleffects 0.32.0 were already present.
- New, untracked files:
  - `tests/reference_parity/test_r2_postest_parity.py`
  - `tests/reference_parity/_generate_r2_postest_R.R`
  - `tests/reference_parity/_fixtures/_generate_r2_postest_data.py`
  - `tests/reference_parity/_fixtures/_generate_r2_postest_stata.do`
  - `tests/reference_parity/_fixtures/r2_postest_data.csv`
  - `tests/reference_parity/_fixtures/r2_postest_stata.json`
  - `tests/reference_parity/_fixtures/r2_postest_R.json`
- Tests: 106 passed and 20 xfailed across the new file and the existing `test_postestimation_stata_parity.py`, `test_margins_at_parity.py`, `test_contrast_pwcompare_parity.py` and `test_postestimation_parity.py`. Run with `--runxfail`, every xfail fails for its diagnosed reason.


## R. rd_iv leftovers: OPEN (sub-agent stopped by the API limit)

The rd_iv sub-agent stopped before it reported. What it left in the worktree:
- **Edits:** `src/statspai/regression/iv_quantile.py` has +234/−28 lines, uncommitted. It appears to add a Chernozhukov–Hansen weighting for over-identified models. **These edits are unverified, and they break an existing test.** I ran the ivqreg-related tests against them:
  - 10 pass: `test_ivqreg_parity.py`, the ivqreg tests in `test_rd_iv_R_parity.py`, `test_iv_cov_tail.py` and `test_cov95_iv_init.py`.
  - 1 fails: `tests/test_econ_trinity.py::TestAdversarial::test_ivqreg_multidim_warns_when_bootstrap_zero`. The expected `UserWarning` ("bootstrap=0") is no longer emitted.
- **Untracked generators and fixtures:**
  - `tests/reference_parity/_generate_r2_rdiv_R.R`
  - `_fixtures/_generate_r2_rdiv_stata.do`
  - `_fixtures/r2_rdiv_{R,Stata}.json`
  - `_fixtures/r2_rdiv_ivqr_{oid,roots}.csv`
- **Not written:** no test file (`test_r2_rdiv_parity.py`) exists.

**Integrator: do not merge `iv_quantile.py` until it has been reviewed and tested.** The alternative is to discard just that file's unstaged diff (restore it to the index version).

Items still open, with their round-1 diagnosis unchanged (see `rd_iv.md` §5):
1. **`ivqreg`, over-identified.** It uses identity weighting where CH uses the inverse covariance. R `IVQR` breaks on R 4.5.
2. **Stata `weakiv` residual.** CLR/K differ by 1.1e-7, AR by 2.1e-8, and the CLR p-value under `small` differs by 1.4e-3.
3. **`effective_f_test`.** `stock_yogo_10pct` is really the MOP k = 1 critical value, and it is used for every k. This lives in `diagnostics/weak_iv.py`, which is on the release line.
4. **`rdsensitivity` / `rdrbounds`.** Still T3.
5. **Class-6 re-search not done.** `rd_multi_score`, `zero_first_stage` and `lasso_iv` were not searched again.
