# /wake — session re-anchor (slash command or paste-prompt)
# Drop this file into `.claude/commands/wake.md` in BOTH repos.
# Design invariant: this prompt contains zero project state — it is a pure pointer.
# All state lives on disk (CLAUDE.md, LOG.md, PRs, git). If this file ever needs
# updating because the project changed, that is a bug in the project, not in this file.

Resurrect this project. You are a fresh session; assume zero inherited memory — the
repo is the only memory.

1. **ORIENT** — Read `CLAUDE.md` in full. Read the tail of `LOG.md`. Run `git status`,
   `git branch --show-current`, `git log --oneline -15`; list open PRs. Identify the
   active epic and read its PR description.

2. **AUTOPSY** — Reconstruct what the previous session finished vs. left dangling, from
   primary sources only (diffs, CI, tests). The previous session's unverified assertions
   are provisional: re-verify before building on them. Append a **death certificate** for
   the previous session to `deaths.jsonl` (epic, branch, last commit, dirty-file count,
   inferred stopping point) — until hooks automate this. If sessions keep dying at the
   same spot, say so: that pattern is data (usually a sign the epic needs splitting).

3. **RECONCILE** — If the working tree is dirty, resolve every file explicitly: commit
   with an honest message, or stash/discard with a LOG note. Nothing stays silently
   ambiguous.

4. **REPORT** — Post a "For the human" block (≤ 5 bullets): where the last session
   stopped, what survived, what you will do next, any open `Q-### "gloss"` items, and
   the default if the human does nothing.

5. **RESUME** — Continue the active epic under the constitution: visibility mandatory,
   waiting exceptional; block only on the constitutional blocking set. If no epic is
   active, propose the next one from the roadmap as a plan PR before writing code.
   Never start new work while an epic dangles — finish it or park it with a LOG line.
