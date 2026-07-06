# causal_rl

> 📂 所属分类:08 · 高级因果推断方法 (Advanced Causal Methods)

Causal Reinforcement Learning (StatsPAI v0.10).

Bridges between RL and causal inference for offline / batch learning
scenarios with unobserved confounding.

References
----------
* Li, Zhang & Bareinboim (2025), arXiv 2510.21110 — Confounding-Robust Deep RL.
* Cunha, Liu, French & Mian (2025), arXiv 2512.18135 — Unifying Causal RL.
* Chemingui, Deshwal, Fern, Nguyen-Tang & Doppa (2025),
  arXiv 2510.22027 — Online Optimization for Offline Safe RL.

**9 个公共函数**

### `sp.BanditBenchmarkResult()`

**Output from a causal-RL benchmark run.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `benchmark` | `string` | ✓ |  | benchmark parameter (str). |
| `optimal_policy` | `string` | ✓ |  | optimal_policy parameter (np.ndarray). |
| `optimal_value` | `number` | ✓ |  | optimal_value parameter (float). |
| `suggested_evaluator` | `string` | ✓ |  | suggested_evaluator parameter (str). |
| `transitions` | `string` | ✓ |  | transitions parameter (pd.DataFrame). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.BanditBenchmarkResult(benchmark="value", transitions="value", optimal_policy="value", optimal_value=1.0, suggested_evaluator="value")
print(result.summary())
```

---
### `sp.CausalDQNResult()`

**Output of confounding-robust Q-learning (:func:`causal_dqn`).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `final_bellman_error` | `number` | ✓ |  | final_bellman_error parameter (float). |
| `gamma_bound` | `number` | ✓ |  | gamma_bound parameter (float). |
| `n_iter` | `integer` | ✓ |  | Number of iter. |
| `policy` | `string` | ✓ |  | policy parameter (np.ndarray). |
| `q_table` | `string` | ✓ |  | q_table parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.CausalDQNResult(q_table="value", policy="value", gamma_bound=1.0, n_iter=1.0, final_bellman_error=1.0)
print(result.summary())
```

---
### `sp.OfflineSafeResult()`

**Output of safe offline policy learning.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cost_threshold` | `number` | ✓ |  | cost_threshold parameter (float). |
| `expected_cost` | `number` | ✓ |  | expected_cost parameter (float). |
| `expected_reward` | `number` | ✓ |  | expected_reward parameter (float). |
| `feasible` | `boolean` | ✓ |  | feasible parameter (bool). |
| `policy` | `string` | ✓ |  | policy parameter (np.ndarray). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.OfflineSafeResult(policy="value", expected_reward=1.0, expected_cost=1.0, cost_threshold=1.0, feasible=True)
print(result.summary())
```

---
### `sp.causal_bandit()`

**Bareinboim-Forney-Pearl contextual causal bandit: pick the optimal arm by Monte-Carlo estimation of E[Y(a) | context].**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `arms` | `array[string]` | ✓ |  | arms parameter (list). |
| `context` | `object` |  |  | context parameter (dict). |
| `n_samples` | `integer` |  | `500` | Number of samples. |
| `reward_fn` | `string` | ✓ |  | reward_fn parameter (callable). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.causal_bandit(arms=["a", "b"], reward_fn="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_rl_family.md`

---
### `sp.causal_dqn()`

**Causal deep Q-network (Li, Zhang, Bareinboim 2025, arXiv:2510.21110) for offline policy learning under unobserved confounding. Learns a confounding-robust Q-function via bootstrap data augmentation.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | `string` | ✓ |  | action parameter (str). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `discount` | `number` |  | `0.95` | Discount factor |
| `n_iter` | `integer` |  | `100` | Fitted-Q iterations |
| `next_state` | `string` | ✓ |  | Next-state column(s) |
| `reward` | `string` | ✓ |  | reward parameter (str). |
| `state` | `string` | ✓ |  | State column(s) |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.causal_dqn(data=df, state="value", action="value", reward="value", next_state="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_rl_family.md`

---
### `sp.causal_rl_benchmark()`

**Generate a synthetic causal-RL benchmark dataset.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `confounding_strength` | `number` |  | `0.5` | Magnitude of unmeasured confounding U -> (action, reward). |
| `n_episodes` | `integer` |  | `1000` | Number of episodes. |
| `name` | `string` |  | `'confounded_bandit'` | 'confounded_targeting', 'confounded_routing'} |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.causal_rl_benchmark()
print(result.summary())
```

> 📁 See also: `docs/guides/causal_rl_family.md`

---
### `sp.counterfactual_policy_optimization()`

**Counterfactual policy evaluation under a linear-Gaussian SCM via noise inversion (Oberst-Sontag 2019, Buesing et al. 2019).**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | `string` | ✓ |  | action parameter (str). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `reward` | `string` | ✓ |  | reward parameter (str). |
| `state` | `string` | ✓ |  | state parameter (str). |
| `target_policy` | `string` | ✓ |  | target_policy parameter (callable). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.counterfactual_policy_optimization(data=df, state="value", action="value", reward="value", target_policy="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_rl_family.md`

---
### `sp.offline_safe_policy()`

**Safe offline policy learning with a cost-constraint.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | `string` | ✓ |  | Column names. state and action must be discrete. |
| `cost` | `string` | ✓ |  | Column names. state and action must be discrete. |
| `cost_threshold` | `number` |  | `0.5` | Max allowed expected cost per step. |
| `data` | `string` | ✓ |  | Transition data (s, a, r, cost). |
| `discount` | `number` |  | `0.95` | discount parameter (float). |
| `n_iter` | `integer` |  | `100` | Number of iter. |
| `reward` | `string` | ✓ |  | Column names. state and action must be discrete. |
| `seed` | `integer` |  | `0` | Random seed for reproducible stochastic steps. |
| `state` | `string` | ✓ |  | Column names. state and action must be discrete. |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.offline_safe_policy(data=df, state="value", action="value", reward="value", cost="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_rl_family.md`

---
### `sp.structural_mdp()`

**Fit a linear SVAR for a Markov decision process and roll out counterfactual trajectories under alternative policies.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action_cols` | `array[string]` | ✓ |  | action_cols parameter (list). |
| `data` | `string` | ✓ |  | pandas DataFrame containing the variables used by the estimator. |
| `next_state_cols` | `array[string]` |  |  | next_state_cols parameter (list). |
| `reward` | `string` | ✓ |  | reward parameter (str). |
| `state_cols` | `array[string]` | ✓ |  | state_cols parameter (list). |
| `time` | `string` |  |  | Time period column. |
| `trajectory` | `string` |  |  | trajectory parameter (str). |

**Example:**

```python
import statspai as sp
import pandas as pd

# Load or prepare data
df = sp.datasets.card_1995()  # example dataset

result = sp.structural_mdp(data=df, state_cols=["a", "b"], action_cols=["a", "b"], reward="value")
print(result.summary())
```

> 📁 See also: `docs/guides/causal_rl_family.md`

---
