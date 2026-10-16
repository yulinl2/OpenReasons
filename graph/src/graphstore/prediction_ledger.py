"""Conjecture/provenance ledger for a bounded graph-instrument demo.

Four distinct evidentiary states MUST remain separate:
  1. a module exists and exposes a runnable callable;
  2. an experiment was actually executed (no evidence captured here);
  3. a structured result/outcome was recorded (none captured here);
  4. an independent validation was conducted (none captured here).

Likewise, a later hand-authored paper dgroup sharing projected predicates is
a POST-HOC STRUCTURAL MATCH, not independently confirmed paper discovery.
The C6 evaluator already named Gibbs–Candès before ACI was lifted.
Preserve the old fixture/structural gate while reporting the correct epistemic
status. See OpenReasons issue #65 and the MetaProof 2026-09-29 audit.
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
                 "refined_into": None, "experiment": None, "confirmed_by": None,
                 "experiment_evidence": {"module_present": False, "executed": False,
                                         "outcome_recorded": False,
                                         "independently_validated": False},
                 "paper_evidence": {"post_hoc_structural_match": False,
                                    "independent_confirmation": False}}
        if e["verdict"] == "uncertain" and cid in directions:
            entry["refined_into"] = {"id": cid, "scope": directions[cid]["scope_verdict"]}
            modname = f"graphstore.experiment_{cid.lower()}"
            try:
                mod = importlib.import_module(modname)
                entry["experiment"] = modname if hasattr(mod, "run_experiment") else None
                entry["experiment_evidence"]["module_present"] = bool(entry["experiment"])
            except ModuleNotFoundError:
                entry["experiment"] = None
        if cid in confirmations:
            paper = confirmations[cid]
            entry["confirmed_by"] = {
                "paper": paper,
                "structurally_verified": _confirms_structurally(repo, paper, e["projection"]),
                "evidence_type": "post_hoc_structural_match",
                "independent_confirmation": False}
            entry["paper_evidence"]["post_hoc_structural_match"] = bool(
                entry["confirmed_by"]["structurally_verified"])
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
            "available_experiment_modules": sum(
                1 for e in entries if e["experiment_evidence"]["module_present"]),
            "experiments_executed_with_evidence": sum(
                1 for e in entries if e["experiment_evidence"]["executed"]),
            "experiment_outcomes_recorded": sum(
                1 for e in entries if e["experiment_evidence"]["outcome_recorded"]),
            "independently_validated_experiments": sum(
                1 for e in entries if e["experiment_evidence"]["independently_validated"]),
            "post_hoc_paper_matches": sum(
                1 for e in entries if e["paper_evidence"]["post_hoc_structural_match"]),
            "independent_paper_confirmations": sum(
                1 for e in entries if e["paper_evidence"]["independent_confirmation"]),
            # Legacy fields now bear their literal evidentiary meaning (not
            # module existence or post-hoc paper links).
            "backed_by_experiment": sum(
                1 for e in entries if e["experiment_evidence"]["outcome_recorded"]),
            "confirmed_by_real_paper": sum(
                1 for e in entries if e["paper_evidence"]["independent_confirmation"]),
        },
    }


def main(argv=None) -> int:
    here = Path(__file__).resolve().parents[2]
    repo = here.parent
    led = build_ledger(repo)
    s = led["summary"]

    print("OpenReasons — evidence-tiered conjecture ledger (no blind confirmation claim)")
    print(f"  {s['n_conjectures']} analogical conjectures judged: "
          f"{s['plausible']} plausible, {s['uncertain']} uncertain, {s['implausible']} implausible")
    print(f"  {s['refined_into_directions']} uncertain -> refined into research directions, "
          f"{s['available_experiment_modules']} experiment modules available; "
          f"{s['experiments_executed_with_evidence']} documented runs; "
          f"{s['experiment_outcomes_recorded']} documented outcomes")
    print(f"  {s['post_hoc_paper_matches']} post-hoc encoded-paper matches; "
          f"{s['independent_paper_confirmations']} independent paper confirmations\n")
    for e in led["entries"]:
        tail = ""
        if e["refined_into"]:
            tail = f"  -> direction {e['refined_into']['id']} ({e['refined_into']['scope']}), {e['experiment']}"
        if e["confirmed_by"]:
            tail = (f"  -> POST-HOC MATCH to curated paper '{e['confirmed_by']['paper']}'"
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
        (s["post_hoc_paper_matches"] >= 1,
         "at least one fixture-level post-hoc match must be present"),
        (entries["C6"]["verdict"] == "plausible"
         and entries["C6"]["confirmed_by"]
         and entries["C6"]["confirmed_by"]["structurally_verified"],
         "C6 must have a fixture-level structural match to the curated ACI representation"),
    ]
    for ok, msg in checks:
        if not ok:
            raise SystemExit(f"prediction-ledger invariant violated: {msg}")
    print("\n  verified here: verdict labels, fixture-based structural match and "
          "experiment module availability only. No experiment outcome or independent "
          "prospective prediction is evidenced by this ledger.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
