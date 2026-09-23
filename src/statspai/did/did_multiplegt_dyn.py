"""de Chaisemartin & D'Haultfœuille (2024) intertemporal event-study DiD.

Differs from ``sp.did_multiplegt`` (dCDH 2020 DID_M): the 2020 estimator
is a consecutive-period switcher-vs-stayer pair rollup, while this 2024
estimator is a **long-difference event study** — at each horizon l ≥ 0,
compares ``Y_{F+l} − Y_{F−1}`` between units first switching at F and a
"not-yet-treated at F+l" control group held stable across the horizon.

Verified anchor
---------------
- de Chaisemartin & D'Haultfœuille (2024) "Difference-in-Differences
  Estimators of Intertemporal Treatment Effects", DOI
  ``10.1162/rest_a_01414`` (bib key ``dechaisemartin2024difference``).

Identification details
----------------------
Every item below is pinned against the authors' own implementations:
R ``DIDmultiplegtDYN`` 2.3.4 (Track A module ``78_multiplegt_dyn``,
``tests/reference_parity/test_multiplegt_dyn_parity.py``) and Stata
``did_multiplegt_dyn`` (``tests/stata_parity/78_multiplegt_dyn.do``), plus
the castle-doctrine panel in
``tests/test_did_multiplegt_dyn_castle_reference.py``. Effects, placebos,
switcher counts, the switcher-weighted aggregate and -- since 1.25.1 --
the analytic standard errors agree to better than 1e-6 relative.

1. **Switcher definition**: each unit's FIRST treatment change, in either
   direction, at period F. Switch-off events are switchers too -- that is
   the design's whole point -- and they are handled the way the reference
   does: their controls must share the switcher's BASELINE treatment level
   (a unit going 1 -> 0 belongs against units that were at 1 and stayed),
   and the difference is divided by the change in treatment so both
   directions measure the same effect per unit of treatment.

2. **Control group per horizon l**: "not-yet-treated at F+l" = units
   whose d stays at its pre-F value through F+l inclusive, which is
   what reproduces the R package's per-horizon samples (matching
   switcher and observation counts, not just point estimates). The
   never-treated-only variant is exposed as ``control='never_treated'``
   and is not separately pinned.

3. **Per-horizon estimate**:

       δ_l = Σ_F w_F × {E[Y_{F+l} − Y_{F−1} | switchers at F]
                        − E[Y_{F+l} − Y_{F−1} | not-yet-treated at F+l]}

   with weights ``w_F`` proportional to the (weighted) number of
   switchers at F. The heteroskedastic-weights variant (dCDH 2023 EJ
   survey) is not implemented.

4. **Placebo lag l < 0** is the mirror image of effect ``|l| − 1`` about
   the base period: the outcome contrast is ``Y_{F−1−|l|} − Y_{F−1}``,
   but the *sample* is the one behind effect ``|l| − 1`` -- switchers
   observed at ``F − 1 + |l|`` and controls not yet switched at
   ``F − 1 + |l|`` -- with the extra requirement that ``Y_{F−1−|l|}`` be
   observed. This is what the reference calls the placebo being computed
   "on the same switchers and controls as the corresponding effect".

   .. versionchanged:: 1.26.0
      ⚠️ Placebo lags 2 and deeper used to take the controls not yet
      switched at ``F`` (the lag-1 rule) and did not require the
      switcher to be observed at ``F − 1 + |l|``. That is a different
      quantity: on the castle-doctrine panel ``placebo_2`` moved from
      0.062241 to 0.050966 and ``placebo_3`` from 0.015389 (21
      switchers) to 0.023244 (20 switchers). Placebo 1 was already the
      same object under both rules and is unchanged.

   .. versionchanged:: 1.21.0
      ⚠️ Before 1.21.0 this was ``Y_{F−1−|l|} − Y_{F−1−|l|−1}`` -- a
      one-period difference sliding backwards rather than a mirrored
      long difference.

5. **Inference**: ``se_method='analytic'`` is the authors' influence
   function variance (``U_Gg_var`` in the package source): every
   (g, t) contribution is a *cell-demeaned* residual, ``diff_y − Ê``,
   where the cell is the cohort for a switcher and the (baseline, t)
   control set for a control, multiplied by the small-sample factor
   ``sqrt(n_cell / (n_cell − 1))`` with ``n_cell`` the number of distinct
   clusters in the cell. A cell with a single cluster (e.g. a cohort with
   one switcher) is centred on and scaled by the pooled switcher+control
   cell at that period instead -- without this a lone switcher would
   contribute a zero residual and the variance would be understated.
   Contributions are summed within ``cluster`` before squaring, and the
   variance is ``Σ_c (Σ_{g∈c} U_g)² / G²`` with ``G`` the number of
   groups.

   .. versionchanged:: 1.26.0
      ⚠️ The previous analytic variance used the plain two-sample
      influence function (no DOF factor, zero residual for
      single-switcher cohorts, no cluster summation). It ran 4-18 %
      below the reference on the castle-doctrine panel and ~1 % below
      on the Track A fixture. It now reproduces ``DIDmultiplegtDYN`` /
      Stata ``did_multiplegt_dyn`` to 1e-6 relative on every horizon
      and on the switcher-weighted aggregate. The default stays
      ``'bootstrap'``; ``model_info['se_method']`` records the choice.

Not implemented
---------------
``controls=``, ``trends_nonparam`` / ``trends_lin``, ``normalized``,
``continuous`` and the heteroskedastic-weights variant. Joint tests still
come from the cluster bootstrap. See ``docs/rfc/multiplegt_dyn.md``.
"""

from __future__ import annotations

import warnings
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

from .._aliases import accepts_aliases
from ..core._bootstrap import bootstrap_se as _bootstrap_se
from ..core.results import CausalResult
from ..exceptions import MethodIncompatibility
from . import _core as _dc


@accepts_aliases(
    _strict=True, id="group", unit="group", treat="treatment", weight="weights"
)
def did_multiplegt_dyn(
    data: pd.DataFrame,
    y: str,
    *,
    group: str,
    time: str,
    treatment: str,
    placebo: int = 0,
    dynamic: int = 3,
    control: str = "not_yet_treated",
    cluster: Optional[str] = None,
    weights: Optional[str] = None,
    n_boot: int = 500,
    alpha: float = 0.05,
    seed: Optional[int] = None,
    aggregation: str = "simple",
    se_method: str = "bootstrap",
    switchers: Optional[str] = None,
    same_switchers: bool = False,
    effects_equal: Any = False,
) -> CausalResult:
    """dCDH (2024) intertemporal event-study DiD estimator.

    Parameters
    ----------
    data : DataFrame
    y : str
        Outcome column.
    group : str
        Unit identifier.
    time : str
        Integer-valued period column.
    treatment : str
        Binary time-varying treatment (0/1). Switch-on and switch-off
        events are both used; see ``switchers=`` to separate them.
    placebo : int, default 0
        Number of pre-treatment placebo horizons (l = -1, ..., -placebo).
    dynamic : int, default 3
        Number of post-treatment dynamic horizons (l = 0, ..., dynamic),
        i.e. ``dynamic + 1`` effects. R / Stata ``effects=k`` is
        ``dynamic=k-1`` here: their ``Effect_k`` is horizon ``k-1``.
    control : {'not_yet_treated', 'never_treated'}, default
        ``'not_yet_treated'``.
    cluster : str, optional
        Cluster column (defaults to ``group``). Used by the bootstrap and,
        since 1.25.1, by the analytic variance: influence contributions
        are summed within cluster before squaring, and the small-sample
        cell factor counts distinct clusters, exactly as the reference
        does. ``group`` must be nested in ``cluster``.
    weights : str, optional
        Observation weight column (Stata ``weight()`` / R ``weight=``, whose
        spelling is accepted here as the alias ``weight=``).
        The weight is read at the row a unit contributes from -- period
        ``F+l`` for an effect and ``F-1+|l|`` for a placebo, mirroring the
        reference -- so time-varying weights behave identically. Every
        switcher mean, control mean, cohort weight and the switcher counts
        used by ``aggregation='switchers'`` become weighted; ``detail``
        keeps the raw count in ``n_switchers`` and the weighted one in
        ``w_switchers``. Must be non-negative; a zero or missing weight
        drops the row.
    n_boot : int, default 500
        Bootstrap replications.
    alpha : float, default 0.05
    seed : int, optional
    se_method : {"bootstrap", "analytic"}, default "bootstrap"
        ``"bootstrap"`` resamples clusters; ``"analytic"`` is the authors'
        influence-function variance and needs no draws, which makes it
        roughly a hundred times faster. It is pinned against
        ``DIDmultiplegtDYN`` and Stata ``did_multiplegt_dyn`` to 1e-6
        relative on every horizon and on the switcher-weighted aggregate
        (module docstring, item 5). The default stays on the bootstrap so
        existing callers' numbers do not move; ``model_info["se_method"]``
        records the choice.

        ``joint_placebo_test`` and ``joint_overall_test`` still come from
        the bootstrap, so they are ``None`` when ``n_boot=0``.
    aggregation : {"simple", "switchers"}, default "simple"
        How the dynamic horizons are combined into the headline
        ``estimate``. ``"simple"`` gives each horizon equal weight;
        ``"switchers"`` weights horizon ``l`` by the (weighted) number of
        switchers contributing to it, which reproduces ``DIDmultiplegtDYN``'s
        ``Av_tot_eff`` and its standard error. The two differ whenever
        later horizons rest on fewer cohorts, which is the normal case in
        staggered designs. The default is left on ``"simple"`` because
        changing it would move the number existing callers get back;
        ``model_info["aggregation"]`` records which was used.
    switchers : {None, 'in', 'out'}, optional
        Estimate on switch-**in** events (treatment rises above its
        period-one level) or switch-**out** events (falls below) only.
        Stata ``did_multiplegt_dyn, switchers()``. Default ``None`` pools
        both, which is what StatsPAI has always done.

        dCDH recommend running the two separately: pooling is only
        meaningful if a switch up and a switch down move the outcome by
        the same amount per unit of treatment, which is an assumption, not
        a fact. Splitting is the way to check it.
    same_switchers : bool, default False
        Restrict the treated arm to switchers observed at *every*
        requested horizon (and at the base period), so the composition is
        held fixed across ℓ. Stata ``did_multiplegt_dyn, same_switchers``.

        Without it, later horizons rest on fewer — and differently
        selected — switchers, so a rising or falling ℓ-profile confounds
        the true dynamic path with a moving sample. With it, the profile
        is comparable across ℓ but rests on a smaller sample. Availability
        is judged per unit against the periods that unit is actually
        observed in, so this is correct on unbalanced panels.
    effects_equal : bool or (int, int), default False
        Test H0 that the dynamic effects are all equal. ``True`` tests
        every estimated effect; a ``(lower, upper)`` pair tests the closed
        horizon range, matching Stata ``did_multiplegt_dyn,
        effects_equal()``.

        Reported in ``model_info['effects_equal_test']`` as
        ``{'statistic', 'df', 'pvalue', 'horizons'}``. The statistic is
        χ² on ``k−1`` degrees of freedom for ``k`` effects — one fewer
        than the all-zero joint test, since equality leaves the common
        level unrestricted. Rejecting says the effect moves with exposure
        length; failing to reject does **not** establish a constant effect.

    Returns
    -------
    CausalResult with ``detail`` = per-event decomposition and
    ``model_info['event_study']`` = horizon-level DataFrame matching the
    canonical event-study schema (so ``sp.did_plot`` works).

    Examples
    --------
    >>> import statspai as sp
    >>> import numpy as np, pandas as pd
    >>> rng = np.random.default_rng(0)
    >>> rows = []
    >>> for i in range(20):
    ...     g = int(rng.choice([5, 8, 0]))  # cohort; 0 = never treated
    ...     for t in range(1, 13):
    ...         d = 1 if (g != 0 and t >= g) else 0
    ...         rows.append({'i': i, 't': t, 'd': d,
    ...                      'y': i + 0.1 * t + 1.0 * d + rng.normal(0, 0.4)})
    >>> df = pd.DataFrame(rows)
    >>> r = sp.did_multiplegt_dyn(
    ...     df, y='y', group='i', time='t', treatment='d',
    ...     placebo=2, dynamic=4, n_boot=50, seed=0,
    ... )
    >>> es = r.model_info['event_study']  # horizon-level event study
    >>> bool(len(es) > 0)
    True
    >>> sens = sp.honest_did(r, m_grid=[0.5])  # Rambachan-Roth sensitivity
    """
    if switchers not in (None, "in", "out"):
        raise ValueError(
            f"switchers must be None, 'in' or 'out', got {switchers!r}. "
            "dCDH recommend estimating switch-in and switch-out effects "
            "separately rather than pooling them."
        )
    if control not in {"not_yet_treated", "never_treated"}:
        raise ValueError(
            f"control={control!r} must be 'not_yet_treated' or 'never_treated'"
        )
    if dynamic < 0 or placebo < 0:
        raise ValueError("dynamic and placebo must be non-negative")
    if aggregation not in {"simple", "switchers"}:
        raise ValueError(
            f"aggregation must be 'simple' or 'switchers', got {aggregation!r}"
        )
    se_method = _dc.normalize_se_method(
        se_method,
        supported=("analytic", "bootstrap"),
        function="did_multiplegt_dyn",
        n_clusters=int(data[cluster or group].nunique()),
    )

    df = data.copy()
    for col in (y, group, time, treatment):
        if col not in df.columns:
            raise ValueError(f"Column {col!r} not in data")
    if not set(df[treatment].dropna().unique()) <= {0, 1}:
        raise ValueError(f"Treatment {treatment!r} must be binary 0/1")
    if weights is not None:
        if weights not in df.columns:
            raise MethodIncompatibility(
                f"weights column {weights!r} not in data",
                diagnostics={"weights": weights},
            )
        wv = pd.to_numeric(df[weights], errors="coerce")
        if (wv.dropna() < 0).any():
            raise MethodIncompatibility(
                f"weights column {weights!r} has negative values",
                diagnostics={"weights": weights},
            )
        df[weights] = wv
    if cluster is not None:
        if cluster not in df.columns:
            raise MethodIncompatibility(
                f"cluster column {cluster!r} not in data",
                diagnostics={"cluster": cluster},
            )
        if df[cluster].isna().any():
            raise MethodIncompatibility(
                f"cluster column {cluster!r} has missing values",
                diagnostics={"cluster": cluster},
            )
        if (df.groupby(group)[cluster].nunique() > 1).any():
            raise MethodIncompatibility(
                f"group {group!r} must be nested within cluster {cluster!r}",
                diagnostics={"group": group, "cluster": cluster},
            )

    df = df.sort_values([group, time]).reset_index(drop=True)
    cluster_var = cluster if cluster is not None else group

    # Identify each unit's FIRST switch, in either direction, and which way
    # it went. A unit that turns treatment off is as much a switcher as one
    # that turns it on -- that is the whole point of the dCDH design, and
    # dropping those events (as this used to) silently changes the estimand.
    first_switch, switch_dir, baseline = _first_switch(
        df, group=group, time=time, treatment=treatment
    )
    df = df.merge(first_switch, on=group, how="left")
    df = df.merge(switch_dir, on=group, how="left")
    df = df.merge(baseline, on=group, how="left")

    # Horizons list: placebo (negative) + dynamic (0..H).
    horizons = list(range(-placebo, dynamic + 1))
    # l = -1 is a genuine placebo, not a mechanical zero: it is
    # Y_{F-2} - Y_{F-1} differenced against the controls, which is only
    # zero in expectation under parallel trends. It maps to the R
    # package's Placebo_1.

    main = _estimate_all_horizons(
        df=df,
        y=y,
        group=group,
        time=time,
        treatment=treatment,
        horizons=horizons,
        control=control,
        switchers=switchers,
        same_switchers=same_switchers,
        weights=weights,
        cluster=cluster_var,
    )

    # Cluster bootstrap for SE
    rng = np.random.default_rng(seed)
    boot_hist = np.full((n_boot, len(horizons)), np.nan)
    for b in range(n_boot):
        try:
            bdf = _dc.cluster_bootstrap_draw(
                df,
                cluster_col=cluster_var,
                rng=rng,
                relabel_cols=[group],
            )
            # Recompute the switch date in the bootstrap sample the SAME
            # way the point estimate does.
            #
            # This used to be `min(time | d == 1)`, i.e. "first period
            # treated". That is the first *switch* only for switch-ON
            # units: a unit going 1 → 0 at F got _F = 1, its own first
            # period, which has no base period F−1 and so silently
            # dropped out of every replicate. The point estimate has
            # handled switch-off events since 1.21.0 via _first_switch;
            # the bootstrap was never updated to match, so on any
            # non-absorbing panel the replicates were estimating a
            # different quantity than the estimate whose variance they
            # were supposed to describe.
            bdf = bdf.drop(
                columns=[c for c in ("_F", "_dir", "_base") if c in bdf.columns]
            )
            fs_b, dir_b, base_b = _first_switch(
                bdf, group=group, time=time, treatment=treatment
            )
            bdf = bdf.merge(fs_b, on=group, how="left")
            bdf = bdf.merge(dir_b, on=group, how="left")
            bdf = bdf.merge(base_b, on=group, how="left")
            best = _estimate_all_horizons(
                df=bdf,
                y=y,
                group=group,
                time=time,
                treatment=treatment,
                horizons=horizons,
                control=control,
                switchers=switchers,
                same_switchers=same_switchers,
                weights=weights,
                cluster=cluster_var,
            )
            for j, h in enumerate(horizons):
                # Align by h
                row = next(
                    (r for r in best["cell_estimates"] if r["horizon"] == h), None
                )
                if row is not None:
                    boot_hist[b, j] = row["delta_l"]
        except Exception:
            continue  # replicate stays NaN; bootstrap_se tracks the failure

    # Per-horizon SE + CI
    es_rows: List[Dict[str, Any]] = []
    z_crit = float(stats.norm.ppf(1 - alpha / 2))
    for j, h in enumerate(horizons):
        row = next((r for r in main["cell_estimates"] if r["horizon"] == h), None)
        if row is None:
            es_rows.append(
                {
                    "relative_time": h,
                    "att": np.nan,
                    "se": np.nan,
                    "pvalue": np.nan,
                    "ci_lower": np.nan,
                    "ci_upper": np.nan,
                    "type": "placebo" if h < 0 else "dynamic",
                    "n_switchers": 0,
                }
            )
            continue
        est = row["delta_l"]
        if se_method == "analytic":
            se = row["_se_analytic"]
        else:
            se = _bootstrap_se(boot_hist[:, j], label=f"did.multiplegt_dyn[h={h}]")
        p = (
            float(2 * stats.norm.sf(abs(est / se)))
            if (se > 0 and np.isfinite(se))
            else np.nan
        )
        ci_lo = est - z_crit * se if (se > 0 and np.isfinite(se)) else np.nan
        ci_hi = est + z_crit * se if (se > 0 and np.isfinite(se)) else np.nan
        es_rows.append(
            {
                "relative_time": h,
                "att": float(est) if np.isfinite(est) else np.nan,
                "se": float(se) if np.isfinite(se) else np.nan,
                "pvalue": p,
                "ci_lower": float(ci_lo) if np.isfinite(ci_lo) else np.nan,
                "ci_upper": float(ci_hi) if np.isfinite(ci_hi) else np.nan,
                "type": "placebo" if h < 0 else "dynamic",
                "n_switchers": int(row["n_switchers"]),
            }
        )

    es_df = _dc.event_study_frame(es_rows)

    # Joint covariance of the reported placebos and effects. Analytic: the
    # horizons' clustered influence sums, cross-multiplied -- the same
    # object whose diagonal is each horizon's SE (the reference's
    # sqrt(var_sq_sum)/G). Bootstrap: the covariance of the replicates.
    _ok = [
        (j, h)
        for j, h in enumerate(horizons)
        if np.isfinite(es_rows[j]["se"]) and es_rows[j]["se"] > 0
    ]
    es_vcov = None
    if _ok:
        _labels = [int(h) for _, h in _ok]
        if se_method == "analytic":
            _rows_h = {r["horizon"]: r for r in main["cell_estimates"]}
            _ncl = int(main["cluster_codes"].max()) + 1
            _S = np.column_stack(
                [
                    np.bincount(
                        main["cluster_codes"],
                        weights=_rows_h[h]["_influence"],
                        minlength=_ncl,
                    )
                    for _, h in _ok
                ]
            )
            _V: Optional[np.ndarray] = (_S.T @ _S) / float(main["n_groups"]) ** 2
        else:
            _B = boot_hist[:, [j for j, _ in _ok]]
            _B = _B[np.all(np.isfinite(_B), axis=1)]
            _V = np.cov(_B, rowvar=False, ddof=1) if len(_B) > 1 else None
        if _V is not None:
            es_vcov = pd.DataFrame(np.atleast_2d(_V), index=_labels, columns=_labels)

    # Joint tests
    placebo_idx = [j for j, h in enumerate(horizons) if h < 0]
    dyn_idx = [j for j, h in enumerate(horizons) if h >= 0]

    joint_placebo = _joint_test_from_boot(main, horizons, boot_hist, placebo_idx)
    joint_overall = _joint_test_from_boot(
        main, horizons, boot_hist, placebo_idx + dyn_idx
    )

    # effects_equal: H0 that the dynamic effects share a common value.
    # False disables it; True tests every estimated effect; (lo, hi) tests
    # the closed range, matching Stata's lower/upper bound form.
    equal_test = None
    equal_range = None
    if effects_equal is not False and effects_equal is not None:
        if effects_equal is True:
            sel = dyn_idx
            equal_range = (
                (horizons[dyn_idx[0]], horizons[dyn_idx[-1]]) if dyn_idx else None
            )
        else:
            try:
                lo, hi = effects_equal
            except (TypeError, ValueError):
                raise ValueError(
                    "effects_equal must be False, True, or a (lower, upper) "
                    f"pair of horizons, got {effects_equal!r}."
                ) from None
            lo, hi = int(lo), int(hi)
            if lo > hi:
                raise ValueError(f"effects_equal=({lo}, {hi}) has its bounds reversed.")
            sel = [j for j in dyn_idx if lo <= horizons[j] <= hi]
            if len(sel) < 2:
                raise ValueError(
                    f"effects_equal=({lo}, {hi}) selects {len(sel)} of the "
                    f"estimated effects {[horizons[j] for j in dyn_idx]}; the "
                    "range must cover at least two of them for an equality "
                    "test to mean anything."
                )
            equal_range = (lo, hi)
        equal_test = _effects_equal_test(main, horizons, boot_hist, sel)

    # Headline estimate over the dynamic horizons. "simple" gives each
    # horizon equal weights; "switchers" weights by the (weighted) switchers
    # behind each one, which is DIDmultiplegtDYN's Av_tot_eff.
    dyn_est = np.array(
        [es_rows[j]["att"] for j in dyn_idx],
        dtype=float,
    )
    rows_by_h = {r["horizon"]: r for r in main["cell_estimates"]}

    def _switcher_weight(j: int) -> float:
        r_h = rows_by_h.get(horizons[j])
        return float(r_h["w_switchers"]) if r_h is not None else 0.0

    if not dyn_est.size:
        headline = np.nan
    elif aggregation == "switchers":
        w = np.array([_switcher_weight(j) for j in dyn_idx], dtype=float)
        ok = np.isfinite(dyn_est) & (w > 0)
        headline = (
            float(np.sum(w[ok] * dyn_est[ok]) / np.sum(w[ok])) if ok.any() else np.nan
        )
    else:
        headline = float(np.nanmean(dyn_est))
    # SE: cross-horizon bootstrap of the average. A replicate contributes
    # only when at least one dynamic horizon was estimated; a fully-failed
    # draw stays NaN so bootstrap_se can surface the failure rate.
    if dyn_idx:
        with warnings.catch_warnings():
            # nanmean of an all-NaN replicate row is an intended NaN.
            warnings.simplefilter("ignore", RuntimeWarning)
            if aggregation == "switchers":
                wb = np.array([_switcher_weight(j) for j in dyn_idx], dtype=float)
                sub = boot_hist[:, dyn_idx]
                mask = np.isfinite(sub)
                denom = (mask * wb).sum(axis=1)
                num = np.nansum(np.where(mask, sub, 0.0) * wb, axis=1)
                boot_avg = np.where(
                    denom > 0, num / np.where(denom > 0, denom, 1.0), np.nan
                )
            else:
                boot_avg = np.nanmean(boot_hist[:, dyn_idx], axis=1)
        se_avg = _bootstrap_se(boot_avg, label="did.multiplegt_dyn.headline")
    else:
        se_avg = np.nan
    if se_method == "analytic" and dyn_idx:
        # Combine the horizons' influence functions with the same weights the
        # headline uses, then square once -- the horizons share control units,
        # so adding their variances would understate the spread. This is the
        # reference's U_Gg_var_global: Σ_l w_l U_Gg_var_l with w_l ∝ N_l.
        psis, wts = [], []
        for k, j in enumerate(dyn_idx):
            r_h = rows_by_h.get(horizons[j])
            if r_h is None or not np.isfinite(dyn_est[k]):
                continue
            psis.append(r_h["_influence"])
            wts.append(float(r_h["w_switchers"]) if aggregation == "switchers" else 1.0)
        if psis:
            wv = np.asarray(wts, dtype=float)
            wv = wv / wv.sum()
            psi_head = np.sum([w * p for w, p in zip(wv, psis)], axis=0)
            se_avg = _clustered_if_se(psi_head, main["cluster_codes"], main["n_groups"])

    if se_avg and se_avg > 0:
        z = headline / se_avg
        p_h = float(2 * stats.norm.sf(abs(z)))
        ci_h = (headline - z_crit * se_avg, headline + z_crit * se_avg)
    else:
        p_h = np.nan
        ci_h = (np.nan, np.nan)

    return CausalResult(
        method=(
            "did_multiplegt_dyn (dCDH 2024 ReStat) "
            "[MVP — pinned to DIDmultiplegtDYN for effects, placebos and "
            "analytic SEs; controls/trends variants not implemented]"
        ),
        estimand=(
            "Average dynamic effect across horizons 0..dynamic "
            f"({aggregation}-weighted)"
        ),
        estimate=headline,
        se=se_avg,
        pvalue=p_h,
        ci=ci_h,
        alpha=alpha,
        n_obs=int(len(df)),
        detail=pd.DataFrame(main["cell_estimates"]),
        model_info={
            "event_study": es_df,
            "event_study_vcov": es_vcov,
            "horizons": horizons,
            "control": control,
            "aggregation": aggregation,
            "se_method": se_method,
            "n_boot": n_boot,
            "cluster_var": cluster_var,
            "weights": weights,
            "n_groups": int(main["n_groups"]),
            "joint_placebo_test": joint_placebo,
            "joint_overall_test": joint_overall,
            "effects_equal_test": equal_test,
            "effects_equal_range": equal_range,
            "switchers": switchers,
            "same_switchers": same_switchers,
            "warning": (
                "MVP scope: no controls=, trends_nonparam/trends_lin, "
                "normalized or continuous options and no "
                "heteroskedastic-weights variant; joint tests come from "
                "the bootstrap only. See docs/rfc/multiplegt_dyn.md for "
                "the production roadmap."
            ),
        },
        _citation_key="dechaisemartin2024difference",
    )


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _first_switch(
    df: pd.DataFrame,
    *,
    group: str,
    time: str,
    treatment: str,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Each unit's first treatment change: when, which way, and from what.

    Returns three frames keyed on ``group``: ``_F`` (the period of the first
    change), ``_dir`` (+1 for a switch on, -1 for a switch off) and ``_base``
    (the treatment level held just before it). Units that never change get
    no row and are therefore eligible as controls.

    The baseline matters as much as the direction. A unit turning treatment
    OFF has to be compared with units that were also ON and stayed ON; using
    the never-treated as its control group compares two different
    counterfactuals and does not give the reference's answer.
    """
    F: Dict[Any, Any] = {}
    direction: Dict[Any, int] = {}
    base: Dict[Any, float] = {}
    for uid, u_df in df.sort_values([group, time]).groupby(group, sort=False):
        vals = u_df[treatment].to_numpy()
        times = u_df[time].to_numpy()
        if len(vals) < 2:
            continue
        changed = np.nonzero(np.diff(vals) != 0)[0]
        if changed.size == 0:
            continue
        k = int(changed[0]) + 1
        F[uid] = times[k]
        direction[uid] = 1 if vals[k] > vals[k - 1] else -1
        base[uid] = float(vals[k - 1])
    idx = pd.Index(list(F), name=group)
    return (
        pd.Series(list(F.values()), index=idx, name="_F").reset_index(),
        pd.Series(list(direction.values()), index=idx, name="_dir").reset_index(),
        pd.Series(list(base.values()), index=idx, name="_base").reset_index(),
    )


def _clustered_if_se(
    psi: np.ndarray, cluster_codes: np.ndarray, n_groups: int
) -> float:
    """``sqrt(Σ_c (Σ_{g∈c} ψ_g)²) / G`` -- the reference's ``sqrt(var_sq_sum)/G``.

    ``psi`` is the group-level influence contribution scaled so that its
    mean is the estimate (``G / N`` × raw contribution). With one group per
    cluster this is the plain ``sqrt(mean(ψ²) / G)``.
    """
    sums = np.bincount(
        cluster_codes, weights=psi, minlength=int(cluster_codes.max()) + 1
    )
    return float(np.sqrt(np.sum(sums**2)) / n_groups)


def _estimate_all_horizons(
    *,
    df: pd.DataFrame,
    y: str,
    group: str,
    time: str,
    treatment: str,
    horizons: List[int],
    control: str,
    switchers: Optional[str] = None,
    same_switchers: bool = False,
    weights: Optional[str] = None,
    cluster: Optional[str] = None,
) -> Dict[str, Any]:
    """Compute δ_l for each horizon h using long-difference event-study.

    For each unique first-treatment period F in the sample:
      switchers at F = units with _F == F.
      For each horizon l:
        - If l >= 0: compare Y_{F+l} − Y_{F-1} between switchers and controls
          not yet switched at F+l.
        - If l < 0: compare Y_{F-1-|l|} − Y_{F-1} (placebo) on the SAME
          switchers and controls as effect |l|-1, i.e. the anchor period is
          F-1+|l|. Matches DIDmultiplegtDYN's Placebo_|l|.
      Control set depends on `control=`.

    Aggregate per horizon with (weighted) n_switchers weights, and carry
    the reference's influence-function variance (``U_Gg_var``) per group.
    """
    cells: List[Dict[str, Any]] = []

    # Unit-level index for the influence functions. Each horizon's estimate
    # is a weighted sum of two-sample mean differences, so its influence
    # function is the corresponding sum of within-cell deviations -- and
    # summing rather than adding variances is what carries the fact that a
    # control unit can serve several events.
    all_units = pd.Index(sorted(df[group].unique()))
    n_panel = len(all_units)
    unit_pos = pd.Series(np.arange(n_panel), index=all_units)
    cl_col = cluster if cluster is not None else group
    cluster_of = df.groupby(group)[cl_col].first().reindex(all_units)
    cluster_codes = pd.factorize(cluster_of.to_numpy())[0]

    # switchers=: estimate switch-in and switch-out events separately.
    # dCDH recommend running the command twice rather than pooling, because
    # the two need not measure the same effect per unit of treatment.
    if switchers == "in":
        directions: Tuple[int, ...] = (1,)
    elif switchers == "out":
        directions = (-1,)
    else:
        directions = (1, -1)

    # same_switchers=: hold the switcher composition fixed across horizons.
    # Without it, a longer horizon is estimated on a shrinking, differently
    # composed set of switchers, so movement across ℓ mixes a genuine
    # dynamic path with a change of who is being averaged over.
    if same_switchers and len(horizons) > 1:
        df = _restrict_to_common_switchers(
            df, group=group, time=time, horizons=horizons
        )

    F_values = sorted(df["_F"].dropna().unique())
    if not F_values:
        return {
            "cell_estimates": [],
            "cluster_codes": cluster_codes,
            "n_groups": n_panel,
        }

    # Never-treated set (units with _F NaN)
    never_ids = set(df[df["_F"].isna()][group].unique())
    # Earliest period actually observed -- a horizon whose base period
    # falls before it has no data and is skipped, exactly as the R
    # package drops the cohorts that cannot support a given placebo.
    t_min = float(df[time].min())

    for h in horizons:
        sum_wdelta = 0.0
        w_total = 0.0
        n_sw = 0
        n_events = 0
        psi = np.zeros(n_panel, dtype=float)

        for F in F_values:
            for direction in directions:
                _cell = _one_event(
                    df=df,
                    y=y,
                    group=group,
                    time=time,
                    treatment=treatment,
                    F=F,
                    h=h,
                    direction=direction,
                    control=control,
                    never_ids=never_ids,
                    t_min=t_min,
                    n_panel=n_panel,
                    unit_pos=unit_pos,
                    weights=weights,
                    cluster_of=cluster_of,
                )
                if _cell is None:
                    continue
                sum_wdelta += _cell["delta"] * _cell["w_sw"]
                w_total += _cell["w_sw"]
                n_sw += _cell["n_sw"]
                n_events += 1
                psi += _cell["psi"]

        if w_total > 0:
            delta_l = sum_wdelta / w_total
            # Reference scaling: U_Gg = (G / N_l) × Σ_t contribution_gt.
            psi = np.asarray(psi * (n_panel / w_total), dtype=float)
            se_analytic = _clustered_if_se(psi, cluster_codes, n_panel)
        else:
            delta_l = np.nan
            se_analytic = np.nan

        cells.append(
            {
                "horizon": h,
                "delta_l": float(delta_l) if np.isfinite(delta_l) else np.nan,
                "n_switchers": n_sw,
                "w_switchers": float(w_total),
                "n_events": n_events,
                "_influence": psi,
                "_se_analytic": se_analytic,
            }
        )

    return {
        "cell_estimates": cells,
        "cluster_codes": cluster_codes,
        "n_groups": n_panel,
    }


def _cell_centre(
    n_own: int, mean_own: float, n_pool: int, mean_pool: float
) -> Tuple[float, float]:
    """(Ê, DOF) for one cell of the reference variance.

    ``compute_E_hat_gt`` / ``compute_DOF_gt`` in ``DIDmultiplegtDYN``: a cell
    with at least two clusters is centred on its own mean and scaled by
    ``sqrt(n/(n-1))``; a single-cluster cell borrows the pooled
    switcher+control cell at the same period; a cell that cannot even do
    that is left uncentred with factor 1.
    """
    if n_own >= 2:
        return mean_own, float(np.sqrt(n_own / (n_own - 1.0)))
    if n_pool >= 2:
        return mean_pool, float(np.sqrt(n_pool / (n_pool - 1.0)))
    return 0.0, 1.0


def _one_event(
    *,
    df: pd.DataFrame,
    y: str,
    group: str,
    time: str,
    treatment: str,
    F: Any,
    h: int,
    direction: int,
    control: str,
    never_ids: set,
    t_min: float,
    n_panel: int,
    unit_pos: pd.Series,
    weights: Optional[str],
    cluster_of: pd.Series,
) -> Optional[Dict[str, Any]]:
    """One (switch period, direction) event at horizon ``h``.

    Three things distinguish a switch-off event from a switch-on one, and
    all three matter:

    * Its controls must share its BASELINE treatment level, not merely be
      untreated. A unit going 1 -> 0 belongs against units that were at 1
      and stayed there; comparing it with the never-treated is a different
      counterfactual and gives a different number.
    * The difference is divided by the change in treatment, so a switch-off
      contributes with the opposite sign and both directions measure the
      same "effect per unit of treatment".
    * It is otherwise an ordinary two-sample comparison, so the influence
      function has the same shape.

    The *anchor* period ``F − 1 + i`` (``i = h + 1`` for an effect,
    ``i = |h|`` for a placebo) decides the sample: a unit must be observed
    there, controls must not have switched by then, and ``weights`` is read
    there. For a placebo the outcome contrast is nonetheless the mirrored
    ``Y_{F−1−i} − Y_{F−1}``.
    """
    sw_mask = (df["_F"] == F) & (df["_dir"] == direction)
    if "_elig" in df.columns:
        # same_switchers: this unit switches at F but cannot support every
        # requested horizon, so it must not contribute an effect. It stays
        # in the frame as a control candidate.
        sw_mask &= df["_elig"]
    switchers = df[sw_mask]
    if switchers.empty:
        return None
    switcher_ids = set(switchers[group].unique())
    base_level = float(switchers["_base"].iloc[0])

    if h >= 0:
        t_pre, t_post = F - 1, F + h
        t_anchor = t_post
    else:
        i = -h
        t_pre, t_post = F - 1 - i, F - 1
        t_anchor = F - 1 + i
    if t_pre < t_min:
        return None

    # Controls: never-switchers plus units that have not switched by the
    # anchor period, restricted to the switcher's baseline level.
    if control == "never_treated":
        candidates = never_ids
    else:
        candidates = set(df[(df["_F"] > t_anchor) | (df["_F"].isna())][group].unique())
    pre_rows = df[df[time] == t_pre]
    same_base = set(pre_rows[pre_rows[treatment] == base_level][group].unique())
    ctrl_ids = (candidates & same_base) - switcher_ids
    if not ctrl_ids:
        return None

    sw = _event_sample(
        df, group, time, y, weights, switcher_ids, t_pre, t_post, t_anchor
    )
    ct = _event_sample(df, group, time, y, weights, ctrl_ids, t_pre, t_post, t_anchor)
    if sw is None or ct is None:
        return None
    sw_ids, sw_dy, sw_w = sw
    c_ids, c_dy, c_w = ct

    w_s = float(sw_w.sum())
    w_c = float(c_w.sum())
    mean_s = float(np.sum(sw_w * sw_dy) / w_s)
    mean_c = float(np.sum(c_w * c_dy) / w_c)
    scale = (-1.0 if h < 0 else 1.0) / direction
    delta = scale * (mean_s - mean_c)

    # Reference variance cells: the cohort for switchers, the (baseline, t)
    # control set for controls, and the pooled cell as the fallback when a
    # cell holds a single cluster. Cluster counts, weighted means.
    n_s = int(cluster_of.loc[sw_ids].nunique())
    n_c = int(cluster_of.loc[c_ids].nunique())
    n_pool = int(cluster_of.loc[sw_ids.append(c_ids)].nunique())
    mean_pool = float((np.sum(sw_w * sw_dy) + np.sum(c_w * c_dy)) / (w_s + w_c))
    e_s, dof_s = _cell_centre(n_s, mean_s, n_pool, mean_pool)
    e_c, dof_c = _cell_centre(n_c, mean_c, n_pool, mean_pool)

    psi = np.zeros(n_panel, dtype=float)
    psi[unit_pos.reindex(sw_ids).to_numpy()] += sw_w * dof_s * (sw_dy - e_s)
    psi[unit_pos.reindex(c_ids).to_numpy()] -= (w_s / w_c) * c_w * dof_c * (c_dy - e_c)
    psi *= scale

    return {"delta": float(delta), "n_sw": int(len(sw_ids)), "w_sw": w_s, "psi": psi}


def _unit_values(
    df: pd.DataFrame,
    group: str,
    time: str,
    y: str,
    ids: Any,
    t: Any,
) -> pd.Series:
    """``y`` at period ``t`` for the given units, indexed by unit, NaN dropped."""
    sub = df[(df[time] == t) & df[group].isin(ids)]
    s = sub.set_index(group)[y].astype(float)
    return s[s.notna()]


def _event_sample(
    df, group, time, y, weights, ids, t_pre, t_post, t_anchor
) -> Optional[Tuple[pd.Index, np.ndarray, np.ndarray]]:
    """Units observed at every period the event needs, with their change and weights.

    Only units observed at BOTH ends of the contrast (and at the anchor
    period, which for a placebo is a third period) contribute -- a unit
    missing any of them has no change and cannot enter the difference. The
    weights is the reference's ``N_gt`` at the anchor row; zero or missing
    weights drop the unit.
    """
    pre = _unit_values(df, group, time, y, ids, t_pre)
    post = _unit_values(df, group, time, y, ids, t_post)
    idx = pre.index.intersection(post.index)
    if t_anchor != t_post:
        anchor = _unit_values(df, group, time, y, ids, t_anchor)
        idx = idx.intersection(anchor.index)
    if len(idx) == 0:
        return None
    if weights is None:
        w = np.ones(len(idx), dtype=float)
    else:
        sub = df[(df[time] == t_anchor) & df[group].isin(idx)].set_index(group)[weights]
        w = sub.reindex(idx).astype(float).fillna(0.0).to_numpy()
        keep = w != 0
        if not keep.any():
            return None
        idx = idx[keep]
        w = w[keep]
    dy = (post.loc[idx] - pre.loc[idx]).to_numpy(dtype=float)
    return idx, dy, w


def _restrict_to_common_switchers(
    df: pd.DataFrame,
    *,
    group: str,
    time: str,
    horizons: List[int],
) -> pd.DataFrame:
    """Drop switchers that cannot support every requested horizon.

    Stata ``did_multiplegt_dyn, same_switchers``. A switcher at F
    contributes to horizon ℓ only if it is observed at both the base
    period F−1 and the comparison period F+ℓ. Panels being what they are,
    late switchers drop out of long horizons and early ones drop out of
    deep placebos — so the ℓ-profile silently mixes the dynamic path with
    a moving composition. Restricting to switchers observed at *every*
    requested period removes that confound, at the cost of sample size.

    Availability is checked per unit against the periods that unit is
    actually observed in, not against the global panel range, so the
    restriction is correct on unbalanced panels.

    Control units (``_F`` NaN) are never dropped: the restriction is about
    the composition of the treated arm.
    """
    # Judged on the EFFECTS (h >= 0) plus the base period F-1, not on the
    # placebos: Stata scopes same_switchers to the effects and has a
    # separate same_switchers_pl for extending it to the placebos.
    need = sorted({-1, *(h for h in horizons if h >= 0)})
    obs = df.groupby(group)[time].apply(set)
    f_of = df.groupby(group)["_F"].first()

    eligible = {}
    for uid, f_val in f_of.items():
        if pd.isna(f_val):
            eligible[uid] = True  # never-switchers are controls, not switchers
            continue
        periods = obs.loc[uid]
        eligible[uid] = all((f_val + h) in periods for h in need)

    # Flag rather than filter. A restricted switcher must stay in the frame
    # with its `_F` intact, because control eligibility is decided from
    # `_F` (`not yet treated at F+l`): dropping the rows would promote a
    # unit that really does switch at F=8 out of the data entirely, and
    # silently shrink the control pool available to the F=4 and F=6
    # events. Blanking `_F` would be worse still — it would promote that
    # unit to a *never*-switcher and let it serve as a control at horizons
    # where it is already treated.
    out = df.copy()
    out["_elig"] = out[group].map(eligible).fillna(True).astype(bool)
    return out


def _effects_equal_test(
    main: Dict[str, Any],
    horizons: List[int],
    boot_hist: np.ndarray,
    indices: List[int],
) -> Optional[Dict[str, Any]]:
    """Wald test of H0: every effect in ``indices`` is equal.

    Stata ``did_multiplegt_dyn, effects_equal``. Differencing adjacent
    effects turns "all equal" into "all contrasts zero", so the existing
    :func:`joint_wald` applies once the contrast matrix R has been pushed
    through both the estimates and the bootstrap covariance::

        H0: δ_1 = δ_2 = ... = δ_k   <=>   R δ = 0,  R = [e_j - e_{j+1}]

    Under the null the statistic is χ²(k−1) — one fewer degree of freedom
    than the corresponding all-zero test, because equality leaves the
    common level free.

    Returns ``None`` when fewer than two effects are available (nothing to
    compare) or the bootstrap has too few usable draws to form R V R'.
    """
    if len(indices) < 2:
        return None
    est = np.array(
        [
            next(
                (
                    r["delta_l"]
                    for r in main["cell_estimates"]
                    if r["horizon"] == horizons[j]
                ),
                np.nan,
            )
            for j in indices
        ],
        dtype=float,
    )
    if np.any(np.isnan(est)):
        return None

    sub = boot_hist[:, indices]
    valid = ~np.any(np.isnan(sub), axis=1)
    if valid.sum() < len(indices) + 1:
        return None
    cov = np.cov(sub[valid], rowvar=False, ddof=1)
    if cov.ndim == 0:
        cov = np.array([[float(cov)]])

    k = len(indices)
    contrast = np.zeros((k - 1, k))
    for r in range(k - 1):
        contrast[r, r] = 1.0
        contrast[r, r + 1] = -1.0

    out = _dc.joint_wald(contrast @ est, contrast @ cov @ contrast.T)
    out["horizons"] = [horizons[j] for j in indices]
    return out


def _joint_test_from_boot(
    main: Dict[str, Any],
    horizons: List[int],
    boot_hist: np.ndarray,
    indices: List[int],
) -> Optional[Dict[str, Any]]:
    if not indices:
        return None
    est = np.array(
        [
            next(
                (
                    r["delta_l"]
                    for r in main["cell_estimates"]
                    if r["horizon"] == horizons[j]
                ),
                np.nan,
            )
            for j in indices
        ],
        dtype=float,
    )
    sub = boot_hist[:, indices]
    valid = ~np.any(np.isnan(sub), axis=1)
    if valid.sum() < len(indices) + 1:
        return None
    cov = np.cov(sub[valid], rowvar=False, ddof=1)
    if cov.ndim == 0:
        cov = np.array([[float(cov)]])
    return _dc.joint_wald(est, cov)
