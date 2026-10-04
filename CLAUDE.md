# CLAUDE.md — session bootstrap for OpenReasons

**Session start, with no instruction from the owner needed** (the owner, 2026-10-04 09:44 EDT; MetaProof #263): before your first action read MetaProof `ledgers/ROOT-SEED.md` ( https://github.com/yulinl2/MetaProof/blob/main/ledgers/ROOT-SEED.md ), first screen only, and follow it. It tells you which role you are (your first message, else your title, else your creator or routine, else a vacant supervisor seat, else a per-question worker), where that role talks (MetaProof #208; the `to:<role>` labels), the owner's filter read in place (MetaSci `kb/owner-guidance/RECAP.md`), the clocks, and where live state is regenerated. With a MetaProof checkout beside this repository: `python3 "$(git rev-parse --show-toplevel)/../MetaProof/bin/session_boot.py" --fetch` prints that screen with the live holders (anchored at the repository root, so it also works from a subdirectory); without one, read that link on GitHub. Then this repository's own rules below.

This repository had no bootstrap file of its own until this minimal one was added 2026-09-28 (MetaSci issue #30),
so the owner's standing instructions have somewhere durable to live instead of being pasted by hand each session.

1. **Read MetaProof `ledgers/OWNER-POLICY.md` first** — the owner's standing operating instructions across all
   eight repositories, verbatim, append-only.
2. **Then this repository's own `README.md`.** Role (MetaProof `ledgers/ROOT-SEED.md`, decision D-16): the
   structure-mapping engine — reads scientific results, represents their reasoning as an (object, attribute,
   relation) graph, and judges novelty / analogy / conjecture by relational structure rather than surface wording.
   Named OpenPriors until 2026-09-02; MetaSci's structure maps pin commit `49f62fb` of this repository.
3. **State as of the chain's last sweep:** dormant since 2026-07-04; pull requests #50–#54 are stale and tied to
   a constitution MetaProof has since archived. Nothing here is queued work by default — check
   `ledgers/ROOT-SEED.md` in MetaProof before assuming otherwise.
