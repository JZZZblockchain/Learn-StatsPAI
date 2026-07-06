# target_trial

> 📂 所属分类:07 · 健康与流行病学方法 (Health & Epidemiology)

Target Trial Emulation (``sp.target_trial``).

JAMA 2022 framework — the unifying language for causal inference from
observational data. Use to formalize the target trial before analysis,
then delegate estimation to ``sp.msm`` / ``sp.tmle`` / ``sp.ltmle``.

Quick start
-----------
>>> import statspai as sp
>>> proto = sp.target_trial.protocol(
...     eligibility="age >= 50 and diabetic == 1",
...     treatment_strategies=["statin at t0", "no statin"],
...     assignment="observational emulation",
...     time_zero="date of diabetes diagnosis",
...     followup_end="min(death, loss, 5y)",
...     outcome="incident MI",
...     causal_contrast="per-protocol",
...     analysis_plan="clone-censor-weight + pooled logistic + IPCW",
...     baseline_covariates=["age", "sex", "bmi", "ldl"],
... )
>>> print(proto.summary())

**5 个公共函数**

### `sp.CloneCensorWeightResult()`

**Cloned, censored and IP-of-censoring-weighted target-trial data.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cloned_data` | `string` | ✓ |  | cloned_data parameter (pd.DataFrame). |
| `n_clones` | `integer` | ✓ |  | Number of clones. |
| `n_originals` | `integer` | ✓ |  | Number of originals. |
| `strategies` | `array[string]` | ✓ |  | strategies parameter (list[str]). |
| `weights_summary` | `object` | ✓ |  | weights_summary parameter (dict). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CloneCensorWeightResult(cloned_data="value", strategies=["a", "b"], n_originals=1.0, n_clones=1.0)
print(result.summary())
```

---
### `sp.TargetTrialProtocol()`

**Formal 7-component target trial protocol.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `analysis_plan` | `string` | ✓ |  | Which estimator will recover the target estimand (e.g. ``"IPW + Cox"``, ``"g-formula + pooled logistic"``). |
| `assignment` | `string` | ✓ |  | "randomization" (for RCT) or "observational emulation" (conditional exchangeability assumed given baseline covariates). |
| `baseline_covariates` | `array[string]` |  | `None` | Covariates measured at or before time zero that render treatment assignment conditionally exchangeable. |
| `causal_contrast` | `string` | ✓ |  | One of ``"ITT"``, ``"per-protocol"``, ``"as-treated"``, ``"observational-analogue"``. |
| `eligibility` | `array[string]` | ✓ |  | Entry criteria at time zero. May be a SQL-like string filter, a list of human-readable conditions, or a predicate that takes a DataFrame row and returns bool. |
| `followup_end` | `string` | ✓ |  | Administrative censoring rule (e.g. ``"min(event, loss, 2026-01-01)"``). |
| `notes` | `string` |  | `''` | Free-form notes (e.g. known sources of confounding). |
| `outcome` | `string` | ✓ |  | Primary outcome definition. |
| `time_varying_covariates` | `array[string]` |  | `None` | Post-baseline covariates affected by prior treatment; trigger g-methods (MSM / parametric g-formula / LTMLE). |
| `time_zero` | `string` | ✓ |  | Explicit rule defining time zero -- usually the moment of eligibility + treatment assignment alignment. This is the single most important field for preventing immortal time bias. |
| `treatment_strategies` | `array[string]` | ✓ |  | Named arms being contrasted, e.g. ``["initiate statin at t0", "no statin"]``. At least two strategies required. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.TargetTrialProtocol(formula="lwage ~ x1 + x2", eligibility=["a", "b"], treatment_strategies=["a", "b"], assignment="value", time_zero="value", followup_end="value", outcome="value", causal_contrast="value", analysis_plan="value")
print(result.summary())
```

---
### `sp.TargetTrialResult()`

**Result of target trial emulation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ci` | `array[string]` | ✓ |  | ci parameter (tuple[float, float]). |
> 📝 *ci 参数（浮点数二元组）。*
| `estimate` | `number` | ✓ |  | estimate parameter (float). |
> 📝 *estimate 参数（浮点数）。*
| `method` | `string` | ✓ |  | Estimator or algorithm variant to use. |
| `n_eligible` | `integer` | ✓ |  | Number of eligible. |
| `n_excluded_immortal` | `integer` | ✓ |  | Number of excluded immortal. |
| `protocol` | `string` | ✓ |  | protocol parameter (TargetTrialProtocol). |
| `se` | `number` | ✓ |  | se parameter (float). |
> 📝 *se 参数（浮点数）。*
| `weights` | `string` | ✓ |  | Observation weights. |
> 📝 *观测权重。*

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.TargetTrialResult(protocol="value", estimate=1.0, se=1.0, ci=["a", "b"], n_eligible=1.0, n_excluded_immortal=1.0, weights="value", method="value")
print(result.summary())
```

---
### `sp.clone_censor_weight()`

**Clone-Censor-Weight (CCW) for sustained-treatment target trials. Clones each subject per strategy, artificially censors on deviation, and re-weights via IPCW.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `censor_covariates` | `array[string]` |  |  | censor_covariates parameter (list). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `id_col` | `string` | ✓ |  | Column name for id. |
| `stabilize` | `boolean` |  | `True` | stabilize parameter (bool). |
| `strategies` | `object` | ✓ |  | strategies parameter (dict[str, callable]). |
| `time_col` | `string` | ✓ |  | Column name for time. |
| `treatment_col` | `string` | ✓ |  | Treatment variable column name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.clone_censor_weight(data=df, id_col="value", time_col="value", treatment_col="value")
print(result.summary())
```

> 📁 See also: `docs/guides/g_methods_ph.md`

---
### `sp.immortal_time_check()`

**Flag subjects whose follow-up begins *before* treatment**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `eligibility_time_col` | `string` | ✓ |  | The protocol's defined time zero. |
| `id_col` | `string` | ✓ |  | Column name for id. |
| `time_col` | `string` | ✓ |  | Follow-up time column. |
| `treatment_start_col` | `string` | ✓ |  | Time of treatment initiation (NaN / ``-inf`` if never treated). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.immortal_time_check(data=df, id_col="value", time_col="value", treatment_start_col="value", eligibility_time_col="value")
print(result.summary())
```

---
