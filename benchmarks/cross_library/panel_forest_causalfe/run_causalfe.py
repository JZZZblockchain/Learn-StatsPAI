"""causalfe side of the comparison (run in a venv with causalfe 0.3.2)."""

import json
import sys
import time

import numpy as np
from dgps import dgp
from causalfe import CFFEForest

name, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
out = []
for s in range(lo, hi):
    X, Y, D, u, t, tau = dgp(name, s)
    tr = D == 1
    t0 = time.time()
    f = CFFEForest(n_trees=100, max_depth=4, min_leaf=20, seed=s).fit(X, Y, D, u, t)
    th, l, h = f.predict_interval(X)
    a = f.ate()
    al, ah = f.ate_interval()
    att = tau[tr].mean()
    out.append(
        dict(
            seed=s,
            rmse=float(np.sqrt(np.mean((th[tr] - tau[tr]) ** 2))),
            corr=float(np.corrcoef(th[tr], tau[tr])[0, 1]),
            pcov=float(np.mean((l[tr] <= tau[tr]) & (tau[tr] <= h[tr]))),
            pwidth=float(np.mean(h[tr] - l[tr])),
            ate_bias=float(a - att),
            ate_cov=bool(al <= att <= ah),
            ate_width=float(ah - al),
            secs=time.time() - t0,
        )
    )
    print(json.dumps(out[-1]), flush=True)
json.dump(out, open(f"cf_{name}_{lo}.json", "w"))
