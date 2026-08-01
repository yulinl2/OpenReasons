# OpenPriors — The Story So Far

> *Open-source your ideas, not just your code.*

**A self-contained introduction, written at the close of Epic AL (consolidate · package ·
demonstrate), intended as the entry point for follow-up studies.** Everything below is
reproducible from this repository with `make setup && make demonstrate`; every number was
recomputed from the pipeline's live output at the time of writing.

---

## 1 · What this is

OpenPriors is an experiment in making a machine do the things a *researcher* does with ideas —
not retrieve documents, but **situate a result among its priors, trace what it builds on, find
what it is structurally analogous to in another field, predict what that analogy implies, tell
the sound predictions from the spurious, refine the open ones into research programs, and test
them**.

It began as a novelty detector and ended as a closed, machine-audited
**discover → predict → confirm** loop. Its flagship run: the system discovered, without
supervision, that five mathematical literatures share one causal skeleton; projected from that
analogy the conjecture *"the weighted conformal calibration procedure is a no-regret play"*;
judged it plausible; and was then confirmed by **a real published paper it had never read** —
Gibbs & Candès' *Adaptive Conformal Inference* — whose grounded content contains exactly the
predicted mechanism. The confirmation is checked structurally, in the system's own
representation, by a deterministic gate that CI enforces.

## 2 · The thesis

Scientific ideas are treated as **structured objects**: every result is decomposed into an
(object, attribute, relation) description — predicate-calculus facts over entities, with
higher-order `CAUSE` facts gluing premises to guarantees. On that representation,
**structure mapping** (Gentner's SME tradition: *isomorphism under renaming, not lexical
overlap*) gives operational definitions of the researcher's verbs:

- **Novelty** = 1 − (best structural coverage by any known prior). What no prior covers is the
  *novel residual* — named, not just scored.
- **Lineage** = `extends` edges recovered when one result's structure contains and refines
  another's. No citation data is used.
- **Analogy** = a bijective, systematicity-favoring correspondence between two results'
  relational structures — across fields, where surface vocabulary shares nothing.
- **Conjecture** = a candidate inference: structure present in one side of an analogy and
  missing from the other, projected across the correspondence as a falsifiable claim.
- **Confirmation** = a later-ingested real result whose grounded facts realize a projected
  conjecture — checked by graph containment, not by assertion.

The bet under test: represent reasoning structurally and gate every step deterministically, and
the "creative" moves of research — noticing deep analogies, generating hypotheses, telling good
ones from bad — become auditable computations.

## 3 · The doctrine (how it was built)

One governing rule — **论证 / 构建 / 独立检验** (*Argue / Build / Independently Verify*) — made
concrete as four engineering principles:

1. **Deterministic wherever checkable.** All alignment, retrieval, transfer, scoring, and
   gating is pure-Python, dependency-light, seeded, and byte-reproducible
   (`SOURCE_DATE_EPOCH` pinned). LLM sub-agents are used *only* where natural-language
   understanding is irreducible (lifting prose into predicate calculus; judging a conjecture's
   scientific plausibility) — in-session, at zero marginal API cost, and never trusted:
   every sub-agent output is committed and admitted only through a deterministic gate.
2. **Grounding.** Every symbol a sub-agent introduces must be a **verbatim substring of the
   source prose**, and every entity used in a fact must be grounded — checked mechanically
   (`grounding.verify`). This is the anti-hallucination contract: nothing enters the graph
   that cannot be pointed to in a real text.
3. **Verify the verifier.** Every gate is unit-tested to **fail on broken input** — tampered
   artifacts, empty evaluation sets, fabricated projections, non-verbatim groundings. A gate
   that cannot go red is treated as no gate at all.
4. **Everything CI-gated, everything reproducible.** Generated documents (the audit report,
   the demonstration transcript, the dashboard, committed run artifacts) carry staleness
   gates: CI regenerates them and fails on drift. Packaging itself is a checked claim (see §8).

## 4 · The system

Seven packages in one monorepo, consolidated behind a root meta-package and one command:

| Package | Role in the pipeline |
|---|---|
| `decomposer/` | Raw LaTeX/HTML/Markdown → clean nested hierarchical structure (char-coverage conservation, schema, idempotence, differential oracle vs LaTeXML). |
| `concept_graph/` | Lifts decomposer output into the (object, attribute, relation) representation + reasoning DAG; the bridge to SME. |
| `matcher/` | MAC content-vector retrieval; renaming-invariance; systematicity foundations. |
| `analogy/` | The SME aligner: structural correspondences, trickle-down systematicity, candidate inferences, skolem entities, minimal ascension; validated on the textbook solar-system → Rutherford-atom mapping. |
| `grounding/` | Prose → grounded predicate-calculus description groups (dgroups), behind the verbatim-grounding gate. |
| `retrieval/` | Library-scale MAC/FAC nearest-prior search; full-proof set-cover decomposition (novel residual); SimHash-LSH ANN. |
| `graph/` | The unified graph store: multi-literature build, unsupervised role discovery, cross-domain analogy, conjecture transfer, the evaluation gate, novelty annotation, query DSL, JSON Schema, the four experiments, and the prediction ledger. |
| `openpriors/` (root) | The consolidation layer: `openpriors run · pipeline · query · experiment · ledger · report · demo · demonstrate · version`. |

Data path, end to end: **raw document → decompose → ground → one unified graph → align/
retrieve (novelty, lineage) → discover cross-domain analogies → transfer conjectures → judge →
refine → experiment → confirm against newly ingested reality.**

## 5 · The corpus

Five literatures, **12 grounded results**, three real papers ingested end-to-end:

- **conformal prediction** — split conformal, weighted conformal, and an arXiv paper on
  conformal inference for counterfactuals (2006.06138), the original novelty case study;
- **optimization** — Banach contraction, gradient descent under strong convexity, plus a real
  Nesterov-acceleration paper;
- **learning theory** — VC and margin generalization;
- **martingale concentration** — McDiarmid and Bernstein;
- **online learning / regret** — online gradient descent and its strong-convexity variant,
  plus Gibbs & Candès' *Adaptive Conformal Inference* (the confirming paper).

Every fact of every result is grounded to a verbatim span of its source prose. The unified
graph over this corpus: **363 nodes** (12 result, 112 fact, 25 functor, 66 entity,
148 conjecture) and **665 edges**, with reified n-ary facts and nested `CAUSE` structure
losslessly reconstructable.

## 6 · How it unfolded (epics A → AL)

The project was built as ~38 epics, one PR at a time, each landing green:

- **Foundations (A–J).** The decomposer front end; the concept-graph bridge; the SME aligner
  and MAC/FAC retrieval; proof-depth set-cover decomposition; HTML-native ingestion;
  trickle-down systematicity; ANN indexing at scale.
- **First real paper and the unified graph (K–T).** A real arXiv paper run end-to-end and its
  novel residual named (`COUNTERFACTUAL`, `NESTED`); reasoning lineage recovered; everything
  unified into one queryable graph; cross-domain analogy edges; **unsupervised role
  discovery**; conjecture transfer; the sub-agent evaluation loop behind a deterministic gate;
  the capstone driver and query DSL.
- **Scaling the web (U–X).** A fourth literature (concentration) joined the analogy web with
  no new design; a second real paper (Nesterov); per-result novelty scoring; a formal JSON
  Schema + validator for the graph.
- **Closing the loop (Y–AJ).** Uncertain conjectures refined into research directions; each
  direction carried to a numerical experiment (C2, C4, C5, C7); a fifth literature (online
  learning) joined; a discrimination/negative-control epic; the third real paper (ACI)
  **confirming prediction C6**; and the **prediction ledger** — the machine-checkable record
  of the whole discover → predict → confirm arc.
- **Hardening and consolidation (AK–AL).** Branch coverage to ~93% with every entrypoint under
  test; a cross-package robustness audit (16 defects fixed, each pinned by a regression that
  fails on the pre-fix code); packaging as a verified claim; the unified CLI; and
  `DEMONSTRATION.md`, a narrated transcript recomputed live and gated against staleness.

## 7 · Principal results

**R1 — Five literatures share one causal skeleton, discovered unsupervised.** Roles are read
from each functor's position in `CAUSE` facts alone (premise-of, conclusion-of, or both — no
hand-coded correspondences, no lexical cues). The discovery: every field has exactly one
**structural-property pivot** — a binary relation that is *both* driven by the field's
assumptions *and* drives its guarantee (`ROLE::PC::2`) — and the five pivots align:

| Field | Pivot (`ROLE::PC::2`) | Guarantee (`ROLE::C::2`) |
|---|---|---|
| conformal | `WEIGHTED_EXCHANGEABLE` | `COVERAGE` |
| optimization | `CONTRACTION` | `LINEAR_CONVERGENCE` |
| learning theory | `UNIFORM_CONVERGENCE` | `GENERALIZATION` |
| concentration | `BOUNDED_MARTINGALE` | `CONCENTRATION` |
| online learning | `NO_REGRET` | `SUBLINEAR_REGRET` |

*weighted-exchangeability : coverage :: contraction : convergence :: uniform-convergence :
generalization :: bounded-martingale : concentration :: no-regret : sublinear regret.* The
fourth and fifth fields joined with **zero engine changes** — the same mechanism kept firing.
In total: 19 roles discovered, **40 cross-domain analogies**; `weighted_conformal` alone is
found analogous to eight results spanning all four other literatures. A committed negative
control verifies the machinery is discriminating rather than permissive.

**R2 — Lineage from structure alone.** With no citation data, the graph recovers each field's
development line, e.g. *counterfactual-conformal paper → weighted conformal → split conformal*
and *Bernstein → McDiarmid*, *margin → VC*.

**R3 — Novelty that names its residual.** The counterfactual-conformal paper scores novelty
0.22 against its nearest prior (weighted conformal) with the residual identified as exactly its
counterfactual/nested-interval contributions — a calibrated judgment, not a similarity score.

**R4 — Conjectures generated and judged, discriminatingly.** 148 falsifiable conjectures were
projected across the analogy web. Seven were carried through the full judgment loop: **2
plausible, 4 uncertain, 1 implausible**. The judge is not a rubber stamp — it rejected the
projected claim that a finite-capacity premise underlies weighted exchangeability (conformal
inference is distribution-free), and the rejection is itself a ledger invariant.

**R5 — Every uncertain conjecture became a tested research program.** All four uncertain
conjectures were refined into precise research directions, each with its own pure-Python
numerical experiment, all four run and green in CI:

- **C2** (importance reweighting): the L²(μ) contraction modulus of the reweighted operator is
  governed by the χ² divergence between distributions.
- **C4** (ERM fixed point): on a Gaussian-mixture EM operator, the projected Banach bound
  ‖θ̂ₙ − θ*‖ ≤ εₙ/(1 − κ) holds for every sample size, at the 1/√n rate.
- **C5** (no-regret fixed point): on two-player quadratic games, vanilla OGD's empirical rate
  equals the spectral radius in every phase cell — convergence iff η < 2μ/L², with averaged
  play converging while the last iterate wanders (the folk theorem, recovered numerically).
- **C7** (curvature vs regret): the informed step contracts at 1 − 1/κ while the
  regret-optimal schedule decays only polynomially — a quantified *price of robustness* that
  grows with conditioning.

**R6 — The flagship: a prediction confirmed by reality.** Conjecture **C6**, projected from
the online ↔ conformal analogy, states that *weighted conformal calibration is a no-regret
play*. Judged plausible. Gibbs & Candès' *Adaptive Conformal Inference* — a real published
paper, ingested only afterwards — **is that paper**: its grounded facts contain the predicted
`NO_REGRET` play and the projected `NO_REGRET → COVERAGE` causal bridge, and it decomposes as
a cross-field synthesis sitting at the analogy junction the system had drawn. The prediction
ledger cross-references the prediction side against the confirmation side and enforces the
arc's invariants in CI: the judge discriminates; every uncertain conjecture has a direction
and a runnable experiment; and C6's confirmation is **structurally verified** — the loop
closes.

## 8 · How much to trust it

- **≈300 tests** (298 at this snapshot) across every package plus cross-cutting suites;
  **11 CI workflows**; branch coverage ~93%.
- Every deterministic gate is *itself* tested to fail on tampered input (fabricated
  projections, empty evaluation sets, non-verbatim groundings, malformed facts).
- Every generated document — `REPORT.md`, `DEMONSTRATION.md`, the dashboard, committed run
  artifacts — is regenerated in CI and fails on drift; transcripts are byte-stable.
- **Packaging is a checked claim**: all 8 wheels build, install into a fresh venv, import, and
  run from outside the source tree, in CI.
- The work was adversarially reviewed throughout: every PR got an external automated review
  (one such review caught a real sign error in the C5 equilibrium computation — fixing it is
  what surfaced the folk-theorem result), and the final epics were audited by independent
  multi-agent verification passes that executed real breakage attempts (the last audit:
  5 confirmed defects, 0 false alarms, all fixed before merge).
- Zero marginal API cost: all NL judgment was done by in-session sub-agents, committed, and
  gated.

## 9 · Limitations (read before planning follow-ups)

1. **Scale.** Twelve results across five literatures is a curated micro-corpus. Ingestion of
   the graph-layer corpora involved sub-agent lifting with human-free but small-N curation;
   the analogy web's behavior at 100× the results is untested.
2. **The judge is an LLM.** The evaluation gate guarantees well-formedness, grounding in real
   transfer output, and discrimination — it does not guarantee scientific correctness of a
   verdict. N = 7 judged conjectures.
3. **One confirmed prediction.** C6 is a genuine, structurally verified discover → predict →
   confirm instance, but a single instance. The arc is demonstrated, not yet measured (no
   base rate, no prospective pre-registration protocol yet).
4. **Role discovery reads `CAUSE` position only.** Richer role lattices (argument types,
   quantifier structure, proof-role context) are unexplored.
5. **Near transfer.** All five literatures are mathematical-statistical; the analogies are
   deep but the domains are cousins. Far-domain transfer (e.g. into biology or economics) is
   untested.
6. **Experiments are illustrative numerics** — small, pure-Python, existence-style
   demonstrations of each direction's central quantitative claim, not exhaustive studies.

## 10 · Where follow-up studies could go

1. **Scale the corpus** — automate decompose → ground for arXiv-scale ingestion (PDF included)
   and measure how the role/analogy discovery behaves as literatures grow.
2. **Prospective prediction protocol** — pre-register conjectures in the ledger *before*
   scanning the literature, then ingest candidate confirming papers blind; estimate a real
   confirmation base rate (turn R6 from an instance into a statistic).
3. **Far-domain transfer** — add literatures with no shared mathematical vocabulary and test
   whether `CAUSE`-position roles still align meaningfully.
4. **Richer ascension** — learn type lattices / role vocabularies beyond `CAUSE` position;
   study when minimal ascension over-merges (the discrimination control gives a harness).
5. **Judge calibration** — collect human expert verdicts on projected conjectures and measure
   the sub-agent judge against them; explore panels and adversarial judging.
6. **Active discovery** — feed high-novelty, high-plausibility conjectures to a literature-
   search agent as queries: the system proposing, the literature disposing, at scale.
7. **A live open problem** — run the full loop on a currently open question and let a
   projected conjecture drive a new (human) proof or experiment.

## 11 · Map of the repository

| Artifact | What it is |
|---|---|
| `README.md` | Orientation: pipeline diagram, epic table, run instructions. |
| `DEMONSTRATION.md` / `make demonstrate` | The whole arc, one narrated reproducible run (recomputed live; staleness-gated). |
| `REPORT.md` / `make report` | The consolidated technical audit report — every literature, lineage, analogy, role, conjecture, direction, and experiment, all figures computed live. |
| `docs/index.html` → [demo.open-priors.org](https://demo.open-priors.org/) | The interactive dashboard: four zoom levels from a children's story to the raw audit graph. |
| `ROADMAP.md` | Governance: the epic → iteration → step method, branch/CI/backup policy. |
| `graph/src/graphstore/prediction_ledger.py` / `openpriors ledger` | The closing artifact: the machine-checkable discover → predict → confirm record. |
| `graph/evaluations/` | The committed conjecture judgments and research directions (sub-agent output, deterministically gated). |
| `tests/` + per-package `tests/` | The gates — including the tests that prove the gates fail on broken input. |

*Start with `make setup && make demonstrate`, then read `DEMONSTRATION.md` next to
`REPORT.md`. The one-command surface is `openpriors <verb>`.*

---

**Status at this snapshot:** epics A–AL complete and merged (or in final review); five
literatures; 12 grounded results; 19 discovered roles; 40 cross-domain analogies; 148
projected conjectures; 7 judged (2 plausible · 4 uncertain · 1 implausible); 4 research
directions, each with a green numerical experiment; **1 prediction structurally confirmed by a
real published paper**. The loop closes — and everything above is one `make demonstrate` away
from being recomputed in front of you.
