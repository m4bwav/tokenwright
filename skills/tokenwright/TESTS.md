# Tests: tokenwright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. Unit tests for tw.py are in the repository's `tests/`. A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim. Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`. Newest first.

## Runs

### T-20261031-1 · 2026-10-31 · claude plugin eval (1 run each, --ablation none) · Windows 11 native · 9/9
- Why: all four descriptions trimmed to bring the budget back to green (C-20261031-3). trigger-1..5 and decoy-1..4 pass. About $1.03.
- led to: none.

### T-20261030-3 · 2026-10-30 · claude plugin eval 2.1.281 (1 run each arm, --scaffold) · Windows 11 native · 1/1
- Why: first multi-turn case. The harness has no multi-turn cases; `context.history_file` seeds a recorded first turn (`turn1.jsonl`, built by the case's `make_history.py`: settings.py read whole, answer 30) and the scaffold swaps in the edited file before the new prompt.
- multiturn-reread: 1.00 both arms, 2 turns, $0.31 with vs $0.30 without. Neither arm re-read settings.py whole; both answered 45 and RETRY_LIMIT unchanged. No saving: bare Claude already searches a file it read earlier.
- Not built: the repeated-job and long-session cases need Bash (scripts, `tw.py changed`, `tw.py score`), which cannot be granted to eval runs on Windows (T-20261030-1). Run them on macOS or Linux.
- led to: none.

### T-20261030-2 · 2026-10-30 · claude plugin eval 2.1.307 (1 run each, --ablation none) · Windows 11 native · 5/5
- Why: the fold of skill-tidy changed the hub's and tokenwright-skills' descriptions and added a fourth skill. trigger-1..3 and decoy-1..2 pass; the catalog cases are recorded in ../tokenwright-catalog/TESTS.md (T-20261030-1). About $0.40.
- led to: none.

### T-20261030-1 · 2026-10-30 · claude plugin eval (3 runs each arm) · owner-pc Windows · 7/7 cases pass
- Triggers: trigger-1, -2 (tokenwright) and trigger-3 (tokenwright-skills) invoked 3/3 with, 0/3 without. Decoys (OAuth refresh token, CSS design tokens) quiet in both arms. $2.17.
- Outcomes: outcome-find-function 1.00 both arms, 2 turns, about $0.056 with vs $0.052 without. outcome-log 1.00 both arms, 5-7 turns, about $0.24 with vs $0.27 without. No saving: bare Claude already greps the 2,690-line file and the 4,000-line log instead of reading them whole.
- Harness: Bash cannot be granted on Windows (no sandbox backend), so outcome cases run with Read, Glob, Grep, Skill only. Grader arm values are with-only or both.
- led to: L-003.
