"""StatsPAI Synthetic DID parity (Python side) -- Module 12.

Runs the **native Python** synthetic-DID estimator
(``sp.sdid(backend='native')``) on the california_prop99 replica
(Arkhangelsky et al. 2021). The companion 12_sdid.R uses
``synthdid::synthdid_estimate`` on the same CSV.

Tier: T2 native reference parity.  The native Python implementation now
mirrors synthdid's collapsed-form Frank-Wolfe weight solver and zeta
scaling, so the ATT matches the R reference on identical CSV bytes.  The
standard-error comparison still uses a small tolerance because StatsPAI
keeps a deterministic all-control placebo SE while ``synthdid_se`` uses
random placebo replications.  StatsPAI also ships an optional
``backend='synthdid'`` R bridge for users who want to delegate directly
to the R package; it is not used as the parity comparator.
"""
from __future__ import annotations

import statspai as sp

from _common import PARITY_SEED, ParityRecord, dump_csv, write_results


MODULE = "12_sdid"


def main() -> None:
    df = sp.datasets.california_prop99()
    dump_csv(df, MODULE)

    fit = sp.sdid(
        df,
        outcome="cigsale",
        unit="state",
        time="year",
        treated_unit="California",
        treatment_time=1989,
        backend="native",
        seed=PARITY_SEED,
    )

    rows: list[ParityRecord] = [
        ParityRecord(
            module=MODULE, side="py", statistic="att_sdid",
            estimate=float(fit.estimate),
            se=float(fit.se),
            ci_lo=float(fit.ci[0]) if fit.ci is not None else None,
            ci_hi=float(fit.ci[1]) if fit.ci is not None else None,
            n=int(len(df)),
        )
    ]

    write_results(
        MODULE, "py", rows,
        extra={
            "method": "sdid",
            "n_treated": int(fit.model_info["n_treated"]),
            "n_control": int(fit.model_info["n_control"]),
            "T_pre": int(fit.model_info["T_pre"]),
            "T_post": int(fit.model_info["T_post"]),
            "se_method": fit.model_info["se_method"],
            "backend": fit.model_info.get("backend", "native"),
            "validation_tier": fit.model_info.get("validation_tier"),
            "reference_backend": fit.model_info.get("reference_backend"),
            "tier": "T2",
            "native_note": (
                "Headline row is the NATIVE Python SDID (backend='native'). "
                "The native solver mirrors synthdid's collapsed-form "
                "Frank-Wolfe weights and zeta scaling, so the ATT is a T2 "
                "same-byte reference-parity row. The SE uses StatsPAI's "
                "deterministic all-control placebo convention, while "
                "synthdid_se uses random placebo replications; the optional "
                "backend='synthdid' R bridge is a convenience feature, not "
                "the parity comparator."
            ),
        },
    )


if __name__ == "__main__":
    main()
