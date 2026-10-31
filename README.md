# tokenwright

![tokenwright banner](.github/images/banner.jpg)

Spend fewer tokens on the same result. A plugin for Claude Code and other agents (Copilot, Codex, Cursor, Gemini CLI read the same skills) that teaches the habits that cut token use, and ships a small CLI that measures where a session's tokens went.

Every token in an agent's context is re-sent on each later turn. A 3,000-token file read early in a 300-turn session is paid for again about 300 times as cache reads. So the cheapest token is the one never loaded, and early waste costs the most.

## What's inside

| Skill | Use it when |
|---|---|
| `tokenwright` | "this is expensive", "context is filling", "why did that cost so much". Habits in four families with measured savings, Claude Code and API levers, a waste vocabulary |
| `tokenwright-script` | A job keeps coming back, or you just solved something fiddly. Turns it into a script with a dry run and a short result |
| `tokenwright-skills` | Writing or reviewing one skill or plugin. Ranks its token savings by where they are paid |
| `tokenwright-catalog` | The wrong skill fires, descriptions overlap, or the whole catalog costs too much. Lints descriptions, checks a rewrite keeps every trigger, splits long bodies, parks rarely used skills, audits startup files. Formerly [skill-tidy](https://github.com/m4bwav/skill-tidy) |

The four families:

1. **Don't load or reload data.** Search then read a range; don't re-read after an edit; skip unchanged re-reads; trim output at the source; outline first; small images; send big sweeps to a subagent.
2. **Shortcut the whole process.** Stop when the answer is known; answer from an index; ask one question; batch calls; `/clear` between tasks; keep the cache warm.
3. **Script a process that repeats.**
4. **Script what you solved the first time.**

## tw.py

Standard-library Python 3.9+, one file: `skills/tokenwright/scripts/tw.py`.

```sh
python tw.py changed src/app.py docs/plan.md   # before a re-read: "unchanged" or just the diff
python tw.py score                             # rank the newest session's token sinks by carried cost
python tw.py repeats --last 50                 # command sequences repeated across sessions
python tw.py skill path/to/plugin              # what each skill costs: always, on trigger, on demand
python tw.py estimate big.log                  # rough tokens before you load something
python tw.py catalog conflicts                 # skills that compete for the same prompts (tidy.py)
```

`tw.py catalog` forwards to `skills/tokenwright-catalog/scripts/tidy.py`, a second standard-library file: `lint`, `conflicts`, `triggers`, `check`, `apply`, `sections`, `split`, `budget`, `usage`, `offload`, `park`, `unpark`, `parked`, `startup`, `harvest`.

Example `score` output on a real 187-turn session: about 28,000 avoidable tokens (files read twice), carried as about 3.3 million cache-read tokens because they entered early.

Measured on the eval fixtures: finding one function in a 2,690-line file costs about 21,400 tokens by a whole read and 56 by `grep -n -A4`. Counting errors in a 4,000-line log costs about 61,600 tokens whole and under 50 with `grep | sort | uniq -c`.

Token counts are estimates (characters / 4). They rank sinks; they do not bill.

## Hooks (off by default)

The plugin installs two hooks that do nothing until you set `TOKENWRIGHT_HOOKS`:

- `warn`: a note to the agent when it reads a large file whole, or a tool returns very large output.
- `block`: also denies whole reads of large files, so the agent searches and reads a range instead.

## Install

```sh
claude plugin marketplace add m4bwav/tokenwright
claude plugin install tokenwright@tokenwright
```

Other agents: copy or link the folders under `skills/` into the agent's skills directory.

Coming from skill-tidy: uninstall it and install tokenwright. Parked skills, backups and the parked index keep working: tidy.py still uses `~/.skill-tidy` and the same index markers. Run `python tw.py catalog parked index` once so the index points at the new tidy.py path.

## Development

```sh
python -m unittest discover -s tests
python scripts/budget.py
```

See [AGENTS.md](AGENTS.md) for the rules. Security: [SECURITY.md](SECURITY.md). License: MIT.
