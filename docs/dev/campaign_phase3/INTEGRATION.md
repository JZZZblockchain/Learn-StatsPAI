# Phase 3 integration ledger

Integration tree: `.claude/worktrees/jss-int` = `origin/main` (HEAD, includes
PR #45 and the dml/forest correctness fix 42147197) + the whole campaign
(round 1: 8 families, round 2: 6 families) as uncommitted changes. Nothing is
committed; this tree waits for maintainer authorisation. It supersedes
`wt/jss-submit`, whose two commits of 2026-09-19 (7904dda0, 6329d0e7) were
made by another session; 6329d0e7 raised the error-taxonomy ceiling and is
deliberately NOT carried over (the raises were migrated instead).

## Numbers

- Estimator callables with a cross-language (R/Stata) grade: 224 -> 415 of
  773 (29.0% -> 53.7%); any numerical evidence 429 -> 540.
- Defects fixed: 174 (round 1: 125, round 2: 49). Drafts:
  `CHANGELOG_phase3.md` + `CHANGELOG_phase3_r2.md`, `MIGRATION_phase3.md` +
  `MIGRATION_phase3_r2.md` (to merge into CHANGELOG.md / MIGRATION.md under
  [Unreleased] at commit time).
- Track A: 89/89 python sides reproduce, 0 drift; fixture lock and parity
  tables regenerated; parity contract green.

## Merge decisions against origin/main

- `dml/_diagnostics.py`: upstream (PR #45) design kept; the campaign's
  alternative (real PLR score + "moment check") dropped; its test replaced by
  a design-independent balance-table identity.
- `forest/forest_inference.py`: merged two independent grf re-alignments:
  upstream structure (GRF engine, training-row requirement, aliases,
  deprecations, calibrate_cate) + campaign operator layer (grf_calibration,
  rate_from_scores, ATE operators) with public functions routed through it.
  Disagreements settled by R grf: calibration t/p (grf: vs 0, one-sided t);
  HC0 n/(n-1) (upstream matched vcovCL); RATE SE (campaign; upstream 28% high).
- `paper.bib`: upstream's chernozhukov2025generic entry kept; campaign adds
  hansen1997approximate, choi2001unit, fuentes2001parametric (verified).
- Error taxonomy: 244 new generic raises migrated to taxonomy classes by
  meaning; ceiling unchanged at 1902 (observed 1879).

## Integration-side fixes (beyond the family deliverables)

Registry ParamSpecs for new parameters; house-style `vce` renames
(`four_way_decomposition`, `calibration_test`, `blp_test`, `gate_test`);
`panel_unitroot(robust=)` registered as a Stata false friend; blp/obp rows in
PYTHON_REFERENCE_ROWS; `iv_wild_bootstrap` full enumeration (exact vs
boottest); `grapple` non-convergence warning; attribution corrections
(Zuber-Colijn-Klaver-Burgess, Park 2026, Han & Shah, Abadie-Zhao,
Arkhangelsky-Samkov, GRF bib key); `docs/guides/synth_experimental.md`
rewritten (removed a variance formula absent from the cited paper and an
unsourced tuning recommendation); unverifiable end pages removed.

## Not merged / open

- `UNREVIEWED_iv_quantile.patch`: an interrupted sub-agent's change to
  `regression/iv_quantile.py`; broke a test; needs review before use.
- `twfe_decomposition`: bit-exact replacement exists
  (`did/_twfe_weights.dcdh_fe_weights`) but is not wired in; the file is on the
  uncommitted stata-grammar line. Strict xfail pins the defect.
- margins family D1-D5 (postestimation line), `rd_extrapolate` flat CATE,
  `focal_cate.se_grid` naming, pre-existing doctest failures (11) in files on
  the stata-grammar line, module 27 Stata quadrature switch.
- Maintainer decisions: lonely-PSU default; `roc_curve` / `direct_standardize`
  / `power_case_control` defaults; attribution note for formulas reimplemented
  from GPL `cmprsk`.

## Paper (Paper-JSS) sync after the release

05-parity-compact.tex "all but two" -> list Python references (econml,
DoubleML, pyblp, obp); coverage numbers; correctness-history table row;
Track A counts; `make submission-ready` after the release tag.
