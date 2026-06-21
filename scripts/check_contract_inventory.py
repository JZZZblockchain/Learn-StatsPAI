"""Static drift gate for StatsPAI cross-cutting contracts.

Checks that the CausalPy-inspired contracts are still wired into source and
export surfaces.  This is intentionally AST/string based so it runs without
optional estimator dependencies.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src" / "statspai"


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _class_methods(path: Path, class_name: str) -> set[str]:
    tree = _parse(path)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
    return set()


def _module_defs(path: Path) -> set[str]:
    tree = _parse(path)
    out = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(node.name)
    return out


def _all_names(path: Path) -> set[str]:
    tree = _parse(path)
    names: set[str] = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__all__":
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            names.add(elt.value)
    return names


def check_contracts() -> list[str]:
    errors: list[str] = []

    effect_path = SRC / "core" / "effect_summary.py"
    defs = _module_defs(effect_path)
    effect_defs = {
        "EffectSummary",
        "effect_summary",
        "causal_effect_summary",
        "bayesian_effect_summary",
    }
    for name in effect_defs:
        if name not in defs:
            errors.append(f"{effect_path.relative_to(REPO_ROOT)} missing {name}")

    if "effect_summary" not in _class_methods(
        SRC / "core" / "results.py", "CausalResult"
    ):
        errors.append("CausalResult missing effect_summary()")
    if "effect_summary" not in _class_methods(
        SRC / "bayes" / "_base.py", "BayesianCausalResult"
    ):
        errors.append("BayesianCausalResult missing effect_summary()")

    checks_defs = _module_defs(SRC / "checks" / "base.py")
    check_defs = {
        "CheckResult",
        "CheckContext",
        "Check",
        "RobustnessBatteryCheck",
        "run_checks",
    }
    for name in check_defs:
        if name not in checks_defs:
            errors.append(f"checks/base.py missing {name}")
    checks_all = _all_names(SRC / "checks" / "__init__.py")
    for name in {"CheckResult", "RobustnessBatteryCheck", "run_checks"}:
        if name not in checks_all:
            errors.append(f"checks/__init__.py __all__ missing {name}")

    intake_defs = _module_defs(SRC / "smart" / "intake.py")
    for name in {"IntakeResult", "design_intake"}:
        if name not in intake_defs:
            errors.append(f"smart/intake.py missing {name}")
    smart_all = _all_names(SRC / "smart" / "__init__.py")
    for name in {"IntakeResult", "design_intake"}:
        if name not in smart_all:
            errors.append(f"smart/__init__.py __all__ missing {name}")

    top_all = _all_names(SRC / "__init__.py")
    for name in {"EffectSummary", "effect_summary", "IntakeResult", "design_intake"}:
        if name not in top_all:
            errors.append(f"statspai.__all__ missing {name}")

    return errors


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on drift.")
    args = parser.parse_args(argv)
    if not args.check:
        parser.error("--check is required")
    errors = check_contracts()
    if errors:
        print("[check_contract_inventory] REGRESSION", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    print("[check_contract_inventory] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
