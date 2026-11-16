# Tests: tokenwright

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. Unit tests for tw.py are in the repository's `tests/`. A test passes on evidence (a tool call in the trace, a file, a marker), never on the transcript's claim. Entry shape: `### T-20261116-3 · 2026-11-16 · transcript scan: `tw.py score --json` on the newest 400 local sessions over 50 KB (30 days) · Windows · habit audit
- Waste tokens by kind (sessions): big output 1,219,450 (101), whole read 352,170 (19), repeat read 255,080 (43), shell cat 99,839 (61), retry 2,536 (6), debug loop 875 (4), poll 473 (3), re-read after own edit 223 (1). 8,420 tool calls.
- Big output by call number: calls 1 to 5 hold about 841k of the 1.22M, mostly whole-file `cat` of handoff, log and plan files at session or subagent start.
- Verdict: cut the habit row "No re-read after own edit" (the harness already says it; 1 hit in 400). Session-start loads become a ledger item.

### T-YYYYMMDD-n · date · harness · env · passed/total`. Newest first.

## Runs

### T-20261116-12 · 2026-11-16 · transcript scan: what does the post hook count for Bash? newest 500 local sessions · Windows · study (hook accuracy)
- Why: ledger g7102dd. In session 9 the big-output note called a ~700-char Bash result ~9.5k tokens.
- Method: every Bash `toolUseResult` (n=5,954; the same object the PostToolUse hook gets as tool_response) against the tool_result text that entered context.
- Result: the response also carries `bashEditDiff`, a diff of files the command edited, which never reaches the model (4.5M chars across the set, next to 13.7M of stdout). Of 172 results the hook sized at 20k+ chars, 100 were over twice their context size, all from bashEditDiff (one: 143k counted, 683 in context).
- Verdict: ship. For Bash the hook now counts stdout plus stderr only, so false big-output notes and meter inflation after sed or script edits stop.
- Limit: one user's sessions. Other tools still count the JSON of their response.

### T-20261116-11 · 2026-11-16 · transcript scan: does Copilot CLI inputTokens include cache reads? 34 local sessions · Windows · study (per-agent reader)
- Why: ledger gc0e1f0. tw.py mapped Copilot `inputTokens` to Claude's `input_tokens`, which counts only uncached input.
- Method: every `session.usage_record` (n=3,229) in local Copilot CLI events.jsonl; compare inputTokens with cacheReadTokens and cacheWriteTokens.
- Result: cache reads never exceed inputTokens (0 of 3,229); in the 2,868 records with a cache hit, reads are a median 98% of inputTokens (max 100%). inputTokens minus reads minus writes is never negative, with writes in 2,927 records.
- Verdict: ship. inputTokens is the whole prompt, cached parts included. tw.py now reports input as inputTokens less reads and writes, so the usage line no longer counts cached input twice (it overstated input about 50-fold on cached turns).
- Limit: one user's sessions, mostly one model (gpt-5.6-luna). No official doc states it; the evidence is the data.

### T-20261116-10 · 2026-11-16 · transcript scan: real tokens per tool result vs chars/4, newest 500 local sessions · Windows · study (estimate accuracy)
- Why: improvement study seed 6 (ledger g302e75). How far is tw.py's chars/4 from what the model bills?
- Method: for each user turn holding one tool result of 3,000+ chars, real tokens = (input + cache creation + cache read) of the next assistant message, less the same for the previous one, less its output tokens. Main sessions only, images skipped.
- Result (n=1,141): median 2.28 chars a token (p25 2.07, p75 2.48). By model: Opus 5.5 2.31 (n=937), Fable 5.2 2.16 (n=180), Sonnet 5 2.26 (n=28). By kind: shell text 2.29, Markdown reads 2.41, JSON 2.22, code reads 2.02. A fit of tokens on chars gives the same slope (2.30 for shell text) with a small intercept (about 150 tokens), so per-turn overhead does not explain it. Stable across sizes (2.23 at 3-6k chars, 2.38 at 15-40k).
- Verdict: ship. chars/4 under-counted every tw.py token figure by about 75%. CHARS_PER_TOKEN is now 2.3; the meter step moves to 43k tokens so it still speaks every ~100k characters. tidy.py is left for its own item (its 5K-token spec check would fire more often; Codex's bytes/4 rule must stay). budget.py keeps bytes/4 as its fixed unit.
- Limit: one maintainer's sessions, mostly English and code.

### T-20261116-9 · 2026-11-16 · transcript scan: tool results 5 before and 5 after each hook note, main sessions over 50 KB · Windows · study (hook value)
- Why: improvement study seed 5 (ledger g2c0e48). Does the agent change what it pulls into context after a meter or big-output note?
- Data: 613 sessions with hook notes, 1,400 without (control: the same event, a non-Read result of 20k+ chars or a 25k-token step, in sessions with no hook).
- Big-output note (n=437): share of the next 5 results at 20k+ chars 11.5% before, 12.6% after; median 2,158 to 1,131 chars. Control (n=129): 21.1% to 19.5%, median 695 to 678.
- Meter note (n=117): 24.4% to 23.2%, median 3,409 to 2,251. Control (n=2,546): 41.1% to 40.8%, median 2,947 to 2,736.
- Verdict: no measurable change in big pulls after either note. Medians fall after a note but the control falls too, and the big-pull share does not move. The notes have earned their keep as a study tool (sinks and bugs found), not as an in-session nudge. Not cut: hooks are opt-in and cheap; changing them is a stop point. Script kept out of the repo (it reads local transcripts).

### T-20261116-7 · 2026-11-16 · live probe in Claude Code (VS Code) plus unit test · Windows · bug found and fixed
- Why: gf6bd83, does the hook meter count subagent tool output?
- Probe: a subagent made one Grep (a tool the main session had not used). The main session's meter file gained a Grep entry of 975 chars, so subagent output was added to the main meter. Unit test test_meter_skips_subagent_tool_output failed first, passes after the fix (55 of 55).
- Live check owed: after installing 0.3.7, repeat the probe; the main meter must not change.

### T-20261116-6 · 2026-11-16 · hook start time, 7 runs each through Git Bash with a sample event · Windows · study
- Median wall time per call: finwright PreToolUse guard (Bash, PowerShell, MCP) 423 ms; tokenwright post 122 ms, pre 114 ms; quirkwright 90 ms; evergreen PostToolUse 62 ms; a bare `true` 32 ms (the spawn floor). finwright's guard is the outlier: about 390 ms over the floor on every shell or MCP call. Ledger item for a PR on finwright; tokenwright makes no change.

### T-20261116-5 · 2026-11-16 · transcript scan (400 newest main sessions over 50 KB plus 602 subagent transcripts) · Windows · study, no change
- Why: ga1faf8. Big output in calls 1-5 looked like state loading that a habit could cut.
- Result: 131 results of 20k chars or more in calls 1-5, about 787k tokens. Compound `cd && cat` of whole state markdown (HANDOFF, continue prompt, plan, SKILL.md) 51 calls, 306k; compound ranged reads (head, sed -n, tail) 40 calls, 235k; whole cats of other markdown 19 calls, 119k; the rest under 50k each. Only one call cat a whole log.md: tailing logs saves about 0.
- Use check: in 47 of 65 long cats the session later used at least three identifiers found only before the last 100 lines. The loads were mostly read for a reason, so "outline then range" would add calls more than it saves; the 318k upper bound (keep 25%) does not hold.
- Verdict: no new habit. Logs are already tailed and the loaded state is used. The cost lever lies with the docs being loaded (HANDOFF length, prompts that stack several files), which belongs to everlast and chainwright, not to tokenwright.

### T-20261116-4 · 2026-11-16 · claude plugin eval (scripts/ab_eval.py, 3 runs each arm, plugin vs stub) · WSL2 Ubuntu · no saving
- Why: gc83186. The history-free change-check case, so the stub arm cannot learn tw.py from a recorded turn 1. Case ab-regen-changed: regen.sh swaps a 1,500-line settings.py for a version with two settings changed; no git, no saved copy; the agent writes changes.txt.
- Result: both arms 3/3. With $0.120 mean (cache read 91.8k, output 210), stub $0.115 (92.4k, 113). Every run in both arms did the same three calls: `cp settings.py $TMPDIR/...`, run regen.sh, `diff`, then write the answer. No arm read the file whole or used tw.py changed.
- Verdict: ruled out as a saving over the bare model in a single turn. `tw.py changed` only pays when the snapshot must outlive the turn or the session (a file edited by someone else between sessions), which no eval has shown yet.
- Spend: about $0.70.

### T-20261116-2 · 2026-11-16 · claude plugin eval 2.1.316 (3 runs each arm, --ablation none twice: plugin vs a stub plugin with no skills or hooks, --keep-temp) · WSL2 Ubuntu · no saving
- Why: the history cases (multiturn-reread, multiturn-changed) were single-arm, so they had never been A/B tested. The stub copy (plugin.json with an empty skills folder and no hooks) gives them a without arm. Token counts come from each kept sandbox's out/trace.jsonl (message.usage), which fills the "cost only" gap of T-20261116-1.
- multiturn-reread: both arms 3/3, one Grep, about 64.8k cache read and 81k cache write a run, $0.171 with and $0.169 without. The bare model already answers from a targeted Grep and never re-reads the whole file.
- multiturn-changed: with 3/3, $0.211 mean, cache read 406k to 507k; stub 2/3 (one judge miss), $0.190 mean, cache read 201k to 347k. Both arms ran `tw.py changed` because the turn-1 history already shows it, so the stub is not a clean baseline. The with arm spent more: bare `python3 tw.py` fails, then two to five calls go to finding the script in the plugin folder.
- Verdict: no saving from re-read avoidance in either case. Two findings: history cases cannot A/B the plugin because the history teaches the behaviour; and finding tw.py costs extra calls when the model starts from a bare `tw.py`.
- Spend: about $2.3.

### T-20261116-1 · 2026-11-16 · claude plugin eval 2.1.316 (3 runs each arm, with-without, --scaffold, Bash Write Edit granted) · WSL2 Ubuntu, TMPDIR on ext4 · 1/1, no saving
- Why: the owed long-session A/B (L-004, improvement study seed 1). New case multiturn-long-job: five CI runs, each about 8,000 log lines over three files (build warnings and top code, failed tests, slowest probe), triaged one run at a time into report.csv. Six regex graders check the header and every row, so both arms are held to the same answer. Fixture generated by make_fixture.py; nothing large is tracked.
- With: pass 3/3 (score 1.00), turns 5, 4, 6 (mean 5.0), cost $0.169, $0.149, $0.176 (mean $0.165).
- Without: pass 3/3 (score 1.00), turns 6, 6, 5 (mean 5.7), cost $0.169, $0.173, $0.149 (mean $0.164).
- Tokens: the harness JSON and report give cost, turns and duration per run but no input, output or cache token counts, so cost stands in for tokens.
- Verdict: no difference. Both arms finish the 15 file steps in about five turns, which means bare Claude already batches the work into a few filtering commands and never pulls the long output into context. The "script repeats" and "trim long output" habits did not pay here because the baseline already does them. A saving would need a job a bare model handles wastefully: output it must read (not filter), or repeats spread over separate user turns.
- Spend: about $0.98.

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
