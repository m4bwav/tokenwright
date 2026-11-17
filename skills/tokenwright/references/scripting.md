# Scripting a repeating or solved job

Loaded on demand from the hub (habits 'script what repeats' and 'script what you solved once'). Was the tokenwright-script skill until 0.4.0; cut after two A/B runs showed no gain (T-20261117-8).

A script pays when a job will run again. The agent's part shrinks to: run it, read a few lines, judge.

## Find the candidate

- **Repeats across sessions**: `python "${CLAUDE_SKILL_DIR}/scripts/tw.py" repeats --last 50` (`python3` on macOS and Linux) lists command sequences seen in several sessions.
- **Solved once**: the commands that worked in this session. Take them from the transcript, not from memory: the failed attempts are not part of the script.
- Worth it when: the job will run again, it has three or more steps, or its output needs trimming to be read.
- Not worth it when: it is a one-off, or each run needs fresh judgement at every step.

## Write it

Checklist, in order:

1. **Inputs** as arguments, never edited constants. Sensible defaults.
2. **Dry run** (`--dry-run`) that prints what it would do and changes nothing. Make it the default for anything destructive.
3. **Idempotent**: running twice does no harm (check before create, skip what is done).
4. **Fail fast** with one clear line naming what failed and what to check. Non-zero exit code. Never catch an error and print success: an agent that cannot see the failure may call the tool again and again, paying for each try.
5. **Output for the judge**: a few lines: a status, counts, the one number, paths to the full logs. Never the raw log.
6. **Where**: beside the project it serves (`scripts/`), or in the skill that owns the job. Standard library where you can.
7. **Record it** where the next session looks: the project's AGENTS.md commands list, the skill's SKILL.md, or the handoff. A script nobody can find saves nothing.
8. **Run it once for real** and compare the result with the manual run.

Templates: [script-templates.md](script-templates.md) (Python and shell skeletons with the dry run, fail-fast and short-output parts already in place).

## Judge the result, not the steps

The agent reads the script's summary and decides. It reads the full log only when the summary says something failed, and then searches it rather than reading it whole.
