# Handoff: tokenwright

Updated 2026-11-15 (after grind session 1). Status: in progress (improvement grind). Continue with [plans/2026-11-15-tokenwright-improve-continue-prompt.md](plans/2026-11-15-tokenwright-improve-continue-prompt.md). It replaces the 2026-10-30 build prompt, whose list was finished at session 30.

## State

- Public: https://github.com/m4bwav/tokenwright. v0.3.3 tagged and released (subagent transcripts in `score`, idle hook 26 ms, `note --saved` checked, hub refresh).
- Four skills (tokenwright, tokenwright-script, tokenwright-skills, tokenwright-catalog), `tw.py` and `tidy.py`. 51 unit tests pass.
- Budget GREEN. habits.md is the largest reference at 2,498 tokens, right at the line.
- Evergreen: hub refreshed 2026-11-15, due 2026-11-24. Catalog unit due 2026-11-21.
- Evals: hub 10 of 10, catalog 5 of 5; outcome-catalog unblocked (with 1.00, without 0.80, T-20261115-1).
- Wiki at 0.3.2 (commit 4dd7e89). Owes a 0.3.3 pass (ledger item).
- Hook meter live since 2026-11-01 (`TOKENWRIGHT_HOOKS=warn`), step kept at 25k after two looks.
- everscout beat `token-saving` feeds refreshes. Harvest targets are in `skills/tokenwright/harvest.json`.

## The improvement grind

- Study and seed list: [research/2026-11-15-improvement-study.md](research/2026-11-15-improvement-study.md). Main finding: no eval has shown a saving yet, since outcome cases score the same with and without the plugin. First question is which parts pay, tested on long sessions.
- Grind state: everlast vault, `projects/tokenwright/private/grind` (pass as `--state`). Session 1 finished seven items; the ledger ranks the rest.
- Open askwright set: `projects/tokenwright/private/ask/road-2026-11-15` in the vault (what finished means; which milestones stay). Until answered, take only road-independent work. The worth-verdict item waits on it.
- Live-use check in flight: from 2026-11-16, compare hook start time and `score` output on sessions with subagents against the numbers in log.md.

## Waits on the owner

- The road and value model: askwright set road-2026-11-15.
- Unattended running is not agreed. No hours or budget are granted, so sessions run attended.

## Grants

- None beyond the owner's standing rules (merge own pull requests after checks, tag and release without asking, tests always allowed).

## Carried over from the build chain

- Every score-kind idea from the book notes is added or ruled out (R-20261030-9 to R-20261101-2). Do not retest them without new data.
- Owed eval case: a job of three or more steps with long output, to test scripting for real (L-004). It is seed 1 in the study note.
- Thresholds rest on one maintainer's transcripts. A second baseline needs another user's data.
