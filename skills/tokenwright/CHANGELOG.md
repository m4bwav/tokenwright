# Changelog: tokenwright

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

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
