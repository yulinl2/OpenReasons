# OpenPriors: Machine-Auditable Idea-Work — A Production Case Study

**Operationalizing the researcher's verbs — novelty, lineage, analogy, conjecture,
confirmation — as deterministic computations over grounded structure, built by agent
sessions under a verification-first doctrine, with a closed discover → predict → confirm
loop as the flagship result.**

*Self-contained technical report, 2026-08-01. All quantitative claims carry receipts into
the public repository (Appendix B); counts are stated as of the pinned record — `main` at
`49f62fb`, the Epic-AL branch at `4530012` — unless dated otherwise; every headline number
is recomputable by one command (`openpriors demonstrate`); inference is labeled as
inference. This report follows the reporting conventions of a companion forensic case study
of the same principal's agent ecosystem (see §10).*

---

## Abstract

OpenPriors is a production experiment in **machine-auditable idea-work**: represent
scientific results as (object, attribute, relation) structures grounded verbatim in their
source prose, and make the moves a researcher performs on ideas — situating a result among
priors, tracing what it builds on, finding cross-field analogies, predicting what an
analogy implies, judging predictions, and confirming them against reality — as
deterministic, receipt-carrying computations. The system was built over a compressed
production window (repository created 2026-05-04; the build sprint ran 2026-06-21 →
2026-07-05 across 38 lettered epics, ≈53 pull requests, ~11,600 lines of pure-Python of
which ~29% are tests) by ephemeral coding-agent sessions under a single human principal,
governed by one doctrine: **论证 / 构建 / 独立检验** (argue / build / independently
verify) — LLM sub-agents only at natural-language boundaries, every sub-agent output
committed and admitted only through a deterministic gate, and every gate unit-tested to
fail on tampered input. Over a five-literature corpus (conformal prediction, optimization,
learning theory, martingale concentration, online learning; 12 grounded results including
three real papers), the system: discovered **unsupervised, from causal position alone**,
that all five fields share one skeleton — a structural-property pivot driving a guarantee
(19 roles; 40 cross-domain analogies; two later fields joined with zero engine changes);
recovered development lineages without citation data; scored novelty with *named*
residuals; projected 148 falsifiable conjectures, of which 7 were judged (2 plausible ·
4 uncertain · 1 rejected), all 4 uncertain ones refined into research directions each
carried to a green numerical experiment; and had its flagship conjecture — *"the weighted
conformal calibration procedure is a no-regret play"* (C6) — **realized by Gibbs & Candès'
Adaptive Conformal Inference, a real published paper the system had not ingested when the
conjecture was generated, with the confirmation checked structurally** (graph containment
of the predicted mechanism in the paper's grounded facts), enforced as a CI invariant. The
report also contributes what the verification machinery caught: an 11-item defect
phenomenology of agent-built research code (vacuous gates, stale derived artifacts, two
recurring nondeterminism sources, checker-side defects, CI blind spots, a near-miss
false-positive confirmation), seven candidate laws with falsifiers under a refutable
central thesis, twelve mechanical invariants, and a nine-card portable protocol suite
including a prospective-prediction protocol designed to remove this study's main confound —
that C6 is a **retrodiction** (the confirming paper predates the system, and the
NL-boundary steps cannot be certified free of pretraining exposure to it; the deterministic
steps can). A novelty ledger against the classic literature corrects the study's own
initial claims: the alignment machinery is deliberately inherited (SME, MAC/FAC), and the
surviving candidate-novel core is the *gated grounding contract*, the *causal-position role
ascension*, and the *structurally-verified closed loop*.

---

## 1. Introduction

### 1.1 The object and the questions

By "machine-auditable idea-work" this report means an arrangement with four properties:

1. **Structured representation.** Every scientific result is decomposed into
   predicate-calculus facts over entities — 1-place attributes, n-ary relations, and
   higher-order `CAUSE` facts gluing premises to guarantees — not embeddings or summaries.
2. **A grounding contract.** Every symbol in that representation must be a verbatim
   substring of the source prose, and every entity used in a fact must be grounded;
   checked mechanically, with the checker itself tested to fail on violations.
3. **A determinism boundary.** LLM sub-agents act only where natural language is
   irreducible (lifting prose into facts; judging a conjecture's plausibility); their
   outputs are committed artifacts admitted through deterministic gates. Everything else —
   alignment, retrieval, transfer, scoring, confirmation — is seeded pure-Python.
4. **Receipts everywhere.** Every claim the system makes about the corpus resolves to a
   committed artifact, a gate, and a test; generated documents are recomputed in CI and
   diffed against their committed versions.

Five questions organized the work:

- **RQ0 (methodological, first in practice).** Can a research pipeline *built almost
  entirely by LLM agent sessions* be made trustworthy enough to carry scientific claims —
  and by which mechanisms?
- **RQ1.** Do the researcher's idea-verbs (novelty, lineage, analogy, conjecture,
  confirmation) admit deterministic operationalization over grounded structure?
- **RQ2.** Does cross-field structure exist that *unsupervised* role discovery — reading
  nothing but each functor's position in `CAUSE` facts — can find?
- **RQ3.** Can the loop close: a projected conjecture, judged, refined, experimentally
  tested, and confirmed against a real paper, with the confirmation machine-checked?
- **RQ4.** What failure phenomenology does agent-built research code exhibit, and which
  mechanical invariants contain it?

### 1.2 Why the case is evidentially unusual

- **Public total retention.** The entire record is public: every artifact, every committed
  sub-agent judgment, every defect and its fix, every review thread, across ≈53 pull
  requests and 54 squash-merged commits on `main`. Commit messages carry session-attribution
  trailers, so generating-process provenance is in-band.
- **Live recomputability.** Every headline number in this report regenerates from one
  command (`openpriors demonstrate`), whose transcript is byte-stable and CI-diffed against
  the committed copy — the report's numbers cannot silently drift from the system's actual
  output (receipt: `tests/test_cli.py::test_committed_demonstration_is_not_stale`).
- **Sabotage-validated checkers as standing discipline.** Every gate ships with tests that
  plant tampered input and require the gate to go red (e.g. the evaluation gate's tamper
  suite in `graph/tests/test_evaluate.py`), so "the gate passed" is evidence, not decor.
- **The negative record is retained.** The stale artifacts, the vacuous-gate defect, the
  sign error, the CI blind spots, and the audits that found them are all in-history with
  their fixes — usable as data (§6.3), not embarrassment to be squashed.

### 1.3 Contributions

1. A precise architectural description of a production idea-work engine: seven packages,
   one meta-package, the grounding contract, and the doctrine's operators and deliberate
   absences (§2).
2. The representation and corpus: five literatures, 12 grounded results, three real
   papers, one unified graph of 363 nodes / 665 edges (§3).
3. The verification machinery with measured outcomes: gate inventory with red-test
   discipline, the determinism and staleness regimes, two independent adversarial audits
   (16 confirmed defects; then 5 confirmed / 0 false alarms), ~93% branch coverage, 298
   tests, 11 CI workflows, and packaging as a checked claim (§4).
4. Ten findings with receipts (§6.1–6.2), headed by the five-field causal skeleton and the
   structurally-confirmed prediction, plus an 11-item defect phenomenology of agent-built
   research code with countermeasures (§6.3).
5. Seven candidate laws with falsifiers under a refutable central thesis, and twelve
   mechanical invariants as their engineering form (§7).
6. A nine-card portable protocol suite — eight executed in-case as standing CI, one
   (the prospective-prediction protocol) specified as the designated instrument for this
   study's main confound — plus executed pilots (§8–§9), a self-correcting novelty ledger
   (§10), and enumerated validity threats (§11).

### 1.4 Epistemic status — three strata

- **Candidate-general** (portable; carries a falsifier or a mechanical check): the verb
  definitions (§3), laws L1–L7, invariants I1–I12, the suite SC-01…SC-09, and the defect
  taxonomy *as a taxonomy*.
- **Case evidence** (one system; existence proofs and effect directions, never rates):
  every count here — 12 results, 40 analogies, 7 judged conjectures, 1 confirmation, the
  defect counts. N=1 dominates §11.
- **Case background** (context; do not generalize): the specific literatures, package
  layout, and harness. For reuse, abstract to roles: *principal* (human — charges,
  judgment, merge authority), *sessions* (mortal executors), *gates* (deterministic
  admission checks), *artifacts* (persisted state), *judge* (the NL sub-agent whose
  verdicts are gated, never trusted).

The report is designed to function as a sole input: §§1–12 state every load-bearing fact
inline; the receipts (Appendix B) are required only for byte-level audit and re-execution.

---

## 2. The case system

### 2.1 Architecture

Seven packages plus a root meta-package, one repository, no runtime dependencies beyond
three vetted libraries in the document front end (`pydantic`, `pylatexenc`, `lxml`) — the
entire graph/analogy layer is stdlib-only:

| organ | role |
|---|---|
| `decomposer/` | raw LaTeX/HTML/Markdown → clean nested structure; verified by char-coverage conservation, schema, idempotence, and a differential oracle vs LaTeXML |
| `concept_graph/` | structure → (object, attribute, relation) representation + reasoning DAG |
| `matcher/` | content-vector (MAC) retrieval; renaming-invariance; systematicity foundations |
| `analogy/` | the SME-style aligner: bijective correspondences, trickle-down systematicity, candidate inferences, skolems, minimal ascension; validated on the textbook solar-system → Rutherford-atom mapping |
| `grounding/` | prose → grounded predicate-calculus dgroups, behind the verbatim-grounding gate |
| `retrieval/` | library-scale MAC/FAC nearest-prior search; proof set-cover decomposition; SimHash-LSH ANN |
| `graph/` | the unified graph store: multi-literature build, role discovery, cross-domain analogy, conjecture transfer, the evaluation gate, novelty annotation, query DSL, JSON Schema, four experiments, the prediction ledger |
| `openpriors/` | consolidation: one CLI (`run · pipeline · query · experiment · ledger · report · demo · demonstrate · version`), source-checkout bootstrap, the demonstration generator |

Persisted state beyond code: the grounded corpora (`grounding/dgroups/` — 11 files;
`retrieval/library/` — 5 files), the committed sub-agent judgments
(`graph/evaluations/`), the generated-and-gated documents (`REPORT.md`,
`DEMONSTRATION.md`, `docs/index.html`), and run artifacts under staleness gates.

### 2.2 The production loop and its operators

Work proceeded as lettered epics, one pull request at a time, each merged only green.
One metabolic cycle:

> **argue** (why this epic; what claim it will add) → **build** (deterministic core +
> gated NL boundary) → **independently verify** (unit + red-tests; CI) → **externally
> review** (an automated reviewer on every PR; comments addressed before merge) →
> **audit** (periodic independent multi-agent adversarial passes) → **metabolize** (every
> confirmed defect becomes a regression that fails on the pre-fix code).

Five operators recur in the record:

- **O1 — defect → regression.** No fix lands without a test that bites on the pre-fix
  code (receipt: `tests/test_robustness.py`, whose docstring states the rule).
- **O2 — claim → gate.** Any prose claim about the system's output is converted into a
  CI-checked invariant (e.g. "the judge discriminates" became a ledger check).
- **O3 — organ genesis.** New artifact classes appear when a claim class recurs
  (`REPORT.md` at Epic AB; the ledger at AJ; `DEMONSTRATION.md` at AL).
- **O4 — generalization as regression.** A new literature must join the analogy web with
  **zero engine changes**; executed twice (Epics U, AC — PRs #28, #38).
- **O5 — external challenge.** Review and audit findings are selection pressure; the
  record includes a reviewer-caught sign error whose fix *strengthened* the scientific
  result (§6.3, DF-10).

### 2.3 Design positions (deliberate absences)

- **No embeddings, no vector store.** All matching is structural or lexical over verbatim
  stores; every match is quotable and grep-receipted. Accepted cost: no fuzzy recall
  beyond the ascension lattice.
- **No runtime API calls.** All NL work is done in-session by sub-agents at zero marginal
  cost; their outputs are committed, so reruns are deterministic and free.
- **No trusted NL output.** Sub-agent artifacts enter only through gates (grounding
  closure; verdict-vocabulary + projection-grounding). The judge's opinions are data,
  never control flow.
- **No scalar-only novelty.** Novelty is a coverage number *plus a named residual* — the
  facts no prior covers — so a score is always accompanied by its explanation.
- **No new runtime dependencies** in the graph layer: auditability over convenience.

### 2.4 History in brief

| era | window (2026) | content | receipts |
|---|---|---|---|
| E0 | May 4 – Jun 20 | repository created; one pre-history draft (an embedding-models report, later superseded by the structural approach) | first commits |
| E1 | Jun 21–26 | front end: epics A–D (decomposer, concept graph, matcher + SME aligner, grounding gate) | PRs #1–#10 |
| E2 | Jun 27 | the compression day: epics E–U — MAC/FAC retrieval, proof set-cover, HTML ingestion, ANN, first real paper, lineage, **the unified graph store (M)**, cross-domain analogy, **unsupervised role ascension (O)**, conjecture transfer, the evaluation loop (Q), capstone driver, query DSL, fourth literature (U) | PRs #11–#28, all merged 06-27 |
| E3 | Jun 28–30 | second real paper (V); per-result novelty (W); JSON Schema (X); research directions (Y) | PRs #29–#32 |
| E4 | Jul 1–3 | experiments begin (C2 = Z, C4 = AA); consolidated report (AB); **fifth literature (AC)**; discrimination control (AE); field-5 judgments (AF); C5 experiment (AG); interactive dashboard; CI-thrift | PRs #33–#44, #46 |
| E5 | Jul 4–5 | C7 experiment (AH); **third real paper — the C6 confirmation (AI)**; **the prediction ledger (AJ)**; coverage & robustness hardening (AK); consolidation/packaging/demonstration (AL) | PRs #45, #47–#49 merged; #50 open at pinning |
| E6 | Jul 18–20 | a governance layer grows in open PRs from a later session lineage (instrument-side constitution, amendments 001–003, provenance headers) — outside this report's pinned scope | PRs #51–#54, open |
| E7 | Aug 1 | this report | — |

### 2.5 The substrate

The five literatures are mathematical-statistical **cousins by design**: near transfer
first, with far transfer explicitly deferred (§12). The stakes are real — the repository,
dashboard, and claims are public, and the third real paper (ACI) was ingested specifically
to test a standing prediction, where failure would have been recorded (the ledger's
confirmation invariant would simply have stayed unsatisfiable and the epic's claim
falsified).

---

## 3. The representation and the corpus

A result is a **dgroup**: facts like `COVERAGE(the_interval, the_level)` and
`CAUSE(WEIGHTED_EXCHANGEABLE(...), COVERAGE(...))`, every symbol grounded to a verbatim
span of the source (`grounding/verify.py` enforces closure; a non-verbatim, empty, or
missing grounding fails the gate, and the gate's own failure modes are unit-tested).
On this representation the verbs are defined:

- **novelty**(r) = 1 − max over priors p of structural coverage(p → r); the uncovered
  facts are the named residual;
- **lineage**: `extends` edges where one result's structure contains and refines another's;
- **analogy**: an SME correspondence between dgroups, systematicity-scored;
- **conjecture**: a candidate inference projected across an analogy — structure present in
  the base, absent in the target, carried over under the correspondence (skolems for
  invented objects);
- **confirmation**: a later-ingested result whose grounded facts contain a projected
  conjecture's mechanism — decided by graph containment, not narrative.

Corpus at the pinned record: **5 literatures, 12 grounded results** (split conformal,
weighted conformal, the Lei–Candès counterfactual-conformal paper
[arXiv:2006.06138](https://arxiv.org/abs/2006.06138); Banach contraction, gradient descent
under strong convexity, a Nesterov-acceleration paper; VC and margin generalization;
McDiarmid and Bernstein; online gradient descent and its strong-convexity variant) plus
the confirming paper (Gibbs–Candès ACI,
[arXiv:2106.00170](https://arxiv.org/abs/2106.00170)). The unified graph: **363 nodes**
(12 result · 112 fact · 25 functor · 66 entity · 148 conjecture) and **665 edges**, facts
reified and losslessly reconstructable, validated against a formal JSON Schema.

---

## 4. Methods: the verification machinery and measured outcomes

### 4.1 Gate inventory and red-test discipline

Every admission point is a deterministic gate, and every gate ships with tests that tamper
with its input and require failure ("verify the verifier"):

| gate | admits | red-tested against |
|---|---|---|
| grounding closure (`grounding/verify.py`) | NL-lifted facts | non-verbatim / empty / non-string groundings; missing keys; wrong-typed sections |
| evaluation gate (`graphstore/evaluate.py`) | the judge's verdicts | invalid verdicts; fabricated projections ("not generated by transfer"); empty reasoning; **empty artifact** (a vacuous pass — found and closed in-case, DF-01); malformed JSON |
| ledger invariants (`graphstore/prediction_ledger.py`) | the arc's closure claims | discrimination (≥1 rejection required); uncertain→direction+experiment closure; structural confirmation with `CAUSE` glue excluded from mechanism matching (DF-09) |
| schema validator (`graphstore/schema.py`) | the unified graph | structural violations |
| discrimination control (`grounding/discrimination.py`, Epic AE) | the analogy web's informativeness | foil corpora must **not** produce the web |

### 4.2 Determinism and staleness regimes

Two nondeterminism sources account for every observed instance (L5, §7): wall-clock
timestamps (countered by a pinned `SOURCE_DATE_EPOCH`, asserted by test) and unordered
iteration (countered by total orders — every sort carries a name tie-break). Two-run
byte-identity of the demonstration transcript is a test. Every generated document is
regenerated in CI and diffed: `REPORT.md` (report-ci), `docs/index.html` (demo-ci),
`DEMONSTRATION.md` (consolidation-ci), and committed run artifacts
(`git diff --exit-code` after a full front-end run in integration-ci).

### 4.3 Adversarial audits and external review

Beyond per-PR automated review (every comment addressed before merge; ≈2–3 substantive
comments per late PR), two independent multi-agent adversarial audits ran, with opposed
briefs and second-pass verification of every finding:

- **Epic AK (hardening):** a cross-package audit confirmed **16 robustness defects**
  (crash-obscurely / pass-silently / resolve-nondeterministically classes); all fixed,
  each pinned by a regression failing on the pre-fix code.
- **Epic AL (consolidation):** a six-dimension audit (packaging, CLI dispatch,
  demonstration faithfulness, test rigor, CI wiring, docs-vs-reality) with independent
  re-verification of each finding: **5 confirmed defects, 0 false alarms**; three
  dimensions returned clean. All five fixed before merge (§6.3).

### 4.4 Measured outcomes

At the pinned record: **298 tests passing** (≈3,400 test LOC over ≈11,600 total Python
LOC); **11 CI workflows**; branch coverage **~93%** (measured at Epic AK, with every gate
`main([])` and CLI `main([])` executed under pytest); **packaging as a checked claim** —
all 8 wheels build, install into a fresh venv as `openpriors[all]`, and import/run from
outside the source tree, in CI (`scripts/verify_packaging.sh`), with every declared
console-script entry point resolved by test (`tests/test_packaging.py`).

---

## 5. The doctrine as data

Reconstructed from the operating record; one practitioner-lineage's failure-tested
positions, reported as the selection environment that produced this system:

1. **论证 / 构建 / 独立检验.** Argue the claim, build the mechanism, verify independently
   of the builder — per epic, per PR, per artifact.
2. **The determinism boundary.** NL work is a boundary crossing: committed, gated, never
   load-bearing while uninspected.
3. **Verbatim or it doesn't enter** (the grounding contract).
4. **A gate without red-tests is not a gate.**
5. **Regenerate, don't trust.** Derived artifacts are recomputed and diffed in CI;
   committed copies are projections, never bedrock.
6. **No silent caps.** Truncation must be marked (the report's correspondence preview
   gained "+N more" markers when a silent `[:3]` was caught — DF-05).
7. **Fail loud.** Malformed input raises with a precise message; silent skips are defects
   by definition.
8. **One PR at a time; merged is final.** External review consumed on every PR; a merged
   PR is never reopened — follow-ups are new work.
9. **Generalization is a regression test.** A new literature joins with zero engine
   changes, or the design is wrong.
10. **Cost physics.** In-session sub-agents only; zero marginal API cost; determinism
    makes reruns free.

---

## 6. Results

### 6.1 Findings I — what the system found (F-01 … F-10)

Each finding carries a receipt (module / artifact / test); all recompute via
`openpriors demonstrate` or `openpriors ledger`.

- **F-01 — Five literatures share one causal skeleton, discovered unsupervised.** Reading
  only each functor's position inside `CAUSE` facts (premise-of, conclusion-of, or both),
  the engine induced 19 roles in 5 signatures. Every field has exactly one
  **structural-property pivot** (`ROLE::PC::2` — both driven by assumptions and driving
  the guarantee), and the pivots align across fields
  (receipt: `graph/src/graphstore/crossdomain.py`; `REPORT.md` §roles):

  | field | pivot (`PC::2`) | guarantee (`C::2`) |
  |---|---|---|
  | conformal | `WEIGHTED_EXCHANGEABLE` | `COVERAGE` |
  | optimization | `CONTRACTION` | `LINEAR_CONVERGENCE` |
  | learning theory | `UNIFORM_CONVERGENCE` | `GENERALIZATION` |
  | concentration | `BOUNDED_MARTINGALE` | `CONCENTRATION` |
  | online learning | `NO_REGRET` | `SUBLINEAR_REGRET` |

- **F-02 — A 40-edge cross-domain analogy web.** `weighted_conformal` alone is found
  analogous to eight results spanning all four other literatures.
- **F-03 — Zero-engine-change generalization, twice.** The fourth literature (Epic U,
  PR #28) and fifth (Epic AC, PR #38) joined the web with no code changes to the
  discovery mechanism — the strongest in-case evidence that F-01 is a property of the
  representation, not of tuning.
- **F-04 — Lineage from structure alone.** Four development chains recovered with no
  citation data, e.g. *counterfactual-conformal → weighted → split conformal*.
- **F-05 — Novelty with named residuals.** The counterfactual-conformal paper scores
  0.2222 against nearest prior `weighted_conformal`, residual exactly its
  `COUNTERFACTUAL`/`NESTED` contributions; `vc_generalization` scores 1.0 (no covering
  prior). A score is never issued without its explanation.
- **F-06 — Conjecture generation and discriminating judgment.** 148 conjectures projected
  deterministically; 7 carried through the judgment loop: 2 plausible, 4 uncertain,
  **1 rejected** (C3 — a finite-capacity premise projected onto conformal inference,
  rejected because conformal validity is distribution-free). The rejection is a ledger
  invariant: a judge that stops discriminating fails CI.
- **F-07 — Every uncertain conjecture became a tested research program.** C2: the L²(μ)
  contraction modulus of an importance-reweighted operator is governed by the χ²
  divergence. C4: the projected Banach bound ‖θ̂ₙ−θ*‖ ≤ εₙ/(1−κ) holds at every sample
  size on a Gaussian-mixture EM operator, at the 1/√n rate. C5: on two-player quadratic
  games, OGD's empirical rate equals the spectral radius in every phase cell (convergence
  iff η < 2μ/L²), averaged play converging while the last iterate wanders. C7: the
  informed step contracts at 1−1/κ while the regret-optimal schedule decays polynomially —
  a quantified price of robustness. (Receipts: `graphstore/experiment_c{2,4,5,7}.py`, all
  green in CI.)
- **F-08 — The flagship: a structurally-confirmed prediction.** C6 — projected from the
  online ↔ conformal correspondence: *the weighted conformal calibration procedure is a
  no-regret play*. Judged plausible. Gibbs & Candès' ACI, ingested afterwards (Epic AI,
  PR #47), realizes it: the paper's grounded facts contain the predicted `NO_REGRET` play
  and the projected `NO_REGRET → COVERAGE` bridge; the check is graph containment with
  `CAUSE` glue excluded from mechanism matching, enforced in CI
  (receipt: `graphstore/prediction_ledger.py::_confirms_structurally`). Epistemic label:
  **retrodiction** — see §10 (N1) and §11 (threat 3).
- **F-09 — The web is discriminating.** The negative control (Epic AE) verifies foil
  input does not produce the analogy web; informativeness is a checked property.
- **F-10 — The confirming paper decomposes as a cross-field synthesis.** ACI's proof
  skeleton set-covers from online + conformal priors, with the online α-update as its
  novel residual — the system's own novelty verb applied to the paper that confirmed it.

### 6.2 The demonstration

`openpriors demonstrate` recomputes the entire arc live (pipeline + ledger; nothing read
from caches), narrates the seven stages, and writes `DEMONSTRATION.md` — byte-stable,
with `--check` failing on drift. It is the report's §6.1 in executable form.

### 6.3 Findings II — a defect phenomenology of agent-built research code (DF-01 … DF-11)

Everything below fired *in this project*, was caught by the machinery (or by external
review), and now has a mechanical countermeasure. Offered as candidate-general taxonomy;
instances are case evidence. Reflexive instances — defects inside the verification layer
itself — are marked ⟲.

- **DF-01 — Vacuous gate pass.** The evaluation gate returned green on an *empty*
  evaluations artifact (nothing to check ⇒ pass). Found by the AK audit; countermeasure:
  non-emptiness is part of `passed`, plus a red-test
  (`test_gate_does_not_rubber_stamp_an_empty_artifact`). The gate class: a checker whose
  domain can silently shrink to ∅.
- **DF-02 — Stale derived artifacts.** Three instances of committed derived state
  drifting from code (graph results ×3 files; an analogy result missing a later-added
  field; six decomposer run files). All three predated their staleness gates; none
  recurred after. Countermeasure: regenerate-and-diff in CI (I7).
- **DF-03 — Wall-clock nondeterminism.** The unified CLI initially failed to pin
  `SOURCE_DATE_EPOCH`; one verb churned 8 committed files on timestamps alone. Found by
  the AL audit; countermeasure: epoch pinned in the bootstrap, asserted by test.
- **DF-04 — Iteration-order nondeterminism.** Set/dict ordering leaked into a report
  preview and into retrieval ranking (cosine ties resolved arbitrarily, so the ANN path
  could disagree with the linear scan). Countermeasure: total orders — every sort carries
  a deterministic tie-break (I8).
- **DF-05 — Silent truncation.** A correspondence preview sliced `[:3]` with no marker —
  readers would take the slice for the whole. Countermeasure: "no silent caps" (+N more
  markers), now doctrine (§5.6).
- **DF-06 — Silent skip / obscure crash on malformed input.** Nine spots crashed with
  unrelated errors or skipped silently on malformed input (half-specified CLI pairs,
  missing keys, wrong types, non-binary `CAUSE` facts, malformed library entries).
  Countermeasure: fail-loud validation with regressions (`tests/test_robustness.py`).
- **DF-07 ⟲ — Checker-side defect.** The regression *asserting* the epoch pin was itself
  wrong (asserted ambient equality, breaking under legitimate caller overrides —
  a test that would cry wolf). Caught by external review of the hardening PR itself.
- **DF-08 ⟲ — CI blind spots.** The root cross-cutting tests were run by **no** workflow
  for most of the project's life; later, the new consolidation workflow's path filter
  excluded the demonstration's actual inputs (a pipeline-source edit could stale the
  transcript without re-running its gate). Both found in-case; countermeasure: a
  filterless cross-cutting workflow + artifact-diff steps.
- **DF-09 ⟲ — Near-miss false-positive confirmation.** The ledger's structural-confirmation
  check could have been satisfied by `CAUSE` glue rather than the predicted mechanism —
  the flagship claim's own checker was the near-miss. Caught in review of the ledger PR;
  countermeasure: glue excluded from mechanism matching. This is the case's sharpest
  instance of the companion study's sensor-layer thesis (§10).
- **DF-10 — Sign error in experiment math.** The C5 equilibrium computation carried a
  sign error; external review caught it, and the corrected computation produced the
  *cleaner* scientific result (averaged-play convergence — the folk theorem). Adversarial
  pressure improved the finding, not just the code.
- **DF-11 — Environment interference.** Harness-side events — a container recycle that
  re-cloned a months-old branch state mid-project, connector disconnections, model-era
  changes across the build — altered behavior with no in-repo cause. Countermeasures:
  remote-as-truth recovery discipline; session-attribution trailers as era stamps.

---

## 7. Candidate laws, the central thesis, and the invariants

Scope: one system observed deeply. These are proposed laws with falsifiers, not
established universals.

### 7.1 The seven laws

- **L1 — Gated-boundary sufficiency.** Confining LLM output to committed,
  deterministically-gated boundary artifacts is sufficient to keep an agent-built research
  pipeline's *claims* auditable end-to-end. Case: every headline claim resolves to gated
  artifacts. Falsifier: a gated-boundary pipeline accumulating load-bearing claims that
  cannot be traced to a gate.
- **L2 — Grounding closure blocks symbol hallucination.** With verbatim-substring
  closure enforced (and red-tested), no hallucinated symbol entered the corpus over 12
  results × 5 literatures. Falsifier: grounded-but-fabricated symbols passing at scale, or
  the gate blocking legitimate abstraction so often that practitioners route around it.
- **L3 — Causal-position roles suffice for near transfer.** `CAUSE`-position role
  ascension alone discovered the five-field skeleton, twice surviving zero-change field
  addition. Falsifier: a cousin field whose pivot fails to align, or a foil corpus passing
  the discrimination control.
- **L4 — A gate that cannot go red decays.** Both in-case gate defects (DF-01, DF-09)
  were exactly failures *of the red direction* — pass conditions satisfiable without the
  checked property. Red-tests found one; adversarial review the other. Falsifier: a
  mature gate suite without red-tests that still catches planted tamper classes.
- **L5 — Two nondeterminism sources.** Every observed reproducibility failure was
  wall-clock or iteration-order (DF-03, DF-04); pinning the epoch and totalizing orders
  achieved byte-stability. Falsifier: a third recurring source in a pure-Python pipeline
  of this shape.
- **L6 — Ungated derived artifacts drift.** All three staleness instances predated their
  gates; zero recurred after (bounded by the short observation window). Falsifier:
  ungated derived artifacts staying true across many epochs of code evolution.
- **L7 — Adversarial margin.** Independent adversarial passes found confirmed defects at
  every maturity level (16 after self-testing; 5/0 after the 16; 2 review catches after
  the 5) — self-testing alone never reached the fixed point. Falsifier: consecutive
  adversarial audits returning empty on dimensions not already mechanically gated.

### 7.2 The central thesis (refutable)

**The researcher's idea-verbs admit deterministic, receipt-carrying operationalization
over grounded structure, sufficient to close a discover → predict → confirm loop on real
literature — and the stable configuration places LLMs only at gated NL boundaries, with
the gates themselves red-tested and the derived record regenerated rather than trusted.**
Refutation surface: scaling the corpus or leaving the near-transfer regime collapses the
role/analogy discovery (L3); the prospective protocol (SC-09) yields a confirmation base
rate indistinguishable from chance; or gated-boundary pipelines prove unable to carry
claims without ungated NL in the load path (L1).

### 7.3 The mechanical invariants (I1 … I12)

**I1** grounding closure on every corpus artifact · **I2** every gate has red-tests
(tamper suite) · **I3** verdicts grounded in real transfer output (no fabricated
projections) · **I4** judge non-emptiness + discrimination (≥1 rejection) · **I5** arc
closure (every uncertain conjecture → direction + runnable experiment) · **I6** structural
confirmation with glue excluded · **I7** regenerate-and-diff on every derived document and
run artifact · **I8** determinism = pinned epoch + total orders, byte-diff-tested ·
**I9** fail-loud typed input validation · **I10** every entrypoint executes green under
test · **I11** packaging closure (wheels build; fresh-venv install; entry points resolve)
· **I12** negative control on the discovery machinery.

---

## 8. The portable protocol suite (SC-01 … SC-09)

Eight cards are executed in-case as standing CI (their provenance instances are §6.3's
defects); the ninth is the designated instrument for this study's main confound. Design
rules follow the companion study: constructive setup, fault injection, constructive ground
truth, machine-checkable pass criteria, **no LLM-judged oracles**.

Coverage, by title: **SC-01** grounding-closure (plant a non-verbatim grounding; gate must
fail) · **SC-02** gate tamper suite (N tamper classes per gate incl. the empty artifact) ·
**SC-03** staleness (mutate upstream; diff gate must fire) · **SC-04** determinism
(two runs byte-identical; clock shifted; locale varied) · **SC-05** discrimination
(foil corpus must not produce the web) · **SC-06** entrypoint sweep (every `main([])`
rc 0) · **SC-07** packaging closure (build/install/import/run from wheels off-tree) ·
**SC-08** ledger arc (invariants I4–I6 against tampered ledgers) · **SC-09** prospective
prediction (below).

One card in full — the instrument follow-up studies should run first:

> **SC-09 — Prospective prediction protocol.** *Provenance:* the C6 confirmation is a
> retrodiction (§11, threat 3). *Setup:* run discovery + transfer on a corpus frozen at
> time T; **pre-register** every projected conjecture (hash the projections; commit the
> hash). *Injection:* none — the world supplies it; candidate confirming papers are
> selected by a party blind to the conjecture list, from literature published or ingested
> after T (strongest form: papers that do not yet exist at T). *Task:* lift each candidate
> under the grounding gate by an extractor given only the paper text (references stripped);
> run the deterministic containment check against the pre-registered projections.
> *Oracle/metrics:* confirmation base rate vs a null of degree-matched random projections;
> contamination bound: the extractor never sees the conjectures, the checker never uses NL.
> *Pass:* base rate above null with pre-registered hashes intact. *Naive-failure
> signature:* post-hoc conjecture selection, or lifts steered toward the projections.
> *Difficulty knobs:* time gap; corpus breadth; blinding strength.

Validation ladder (declared): in-case CI execution (SC-01…08 — a floor, by construction)
→ port to a second corpus/system → SC-09 executed once → SC-09 at scale. Only the first
rung is complete.

---

## 9. Executed pilots

- **Four research-direction experiments** (F-07), each a pure-Python instrument run in CI;
  quantitative outcomes stated in §6.1 and reproduced by `openpriors experiment`.
- **The confirmation instrument** (F-08): deterministic containment, hardened against its
  own false-positive mode (DF-09), enforced as CI invariants with red-tests.
- **The negative control** (F-09): executed as a standing gate, not a one-off.
- **The hardening pass as instrument** (Epic AK): entrypoint sweep + robustness audit —
  the measured outcome was §4.4's coverage and the 16-defect ledger, all metabolized into
  regressions (operator O1).

---

## 10. Related work and the novelty ledger

The alignment machinery is **deliberately inherited**: structure-mapping theory and SME
(Gentner 1983, *Cognitive Science* 7; Falkenhainer, Forbus & Gentner 1989, *Artificial
Intelligence* 41), MAC/FAC two-stage retrieval (Forbus, Gentner & Law 1995, *Cognitive
Science* 19), and candidate inference / systematicity as defined there. Cross-literature
undiscovered-connection mining descends from Swanson's literature-based discovery
(Swanson 1986, *Perspectives in Biology and Medicine* 30). The substrate mathematics is
prior art by construction: weighted/covariate-shift conformal
([arXiv:1904.06019](https://arxiv.org/abs/1904.06019)), counterfactual conformal
([arXiv:2006.06138](https://arxiv.org/abs/2006.06138)), and ACI
([arXiv:2106.00170](https://arxiv.org/abs/2106.00170)) — the system's contribution is
*finding the bridge without being told*, not the bridge itself. (Print-era citations are
canonical bibliographic references; arXiv links are tool-verified.)

Initial novelty claims, corrected in the writing of this report:

- **N1 (corrected — the flagship's tense).** "The system predicted ACI" overclaims: ACI
  (2021) predates the system, so F-08 is a **retrodiction** — the deterministic machinery
  projected the mechanism without the paper in-corpus, but NL-boundary steps (the judge;
  the extractor who lifted ACI) cannot be certified free of pretraining exposure. What
  survives cleanly: conjecture *generation* and confirmation *checking* are deterministic
  and auditable; the grounding gate ties every checked fact to verbatim ACI text. The
  prospective protocol (SC-09) is the designated cure, and until it runs, F-08 is an
  existence proof of the *pipeline*, not a measured predictive power.
- **N2 (narrowed).** "Unsupervised role discovery" as a general idea is not new
  (predicate-role induction has cognitive-science lineage); the candidate-new residue is
  the specific *causal-position ascension* (`ROLE::{P,C,PC}::arity` read from `CAUSE`
  structure) and its twice-replicated zero-change field addition.
- **N3 (narrowed).** Novelty-as-structural-coverage is a cousin of SME's normalized
  scoring; the useful residue is the **named residual** contract (a score never ships
  without the uncovered facts) and its gating.
- **N4 (bounded).** The verification doctrine (red-tested gates, regenerate-don't-trust,
  adversarial audits) has independent convergent practice in the companion forensic study
  of the same principal's ecosystem — a private-record case study whose sensor-layer
  thesis ("improvement pressure redistributes error into the sensing layer") this case
  *replicates in miniature*: DF-07/DF-08/DF-09 are checker-side defects discovered only by
  meta-verification, alongside that study's L10 (mechanism-over-will: our DF-fixes only
  held as CI mechanisms) and L12 (unconsumed records are inert: our gates are forced
  consumers by construction). Correlated evidence (same principal/toolchain), so counted
  as convergence, not replication.
- **N5 (open, unchecked).** The end-to-end *closed loop* — grounded corpus → unsupervised
  cross-field analogy → deterministic conjecture projection → gated judgment → experiment
  → structural confirmation, all CI-enforced — is claimed candidate-new **as a composed,
  machine-auditable artifact**. A systematic 2024–2026 depth-check against LLM
  hypothesis-generation and AI-for-science pipelines has *not* been executed; this claim
  is therefore held at initial-claim grade, explicitly awaiting its own N-ledger pass
  (§12).

---

## 11. Threats to validity

1. **Single system, single principal-lineage.** All empirics are one case; the audits and
   this report are written by agent sessions of the same class and toolchain — correlated
   evidence by the companion study's own collision law. The suite (§8) is the path to
   uncorrelated replication.
2. **Self-measurement.** Coverage, test counts, and audit outcomes are the system
   measuring itself; mitigations (external review, opposed-brief audits, red-tests) reduce
   but do not remove this.
3. **Retrodiction and contamination (the main confound).** See N1. Decomposition: role
   discovery, transfer, and containment are deterministic (clean); the judge's "plausible"
   and the extractor's lift are NL-boundary steps by models plausibly exposed to ACI in
   pretraining. The grounding gate bounds the lift (every fact is verbatim paper text);
   nothing bounds the judge. SC-09 is the designated removal.
4. **Micro-corpus, near transfer.** 12 curated results in cousin fields; the discovery
   laws (L3) are untested at scale and off-family. The judged-conjecture sample is N=7;
   the confirmed-prediction sample is N=1.
5. **Grain sensitivity.** "12 results", "40 analogies", "148 conjectures" depend on
   segmentation and thresholds fixed in code; the counts are reproducible but the grains
   are design choices, and share-style claims should not be lifted off them.
6. **Judge opacity.** The gate certifies well-formedness, grounding, and discrimination —
   not correctness of any verdict. Verdicts are one committed sub-agent judgment each.
7. **Era effects.** The build crossed harness and model-family eras (DF-11); commit
   trailers stamp sessions, but no controlled comparison across eras was run, so
   behavioral attribution across the build is not claimed.

---

## 12. Open problems

**Instruments.** Execute SC-09 (prospective protocol) — the single highest-value follow-up;
port SC-01…08 to a second corpus; encode the discrimination control as a per-field
falsification harness for L3.

**Measurements.** Confirmation base rate vs null (SC-09); L3 at 10× corpus scale and on a
non-cousin field; judge calibration against human experts (panel + adversarial judging);
grain-sensitivity bands for every count in §6.

**Theory.** When does causal-position ascension over-merge (the discrimination control
gives the harness)? What is the minimal role vocabulary for far transfer? Can the named
residual drive automated literature search (the system proposing, the literature
disposing)?

**External validity.** The decisive step, as in the companion study: reproduction of the
laws' predictions on a system unrelated to this case — different corpus, different
principal, different toolchain.

---

## Appendix A — glossary

**dgroup** — a result's grounded (object, attribute, relation) description; the unit of
the corpus. **Grounding** — the verbatim-substring contract binding every symbol to source
prose. **SME** — structure-mapping engine; alignment by relational isomorphism under
renaming. **MAC/FAC** — cheap content-vector filter, expensive structural rerank.
**Role ascension** — unsupervised role assignment `ROLE::{P,C,PC}::arity` read from a
functor's positions in `CAUSE` facts. **Pivot** — a field's `PC::2` role: the structural
property both driven by assumptions and driving the guarantee. **Candidate inference /
conjecture** — structure projected across an analogy into the target, skolemizing invented
objects. **Structural confirmation** — deterministic containment of a projected mechanism
in a later-ingested paper's grounded facts, glue excluded. **Gate** — a deterministic
admission check; **red-test** — a test that tampers with a gate's input and requires
failure. **Staleness gate** — CI regeneration + diff of a committed derived artifact.
**The judge** — the in-session sub-agent whose committed verdicts the evaluation gate
admits. **Ledger** — the CI-enforced record cross-referencing predictions with
confirmations. **F/DF/L/I/SC-nn** — findings, defect phenomena, laws, invariants, and
suite cards as numbered in §§6–8.

## Appendix B — data availability and verification

The complete record is **public**: [github.com/yulinl2/OpenPriors](https://github.com/yulinl2/OpenPriors).
Pinned coordinates for this report's counts: `main` at `49f62fb` (Epic AK merged); the
Epic-AL branch `claude/openpriors-consolidate-package-demo-9m9cjs` at `4530012` (open as
PR [#50](https://github.com/yulinl2/OpenPriors/pull/50) at pinning; contains everything on
`main` plus consolidation/packaging/demonstration and this report's home). Open PRs
#51–#54 (a governance layer from a later session lineage) are outside the pinned scope.
Commit messages across the record carry session-attribution trailers — themselves part of
the provenance dataset.

Key coordinates (branch-pinned): the corpus (`grounding/dgroups/`, `retrieval/library/`);
the committed judgments (`graph/evaluations/`); the gates
(`grounding/src/grounding/verify.py`, `graph/src/graphstore/evaluate.py`,
`graph/src/graphstore/prediction_ledger.py`); the red-tests
(`graph/tests/test_evaluate.py`, `tests/test_robustness.py`); the generated-and-gated
documents (`REPORT.md`, `DEMONSTRATION.md`, `docs/index.html` →
[demo.open-priors.org](https://demo.open-priors.org/)); the experiments
(`graph/src/graphstore/experiment_c{2,4,5,7}.py`); the suite's CI form
(`.github/workflows/`, 11 workflows).

**Verification.** From a fresh clone:

```
make setup          # one venv, pinned deps
make test           # 298 tests, incl. every red-test and staleness gate
make demonstrate    # recompute the whole arc; DEMONSTRATION.md is byte-stable
openpriors ledger   # the discover → predict → confirm record, invariants enforced
make package        # build all 8 wheels; fresh-venv install/import/run off-tree
```

By the case's own attribution doctrine, this report's generating process is recorded in
the repository's commit trailers rather than asserted as authority.
