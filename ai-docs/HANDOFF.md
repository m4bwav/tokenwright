# Handoff: tokenwright

Updated 2026-10-30 (session 9). Continue with `ai-docs/plans/2026-10-30-tokenwright-continue-prompt.md`.

## State

- PUBLIC: https://github.com/m4bwav/tokenwright, CI green. v0.2.3 tagged and released 2026-10-30 (https://github.com/m4bwav/tokenwright/releases/tag/v0.2.3; PR #9: Meadows habits). Installed as `tokenwright@mark-local` 0.2.3.
- Four skills: tokenwright (hub + references habits, levers, waste-vocabulary), tokenwright-script (+ templates), tokenwright-skills, tokenwright-catalog (formerly skill-tidy: lint, conflicts, check/apply, split, park, startup; `scripts/tidy.py`, also `tw.py catalog`). tw.py: changed, score, repeats, skill, estimate, catalog, hook. Hooks inert unless `TOKENWRIGHT_HOOKS` is warn or block.
- Two evergreen units: the hub (`skills/tokenwright/evergreen.json`, next due 2026-11-13) and tokenwright-catalog (`skills/tokenwright-catalog/evergreen.json`, next due 2026-11-05, history carried over from skill-tidy).
- Tests: 41 unit tests (test_tw.py + test_tidy.py). Budget YELLOW: descriptions total about 1,920 characters (green line 1,500). Accepted with the fold; see ai-docs/decisions/2026-10-30-fold-skill-tidy.md.
- Evals: hub T-20261030-2 5/5 (triggers, decoys); T-20261030-3 multiturn-reread 1/1, no gain over baseline (multi-turn via `context.history_file` + scaffold). Catalog T-20261030-1 5/6: outcome-catalog fails because the WSL2 eval sandbox (claude 2.1.307) makes the workspace read-only (catalog L-003). Re-run it on macOS or Linux, or when the harness allows writes.
- Wiki live at 0.2.3 (https://github.com/m4bwav/tokenwright/wiki), note in ai-docs/notes/2026-10-30-github-wiki.md.
- skill-tidy: 0.2.5 released as the last release with a moved notice; repository archived 2026-10-30 (Mark's go-ahead; description says moved). skill-tidy@mark-local uninstalled and removed from the Ai marketplace. The parked-skills index in the user CLAUDE.md points at `tokenwright/skills/tokenwright-catalog/scripts/tidy.py`.
- everscout beat `token-saving`: built, first scan folded in. Scan with `--reddit-reader rss` (the global `reddit.reader: auto` would switch to Arctic Shift on 2026-11-13).

## Waits on Mark

Nothing. skill-tidy's Claude directory submission was withdrawn by Mark 2026-10-30.

## Next

1. Multi-turn evals that need Bash (a repeated job that should become a script; a long session scored by tw.py; `tw.py changed`): run on macOS or Linux, since Windows eval runs cannot get Bash. Pattern: cases/multiturn-reread (make_history.py builds turn1.jsonl).
2. Books: Pragmatic Programmer and Algorithms to Live By done (notes in Ai/books/plugin-learnings tokenwright-pragmatic.md and tokenwright-algorithms.md). Meadows done too (tokenwright-meadows.md). No book left on disk in books.md; Berryman and Ziegler is not on disk. Still owed from the three notes: a visible meter in hook mode, score against the best past session of the same kind, a workaround-after-deny score kind, a MUST/NEVER count in tw.py skill; tw.py score kinds poll, plateau, stale, debug-loop, many-similar-edits and an exploration share line; tokenwright-skills checks (copied AGENTS.md text, retry loops with no cap); all need thresholds from real transcripts (item 3).
3. Calibrate tw.py thresholds (400 lines, 20k chars) across many transcripts.
4. Optional: trim descriptions back to green if a trigger eval shows room.
