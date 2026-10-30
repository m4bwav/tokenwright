# Handoff: tokenwright

Updated 2026-10-30 (session 2). Continue with `ai-docs/plans/2026-10-30-tokenwright-continue-prompt.md`.

## State

- 0.1.0 built and committed locally on `main` (no remote yet). Installed as `tokenwright@mark-local` (entry added to the Ai marketplace.json).
- Skills: tokenwright (hub + references habits, levers, waste-vocabulary), tokenwright-script (+ templates), tokenwright-skills. tw.py: changed, score, repeats, skill, estimate, hook. Hooks inert unless `TOKENWRIGHT_HOOKS` is warn or block.
- Tests: 11 unit tests pass; budget GREEN. Evals T-20261030-1: 7/7 pass (triggers +1.00 over baseline, decoys quiet), but the two outcome cases showed no cost saving (L-003).
- Banner and social preview in `.github/images` (Z-Image Turbo, seed 33).
- Research: `ai-docs/research/` (web survey, books). Private survey of existing habits: everlast vault `projects/tokenwright/private/`. Book notes: `Ai/books/plugin-learnings/tokenwright-lean-goal.md` (Ohno, Womack, Goldratt).
- evergreen PR https://github.com/m4bwav/evergreen/pull/14 MERGED (session 2): optional W section in the wrap-up (calls `tw.py score`), T kept; the wrap-up now takes fixes for T/W candidates from tokenwright's habits, tokenwright-script and tokenwright-skills, and evergreen-new runs tokenwright-skills on a finished skill. Also fixed evergreen CI: Python 3.9 runs on ubuntu-24.04 (ubuntu-latest 26.04 has no 3.9).
- everscout beat `token-saving`: built (16 sources, read only, probe 14 ok), first scan folded into habits.md and levers.md. Its folder is the private beat dir (indie-ai-scout/beats/token-saving); data in ~/.everscout/data/token-saving. Scan with `--reddit-reader rss`: the global config `reddit.reader: auto` would switch to Arctic Shift on 2026-11-13.

## Waits on Mark

1. Creating the public repo `m4bwav/tokenwright` was refused by the auto-mode permission classifier again in session 2, even with Mark's go-ahead for a full release in the prompt. Mark: run `gh repo create m4bwav/tokenwright --public --source . --push` in the clone yourself (or add a Bash allow rule); the next session then checks CI, writes the wiki and tags v0.1.0. Local paths already scrubbed from tracked files.
2. Name: kept tokenwright. Skill-tidy: stays separate for now; fold in or not?

## Next

1. Publish (above), CI green, wiki (wikiwright), tag v0.1.0 and release.
2. Multi-turn evals where the habits should matter: a re-read after an external change (`tw.py changed`), a repeated job that should become a script, a long session scored by tw.py.
3. Fold the beat's first findings into habits.md and levers.md.
4. Next books: Pragmatic Programmer, Algorithms to Live By.
5. Calibrate tw.py thresholds (400 lines, 20k chars) across many transcripts.
