"""StatsPAI side of the comparison (PYTHONPATH=<repo>/src)."""

import json
import sys
import time
import warnings

import numpy as np
from dgps import dgp  # run from this directory

import statspai as sp

warnings.filterwarnings("ignore")

name, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
out = []
for s in range(lo, hi):
    X, Y, D, u, t, tau = dgp(name, s)
    tr = D == 1
    t0 = time.time()
    cf = sp.causal_forest(
        Y=Y, T=D, X=X, id=u, time=t, fe="twoway", n_estimators=2000, random_state=s
    )
    th = cf.predict()
    se = np.sqrt(cf.effect_variance())
    l, h = th - 1.96 * se, th + 1.96 * se
    a = cf.average_treatment_effect("treated")
    att = tau[tr].mean()
    cal = sp.calibrate_cate(cf)["cate"]
    out.append(
        dict(
            seed=s,
            rmse=float(np.sqrt(np.mean((th[tr] - tau[tr]) ** 2))),
            corr=float(np.corrcoef(th[tr], tau[tr])[0, 1]),
            rmse_cal=float(np.sqrt(np.mean((cal[tr] - tau[tr]) ** 2))),
            pcov=float(np.mean((l[tr] <= tau[tr]) & (tau[tr] <= h[tr]))),
            pwidth=float(np.mean(h[tr] - l[tr])),
            ate_bias=float(a["estimate"] - att),
            ate_cov=bool(a["ci_low"] <= att <= a["ci_high"]),
            ate_width=float(a["ci_high"] - a["ci_low"]),
            plug_bias=float(a["forest_plug_in"] - att),
            secs=time.time() - t0,
        )
    )
    print(json.dumps(out[-1]), flush=True)
json.dump(out, open(f"sp_{name}_{lo}.json", "w"))
