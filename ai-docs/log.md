# Log

## 2026-10-30 · session 1 · kickoff
- Built the plugin from prompts/2026-10-30-token-saving-plugin-kickoff.md: three skills, tw.py with 11 unit tests, hooks off by default, evals with fixtures, budget, banner (Z-Image Turbo, seed 33).
- Research: web survey (research/2026-10-30-token-saving-survey-web.md), local survey of existing habits (private sidecar in the maintainer vault, projects/tokenwright/private), books list (research/books.md). Ohno, Womack and Goldratt read into the book-learnings notes.
- Measured: inventory fixture 21,400 tokens whole vs 56 by grep; server.log 61,600 vs under 50. tw.py score on a 187-turn session: 28k avoidable tokens carried as 3.3M cache reads.
- Lessons: L-001 usage dedupe by requestId; L-002 rank by carried cost.
- Evals T-20261030-1: 7/7 pass; triggers +1.00 over baseline; outcome cases show no saving (L-003). Bash cannot be granted to eval runs on Windows.
- everscout beat token-saving built and scanned (16 sources, 9 notes); seven field reports folded into habits.md (C-20261030-2, R-20261030-6).
- Public repo creation refused by the permission classifier; waits on Mark. evergreen PR #14 open for Mark.

## 2026-10-30 session 2

- Mark gave permission for a full release; `gh repo create --public` still refused by the auto-mode classifier (Create Public Surface). Stopped there per the denial rules; repo stays local.
- Scrubbed the local start path from the continue prompt (public-repo rule).
- evergreen PR #14 merged after fixing its red check (ubuntu-latest now 26.04 without Python 3.9; 3.9 moved to ubuntu-24.04) and adding tokenwright pointers to evergreen-wrapup (fixes for T/W candidates) and evergreen-new (tokenwright-skills review), as Mark asked.
- Mark switched to manual mode; repo created public and pushed, CI green, topics set, v0.1.0 tagged and released. Wiki waits for the first page in the web UI; social preview upload is manual.
