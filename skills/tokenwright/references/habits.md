# Habits catalogue

Each habit: when it applies, how, and the saving. "Measured" numbers come from `evals/` in this repository or from the source named; "estimate" means arithmetic from sizes, not a run. Carried cost = tokens × later turns, paid as cache read.

## Family 1: don't load or reload data

| Habit | When | How | Saving |
|---|---|---|---|
| Search, then ranged read | You need a few lines of a file over about 200 lines | `Grep -n -C 3 pattern file`, then Read `offset`/`limit` | Measured payload (fixture `inventory.py`, 2,690 lines): about 21,400 tokens whole, 56 for `grep -n -A4` of the function. A 4,000-line log: about 61,600 whole (past the Read cap), under 50 for `grep ERROR \| sort \| uniq -c` |
| No re-read after own edit | Right after Edit or Write | Trust the tool; it errors on failure | The whole file each time |
| Skip unchanged re-reads | Checking whether a file you read earlier changed (another process, a build, the user) | `tw.py changed <paths>`; in a repo `git diff --stat` | Unchanged: one line. Changed: diff only |
| Trim output at the source | Any command that can print a lot | `head`, `tail -n 40`, `--stat`, `--oneline`, `-q`, Grep `head_limit`, `files_with_matches`, `jq '.field'` | Bash caps at 30k chars; trimming keeps it near the few hundred you need |
| Outline first | Long documents, books, big code files | Headings (`grep -n '^#'`), a symbol list, a TOC; readwright for books and PDFs | Most of the document never loads |
| Small images | Reading screenshots, renders, contact sheets | Resize to the size you need; crop to the region | About 1,600 tokens per full image |
| Delegate big reads | Logs, long diffs, many-file sweeps where you need a conclusion | A subagent (Explore, or a Haiku one) or local-delegate | The sweep's tokens stay out of the main context |
| Don't paste what a file already holds | Writing a report or handing work over | Name the path | Output and later input |

## Family 2: shortcut the whole process

| Habit | When | How |
|---|---|---|
| Stop when the answer is known | Mid-exploration | Act; don't confirm what the evidence already settles |
| Answer from what you have | The fact is in context, an index, a CODEMAP, a cache | Look there before searching |
| Ask one question | A fork the user settles in a word | Ask before exploring both branches |
| Batch independent calls | Several reads or commands that don't depend on each other | One turn, many calls; each turn re-sends the context |
| `/clear` between unrelated tasks | A new task | Free; the largest saving there is |
| Keep the cache warm | Long task | Don't switch model, fast mode or plugins mid-task |
| Right-size the model | Mechanical steps | Haiku, a local model, or lower effort |
| Check cheaply before an expensive step | Before a long render, a big generation, a slow test suite | A dry run or a probe that can fail fast |

## Family 3: script a process that repeats

When the same multi-step job comes back (`tw.py repeats` lists command sequences seen in several sessions), write a script that runs the steps and prints only what needs judgement: a pass or fail line, a short table, the one number. The agent reads ten lines instead of re-deriving the job. Procedure: tokenwright-script.

## Family 4: script what you solved the first time

The first run of a fiddly job (a release, a migration, a data fix) is exploration. Once it works, save the commands that worked, with a dry run and a check, beside the project, and note the script in the docs the next session reads. Next time it costs one command. Procedure: tokenwright-script.

## Output side

- Say it once. No recap of tool output the user can see, no summary of a diff they will read.
- Short plain answers. Output tokens cost about five times input.
- Don't ask a model to "be brief" by a style gimmick; just don't pad. Measured gimmicks saved under 10%.

## Measuring

- `tw.py score` on the session that felt expensive. The carried column shows how much each early sink cost later.
- Compare two runs of the same task with and without a habit; see `evals/` for the method.

## Reported in the field (community reports, not verified here)

From the everscout `token-saving` beat's first scan, 2026-10-30. Single-author figures; treat as leads, not measurements.

| Habit | Reported result | Source |
|---|---|---|
| Route mechanical code writing to a cheap model behind a test gate; the strong model plans | 55 to 63% fewer strong-model tokens; one fewer hard bug solved of 9 | reddit.com/r/ClaudeCode/comments/1xjqoi0 |
| Effort per task: low for routine, high for hard, never max by default | max changed a median 664 lines vs 140 at high and solved less; Sonnet low solved 88% at $0.31 a run vs Opus default 88% at $1.07 | reddit.com/r/ClaudeCode/comments/1xjl3dv |
| Lean headless `claude -p`: `--tools ""`, `--strict-mcp-config`, `--setting-sources ""`, `--no-session-persistence`, a temp working dir, a small model, results cached by input hash | Faster and smaller; no token numbers | reddit.com/r/ClaudeAI/comments/1xjg504 |
| Let a script or template produce deterministic output instead of the model writing it | 80 to 115x fewer output tokens ($0.16 vs $6.60 to $9.20) | reddit.com/r/ClaudeCode/comments/1xjcmdd |
| Turn off MCP servers the task does not need; a skill costs 100 to 200 tokens listed, an MCP server tens of thousands | Poster's figures | reddit.com/r/ChatGPTCoding/comments/1xexygi |
| A hook that denies a repeated identical call or a call past a spend cap | Stops loops early | reddit.com/r/cursor/comments/1xjdzwa |
| Check usage after an upgrade: a vendor change tripled per-request context in one tool | 3 calls of about 150k tokens for a two-file question | forum.cursor.com/t/176786 |
