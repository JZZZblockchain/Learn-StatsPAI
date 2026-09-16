"""Every script under ``examples/`` must run to completion.

``examples/rd_lee.py`` crashed for several releases -- it asked for columns
the bundled Senate extract no longer has -- while the reviewer guide kept
pointing readers at it. Nothing executed the scripts, so nothing noticed.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

import statspai as sp

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
# Scripts that take more than ~10 s run only with ``-m slow``.
SLOW = {"nhefs_whatif.py", "policy_index_hdfe_iv.py"}


def _params():
    for script in sorted(EXAMPLES.glob("*.py")):
        marks = [pytest.mark.slow] if script.name in SLOW else []
        yield pytest.param(script, id=script.name, marks=marks)


@pytest.mark.parametrize("script", list(_params()))
def test_example_script_runs(script, tmp_path):
    env = dict(os.environ)
    # Run against the same statspai this test process imported (worktree /
    # editable install), not whatever the subprocess would resolve on its own.
    pkg_root = str(Path(sp.__file__).resolve().parent.parent)
    env["PYTHONPATH"] = os.pathsep.join(
        p for p in (pkg_root, env.get("PYTHONPATH", "")) if p
    )
    env["MPLBACKEND"] = "Agg"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    assert proc.stdout.strip()
