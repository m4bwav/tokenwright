---
name: tokenwright-script
description: Turn a repeating or already-solved agent process into a script, so the next run is one command: finds candidates (tw.py repeats) and writes the script with inputs, a dry run and idempotence. Use on 'script this', 'we keep doing this', 'make this one command', 'automate what you just did', 'next time this should be quick', or when tokenwright names a repeat.
license: MIT
metadata:
  version: 0.2.12
---

# tokenwright-script

A script pays when a job will run again. The agent's part shrinks to: run it, read a few lines, judge.

## Find the candidate

- **Repeats across sessions**: `python ../tokenwright/scripts/tw.py repeats --last 50` lists command sequences seen in several sessions.
- **Solved once**: the commands that worked in this session. Take them from the transcript, not from memory: the failed attempts are not part of the script.
- Worth it when: the job will run again, it has three or more steps, or its output needs trimming to be read.
- Not worth it when: it is a one-off, or each run needs fresh judgement at every step.

## Write it

Checklist, in order:

1. **Inputs** as arguments, never edited constants. Sensible defaults.
2. **Dry run** (`--dry-run`) that prints what it would do and changes nothing. Make it the default for anything destructive.
3. **Idempotent**: running twice does no harm (check before create, skip what is done).
4. **Fail fast** with one clear line naming what failed and what to check. Non-zero exit code.
5. **Output for the judge**: a few lines: a status, counts, the one number, paths to the full logs. Never the raw log.
6. **Where**: beside the project it serves (`scripts/`), or in the skill that owns the job. Standard library where you can.
7. **Record it** where the next session looks: the project's AGENTS.md commands list, the skill's SKILL.md, or the handoff. A script nobody can find saves nothing.
8. **Run it once for real** and compare the result with the manual run.

Templates: [references/templates.md](references/templates.md) (Python and shell skeletons with the dry run, fail-fast and short-output parts already in place).

## Judge the result, not the steps

The agent reads the script's summary and decides. It reads the full log only when the summary says something failed, and then searches it rather than reading it whole.
