# Session transcripts in other agents (Codex, Copilot, Cursor, Gemini CLI)

Checked 2026-11-15. Question: can `tw.py score` and `repeats` read sessions from agents other than Claude Code?
Local evidence comes from one Windows machine. Only file counts and key names were read, never content.
"Secondary" means a third-party source. Confirm those against official docs before relying on them.

## OpenAI Codex CLI

- Path: `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl`. `CODEX_HOME` defaults to `~/.codex` on all OSes. Archived rollouts go to `archived_sessions/`. A `state_*.sqlite` index sits alongside.
- Seen locally: 3 rollout files, all compressed as `.jsonl.zst`. They read with `zstd -dc`. Python has no stdlib zstd before 3.14 (`compression.zstd`). A parser must call the `zstd` binary or skip these files.
- Format: JSONL. Each line has `timestamp`, `type` and `payload`.
  - Line types seen: `session_meta`, `turn_context`, `response_item`, `event_msg`, `token_usage_record`, `world_state` and `inter_agent_communication_metadata`.
  - `response_item` payload types seen: `message`, `reasoning`, `function_call`, `function_call_output`, `custom_tool_call`, `custom_tool_call_output`, `agent_message` and `additional_tools`.
  - Tool calls carry `name`, `arguments` and `call_id`. Tool outputs carry `call_id` and `output`. The output's size is its length.
  - Usage comes in `event_msg` lines with payload type `token_count`. `payload.info` holds `total_token_usage`, `last_token_usage` and `model_context_window`. The usage keys are `input_tokens`, `cached_input_tokens`, `cache_write_input_tokens`, `output_tokens`, `reasoning_output_tokens` and `total_tokens`.
- Skills and hooks: Codex reads `AGENTS.md` and `SKILL.md` folders (`~/.agents/skills`, `.agents/skills`). It also has a hooks config. This comes from the developers.openai.com Codex skills and hooks pages, which were not re-fetched in this check. Verify before relying on it.
- Sources (secondary): [rollout format](https://codex.danielvaughan.com/2026/06/01/codex-cli-session-history-local-search-rollout-format-knowledge-mining/), [session management](https://codex.danielvaughan.com/2026/04/13/codex-cli-session-management-resume-fork-transcripts), [issue 24948 on large rollouts](https://upd.dev/openai/codex/issues/24948). The primary source to read next is the openai/codex repository, `codex-rs/protocol`.

## GitHub Copilot CLI

- Path: `~/.copilot/session-state/<sessionId>/events.jsonl`. The CLI uses the first of `--config-dir`, `COPILOT_HOME`, then `~/.copilot`. This is the same on all OSes.
- Seen locally: 34 `events.jsonl` files.
- Format: JSONL. Each line has `id`, `parentId`, `timestamp`, `type` and `data`.
  - Messages: `user.message` keeps its text in `data.content`. `assistant.message` carries `data.content`, `model` and `toolRequests`.
  - Tools: `tool.execution_start` carries `toolCallId`, `toolName` and `arguments`. `tool.execution_complete` carries `toolCallId`, `success`, `result.content` and `result.detailedContent`.
  - Usage: there is one `session.usage_record` per model call. `data.usage` holds `inputTokens`, `outputTokens`, `cacheReadTokens`, `cacheWriteTokens`, `reasoningTokens`, `model`, `cost`, `duration` and `numToolCalls`.
  - Also seen: `hook.start`, `hook.end`, `permission.requested`, `assistant.turn_start` and `assistant.turn_end`.
- Skills: `~/.copilot/skills/<name>/SKILL.md`, plus project skills. Hooks: `.github/hooks/`, `~/.copilot/hooks/`, or the `hooks` key in `~/.copilot/settings.json`.
- Source (official): [Copilot CLI config dir reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference).

## GitHub Copilot in VS Code (agent mode)

- Path: `<VS Code user dir>/workspaceStorage/<hash>/chatSessions/*.jsonl`. The user dir is `%APPDATA%/Code/User` on Windows, `~/Library/Application Support/Code/User` on macOS and `~/.config/Code/User` on Linux.
- Seen locally: 53 files across 17 workspaces. Each line has `kind` and `v`. The first line's `v` holds `sessionId`, `creationDate`, `requests`, `version` and more. Later lines look like patches to that object.
- No token usage field was seen. Tool sizes would have to come from the responses inside `requests`. A parser is feasible, but the format is internal and undocumented.
- Skills: VS Code reads `AGENTS.md`, `.github/copilot-instructions.md` and agent skills. Check the current skill paths in the VS Code docs.

## Cursor (agent and CLI)

- Path (secondary, not confirmed in official docs): `~/.cursor/projects/<project-slug>/agent-transcripts/<session-id>/<session-id>.jsonl`.
- The official CLI changelog confirms an `agent-transcripts/<parent>/subagents/` folder. It also confirms that hooks receive the file as `transcript_path` and `CURSOR_TRANSCRIPT_PATH`. The editor keeps its chats in a SQLite `state.vscdb`.
- Seen locally: there is no `~/.cursor` folder, so no example exists.
- Token usage fields: unknown. A forum thread asks for richer transcripts, which suggests the transcripts carry no token counts.
- Skills: Cursor reads `.cursor/skills/`, `.agents/skills/` and `~/.agents/skills/`. It also reads `.claude/skills/` and `.codex/skills/`. Hooks are configured in `.cursor/hooks.json`.
- Sources: [Cursor skills docs](https://cursor.com/docs/skills) (official), [Cursor CLI changelog](https://cursor.com/docs/cli/changelog) (official), [forum thread on transcripts](https://forum.cursor.com/t/richer-agent-transcripts-lifecycle-data-for-observability-langfuse-stop-hooks/166592).

## Gemini CLI

- Path: `~/.gemini/tmp/<project>/chats/`. `<project>` is a hash or a short name. The chats are `session-<date>-<id>.jsonl` files plus one subfolder per session. A `logs.json` sits beside the `chats` folder.
- Sessions are deleted after 30 days by default (`general.sessionRetention.maxAge`). No home-directory override was confirmed.
- Seen locally: 3 JSONL chat files.
- Format: JSONL.
  - The first line is a header with `sessionId`, `projectHash`, `startTime`, `lastUpdated` and `kind`.
  - Message lines carry `id`, `timestamp`, `type` and `content`. Model lines add `model`, `thoughts`, `tokens` and sometimes `toolCalls`.
  - `tokens` holds `input`, `output`, `cached`, `thoughts`, `tool` and `total`.
  - Some lines are patch operations: `$set`, `$patch` or `$rewindTo`. A parser must skip or apply them.
- Skills and hooks: the `gemini skills` command manages skills. Extensions bundle skills, MCP servers and hooks. Hooks switch on with `hooksConfig.enabled`.
- Sources: [core concepts](https://geminicli.com/docs/core/concepts) and [commands](https://geminicli.com/docs/reference/commands) (official), [sessions page mirror](https://www.mintlify.com/google-gemini/gemini-cli/cli/sessions) (secondary).

## Support table

| agent | sessions readable by score | token usage recorded | skills load | hooks | evidence |
|---|---|---|---|---|---|
| Codex CLI | feasible (needs zstd for .zst) | yes, incl. cached and reasoning | yes | yes (verify) | 3 local files, secondary docs |
| Copilot CLI | feasible | yes, per call, richest of all | yes | yes | 34 local files, official docs |
| Copilot VS Code | feasible, undocumented | not seen | yes | partly | 53 local files |
| Cursor | feasible on paper | unknown | yes | yes | no local data, official skills docs |
| Gemini CLI | feasible | yes, per model message | yes | yes | 3 local files, official docs |

## Synthetic fixture shapes (key names only)

Copilot CLI `events.jsonl`, one object per line:

- `{id, parentId, timestamp, type:"user.message", data:{content}}`
- `{..., type:"assistant.message", data:{content, model, toolRequests:[]}}`
- `{..., type:"tool.execution_start", data:{toolCallId, toolName, arguments}}`
- `{..., type:"tool.execution_complete", data:{toolCallId, success, result:{content, detailedContent}}}`
- `{..., type:"session.usage_record", data:{usage:{model, inputTokens, outputTokens, cacheReadTokens, cacheWriteTokens, reasoningTokens}}}`

Gemini CLI chat JSONL:

- `{sessionId, projectHash, startTime, lastUpdated, kind}`
- `{id, timestamp, type:"user", content}`
- `{id, timestamp, type:"gemini", content, model, thoughts, tokens:{input, output, cached, thoughts, tool, total}, toolCalls:[]}`
- `{"$set": {...}}`. Ignore it.

The `type` values "user" and "gemini" are an assumption. Confirm them in the gemini-cli source before writing a test.

Codex rollout JSONL, after decompression:

- `{timestamp, type:"session_meta", payload:{}}`
- `{timestamp, type:"response_item", payload:{type:"message", role, content:[]}}`
- `{..., payload:{type:"function_call", name, arguments, call_id}}` and `{..., payload:{type:"function_call_output", call_id, output}}`
- `{..., type:"event_msg", payload:{type:"token_count", info:{total_token_usage:{input_tokens, cached_input_tokens, output_tokens, reasoning_output_tokens, total_tokens}, last_token_usage:{}}}}`
