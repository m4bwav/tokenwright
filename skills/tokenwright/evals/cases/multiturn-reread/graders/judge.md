---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- says REQUEST_TIMEOUT is now 45
- says RETRY_LIMIT is still 3 (unchanged)
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: REQUEST_TIMEOUT is 45 (was 30); RETRY_LIMIT is unchanged at 3.
