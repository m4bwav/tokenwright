---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- names 'db pool exhausted' with count 2
- names 'payment timeout' with count 1
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: Two distinct errors: db pool exhausted (max=20) twice, payment timeout order=4417 once.
