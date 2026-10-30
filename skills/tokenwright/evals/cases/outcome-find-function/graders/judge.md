---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- the answer is 17
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: 17 (return round(demand * lead_days + safety + 17, 2)).
