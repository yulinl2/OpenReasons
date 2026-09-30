"""Locate the source checkout and wire every package's ``src`` onto ``sys.path``.

The monorepo runs on ``PYTHONPATH`` (each package declares its siblings as dependencies but
they are resolved in-tree, not pip-installed — see each ``pyproject.toml``). The unified CLI
reproduces exactly the path layout the Makefile encodes, in one place, so a single
``openpriors <verb>`` works from a fresh clone with nothing installed.

Compute verbs also read the committed corpora (``grounding/dgroups/``, ``retrieval/library/``,
``graph/results/`` …), so they are inherently source-tree operations. If the tree isn't found
(e.g. only the built wheel is installed, off the repo), we fail loud with a precise message
rather than an obscure import/FileNotFound error deep in a stage.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# openpriors/ lives at the repo root, so the root is one level up from this file.
REPO_ROOT = Path(__file__).resolve().parents[1]

# Pin the reproducible-artifact epoch the same way the Makefile does (`export SOURCE_DATE_EPOCH`),
# so a verb that regenerates timestamped artifacts (e.g. `openpriors run`) is byte-for-byte
# deterministic through the unified CLI too — not just under `make`. setdefault keeps any explicit
# override the caller set.
os.environ.setdefault("SOURCE_DATE_EPOCH", "1735689600")

# Every importable source root + the two loose script dirs (demo/, report/). Union is safe:
# the package names are disjoint, so there is no shadowing across these directories.
_SRC_DIRS = (
    "decomposer/src", "concept_graph/src", "matcher/src", "analogy/src",
    "grounding/src", "retrieval/src", "graph/src", "demo", "report",
)


def is_source_checkout() -> bool:
    """True iff we're running inside the OpenPriors repo (the packages' src trees exist)."""
    return (REPO_ROOT / "graph" / "src" / "graphstore").is_dir()


def require_source_checkout(verb: str) -> Path:
    if not is_source_checkout():
        raise SystemExit(
            f"openpriors {verb}: this command runs the pipeline over the committed corpora and "
            f"must be run from a source checkout of the OpenPriors repository.\n"
            f"  git clone https://github.com/yulinl2/OpenPriors && cd OpenPriors && openpriors {verb}"
        )
    return REPO_ROOT


def wire_path() -> Path:
    """Prepend the in-tree source roots to ``sys.path`` (idempotent). Returns the repo root."""
    for rel in _SRC_DIRS:
        d = REPO_ROOT / rel
        s = str(d)
        if d.is_dir() and s not in sys.path:
            sys.path.insert(0, s)
    return REPO_ROOT
