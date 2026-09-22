# Phase 3, round 2: `synth_rest` family

Worktree `r2-synth-rest`. Nothing is committed and the round-1 baseline stays staged.

**Reference fixture.** `tests/reference_parity/_fixtures/synth_rest_R.json` is written by
`tests/reference_parity/_generate_synth_rest_R.R` (R 4.5.2). Its inputs come from
`tests/reference_parity/_generate_synth_rest_data.py`, which uses fixed seeds and writes
`_fixtures/synth_rest_{scm,donor_subsets,multi,stag,ss_panel,ss_panel_unbal,ss_shares,ss_shocks}.csv`.

**Test.** `tests/reference_parity/test_synth_rest_R_parity.py`: 24 tests, all green.

**Package versions** (from the fixture `meta`):

| package | version |
| --- | --- |
| Synth | 1.1.10 |
| SCtools | 0.3.3.1 |
| kernlab | 0.9.33 |
| quadprog | 1.5.8 |
| scinference | 0.0.0.9000 @ 567c6889ce0a1d269a62d415b88aa6baf723a3fe |
| limSolve | 2.0.3 |
| augsynth | 0.2.0 |
| osqp | 1.0.0 |
| synthdid | 0.0.9 |
| AER | 1.2.16 |
| sandwich | 3.1.1 |
| ShiftShareSE | 1.1.0 |
| bartik.weight | 0.1.0 |
| fixest | 0.14.0 |

## 1. Per-function table

Outcome classes: 1 aligned · 2 defect fixed then aligned · 3 convention · 4 reference wrong ·
5 stochastic · 6 no canonical reference / different estimand.

| function | reference | class | max rel err est / SE | test |
| --- | --- | --- | --- | --- |
| `synth_loo` | `Synth::synth` 1.1.10 per fit (`custom.v = var/range²` → identical QP; exact quadprog solve; Synth's ipop agrees ≤ 1e-5) | 2 (D1, D2) | ATT / pre-RMSPE ≤ 3e-14; SE/p: none (descriptive i.i.d.) | `test_synth_rest_R_parity.py` |
| `synth_time_placebo` | same | 2 (D1, D2) | ATT ≤ 1e-13 on the 5 identified placebo times (7 with T0 < J have non-unique weights, not compared) | same |
| `synth_donor_sensitivity` | same; the numpy subset draws are replayed and the replay is asserted | 2 (D1) | ATT / pre-RMSPE ≤ 1e-13 | same |
| `synth_rmspe_filter` | `SCtools::mspe.test` 0.3.3.1 (with `discard.extreme`, `mspe.limit` 2/5/20) | 2 (D1) + 3 (D3, options added) | placebo pre-RMSPE and ratios ≤ 1e-13; p-values and n-kept exact, both pool conventions | same |
| `synth_sensitivity` | composition of the four above | 2 | via parts | same |
| `conformal_synth` | `scinference` (authors' package; `sc`, moving block) | 2 (D4, rewritten) + 4 (D5, lsei) | joint p-values exact on all 45 grid points against the quadprog replica, and exact against scinference on the 43 where lsei succeeds; pointwise p0 exact; pointwise CIs exact against the replica (and against scinference for the period with no lsei failure); ATT 9e-16 | same |
| `multi_outcome_synth` | `augsynth::augsynth_multiout` 0.2.0 (`progfunc="None"`, concat / avg), OSQP eps 1e-12 | 1 (weights / ATT); 6 for placebo SE, p and Fisher joint p (augsynth has only conformal for multi-outcome) | weights 1.4e-15 / 9e-15 abs; per-outcome ATT ≤ 1e-13 | same |
| `sequential_sdid` | `synthdid::synthdid_estimate` 0.0.9 per cohort block | 1 per block; 6 as "Arkhangelsky–Samkov" (D6, mislabelled, no code exists) | ATT(g) ≤ 1e-8 (asserted), aggregate reproduced | same |
| `synth_survival` | none: Han & Shah (arXiv:2511.14133) is a different estimator (survival scale, PCR weights) and publishes no code | 6; defects D7 fixed | identity: exact-copy DGP → weight e_j, pre-gap < 1e-9; band = [gap − q_hi, gap − q_lo] | same |
| `synth_power`, `synth_mde` | none (no package does SCM power) | 6; defects D8 fixed | identities: power = 0 when α < 1/(J+1); power 1 at a large effect | same |
| `qqsynth` | alias of `discos(method="quantile")` (round-1 T2 against DiSCos) | 1 by alias | — | round-1 `test_did_synth_synthvar_parity.py` |
| `stochastic_dominance` | none found (DiSCos has no dominance test) | 6 | — | — |
| `synth_experimental_design` | Abadie–Zhao SCDesign (github jinglongzhao2/SCDesign @ 8e1e9f5, R + Gurobi MIQP) solves a different design problem | 6; mislabelled (D9) | identity: ranking = direct LOO fits, 1e-10 | same |
| `shift_share_political` | `AER::ivreg` + `sandwich` HC1; `ShiftShareSE::ivreg_ss` (EHW / AKM / AKM0); `bartik.weight::bw`; `anova(lm)` | 2 (D10) | β 2e-16; HC1 SE 2e-15; AKM SE 1.5e-15; AKM p 2.7e-8 (reference cancellation); AKM0 p 6e-15; α_k 2e-16 abs; β_k 5e-15; balance F 1e-15 | same |
| `shift_share_political_panel` | `fixest::feols` (ssc adj = FALSE, cluster.adj = FALSE); `ivreg_ss` with FE dummies; `bw` with FE dummies; `AER`+HC0 per period; FE partial F from feols RSS | 2 (D11) | β ≤ 2e-15; unit / time / two-way CR0 SE ≤ 1.1e-14 (incl. unbalanced panel); AKM SE 1.2e-15; AKM0 CI 3e-15; Rotemberg 4e-15 abs; per-period 3e-15; first-stage F 5e-15 | same |

**Stata.** Stata `synth` (SSC, Hainmueller 0.0.8) and `synth_runner` 1.6.0 (GitHub bquistorff)
are installed in the private ado dir, and their source was read.

- `synth_runner` does the following:
  - excludes the treated unit from placebo pools;
  - filters with `pre_limit_mult()` on the RMSPE scale;
  - reports `p = #{|placebo| >= |treated|} / n`, with no +1.
- `synth.ado` rounds `e(W_weights)` / the weights to 3 decimals (`roundmat`). A probe gave
  0.285 / 0.715. The gaps therefore carry up to ~1e-3 weight error, and no Stata side can reach
  T2. Not run as a reference: open (see §5).

## 2. Defects

### D1. Shared simplex solver stopped at SLSQP tolerance

**What.** `_core.solve_simplex_weights` is used by all these tools, `sp.synth` equal-V fits,
`conformal`, `multi_outcome` and `experimental_design`. It returned weights ~1e-7 off the
optimum, which put gaps ~1e-6 off. That is the first divergence against Synth / quadprog.

**Fix.** When the problem is strictly convex (full column rank, or ridge > 0), the function now
uses the exact primal active-set solver round 1 wrote for DiSCos. That solver moved from
`discos.py` to `_core._eq_bounded_lsq`; `discos` now imports it. Rank-deficient problems keep
SLSQP, so the chosen minimiser does not move where it is not unique.

**Numbers.** Treated fit, before → after: weights 9e-8 → 2e-14 abs, ATT 3e-8 → 5e-15 rel.
⚠️ Default output moves by about 1e-7. Example: the pinned pre-RMSPE in
`test_synth_helpers_untested.py` went 0.17714 → 0.1771399093.

### D2. Degenerate naive p-values in `synth_loo` / `synth_time_placebo`

**What.** With one placebo post-period, `np.std` = 0 gave `se = 0`, then `z = inf`, then
`p = 0`. The last time placebo was therefore always "significant" (on the fixture:
att −0.041, p 0.0).

**Fix.**
- SE and p are NaN when T1 < 2 or SE ≤ 0.
- The docstrings now say these are descriptive i.i.d.-gap quantities, and that `alpha` is unused.
- The summary line is relabelled.
- Silently dropped fits now raise a `RuntimeWarning`.

### D3. `synth_rmspe_filter` conventions (convention class 3)

The function cut on the pre-RMSPE scale and kept the treated unit in the placebo donor pools.
ADH 2010 and SCtools cut on MSPE (20 / 5 / 2 × California), and SCtools and `synth_runner` drop
the treated unit from placebo pools. New keyword-only options: `metric={"rmspe","mspe"}` and
`placebo_pool={"include_treated","exclude_treated"}`. Defaults are unchanged. The placebo table
and the treated ratio are exposed in `df.attrs`. Both conventions are tested against SCtools.

### D4. `conformal_synth` computed a different procedure than CWZ / scinference

**What was wrong.**
- The weights were fit on the pre-period only and never re-estimated under the null.
- Pointwise p used `(1+#)/(T0+1)` on pre-fit residuals.
- The joint test used |mean| of the residuals, not the sum of |u|.

**Fix.** Rewritten to scinference's procedure:
- the SC is refit on all T0 + T1 periods with the post outcomes shifted by θ0;
- moving-block statistic `S_s = Σ|u|` over length-T1 cyclic blocks, `p = mean(S >= S_{T0+1})`;
- pointwise p uses T0 + one post-period, `p = mean(|u| >= |u_post|)`;
- CIs by grid inversion.

**New behaviour.**
- When α is below the smallest attainable p (1/(T0+1) pointwise, 1/(T0+T1) joint), the set is
  (−inf, inf).
- Grid truncation warns and sets `model_info['ci_truncated']`.
- The joint p-value grid is exposed.
- The default grid is widened to ±max(5·sd(pre-residuals), 3·max|post gap|).
- `se` is documented as a CI-implied scale.
- `pre_treatment_rmse` is no longer rounded to 6 decimals.

⚠️ Default p / CI / se changed. On the `test_cov95_synth_variants` panel: p 0.0556 → 0.444, and
the CI is now (−inf, inf) at α 0.05 because T = 18 < 20. The estimate is unchanged.

### D5. Reference defect, scinference (T4)

`sc()` calls `limSolve::lsei(type=1)` and never checks `IsError`. At θ0 ∈ {8.75, 9} lsei fails
and returns infeasible weights: negative weights, SSR 310.4 against 86.6 at the true simplex
optimum. scinference then reports joint p 0.55 / 0.65, where the true value is 0.2 / 0.2.

**Evidence.** The generator records every lsei `IsError`. It also re-runs scinference's
movingblock / confidence_interval code with quadprog as the solver. StatsPAI equals that replica
on every grid point, and equals scinference exactly wherever lsei succeeded. This should be
reported upstream.

### D6. `sequential_sdid` is not Arkhangelsky–Samkov

Arkhangelsky–Samkov's Algorithm 1 (arXiv:2404.00164; checked on the arXiv HTML v2):
- aggregates by cohort;
- loops over horizons;
- imputes τ̂ back into the treated outcome;
- uses an η²Σω²/π penalty and a Bayesian bootstrap.

The code instead runs cohort-by-cohort `sp.sdid` on truncated sub-panels. Its numbers are correct
for that estimator (they equal `synthdid` per cohort). Module, function, summary and `model_info`
are relabelled ("cohort_by_cohort_sdid").

Also:
- The `cohort_weights="size"` docstring was wrong: it weights by units, not units × post-periods.
- Dropped cohorts now warn.

No public code of the actual estimator was found (web search; the paper mentions none).

### D7. `synth_survival`

- **Inexact solver.** The exponentiated-gradient loop stopped short: weights off by 0.03 and
  SSR 7% too large on a 12-period, 8-donor example. It now uses the exact solver.
- **Wrong sign of the band.** It was `gap + q`; it is now `gap − q_hi, gap − q_lo` (inverting
  gap − effect ~ placebo distribution).
- **Wrong band type.** The band was documented as "uniform" but is pointwise.
- **Wrong attribution.** The module claimed to be Han–Shah SSC, a different estimator (survival
  scale, unconstrained PCR weights; arXiv HTML read). It is relabelled and the citation key
  changed to `abadie2010synthetic`.
- **Swallowed errors.** The bare `except Exception: continue` is removed.

⚠️ Default output changed: weights / counterfactual, and the band.

### D8. `synth_power` / `synth_mde`

- **Wrong rejection rule.** It rejected when `ratio >=` the interpolated (1−α) quantile of the
  placebo ratios. That is not the rank test `sp.synth` reports, and it is anti-conservative. Now
  it rejects when `placebo_rank_pvalue <= α`.
- **Null baseline kept the real effect.** The observed post gaps (with the true effect) were used
  as the null baseline, so power at δ = 0 was 1.0 on Prop. 99. Now the post gaps are centred
  before injecting δ.
- **Swallowed errors.** The bare `except` now warns.

⚠️ Default output changed. On Prop. 99 (n_sim 50), power at δ = 0 went 1.0 → 0.0 and the MDE
0 → 10.9.

With J = 8 placebos and α = 0.05 no effect is detectable (1/9 > α), so `synth_mde` now returns
inf there. Two cov95 tests that pinned the old numbers are updated with that rationale.

### D9. `synth_experimental_design` misattributed

The function claimed to implement Abadie–Zhao (arXiv:2108.02196 v5; title / authors checked via
the arXiv API and the abstract page). It also cited a variance formula `Var ≈ Σσ²_i` that does
not appear in that paper. The paper's design is a joint w / v MIQP targeting population
predictor means; the authors' code uses Gurobi. The implemented LOO-fit ranking is kept and
relabelled: `method="loo_sc_fit_ranking"` (was `"abadie_zhao_2025"`). `expected_variance` is
documented as a heuristic sum of pre-MSPEs.

### D10. `shift_share_political`

- **Mislabelled SE.** The summary said "SE (AKM shock-cluster)" but reported HC1. HC1 is kept as
  `se` (it equals AER+HC1). AKM, AKM0 CI / p and EHW are added to `diagnostics` through the
  round-1 `_akm` kernel, and equal `ivreg_ss`.
- **Wrong Rotemberg weights.** They were normalised by Σ|·|, so they did not sum to one, and had
  no `beta_k`. They are now `sp.bartik`'s GPSS weights, which equal `bartik.weight::bw`. Before
  vs after, max |α_k|: 0.447 vs 0.702.
- **Wrong share-balance df.** df1 was K. With shares summing to one it is rank([1, S]) − 1.
  Before → after: F 0.924 → 1.143, p 0.490 → 0.357. This equals `anova(lm)`.
- **Unverified attribution.** "Park & Xu" and the attributions to a "§4.2" were unverified. The
  paper is single-authored: Park 2026, arXiv:2603.00135, checked via the arXiv API and the
  abstract page, and it matches `paper.bib::park2026shift`. Attributions removed from the module,
  the guide and the test docstrings.

### D11. `shift_share_political_panel`

- **Two-way FE on unbalanced panels.** The within transformation was one pass of unit-then-time
  demeaning, which is inexact on unbalanced panels. It now uses alternating projections to
  convergence and equals fixest on the 7-row-deleted panel at 1e-14.
- **`cluster="twoway"` was really HC0** (clusters were unit × time cells). It is now CGM
  unit + time − cell, and equals fixest `~unit+time`.
- **Wrong AKM formula** (round-1 finding; `u_k = Σ s Z̃ ε`, no hX). It now uses `_akm_fit` with
  W in industry × period blocks (or industries, if the shocks are constant over time). It equals
  `ivreg_ss` with FE dummies at 1e-15. `akm0_ci` is added.
- **Wrong Rotemberg weights.** x was demeaned by period only (unit FE and covariates were
  ignored) and normalised by Σ|·|. The weights are now GPSS on the FE-residualised x and equal
  `bw` with FE dummies.
- **`first_stage_F` was not an F.** It was `var(D̂)/var(resid)`. It is now the homoskedastic
  partial F with FE df and equals the feols-RSS F. fixest's own `fitstat("ivf1")` is a different
  quantity; its value is recorded in the fixture but not compared.

⚠️ Default output changed:
- the point estimate on unbalanced panels;
- the SE with `cluster="twoway"` / `"shock"`;
- the Rotemberg weights and `first_stage_F`.

Balanced-panel β and the unit / time SEs were already right.

## 3. Proposed promotion records

```python
    "synth_loo": {
        "status": "bit-exact",
        "reference": "Synth::synth 1.1.10 (per fit, custom.v matched; QP solved exactly by quadprog::solve.QP)",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "Synth": "1.1.10", "quadprog": "1.5.8", "kernlab": "0.9.33"},
        "tolerance": "ATT and pre-RMSPE 1e-9 rel (observed <= 3e-14)",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "Each leave-one-out fit is Synth's QP with custom.v = var_k / range_k^2, which makes Synth's sd-scaled problem identical to StatsPAI's range-scaled equal-V problem; Synth's own ipop solve agrees at ipop precision (<= 1e-4). The se / pvalue columns are descriptive i.i.d.-gap quantities with no reference. Regenerate via _generate_synth_rest_R.R.",
    },
    "synth_time_placebo": {
        "status": "bit-exact",
        "reference": "Synth::synth 1.1.10 (per placebo time, custom.v matched; quadprog exact)",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "Synth": "1.1.10", "quadprog": "1.5.8"},
        "tolerance": "placebo ATT 1e-9 rel (observed <= 1e-13) on identified placebo times",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "Post-treatment rows are discarded before the placebo fits. Placebo times with fewer pre-periods than donors have non-unique weights and are not compared (7 of 12 on the fixture).",
    },
    "synth_donor_sensitivity": {
        "status": "bit-exact",
        "reference": "Synth::synth 1.1.10 on the replayed numpy donor subsets (custom.v matched; quadprog exact)",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "Synth": "1.1.10", "quadprog": "1.5.8"},
        "tolerance": "ATT and pre-RMSPE 1e-9 rel (observed <= 1e-13)",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "The subsets (k=6, n_samples=5, seed=7) are replayed in _generate_synth_rest_data.py and the test asserts the replay equals the function's draws.",
    },
    "synth_rmspe_filter": {
        "status": "bit-exact",
        "reference": "SCtools::mspe.test 0.3.3.1 (discard.extreme, mspe.limit 2/5/20) on Synth fits",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "SCtools": "0.3.3.1", "Synth": "1.1.10", "quadprog": "1.5.8"},
        "tolerance": "placebo pre-RMSPE and ratios 1e-9 rel (observed <= 1e-13); p-values and kept counts exact",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "SCtools conventions via metric='mspe', placebo_pool='exclude_treated'; the default (RMSPE scale, treated unit in placebo pools) is also held to the same fits with placebo_pool='include_treated'. mspe.test is run on a tdf object built as generate.placebos builds it.",
    },
    "conformal_synth": {
        "status": "bit-exact",
        "reference": "scinference (Chernozhukov-Wuthrich-Zhu authors' package, GitHub kwuthrich/scinference 567c688): estimation_method='sc', permutation_method='mb'",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "scinference": "0.0.0.9000 567c6889ce0a1d269a62d415b88aa6baf723a3fe", "limSolve": "2.0.3", "quadprog": "1.5.8"},
        "tolerance": "p-values exact (rank statistics); ATT 1e-9 rel (observed 9e-16); CI end points exact on the grid",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "Joint moving-block p-values on a 45-point grid, pointwise p at 0, pointwise CIs at alpha 0.1. At two extreme grid values limSolve::lsei fails (IsError) and scinference uses infeasible weights (reference defect); there StatsPAI is held to scinference's code with quadprog as the solver.",
    },
    "multi_outcome_synth": {
        "status": "bit-exact",
        "reference": "augsynth::augsynth_multiout 0.2.0 (progfunc='None', scm=TRUE, combine_method 'concat' / 'avg'); synth_qp re-run at OSQP eps 1e-12",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "augsynth": "0.2.0", "osqp": "1.0.0"},
        "tolerance": "weights 1e-10 abs (observed <= 9e-15); per-outcome ATT 1e-9 rel",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "Shared weights and per-outcome ATTs only. The placebo SE / p-values and the Fisher joint p-value are StatsPAI's own (augsynth offers only conformal inference for multiple outcomes). Stock augsynth (eps 1e-8) agrees to 1e-6.",
    },
    "shift_share_political": {
        "status": "bit-exact",
        "reference": "AER::ivreg + sandwich HC1; ShiftShareSE::ivreg_ss (EHW / AKM / AKM0); bartik.weight::bw; anova(lm) share balance",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "AER": "1.2.16", "sandwich": "3.1.1", "ShiftShareSE": "1.1.0", "bartik.weight": "0.1.0"},
        "tolerance": "estimate / SEs / Rotemberg / F 1e-9 rel (observed <= 5e-15); AKM p-value 1e-7 rel (ShiftShareSE uses 2*(1-pnorm), cancellation at p ~ 1e-9)",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "Long difference (period 5 minus 1) with national shock g = shocks[5] - shocks[1], leave_one_out=False. AKM / AKM0 in diagnostics; Rotemberg alpha_k, beta_k are GPSS.",
    },
    "shift_share_political_panel": {
        "status": "bit-exact",
        "reference": "fixest::feols 0.14.0 (ssc adj=FALSE, cluster.adj=FALSE; unit / time / two-way clusters; unit, time, two-way FE; unbalanced panel); ShiftShareSE::ivreg_ss with FE dummies (AKM); bartik.weight::bw with FE dummies; AER + HC0 per period",
        "reference_versions": {"R": "R version 4.5.2 (2025-10-31)", "fixest": "0.14.0", "ShiftShareSE": "1.1.0", "bartik.weight": "0.1.0", "AER": "1.2.16", "sandwich": "3.1.1"},
        "tolerance": "estimate / SEs / Rotemberg / first-stage F 1e-9 rel (observed <= 1.1e-14)",
        "sides": ["py", "R"],
        "test": ["tests/reference_parity/test_synth_rest_R_parity.py", "tests/reference_parity/_fixtures/synth_rest_R.json"],
        "note": "Cluster SEs are CR0 (two-way = Cameron-Gelbach-Miller); AKM shock clusters are industry x period because the fixture's shocks vary over time. first_stage_F is the textbook partial F with FE df (computed from feols RSS); fixest's fitstat 'ivf1' is a different quantity and not compared.",
    },
```

`sequential_sdid` is deliberately not promoted: the name promises an estimator it does not
implement. If the integrator wants a record for the per-cohort blocks, use status "aligned" with
note "per-cohort ATT(g) = synthdid::synthdid_estimate 0.0.9 on the cohort sub-panel (1e-8);
not the Arkhangelsky–Samkov sequential estimator".

## 4. CHANGELOG / MIGRATION

**Added**
- `sp.synth_rmspe_filter(metric=, placebo_pool=)`: SCtools / ADH MSPE cut-offs, and placebo
  donor pools without the treated unit. Also placebo table in `df.attrs`.
- `sp.conformal_synth`: `model_info['joint_pvalue_grid']`, `ci_truncated`, `*_ci_unbounded`.
- `sp.shift_share_political`: AKM / AKM0 SE, CI and p in `diagnostics`; `beta_k` in `rotemberg_top`.
- `sp.shift_share_political_panel`: `diagnostics['akm0_ci']`, `['balanced']`.
- `sp.multi_outcome_synth`: `model_info['placebo_failures']`.

**⚠️ Correctness**
- ⚠️ `solve_simplex_weights` (all no-covariate SCM fits): exact active-set solution for
  identified problems. Outputs move by about 1e-7.
- ⚠️ `sp.conformal_synth`: now the Chernozhukov–Wüthrich–Zhu / `scinference` procedure (null
  re-estimation, moving-block Σ|u|). p-value, CI and se change; CI is (−inf, inf) when α is
  below the smallest attainable p.
- ⚠️ `sp.synth_power` / `sp.synth_mde`: rank-p rejection rule and a centred null baseline.
  Power is no longer 1 at δ = 0; the MDE is inf when α < 1/(J+1).
- ⚠️ `sp.synth_survival`: exact weights; the placebo band sign is fixed (`gap − q`); the band is
  documented as pointwise.
- ⚠️ `sp.shift_share_political`: Rotemberg weights are the GPSS weights (signed, sum to 1);
  share-balance F df fixed.
- ⚠️ `sp.shift_share_political_panel`:
  - exact two-way within transformation (unbalanced panels);
  - `cluster='twoway'` is CGM;
  - `cluster='shock'` is the AKM formula;
  - Rotemberg weights on FE-residualised x;
  - `first_stage_F` is a real partial F.
- ⚠️ `sp.synth_loo` / `sp.synth_time_placebo`: se / pvalue are NaN instead of 0 when undefined
  (T1 = 1).

**Changed / Fixed (labels)**
- `sp.sequential_sdid` is documented as cohort-by-cohort SDID, not Arkhangelsky–Samkov;
  `model_info['estimator']` added.
- `sp.synth_experimental_design`: `method` is now `"loo_sc_fit_ranking"`, and the Abadie–Zhao
  attribution is removed.
- `sp.synth_survival`: no longer claims Han–Shah SSC.
- `sp.shift_share_political*`: "Park & Xu" becomes Park (2026).
- `sp.multi_outcome_synth`: citation now lists all three authors.
- `sp.qqsynth` docstring corrected.

**MIGRATION rows**

| function | old default | new default | how to get old |
| --- | --- | --- | --- |
| `conformal_synth` | naive pre-residual ranks | CWZ moving block | not kept (old procedure had no reference) |
| `synth_power` / `synth_mde` | quantile rule; real effect in baseline | rank-p rule; centred baseline | not kept (anti-conservative) |
| `synth_survival` | EG solver; band `gap + q` | exact; band `gap − q` | not kept |
| `shift_share_political_panel(cluster="twoway")` | HC0 on unit × time cells | CGM two-way | not kept (mislabelled) |
| `shift_share_political*` Rotemberg | Σ\|·\|-normalised | GPSS signed | `abs_weight` column retained |
| `synth_experimental_design().method` | `"abadie_zhao_2025"` | `"loo_sc_fit_ranking"` | — |

## 5. Not closed

- **Stata side** of the SCM tools: `synth_runner` 1.6.0 and `synth` are installed privately.
  `synth.ado` rounds the unit weights to 3 decimals (`roundmat`; probe `e(W_weights)` gave
  0.285 / 0.715). At best the rank p-values could agree; no T2 is possible. Not run. A future
  run could compare `pval_joint_post` against
  `synth_rmspe_filter(placebo_pool="exclude_treated")` with StatsPAI's `#/n` → `(#+1)/(n+1)`
  mapping.
- **`sequential_sdid` as Arkhangelsky–Samkov** (class 6): no code exists. Implementing
  Algorithm 1 is a new-estimator task.
- **`stochastic_dominance`** (class 6):
  - no reference test exists;
  - its KS fallback treats quantile values as samples (not a valid test);
  - the order-1 p-value ranks the minimum quantile gap.
  Left as is and documented here; it needs a methodological redesign, not a parity fix.
- **`synth_survival`, `synth_power`, `synth_experimental_design`** are class 6 (identities only).
- **`multi_outcome_synth`**: the placebo SE, placebo p-values and the Fisher joint p have no
  reference. `estimate` averages raw-unit ATTs across outcomes (documented).
- **Forbidden files needing integrator edits:**
  - `registry.py` still says "Park-Xu", "Abadie-Zhao" and "Sequential SDID (Arkhangelsky &
    Samkov)" (entries around lines 7917–7947 and 8696–8824).
  - `docs/index.md` lines 52–54 (release history) repeat those labels.
  - Schemas / agent cards need regenerating (docstrings changed; one new keyword-only signature
    in `synth_rmspe_filter`).
- **Upstream reports:** scinference should check `lsei(...)$IsError` (D5).

## 6. .gitignore

`tests/reference_parity/_fixtures/_ado_synth_rest/` is already covered by the existing
`tests/reference_parity/_fixtures/_ado_*/` rule. Nothing new.

## Files

**Changed:**
- `src/statspai/synth/{_core,sensitivity,conformal,multi_outcome,power,survival,sequential_sdid,experimental_design,discos,__init__}.py`
- `src/statspai/bartik/political.py`
- `docs/guides/{shift_share_political_panel,v1_2_frontier}.md`
- `tests/test_{synth_helpers_untested,cov95_synth_classic_paths,cov95_synth_more,cov95_synth_variants,shift_share_political}.py`
  (pins updated, with rationale)

**New:** the generator, data script, fixtures and parity test listed at the top.

**Tests run green:**
- the new file (24);
- all `-k synth|scm|discos|sdid|conformal|sensitivity|shift_share|bartik|political|survival|power|experimental|multi_outcome|sequential` tests (1933 passed after the pin updates);
- doctests of the changed modules;
- round-1 `test_did_synth_{synthvar,shiftshare}_parity.py`.
