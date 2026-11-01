---
name: tokenwright-catalog
description: "Cut what the whole skill catalog costs and fix skills that fire on each other's prompts: lint descriptions, explain clashes, split long bodies, park rarely used skills, audit startup files. Use on 'why did the wrong skill fire', 'skills overlap', 'shorten my skill descriptions', 'how many tokens do my skills cost', 'park or unpark a skill', 'trim startup context'."
license: MIT
metadata:
  version: "0.2.9"
---

# tokenwright-catalog

A skill catalog costs tokens every session and, past about 20-30 skills, costs selection accuracy. Overlapping descriptions cost more than raw count, and very large catalogs (about 1,000) make agents stop loading skills at all (RESEARCH.md). This skill finds the problems with a script and fixes them with judgment, one rewrite per skill. It was the skill-tidy plugin before tokenwright 0.2.0.

`TIDY` below means `python "<this folder>/scripts/tidy.py"` (`python3` on macOS and Linux), or `tw.py catalog` from the hub, which forwards to it. Every command takes `--agent claude|codex|copilot|cursor|all` (default claude), `--project PATH` (default cwd) and `--json`. Rules and their evidence: [references/rules.md](references/rules.md).

## Step 0: freshness

Read [evergreen.json](evergreen.json). If `contradiction` is set or today is on or after `next_due`, say so in one line, do the task, then refresh (MAINTENANCE.md). Host limits and settings change monthly.

## Step 1: measure

Run what the request needs, not everything:

- `TIDY conflicts`: pairs at TF-IDF cosine 0.45+ (0.65+ near-duplicate), the words both share, trigger phrases both claim, and a starting boundary sentence for each side.
- `TIDY lint [SKILL_DIR ...]`: rules ST001-ST023; errors are spec or host limits, warnings are research-backed style. Exit code 1 when an error exists.
- `TIDY budget --window <model window>`: listing size against Claude Code's 1% character budget (over it, least-used descriptions are dropped; `SLASH_COMMAND_TOOL_CHAR_BUDGET` fixes it in characters), Codex's 2% / 8,000 chars (`skills.max_context_tokens` overrides it), the 1,536 cut and the spec's 1,024.
- `TIDY usage --days 30`, `TIDY startup`: invocations from transcripts (headless runs shown apart as `+N headless`, never counted as use); the instruction chain, memory and MCP settings.

## Step 2: fix a conflict (no functionality lost)

1. Decide the split in one sentence per skill: each one's job and which user phrasing belongs to which. If the same request should reach both, recommend merging instead of rewording, and stop for the user.
2. `TIDY triggers <skill>` for both. Every trigger's meaning must survive; a phrase may move to the skill that owns it.
3. Optional evidence: `TIDY harvest <skill>` writes a brief with prompts that matched but did not invoke it and invocations that look unrelated.
4. Write ONE rewrite of the weaker or longer description (editing both sides adds under 0.5% in the research). Key use case and trigger words first; what it does plus "Use when"; at most 1,024 chars, about 100-200 words; no steering text; end with one boundary sentence naming the sibling. Keep triggers in `description`, not `when_to_use` (only Claude Code reads that).
5. `TIDY check <skill> --new <file>` must print `OK`: no errors, no lost trigger, closest similarity lower than before. Then `TIDY apply <skill> --new <file>` (backup under `~/.skill-tidy/backups/`). Installed plugin copies are refused: edit the source repository and reinstall. If `apply` cannot write (a read-only sandbox), make the same change with the Edit tool once `check` printed OK.
6. Confirm with `TIDY conflicts`; report before and after scores. Lexical scores are a proxy; for live routing evidence, offer google/skill-reach (`reach eval`), never install it unasked.
7. When rewording cannot separate two installed skills, say so: install location decided the winner more than listing order, and the conflict was settled at the first skill read (arXiv 2610.11647). Offer parking or disabling one (Step 3) before a hook; judge from transcripts, since the reply rarely names the skill that ran.

## Step 3: save tokens

- Never-used skills: `TIDY offload --days 30` prints Claude Code `skillOverrides` "name-only" entries (still invocable, description stops loading), plugin skills to disable per project, and Codex `[[skills.config]] enabled = false` lines. `--write` merges the Claude Code entries into `~/.claude/settings.json` with a backup. Ask first; a monthly skill can look unused over 30 days.
- Long descriptions: shorten the ones `lint` flags ST005/ST006/ST007 with the Step 2 loop.
- Long bodies (ST020): `TIDY sections <skill>` sizes each section and marks supplementary ones. For each one not every run needs, `TIDY split <skill> --section "<heading>" --when "<tasks that need it>"` moves it to `references/<slug>.md` and leaves a `Read <file> when <condition>.` line. Keep references one level deep (ST021). Source folders only. For a single skill's full review use tokenwright-skills.
- Rarely used skills: park them. `TIDY parked suggest` ranks candidates; after the user agrees, `TIDY park <name>` (or `--plugin`, `--soft`, `--scope project`) moves each out of every scanned folder and writes a grouped one-line index into the always-read instruction files, so the agent still finds it. `TIDY unpark <name>` restores it; `TIDY parked doctor` checks the lot and dangling links; `TIDY parked index` rewrites the index (run it after this skill moves). Read [references/parking.md](references/parking.md) before the first park or when asked how parking works.
- Manual-only skills: suggest `disable-model-invocation: true` (no listing cost; `/name` still works). Skills tied to file types: suggest `paths:` globs.
- Startup: `TIDY startup` shows the biggest instruction files and imports, `alwaysLoad` MCP servers and whether tool search is off. Suggest moving rarely needed detail into files loaded on demand. Stale paths and contradicting instruction files: point to Claude Code's `/doctor prompt-audit`.

## Step 4: report

One short list: what changed (file, before and after chars and similarity), what was only suggested, estimated tokens saved per session, what is left for the user. Record a lesson in [LEARNINGS.md](LEARNINGS.md) when a host behaved differently from the rules.

## Maintenance

Evergreen unit: [RESEARCH.md](RESEARCH.md), [CHANGELOG.md](CHANGELOG.md), [LEARNINGS.md](LEARNINGS.md), [TESTS.md](TESTS.md), state in [evergreen.json](evergreen.json), protocol in [MAINTENANCE.md](MAINTENANCE.md). Eval cases sit with the hub's (`../tokenwright/evals/cases`, ids in `evals/evals.json`).
