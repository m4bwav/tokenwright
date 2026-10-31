# Decision: fold skill-tidy in as tokenwright-catalog (2026-10-30)

The maintainer approved the fold the same day the question came up.

- A fourth skill, not a merge into tokenwright-skills: one skill's review and the whole catalog's work have different triggers. Cost: descriptions total about 1,920 characters (budget yellow, over the 1,500 green line). That is still less than the about 2,400 users paid with skill-tidy installed beside tokenwright 0.1.0.
- tidy.py moves whole as a second file (`skills/tokenwright-catalog/scripts/tidy.py`). tw.py stays one file; `tw.py catalog` forwards to tidy.py by subprocess.
- Legacy names kept: the `~/.skill-tidy` state folder, `SKILLTIDY_STATE`/`SKILLTIDY_HOME` and the `skill-tidy:parked` markers, so existing parking lots, backups and indexes keep working.
- tokenwright-catalog stays its own evergreen unit, with skill-tidy's RESEARCH, CHANGELOG, LEARNINGS and TESTS carried over unchanged (no renumbering). MAINTENANCE.md switched to the plugin-protocol pointer like the hub's. Its eval cases sit with the hub's cases, renamed trigger-4, trigger-5, decoy-3, decoy-4, action-catalog, outcome-catalog.
- skill-tidy: last release 0.2.5 with a moved notice (the one-version alias). Archiving the repository and withdrawing its Claude directory submission are left to the maintainer.
