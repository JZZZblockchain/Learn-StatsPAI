# plots

> 📂 所属分类:09 · 结果导出与可视化 (Output & Visualization)

Visualization module for StatsPAI.

Provides publication-quality academic plots:
- binscatter: Binned scatter plots with residualization (Cattaneo et al. 2024)
- coefplot: Coefficient comparison forest plots
- event_study_plot: DID event study (via CausalResult)
- rdplot: RD visualization (via rd module)
- marginsplot: Marginal effects (via postestimation)
- interactive: Interactive plot editor with data protection

**8 个公共函数**

### `sp.binscatter()`

**Binned scatter plot with optional residualization.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `absorb` | `array[string]` |  |  | Fixed-effect variables to absorb (demeaned within groups) before binning. More efficient than including as dummies in ``controls``. |
| `ax` | `string` |  |  | Axes to draw on. Creates new figure if None. |
| `by` | `string` |  |  | Grouping variable -- produces separate series on the same plot (e.g., ``by='female'`` overlays male and female). |
| `ci` | `boolean` |  | `False` | Show pointwise confidence intervals within each bin. |
| `ci_level` | `number` |  | `0.95` | Confidence level for CIs. |
| `colors` | `array[string]` |  |  | Colors for each ``by`` group. |
| `controls` | `array[string]` |  |  | Control variables to partial out from both Y and X before binning. Uses OLS residualization. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `figsize` | `array[string]` |  | `[8, 6]` | figsize parameter (Tuple[float, float]). |
| `fit` | `string` |  | `'linear'` | Overlay fit line: ``'linear'``, ``'quadratic'``, ``'cubic'``, ``'poly4'``, or ``'none'``. |
| `fit_on_raw` | `boolean` |  | `False` | If True, fit the overlay line on the raw (residualized) micro data, not the bin means. More accurate for nonlinear fits. |
| `legend` | `boolean` |  | `True` | legend parameter (bool). |
| `line_kw` | `object` |  |  | Extra kwargs for ``ax.plot()`` (the fit line). |
| `markers` | `array[string]` |  |  | Marker styles for each ``by`` group. |
| `n_bins` | `integer` |  |  | Number of bins. Default: min(20, ceil(n^(1/3))) following the IMSE-optimal rate from Cattaneo et al. (2024). |
| `quantiles` | `boolean` |  | `True` | If True, bins are quantile-spaced (equal number of obs per bin). If False, bins are evenly spaced on the X-axis. |
| `scatter_kw` | `object` |  |  | Extra kwargs for ``ax.scatter()``. |
| `title` | `string` |  |  | title parameter (Optional[str]). |
| `weights` | `string` |  |  | Analytic weight variable. |
| `x` | `string` | ✓ |  | Running variable (X-axis). |
| `x_label` | `string` |  |  | x_label parameter (Optional[str]). |
| `y` | `string` | ✓ |  | Outcome variable (Y-axis). |
| `y_label` | `string` |  |  | y_label parameter (Optional[str]). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.binscatter(y="outcome", x=["treatment", "covariate1", "covariate2"], data=df)
print(result.summary())
```

---
### `sp.counterfactual_data()`

**Normalise a fitted result into a tidy counterfactual frame.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `result` | `string` | ✓ |  | A StatsPAI result carrying an observed-vs-counterfactual time series: a ``sp.causal_impact`` result, any ``sp.synth`` family result, or an ``sp.its`` ``ITSResult``. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.counterfactual_data(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`

---
### `sp.counterfactual_plot()`

**Plot observed vs counterfactual with an uncertainty band.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ax` | `string` |  |  | Draw the trajectory panel into this axis instead of a new figure. When given, the effect panel is suppressed (single-axis mode). |
| `bands` | `boolean` |  | `True` | Shade the counterfactual / effect uncertainty bands when available. |
| `figsize` | `array[string]` |  | `[10.0, 7.0]` | Figure size when a new figure is created. |
| `result` | `string` | ✓ |  | Any result supported by :func:`counterfactual_data`. |
| `show_effect` | `boolean` |  | `True` | Add the lower pointwise-effect panel. |
| `title` | `string` |  |  | Figure title. Defaults to the result's method. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.counterfactual_plot(result="value")
print(result.summary())
```

> 📁 See also: `docs/guides/unified_quasi_experiments.md`

---
### `sp.get_code()`

**Get reproducible code for all interactive edits made to a figure.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `fig` | `string` | ✓ |  | fig parameter. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.get_code(fig="value")
print(result.summary())
```

---
### `sp.interactive()`

**Open an interactive editor for a matplotlib figure.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `fig` | `string` | ✓ |  | The figure to edit. Typically from ``result.plot()`` or ``sp.binscatter()``. |
| `protect_data` | `boolean` |  | `True` | Lock data-representing elements (scatter points, regression lines, confidence intervals) from modification. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.interactive(fig="value")
print(result.summary())
```

> 📁 See also: `docs/guides/migration-from-r.md`

---
### `sp.list_themes()`

**List all available themes grouped by source.**

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.list_themes()
print(result.summary())
```

---
### `sp.set_theme()`

**Set global matplotlib theme for publication-quality plots.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `font_scale` | `number` |  | `1.0` | Scale factor for all font sizes. |
| `name` | `string` |  | `'academic'` | Theme name. Use ``list_themes()`` to see all available options. ``'default'`` resets to matplotlib defaults. |
| `palette` | `string` |  |  | Color palette name. Defaults to matching the theme. Only applies to StatsPAI themes. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.set_theme()
print(result.summary())
```

---
### `sp.use_chinese()`

**One-line fix for Chinese text rendering in matplotlib.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `style` | `string` |  | `'auto'` | - ``'auto'``: auto-detect the best available Chinese font - ``'serif'``: prefer serif fonts ( Songti SC, SimSun) - ``'sans'``: prefer sans-serif fonts ( PingFang, SimHei) - Any specific font name, e.g. ``'Songti SC'``, ``'SimHei'`` |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.use_chinese()
print(result.summary())
```

---
