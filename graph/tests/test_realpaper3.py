"""Third real paper end-to-end (Epic AI): Gibbs & Candes, Adaptive Conformal Inference.

The paper the system predicted. Conjecture C6 (judged plausible) projected that weighted
conformal calibration is a no-regret play; this ingests the real Gibbs & Candes paper and checks
it (a) grounds, (b) decomposes as a genuine CROSS-FIELD synthesis (online + conformal priors)
whose novel residual is the NO_REGRET -> COVERAGE bridge, and (c) sits at the analogy junction of
the two fields — the C6 conjecture realized by a real publication.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(REPO / "analogy" / "src"))
sys.path.insert(0, str(REPO / "retrieval" / "src"))
sys.path.insert(0, str(REPO / "grounding" / "src"))

from graphstore.realpaper3 import run

REP = run(REPO)


def test_paper_and_priors_are_grounded():
    from grounding.verify import check_section
    paper = json.loads((REPO / "grounding" / "dgroups" / "aci_paper.json").read_text())["target"]
    assert check_section(paper)["passed"]
    lib = json.loads((REPO / "retrieval" / "library" / "aci_priors.json").read_text())
    for k, v in lib.items():
        if not k.startswith("_"):
            assert check_section(v)["passed"], k


def test_decomposition_is_a_cross_field_synthesis():
    dec = REP["decompose"]
    # the defining signature: covered by priors from TWO DIFFERENT fields (unlike K / V)
    assert set(dec["covering_priors"]) == {"online_no_regret", "conformal_prediction_set"}
    assert 0.0 < dec["coverage_fraction"] < 1.0 and dec["residual_facts"]


def test_novel_residual_is_the_c6_bridge_and_shift_robustness():
    dec = REP["decompose"]
    # the contribution is exactly the mechanism C6 predicted: no-regret -> coverage, under shift
    assert any(r.startswith("CAUSE(NO_REGRET(") and "COVERAGE(" in r for r in dec["residual_facts"])
    assert any(s.startswith("DISTRIBUTION_SHIFT") for s in dec["novel_contributions"])
    assert any(s.startswith("COVERAGE") for s in dec["novel_contributions"])
    # the ACI online alpha-update rule (from the coverage errors) is part of the contribution too
    assert any(s.startswith("ONLINE_UPDATE") for s in dec["novel_contributions"])
    # the borrowed conformal machinery (the base set) is NOT in the residual
    assert not any(s.startswith("CONFORMAL_INTERVAL") for s in dec["novel_contributions"])


def test_no_regret_play_is_the_structural_property_role():
    asc = REP["ascension"]
    assert asc.get("NO_REGRET", "").startswith("ROLE::PC::")
    assert asc.get("COVERAGE", "").endswith("::C::2")       # the guarantee role


def test_paper_sits_at_the_junction_of_online_and_conformal():
    # analogous to an online-learning result...
    a_on = next((x for x in REP["to_online"]
                 if x["a"] == "adaptive_conformal_inference"
                 and x["b"] in {"online_gradient_descent", "online_strong_convexity"}), None)
    assert a_on is not None and a_on["score"] >= 3.0
    # ...AND to a conformal result — the same paper bridges both fields (C6 realized)
    a_cf = next((x for x in REP["to_conformal"]
                 if x["a"] == "adaptive_conformal_inference" and x["b"] == "weighted_conformal"),
                None)
    assert a_cf is not None and a_cf["score"] >= 3.0
    # the no-regret play is what corresponds across the online bridge
    assert a_on["correspondences"].get("the_play") == "the_play"


def test_paper_is_grounded_in_the_committed_c6_prediction():
    # tie-back: the paper's provenance names the conjecture that predicted it, and C6 exists
    prov = json.loads(
        (REPO / "grounding" / "dgroups" / "aci_paper.json").read_text())["_provenance"]
    assert "C6" in prov["predicted_by"]
    evals = json.loads(
        (REPO / "graph" / "evaluations" / "conjecture_evaluations.json").read_text())["evaluations"]
    c6 = next(e for e in evals if e["id"] == "C6")
    assert c6["verdict"] == "plausible" and "NO_REGRET" in c6["projection"]
