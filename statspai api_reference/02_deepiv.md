# deepiv

> 📂 所属分类:02 · 元学习器与机器学习因果推断 (Meta-Learners & ML Causal)

DeepIV: Deep Learning Instrumental Variables (Hartford et al. 2017).

Uses a two-stage neural network approach:
  Stage 1: Mixture Density Network estimates P(T | Z, X)
  Stage 2: Response network minimises counterfactual loss using
           Monte-Carlo samples from the learned treatment distribution.

References
----------
Hartford, J., Lewis, G., Leyton-Brown, K., & Taddy, M. (2017).
"Deep IV: A Flexible Approach for Counterfactual Prediction."
*Proceedings of the 34th International Conference on Machine Learning (ICML)*. [@hartford2017deep]

**2 个公共函数**

### `sp.DeepIV()`

**Deep Instrumental Variables estimator (Hartford et al. 2017).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level. |
| `batch_size` | `integer` |  | `256` | batch_size parameter (int). |
| `covariates` | `array[string]` | ✓ |  | Exogenous controls. |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `first_stage_epochs` | `integer` |  | `100` | Stage 1 training epochs. |
| `hidden_layers` | `array[string]` |  | `[128, 64]` | Hidden layer sizes. |
| `instruments` | `array[string]` | ✓ |  | Excluded instruments. |
| `learning_rate` | `number` |  | `0.001` | learning_rate parameter (float). |
| `n_components` | `integer` |  | `10` | Gaussian mixture components in the MDN. |
| `n_gradient_samples` | `integer` |  | `0` | Independent additional samples for the gradient path. ``0`` reproduces EconML's default (biased but variance-regularized); ``>= 1`` activates Hartford et al.'s paired-sample unbiased gradient estimator. |
| `n_samples` | `integer` |  | `1` | MC samples per observation used to form the Stage-2 residual. |
| `random_state` | `integer` |  | `42` | Random seed or RandomState for reproducible stochastic steps. |
> 📝 *随机种子或 RandomState，用于可重复的随机步骤。*
| `second_stage_epochs` | `integer` |  | `100` | Stage 2 training epochs. |
| `treat` | `string` | ✓ |  | Endogenous treatment variable (continuous). |
| `verbose` | `boolean` |  | `False` | verbose parameter (bool). |
| `y` | `string` | ✓ |  | Outcome variable. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.DeepIV(y="outcome", data=df, treat="value", instruments=["a", "b"], covariates=["a", "b"])
print(result.summary())
```

---
### `sp.deepiv()`

**Estimate causal effects using Deep Instrumental Variables.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `alpha` | `number` |  | `0.05` | Significance level for confidence interval. |
| `batch_size` | `integer` |  | `256` | Mini-batch size. |
| `covariates` | `array[string]` | ✓ |  | Exogenous control variable names. |
| `data` | `string` | ✓ |  | Input data. |
> 📝 *输入数据。*
| `first_stage_epochs` | `integer` |  | `100` | Training epochs for the treatment model (MDN). |
| `hidden_layers` | `array[string]` |  | `[128, 64]` | Hidden layer sizes for both networks. |
| `instruments` | `array[string]` | ✓ |  | Excluded instrument variable names. |
| `learning_rate` | `number` |  | `0.001` | Adam learning rate. |
| `n_components` | `integer` |  | `10` | Number of Gaussian mixture components in the MDN (stage 1). |
| `n_gradient_samples` | `integer` |  | `0` | Number of **independent** additional samples used for the gradient path. When ``0`` (default), a single set of samples is used, matching Microsoft EconML's default behaviour and producing a biased but variance-regularized gradient estimator. When ``> 0``, two independent sample sets are drawn and the unbiased paired-sample estimator ``mean((y - h(p, x)) * (y - h(p', x)))`` from Hartford et al. Section 3.2 is used instead. Set to ``1`` or higher if you specifically need unbiased gradients (e.g. for asymptotic consistency arguments). |
| `n_samples` | `integer` |  | `1` | Number of MC samples per observation used to form the Stage-2 residual ``(y - h(t, x))``. |
| `random_state` | `integer` |  | `42` | Random seed for reproducibility. |
| `second_stage_epochs` | `integer` |  | `100` | Training epochs for the response model. |
| `treat` | `string` | ✓ |  | Endogenous treatment variable name (continuous). |
| `verbose` | `boolean` |  | `False` | Print training progress. |
| `y` | `string` | ✓ |  | Outcome variable name. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.deepiv(y="outcome", data=df, treat="value", instruments=["a", "b"], covariates=["a", "b"])
print(result.summary())
```

> 📁 See also: `docs/guides/gpu_acceleration.md`

---
