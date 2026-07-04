"""Third real paper end-to-end (Epic AI): Gibbs & Candes, Adaptive Conformal Inference.

Parallels Epic K (arXiv 2006.06138, conformal) and Epic V (Nesterov, optimization), but with a
twist that is the whole point: **the system predicted this paper before reading it.** Conjecture
C6 (Epic AF), judged *plausible*, projected across the ``online_gradient_descent ~~
weighted-conformal`` analogy that *"the weighted conformal calibration procedure is a no-regret
play."* Gibbs & Candes (2021) is exactly that result in the real literature: an online gradient
update on the miscoverage level (a no-regret procedure with bounded {0,1} gradient feedback)
restores long-run coverage under arbitrary distribution shift.

So this driver does two things and asserts both:

  1. **decompose** (set cover) the paper against its priors — and find it is a genuine
     *cross-field synthesis*: covered by priors from BOTH online learning (``online_no_regret``)
     and conformal prediction (``conformal_prediction_set``), unlike Nesterov (all-optimization)
     or the counterfactual paper (all-conformal). The novel residual is the ACI online
     alpha-update rule (``ONLINE_UPDATE``, from the coverage errors) together with the
     ``NO_REGRET -> COVERAGE`` bridge and its distribution-shift robustness — the contribution
     neither field alone provides. (The guarantee is long-run / time-averaged empirical
     coverage, not per-step marginal coverage — the latter is unattainable under adversarial
     shift);
  2. **situate cross-domain** — the paper's ``NO_REGRET`` is discovered at the same ``PC/2``
     structural-property role, so the paper is analogous to BOTH the online-learning results and
     the conformal results, sitting at the junction of the two fields. That junction *is* the C6
     conjecture, now instantiated by a real published paper.
"""

from __future__ import annotations

import json
from pathlib import Path

from analogy.predicates import Dgroup
from retrieval.decompose import decompose
from retrieval.engine import expr_from_json, load_library

from .crossdomain import _load_corpus, cross_domain_analogies, discover_role_ascension


def run(repo: Path) -> dict:
    paper = json.loads((repo / "grounding" / "dgroups" / "aci_paper.json").read_text())["target"]
    target = Dgroup(paper["name"], [expr_from_json(f) for f in paper["facts"]])

    priors = load_library(repo / "retrieval" / "library" / "aci_priors.json")
    dec = decompose(target, priors)

    conf, _, _ = _load_corpus(repo / "retrieval" / "library" / "conformal_theorems.json")
    online, _, _ = _load_corpus(repo / "grounding" / "dgroups" / "online_learning_corpus.json")
    aci = {paper["name"]: target}
    ascension = discover_role_ascension(conf, online, aci)
    to_online = cross_domain_analogies(aci, online, ascension=ascension)
    to_conformal = cross_domain_analogies(aci, conf, ascension=ascension)
    return {"decompose": dec, "ascension": ascension,
            "to_online": to_online, "to_conformal": to_conformal}


def main(argv=None) -> int:
    here = Path(__file__).resolve().parents[2]
    repo = here.parent
    res = run(repo)
    dec, asc = res["decompose"], res["ascension"]

    print(f"paper '{dec['target']}' ({dec['n_facts']} facts) — Gibbs & Candes 2021, "
          f"Adaptive Conformal Inference")
    print(f"  predicted by the system as conjecture C6 (judged plausible): "
          f"'weighted conformal calibration is a no-regret play'")
    print(f"  = cross-field synthesis of priors from TWO fields: {', '.join(dec['covering_priors'])}")
    print(f"  covered {dec['covered_facts']}/{dec['n_facts']} ({dec['coverage_fraction']})")
    print(f"  novel contribution (residual): {', '.join(dec['novel_contributions'])}")
    print(f"    ...including the NO_REGRET -> COVERAGE bridge (the C6 mechanism itself)")
    print(f"\n  its no-regret play is discovered at role {asc.get('NO_REGRET')} (same as the "
          f"other fields'\n  structural property), so the paper sits at the analogy junction:")
    for a in res["to_online"][:1]:
        print(f"    ~~ online:    {a['b']} (score {a['score']})")
    for a in res["to_conformal"][:1]:
        print(f"    ~~ conformal: {a['b']} (score {a['score']})")

    # invariants (CI gate; explicit raise so it holds under `python -O`)
    residual = set(dec["residual_facts"])
    bridge = any(r.startswith("CAUSE(NO_REGRET(") and "COVERAGE(" in r for r in residual)
    checks = [
        (set(dec["covering_priors"]) == {"online_no_regret", "conformal_prediction_set"},
         "ACI must be covered by priors from BOTH fields (online + conformal)"),
        (0.0 < dec["coverage_fraction"] < 1.0,
         "a real cross-field synthesis: partial reuse, non-empty residual"),
        (bridge, "the novel residual must contain the NO_REGRET -> COVERAGE bridge (C6)"),
        (any(s.startswith("DISTRIBUTION_SHIFT") for s in dec["novel_contributions"]),
         "the residual must include the distribution-shift robustness"),
        (asc.get("NO_REGRET", "").startswith("ROLE::PC::"),
         "the no-regret play must be discovered as the PC/2 structural-property role"),
        (any(a["a"] == "adaptive_conformal_inference"
             and a["b"] in {"online_gradient_descent", "online_strong_convexity"}
             and a["score"] >= 3.0 for a in res["to_online"]),
         "ACI must be cross-domain analogous to an online-learning result"),
        (any(a["a"] == "adaptive_conformal_inference"
             and a["b"] == "weighted_conformal" and a["score"] >= 3.0 for a in res["to_conformal"]),
         "ACI must ALSO be cross-domain analogous to a conformal result (the junction)"),
    ]
    for ok, msg in checks:
        if not ok:
            raise SystemExit(f"realpaper3 invariant violated: {msg}")
    print(f"\n  confirmed: a real published paper the system PREDICTED — decomposed as a genuine "
          f"cross-field\n  synthesis (online no-regret + conformal set), with the "
          f"no-regret->coverage bridge as its\n  contribution, sitting at the analogy junction "
          f"of the two fields it unites. C6 realized.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
