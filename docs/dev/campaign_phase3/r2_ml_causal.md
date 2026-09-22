# Round 2 — `ml_causal` family (grf operators, CDDF BLP/GATES, OPE, DML panel)

Worktree `.claude/worktrees/r2-grf-ope`. Status: DONE (open items in section 5).

Pattern used throughout (as `test_grf_aipw_operator_parity.py`): the forest /
learner is the only stochastic factor; the R script grows ONE
`grf::causal_forest`, freezes its OOB `tau.hat`, `Y.hat`, `W.hat`, and every
post-fit operator is compared deterministically on those vectors.

Files: data `tests/reference_parity/_fixtures/_generate_ml_causal_data.py`
(→ `ml_causal_{cate,ope,panel,panel_unbal}.csv`), generator
`tests/reference_parity/_generate_ml_causal_R.R` (→ `_fixtures/ml_causal_R.json`,
R 4.5.2, grf 2.6.1, GenericML 0.2.3, sandwich 3.1.1), test
`tests/reference_parity/test_ml_causal_R_parity.py` (34 tests).

## 1. Per-function table

| function | reference | class | max rel err est / SE | test |
| --- | --- | --- | --- | --- |
| `average_treatment_effect` (all/treated/control) | `grf::average_treatment_effect` 2.6.1 | 1 (T2) | 1.4e-15 / 1.3e-15 | test_ml_causal_R_parity.py |
| `average_treatment_effect` (overlap) | same, `target.sample="overlap"` | 2 (fixed) → 1 | 2.0e-15 / 5.2e-16 | same |
| `calibration_test` / `test_calibration` | `grf::test_calibration` (HC3, HC1) | 2 (fixed) → 1 | coef 1.1e-15, SE 1.1e-15, one-sided p 1.6e-13 | same |
| `rate` point + TOC | `grf::rank_average_treatment_effect` / `.fit` (with ties) | 2 (fixed) → 1 | 3.9e-15 / TOC 4.6e-15 | same |
| `rate` SE | grf half-sample bootstrap (R=2000) | 5 (T3) + fix | IF 0.07251 vs grf 0.07444 (AUTOC), 0.02164 vs 0.02201 (QINI); tol 6% | same |
| `honest_variance` | none (grf has no counterpart) | 2 (fixed) + 6 | identity sd(tau)/sqrt(n) at 5% (MC) | same |
| `forest_diagnostics` | none (descriptive) | 6 + fix (loud NaN) | identities exact | same |
| `blp_test` | `GenericML::BLP` 0.2.3 (const, HC1; with/without B) | 2 (fixed) → 1 | 2.3e-15 / 1.2e-15 | same + test_metalearners.py |
| `gate_test` | `GenericML::GATES` (monotonize=FALSE) + `quantile_group` | 2 (fixed) → 1 | 5.7e-16 / 1.9e-15 | same |
| `cate_eval` | grf RATE (shares `sp.rate` operator) | 2 (fixed) → 1 | = rate | same |
| `cate_by_group`, `cate_summary` | none — descriptive summaries of predictions | 6 | — | — |
| `ips` | Python `obp` 0.5.7 `InverseProbabilityWeighting` (lambda inf, 2) | 2 (fixed) → 1 | ~1e-15 / SE identity 1e-10 | test_ml_causal_obp_parity.py |
| `snips` | `obp` `SelfNormalizedInverseProbabilityWeighting`; SE = delta method (= `sp.ope.snips`) | 2 (fixed) → 1 | ~1e-15 / SE bootstrap-scale check | same |
| `direct_method` | `obp` `DirectMethod`, same reward model via new `q_hat=` | 1 | ~1e-15 | same |
| `doubly_robust` | `obp` `DoublyRobust` (lambda inf, 2), `q_hat=` | 2 (fixed) → 1 | ~1e-15 | same |
| `policy_value` | none; closed form `mean(Gamma*pi)` (R `policytree` / `grf` export no value function) | 6 | identity 1e-15 (existing test_policy_value_parity.py) | — |
| `policy_targeting` | none (rank-and-treat bookkeeping) | 6 | doctest identities | — |
| `dml_panel` | Python `DoubleML` 0.11.3 `DoubleMLPLR` cluster (unit) on `fixest::demean` data; R `ddml` 0.3.1 as convention (CR1) | 2 (fixed) → 1 | 1e-15 / 1e-15; within transform vs fixest 1e-10 abs | test_ml_causal_dml_parity.py |
| `dml_model_averaging` / `model_averaging_dml` | R `ddml::ddml_plm(shortstack=TRUE, ensemble_type="nnls1")` | 3 (weights T2; final regression convention: ddml intercept + HC1, rebuilt from our residuals at 1e-10) | weights 1e-14 | same |
| `dml_diagnostics` | none | 2 (fixed) + 6 | identities 1e-12 | same |
| `cluster_cate` | none: k-means clusters + within-cluster difference in means (checked `grf`, `GenericML`, `policytree`; no package does this) | 6 | existing recovery test | test_ml_causal_recovery_parity_round2.py |
| `focal_cate` | none: per-point linear DR-learner; `se_grid` is the residual SD of the pseudo-outcome regression, not a standard error of tau(x) (flagged, not changed) | 6 | existing recovery test | same |
| `auto_cate` | none (selection over learners; file on release-line list, not touched) | 6 | existing | test_ml_causal_recovery_parity.py |
| `cate_by_group`, `cate_summary` | none — descriptive summaries of predictions | 6 | — | — |

## 2. Defects found (all in files NOT on the release-line list)

1. **`calibration_test` was not grf's test** (first divergence: the design
   matrix). Old: regress a Horvitz–Thompson pseudo-outcome on
   `[tau, tau - mean(tau)]` (HC1, two-sided normal p). Because the two columns
   share `tau`, the "differential" coefficient estimated `b2 - b1`, not `b2`,
   so its test of 0 was a test of *equal* calibration. grf regresses
   `Y - Y.hat` on `(W - W.hat)·mean(tau)` and `(W - W.hat)(tau - mean)`, HC3,
   one-sided p from t(n-2). Fixture: differential 0.180 → **1.187** (grf
   1.18726); mean 0.985 → 1.00297. Also: the old code silently used
   mean-of-Y / mean-of-T stand-ins for nuisances on any non-training `X`; now
   raises. ⚠️ default output changed. New `vcov_type=` (default HC3).
2. **`rate`**: (a) scores were a HT signal, not grf's AIPW scores; (b) ties
   in priorities not averaged; (c) QINI weights `1 - u` (vs grf `k/n`), off by
   exactly `mean(score)/(2n)` (0.25814 vs 0.25869); (d) the influence-function
   SE omitted the rank-estimation term: 0.0949 vs grf bootstrap 0.0744
   (**+28%**). Fixed: grf operator exact; analytic rank-corrected SE 0.0725
   (within grf MC). Added `priorities=`, `se_method='half_sample'`,
   `n_bootstrap=`. Non-training `X` now raises. ⚠️ default output changed.
3. **`cate_eval`** had its own copy of the old RATE (same defects 2b–2d);
   now shares the operator. ⚠️ default output changed.
4. **`average_treatment_effect(target_sample='overlap')`** used an
   `e(1-e)`-weighted AIPW mean; grf uses the R-learner OLS with intercept +
   HC3. Fixture: 1.12386 / 0.07687 → 1.12514 / 0.07968 (grf exact). Also
   out-of-sample rows now warn when falling back to plug-in (was silent
   except for a `method` field). ⚠️ default output changed (overlap only).
5. **`honest_variance`** SE was `sd(half-means)/sqrt(n_splits)` — Monte
   Carlo error of the average, shrinking to 0 with more splits (0.0038 at 25
   splits vs sampling SE 0.024). Now the half-sample spread (FPC ½ makes it
   ≈ sd(tau)/sqrt(n)). Docstring now says it is descriptive. ⚠️
6. **`forest_diagnostics`** on non-training rows filled propensities with
   `mean(T)` → reported perfect overlap. Now NaN + warning.
7. **`blp_test`** ran unweighted OLS on **in-sample** CATE predictions with a
   docstring claiming equivalence to `grf::test_calibration`. On a
   constant-effect DGP (n=400, T-learner) it reported beta2 ≈ 1.43,
   p ≈ 3e-52. Now CDDF WLS (weights 1/(p(1-p))), out-of-fold proxy by default
   (`proxy='cross_fit'`), optional `propensity=`, `baseline=`,
   `vcov_type=` (default HC1; GenericML default `const` available).
   Null DGP: beta2 0.137, p 0.29. Old behaviour reachable via
   `proxy='in_sample'` (tested). ⚠️
8. **`gate_test`** had no outcome regression at all: ANOVA / t-tests on the
   model's own predictions grouped by the same predictions (p-values
   meaningless). Now GATES WLS when `y/treat/covariates` given; the old
   descriptive path remains, with a warning. Also found while pinning:
   `sandwich::vcovHC(type="const")` on a weighted lm is **not** `vcov(lm)`
   (it uses `sum((w e)^2)/(n-k) · (X'WX)^-1 X'X (X'WX)^-1`); implemented as R.

9. **OPE `clip` floored the behaviour propensity** at `1/clip` as well as
   capping the weight (`ips` / `snips` / `doubly_robust`): with `clip=2`
   IPS gave 0.8496 vs obp `lambda_=2` 1.1904. Now caps the weight only
   (obp's `lambda_`); `pi_b <= 0` raises. Inert at the default `clip=50`
   whenever `pi_b >= 0.02`.
10. **`snips` SE divided by `sum(w)` instead of `mean(w)`**: 0.00039 vs
    bootstrap 0.0174 (n = 2000). Now the delta-method SE, equal to
    `sp.ope.snips`. ⚠️
11. **`doubly_robust` with a 1-D (deterministic action) policy** read the
    action vector as target *probabilities* in the correction term (weights
    = action index / pi_b). Fixture, always-action-2: 1.3054 → 0.8555
    (arm-2 sample mean 0.896). ⚠️
12. **`dml_panel` two-way within transform stopped after one sweep** — exact
    only for balanced unweighted panels. Unbalanced fixture: max abs error
    0.19 in y; estimate 0.82050 → 0.81951 (DoubleML 0.81951). Now
    alternating projections to 1e-13 (fixest-equal). ⚠️ (unbalanced /
    weighted two-way only).
13. **`dml_diagnostics` "orthogonality test" was identically 0 / p = 1**: the
    PLR "score" was the demeaned outcome residual. Now the PLR score
    `(y_r - theta d_r) d_r`; statistic relabelled as a moment check (zero by
    construction for n_rep = 1), since no mean-of-score statistic can test
    nuisance specification.
14. `dml_model_averaging` CLS weights: SLSQP (ftol 1e-10) replaced by an
    exact support-enumeration QP for K <= 12 (SLSQP beyond, now warns when
    it falls back instead of silently). Not a default-output change beyond
    ~1e-8.

Added (no numeric change): `fold_indices=` on `dml_panel` and
`dml_model_averaging`; `q_hat=` on `direct_method` / `doubly_robust`;
stacked residuals in `dml_model_averaging().model_info`.

Shared core: new `src/statspai/metalearners/_cddf.py`.

## 3. Promotion records (final, paste-ready)

Grading choice for `rate` / `cate_eval`: **"aligned"**, with the tolerance
string stating that the point estimate and TOC curve are exact and the SE is
T3 (grf's SE is a half-sample bootstrap). No `_FACTOR_NOTES` entry is needed.

The block below `exec`s cleanly with no builtins (`exec(src, {"__builtins__": {}})`, checked).

```python
R_VER = "R version 4.5.2 (2025-10-31)"
GRF_TEST = [
    "tests/reference_parity/test_ml_causal_R_parity.py",
    "tests/reference_parity/_fixtures/ml_causal_R.json",
]
OBP_TEST = [
    "tests/reference_parity/test_ml_causal_obp_parity.py",
    "tests/reference_parity/_fixtures/ml_causal_obp.json",
]
DML_TEST = [
    "tests/reference_parity/test_ml_causal_dml_parity.py",
    "tests/reference_parity/_fixtures/ml_causal_panel_R.json",
    "tests/reference_parity/_fixtures/ml_causal_doubleml.json",
]
GRF_OP_NOTE = (
    "Factored evidence: grf grows one causal forest (2000 trees, seed 42) and "
    "its OOB tau.hat, Y.hat and W.hat are frozen in the fixture; StatsPAI's "
    "operator runs on exactly those vectors. The forest itself is not "
    "pinnable across implementations (see causal_forest)."
)
CALIB_REF = "grf::test_calibration 2.6.1 (vcov.type HC3 default and HC1), forest outputs held fixed"
CALIB_TOL = (
    "coef, se, t 1e-10 rel (observed 1.1e-15); one-sided p-value 1e-8 rel "
    "(observed 1.6e-13)"
)
RATE_TOL = (
    "Point estimate (AUTOC, QINI) and TOC curve on q = 0.1..1 exact at 1e-10 rel "
    "(observed 4.6e-15), including a 30-group tied-priority case against "
    "rank_average_treatment_effect.fit. SE is T3: the analytic rank-corrected "
    "influence-function SE is compared with grf's half-sample bootstrap "
    "(R = 2000) at 6% rel (observed 2.6% AUTOC, 1.7% QINI)."
)
OBP_VERSIONS = {"obp": "0.5.7"}
OBP_NOTE = (
    "Python cross-package reference, not R or Stata: no R/Stata "
    "implementation takes K-action logged-bandit data with given behaviour "
    "and evaluation policies. Behaviour propensities, evaluation policy and a "
    "fixed reward model (q_hat=) are columns of ml_causal_ope.csv, so the "
    "estimator is deterministic. obp reports bootstrap intervals only; the "
    "analytic SE is checked as sd(obp round rewards)/sqrt(n) at 1e-10."
)
AVG_REF = "ddml::ddml_plm 0.3.1 (shortstack = TRUE, ensemble_type = 'nnls1'), OLS candidates, shared folds"
AVG_TOL = (
    "short-stacking weights 1e-10 (observed 4.4e-14); ddml's final "
    "lm(y_r ~ d_r) with intercept and HC1 SE rebuilt from StatsPAI's stacked "
    "residuals at 1e-10 (observed 4.8e-16)"
)
AVG_NOTE = (
    "Convention difference in the last step only: StatsPAI solves the "
    "no-intercept PLR moment with the HC0 sandwich (DoubleML convention); "
    "ddml fits OLS with an intercept and reports HC1. The raw point estimates "
    "differ by 1.2e-5 rel on the fixture for that reason."
)
GENERICML_VERSIONS = {"R": R_VER, "GenericML": "0.2.3", "sandwich": "3.1.1"}

PROMOTIONS = {
    "average_treatment_effect": {
        "status": "bit-exact",
        "reference": "grf::average_treatment_effect 2.6.1 (target.sample all, treated, control, overlap), forest outputs held fixed",
        "reference_versions": {"R": R_VER, "grf": "2.6.1"},
        "tolerance": "estimate and std.err 1e-10 rel (observed 2.0e-15)",
        "sides": ["py", "R"],
        "test": GRF_TEST,
        "note": GRF_OP_NOTE + " clip=0 on the comparison (grf does not clip); the default clip=0.01 is asserted inert on this fixture.",
    },
    "calibration_test": {
        "status": "bit-exact",
        "reference": CALIB_REF,
        "reference_versions": {"R": R_VER, "grf": "2.6.1", "sandwich": "3.1.1"},
        "tolerance": CALIB_TOL,
        "sides": ["py", "R"],
        "test": GRF_TEST,
        "note": GRF_OP_NOTE,
    },
    "test_calibration": {
        "status": "bit-exact",
        "reference": CALIB_REF,
        "reference_versions": {"R": R_VER, "grf": "2.6.1", "sandwich": "3.1.1"},
        "tolerance": CALIB_TOL,
        "sides": ["py", "R"],
        "test": GRF_TEST,
        "note": "Alias of calibration_test (asserted to return an identical frame). " + GRF_OP_NOTE,
    },
    "rate": {
        "status": "aligned",
        "reference": "grf::rank_average_treatment_effect and rank_average_treatment_effect.fit 2.6.1 (AUTOC, QINI, TOC), forest outputs held fixed",
        "reference_versions": {"R": R_VER, "grf": "2.6.1"},
        "tolerance": RATE_TOL,
        "sides": ["py", "R"],
        "test": GRF_TEST,
        "note": GRF_OP_NOTE,
    },
    "cate_eval": {
        "status": "aligned",
        "reference": "grf::rank_average_treatment_effect 2.6.1 (AUTOC, QINI, TOC), fed grf's nuisances; shares sp.rate's operator",
        "reference_versions": {"R": R_VER, "grf": "2.6.1"},
        "tolerance": RATE_TOL,
        "sides": ["py", "R"],
        "test": GRF_TEST,
        "note": "Given e_hat, m_hat, mu1_hat, mu0_hat from grf's forest (no internal cross-fit). " + GRF_OP_NOTE,
    },
    "blp_test": {
        "status": "bit-exact",
        "reference": "GenericML::BLP 0.2.3 (vcovHC const and HC1; with and without the baseline proxy)",
        "reference_versions": GENERICML_VERSIONS,
        "tolerance": "beta and SE 1e-10 rel (observed 2.3e-15); one-sided p 1e-8 rel",
        "sides": ["py", "R"],
        "test": GRF_TEST,
        "note": "Grade covers the weighted regression given the CATE proxy, propensity and baseline proxy (identical inputs on both sides); the default out-of-fold proxy refit is StatsPAI's own.",
    },
    "gate_test": {
        "status": "bit-exact",
        "reference": "GenericML::GATES 0.2.3 (monotonize = FALSE) with GenericML::quantile_group membership",
        "reference_versions": GENERICML_VERSIONS,
        "tolerance": "gamma_k, SE and gamma_K - gamma_1 1e-10 rel (observed 1.9e-15); group membership identical",
        "sides": ["py", "R"],
        "test": GRF_TEST,
        "note": "Only the y/treat/covariates (GATES regression) path is graded; the descriptive fallback without outcomes is not.",
    },
    "ips": {
        "status": "bit-exact",
        "reference": "Open Bandit Pipeline (obp) 0.5.7 InverseProbabilityWeighting (lambda_ inf and 2)",
        "reference_versions": OBP_VERSIONS,
        "tolerance": "value 1e-12 rel (observed 0.0); SE identity 1e-10",
        "sides": ["py"],
        "test": OBP_TEST,
        "note": OBP_NOTE,
    },
    "snips": {
        "status": "bit-exact",
        "reference": "Open Bandit Pipeline (obp) 0.5.7 SelfNormalizedInverseProbabilityWeighting",
        "reference_versions": OBP_VERSIONS,
        "tolerance": "value 1e-12 rel (observed 0.0); delta-method SE identity 1e-10 and equal to sp.ope.snips",
        "sides": ["py"],
        "test": OBP_TEST,
        "note": OBP_NOTE,
    },
    "direct_method": {
        "status": "bit-exact",
        "reference": "Open Bandit Pipeline (obp) 0.5.7 DirectMethod (same reward-model matrix via q_hat=)",
        "reference_versions": OBP_VERSIONS,
        "tolerance": "value 1e-12 rel (observed 0.0); SE identity 1e-10",
        "sides": ["py"],
        "test": OBP_TEST,
        "note": OBP_NOTE + " The default internal random-forest reward model is not graded.",
    },
    "doubly_robust": {
        "status": "bit-exact",
        "reference": "Open Bandit Pipeline (obp) 0.5.7 DoublyRobust (lambda_ inf and 2; same reward model via q_hat=)",
        "reference_versions": OBP_VERSIONS,
        "tolerance": "value 1e-12 rel (observed 1.8e-16); SE identity 1e-10",
        "sides": ["py"],
        "test": OBP_TEST,
        "note": OBP_NOTE + " The default internal random-forest reward model is not graded.",
    },
    "dml_panel": {
        "status": "bit-exact",
        "reference": "fixest::demean 0.14.0 (unit and unit+time absorption, balanced and unbalanced) and ddml::ddml_plm 0.3.1 (OLS learner, unit clusters, shared folds)",
        "reference_versions": {"R": R_VER, "fixest": "0.14.0", "ddml": "0.3.1", "sandwich": "3.1.1", "doubleml": "0.11.3", "scikit-learn": "1.6.1"},
        "tolerance": "within transform 1e-10 abs (observed 2.6e-14); estimate 1e-10 rel vs ddml and DoubleML (observed 4.1e-16); SE 1e-10 rel vs DoubleML (observed 1.4e-15) and vs ddml after the CR1 factor",
        "sides": ["py", "R"],
        "test": DML_TEST,
        "note": "OLS learners and shared unit-level folds (fold_indices=). R leg: fixest pins the FE absorption, ddml the PLR estimate; ddml's SE is CR1 = StatsPAI's times sqrt(G/(G-1)(n-1)/(n-2)) (tested to 1e-10). Python leg: DoubleML 0.11.3 DoubleMLPLR with one-way unit clustering on the fixest-demeaned data matches estimate and SE (R DoubleML 1.0.2 refuses external splits with clustered data).",
    },
    "dml_model_averaging": {
        "status": "aligned",
        "reference": AVG_REF,
        "reference_versions": {"R": R_VER, "ddml": "0.3.1", "sandwich": "3.1.1"},
        "tolerance": AVG_TOL,
        "sides": ["py", "R"],
        "test": DML_TEST,
        "note": AVG_NOTE,
    },
    "model_averaging_dml": {
        "status": "aligned",
        "reference": AVG_REF,
        "reference_versions": {"R": R_VER, "ddml": "0.3.1", "sandwich": "3.1.1"},
        "tolerance": AVG_TOL,
        "sides": ["py", "R"],
        "test": DML_TEST,
        "note": "Alias of dml_model_averaging. " + AVG_NOTE,
    },
}
```

`PYTHON_REFERENCE_ROWS` additions (`src/statspai/_parity_taxonomy.py`):

```python
    "ips": "obp (Python; Open Bandit Pipeline) 0.5.7 InverseProbabilityWeighting",
    "snips": "obp (Python; Open Bandit Pipeline) 0.5.7 SelfNormalizedInverseProbabilityWeighting",
    "direct_method": "obp (Python; Open Bandit Pipeline) 0.5.7 DirectMethod",
    "doubly_robust": "obp (Python; Open Bandit Pipeline) 0.5.7 DoublyRobust",
```

`dml_panel` is not added: its R leg (fixest + ddml) is really compared, and
the DoubleML leg is recorded in its `note`.

Not promoted (class 6, keep current grade): `honest_variance`,
`forest_diagnostics`, `dml_diagnostics`, `policy_value`, `policy_targeting`,
`cluster_cate`, `focal_cate`, `auto_cate`, `cate_by_group`, `cate_summary`.

## 4. CHANGELOG / MIGRATION drafts

⚠️ Correctness:
- `sp.calibration_test` / `sp.test_calibration` now compute `grf::test_calibration` (differential coefficient was `b2 - b1`; HC3; one-sided t p-values). Rows must be the training sample.
- `sp.rate`: grf AIPW scores, tie averaging, QINI `k/n` weights, rank-corrected IF SE (old SE ~30% too large). New `priorities=`, `se_method=`, `n_bootstrap=`.
- `sp.cate_eval`: same RATE fixes.
- `sp.average_treatment_effect(target_sample='overlap')`: grf R-learner estimator; plug-in fallback now warns.
- `sp.honest_variance`: `se` no longer divided by `sqrt(n_splits)`.
- `sp.blp_test`: CDDF weighted regression, out-of-fold proxy by default (old in-sample OLS rejected a constant effect at p ~ 1e-52). New `propensity=`, `baseline=`, `proxy=`, `vcov_type=`, `seed=`.
- `sp.gate_test`: GATES regression when `y/treat/covariates` given; descriptive path warns.
Fixed: `sp.forest_diagnostics` reports NaN overlap (not perfect overlap) for rows without propensities.

- `sp.ips` / `sp.snips` / `sp.doubly_robust`: `clip` caps weights only; `snips` SE fixed (was ~sqrt(n) too small); `doubly_robust` 1-D policy fixed.
- `sp.dml_panel(include_time_fe=True)`: exact two-way within transform on unbalanced / weighted panels.
- `sp.dml_diagnostics`: score and moment check fixed.
Added: `fold_indices=` (`dml_panel`, `dml_model_averaging`), `q_hat=` (`direct_method`, `doubly_robust`), `vcov_type=` (`calibration_test`), `priorities=` / `se_method=` / `n_bootstrap=` (`rate`), `propensity=` / `baseline=` / `proxy=` / `vcov_type=` / `seed=` (`blp_test`, `gate_test`).

MIGRATION rows: one per ⚠️ item above ("old number → new number on fixture" as in §2); `proxy='in_sample'` reproduces old `blp_test` proxy (but weighted).

## 5. Open / not closed

- `rate` SE is T3 by nature (grf's is a bootstrap): analytic SE within 3% of grf R = 2000.
- `focal_cate.se_grid` is the residual SD of the pseudo-outcome regression,
  not an SE of tau(x); left as is (no reference, class 6) — needs a
  maintainer decision (rename or compute a proper SE).
- `blp_test` / `gate_test` docstrings cite CDDF as "(citation needed)": no
  verified bib entry exists (`chernozhukov2020generic` in paper.bib is a
  different paper — Chernozhukov, Fernandez-Val, Melly, Wuthrich 2020 JASA;
  the old forest_inference docstring misused it, removed). Also the old
  forest_inference header cited `athey2019surrogate` for GRF (wrong key);
  replaced by `athey2019generalized`. The same wrong key remains in
  `forest/iv_forest.py` and `forest/multi_arm_forest.py` (not touched).
- Pre-existing: `pytest --doctest-modules src/statspai/forest/forest_inference.py`
  collects the alias `test_calibration` as a test (fixture `forest` not found).
- Registry ParamSpecs for the new keyword arguments and schema regeneration
  are the integrator's (registry.py / schemas not edited).

## 6. .gitignore

None. obp is installed with `pip install --no-deps --target <tmp>` outside
the repo (documented in `_generate_ml_causal_obp.py`).

## 7. Files

New: `tests/reference_parity/_fixtures/_generate_ml_causal_data.py`,
`_generate_ml_causal_obp.py`, `_generate_ml_causal_doubleml.py`,
`tests/reference_parity/_generate_ml_causal_R.R`, `_generate_ml_causal_panel_R.R`,
fixtures `ml_causal_{cate,ope,panel,panel_unbal}.csv`,
`ml_causal_{R,panel_R,obp,doubleml}.json`, tests
`test_ml_causal_{R,obp,dml}_parity.py`, `src/statspai/metalearners/_cddf.py`.
Modified: `forest/forest_inference.py`, `metalearners/{diagnostics,cate_eval}.py`,
`policy_learning/ope.py`, `dml/{panel_dml,model_averaging,_diagnostics}.py`,
`tests/test_{forest_inference,metalearners,cov95_dml_diag_sens}.py`.
Generator order: data.py → both .R → obp.py / doubleml.py.

## 8. Test run

Last full run of every touched module's tests plus the new parity files and
doctests of the modified modules: 381 passed, 1 skipped, 0 failed (the one
failure, `test_ml_causal_polish.py::TestDMLDiagnostics::test_summary_string`,
was the renamed summary label; updated and re-run green). New parity tests:
`test_ml_causal_R_parity.py` 34, `test_ml_causal_obp_parity.py` 11,
`test_ml_causal_dml_parity.py` 15. Also modified test files for the new
contracts: `tests/test_ml_causal_polish.py` (label).
