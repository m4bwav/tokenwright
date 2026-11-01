# Tests: tokenwright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. Unit tests for tw.py are in the repository's `tests/`. A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim. Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`. Newest first.

## Runs

### T-20261101-2 · 2026-11-01 · claude plugin eval 2.1.316 (3 runs, single-arm, --scaffold) · WSL2 Ubuntu · 1/1
- Why: evergreen-tune on multiturn-repeat-job (T-20261101-1 fail). Iteration 1: added 'same again for' to tokenwright-script's description; still 0/3 Write, 2 turns, $0.05 a run. Reverted.
- Ruling: the job is two commands and answers in two turns. tokenwright-script's own rule says a script pays at three or more steps or when output needs trimming, so the case expected what the skill advises against. Dropped the wrote-script grader; the judge (right counts) stays. Re-run 3/3, $0.15.
- Harness: the run wrote its own 900 KB session transcript next to turn1.jsonl; now gitignored.
- led to: L-004.

### T-20261101-1 · 2026-11-01 · claude plugin eval 2.1.316 (1 run each arm, --scaffold, Bash Write Edit granted) · WSL2 Ubuntu, TMPDIR on ext4 · 8/9
- Why: first run with Bash, on Linux. The read-only sandbox of catalog L-003 came from the eval temp folder on WSL's tmpfs /tmp; with `TMPDIR=$HOME/evaltmp` writes work. Command in AGENTS.md.
- New cases: outcome-score (tw.py score on a generated transcript), multiturn-changed (snapshot seeded by the scaffold, `tw.py changed` on turn 2), multiturn-repeat-job (third request for the same two-command log summary).
- action-catalog Δ +1.00, outcome-catalog Δ +0.40 (baseline edits without checking). outcome-find-function, outcome-log, outcome-score Δ 0 (both arms 1.00; the with arm ran tw.py score). multiturn-changed 1.00 (used `tw.py changed`, no whole re-read), multiturn-reread 1.00. History cases now run single-arm (the harness says history carries the plugin into both arms).
- Fail: multiturn-repeat-job 0.50: right counts, but no script written on the third repeat; "Same again for ..." does not wake tokenwright-script. To evergreen-tune.
- About $2.0.
- led to: catalog L-003 resolved.

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
