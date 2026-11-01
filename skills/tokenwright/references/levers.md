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
- Subagents and `context: fork` skills: their reads stay in their own context; only the result returns. Give simple ones Haiku. See Subagents below for when they pay.

## Subagents: a smaller main context, a bigger bill

- They move tokens, they do not remove them. Anthropic measured single agents at about 4x the tokens of chat and multi-agent research at about 15x; Claude Code agent teams at about 7x a normal session. Subagent requests count toward the same usage limits (R-20261031-10).
- Each one pays a cold start: its own system prompt, tools and CLAUDE.md, and its first request misses the parent's cache. A fork reuses the parent's prefix and hits the cache. Subagents get a 5-minute cache TTL even on a subscription (`CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` overrides).
- They pay on verbose, independent, read-heavy work whose answer is small: test runs, log reads, doc fetches, many-file sweeps, a review that should not be anchored on your reasoning. The main context keeps the 1,000 to 2,000 token conclusion instead of the 50k-token sweep, and a smaller context also answers better (context rot, R-20261031-10).
- They lose on small lookups (a known file, one grep), on tightly coupled sequential work (plan, implement, test share context), on frequent back-and-forth, and when parallel agents must make consistent decisions. If you will re-read what the subagent read to check it, you paid twice.
- Brief like a peer: objective, what is ruled out, output format and a length cap. For big results have it write a file and return the path. Many detailed returns still fill the main context.
- Cheaper alternatives first: a script or hook that filters output (a 10k-line log to a few hundred tokens) costs no second model. Override the built-in Explore with a `model: haiku` agent of the same name for cheap sweeps.
- No public size threshold exists; check with `/usage` (per-subagent share) or `tw.py score` before and after.

## Output caps

- Bash output is capped at 30,000 characters (`BASH_MAX_OUTPUT_LENGTH`), file reads at about 25k tokens, MCP output at 25k (`MAX_MCP_OUTPUT_TOKENS`, warning at 10k). Caps stop disasters; they do not make 29,000 characters cheap.
- A PreToolUse hook can rewrite noisy commands (the docs' example shows only failing tests). tokenwright's own hooks warn instead.

## API side

- Cache writes cost 1.25x input (5 minutes) or 2x (1 hour); reads 0.1x. Minimum cacheable prefix is 512 tokens on 5.x models; shorter prompts silently skip caching. Put stable text first and the breakpoint after it.
- Message Batches: 50% off for work that can wait.
- Token counting endpoint: free; use it to measure before and after.
- Context editing (tool result clearing) and the memory tool: Anthropic reports 84% fewer tokens on a 100-turn search eval (their own figure). Tool search cut definition tokens about 85% (their own figure).
- Smaller models for mechanical steps: Haiku or a local model for extraction, classification and summaries.

## Result caching

- Cache expensive tool results (web fetches, searches, slow commands) by an exact hash of the input, with an expiry; a repeat costs nothing.
- Avoid semantic caching (reuse for a similar input) unless a measured hit rate justifies tuning the similarity threshold and the false hits it brings (Huyen, AI Engineering ch. 10).

## Popular add-ons, measured by others

An independent test reported "caveman" style output compression saving about 8.5% (claimed 65%), and another found it no better than asking for brief answers. Treat claims of large savings from output-style tools with suspicion; measure with `tw.py score` on your own sessions.

## Recent changes (from the beat)

- Claude Code 2.1.311: sessions past 200k tokens compact and continue instead of stopping; CLAUDE.md is re-read after auto-compaction (github.com/anthropics/claude-code/releases/tag/v2.1.311).
- Read shows only about the first 37k characters of a very long single-line tool result (community report): don't rely on a huge one-line JSON reaching the model whole.
- Unconfirmed: a report of session caches invalidating about every 10 minutes. Watch `cache_creation_input_tokens` in `tw.py score --json` if a session feels expensive.
