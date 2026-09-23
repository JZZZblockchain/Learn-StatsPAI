"""DGPs A (causalfe paper) and B (selection on FE, dynamic effects)."""

import numpy as np


def dgp(name, seed):
    r = np.random.default_rng(seed)
    if name == "A":  # causalfe paper DGP: dgp_did_heterogeneous(N=200, T=6)
        N, T = 200, 6
        X = r.normal(size=(N * T, 3))
        unit = np.repeat(np.arange(N), T)
        time = np.tile(np.arange(T), N)
        tau = X[:, 0].copy()
        adopt = r.integers(1, T, size=N)
        D = (time >= adopt[unit]).astype(float)
        alpha = r.normal(size=N)
        gamma = r.normal(size=T)
        Y = tau * D + alpha[unit] + gamma[time] + r.normal(size=N * T)
    else:  # B: FE ~ x, selection on FE, never-treated, dynamic effects
        N, T = 200, 8
        xu = r.normal(size=(N, 3))
        unit = np.repeat(np.arange(N), T)
        time = np.tile(np.arange(T), N)
        alpha = 2 * xu[:, 0] + r.normal(size=N)
        p = 1 / (1 + np.exp(-alpha / 2))
        cohort = np.where(r.random(N) < p, r.choice([3, 5, 7], size=N), 99)
        D = (time >= cohort[unit]).astype(float)
        e = np.maximum(time - cohort[unit], 0)
        X = xu[unit]
        tau = (1 + X[:, 0]) * (1 + 0.25 * e)
        gamma = np.cumsum(r.normal(0, 0.5, size=T))
        Y = alpha[unit] + gamma[time] + tau * D + r.normal(size=N * T)
    return X, Y, D, unit, time, tau
