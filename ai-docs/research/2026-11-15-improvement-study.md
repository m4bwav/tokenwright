# Improvement study, 2026-11-15

A read of the whole plugin and repository at v0.3.2, made to seed the improvement grind ([continue prompt](../plans/2026-11-15-tokenwright-improve-continue-prompt.md)). Facts below were checked on that day unless marked as a lead. Leads are untested: the grind turns each into a ledger item with a test.

## Where the plugin stands

- Four skills, two CLIs: `tw.py` (621 lines; changed, score, note, meter, repeats, skill, estimate, catalog, hook) and `tidy.py` (1,812 lines; scan, lint, conflicts, triggers, sections, split, park, unpark, parked, budget, usage, offload, startup, harvest).
- 48 unit tests pass. `scripts/budget.py` is YELLOW: `references/levers.md` is 2,527 tokens against a green line of 2,500.
- Hub evergreen unit: last checked 2026-10-30, due 2026-11-13, so overdue. `verify_at_use` is on and all three volatile claims carry the 2026-10-30 check date. The catalog unit was refreshed 2026-11-15 and is due 2026-11-21.
- Evals: 10 of 10 hub cases pass and 5 of 5 catalog cases, with `outcome-catalog` recorded as blocked by a read-only sandbox. T-20261101-1 found the cause (the eval temp folder on tmpfs) and the fix (`TMPDIR` on a real disk), so the block may already be solvable.
- The handoff and log stopped at 0.2.12. Releases 0.2.13 to 0.3.2 (the `note` command, the file-path habit, harvest targets, the listing budget override) were recorded in the CHANGELOGs but not in `ai-docs/`. HANDOFF.md was rewritten with this study.

## The main finding

No eval has yet shown a saving. Every outcome case scores the same with and without the plugin (T-20261030-1, T-20261030-3, T-20261101-1), because current models already search before they read on short tasks (L-003). The measured value so far is in the tools (`tw.py changed` gets used, `score` ranks sinks) and in the catalog skill (action and outcome deltas of +1.00 and +0.40). The habits text, which is most of what loads, is unproven.

So the first question for the grind is not "what to add" but "which parts pay": a with-versus-without test on long sessions, where L-002 and L-003 say the saving should be.

## Seed candidates

Each is a lead with the cheapest test that could prove it wrong.

### Prove or cut what exists

1. Long-session A/B. Build the owed eval case (L-004): a job of three or more steps with long output, repeated, in a session long enough for carried cost to matter. Test: `claude plugin eval` both arms, tokens and cost compared.
2. Worth verdict per skill. No evergreen-worth run is on record for any of the four skills. Test: evergreen-worth lite scan first (cost per session, real firing rate), heavy A/B only where the lite scan is unclear.
3. Habit-by-habit audit. For each row of `references/habits.md`, is the saving measured, an estimate, or already what a bare model does? Test: a transcript scan for how often the wasteful pattern still occurs. A habit the model already follows is a candidate to cut, which also buys budget.
4. `tw.py note` adoption. How many sessions that loaded tokenwright wrote a note, and do the guesses agree with `score`? Test: scan transcripts since 0.3.0.
5. Hook value. The meter speaks once or twice a session. Did the agent change what it did after a note? Test: compare tool output in the calls after a meter note with the calls before.

### Measurement accuracy

6. Characters divided by four. Check the estimate against the real `usage` fields in transcripts, by content kind (code, JSON, prose, base64). Test: a scan; if the error is large for one kind, a per-kind divisor.
7. Subagent cost. `tw.py score` shows no handling of sidechain or subagent transcripts (lead: confirm by reading `load_events`). Agent and workflow fan-outs are now a large share of spend. Test: score a session with subagents and compare against its real usage.
8. Thresholds on one user's data. The open question in RESEARCH.md stands: every threshold comes from one maintainer's 300 transcripts. A second baseline needs another user's data, so this one may wait on the owner.

### Reach

9. Other agents. The plugin says cross-agent, but `tw.py` names no Codex, Copilot, Cursor or Gemini transcript format. Test: find where each stores sessions and whether `score` can read one. Cheap first step: document what works where.
10. New platform levers. The last full research pass was 2026-10-30 to 2026-11-01. Test: the search plan in RESEARCH.md against current Claude Code and API docs and changelogs, each claim from a primary source.
11. The `token-saving` beat and the harvest targets. Fold in what the scans since 2026-11-01 found.

### Upkeep

12. Bring `levers.md` back under 2,500 tokens (move a section to its own reference, or cut what item 3 rules out).
13. Refresh the hub unit and re-check its three volatile claims.
14. Re-run `outcome-catalog` in WSL with `TMPDIR` on a real disk and clear the block if it passes.
15. Wiki: last recorded at 0.2.12. Check it against 0.3.2.
16. Hook latency. Each hooked tool call starts a Python process. Measure the delay per call on Windows; a slow hook costs time on every Read.
17. Overlap check with context-health and repo-traffic (already on the plugin backlog).

## Draft grind profile

For the first session to check with `grw.py doctor`, not a decision. The state folder is `projects/tokenwright/private/grind` in the everlast vault, outside this repository, because ledger evidence can name private sessions.

```json
{
 "project": "tokenwright", "min_value": 2, "ask_route": "askwright",
 "people": {"owner": {"review_cap": 2}},
 "lanes": {
  "research": {"kind": "maintenance"},
  "study": {"kind": "tests"},
  "evals": {"kind": "tests"},
  "cli": {"kind": "code"},
  "skill-text": {"kind": "writing"},
  "upkeep": {"kind": "maintenance"}
 },
 "guards": {"merge": "allow: after checks pass", "touch_main": "deny: branch", "stack_on_pending": "deny"},
 "discover": ["score recent sessions for sinks nothing catches", "research sweep against the search plan", "re-run the eval suite", "budget and docs drift"]
}
```

Draft road, for the owner to correct once: finished means "a user can see, in numbers from their own sessions, what tokenwright saved, and every habit and command in it has a test behind it". Milestones: a long-session A/B that shows a saving (weight 3), a worth verdict for each skill (3), every habit measured or cut (2), `score` right for sessions with subagents (2), an honest per-agent support table (1).
