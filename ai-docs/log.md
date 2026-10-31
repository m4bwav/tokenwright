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

## 2026-10-30 session 3

- Social preview uploaded through the browser (repo Settings).
- Wiki written with wikiwright and pushed: 8 pages, every output verified against tw.py at v0.1.0 (ai-docs/notes/2026-10-30-wiki-verify.py and .out.txt); live check 0 failures. Note: ai-docs/notes/2026-10-30-github-wiki.md.
- Found two tw.py bugs for 0.1.1: score double counts a second whole read (whole-read + repeat read); changed reports one line too many.

## 2026-10-30 session 4

- Mark approved folding skill-tidy in. tokenwright 0.2.0: fourth skill tokenwright-catalog (tidy.py moved whole, `tw.py catalog` forwards), PR #1 merged, tagged and released. Decision: ai-docs/decisions/2026-10-30-fold-skill-tidy.md.
- tidy.py `apply` backs up beside the file when the state folder cannot be written (found by the eval run: the WSL2 eval sandbox is read-only).
- Evals: hub T-20261030-2 5/5; catalog T-20261030-1 5/6, outcome-catalog blocked by the sandbox after three tuning iterations (L-003 in the catalog unit).
- skill-tidy 0.2.5 released with a moved notice (PR #10 merged). Local: skill-tidy@mark-local uninstalled and removed from the Ai marketplace; tokenwright@mark-local updated to 0.2.0; the parked index in the user CLAUDE.md now points at tokenwright-catalog's tidy.py (`tw.py catalog parked index`).
- Wiki updated for 0.2.0, live check 0 failures.

## 2026-10-30 session 5

- Mark approved archiving and withdrawing skill-tidy. m4bwav/skill-tidy description set to a moved notice and archived. Directory withdrawal blocked by the finwright guard hook (false positive on the word "withdraw"); left for Mark.

## 2026-10-30 session 6

- Fixed the two tw.py bugs the wiki found: `score` counts a second whole read once (as a repeat read); `changed` line count no longer adds one for a final newline. Two tests (41 pass). PR #3 merged, v0.2.1 tagged and released, tokenwright@mark-local updated to 0.2.1.
- Wiki updated for 0.2.1 (Commands, FAQ, Getting-Started, Versions-and-Upgrading, _Footer); outputs 14 checked 0 missing, live 0 failures.
- tidy.py's `conflicts` prints shared words in set order, which changes per run; the wiki verify script now sets PYTHONHASHSEED=0.
- First multi-turn eval, multiturn-reread: `claude plugin eval` has no multi-turn cases, so `context.history_file` seeds a recorded first turn and the scaffold changes the file before the new prompt. 1.00 in both arms, no saving (T-20261030-3). The Bash-dependent cases wait for a macOS or Linux run.

## 2026-10-30 session 7

- tidy.py `conflicts` shared words now break ties alphabetically; the test checks three hash seeds give one answer (catalog C-20261030-3). The wiki verify script no longer needs PYTHONHASHSEED=0.
- Mark withdrew skill-tidy's Claude directory submission himself. Nothing waits on him now.
