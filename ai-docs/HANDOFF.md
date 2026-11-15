# Handoff: tokenwright

Updated 2026-11-15. Status: in progress (improvement grind, not yet started). Continue with [plans/2026-11-15-tokenwright-improve-continue-prompt.md](plans/2026-11-15-tokenwright-improve-continue-prompt.md). It replaces the 2026-10-30 build prompt, whose list was finished at session 30.

## State

- Public: https://github.com/m4bwav/tokenwright. v0.3.2 tagged and released (0.3.0 `tw.py note`, 0.3.1 pass data by file path, 0.3.2 `SLASH_COMMAND_TOOL_CHAR_BUDGET` honoured by the listing budget). No open pull requests or issues on 2026-11-15.
- Four skills (tokenwright, tokenwright-script, tokenwright-skills, tokenwright-catalog), `tw.py` and `tidy.py`. 48 unit tests pass.
- Budget YELLOW: `references/levers.md` is 2,527 tokens against a green line of 2,500.
- Evergreen: the hub is overdue (last checked 2026-10-30, due 2026-11-13; three volatile claims to re-check). The catalog unit was refreshed 2026-11-15, due 2026-11-21.
- Evals: hub 10 of 10, catalog 5 of 5 with `outcome-catalog` recorded as blocked by a read-only sandbox. T-20261101-1 found a fix (`TMPDIR` on a real disk in WSL), so a re-run may clear it.
- Wiki last recorded at 0.2.12. Check it against 0.3.2.
- Hook meter live since 2026-11-01 (`TOKENWRIGHT_HOOKS=warn`), step kept at 25k after two looks.
- everscout beat `token-saving` feeds refreshes. Harvest targets are in `skills/tokenwright/harvest.json`.

## The improvement grind

- Study and seed list: [research/2026-11-15-improvement-study.md](research/2026-11-15-improvement-study.md). Main finding: no eval has shown a saving yet, since outcome cases score the same with and without the plugin. First question is which parts pay, tested on long sessions.
- Grind state does not exist yet. The first session sets it up in the everlast vault at `projects/tokenwright/private/grind` from the draft profile and road in the study note, and puts the road on an askwright page.
- No askwright set is open. No live-use check is in flight.
- No ledger yet, so the 17 seed candidates in the study note are the queue. Load them with `grw.py add` at setup.

## Waits on the owner

- The road and value model, once the first session puts them on an askwright page.
- Unattended running is not agreed. No hours or budget are granted, so sessions run attended.

## Grants

- None beyond the owner's standing rules (merge own pull requests after checks, tag and release without asking, tests always allowed).

## Carried over from the build chain

- Every score-kind idea from the book notes is added or ruled out (R-20261030-9 to R-20261101-2). Do not retest them without new data.
- Owed eval case: a job of three or more steps with long output, to test scripting for real (L-004). It is seed 1 in the study note.
- Thresholds rest on one maintainer's transcripts. A second baseline needs another user's data.
