"""sp.randomize follows randomizr's complete_ra / block_ra / cluster_ra rules.

Random draws cannot match across languages (different generators), so
these tests assert the allocation rule itself, which is deterministic:
arm counts are floor(N p_j) or floor(N p_j) + 1, misfits are allocated at
random (not to a fixed arm), and re-randomization redraws from the same
design. Rule transcribed from randomizr 2.0.1 ``complete_ra``.
"""

import numpy as np
import pandas as pd
import pytest

import statspai as sp


def _df(n=103, seed=0):
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "s": np.repeat([1, 2, 3, 4], [5, 7, 40, 51])[:n],
            "cl": np.arange(n) // 4,
            "x": rng.normal(size=n),
            "z": rng.normal(size=n),
        }
    )


def test_complete_method_fixes_the_counts():
    df = _df()
    for seed in range(20):
        r = sp.randomize(df, method="complete", seed=seed)
        assert r.n_treated in (51, 52)  # floor(103/2), +1 misfit


def test_block_counts_and_random_misfits():
    df = _df()
    got = {1: set(), 2: set()}
    for seed in range(60):
        a = sp.randomize(df, strata="s", seed=seed).data
        n1 = a.groupby("s")["treatment"].sum()
        sizes = a.groupby("s").size()
        assert ((n1 == sizes // 2) | (n1 == sizes // 2 + 1)).all()
        got[1].add(int(n1[1]))
        got[2].add(int(n1[2]))
    # The misfit of an odd stratum goes to either arm (it used to go to a
    # fixed arm: 2 of 5, 4 of 7 treated).
    assert got[1] == {2, 3} and got[2] == {3, 4}


def test_three_arm_counts_with_unequal_prob():
    df = _df()
    p = [0.2, 0.3, 0.5]
    for seed in range(20):
        a = sp.randomize(df, n_arms=3, prob=p, method="complete", seed=seed).data
        c = a["treatment"].value_counts().reindex(range(3), fill_value=0).to_numpy()
        fl = np.floor(103 * np.array(p)).astype(int)
        assert c.sum() == 103 and np.all((c == fl) | (c == fl + 1))


def test_cluster_assignment_is_complete_over_clusters():
    df = _df()
    a = sp.randomize(df, cluster="cl", seed=3).data
    assert (a.groupby("cl")["treatment"].nunique() == 1).all()
    ncl = df["cl"].nunique()
    n1 = a.groupby("cl")["treatment"].first().sum()
    assert n1 in (ncl // 2, ncl // 2 + 1)


def test_rerandomization_keeps_the_block_design():
    df = _df()
    a = sp.randomize(df, strata="s", balance_vars=["x", "z"], n_rerand=50, seed=1).data
    n1 = a.groupby("s")["treatment"].sum()
    sizes = a.groupby("s").size()
    assert ((n1 == sizes // 2) | (n1 == sizes // 2 + 1)).all()


def test_rejects_bad_prob():
    with pytest.raises(ValueError, match="prob"):
        sp.randomize(_df(), prob=[0.7, 0.7])
