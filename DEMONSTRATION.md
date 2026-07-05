# OpenPriors — end-to-end demonstration

*One reproducible run of the whole arc: **discover → predict → confirm**. Every number below is recomputed live by `openpriors demonstrate` (`graphstore.pipeline` + `graphstore.prediction_ledger`), not read from a cache. Because every stage is deterministic, this transcript is byte-stable.*

## 1 · Ingest — grounded results become one graph

Ingested **12 results** across **5 literatures** (conformal, optimization, learning, concentration, online), each fact grounded in a verbatim span of its source.

The unified (object, attribute, relation) graph: **363 nodes** (conjecture 148, entity 66, fact 112, functor 25, result 12) and **665 edges**.

## 2 · Novelty — what's new against the nearest prior

OpenPriors began as a novelty detector; the score is `1 − best-prior coverage`.

- **Most novel:** `vc_generalization` (novelty 1.0), no prior in the corpus covers it — contributing `FINITE_VC(the_class, the_dim)`, `GENERALIZATION(the_bound, the_excess)`, `UNIFORM_CONVERGENCE(the_risk, the_dim)`.
- **Least novel:** `arxiv-2006.06138-main` (novelty 0.2222), closely covered by `weighted_conformal`.

## 3 · Lineage — each field's development line, recovered from structure

No citations are read; the `extends` edges are inferred from grounded relational structure alone:

- `arxiv-2006.06138-main` → `weighted_conformal` → `split_conformal`
- `bernstein_concentration` → `mcdiarmid_concentration`
- `gd_strong_convexity` → `banach_contraction`
- `margin_generalization` → `vc_generalization`
- `online_strong_convexity` → `online_gradient_descent`
- `weighted_conformal` → `split_conformal`

## 4 · Analogy — cross-domain, discovered unsupervised

With roles read from each fact's CAUSE position (no hand-coded correspondences), the engine induced **19 roles** in **3 kinds** (C, P, PC) and discovered **40 cross-domain analogies**.

Role legend:
- `C` — conclusion/guarantee (is driven by a CAUSE)
- `P` — premise (drives a CAUSE)
- `PC` — structural-property pivot (both premise-of and conclusion-of)

For example, `weighted_conformal` is found analogous to `banach_contraction`, `bernstein_concentration`, `gd_strong_convexity`, `margin_generalization`, `mcdiarmid_concentration`, `online_gradient_descent`, `online_strong_convexity`, `vc_generalization` — across different literatures.

## 5 · Conjecture — what each analogy predicts

Transferring candidate inferences across every analogy projected **148 analogical conjectures** — falsifiable predictions the system had not been told.

## 6 · Evaluate — an independent judge, deterministically gated

An in-session sub-agent judged the conjectures; the deterministic gate **PASSED** and the judge **discriminates** — 2 plausible, 4 uncertain, 1 implausible (not a rubber stamp).

## 7 · Confirm — the prediction ledger closes the loop

The ledger cross-references the *prediction* side against the *confirmation* side:

- 7 conjectures judged (2 plausible · 4 uncertain · 1 implausible)
- 4 uncertain → refined into research directions, all 4 backed by a runnable numerical experiment
- **1 confirmed by a real ingested paper**

| Conjecture | Verdict | Statement | Outcome |
|---|---|---|---|
| `C1` | plausible | The conformal prediction/calibration procedure has a fixed point in th | — |
| `C2` | uncertain | An importance/likelihood-ratio reweighting between distributions under | → direction (narrow), `graphstore.experiment_c2` |
| `C3` | implausible | A finite-capacity / complexity-control premise underlies weighted exch | — |
| `C4` | uncertain | The ERM / uniform-convergence operator has a fixed point. | → direction (promising), `graphstore.experiment_c4` |
| `C5` | uncertain | The no-regret online play has a fixed point - a limit object the play  | → direction (promising), `graphstore.experiment_c5` |
| `C6` | plausible | The weighted conformal calibration procedure is a no-regret play: boun | ✅ **CONFIRMED** by real paper `adaptive_conformal_inference` (structurally verified: True) |
| `C7` | uncertain | A curvature (strong-convexity) bound causes the offline gradient-desce | → direction (narrow), `graphstore.experiment_c7` |

**The loop closes:** the system generated falsifiable predictions by analogy, an independent judge separated the sound from the spurious, the uncertain ones were refined and experimentally tested, and its flagship prediction (C6 — *the weighted conformal calibration procedure is a no-regret play*) was realized by a real published paper it had never read, and confirmed **structurally** in the system's own representation.

