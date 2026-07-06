# spatial

> 📂 所属分类:05 · 经济计量方法 (Econometric Methods)

Spatial econometrics — StatsPAI's answer to R's ``spatialreg + spdep + mgwr``
and Python's PySAL.

Three layers, flat-imported for convenience:

Weights
-------
``W``, ``queen_weights``, ``rook_weights``, ``knn_weights``,
``distance_band``, ``kernel_weights``, ``block_weights``.

Exploratory spatial data analysis (ESDA)
---------------------------------------
``moran``, ``moran_local``, ``geary``, ``getis_ord_g``, ``getis_ord_local``,
``join_counts``, ``moran_plot``, ``lisa_cluster_map``.

Regression
----------
- ML estimators: ``sar``, ``sem``, ``sdm``, ``slx``, ``sac``
- Diagnostics: ``lm_tests``, ``moran_residuals``
- Effects: ``impacts`` (LeSage-Pace direct / indirect / total)

All regression estimators accept a :class:`W` object, a ``scipy.sparse``
matrix, or an ``(n, n)`` ndarray for the weights argument.

Examples
--------
>>> import statspai as sp
>>> w = sp.knn_weights(coords, k=6); w.transform = "R"
>>> moran = sp.moran(df["y"], w)
>>> result = sp.sar(w, data=df, formula='y ~ x1 + x2')
>>> eff = sp.impacts(result)
>>> lms = sp.lm_tests("y ~ x1 + x2", df, w)

**35 个公共函数**

### `sp.SpatialDiDResult()`

**Result object for :func:`spatial_did`.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `ci_direct` | `array[string]` | ✓ |  | ci_direct parameter (tuple). |
| `ci_spillover` | `array[string]` | ✓ |  | ci_spillover parameter (tuple). |
| `ci_total` | `array[string]` |  | `[nan, nan]` | ci_total parameter (tuple). |
| `coefficients` | `string` | ✓ |  | coefficients parameter (pd.DataFrame). |
| `data_info` | `object` |  | `None` | data_info parameter (Dict[str, Any]). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `direct_effect` | `number` | ✓ |  | direct_effect parameter (float). |
| `model_info` | `object` |  | `None` | model_info parameter (Dict[str, Any]). |
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `pvalue_direct` | `number` | ✓ |  | pvalue_direct parameter (float). |
| `pvalue_spillover` | `number` | ✓ |  | pvalue_spillover parameter (float). |
| `pvalue_total` | `number` |  | `nan` | pvalue_total parameter (float). |
| `se_direct` | `number` | ✓ |  | se_direct parameter (float). |
| `se_spillover` | `number` | ✓ |  | se_spillover parameter (float). |
| `se_total` | `number` |  | `nan` | se_total parameter (float). |
| `se_type` | `string` |  | `'cluster'` | se_type parameter (str). |
| `spillover_effect` | `number` | ✓ |  | spillover_effect parameter (float). |
| `total_effect` | `number` |  | `nan` | total_effect parameter (float). |
| `vcov` | `string` |  |  | Variance-covariance estimator option. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SpatialDiDResult(direct_effect=1.0, spillover_effect=1.0, se_direct=1.0, se_spillover=1.0, ci_direct=["a", "b"], ci_spillover=["a", "b"], pvalue_direct=1.0, pvalue_spillover=1.0, coefficients="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.SpatialIVResult()`

**Container for :func:`spatial_iv` Kelejian-Prucha S2SLS estimates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coefficients` | `string` | ✓ |  | coefficients parameter (pd.DataFrame). |
| `detail` | `object` |  | `None` | Amount of result detail to return. |
> 📝 *返回的结果详细程度。*
| `n_obs` | `integer` | ✓ |  | Number of obs. |
| `rho` | `number` | ✓ |  | rho parameter (float). |
| `rho_se` | `number` | ✓ |  | rho_se parameter (float). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SpatialIVResult(rho=1.0, rho_se=1.0, coefficients="value", n_obs=1.0)
print(result.summary())
```

---
### `sp.SpatialModel()`

**Unified spatial regression estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `model_type` | `string` |  | `'sar'` | model_type parameter (str). |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.SpatialModel(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.W()`

**Spatial weights matrix with CSR-sparse backing.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `id_order` | `array[string]` |  |  | Explicit ordering of observation ids. Defaults to ``sorted(neighbors)``. |
| `neighbors` | `array[string]` | ✓ |  | Mapping observation id -> list of neighbour ids. |
| `weights` | `array[string]` |  |  | Matching weight values. If ``None``, binary (1.0) weights are used. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.W(neighbors=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/gpu_acceleration.md`, `docs/guides/proximal_family.md`

---
### `sp.block_weights()`

**Block (regime) spatial weights -- full connectivity within each group.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `regimes` | `array[string]` | ✓ |  | Length-``n`` array of group labels (any hashable dtype). Units with equal labels become mutual neighbours. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.block_weights(regimes=["a", "b"])
print(result.summary())
```

---
### `sp.distance_band()`

**Distance-band spatial weights -- connect units within a fixed radius.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `binary` | `boolean` |  | `True` | If True all neighbour weights are ``1.0``; if False they are inverse Euclidean distance ``1/d`` (coincident points are dropped via an infinite distance). |
| `coords` | `string` | ✓ |  | ``(n, d)`` array of coordinates. |
| `threshold` | `number` | ✓ |  | Distance band radius. Units within this distance become neighbours. Choose at least the maximum nearest-neighbour distance to avoid islands (units with no neighbours). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.distance_band(coords="value", threshold=1.0)
print(result.summary())
```

---
### `sp.geary()`

**Global Geary's C -- squared-difference measure of spatial autocorrelation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `permutations` | `integer` |  | `999` | Number of random permutations for the pseudo p-value (and the empirical variance / z-score). ``0`` skips the permutation test, in which case ``variance``, ``z_score`` and ``p_norm`` are ``NaN``. |
| `seed` | `integer` |  |  | Seed for the permutation RNG for reproducibility. |
| `w` | `string` | ✓ |  | Spatial weights object; ``w.sparse`` must have non-zero total. |
| `y` | `string` | ✓ |  | Variable of interest, length ``n``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.geary(y="outcome", w="value")
print(result.summary())
```

---
### `sp.getis_ord_g()`

**Global Getis-Ord G -- overall concentration of high (or low) values.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `permutations` | `integer` |  | `999` | Number of random permutations for the pseudo p-value, empirical variance and z-score. ``0`` skips the permutation test. |
| `seed` | `integer` |  |  | Seed for the permutation RNG for reproducibility. |
| `w` | `string` | ✓ |  | Spatial weights object defining the neighbourhood structure. |
| `y` | `string` | ✓ |  | Non-negative variable of interest, length ``n``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.getis_ord_g(y="outcome", w="value")
print(result.summary())
```

---
### `sp.getis_ord_local()`

**Local Getis-Ord Gi / Gi* -- hotspot and coldspot detection.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `permutations` | `integer` |  | `999` | Accepted for API symmetry; the current implementation returns the analytic standardised statistic. |
| `seed` | `integer` |  |  | Seed placeholder for API symmetry. |
| `star` | `boolean` |  | `True` | If True compute Gi* (self-included); otherwise Gi (self-excluded). |
| `w` | `string` | ✓ |  | Spatial weights object; densified internally to an ``n x n`` matrix. |
| `y` | `string` | ✓ |  | Variable of interest, length ``n``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.getis_ord_local(y="outcome", w="value")
print(result.summary())
```

---
### `sp.gwr()`

**Fit Geographically Weighted Regression.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Design matrix WITHOUT constant unless ``add_constant=False``. |
| `add_constant` | `boolean` |  | `True` | Prepend a column of ones to ``X``. |
| `bw` | `number` | ✓ |  | Bandwidth. Interpretation depends on ``fixed``: - ``fixed=True``: metric distance. - ``fixed=False`` (default, "adaptive"): number of nearest neighbours. Non-integer values are rounded up to include the fractional neighbour, consistent with ``mgwr``. |
| `coords` | `string` | ✓ |  | Point coordinates (projected -- use UTM or equivalent; lat/lon will bias distances in most regions). |
| `fixed` | `boolean` |  | `False` | fixed parameter (bool). |
| `kernel` | `string (enum)` |  | `'bisquare'` | Bisquare is mgwr's default. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **kernel** options: `'bisquare'`, `'gaussian'`, `'exponential'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.gwr(y="outcome", coords="value", X="value", bw=1.0)
print(result.summary())
```

---
### `sp.gwr_bandwidth()`

**Select GWR bandwidth via golden-section search.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `add_constant` | `boolean` |  | `True` | add_constant parameter (bool). |
| `bw_max` | `number` |  |  | Override the default search bounds. |
| `bw_min` | `number` |  |  | Override the default search bounds. |
| `coords` | `string` | ✓ |  | coords parameter. |
| `criterion` | `string (enum)` |  | `'AICc'` | Default AICc matches mgwr. |
| `fixed` | `boolean` |  | `False` | If False (default), the bandwidth is a nearest-neighbour count (integer-valued; rounded at each candidate). |
| `kernel` | `string` |  | `'bisquare'` | Kernel function used for weighting or smoothing. |
| `tol` | `number` |  | `0.001` | Numerical convergence tolerance. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

> **criterion** options: `'AICc'`, `'AIC'`, `'BIC'`, `'CV'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.gwr_bandwidth(y="outcome", coords="value", X="value")
print(result.summary())
```

---
### `sp.impacts()`

**Compute direct / indirect / total impacts + simulated SEs.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `n_sim` | `integer` |  | `1000` | Number of Monte-Carlo draws for simulated SEs. |
| `result` | `string` | ✓ |  | Output of ``sp.sar``, ``sp.sdm``, or ``sp.sac``. |
| `seed` | `integer` |  |  | RNG seed. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.impacts(result="value")
print(result.summary())
```

---
### `sp.join_counts()`

**Join-count statistics for a binary spatial variable.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `permutations` | `integer` |  | `999` | Number of random permutations for the BB pseudo p-value. ``0`` skips the test. |
| `seed` | `integer` |  |  | Seed for the permutation RNG for reproducibility. |
| `w` | `string` | ✓ |  | Spatial weights object defining the join structure. |
| `y` | `string` | ✓ |  | Binary variable, values in ``{0, 1}``, length ``n``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.join_counts(y="outcome", w="value")
print(result.summary())
```

---
### `sp.kernel_weights()`

**Kernel (distance-decay) spatial weights from point coordinates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `bandwidth` | `number` | ✓ |  | With ``fixed=True``, the bandwidth distance ``h`` (for the bisquare and triangular kernels, neighbours beyond ``h`` get zero weight; the gaussian kernel has infinite support so all units are included). With ``fixed=False``, the integer number of nearest neighbours that defines the adaptive bandwidth. |
| `coords` | `string` | ✓ |  | ``(n, d)`` array of coordinates. |
| `fixed` | `boolean` |  | `True` | Fixed (True) versus adaptive (False) bandwidth. |
| `kernel` | `string (enum)` |  | `'gaussian'` | Kernel shape. ``gaussian`` ``exp(-u^2/2)``; ``bisquare`` ``(1-u^2)^2`` for ``u<1``; ``triangular`` ``1-u`` for ``u<1``, where ``u = d / bandwidth``. |

> **kernel** options: `'gaussian'`, `'bisquare'`, `'triangular'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.kernel_weights(coords="value", bandwidth=1.0)
print(result.summary())
```

---
### `sp.knn_weights()`

**k-nearest-neighbour spatial weights from point coordinates.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `coords` | `string` | ✓ |  | ``(n, d)`` array of coordinates (typically ``d=2``). |
| `k` | `integer` |  | `5` | Number of nearest neighbours per unit. Must satisfy ``0 < k < n``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.knn_weights(coords="value")
print(result.summary())
```

---
### `sp.lisa_cluster_map()`

**Classify each observation HH/LL/HL/LH/Not significant and colour on a GDF.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter (Optional[Any]). |
| `gdf` | `string` | ✓ |  | gdf parameter. |
| `p_threshold` | `number` |  | `0.05` | p_threshold parameter (float). |
| `w` | `string` | ✓ |  | Weights, spatial weights, or balancing-weight input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lisa_cluster_map(y="outcome", w="value", gdf="value")
print(result.summary())
```

---
### `sp.lm_tests()`

**Anselin (1988) Lagrange multiplier battery.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | ``"y ~ x1 + x2"`` style formula (constant added automatically). |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.lm_tests(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.mgwr()`

**Multiscale GWR via back-fitting.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X` | `string` | ✓ |  | Feature matrix or covariate DataFrame. |
| `add_constant` | `boolean` |  | `True` | add_constant parameter (bool). |
| `bw_init` | `number` |  |  | bw_init parameter (Optional[float]). |
| `coords` | `string` | ✓ |  | coords parameter. |
| `fixed` | `boolean` |  | `False` | fixed parameter (bool). |
| `kernel` | `string` |  | `'bisquare'` | Kernel function used for weighting or smoothing. |
| `max_iter` | `integer` |  | `200` | Maximum number of optimisation iterations. |
| `tol` | `number` |  | `1e-05` | Numerical convergence tolerance. |
> 📝 *数值收敛容差。*
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.mgwr(y="outcome", coords="value", X="value")
print(result.summary())
```

---
### `sp.moran()`

**Global Moran's I -- test for global spatial autocorrelation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `permutations` | `integer` |  | `999` | Number of conditional random permutations used for the pseudo p-value. Set to ``0`` to skip the permutation test and rely on the analytic z-score only. |
| `seed` | `integer` |  |  | Seed for the permutation RNG (``numpy.random.default_rng``) for reproducible pseudo p-values. |
| `two_tailed` | `boolean` |  | `True` | If True the analytic ``p_norm`` is two-tailed; otherwise it is the upper-tail (positive autocorrelation) p-value. |
| `w` | `string` | ✓ |  | Spatial weights object. ``w.sparse`` must be an ``n x n`` matrix whose total sum is non-zero. Row-standardised or binary weights both work. |
| `y` | `string` | ✓ |  | Variable of interest, length ``n`` (one value per spatial unit). Flattened to 1-D internally. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.moran(y="outcome", w="value")
print(result.summary())
```

---
### `sp.moran_local()`

**Local Moran's I (LISA) -- per-location spatial association.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `permutations` | `integer` |  | `999` | Number of conditional permutations for the per-location pseudo p-values. ``0`` skips the permutation test. |
| `seed` | `integer` |  |  | Seed for the permutation RNG for reproducibility. |
| `w` | `string` | ✓ |  | Spatial weights object; ``w.sparse`` is the ``n x n`` weights matrix. |
| `y` | `string` | ✓ |  | Variable of interest, length ``n``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.moran_local(y="outcome", w="value")
print(result.summary())
```

---
### `sp.moran_plot()`

**Moran scatter: z vs spatial lag Wz. Slope of OLS line = Moran's I.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | ax parameter (Optional[Any]). |
| `w` | `string` | ✓ |  | Weights, spatial weights, or balancing-weight input for this estimator. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.moran_plot(y="outcome", w="value")
print(result.summary())
```

---
### `sp.moran_residuals()`

**Moran's I applied to regression residuals (quick LM-err companion).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `residuals` | `string` | ✓ |  | residuals parameter (np.ndarray). |
> 📝 *residuals 参数（np.ndarray）。*
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.moran_residuals(residuals="value", W="value")
print(result.summary())
```

---
### `sp.queen_weights()`

**Queen-contiguity spatial weights from polygon geometries.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gdf` | `string` | ✓ |  | Layer of polygon geometries (accessed via ``gdf.geometry`` and the spatial index ``gdf.sindex``). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.queen_weights(gdf="value")
print(result.summary())
```

---
### `sp.rook_weights()`

**Rook-contiguity spatial weights from polygon geometries.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gdf` | `string` | ✓ |  | Layer of polygon geometries. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.rook_weights(gdf="value")
print(result.summary())
```

---
### `sp.sac()`

**SAC / SARAR: combined spatial lag + spatial error model.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sac(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.sar()`

**Spatial Autoregressive (Lag) Model: Y = rhoWY + Xbeta + epsilon via ML.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | (n,n) spatial weights matrix |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | 'y ~ x1 + x2' |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sar(data=df, W="value")
print(result.summary())
```

---
### `sp.sar_gmm()`

**Kelejian-Prucha (1998) 2SLS for SAR with spatial-lag instruments.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `robust` | `string` |  |  | Robust standard-error or covariance estimator option. |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |
| `w_lags` | `integer` |  | `1` | w_lags parameter (int). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sar_gmm(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.sarar_gmm()`

**Combined GMM: Kelejian-Prucha SAR 2SLS then SEM GMM on residuals.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `robust` | `string` |  |  | Robust standard-error or covariance estimator option. |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sarar_gmm(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.sdm()`

**Spatial Durbin Model: Y = rhoWY + Xbeta + WXtheta + epsilon with direct/indirect effects. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | (n,n) spatial weights matrix |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sdm(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.sem()`

**Spatial Error Model: Y = Xbeta + u, u = lambdaWu + epsilon via ML.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | (n,n) spatial weights matrix |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sem(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

> 📁 See also: `docs/guides/mediation.md`

---
### `sp.sem_gmm()`

**Kelejian-Prucha (1999) GMM for the spatial-error parameter lambda. Validation: certified parity evidence.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `robust` | `string` |  |  | When ``"het"``, the final beta covariance uses the heteroscedasticity- robust sandwich (Arraiz et al. 2010 / ``spreg.GM_Error_Het``). |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.sem_gmm(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.slx()`

**Spatial Lag of X (SLX) model: ``Y = Xbeta + WXtheta + epsilon``.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Covariates, proxy variables, or weights used by this estimator. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `formula` | `string` | ✓ |  | Model formula using patsy/R-style syntax. |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.slx(formula="lwage ~ x1 + x2", data=df, W="value")
print(result.summary())
```

---
### `sp.spatial_did()`

**Spatial DiD with direct and spillover treatment effects.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Spatial weights matrix over units. If a StatsPAI ``W`` object carries an ``id_order``, that order is respected. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals. |
| `cluster` | `string` |  |  | Cluster variable for ``se_type='cluster'``. Defaults to ``unit``. |
| `conley_cutoff` | `number` |  |  | Spatial cutoff for Conley-HAC standard errors. |
| `conley_kernel` | `string (enum)` |  | `'bartlett'` | conley_kernel parameter (str). |
| `coords` | `array[string]` |  |  | Convenience pair ``(lat, lon)`` in degrees. |
| `covariates` | `array[string]` |  |  | Additional controls included after absorbing unit and time effects. |
| `data` | `string` | ✓ |  | Long panel with one row per unit-period. |
| `distance_matrix` | `string` |  |  | Unit-by-unit distances in the same units as ``conley_cutoff``. |
| `event_base` | `integer` |  | `-1` | Omitted relative-time period. |
| `event_study` | `boolean` |  | `False` | Estimate direct and spillover event-study paths by relative time. |
| `event_window` | `array[string]` |  |  | Inclusive event-time window. Defaults to observed support capped at [-5, 5] when ``event_study=True``. |
| `lat` | `string` |  |  | Latitude/longitude columns in degrees. |
| `lon` | `string` |  |  | Latitude/longitude columns in degrees. |
| `normalize_W` | `boolean` |  | `True` | Row-normalise weights before constructing ``WD``. |
| `se_type` | `string (enum)` |  | `'cluster'` | Covariance estimator. ``conley`` uses spatial-HAC dependence within each period and requires ``conley_cutoff`` plus coordinates or a unit-level distance matrix. |
| `time` | `string` | ✓ |  | Outcome, treatment, unit-id, and time-id columns. ``treat`` may be binary or a continuous exposure intensity; the spatial lag uses the same scale. |
| `treat` | `string` | ✓ |  | Outcome, treatment, unit-id, and time-id columns. ``treat`` may be binary or a continuous exposure intensity; the spatial lag uses the same scale. |
| `unit` | `string` | ✓ |  | Outcome, treatment, unit-id, and time-id columns. ``treat`` may be binary or a continuous exposure intensity; the spatial lag uses the same scale. |
| `unit_order` | `array[string]` |  |  | Explicit row/column order of ``W``. |
| `y` | `string` | ✓ |  | Outcome, treatment, unit-id, and time-id columns. ``treat`` may be binary or a continuous exposure intensity; the spatial lag uses the same scale. |

> **conley_kernel** options: `'uniform'`, `'bartlett'`

> **se_type** options: `'cluster'`, `'robust'`, `'conley'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.spatial_did(y="outcome", data=df, treat="value", unit="value", time="value", W="value")
print(result.summary())
```

---
### `sp.spatial_iv()`

**Spatial 2SLS estimator.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | Spatial weights matrix (n_obs x n_obs). Should be row-normalised. |
| `alpha` | `number` |  | `0.05` | Significance level for confidence intervals and tests. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `endog` | `array[string]` | ✓ |  | Names of additional endogenous regressors. |
| `exog` | `array[string]` | ✓ |  | Names of exogenous regressors (included instruments). |
| `include_WY` | `boolean` |  | `True` | If True, include WY as a regressor (spatial autoregressive coefficient rho). |
| `instruments` | `array[string]` |  |  | Extra excluded instruments beyond the spatial lags of X. |
| `y` | `string` | ✓ |  | Outcome variable column name or outcome array. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.spatial_iv(y="outcome", data=df, endog=["a", "b"], exog=["a", "b"], W="value")
print(result.summary())
```

---
### `sp.spatial_panel()`

**Fit a spatial panel model by concentrated ML (Elhorst 2014).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `W` | `string` | ✓ |  | N x N spatial weights matrix aligned with ``sorted(data[entity].unique())``. |
| `data` | `string` | ✓ |  | Long-format panel; must be balanced. |
| `effects` | `string (enum)` |  | `'fe'` | ``"fe"`` = entity FE only. ``"twoways"`` = entity + time demeaning. |
| `entity` | `string` | ✓ |  | Column names identifying entity and time dimensions. |
| `formula` | `string` | ✓ |  | ``"y ~ x1 + x2"``. Constant is dropped (absorbed by the entity FE). |
| `model` | `string (enum)` |  | `'sar'` | Model variant or parameterisation to fit. |
| `row_normalize` | `boolean` |  | `True` | row_normalize parameter (bool). |
| `time` | `string` | ✓ |  | Column names identifying entity and time dimensions. |

> **effects** options: `'fe'`, `'twoways'`

> **model** options: `'sar'`, `'sem'`, `'sdm'`

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.spatial_panel(data=df, entity="value", time="value", W="value")
print(result.summary())
```

---
