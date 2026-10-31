# GitHub wiki (2026-10-30, tokenwright 0.2.0)

Wiki: https://github.com/m4bwav/tokenwright/wiki. Working copy: sibling clone `tokenwright.wiki` (branch master). Made with wikiwright.

## Pages

Home, Getting-Started, Commands, Hooks, Skills, FAQ, Versions-and-Upgrading, Development, _Sidebar, _Footer. Pages naming the version: Getting-Started (`--version` output), FAQ, Versions-and-Upgrading, _Footer.

## How the examples were verified

`2026-10-30-wiki-verify.py` copies tw.py from tag v0.1.0 (`git show`) into a scratch folder, builds synthetic files, transcripts and a skill, and runs every command the pages show. Output saved in `2026-10-30-wiki-verify.out.txt`. Checks: `wikiwright.py check` 0 errors, `outputs` 12 checked 0 missing, `snippets` 0 missing, `live` 8 pages 0 failures, everwrite tells 0 strong after the fix. Unit tests: 11 pass. Not tested: other agents, hook latency.

## Update for 0.2.0 (2026-10-30)

The script now lays tw.py and tidy.py out as in the plugin (so `tw.py catalog` finds tidy.py). It adds catalog cases (version, conflicts, lint) with two overlapping skills in a throwaway home (`SKILLTIDY_HOME`). diffout against the 0.1.0 output: 1 changed (version), 3 added. Pages changed: Home, Skills, Commands (catalog section), Versions-and-Upgrading, Getting-Started, FAQ, Development, _Footer. check 0 errors (Home has no version: a warning, as before), outputs 14 checked 0 missing, tells 0 strong, live 8 pages 0 failures. The catalog commands that write (apply, park, split) are described from the source and tests, not run by the script.

## Facts the README lacks

- `TOKENWRIGHT_HOOKS=1` or `on` act as `warn`.
- The pre hook threshold is file size over 24,000 bytes (BIG_FILE_LINES*60), not lines; `block` only affects the pre hook.
- `changed` decides by size and mtime, then sha256; files over 2 MB keep no stored copy.
- `repeats` normalises cd prefixes, strings, numbers and paths; only Bash and PowerShell calls.
- `skill` flags: description over 600 chars, body over 500 lines, 25+ line code blocks, 15+ steps without scripts/, unlinked files over 2,000 bytes.

## Inaccuracies and bugs found (fix in 0.1.1)

1. `score` lists a second whole read as both `whole-read` and `repeat read` and sums both, so the avoidable total double counts (tw.py score loop).
2. `changed` reports lines as newlines + 1: a 3-line file with a final newline shows 4 lines.
3. README says hooks fire on "a large file"; it does not say the size is bytes or that `block` leaves the post hook a warning.

## Update procedure

Bump `WIKI_TAG`, run the script, `wikiwright.py diffout` old vs new output, fix differing pages and the pages listed above, then check, outputs, snippets, push, live.
