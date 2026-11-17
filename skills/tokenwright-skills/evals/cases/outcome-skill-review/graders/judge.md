---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- the description is ranked first or second
- it suggests a script for the manual steps
- notes.md is flagged as unlinked
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: the description is far too long (paid every session) and ranks first; the 30 manual steps and the 40-line code block should be a script; notes.md is unlinked.
