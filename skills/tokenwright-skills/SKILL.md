---
name: tokenwright-skills
description: Review a skill or plugin for token cost and rank the savings: description length (paid in every session), always-loaded text, references that should load on demand, instructions that should be a script, sweeps a subagent should own, files nothing links to. Runs tw.py skill. Use when writing or reviewing one skill ('is this skill too big', 'make this skill cheaper', 'token cost of my plugin', 'review this SKILL.md for tokens'), and from evergreen-new and evergreen-tune. The whole catalog: tokenwright-catalog.
license: MIT
metadata:
  version: 0.2.0
---

# tokenwright-skills

A skill costs in three tiers. Fix the most-paid tier first.

| Tier | What | Paid |
|---|---|---|
| Always | name + description (cut at 1,536 characters in Claude Code) | Every turn of every session where the skill is installed |
| On trigger | SKILL.md body | Each session that uses it, then carried every later turn |
| On demand | references, scripts' output, kb files | Only when read |

## Steps

1. Measure: `python ../tokenwright/scripts/tw.py skill <skill-or-plugin-dir>`. It prints the three tiers per skill and ranked findings.
2. Walk the checklist below for what the script cannot judge.
3. Report the savings largest first, each with the tokens saved and where they are saved (always, trigger, demand). Weigh "always" savings by how many skills a user has installed; a 100-token cut in a description beats a 1,000-token cut in a reference.
4. Edit only if asked. Never cut a trigger phrase that evals show the skill needs; re-run the trigger evals after a description change.

## Checklist

- **Description**: what it does and when to use it, with the user's trigger phrases. No history, no feature list, no explanation of how. Aim at 300 to 600 characters; past 1,024 some hosts reject it.
- **Rarely used skill**: a slash-command-only skill can set `disable-model-invocation: true` (no description cost), or be parked (tokenwright-catalog). Long sections move with its `split` command.
- **Body**: rules and routing. Procedures, tables and examples move to `references/` with a line saying when to read each. Aim under 200 lines.
- **Code in prose**: a code block the agent retypes, or a numbered procedure it follows step by step every time, should be a script it runs (tokenwright-script). The script's output should be a few lines.
- **Sweeps**: steps that read many files to produce one answer belong in a subagent or `context: fork`, so the reads never reach the main context.
- **Findable files**: every reference should be named in SKILL.md or an index it names. An unlinked file is either dead (delete) or unreachable (link it).
- **Duplication**: text copied from a neighbour skill. Link instead.
- **Model pinning**: a frontmatter model different from the session's breaks the prompt cache for that turn. Pin only when the saving is clear.

See [../tokenwright/references/levers.md](../tokenwright/references/levers.md) for what loads when.
