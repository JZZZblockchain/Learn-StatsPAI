"""
Difference-in-Differences (DID) module for StatsPAI.

Provides estimators for:
- Classic 2×2 DID (two groups, two periods)
- Triple Differences / DDD (two groups, two periods, within-unit subgroup)
- Callaway & Sant'Anna (2021) — staggered DID with DR/IPW/REG
- Sun & Abraham (2021) — interaction-weighted event study
- Synthetic DID (Arkhangelsky et al. 2021)
- Goodman-Bacon (2021) — TWFE decomposition diagnostic
- Honest DID (Rambachan & Roth 2023) — parallel trends sensitivity
- de Chaisemartin & D'Haultfoeuille (2020) — DID with treatment switching
- Borusyak, Jaravel & Spiess (2024) — imputation DID estimator
- Stacked DID (Cengiz, Dube, Lindner & Zipperer, 2019)
- did_analysis() — one-call DID workflow
- Wooldridge (2021) — extended TWFE with cohort × time interactions
- Sant'Anna & Zhao (2020) — doubly robust DID
- TWFE decomposition — Bacon (2021) + de Chaisemartin–D'Haultfoeuille (2020) weights
"""

from typing import Optional, List

import pandas as pd

from ..core.results import CausalResult
from .did_2x2 import did_2x2
from .overlap_did import overlap_weighted_did, dl_propensity_score
from .ddd import ddd
from .callaway_santanna import callaway_santanna
from .aggte import aggte
from .report import cs_report, CSReport
from .bjs_inference import bjs_pretrend_joint
from .sun_abraham import sun_abraham
from .bacon import bacon_decomposition
from .honest_did import honest_did, breakdown_m
from .event_study import event_study
from .analysis import did_analysis, DIDAnalysis
from .did_multiplegt import did_multiplegt
from .did_imputation import did_imputation
from .stacked_did import stacked_did
from .gardner_2s import gardner_did, did_2stage
from .harvest import harvest_did, HarvestDIDResult
from .cic import cic
from .pretrends import (
    pretrends_test,
    pretrends_power,
    sensitivity_rr,
    SensitivityResult,
    pretrends_summary,
)
from .wooldridge_did import wooldridge_did, etwfe, etwfe_emfx, drdid, twfe_decomposition
from .did_bcf import did_bcf
from .cohort_anchored import cohort_anchored_event_study
from .design_robust import design_robust_event_study
from .misclassified import did_misclassified
from .summary import did_summary, did_summary_to_markdown, did_summary_to_latex, did_report
from .continuous_did import continuous_did
from .plots import (
    parallel_trends_plot,
    bacon_plot,
    group_time_plot,
    did_plot,
    event_study_plot as enhanced_event_study_plot,
    treatment_rollout_plot,
    sensitivity_plot,
    cohort_event_study_plot,
    ggdid,
    did_summary_plot,
)

bjs = did_imputation
borusyak_jaravel_spiess = did_imputation


def did(
    data: pd.DataFrame,
    y: str,
    treat: str,
    time: str,
    id: Optional[str] = None,
    covariates: Optional[List[str]] = None,
    method: str = 'auto',
    estimator: str = 'dr',
    control_group: str = 'nevertreated',
    base_period: str = 'universal',
    cluster: Optional[str] = None,
    robust: bool = True,
    alpha: float = 0.05,
    weights: Optional[str] = None,
    # DDD-specific
    subgroup: Optional[str] = None,
    # SDID-specific
    treat_unit=None,
    treat_time=None,
    se_method: str = 'placebo',
    # CS aggte-dispatch (v0.7.1+)
    aggregation: Optional[str] = None,
    n_boot: int = 1000,
    random_state: Optional[int] = None,
    panel: bool = True,
    anticipation: int = 0,
    **kwargs,
) -> CausalResult:
    """
    Difference-in-Differences estimation.

    Unified entry point that auto-detects design type and dispatches to
    the appropriate estimator.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataset.
    y : str
        Outcome variable name.
    treat : str
        Treatment variable. **The column semantics depend on the design** —
        one of the most common pitfalls in DID:

        - **2×2 DID** (no ``id``, two periods): a 0/1 group indicator
          (treated vs. control), identical to a standard DID dummy.
        - **Staggered DID** (Callaway–Sant'Anna, Sun–Abraham, SDID,
          Borusyak–Jaravel–Spiess, de Chaisemartin–D'Haultfœuille,
          Wooldridge etwfe): the **first treatment period** for each unit
          (aka the cohort / g-variable in R's ``did`` package). Never-treated
          units must have ``0`` (or ``NaN``), **not ``1``**. A plain 0/1
          indicator will silently be interpreted as "everyone was first
          treated in period 1," producing nonsense estimates.

        If you only have a 0/1 ``treated`` column, construct ``first_treat``
        per unit and broadcast it to all of that unit's rows::

            # First treated year per unit (NaN for never-treated units)
            first = (df.loc[df['treated'] == 1]
                       .groupby('id')['year'].min())
            df['first_treat'] = df['id'].map(first).fillna(0).astype(int)
            sp.did(df, y='y', treat='first_treat', time='year', id='id')
    time : str
        Time period variable.
    id : str, optional
        Unit identifier. Required for staggered DID and SDID.
    covariates : list of str, optional
        Covariate names for conditional parallel trends / controls.
    method : str, default 'auto'
        - ``'auto'`` — 2×2 if ``id`` is None and treatment is binary,
          else Callaway-Sant'Anna.
        - ``'2x2'`` — classic two-period, two-group DID.
        - ``'ddd'`` — triple differences (requires ``subgroup``).
        - ``'callaway_santanna'`` or ``'cs'`` — staggered DID.
        - ``'sun_abraham'``, ``'sa'``, or ``'sunab'`` — IW event study.
        - ``'bjs'`` or ``'did_imputation'`` — Borusyak-Jaravel-Spiess
          imputation DID.
        - ``'sdid'`` — synthetic DID (Arkhangelsky et al. 2021).
    estimator : str, default 'dr'
        For staggered DID: ``'dr'`` (doubly robust), ``'ipw'``, ``'reg'``.
    control_group : str, default 'nevertreated'
        For staggered DID: ``'nevertreated'`` or ``'notyettreated'``.
    base_period : str, default 'universal'
        For staggered DID: ``'universal'`` or ``'varying'``.
    cluster : str, optional
        Cluster variable for standard errors.
    robust : bool, default True
        HC1 robust standard errors (2×2 / DDD only).
    alpha : float, default 0.05
        Significance level for confidence intervals.
    weights : str, optional
        Column name for analytical weights (e.g. population weights).
        Supported for ``'2x2'``, ``'ddd'``, and event study methods.
        Equivalent to Stata's ``[aweight=...]``.
    subgroup : str, optional
        For DDD: binary affected-subgroup indicator.
    treat_unit : optional
        For SDID: treated unit(s).
    treat_time : optional
        For SDID: treatment time.
    se_method : str, default 'placebo'
        For SDID: 'placebo', 'bootstrap', or 'jackknife'.
    aggregation : str, optional
        When set and ``method`` is Callaway–Sant'Anna, the raw ATT(g,t)
        result is passed through :func:`aggte` with ``type=aggregation``
        (``'simple'``, ``'dynamic'``, ``'group'``, or ``'calendar'``),
        delivering the aggregated ATT with Mammen multiplier-bootstrap
        uniform confidence bands in a single call.
    n_boot : int, default 1000
        Bootstrap replications for the multiplier bootstrap when
        ``aggregation`` is set.
    random_state : int, optional
        Seed for the multiplier bootstrap.
    panel : bool, default True
        Forwarded to :func:`callaway_santanna`; set ``panel=False`` for
        repeated cross-sections.
    anticipation : int, default 0
        Forwarded to :func:`callaway_santanna`.

    Returns
    -------
    CausalResult
        Estimation results with ``.summary()``, ``.plot()``,
        ``.to_latex()``, ``.cite()`` methods.

    Examples
    --------
    >>> import statspai as sp
    >>> import numpy as np, pandas as pd
    >>> rng = np.random.default_rng(0)

    Classic 2x2 DID (one binary treatment, two periods):

    >>> n = 200
    >>> df = pd.DataFrame({
    ...     'treated': np.repeat(rng.integers(0, 2, n), 2),
    ...     'post': np.tile([0, 1], n),
    ... })
    >>> df['wage'] = (1.0 + 2.0 * df['treated'] + 1.5 * df['post']
    ...               + 3.0 * df['treated'] * df['post']
    ...               + rng.normal(0, 1, len(df)))
    >>> result = sp.did(df, y='wage', treat='treated', time='post')
    >>> bool(result.estimate > 0)
    True

    Triple Differences (a third dimension via ``subgroup``):

    >>> df['low_wage'] = np.repeat(rng.integers(0, 2, n), 2)
    >>> ddd = sp.did(df, y='wage', treat='treated', time='post',
    ...              method='ddd', subgroup='low_wage')

    Staggered DID (cohort column gives first-treatment time; 0 = never):

    >>> rows = []
    >>> for u in range(30):
    ...     first = int(rng.choice([2003, 2005, 0]))
    ...     for yr in range(2000, 2008):
    ...         on = 1 if (first != 0 and yr >= first) else 0
    ...         rows.append({'unit': u, 'year': yr, 'first_treat': first,
    ...                      'y': 5 + 2.0 * on + rng.normal(0, 1)})
    >>> panel = pd.DataFrame(rows)
    >>> staggered = sp.did(panel, y='y', treat='first_treat',
    ...                    time='year', id='unit')
    >>> bool(staggered.estimate == staggered.estimate)  # finite
    True
    """
    # --- Input validation (Stata-quality error messages) ---
    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            f"'data' must be a pandas DataFrame, got {type(data).__name__}."
        )
    if data.empty:
        raise ValueError("DataFrame is empty — no observations for DID.")
    required = {'y': y, 'treat': treat, 'time': time}
    if id is not None:
        required['id'] = id
    if subgroup is not None:
        required['subgroup'] = subgroup
    if weights is not None:
        required['weights'] = weights
    if covariates:
        for c in covariates:
            required[f'covariate ({c})'] = c
    missing = {label: col for label, col in required.items()
               if col not in data.columns}
    if missing:
        details = ', '.join(f'{l}={c!r}' for l, c in missing.items())
        available = ', '.join(sorted(data.columns)[:10])
        raise ValueError(
            f"Column(s) not found in data: {details}. "
            f"Available: {available}"
            + (" ..." if len(data.columns) > 10 else "")
        )

    # If estimator-specific aggregation arguments are passed with auto,
    # choose the estimator whose aggregation vocabulary was requested.
    _sa_aggregations = {
        'event_time',
        'event_time_equal',
        'equal_event_time',
        'fixest',
        'fixest_att',
        'treated_cell',
        'treated_cell_weighted',
    }
    if aggregation is not None and method == 'auto' and id is not None:
        method = (
            'sun_abraham'
            if aggregation in _sa_aggregations
            else 'callaway_santanna'
        )

    # Validate that CS-only arguments were not paired with a non-CS
    # method — fail loudly rather than swallow the argument.
    _cs_methods = {'callaway_santanna', 'cs', 'auto'}
    _sa_methods = {'sun_abraham', 'sa', 'sunab'}
    if aggregation is not None and method not in (_cs_methods | _sa_methods):
        raise ValueError(
            f"`aggregation={aggregation!r}` is only supported with the "
            f"Callaway-Sant'Anna estimator (method='cs') or the "
            f"Sun-Abraham estimator (method='sun_abraham'); got "
            f"method={method!r}."
        )
    if (not panel) and method not in _cs_methods:
        raise ValueError(
            f"`panel=False` is only supported with Callaway-Sant'Anna; "
            f"got method={method!r}."
        )
    if anticipation != 0 and method not in _cs_methods:
        raise ValueError(
            f"`anticipation={anticipation}` is only supported with "
            f"Callaway-Sant'Anna; got method={method!r}."
        )

    # Auto-detect if subgroup is provided → DDD
    if method == 'auto' and subgroup is not None:
        method = 'ddd'

    # Auto-detect method
    if method == 'auto':
        if id is not None:
            method = 'callaway_santanna'
        else:
            treat_vals = set(data[treat].dropna().unique())
            if treat_vals <= {0, 1, True, False}:
                method = '2x2'
            else:
                raise ValueError(
                    f"Cannot auto-detect DID type. Treatment '{treat}' has "
                    f"values {sorted(treat_vals)}. Provide 'id' for staggered "
                    "DID, or set method='2x2' or method='callaway_santanna'."
                )

    # ── Normalize aliases ─────────────────────────────────────────── #
    _METHOD_ALIASES = {'did2s': '2x2'}
    method = _METHOD_ALIASES.get(method, method)

    # 'classic' / 'twfe': run 2x2 DID.
    # If time has >2 values, collapse into pre/post using median split.
    if method in ('classic', 'twfe'):
        n_time = data[time].nunique()
        if n_time > 2:
            time_mid = data[time].median()
            data = data.copy()
            data['_post'] = (data[time] >= time_mid).astype(int)
            time = '_post'
        method = '2x2'

    # ── Dispatch ───────────────────────────────────────────────────── #

    if method == '2x2':
        return did_2x2(
            data, y=y, treat=treat, time=time,
            covariates=covariates, cluster=cluster,
            robust=robust, alpha=alpha, weights=weights,
        )

    if method == 'ddd':
        if subgroup is None:
            raise ValueError(
                "'subgroup' is required for Triple Differences (DDD). "
                "Provide the name of a binary column indicating the "
                "affected subgroup."
            )
        return ddd(
            data, y=y, treat=treat, time=time, subgroup=subgroup,
            covariates=covariates, cluster=cluster,
            robust=robust, alpha=alpha, weights=weights,
        )

    if method in ('callaway_santanna', 'cs'):
        if id is None:
            raise ValueError(
                "'id' (unit identifier) is required for staggered DID."
            )
        cs_result = callaway_santanna(
            data, y=y, g=treat, t=time, i=id,
            x=covariates, estimator=estimator,
            control_group=control_group,
            base_period=base_period, alpha=alpha,
            anticipation=anticipation, panel=panel,
        )
        if aggregation is not None:
            if aggregation not in ('simple', 'dynamic', 'group', 'calendar'):
                raise ValueError(
                    f"aggregation must be one of "
                    f"'simple'/'dynamic'/'group'/'calendar', "
                    f"got {aggregation!r}"
                )
            return aggte(
                cs_result, type=aggregation, alpha=alpha,
                n_boot=n_boot, random_state=random_state,
            )
        return cs_result

    if method in ('sun_abraham', 'sa', 'sunab'):
        if id is None:
            raise ValueError(
                "'id' (unit identifier) is required for Sun-Abraham."
            )
        return sun_abraham(
            data, y=y, g=treat, t=time, i=id,
            covariates=covariates, cluster=cluster,
            aggregation=aggregation or 'event_time',
            alpha=alpha,
        )

    if method in (
        'bjs',
        'did_imputation',
        'borusyak_jaravel_spiess',
        'borusyak',
    ):
        if id is None:
            raise ValueError(
                "'id' (unit identifier) is required for BJS imputation."
            )
        horizon = kwargs.pop('horizon', None)
        event_window = kwargs.pop('event_window', None)
        if horizon is None and event_window is not None:
            lo, hi = int(event_window[0]), int(event_window[1])
            horizon = list(range(lo, hi + 1))
        return did_imputation(
            data,
            y=y,
            group=id,
            time=time,
            first_treat=treat,
            controls=covariates,
            horizon=horizon,
            cluster=cluster,
            alpha=alpha,
        )

    if method == 'sdid':
        from ..synth.sdid import sdid as _sdid
        if id is None:
            raise ValueError("'id' (unit identifier) is required for SDID.")
        # Infer treat_unit / treat_time from the treat column if not provided
        _treat_unit = treat_unit
        _treat_time = treat_time
        if _treat_unit is None and _treat_time is None:
            # treat column encodes first treatment period (0 = never treated)
            treated_mask = data[treat] > 0
            if treated_mask.any():
                _treat_unit = data.loc[treated_mask, id].unique().tolist()
                _treat_time = int(data.loc[treated_mask, treat].min())
        return _sdid(
            data, y=y, unit=id, time=time,
            treat_unit=_treat_unit, treat_time=_treat_time,
            method='sdid', covariates=covariates,
            se_method=se_method, alpha=alpha, **kwargs,
        )

    raise ValueError(
        f"Unknown DID method: '{method}'. "
        "Available: '2x2' (or 'classic', 'twfe'), 'ddd', "
        "'callaway_santanna' (or 'cs'), 'sun_abraham' (or 'sa'), "
        "'bjs' (or 'did_imputation'), 'sdid'."
    )


__all__ = [
    'did',
    'did_2x2',
    'overlap_weighted_did',
    'dl_propensity_score',
    'ddd',
    'callaway_santanna',
    'aggte',
    'cs_report',
    'CSReport',
    'bjs_pretrend_joint',
    'sun_abraham',
    'bacon_decomposition',
    'honest_did',
    'breakdown_m',
    'event_study',
    'did_analysis',
    'DIDAnalysis',
    'did_multiplegt',
    'did_imputation',
    'bjs',
    'borusyak_jaravel_spiess',
    'stacked_did',
    'gardner_did',
    'did_2stage',
    'cic',
    # Wooldridge / DR-DID / TWFE decomposition
    'wooldridge_did',
    'etwfe',
    'etwfe_emfx',
    'did_summary',
    'did_summary_to_markdown',
    'did_summary_to_latex',
    'did_report',
    'drdid',
    'twfe_decomposition',
    # v0.10 staggered DiD frontier
    'did_bcf',
    'cohort_anchored_event_study',
    'design_robust_event_study',
    'did_misclassified',
    # Pre-trends
    'pretrends_test',
    'pretrends_power',
    'sensitivity_rr',
    'SensitivityResult',
    'pretrends_summary',
    # Plots
    'parallel_trends_plot',
    'bacon_plot',
    'group_time_plot',
    'did_plot',
    'enhanced_event_study_plot',
    'treatment_rollout_plot',
    'sensitivity_plot',
    'cohort_event_study_plot',
    'ggdid',
    'did_summary_plot',
]
