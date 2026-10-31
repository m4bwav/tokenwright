# AGENTS.md

Rules for any AI agent (Claude Code, Copilot, Cursor, Codex, Gemini CLI) working in this repository. `CLAUDE.md` imports this file and `.github/copilot-instructions.md` points here.

## What this is

tokenwright: a cross-agent plugin for spending fewer tokens on the same result. Four skills under `skills/`: `tokenwright` (the hub: habits catalogue, levers, waste vocabulary in `references/`), `tokenwright-script` (turn a repeating or solved process into a script), `tokenwright-skills` (review one skill for token cost) and `tokenwright-catalog` (the whole catalog: lint and de-conflict descriptions, split bodies, park skills, audit startup; formerly the skill-tidy plugin). `skills/tokenwright-catalog/scripts/tidy.py` is its own standard-library CLI, reached directly or through `tw.py catalog`; it keeps the legacy `~/.skill-tidy` state folder and `skill-tidy:parked` markers so existing parking lots keep working. `skills/tokenwright/scripts/tw.py` is the single standard-library CLI (changed, score, repeats, skill, estimate, catalog, hook). `hooks/hooks.json` wires tw.py's hook mode; it does nothing unless `TOKENWRIGHT_HOOKS` is `warn` or `block`. Evergreen companions sit beside the hub's SKILL.md; eval cases and fixtures in `skills/tokenwright/evals/`. Unit tests in `tests/`; research, decisions, log and handoff under `ai-docs/` (start with `ai-docs/HANDOFF.md`).

## Rules

- The plugin must be cheap itself. `python scripts/budget.py` (red fails CI; tell the maintainer about a yellow in one line). Keep each SKILL.md under 150 lines and each description under 700 characters.
- `tw.py` stays one standard-library Python file (3.9 or newer) for Windows, macOS and Linux, UTF-8 and LF. Every change gets a test in `tests/test_tw.py` with a synthetic transcript; never commit a real transcript. Run `python -m unittest discover -s tests` before committing.
- A saving claimed in the habits catalogue is measured (cite the eval or the source) or labelled an estimate.
- Book ideas are paraphrased with chapter citations; quotes stay under about ten words; no local paths to books.
- The hub is an evergreen unit. Before editing it read `skills/tokenwright/evergreen.json`; if `next_due` has passed or `contradiction` is set, say so and refresh after the task. Log every change in the skill's `CHANGELOG.md` with its reason; lessons go to `LEARNINGS.md`. The everscout beat `token-saving` feeds refreshes as leads.
- A release bumps the version in `.claude-plugin/plugin.json`, `plugin.json`, `VERSION` in `tw.py`, `metadata.version` in each SKILL.md and the CHANGELOG together, then tags `vX.Y.Z` and publishes a GitHub Release.
- tokenwright-catalog is a second evergreen unit with its own companions and `evergreen.json`; its eval cases sit with the hub's in `skills/tokenwright/evals/cases` (trigger-4, trigger-5, decoy-3, decoy-4, action-catalog, outcome-catalog). Changes to tidy.py get a test in `tests/test_tidy.py`.
- Neighbours: context-health, local-delegate, readwright, evergreen-wrapup (calls `tw.py score`). Link, never copy.
- This is a public repository: no person named other than the author credit and published authors, no machine, no absolute local path, no credential, no transcript content. Plain short sentences, no em dashes, relative markdown links, never wikilinks.
- No AI attribution anywhere: no Co-Authored-By trailers, no "generated with" lines in commits, pull requests, releases or files.

## Commands

- Tests: `python -m unittest discover -s tests`
- Budget: `python scripts/budget.py`
- Score the newest session: `python skills/tokenwright/scripts/tw.py score`
- Plugin manifest: `claude plugin validate .`
- Evals: `claude plugin eval . --no-publish --trust-plugin --case "trigger-*"`

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here. Scan it at the start of a task and open only matching entries; read `ai-docs/HANDOFF.md` when continuing unfinished work.
- Before finishing a task that hit a dead end, verified a non-obvious command or made a design choice, record it in `ai-docs/` and rewrite `HANDOFF.md` when work is left unfinished.
