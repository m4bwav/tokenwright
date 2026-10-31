# Claude Code and API levers

Checked 2026-10-30 against code.claude.com/docs and docs.claude.com. Sources and dates are in the repository's `ai-docs/research/2026-10-30-token-saving-survey-web.md`. Version-specific numbers drift: re-check on refresh.

## The prompt cache decides most of the bill

- Each request re-sends the whole context. The cache matches the start of the request exactly, and a hit is billed at about a tenth of input (a twentieth on Opus and Sonnet 5.5).
- Things that break the cache, so the next turn pays full price for everything: switching model, toggling fast mode, connecting MCP servers or plugins whose tools load up front, compacting, upgrading Claude Code, and a skill whose frontmatter names another model. Changing effort keeps the cache on the 5.5 models and Fable 5.1 but breaks it on most others.
- TTL: a subscription within plan usage gets 1 hour for the main conversation; subagents, forks, compaction, API keys and usage credits get 5 minutes. Settable with `CLAUDE_CODE_PROMPT_CACHE_TTL` and `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`.
- Habit: settle model, tools and plugins before a long task; don't switch mid-task.

## Rank the fix (leverage)

- Weakest to strongest (after Meadows ch. 6): a setting or cap; a shorter delay; what the agent can see (a meter, `/context`, a short output); a rule (a hook, a script); the goal (what counts as done).
- A cap stops a disaster and changes no habit. Prefer the highest rung the task allows.
- A hook that only blocks gets worked around at the same cost (a blocked Read becomes `cat` through Bash). A hook should name the cheap route.

## Context commands

- `/clear` between unrelated tasks: free, and the biggest single saving.
- `/compact` (with a focus line) is cheap while the cache is warm, expensive after an idle break.
- `/rewind` returns to a prefix that is already cached: better than compacting away a dead end.
- `/context` shows what fills the window; `/cost` and the status line show spend.

## What loads when

- CLAUDE.md and AGENTS.md: every turn. Keep under about 200 lines; move workflows into skills.
- Skill descriptions: every turn, cut at 1,536 characters. The body loads on invoke; files beside it only when read. `disable-model-invocation: true` removes the description entirely (slash command only).
- MCP tool schemas: deferred behind tool search when enabled; otherwise every turn. A CLI the agent already knows costs nothing until used, so prefer CLIs where one exists.
- Subagents and `context: fork` skills: their reads stay in their own context; only the result returns. Give simple ones Haiku.

## Output caps

- Bash output is capped at 30,000 characters (`BASH_MAX_OUTPUT_LENGTH`), file reads at about 25k tokens, MCP output at 25k (`MAX_MCP_OUTPUT_TOKENS`, warning at 10k). Caps stop disasters; they do not make 29,000 characters cheap.
- A PreToolUse hook can rewrite noisy commands (the docs' example shows only failing tests). tokenwright's own hooks warn instead.

## API side

- Cache writes cost 1.25x input (5 minutes) or 2x (1 hour); reads 0.1x. Minimum cacheable prefix is 512 tokens on 5.x models; shorter prompts silently skip caching. Put stable text first and the breakpoint after it.
- Message Batches: 50% off for work that can wait.
- Token counting endpoint: free; use it to measure before and after.
- Context editing (tool result clearing) and the memory tool: Anthropic reports 84% fewer tokens on a 100-turn search eval (their own figure). Tool search cut definition tokens about 85% (their own figure).
- Smaller models for mechanical steps: Haiku or a local model for extraction, classification and summaries.

## Popular add-ons, measured by others

An independent test reported "caveman" style output compression saving about 8.5% (claimed 65%), and another found it no better than asking for brief answers. Treat claims of large savings from output-style tools with suspicion; measure with `tw.py score` on your own sessions.

## Recent changes (from the beat)

- Claude Code 2.1.311: sessions past 200k tokens compact and continue instead of stopping; CLAUDE.md is re-read after auto-compaction (github.com/anthropics/claude-code/releases/tag/v2.1.311).
- Read shows only about the first 37k characters of a very long single-line tool result (community report): don't rely on a huge one-line JSON reaching the model whole.
- Unconfirmed: a report of session caches invalidating about every 10 minutes. Watch `cache_creation_input_tokens` in `tw.py score --json` if a session feels expensive.
