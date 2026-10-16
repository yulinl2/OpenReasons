# Scientific interface contract — what each OpenReasons stage means

**2026-10-16 · working interface digest; not an implemented full semantic pipeline or a replacement research proposal.** Owner priority: the value of OpenReasons is its **claim/document decomposer and formal-encoding infrastructure**. This document describes the current stage boundaries *without* assuming that every intended guarantee is already met. This is part of [major cleanup PR #66](https://github.com/yulinl2/OpenReasons/pull/66), with a stacked [evidence-state code PR #67](https://github.com/yulinl2/OpenReasons/pull/67) and scientific questions [#68](https://github.com/yulinl2/OpenReasons/issues/68)/[#69](https://github.com/yulinl2/OpenReasons/issues/69).

**Original research context:** the [five owner-uploaded OpenPriors texts](https://github.com/yulinl2/OpenPriors/blob/main/research/ORIGINAL-SOURCES.md) present a *research problem and hypotheses*, not a universal coding standard. The [cross-repo digestion in OpenPriors draft #7](https://github.com/yulinl2/OpenPriors/pull/7) explicitly separates the roles and unsettled assumptions. OpenReasons is not compelled to implement the three-term novelty objective in order for source-linked encoding to be valuable.

## Stage types and what the tests would have to show

| Stage | Current input → output or goal | Status of evidence | Does **NOT** establish |
| --- | --- | --- | --- |
| **S0 document structural decomposition** | Raw TeX/Markdown/HTML → source spans, typed roles, hierarchy and references; [decomposer schema](../decomposer/src/decomposer/schema.py), [P1–P4 principles](../decomposer/docs/principles.md) | [CODE] Structural conservation/referential checks; original explicit design goal. Check role assignment separately across formats. | Complete extraction of claims expressed in arbitrary prose, logical entailment, or novelty |
| **S1 semantic claim encoding** | S0 + raw source → propositions, premises, quantifiers, scope, definitions, dependencies and source links in a typed intermediate representation | [OPEN] Desired programme interface; [MetaSci 2026-09-28 intake](https://github.com/yulinl2/MetaSci/blob/main/kb/intake/2026-09-28_openpriors-line-intake-manifest.md): 0 `assert` among 299 Markdown structure nodes; that specifically shows S0 checks do not certify S1. | That S0's useful structural contract is a failure or that an LLM is a truth oracle |
| **S2 grounded relational description group** | A source passage + agent-authored `facts` and `groundings` → `Dgroup` accepted by [grounding/verify.py](../grounding/src/grounding/verify.py) | [CODE] Checks entities' verbatim source substrings, not complete semantic preservation. Riddle and paper fixtures may involve manually annotated targets. | Correct logical interpretation of all relevant conditions, empirical truth |
| **S3 structural alignment & candidate inference** | Hand/agent encoded `Dgroup` pairs → greedy mapping and projected candidate relations | [CODE] [SME-style aligner](../analogy/src/analogy/align.py), structural consistency by entity maps, with candidate projections. | That base entails target, that analogies are sound or future-useful |
| **S4 matched-fact source selection / reuse heuristic** | Fact sets → MAC/FAC shortlist, greedy set cover, `1−coverage`, possibly nearest encoded prior | [CODE] [retrieval](../retrieval/src/retrieval/decompose.py), [graph/novelty](../graph/src/graphstore/novelty_graph.py). Candidate restriction by fact-count, not by historical date. | Conditional MDL cost `L_π`, source chronology, verified *scientific novelty* or intellectual inheritance |
| **S5 experiment/conjecture fixtures** | Curated directions, programs, verdict files and paper descriptions → ledger/reports | [CODE] C6 evaluator had named Gibbs–Candès before later paper lift; [PR #67](https://github.com/yulinl2/OpenReasons/pull/67) separates module existence, run, outcome, independent validation. | Blind forecasting or complete semantic/experimental validation by code existence |

**Key scope correction:** [decomposer principles §0](../decomposer/docs/principles.md) already explicitly distinguish *source-structural floor* from later `proves`/`assumes` semantic edges. “0 ASSERT / 299” is not a proof the tool failed to preserve document bytes or source references. It is evidence of an unresolved higher-level semantic extraction interface. Conversely, getting every byte back does not imply the meaning-level layer is solved.

## Non-equivalent source labels and the historical experiment plan

The [June 13 OpenPriors action plan §2.1](https://github.com/yulinl2/OpenPriors/blob/main/sources/2026-10-16-owner-upload/2026-06-13-Sat-0742-openpriors-action-plan-cc-handoff-v1_0_md.md) **already** separates historical inheritance `actual_descent` and `legitimacy` from economic derivability, includes independent rediscovery and standard-primitive negative controls, and marks provisional LLM labels for human checking. Do **not** teach new agents that the owner's original scientific design collapsed these.

A tool's retrieved source may be an *explanatory sufficient set* rather than an *actually inherited historical source*. Its semantic/causal provenance is **not identified** by mapping score or by position in a graph. Query functions should label edges `structural_candidate`, `verified_entailment`, `historical_evidence`, etc., only on evidence that supports that role.

## What a legitimate end-to-end validation would require

1. Independently adjudicated full-document examples and semantic claim gold, with explicit source granularity; test across equivalent markups and paraphrases, changed quantifiers, negated assumptions.
2. Distinguish text-preservation, semantic equivalence, derivation checking, historical source evidence, and experimental reproduction as **different oracles**; no “PASS” of one means “PASS” of all.
3. Freeze `Dgroup` extraction/prediction before hidden evaluation; measure dependence on human/agent manual construction. Report error propagation `S0→S1→...→S5` *as data*, without treating successful later fixtures as upstream validations.
4. Benchmark `C_hist` vs `C_explain` with **different labels and success criteria**, recognizing multiple valid explainers and unknown historical genealogy.
5. Report representation dependence of coverage: split/merge same meaning into different facts, repeated facts, alternative predicate taxonomies; the code's 0.15/0.6 thresholds are not scientifically calibrated correctness decisions.
6. Keep independent problem boundaries: OpenPriors original `N_∞` vs `N_τ*` fork, MetaSci claim/kernel conjectures, MetaProof decoder-conditioned future total cost. An instrument usable by all of them does not prove the loss functions equivalent.

## Research questions still open

[OpenReasons #68](https://github.com/yulinl2/OpenReasons/issues/68) — claim IR semantics · [OpenReasons #69](https://github.com/yulinl2/OpenReasons/issues/69) — novelty/mapping construct validity · [OpenPriors #2](https://github.com/yulinl2/OpenPriors/issues/2) and [#6](https://github.com/yulinl2/OpenPriors/issues/6) — novelty estimand, formal theorem obligations · [MetaSci M1 board](https://github.com/yulinl2/MetaSci/blob/main/kb/QUESTION-BOARD.md) — question-first semantic/oracle programme.

**This is not a request to rewrite the structural parser or implement a universal science theorem prover in a single PR.** It is a typed contract for how each result may and may not be interpreted. Keep negative controls and inconclusive results.
