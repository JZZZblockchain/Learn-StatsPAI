r"""
Gardner (2021) two-stage DID estimator (a.k.a. ``did2s``).

The **two-stage DID** method of Gardner (2021) recovers the ATT under staggered
treatment adoption by a two-step regression:

1. **Stage 1 — Fit FE model on untreated rows only.**
   Using observations where the unit is *not yet* treated, regress the outcome
   on unit and time fixed effects (plus any covariates):

       Y_it = alpha_i + lambda_t + X_it' beta + e_it    for (i, t) untreated.

2. **Stage 2 — Residualise + regress on treatment.**
   Construct the residualised outcome  Y_tilde_it = Y_it - (predicted from
   Stage 1), and fit a pooled regression on treatment dummies (either a single
   ATT or an event-study by relative time):

       Y_tilde_it = tau * D_it + u_it.

The default standard errors (``vce='analytic'``) are the *corrected* clustered
variance of Gardner (2022) as implemented by R ``did2s::did2s`` and Stata
``did2s``: the Stage-2 cluster sandwich is built from the two-stage influence
function, so the estimation error of the Stage-1 fixed effects propagates into
the Stage-2 variance instead of being treated as known. Writing ``X1`` for the
Stage-1 design, ``X10`` for that design with treated rows zeroed, ``e1`` for
the Stage-1 residual (zero on treated rows), ``X2`` / ``e2`` for the Stage-2
design and residual, and ``g`` for clusters::

    gamma = (X10' X10)^{-1} X1' X2
    s_g   = sum_{i in g} ( x2_i e2_i  -  gamma' x10_i e1_i )
    V     = (X2' X2)^{-1} [ sum_g s_g s_g' ] (X2' X2)^{-1}

with no small-sample cluster factor, exactly as the two reference
implementations. ``vce='stage2'`` recovers the previous default, which
clustered the Stage-2 residuals only and therefore understated uncertainty
(about 26% low on the mpdta fixture); ``vce='bootstrap'`` resamples whole
clusters and re-runs both stages. The estimator closely parallels the
Borusyak-Jaravel-Spiess (2024) imputation estimator numerically, but the
two-step regression framing makes event studies and covariate interactions
trivial.

References
----------
[@gardner2022twostage] Gardner (2022), "Two-stage differences in differences."
[@butts2022stage] Butts and Gardner (2022), "did2s: Two-Stage
    Difference-in-Differences", *The R Journal*.
"""

from __future__ import annotations

import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats as sp_stats

from .._aliases import accepts_aliases
from ..core._bootstrap import bootstrap_se as _bootstrap_se
from ..core.results import CausalResult

__all__ = ["gardner_did", "did_2stage"]


def _gardner_cluster_bootstrap(
    df: pd.DataFrame,
    y: str,
    group: str,
    time: str,
    first_treat: str,
    controls: List[str],
    event_study: bool,
    horizon: Optional[List[int]],
    cluster: str,
    names: List[str],
    n_boot: int,
    seed: int,
) -> Tuple[Dict[str, float], float]:
    """Pairs-cluster bootstrap of the *full* Gardner two-step procedure.

    Resamples whole clusters and re-runs both stages, so the Stage-1
    estimation error enters the SE by construction. This is the
    ``bootstrap = TRUE`` path of ``did2s::did2s``; the default analytic SE
    reaches the same target through the corrected influence function
    (:func:`_did2s_corrected_vcov`). Returns ``(per_coef_se, overall_att_se)``.
    """
    rng = np.random.default_rng(seed)
    clusters = pd.unique(df[cluster])
    n_g = len(clusters)
    rows_by_cluster = {c: df[df[cluster] == c] for c in clusters}
    ctrl = controls if controls else None

    n_boot_int = int(n_boot)
    # Pre-size to the full attempt count so failed replicates stay NaN and
    # bootstrap_se can surface the failure rate loudly (CLAUDE.md §3.7)
    # instead of silently computing the SD over survivors only.
    boot_overall = np.full(n_boot_int, np.nan, dtype=float)
    boot_coefs: Dict[str, np.ndarray] = {
        nm: np.full(n_boot_int, np.nan, dtype=float) for nm in names
    }
    for b in range(n_boot_int):
        drawn = rng.choice(n_g, size=n_g, replace=True)
        parts = []
        for j, ci in enumerate(drawn):
            sub = rows_by_cluster[clusters[ci]].copy()
            # Fresh, globally-unique ids so a cluster drawn twice (and the
            # units inside it) do not collide in the re-estimation.
            sub[group] = sub[group].astype(str) + f"__b{j}"
            sub["__bcl"] = j
            parts.append(sub)
        bd = pd.concat(parts, ignore_index=True)
        try:
            r = gardner_did(
                bd,
                y=y,
                group=group,
                time=time,
                first_treat=first_treat,
                controls=ctrl,
                event_study=event_study,
                horizon=horizon,
                cluster="__bcl",
                vce="none",
            )
        except Exception:
            continue  # replicate stays NaN; bootstrap_se tracks the failure
        if np.isfinite(r.estimate):
            boot_overall[b] = float(r.estimate)
        es = r.model_info.get("event_study") if event_study else None
        if es:
            for nm in names:
                boot_coefs[nm][b] = float(es["coef"].get(nm, np.nan))
        elif names:
            # Static mode: the single coefficient *is* the overall ATT.
            # Filling it here keeps bootstrap_se from reporting a false
            # "0/n replicates succeeded" for a series that was never used.
            boot_coefs[names[0]][b] = boot_overall[b]

    overall_se = _bootstrap_se(boot_overall, label="did.gardner.overall")
    se_dict: Dict[str, float] = {}
    for nm in names:
        se_dict[nm] = _bootstrap_se(boot_coefs[nm], label=f"did.gardner[{nm}]")
    if not event_study and names:
        se_dict[names[0]] = overall_se
    return se_dict, overall_se


def _cluster_vcov(
    X: np.ndarray,
    resid: np.ndarray,
    cluster: np.ndarray,
) -> np.ndarray:
    """Liang-Zeger cluster-robust variance for an OLS coefficient vector."""
    n, k = X.shape
    xtx_inv = np.linalg.pinv(X.T @ X)
    clusters = np.unique(cluster)
    G = len(clusters)
    meat = np.zeros((k, k))
    for g in clusters:
        mask = cluster == g
        xg = X[mask]
        eg = resid[mask]
        s = xg.T @ eg
        meat += np.outer(s, s)
    if G > 1 and n > k:
        dof = G / (G - 1) * (n - 1) / (n - k)
    else:
        dof = 1.0
    return np.asarray(dof * xtx_inv @ meat @ xtx_inv, dtype=float)


def _did2s_corrected_vcov(
    X2: np.ndarray,
    resid2: np.ndarray,
    X1: np.ndarray,
    untreated: np.ndarray,
    resid1: np.ndarray,
    cluster: np.ndarray,
) -> np.ndarray:
    """Two-stage (did2s) corrected cluster-robust variance of the Stage-2 OLS.

    Implements the corrected clustered variance of Gardner (2022) exactly as
    ``did2s::did2s`` (R, 1.2.1) and Stata ``did2s`` build it. With ``X10``
    the Stage-1 design ``X1`` with treated rows zeroed and ``e1`` the Stage-1
    residual (also zero on treated rows), the per-observation influence
    contribution to the Stage-2 score is ``x2_i e2_i - gamma' x10_i e1_i``
    where ``gamma = (X10'X10)^{-1} X1'X2`` maps Stage-1 coefficient error into
    the Stage-2 score. Summing within clusters and sandwiching with
    ``(X2'X2)^{-1}`` gives the variance. No small-sample cluster factor is
    applied, matching both references (the Stage-2-only
    :func:`_cluster_vcov` applies ``G/(G-1) (n-1)/(n-k)``).

    Rank-deficient ``X10'X10`` (a unit or period with no untreated rows)
    falls back to the Moore-Penrose inverse, mirroring
    ``did2s:::robust_solve_XtX``.

    Parameters
    ----------
    X2, resid2
        Stage-2 design (``n x k2``) and residual.
    X1, untreated, resid1
        Stage-1 design on *all* rows (``n x k1``), the untreated-row mask,
        and the Stage-1 residual on all rows (only untreated entries are
        used).
    cluster
        Cluster labels, length ``n``.
    """
    from scipy import linalg as sp_linalg

    untreated = np.asarray(untreated, dtype=bool)
    X10 = np.where(untreated[:, None], X1, 0.0)
    e1 = np.where(untreated, resid1, 0.0)
    gram1 = X10.T @ X10
    x1t_x2 = X1.T @ X2
    try:
        chol = sp_linalg.cho_factor(gram1, lower=True, check_finite=False)
        gamma = sp_linalg.cho_solve(chol, x1t_x2, check_finite=False)
    except (np.linalg.LinAlgError, sp_linalg.LinAlgError):
        gamma = np.linalg.pinv(gram1, hermitian=True) @ x1t_x2
    # n x k2 influence contributions (sign is irrelevant for the outer product).
    score = X2 * resid2[:, None] - (X10 @ gamma) * e1[:, None]
    codes, uniq = pd.factorize(np.asarray(cluster))
    sums = np.zeros((len(uniq), X2.shape[1]))
    np.add.at(sums, codes, score)
    meat = sums.T @ sums
    xtx_inv = np.linalg.pinv(X2.T @ X2, hermitian=True)
    return np.asarray(xtx_inv @ meat @ xtx_inv, dtype=float)


def _build_fe_design(
    unit: np.ndarray,
    time: np.ndarray,
    X: Optional[np.ndarray],
    *,
    u_levels: Optional[np.ndarray] = None,
    t_levels: Optional[np.ndarray] = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build (intercept, unit dummies minus one, time dummies minus one, X).

    When ``u_levels``/``t_levels`` are provided, builds the design against that
    reference set of levels (useful for prediction on a different sample).
    """
    if u_levels is None:
        u_levels = np.unique(unit)
    if t_levels is None:
        t_levels = np.unique(time)

    n = len(unit)
    # Intercept
    intercept = np.ones((n, 1))
    # Unit dummies drop first level
    D_u = np.zeros((n, max(len(u_levels) - 1, 0)))
    for j, lvl in enumerate(u_levels[1:]):
        D_u[:, j] = (unit == lvl).astype(float)
    # Time dummies drop first level
    D_t = np.zeros((n, max(len(t_levels) - 1, 0)))
    for j, lvl in enumerate(t_levels[1:]):
        D_t[:, j] = (time == lvl).astype(float)

    parts = [intercept, D_u, D_t]
    if X is not None and X.size > 0:
        parts.append(X)
    A = np.hstack(parts)
    return A, u_levels, t_levels


@accepts_aliases(_strict=True, id="group", unit="group", covariates="controls")
def gardner_did(
    data: pd.DataFrame,
    y: str,
    group: str,
    time: str,
    first_treat: str,
    controls: Optional[List[str]] = None,
    event_study: bool = False,
    horizon: Optional[List[int]] = None,
    cluster: Optional[str] = None,
    alpha: float = 0.05,
    vce: str = "analytic",
    n_boot: int = 199,
    boot_seed: int = 0,
) -> CausalResult:
    """Gardner (2021) two-stage DID estimator.

    Parameters
    ----------
    data : pd.DataFrame
        Long-format panel.
    y : str
        Outcome column name.
    group : str
        Unit (panel-id) column.
    time : str
        Time column.
    first_treat : str
        First-treatment-period column.  Never-treated units should be encoded
        as ``0``, ``NaN``, or ``+inf``.
    controls : list of str, optional
        Additional covariates included in both stages.
    event_study : bool, default False
        If True, Stage 2 reports coefficients by relative time
        ``k = t - first_treat_i``.
    horizon : list of int, optional
        Relative-time leads/lags to report when ``event_study=True``;
        defaults to ``range(-5, 6)`` intersected with available support.
    cluster : str, optional
        Cluster variable for Stage-2 SEs.  Defaults to ``group``.
    alpha : float, default 0.05
        Two-sided CI level.
    vce : {'analytic', 'stage2', 'bootstrap', 'none'}, default 'analytic'
        Standard-error mode. ``'analytic'`` is the two-stage corrected
        clustered variance of Gardner (2022): the Stage-2 cluster sandwich is
        built from the influence function of *both* stages, so the estimation
        error of the Stage-1 fixed effects is propagated. It reproduces R
        ``did2s::did2s`` and Stata ``did2s`` (rel < 1e-6 on the mpdta
        fixture) and carries no small-sample cluster factor, as they do not.
        ``'stage2'`` is the previous default: it clusters the Stage-2 residuals
        alone (with the ``G/(G-1)(n-1)/(n-k)`` factor) as if the imputed
        counterfactual were known data, and understates uncertainty (about
        26% low on mpdta; empirically ~0.78 coverage at a nominal 95% level).
        It is kept so earlier numbers can be reproduced and emits a
        ``UserWarning``. ``'bootstrap'`` resamples whole clusters and re-runs
        the full two-step procedure (``did2s(bootstrap = TRUE)``). ``'none'``
        is the fast internal path used by the bootstrap replicates (Stage-2
        SE, no warning). Point estimates are identical in every mode.
    n_boot : int, default 199
        Number of cluster-bootstrap replications when ``vce='bootstrap'``.
    boot_seed : int, default 0
        Seed for the cluster bootstrap (deterministic results).

    Returns
    -------
    CausalResult
        ``.estimate`` is the overall ATT; ``.model_info['event_study']``
        carries the event-study dict when requested.  Supplies ``.summary()``,
        ``.cite()``, and is compatible with ``sp.outreg2()``.

    Notes
    -----
    Identification requires the usual staggered-DID conditions (parallel
    trends, no anticipation) plus a linear two-way FE + additive covariate
    structure for the untreated potential outcome.  Standard errors cluster
    by ``cluster`` (default: unit). In event-study mode the per-horizon SEs
    come from the same corrected variance (each horizon dummy is a Stage-2
    regressor), and the overall ATT is the treated-observation-weighted mean
    of the post-treatment horizons with its SE taken from the full
    cross-horizon covariance; ``model_info['event_study']['vcov']`` carries
    that covariance. Units with no untreated observation make the Stage-1
    Gram matrix rank deficient; the variance then uses the Moore-Penrose
    inverse, as ``did2s`` does.

    References
    ----------
    [@gardner2022twostage] Gardner (2022), "Two-stage differences in
    differences."
    [@butts2022stage] Butts and Gardner (2022), "did2s: Two-Stage
    Difference-in-Differences", *The R Journal*.

    Examples
    --------
    Staggered panel with a never-treated group (``first_treat = 0``).
    ``sp.did_2stage`` is an alias of this function.

    >>> import numpy as np
    >>> import pandas as pd
    >>> import statspai as sp
    >>> rng = np.random.default_rng(42)
    >>> n_units, n_periods = 40, 8
    >>> unit = np.repeat(np.arange(n_units), n_periods)
    >>> time = np.tile(np.arange(1, n_periods + 1), n_units)
    >>> first = np.where(unit < 20, 5, 0)  # 0 = never treated
    >>> d = ((first > 0) & (time >= first)).astype(float)
    >>> y = (0.5 * unit + 0.3 * time + 2.0 * d
    ...      + rng.normal(0, 0.5, unit.size))
    >>> df = pd.DataFrame(
    ...     {"y": y, "unit": unit, "time": time, "g": first}
    ... )
    >>> res = sp.gardner_did(
    ...     df, y="y", group="unit", time="time", first_treat="g"
    ... )
    >>> round(res.estimate, 2)  # true ATT = 2.0
    2.03
    """
    if vce not in ("analytic", "stage2", "bootstrap", "none"):
        raise ValueError(
            "vce must be 'analytic', 'stage2', 'bootstrap', or 'none'; " f"got {vce!r}"
        )
    if controls is None:
        controls = []
    df = data.copy()
    for col in [y, group, time, first_treat] + controls:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in data")

    df[y] = pd.to_numeric(df[y], errors="coerce")
    df = df.dropna(subset=[y, group, time, first_treat]).reset_index(drop=True)

    if cluster is None:
        cluster = group
    elif cluster not in df.columns:
        raise ValueError(f"cluster column '{cluster}' not found")

    ft = df[first_treat].to_numpy(dtype=float)
    t_arr = df[time].to_numpy(dtype=float)
    treated_now = np.array(
        [(np.isfinite(fi) and fi > 0 and ti >= fi) for fi, ti in zip(ft, t_arr)]
    )
    df["_D"] = treated_now.astype(float)

    # ── Stage 1: FE + covariate regression on untreated rows ────── #
    untreated_mask = ~treated_now
    if untreated_mask.sum() < 10:
        raise ValueError("Not enough untreated observations for Stage 1 (<10).")

    unit_all = df[group].to_numpy()
    time_all = df[time].to_numpy()
    X_all = df[controls].to_numpy(dtype=float) if controls else np.zeros((len(df), 0))

    # Stage-1 fit: design against ALL units/times seen in the data; rows from
    # untreated subset only.  Units that appear only in treated rows simply
    # get a zero dummy — they contribute nothing to the untreated fit but can
    # still be predicted (via intercept + time FE only).
    u_levels = np.unique(unit_all)
    t_levels = np.unique(time_all)

    A_un, _, _ = _build_fe_design(
        unit_all[untreated_mask],
        time_all[untreated_mask],
        X_all[untreated_mask] if controls else None,
        u_levels=u_levels,
        t_levels=t_levels,
    )
    y_un = df.loc[untreated_mask, y].to_numpy(dtype=float)

    coefs, *_ = np.linalg.lstsq(A_un, y_un, rcond=None)

    # Predict counterfactual Y(0) for all rows using Stage-1 coefficients.
    A_full, _, _ = _build_fe_design(
        unit_all,
        time_all,
        X_all if controls else None,
        u_levels=u_levels,
        t_levels=t_levels,
    )
    y_all_arr = df[y].to_numpy(dtype=float)
    y_hat_0 = A_full @ coefs
    y_tilde = y_all_arr - y_hat_0

    # ── Stage 2: recover treatment effects from the imputed gap ──── #
    # Overall ATT: clustered OLS of ỹ on the treatment indicator, with
    # an intercept to absorb any mean residual in the untreated rows.
    # Event study: direct within-(cohort × relative-time) averaging of ỹ
    # — the Borusyak-Jaravel-Spiess style — to avoid the reference-
    # category contamination bias that a Stage-2 dummy regression would
    # introduce (the "baseline" in a dummy regression lumps never-treated
    # units together with treated units outside the event-study horizon,
    # pulling every coefficient toward the residual mean).
    cl = df[cluster].to_numpy()
    if event_study:
        rel_time = np.where(
            np.isfinite(ft) & (ft > 0),
            t_arr - ft,
            np.inf,  # never-treated → excluded
        )
        if horizon is None:
            support = np.unique(rel_time[np.isfinite(rel_time)])
            horizon = [int(k) for k in support if -5 <= int(k) <= 5]
            if 0 not in horizon:
                horizon.append(0)
            horizon = sorted(set(horizon))

        names, est_list, se_list, count_list, mask_list = [], [], [], [], []
        for k in horizon:
            key = f"D_k{int(k):+d}"
            names.append(key)
            mask = rel_time == k
            mask_list.append(mask)
            n_k = int(mask.sum())
            count_list.append(n_k)
            if n_k == 0:
                est_list.append(float("nan"))
                se_list.append(float("nan"))
                continue
            y_k = y_tilde[mask]
            coef_k = float(np.mean(y_k))
            # Stage-2-only cluster-robust SE of the within-bin mean (the
            # 'stage2' / 'none' modes; overwritten below for 'analytic').
            cl_k = cl[mask]
            uniq = np.unique(cl_k)
            G = len(uniq)
            if G > 1:
                # SE of the unweighted mean over n rows, allowing cluster
                # correlation: Var(mean) ≈ (1/n²) Σ_g (Σ_{i∈g} (y_ki - coef))²
                sq = 0.0
                for g in uniq:
                    idx = cl_k == g
                    sq += float(np.sum(y_k[idx] - coef_k)) ** 2
                var_k = sq / (len(y_k) ** 2)
                se_k = float(np.sqrt(max(var_k, 0.0)))
            else:
                se_k = float(np.std(y_k, ddof=1) / np.sqrt(len(y_k)))
            est_list.append(coef_k)
            se_list.append(se_k)
        est = np.array(est_list)
        se = np.array(se_list)
        n_h = len(names)
        es_vcov = np.full((n_h, n_h), np.nan)
        if vce == "analytic":
            # The bin means are the OLS coefficients of ỹ on the mutually
            # exclusive horizon dummies (no intercept) -- did2s's
            # `~ 0 + i(rel_time, ref = ...)` second stage -- so the
            # corrected two-stage variance applies column by column, and
            # the off-diagonal blocks give the cross-horizon covariance.
            keep = [j for j, n_k in enumerate(count_list) if n_k > 0]
            if keep:
                X2_es = np.column_stack([mask_list[j].astype(float) for j in keep])
                resid2_es = y_tilde - X2_es @ est[keep]
                V_es = _did2s_corrected_vcov(
                    X2_es, resid2_es, A_full, untreated_mask, y_tilde, cl
                )
                es_vcov[np.ix_(keep, keep)] = V_es
                se = np.sqrt(np.clip(np.diag(es_vcov), 0, None))
        coef_dict = dict(zip(names, est))
        se_dict = dict(zip(names, se))
        count_dict = dict(zip(names, count_list))
    else:
        X2 = df["_D"].to_numpy(dtype=float).reshape(-1, 1)
        names = ["ATT"]
        design2 = np.column_stack([np.ones(len(y_tilde)), X2])
        coef2, *_ = np.linalg.lstsq(design2, y_tilde, rcond=None)
        resid2 = y_tilde - design2 @ coef2
        if vce == "analytic":
            # did2s regresses on the treatment dummy alone; the influence
            # function of the treatment coefficient is identical under the
            # [1, D] parametrisation because the intercept lies in the
            # Stage-1 column space (the untreated-row terms cancel exactly).
            V = _did2s_corrected_vcov(
                design2, resid2, A_full, untreated_mask, y_tilde, cl
            )
        else:
            V = _cluster_vcov(design2, resid2, cl)
        se_full = np.sqrt(np.clip(np.diag(V), 0, None))
        est = coef2[1:]
        se = se_full[1:]
        coef_dict = dict(zip(names, est))
        se_dict = dict(zip(names, se))

    # Standard-error mode. 'analytic' (default) is the did2s-corrected
    # two-stage clustered variance computed above; 'stage2' is the legacy
    # Stage-2-only sandwich (kept for reproducing earlier numbers, warns);
    # 'bootstrap' resamples whole clusters and re-runs both stages; 'none'
    # is the Stage-2 sandwich without the warning (used internally by the
    # bootstrap to avoid recursion).
    boot_overall_se: Optional[float] = None
    if vce == "analytic" and len(pd.unique(cl)) < 2:
        warnings.warn(
            "gardner_did: the cluster-robust variance needs at least two "
            "clusters; with a single cluster the two-stage corrected SE "
            "degenerates to zero. Pass a finer `cluster` or vce='bootstrap'.",
            UserWarning,
            stacklevel=2,
        )
    if vce == "bootstrap":
        se_dict, boot_overall_se = _gardner_cluster_bootstrap(
            df,
            y,
            group,
            time,
            first_treat,
            controls,
            event_study,
            horizon if event_study else None,
            cluster,
            names,
            n_boot,
            boot_seed,
        )
    elif vce == "stage2":
        warnings.warn(
            "gardner_did: vce='stage2' clusters the Stage-2 residuals only and "
            "ignores the variance from estimating the Stage-1 fixed effects, "
            "so it understates uncertainty (about 26% low on mpdta; "
            "empirically ~0.78 coverage at a nominal 95% level). It is kept "
            "only to reproduce earlier output; the default vce='analytic' is "
            "the did2s-corrected two-stage variance.",
            UserWarning,
            stacklevel=2,
        )

    z = sp_stats.norm.ppf(1 - alpha / 2)
    ci = {
        k: (coef_dict[k] - z * se_dict[k], coef_dict[k] + z * se_dict[k]) for k in names
    }

    if event_study:
        post_keys = [
            k
            for k in names
            if int(k.split("k")[1]) >= 0
            and np.isfinite(coef_dict[k])
            and count_dict.get(k, 0) > 0
        ]
        if post_keys:
            # Treated-observation-weighted mean of the post-treatment coefs
            # (the did2s aggregated-ATT convention). An *unweighted* mean
            # disagrees with the non-event-study ATT whenever the horizons have
            # unbalanced support / heterogeneous effects.
            w = np.array([count_dict[k] for k in post_keys], dtype=float)
            wn = w / w.sum()
            coefs_post = np.array([coef_dict[k] for k in post_keys], dtype=float)
            att_overall = float(np.dot(wn, coefs_post))
            if vce == "bootstrap" and boot_overall_se is not None:
                # Bootstrapping the overall ATT directly accounts for the
                # cross-horizon correlation.
                att_se = float(boot_overall_se)
            elif vce == "analytic":
                # Delta method through the full corrected cross-horizon
                # covariance: Var(w'θ) = w' V w.
                idx = [names.index(k) for k in post_keys]
                V_post = es_vcov[np.ix_(idx, idx)]
                att_se = float(np.sqrt(max(float(wn @ V_post @ wn), 0.0)))
            else:
                # Stage-2-only SE of the weighted average (horizons treated
                # as independent; the legacy 'stage2' / 'none' behaviour).
                ses_post = np.array([se_dict[k] for k in post_keys], dtype=float)
                att_se = float(np.sqrt(np.sum((wn * ses_post) ** 2)))
        else:
            att_overall, att_se = float("nan"), float("nan")
    else:
        att_overall = float(coef_dict["ATT"])
        att_se = float(se_dict["ATT"])

    pvalue = (
        float(2 * sp_stats.norm.sf(abs(att_overall / att_se)))
        if att_se > 0
        else float("nan")
    )

    n_units = int(df[group].nunique())
    n_treated_units = int(df.loc[treated_now, group].nunique())

    se_convention = {
        "analytic": (
            "did2s corrected two-stage clustered variance (Gardner 2022): "
            "Stage-1 estimation error propagated, no small-sample factor; "
            "matches R did2s::did2s and Stata did2s"
        ),
        "stage2": (
            "legacy Stage-2-only cluster sandwich with G/(G-1)(n-1)/(n-k); "
            "ignores Stage-1 estimation error (understates)"
        ),
        "bootstrap": "pairs-cluster bootstrap of the full two-step procedure",
        "none": "Stage-2-only cluster sandwich (internal fast path)",
    }[vce]
    model_info = {
        "method": "Gardner 2021 two-stage DID",
        "vce": vce,
        "se_convention": se_convention,
        "n_obs": int(len(df)),
        "n_units": n_units,
        "n_treated_units": n_treated_units,
        "alpha": alpha,
        "stage1_n": int(untreated_mask.sum()),
        "event_study": (
            {
                "horizon": names,
                "coef": coef_dict,
                "se": se_dict,
                "ci": ci,
                "vcov": (
                    pd.DataFrame(es_vcov, index=names, columns=names)
                    if vce == "analytic"
                    else None
                ),
            }
            if event_study
            else None
        ),
        "citation": (
            "Gardner, J. (2022). Two-stage differences in differences. "
            "arXiv:2207.05943. Butts & Gardner (2022), The R Journal."
        ),
    }

    _result = CausalResult(
        method="Gardner 2021 two-stage DID (did2s)",
        estimand="ATT",
        estimate=att_overall,
        se=att_se,
        pvalue=pvalue,
        ci=(att_overall - z * att_se, att_overall + z * att_se),
        alpha=alpha,
        n_obs=int(len(df)),
        model_info=model_info,
    )
    try:
        from ..output._lineage import attach_provenance as _attach_prov

        _attach_prov(
            _result,
            function="sp.did.gardner_did",
            params={
                "y": y,
                "group": group,
                "time": time,
                "first_treat": first_treat,
                "controls": controls,
                "event_study": event_study,
                "horizon": horizon,
                "cluster": cluster,
                "alpha": alpha,
            },
            data=data,
            overwrite=False,
        )
    except Exception:  # pragma: no cover
        pass
    return _result


# Convenience alias aligned with the R package ``did2s``.
did_2stage = gardner_did
