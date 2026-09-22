# Synthetic Controls for Experimental Design

> A planning heuristic in the spirit of synthetic-control experimental
> design. It is **not** the Abadie & Zhao design [@abadie2025synthetic],
> which chooses treated units and weights jointly by mixed-integer
> programming; see the note at the end of section 1.

## 1. The flipped workflow

Classical synthetic control answers: "I already have treated unit *A* —
build a reweighted average of donors that approximates *A* in the
pre-period, then impute *A*'s post-period counterfactual."

**Experimental design** flips this: you have a pool of candidates and a
budget `k`, and you want to decide *which* `k` units to treat before the
experiment starts.

`sp.synth_experimental_design` (`method="loo_sc_fit_ranking"`) ranks the
candidates by how well each can be reproduced by a synthetic control
built from the other units in the pre-period, and selects the `k` with
the smallest pre-period MSPE (or RMSE). Units that are easy to
reproduce give counterfactuals that rely less on extrapolation.
`expected_variance` is the **sum of the selected units' pre-period
MSPEs**, a heuristic score for comparing assignments. It is not the
variance of an ATT estimator and does not translate into a confidence
interval width.

The design in Abadie & Zhao [@abadie2025synthetic] solves a different
problem: it targets population-level predictor means with jointly chosen
treated and control weights (the authors' code solves a mixed-integer
program). Use their code when that design is what you need.

## 2. API

```python
import statspai as sp

res = sp.synth_experimental_design(
    data=df,              # long-format panel
    unit='unit',
    time='time',
    outcome='y',
    k=5,                  # budget: treat 5 units
    pre_period=(0, 19),   # closed interval, pre-treatment periods
    candidates=None,      # default: all units are candidates
    donors=None,          # default: non-candidates; leave-one-out fallback
    risk='mspe',          # 'mspe' or 'rmse'
    concentration_weight=0.0,  # penalise Herfindahl weight concentration
    penalization=0.0,     # simplex-solver ridge penalty
    n_random=500,         # Monte-Carlo sample for the random-assignment baseline
    random_state=0,
)
```

Returns a `SynthExperimentalDesignResult` with

- `selected` — the `k` recommended units
- `ranking` — DataFrame with per-candidate risk scores
- `weights` — per-candidate donor weight vectors (for audit)
- `expected_variance`, `baseline_variance` — sum-MSPE under the
  chosen vs random assignment
- `summary()` — human-readable report

## 3. Recipe on a synthetic panel

```python
import numpy as np, pandas as pd, statspai as sp

rng = np.random.default_rng(0)
n_units, n_periods = 30, 20
F = rng.normal(size=(n_periods, 3))
L = rng.normal(size=(n_units, 3))
Y = L @ F.T + 0.1 * rng.normal(size=(n_units, n_periods))

df = pd.DataFrame([
    {'unit': i, 'time': t, 'y': Y[i, t]}
    for i in range(n_units) for t in range(n_periods)
])

res = sp.synth_experimental_design(
    df, unit='unit', time='time', outcome='y',
    k=5, pre_period=(0, 19), random_state=0, n_random=200,
)
print(res.summary())
```

On this panel the summed pre-period MSPE of the selected units is 96%
lower than that of a random choice of `k` units (0.017 vs 0.480): the
selected units are the ones a synthetic control reproduces best.

## 4. When to use this vs `sp.synth`

| Step                          | Function                       |
|-------------------------------|--------------------------------|
| Deciding which units to treat | `sp.synth_experimental_design` |
| Post-treatment counterfactual | `sp.synth(method='classic')`   |
| Inference on the ATT          | `sp.scpi` / `sp.sdid`          |
| Cross-estimator robustness    | `sp.synth_compare`             |

The two are **sequential**: run `synth_experimental_design` at the
planning stage, then let the experiment run and hand the result to the
regular `sp.synth` pipeline.

## 5. Common pitfalls

- **Panel must be balanced** inside `pre_period`.  The function raises
  if any (unit, time) cell is NaN.
- Setting `candidates` equal to all units triggers the leave-one-out
  fallback — each candidate's donor pool becomes the other `n - 1`
  units.  This is fine but inflates computation.
- **`concentration_weight > 0`** adds a Herfindahl penalty to avoid
  selecting units whose SC fit depends on a single donor. There is no
  published default for it; choose it by checking how the selection
  changes over a small grid.

## 6. References

- [@abadie2025synthetic] — the Abadie & Zhao experimental-design paper
  (a different design; see section 1).
- [@abadie2021synthetic] — Abadie (2021), synthetic controls: feasibility,
  data requirements and methodological aspects.

<!-- AGENT-BLOCK-START: synth -->

## For Agents

**Pre-conditions**
- panel data in long form (unit × time × outcome)
- single treated unit (classic) or a treatment-timing column (staggered)
- ≥ 10 donor (untreated) units with similar pre-treatment trajectories
- ≥ 10 pre-treatment periods (fewer → large weight on any one year)

**Identifying assumptions**
- Treatment effect on the treated is identified by the counterfactual implicit in the donor weights
- No spillover from treated unit to donors (SUTVA)
- Donor pool contains units whose outcomes plausibly track the treated counterfactual
- Pre-treatment fit (RMSPE) is small relative to post-treatment effect for placebo inference

**Failure modes → recovery**

| Symptom | Exception | Remedy | Try next |
| --- | --- | --- | --- |
| Pre-treatment RMSPE > post-treatment effect | `AssumptionWarning` | Poor pre-fit — switch to method='demeaned'/'augmented' or enlarge donor pool. | `sp.synth` |
| Placebo p-value ≥ 0.1 despite visible gap | `AssumptionWarning` | Use inference='conformal' (valid under weak assumptions) or report ranked placebo statistic. | `sp.synth` |
| All weight concentrated on one donor | `AssumptionWarning` | Interpolation bias risk — check method='elastic_net' or augmented SCM. | `sp.synth` |
| Treated unit outside donor convex hull | `IdentificationFailure` | Extrapolation needed — use method='unconstrained' or 'augmented'. | `sp.synth` |

**Alternatives (ranked)**
- `sp.sdid`
- `sp.did`
- `sp.matrix_completion`
- `sp.causal_impact`

**Typical minimum N**: 10

<!-- AGENT-BLOCK-END -->
