# Claude Code and API levers

Checked 2026-11-15 against code.claude.com/docs and platform.claude.com/docs. Sources and dates: [RESEARCH.md](../RESEARCH.md). Version-specific numbers drift: re-check on refresh.

## The prompt cache decides most of the bill

- Each request re-sends the whole context. The cache matches the start of the request exactly, and a hit is billed at 0.1x input or less (0.05x on Opus and Sonnet 5.5, 0.025x on Fable 5.1 and 5.2).
- Cache breaks, after which the next turn pays full price for everything: switching model, toggling fast mode, connecting MCP servers or plugins whose tools load up front, compacting, upgrading Claude Code, a skill whose frontmatter names another model, and old images dropped once a request holds too many. Changing effort keeps the cache on the 5.5 models and Fable 5.1 but breaks it on most others.
- TTL: a subscription within plan usage gets 1 hour for the main conversation; subagents, forks, compaction, API keys and usage credits get 5 minutes. Settable with `CLAUDE_CODE_PROMPT_CACHE_TTL` and `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`. On the 1-hour TTL a long idle conversation may be compacted (`idleCompaction: false` stops it).
- Habit: settle model, tools and plugins before a long task.

## Rank the fix (leverage)

- Weakest to strongest (after Meadows ch. 6): a setting or cap; a shorter delay; what the agent can see (a meter, `/context`, a short output); a rule (a hook, a script); the goal (what counts as done).
- A cap stops a disaster but changes no habit. Prefer the highest rung the task allows.
- A hook that only blocks gets worked around at the same cost (a blocked Read becomes `cat`). A hook should name the cheap route.

## Context commands

- `/clear` between unrelated tasks: free, and the biggest single saving.
- `/compact` (with a focus line) is cheap while the cache is warm, expensive after an idle break.
- `/rewind` returns to a prefix that is already cached: better than compacting away a dead end.
- `/context` shows what fills the window. `/usage` shows spend, the cache hit share with the likely cause of the last miss, and each skill's, subagent's and MCP server's share.

## What loads when

- CLAUDE.md and AGENTS.md: every turn. Under about 200 lines; workflows go in skills.
- Skill descriptions: every turn, cut at 1,536 characters. The body loads on invoke; files beside it only when read. `disable-model-invocation: true` removes the description entirely (slash command only).
- MCP tool schemas: deferred behind tool search when enabled; otherwise every turn. A CLI the agent already knows costs nothing until used, so prefer CLIs where one exists.
- Fewer tools in view: disable MCP servers and plugins a task does not use; each loaded definition costs every turn, and more tools mean more wrong picks (Berryman and Ziegler, Prompt Engineering for LLMs ch. 8). Too big even for an outline: summarize files, then folders from those summaries (ch. 5).
- `@file` mentions: the whole file (to the Read cap) plus its directory's CLAUDE.md files, with no tool call, so PreToolUse hooks never see it. `CLAUDE_CODE_DISABLE_FILE_MENTIONS=1` passes only paths. VS Code attaches the selection and names the open file; both can be turned off.
- Subagents and `context: fork` skills: their reads stay in their own context; only the result returns. Give simple ones Haiku. See Subagents below for when they pay.

## Subagents: a smaller main context, a bigger bill

- They move tokens, not remove them. Anthropic measured single agents at about 4x the tokens of chat, multi-agent research about 15x, Claude Code agent teams about 7x a normal session; all count toward the same limits (R-20261031-10).
- Each one pays a cold start: its own system prompt, tools and CLAUDE.md, and its first request misses the parent's cache. A fork reuses the parent's prefix and hits the cache. Subagents get a 5-minute cache TTL even on a subscription (`CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` overrides). `CLAUDE_CODE_DISABLE_AGENT_PROGRESS_SUMMARIES=1` drops the extra requests that write their progress summaries.
- They pay on verbose, independent, read-heavy work whose answer is small: test runs, log reads, doc fetches, many-file sweeps, a review not anchored on your reasoning. The main context keeps a 1,000 to 2,000 token conclusion instead of a 50k-token sweep, and a smaller context answers better (context rot, R-20261031-10).
- They lose on small lookups (a known file, one grep), on coupled sequential work (plan, implement, test share context), on frequent back-and-forth, and when parallel agents must decide consistently. Re-reading what the subagent read pays twice.
- Brief like a peer: objective, what is ruled out, output format and a length cap. For big results have it write a file and return the path.
- Briefing a reasoning model or a high-effort agent: leave out step-by-step instructions, a role and requests to show its reasoning. It plans on its own, and forced paths or roles cost tokens and can lower quality (Koch et al., Prompt Engineering in the Enterprise, sec. 6.4). Name the assumptions already ruled out instead.
- Cheaper first: a script or hook that filters output (a 10k-line log to a few hundred tokens) costs no second model. For cheap sweeps, override the built-in Explore with a `model: haiku` agent of the same name.
- No public size threshold exists; check with `/usage` (per-subagent share) or `tw.py score` before and after.

## Output caps

- Bash output is capped at 30,000 characters (`BASH_MAX_OUTPUT_LENGTH`, at most 150,000), file reads at 25k tokens, MCP output at 25k tokens (`MAX_MCP_OUTPUT_TOKENS`, warning at 10k; text past 50,000 characters goes to a file). Caps stop disasters; they do not make 29,000 characters cheap.
- A PreToolUse hook can rewrite noisy commands (the docs' example keeps the last 100 lines of test output). tokenwright's own hooks warn instead.

## Format and lint in a hook, failures only

- A PostToolUse hook on `Edit|Write` runs the formatter (the docs' example: `jq -r '.tool_input.file_path' | xargs npx prettier --write`), so the model never writes or re-reads formatting fixes.
- Lint the same way: exit 0 when clean (PostToolUse stdout on exit 0 never reaches the model), exit 2 with only the failures on stderr. `additionalContext` past 10,000 characters is saved to a file and the model sees a 2,000-character preview.
- Scope it to the edited file; a whole-repo lint on every edit costs wall time.
- Typed languages: a code intelligence (LSP) plugin turns grep-then-read-candidates into one go-to-definition call.

## API side

- Cache writes cost 1.25x input (5 minutes) or 2x (1 hour); reads 0.1x or less. Minimum cacheable prefix is 512 tokens on current models (1,024 on Sonnet 5); shorter prompts silently skip caching. Put stable text first and the breakpoint after it.
- Message Batches: 50% off for work that can wait.
- Token counting endpoint: free; use it to measure before and after.
- Context editing (tool result clearing) and the memory tool: Anthropic reports 84% fewer tokens on a 100-turn search eval (their own figure). Tool search cut definition tokens about 85% (their own figure).
- Smaller models for mechanical steps: Haiku or a local model for extraction, classification and summaries.
- A per-request model router can lose the prompt cache: a hit needs the same model on consecutive requests (Microsoft Foundry Model Router docs, read 2026-11-05; session affinity helps but guarantees no hit). Route per task or session, and weigh the savings against the misses.

## Search, not retrieval, for code

- Claude Code dropped an early RAG design for agentic search (grep, glob, reads), reportedly for simplicity, freshness and privacy (secondary source, R-20261101-1). For code, a CODEMAP and search beat a chunking pipeline; RAG fits big document sets outside the repository.
- When a tool must retrieve (an MCP search tool, docs RAG), return the top few reranked results, not every match: extra chunks cost tokens, and models attend most to the first and last pieces. Search small, read wide only around hits; grep then a ranged read is the agent form (Iusztin and Labonne, LLM Engineer's Handbook, sec. 97 and 219).
- Before paying for a summary of long text, try selecting: keep the sentences most relevant to the question and least like those already kept (MMR), and stop at a word budget. No model call, original wording (Zhai and Massung, Text Data Management and Analysis, sec. 16.2). Unmeasured here.
- Before retrieved text enters the context, drop copies and off-topic passages, and reuse what an earlier turn returned instead of searching again. For a whole-corpus question, answer from a summary or graph index (a CODEMAP) and drill down only where it points (Wei and Wu, Advanced Retrieval-Augmented Generation, sec. 3.3, 4.4, 7.2).

## Result caching

- Cache expensive tool results (web fetches, searches, slow commands) by an exact hash of the input, with an expiry; a repeat costs nothing.
- Avoid semantic caching (reuse for a similar input) unless a measured hit rate justifies its tuning and false hits (Huyen, AI Engineering ch. 10).

## Popular add-ons, measured by others

An independent test reported "caveman" style output compression saving about 8.5% (claimed 65%), and another found it no better than asking for brief answers. Doubt large claims for output-style tools; measure with `tw.py score`.

## Recent changes (from the beat)

- Claude Code 2.1.311: sessions past 200k tokens compact and continue instead of stopping; CLAUDE.md is re-read after auto-compaction.
- Read shows only about the first 37k characters of a very long one-line tool result (community report): a huge one-line JSON may not reach the model whole.
- 2.1.321: background command output over 1,000 characters reaches the model as its start and end only.
- A session that feels expensive: read the cache line in `/usage`, or `cache_creation_input_tokens` in `tw.py score --json`.
