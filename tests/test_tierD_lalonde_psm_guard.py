"""Tier D guard — pin the LaLonde classic-track replication numbers.

Part of the P1 campaign (see ``.tierd_campaign/CAMPAIGN.md``). The
``sp.replicate('lalonde_1986')`` registry ships *golden numbers* for the classic
track, but no test guarded the live 1:1 NN propensity-score-matching ATT. This
test is that missing guard: it pins all three classic LaLonde numbers to their
current deterministic values on the bundled real data, including the stable
index-anchored nearest-neighbor tie-break in ``sp.match``.

The naive and covariate-adjusted OLS values reproduce R ``MatchIt`` to the
dollar; the PSM value is the deterministic ``sp.match(method='nearest')`` output
after exact-distance ties on the binary covariates are resolved by source index.

This guard accompanies the nearest-neighbor tie-break fix; only exact-tie
matching designs can move.
"""

import pytest

import statspai as sp

COVS = ["age", "educ", "black", "hispanic", "married", "nodegree", "re74", "re75"]


@pytest.fixture(scope="module")
def lalonde():
    df, _ = sp.replicate("lalonde_1986")
    return df


def test_naive_ols_matches_matchit(lalonde):
    naive = sp.regress("re78 ~ treat", data=lalonde, robust="hc1")
    assert float(naive.params["treat"]) == pytest.approx(-635.03, abs=1.0)


def test_adjusted_ols_matches_matchit(lalonde):
    adj = sp.regress("re78 ~ treat + " + " + ".join(COVS), data=lalonde, robust="hc1")
    assert float(adj.params["treat"]) == pytest.approx(1548.24, abs=1.0)


def test_psm_att_is_deterministic_and_pinned(lalonde):
    # Deterministic across runs; pinned to the current value so any tie-break /
    # algorithm change in sp.match is caught (the guard that was missing before).
    vals = [
        float(
            sp.match(
                data=lalonde, y="re78", treat="treat", covariates=COVS, method="nearest"
            ).estimate
        )
        for _ in range(3)
    ]
    assert len(set(round(v, 6) for v in vals)) == 1  # deterministic within a run
    assert vals[0] == pytest.approx(1963.43, abs=0.1)


def test_psm_recovers_experimental_benchmark(lalonde):
    # The scientific content of DW (1999): matching recovers the ~$1,794
    # experimental benchmark and removes the negative naive selection bias.
    naive = float(
        sp.regress("re78 ~ treat", data=lalonde, robust="hc1").params["treat"]
    )
    psm = float(
        sp.match(
            data=lalonde, y="re78", treat="treat", covariates=COVS, method="nearest"
        ).estimate
    )
    assert naive < 0 < psm
    assert 1500.0 < psm < 2500.0
