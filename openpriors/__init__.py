"""OpenPriors — the whole system behind one import and one command.

This top-level package is the *consolidation* layer over the seven monorepo packages
(decomposer, concept_graph, matcher, analogy, grounding, retrieval, graphstore). It exposes
a single ``openpriors`` console entry point that dispatches every stage of the
discover -> predict -> confirm arc — so the system is driven by one verb, not by
remembering a different ``PYTHONPATH`` for each package.
"""

from __future__ import annotations

__version__ = "0.1.0"

# The seven packages this meta-package consolidates, in dependency order. Kept here as the
# single source of truth for `openpriors version` and the packaging-consistency gate.
PACKAGES = (
    "openpriors-analogy",
    "openpriors-concept-graph",
    "openpriors-decomposer",
    "openpriors-grounding",
    "openpriors-matcher",
    "openpriors-retrieval",
    "openpriors-graph",
)
