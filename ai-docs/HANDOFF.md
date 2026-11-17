# Handoff: tokenwright

Updated 2026-11-16 (after grind session 15). Status: in progress (improvement grind). Continue with [plans/2026-11-15-tokenwright-improve-continue-prompt.md](plans/2026-11-15-tokenwright-improve-continue-prompt.md). It replaces the 2026-10-30 build prompt, whose list was finished at session 30.

## State

- Public: https://github.com/m4bwav/tokenwright. v0.3.13 released (0.3.13 delegation habit names its 5k break-even, T-20261116-14).
- Four skills (tokenwright, tokenwright-script, tokenwright-skills, tokenwright-catalog), `tw.py` and `tidy.py`. 59 unit tests pass.
- Budget GREEN. habits.md is the largest reference at 2,498 tokens, right at the line.
- Evergreen: hub refreshed 2026-11-15, due 2026-11-24. Catalog unit due 2026-11-21.
- Evals: hub 10 of 10, catalog 5 of 5; outcome-catalog unblocked (with 1.00, without 0.80, T-20261115-1).
- Wiki at 0.3.12 (commit 660c558), refreshed in session 14.
- Hook meter live since 2026-11-01 (`TOKENWRIGHT_HOOKS=warn`), step kept at 25k after two looks.
- everscout beat `token-saving` feeds refreshes. Harvest targets are in `skills/tokenwright/harvest.json`.

## The improvement grind

- Study and seed list: [research/2026-11-15-improvement-study.md](research/2026-11-15-improvement-study.md). Main finding: no eval has shown a saving yet, since outcome cases score the same with and without the plugin. First question is which parts pay, tested on long sessions.
- Grind state: everlast vault, `projects/tokenwright/private/grind` (pass as `--state`). Session 1 finished seven items; the ledger ranks the rest.
- Road confirmed 2026-11-16 (askwright road-2026-11-15 answered): finished = reach, works and is measured on Codex, Copilot, Cursor and Gemini CLI as well as Claude Code. Milestones: the long-session A/B, and per-agent support.
- Per-agent: table in [research/2026-11-16-other-agents-sessions.md](research/2026-11-16-other-agents-sessions.md). Copilot CLI read by score. Next readers: Gemini CLI, then Codex (zstd). Cursor has no local data.
- A/B: T-20261116-1 (long job) and T-20261116-2 (history cases, stub-plugin arm) showed no saving. `scripts/ab_eval.py` now runs any A/B with tokens per arm. History cases leak the plugin into the stub arm, so the next case needs no history (ledger item). Ledger also holds: tw.py discoverability (bare `tw.py` costs 2-5 calls).
- Session 6 ruled out: change-check in one turn (T-20261116-4, case ab-regen-changed) and a habit for session-start loads (T-20261116-5, loads are used). Hook times in T-20261116-6.
- Session 7: live meter check passed (T-20261116-8). finwright guard PR #21 (~470 to ~210 ms a call) merged 2026-11-16. Next picks: the ledger (`grw.py next`).
- Session 8: hook notes do not change what the agent pulls next (T-20261116-9).
- Session 15: delegation break-even scanned and shipped in 0.3.13 (T-20261116-14). Next picks: live check g272313 from 2026-11-17, worth lite scan gf7e6ad, then the ledger. Wiki is at 0.3.12; 0.3.13 changed only habits.md wording, so no wiki change (small ruling).
- Session 14: wiki refreshed to 0.3.12 (gd596be). Next picks: live check g272313 (only from 2026-11-17; grw.py offers it earlier, so skip it until then), delegation break-even g79cddf (A/B), worth lite scan gf7e6ad.
- Session 13: effort-change and subagent-TTL claims verified from docs, no habit (R-20261116-1, -2); second-baseline item dropped (stop point). Next picks: live check g272313 from 2026-11-17, delegation break-even g79cddf (A/B), wiki gd596be.
- Session 12: see log. Next picks: the three verify items from the beat scan (effort change and cache, subagent 1-hour TTL, delegation break-even); live check g272313 from 2026-11-17.
- Session 11: the post hook counted Bash's bashEditDiff (never in context), so sed or script edits raised false big-output notes (T-20261116-12); fixed in 0.3.10. Live check: from 2026-11-17, Bash edits should no longer raise ~30k notes. Next pick: the ledger (beat rescan g81ef2d, tw.py discoverability gf74a42).
- Session 10: Copilot inputTokens includes cache reads and writes (T-20261116-11); fixed in 0.3.9. Next pick: the beat rescan (g81ef2d), then the ledger.
- Session 9: real rate is 2.3 chars a token, not 4 (T-20261116-10); tw.py fixed in 0.3.8, tidy.py has a ledger item. Next picks: the ledger (`grw.py next`; beat rescan and Copilot cache-read check are top).
- Live-use check in flight: from 2026-11-16, compare hook start time and `score` output on sessions with subagents against the numbers in log.md.

## Waits on the owner

- Nothing open on askwright.
- Unattended running is not agreed. No hours or budget are granted, so sessions run attended.

## Grants

- None beyond the owner's standing rules (merge own pull requests after checks, tag and release without asking, tests always allowed).

## Carried over from the build chain

- Every score-kind idea from the book notes is added or ruled out (R-20261030-9 to R-20261101-2). Do not retest them without new data.
- Owed eval case: a job of three or more steps with long output, to test scripting for real (L-004). It is seed 1 in the study note.
- Thresholds rest on one maintainer's transcripts. A second baseline needs another user's data.
