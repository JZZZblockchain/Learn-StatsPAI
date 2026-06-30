# Grammar + SE-menu convergence — week roadmap

Tracks the "consistent grammar + universal SE menu" workstream prompted by the
reviewer note on signature consistency. **Constraint (ratified 2026-06-30):**
additive + reversible only during JSS review — no estimator default or numerical
output changes; no hard deprecations until after acceptance. Canonical
spellings: `vce` (SE), `y` (outcome), `treat` (treatment).

## Done (this branch: `worktree-grammar-se-menu`)

- **D1 — signature house-style lint.** `src/statspai/_house_style.py` (canonical
  vocab + alias map + false-friend allowlist), `scripts/signature_house_style.py`
  (introspection lint, `--json/--check/--update-baseline` ratchet),
  `signature_house_style_baseline.json` (186 legacy sites, 41 acknowledged false
  friends), `tests/test_signature_house_style.py`.
- **D2 — alias plumbing.** `src/statspai/_aliases.py` (`@accepts_aliases`,
  silent additive forwarding, warns gated off, conflict→TypeError,
  signature-preserving). Applied to `sp.regress` (`vce=`→`robust=`, coef+SE
  bit-identical across nonrobust/hc1/hc3/cluster). `tests/test_aliases.py`.
- **D4a — SE-menu matrix gate.** `scripts/se_menu_matrix.py` (curated coverage
  matrix validated against the live API; drift guard; native-up/unsafe-down
  ratchet). Today: 34 native, 5 standalone, 5 unsafe (`ivreg`), 12 stranded.
  `tests/test_se_menu_matrix.py`.
- **Grammar doc.** `docs/guides/grammar.md` (canonical vocab + honest SE matrix
  + the two gates).
- **D3 — shared design extractor.** `inference/jackknife.py::_design_from_result`
  prefers stored `data_info['X'/'y'/'var_names']`, falls back to the formula
  re-parse only when rows can't be aligned (NA-filtered samples). `cr2_se` and
  `wild_cluster_boot` rerouted through it. Proven **byte-identical** to the
  re-parse path on `sp.regress` (forced-fallback test).
- **D4b (partial) — feols within-design.** `fixest/adapter.py` now stores the
  pyfixest within-transformed design (`_X`/`_Y`/`_coefnames`) on the result —
  purely additive, no feols numerics change. So `wild_cluster_boot` / `conley` /
  `twoway_cluster` / `cr2_se` now run on `sp.feols` (previously `KeyError: 'X'`).
  Matrix: feols `wild_cluster_boot` and `conley` flipped `na → standalone`.
  **Verified with no external tools:** (a) feols-no-FE ≡ regress exactly for
  cr2/wild/conley/twoway; (b) feols-FE wild bootstrap byte-identical to
  `regress` on manually FE-demeaned data (the textbook within wild bootstrap).
  `tests/test_se_menu_feols_wiring.py` (8 tests).
- **D4b-cont — native `feols(vce="wild")`.** `fixest/wrapper.py` now exposes a
  first-class `feols(..., vce="wild", cluster=...)` running the WCR wild cluster
  bootstrap on the within design (plus `vce=` as the canonical alias for `vcov=`
  and `cluster=` as one-way CRV1 shorthand, mirroring `sp.regress`). Matrix:
  feols `wild_cluster_boot` flipped `standalone → native` (native cells 34→35).
  **External parity vs Stata** `reghdfe`+`boottest` (18 MP, boottest 4.5.3):
  point estimate & CRV1 SE match `reghdfe` to ~1e-9, wild p-value matches
  `boottest`'s exact 2¹⁵ enumeration to MC error (0.0265 vs 0.0263).
  `tests/reference_parity/test_feols_wild_boottest_parity.py` (frozen Stata
  values, no R/Stata needed in CI).

## Remaining

### D3-cont — single vcov backend  *(deep, multi-session)*
- Wire `core/_vcov.py` canonical primitives (`sandwich_vcov`, `cluster_robust_vcov`,
  `hc_vcov`) as the single backend; retire per-estimator sandwich re-implementations.
- ⚠ Collision risk: `core/results.py` is edited by the parallel window — rebase/merge carefully.

### D4b-cont — remaining SE-menu cells  *(touches estimators)*
Against the `se_menu_matrix` gate:
- **feols `cr2_cr3`**: held at `na`. The within-transform CR2 omits the FE
  projection from the leverage adjustment, so it is NOT guaranteed equal to
  `clubSandwich`'s absorbed-FE CR2. Flip only after an R `clubSandwich` parity
  test (needs the absorbed-FE hat-matrix correction).
- **Native `vce=` on feols**: promote the standalone wild/conley to a native
  `feols(..., vce="wild")` parameter and unify the two `feols` doors (pyfixest
  vs panel) so their SE menus match.
- **`ivreg`**: two-stage-aware wild/CR2 (kill the 5 ⚠ cells); the standalone
  helpers currently refit plain OLS and drop the IV structure. Needs the 2SLS
  projected design stored on the result, then parity vs Stata `ivreg2`/`boottest`.

### D5 — unify the result contract  *(collision risk: results.py)*
- One §3-true protocol: `summary`/`plot`/`to_latex`/`to_word`/`to_excel`/`cite`
  (today only 11/279 classes satisfy all six; `to_word` 6%, `to_excel` 7%).
- Reconcile naming: `postestimation_contract` advertises `to_docx`/`to_html`
  while §3 / canonical classes use `to_word`/`to_excel` — pick one, alias the other.
- Push `ResultProtocolMixin` (71 classes) to the full six.
- Convert the worst ~67 raw-`dict`-returning functions (`hausman_test`, `irf`,
  `evalue`, `sensemakr`, `wild_cluster_*`, …) to lightweight result objects.
- Extend `result_protocol_audit.py` to track the §3 six and gate it.

### D6 — family front doors  *(collision risk: recommend.py, detect_design)*
- BJS: `bjs` = `borusyak_jaravel_spiess` = `did_imputation` → one canonical +
  deprecated aliases. Same for `gardner_did` = `did_2stage`.
- Move/deprecate the misfiled `did_estimate` (a synthdid alias in the DiD namespace).
- `did(method=)` route to staggered estimators, or document the front door.
- Unify `detect_design` (3 designs) and `recommend._detect_design` (7) into
  shared code; add synthetic-control coverage (today zero in `recommend`).
- Coordinate with the parallel window already editing `recommend.py`.

### D7 — CI wiring + paper check
- Promote `signature_house_style --check` and `se_menu_matrix --check` to
  blocking gates in `.github/workflows/ci-cd.yml` (alongside `error_taxonomy_audit`).
- Add `result_protocol_audit` §3 gate once D5 lands.
- **Audit `paper.md` / JSS manuscript** for any "universal SE menu" wording that
  overstates current coverage — the matrix shows wild/CR2/Conley are OLS-path +
  FE-path-wild today, not universal. Reword to match reality before it reaches a reviewer.

## Merge note
This branch is isolated from a concurrent window editing `results.py`,
`recommend.py`, `iv.py`, `registry.py`, `README*`. New files here don't collide;
the only shared edit is `regression/ols.py` (one decorator line). Reconcile
`_house_style.py`/test refinements (e.g. the `rd_flex` `W` false-friend) when merging.
