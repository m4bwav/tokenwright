# Continue prompt: tokenwright

Start a session in the tokenwright clone (`Ai/tokenwright` in the maintainer's projects folder) with:

```
Execute ai-docs/plans/2026-10-30-tokenwright-continue-prompt.md
```

This file does not change between sessions. State lives in `ai-docs/HANDOFF.md`.

## Load state (read, do not redo)

1. `ai-docs/HANDOFF.md` (where things stand, what waits on Mark), then the newest entries of `ai-docs/log.md`.
2. `AGENTS.md` (rules), `ai-docs/decisions/`, and `skills/tokenwright/evergreen.json` (due date, tests, scout link).
3. Research only as needed: `ai-docs/research/` and the book notes `Ai/books/plugin-learnings/tokenwright-lean-goal.md`. The private survey of existing habits is in the everlast vault under `projects/tokenwright/private/`.
4. Skills to read when their step comes: ludowright's repo for release layout, wikiwright for the wiki, evergreen-test and evergreen-tune for evals, everscout-scan for the beat.

## Order of work

1. Anything HANDOFF lists as answered by Mark: act on it first.
2. Publish if not done: public repo `m4bwav/tokenwright`, push, CI green, social preview, topics.
3. Evals: read the latest results, record a T- entry in `skills/tokenwright/TESTS.md` and `evergreen.json.tests`; failing cases go to evergreen-tune (three iterations at most).
4. Fold the everscout `token-saving` beat's findings into `references/habits.md` and `references/levers.md` with sources (R- entries in RESEARCH.md, C- entries in CHANGELOG.md).
5. Books: run the next one or two from `ai-docs/research/books.md` through the book-learnings process.
6. Wiki via wikiwright; then tag and cut the GitHub release (bump all version spots together, see AGENTS.md).
7. Evergreen PR (wrap-up W section): if merged, nothing more; if Mark asks to drop the T section, do that in a new PR.

## Stop points (ask Mark)

- Plugin name change; archiving the skill-tidy repository or withdrawing its Claude directory listing; any evergreen change that removes the wrap-up's own token checks (open the PR, don't merge); any forum posting; publishing to a package registry.

## Hand-over rules

- No AI attribution anywhere. Public repo: no local paths, no names but the author credit, no transcript content.
- Merge your own PRs on tokenwright once checks pass; tag and release yourself once checks pass.
- Before stopping: update `ai-docs/HANDOFF.md`, add a log entry to `ai-docs/log.md`, update the backlog entry in `Ai/plugin-backlog/new-plugins.md`, then end the reply with the same start line:

```
Execute ai-docs/plans/2026-10-30-tokenwright-continue-prompt.md
```

and the folder to start in (the tokenwright clone (`Ai/tokenwright` in the maintainer's projects folder)).
