# Handoff: tokenwright

Updated 2026-10-30 (session 1). Continue with `ai-docs/plans/2026-10-30-tokenwright-continue-prompt.md`.

## State

- 0.1.0 built and committed locally on `main` (no remote yet). Installed as `tokenwright@mark-local` (entry added to the Ai marketplace.json).
- Skills: tokenwright (hub + references habits, levers, waste-vocabulary), tokenwright-script (+ templates), tokenwright-skills. tw.py: changed, score, repeats, skill, estimate, hook. Hooks inert unless `TOKENWRIGHT_HOOKS` is warn or block.
- Tests: 11 unit tests pass; budget GREEN. Evals T-20261030-1: 7/7 pass (triggers +1.00 over baseline, decoys quiet), but the two outcome cases showed no cost saving (L-003).
- Banner and social preview in `.github/images` (Z-Image Turbo, seed 33).
- Research: `ai-docs/research/` (web survey, books). Private survey of existing habits: everlast vault `projects/tokenwright/private/`. Book notes: `Ai/books/plugin-learnings/tokenwright-lean-goal.md` (Ohno, Womack, Goldratt).
- evergreen PR https://github.com/m4bwav/evergreen/pull/14 adds an optional W section to the wrap-up (calls `tw.py score`); T section kept. Assigned to Mark with needs-review, left open because tokenwright is not public yet.
- everscout beat `token-saving`: built (16 sources, read only, probe 14 ok), first scan folded into habits.md and levers.md. Its folder is the private beat dir (indie-ai-scout/beats/token-saving); data in ~/.everscout/data/token-saving. Scan with `--reddit-reader rss`: the global config `reddit.reader: auto` would switch to Arctic Shift on 2026-11-13.

## Waits on Mark

1. Creating the public repo `m4bwav/tokenwright` was refused by the auto-mode permission classifier. Mark: create it, or allow it, then the next session pushes, checks CI, writes the wiki and releases.
2. Name: kept tokenwright. Skill-tidy: stays separate for now; fold in or not?
3. PR #14 on evergreen: merge when happy.

## Next

1. Publish (above), CI green, wiki (wikiwright), tag v0.1.0 and release.
2. Multi-turn evals where the habits should matter: a re-read after an external change (`tw.py changed`), a repeated job that should become a script, a long session scored by tw.py.
3. Fold the beat's first findings into habits.md and levers.md.
4. Next books: Pragmatic Programmer, Algorithms to Live By.
5. Calibrate tw.py thresholds (400 lines, 20k chars) across many transcripts.
