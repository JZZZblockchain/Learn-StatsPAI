# Panel Shift-Share IV for Political Science

> Background: Park (arXiv:2603.00135, 2026); inference: Adão-Kolesár-Morales
> (QJE 2019) shock-level variance. Numbers are checked against R `fixest`,
> `ShiftShareSE::ivreg_ss` and `bartik.weight` in
> `tests/reference_parity/test_synth_rest_R_parity.py`.

## 1. When to use this

Use `sp.shift_share_political_panel` when **all** of the following hold:

- You have a **unit × time** panel (states × years, counties × election
  cycles, etc.).
- Your endogenous regressor is built from unit-specific *exposure
  shares* times a common *shift* vector — the canonical Bartik /
  shift-share setup.
- Either the shares **or** the shocks (or both) vary over time.
- You want pooled 2SLS with fixed effects plus the AKM
  shock-level SE.

For single-period (cross-section / long-difference) designs use
`sp.shift_share_political` or `sp.bartik` instead.

## 2. API

```python
import statspai as sp

res = sp.shift_share_political_panel(
    data=df,                    # long-format unit × time panel
    unit='state',
    time='year',
    outcome='vote_share',
    endog='exposure',

    # --- shares: either time-invariant (DataFrame unit×industry)
    # ---          or per-period (dict[time -> DataFrame])
    shares=shares,

    # --- shocks: either (1) Series (industry -> scalar; constant across time)
    # ---          or    (2) DataFrame (time × industry)
    # ---          or    (3) dict[time -> Series]
    shocks=shocks,

    covariates=['demographic_controls', 'fiscal_base'],
    fe='two-way',               # two-way | unit | time | none
    cluster='shock',            # shock | unit | time | twoway
    alpha=0.05,
)
print(res.summary())
```

Returns `ShiftSharePoliticalPanelResult` with

- `estimate`, `se`, `ci` — pooled 2SLS coefficient on `endog`
- `per_period` — DataFrame of cross-sectional estimates per `time`
  (turn it into an event-study plot directly)
- `rotemberg_panel` — industry-level weight decomposition, aggregated
  across all periods
- `share_balance` — F-test of pre-period covariates on the share matrix
- `diagnostics` — includes `cluster` label, `akm_se`, `first_stage_F`

## 3. The AKM shock-clustered SE

Standard unit- or two-way-clustered SEs are **inconsistent** for
shift-share designs: they ignore the fact that observations sharing a
shock are correlated through the common shifter, not through a geographic
cluster.  Adão-Kolesár-Morales (2019) derive the correct variance
estimator by clustering at the **shock** level with share-weighted
scores. The panel version used here is exactly `ShiftShareSE::ivreg_ss`
with the fixed effects as controls: the shock-level score is
$\hat X_k\, s_k'\hat\varepsilon$ with $\hat X_k$ the coefficients of the
control-residualised instrument on the share matrix. Shock clusters are
industries when the shocks are constant over time and industry × period
otherwise. (Before the 2026-09 fix this function used
$\sum_{i,t} s_{ikt}\tilde Z_{it}\hat\varepsilon_{it}$, which is not the AKM
formula.)  Pass `cluster='shock'` to
get this variance; the `diagnostics['akm_se']` field is also populated
so you can report both numbers side-by-side.

`cluster='unit'` / `'time'` are CR0 cluster-robust SEs (fixest with
`ssc(adj=FALSE, cluster.adj=FALSE)`); `'twoway'` is Cameron-Gelbach-Miller
two-way clustering by unit and time.

## 4. Fixed-effects choices

| `fe`         | What's absorbed           | When to pick                   |
|--------------|---------------------------|--------------------------------|
| `'two-way'`  | Unit + time FEs (default) | Almost always |
| `'unit'`     | Unit FEs only             | Time-invariant shares + strong time trend |
| `'time'`     | Time FEs only             | Balanced panel with few units  |
| `'none'`     | No FEs                    | You want pure cross-period pool |

Two-way FE are removed by alternating projections to convergence, so the
within transformation is exact on unbalanced panels too.

## 5. End-to-end recipe

```python
import numpy as np, pandas as pd, statspai as sp

rng = np.random.default_rng(0)
units, times, inds = list(range(100)), list(range(4)), [f'I{k}' for k in range(15)]

shares = pd.DataFrame(
    rng.dirichlet(np.ones(15), size=len(units)),
    index=units, columns=inds,
)
shocks = pd.DataFrame(
    rng.normal(size=(len(times), 15)),
    index=times, columns=inds,
)

rows = []
tau = 0.30
for i in units:
    for t in times:
        b = float((shares.loc[i] * shocks.loc[t]).sum())
        x = b + rng.normal(scale=0.1)
        y = tau * x + rng.normal(scale=0.1)
        rows.append({'u': i, 't': t, 'y': y, 'x': x})
df = pd.DataFrame(rows)

res = sp.shift_share_political_panel(
    df, unit='u', time='t', outcome='y', endog='x',
    shares=shares, shocks=shocks, cluster='shock',
)
print(res.summary())
```

Expected output on this DGP: estimate ≈ 0.296, shock-clustered
SE ≈ 0.009, per-period event-study stable around 0.3, the top-5
industries sum to ~95% of Rotemberg weight.

## 6. Pretrend / placebo checks

Because the per-period table `res.per_period` gives one estimate per
year, you can feed it straight into the event-study plotting helpers
or write your own pretrend Wald test:

```python
pre = res.per_period[res.per_period['time'] < treatment_year]
wald = (pre['estimate'] / pre['se']).pow(2).sum()
import scipy.stats as stats
p = 1 - stats.chi2.cdf(wald, df=len(pre))
print(f'Joint pretrend p-value: {p:.3f}')
```

## 7. Common pitfalls

- **Mis-aligned industry sets.**  If `shares.columns` and
  `shocks.index` don't share any labels the function raises.  When
  they only partially overlap the function silently intersects — use
  `res.n_industries` to confirm the size of the intersection.
- **Very-weak first stage.**  Check `res.diagnostics['first_stage_F']`;
  the shock-cluster variance estimator blows up when the FE-demeaned
  instrument is near-zero.
- **Share balance.**  A significant share-balance F on a pre-treatment
  covariate is a warning that the shares encode latent unit
  characteristics — consider adding the offending variable to
  `covariates=` and re-running.

## 8. References

- `park2026shift` — Park, P. K. (2026).
  *Shift-Share Designs in Political Science.*  arXiv preprint, arXiv:2603.00135.
- Adão, R., Kolesár, M. & Morales, E. (2019).
  *Shift-Share Designs: Theory and Inference.*  QJE 134(4).
- Borusyak, K., Hull, P. & Jaravel, X. (2022).
  *Quasi-Experimental Shift-Share Research Designs.*  ReStud 89.

<!-- AGENT-BLOCK-START: bartik -->

## For Agents

**Pre-conditions**
- pre-period shares are pre-determined (measured strictly before the outcome window)
- shocks are as-good-as-random conditional on unit-level controls
- ≥ 50 regions for AKM shift-share SE to be well-sized
- enough industries / groups (n_shares × avg_share_concentration not too concentrated)

**Identifying assumptions**
- Exogeneity of shocks conditional on pre-period exposure structure (Borusyak-Hull-Jaravel)
- Shock-level IV: shocks are independent of region-level unobserved trends
- Asymptotic framework: many shocks (L → ∞) — check via sp.ssaggregate Herfindahl
- First-stage relevance: Bartik predicts local exposure

**Failure modes → recovery**

| Symptom | Exception | Remedy | Try next |
| --- | --- | --- | --- |
| Herfindahl of shares too concentrated (one industry dominates) | `statspai.AssumptionWarning` | Shift-share SE unreliable — use Adão-Kolesár-Morales shock-level SE via sp.shift_share_se. | `sp.shift_share_se` |
| First-stage F < 10 | `statspai.AssumptionWarning` | Shares don't predict exposure enough — report weak-IV-robust CI (sp.anderson_rubin_ci). | `sp.anderson_rubin_ci` |
| Shocks correlate with pre-trends | `statspai.AssumptionViolation` | Shock exogeneity fails — drop the violating shock dimension or add trend controls. |  |

**Alternatives (ranked)**
- `sp.iv`
- `sp.shift_share_se`
- `sp.shift_share_political`
- `sp.shift_share_political_panel`

**Typical minimum N**: 100

<!-- AGENT-BLOCK-END -->
