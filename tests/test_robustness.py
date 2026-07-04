"""Robustness regressions (Epic AK): each fix from the cross-package audit, verified to bite.

Every test here fails on the PRE-fix code (crash / nondeterminism / silent pass) and passes on
the hardened code — verify-the-verifier for the hardening pass itself.
"""

import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
for rel in ("decomposer/src", "concept_graph/src", "matcher/src", "analogy/src",
            "grounding/src", "retrieval/src", "graph/src"):
    sys.path.insert(0, str(REPO / rel))


# --- grounding.verify: fail loud on malformed sections, don't crash --------------------------
def test_grounding_check_section_reports_nonstring_grounding():
    from grounding.verify import check_section
    rep = check_section({"text": "abc", "groundings": {"x": None}, "facts": [["P", "x"]]})
    assert rep["passed"] is False and "x" in rep["non_verbatim_groundings"]   # reported, not crash


def test_grounding_check_section_missing_key_fails_loud():
    from grounding.verify import check_section
    for bad in ({"groundings": {}, "facts": []}, {"text": "t", "groundings": {}}):
        with pytest.raises(ValueError):
            check_section(bad)


# --- crossdomain: reject a malformed (non-binary) CAUSE ---------------------------------------
def test_crossdomain_rejects_malformed_cause_arity():
    from analogy.predicates import Dgroup
    from graphstore.crossdomain import discover_role_ascension
    bad = {"d": Dgroup("d", [("CAUSE", ("A", "x"), ("B", "y"), ("C", "z"))])}   # arity 3
    with pytest.raises(ValueError):
        discover_role_ascension(bad)


# --- retrieval.engine: reject malformed expressions / library entries -------------------------
def test_expr_from_json_rejects_nonstring_head():
    from retrieval.engine import expr_from_json
    with pytest.raises(ValueError):
        expr_from_json([["NESTED"], "x"])                # head is a list, not a functor string


def test_load_library_rejects_malformed_entry(tmp_path):
    from retrieval.engine import load_library
    p = tmp_path / "lib.json"
    p.write_text(json.dumps({"ok": {"name": "n", "facts": []}, "broken": {"name": "n"}}))
    with pytest.raises(ValueError):
        load_library(p)


# --- retrieval.index / engine: cosine ties broken deterministically by name -------------------
def test_mac_index_query_is_deterministic_on_ties():
    from retrieval.engine import functor_vector, load_library
    from retrieval.index import MacIndex, linear_top_k
    lib = load_library(REPO / "retrieval" / "library" / "conformal_theorems.json")
    libvec = {n: functor_vector(g) for n, g in lib.items()}
    idx = MacIndex(libvec)
    q = {"NONEXISTENT_FUNCTOR": 1}                        # shares nothing -> every cosine ties at 0
    # the fallback exact-scan now breaks the total tie by name, so it agrees with the linear scan
    assert idx.query(q, max_hamming=0)["top_k"] == linear_top_k(q, libvec)


# --- analogy.examples: reject a malformed dgroup ----------------------------------------------
def test_from_concept_dgroup_rejects_malformed(tmp_path):
    from analogy import examples
    p = tmp_path / "dg.json"
    p.write_text(json.dumps({"attributes": [{"pred": "P"}], "relations": []}))   # missing 'arg'
    with pytest.raises(ValueError):
        examples.from_concept_dgroup(str(p))


# --- decomposer.markdown: a Path to a missing file fails loud, not silent inline --------------
def test_markdown_normalize_missing_path_fails_loud(tmp_path):
    from decomposer.adapters.markdown import normalize
    with pytest.raises(FileNotFoundError):
        normalize(tmp_path / "does_not_exist.md")


# --- analogy.cli: a half-specified --base/--target pair fails loud -----------------------------
def test_analogy_cli_half_specified_pair_errors():
    from analogy import cli
    with pytest.raises(SystemExit):                      # ap.error() exits, not a silent skip
        cli.main(["--base", "/tmp/only_base.json"])
