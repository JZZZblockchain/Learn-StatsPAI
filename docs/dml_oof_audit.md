# DML OOF audit contract

StatsPAI can retain the predictions, folds, score rows, and training provenance
used by an unweighted binary-treatment IRM ATE fit. This path is intended for
auditing a fitted estimator. It does not change the estimand or provide a test
of causal identification.

## Retaining an internal fit

This complete synthetic example retains three repetitions:

```python
import numpy as np
import pandas as pd
import statspai as sp

rng = np.random.default_rng(42)
x = rng.normal(size=200)
d = np.tile([0, 1], 100)
df = pd.DataFrame({"x": x, "d": d, "y": 2 * d + x + rng.normal(size=200)})
result = sp.dml(
    df, y="y", treat="d", covariates=["x"], model="irm",
    ml_g="linear", ml_m="logistic", n_folds=2, n_rep=3,
    store_oof=True, observation_ids=[f"unit:{i}" for i in range(len(df))],
)
bundle = result.get_oof()
assert len(bundle.to_frame()) == 600
assert len(result.get_residuals(rep=0)) == 200
assert len(bundle.score_concentration()) == 3
```

Pass `store_oof=True` and, when stable row identifiers are available, provide
them through `observation_ids`:

```python
result = estimator.fit(store_oof=True, observation_ids=row_ids)
bundle = result.get_oof()
```

The returned `OOFBundle` is a defensive copy. Its prediction arrays have shape
`(n_rep, n_obs)`, its score arrays have the same repeat-major layout, and
`bundle.to_frame()` returns one row per repeat and observation. The bundle
records each outer fold's test rows, outer-training rows, nuisance-training
rows, preprocessing scope, and provenance origin. Internal retained fits use
the origin `statspai_internal`.

The feature is opt-in. A fit without `store_oof=True` keeps the historical
result behavior and `result.get_oof()` raises a stable unavailable error.

The public estimator parameters are described in `sp.describe_function("dml")`
and its generated schema. `OOFPredictions` and `OOFBundle` are factory-only
value objects, explicitly excluded from the agent's callable estimator catalog;
construct them through `from_arrays` or `from_json`. The individual-level
controls are Python-only and are rejected by generic agent payload handling.
The package's ordinary result JSON does not include retained records.

Internal retained fits require at least 10 training observations in each
treatment arm of every outer fold and raise `DataInsufficient` otherwise.
Explicit internal fold assignments require a single repeat. PLR, PLIV, IIVM,
ATTE, weighted fits, and normalized IPW do not support OOF retention yet and
fail explicitly if requested. Their ordinary fitting paths remain available,
including the current upstream three-nuisance IV-type PLR implementation.

## Scoring external predictions

Create a versioned `OOFPredictions` object with the observed rows, `g0`, `g1`,
raw propensity predictions, fold assignments, declared training records, and
source metadata. Then pass that object in memory:

```python
result = estimator.fit(
    external_predictions=predictions,
    store_oof=True,
    observation_ids=row_ids,
)
bundle = result.get_oof()
```

StatsPAI validates row count and order, observed `Y`, `D`, and `X`, covariate
names, repeat and fold counts, outer-training scopes, nuisance-training scopes,
and the three prediction hashes before scoring. External predictions go
directly to the common IRM scorer. The nuisance learners, fold generator, and
internal subgroup fallback are not called. The bundle identifies this route as
`statspai_irm_external_predictions`; external fit records have no StatsPAI fit
seed or subgroup-fallback count.

The three `OOFPredictions.hashes` cover separate partitions:

- `data`: row IDs, covariate names, and observed `Y`, `D`, and `X`;
- `predictions_and_folds`: `g0`, `g1`, `ps_raw`, and `fold_ids`;
- `training_source`: training records and source metadata.

`OOFBundle.hash` additionally covers the prediction snapshot, scored arrays,
input-row mapping, repeat aggregation, and scoring metadata. Readers reject
unknown schema versions, malformed digests, duplicate JSON keys, and any hash
mismatch. The schemas remain `statspai.dml.predictions/1` and
`statspai.dml.oof/1`.

## Score concentration

Call `bundle.score_concentration()` to obtain one JSON-ready record per repeat.
The method reads the centered score `phi = bundle.psi[rep]`. For squared-score
shares `w_i = phi_i**2 / sum_j(phi_j**2)`, it reports:

- `cmax`: `max_i(w_i)`;
- `z_c`: `n_obs * cmax / (2 * log(n_obs))`, using the natural logarithm;
- `top_share`: the sum of the largest `ceil(top_fraction * n_obs)` shares;
- `h`: `sum_i(w_i**2)`, the score-share Herfindahl concentration;
- `effective_score_count`: `1 / h`.

`top_fraction` defaults to `0.01` and must be a finite scalar in `(0, 1]`.
Every returned mapping has these fields in a stable order:

```text
rep, status, failure_reason, n_obs, top_fraction, top_count,
cmax, z_c, top_share, h, effective_score_count
```

Successful rows use `status="ok"` and `failure_reason=None`. A nonfinite score,
zero squared-score mass, overflowed mass, too few score rows, or nonfinite
derived statistic produces `status="diagnostic_unavailable"`, a specific
`failure_reason`, and `None` for all five diagnostic values. An unavailable
diagnostic is an explicit failed state; downstream alarm policies must not
silently treat it as a non-alarm.

## IRM score and variance convention

For clipped propensity `m`, StatsPAI stores the AIPW pseudo-outcome

```text
psi_b = g1 - g0 + D * (Y - g1) / m - (1 - D) * (Y - g0) / (1 - m)
```

For each repeat, `theta = mean(psi_b)`, `psi = psi_b - theta`, and
`se = std(psi_b, ddof=0) / sqrt(n_obs)`. This is also the DoubleML linear-score
calculation with `psi_a = -1`,
`theta = -mean(psi_b) / mean(psi_a)`, and
`se**2 = mean((psi_a * theta + psi_b)**2) /
(mean(psi_a)**2 * n_obs)`.

The focused parity fixture checks every `psi_b` row and both scalar outputs
against a transparent formula and an independently written DoubleML-style
moment calculation. This establishes conformity to the tested score contract;
it is not evidence for universal statistical validity.

Full bundle JSON contains individual row IDs, outcomes, treatments,
covariates, predictions, and scores. Store and share it according to the data
policy that applies to the source data. A public replication artifact should
normally retain aggregate diagnostics and hashes, with full arrays only for a
synthetic fixture.
