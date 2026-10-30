# Token-saving survey (web), 2026-10-30

Feeds the tokenwright plugin. Every line is "claim, source (checked 2026-10-30)".
Vendor docs are primary. Community numbers are marked as claims or secondhand.

## 1. Claude Code levers (official docs)

### Prompt caching and TTL
- Claude Code re-sends the whole context every turn. Caching bills the unchanged prefix at the cached rate. The match is an exact prefix, with no per-file caching. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- Request layers in order: system prompt plus tools, then project context (CLAUDE.md, memory), then conversation. A change in an early layer recomputes everything after it. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- Things that break the cache: switching model, changing effort (on most models), toggling fast mode, connecting or removing MCP servers when tools are not deferred, denying a whole tool without tool search, compaction, dropping old images, upgrading Claude Code. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- Things that keep the cache: editing repo files, editing CLAUDE.md mid-session (the edit only applies after /clear, /compact or a restart), changing permission mode, changing output style, invoking skills, /recap, /rewind, spawning a subagent. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- On Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1 with an API key or a subscription, changing effort keeps the cache. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- A skill or command whose frontmatter names another model is a model switch for that turn, so it misses the cache. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- Default TTL: one hour for the main conversation on a subscription within plan usage. Five minutes for subagents, forks, compaction and everything else, and for API keys, cloud providers and usage credits. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- Set the TTL with `promptCacheTtl` or `CLAUDE_CODE_PROMPT_CACHE_TTL` (main), and `subagentPromptCacheTtl` or `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` (others). Values are `5m` or `1h`. Needs v2.1.242 or later. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- One hour pays off when you idle past five minutes. It costs more on short bursts that never idle. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- A fork inherits the parent prefix and reads its cache. A fresh subagent builds its own cache from scratch. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- The cache is scoped to one machine and directory. Parallel sessions in the same directory can share it. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- `/usage` shows a "Prompt cache (main)" line with hit share, misses and likely cause of the last miss (v2.1.251+, cause v2.1.260+). https://code.claude.com/docs/en/costs (checked 2026-10-30)

### Compaction, /clear, /rewind, /context
- `/compact` sends a summarization request over the whole history. With a warm cache it costs a fraction of the context size. After a break past the TTL it reprocesses everything uncached. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- Run `/compact` at natural breaks, not mid-task. Use `/rewind` to abandon a path, since it lands on an already cached prefix. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- `/clear` costs nothing and is the advice for unrelated work. `/compact Focus on ...` steers what survives. A "Compact instructions" section in CLAUDE.md does the same. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Idle compaction can run on the one-hour TTL. Turn it off with `idleCompaction: false` (v2.1.290+). https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` can only lower the auto-compact threshold. `CLAUDE_CODE_AUTO_COMPACT_WINDOW` sets the window from 100k to 1M tokens. https://code.claude.com/docs/en/env-vars (checked 2026-10-30)
- Run `/context` to see what is using space. https://code.claude.com/docs/en/costs (checked 2026-10-30)

### Usage display
- `/usage` shows session cost at list price, tokens by model, cache reads and writes. Totals reset on `/clear` since v2.1.211. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- On plans, `/usage` attributes usage to skills, subagents, plugins and MCP servers, and lists recommendations at 10%+ share (for example "Trim CLAUDE.md, 49k tokens per request"). Press `f` to apply some (v2.1.305+). https://code.claude.com/docs/en/costs (checked 2026-10-30)
- The status line can show cost and a `prompt_cache` object. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- The spinner token count is output of the current turn only, not context size. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Enterprise average is about $13 per developer per active day, $150 to $250 a month, and under $30 a day for 90% of users. https://code.claude.com/docs/en/costs (checked 2026-10-30)

### Deferred tools and MCP
- MCP tool definitions are deferred by default. Only names and server instructions load until a tool is used. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- `ENABLE_TOOL_SEARCH`: unset or true defers MCP tools. `auto` turns search on once definitions reach 10% of context. https://code.claude.com/docs/en/env-vars (checked 2026-10-30)
- CLI tools like `gh` or `aws` are still cheaper than MCP servers because they add no tool listing. Disable unused servers in `/mcp`. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` caps tool descriptions at 4096 chars (16384 for searched tools). https://code.claude.com/docs/en/env-vars (checked 2026-10-30)

### Skills (progressive disclosure)
- Description (name, description, when_to_use) loads every turn, cut at 1,536 characters. Body loads on invoke and stays. Supporting files load only when read. Scripts run without loading. https://code.claude.com/docs/en/skills (checked 2026-10-30)
- `disable-model-invocation: true` removes the description from context entirely. https://code.claude.com/docs/en/skills (checked 2026-10-30)
- `context: fork` runs the body in a subagent and returns only the result. With `agent: Explore` it also skips CLAUDE.md. https://code.claude.com/docs/en/skills (checked 2026-10-30)
- Keep SKILL.md under 500 lines. Re-invoking an unchanged skill adds only an "already loaded" note. After compaction each recent skill keeps its first 5,000 tokens, 25,000 total. https://code.claude.com/docs/en/skills (checked 2026-10-30)
- Move workflow detail out of CLAUDE.md into skills. Keep CLAUDE.md under 200 lines. https://code.claude.com/docs/en/costs (checked 2026-10-30)

### Subagents, forks, teams
- Delegate tests, docs fetches and log reading to subagents. The verbose output stays there and only a summary returns. Their tokens still count. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Set `model: haiku` for simple subagents. `CLAUDE_CODE_SUBAGENT_MODEL` sets the default subagent model. https://code.claude.com/docs/en/costs and https://code.claude.com/docs/en/env-vars (checked 2026-10-30)
- Agent teams use about 7x more tokens than a standard session when teammates run in plan mode. https://code.claude.com/docs/en/costs (checked 2026-10-30)

### Effort and model choice
- Thinking is billed as output. Lower effort with `/effort` for simple work. Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable models cannot turn thinking off. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Sonnet handles most coding. Reserve Opus for architecture and multi-step reasoning. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- `opusplan` switches model on each plan-mode toggle, which restarts the cache. https://code.claude.com/docs/en/prompt-caching (checked 2026-10-30)

### Hooks and output limits
- A PreToolUse hook can rewrite a Bash command, for example to pipe test output through `grep FAIL | head -100`. A log grep hook can cut tens of thousands of tokens to hundreds. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- `BASH_MAX_OUTPUT_LENGTH` defaults to 30,000 characters (max 150,000). The `bashOutputMaxChars` setting overrides it. https://code.claude.com/docs/en/env-vars (checked 2026-10-30)
- `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` defaults to 25,000 tokens per read. https://code.claude.com/docs/en/env-vars (checked 2026-10-30)
- `MAX_MCP_OUTPUT_TOKENS` defaults to 25,000, with a warning above 10,000. https://code.claude.com/docs/en/env-vars (checked 2026-10-30)
- `CLAUDE_CODE_MAX_OUTPUT_TOKENS`: higher values shrink room before auto-compaction. https://code.claude.com/docs/en/env-vars (checked 2026-10-30)
- `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` defaults to 200. https://code.claude.com/docs/en/env-vars (checked 2026-10-30)

### Other habits from the cost page
- Code intelligence (LSP) plugins: one go-to-definition replaces a grep plus several candidate reads. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Specific prompts beat vague ones that trigger broad scanning. Plan mode, early Escape and incremental tests avoid wasted paths. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Hidden background spend: loops, scheduled tasks, cross-session messages, goal check-ins and prompt suggestions each resend context. https://code.claude.com/docs/en/costs (checked 2026-10-30)

## 2. Anthropic API side

- Cache multipliers on base input: 5-minute write 1.25x, 1-hour write 2x, read 0.1x. Reads are 0.05x on Opus 5.5 and Sonnet 5.5, 0.025x on Fable 5.1 and Mythos 5.1. https://platform.claude.com/docs/en/build-with-claude/prompt-caching (checked 2026-10-30)
- Up to 4 explicit breakpoints. Lookback is 20 blocks per breakpoint. Minimum cacheable length is 512 tokens on current 5.x models, 1,024 to 4,096 on older ones. Short prompts silently skip caching. https://platform.claude.com/docs/en/build-with-claude/prompt-caching (checked 2026-10-30)
- Hierarchy is tools, then system, then messages. Timestamps in the prefix and unstable JSON key order break hits. https://platform.claude.com/docs/en/build-with-claude/prompt-caching (checked 2026-10-30)
- Message Batches cost 50% of standard rates and finish within 24 hours, most in under an hour (secondary sources; caps of 10k and 100k requests conflict). https://anthropic.com/news/message-batches-api and https://dev.to/gabrielanhaia/anthropic-message-batching-when-50-off-is-worth-the-latency-4jfc (checked 2026-10-30)
- Token counting is free, with its own rate limits separate from message creation. https://platform.claude.com/docs/en/build-with-claude/token-counting (checked 2026-10-30)
- Context editing (beta header `context-management-2025-06-27`): `clear_tool_uses_20250919` clears oldest tool results. Defaults: trigger 100k input tokens, keep 3 tool uses. `clear_at_least` makes sure a clear is worth the cache rewrite. `clear_thinking_20251015` handles old thinking. https://platform.claude.com/docs/en/build-with-claude/context-editing (checked 2026-10-30)
- Server-side compaction is the docs' primary strategy for long conversations. Client-side `compaction_control` is deprecated. https://platform.claude.com/docs/en/build-with-claude/context-editing (checked 2026-10-30)
- Memory tool (`memory_20250818`) pairs with context editing: Claude gets a warning to save notes before results are cleared. https://platform.claude.com/docs/en/build-with-claude/context-editing (checked 2026-10-30)
- Anthropic reports context editing cut tokens 84% in a 100-turn web search eval. Memory plus context editing improved agentic search 39% over baseline, context editing alone 29%. Internal numbers. https://www.anthropic.com/news/context-management (checked 2026-10-30)
- Tool Search Tool: about 85% fewer tokens for tool definitions (secondhand: about 77k to 8.7k). Accuracy rose on Opus 4.5 from 79.5% to 88.1%. https://www.anthropic.com/engineering/advanced-tool-use (checked 2026-10-30)
- Programmatic tool calling keeps intermediate results out of context. A 37% reduction is cited only in a secondary source. https://www.anthropic.com/engineering/advanced-tool-use (checked 2026-10-30, figure unverified)
- Smaller models for mechanical steps: Haiku for simple subagents is the official advice. https://code.claude.com/docs/en/costs (checked 2026-10-30)

## 3. Other agents and community tools

### Other agents
- Aider sends a repo map of files, key symbols and definition lines. Default budget is `--map-tokens` 1k, and it grows when no files are in chat. It ranks a dependency graph to fit the budget. https://aider.chat/docs/repomap.html (checked 2026-10-30)
- The ranking uses tree-sitter tags and PageRank weighted toward identifiers in chat, fitted by binary search. Aider never isolated the map's benefit in an ablation. https://agentpatterns.ai/context-engineering/repository-map-pattern/ (checked 2026-10-30)
- Codex CLI reads AGENTS.md down the tree with a size cap `project_doc_max_bytes` (third-party guide). https://codex.danielvaughan.com/2026/06/15/agents-md-beyond-init-writing-project-instructions-that-reduce-token-spend-hooks-mcp-skills/ (checked 2026-10-30, unverified against OpenAI docs)
- A cited Princeton study says a good AGENTS.md cut Codex output tokens 16.6% and runtime 28.6% (secondhand). Same source as above (checked 2026-10-30)
- Cursor agent mode reads AGENTS.md and `.cursor/rules/*.mdc`; glob-scoped rules load only for matching files, which saves tokens over always-on rules. https://thepromptshelf.dev/blog/agents-md-vs-cursor-project-rules-2026/ (checked 2026-10-30)
- Copilot guidance treats always-on instruction files as a cost and argues for short ones; no official token budget found. https://olivomarco.github.io/github-copilot-token-optimization/07-agents-md-problem/ (checked 2026-10-30)

### Community tools
- ccusage reads Claude Code's local JSONL logs and reports spend by day, session and project. Guides say measure a baseline first. https://computingforgeeks.com/reduce-claude-code-token-usage-tools/ (checked 2026-10-30)
- caveman compresses output style. Authors now claim 65% of output tokens (down from 75%). https://pasqualepillitteri.it/en/news/7881/caveman-rtk-pxpipe-headroom-claude-code-tokens (checked 2026-10-30)
- rtk rewrites Bash output via a hook. Claims 60 to 90%, example 118k to 23.9k. It only covers Bash, not Read, Grep or Glob. Same source (checked 2026-10-30)
- headroom compresses at the API proxy, claims 15 to 20% on coding agents. pxpipe renders context as images, claims 59 to 70%, but is not byte-exact and can confabulate IDs. Same source (checked 2026-10-30)
- Ponytail (YAGNI ladder skill) claims 54% less code and 22% fewer tokens on one repo. Same source (checked 2026-10-30)
- Independent test (JetBrains, via secondary write-up): caveman saved about 8.5% not 65%, rtk saved about nothing and sometimes cost more at low effort, Ponytail saved about 10%. https://www.mindstudio.ai/blog/claude-token-saving-plugins-tested/ (checked 2026-10-30; original report not located)
- Another benchmark found caveman similar to just asking "be brief". https://computingforgeeks.com/reduce-claude-code-token-usage-tools/ (checked 2026-10-30)
- Serena is an LSP-backed MCP server returning symbols rather than whole files. No measured figure found. Same source (checked 2026-10-30)
- Repomix and code2prompt pack a repo into one prompt. They help chat UIs but run against the agent habit of reading less. No measurement found (searched 2026-10-30).

## 4. Published measurements

- Context editing: 84% fewer tokens over 100 turns (Anthropic internal). https://www.anthropic.com/news/context-management (checked 2026-10-30)
- Tool search: 85% fewer definition tokens. https://www.anthropic.com/engineering/advanced-tool-use (checked 2026-10-30)
- Multi-agent systems use about 15x the tokens of chat (secondhand from Anthropic's research system post). https://www.zivtech.com/blog/economics-of-claude-code-part-2-agent-tradeoff (checked 2026-10-30)
- Agent teams in plan mode: about 7x. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Exploration in a subagent versus the parent: one author claims 75x less parent context weight. Unverified. https://www.zivtech.com/blog/economics-of-claude-code-part-2-agent-tradeoff (checked 2026-10-30)
- Grep plus ranged read versus full read: no published before/after found. The docs' log-grep hook example (tens of thousands to hundreds) is the closest. https://code.claude.com/docs/en/costs (checked 2026-10-30)
- Compaction: no public before/after numbers beyond the docs' qualitative description. (searched 2026-10-30)

## Ranked habits by likely saving

1. `/clear` between unrelated tasks; keep sessions short. Long context is re-read every turn.
2. Keep the cache warm: pick model and effort at the start, no mid-task model, MCP or plugin toggles, use 1h TTL if you idle.
3. Push verbose work (tests, logs, docs, wide search) into subagents or forks on a cheaper model; return summaries.
4. Filter tool output at the source: grep, `head`, test failures only, hooks that trim Bash output.
5. Read narrowly: grep or LSP first, then ranged reads, never whole large files.
6. Shrink always-on context: CLAUDE.md under 200 lines, details in skills, defer or drop MCP servers, prefer CLIs.
7. Match model and effort to the step; Haiku or low effort for mechanical steps.
8. Compact at breaks with focus instructions; rewind instead of compacting a dead end.
9. Specific prompts and plan mode to avoid wrong-path rework.
10. Terse output style: real but small (about 8 to 10% in the one independent test).

## Open questions

- No independent before/after for grep-plus-range versus full reads. Tokenwright could measure it.
- JetBrains' original report was not found. Need the primary source before quoting 8.5%.
- Batch request cap (10k vs 100k) conflicts across sources.
- Programmatic tool calling 37% figure not seen in Anthropic's own text.
- Does the 1h TTL pay off for typical Claude Code use on API keys? Break-even depends on idle pattern.
- Codex, Cursor and Copilot claims here come from third-party guides; check their official docs.
- Real cost of a subagent's startup (system prompt, CLAUDE.md, tools) versus the context it saves.
