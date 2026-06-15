"""Resolve a registered StatsPAI function name to its callable object.

The agent-facing surface is ``sp.list_functions()`` (the registry). Most
names resolve at the top level (``getattr(sp, name)``), but a few are
*intentionally* submodule-scoped — e.g. ``sp.causal_llm.echo_client``,
``sp.causal_llm.anthropic_client``, ``sp.causal_llm.openai_client``,
``sp.assimilation.particle_filter``. Those are registered and documented
under their submodule path, and the registry-vs-``__all__`` asymmetry is
recorded in the frozen baseline of
``tests/test_api_surface_consistency.py`` — i.e. it is a deliberate
contract, not a gap.

``sp.describe_function(name)`` already works for every registered name
(the agent-native contract holds regardless of exposure path). The
coverage / runnability tooling, however, historically resolved only via
``getattr(sp, name)`` and therefore could not see the docstrings of the
submodule-scoped functions. This helper closes that blind spot so the
gates measure the *documented docstring* of every registered function,
independent of whether it is also re-exported at the top level.

Resolution order:

1. ``getattr(sp, name)`` — the common top-level path.
2. ``getattr(sp.<category>, name)`` — the category from
   ``describe_function`` doubles as the submodule for the scoped
   functions; ``getattr(sp, category)`` triggers the lazy import.
3. A scan of already-loaded ``statspai.*`` submodules for a callable
   whose ``__name__`` matches — a last resort that needs no extra
   imports (steps 1-2 will have loaded the relevant module).
"""

from __future__ import annotations

import sys
import types
from typing import Optional


def resolve_registered(sp, name: str) -> Optional[object]:
    """Return the callable for a registered ``name``, or ``None``.

    Tries the top level first, then the function's category submodule,
    then a scan of loaded ``statspai.*`` modules.
    """
    obj = getattr(sp, name, None)
    if obj is not None:
        return obj

    # Category-directed: for the submodule-scoped functions the
    # registry category equals the submodule name, and getattr on the
    # package triggers the lazy import.
    try:
        cat = (sp.describe_function(name) or {}).get("category")
    except Exception:
        cat = None
    if cat:
        mod = getattr(sp, cat, None)
        if mod is not None:
            cand = getattr(mod, name, None)
            if cand is not None:
                return cand

    # Last resort: scan loaded statspai submodules for the name.
    for modname, mod in list(sys.modules.items()):
        if not modname.startswith("statspai"):
            continue
        if not isinstance(mod, types.ModuleType):
            continue
        cand = getattr(mod, name, None)
        if cand is not None and getattr(cand, "__name__", None) == name:
            return cand

    return None
