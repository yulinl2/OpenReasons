"""The prediction ledger (Epic AJ): the discover -> predict -> confirm arc, gated.

Cross-references the prediction side (conjectures, research directions, experiment modules)
against the confirmation side (real ingested papers) and checks the arc closes: the judge
discriminates, every uncertain conjecture is refined + experimentally tested, and the flagship
C6 prediction is structurally confirmed by the real ACI paper. The confirmation check is
unit-tested to FAIL on a paper that lacks the predicted mechanism (verify the verifier).
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(REPO / "analogy" / "src"))
sys.path.insert(0, str(REPO / "retrieval" / "src"))
sys.path.insert(0, str(REPO / "grounding" / "src"))

from graphstore.prediction_ledger import (_confirms_structurally, _real_papers_by_prediction,
                                          build_ledger)

LED = build_ledger(REPO)
BY_ID = {e["id"]: e for e in LED["entries"]}


def test_every_conjecture_is_judged_and_the_judge_discriminates():
    assert LED["summary"]["n_conjectures"] == len(BY_ID) >= 7
    for e in LED["entries"]:
        assert e["verdict"] in {"plausible", "uncertain", "implausible"}
    # not a rubber stamp: at least one rejected, at least one accepted
    assert LED["summary"]["implausible"] >= 1 and LED["summary"]["plausible"] >= 1


def test_every_uncertain_conjecture_is_refined_and_experimented():
    uncertain = [e for e in LED["entries"] if e["verdict"] == "uncertain"]
    assert uncertain
    for e in uncertain:
        assert e["refined_into"] is not None, e["id"]
        assert e["experiment"] and e["experiment"].startswith("graphstore.experiment_"), e["id"]
    # the count is self-consistent
    assert LED["summary"]["refined_into_directions"] == LED["summary"]["backed_by_experiment"] \
        == len(uncertain)


def test_flagship_prediction_c6_is_structurally_confirmed_by_the_real_paper():
    c6 = BY_ID["C6"]
    assert c6["verdict"] == "plausible"
    assert c6["confirmed_by"] is not None
    assert c6["confirmed_by"]["paper"] == "adaptive_conformal_inference"
    assert c6["confirmed_by"]["structurally_verified"] is True
    # the confirmation was discovered from the paper's own provenance, generically
    assert _real_papers_by_prediction(REPO).get("C6") == "adaptive_conformal_inference"


def test_confirmation_is_a_real_structural_check_not_a_metadata_claim():
    # verify the verifier: a paper WITHOUT the predicted mechanism must not be "confirmed"
    # (nesterov has no NO_REGRET play, so C6's projection cannot be confirmed by it)
    assert not _confirms_structurally(
        REPO, "nesterov_acceleration",
        "CAUSE(BOUNDED_GRADIENTS(skolem:the_losses, the_weights), NO_REGRET(cal_test, the_weights))")
    # and a nonexistent paper is not confirmed
    assert not _confirms_structurally(REPO, "no_such_paper", "NO_REGRET(x, y)")


def test_plausible_but_unconfirmed_predictions_stay_open():
    # C1 (conformal has a fixed point) is plausible but not tied to an ingested paper -> open
    c1 = BY_ID["C1"]
    assert c1["verdict"] == "plausible" and c1["confirmed_by"] is None
