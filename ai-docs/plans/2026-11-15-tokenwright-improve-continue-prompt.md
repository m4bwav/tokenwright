# Continue prompt: tokenwright improvement grind

Start a session in the tokenwright clone with:

```
Execute <tokenwright clone>/ai-docs/plans/2026-11-15-tokenwright-improve-continue-prompt.md
```

`<tokenwright clone>` stands for the clone's absolute path. This repository is public, so the path is never written here. This file does not change between sessions. State lives in `ai-docs/HANDOFF.md` and the grind ledger.

## Goal

Find out whether tokenwright can save more tokens for the same result, and prove each change. Every session researches, studies, suggests and tests. An idea ships only after a test shows it helps. An idea that fails its test is recorded as ruled out with its numbers, so no session tests it twice. Cutting a part that tests show does nothing counts as an improvement.

## The three skills that run this chain

- chainwright: session rules (own worktree and branch, facts to the shared log, hand-over order). Read its SKILL.md before anything else.
- grindwright: the ledger and the loop (`grw.py`). It picks the next item, so a wait on the owner closes one lane and never the session.
- askwright: every question for the owner goes on a decision page (`ask.py`) with a real guess. Other work carries on.

Read when their step comes: evergreen-refresh, evergreen-test, evergreen-tune, evergreen-worth, everscout-scan, releasewright, wikiwright.

## Load state (read, do not redo)

1. `AGENTS.md`, then `ai-docs/HANDOFF.md` and the newest entries of `ai-docs/log.md`. Compare HANDOFF's age with `git log` and the tags, and trust the newer evidence.
2. `ai-docs/INDEX.md`. Open only what matches the item in hand. The improvement study and its seed list are under `ai-docs/research/`.
3. Both `evergreen.json` files: due dates, failing or blocked tests, volatile claims.
4. Grind state: `projects/tokenwright/private/grind` in the everlast vault, passed to `grw.py` as `--state`. It stays out of this repository because ledger evidence can name private sessions. If there is no `profile.json` there, set up once as grindwright says (init, profile, road, doctor, plan), starting from the draft in the study note, and put the road to the owner on one askwright page. Until the road is confirmed, take only work every road includes: failing tests, bugs, overdue refreshes, a yellow or red budget, stale docs.

## The loop

`grw.py session start`, then `grw.py next --claim`, until `grw.py session check` allows stopping. The owner's answers and notes come first. Four lanes feed each other.

1. Research: what is new outside. Sources: Claude Code and API docs and changelogs, the docs of other agents (Codex, Copilot, Cursor, Gemini CLI), the everscout beat `token-saving`, the technique-harvest targets in `skills/tokenwright/harvest.json`, other token tools, the book list in `ai-docs/research/books.md`. A claim that will ship needs a primary source. Each finding gets an R- entry and, when it suggests a change, a ledger item.
2. Study: how the plugin does in real use. `tw.py score` and `tw.py repeats` over recent sessions, `tw.py catalog usage` and `tw.py catalog harvest` for firing and missed invocations, `tw.py note` lines and meter notes in transcripts, the eval record in both TESTS.md files, both LEARNINGS.md files, open issues, `scripts/budget.py`. Two questions: which sinks keep coming back that no habit, score kind or hook catches, and which parts of the plugin never fire or never change what the agent does.
3. Suggest: every candidate is a ledger item with its source, the expected saving (measured, or labelled an estimate), what it adds to the plugin's own budget, and the cheapest test that could prove it wrong.
4. Test: start on the lowest rung that can prove the idea wrong, and climb only while it survives.
   - A unit test with a synthetic transcript. Always, for code.
   - A scan over real local transcripts: how often does the pattern occur, and what would the change have saved? A rare pattern is ruled out.
   - `claude plugin eval` with and without the plugin. Commands are in AGENTS.md. Cases that need Bash run in WSL.
   - evergreen-worth, for the with-versus-without verdict on a whole skill.
   - Live use over several sessions, read back from transcripts by a later session. Record in HANDOFF what to look for and from which date.

Then record the run (a T- entry) and the verdict: ship, rule out (an R- entry with the numbers), or ask.

Ship means: failing test first, the change, a CHANGELOG entry with its reason, budget green, then merge and release as AGENTS.md and the owner's standing rules say. Update the installed plugin and the wiki after a release.

## Rules for the session itself

- Batches go to subagents: a research sweep, a transcript scan, an eval run. Hand over data as a file path and keep only the short report. Hand on to the next session when context runs low, not after each batch.
- Real transcripts are read on this machine only. Counts and aggregates may enter the repository. Transcript content, session names and local paths may not.
- Practise the plugin. Before hand-over run `tw.py score` on this session. A sink it finds is a study finding and goes in the ledger. Write `tw.py note` when tokenwright changed what you did.
- Small rulings are decided and flagged in one line. Work found and left for later goes in with `grw.py add`, not only in HANDOFF.

## Stop points (ask the owner, on an askwright page)

- Removing or renaming a skill, a `tw.py` or `tidy.py` command, or the plugin. Cutting one habit row or one reference section after a failed test is a small ruling.
- Turning hooks on by default, or changing what `block` denies.
- Editing settings, hooks or environment variables outside this repository.
- Any change to another plugin's repository beyond opening a pull request there.
- Forum posts, directory submissions and publishing to a package registry.
- Running this chain unattended. It needs hours and a budget agreed by the owner and recorded in HANDOFF.md first.
- Anything that needs a second person's transcripts or data.

## Stop early

Stop when HANDOFF.md says `Status: finished`, or when `grw.py session check` shows that everything left waits on the owner and one discovery pass (a research sweep and a study pass) found nothing above the value floor. Say what waits and where the page is. Never fill an unanswered question with its guess.

## Hand-over

In this order, as chainwright says:

1. `grw.py session end --lesson "<plugin>: <lesson> -> <where>"`.
2. The wrap-up (evergreen-wrapup; skip quietly if absent, report a failure but do not let it block).
3. A log entry in `ai-docs/log.md` and a rewrite of `ai-docs/HANDOFF.md`: state, open askwright sets, live-use checks in flight, what waits on the owner. Keep it short. Regenerate `ai-docs/INDEX.md` when a file was added.
4. Merge the session's pull request once checks pass and remove the session's worktree.
5. Only then print the same start command, with `<tokenwright clone>` replaced by the clone's absolute path:

```
Execute <tokenwright clone>/ai-docs/plans/2026-11-15-tokenwright-improve-continue-prompt.md
```
