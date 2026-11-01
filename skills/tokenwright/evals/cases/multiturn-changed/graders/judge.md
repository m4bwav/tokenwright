---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- says REQUEST_TIMEOUT went from 30 to 45
- says FEATURE_0900_ENABLED went from False to True
- names no other change
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: two changes, REQUEST_TIMEOUT 30 -> 45 and FEATURE_0900_ENABLED False -> True.
