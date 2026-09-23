"""Heterogeneity analysis after a causal forest: groups, support, pre-trends.

Three questions come after the forest has produced ``tau(x)``, and each
needs its own inference rather than a summary of the fitted predictions:

* :func:`forest_group_effects` -- how large is the effect for a country
  pair, a country, a period, or a quantile of the forest's prediction?
  Averages of unbiased scores with valid standard errors (imputation scores
  for forests with fixed effects, AIPW scores otherwise), including
  membership groups for dyadic data and a dyadic-robust variance.
* :func:`forest_support` -- is a counterfactual prediction for a unit that
  was never treated an interpolation or an extrapolation?
* :func:`cate_pretrend_test` -- were the units the forest ranks as high-
  effect already on a different trajectory before treatment?

The worked example in ``docs/guides/heterogeneity_panel_forests.md``
reproduces the workflow of [aytug2026euro] (causal forests with fixed
effects [kattenberg2023causal] on a dyadic trade panel) on simulated data.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from scipy import stats

from .._aliases import accepts_aliases
from ..exceptions import DataInsufficient, MethodIncompatibility
from . import _fe_imputation as fi
from . import _grf_inference as gi

__all__ = ["forest_group_effects", "forest_support", "cate_pretrend_test"]


def _require_grf(forest: Any, context: str) -> None:
    if not getattr(forest, "fitted_", False) or not gi.is_grf_forest(forest):
        raise MethodIncompatibility(
            f"{context} needs a causal forest fitted with the GRF engine.",
            recovery_hint=(
                "Fit with sp.causal_forest(...) (default split_rule='grf') "
                "before calling this function."
            ),
        )


# --------------------------------------------------------------------------- #
#  Group effects
# --------------------------------------------------------------------------- #


@accepts_aliases(_strict=True, controls="covariates")
def forest_group_effects(
    forest: Any,
    by: Any = None,
    *,
    members: Any = None,
    n_groups: int = 4,
    cluster: Any = None,
    variance: str = "forest",
    alpha: float = 0.05,
    scale: str = "level",
    min_rows: int = 1,
    covariates: Any = "none",
) -> pd.DataFrame:
    """Average treatment effects by group, with valid standard errors.

    A causal forest's predictions are regularised: averaging them over a
    group gives a number that is shrunk toward the overall mean and whose
    spread says nothing about sampling error.  This function averages an
    *unbiased* per-row signal instead and uses the forest only to form
    groups when asked to:

    * **Forests with two-way fixed effects** (``fe="twoway"``): the
      imputation score ``Y - alpha_hat_i - gamma_hat_t`` of each treated
      cell, with unit and period effects fitted on the untreated cells
      [borusyak2024revisiting].  Each group estimate is the ATT over the
      group's treated cells.  Standard errors use the exact linear weights
      of the imputation estimator; treated residuals are centred on the
      out-of-bag forest prediction and then on cohort x event-time means
      (``variance="forest"``) or on those means only (``variance="bjs"``,
      the conservative convention of :func:`statspai.did_imputation`).
    * **Pooled forests**: the AIPW score of every row; each estimate is the
      group ATE.

    Rows are weighted by the forest's observation weights, so with
    ``equalize_cluster_weights=True`` every cluster gets equal weight in each
    group average (a different estimand from :func:`statspai.did_imputation`,
    which weights treated cells equally).

    Parameters
    ----------
    forest : CausalForest
        Fitted with the GRF engine.
    by : None, "cate_quantile" or array-like
        ``None`` pools all eligible rows (or, with ``members``, forms one
        group per member).  ``"cate_quantile"`` bins eligible rows into
        ``n_groups`` quantiles of the out-of-bag forest prediction (sorted
        group average treatment effects, [chernozhukov2025generic]).  An
        array gives one label per training row (a pair id, a period band,
        ``df["year"] >= 2009`` ...).
    members : (n, 2) array-like, optional
        The two members of each row of dyadic data (exporter and importer,
        the two countries of a pair).  With ``by=None`` each member is a
        group and a row counts for both of its members -- the average
        effect over all pairs a country belongs to.
    n_groups : int, default 4
        Number of quantile groups for ``by="cate_quantile"``.
    cluster : None, "dyadic" or array-like
        ``None`` clusters by the forest's clusters (default: the panel
        unit).  ``"dyadic"`` (requires ``members``) allows any two rows
        that share a member to be correlated [aronow2015cluster].  An array
        gives other cluster ids.
    variance : {"forest", "bjs"}, default "forest"
        Forests with fixed effects only; see above.
    alpha : float, default 0.05
    scale : {"level", "percent"}, default "level"
        ``"percent"`` adds ``100 * (exp(x) - 1)`` columns for log outcomes
        (interval endpoints are transformed, not re-derived).
    min_rows : int, default 1
        Drop groups with fewer eligible rows.
    covariates : "none", "auto", list of str or array, default "none"
        Forests with fixed effects only: covariates entering the untreated
        outcome model linearly, ``Y(0) = alpha_i + gamma_t + C' beta``.
        ``"none"`` is the pure two-way model of
        :func:`statspai.did_imputation`; ``"auto"`` adds the forest's effect
        modifiers and covariates that vary within units (time-invariant ones
        are absorbed by the unit effect).  Controls must not be affected by
        the treatment.

    Returns
    -------
    pandas.DataFrame
        One row per group: ``n_rows``, ``n_units``, ``estimate``, ``se``,
        ``z``, ``p``, ``ci_low``, ``ci_high`` and ``forest_mean`` (the mean
        out-of-bag prediction over the same rows, for comparison).
        ``attrs`` holds ``method``, ``estimand``, the full ``vcov`` and
        ``tests``: a Wald test that all group effects are equal and the
        last-minus-first difference with its standard error.

    Examples
    --------
    >>> import statspai as sp
    >>> df = sp.datasets.currency_union_panel(seed=0)
    >>> cf = sp.causal_forest(
    ...     data=df, y="log_trade", d="euro",
    ...     x=["pre_trade", "log_gdp_prod", "log_gdppc"],
    ...     id="pair", time="year", fe="twoway",
    ...     n_estimators=400, random_state=0,
    ... )
    >>> by_country = sp.forest_group_effects(
    ...     cf, members=df[["country_i", "country_j"]].to_numpy(),
    ...     scale="percent",
    ... )
    >>> by_country.index.name
    'group'

    References
    ----------
    [borusyak2024revisiting], [chernozhukov2025generic], [aronow2015cluster],
    [kattenberg2023causal]
    """
    _require_grf(forest, "forest_group_effects()")
    return fi.group_effects(
        forest,
        by,
        members=members,
        n_groups=n_groups,
        cluster=cluster,
        variance=variance,
        alpha=alpha,
        scale=scale,
        min_rows=min_rows,
        covariates=covariates,
    )


# --------------------------------------------------------------------------- #
#  Support of counterfactual predictions
# --------------------------------------------------------------------------- #


def _reference_rows(forest: Any) -> np.ndarray:
    """Rows that inform the effect: switching units for FE forests."""
    n = int(len(forest._Y_original))
    if not gi.is_fe_forest(forest):
        return np.ones(n, dtype=bool)
    unit = np.asarray(forest._fe_unit, dtype=np.int64)
    T = np.asarray(forest._T_original, dtype=float)
    n_u = int(unit.max()) + 1
    lo = np.full(n_u, np.inf)
    hi = np.full(n_u, -np.inf)
    np.minimum.at(lo, unit, T)
    np.maximum.at(hi, unit, T)
    return np.asarray((hi > lo)[unit])


def _kth_distance(ref: np.ndarray, query: np.ndarray, k: int) -> np.ndarray:
    from scipy.spatial import cKDTree

    dist, _ = cKDTree(ref).query(query, k=k)
    dist = np.asarray(dist)
    return dist if dist.ndim == 1 else dist[:, -1]


def _kth_distance_other_units(
    ref: np.ndarray, groups: np.ndarray, k: int
) -> np.ndarray:
    """k-th nearest-neighbour distance of each reference row to rows of
    *other* units, so repeated rows of a unit cannot shrink the benchmark
    that a new unit is compared with."""
    from scipy.spatial import cKDTree

    max_rows = int(np.bincount(groups).max())
    kk = min(k + max_rows, ref.shape[0])
    dist, idx = cKDTree(ref).query(ref, k=kk)
    dist = np.asarray(dist).reshape(ref.shape[0], -1)
    idx = np.asarray(idx).reshape(ref.shape[0], -1)
    other = groups[idx] != groups[:, None]
    out = np.full(ref.shape[0], np.nan)
    for i in range(ref.shape[0]):
        d = dist[i, other[i]]
        if d.size >= k:
            out[i] = d[k - 1]
    return out


def forest_support(
    forest: Any,
    X_new: Any,
    *,
    k: int = 10,
    quantile: float = 0.95,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Check whether new rows lie inside the support that informs ``tau(x)``.

    Predicting the effect a unit *would* have had (a country that did not
    adopt a currency, a region that was never treated) applies the fitted
    ``tau(x)`` outside the treated sample.  That is a model-based
    extrapolation, credible only where the forest has seen similar units
    switch treatment.  For every row of ``X_new`` this reports

    * ``cate``, its little-bag ``se`` and a ``(1 - alpha)`` interval;
    * ``n_outside_range`` -- effect modifiers outside the ``[min, max]`` of
      the reference rows;
    * ``knn_ratio`` -- the distance (on reference-standardised modifiers)
      to the ``k``-th nearest reference row, divided by the ``quantile``
      of the reference rows' distance to their ``k``-th nearest row from a
      *different* unit (rows of the same unit are excluded, so a unit's
      other periods do not shrink the benchmark).  Above 1 the row is
      farther from the data than all but ``1 - quantile`` of the reference
      rows are from other units;
    * ``supported`` -- ``n_outside_range == 0`` and ``knn_ratio <= 1``.

    The reference rows are the rows that inform the effect: for a forest
    with fixed effects, the rows of units whose treatment varies (only they
    identify the within effect); for a pooled forest, all training rows.

    Parameters
    ----------
    forest : CausalForest
        Fitted with the GRF engine.
    X_new : array-like or DataFrame
        Effect modifiers of the rows to predict (DataFrame columns are
        matched to the fitted feature names).
    k : int, default 10
    quantile : float, default 0.95
    alpha : float, default 0.05

    Returns
    -------
    pandas.DataFrame
        One row per row of ``X_new``; ``attrs["summary"]`` holds the share
        of supported rows and the reference-sample size.

    Examples
    --------
    >>> import statspai as sp
    >>> df = sp.datasets.currency_union_panel(seed=0)
    >>> x = ["pre_trade", "log_gdp_prod", "log_gdppc"]
    >>> cf = sp.causal_forest(
    ...     data=df, y="log_trade", d="euro", x=x,
    ...     id="pair", time="year", fe="twoway",
    ...     n_estimators=400, random_state=0,
    ... )
    >>> outs = df[df["ever_euro"] == 0]
    >>> sup = sp.forest_support(cf, outs[x])
    >>> bool(sup["supported"].mean() > 0)
    True
    """
    _require_grf(forest, "forest_support()")
    if not isinstance(k, (int, np.integer)) or isinstance(k, bool) or k < 1:
        raise MethodIncompatibility(
            "forest_support(): k must be a positive integer.",
            recovery_hint="Use k=10.",
        )
    if not 0.0 < float(quantile) < 1.0 or not 0.0 < float(alpha) < 1.0:
        raise MethodIncompatibility(
            "forest_support(): quantile and alpha must lie in (0, 1).",
            recovery_hint="Use quantile=0.95, alpha=0.05.",
        )
    Xn = forest._prepare_effect_matrix(X_new, context="forest_support()")
    ref_mask = _reference_rows(forest)
    ref = np.asarray(forest._X_original, dtype=float)[ref_mask]
    if gi.is_fe_forest(forest):
        ref_units = np.asarray(forest._fe_unit, dtype=np.int64)[ref_mask]
    elif getattr(forest, "_clusters", None) is not None:
        ref_units = np.asarray(forest._clusters, dtype=np.int64)[ref_mask]
    else:
        ref_units = np.arange(ref.shape[0], dtype=np.int64)
    ref_units = np.asarray(pd.factorize(pd.Series(ref_units))[0], dtype=np.int64)
    if ref.shape[0] <= k:
        raise DataInsufficient(
            "forest_support(): fewer reference rows than k.",
            recovery_hint="Lower k.",
            diagnostics={"n_reference_rows": int(ref.shape[0]), "k": int(k)},
        )
    lo, hi = ref.min(axis=0), ref.max(axis=0)
    outside = (Xn < lo) | (Xn > hi)
    scale = ref.std(axis=0)
    scale = np.where(scale > 0, scale, 1.0)
    ref_s = (ref - ref.mean(axis=0)) / scale
    new_s = (Xn - ref.mean(axis=0)) / scale
    if int(ref_units.max()) + 1 <= k:
        raise DataInsufficient(
            "forest_support(): the reference rows come from k or fewer units.",
            recovery_hint="Lower k.",
            diagnostics={"n_reference_units": int(ref_units.max()) + 1, "k": int(k)},
        )
    ref_dist = _kth_distance_other_units(ref_s, ref_units, int(k))
    cutoff = float(np.nanquantile(ref_dist, float(quantile)))
    new_dist = _kth_distance(ref_s, new_s, int(k))
    ratio = new_dist / cutoff if cutoff > 0 else np.where(new_dist > 0, np.inf, 0.0)
    cate = np.asarray(forest.effect(Xn), dtype=float).ravel()
    try:
        var = np.asarray(forest.effect_variance(Xn), dtype=float).ravel()
        se = np.sqrt(np.clip(var, 0.0, None))
    except MethodIncompatibility:
        se = np.full(cate.size, np.nan)
    z = float(stats.norm.ppf(1 - float(alpha) / 2))
    names = list(getattr(forest, "_feature_names", None) or [])
    out = pd.DataFrame(
        {
            "cate": cate,
            "se": se,
            "ci_low": cate - z * se,
            "ci_high": cate + z * se,
            "n_outside_range": outside.sum(axis=1).astype(int),
            "knn_distance": new_dist,
            "knn_ratio": ratio,
        }
    )
    out["supported"] = (out["n_outside_range"] == 0) & (out["knn_ratio"] <= 1.0)
    if isinstance(X_new, pd.DataFrame):
        out.index = X_new.index
    per_feature = {
        (names[j] if j < len(names) else f"X{j}"): float(outside[:, j].mean())
        for j in range(Xn.shape[1])
    }
    out.attrs["summary"] = {
        "share_supported": float(out["supported"].mean()),
        "share_outside_range_by_feature": per_feature,
        "n_reference_rows": int(ref.shape[0]),
        "reference": (
            "rows of units whose treatment varies"
            if gi.is_fe_forest(forest)
            else "all training rows"
        ),
        "knn_cutoff": cutoff,
        "k": int(k),
        "quantile": float(quantile),
    }
    return out


# --------------------------------------------------------------------------- #
#  Pre-trends by predicted-effect group
# --------------------------------------------------------------------------- #


def _two_way_demean(V: np.ndarray, unit: np.ndarray, time: np.ndarray) -> np.ndarray:
    from . import _grf_engine as engine

    n = unit.size
    idx = np.arange(n, dtype=np.int64)
    G = np.ones(n)
    n_u = int(unit.max()) + 1
    n_t = int(time.max()) + 1
    cols = []
    for j in range(V.shape[1]):
        out = np.zeros(n)
        sweeps = engine._fe_residualize(
            idx,
            np.ascontiguousarray(V[:, j], dtype=np.float64),
            G,
            unit,
            time,
            np.zeros(n_u),
            np.zeros(n_u),
            np.zeros(n_t),
            np.zeros(n_t),
            out,
            100000,
            1e-13,
        )
        if sweeps < 0:
            raise DataInsufficient(
                "cate_pretrend_test(): the two-way within transformation did "
                "not converge.",
                recovery_hint=(
                    "Check the untreated panel for disconnected unit-period " "sets."
                ),
            )
        cols.append(out)
    return np.column_stack(cols)


@accepts_aliases(_strict=True, controls="covariates")
def cate_pretrend_test(
    forest: Any,
    *,
    n_groups: int = 2,
    leads: Optional[int] = None,
    groups: Any = None,
    time_effects: str = "common",
    alpha: float = 0.05,
    covariates: Any = "none",
) -> Dict[str, Any]:
    """Test whether predicted-effect groups had different pre-treatment trends.

    Heterogeneity found by a forest can be spurious if the units it ranks
    high were already diverging before treatment [aytug2026euro].  This
    test sorts units into ``n_groups`` quantiles of their mean out-of-bag
    prediction (or uses ``groups``) and, on the **untreated** cells only,
    regresses the outcome on unit and period effects and on lead indicators
    ``1[t - g = k] x 1[group]`` for ``k = -1, ..., -leads`` -- the
    pre-trend regression of [borusyak2024revisiting], interacted with the
    groups.  Periods earlier than ``-leads`` and never-treated units are the
    reference.  Using untreated cells only keeps post-treatment effect
    heterogeneity out of the test.

    Two Wald tests are reported: all leads are zero, and the leads are
    equal across groups (for each ``k``, every group's lead equals the
    first group's).  The second is the test that bears on heterogeneity.
    Standard errors are clustered by the forest's clusters with the CR1
    factor ``G/(G-1) (n-1)/(n-K)``, where ``K`` counts the leads and the
    period effects (unit effects are nested in unit clusters, fixest's
    ``fixef.K = "nested"``).

    Parameters
    ----------
    forest : CausalForest
        Fitted with ``fe="twoway"`` and a binary absorbing treatment.
    n_groups : int, default 2
        Quantile groups of the unit-level mean OOB prediction.
    leads : int, optional
        Number of pre-treatment leads (default: ``min(4, L - 1)`` where
        ``L`` is the longest pre-treatment spell; with ``L`` leads every
        pre-period of the earliest-observed units is a lead and the leads
        are collinear with their unit effects).
    groups : array-like, optional
        One label per training row, constant within units; overrides
        ``n_groups``.
    time_effects : {"common", "by_group"}, default "common"
        ``"common"`` matches the forest and the imputation scores, which
        use one set of period effects; ``"by_group"`` gives each group its
        own period effects (separate event studies per group).
    alpha : float, default 0.05
    covariates : "none", "auto", list of str or array, default "none"
        Time-varying covariates added linearly, as in the imputation model
        of :func:`forest_group_effects`.

    Returns
    -------
    dict
        ``coefficients`` (DataFrame indexed by group and lead), ``joint_zero``
        and ``equal_across_groups`` (``stat``, ``df``, ``p``), ``group_of_unit``
        (Series), ``n_obs``, ``n_clusters`` and ``method``.

    Examples
    --------
    >>> import statspai as sp
    >>> df = sp.datasets.currency_union_panel(seed=0)
    >>> cf = sp.causal_forest(
    ...     data=df, y="log_trade", d="euro",
    ...     x=["pre_trade", "log_gdp_prod", "log_gdppc"],
    ...     id="pair", time="year", fe="twoway",
    ...     n_estimators=400, random_state=0,
    ... )
    >>> res = sp.cate_pretrend_test(cf, n_groups=2, leads=3)
    >>> sorted(res["equal_across_groups"])
    ['df', 'p', 'stat']

    References
    ----------
    [borusyak2024revisiting], [aytug2026euro]
    """
    context = "cate_pretrend_test()"
    _require_grf(forest, context)
    if not gi.is_fe_forest(forest):
        raise MethodIncompatibility(
            f"{context} needs a causal forest with fixed effects (fe=...).",
            recovery_hint=(
                "Fit sp.causal_forest(..., id=, time=, fe='twoway'); for "
                "staggered designs sp.did_forest() reports its own pre-trend test."
            ),
            alternative_functions=["sp.did_forest"],
        )
    if time_effects not in ("common", "by_group"):
        raise MethodIncompatibility(
            f"{context}: time_effects must be 'common' or 'by_group'.",
            recovery_hint="Use time_effects='common'.",
        )
    design = fi.imputation_design(forest, context, covariates)
    if not design.absorbing:
        raise MethodIncompatibility(
            f"{context} needs an absorbing (staggered) treatment so that "
            "leads relative to the adoption period are defined.",
            recovery_hint="Use a design in which units stay treated once treated.",
        )
    unit, time = design.unit, design.time
    n = design.n
    n_u = int(unit.max()) + 1

    # Unit-level groups.
    if groups is None:
        if not isinstance(n_groups, (int, np.integer)) or n_groups < 2:
            raise MethodIncompatibility(
                f"{context}: n_groups must be an integer >= 2.",
                recovery_hint="Use n_groups=2 (above / below the median).",
            )
        tau = np.asarray(forest._oob_tau, dtype=float)
        ok = np.isfinite(tau)
        s = np.bincount(unit[ok], weights=tau[ok], minlength=n_u)
        c = np.bincount(unit[ok], minlength=n_u)
        unit_tau = np.divide(s, c, out=np.full(n_u, np.nan), where=c > 0)
        valid = np.isfinite(unit_tau)
        ranks = pd.Series(unit_tau[valid]).rank(method="first").to_numpy()
        code = np.full(n_u, -1, dtype=np.int64)
        code[valid] = np.minimum(
            (ranks - 1) * n_groups // valid.sum(), n_groups - 1
        ).astype(np.int64)
        labels: List[Any] = [f"Q{g + 1}" for g in range(int(n_groups))]
        row_group = code[unit]
    else:
        arr = np.asarray(groups, dtype=object)
        if arr.ndim != 1 or arr.size != n or pd.isna(pd.Series(arr)).any():
            raise MethodIncompatibility(
                f"{context}: groups must give one non-missing label per training row.",
                recovery_hint="Pass df['group'].to_numpy() aligned with the fit rows.",
            )
        codes, uniq = pd.factorize(pd.Series(arr), sort=True)
        per_unit = pd.Series(codes).groupby(unit).nunique()
        if (per_unit > 1).any():
            raise MethodIncompatibility(
                f"{context}: groups must be constant within units.",
                recovery_hint="Assign each unit to one group.",
            )
        row_group = codes.astype(np.int64)
        labels = list(uniq)
    G = len(labels)
    if G < 2:
        raise DataInsufficient(
            f"{context}: need at least two groups.",
            recovery_hint="Use n_groups >= 2 or pass two or more labels.",
        )

    untreated = ~design.treated & (row_group >= 0)
    ever = design.cohort >= 0
    rel = design.rel
    max_leads = int(-rel[untreated & ever].min()) if np.any(untreated & ever) else 0
    if max_leads < 2 and leads is None:
        raise DataInsufficient(
            f"{context}: treated units have at most one untreated period "
            "before adoption, so leads cannot be separated from unit effects.",
            recovery_hint=(
                "Pass leads=1 explicitly only if some units have more " "pre-periods."
            ),
            diagnostics={"max_leads": max_leads},
        )
    if leads is None:
        leads = min(4, max_leads - 1)
    if not isinstance(leads, (int, np.integer)) or leads < 1 or leads > max_leads:
        raise DataInsufficient(
            f"{context}: leads must be between 1 and {max_leads} for this panel.",
            recovery_hint=(
                "Treated units need that many untreated periods before " "adoption."
            ),
            diagnostics={"max_leads": max_leads},
        )
    rows = np.flatnonzero(untreated)
    cols: List[np.ndarray] = []
    index: List[Any] = []
    for g in range(G):
        for kk in range(1, int(leads) + 1):
            col = ((row_group[rows] == g) & ever[rows] & (rel[rows] == -kk)).astype(
                float
            )
            if col.sum() == 0:
                continue
            cols.append(col)
            index.append((labels[g], -kk))
    if not cols:
        raise DataInsufficient(
            f"{context}: no untreated pre-treatment cells within the leads.",
            recovery_hint="Use fewer leads or a panel with pre-periods.",
        )
    n_leads_cols = len(cols)
    if design.control_names:
        C, cnames = fi._candidate_covariates(forest, covariates)
        C = C[:, [cnames.index(c) for c in design.control_names]]
        cols.extend(C[rows].T)
    L = np.column_stack(cols)
    y = design.y[rows]
    u = np.asarray(pd.factorize(pd.Series(unit[rows]))[0], dtype=np.int64)
    if time_effects == "common":
        tt = np.asarray(pd.factorize(pd.Series(time[rows]))[0], dtype=np.int64)
    else:
        key = pd.Series(time[rows].astype(np.int64) * (G + 1) + row_group[rows])
        tt = np.asarray(pd.factorize(key)[0], dtype=np.int64)
    V = _two_way_demean(np.column_stack([y, L]), u, tt)
    yd, Ld = V[:, 0], V[:, 1:]
    XtX = Ld.T @ Ld
    if np.linalg.matrix_rank(XtX) < Ld.shape[1]:
        raise DataInsufficient(
            f"{context}: the lead indicators are collinear with the fixed effects.",
            recovery_hint="Use fewer leads or time_effects='common'.",
        )
    XtX_inv = np.linalg.inv(XtX)
    beta_all = XtX_inv @ (Ld.T @ yd)
    resid = yd - Ld @ beta_all
    cl = design.clusters[rows]
    cl = np.asarray(pd.factorize(pd.Series(cl))[0], dtype=np.int64)
    n_cl = int(cl.max()) + 1
    S = np.zeros((n_cl, Ld.shape[1]))
    np.add.at(S, cl, Ld * resid[:, None])
    n_obs = rows.size
    # Period effects: one redundancy with the unit effects per group of
    # units sharing a set of period dummies (all units for common period
    # effects, each group for group-specific ones).
    n_period_sets = 1 if time_effects == "common" else G
    k_fe_time = int(tt.max()) + 1 - n_period_sets
    unit_nested = bool(pd.Series(cl).groupby(u).nunique().max() == 1)
    K = Ld.shape[1] + k_fe_time + (0 if unit_nested else int(u.max()) + 1)
    factor = n_cl / (n_cl - 1) * (n_obs - 1) / max(n_obs - K, 1)
    vcov_all = factor * XtX_inv @ (S.T @ S) @ XtX_inv
    beta = beta_all[:n_leads_cols]
    vcov = vcov_all[:n_leads_cols, :n_leads_cols]
    se = np.sqrt(np.clip(np.diag(vcov), 0.0, None))
    z = float(stats.norm.ppf(1 - alpha / 2))
    coef = pd.DataFrame(
        {
            "coef": beta,
            "se": se,
            "z": beta / np.where(se > 0, se, np.nan),
            "ci_low": beta - z * se,
            "ci_high": beta + z * se,
        },
        index=pd.MultiIndex.from_tuples(index, names=["group", "lead"]),
    )
    coef["p"] = 2 * stats.norm.sf(np.abs(coef["z"]))

    def _wald(R: np.ndarray) -> Dict[str, float]:
        d = R @ beta
        M = R @ vcov @ R.T
        stat = float(d @ np.linalg.pinv(M) @ d)
        dof = int(np.linalg.matrix_rank(M))
        return {"stat": stat, "df": dof, "p": float(stats.chi2.sf(stat, dof))}

    joint = _wald(np.eye(beta.size))
    rows_R = []
    pos = {key: i for i, key in enumerate(index)}
    for kk in range(1, int(leads) + 1):
        base = (labels[0], -kk)
        if base not in pos:
            continue
        for g in range(1, G):
            key = (labels[g], -kk)
            if key in pos:
                r = np.zeros(beta.size)
                r[pos[key]] = 1.0
                r[pos[base]] = -1.0
                rows_R.append(r)
    equal = (
        _wald(np.vstack(rows_R)) if rows_R else {"stat": np.nan, "df": 0, "p": np.nan}
    )
    group_of_unit = pd.Series(
        [
            labels[c] if c >= 0 else None
            for c in pd.Series(row_group).groupby(unit).first()
        ],
        name="group",
    )
    return {
        "coefficients": coef,
        "joint_zero": joint,
        "equal_across_groups": equal,
        "group_of_unit": group_of_unit,
        "leads": int(leads),
        "n_obs": int(n_obs),
        "n_clusters": n_cl,
        "time_effects": time_effects,
        "controls": list(design.control_names),
        "method": (
            "pre-trend regression on untreated cells with unit and "
            f"{'common' if time_effects == 'common' else 'group-specific'} "
            "period effects and group x lead indicators; CR1 cluster-robust "
            "Wald tests"
        ),
    }
