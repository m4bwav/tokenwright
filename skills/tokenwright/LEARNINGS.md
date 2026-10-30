# Learnings: tokenwright

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-001 · 2026-10-30 · Count usage once per request, not once per transcript line
- Trigger: tw.py score reported 487 turns for a session that had 187; one response is written as several assistant lines repeating the same usage.
- Hypothesis: transcripts split a response by content block; dedupe on requestId (fall back to message.id).

### L-002 · 2026-10-30 · Carried cost, not size, ranks sinks
- Trigger: in a 187-turn session, 28k avoidable tokens became about 3.3M cache-read tokens because most entered early.
- Hypothesis: every loaded token is re-read each later turn until compaction; rank by tokens times later turns.
