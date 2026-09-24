"""No two FunctionSpecs may quietly claim the same name.

``register()`` is ``_REGISTRY[spec.name] = spec``: the later call wins and
the earlier one vanishes without a word. On 2026-09-24 that had eaten a
whole spec's worth of curation -- ``ddd`` was registered twice, the second
entry was a stale copy whose reference still called
``sp.ddd_heterogeneous`` "on the roadmap", and it silently overwrote the
maintained entry. ``sp.help('ddd')`` and ``sp.function_schema('ddd')``
showed the stale text, and the ``id=`` / ``method=`` parameters another
session had just documented were invisible to every agent.

The other four pairs found at the same time -- ``did_analysis``,
``event_study``, ``harvest_did``, ``overlap_weighted_did`` -- were merged
in the same pass. Between them the effective specs had been hiding eleven
parameters from ``sp.function_schema()``, so to an agent those arguments
did not exist: seven on ``did_analysis`` alone (``covariates``,
``cluster``, ``robust``, ``alpha``, ``control_group``, ``estimator``,
``event_window``). The registry is now duplicate-free and every one of the
five covers its whole signature; this test keeps it that way.
"""

from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "src" / "statspai" / "registry.py"

# Deliberately empty. A duplicate is never acceptable: whichever spec is
# registered second wins and the first one's curation is lost in silence.
# If a pair ever has to be tolerated, list it here with what its effective
# spec hides, and shrink the list back to nothing as soon as possible.
KNOWN_DUPLICATES: dict = {}


def _spec_names() -> list[str]:
    """Every ``name=`` passed to a ``FunctionSpec(...)`` call, in order."""
    tree = ast.parse(REGISTRY.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "FunctionSpec"):
            continue
        for kw in node.keywords:
            if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                names.append(str(kw.value.value))
    return names


def test_no_new_duplicate_function_specs():
    counts = Counter(_spec_names())
    duplicated = sorted(n for n, c in counts.items() if c > 1)
    new = sorted(set(duplicated) - set(KNOWN_DUPLICATES))
    assert not new, (
        "these names are registered twice, so the later FunctionSpec silently "
        f"replaces the earlier one and its curation is lost: {new}. Merge the "
        "pair into one spec (keep the maintained entry, fold in whatever the "
        "stale one uniquely had, delete the stale one) rather than editing "
        "whichever copy you happened to open."
    )


def test_known_duplicates_are_still_duplicated():
    # A ratchet only ratchets if it notices when an entry is fixed.
    counts = Counter(_spec_names())
    fixed = sorted(n for n in KNOWN_DUPLICATES if counts[n] <= 1)
    assert not fixed, (
        f"{fixed} no longer has a duplicate spec -- remove it from "
        "KNOWN_DUPLICATES so the list keeps shrinking."
    )


def test_the_registry_is_duplicate_free():
    counts = Counter(_spec_names())
    assert counts, "no FunctionSpec calls parsed -- the AST walk is broken"
    assert max(counts.values()) == 1, (
        "a name is registered twice: "
        f"{sorted(n for n, c in counts.items() if c > 1)}"
    )


def test_no_registered_spec_hides_a_parameter_of_its_function():
    """The five de-duplicated entries must keep covering their signatures.

    Hiding a parameter is how the duplicates did their damage: the argument
    is real, the function accepts it, and no agent can see it.
    """
    import inspect

    import statspai as sp
    from statspai import registry as R

    sp.describe_function("ddd")  # force the full registry
    hidden = {}
    for name in (
        "ddd",
        "did_analysis",
        "event_study",
        "harvest_did",
        "overlap_weighted_did",
    ):
        fn = getattr(sp, name)
        sig = {
            q
            for q, o in inspect.signature(fn).parameters.items()
            if o.kind not in (o.VAR_POSITIONAL, o.VAR_KEYWORD)
        }
        spec = {ps.name for ps in R._REGISTRY[name].params}
        if sig - spec:
            hidden[name] = sorted(sig - spec)
    assert not hidden, f"registry entries hiding real parameters: {hidden}"
