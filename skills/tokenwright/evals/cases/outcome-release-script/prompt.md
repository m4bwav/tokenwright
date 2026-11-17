---
runs: 3
max_turns: 20
timeout_seconds: 600
tags: [bash]
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---

We do the release steps in evals/fixtures/release/RELEASING.md by hand every week. Turn them into one script I can run, then run it once for real.
