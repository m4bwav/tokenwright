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

## Open questions

- Batch API request cap: sources disagree (10k vs 100k).
- Programmatic tool calling's 37% figure: secondary sources only.
- Thresholds for "big output" (20k chars) and "whole read" (400 lines) need a baseline across many real transcripts.

## Search plan

- subject: Claude Code changelog and docs (costs, caching, context, skills, hooks), Anthropic API release notes.
- tooling: GitHub `path:SKILL.md token`, hooks and MCP servers that trim output, ccusage-style meters.
- practice: the everscout beat `token-saving` (Claude Code issues, r/ClaudeAI, r/ClaudeCode, Hacker News, OpenAI and Cursor forums).
- testing: published token measurements; claude plugin eval cost fields.
