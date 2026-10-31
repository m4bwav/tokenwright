# Handoff: tokenwright

Updated 2026-10-30 (session 4). Continue with `ai-docs/plans/2026-10-30-tokenwright-continue-prompt.md`.

## State

- PUBLIC: https://github.com/m4bwav/tokenwright, CI green. v0.2.0 tagged and released 2026-10-30 (https://github.com/m4bwav/tokenwright/releases/tag/v0.2.0). Installed as `tokenwright@mark-local` 0.2.0.
- Four skills: tokenwright (hub + references habits, levers, waste-vocabulary), tokenwright-script (+ templates), tokenwright-skills, tokenwright-catalog (formerly skill-tidy: lint, conflicts, check/apply, split, park, startup; `scripts/tidy.py`, also `tw.py catalog`). tw.py: changed, score, repeats, skill, estimate, catalog, hook. Hooks inert unless `TOKENWRIGHT_HOOKS` is warn or block.
- Two evergreen units: the hub (`skills/tokenwright/evergreen.json`, next due 2026-11-13) and tokenwright-catalog (`skills/tokenwright-catalog/evergreen.json`, next due 2026-11-05, history carried over from skill-tidy).
- Tests: 39 unit tests (test_tw.py + test_tidy.py). Budget YELLOW: descriptions total about 1,920 characters (green line 1,500). Accepted with the fold; see ai-docs/decisions/2026-10-30-fold-skill-tidy.md.
- Evals: hub T-20261030-2 5/5 (triggers, decoys). Catalog T-20261030-1 5/6: outcome-catalog fails because the WSL2 eval sandbox (claude 2.1.307) makes the workspace read-only (catalog L-003). Re-run it on macOS or Linux, or when the harness allows writes.
- Wiki live at 0.2.0 (https://github.com/m4bwav/tokenwright/wiki), note in ai-docs/notes/2026-10-30-github-wiki.md.
- skill-tidy: 0.2.5 released as the last release with a moved notice; repository archived 2026-10-30 (Mark's go-ahead; description says moved). skill-tidy@mark-local uninstalled and removed from the Ai marketplace. The parked-skills index in the user CLAUDE.md points at `tokenwright/skills/tokenwright-catalog/scripts/tidy.py`.
- everscout beat `token-saving`: built, first scan folded in. Scan with `--reddit-reader rss` (the global `reddit.reader: auto` would switch to Arctic Shift on 2026-11-13).

## Waits on Mark

1. skill-tidy's Claude directory submission: Mark approved withdrawal 2026-10-30, but the finwright PreToolUse guard blocks browser actions containing "withdraw". Mark clicks "Withdraw submission" on claude.ai/directory/manage (Skill Tidy page) himself, or confirms through the guard.

## Next

1. Fix the two tw.py bugs the wiki found (score double count of a second whole read; changed line count off by one), with tests; release 0.2.1 and run the wiki's update mode.
2. Multi-turn evals where the habits should matter: a re-read after an external change (`tw.py changed`), a repeated job that should become a script, a long session scored by tw.py.
3. Next books: Pragmatic Programmer, Algorithms to Live By.
4. Calibrate tw.py thresholds (400 lines, 20k chars) across many transcripts.
5. Optional: trim descriptions back to green if a trigger eval shows room.
