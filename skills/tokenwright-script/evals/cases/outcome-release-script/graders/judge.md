---
type: llm
name: 'expectations'
---

PASS if the run meets every one of these:
- CHANGELOG.md has exactly one '## 1.4.3' heading, above '## 1.4.2'
- the script has a dry-run option that changes no file
- the script stops, refuses or is a no-op on a second run in the same state, instead of bumping to 1.4.4 unasked
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
