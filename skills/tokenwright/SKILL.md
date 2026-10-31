---
name: tokenwright
description: Spend fewer tokens on the same result in any agent work. Habits by family (don't load or reload data, shortcut the process, script repeats) and tw.py (skip unchanged re-reads with a diff, rank a session's token sinks, cost a skill). Use on 'save tokens', 'this is expensive', 'context is filling', 'why did that cost so much', 'score this session', 'did the file change'. One skill's cost: tokenwright-skills; the catalog: tokenwright-catalog; scripting: tokenwright-script.
license: MIT
metadata:
  version: 0.2.1
---

# tokenwright

Every token that enters the context is paid again, as cache read, on each later turn until compaction or `/clear`. A 3,000-token file read at turn 20 of a 400-turn session costs about 1.1M cache-read tokens. So the cheapest token is the one never loaded, and early waste costs most.

Scripts: `python scripts/tw.py <command>` (standard library, Python 3.9+). Path is relative to this skill's folder.

## Method: find the bottleneck first

1. Measure: `tw.py score` (newest transcript) or `tw.py score <file.jsonl>`. It ranks sinks by carried cost and names the fix.
2. Fix the largest sink only. Savings elsewhere do little while one sink dominates.
3. If the same sink comes back across sessions, make the fix structural: a script (tokenwright-script), a hook (`hooks/`), or a skill change (tokenwright-skills).
4. Measure again.

Never cut a check that prevents a retry: a failed attempt costs more than the check.

## The habits, by family

Read [references/habits.md](references/habits.md) for each habit's when, how and measured saving. The short form:

**1. Don't load or reload data**
- Search, then read a range: `Grep -n` (with `-C 3`), then Read with offset and limit. Read whole only to edit much of a file or when it is short (under about 200 lines).
- Don't re-read after your own Edit: the tool errors if it failed. Re-read only the changed range if you must.
- Before re-reading to check for changes, run `tw.py changed <paths>`: unchanged files cost one line, changed ones only their diff. `git diff --stat` does the same inside a repo.
- Trim command output at the source: `head`, `tail -n`, `--stat`, `-q`, `--oneline`, Grep `head_limit` and `files_with_matches`, `jq` field picks.
- Outline before sections: headings, `grep -n '^#'`, symbol lists, then one section (readwright for books and PDFs).
- Shrink images before reading them; one 1568 px image is about 1,600 tokens.
- Send big mechanical reads (logs, long diffs, many files) to a subagent or local-delegate so only the answer returns.

**2. Shortcut the whole process**
- Stop when the answer is known. Skip steps that cannot change it.
- Answer from what is already in context, a cache, an index or a map (CODEMAP, INDEX.md) before exploring.
- Ask one question instead of exploring a fork the user can settle in a word.
- Batch independent calls in one turn; each turn re-sends the whole context.
- Pick the smallest model and effort that does the step (Haiku or a local model for mechanical work).

**3. Script a process that repeats**
- When a multi-step job recurs (`tw.py repeats` finds them across sessions), a script does the steps and prints only what the agent must judge. See tokenwright-script.

**4. Script what you solved the first time**
- After working something out, save the commands that worked as a script with a dry run, so the next run is one command, not a session. See tokenwright-script.

**Output side**: say it once, short. No recap of what the user can see, no file dumps in replies. Output tokens cost about five times input.

## Waste vocabulary

The report names each sink by its kind of waste, after lean manufacturing ([references/waste-vocabulary.md](references/waste-vocabulary.md)): transport (data moved into context unused), motion (the same thing read twice), defects (retries), overproduction (output nobody reads), inventory (loaded but never used), waiting (serial turns that could be one), overprocessing (work past what the answer needs).

## tw.py commands

| Command | Use |
|---|---|
| `changed <paths> [--quiet]` | Before a re-read. Prints `unchanged` or a diff. First call stores a snapshot in `.tokenwright/snapshots` |
| `score [transcript] [--json]` | After a session or when it felt expensive. Ranks sinks by carried cost |
| `repeats [transcripts] [--last N]` | Find command sequences repeated across sessions: script candidates |
| `skill <dir>` | Cost of a skill or plugin: always loaded, on trigger, on demand |
| `estimate <paths>` | Rough tokens of files before loading them |
| `catalog <tidy args>` | The whole skill catalog: forwards to tokenwright-catalog's tidy.py |

Token counts are estimates (characters / 4). Use them to rank, not to bill. For exact counts use the API's token counting endpoint.

## Claude Code levers

See [references/levers.md](references/levers.md): prompt cache and its TTL, `/compact` and `/clear`, `/context`, deferred tools, skills' progressive loading, subagents and forks, effort, output limits, hooks, model per task.

## Hooks (off by default)

`hooks/hooks.json` warns on a whole read of a large file and on very large tool output. They do nothing until `TOKENWRIGHT_HOOKS=warn` (or `block`, which denies whole reads of large files) is set in the environment.

## Neighbours

tokenwright-catalog (formerly skill-tidy) lints, de-conflicts and parks the skill catalog (`tw.py catalog`); context-health watches a session's context; local-delegate sends mechanical reads to a local model; readwright reads documents by outline; evergreen-wrapup calls `tw.py score` for its token sinks. Link to them, don't copy them.
