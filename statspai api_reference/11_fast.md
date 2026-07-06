# fast

> 📂 所属分类:11 · 其他杂项 (Other)

``statspai.fast`` — performance-instrumentation and native-kernel home.

Contents (v1.8 / Phase 1+):

- :func:`hdfe_bench` — wall-time + correctness regression harness.
- :func:`demean`     — multi-way HDFE within-transform with Aitken
  acceleration, backed by a Rust kernel (NumPy fallback).

The module exposes building blocks that Phase 2+ (PPML / GLM HDFE),
Phase 3 (`sp.within`), and Phase 5 (Polars/Arrow direct) sit on top of.

**5 个公共函数**

### `sp.demean()`

**Return the within-transformed ``x`` and the singleton keep mask. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `drop_singletons` | `boolean` |  | `True` | drop_singletons parameter (bool). |
| `fe` | `string` | ✓ |  | fe parameter (Union[pd.DataFrame, np.ndarray]). |
| `maxiter` | `integer` |  | `10000` | maxiter parameter (int). |
| `solver` | `string` |  | `'map'` | solver parameter (str). |
| `tol` | `number` |  | `1e-08` | Numerical convergence tolerance. |
| `weights` | `string` |  |  | Observation weights. |
| `x` | `string` | ✓ |  | Primary running variable, regressor, or feature input for this estimator. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.demean(x=["treatment", "covariate1", "covariate2"], fe="value")
print(result.summary())
```

> 📁 See also: `docs/guides/gpu_acceleration.md`, `docs/guides/panel_data.md`

---
### `sp.etable()`

**Display a pyfixest-style regression table for StatsPAI results.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.etable()
print(result.summary())
```

> 📁 See also: `docs/guides/exporting-regression-tables.md`, `docs/guides/migration-from-r.md`

---
### `sp.event_study()`

**Traditional OLS event-study with entity and time FEs. Generates relative-time dummies around the treatment date, omits a reference period, and estimates via TWFE + optional clustered SE. Exposed for users who want the classical specification alongside CS / SA / BJS; not robust to staggered-effect heterogeneity -- use sp.sun_abraham for that.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `cluster` | `string` |  |  | Cluster identifier column for clustered standard errors. |
| `covariates` | `array[string]` |  |  | Covariate matrix, DataFrame, or column names. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `ref_period` | `integer` |  | `-1` | Reference relative-time period to omit |
| `time` | `string` | ✓ |  | Time period column. |
> 📝 *时间周期列。*
| `treat_time` | `string` | ✓ |  | First-treatment period column |
| `unit` | `string` | ✓ |  | Unit identifier |
| `window` | `array[string]` |  | `[-4, 4]` | (lead, lag) horizons |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.event_study(y="outcome", data=df, treat_time="value", time="value", unit="value")
print(result.summary())
```

> 📁 See also: `docs/guides/choosing_did_estimator.md`

---
### `sp.feols()`

**Estimate OLS / IV with high-dimensional fixed effects via pyfixest. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Cluster id column for the extended ``vce=`` menu; also a shorthand for one-way ``{"CRV1": cluster}``. |
| `collin_tol` | `number` |  | `1e-06` | Collinearity tolerance. |
| `conley_cutoff` | `number` |  |  | Conley distance cutoff in km for ``vce="conley"``. |
| `conley_lat` | `string` |  |  | Coordinate columns (decimal degrees) for ``vce="conley"``. |
| `conley_lon` | `string` |  |  | Coordinate columns (decimal degrees) for ``vce="conley"``. |
| `data` | `string` | ✓ |  | Input dataset. |
| `fixef_rm` | `string` |  | `'none'` | How to handle singleton fixed effects: ``"none"`` (keep) or ``"singleton"`` (drop). |
| `fml` | `string` | ✓ |  | A pyfixest-style formula. Examples: - ``"Y ~ X1 + X2"`` -- plain OLS - ``"Y ~ X1 \| firm + year"`` -- two-way fixed effects - ``"Y ~ 1 \| firm \| X1 ~ Z1"`` -- IV with fixed effects - ``"Y ~ X1 \| csw0(firm, year)"`` -- multiple estimations |
| `lean` | `boolean` |  | `False` | If True, drop large intermediate arrays to save memory. |
| `seed` | `integer` |  |  | RNG seed for ``vce="wild"``. |
| `ssc` | `string` |  |  | Small-sample correction via ``pyfixest.ssc()``. |
| `vcov` | `object` |  |  | Variance-covariance estimator (``vce=`` is the canonical alias). - ``"iid"`` -- classical - ``"HC1"``, ``"HC2"``, ``"HC3"`` -- heteroskedasticity-robust - ``{"CRV1": "firm"}`` -- cluster-robust - ``{"CRV1": "firm + year"}`` -- two-way clustering - ``vce="CR2"`` / ``"CR3"`` / ``"jackknife"`` (with ``cluster=``) -- Pustejovsky-Tipton bias-reduced cluster-robust on the FE-absorbed within design; matches R ``clubSandwich::vcovCR(plm)``. - ``vce="wild"`` (with ``cluster=``) -- WCR wild cluster bootstrap (Cameron-Gelbach-Miller 2008); validated against Stata ``boottest``. - ``vce="conley"`` (with ``conley_lat=/conley_lon=/conley_cutoff=``) -- Conley spatial HAC (Stata ``acreg`` planar-distance convention). |
| `weights` | `string` |  |  | Column name for regression weights. |
| `wild_reps` | `integer` |  | `999` | Bootstrap replications for ``vce="wild"``. |
| `wild_weight_type` | `string` |  | `'rademacher'` | Wild weight distribution (``"rademacher"``, ``"webb"``, ``"mammen"``). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.feols(formula="lwage ~ x1 + x2", data=df, fml="value")
print(result.summary())
```

> 📁 See also: `docs/guides/economist_mcp_workflow.md`, `docs/guides/economist_mcp_workflow_zh.md`, `docs/guides/gpu_acceleration.md`

---
### `sp.fepois()`

**Estimate Poisson regression with high-dimensional fixed effects via pyfixest. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster` | `string` |  |  | Cluster id column for the extended ``vce=`` menu; also a shorthand for one-way ``{"CRV1": cluster}``. |
| `collin_tol` | `number` |  | `1e-06` | Collinearity tolerance. |
| `conley_cutoff` | `number` |  |  | conley_cutoff parameter (Optional[float]). |
| `conley_lat` | `string` |  |  | conley_lat parameter (Optional[str]). |
| `conley_lon` | `string` |  |  | conley_lon parameter (Optional[str]). |
| `data` | `string` | ✓ |  | Input dataset. |
| `fixef_rm` | `string` |  | `'none'` | Singleton fixed effect handling. |
| `fml` | `string` | ✓ |  | pyfixest formula. E.g. ``"Y ~ X1 \| firm"``. |
| `iwls_maxiter` | `integer` |  | `25` | Max IWLS iterations. |
| `iwls_tol` | `number` |  | `1e-08` | IWLS convergence tolerance. |
| `seed` | `integer` |  |  | RNG seed for sampled (non-enumerated) ``vce="wild"`` draws. |
| `ssc` | `string` |  |  | Small-sample correction. |
| `vcov` | `object` |  |  | Variance-covariance estimator (``vce=`` is the canonical alias). Besides the pyfixest values (``"iid"``, ``"HC1"``, ``{"CRV1": "firm"}``, ...), accepts the extended menu: - ``vce="CR2"`` / ``"CR3"`` / ``"jackknife"`` (with ``cluster=``) -- clubSandwich glm bias-reduced cluster-robust SEs on the FE-as-dummies design; matches R ``clubSandwich::vcovCR(glm)``. - ``vce="wild"`` (with ``cluster=``) -- restricted score wild cluster bootstrap (Kline-Santos 2012) with Stata ``boottest``'s exact studentization; bit-exact vs ``boottest`` in the enumerated regime. |
| `weights` | `string` |  |  | Column name for regression weights (not supported with the extended ``vce=`` menu). |
| `wild_reps` | `integer` |  | `9999` | Replications for ``vce="wild"``. When ``2**G <= wild_reps`` the full Rademacher grid is enumerated (deterministic). |
| `wild_weight_type` | `string` |  | `'rademacher'` | Wild weight distribution (``"rademacher"`` or ``"webb"``). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.fepois(formula="lwage ~ x1 + x2", data=df, fml="value")
print(result.summary())
```

> 📁 See also: `docs/guides/grammar.md`, `docs/guides/migration-from-r.md`, `docs/guides/panel_data.md`

---
