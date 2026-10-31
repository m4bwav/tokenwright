# Changelog: tokenwright

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

### C-20261031-3 · 2026-10-31 · meter, compare, budget back to green (0.2.7)
- because: book-note items held back while the budget was yellow (HANDOFF session 18); Mark asked for them 2026-10-31
- files: scripts/tw.py (`meter`, hook meter, `score --compare`), hooks/hooks.json (post hook also on Read and Glob), evals/fixtures/make_server_log.py replaces the 250 KB server.log, all four descriptions trimmed (1,920 to 1,467 characters; tidy.py check OK on each)
- The meter and the best-past-session comparison are design choices, not calibrated thresholds: 25k tokens per meter step, past sessions under 10 tool calls skipped.

### C-20261031-2 · 2026-10-31 · AI Engineering (0.2.6)
- because: R-20261031-8 (book-learnings pass)
- files: references/habits.md (Family 1: Edges, not middle; Memory by frequency), references/levers.md (Result caching)
- Both habits are estimates; the rule-placement test is a study item on the token-saving beat.

### C-20261031-1 · 2026-10-31 · tw.py score kind debug-loop (0.2.5)
- because: R-20261031-1
- files: scripts/tw.py (`debug-loop`, DEBUG_LOOP_ERRORS = 3), references/waste-vocabulary.md (Defects row), tests/test_tw.py
- The third failed call in a row to one tool is a `debug-loop` sink, once per streak. `retry` still covers an unchanged resend. Plateau, stale and workaround-after-deny still wait for thresholds.

### C-20261030-7 · 2026-10-30 · tw.py score kind poll (0.2.4)
- because: R-20261030-10
- files: scripts/tw.py (`poll`, POLL_RUNS = 3), references/waste-vocabulary.md (Waiting row), tests/test_tw.py
- The third and later run of one exact shell command in a session is a `poll` sink. Plateau, stale, debug-loop and the others still wait for thresholds.

### C-20261030-6 · 2026-10-30 · Thinking in Systems (0.2.3)
- because: R-20261030-8 (book-learnings pass)
- files: references/habits.md (Family 1 one row, Family 2 two rows), references/levers.md (Rank the fix), ../tokenwright-skills/SKILL.md (Shouted rules)
- All savings are estimates. A visible meter in hook mode, scoring against a best past session, and a workaround-after-deny score kind wait for real-transcript thresholds.

### C-20261030-5 · 2026-10-30 · Two books: Pragmatic Programmer, Algorithms to Live By (0.2.2)
- because: R-20261030-7 (book-learnings pass)
- files: references/habits.md (Family 2, six rows), references/waste-vocabulary.md (Defects, Waiting)
- Stop rule before a search, bisect instead of scan, read the error first, change approach after two misses, sample before a sweep, wait with a deadline. All savings are estimates. New tw.py score kinds (poll, plateau, stale, debug-loop) wait for thresholds from real transcripts.

### C-20261030-4 · 2026-10-30 · tw.py score and changed fixes (0.2.1)
- because: wiki verification (ai-docs/notes/2026-10-30-github-wiki.md, bugs 1 and 2)
- files: scripts/tw.py (score, changed), ../../tests/test_tw.py
- `score` counted a second whole read of a big file twice, as whole-read and as repeat read; it now counts once, as a repeat read. `changed` reported one line too many for files ending in a newline.

### C-20261030-3 · 2026-10-30 · skill-tidy folded in as tokenwright-catalog (0.2.0)
- because: user request (fold skill-tidy into tokenwright)
- files: SKILL.md (description, tw.py commands, Neighbours), scripts/tw.py (catalog command, VERSION), ../tokenwright-skills/SKILL.md (description boundary), ../tokenwright-catalog/ (new skill, from skill-tidy 0.2.4), evals/cases (six catalog cases), ../../tests/test_tidy.py
- The catalog work skill-tidy did ships as a fourth skill with its own evergreen records. `tw.py catalog` forwards to its tidy.py. Descriptions now total about 1,900 characters (budget yellow), against about 2,400 for tokenwright 0.1.0 plus skill-tidy installed side by side.

### C-20261030-2 · 2026-10-30 · Field reports from the token-saving beat
- because: R-20261030-6 (beat scan 2026-10-30)
- files: references/habits.md (Reported in the field), references/levers.md (Recent changes)
- Seven community-reported habits with their numbers and links, marked unverified; Claude Code 2.1.311 compaction change.

### C-20261030-1 · 2026-10-30 · Created (0.1.0)
- because: user request (kickoff 2026-10-30)
- files: all
- Hub skill with the habits catalogue, levers and waste vocabulary; tokenwright-script and tokenwright-skills; tw.py (changed, score, repeats, skill, estimate, hook); hooks off by default.
