# /sleep — epic-close compression ritual (slash command or paste-prompt)
# Drop into `.claude/commands/sleep.md` in BOTH repos. Wake solves; sleep compresses.
# Zero project state in this file — pure pointer; all state lives on disk.

Close out the current epic. Do not start anything new during this ritual.

1. **VERIFY** — CI green; adversarial review done; REPORT.md section written; every
   figure live-computed; every claim carries its ID + gloss + tier; the PR's `Serves:`
   link and "For the human" block are current and honest (including "Assumptions & Cut
   Corners").
2. **COMPRESS** — Write the one-line LOG entry **from the PR diff, not from memory**
   (glossed IDs; epic letter with its name). This line is the only thing the next
   session is guaranteed to read — make it sufficient.
3. **PARK** — File any still-open `Q-### "gloss"` / `A-### "gloss"` items as issues;
   move stray ideas to PARKING.md with one-line glosses. Nothing lives only in this
   session's context.
4. **HANDOFF** — Leave the tree clean (commit, or stash/discard with a LOG note). Open
   the PR. Either start the next epic on a stacked branch with a fresh plan, or end the
   session cleanly. Never leave a dirty tree asleep.
