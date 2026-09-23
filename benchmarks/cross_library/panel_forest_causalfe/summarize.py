"""Average the per-replication JSON lines in *.log."""

import glob
import json

import pandas as pd

for tool in ["cf", "sp"]:
    for name in "AB":
        rows = [
            json.loads(line)
            for path in sorted(glob.glob(f"{tool}_{name}*.log"))
            for line in open(path)
            if line.startswith("{")
        ]
        if not rows:
            continue
        frame = pd.DataFrame(rows)
        print(tool, name, len(frame))
        print(frame.drop(columns=["seed"]).mean().round(3).to_dict())
