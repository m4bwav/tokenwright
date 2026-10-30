# Log

## 2026-10-30 · session 1 · kickoff
- Built the plugin from prompts/2026-10-30-token-saving-plugin-kickoff.md: three skills, tw.py with 11 unit tests, hooks off by default, evals with fixtures, budget, banner (Z-Image Turbo, seed 33).
- Research: web survey (research/2026-10-30-token-saving-survey-web.md), local survey of existing habits (private sidecar in the maintainer vault, projects/tokenwright/private), books list (research/books.md). Ohno, Womack and Goldratt read into the book-learnings notes.
- Measured: inventory fixture 21,400 tokens whole vs 56 by grep; server.log 61,600 vs under 50. tw.py score on a 187-turn session: 28k avoidable tokens carried as 3.3M cache reads.
- Lessons: L-001 usage dedupe by requestId; L-002 rank by carried cost.
