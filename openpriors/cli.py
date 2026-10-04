"""``openpriors`` — one command over the whole discover -> predict -> confirm arc.

    openpriors run          front end: raw docs -> decompose -> concept graph -> match -> ground
    openpriors pipeline     graph layer: unify -> lineage -> analogy -> conjecture -> evaluate
    openpriors query        run the query DSL over the unified graph (a tour of worked questions)
    openpriors experiment   run every research-direction experiment (C2, C4, C5, C7)
    openpriors ledger       the prediction ledger: discover -> predict -> confirm, cross-referenced
    openpriors report       regenerate REPORT.md from live pipeline output
    openpriors demo         rebuild the interactive dashboard (docs/index.html)
    openpriors demonstrate  narrated end-to-end run of the whole arc (writes DEMONSTRATION.md)
    openpriors version      show the versions of every consolidated package

Each verb reproduces the exact path layout the Makefile encodes, so a single command works
from a fresh clone with nothing installed.
"""

from __future__ import annotations

import sys

from . import PACKAGES, __version__
from ._bootstrap import REPO_ROOT, is_source_checkout, require_source_checkout, wire_path

# package name (as declared in pyproject) -> the monorepo directory that holds it
_PKG_DIR = {
    "openpriors-analogy": "analogy", "openpriors-concept-graph": "concept_graph",
    "openpriors-decomposer": "decomposer", "openpriors-grounding": "grounding",
    "openpriors-matcher": "matcher", "openpriors-retrieval": "retrieval",
    "openpriors-graph": "graph",
}


def _run(rest):
    require_source_checkout("run")
    wire_path()
    import analogy.cli
    import concept_graph.cli
    import decomposer.cli
    import grounding.cli
    import matcher.cli
    for mod in (decomposer.cli, concept_graph.cli, matcher.cli, analogy.cli, grounding.cli):
        rc = mod.main([])
        if rc:
            return rc
    return 0


def _pipeline(rest):
    require_source_checkout("pipeline")
    wire_path()
    from graphstore import pipeline
    return pipeline.main(rest or [])


def _query(rest):
    require_source_checkout("query")
    wire_path()
    from graphstore import dsl_cli
    return dsl_cli.main(rest)


def _experiment(rest):
    require_source_checkout("experiment")
    wire_path()
    from graphstore import (experiment_c2, experiment_c4, experiment_c5,
                            experiment_c7)
    for mod in (experiment_c2, experiment_c4, experiment_c5, experiment_c7):
        rc = mod.main([])
        if rc:
            return rc
    return 0


def _ledger(rest):
    require_source_checkout("ledger")
    wire_path()
    from graphstore import prediction_ledger
    return prediction_ledger.main(rest or [])


def _report(rest):
    require_source_checkout("report")
    wire_path()
    import build_report
    build_report.build()
    return 0


def _demo(rest):
    require_source_checkout("demo")
    wire_path()
    import build_demo
    build_demo.build()
    return 0


def _demonstrate(rest):
    from . import demonstrate
    return demonstrate.main(rest)


def _pkg_version(name: str) -> str:
    """Read a package's declared version from its pyproject (source checkout), else '?'."""
    import re
    pp = REPO_ROOT / _PKG_DIR[name] / "pyproject.toml"
    if not pp.is_file():
        return "?"
    m = re.search(r'(?m)^\s*version\s*=\s*"([^"]+)"', pp.read_text(encoding="utf-8"))
    return m.group(1) if m else "?"


def _version(rest):
    print(f"openpriors {__version__}")
    if not is_source_checkout():
        for name in PACKAGES:
            print(f"  {name}")
        return 0
    width = max(len(n) for n in PACKAGES)
    for name in PACKAGES:
        print(f"  {name.ljust(width)}  {_pkg_version(name)}")
    return 0


VERBS = {
    "run": (_run, "front end: decompose -> concept graph -> match -> ground"),
    "pipeline": (_pipeline, "graph layer: unify -> lineage -> analogy -> conjecture -> evaluate"),
    "query": (_query, "run the query DSL over the unified graph (a tour of worked questions)"),
    "experiment": (_experiment, "run every research-direction experiment (C2, C4, C5, C7)"),
    "ledger": (_ledger, "the prediction ledger: discover -> predict -> confirm"),
    "report": (_report, "regenerate REPORT.md from live pipeline output"),
    "demo": (_demo, "rebuild the interactive dashboard (docs/index.html)"),
    "demonstrate": (_demonstrate, "narrated end-to-end run of the whole arc"),
    "version": (_version, "show the versions of every consolidated package"),
}


def _usage() -> str:
    width = max(len(v) for v in VERBS)
    lines = ["openpriors — one command over the whole discover -> predict -> confirm arc", "",
             "usage: openpriors <verb> [args...]", "", "verbs:"]
    for verb, (_, help_) in VERBS.items():
        lines.append(f"  {verb.ljust(width)}  {help_}")
    return "\n".join(lines)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(_usage())
        return 0
    verb, rest = argv[0], argv[1:]
    if verb not in VERBS:
        print(f"openpriors: unknown verb {verb!r}\n", file=sys.stderr)
        print(_usage(), file=sys.stderr)
        return 2
    return VERBS[verb][0](rest) or 0


if __name__ == "__main__":
    sys.exit(main())
