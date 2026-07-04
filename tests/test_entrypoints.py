"""Entrypoint coverage + robustness: every module gate's ``main()`` runs green under pytest.

The experiment / pipeline / real-paper / gate modules each expose a ``main(argv=None) -> int``
that runs the module's CI invariants and returns 0 (raising ``SystemExit`` on violation). Those
gates were previously exercised only by the CI workflows, not by ``make test`` — so a broken
invariant would pass locally and only fail in CI. Running them here means the whole gated chain
is validated in the unit suite too (defense in depth), and it closes the entrypoints' coverage.
"""

import importlib
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
for rel in ("decomposer/src", "concept_graph/src", "matcher/src", "analogy/src",
            "grounding/src", "retrieval/src", "graph/src", "demo", "report"):
    sys.path.insert(0, str(REPO / rel))

# gate/driver mains that ignore argv and return 0 on success (raise SystemExit on a broken
# invariant). Running each is both a coverage pass over its main() and a re-run of its gate.
GATE_MAINS = [
    "graphstore.crossdomain", "graphstore.multidomain", "graphstore.discover",
    "graphstore.evaluate", "graphstore.schema", "graphstore.pipeline",
    "graphstore.prediction_ledger", "graphstore.realpaper2", "graphstore.realpaper3",
    "graphstore.experiment_c2", "graphstore.experiment_c4", "graphstore.experiment_c5",
    "graphstore.experiment_c7", "graphstore.dsl_cli", "graphstore.transfer_cli",
    "retrieval.realpaper", "retrieval.decompose", "retrieval.lineage", "retrieval.index",
    "grounding.casestudy", "grounding.discrimination",
]


# the argparse CLI front-ends. Each reads committed inputs by default but WRITES its outputs to
# a dir; we redirect that output to a throwaway tmp dir via the CLI's own flag, so exercising the
# CLI can never mutate tracked sample artifacts. (retrieval/graphstore write to a fixed, tracked
# results/ dir deterministically — byte-identical on re-run — so they take no redirect.)
CLI_MAINS = [
    ("decomposer.cli", "--runs"),
    ("concept_graph.cli", "--out"),
    ("matcher.cli", "--out"),
    ("analogy.cli", "--out"),
    ("grounding.cli", "--out"),
    ("retrieval.cli", None),
    ("graphstore.cli", None),
]


@pytest.mark.parametrize("modname", GATE_MAINS)
def test_gate_main_runs_green(modname):
    mod = importlib.import_module(modname)
    assert hasattr(mod, "main"), f"{modname} has no main()"
    rc = mod.main([])
    assert rc == 0, f"{modname}.main() returned {rc}, expected 0"


@pytest.mark.parametrize("modname,out_flag", CLI_MAINS)
def test_cli_main_runs_green_on_defaults(modname, out_flag, tmp_path):
    mod = importlib.import_module(modname)
    assert hasattr(mod, "main"), f"{modname} has no main()"
    argv = [out_flag, str(tmp_path)] if out_flag else []
    rc = mod.main(argv)
    assert rc == 0, f"{modname}.main({argv}) returned {rc}, expected 0"
