# Research: tokenwright

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); lessons in [LEARNINGS.md](LEARNINGS.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Protocol: MAINTENANCE.md.

Topic: ways an AI agent spends fewer tokens on the same result: Claude Code and API cost levers, context loading habits, scripting repeated work, skill token cost. Tier `fast`. Last refresh 2026-10-30; next due 2026-11-13.

## Current understanding

- The prompt cache decides most of the bill in long sessions: every token in context is re-read each turn, at about a tenth of input price (R-20261030-1). Early waste costs most.
- Cache breaks (model switch, fast mode toggle, MCP or plugin connect, compaction, upgrades) make the next turn pay full price for everything (R-20261030-1).
- `/clear` between unrelated tasks is free and the largest single saving; `/rewind` beats compacting a dead end (R-20261030-2).
- Skill descriptions load every turn and are cut at 1,536 characters; bodies on invoke; files on read (R-20261030-3).
- Output-style compression tools save far less than claimed in independent tests (about 8.5% against 65% claimed) (R-20261030-4).
- No published before-and-after numbers exist for search-then-range reads or compaction; this plugin's evals measure them (R-20261030-5).

## Findings

### R-20261030-1 · subject · magnitude n/a (creation)
Cache matching, TTLs (1 h main conversation on a subscription, 5 min for subagents and API keys), what breaks the cache. Sources: code.claude.com/docs (costs, prompt caching pages), checked 2026-10-30. Detail: repository ai-docs/research/2026-10-30-token-saving-survey-web.md.

### R-20261030-2 · practice · magnitude n/a
/clear, /compact, /rewind trade-offs. Same sources.

### R-20261030-3 · tooling · magnitude n/a
Skill loading tiers and the description cut. code.claude.com/docs skills page, checked 2026-10-30.

### R-20261030-4 · practice · magnitude n/a
Independent test of caveman, rtk and Ponytail (secondary write-up of a JetBrains test; original not found).

### R-20261030-5 · testing · magnitude n/a
No published measurements for the basic read habits.

### R-20261030-6 · practice · magnitude 0.3
First scan of the everscout beat token-saving (16 sources, 194 items, 9 notes): model routing with a test gate, effort per task, lean headless runs, templates for deterministic output, MCP vs skill cost, loop-guard hooks. Single-author reports. Links in references/habits.md.

### R-20261030-7 · practice · magnitude 0.2
Hunt and Thomas, *The Pragmatic Programmer* 20th anniversary ed. (Topics 12, 20, 27, 38) and Christian and Griffiths, *Algorithms to Live By* (ch. 1, 2, 4, 9, 10): stopping rules, bisection, debugging discipline, backoff, local peaks. Paraphrased in the book-learnings notes, not in this repository.

### R-20261030-8 · practice · magnitude 0.2
Meadows, *Thinking in Systems* (ch. 2, 4, 5, 6): delays and oscillation, bounded rationality, system traps, leverage points. Paraphrased in the book-learnings notes, not in this repository.

### R-20261030-9 · testing · magnitude 0.1
Baseline across 300 recent Claude Code transcripts (12,928 tool results, 256 whole-file reads), measured 2026-10-30. Text tool results: median 311 chars, p95 7,763, p99 18,067, p99.9 40,337; 0.8% are 20k or more, and 68 of 300 sessions have at least one. Whole reads: median 66 lines, p90 288, p95 392, p99 591; 4.7% are 400 lines or more, in 12 sessions. Both lines sit near the tail (p99 and p95), so `BIG_OUTPUT_CHARS = 20000` and `BIG_FILE_LINES = 400` stay. Counting image blocks as text inflates output sizes about sevenfold; measure text only. Source: local transcripts, one maintainer's work, not a population.

### R-20261030-10 · testing · magnitude 0.1
Exact repeats of a shell command across the same 300 local transcripts, measured 2026-10-30: 9,088 commands ran once, 351 twice, 5 three times, 2 four times; none more. The most repeated command per session has median 1, p95 2, p99 3; 7 sessions reach 3. So `POLL_RUNS = 3` flags about the top 2% of sessions. Polling here mostly runs through background loops and Monitor, which do not repeat the command in the transcript, so the kind catches hand polling only. Source: local transcripts, one maintainer's work.

### R-20261031-1 · testing · magnitude 0.1
Failed tool calls across the same 300 local transcripts, measured 2026-10-31: errors per session median 0, p95 6, p99 12, max 16. The longest run of failed calls in a row to one tool per session: 0 in 162 sessions, 1 in 124, 2 in 11, 3, 4 and 6 in one each. So `DEBUG_LOOP_ERRORS = 3` flags about the top 1% of sessions. Errors are mostly isolated; a streak of three is rare enough to be worth a look. Source: local transcripts, one maintainer's work.

### R-20261031-2 · testing · magnitude 0.1
Denied calls across the same 300 local transcripts, measured 2026-10-31: 26 denials (auto-mode classifier 15, built-in safety check 4, a guard hook 2, user rejections the rest) in 8 sessions; at most 2 per session. After 24 of 26 the next call was the same tool, mostly the same command split or narrowed, which is the right response to a classifier denial; true workarounds (for example `rm -rf` denied, then `rmdir`) look the same and cannot be told apart from the call alone. So a `workaround-after-deny` score kind was not added: too rare to matter for tokens and no mechanical signal for "same end". The concern stays a habit (judgement), not a tw.py check. Source: local transcripts, one maintainer's work.

### R-20261031-3 · testing · magnitude 0.1
A `plateau` scan across the same 300 local transcripts, measured 2026-10-31: the same shell command failing again after an edit, with no pass between. Longest such run per session: 0 in 176 sessions, 1 in 121, 2 in 3, never 3. So a `plateau` score kind at three runs would never fire; not added. Two variations then a step back stays a habit row; `debug-loop` and `retry` already catch the failure streaks that do occur. Source: local transcripts, one maintainer's work.

### R-20261031-4 · testing · magnitude 0.1
A `many-similar-edits` scan across the same 300 transcripts, measured 2026-10-31: Edit calls with the same old and new text grouped by file. No session has the same edit in two files (109 sessions edit at all). Bulk changes already go through scripts, so the kind was not added. Source: local transcripts, one maintainer's work.

## Open questions

- Batch API request cap: sources disagree (10k vs 100k).
- Programmatic tool calling's 37% figure: secondary sources only.
- Thresholds checked against one maintainer's 300 transcripts (R-20261030-9); a second user's baseline would show whether they generalise.

## Search plan

- subject: Claude Code changelog and docs (costs, caching, context, skills, hooks), Anthropic API release notes.
- tooling: GitHub `path:SKILL.md token`, hooks and MCP servers that trim output, ccusage-style meters.
- practice: the everscout beat `token-saving` (Claude Code issues, r/ClaudeAI, r/ClaudeCode, Hacker News, OpenAI and Cursor forums).
- testing: published token measurements; claude plugin eval cost fields.
