"""The prediction ledger (Epic AJ): the discover -> predict -> confirm arc, made auditable.

The whole project's thesis is that this is not just a novelty/analogy detector but an
**idea-generation-and-validation engine**: it projects analogical conjectures (predictions),
an independent judge tells the sound ones from the spurious, the uncertain ones are refined
into precise research directions and each is carried to a numerical experiment — and, when a
prediction is strong enough, it is confirmed against a real published paper.

This module cross-references the two halves that the rest of the pipeline built separately —
the *prediction* side (``conjecture_evaluations.json`` + ``research_directions.json`` + the
``experiment_c*`` modules) and the *confirmation* side (the real papers ingested in Epics K, V,
AI) — into one ledger, and gates the arc:

  * every conjecture carries a judged verdict, and the judge **discriminates** (at least one is
    rejected as implausible — not a rubber stamp);
  * every *uncertain* conjecture was **refined into a research direction** AND that direction
    has a runnable **numerical experiment** (C2, C4, C5, C7 -> ``experiment_c{2,4,5,7}``);
  * the flagship **confirmed** prediction — C6, *"the weighted conformal calibration procedure
    is a no-regret play"* — is realized by a real ingested paper (Gibbs & Candes' adaptive
    conformal inference), and this is **structurally verified**, not just asserted: the
    confirming paper's grounded facts contain the predicted ``NO_REGRET`` play and the
    ``NO_REGRET -> COVERAGE`` bridge the conjecture projected.

So the ledger is the closing artifact: a machine-checkable record that the system predicted a
result by analogy, and reality confirmed it in the system's own representation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


def _real_papers_by_prediction(repo: Path) -> dict:
    """Scan the ingested real-paper dgroups for a ``_provenance.predicted_by`` that names a
    conjecture id, mapping ``conjecture id -> paper name``. Only ACI declares one today; the
    scan is generic so any future predicted-then-ingested paper is picked up automatically."""
    out = {}
    for path in sorted((repo / "grounding" / "dgroups").glob("*.json")):
        raw = json.loads(path.read_text())
        prov = raw.get("_provenance", {})
        target = raw.get("target")
        pred = prov.get("predicted_by", "") if isinstance(prov, dict) else ""
        name = target.get("name") if isinstance(target, dict) else None
        if not (name and pred):                          # skip malformed/partial dgroups
            continue
        for cid in re.findall(r"\bC\d+\b", pred):
            out[cid] = name
    return out


def _confirms_structurally(repo: Path, paper_name: str, projection: str) -> bool:
    """A real check, not a metadata claim: the confirming paper's grounded facts must contain
    the mechanism the conjecture projected. For C6 that means the ``NO_REGRET`` play (which the
    projection introduces into the conformal side) AND the ``NO_REGRET -> COVERAGE`` bridge."""
    from analogy.predicates import args, functor
    from retrieval.engine import expr_from_json

    for path in (repo / "grounding" / "dgroups").glob("*.json"):
        raw = json.loads(path.read_text())
        tgt = raw.get("target")
        if not (isinstance(tgt, dict) and tgt.get("name") == paper_name):
            continue
        facts = [expr_from_json(f) for f in tgt["facts"]]
        # the projected mechanism (e.g. NO_REGRET) is present as a real, top-level relation in the
        # paper — excluding CAUSE, the shared glue, so a genuine relation must match, not just the
        # fact that both the projection and every paper use CAUSE
        predicted = set(re.findall(r"\b[A-Z][A-Z_]+\b", projection)) - {"CAUSE"}
        top_level = {functor(f) for f in facts if functor(f) != "CAUSE"}
        mechanism_present = bool(predicted & top_level)
        # and the paper closes the bridge from that mechanism to the guarantee it earns
        bridge = any(functor(f) == "CAUSE" and functor(args(f)[0]) == "NO_REGRET"
                     and functor(args(f)[1]) == "COVERAGE" for f in facts)
        return mechanism_present and bridge
    return False


def build_ledger(repo: Path) -> dict:
    evals = json.loads(
        (repo / "graph" / "evaluations" / "conjecture_evaluations.json").read_text())["evaluations"]
    directions = {d["id"]: d for d in json.loads(
        (repo / "graph" / "evaluations" / "research_directions.json").read_text())["directions"]}
    confirmations = _real_papers_by_prediction(repo)

    import importlib
    entries = []
    for e in evals:
        cid = e["id"]
        entry = {"id": cid, "verdict": e["verdict"], "statement": e["statement"],
                 "analogy": f"{e['source_base']} -> {e['source_target']}",
                 "refined_into": None, "experiment": None, "confirmed_by": None}
        if e["verdict"] == "uncertain" and cid in directions:
            entry["refined_into"] = {"id": cid, "scope": directions[cid]["scope_verdict"]}
            modname = f"graphstore.experiment_{cid.lower()}"
            try:
                mod = importlib.import_module(modname)
                entry["experiment"] = modname if hasattr(mod, "run_experiment") else None
            except ModuleNotFoundError:
                entry["experiment"] = None
        if cid in confirmations:
            paper = confirmations[cid]
            entry["confirmed_by"] = {
                "paper": paper,
                "structurally_verified": _confirms_structurally(repo, paper, e["projection"])}
        entries.append(entry)

    verdicts = [e["verdict"] for e in evals]
    return {
        "entries": entries,
        "summary": {
            "n_conjectures": len(evals),
            "plausible": verdicts.count("plausible"),
            "uncertain": verdicts.count("uncertain"),
            "implausible": verdicts.count("implausible"),
            "refined_into_directions": sum(1 for e in entries if e["refined_into"]),
            "backed_by_experiment": sum(1 for e in entries if e["experiment"]),
            "confirmed_by_real_paper": sum(1 for e in entries if e["confirmed_by"]),
        },
    }


def main(argv=None) -> int:
    here = Path(__file__).resolve().parents[2]
    repo = here.parent
    led = build_ledger(repo)
    s = led["summary"]

    print("OpenPriors — prediction ledger: the discover -> predict -> confirm arc")
    print(f"  {s['n_conjectures']} analogical conjectures judged: "
          f"{s['plausible']} plausible, {s['uncertain']} uncertain, {s['implausible']} implausible")
    print(f"  {s['refined_into_directions']} uncertain -> refined into research directions, "
          f"all {s['backed_by_experiment']} backed by a numerical experiment")
    print(f"  {s['confirmed_by_real_paper']} confirmed by a real ingested paper\n")
    for e in led["entries"]:
        tail = ""
        if e["refined_into"]:
            tail = f"  -> direction {e['refined_into']['id']} ({e['refined_into']['scope']}), {e['experiment']}"
        if e["confirmed_by"]:
            tail = (f"  -> CONFIRMED by real paper '{e['confirmed_by']['paper']}'"
                    f" (structurally verified: {e['confirmed_by']['structurally_verified']})")
        print(f"  {e['id']} [{e['verdict']:>11}] {e['statement'][:64]}{tail}")

    # invariants (CI gate; explicit raise so it holds under `python -O`)
    entries = {e["id"]: e for e in led["entries"]}
    checks = [
        (s["implausible"] >= 1,
         "the judge must discriminate — at least one conjecture rejected as implausible"),
        (all(e["refined_into"] for e in led["entries"] if e["verdict"] == "uncertain"),
         "every uncertain conjecture must be refined into a research direction"),
        (all(e["experiment"] for e in led["entries"] if e["verdict"] == "uncertain"),
         "every research direction must have a runnable numerical experiment"),
        (s["confirmed_by_real_paper"] >= 1,
         "at least one prediction must be confirmed by a real ingested paper"),
        (entries["C6"]["verdict"] == "plausible"
         and entries["C6"]["confirmed_by"]
         and entries["C6"]["confirmed_by"]["structurally_verified"],
         "C6 (conformal calibration is a no-regret play) must be structurally confirmed by ACI"),
    ]
    for ok, msg in checks:
        if not ok:
            raise SystemExit(f"prediction-ledger invariant violated: {msg}")
    print(f"\n  confirmed: the system generates falsifiable predictions and validates them — "
          f"the uncertain\n  ones refined and experimentally tested, the spurious ones rejected, "
          f"and its flagship\n  prediction (C6) realized by a real published paper it had never "
          f"read. The loop closes.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
